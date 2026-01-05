from typing import List
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def extract_annotation_module(study_key: str, study_data: pd.Series) -> List:
    """
    Extract FDAAA 801 regulatory violations.
    These indicate FDA compliance issues (non-submission, false information, penalties).
    """
    violations = []

    annotations_index = NON_SCALAR_FIELDS["annotations"]["index_field"]
    annotation_data = study_data.get(annotations_index)
    if isinstance(annotation_data, dict) and annotation_data:
        violation_events = annotation_data.get('violationEvents')

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
