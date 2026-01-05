from typing import List
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def extract_violations(study_key: str, study_data: pd.Series) -> List:
    """
    Extract FDAAA 801 regulatory violations.
    These indicate FDA compliance issues (non-submission, false information, penalties).
    """
    violations = []

    violation_index = NON_SCALAR_FIELDS["violation_events"]["index_field"]
    violation_events = study_data.get(violation_index)

    if isinstance(violation_events, (list, np.ndarray)) and len(violation_events) > 0:
        for event in violation_events:
            issued_date = event.get("issuedDate")
            event_type = event.get("type")
            violation_key = generate_key(study_key, issued_date, event_type)

            violations.append(
                {
                    "violation_key": violation_key,
                    "study_key": study_key,
                    "violation_type": event_type,
                    "issued_date": issued_date,
                    "description": event.get("description"),
                    "creation_date": event.get("creationDate"),
                    "release_date": event.get("releaseDate"),
                    "posted_date": event.get("postedDate"),
                }
            )

    return violations
