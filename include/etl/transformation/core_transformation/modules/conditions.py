from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NESTED_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")




def transform_conditions(nct_id: str, study_key: str, study_data: pd.Series) -> Tuple:
    conditions = []
    study_conditions = []

    conditions_index = NESTED_FIELDS["conditions"]["index_field"]
    conditions_list = study_data.get(conditions_index)

    if isinstance(conditions_list, (list, np.ndarray)) and len(conditions_list) > 0:
        for condition in conditions_list:
            condition_key = generate_key(condition)

            conditions.append(
                {"condition_key": condition_key, "condition_name": condition}
            )

            study_conditions.append(
                {
                    "study_key": study_key,
                    "condition_key": condition_key,
                }
            )

    else:
        log.warning(f"No conditions found for study {study_key}, page - NCT ID {nct_id}")

    return conditions, study_conditions


def transform_keywords(study_key: str, study_data: pd.Series) -> Tuple:
    keywords = []
    study_keywords = []

    keywords_index = NESTED_FIELDS["keywords"]["index_field"]
    keywords_list = study_data.get(keywords_index)

    if isinstance(keywords_list, (list, np.ndarray)) and len(keywords_list) > 0:

        for keyword in keywords_list:
            keyword_key = generate_key(keyword)

            keywords.append({"keyword_key": keyword_key, "keyword_name": keyword})

            study_keywords.append(
                {
                    "study_key": study_key,
                    "keyword_key": keyword_key,
                }
            )

    return keywords, study_keywords
