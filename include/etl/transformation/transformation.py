from typing import Dict, List, Tuple, Hashable
import logging
import pandas as pd
import numpy as np
import hashlib
import json

from transformer_config import SINGLE_FIELDS, NESTED_FIELDS
from data_quality import DataQualityHandler
from airflow.utils.context import Context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


class Transformer:
    def __init__(self, context: Context, s3_dest_hook: S3Hook = None):
        self.context = context
        self.execution_date = self.context.get("ds")
        self.log = logging.getLogger("airflow.task")

        self.s3 = s3_dest_hook or S3Hook(aws_conn_id="aws_airflow")
        self.dq_handler = DataQualityHandler()

    @staticmethod
    def generate_key(*args) -> str:
        """Generates a deterministic surrogate key from input values."""
        combined = "|".join(str(arg) for arg in args if arg is not None)
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def transform_all_studies(self, folder: str) -> None:
        for study_file in folder:
            study_file_loc = ""
            try:
                # pull from s3
                self.transform_study_file(study_file_loc)
                # checkpoint

            # inner loop will fail gracefully wherever possible and errors will only raise for critical issues
            except Exception as e:
                raise

    def transform_study_file(self, data_loc: str):
        """
        Transform a batch of raw study dicts in a file.
        Args:
            data_loc: Location of the  file
        """
        all_studies = []
        all_sponsors = []
        all_study_sponsors = []

        all_conditions = []
        all_study_conditions = []

        all_keywords = []
        all_study_keywords = []

        all_study_arm_group_interventions = []
        all_interventions = []
        all_study_interventions = []

        all_locations = []
        all_study_locations = []
        all_central_contacts = []
        all_study_central_contacts = []

        all_study_references = []
        all_study_links = []

        all_ipds = []
        all_flow_groups = []
        all_flow_period_events = []



        df_studies = pd.read_parquet(data_loc)
        df_studies = pd.json_normalize(df_studies["studies"])

        for idx, study in df_studies.iterrows():
            nct_index = SINGLE_FIELDS['nct_id']
            nct_id = study.get(nct_index)
            
            if not nct_id:
                self.log.warning(f"Study missing NCT ID, skipping {idx}")  
                continue

            study_key = self.generate_key(nct_id)

            # study
            study_record = self.extract_study_fields(study_key, study)
            all_studies.append(study_record)

            # sponsors
            sponsors, study_sponsors = self.extract_sponsors(idx, study_key, study)
            all_sponsors.extend(sponsors)
            all_study_sponsors.extend(study_sponsors)

            # conditions and keywords
            conditions, study_conditions = self.extract_conditions(idx, study_key, study)
            all_conditions.extend(conditions)
            all_study_conditions.extend(study_conditions)

            keywords, study_keywords = self.extract_keywords(idx, study_key, study)
            all_keywords.extend(keywords)
            all_study_keywords.extend(study_keywords)

            # groups and interventions
            arm_group_interventions = self.extract_arm_groups(idx, study_key, study)
            all_study_arm_group_interventions.extend(arm_group_interventions)

            interventions, study_interventions = self.extract_interventions(idx, study_key, study)
            all_interventions.extend(interventions)
            all_study_interventions.extend(study_interventions)

            # contacts and locations
            central_contacts, study_central_contacts  = self.extract_central_contacts(idx, study_key, study)
            all_central_contacts.extend(central_contacts)
            all_study_central_contacts.extend(study_central_contacts)

            locations, study_locations = self.extract_locations(idx, study_key, study)
            all_locations.extend(locations)
            all_study_locations.extend(study_locations)

            references = self.extract_references(idx, study_key, study)
            all_study_references.extend(references)

            links = self.extract_links(idx, study_key, study)
            all_study_links.extend(links)

            ipds = self.extract_ipds(idx, study_key, study)
            all_ipds.extend(ipds)

            flow_groups = self.extract_flow_groups(idx,study_key, study)
            all_flow_groups.extend(flow_groups)

            flow_period_events = self.extract_flow_events(idx, study_key, study)
            all_flow_period_events.extend(flow_period_events)





        df_studies = pd.DataFrame(all_studies)

        #sponsors and collaborators
        df_sponsors = pd.DataFrame(all_sponsors)
        df_study_sponsors = pd.DataFrame(all_study_sponsors)

        #conditions and keywords
        df_conditions = pd.DataFrame(all_conditions)
        df_study_conditions = pd.DataFrame(all_study_conditions)
        df_keywords = pd.DataFrame(all_keywords)
        df_study_keywords = pd.DataFrame(all_study_keywords)

        #arms and interventions
        df_interventions = pd.DataFrame(all_interventions)
        df_study_interventions = pd.DataFrame(all_study_interventions)
        df_arm_group_interventions = pd.DataFrame(
            all_study_arm_group_interventions
        )

        # contacts and locations
        df_central_contacts = pd.DataFrame(all_central_contacts)
        df_study_central_contacts = pd.DataFrame(all_study_central_contacts)
        df_locations = pd.DataFrame(all_locations)
        df_study_locations = pd.DataFrame(all_study_locations)

        #links and references
        df_references = pd.DataFrame(all_study_references)
        df_links = pd.DataFrame(all_study_links)

        #IPD
        df_ipds = pd.DataFrame(all_ipds)

        #Milestones
        df_flow_groups = pd.DataFrame(all_flow_groups)
        df_flow_period_events = pd.DataFrame(all_flow_period_events)

        # dedupe
        df_sponsors = df_sponsors.drop_duplicates(subset=["sponsor_key"])
        df_conditions = df_conditions.drop_duplicates(subset=["condition_key"])
        df_keywords = df_keywords.drop_duplicates(subset=["keyword_key"])
        df_interventions = df_interventions.drop_duplicates(subset=["intervention_key"])
        df_arm_group_interventions = df_arm_group_interventions.drop_duplicates(subset=["study_arm_key", "study_key", "arm_intervention_name"])
        df_locations = df_locations.drop_duplicates(subset=["location_key"])
        df_central_contacts = df_central_contacts.drop_duplicates(subset=["contact_key"])

        df_references = df_references.drop_duplicates(subset=["study_key", "ref_key"])
        df_links = df_links.drop_duplicates(subset=["study_key", "link_key", "url"])
        df_ipds = df_ipds.drop_duplicates(subset=["study_key", "ipd_key"])

        df_flow_groups = df_flow_groups.drop_duplicates(subset=["study_key", "group_key"])


        #Aggregate to mitigate data quality errors. check docs/data_quality_issues.md for details
        df_flow_period_events = df_flow_period_events.groupby(
            ['study_key', 'period_title', 'event_class', 'event_type', 'group_id'],
            as_index=False
        ).agg({
            'num_subjects': 'sum',
            'period_key': 'first'
        })



        # load
        return df_studies, df_sponsors, df_study_sponsors

    @staticmethod
    def extract_study_fields(study_key: str, study_data: pd.Series) -> Dict:
        study_record = dict()

        study_record["study_key"] = study_key
        for entity_key in SINGLE_FIELDS:
            index_field = SINGLE_FIELDS.get(entity_key)

            study_record[entity_key] = study_data.get(index_field)

        return study_record


    def extract_sponsors(self, idx: Hashable, study_key: str, study_data: pd.Series) -> Tuple:
        """
        Extract sponsors from a single study.
        Args:
            idx: The index of the study on the current page
            study_key: The generated key for this study
            study_data: The nested dict for one study (not a DataFrame)
        Returns:
            Tuple of (sponsors_list, study_sponsors_list)
        """

        sponsors = []
        study_sponsors = []

        # Extract lead sponsor
        lead_sponsor_index = NESTED_FIELDS["sponsor"]["index_field"]

        # sponsor name and class are scalar values and MUST be extracted directly
        lead_sponsor_name = study_data.get(f'{lead_sponsor_index}.name')
        lead_sponsor_class = study_data.get(f'{lead_sponsor_index}.class')

        if pd.notna(lead_sponsor_name) and pd.notna(lead_sponsor_class):
            sponsor_key = self.generate_key(
                lead_sponsor_name, lead_sponsor_class
            )
            sponsors.append(
                {
                    "sponsor_key": sponsor_key,
                    "name": lead_sponsor_name,
                    "sponsor_class": lead_sponsor_class,
                }
            )

            study_sponsors.append(
                {"study_key": study_key, "sponsor_key": sponsor_key, "is_lead": True}
            )
        else:
            self.log.warning(f"No lead sponsor found for study {study_key}, page - index {idx}")


        # Extract collaborators
        collaborators_index = NESTED_FIELDS["collaborators"]["index_field"]
        collaborators_list = study_data.get(collaborators_index)

        if isinstance(collaborators_list, (list, np.ndarray)) and len(collaborators_list) > 0:
            for collaborator in collaborators_list:
                sponsor_key = self.generate_key(
                    collaborator.get("name"), collaborator.get("class")
                )

                sponsors.append(
                    {
                        "sponsor_key": sponsor_key,
                        "name": collaborator.get("name"),
                        "sponsor_class": collaborator.get("class"),
                    }
                )

                study_sponsors.append(
                    {"study_key": study_key, "sponsor_key": sponsor_key, "is_lead": False}
                )

        return sponsors, study_sponsors


    def extract_conditions(self, idx: Hashable, study_key: str, study_data: pd.Series) -> Tuple:
        conditions = []
        study_conditions = []

        conditions_index = NESTED_FIELDS["conditions"]["index_field"]
        conditions_list = study_data.get(conditions_index)


        if isinstance(conditions_list, (list, np.ndarray)) and len(conditions_list) > 0:
            for condition in conditions_list:
                condition_key = self.generate_key(condition)

                conditions.append(
                    {"condition_key": condition_key, "condition_name": condition}
                )

                study_conditions.append(
                    {
                        "study_key": study_key,
                        "condition_key": condition_key,
                    }
                )

        else:
            self.log.warning(f"No conditions found for study {study_key}, page - index {idx}")

        return conditions, study_conditions


    def extract_keywords(self, idx: Hashable, study_key: str, study_data: pd.Series) -> Tuple:
        keywords = []
        study_keywords = []

        keywords_index = NESTED_FIELDS["keywords"]["index_field"]
        keywords_list = study_data.get(keywords_index)

        if isinstance(keywords_list, (list, np.ndarray)) and len(keywords_list) > 0:

            for keyword in keywords_list:
                keyword_key = self.generate_key(keyword)

                keywords.append({"keyword_key": keyword_key, "keyword_name": keyword})

                study_keywords.append(
                    {
                        "study_key": study_key,
                        "keyword_key": keyword_key,
                    }
                )
        return keywords, study_keywords


    def extract_interventions(self, idx: Hashable, study_key: str, study_data: pd.Series) -> Tuple:
        intervention_names = []
        study_interventions = []

        interventions_index = NESTED_FIELDS["interventions"]["index_field"]
        interventions_list = study_data.get(interventions_index)

        if isinstance(interventions_list, (list, np.ndarray)) and len(interventions_list) > 0:
            for intervention in interventions_list:
                main_name = intervention.get("name")
                intervention_type = intervention.get("type")
                description = intervention.get("description")

                intervention_key = self.generate_key(main_name, intervention_type)
                intervention_names.append({
                    "intervention_key": intervention_key,
                    "intervention_name": main_name,
                    "intervention_type": intervention_type,
                    "description": description,
                    "is_primary_name": True
                })

                study_interventions.append({
                    "study_key": study_key,
                    "intervention_key": intervention_key,
                    "is_primary_name": True
                })


                other_names = intervention.get("otherNames")
                if isinstance(other_names, (list, np.ndarray)) and len(other_names) > 0:
                    for other_name in other_names:
                        if other_name == main_name:
                            continue  # some studies put the main name in the list of other names

                        intervention_key = self.generate_key(other_name, intervention_type)
                        intervention_names.append({
                            "intervention_key": intervention_key,
                            "intervention_name": other_name,
                            "intervention_type": intervention_type,
                            "description": description,  # inherits from parent

                        })

                        study_interventions.append({
                            "study_key": study_key,
                            "intervention_key": intervention_key,
                            "is_primary_name": False
                        })
        else:
            pass
            # self.log.warning(f"No interventions found for study {study_key}, {idx}") #noisy


        return intervention_names, study_interventions


    def extract_arm_groups(self, idx: Hashable, study_key: str, study_data: pd.Series) -> List:
        study_arms_interventions = []

        study_arms_index = NESTED_FIELDS["arm_groups"]["index_field"]
        study_arms_list = study_data.get(study_arms_index)

        if isinstance(study_arms_list, (list, np.ndarray)) and len(study_arms_list) > 0:
            for study_arm in study_arms_list:
                study_arm_label = study_arm.get("label")
                study_arm_description = study_arm.get("description")
                study_arm_type = study_arm.get("type")

                arm_intervention_key = self.generate_key(study_key, study_arm_label, study_arm_description,
                                                         study_arm_type)

                arm_interventions = study_arm.get("interventionNames")
                if isinstance(arm_interventions, (list, np.ndarray)) and len(arm_interventions) > 0:

                    for intervention in arm_interventions:
                        study_arms_interventions.append(
                            {
                                "study_key": study_key,
                                "arm_intervention_key": arm_intervention_key,
                                "arm_label": study_arm_label,
                                "arm_description": study_arm_description,
                                "arm_type": study_arm_type,
                                "arm_intervention_name": intervention,
                            }
                        )
                else:
                    study_arms_interventions.append(
                        {
                            "study_key": study_key,
                            "arm_intervention_key": arm_intervention_key,
                            "arm_label": study_arm_label,
                            "arm_description": study_arm_description,
                            "arm_type": study_arm_type,
                            "arm_intervention_name": None,
                        }
                    )

        # else:
        #     self.log.warning(f"No arms found for study {study_key}, page - index {idx}") #too noisy

        return study_arms_interventions



    def extract_central_contacts(self, idx: Hashable, study_key: str, study_data: pd.Series) -> Tuple:
        central_contacts = []
        study_central_contacts = []

        central_contacts_index = NESTED_FIELDS["central_contacts"]["index_field"]
        central_contacts_list = study_data.get(central_contacts_index)

        if isinstance(central_contacts_list, (list, np.ndarray)) and len(central_contacts_list) > 0:

            for central_contact in central_contacts_list:
                name = central_contact.get("name")
                role = central_contact.get("role")
                phone = central_contact.get("phone")
                email = central_contact.get("email")

                central_contact_key = self.generate_key(name, role, phone, email)

                central_contacts.append(
                    {"contact_key": central_contact_key,
                     "contact_name": name,
                     "contact_role": role,
                     "contact_phone": phone,
                     "contact_email": email,
                     })

                study_central_contacts.append(
                    {
                        "study_key": study_key,
                        "contact_key": central_contact_key,
                    }
                )

        return central_contacts, study_central_contacts

    def extract_locations(self, idx: Hashable, study_key: str, study_data: pd.Series) -> Tuple:
        """
        Extract locations with status resolution
        """
        locations = []
        study_locations = []


        locations_index = NESTED_FIELDS["locations"]["index_field"]
        locations_list = study_data.get(locations_index)

        if isinstance(locations_list, (list, np.ndarray)) and len(locations_list) > 0:
            for location in locations_list:
                facility = location.get("facility")
                city = location.get("city")
                state = location.get("state")
                country = location.get("country")

                location_key = self.generate_key(facility, city, state, country)
                curr_location = {
                    "location_key": location_key,
                    "facility": facility,
                    "city": city,
                    "state": state,
                    "country": state,
                    "status": location.get("status")

                }
                geopoint = location.get("geoPoint")
                if isinstance(geopoint, dict) and geopoint:
                    curr_location["lat"] = float(geopoint.get("lat")) if geopoint.get("lat") else None
                    curr_location["lon"] = float(geopoint.get("lon")) if geopoint.get("lon") else None

                locations.append(curr_location)

                # resolve location status

                overall_status = study_data.get("protocolSection.statusModule.overallStatus")

                statuses = [loc.get("status") for loc in locations if loc.get("status")]
                unique_statuses = set(statuses)


                resolved_status, status_type = self.dq_handler.resolve_location_status(overall_status, unique_statuses)

                study_locations.append({
                    "study_key": study_key,
                    "location_key": location_key,
                    "status": resolved_status,
                    "status_type": status_type, #aCTUAL or inferred
                    "contacts": location.get("contacts"),

                })

        return locations, study_locations

    def extract_references(self, idx: Hashable, study_key: str, study_data: pd.Series) -> List:

        study_references = []

        references_index = NESTED_FIELDS["references"]["index_field"]
        references_list = study_data.get(references_index)

        if isinstance(references_list, (list, np.ndarray)) and len(references_list) > 0:

            for reference in references_list:
                pmid = reference.get('pmid')
                reference_key = self.generate_key(study_key, pmid)
                study_references.append({
                    "study_key": study_key,
                    "ref_key": reference_key,
                    "pmid": pmid,
                    "type": reference.get("type"),
                    "citation": reference.get("citation")
                })

        return study_references

    def extract_links(self, idx: Hashable, study_key: str, study_data: pd.Series) -> List:
        study_links = []

        links_index = NESTED_FIELDS["see_also"]["index_field"]
        links_list = study_data.get(links_index)

        if isinstance(links_list, (list, np.ndarray)) and len(links_list) > 0:

            for link in links_list:
                label = link.get('label')
                study_links.append({
                    "study_key": study_key,
                    "link_key": link,
                    "label": label,
                    "url": link.get("url")
                })

        return study_links

    def extract_ipds(self, idx: Hashable, study_key: str, study_data: pd.Series) -> List:
        study_ipds = []

        ipds_index = NESTED_FIELDS["avail_ipds"]["index_field"]
        ipds_list = study_data.get(ipds_index)

        if isinstance(ipds_list, (list, np.ndarray)) and len(ipds_list) > 0:

            for ipd in ipds_list:
                ipd_id = ipd.get('id')
                ipd_type = ipd.get('type')
                ipd_url = ipd.get('url')

                ipd_key = self.generate_key(study_key, ipd_id, ipd_type, ipd_url)
                study_ipds.append({
                    "study_key": study_key,
                    "ipd_key": ipd_key,
                    "id": ipd_id,
                    "type": ipd_type,
                    "url": ipd_url,
                    "comment": ipd.get("comment")
                })
        return study_ipds


    def extract_flow_groups(self, idx: Hashable, study_key: str, study_data: pd.Series) -> List:
        study_flow_groups = []

        flow_index = NESTED_FIELDS["flow_groups"]["index_field"]
        flow_group_list = study_data.get(flow_index)

        if isinstance(flow_group_list, (list, np.ndarray)) and len(flow_group_list) > 0:
            for flow in flow_group_list:
                group_id = flow.get('id')
                group_key = self.generate_key(study_key, group_id)

                study_flow_groups.append({
                    "study_key": study_key,
                    "group_key": group_key,
                    "id": group_id,
                    "title": flow.get("title"),
                    "description": flow.get("description")

                })

        return study_flow_groups

    def extract_flow_events(self, idx: Hashable, study_key: str, study_data: pd.Series) -> List:
        flow_period_events = []

        flow_index = NESTED_FIELDS["flow_periods"]["index_field"]
        flow_period_list = study_data.get(flow_index)

        if isinstance(flow_period_list, (list, np.ndarray)) and len(flow_period_list) > 0:
            for period in flow_period_list:
                period_title = period.get('title')
                period_key = self.generate_key(study_key, period_title)

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

                                "group_id":"UNKNOWN",
                                "num_subjects": None, #not 0

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
                                "group_id":"UNKNOWN",
                                "num_subjects": None, #not 0

                            })



        return flow_period_events


