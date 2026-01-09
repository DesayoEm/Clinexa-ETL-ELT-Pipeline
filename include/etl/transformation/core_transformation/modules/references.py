from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key


log = logging.getLogger("airflow.task")


def transform_reference_module(study_key: str, study_data: pd.Series) -> Tuple:
    """
    Extract literature references, external links, and IPD sharing info from a study.

    Args:
        study_key: Unique identifier for the clinical trial study.
        study_data: Flattened study record containing nested reference data
            at the path specified in NON_SCALAR_FIELDS["references"].

    Returns:
        Three-element tuple containing:
            - study_references: Literature citations
            - link_references: External URLs
            - ipd_references: IPD sharing records

        All lists return empty if no references exist for the study.
    """
    study_references = []
    link_references = []
    ipd_references = []

    references_index = NON_SCALAR_FIELDS["references"]["index_field"]

    references_list = study_data.get(f"{references_index}.references")

    if isinstance(references_list, (list, np.ndarray)) and len(references_list) > 0:

        for reference in references_list:
            pmid = reference.get("pmid")
            reference_key = generate_key(study_key, pmid)
            study_references.append(
                {
                    "study_key": study_key,
                    "ref_key": reference_key,
                    "pmid": pmid,
                    "type": reference.get("type"),
                    "citation": reference.get("citation"),
                }
            )

    links_list = study_data.get(f"{references_index}.seeAlsoLinks")
    if isinstance(links_list, (list, np.ndarray)) and len(links_list) > 0:

        for link in links_list:
            label = link.get("label")
            url = link.get("url")
            link_key = generate_key(study_key, label, url)
            link_references.append(
                {
                    "study_key": study_key,
                    "link_key": link_key,
                    "label": label,
                    "url": url,
                }
            )

    ipds_list = study_data.get(f"{references_index}.availIpds")

    if isinstance(ipds_list, (list, np.ndarray)) and len(ipds_list) > 0:

        for ipd in ipds_list:
            ipd_id = ipd.get("id")
            ipd_type = ipd.get("type")
            ipd_url = ipd.get("url")

            ipd_key = generate_key(study_key, ipd_id, ipd_type, ipd_url)
            ipd_references.append(
                {
                    "study_key": study_key,
                    "ipd_key": ipd_key,
                    "id": ipd_id,
                    "type": ipd_type,
                    "url": ipd_url,
                    "comment": ipd.get("comment"),
                }
            )

    return study_references, link_references, ipd_references
