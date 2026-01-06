from typing import List, Dict
from collections import defaultdict
import logging
import pandas as pd

from include.etl.transformation.config import SCALAR_FIELDS
from include.etl.transformation.utils import generate_key
from include.etl.transformation.models import StudyResult

from include.etl.transformation.core_transformation.modules.study_main import (
    transform_scalar_fields,
)

from include.etl.transformation.core_transformation.modules.identification import (
    transform_identification_module,
)
from include.etl.transformation.core_transformation.modules.sponsor_collaborator import (
    transform_sponsor_and_collaborators,
)
from include.etl.transformation.core_transformation.modules.conditions import (
    transform_conditions,
)
from include.etl.transformation.core_transformation.modules.arms_intervention import (
    transform_arms_interventions,
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


def process_study_file(file_loc: str) -> List[StudyResult]:
    """
    Process a parquet file containing raw study data from ClinicalTrials.gov API.

    Reads the nested JSON structure, normalizes it, and transforms each study
    into the dimensional model schema. Studies missing NCT IDs are skipped
    with a warning.

    Args:
        file_loc: Path to parquet file containing raw API response data
                  with a 'studies' column of nested JSON.

    Returns:
        List of StudyResult objects, one per successfully processed study.

    Raises:
        Exception: Re-raises any transformation error after logging
    """
    batch_results: List[StudyResult] = []

    df_studies = pd.read_parquet(file_loc)
    df_studies = pd.json_normalize(df_studies["studies"])

    for idx, study in df_studies.iterrows():
        nct_index = SCALAR_FIELDS["nct_id"]
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

    # scalar fields
    study_fields = transform_scalar_fields(study_key, study)
    result["studies"].append(study_fields)

    # identificationModule
    secondary_ids, nct_aliases = transform_identification_module(study_key, study)
    result["secondary_ids"].extend(secondary_ids)
    result["nct_aliases"].extend(nct_aliases)

    # sponsorCollaboratorsModule
    sponsor, study_sponsor, collaborators, study_collaborators = (
        transform_sponsor_and_collaborators(nct_id, study_key, study)
    )
    result["sponsors"].extend(sponsor)
    result["study_sponsors"].extend(study_sponsor)
    result["collaborators"].extend(collaborators)
    result["study_collaborators"].extend(study_collaborators)

    # conditionsModule
    conditions, study_conditions, keywords, study_keywords = transform_conditions(
        nct_id, study_key, study
    )
    result["conditions"].extend(conditions)
    result["study_conditions"].extend(study_conditions)
    result["keywords"].extend(keywords)
    result["study_keywords"].extend(study_keywords)

    # armsInterventionsModule
    (
        arm_groups,
        arm_interventions,
        intervention_names,
        study_intervention_names,
        other_interventions_names,
        study_other_interventions_names,
    ) = transform_arms_interventions(study_key, study)
    result["arm_groups"].extend(arm_groups)
    result["arm_interventions"].extend(arm_interventions)
    result["intervention_names"].extend(intervention_names)
    result["study_intervention_names"].extend(study_intervention_names)
    result["other_interventions_names"].extend(other_interventions_names)
    result["study_other_interventions_names"].extend(study_other_interventions_names)

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
        studies=result["studies"],
        secondary_ids=result["secondary_ids"],
        nct_aliases=result["nct_aliases"],
        sponsors=result["sponsors"],
        study_sponsors=result["study_sponsors"],
        collaborators=result["collaborators"],
        study_collaborators=result["study_collaborators"],
        conditions=result["conditions"],
        study_conditions=result["study_conditions"],
        keywords=result["keywords"],
        study_keywords=result["study_keywords"],
        arm_groups=result["arm_groups"],
        arm_interventions=result["arm_interventions"],
        intervention_names=result["intervention_names"],
        study_intervention_names=result["study_intervention_names"],
        other_interventions_names=result["other_interventions_names"],
        study_other_interventions_names=result["study_other_interventions_names"],
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

    # identificationModule
    df_secondary_ids = pd.DataFrame(results["secondary_ids"])
    df_nct_aliases = pd.DataFrame(results["nct_aliases"])

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
    df_arm_groups = pd.DataFrame(results["arm_groups"])
    df_arm_interventions = pd.DataFrame(results["arm_interventions"])
    df_intervention_names = pd.DataFrame(results["intervention_names"])
    df_study_intervention_names = pd.DataFrame(results["study_intervention_names"])
    df_other_interventions_names = pd.DataFrame(results["other_interventions_names"])
    df_study_other_interventions_names = pd.DataFrame(
        results["study_other_interventions_names"]
    )

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
    df_intervention_names = df_intervention_names.drop_duplicates(
        subset=["intervention_key"]
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
        df_secondary_ids,
        df_nct_aliases,
        df_sponsors,
        df_study_sponsors,
        df_collaborators,
        df_study_collaborators,
        df_conditions,
        df_study_conditions,
        df_keywords,
        df_study_keywords,
        df_arm_groups,
        df_arm_interventions,
        df_intervention_names,
        df_study_intervention_names,
        df_other_interventions_names,
        df_study_other_interventions_names,
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
