from dataclasses import dataclass, asdict, fields
from typing import List, Dict


@dataclass
class StudyResult:
    """
    Container for all dimensional model records extracted from a single study.

    Groups the output of transform_single_study into named attributes for
    clarity when aggregating batch results. Each attribute holds a list of dicts representing records
    for that entity table.
    """

    studies: List  # single study
    secondary_ids: List
    nct_aliases: List
    sponsors: List
    study_sponsors: List
    collaborators: List
    study_collaborators: List
    conditions: List
    study_conditions: List
    keywords: List
    study_keywords: List
    arm_groups: List
    arm_interventions: List
    intervention_names: List
    study_intervention_names: List
    other_interventions_names: List
    study_other_interventions_names: List
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

    @classmethod
    def expected_tables(cls) -> List[str]:
        """Canonical list of expected output tables for the StudyResult schema."""
        return [f.name for f in fields(cls)]
