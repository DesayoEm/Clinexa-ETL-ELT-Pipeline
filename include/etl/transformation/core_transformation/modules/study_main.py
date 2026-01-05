from typing import Dict
import pandas as pd
from include.etl.transformation.config import SCALAR_FIELDS


def transform_study_fields(study_key: str, study_data: pd.Series) -> Dict:
    study_record = dict()

    study_record["study_key"] = study_key
    for entity_key in SCALAR_FIELDS:
        index_field = SCALAR_FIELDS.get(entity_key)

        study_record[entity_key] = study_data.get(index_field)

    return study_record
