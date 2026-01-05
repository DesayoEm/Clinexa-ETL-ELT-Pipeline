from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key


log = logging.getLogger("airflow.task")


def transform_adverse_events(self, study_key: str, study_data: pd.Series) -> Tuple:

    adverse_event = []
    event_groups = []
    serious_events = []
    serious_event_stats = []
    other_events = []
    other_event_stats = []

    events_index = NON_SCALAR_FIELDS["adverse_events"]["index_field"]
    event_data = study_data.get(events_index)

    if isinstance(event_data, dict) and event_data:
        description = event_data.get("description")
        adverse_event_key = generate_key(study_key, description)

        adverse_event.append(
            {
                "adverse_event_key": adverse_event_key,
                "study_key": study_key,
                "description": description,
                "frequency_threshold": event_data.get("frequencyThreshold"),
                "time_frame": event_data.get("timeFrame"),
                "mortality_cmt": event_data.get("allCauseMortalityComment"),
            }
        )

        event_groups = event_data.get("eventGroups")

        if isinstance(event_groups, (list, np.ndarray)) and len(event_groups) > 0:
            for event_group in event_groups:
                group_id = event_group.get("id")
                event_group_key = self.generate_key(
                    study_key, adverse_event_key, group_id
                )

                event_groups.append(
                    {
                        "event_group_key": event_group_key,
                        "study_key": study_key,
                        "adverse_event_key": adverse_event_key,
                        "group_id": group_id,
                        "title": event_group.get("title"),
                        "description": event_group.get("description"),
                        "num_deaths": event_group.get("deathsNumAffected"),
                        "num_deaths_at_risk": event_group.get("deathsNumAtRisk"),
                        "num_serious": event_group.get("seriousNumAffected"),
                        "num_serious_at_risk": event_group.get("seriousNumAtRisk"),
                        "num_other": event_group.get("otherNumAffected"),
                        "num_other_at_risk": event_group.get("otherNumAtRisk"),
                    }
                )

        serious_events_list = event_data.get("seriousEvents")

        if (
            isinstance(serious_events_list, (list, np.ndarray))
            and len(serious_events) > 0
        ):
            for serious_event in serious_events_list:
                term = serious_event.get("term")
                serious_event_key = self.generate_key(
                    study_key, adverse_event_key, term
                )

                serious_events.append(
                    {
                        "serious_event_key": serious_event_key,
                        "adverse_event_key": adverse_event_key,
                        "study_key": study_key,
                        "term": term,
                        "organ_system": serious_event.get("organSystem"),
                        "source_vocab": serious_event.get("sourceVocabulary"),
                        "assessment_type": serious_event.get("assessmentType"),
                        "notes": serious_event.get("notes"),
                    }
                )
                serious_event_stats_list = serious_event.get("stats")
                if (
                    isinstance(serious_event_stats_list, (list, np.ndarray))
                    and len(serious_event_stats_list) > 0
                ):
                    for serious_event_stat in serious_event_stats_list:
                        group_id = serious_event_stat.get("groupId")
                        event_stat_key = self.generate_key(
                            study_key, adverse_event_key, serious_event_key, group_id
                        )

                        serious_event_stats.append(
                            {
                                "event_stat_key": event_stat_key,
                                "serious_event_key": serious_event_key,
                                "adverse_event_key": adverse_event_key,
                                "study_key": study_key,
                                "group_id": group_id,
                                "num_events": serious_event_stat.get("numEvents"),
                                "num_affected": serious_event_stat.get("numAffected"),
                                "num_at_risk": serious_event_stat.get("numAtRisk"),
                            }
                        )

        other_events_list = event_data.get("otherEvents")
        if (
            isinstance(other_events_list, (list, np.ndarray))
            and len(other_events_list) > 0
        ):
            for other_event in other_events_list:
                term = other_event.get("term")
                other_event_key = self.generate_key(study_key, adverse_event_key, term)

                serious_events.append(
                    {
                        "other_event_key": other_event_key,
                        "adverse_event_key": adverse_event_key,
                        "study_key": study_key,
                        "term": term,
                        "organ_system": other_event.get("organSystem"),
                        "source_vocab": other_event.get("sourceVocabulary"),
                        "assessment_type": other_event.get("assessmentType"),
                        "notes": other_event.get("notes"),
                    }
                )

                other_event_stats_list = other_event.get("stats")
                if (
                    isinstance(other_event_stats_list, (list, np.ndarray))
                    and len(other_event_stats_list) > 0
                ):
                    for other_event_stat in other_event_stats_list:

                        group_id = other_event_stat.get("groupId")
                        event_stat_key = self.generate_key(
                            study_key, adverse_event_key, other_event_key, group_id
                        )

                        other_event_stats.append(
                            {
                                "event_stat_key": event_stat_key,
                                "other_event_key": other_event_key,
                                "adverse_event_key": adverse_event_key,
                                "study_key": study_key,
                                "group_id": group_id,
                                "num_events": other_event_stat.get("numEvents"),
                                "num_affected": other_event_stat.get("numAffected"),
                                "num_at_risk": other_event_stat.get("numAtRisk"),
                            }
                        )

    return (
        adverse_event,
        event_groups,
        serious_events,
        serious_event_stats,
        other_events,
        other_event_stats,
    )
