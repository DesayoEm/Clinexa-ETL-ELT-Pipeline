from typing import Dict, Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NESTED_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_conditions_mesh(nct_id: str, study_key: str, study_data: pd.Series) -> Tuple:
    conditions_mesh = []
    study_conditions_mesh = []

    conditions_ancestors = []
    study_conditions_ancestors = []

    conditions_browse_leaves = []
    study_conditions_browse_leaves = []

    conditions_browse_branches = []
    study_conditions_browse_branches = []

    conditions_browse_index = NESTED_FIELDS["conditions_browse"]["index_field"]
    conditions_browse_data = study_data.get(conditions_browse_index)

    if isinstance(conditions_browse_data, dict) and conditions_browse_data:
        meshes = conditions_browse_data.get("meshes")
        for mesh in meshes:
            pass

        ancestors = conditions_browse_data.get("ancestors")
        for ancestor in ancestors:
            pass

        browse_leaves = conditions_browse_data.get("browseLeaves")
        for leaves in browse_leaves:
            pass

        browse_branches = conditions_browse_data.get("browseBranches")
        for branch in browse_branches:
            pass


    # else:
    #     log.warning(f"No conditions_mesh found for study {study_key}, page - NCT ID {nct_id}")

    return conditions_mesh, study_conditions_mesh