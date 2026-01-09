from typing import Dict
import pandas as pd
from include.etl.transformation.config import SCALAR_FIELDS


def transform_scalar_fields(study_key: str, study_data: pd.Series) -> Dict:
    """
    Transform scalar (non-nested) fields into the main study fact record.

    This function collects fields that have a one-to-one relationship with the study
    directly into the central study record.

    Field mappings are defined in SCALAR_FIELDS config, which maps output
    column names to their source paths in the flattened study data.

    Args:
        study_key: Unique identifier for the clinical trial study.
        study_data: Flattened study record containing all study fields.

    Returns:
        Single dictionary representing one row in the study fact table,
        with study_key and all scalar fields defined in SCALAR_FIELDS.
        Missing fields will have None values.
    """
    study_record = dict()

    study_record["study_key"] = study_key
    for entity_key in SCALAR_FIELDS:
        index_field = SCALAR_FIELDS.get(entity_key)

        study_record[entity_key] = study_data.get(index_field)

    return study_record
