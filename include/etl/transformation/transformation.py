from typing import Dict, List, Any, Hashable, Tuple
import io
import logging
import json
from datetime import datetime
import pandas as pd
import hashlib

from transformer_config import SINGLE_FIELDS, NESTED_FIELDS
from data_cleaning import Cleaner
from airflow.utils.context import Context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class Transformer:
    def __init__(self, context: Context, s3_dest_hook: S3Hook = None):
        self.context = context
        self.execution_date = self.context.get("ds")
        self.log = logging.getLogger("airflow.task")

        self.s3 = s3_dest_hook or S3Hook(aws_conn_id="aws_airflow")
        self.cleaner = Cleaner()


    @staticmethod
    def generate_key(*args) -> str:
        """Generates a deterministic surrogate key from input values."""
        combined = "|".join(str(arg) for arg in args if arg is not None)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    @staticmethod
    def deep_get(data: dict, path: str):
        """Safely navigate nested dict using dot notation path."""
        keys = path.split('.')
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value


    @staticmethod
    def transform_all_studies(self, loc: str) -> None:
        for study_file in loc:
            try:
                #pull from s3
                df_studies = self.read_parquet(study_file)
                self.transform_study_file(df_studies)
                #checkpoint

            #inner loop will fail gracefully wherever possible and errors will only raise for critical issues
            except Exception as e:
                raise


    def transform_study_file(self, data_loc: str):
        """
        Transform a batch of raw study dicts in a file.
        Args:
            data_loc: Location of the  file
        """
        df_studies = pd.read_parquet(data_loc)
        df_studies = pd.json_normalize(df_studies['studies'])

        all_sponsors = []
        all_study_sponsors = []
        all_studies = []

        for study in df_studies:

            nct_id = self.deep_get(study, 'protocolSection.identificationModule.nctId')
            if not nct_id:
                self.log.warning("Study missing NCT ID, skipping") #log page and index
                continue

            study_key = self.generate_key(nct_id)

            #study
            study_record = self.extract_study_fields(study_key, study)
            all_studies.append(study_record)

            #sponsors
            sponsors, study_sponsors = self.extract_sponsors(study_key, study)
            all_sponsors.extend(sponsors)
            all_study_sponsors.extend(study_sponsors)



        #build dataframes from lists and dicts
        df_sponsors = pd.DataFrame(all_sponsors)
        df_study_sponsors = pd.DataFrame(all_study_sponsors)
        df_studies = pd.DataFrame(all_studies)

        # dedupe
        df_sponsors = df_sponsors.drop_duplicates(subset=['sponsor_key'])

        # load
        return df_studies, df_sponsors, df_study_sponsors


    def extract_study_fields(self, study_key: str, study_df: dict) -> Dict:
        study_record = dict()

        study_record['study_key'] = study_key
        for entity_key in SINGLE_FIELDS:
            index_field = SINGLE_FIELDS.get(entity_key)

            study_record[entity_key] = self.deep_get(study_df, index_field)

        return study_record


    def extract_sponsors(self, study_key: str, study_df: pd.DataFrame):
        df_sponsor = pd.DataFrame()
        df_study_sponsor = pd.DataFrame()

        lead_sponsor_index = NESTED_FIELDS['sponsors'].get('index_field')
        lead_sponsor = study_df[lead_sponsor_index]

        sponsor_key = self.generate_key(lead_sponsor.get('name'), lead_sponsor.get('class'))

        df_sponsor['sponsor_key'] = sponsor_key
        df_sponsor['name'] = lead_sponsor.get('name')
        df_sponsor['class'] = lead_sponsor.get('class')


        df_study_sponsor['sponsor_key'] = sponsor_key
        df_study_sponsor['study_key'] = study_key
        df_study_sponsor['is_lead'] = True


        #Extract collaborators
        collaborator_index = NESTED_FIELDS['collaborators'].get('index_field')
        collaborators = study_df[collaborator_index]

        for collaborator in collaborators:
            collaborator_key = self.generate_key(collaborator.get('name'), collaborator.get('class'))
            df_sponsor['sponsor_key'] = collaborator_key
            df_sponsor['name'] = collaborator.get('name')
            df_sponsor['class'] = collaborator.get('class')

            df_study_sponsor['sponsor_key'] = sponsor_key
            df_study_sponsor['study_key'] = study_key
            df_study_sponsor['is_lead'] = False













    def extract_conditions(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_interventions(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_arm_groups(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_locations(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_officials(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_outcomes(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_see_also(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_study_phases(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_age_group(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_ipd_info_types(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_id_infos(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_nct_id_aliases(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_condition_mesh(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_intervention_mesh(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_large_documents(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_unposted_events(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_violation_events(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_removed_countries(self, study_key: str, study_df: pd.DataFrame):
        pass

    def extract_submission_infos(self, study_key: str, study_df: pd.DataFrame):
        pass













