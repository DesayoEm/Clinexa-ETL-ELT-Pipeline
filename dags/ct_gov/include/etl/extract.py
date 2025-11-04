
import requests
import io
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from typing import Dict

from ct_gov.include.config import config
from ct_gov.include.notification_middleware.extractor_middleware import (
    persist_extraction_state_before_exit, persist_extraction_state_before_failure
)

from ct_gov.include.handlers.rate_limit_handler import RateLimiterHandler
from ct_gov.include.handlers.s3_handler import S3Handler
from ct_gov.include.tests.extractor_stress_test import FailureGenerator
from ct_gov.include.exceptions import RequestTimeoutError

from airflow.utils.log.logging_mixin import LoggingMixin
log = LoggingMixin().log


log = LoggingMixin().log


class Extractor:
    def __init__(
            self,
            context: Dict,
            destination: str,
            s3_hook,
            timeout: int = 30,
            max_retries: int = 3
        ):
        self.starting_point = self.determine_starting_point(context)
        self.last_saved_page = self.starting_point['last_saved_page']
        self.current_page = self.last_saved_page if self.last_saved_page else 0

        # technically current page should be  last saved + 1 but the val is incremented
        # by one in the make_requests func so no need to do it here

        self.last_saved_token = self.starting_point['last_saved_token']
        self.next_page_url = self.starting_point['next_page_url']

        self.timeout = timeout
        self.max_retries = max_retries

        self.failure_generator = FailureGenerator(True, 0.5)
        self.rate_limit_handler = RateLimiterHandler()
        self.context = context

        self.s3 = s3_hook
        self.bucket_destination = destination



        log.info(
            f"Initializing Extractor... \n"
            f"\n Last saved is page {self.last_saved_page}"
            f"\n URL to extract is {self.next_page_url}"

            )


    @staticmethod
    def determine_starting_point(context: Dict):
        log.info(f"Determining starting point for extractor...")

        ti = context['task_instance']
        if not ti:
            log.warning("No task instance found in context, starting fresh")
            return {
                'last_saved_page': 0,
                'last_saved_token': None,
                'next_page_url': config.FIRST_PAGE_URL
            }

        states = ti.xcom_pull(
            task_ids=ti.task_id,
            key="previous_states",
            include_prior_dates=False,
        )

        if states and isinstance(states, list) and len(states) > 0:
            state = states[0]

            if (state.get('pages_loaded') is not None and
                    state.get('last_saved_token') is not None and
                    state.get('run_state') != 'FAILED'):

                log.info(f"Valid existing context found from last run: {state} \n \n")
                return {
                    'last_saved_page': state['pages_loaded'],
                    'last_saved_token': state['last_saved_token'],
                    'next_page_url': f"{config.BASE_URL}{state['last_saved_token']}"
                }
            else:
                log.info(f"Invalid or incomplete state found, starting fresh: {state} \n \n")


        log.info(f"No valid context found from previous run, starting fresh... \n \n")
        return {
            'last_saved_page': 0,
            'last_saved_token': None,
            'next_page_url': config.FIRST_PAGE_URL
        }




    def make_requests(self):
        while self.current_page < 10:
            try:
                url = self.next_page_url

                self.current_page += 1
                log.info(f"Starting from page {self.current_page}")

                self.rate_limit_handler.wait_if_needed()

                for attempt in range(self.max_retries):
                    response = requests.get(url, timeout=self.timeout)
                    attempt += 1
                    log.info(f"Starting from page {self.current_page}, attempt {attempt}")
                    if response.status_code == 200:
                        data = response.json()
                        self.save_response(data, self.bucket_destination)

                        next_page_token = data.get("nextPageToken")
                        break

                    elif attempt >= self.max_retries and response.status_code != 200:
                        log.error(
                            f"Request exception FAILED AFTER 3 attempts on page {self.current_page}"
                        )

                        persist_extraction_state_before_failure(
                            error=RequestTimeoutError,
                            context=self.context,
                            metadata={
                                'pages_loaded': self.last_saved_page,
                                'last_saved_token': self.last_saved_token,
                                'next_page_url': self.next_page_url,
                                'date': self.context["ds"]
                            }

                        )

                if not next_page_token:
                    log.info(
                    f"Next page not found on page {self.current_page}"
                    f"Check metadata for the token for this page")

                    metadata = {
                        'pages_loaded': self.last_saved_page,
                        'last_saved_token': self.last_saved_token,
                        'next_page_url': self.next_page_url,
                        'date': self.context["ds"]
                    }
                    persist_extraction_state_before_exit(self.context, metadata)


                # if self.current_page == 10:
                #     self.failure_generator.maybe_fail_extraction(self.current_page)

                self.last_saved_token = next_page_token
                self.next_page_url = f"{config.BASE_URL}{next_page_token}"


                log.info(
                    f'Successfully made request to {self.next_page_url} \n Last loaded page is page {self.current_page}'
                     f'\n Next page is {self.next_page_url}'
                    )



            except Exception as e:
                persist_extraction_state_before_failure(
                    error = e,
                    context=self.context,
                    metadata={
                        'last_saved_page': self.last_saved_page,
                        'last_saved_token': self.last_saved_token,
                        'next_page_url': self.next_page_url,
                        'date': self.context["ds"]
                        },
                    )

        metadata = {
            'pages_loaded': self.last_saved_page,
            'last_saved_token': self.last_saved_token,
            'next_page_url': self.next_page_url,
            'date': self.context["ds"]
        }
        persist_extraction_state_before_exit(self.context, metadata)


    def save_response(self, data: Dict, bucket_destination: str):
        df = pd.DataFrame(data)
        table = pa.Table.from_pandas(df)

        buffer = io.BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0)

        parts = bucket_destination.split("/", 1)
        bucket_name = parts[0]
        prefix = parts[1]

        key = f"{prefix}/{self.current_page}.parquet"

        self.s3.load_bytes(
            bytes_data=buffer.getvalue(),
            key=key,
            bucket_name=bucket_name,
            replace=True
        )

        log.info(
            f"Successfully saved page {self.last_saved_page} at s3://{bucket_name}/{key}"
        )
