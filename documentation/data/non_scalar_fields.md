
### Source: https://clinicaltrials.gov/data-api/about-api/study-data-structure


## identificationModule

- **Index Field:** `protocolSection.identificationModule`
- **Description**: Study Identification

### Non-scalar fields
##### `nctIdAliases`
- **Definition**: Identifier(s) that are considered "Obsolete" or "Duplicate".
- **Data Type**: nct[]


##### `SecondaryIdInfo`
- **Definition**: An identifier(s) (ID), if any, other than the organization's Unique Protocol Identification Number or the NCT number that is assigned to the clinical study.
- **Data Type**: SecondaryIdInfo[]
- **Fields**: [id, type, domain, link]


---

## SponsorCollaboratorsModule

- **Index Field:** `protocolSection.sponsorCollaboratorsModule`
- **Description**: Organizations responsible for the study.


### Non-scalar fields
### `sponsor`

- **Definition**: Name of the sponsoring entity or individual
- **Data Type**: Sponsor

#### Fields

##### `name`
- **Definition**: Name of the sponsoring entity or individual
- **Data Type**: Text
- **Limit**: 160 characters

##### `class`
- **Definition**: Category of the sponsoring organization
- **Data Type**: Enum(AgencyClass)
- **Enum Values**:
  - `NIH` - National Institutes of Health
  - `FED` - Other Federal Agency
  - `OTHER_GOV` - Other Governmental (non-US)
  - `INDIV` - Individual
  - `INDUSTRY` - Industry/Pharmaceutical
  - `NETWORK` - Research Network
  - `AMBIG` - Ambiguous
  - `OTHER` - Other
  - `UNKNOWN` - Unknown


### Non-scalar fields
### `collaborators`

- **Definition**: Other organizations, if any, providing support. Support may include funding, design, implementation, data analysis or reporting.
- **Data Type**: Sponsor[]

#### Fields

##### `name`
- **Definition**: Name of the sponsoring entity or individual
- **Data Type**: Text
- **Limit**: 160 characters

##### `class`
- **Definition**: Category of the sponsoring organization
- **Data Type**: Enum(AgencyClass)
- **Enum Values**:
  - `NIH` - National Institutes of Health
  - `FED` - Other Federal Agency
  - `OTHER_GOV` - Other Governmental (non-US)
  - `INDIV` - Individual
  - `INDUSTRY` - Industry/Pharmaceutical
  - `NETWORK` - Research Network
  - `AMBIG` - Ambiguous
  - `OTHER` - Other
  - `UNKNOWN` - Unknown



- **Lead Sponsor**: Exactly 1 per study. The organization or person who initiates the study and has authority and control over it.
- **Collaborators**: 0 to many. Other organizations providing support (funding, design, implementation, data analysis, reporting).



---


## ConditionsModule 

- **Index Field:** `protocolSection.conditionsModule`
- **Description**: The name(s) of the disease(s) or condition(s) studied in the clinical study, or the focus of the clinical study.


### Non-scalar fields
###  `conditions`

- **Object Type**: text[]

### `keywords`

- **Description**: Words or phrases that best describe the protocol. Keywords help users find studies in the database
- **Object Type**: text[]



---

## armsInterventionsModule 

- **Index Field:** `protocolSection.armsInterventionsModule`
- **Description**: A description of each arm of the clinical trial that indicates its role in the clinical trial

### Non-scalar fields
### `ArmGroup`

- **Object Type**: ArmGroup[]
- **Description**: Pre-specified group or subgroup of participants assigned to receive specific intervention(s) (or no intervention) according to protocol. For interventional studies only. Observational studies use Groups/Cohorts with the same structure but different semantics.


#### Fields

##### `label`
- **Definition**: Short name used to identify the arm
- **Data Type**: Text
- **Limit**: 100 characters

##### `type`
- **Definition**: The role of the arm in the clinical trial
- **Data Type**: Enum(ArmGroupType)
- **Enum Values**:
  - `EXPERIMENTAL` - Experimental
  - `ACTIVE_COMPARATOR` - Active Comparator
  - `PLACEBO_COMPARATOR` - Placebo Comparator
  - `SHAM_COMPARATOR` - Sham Comparator
  - `NO_INTERVENTION` - No Intervention
  - `OTHER` - Other

##### `description`
- **Definition**: Additional descriptive information to differentiate this arm from others (including which interventions are administered)
- **Data Type**: Markup
- **Limit**: 999 characters

#####  `interventionNames`
- **Definition**: Names of interventions associated with this arm. References `interventions[].name` within the same study.
- **Data Type**: text[]
- **Limit**: 200 characters per name


### `intervention`

- **Description**: The intervention(s) studied in the clinical trial. For interventional studies, at least one required. For observational studies, specifies interventions/exposures of interest if any.
- **Object Type**: Intervention[]

#### Fields

##### `name`
- **Definition**: Brief descriptive name for the intervention. Non-proprietary name required if available.
- **Data Type**: Text
- **Limit**: 200 characters


##### `type`
- **Definition**: General type of intervention
- **Data Type**: Enum(InterventionType)
- **Enum Values**:
  - `DRUG` - Drug (including placebo)
  - `DEVICE` - Device (including sham)
  - `BIOLOGICAL` - Biological/Vaccine
  - `PROCEDURE` - Procedure/Surgery
  - `RADIATION` - Radiation
  - `BEHAVIORAL` - Behavioral (e.g., psychotherapy, lifestyle counseling)
  - `GENETIC` - Genetic (gene transfer, stem cell, recombinant DNA)
  - `DIETARY_SUPPLEMENT` - Dietary Supplement (vitamins, minerals)
  - `COMBINATION_PRODUCT` - Combination Product (drug+device, biological+device, etc.)
  - `DIAGNOSTIC_TEST` - Diagnostic Test (imaging, in vitro)
  - `OTHER` - Other

##### `description`
- **Definition**: Details sufficient to distinguish this intervention from similar ones (e.g., dosage form, dosage, frequency, duration for drugs)
- **Data Type**: Markup
- **Limit**: 1,000 characters


##### `otherNames`
- **Definition**: Other current/former names or aliases (brand names, serial numbers)
- **Data Type**: text[]
- **Limit**: 200 characters per name



### Arm <-->Intervention Relationship

**Source Data**: The API provides bidirectional references:
- `armGroups[].interventionNames` - intervention names per arm
- `interventions[].armGroupLabels` - arm labels per intervention

**Decision**: `armGroups[].interventionNames` as the source of truth for arm interventions and interventions[] as the source of truth interventions

**Rationale**:
1. Matches analytical workflow (arm -> intervention, not reverse)
2. User-entered data may have inconsistencies between the two lists
3. Avoids reconciliation logic and potential mismatches from bidirectional data quality issues

**Implication**: Queries for "which arms use this intervention" require joining through `bridge_arm_interventions` from the arm side. We do not model the reverse relationship from `interventions[].armGroupLabels`.


---

## SponsorCollaboratorsModule

- **Index Field:** `protocolSection.outcomesModule`
- **Description**: Outcome Measures


### Non-scalar fields
### `primaryOutcomes`

- **Definition**:  A description of each primary outcome measure (or for observational studies, specific key measurement[s] or observation[s] used to describe patterns of diseases or traits or associations with exposures, risk factors or treatment).
- **Data Type**: Outcome[]

#### Fields

##### `measure`
- **Definition**: Name of the specific primary outcome measure
- **Data Type**: Text
- **Limit**: 254 characters

##### `description`
- **Definition**: Description of the metric used to characterize the specific primary outcome measure, if not included in the primary outcome measure title.
- **Data Type**: Text
- **Limit**: 999 characters

##### `timeFrame`
- **Definition**: Time point(s) at which the measurement is assessed for the specific metric used
- **Data Type**: Text
- **Limit**: 254 characters


### `secondaryOutcomes`

- **Definition**:  A description of each secondary outcome measure (or for observational studies, specific key measurement[s] or observation[s] used to describe patterns of diseases or traits or associations with exposures, risk factors or treatment).
- **Data Type**: Outcome[]

#### Fields

##### `measure`
- **Definition**: Name of the specific secondary outcome measure
- **Data Type**: Text
- **Limit**: 254 characters

##### `description`
- **Definition**: Description of the metric used to characterize the specific secondary outcome measure, if not included in the primary outcome measure title.
- **Data Type**: Text
- **Limit**: 999 characters

##### `timeFrame`
- **Definition**: Time point(s) at which the measurement is assessed for the specific metric used
- **Data Type**: Text
- **Limit**: 254 characters



### `otherOutcomes`

- **Definition**:  A description of each other outcome measure (or for observational studies, specific key measurement[s] or observation[s] used to describe patterns of diseases or traits or associations with exposures, risk factors or treatment).
- **Data Type**: Outcome[]

#### Fields

##### `measure`
- **Definition**: Name of the specific other outcome measure
- **Data Type**: Text
- **Limit**: 254 characters

##### `description`
- **Definition**: Description of the metric used to characterize the other primary outcome measure, if not included in the primary outcome measure title.
- **Data Type**: Text
- **Limit**: 999 characters

##### `timeFrame`
- **Definition**: Time point(s) at which the measurement is assessed for the specific metric used
- **Data Type**: Text
- **Limit**: 254 characters



---

## contactsLocationsModule

- **Index Field:** `protocolSection.contactsLocationsModule`
- **Description**:Contacts, Locations, and Investigator Information

### Non-scalar fields

### `centralContacts`
- **Definition**: Contact person(s) for general enrollment questions across all study locations. Required if no facility-level contacts provided.
- **Object Type**: centralContacts[]
- **Cardinality**: 0 to many (but at least one central OR facility contact required per study)


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



### `locations`

- **Object Type**: Location[]
- **Description**: Participating facility in a clinical study

#### Fields

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


##### `contacts`
- **Data Type**: JSON
--- Saved as a JSON blob

Extract locations and stores location contact as JSON blob.
NOTE: Officials are stored denormalized as JSON since not used for filtering/analysis.
Avoids snowflaking the schema while preserving all contact information for downstream applications.

---

## referencesModule

- **Index Field:** `protocolSection.referencesModule`
- **Description**:Citations to publications related to the protocol

### Non-scalar fields

### `references`
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


### `see_also`
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


---

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


##### Nested 
###### `OutcomeGroup`
###### `groups`
- **Definition**:  Arms or comparison groups in the study, 
- including all arms or comparison groups based on the pre-specified protocol and/or statistical analysis plan.

- **DataType**: OutcomeGroup[id, title, description]

###### `OutcomeDenom`
###### `denoms`

###### OutcomeDenom Fields
###### `units`
- **Definition**:  If the analysis is based on a unit other than participants, the number of units for which an outcome was measured and analyzed, for each outcome measure and each arm/group.
- **DataType**: Text


###### `counts`
- **Definition**:   Number of participants for whom an outcome measure was measured and analyzed, for each outcome measure and each arm/group.
- **DataType**: DenomCount[groupId, value]


###### `OutcomeClass`
###### `groups`
- **Definition**:  Arms or comparison groups in the study, 
- including all arms or comparison groups based on the pre-specified protocol and/or statistical analysis plan.

- **DataType**: MeasureClass[]



###### `counts`
- **Definition**:   Number of participants for whom an outcome measure was measured and analyzed, for each outcome measure and each arm/group.
- **DataType**: DenomCount[groupId, value]






## adverseEventsModule

- **Index Field:** `resultsSection.adverseEventsModule`
- **Definition**: Information for completing three tables summarizing adverse events.
- 1.All-Cause Mortality: 
- 2.Serious Adverse Events:
- 3.Other (Not Including Serious) Adverse Events: 
- 
- **DataType**: AdverseEventsModule


##### Fields
###### `frequencyThreshold`
- **Definition**: The frequency of occurrence that an Other (Not Including Serious) Adverse Event must exceed, within any arm or comparison group, 
to be reported in the Other (Not Including Serious) Adverse Event table. 
- 
The number for the frequency threshold must be less than or equal to the allowed maximum (5%).
For example, a threshold of 5 percent indicates that all Other (Not Including Serious) Adverse Events with a frequency greater than 5 percent within at least one arm or comparison group are reported.

- **DataType**: Text


###### `timeFrame`
- **Definition**: The specific period of time over which adverse event data were collected.
- 
- **Limit**: 500 characters.
- **DataType**: Text

###### `description`
- **Definition**:  If the adverse event information collected in the clinical study is collected based on a different definition of adverse event and/or serious adverse event than the standard Adverse Events definition, 
   a brief description of how the definitions differ.
- **DataType**: Text


###### `allCauseMortalityComment`
- **Definition**:  If the adverse event information collected in the clinical study is collected based on a different definition of adverse event and/or serious adverse event than the standard Adverse Events definition, 
   a brief description of how the definitions differ.

- **DataType**: Markup


##### Nested
###### `eventGroups`
- **Definition**:  rms or comparison groups in the study, 
- including all arms or comparison groups based on the pre-specified protocol and/or statistical analysis plan.

- **DataType**: EventGroup[]

##### eventGroups Fields

###### `id`
- **Definition**: Internal group id
- **DataType**: Text

###### `title`
- **Definition**: Label used to identify each arm or comparison group.
- **DataType**: Text
- **Limit**: >=4 and <= 100 characters.

###### `description`
- **Definition**: Brief description of each arm or comparison group. 
- **DataType**: Text
- **Limit**: 1500 characters.

###### `deathsNumAtRisk`
- **Definition**: Overall number of participants, in each arm/group, included in the assessment of deaths due to any cause
- **DataType**: integer 

###### `seriousNumAffected`
- **Definition**: Overall number of participants affected by one or more Serious Adverse Events, for each arm/group.
- **DataType**: integer 

###### `seriousNumAtRisk`
- **Definition**: Overall number of participants included in the assessment of serious adverse events (that is, the denominator for calculating frequency of serious adverse events), for each arm/group.
- **DataType**: integer 

###### `otherNumAffected`
- **Definition**: Overall number of participants affected, for each arm/group, by at least one Other (Not Including Serious) Adverse Event(s) reported in the table.
- **DataType**: integer 

###### `otherNumAtRisk`
- **Definition**: Overall number of participants, for each arm/group, included in the assessment of Other (Not Including Serious) 
  Adverse Events during the study (that is, the denominator for calculating frequency of Other (Not Including Serious) Adverse Events).
- **DataType**: integer 



###### `eventGroups`
- **Definition**:  rms or comparison groups in the study, 
- including all arms or comparison groups based on the pre-specified protocol and/or statistical analysis plan.

- **DataType**: EventGroup[]

##### eventGroups Fields

###### `id`
- **Definition**: Internal group id
- **DataType**: Text

###### `title`
- **Definition**: Label used to identify each arm or comparison group.
- **DataType**: Text
- **Limit**: >=4 and <= 100 characters.

###### `description`
- **Definition**: Brief description of each arm or comparison group. 
- **DataType**: Text
- **Limit**: 1500 characters.

###### `deathsNumAtRisk`
- **Definition**: Overall number of participants, in each arm/group, included in the assessment of deaths due to any cause
- **DataType**: integer 

###### `seriousNumAffected`
- **Definition**: Overall number of participants affected by one or more Serious Adverse Events, for each arm/group.
- **DataType**: integer 

###### `seriousNumAtRisk`
- **Definition**: Overall number of participants included in the assessment of serious adverse events (that is, the denominator for calculating frequency of serious adverse events), for each arm/group.
- **DataType**: integer 

###### `otherNumAffected`
- **Definition**: Overall number of participants affected, for each arm/group, by at least one Other (Not Including Serious) Adverse Event(s) reported in the table.
- **DataType**: integer 

###### `otherNumAtRisk`
- **Definition**: Overall number of participants, for each arm/group, included in the assessment of Other (Not Including Serious) 
  Adverse Events during the study (that is, the denominator for calculating frequency of Other (Not Including Serious) Adverse Events).
- **DataType**: integer 




###### `seriousEvents`
- **Definition**: A table of all anticipated and unanticipated serious adverse events, grouped by organ system, with the number and frequency of such events by arm or comparison group of the clinical study.

- **DataType**: AdverseEvent[]

##### seriousEvents Fields

###### `term`
- **Definition**: Descriptive word or phrase for the adverse event.
- **DataType**: Text
- **Limit**: 100 characters.

###### `organSystem`
- **Definition**: High-level categories used to group adverse event terms by body or organ system. 
- **DataType**: Text


###### `sourceVocabulary`
- **Definition**: Standard terminology, controlled vocabulary, or classification and version from which adverse event terms are drawn, if any (for example, SNOMED CT, MedDRA 10.0).
  IF BLANK, the value specified as the Source Vocabulary for Table Default should be used.
- **DataType**: Text
- **Limit**: 20 characters.


###### `assessmentType`
- **Definition**: The type of approach taken to collect adverse event information.
- **DataType**: Text
- **Limit**: 20 characters.

###### `notes`
- **Definition**: Additional relevant information about the adverse event.
- **DataType**: Text
- **Limit**: 250 characters.

###### `stats`
- **Definition**: Statistical information for each Serious Adverse Event
- **DataType**:EventStats[groupId, numEvents, numAffected, numAtRisk]
- **Fields**: 250 characters.



###### `otherEvents`
- **Definition**:Other (Not Including Serious) Adverse Events - similar to Serious AE

- **DataType**: AdverseEvent[]

##### otherEvents Fields

###### `term`
- **Definition**: Descriptive word or phrase for the adverse event.
- **DataType**: Text
- **Limit**: 100 characters.

###### `organSystem`
- **Definition**: High-level categories used to group adverse event terms by body or organ system. 
- **DataType**: Text


###### `sourceVocabulary`
- **Definition**: Standard terminology, controlled vocabulary, or classification and version from which adverse event terms are drawn, if any (for example, SNOMED CT, MedDRA 10.0).
  IF BLANK, the value specified as the Source Vocabulary for Table Default should be used.
- **DataType**: Text
- **Limit**: 20 characters.


###### `assessmentType`
- **Definition**: The type of approach taken to collect adverse event information.
- **DataType**: Text
- **Limit**: 20 characters.

###### `notes`
- **Definition**: Additional relevant information about the adverse event.
- **DataType**: Text
- **Limit**: 250 characters.

###### `stats`
- **Definition**: Statistical information for each Other  Event
- **DataType**:EventStats[]
- **Fields**: [groupId, numEvents, numAffected, numAtRisk]



## annotationModule

### violationEvents

**Index Field(s):** 
- `annotationSection.annotationModule.violationAnnotation.violationEvents`

- **Description**: Organizations responsible for the study.
- **DataType**: ViolationEvent[]


##### violationEvents Fields

###### `type`
- **Definition**: Descriptive word or phrase for the adverse event.
- **Data Type**: Enum(ViolationEventType)
**Enum Values**:
- VIOLATION_IDENTIFIED - Violation Identified by FDA
- CORRECTION_CONFIRMED - Correction Confirmed by FDA
- PENALTY_IMPOSED - Penalty Imposed by FDA
- ISSUES_IN_LETTER_ADDRESSED_CONFIRMED - Issues in letter addressed; confirmed by FDA.


###### `description`
- **Definition**: description
- **DataType**: Text

###### `creationDate`
- **Definition**: Date the violation entered in PRS
- **DataType**: NormalizedDate 

###### `issuedDate`
- **Definition**: Date the FDA issued the violation
- **DataType**: NormalizedDate 

###### `releaseDate`
- **Definition**: Date the study record was submitted
- **DataType**: NormalizedDate 

###### `postedDate`
- **Definition**: Date the violation is available on clinicaltrials.gov
- **DataType**: NormalizedDate 
---

## conditionBrowseModule

#### meshes 

**Index Field(s):** `derivedSection.conditionBrowseModule.meshes`

- **Description**: MeSH terms of Condition/Diseases field
- **DataType**: Mesh[]

#### meshes Fields

###### `id`
- **Definition**: MeSH ID
- **DataType**: Text

###### `term`
- **Definition**: MeSH Heading
- **DataType**: Text


#### ancestors 

**Index Field(s):** `derivedSection.conditionBrowseModule.ancestors`

- **Description**: Ancestor (higher level and more broad) terms of Condition MeSH terms in MeSH Tree hierarchy
- **DataType**: Mesh[]

#### ancestors Fields

###### `id`
- **Definition**: MeSH ID
- **DataType**: Text

###### `term`
- **Definition**: MeSH Heading
- **DataType**: Text

#### browseLeaves 

**Index Field(s):** `derivedSection.conditionBrowseModule.browseLeaves`

- **Description**: Leaf browsing topics for Condition field
- **DataType**: BrowseLeaf[]

#### browseLeaves Fields

###### `id`
- **Definition**: MeSH ID
- **DataType**: Text

###### `asFound`
- **Definition**: Normalized Condition term used to find the topic
- **DataType**: Text

###### `relevance`
- **Definition**: Normalized Condition term used to find the topic
- **Data Type**: Enum(BrowseLeafRelevance)
**Enum Values**:
- LOW - low
- HIGH - high



#### browseBranches 

**Index Field(s):** `derivedSection.conditionBrowseModule.browseBranches`

- **Description**: Branch browsing topics for Condition field
- **DataType**: BrowseBranch[]

#### browseBranches Fields

###### `abbrev`
- **Definition**: MeSH abbreviation
- **DataType**: Text

###### `name`
- **Definition**: name
- **DataType**: Text

###### `relevance`
- **Definition**: Normalized Condition term used to find the topic
- **Data Type**: Enum(BrowseLeafRelevance)
**Enum Values**:
- LOW - low
- HIGH - high