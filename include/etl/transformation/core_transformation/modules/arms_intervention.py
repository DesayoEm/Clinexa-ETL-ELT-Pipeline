from typing import List, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_arms_interventions_module(study_key: str, study_data: pd.Series) -> Tuple:
    """
    Extract arm groups and interventions from a clinical trial study.

    Processes the arms/interventions module to produce normalized tables for:
    - Arm groups (treatment/control cohorts in the study design)
    - Arm-to-intervention mappings (which interventions each arm receives)
    - Intervention definitions (drugs, devices, procedures, etc.)
    - Study-to-intervention mappings (linking studies to their interventions)

    Interventions may have alternate names (e.g., brand vs generic drug names).
    These are extracted separately but inherit type and description from their
    parent intervention. The armGroupLabels field on interventions is excluded
    as a data source; arm-intervention relationships are derived solely from
    armGroups[].interventionNames to maintain a single source of truth.

    Args:
        study_key: Unique identifier for the clinical trial study.
        study_data: Flattened study record containing nested arm and
            intervention data

    Returns:
        Six-element tuple containing:
            - arm_groups: Arm group dimension records
            - arm_interventions: Bridge table linking arms to intervention names
            - intervention_names: Primary intervention dimension records
            - study_intervention_names: Bridge table for primary interventions
            - other_interventions_names: Alternate name intervention records
            - study_other_interventions_names: Bridge table for alternate names


        All lists return empty if no arms/interventions exist for the study.
    """

    arm_groups = []
    arm_interventions = []

    intervention_names = []
    study_intervention_names = []
    other_interventions_names = []
    study_other_interventions_names = []

    arms_interventions_index = NON_SCALAR_FIELDS["arms_interventions"]["index_field"]
    arm_groups_list = study_data.get(f"{arms_interventions_index}.armGroups")

    if isinstance(arm_groups_list, (list, np.ndarray)) and len(arm_groups_list) > 0:
        for arm_group in arm_groups_list:
            arm_label = arm_group.get("label")
            arm_description = arm_group.get("description")
            arm_type = arm_group.get("type")

            arm_group_key = generate_key(
                study_key, arm_label, arm_description, arm_type
            )

            arm_groups.append(
                {
                    "study_key": study_key,
                    "arm_group_key": arm_group_key,
                    "arm_label": arm_label,
                    "arm_description": arm_description,
                    "arm_type": arm_type,
                }
            )

            arm_interventions_list = arm_group.get("interventionNames")
            if (
                isinstance(arm_interventions_list, (list, np.ndarray))
                and len(arm_interventions_list) > 0
            ):

                for arm_intervention in arm_interventions_list:
                    arm_interventions.append(
                        {
                            "study_key": study_key,
                            "arm_group_key": arm_group_key,
                            "arm_intervention_name": arm_intervention,
                        }
                    )

    interventions_list = study_data.get(f"{arms_interventions_index}.interventions")
    if (
        isinstance(interventions_list, (list, np.ndarray))
        and len(interventions_list) > 0
    ):
        for intervention in interventions_list:
            main_name = intervention.get("name")
            intervention_type = intervention.get("type")
            description = intervention.get("description")

            intervention_key = generate_key(main_name, intervention_type)
            intervention_names.append(
                {
                    "intervention_key": intervention_key,
                    "intervention_name": main_name,
                    "intervention_type": intervention_type,
                    "description": description,
                }
            )

            study_intervention_names.append(
                {
                    "study_key": study_key,
                    "intervention_key": intervention_key,
                    "is_primary_name": True,
                }
            )

            other_names = intervention.get("otherNames")

            if isinstance(other_names, (list, np.ndarray)) and len(other_names) > 0:
                for other_name in other_names:
                    if other_name == main_name:
                        continue  # some studies put the main name in the list of other names

                    intervention_key = generate_key(other_name, intervention_type)
                    other_interventions_names.append(
                        {
                            "intervention_key": intervention_key,
                            "intervention_name": other_name,
                            "intervention_type": intervention_type,  # inherit from parent
                            "description": description,  # inherit from parent
                        }
                    )

                    study_other_interventions_names.append(
                        {
                            "study_key": study_key,
                            "intervention_key": intervention_key,
                            "is_primary_name": False,
                        }
                    )
            # armGroupLabels is excluded. check docs/excluded_fields.md for reasons

    return (
        arm_groups,
        arm_interventions,
        intervention_names,
        study_intervention_names,
        other_interventions_names,
        study_other_interventions_names,
    )
