from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_conditions_browse_module(study_key: str, study_data: pd.Series) -> Tuple:
    conditions_mesh = []
    study_conditions_mesh = []

    conditions_mesh_ancestors = []
    study_conditions_mesh_ancestors = []

    conditions_browse_leaves = []
    study_conditions_browse_leaves = []

    conditions_browse_branches = []
    study_conditions_browse_branches = []

    conditions_browse_index = NON_SCALAR_FIELDS["conditions_browse"]["index_field"]

    meshes = study_data.get(f"{conditions_browse_index}.meshes")
    if isinstance(meshes, (list, np.ndarray)) and len(meshes) > 0:
        for mesh in meshes:
            mesh_id = mesh.get("id")
            mesh_terms = mesh.get("terms")

            if isinstance(mesh_terms, str) and mesh_terms:
                terms = mesh_terms.split(",")
                for term in terms:
                    term = term.strip()
                    mesh_key = generate_key(study_key, mesh_id, term)
                    conditions_mesh.append(
                        {
                            "mesh_key": mesh_key,
                            "study_key": study_key,
                            "mesh_id": mesh_id,
                            "mesh_term": term,
                        }
                    )

                    study_conditions_mesh.append(
                        {"mesh_key": mesh_key, "study_key": study_key}
                    )

    mesh_ancestors_list = study_data.get(f"{conditions_browse_index}.ancestors")
    if (
        isinstance(mesh_ancestors_list, (list, np.ndarray))
        and len(mesh_ancestors_list) > 0
    ):
        for mesh_ancestor in mesh_ancestors_list:
            ancestor_id = mesh_ancestor.get("id")
            ancestor_terms = mesh_ancestor.get("terms")

            if isinstance(ancestor_terms, str) and ancestor_terms:
                terms = ancestor_terms.split(",")
                for term in terms:
                    term = term.strip()
                    ancestor_key = generate_key(study_key, ancestor_id, term)
                    conditions_mesh_ancestors.append(
                        {
                            "mesh_ancestor_key": ancestor_key,
                            "study_key": study_key,
                            "mesh_ancestor_id": ancestor_id,
                            "mesh_ancestor_term": term,
                        }
                    )

                    study_conditions_mesh_ancestors.append(
                        {"mesh_ancestor_key": ancestor_key, "study_key": study_key}
                    )

    mesh_browse_leaves = study_data.get(f"{conditions_browse_index}.browseLeaves")
    if (
        isinstance(mesh_browse_leaves, (list, np.ndarray))
        and len(mesh_browse_leaves) > 0
    ):
        for browse_leaf in mesh_browse_leaves:
            leaf_id = browse_leaf.get("id")
            leaf_key = generate_key(study_key, leaf_id)

            conditions_browse_leaves.append(
                {
                    "leaf_key": leaf_key,
                    "study_key": study_key,
                    "name": browse_leaf.get("name"),
                    "as_found": browse_leaf.get("asFound"),
                    "relevance": browse_leaf.get("relevance"),
                }
            )

            study_conditions_browse_leaves.append(
                {"mesh_browse_leaf_key": leaf_key, "study_key": study_key}
            )

    mesh_browse_branches = study_data.get(f"{conditions_browse_index}.browseBranches")

    if (
        isinstance(mesh_browse_branches, (list, np.ndarray))
        and len(mesh_browse_branches) > 0
    ):
        for browse_branch in mesh_browse_branches:
            branch_id = browse_branch.get("id")
            branch_key = generate_key(study_key, branch_id)

            conditions_browse_branches.append(
                {
                    "branch_key": branch_key,
                    "study_key": study_key,
                    "name": browse_branch.get("name"),
                    "as_found": browse_branch.get("asFound"),
                    "relevance": browse_branch.get("relevance"),
                }
            )

            study_conditions_browse_branches.append(
                {"mesh_browse_branch_key": branch_key, "study_key": study_key}
            )

    # else:
    #     log.warning(f"No conditions_mesh found for study {study_key}, page - NCT ID {nct_id}")

    return (
        conditions_mesh,
        study_conditions_mesh,
        conditions_mesh_ancestors,
        study_conditions_mesh_ancestors,
        conditions_browse_leaves,
        study_conditions_browse_leaves,
        conditions_browse_branches,
        study_conditions_browse_branches,
    )
