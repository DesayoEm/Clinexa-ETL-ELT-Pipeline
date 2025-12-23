from typing import Tuple
import io
import json
from datetime import datetime
import pandas as pd
import hashlib

from include.etl.transformation.data_cleaning import Cleaner
from airflow.utils.context import Context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log


class Transformer:
    def __init__(self, context: Context, s3_dest_hook: S3Hook = None):
        self.context = context
        self.s3 = s3_dest_hook or S3Hook(aws_conn_id="aws_airflow")
        self.cleaner = Cleaner()
        self.problematic_records: pd.DataFrame = pd.DataFrame()
        self.batch_size: int = 100000
        self.duplicate_count: int = 0

    @staticmethod
    def generate_key(*args) -> str:
        """Generates a deterministic surrogate key from input values."""
        combined = "|".join(str(arg) for arg in args if arg is not None)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reusable column standardization"""
        df.columns = [self.cleaner.standardize_column_name(col) for col in df.columns]
        return df

    def upload_problematic_records_to_s3(
        self, data: pd.DataFrame, source: str, dest_bucket: str, dest_key: str
    ) -> str:
        """converts Dict into Parquet and uploads to S3."""
        buffer = io.BytesIO()
        row_count = len(data)

        data.to_parquet(buffer, engine="pyarrow", index=False, compression="snappy")
        file_size_bytes = buffer.tell()
        buffer.seek(0)

        dest_key = f"{dest_key}.parquet"
        self.s3_dest_hook.load_file_obj(
            file_obj=buffer, key=dest_key, bucket_name=dest_bucket, replace=True
        )

        location = f"s3://{dest_bucket}/{dest_key}"

        log.info(
            f"Successfully uploaded to {location}"
            f"({row_count} rows, {file_size_bytes / 1024 / 1024:.2f} MB)"
        )

        manifest = {
            "data_file": dest_key,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "metrics": {"row_count": row_count, "file_size_bytes": file_size_bytes},
            "lineage": {
                "data_type": "problematic data",
                "source": source,
                "dag_id": self.context["dag"].dag_id,
                "run_id": self.context["run_id"],
                "execution_date": self.context["ds"],
            },
        }

        manifest_key = dest_key.replace(".parquet", "-manifest.json")
        self.s3_dest_hook.load_string(
            string_data=json.dumps(manifest, indent=2),
            key=manifest_key,
            bucket_name=dest_bucket,
            replace=True,
        )

        log.info(
            f"problematic data manifest saved to s3://{dest_bucket}/{manifest_key}"
        )

        return location

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
        """Reusable deduplication"""
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            df.drop_duplicates(inplace=True)

        return df, duplicate_count

    @staticmethod
    def add_key_as_first_column(df: pd.DataFrame, key_col: str) -> pd.DataFrame:
        """Move key column to first position"""
        return df[[key_col] + [col for col in df.columns if col != key_col]]

    def transform_entity(self, entity_data_location: str, entity_type: str):
        """Transform and load at once or in batches"""
        try:
            entity_df = pd.read_parquet(entity_data_location)
        except Exception as e:
            raise DataLoadError(error=e, entity_type=entity_type)

        total_rows = len(entity_df)
        # load in batches if more than 100k rows
        if total_rows > self.batch_size:
            self.transform_and_load_batches(
                entity_data_location, entity_type, entity_df, total_rows
            )
        else:
            self.transform_and_load_all(entity_data_location, entity_type, entity_df)