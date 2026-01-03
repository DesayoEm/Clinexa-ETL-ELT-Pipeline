from dataclasses import dataclass,asdict
from typing import List, Dict


@dataclass
class OutcomeExtraction:
    measures: List
    groups: List
    denom_units: List
    denom_counts: List
    measurements: List
    analyses: List
    comparison_groups: List


@dataclass
class StudyResult:
    """
    Container for all dimensional model records extracted from a single study.

    Groups the output of transform_single_study into named attributes for
    clarity when aggregating batch results. Each attribute holds a list of dicts representing records
    for that entity table.
    """
    study: List #single study
    sponsors: List
    study_sponsors: List
    collaborators: List
    study_collaborators: List
    conditions: List
    study_conditions: List
    keywords: List
    study_keywords: List
    arm_group_interventions: List
    interventions: List
    study_interventions: List
    central_contacts: List
    study_central_contacts: List
    locations: List
    study_locations: List
    references: List
    links: List
    ipds: List
    flow_groups: List
    flow_period_events: List

    def tables(self) -> Dict[str, List[Dict]]:
        return asdict(self)