ONE_TO_ONE_FIELDS = {
    # Identification
    "nct_id": "protocolSection.identificationModule.nctId",
    "brief_title": "protocolSection.identificationModule.officialTitle",
    "official_title": "protocolSection.identificationModule.officialTitle",
    "acronym": "protocolSection.identificationModule.acronym",
    "org_study_id": "protocolSection.identificationModule.orgStudyIdInfo.id",
    "org_study_type": "protocolSection.identificationModule.orgStudyIdInfo.type",
    "org_study_link": "protocolSection.identificationModule.orgStudyIdInfo.link",

    # Description
    "brief_summary": "protocolSection.descriptionModule.briefSummary",
    "detailed_description": "protocolSection.descriptionModule.detailedDescription",

    # Design (single values)
    "study_type": "protocolSection.designModule.studyType",
    "enrollment_type": "protocolSection.designModule.enrollmentInfo.type",
    "enrollment_count": "protocolSection.designModule.enrollmentInfo.count",
    "design_allocation": "protocolSection.designModule.designInfo.allocation",
    "design_intervention_model": "protocolSection.designModule.designInfo.interventionModel",
    "design_intervention_model_desc": "protocolSection.designModule.designInfo.interventionModelDescription",
    "design_primary_purpose": "protocolSection.designModule.designInfo.primaryPurpose",
    "design_observational_model": "protocolSection.designModule.designInfo.observationalModel",
    "design_time_perspective": "protocolSection.designModule.designInfo.timePerspective",
    "design_masking": "protocolSection.designModule.designInfo.maskingInfo.masking",
    "design_masking_desc": "protocolSection.designModule.designInfo.maskingInfo.maskingDescription",
    "design_who_masked": "protocolSection.designModule.designInfo.maskingInfo.whoMasked",

    # Expanded access
    "expanded_access_type_intermediate": "protocolSection.designModule.expandedAccessTypes.intermediate",
    "expanded_access_type_treatment": "protocolSection.designModule.expandedAccessTypes.treatment",

    # Biospecimen
    "biospecimen_retention": "protocolSection.designModule.bioSpec.retention",
    "biospecimen_description": "protocolSection.designModule.bioSpec.description",

    # Eligibility
    "eligibility_criteria": "protocolSection.eligibilityModule.eligibilityCriteria",
    "healthy_volunteers": "protocolSection.eligibilityModule.healthyVolunteers",
    "sex": "protocolSection.eligibilityModule.sex",
    "gender_based": "protocolSection.eligibilityModule.genderBased",
    "gender_description": "protocolSection.eligibilityModule.genderDescription",
    "min_age": "protocolSection.eligibilityModule.minimumAge",
    "max_age": "protocolSection.eligibilityModule.maximumAge",
    "population_desc": "protocolSection.eligibilityModule.studyPopulation",
    "sampling_method": "protocolSection.eligibilityModule.samplingMethod",

    # Status
    "overall_status": "protocolSection.statusModule.overallStatus",
    "last_known_status": "protocolSection.statusModule.lastKnownStatus",
    "status_verified_date": "protocolSection.statusModule.statusVerifiedDate",
    "delayed_posting": "protocolSection.statusModule.delayedPosting",
    "start_date": "protocolSection.statusModule.startDateStruct.date",
    "start_date_type": "protocolSection.statusModule.startDateStruct.type",
    "first_submit_date": "protocolSection.statusModule.studyFirstSubmitDate",
    "first_submit_qc_date": "protocolSection.statusModule.studyFirstSubmitQcDate",
    "last_update_submit_date": "protocolSection.statusModule.lastUpdateSubmitDate",
    "completion_date": "protocolSection.statusModule.completionDateStruct.date",
    "completion_date_type": "protocolSection.statusModule.completionDateStruct.type",
    "why_stopped": "protocolSection.statusModule.whyStopped",
    "has_expanded_access": "protocolSection.statusModule.expandedAccessInfo.hasExpandedAccess",

    # Oversight
    "has_dmc": "protocolSection.oversightModule.oversightHasDmc",
    "is_fda_regulated_drug": "protocolSection.oversightModule.isFdaRegulatedDrug",
    "is_fda_regulated_device": "protocolSection.oversightModule.isFdaRegulatedDevice",
    "is_unapproved_device": "protocolSection.oversightModule.isUnapprovedDevice",
    "is_us_export": "protocolSection.oversightModule.isUsExport",

    # Individual participant data
    "ipd_sharing": "protocolSection.ipdSharingStatementModule.ipdSharing",
    "ipd_description": "protocolSection.ipdSharingStatementModule.description",
    "ipd_time_frame": "protocolSection.ipdSharingStatementModule.timeFrame",
    "ipd_access_criteria": "protocolSection.ipdSharingStatementModule.accessCriteria",
    "ipd_url": "protocolSection.ipdSharingStatementModule.url",

    # Large documents
    "large_doc_no_sap": "documentSection.largeDocumentModule.noSap",

    # Miscellaneous
    "version_holder": "derivedSection.miscInfoModule.versionHolder",
    "has_results": "hasResults",
    "last_updated": "protocolSection.statusModule.lastUpdatePostDateStruct.date",
    "unposted_responsible_party": "annotationSection.annotationModule.unpostedAnnotation.unpostedResponsibleParty",
    "limitations_description": "resultsSection.moreInfoModule.limitationsAndCaveats.description",

    # Certain agreements
    "certain_agreement_pi_sponsor_employee": "resultsSection.moreInfoModule.certainAgreement.piSponsorEmployee",
    "certain_agreement_restriction_type": "resultsSection.moreInfoModule.certainAgreement.restrictionType",
    "certain_agreement_restrictive": "resultsSection.moreInfoModule.certainAgreement.restrictiveAgreement",
    "certain_agreement_other_details": "resultsSection.moreInfoModule.certainAgreement.otherDetails",

    # Point of contact
    "point_of_contact_title": "resultsSection.moreInfoModule.pointOfContact.title",
    "point_of_contact_organization": "resultsSection.moreInfoModule.pointOfContact.organization",
    "point_of_contact_email": "resultsSection.moreInfoModule.pointOfContact.email",
    "point_of_contact_phone": "resultsSection.moreInfoModule.pointOfContact.phone",
    "point_of_contact_phone_ext": "resultsSection.moreInfoModule.pointOfContact.phoneExt",

    # Submission tracking
    "submission_tracking_estimated_results_date": "derivedSection.miscInfoModule.submissionTracking.estimatedResultsFirstSubmitDate",
    "submission_tracking_first_mcp_date": "derivedSection.miscInfoModule.submissionTracking.firstMcpInfo.postDateStruct.date",
    "submission_tracking_first_mcp_type": "derivedSection.miscInfoModule.submissionTracking.firstMcpInfo.postDateStruct.type",
}


NESTED_FIELDS = {

  "sponsors": {
        "path": "protocolSection.sponsorCollaboratorsModule.leadSponsor",
        "object_type": "simple dict",
        "fields": [
            ("lead_sponsor_name", "name"),
            ("lead_sponsor_class", "class"),
        ],
        "table_name": "sponsors",
        "bridge_table_name": "study_sponsors",
        "transformer_method": "extract_sponsors"
    },

    "collaborators": {
        "path": "protocolSection.sponsorCollaboratorsModule.collaborator",
        "object_type": "array_of_dicts",
        "fields": [
            ("sponsor_name", "name"),
            ("sponsor_class", "class"),
        ],
        "table_name": "sponsor",
        "bridge_table_name": "study_sponsors",
        "transformer_method": "extract_sponsors"
    },
    
    "conditions": {
        "path": "protocolSection.conditionsModule.conditions",
        "object_type": "simple_array",
        "table_name": "conditions",
        "bridge_table_name": "study_conditions",
        "field_name": "condition_name",
        "transformer_method":"extract_conditions"
    },
    
    "keywords": {
        "path": "protocolSection.conditionsModule.keywords",
        "entity": "keyword",
        "object_type": "simple_array",
        "table_name": "keywords",
        "bridge_table_name": "study_keywords",
        "field_name": "study_keyword",
        "transformer_method":"extract_keywords"
    },

    "interventions": {
        "path": "protocolSection.armsInterventionsModule.interventions",
        "entity": "intervention",
        "object_type": "array_of_dicts",
        "fields": [
            ("intervention_name", "name"),
            ("intervention_description", "description"),
            ("object_type", "object_type"),
        ],
        "nested": {
            "nested_path": {
                "object_type": "nested_simple_array",
                "table_name": "intervention_other_names",
                "field_name": "intervention_other_name"
        },
        "table_name": "interventions",
        "bridge_table_name": "study_interventions",
        "transformer_method": "extract_interventions"
        }
    },

    "arm_groups": {
        "path": "protocolSection.armsInterventionsModule.armGroups",
        "object_type": "array_of_dicts",
        "table_name": "study_arm_groups",
        "fields": [
            ("arm_group_label", "label"),
            ("arm_group_description", "description"),
            ("object_type", "object_type"),
        ],
        "nested": {
            "interventionNames": {
                "object_type": "nested_simple_array",
                "bridge_table_name": "arm_group_interventions",
                "field_name": "intervention_name"
        },
        "transformer_method": "extract_arm_groups"
        }
    },

    "locations": {
        "path": "protocolSection.contactsLocationsModule.locations",
        "object_type": "array_of_dicts",
        "table_name": "sites",
        "bridge_table_name": "study_sites",
        "fields": [
            ("site_facility", "facility"),
            ("city", "city"),
            ("state", "state"),
            ("zip", "zip"),
            ("country", "country"),
            ("site_status", "status"),
        ],
        "nested": {
            "geoPoint": {
                "object_type": "simple_array",
                 "fields": ["lat", "lon"],
            },

            "contacts": {
                "object_type": "nested_array_of_dicts",
                "table_name": "contacts",
                "bridge_table_name": "location_contacts",
                "fields": [
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
        "path": "protocolSection.contactsLocationsModule.centralContacts",
        "object_type": "array_of_dicts",
        "table_name": "contacts",
        "bridge_table_name": "study_contacts",
        "fields": [
            ("name", "name"),
            ("role", "role"),
            ("email", "email"),
            ("phone", "phone"),
            ("phoneExt", "phoneExt")
        ],
        "transformer_method": "extract_contacts"
    },

    "overall_officials": {
        "path": "protocolSection.contactsLocationsModule.overallOfficials",
        "object_type": "array_of_dicts",
        "table_name": "investigators",
        "bridge_table_name": "study_investigators",
        "fields": [
            ("name", "name"),
            ("affiliation", "affiliation"),
            ("role", "role")
        ],
        "transformer_method": "extract_officials"
    },

    "primary_outcomes": {
        "path": "protocolSection.outcomesModule.primaryOutcomes",
        "object_type": "array_of_dicts",
        "table_name": "study_outcomes",
        "fields": [
            ("measure", "measure"),
            ("description", "description"),
            ("timeFrame", "timeFrame")
        ],
        "transformer_method": "extract_outcomes",
        "outcome_type": "PRIMARY",
    },

    "secondary_outcomes": {
        "path": "protocolSection.outcomesModule.secondaryOutcomes",
        "object_type": "array_of_dicts",
        "table_name": "study_outcomes",
        "fields": [
            ("measure", "measure"),
            ("description", "description"),
            ("timeFrame", "timeFrame")
        ],
        "transformer_method": "extract_outcomes",
        "outcome_type": "SECONDARY",
    },

    "other_outcomes": {
        "path": "protocolSection.outcomesModule.otherOutcomes",
        "object_type": "array_of_dicts",
        "table_name": "study_outcomes",
        "fields": [
            ("measure", "measure"),
            ("description", "description"),
            ("timeFrame", "timeFrame")
        ],
        "transformer_method": "extract_outcomes",
        "outcome_type": "OTHER",
    },

    "references": {
        "path": "protocolSection.referencesModule.references",
        "object_type": "array_of_dicts",
        "table_name": "study_publications",
        "extract_fields": ["pmid", "object_type", "citation"],
    },

    "retractions": {
        "path": "protocolSection.referencesModule.retractions",
        "object_type": "array_of_dicts",
        "table_name": "study_retractions",
        "fields": [
            ("pmid", "pmid"),
            ("status", "status")
        ],
        "transformer_method": "extract_outcomes",
    },

    "see_also": {
        "path": "protocolSection.referencesModule.seeAlsoLinks",
        "object_type": "array_of_dicts",
        "table_name": "study_see_also",
        "fields": [
            ("label", "label"),
            ("url", "url")
        ],
        "transformer_method": "extract_see_also"
    },

    "phases": {
        "path": "protocolSection.designModule.phases",
        "object_type": "simple_array",
        "table_name": "phases",
        "bridge_table_name": "study_phases",
        "field_name": "phase",
        "transformer_method": "extract_study_phases"
    },


    "std_ages": {
        "path": "protocolSection.eligibilityModule.stdAges",
        "object_type": "simple_array",
        "table_name": "age_groups",
        "bridge_table_name": "study_age_groups",
        "field_name": "age_group",
        "transformer_method": "extract_age_group"
    },

    "ipd_info_types": {
        "path": "protocolSection.ipdSharingStatementModule.infoTypes",
        "object_type": "simple_array",
        "table_name": "ipd_info_types",
        "bridge_table_name": "study_ipd_info_types",
        "field_name": "info_type",
        "transformer_method": "extract_ipd_info_types"
    },
#NOT EVERYTHING NEEDS A BRIDGE
    "secondary_id_infos": {
        "path": "protocolSection.identificationModule.secondaryIdInfos",
        "object_type": "array_of_dicts",
        "table_name": "secondary_ids",
        "bridge_table_name": "study_secondary_ids",
        "fields": [
            ("id", "id"),
            ("object_type", "object_type"),
            ("domain", "domain"),
            ("link", "link")
        ],
        "transformer_method": "extract_id_infos"

    },
    "nct_id_aliases": {
        "path": "protocolSection.identificationModule.nctIdAliases",
        "object_type": "simple_array",
        "table_name": "nct_aliases",
        "bridge_table_name": "study_nct_aliases",
        "field_name": "alias_nct_id",
        "transformer_method": "extract_nct_id_aliases"
    },

    # ===== DERIVED SECTION (MeSH) =====
    # CONDITION MESH TERMS


    "condition_mesh_terms": {
        "path": "derivedSection.conditionBrowseModule.meshes",
        "object_type": "array_of_dicts",
        "fields": [
            ("id", "id"),
            ("term", "term")
        ],
        "table_name": "condition_mesh_terms",
        "bridge_table_name": "study_conditions_mesh",
        "is_primary": True,
        "transformer_method": "extract_condition_mesh"
    },

    "condition_mesh_ancestors": {
        "path": "derivedSection.conditionBrowseModule.ancestors",
        "object_type": "array_of_dicts",
        "fields": [
            ("id", "id"),
            ("term", "term")
        ],
        "table_name": "condition_mesh_terms",
        "bridge_table_name": "study_conditions_mesh",
        "is_primary": False,
        "transformer_method": "extract_condition_mesh"
    },

    "intervention_mesh_terms": {
        "path": "derivedSection.interventionBrowseModule.meshes",
        "object_type": "array_of_dicts",
        "fields": [
            ("id", "id"),
            ("term", "term")
        ],
        "table_name": "intervention_mesh_terms",
        "bridge_table_name": "study_interventions_mesh",
        "is_primary": True,
        "transformer_method": "extract_intervention_mesh"
    },

    "intervention_mesh_ancestors": {
        "path": "derivedSection.interventionBrowseModule.ancestors",
        "object_type": "array_of_dicts",
        "fields": [
            ("id", "id"),
            ("term", "term")
        ],
        "table_name": "intervention_mesh_terms",
        "bridge_table_name": "study_interventions_mesh",
        "is_primary": False,
        "transformer_method": "extract_intervention_mesh"
    },

    "large_documents": {
        "path": "documentSection.largeDocumentModule.largeDocs",
        "object_type": "array_of_dicts",
        "fields": [
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
        "table_name": "study_documents",
        "transformer_method": "extract_large_documents"
    },

    "unposted_events": {
        "path": "annotationSection.annotationModule.unpostedAnnotation.unpostedEvents",
        "object_type": "array_of_dicts",
        "fields": [
            ("object_type", "object_type"),
            ("date", "date"),
            ("dateUnknown", "dateUnknown"),
        ],
        "table_name": "unposted_events",
        "bridge_table_name": "study_unposted_events",
        "transformer_method": "extract_unposted_events"
    },

    "violation_events": {
        "path": "annotationSection.annotationModule.violationAnnotation.violationEvents",
        "object_type": "array_of_dicts",
        "fields": [
            ("object_type", "object_type"),
            ("description", "description"),
            ("creationDate", "creationDate"),
            ("issuedDate", "issuedDate"),
            ("releaseDate", "releaseDate"),
            ("postedDate", "postedDate"),
        ],
        "table_name": "violation_events",
        "bridge_table_name": "study_violation_events",
        "transformer_method": "extract_violation_events"
    },

    "removed_countries": {
        "path": "derivedSection.miscInfoModule.removedCountries",
        "object_type": "simple_array",
        "table_name": "countries",
        "bridge_table_name": "study_removed_countries",
        "field_name": "country",
        "transformer_method": "extract_removed_countries"
    },

    "submission_infos": {
        "path": "derivedSection.miscInfoModule.submissionTracking.submissionInfos",
        "object_type": "array_of_dicts",
        "fields": [
            ("releaseDate", "releaseDate"),
            ("unreleaseDate", "unreleaseDate"),
            ("unreleaseDateUnknown", "unreleaseDateUnknown"),
            ("resetDate", "resetDate"),
            ("mcpReleaseN", "mcpReleaseN")
        ],
        "table_name": "submission_tracking",
        "bridge_table_name": "study_submission_tracking",
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
