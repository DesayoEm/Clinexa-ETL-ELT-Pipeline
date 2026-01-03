from typing import List, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NESTED_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_references(study_key: str, study_data: pd.Series) -> List:
    study_references = []

    references_index = NESTED_FIELDS["references"]["index_field"]
    references_list = study_data.get(references_index)

    if isinstance(references_list, (list, np.ndarray)) and len(references_list) > 0:

        for reference in references_list:
            pmid = reference.get('pmid')
            reference_key = generate_key(study_key, pmid)
            study_references.append({
                "study_key": study_key,
                "ref_key": reference_key,
                "pmid": pmid,
                "type": reference.get("type"),
                "citation": reference.get("citation")
            })

    return study_references


def transform_links(study_key: str, study_data: pd.Series) -> List:
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

def transform_ipds(study_key: str, study_data: pd.Series) -> List:
    study_ipds = []

    ipds_index = NESTED_FIELDS["avail_ipds"]["index_field"]
    ipds_list = study_data.get(ipds_index)

    if isinstance(ipds_list, (list, np.ndarray)) and len(ipds_list) > 0:

        for ipd in ipds_list:
            ipd_id = ipd.get('id')
            ipd_type = ipd.get('type')
            ipd_url = ipd.get('url')

            ipd_key =generate_key(study_key, ipd_id, ipd_type, ipd_url)
            study_ipds.append({
                "study_key": study_key,
                "ipd_key": ipd_key,
                "id": ipd_id,
                "type": ipd_type,
                "url": ipd_url,
                "comment": ipd.get("comment")
            })
    return study_ipds
