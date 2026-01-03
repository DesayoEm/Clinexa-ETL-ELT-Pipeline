from typing import List, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NESTED_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")



def transform_interventions(study_key: str, study_data: pd.Series) -> Tuple:
    intervention_names = []
    study_interventions = []

    interventions_index = NESTED_FIELDS["interventions"]["index_field"]
    interventions_list = study_data.get(interventions_index)

    if isinstance(interventions_list, (list, np.ndarray)) and len(interventions_list) > 0:
        for intervention in interventions_list:
            main_name = intervention.get("name")
            intervention_type = intervention.get("type")
            description = intervention.get("description")

            intervention_key = generate_key(main_name, intervention_type)
            intervention_names.append({
                "intervention_key": intervention_key,
                "intervention_name": main_name,
                "intervention_type": intervention_type,
                "description": description,
                "is_primary_name": True
            })

            study_interventions.append({
                "study_key": study_key,
                "intervention_key": intervention_key,
                "is_primary_name": True
            })

            other_names = intervention.get("otherNames")
            if isinstance(other_names, (list, np.ndarray)) and len(other_names) > 0:
                for other_name in other_names:
                    if other_name == main_name:
                        continue  # some studies put the main name in the list of other names

                    intervention_key = generate_key(other_name, intervention_type)
                    intervention_names.append({
                        "intervention_key": intervention_key,
                        "intervention_name": other_name,
                        "intervention_type": intervention_type,
                        "description": description,  # inherits from parent

                    })

                    study_interventions.append({
                        "study_key": study_key,
                        "intervention_key": intervention_key,
                        "is_primary_name": False
                    })
    else:
        pass
        # log.warning(f"No interventions found for study {study_key}, {idx}") #noisy

    return intervention_names, study_interventions


def transform_arm_groups(study_key: str, study_data: pd.Series) -> List:
    study_arms_interventions = []

    study_arms_index = NESTED_FIELDS["arm_groups"]["index_field"]
    study_arms_list = study_data.get(study_arms_index)

    if isinstance(study_arms_list, (list, np.ndarray)) and len(study_arms_list) > 0:
        for study_arm in study_arms_list:
            study_arm_label = study_arm.get("label")
            study_arm_description = study_arm.get("description")
            study_arm_type = study_arm.get("type")

            arm_intervention_key = generate_key(study_key, study_arm_label, study_arm_description,
                                                     study_arm_type)

            arm_interventions = study_arm.get("interventionNames")
            if isinstance(arm_interventions, (list, np.ndarray)) and len(arm_interventions) > 0:

                for intervention in arm_interventions:
                    study_arms_interventions.append(
                        {
                            "study_key": study_key,
                            "arm_intervention_key": arm_intervention_key,
                            "arm_label": study_arm_label,
                            "arm_description": study_arm_description,
                            "arm_type": study_arm_type,
                            "arm_intervention_name": intervention,
                        }
                    )
            else:
                study_arms_interventions.append(
                    {
                        "study_key": study_key,
                        "arm_intervention_key": arm_intervention_key,
                        "arm_label": study_arm_label,
                        "arm_description": study_arm_description,
                        "arm_type": study_arm_type,
                        "arm_intervention_name": None,
                    }
                )

    # else:
    #     log.warning(f"No arms found for study {study_key}, page - index {idx}") #too noisy

    return study_arms_interventions