from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS


log = logging.getLogger("airflow.task")


def transform_study_outcomes(
    nct_id: str, study_key: str, study_data: pd.Series
) -> Tuple:
    primary_outcomes = []
    secondary_outcomes = []
    other_outcomes = []

    outcomes_index = NON_SCALAR_FIELDS["study_outcomes"]["index_field"]
    outcomes_data = study_data.get(outcomes_index)

    if isinstance(outcomes_data, dict) and outcomes_data:

        study_primary_outcomes = outcomes_data.get("primaryOutcomes")
        if (
            isinstance(study_primary_outcomes, (list, np.ndarray))
            and len(study_primary_outcomes) > 0
        ):
            for primary_outcome in study_primary_outcomes:

                primary_outcomes.append(
                    {
                        "study_key": study_key,
                        "measure": primary_outcome.get("measure"),
                        "description": primary_outcome.get("description"),
                        "time_frame": primary_outcome.get("timeFrame"),
                    }
                )

            study_secondary_outcomes = outcomes_data.get("secondaryOutcomes")
            if (
                isinstance(study_secondary_outcomes, (list, np.ndarray))
                and len(study_secondary_outcomes) > 0
            ):
                for secondary_outcome in study_secondary_outcomes:
                    secondary_outcomes.append(
                        {
                            "study_key": study_key,
                            "measure": secondary_outcome.get("measure"),
                            "description": secondary_outcome.get("description"),
                            "time_frame": secondary_outcome.get("timeFrame"),
                        }
                    )

            study_other_outcomes = outcomes_data.get("otherOutcomes")
            if (
                isinstance(study_other_outcomes, (list, np.ndarray))
                and len(study_other_outcomes) > 0
            ):
                for other_outcome in study_other_outcomes:
                    other_outcomes.append(
                        {
                            "study_key": study_key,
                            "measure": other_outcome.get("measure"),
                            "description": other_outcome.get("description"),
                            "time_frame": other_outcome.get("timeFrame"),
                        }
                    )

    else:
        log.warning(f"No outcomes found for study {study_key}, page - NCT ID {nct_id}")

    return primary_outcomes, secondary_outcomes, other_outcomes
