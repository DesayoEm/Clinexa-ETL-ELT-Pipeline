from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_outcome_measures(study_key: str, study_data: pd.Series) -> Tuple:
    outcome_measures = []
    outcome_measure_groups = []
    outcome_measure_denom_units = []
    outcome_measure_denom_counts = []
    outcome_measure_measurements = []
    outcome_measure_analyses = []
    outcome_measure_comparison_groups = []

    outcomes_index = NON_SCALAR_FIELDS["outcome_measures"]["index_field"]
    outcomes_measures_list = study_data.get(outcomes_index)

    if (
        isinstance(outcomes_measures_list, (list, np.ndarray))
        and len(outcomes_measures_list) > 0
    ):
        for outcome_measure in outcomes_measures_list:
            outcome_measure_title = outcome_measure.get("title")
            outcome_measure_type = outcome_measure.get("type")
            outcome_measure_key = generate_key(
                study_key, outcome_measure_title, outcome_measure_type
            )

            outcome_measures.append(
                {
                    "outcome_measure_key": outcome_measure_key,
                    "study_key": study_key,
                    "outcome_type": outcome_measure_type,
                    "title": outcome_measure_title,
                    "description": outcome_measure.get("description"),
                    "population_description": outcome_measure.get(
                        "populationDescription"
                    ),
                    "reporting_status": outcome_measure.get("reportingStatus"),
                    "anticipated_posting_date": outcome_measure.get(
                        "anticipatedPostingDate"
                    ),
                    "param_type": outcome_measure.get("paramType"),
                    "dispersion_type": outcome_measure.get("dispersionType"),
                    "unit_of_measure": outcome_measure.get("unitOfMeasure"),
                    "calculate_pct": outcome_measure.get("calculatePct"),
                    "time_frame": outcome_measure.get("timeFrame"),
                    "denom_units_selected": outcome_measure.get("denomUnitsSelected"),
                }
            )

            groups = outcome_measure.get("groups", [])
            if isinstance(groups, (list, np.ndarray)) and len(groups) > 0:
                for group in groups:
                    group_id = group.get("id")
                    outcome_group_key = generate_key(
                        study_key, outcome_measure_key, group_id
                    )

                    outcome_measure_groups.append(
                        {
                            "outcome_group_key": outcome_group_key,
                            "study_key": study_key,
                            "outcome_measure_key": outcome_measure_key,
                            "group_id": group_id,
                            "title": group.get("title"),
                            "description": group.get("description"),
                        }
                    )

            denoms_list = outcome_measure.get("denoms")
            if isinstance(denoms_list, (list, np.ndarray)) and len(denoms_list) > 0:
                for denom in denoms_list:
                    denom_unit = denom.get("units")
                    denom_unit = denom_unit.upper() if denom_unit else "UNKNOWN"
                    denom_unit_key = generate_key(denom_unit)

                    outcome_measure_denom_units.append(
                        {
                            "denom_unit_key": denom_unit_key,
                            "denom_unit": denom_unit,
                        }
                    )

                    denom_counts = denom.get("counts")
                    if (
                        isinstance(denom_counts, (list, np.ndarray))
                        and len(denom_counts) > 0
                    ):
                        for denom_count in denom_counts:
                            denom_count_group_id = denom_count.get("groupId")
                            denom_count_group_key = generate_key(
                                study_key, outcome_measure_key, denom_count_group_id
                            )
                            denom_count_key = generate_key(
                                study_key,
                                outcome_measure_key,
                                denom_unit_key,
                                denom_count_group_id,
                            )

                            outcome_measure_denom_counts.append(
                                {
                                    "denom_count_key": denom_count_key,
                                    "study_key": study_key,
                                    "outcome_measure_key": outcome_measure_key,
                                    "denom_unit_key": denom_unit_key,
                                    "denom_group_key": denom_count_group_key,
                                    "group_id": denom_count_group_id,
                                    "denom_value": denom_count.get("value"),
                                }
                            )

            classes = outcome_measure.get("classes")
            if isinstance(classes, (list, np.ndarray)) and len(classes) > 0:
                categories = classes[0].get(
                    "categories"
                )  # class is not a true container and only wraps categories contrary to what the docs say
                if isinstance(categories, (list, np.ndarray)) and len(categories) > 0:
                    for cat_idx, category in enumerate(categories):
                        measurements = category.get("measurements")
                        if (
                            isinstance(measurements, (list, np.ndarray))
                            and len(measurements) > 0
                        ):
                            for measurement in measurements:
                                meas_group_id = measurement.get("groupId")
                                meas_group_key = generate_key(
                                    study_key, outcome_measure_key, meas_group_id
                                )

                                outcome_measure_measurements.append(
                                    {
                                        "measurement_key": meas_group_key,
                                        "outcome_measure_key": outcome_measure_key,
                                        "study_key": study_key,
                                        "group_id": meas_group_id,
                                        "value": measurement.get("value"),
                                        "lower_limit": measurement.get("lowerLimit"),
                                        "upper_limit": measurement.get("upperLimit"),
                                        "spread": measurement.get("spread"),
                                        "comment": measurement.get("comment"),
                                    }
                                )

            analyses = outcome_measure.get("analyses")
            if isinstance(analyses, (list, np.ndarray)) and len(analyses) > 0:
                for analysis in analyses:
                    param_type = (analysis.get("paramType"),)
                    param_value = analysis.get("paramValue")

                    analysis_key = generate_key(
                        study_key, outcome_measure_key, param_type, param_value
                    )

                    outcome_measure_analyses.append(
                        {
                            "analysis_key": analysis_key,
                            "study_key": study_key,
                            "outcome_measure_key": outcome_measure_key,
                            "param_type": param_type,
                            "param_value": param_value,
                            "dispersion_type": analysis.get("dispersionType"),
                            "dispersion_value": analysis.get("dispersionValue"),
                            "statistical_method": analysis.get("statisticalMethod"),
                            "statistical_comment": analysis.get("statisticalComment"),
                            "p_value": analysis.get("pValue"),
                            "p_value_comment": analysis.get("pValueComment"),
                            "non_inferiority_type": analysis.get("nonInferiorityType"),
                        }
                    )

                    analysis_comparison_groups = analysis.get("comparisonGroups")
                    if (
                        isinstance(analysis_comparison_groups, (list, np.ndarray))
                        and len(analysis_comparison_groups) > 0
                    ):
                        for group in analysis_comparison_groups:
                            outcome_measure_comparison_groups.append(
                                {
                                    "analysis_key": analysis_key,
                                    "outcome_measure_key": group.get(
                                        "outcomeMeasureKey"
                                    ),
                                    "study_key": study_key,
                                    "group_id": group.get("groupId"),
                                }
                            )

    return (
        outcome_measures,
        outcome_measure_groups,
        outcome_measure_denom_units,
        outcome_measure_denom_counts,
        outcome_measure_measurements,
        outcome_measure_analyses,
        outcome_measure_comparison_groups,
    )
