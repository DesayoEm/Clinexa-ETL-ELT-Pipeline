SINGLE_FIELDS = {
    # Identification
    "nct_id": "protocolSection.identificationModule.nctId",
    "brief_title": "protocolSection.identificationModule.briefTitle",
    "official_title": "protocolSection.identificationModule.officialTitle",
    "acronym": "protocolSection.identificationModule.acronym",
    "org_study_id": "protocolSection.identificationModule.orgStudyIdInfo.id",
    # Description
    "brief_summary": "protocolSection.descriptionModule.briefSummary",
    "detailed_desc": "protocolSection.descriptionModule.detailedDescription",

    # Sponsor
    "responsible_party": "protocolSection.sponsorCollaboratorsModule.responsibleParty.type",

    # Design
    "study_type": "protocolSection.designModule.studyType",
    "patient_registry": "protocolSection.designModule.patientRegistry",
    "enrollment_type": "protocolSection.designModule.enrollmentInfo.type",
    "enrollment_count": "protocolSection.designModule.enrollmentInfo.count",
    "design_allocation": "protocolSection.designModule.designInfo.allocation",
    "design_intervention_model": "protocolSection.designModule.designInfo.interventionModel",
    "design_intervention_model_desc": "protocolSection.designModule.designInfo.interventionModelDescription",
    "design_primary_purpose": "protocolSection.designModule.designInfo.primaryPurpose",
    "design_observational_model": "protocolSection.designModule.designInfo.observationalModel",
    "design_time_perspective": "protocolSection.designModule.designInfo.timePerspective",
    "design_masking": "protocolSection.designModule.designInfo.maskingInfo.masking",
    # Biospecimen
    "biospec_retention": "protocolSection.designModule.bioSpec.retention",
    "biospec_desc": "protocolSection.designModule.bioSpec.description",
    # Eligibility
    "eligibility_criteria": "protocolSection.eligibilityModule.eligibilityCriteria",
    "healthy_volunteers": "protocolSection.eligibilityModule.healthyVolunteers",
    "sex": "protocolSection.eligibilityModule.sex",
    "min_age": "protocolSection.eligibilityModule.minimumAge",
    "max_age": "protocolSection.eligibilityModule.maximumAge",
    "population_desc": "protocolSection.eligibilityModule.studyPopulation",
    "sampling_method": "protocolSection.eligibilityModule.samplingMethod",
    # Status
    "overall_status": "protocolSection.statusModule.overallStatus",
    "last_known_status": "protocolSection.statusModule.lastKnownStatus",
    "status_verified_date": "protocolSection.statusModule.statusVerifiedDate",
    "start_date": "protocolSection.statusModule.startDateStruct.date",
    "start_date_type": "protocolSection.statusModule.startDateStruct.type",
    "first_submit_date": "protocolSection.statusModule.studyFirstSubmitDate",
    "last_update_submit_date": "protocolSection.statusModule.lastUpdateSubmitDate",
    "completion_date": "protocolSection.statusModule.completionDateStruct.date",
    "completion_date_type": "protocolSection.statusModule.completionDateStruct.type",
    "why_stopped": "protocolSection.statusModule.whyStopped",
    "has_expanded_access": "protocolSection.statusModule.expandedAccessInfo.hasExpandedAccess",
    "expanded_access_nct": "protocolSection.statusModule.expandedAccessInfo.nctId",
    "expanded_access_status": "protocolSection.statusModule.expandedAccessInfo.statusForNctId",
    # Oversight
    "has_dmc": "protocolSection.oversightModule.oversightHasDmc",
    "is_fda_regulated_drug": "protocolSection.oversightModule.isFdaRegulatedDrug",
    "is_fda_regulated_device": "protocolSection.oversightModule.isFdaRegulatedDevice",
    "is_unapproved_device": "protocolSection.oversightModule.isUnapprovedDevice",
    "is_us_export": "protocolSection.oversightModule.isUsExport",

    # Individual participant data
    "ipd_sharing": "protocolSection.ipdSharingStatementModule.ipdSharing",
    "ipd_desc": "protocolSection.ipdSharingStatementModule.description",
    "ipd_time_frame": "protocolSection.ipdSharingStatementModule.timeFrame",
    "ipd_access_criteria": "protocolSection.ipdSharingStatementModule.accessCriteria",
    "ipd_url": "protocolSection.ipdSharingStatementModule.url",

    # contacts
    "poc_title": "resultsSection.moreInfoModule.pointOfContact.title",
    "poc_organization": "resultsSection.moreInfoModule.pointOfContact.organization",
    "poc_email": "resultsSection.moreInfoModule.pointOfContact.email",
    "poc_phone": "resultsSection.moreInfoModule.pointOfContact.phone",
    "poc_phone_ext": "resultsSection.moreInfoModule.pointOfContact.phoneExt",

    # Participant flow
    "flow_pre_assignment_details": "resultsSection.participantFlowModule.preAssignmentDetails",
    "flow_recruitment_details": "resultsSection.participantFlowModule.recruitmentDetails",
    "flow_type_units_analysed": "resultsSection.participantFlowModule.typeUnitsAnalyzed",

    # Certain agreements
    "certain_agreement_pi_sponsor_employee": "resultsSection.moreInfoModule.certainAgreement.piSponsorEmployee",
    "certain_agreement_restrictive": "resultsSection.moreInfoModule.certainAgreement.restrictiveAgreement",
    "certain_agreement_other_details": "resultsSection.moreInfoModule.certainAgreement.otherDetails",
    "certain_agreement_restriction_type": "resultsSection.moreInfoModule.certainAgreement.restrictionType",


    # Submission tracking
    "sub_tracking_estimated_results_date": "derivedSection.miscInfoModule.submissionTracking.estimatedResultsFirstSubmitDate",

    # Miscellaneous
    "version_holder": "derivedSection.miscInfoModule.versionHolder",
    "has_results": "hasResults",
    "last_updated": "protocolSection.statusModule.lastUpdatePostDateStruct.date",
    "limitations_desc": "resultsSection.moreInfoModule.limitationsAndCaveats.description",

}

NESTED_FIELDS = {
    #statusModule
    "expanded_access": {
        "index_field": "protocolSection.statusModule.expandedAccessInfo",
        "object_type": "simple dict",
        "fields": ['name', 'class'],
    },

    #sponsorCollaboratorsModule
    "sponsor": { #SCALAR BUT TREATED AS A SEPARATE DIM
        "index_field": "protocolSection.sponsorCollaboratorsModule.leadSponsor",
        "object_type": "simple dict",
        "fields": ['name', 'class']
    },
    "collaborators": {
        "index_field": "protocolSection.sponsorCollaboratorsModule.collaborators",
        "object_type": "array_of_dicts",
        "fields": ['name', 'class']
    },

    #conditionsModule
    "conditions": {
        "index_field": "protocolSection.conditionsModule.conditions",
        "object_type": "simple_array",
        "field_name": "condition_name",
    },
    "keywords": {
        "index_field": "protocolSection.conditionsModule.keywords",
        "object_type": "simple_array",
        "field_name": "keyword"
    },

    #armsInterventionsModule
    "interventions": {
        "index_field": "protocolSection.armsInterventionsModule.interventions",
        "object_type": "array_of_dicts",
        "fields": ['name', 'description', 'type']

    },
    "arm_groups": {
        "index_field": "protocolSection.armsInterventionsModule.armGroups",
        "object_type": "array_of_dicts",
        "fields": ['label', 'type', 'description']
    },

    #outcomesModule
    "primary_outcomes": {
        "index_field": "protocolSection.outcomesModule.primaryOutcomes",
        "object_type": "array_of_dicts",
        "fields": ['measure', 'description','timeFrame'],
    },
    "secondary_outcomes": {
        "index_field": "protocolSection.outcomesModule.secondaryOutcomes",
        "object_type": "array_of_dicts",
        "fields": ['measure', 'description','timeFrame'],
    },
    "other_outcomes": {
        "index_field": "protocolSection.outcomesModule.otherOutcomes",
        "object_type": "array_of_dicts",
        "fields": ['measure', 'description','timeFrame'],
    },

    # contactsLocationsModule
    "central_contacts": {
        "index_field": "protocolSection.contactsLocationsModule.centralContacts",
        "object_type": "array_of_dicts",
        "fields": ['name', 'role','email', 'phone', 'phoneExt'],
    },
    "locations": {
        "index_field": "protocolSection.contactsLocationsModule.locations",
        "object_type": "array_of_dicts",
        "fields": ['facility', 'city', 'state', 'zip', 'country', 'status'],

        "nested": {
            "geoPoint": {
                "object_type": "simple_dict",
                "fields": ["lat", "lon"],
            },
            #contacts are saved as a JSON blob
            "contacts": {
                "object_type": "nested_array_of_dicts",
                "fields": ['name', 'role','email', 'phone', 'phoneExt'],
            }
        }
    },
    #referencesModule
    "references": {
        "index_field": "protocolSection.referencesModule.references",
        "object_type": "array_of_dicts",
        "fields": ["pmid", "type"],
    },

    "see_also": {
        "index_field": "protocolSection.referencesModule.seeAlsoLinks",
        "object_type": "array_of_dicts",
        "fields": ["label",  "url"]
    },

    "avail_ipds": {
        "index_field": "protocolSection.referencesModule.availIpds",
        "object_type": "array_of_dicts",
        "fields": ["id", "type", "url", "comment"]
    },

    # participantFlowModule
    'flow_groups': {
        'index_field': 'resultsSection.participantFlowModule.groups',
        'type': 'array_of_dicts',
        'fields': ['id', 'title', 'description']
    },


    'flow_periods': {
        'index_field': 'resultsSection.participantFlowModule.periods',
        'type': 'array_of_dicts',
        'fields': ['title'],
        'nested': {
            'milestones': ['type', 'comment', 'achievements'],
            'dropWithdraws': ['type', 'comment', 'reasons']
        }
    },

    # outcomeMeasuresModule
    'outcome_measures': {
        'index_field': 'resultsSection.outcomeMeasuresModule.outcomeMeasures',
        'type': 'array_of_dicts',
        'fields': [
            'type', 'title', 'description', 'populationDescription', 'reportingStatus','anticipatedPostingDate',
            'paramType', 'dispersionType', 'unitOfMeasure', 'calculatePct', 'timeFrame', 'denomUnitsSelected'
            'typeUnitsAnalyzed'],
        'nested': {
            'OutcomeGroup': ['id', 'title', 'description'],
            'OutcomeDenom': ['units', 'counts' , ['groupId', 'value']],
            'OutcomeClass': ['categories', 'comment', 'achievements'],
            'OutcomeAnalysis ': ['type', 'comment', 'reasons']
        }
    },
    #adverseEventsModule
    'adverse_events': {
        'index_field': 'resultsSection.adverseEventsModule',
        'type': 'array_of_dicts',
        'fields': [
            'frequencyThreshold', 'timeFrame', 'description', 'allCauseMortalityComment'],
        'nested': {
            'eventGroups': ['id', 'title', 'description', 'deathsNumAffected', 'deathsNumAffected', 'deathsNumAtRisk',
                            'seriousNumAffected', 'seriousNumAtRisk', 'otherNumAffected', 'otherNumAtRisk'],

            'seriousEvents': ['term', 'organSystem', 'sourceVocabulary', 'notes', ['groupId', 'numEvents', 'numAffected', 'numAtRisk']],
            'OtherEvent ': ['term', 'organSystem', 'sourceVocabulary', 'notes', ['groupId', 'numEvents', 'numAffected', 'numAtRisk']],
        }
    },
    #annotationModule
    "violation_events": {
        "index_field": "annotationSection.annotationModule.violationAnnotation.violationEvents",
        "object_type": "array_of_dicts",
        "fields": ['type', 'description', 'creationDate', 'issuedDate',
                   'releaseDate', 'postedDate'],
    },

    # conditionBrowseModule
    "conditions_browse": {
        "index_field": "derivedSection.conditionBrowseModule",
        "object_type": "nested_dict",
        'nested': {
            'meshes': ['id', 'term'],
            'ancestors': ['id', 'term'],
            'browseLeaves': ['id', 'name', 'asFound', 'relevance'],
            'browseBranches': ['abbrev', 'name']
        }

    },

    "interventions_browse": {
        "index_field": "derivedSection.interventionBrowseModule",
        "object_type": "nested_dict",
        'nested': {
            'meshes': ['id', 'term'],
            'ancestors': ['id', 'term'],
            'browseLeaves': ['id', 'name', 'asFound', 'relevance'],
            'browseBranches': ['abbrev', 'name']
    }
    },







    "phases": {
        "index_field": "protocolSection.designModule.phases",
        "object_type": "simple_array",
        "field_name": "phase"
    },

    "ipd_info_types": {
        "index_field": "protocolSection.ipdSharingStatementModule.infoTypes",
        "object_type": "simple_array",
        "field_name": "info_type"
    },
    "secondary_id_infos": {
        "index_field": "protocolSection.identificationModule.secondaryIdInfos",
        "object_type": "array_of_dicts",
        "fields": [
            ("id", "id"),
            ("object_type", "object_type"),
            ("domain", "domain"),
            ("link", "link"),
        ]
    },
    "nct_id_aliases": {
        "index_field": "protocolSection.identificationModule.nctIdAliases",
        "object_type": "simple_array",
        "field_name": "alias_nct_id"
    },



}
