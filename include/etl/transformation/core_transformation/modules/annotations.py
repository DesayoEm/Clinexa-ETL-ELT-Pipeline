from typing import List
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_annotations_module(study_key: str, study_data: pd.Series) -> List:
    """
    Extract FDAAA 801 regulatory violations.
    These indicate FDA compliance issues (non-submission, false information, penalties).
    """
    violations = []

    annotations_index = NON_SCALAR_FIELDS["annotations"]["index_field"]
    violations_list = study_data.get(annotations_index)

    if isinstance(violations_list, (list, np.ndarray)) and len(violations_list) > 0:

        for violation in violations_list:
            issued_date = violation.get("issuedDate")
            event_type = violation.get("type")
            violation_key = generate_key(study_key, issued_date, event_type)

            violations.append(
                {
                    "violation_key": violation_key,
                    "study_key": study_key,
                    "violation_type": event_type,
                    "issued_date": issued_date,
                    "description": violation.get("description"),
                    "creation_date": violation.get("creationDate"),
                    "release_date": violation.get("releaseDate"),
                    "posted_date": violation.get("postedDate"),
                }
            )

    return violations
