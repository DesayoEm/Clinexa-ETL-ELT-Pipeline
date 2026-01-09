import logging
from typing import List, Dict
from collections import defaultdict
from airflow.utils.context import Context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from include.etl.transformation.core_transformation.study_transformation import (
    process_study_file,
    post_process_tables,
)
from include.etl.transformation.models import StudyResult

EXPECTED_TABLES = StudyResult.expected_tables()


class Transformer:
    """
    Manages the end-to-end transformation workflow: iterating through raw
    parquet files in S3, transforming each into normalised  records,
    merging results, and handling failures with checkpoint recovery.

    Designed to run within an Airflow task context, using the execution date
    for partitioning and S3Hook for file access.

    Attributes:
        context: Airflow task context providing execution metadata.
        execution_date: Logical date of the DAG run (ds), used for partitioning.
        log: Airflow task logger for structured logging.
        s3: S3Hook instance for reading source files and writing checkpoints.
    """

    def __init__(self, context: Context, s3_dest_hook: S3Hook = None):
        self.context = context
        self.execution_date = context.get("ds")
        self.log = logging.getLogger("airflow.task")
        self.s3 = s3_dest_hook or S3Hook(aws_conn_id="aws_airflow")

    def mark_checkpoint(self, index, file):
        """
        Persist progress marker to enable resumption after failure.

        Saves the index and file path of the last attempted file, allowing
        transform_studies_batch to skip already-processed files on retry.

        Args:
            index: Position in the file list where processing failed.
            file: S3 path of the file that failed.
        """

    def load_checkpoint(self):
        """
        Load previously saved checkpoint to resume interrupted processing.

        Retrieves the last successful file index from S3, allowing the batch
        to skip already-processed files. Returns None or starting index if
        no checkpoint exists.
        """

    @staticmethod
    def merge_batch_results(batch_results: List[StudyResult]) -> Dict[str, List[Dict]]:
        """
        Aggregate StudyResult objects into a single dictionary of record lists.

        Combines records from multiple studies into table-keyed lists suitable
        for DataFrame conversion in `post_process_tables`.

        Args:
            batch_results: List of StudyResult objects from process_study_file.

        Returns:
            Dictionary mapping table names to lists of record dicts,
            with all studies' records concatenated per table.
        """
        merged: Dict[str, List[Dict]] = defaultdict(list)

        for study_result in batch_results:
            for table, rows in study_result.tables().items():
                merged[table].extend(rows)

        missing = set(EXPECTED_TABLES) - merged.keys()

        if missing:
            raise ValueError(f"Missing tables: {missing}")

        return merged

    def transform_studies_batch(self, loc: str):
        """
        Process all raw study files for the current execution date.

        Iterates through parquet files at the given S3 location, transforming
        each file's studies
        On failure, marks a checkpoint and re-raises to trigger Airflow retry with resumption.

        Args:
            loc: S3 prefix/location containing raw parquet files to process.

        Raises:
            Exception: Re-raises any processing error after checkpointing,
                preserving the original exception for Airflow visibility.
        """
        files = ""  # s3 loc
        self.load_checkpoint()
        for index, file_path in enumerate(files):

            try:
                batch_result = process_study_file(file_path)
                merged_batch_results = self.merge_batch_results(batch_result)
                dfs = post_process_tables(merged_batch_results)

                return dfs

                # load

            except Exception as e:
                self.mark_checkpoint(index, file_path)
                self.log.exception(f"File failed: Exception: {str(e)}")
                raise
