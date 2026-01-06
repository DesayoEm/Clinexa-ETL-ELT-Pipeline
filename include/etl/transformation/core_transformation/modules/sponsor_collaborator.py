from typing import Dict, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_sponsor_and_collaborators(
    nct_id: str, study_key: str, study_data: pd.Series
) -> Tuple:
    """
    Extract sponsors from a single study.
    Args:
        nct_id: The natural key for this study
        study_key: The generated key for this study
        study_data: The nested dict for one study (not a DataFrame)
    Returns:
        Tuple of (sponsors_list, study_sponsors_list)
    """

    sponsor = []
    study_sponsor = []
    collaborators = []
    study_collaborators = []

    sponsor_collaborator_index = NON_SCALAR_FIELDS["sponsor_collaborators"][
        "index_field"
    ]

    ## sponsor name and class are scalar values and MUST be transformed as so
    lead_sponsor_name = study_data.get(f"{sponsor_collaborator_index}.leadSponsor.name")
    lead_sponsor_class = study_data.get(
        f"{sponsor_collaborator_index}.leadSponsor.class"
    )

    if pd.notna(lead_sponsor_name) and pd.notna(lead_sponsor_class):

        sponsor_key = generate_key(lead_sponsor_name, lead_sponsor_class)
        sponsor.append(
            {
                "sponsor_key": sponsor_key,
                "name": lead_sponsor_name,
                "sponsor_class": lead_sponsor_class,
            }
        )

        study_sponsor.append({"study_key": study_key, "sponsor_key": sponsor_key})

    # collaborators
    collaborators_list = study_data.get(f"{sponsor_collaborator_index}.collaborators")

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
                }
            )

    return sponsor, study_sponsor, collaborators, study_collaborators
