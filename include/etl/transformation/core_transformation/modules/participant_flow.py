from typing import List, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NESTED_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_flow_groups(study_key: str, study_data: pd.Series) -> List:
    study_flow_groups = []

    flow_index = NESTED_FIELDS["flow_groups"]["index_field"]
    flow_group_list = study_data.get(flow_index)

    if isinstance(flow_group_list, (list, np.ndarray)) and len(flow_group_list) > 0:
        for flow in flow_group_list:
            group_id = flow.get('id')
            group_key = generate_key(study_key, group_id)

            study_flow_groups.append({
                "study_key": study_key,
                "group_key": group_key,
                "id": group_id,
                "title": flow.get("title"),
                "description": flow.get("description")

            })

    return study_flow_groups


def transform_flow_events(study_key: str, study_data: pd.Series) -> List:
    flow_period_events = []

    flow_index = NESTED_FIELDS["flow_periods"]["index_field"]
    flow_period_list = study_data.get(flow_index)

    if isinstance(flow_period_list, (list, np.ndarray)) and len(flow_period_list) > 0:
        for period in flow_period_list:
            period_title = period.get('title')
            period_key = generate_key(study_key, period_title)

            period_milestones = period.get('milestones')
            if isinstance(period_milestones, (list, np.ndarray)) and len(period_milestones) > 0:
                for period_milestone in period_milestones:
                    milestone_type = period_milestone.get('type')
                    milestone_achievements = period_milestone.get('achievements')

                    if isinstance(milestone_achievements, (list, np.ndarray)) and len(milestone_achievements) > 0:
                        for achievement in milestone_achievements:
                            flow_period_events.append({
                                "study_key": study_key,
                                "period_key": period_key,
                                "event_class": "ACHIEVEMENT",
                                "event_type": milestone_type,
                                "period_title": period_title,
                                "group_id": achievement.get('groupId'),
                                "num_subjects": achievement.get('numSubjects'),

                            })
                    else:
                        flow_period_events.append({
                            "study_key": study_key,
                            "event_class": "ACHIEVEMENT",
                            "event_type": milestone_type,
                            "period_key": period_key,
                            "period_title": period_title,

                            "group_id": "UNKNOWN",
                            "num_subjects": None,  # not 0

                        })

            period_withdrawals = period.get('dropWithdraws')
            if isinstance(period_withdrawals, (list, np.ndarray)) and len(period_withdrawals) > 0:
                for withdrawal in period_withdrawals:
                    withdrawal_type = withdrawal.get('type')
                    withdrawal_reasons = withdrawal.get('reasons')

                    if isinstance(withdrawal_reasons, (list, np.ndarray)) and len(withdrawal_reasons) > 0:
                        for reason in withdrawal_reasons:
                            flow_period_events.append({
                                "study_key": study_key,
                                "period_key": period_key,
                                "event_class": "WITHDRAWAL",
                                "event_type": withdrawal_type,
                                "period_title": period_title,
                                "group_id": reason.get('groupId'),
                                "num_subjects": reason.get('numSubjects'),

                            })
                    else:
                        flow_period_events.append({
                            "study_key": study_key,
                            "event_class": "WITHDRAWAL",
                            "event_type": withdrawal_type,
                            "period_key": period_key,
                            "period_title": period_title,
                            "group_id": "UNKNOWN",
                            "num_subjects": None,  # not 0

                        })

    return flow_period_events