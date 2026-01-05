from typing import Dict, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_sponsors(nct_id: str, study_key: str, study_data: pd.Series) -> Tuple:
    """
    Extract sponsors from a single study.
    Args:
        nct_id: The natural key for this study
        study_key: The generated key for this study
        study_data: The nested dict for one study (not a DataFrame)
    Returns:
        Tuple of (sponsors_list, study_sponsors_list)
    """

    sponsors = []
    study_sponsors = []

    # Extract lead sponsor
    lead_sponsor_index = NON_SCALAR_FIELDS["sponsor"]["index_field"]

    # sponsor name and class are scalar values and MUST be extracted directly
    lead_sponsor_name = study_data.get(f"{lead_sponsor_index}.name")
    lead_sponsor_class = study_data.get(f"{lead_sponsor_index}.class")

    if pd.notna(lead_sponsor_name) and pd.notna(lead_sponsor_class):
        sponsor_key = generate_key(lead_sponsor_name, lead_sponsor_class)
        sponsors.append(
            {
                "sponsor_key": sponsor_key,
                "name": lead_sponsor_name,
                "sponsor_class": lead_sponsor_class,
            }
        )

        study_sponsors.append(
            {"study_key": study_key, "sponsor_key": sponsor_key, "is_lead": True}
        )
    else:
        log.warning(
            f"No lead sponsor found for study {study_key}, page - NCT ID {nct_id}"
        )

    return sponsors, study_sponsors


def transform_collaborators(study_key: str, study_data: pd.Series) -> Tuple:
    collaborators = []
    study_collaborators = []

    # Extract collaborators
    collaborators_index = NON_SCALAR_FIELDS["collaborators"]["index_field"]
    collaborators_list = study_data.get(collaborators_index)

    if (
        isinstance(collaborators_list, (list, np.ndarray))
        and len(collaborators_list) > 0
    ):
        for collaborator in collaborators_list:
            collaborator_key = generate_key(
                collaborator.get("name"), collaborator.get("class")
            )

            collaborators.append(
                {
                    "collaborator_key": collaborator_key,
                    "name": collaborator.get("name"),
                    "collaborator_class": collaborator.get("class"),
                }
            )

            study_collaborators.append(
                {
                    "study_key": study_key,
                    "collaborator_key": collaborator_key,
                    "is_lead": False,
                }
            )

    return collaborators, study_collaborators
