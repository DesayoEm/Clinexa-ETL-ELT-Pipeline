
### Source: https://clinicaltrials.gov/data-api/about-api/study-data-structure


### NESTED FIELDS

## SponsorCollaboratorsModule

### sponsors

**Index Field(s):** 
- `protocolSection.sponsorCollaboratorsModule.leadSponsor`
- `protocolSection.sponsorCollaboratorsModule.collaborators[]`

**NOTE**: *sponsor name and class are scalar values and MUST be extracted directly*

**Object Type**: Simple dict (leadSponsor) / Array of dicts (collaborators)

**Description**: Organizations responsible for the study.

- **Lead Sponsor**: Exactly 1 per study. The organization or person who initiates the study and has authority and control over it.
- **Collaborators**: 0 to many. Other organizations providing support (funding, design, implementation, data analysis, reporting).


#### Fields

##### `name`
- **Definition**: Name of the sponsoring entity or individual
- **Data Type**: Text
- **Limit**: 160 characters

##### `class`
- **Definition**: Category of the sponsoring organization
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


---

## armsInterventionsModule 

### arm_groups

**Index Field:** `protocolSection.armsInterventionsModule.armGroups[]`

**Object Type**: Array of dicts

**Description**: Pre-specified group or subgroup of participants assigned to receive specific intervention(s) (or no intervention) according to protocol. For interventional studies only. Observational studies use Groups/Cohorts with the same structure but different semantics.

---

#### Fields

##### `label`
- **Definition**: Short name used to identify the arm
- **Data Type**: Text
- **Limit**: 100 characters
- **Required**: Yes

##### `type`
- **Definition**: The role of the arm in the clinical trial
- **Data Type**: Enum(ArmGroupType)
- **Required**: Yes
- **Enum Values**:
  - `EXPERIMENTAL` — Experimental
  - `ACTIVE_COMPARATOR` — Active Comparator
  - `PLACEBO_COMPARATOR` — Placebo Comparator
  - `SHAM_COMPARATOR` — Sham Comparator
  - `NO_INTERVENTION` — No Intervention
  - `OTHER` — Other

##### `description`
- **Definition**: Additional descriptive information to differentiate this arm from others (including which interventions are administered)
- **Data Type**: Markup
- **Limit**: 999 characters
- **Required**: Conditional

#### Nested Fields
######  `interventionNames`
- **Definition**: Names of interventions associated with this arm. References `interventions[].name` within the same study.
- **Data Type**: Array of Text
- **Limit**: 200 characters per name
- **Required**: Yes (for interventional studies)



#### Dimensional Model Mapping

- **Bridge Table**: `bridge_study_arm_groups` 
- **Surrogate Key**: `hash(study_key, label)`


---

### interventions

**Index Field:** `protocolSection.armsInterventionsModule.interventions[]`

**Object Type**: Array of dicts

**Description**: The intervention(s) studied in the clinical trial. For interventional studies, at least one required. For observational studies, specifies interventions/exposures of interest if any.

---

#### Fields

##### `name`
- **Definition**: Brief descriptive name for the intervention. Non-proprietary name required if available.
- **Data Type**: Text
- **Limit**: 200 characters
- **Required**: Yes

##### `type`
- **Definition**: General type of intervention
- **Data Type**: Enum(InterventionType)
- **Required**: Yes
- **Enum Values**:
  - `DRUG` — Drug (including placebo)
  - `DEVICE` — Device (including sham)
  - `BIOLOGICAL` — Biological/Vaccine
  - `PROCEDURE` — Procedure/Surgery
  - `RADIATION` — Radiation
  - `BEHAVIORAL` — Behavioral (e.g., psychotherapy, lifestyle counseling)
  - `GENETIC` — Genetic (gene transfer, stem cell, recombinant DNA)
  - `DIETARY_SUPPLEMENT` — Dietary Supplement (vitamins, minerals)
  - `COMBINATION_PRODUCT` — Combination Product (drug+device, biological+device, etc.)
  - `DIAGNOSTIC_TEST` — Diagnostic Test (imaging, in vitro)
  - `OTHER` — Other

##### `description`
- **Definition**: Details sufficient to distinguish this intervention from similar ones (e.g., dosage form, dosage, frequency, duration for drugs)
- **Data Type**: Markup
- **Limit**: 1,000 characters
- **Required**: Yes

##### `armGroupLabels`
- **Definition**: Labels of arm groups that receive this intervention. References `armGroups[].label` within the same study.
- **Data Type**: Array of Text
- **Required**: Yes (if multiple arms exist)

##### `otherNames`
- **Definition**: Other current/former names or aliases (brand names, serial numbers)
- **Data Type**: Array of Text
- **Limit**: 200 characters per name
- **Required**: No

---

#### Dimensional Model Mapping

- **Target Table**: `dim_interventions`
- **Surrogate Key**: `hash(study_key, name, type)`
- **Bridge Table**: `bridge_study_interventions` (study_key, intervention_key)

---

### Arm <-->Intervention Relationship

**Source Data**: The API provides bidirectional references:
- `armGroups[].interventionNames` — intervention names per arm
- `interventions[].armGroupLabels` — arm labels per intervention

**Decision**: `armGroups[].interventionNames` as the source of truth for arm interventions and interventions[] as the source of truth interventions

**Rationale**:
1. Matches analytical workflow (arm -> intervention, not reverse)
2. User-entered data may have inconsistencies between the two lists
3. Avoids reconciliation logic and potential mismatches from bidirectional data quality issues

**Implication**: Queries for "which arms use this intervention" require joining through `bridge_arm_interventions` from the arm side. We do not model the reverse relationship from `interventions[].armGroupLabels`.


### design_who_masked
**Index Field:** protocolSection.designModule.designInfo.maskingInfo.whoMasked

**Definition**: The party or parties involved in the clinical trial who are prevented from having knowledge of the interventions assigned to individual participants

**DataType**: [Enum(WhoMasked)]

**Enum Values**:
* PARTICIPANT - Participant
* CARE_PROVIDER - Care Provider
* INVESTIGATOR - Investigator
* OUTCOMES_ASSESSOR - Outcomes Assessor


## contactsLocationsModule

#### locations

**Index Field(s):** `protocolSection.contactsLocationsModule.locations`

**Object Type**: Array of Dicts

**Description**: Participating facility in a clinical study

##### `facility`
- **Definition**: ull name of the organization where the clinical study is being conducted
- **Data Type**: Text
- **Limit**: 254 characters


##### `status`
- **Definition**: Individual Site Status 
- **Data Type**: Enum(RecruitmentStatus)
- **Enum Values**:
  - `ACTIVE_NOT_RECRUITING` - Active, not recruiting
  - `COMPLETED` - Completed
  - `ENROLLING_BY_INVITATION` - Enrolling by invitation
  - `NOT_YET_RECRUITING` - Not yet recruiting
  - `RECRUITING` - Recruiting
  - `SUSPENDED` - Suspended
  - `TERMINATED` - Terminated
  - `WITHDRAWN` - Withdrawn
  - `AVAILABLE` - Available

    
**LOCATION STATUS RESOLUTION**

Location-level statuses can be inconsistent/outdated. Use study-level overall_status as the authoritative source:

1. Study COMPLETED/TERMINATED -> inherit study status (can't recruit)
2. Study NOT_YET_RECRUITING -> inherit study status (hasn't started)
3. Study RECRUITING + conflicting locations AND one is RECRUITING -> UNCLEAR
4. Study RECRUITING + no location says RECRUITING -> use location status

This ensures patient matching prioritizes study-level recruitment status while flagging ambiguous cases.
"""

##### `city`
- **Definition**: City
- **Data Type**: GeoName

##### `state`
- **Definition**: State/Province. Required for U.S. locations (including territories of the United States)
- **Data Type**: GeoName

##### `zip`
- **Definition**: ZIP/Postal Code. Required for U.S. locations (including territories of the United States)
- **Data Type**: GeoName

##### `geoPoint`
- **Definition**: Lat and Lon
- **Data Type**: Dict

#### Nested Fields
##### `contacts`
--- Saved as a JSON blob

Extract locations and stores location contact as JSON blob.
NOTE: Officials are stored denormalized as JSON since not used for filtering/analysis.
Avoids snowflaking the schema while preserving all contact information for downstream applications.

#### Model Mapping
- **Target Table**: `locations`
- **Bridge Table**: `bridge_study_locations` 

--- 

### central_contacts

- **Index Field:** `protocolSection.contactsLocationsModule.centralContacts[]`
- **Definition**: Contact person(s) for general enrollment questions across all study locations. Required if no facility-level contacts provided.
- **Object Type**: Array of dicts
- **Cardinality**: 0 to many (but at least one central OR facility contact required per study)

---

#### Fields

##### `name`
- **Definition**: Name or title of contact person
- **Data Type**: Text
- **Required**: Yes

##### `role`
- **Definition**: Role of the contact
- **Data Type**: Enum(CentralContactRole)
- **Values**: `CONTACT`, `PRINCIPAL_INVESTIGATOR`, etc.

##### `phone`
- **Definition**: Telephone number (preferably toll-free)
- **Data Type**: Text
- **Required**: Yes

##### `phoneExt`
- **Definition**: Phone extension
- **Data Type**: Text
- **Required**: No

##### `email`
- **Definition**: Email address
- **Data Type**: Text
- **Required**: Yes

---

#### Dimensional Model Mapping

- **Target Table**: `dim_contacts`
- **Bridge Table**: `bridge_study_contacts` (study_key, contact_key)
- **Surrogate Key**: `hash(study_key, name, role, phone)`

---


## References

### references
- **Index Field:** `protocolSection.referencesModule.references`
- **Definition**: Citations to publications related to the protocol
- **DataType**: Reference[]

#### Fields

##### `pmid`
- **Definition**: PubMed identifier for the citation in MEDLINE
- **Data Type**: Text
- **Required**: Yes

##### `type`
- **Definition**: Reference type
- **Data Type**: Enum(ReferenceType)
**Enum Values**:
- PARTICIPANT - Participant
- BACKGROUND - background
- RESULT - result
- DERIVED - derived

##### `citations`
- **Definition**: PubMed identifier for the citation in MEDLINE
- **Data Type**: Text
- **Required**: Yes

### see_also
- **Index Field:** `protocolSection.referencesModule.seeAlsoLinks`
- **Definition**:  A website directly relevant to the protocol 
- **DataType**: SeeAlsoLink[]

#### Fields

##### `label`
- **Definition**: Title or brief description of the linked page.
- **Data Type**: Text
- **Limit**: 254 characters.

##### `url`
- **Definition**: Complete URL, including http:// or https:
- **Data Type**: Text
- **Limit**: 3,999 characters.



### availIpds
- **Index Field:** `protocolSection.referencesModule.availIpds`
- **Definition**: Available individual participant data (IPD) sets and supporting information that are being shared for the study.
- **DataType**: AvailIpd[]

#### Fields

##### `id`
- **Definition**:  The unique identifier used by a data repository for the data set or supporting information.
- **Data Type**: Text
- **Limit**: 30 characters

##### `type`
- **Definition**:  The type of data set or supporting information being shared.
- **Data Type**: Text
- **Limit**: 30 characters

##### `url`
- **Definition**:  The web address used to request or access the data set or supporting information.
- **Data Type**: Text
- **Limit**: 3999 characters

##### `comment`
- **Definition**:  Additional information including the name of the data repository or other location where the data set or supporting information is available.
- **Data Type**: Text
- **Limit**: 30 characters




### FlowGroup 
- **Index Field:** `resultsSection.participantFlowModule.groups`
- **Definition**: Arms or groups for describing the flow of participants through the clinical study. In general, it must include each arm to which participants were assigned.
- **DataType**: FlowGroup[]

#### Fields

##### `id`
- **Definition**: Arm/Group ID generated by PRS
- **Data Type**: Text

##### `title`
- **Definition**: Descriptive label used to identify each arm or group.
- **Data Type**: Text
- **Limit**:  >=4 and <= 100 characters.

##### `description`
- **Definition**: Brief description of each arm or group. In general, it must include sufficient details to understand each arm to which participants were assigned and the intervention strategy used in each arm.
- **Data Type**: Text
- **Limit**: 1500 characters.



### FlowPeriod
- **Index Field:** `resultsSection.participantFlowModule.periods`
- **Definition**: Discrete stages of a clinical study during which numbers of participants at specific significant events or points of time are reported.
- **DataType**: FlowPeriod[]

#### Fields

##### `title`
- **Definition**:  Title describing a stage of the study. If only one period is defined, the default title is Overall Study. 
- **Data Type**: Text
- **Limit**: 40 characters.


### FlowPeriod milestones
- **Index Field:** `resultsSection.participantFlowModule.periods.milestones`
- **Description**: Arm/Group ID generated by PRS
- **Data Type**: FlowMilestone[]

#### FlowMilestone Fields
- ##### `type`
- **Definition**:  Title describing a stage of the study. If only one period is defined, the default title is Overall Study. 
- **Data Type**: Text
- **Limit**: 40 characters.

- ##### `comment`
- **Definition**:  Additional information about the milestone or data.
- **Data Type**: Text
- **Limit**: 500 characters.

- ##### `achievements`
- **Definition**:  Milestone Data (per arm/group)
- **Data Type**: FlowStats[]
- **Limit**: 40 characters.

##### FlowStats Fields

- ##### `groupId`
- **Definition**:  Milestone Data (per arm/group)
- **Data Type**: ID

- ##### `groupId`
- **Definition**:  group id
- **Data Type**: Type
- **Limit**: 500 characters.

- ##### `numSubjects`
- **Definition**:   number of subjects
- **Data Type**: ID

- ##### `numUnits`
- **Definition**:  number of units


####  FlowDropWithdraw
- **Index Field:** `resultsSection.participantFlowModule.periods.dropWithdraws`
- **Definition**: Additional information about participants who did not complete the study or period. If reasons are provided, the total number of participants listed as Not Completed must be accounted for by all reasons for non-completion.
- **DataType**:  DropWithdraw[]

##### Fields

###### `type`
- **Definition**:  Reason why participants did not complete the study or period.
- **Data Type**: Text


###### `comment`
- **Definition**:A brief description of the reason for non-completion, if "Other" Reason Not Completed Type is selected.
- **Data Type**: Text
- **Limit**: 500 characters.
- * Other Reason [*] - A brief description of the reason for non-completion, if "Other" Reason Not Completed Type is selected
- * **Limit**: 100 characters.


######  FlowReason
- **Index Field:** `resultsSection.participantFlowModule.periods.dropWithdraws.reasons`
- **Definition**: Reason for Not Completed per arm/group
- **DataType**:  FlowStats[]

##### Fields

###### `groupId`
- **Definition**:  Internally generated ID for reason not completed per arm/group

###### `comment`
- **Definition**:  Reason why participants did not complete the study or period, for each Reason Not Completed.

###### `numSubjects`
- **Definition**:  Number of participants in each arm or group that did not complete the study or period, for each Reason Not Completed.

**FLOW PERIOD DUPLICATE HANDLING**

### Issue
- Some studies contain duplicate period entries with the same title  but different participant counts.

- **Resolution**:Aggregate duplicate (study, period, event, group) combinations  by SUMMING num_subjects. 

- This assumes multiple entries represent cumulative enrollment or separate cohorts within the same period.

- **Limitation:** If entries represent corrections (not additions), totals may  be inflated.



## Outcome measures module

- **Index Field:** `resultsSection.outcomeMeasuresModule.outcomeMeasures`
- **Definition**: "Outcome measure" means a pre-specified measurement that is used to determine the effect of an experimental variable on participants in the study. 
- **DataType**: OutcomeMeasure[]

##### Fields

###### `type`
- **Definition**:  The type of outcome measure
- **DataType**: Enum(OutcomeMeasureType)
**Enum Values**:
- * PARTICIPANT - Participant
- * CARE_PROVIDER - Care Provider
- * INVESTIGATOR - Investigator
- * OUTCOMES_ASSESSOR - Outcomes Assessor**

###### `title`
- **Definition**: Name of the specific outcome measure.
- **Limit**: 255 characters.
- **DataType**: Text


###### `description`
- **Definition**: Additional information about the outcome measure, including a description of the metric used to characterize the specific outcome measure, if not included in the Outcome Measure Title.
- **Limit**: 999 characters.
- **DataType**: Text
- 

###### `populationDescription` 
- **Definition**: If the Number of Participants Analyzed or Number of Units Analyzed differs from the number of participants or units assigned to the arm or comparison group, 
      brief description of the reason for the difference (such as how the analysis population was determined).
- **Limit**: 500 characters.
- **DataType**: Text

###### `reportingStatus`
- **Definition**:  Whether there is Outcome Measure Data reported
- **DataType**: Enum(ReportingStatus)

**Enum Values**:
- * NOT_POSTED - Not Posted
- * POSTED - Posted

###### `anticipatedPostingDate`
- **Definition**:  If Outcome Measure Data are not included for an outcome measure, the expected month and year they will be submitted.
- **DataType**: PartialDate

###### `paramType`
- **Definition**:  The type of data for the outcome measure.
- **DataType**: Enum(MeasureParam)

**Enum Values**:
- * GEOMETRIC_MEAN - Geometric Mean
- *GEOMETRIC_LEAST_SQUARES_MEAN - Geometric Least Squares Mean
- *LEAST_SQUARES_MEAN - Least Squares Mean
- *LOG_MEAN - Log Mean
- *MEAN - Mean
- *MEDIAN - Median
- *NUMBER - Number
- *COUNT_OF_PARTICIPANTS - Count of Participants
- *COUNT_OF_UNITS - Count of Units


###### `dispersionType` 
- **Definition**: Measure of Dispersion/Precision
- **DataType**: Text
- 
###### `unitOfMeasure` 
- **Definition**: An explanation of what is quantified by the data (for example, participants, mm Hg), for each outcome measure.
- **DataType**: Text
- **Limit**: 40 characters.
- 
###### `calculatePct` 
- **Definition**: 	
percentage of OutcomeMeasurementValue/OutcomeMeasureDenomCountValue (internally calculated)
- **DataType**: Boolean

###### `timeFrame` 
- **Definition**: Time point(s) at which the measurement was assessed for the specific metric used. The description of the time point(s) of assessment must be specific to the outcome measure 
    and is generally the specific duration of time over which each participant is assessed (not the overall duration of the study).
- **DataType**: Text
- **Limit**: 255 characters.

###### `typeUnitsAnalyzed` 
- **Definition**: f the analysis is based on a unit other than participants, a description of the unit of analysis (for example, eyes, lesions, implants).
- **DataType**: Text
- **Limit**: 40 characters.

###### `denomUnitsSelected` 
- **Definition**: OutcomeMeasureTypeUnitsAnalyzed
- **DataType**: Text












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

    
    "phases": {
        **Index Field:** "protocolSection.designModule.phases",
        **Object_type**: "simple_array",
        **Table_name**: "phases",
        **Bridge_table_name**: "study_phases",
        **Field_name**: "phase",
        "transformer_method": "extract_study_phases"
    },


    "ipd_info_types": {
        **Index Field:** "protocolSection.ipdSharingStatementModule.infoTypes",
        **Object_type**: "simple_array",
        **Table_name**: "ipd_info_types",
        **Bridge_table_name**: "study_ipd_info_types",
        **Field_name**: "info_type",
        "transformer_method": "extract_ipd_info_types"
    },

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


### design_who_masked
**Index Field:** protocolSection.designModule.designInfo.maskingInfo.whoMasked

**Definition**: The party or parties involved in the clinical trial who are prevented from having knowledge of the interventions assigned to individual participants

**DataType**: [Enum(WhoMasked)]

**Enum Values**:
* PARTICIPANT - Participant
* CARE_PROVIDER - Care Provider
* INVESTIGATOR - Investigator
* OUTCOMES_ASSESSOR - Outcomes Assessor
