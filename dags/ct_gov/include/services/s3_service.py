from typing import Dict
from datetime import datetime
import boto3
import os
from airflow.utils.log.logging_mixin import LoggingMixin
# from dags.ct_gov.include.config import config
from ct_gov.include.config import config
from ct_gov.include.services.middleware import persist_state_before_failure


log = LoggingMixin().log


class S3Service:
    def __init__(self, context: Dict):
        self.client = boto3.client(
            's3',
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION,
        )
        self.context = context


    def create_folder(self, bucket: str):
        exec_date = self.context["execution_date"]
        folder_name = f"{exec_date}/"
        try:
            self.client.put_object(Bucket=bucket, Key=folder_name)
            return f"{bucket}/{folder_name}/"

        except Exception as e:
            persist_state_before_failure(
                error=e,
                context=self.context,
                metadata={
                    'destination': f"{bucket}/{folder_name}/"
                }
            )


    def upload_file(self, file_name: str, bucket: str):
        object_name = os.path.basename(file_name)
        self.client.upload_file(file_name, bucket, object_name)

