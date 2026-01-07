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
    transform_sponsor_and_collaborators_module,
)
from include.etl.transformation.core_transformation.modules.conditions import (
    transform_conditions_module,
)
from include.etl.transformation.core_transformation.modules.arms_intervention import (
    transform_arms_interventions_module,
)

from include.etl.transformation.core_transformation.modules.outcomes import (
    transform_outcomes_module,
)

from include.etl.transformation.core_transformation.modules.contacts_location import (
    transform_contacts_location_module,
)
from include.etl.transformation.core_transformation.modules.references import (
    transform_reference_module,
)
from include.etl.transformation.core_transformation.modules.outcome_measures import (
    transform_outcome_measures_module,
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
        transform_sponsor_and_collaborators_module(nct_id, study_key, study)
    )
    result["sponsors"].extend(sponsor)
    result["study_sponsors"].extend(study_sponsor)
    result["collaborators"].extend(collaborators)
    result["study_collaborators"].extend(study_collaborators)

    # conditionsModule
    conditions, study_conditions, keywords, study_keywords = (
        transform_conditions_module(nct_id, study_key, study)
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
    ) = transform_arms_interventions_module(study_key, study)
    result["arm_groups"].extend(arm_groups)
    result["arm_interventions"].extend(arm_interventions)
    result["intervention_names"].extend(intervention_names)
    result["study_intervention_names"].extend(study_intervention_names)
    result["other_interventions_names"].extend(other_interventions_names)
    result["study_other_interventions_names"].extend(study_other_interventions_names)

    # outcomesModule
    primary_outcomes, secondary_outcomes, other_outcomes = transform_outcomes_module(
        study_key, study
    )
    result["primary_outcomes"].extend(primary_outcomes)
    result["secondary_outcomes"].extend(secondary_outcomes)
    result["other_outcomes"].extend(other_outcomes)

    # contactsLocationsModule
    central_contacts, study_central_contacts, locations, study_locations = (
        transform_contacts_location_module(study_key, study)
    )
    result["central_contacts"].extend(central_contacts)
    result["study_central_contacts"].extend(study_central_contacts)
    result["locations"].extend(locations)
    result["study_locations"].extend(study_locations)

    # referencesModule
    references, link_references, ipd_references = transform_reference_module(
        study_key, study
    )
    result["references"].extend(references)
    result["link_references"].extend(link_references)
    result["ipd_references"].extend(ipd_references)

    # outcomeMeasuresModule
    (
        outcome_measures,
        outcome_measure_groups,
        outcome_measure_denom_units,
        outcome_measure_denom_counts,
        outcome_measure_measurements,
        outcome_measure_analyses,
        outcome_measure_comparison_groups,
    ) = transform_outcome_measures_module(study_key, study)
    result["outcome_measures"].extend(outcome_measures)
    result["outcome_measure_groups"].extend(outcome_measure_groups)
    result["outcome_measure_denom_units"].extend(outcome_measure_denom_units)
    result["outcome_measure_denom_counts"].extend(outcome_measure_denom_counts)
    result["outcome_measure_measurements"].extend(outcome_measure_measurements)
    result["outcome_measure_analyses"].extend(outcome_measure_analyses)
    result["outcome_measure_comparison_groups"].extend(
        outcome_measure_comparison_groups
    )

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
        primary_outcomes=result["primary_outcomes"],
        secondary_outcomes=result["secondary_outcomes"],
        other_outcomes=result["other_outcomes"],
        central_contacts=result["central_contacts"],
        study_central_contacts=result["study_central_contacts"],
        locations=result["locations"],
        study_locations=result["study_locations"],
        references=result["references"],
        link_references=result["link_references"],
        ipd_references=result["ipd_references"],
        outcome_measures=result["outcome_measures"],
        outcome_measure_groups=result["outcome_measure_groups"],
        outcome_measure_denom_units=result["outcome_measure_denom_units"],
        outcome_measure_denom_counts=result["outcome_measure_denom_counts"],
        outcome_measure_measurements=result["outcome_measure_measurements"],
        outcome_measure_analyses=result["outcome_measure_analyses"],
        outcome_measure_comparison_groups=result["outcome_measure_comparison_groups"],
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

    # outcomesModule
    df_primary_outcomes = pd.DataFrame(results["primary_outcomes"])
    df_secondary_outcomes = pd.DataFrame(results["secondary_outcomes"])
    df_other_outcomes = pd.DataFrame(results["other_outcomes"])

    # contactsLocationsModule
    df_central_contacts = pd.DataFrame(results["central_contacts"])
    df_study_central_contacts = pd.DataFrame(results["study_central_contacts"])
    df_locations = pd.DataFrame(results["locations"])
    df_study_locations = pd.DataFrame(results["study_locations"])

    # referencesModule
    df_references = pd.DataFrame(results["references"])
    df_link_references = pd.DataFrame(results["link_references"])
    df_ipd_references = pd.DataFrame(results["ipd_references"])

    # outcomeMeasuresModule
    df_outcome_measures = pd.DataFrame(results["outcome_measures"])
    df_outcome_measure_groups = pd.DataFrame(results["outcome_measure_groups"])
    df_outcome_measure_denom_units = pd.DataFrame(
        results["outcome_measure_denom_units"]
    )
    df_outcome_measure_denom_counts = pd.DataFrame(
        results["outcome_measure_denom_counts"]
    )
    df_outcome_measure_measurements = pd.DataFrame(
        results["outcome_measure_measurements"]
    )
    df_outcome_measure_analyses = pd.DataFrame(results["outcome_measure_analyses"])
    df_outcome_measure_comparison_groups = pd.DataFrame(
        results["outcome_measure_comparison_groups"]
    )

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
        df_primary_outcomes,
        df_secondary_outcomes,
        df_other_outcomes,
        df_central_contacts,
        df_study_central_contacts,
        df_locations,
        df_study_locations,
        df_references,
        df_link_references,
        df_ipd_references,
        df_outcome_measures,
        df_outcome_measure_groups,
        df_outcome_measure_denom_units,
        df_outcome_measure_denom_counts,
        df_outcome_measure_measurements,
        df_outcome_measure_analyses,
        df_outcome_measure_comparison_groups,
    ]
