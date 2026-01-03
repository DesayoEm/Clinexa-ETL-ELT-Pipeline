from typing import List, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NESTED_FIELDS
from include.etl.transformation.utils import generate_key
from include.etl.transformation.custom_data_classes import OutcomeExtraction

log = logging.getLogger("airflow.task")


def transform_outcome_measures(self, study_key: str, study_data: pd.Series) -> Tuple[
    List, List, List, List, List, List]:
    outcome_measures = []
    outcome_groups = []
    outcome_denom_units = []
    outcome_denom_counts = []
    outcome_measurements = []
    outcome_analyses = []

    outcomes_index = NESTED_FIELDS["outcome_measures"]["index_field"]
    outcomes_list = study_data.get(outcomes_index)

    if isinstance(outcomes_list, (list, np.ndarray)) and len(outcomes_list) > 0:
        for outcome in outcomes_list:
            outcome_title = outcome.get('title')
            outcome_type = outcome.get('type')
            outcome_key = self.generate_key(study_key, outcome_title, outcome_type)

            # DIMENSION: outcome_measures
            outcome_measures.append({
                'outcome_key': outcome_key,
                'study_key': study_key,
                'outcome_type': outcome_type,
                'title': outcome_title,
                'description': outcome.get('description'),
                'population_description': outcome.get('populationDescription'),
                'reporting_status': outcome.get('reportingStatus'),
                'anticipated_posting_date': outcome.get('anticipatedPostingDate'),
                'param_type': outcome.get('paramType'),
                'dispersion_type': outcome.get('dispersionType'),
                'unit_of_measure': outcome.get('unitOfMeasure'),
                'calculate_pct': outcome.get('calculatePct'),
                'time_frame': outcome.get('timeFrame'),
                'denom_units_selected': outcome.get('denomUnitsSelected'),
            })

            # DIMENSION: outcome_groups
            groups = outcome.get('groups', [])
            if isinstance(groups, (list, np.ndarray)) and len(groups) > 0:
                for group in groups:
                    group_id = group.get('id')
                    outcome_group_key = self.generate_key(study_key, outcome_key, group_id)

                    outcome_groups.append({
                        'outcome_group_key': outcome_group_key,
                        'study_key': study_key,
                        'outcome_key': outcome_key,
                        'group_id': group_id,
                        'title': group.get('title'),
                        'description': group.get('description')
                    })

            # STAGING: denoms (denominators)
            denoms = outcome.get('denoms', [])
            if isinstance(denoms, (list, np.ndarray)) and len(denoms) > 0:
                for denom in denoms:
                    denom_unit = denom.get('units')  # Note: 'units' not 'unit'
                    denom_unit = denom_unit.upper() if denom_unit else 'UNKNOWN'
                    denom_unit_key = self.generate_key(denom_unit)

                    outcome_denom_units.append({
                        'denom_unit_key': denom_unit_key,
                        'denom_unit': denom_unit,
                    })

                    denom_counts = denom.get('counts', [])
                    if isinstance(denom_counts, (list, np.ndarray)) and len(denom_counts) > 0:
                        for denom_count in denom_counts:
                            denom_count_group_id = denom_count.get('groupId')
                            denom_count_group_key = self.generate_key(study_key, outcome_key, denom_count_group_id)
                            denom_count_key = self.generate_key(study_key, outcome_key, denom_unit_key,
                                                                denom_count_group_id)

                            outcome_denom_counts.append({
                                'denom_count_key': denom_count_key,
                                'study_key': study_key,
                                'outcome_key': outcome_key,
                                'denom_unit_key': denom_unit_key,
                                'denom_group_key': denom_count_group_key,
                                'group_id': denom_count_group_id,
                                'denom_value': denom_count.get('value')
                            })

            # STAGING: measurements (preserve ALL classes/categories)
            classes = outcome.get('classes', [])
            if isinstance(classes, (list, np.ndarray)) and len(classes) > 0:
                for class_idx, cls in enumerate(classes):
                    categories = cls.get('categories', [])
                    if isinstance(categories, (list, np.ndarray)) and len(categories) > 0:
                        for cat_idx, category in enumerate(categories):
                            measurements = category.get('measurements', [])  # Fixed typo
                            if isinstance(measurements, (list, np.ndarray)) and len(measurements) > 0:
                                for measurement in measurements:
                                    meas_group_id = measurement.get('groupId')
                                    meas_group_key = self.generate_key(study_key, outcome_key, meas_group_id)
                                    measurement_key = self.generate_key(study_key, outcome_key, str(class_idx),
                                                                        str(cat_idx), meas_group_id)

                                    outcome_measurements.append({
                                        'measurement_key': measurement_key,
                                        'study_key': study_key,
                                        'outcome_key': outcome_key,
                                        'class_index': class_idx,  # Preserve structure
                                        'category_index': cat_idx,  # Preserve structure
                                        'group_key': meas_group_key,
                                        'group_id': meas_group_id,
                                        'value': measurement.get('value'),
                                        'lower_limit': measurement.get('lowerLimit'),
                                        'upper_limit': measurement.get('upperLimit'),
                                        'spread': measurement.get('spread'),
                                        'comment': measurement.get('comment')
                                    })

            # FACT: outcome_analyses
            analyses = outcome.get('analyses', [])
            if isinstance(analyses, (list, np.ndarray)) and len(analyses) > 0:
                for analysis_idx, analysis in enumerate(analyses):
                    analysis_key = self.generate_key(study_key, outcome_key, str(analysis_idx))

                    outcome_analyses.append({
                        'analysis_key': analysis_key,
                        'study_key': study_key,
                        'outcome_key': outcome_key,
                        'comparison_groups': json.dumps(analysis.get('groupIds', [])),  # Store as JSON
                        'param_type': analysis.get('paramType'),
                        'param_value': analysis.get('paramValue'),
                        'dispersion_type': analysis.get('dispersionType'),
                        'dispersion_value': analysis.get('dispersionValue'),
                        'statistical_method': analysis.get('statisticalMethod'),
                        'statistical_comment': analysis.get('statisticalComment'),
                        'p_value': analysis.get('pValue'),
                        'p_value_comment': analysis.get('pValueComment'),
                        'non_inferiority_type': analysis.get('nonInferiorityType'),
                    })

    return outcome_measures, outcome_groups, outcome_denom_units, outcome_denom_counts, outcome_measurements, outcome_analyses



