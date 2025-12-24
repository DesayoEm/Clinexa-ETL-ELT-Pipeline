
### Source: https://clinicaltrials.gov/data-api/about-api/study-data-structure


### NESTED FIELDS

## SponsorCollaboratorsModule

### sponsors

**Index Field(s):** 
- `protocolSection.sponsorCollaboratorsModule.leadSponsor`
- `protocolSection.sponsorCollaboratorsModule.collaborators[]`

**Object Type**: Simple dict (leadSponsor) / Array of dicts (collaborators)

**Description**: Organizations responsible for the study.

- **Lead Sponsor**: Exactly 1 per study. The organization or person who initiates the study and has authority and control over it.
- **Collaborators**: 0 to many. Other organizations providing support (funding, design, implementation, data analysis, reporting).


#### Fields

##### `name`
- **Description**: Name of the sponsoring entity or individual
- **Data Type**: Text
- **Limit**: 160 characters

##### `class`
- **Description**: Category of the sponsoring organization
- **Data Type**: Enum(AgencyClass)
- **Enum Values**:
  - `NIH` — National Institutes of Health
  - `FED` — Other Federal Agency
  - `OTHER_GOV` — Other Governmental (non-US)
  - `INDIV` — Individual
  - `INDUSTRY` — Industry/Pharmaceutical
  - `NETWORK` — Research Network
  - `AMBIG` — Ambiguous
  - `OTHER` — Other
  - `UNKNOWN` — Unknown



#### Model Mapping

- **Target Table**: `dim_sponsors`
- **Bridge Table**: `bridge_study_sponsors` 
- **Discriminator**: `is_lead_sponsor` (boolean) — added during transformation

---


## ConditionsModule 

### conditions

**Index Field(s):** `protocolSection.conditionsModule.conditions`

**Object Type**: Simple array

**Description**: The name(s) of the disease(s) or condition(s) studied in the clinical study, or the focus of the clinical study.

#### Model Mapping
- **Target Table**: `conditions`
- **Bridge Table**: `bridge_study_conditions` 
- **column_name**: `condition_name` 

---

### keywords

**Index Field(s):** `protocolSection.conditionsModule.keywords`

**Object Type**: Simple array

**Description**: Words or phrases that best describe the protocol. Keywords help users find studies in the database

#### Model Mapping
- **Target Table**: `keywords`
- **Bridge Table**: `bridge_study_keywords` 
- **column_name**: `keyword` 

---

## armsInterventionsModule 

### interventions

**Index Field(s):** `protocolSection.armsInterventionsModule.interventions`

**Object Type**: Array of Dicts

**Description**: The intervention(s) associated with each arm or group; at least one intervention must be specified for interventional studies. 

For observational studies, the intervention(s)/exposure(s) of interest


#### Fields

##### `name`
- **Description**: brief descriptive name used to refer to the intervention(s) studied in each arm of the clinical study. 
- **Data Type**: Text
- **Limit**: 200 characters

##### `description`
- **Description**: Details that can be made public about the intervention, other than the Intervention Name(s) and Other Intervention Name(s), sufficient to distinguish the intervention from other, similar interventions studied in the same or another clinical study. 
- **Data Type**: Text
- **Limit**: 1000 characters

#### Nested Fields
##### `otherNames`
- **Description**:  Other current and former name(s) or alias(es), if any, different from the Intervention Name. 
- **Data Type**: [Text] / Simple array
- **Limit**: 160 characters


#### Model Mapping
- **Target Table**: `interventions`
- **Bridge Table**: `bridge_study_interventions` 


---

### arm_groups

**Index Field(s):** `protocolSection.armsInterventionsModule.armGroups`

**Object Type**: Array of Dicts

**Description**: A description of each arm of the clinical trial that indicates its role in the clinical trial


#### Fields

##### `label`
- **Description**: The short name used to identify the arm.
- **Data Type**: Text
- **Limit**: 100 characters

##### `type`
- **Description**: The role of each arm in the clinical trial.
- **Data Type**: Enum(ArmGroupType)
- **Source Values**: 

- * EXPERIMENTAL - Experimental
- * ACTIVE_COMPARATOR - Active Comparator
- * PLACEBO_COMPARATOR - Placebo Comparator
- * SHAM_COMPARATOR - Sham Comparator
- * NO_INTERVENTION - No Intervention
- * OTHER - Other


##### `description`
- **Description**:  Additional descriptive information (including which interventions are administered in each arm) to differentiate each arm from other arms in the clinical trial.
- **Data Type**: Text
- **Limit**: 999 characters


#### Nested Fields
##### `interventionNames`
- **Description**:  A brief descriptive name used to refer to the intervention(s) studied in each arm of the clinical study. 
- **Data Type**: [Text] / Simple array
- **Limit**: 200 characters


#### Model Mapping
- **Target Table**: `study_arms`
- **Bridge Table**: `bridge_study_arms` 

#how do arms tie back to interventions?


---


## contactsLocationsModule

    "locations": {
        **Index Field:** "protocolSection.contactsLocationsModule.locations",
        **Object_type**: "array_of_dicts",
        **Table_name**: "sites",
        **Bridge_table_name**: "study_sites",
        **Fields**: [
            ("site_facility", "facility"),
            ("city", "city"),
            ("state", "state"),
            ("zip", "zip"),
            ("country", "country"),
            ("site_status", "status"),
        ],
        "nested": {
            "geoPoint": {
                **Object_type**: "simple_array",
                 **Fields**: ["lat", "lon"],
            },

            "contacts": {
                **Object_type**: "nested_array_of_dicts",
                **Table_name**: "contacts",
                **Bridge_table_name**: "location_contacts",
                **Fields**: [
                    ("name", "name"),
                    ("role", "role"),
                    ("email", "email"),
                    ("phone", "phone"),
                    ("phoneExt", "phoneExt")
                ]
            }
        },
        "transformer_method": "extract_contacts"
    },

    "central_contacts": {
        **Index Field:** "protocolSection.contactsLocationsModule.centralContacts",
        **Object_type**: "array_of_dicts",
        **Table_name**: "contacts",
        **Bridge_table_name**: "study_contacts",
        **Fields**: [
            ("name", "name"),
            ("role", "role"),
            ("email", "email"),
            ("phone", "phone"),
            ("phoneExt", "phoneExt")
        ],
        "transformer_method": "extract_contacts"
    },

    "overall_officials": {
        **Index Field:** "protocolSection.contactsLocationsModule.overallOfficials",
        **Object_type**: "array_of_dicts",
        **Table_name**: "investigators",
        **Bridge_table_name**: "study_investigators",
        **Fields**: [
            ("name", "name"),
            ("affiliation", "affiliation"),
            ("role", "role")
        ],
        "transformer_method": "extract_officials"
    },

    "primary_outcomes": {
        **Index Field:** "protocolSection.outcomesModule.primaryOutcomes",
        **Object_type**: "array_of_dicts",
        **Table_name**: "study_outcomes",
        **Fields**: [
            ("measure", "measure"),
            ("description", "description"),
            ("timeFrame", "timeFrame")
        ],
        "transformer_method": "extract_outcomes",
        "outcome_type": "PRIMARY",
    },

    "secondary_outcomes": {
        **Index Field:** "protocolSection.outcomesModule.secondaryOutcomes",
        **Object_type**: "array_of_dicts",
        **Table_name**: "study_outcomes",
        **Fields**: [
            ("measure", "measure"),
            ("description", "description"),
            ("timeFrame", "timeFrame")
        ],
        "transformer_method": "extract_outcomes",
        "outcome_type": "SECONDARY",
    },

    "other_outcomes": {
        **Index Field:** "protocolSection.outcomesModule.otherOutcomes",
        **Object_type**: "array_of_dicts",
        **Table_name**: "study_outcomes",
        **Fields**: [
            ("measure", "measure"),
            ("description", "description"),
            ("timeFrame", "timeFrame")
        ],
        "transformer_method": "extract_outcomes",
        "outcome_type": "OTHER",
    },

    "references": {
        **Index Field:** "protocolSection.referencesModule.references",
        **Object_type**: "array_of_dicts",
        **Table_name**: "study_publications",
        "extract_fields": ["pmid", **Object_type**, "citation"],
    },

    "retractions": {
        **Index Field:** "protocolSection.referencesModule.retractions",
        **Object_type**: "array_of_dicts",
        **Table_name**: "study_retractions",
        **Fields**: [
            ("pmid", "pmid"),
            ("status", "status")
        ],
        "transformer_method": "extract_outcomes",
    },

    "see_also": {
        **Index Field:** "protocolSection.referencesModule.seeAlsoLinks",
        **Object_type**: "array_of_dicts",
        **Table_name**: "study_see_also",
        **Fields**: [
            ("label", "label"),
            ("url", "url")
        ],
        "transformer_method": "extract_see_also"
    },

    "phases": {
        **Index Field:** "protocolSection.designModule.phases",
        **Object_type**: "simple_array",
        **Table_name**: "phases",
        **Bridge_table_name**: "study_phases",
        **Field_name**: "phase",
        "transformer_method": "extract_study_phases"
    },


    "std_ages": {
        **Index Field:** "protocolSection.eligibilityModule.stdAges",
        **Object_type**: "simple_array",
        **Table_name**: "age_groups",
        **Bridge_table_name**: "study_age_groups",
        **Field_name**: "age_group",
        "transformer_method": "extract_age_group"
    },

    "ipd_info_types": {
        **Index Field:** "protocolSection.ipdSharingStatementModule.infoTypes",
        **Object_type**: "simple_array",
        **Table_name**: "ipd_info_types",
        **Bridge_table_name**: "study_ipd_info_types",
        **Field_name**: "info_type",
        "transformer_method": "extract_ipd_info_types"
    },
#NOT EVERYTHING NEEDS A BRIDGE
    "secondary_id_infos": {
        **Index Field:** "protocolSection.identificationModule.secondaryIdInfos",
        **Object_type**: "array_of_dicts",
        **Table_name**: "secondary_ids",
        **Bridge_table_name**: "study_secondary_ids",
        **Fields**: [
            ("id", "id"),
            (**Object_type**, **Object_type**),
            ("domain", "domain"),
            ("link", "link")
        ],
        "transformer_method": "extract_id_infos"

    },
    "nct_id_aliases": {
        **Index Field:** "protocolSection.identificationModule.nctIdAliases",
        **Object_type**: "simple_array",
        **Table_name**: "nct_aliases",
        **Bridge_table_name**: "study_nct_aliases",
        **Field_name**: "alias_nct_id",
        "transformer_method": "extract_nct_id_aliases"
    },

    # ===== DERIVED SECTION (MeSH) =====
    # CONDITION MESH TERMS


    "condition_mesh_terms": {
        **Index Field:** "derivedSection.conditionBrowseModule.meshes",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            ("id", "id"),
            ("term", "term")
        ],
        **Table_name**: "condition_mesh_terms",
        **Bridge_table_name**: "study_conditions_mesh",
        "is_primary": True,
        "transformer_method": "extract_condition_mesh"
    },

    "condition_mesh_ancestors": {
        **Index Field:** "derivedSection.conditionBrowseModule.ancestors",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            ("id", "id"),
            ("term", "term")
        ],
        **Table_name**: "condition_mesh_terms",
        **Bridge_table_name**: "study_conditions_mesh",
        "is_primary": False,
        "transformer_method": "extract_condition_mesh"
    },

    "intervention_mesh_terms": {
        **Index Field:** "derivedSection.interventionBrowseModule.meshes",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            ("id", "id"),
            ("term", "term")
        ],
        **Table_name**: "intervention_mesh_terms",
        **Bridge_table_name**: "study_interventions_mesh",
        "is_primary": True,
        "transformer_method": "extract_intervention_mesh"
    },

    "intervention_mesh_ancestors": {
        **Index Field:** "derivedSection.interventionBrowseModule.ancestors",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            ("id", "id"),
            ("term", "term")
        ],
        **Table_name**: "intervention_mesh_terms",
        **Bridge_table_name**: "study_interventions_mesh",
        "is_primary": False,
        "transformer_method": "extract_intervention_mesh"
    },

    "large_documents": {
        **Index Field:** "documentSection.largeDocumentModule.largeDocs",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            ("typeAbbrev", "typeAbbrev"),
            ("hasProtocol", "hasProtocol"),
            ("hasSap", "hasSap"),
            ("hasIcf", "hasIcf"),
            ("label", "label"),
            ("date", "date"),
            ("uploadDate", "uploadDate"),
            ("filename", "filename"),
            ("size", "size"),
        ],
        **Table_name**: "study_documents",
        "transformer_method": "extract_large_documents"
    },

    "unposted_events": {
        **Index Field:** "annotationSection.annotationModule.unpostedAnnotation.unpostedEvents",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            (**Object_type**, **Object_type**),
            ("date", "date"),
            ("dateUnknown", "dateUnknown"),
        ],
        **Table_name**: "unposted_events",
        **Bridge_table_name**: "study_unposted_events",
        "transformer_method": "extract_unposted_events"
    },

    "violation_events": {
        **Index Field:** "annotationSection.annotationModule.violationAnnotation.violationEvents",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            (**Object_type**, **Object_type**),
            ("description", "description"),
            ("creationDate", "creationDate"),
            ("issuedDate", "issuedDate"),
            ("releaseDate", "releaseDate"),
            ("postedDate", "postedDate"),
        ],
        **Table_name**: "violation_events",
        **Bridge_table_name**: "study_violation_events",
        "transformer_method": "extract_violation_events"
    },

    "removed_countries": {
        **Index Field:** "derivedSection.miscInfoModule.removedCountries",
        **Object_type**: "simple_array",
        **Table_name**: "countries",
        **Bridge_table_name**: "study_removed_countries",
        **Field_name**: "country",
        "transformer_method": "extract_removed_countries"
    },

    "submission_infos": {
        **Index Field:** "derivedSection.miscInfoModule.submissionTracking.submissionInfos",
        **Object_type**: "array_of_dicts",
        **Fields**: [
            ("releaseDate", "releaseDate"),
            ("unreleaseDate", "unreleaseDate"),
            ("unreleaseDateUnknown", "unreleaseDateUnknown"),
            ("resetDate", "resetDate"),
            ("mcpReleaseN", "mcpReleaseN")
        ],
        **Table_name**: "submission_tracking",
        **Bridge_table_name**: "study_submission_tracking",
        "transformer_method": "extract_submission_infos"
    },


    # # PARTICIPANT FLOW GROUPS
    # 'participant_flow_groups': {
    #     'path': 'resultsSection.participantFlowModule.groups',
    #     'type': 'array_of_dicts',
    #     'table_name': 'flow_groups',
    #     'bridge_table_name': 'study_flow_groups',
    #     'extract_fields': ['id', 'title', 'description']
    # },
    #
    # # PARTICIPANT FLOW PERIODS
    # 'participant_flow_periods': {
    #     'path': 'resultsSection.participantFlowModule.periods',
    #     'type': 'array_of_dicts',
    #     'table_name': 'flow_periods',
    #     'bridge_table_name': 'study_flow_periods',
    #     'extract_fields': ['title'],
    #     'nested_arrays': {
    #         'milestones': ['type', 'comment', 'achievements'],
    #         'dropWithdraws': ['type', 'comment', 'reasons']
    #     }
    # },
    #
    # # BASELINE GROUPS
    # 'baseline_groups': {
    #     'path': 'resultsSection.baselineCharacteristicsModule.groups',
    #     'type': 'array_of_dicts',
    #     'table_name': 'baseline_groups',
    #     'bridge_table_name': 'study_baseline_groups',
    #     'extract_fields': ['id', 'title', 'description']
    # },
    #
    # # BASELINE DENOMS
    # 'baseline_denoms': {
    #     'path': 'resultsSection.baselineCharacteristicsModule.denoms',
    #     'type': 'array_of_dicts',
    #     'table_name': 'baseline_denoms',
    #     'extract_fields': ['units'],
    #     'nested_arrays': {
    #         'counts': ['groupId', 'value']
    #     }
    # },
    #
    # # BASELINE MEASURES
    # 'baseline_measures': {
    #     'path': 'resultsSection.baselineCharacteristicsModule.measures',
    #     'type': 'array_of_dicts',
    #     'table_name': 'baseline_measures',
    #     'extract_fields': [
    #         'title', 'description', 'populationDescription',
    #         'paramType', 'dispersionType', 'unitOfMeasure',
    #         'calculatePct', 'denomUnitsSelected'
    #     ],
    #     'nested_arrays': {
    #         'denoms': ['units', 'counts'],
    #         'classes': ['title', 'denoms', 'categories']
    #     }
    # },
    #
    # # OUTCOME MEASURES
    # 'outcome_measures_results': {
    #     'path': 'resultsSection.outcomeMeasuresModule.outcomeMeasures',
    #     'type': 'array_of_dicts',
    #     'table_name': 'outcome_measure_results',
    #     'extract_fields': [
    #         'type', 'title', 'description', 'populationDescription',
    #         'reportingStatus', 'anticipatedPostingDate',
    #         'paramType', 'dispersionType', 'unitOfMeasure',
    #         'calculatePct', 'timeFrame', 'typeUnitsAnalyzed',
    #         'denomUnitsSelected'
    #     ],
    #     'nested_arrays': {
    #         'groups': ['id', 'title', 'description'],
    #         'denoms': ['units', 'counts'],
    #         'classes': ['title', 'denoms', 'categories'],
    #         'analyses': [
    #             'groupIds', 'paramType', 'paramValue',
    #             'dispersionType', 'dispersionValue',
    #             'statisticalMethod', 'statisticalComment',
    #             'pValue', 'pValueComment',
    #             'ciNumSides', 'ciPctValue', 'ciUpperLimit', 'ciLowerLimit',
    #             'estimateComment', 'testedNonInferiority',
    #             'nonInferiorityType', 'nonInferiorityComment',
    #             'otherAnalysisDescription', 'groupDescription'
    #         ]
    #     }
    # },
    #
    # # ADVERSE EVENT GROUPS
    # 'adverse_event_groups': {
    #     'path': 'resultsSection.adverseEventsModule.eventGroups',
    #     'type': 'array_of_dicts',
    #     'table_name': 'ae_groups',
    #     'bridge_table_name': 'study_ae_groups',
    #     'extract_fields': [
    #         'id', 'title', 'description',
    #         'deathsNumAffected', 'deathsNumAtRisk',
    #         'seriousNumAffected', 'seriousNumAtRisk',
    #         'otherNumAffected', 'otherNumAtRisk'
    #     ]
    # },
    #
    # # SERIOUS ADVERSE EVENTS
    # 'serious_adverse_events': {
    #     'path': 'resultsSection.adverseEventsModule.seriousEvents',
    #     'type': 'array_of_dicts',
    #     'table_name': 'adverse_events',
    #     'extract_fields': [
    #         'term', 'organSystem', 'sourceVocabulary',
    #         'assessmentType', 'notes'
    #     ],
    #     'nested_arrays': {
    #         'stats': ['groupId', 'numEvents', 'numAffected', 'numAtRisk']
    #     },
    #     'severity': 'SERIOUS'
    # },
    #
    # # OTHER ADVERSE EVENTS
    # 'other_adverse_events': {
    #     'path': 'resultsSection.adverseEventsModule.otherEvents',
    #     'type': 'array_of_dicts',
    #     'table_name': 'adverse_events',
    #     'extract_fields': [
    #         'term', 'organSystem', 'sourceVocabulary',
    #         'assessmentType', 'notes'
    #     ],
    #     'nested_arrays': {
    #         'stats': ['groupId', 'numEvents', 'numAffected', 'numAtRisk']
    #     },
    #     'severity': 'OTHER'
    # }

    }
