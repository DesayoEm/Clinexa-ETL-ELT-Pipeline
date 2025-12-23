from typing import Dict, List, Any, Hashable, Tuple
import io
import logging
import json
from datetime import datetime
import pandas as pd
import pyarrow.parquet as pq
import hashlib

from transformer_config import ONE_TO_ONE_FIELDS, NESTED_FIELDS
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
    def remove_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """Reusable deduplication"""
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            df.drop_duplicates(inplace=True)

        return df, duplicate_count


    def read_parquet(self, data_loc: str):
        """Transform and load at once or in batches"""
        try:
            df_studies = pd.read_parquet(data_loc)
            df_studies = pd.json_normalize(df_studies['studies'])

            for study in df_studies:
                self.extract_study_fields(study)

        except Exception as e:
            raise


    def extract_study_fields(self, df_normalized):
        """Transform and load at once or in batches"""
        try:
            df_study = pd.DataFrame()
            study_key = self.generate_key(df_normalized['protocolSection.identificationModule.nctId'])
            if not study_key:
                self.log.warning(f"Study missing NCT ID, skipping index {''}")
                return
            df_study['study_key'] = study_key

            #clean specific fields

            for entity_key in NESTED_FIELDS:
                self.extract_study_entity(NESTED_FIELDS, entity_key, study_key, df_normalized)

        except Exception as e:
            raise

    def extract_study_entity(self, entity_map: Dict, entity_name: str, study_key: str, study_df: pd.DataFrame):
        method_name = entity_map.get(entity_name).lower()
        transformer_method = getattr(self, method_name)

        entity_df = transformer_method(study_key, study_df)

        return entity_df


    def extract_sponsors(self, study_key: str, study_df: pd.DataFrame):
        pass

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













