from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_identification_module(study_key: str, study_data: pd.Series) -> Tuple:

    secondary_ids = []
    nct_aliases = []

    identification_index = NON_SCALAR_FIELDS["identification"]["index_field"]

    # Secondary id infos
    secondary_id_infos = study_data.get(f"{identification_index}.secondaryIdInfos")

    if (
        isinstance(secondary_id_infos, (list, np.ndarray))
        and len(secondary_id_infos) > 0
    ):
        for secondary_id_info in secondary_id_infos:
            secondary_id = secondary_id_info.get("id")
            secondary_id_key = generate_key(study_key, secondary_id)

            secondary_ids.append(
                {
                    "secondary_id_key": secondary_id_key,
                    "study_key": study_key,
                    "id": secondary_id,
                    "type": secondary_id_info.get("type"),
                    "domain": secondary_id_info.get("domain"),
                    "link": secondary_id_info.get("link"),
                }
            )

        # nct id aliases
        nct_id_aliases = study_data.get(f"{identification_index}.nctIdAliases")

        if isinstance(nct_id_aliases, (list, np.ndarray)) and len(nct_id_aliases) > 0:
            for nct_id_alias in nct_id_aliases:
                nct_aliases.append(
                    {
                        "study_key": study_key,
                        "id_alias": nct_id_alias,
                    }
                )

    return secondary_ids, nct_aliases
