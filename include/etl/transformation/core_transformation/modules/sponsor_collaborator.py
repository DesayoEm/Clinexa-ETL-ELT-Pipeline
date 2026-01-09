from typing import Dict, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_sponsor_and_collaborators_module(
    nct_id: str, study_key: str, study_data: pd.Series
) -> Tuple:
    """
    Transform lead sponsor and collaborating organizations from a clinical trial.

    Every study has exactly one lead sponsor (the organization responsible for
    the trial) and zero or more collaborators (other organizations involved).

    Lead sponsor fields are scalar values at a fixed path,
    while collaborators are in an array.

    Args:
        nct_id: ClinicalTrials.gov identifier (e.g., "NCT12345678").
        study_key: Unique identifier for the clinical trial study.
        study_data: Flattened study record containing sponsor data


    Returns:
        Four-element tuple containing:
            - sponsor: Lead sponsor dimension records
            - study_sponsor: Bridge table linking study to lead sponsor
            - collaborators: Collaborator dimension records
            - study_collaborators: Bridge table linking study to collaborators

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
