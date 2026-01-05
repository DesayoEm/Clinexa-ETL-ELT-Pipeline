from typing import List, Dict
from collections import defaultdict
import logging
import pandas as pd

from include.etl.transformation.config import SINGLE_FIELDS
from include.etl.transformation.utils import generate_key
from include.etl.transformation.custom_data_classes import StudyResult

from include.etl.transformation.core_transformation.modules.study_main import (
    transform_study_fields,
)
from include.etl.transformation.core_transformation.modules.sponsor_collaborator import (
    transform_sponsors,
    transform_collaborators,
)
from include.etl.transformation.core_transformation.modules.conditions import (
    transform_conditions,
    transform_keywords,
)
from include.etl.transformation.core_transformation.modules.arms_intervention import (
    transform_arm_groups,
    transform_interventions,
)
from include.etl.transformation.core_transformation.modules.contacts_location import (
    transform_locations,
    transform_central_contacts,
)
from include.etl.transformation.core_transformation.modules.references import (
    transform_references,
    transform_links,
    transform_ipds,
)
from include.etl.transformation.core_transformation.modules.participant_flow import (
    transform_flow_events,
    transform_flow_groups,
)

log = logging.getLogger("airflow.task")


def post_process_tables(results: Dict[str, List[Dict]]) -> List[pd.DataFrame]:
    """
    Convert raw transformation results into deduplicated DataFrames.

    Takes the aggregated dictionary of entity lists from batch processing,
    converts each to a DataFrame, and applies deduplication to dimension tables

    Args:
        results: Dictionary mapping entity names to lists of record dicts

    Returns:
        List of DataFrames in fixed order for downstream loading:
        [studies, sponsors, study_sponsors, collaborators, study_collaborators,
         conditions, study_conditions, keywords, study_keywords, interventions,
         study_interventions, arm_group_interventions, central_contacts,
         study_central_contacts, locations, study_locations, references,
         links, ipds, flow_groups, flow_period_events]
    """

    df_studies = pd.DataFrame(results["studies"])

    # sponsorCollaboratorsModule
    df_sponsors = pd.DataFrame(results["sponsors"])
    df_study_sponsors = pd.DataFrame(results["study_sponsors"])
    df_collaborators = pd.DataFrame(results["collaborators"])
    df_study_collaborators = pd.DataFrame(results["study_collaborators"])

    # conditionsModule
    df_conditions = pd.DataFrame(results["conditions"])
    df_study_conditions = pd.DataFrame(results["study_conditions"])
    df_keywords = pd.DataFrame(results["keywords"])
    df_study_keywords = pd.DataFrame(results["study_keywords"])

    # armsInterventionsModule
    df_interventions = pd.DataFrame(results["interventions"])
    df_study_interventions = pd.DataFrame(results["study_interventions"])
    df_arm_group_interventions = pd.DataFrame(results["arm_group_interventions"])

    # contactsLocationsModule
    df_central_contacts = pd.DataFrame(results["central_contacts"])
    df_study_central_contacts = pd.DataFrame(results["study_central_contacts"])
    df_locations = pd.DataFrame(results["locations"])
    df_study_locations = pd.DataFrame(results["study_locations"])

    # referencesModule
    df_references = pd.DataFrame(results["references"])
    df_links = pd.DataFrame(results["links"])
    df_ipds = pd.DataFrame(results["ipds"])

    # outcomeMeasuresModule
    df_flow_groups = pd.DataFrame(results["flow_groups"])
    df_flow_period_events = pd.DataFrame(results["flow_period_events"])

    # dedupe
    df_sponsors = df_sponsors.drop_duplicates(subset=["sponsor_key"])
    df_collaborators = df_collaborators.drop_duplicates(subset=["collaborator_key"])
    df_conditions = df_conditions.drop_duplicates(subset=["condition_key"])
    df_keywords = df_keywords.drop_duplicates(subset=["keyword_key"])
    df_interventions = df_interventions.drop_duplicates(subset=["intervention_key"])
    df_arm_group_interventions = df_arm_group_interventions.drop_duplicates(
        subset=["study_arm_key", "study_key", "arm_intervention_name"]
    )
    df_locations = df_locations.drop_duplicates(subset=["location_key"])
    df_central_contacts = df_central_contacts.drop_duplicates(subset=["contact_key"])

    df_references = df_references.drop_duplicates(subset=["study_key", "ref_key"])
    df_links = df_links.drop_duplicates(subset=["study_key", "link_key", "url"])
    df_ipds = df_ipds.drop_duplicates(subset=["study_key", "ipd_key"])

    df_flow_groups = df_flow_groups.drop_duplicates(subset=["study_key", "group_key"])

    # Aggregate to mitigate flow duplicates. check docs/data_quality_issues.md for details
    df_flow_period_events = df_flow_period_events.groupby(
        ["study_key", "period_title", "event_class", "event_type", "group_id"],
        as_index=False,
    ).agg({"num_subjects": "sum", "period_key": "first"})

    return [
        df_studies,
        df_sponsors,
        df_study_sponsors,
        df_collaborators,
        df_study_collaborators,
        df_conditions,
        df_study_conditions,
        df_keywords,
        df_study_keywords,
        df_interventions,
        df_study_interventions,
        df_arm_group_interventions,
        df_central_contacts,
        df_study_central_contacts,
        df_locations,
        df_study_locations,
        df_references,
        df_links,
        df_ipds,
        df_flow_groups,
        df_flow_period_events,
    ]


def process_study_file(data_loc: str) -> List[StudyResult]:
    """
    Process a parquet file containing raw study data from ClinicalTrials.gov API.

    Reads the nested JSON structure, normalizes it, and transforms each study
    into the dimensional model schema. Studies missing NCT IDs are skipped
    with a warning.

    Args:
        data_loc: Path to parquet file containing raw API response data
                  with a 'studies' column of nested JSON.

    Returns:
        List of StudyResult objects, one per successfully processed study.

    Raises:
        Exception: Re-raises any transformation error after logging
    """
    batch_results: List[StudyResult] = []

    df_studies = pd.read_parquet(data_loc)
    df_studies = pd.json_normalize(df_studies["studies"])

    for idx, study in df_studies.iterrows():
        nct_index = SINGLE_FIELDS["nct_id"]
        nct_id = study.get(nct_index)

        if not nct_id:
            log.warning(f"Study missing NCT ID, skipping {idx}")
            continue

        try:
            result = transform_single_study(nct_id, study)
            batch_results.append(result)
        except Exception as e:
            log.exception(f"Error processing study {nct_id}: {e}")
            raise

    return batch_results


def transform_single_study(nct_id: str, study: pd.Series) -> StudyResult:
    """
    Transform a single study record into a normalised schema.

    Orchestrates all module-specific transformations (sponsors, conditions,
    interventions, etc.) and collects their outputs into a StudyResult.
    Each transformation module returns dimension records and bridge table
    records linking them to the study.

    Args:
        nct_id: The ClinicalTrials.gov identifier (e.g., 'NCT12345678').
        study: Pandas Series containing the flattened study data from
               json_normalize, with dot-notation column names.

    Returns:
        StudyResult dataclass containing lists of records for each entity
        type in the model.
    """
    study_key = generate_key(nct_id)

    result = defaultdict(list)

    result["study"].append(transform_study_fields(study_key, study))

    # sponsorCollaboratorsModule
    sponsors, study_sponsors = transform_sponsors(nct_id, study_key, study)
    result["sponsors"].extend(sponsors)
    result["study_sponsors"].extend(study_sponsors)

    collaborators, study_collaborators = transform_collaborators(study_key, study)
    result["collaborators"].extend(collaborators)
    result["study_collaborators"].extend(study_collaborators)

    # conditionsModule
    conditions, study_conditions = transform_conditions(nct_id, study_key, study)
    result["conditions"].extend(conditions)
    result["study_conditions"].extend(study_conditions)

    keywords, study_keywords = transform_keywords(study_key, study)
    result["keywords"].extend(keywords)
    result["study_keywords"].extend(study_keywords)

    # armsInterventionsModule
    arm_group_interventions = transform_arm_groups(study_key, study)
    result["arm_group_interventions"].extend(arm_group_interventions)

    interventions, study_interventions = transform_interventions(study_key, study)
    result["interventions"].extend(interventions)
    result["study_interventions"].extend(study_interventions)

    # contactsLocationsModule
    central_contacts, study_central_contacts = transform_central_contacts(
        study_key, study
    )
    result["central_contacts"].extend(central_contacts)
    result["study_central_contacts"].extend(study_central_contacts)

    locations, study_locations = transform_locations(study_key, study)
    result["locations"].extend(locations)
    result["study_locations"].extend(study_locations)

    # referencesModule
    references = transform_references(study_key, study)
    result["references"].extend(references)

    links = transform_links(study_key, study)
    result["links"].extend(links)

    ipds = transform_ipds(study_key, study)
    result["ipds"].extend(ipds)

    # outcomeMeasuresModule
    flow_groups = transform_flow_groups(study_key, study)
    result["flow_groups"].extend(flow_groups)

    flow_period_events = transform_flow_events(study_key, study)
    result["flow_period_events"].extend(flow_period_events)

    return StudyResult(
        study=result["study"],
        sponsors=result["sponsors"],
        study_sponsors=result["study_sponsors"],
        collaborators=result["collaborators"],
        study_collaborators=result["study_collaborators"],
        conditions=result["conditions"],
        study_conditions=result["study_conditions"],
        keywords=result["keywords"],
        study_keywords=result["study_keywords"],
        arm_group_interventions=result["arm_group_interventions"],
        interventions=result["interventions"],
        study_interventions=result["study_interventions"],
        central_contacts=result["central_contacts"],
        study_central_contacts=result["study_central_contacts"],
        locations=result["locations"],
        study_locations=result["study_locations"],
        references=result["references"],
        links=result["links"],
        ipds=result["ipds"],
        flow_groups=result["flow_groups"],
        flow_period_events=result["flow_period_events"],
    )
