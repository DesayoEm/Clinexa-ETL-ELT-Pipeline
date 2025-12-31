from typing import Set, Tuple

class DataQualityHandler:
    def __init__(self):
        pass

    @staticmethod
    def resolve_location_status(overall_status: str, location_statuses: Set) -> Tuple[str, str]:
        """
        Resolve conflicting location statuses.

        Rules:
        0. No statis -. USE overall status
        1. Single status -> use it
        2. {RECRUITING, NOT_YET_RECRUITING} -> RECRUITING (progression)
        3. RECRUITING + final status -> final status (study ended)
        4. RECRUITING + other -> RECRUITING_STATUS_UNCLEAR
        """

        actual = "ACTUAL"
        inferred = "INFERRED"
        overall = "OVERALL"

        if not location_statuses:
            status_type = overall
            return overall_status, status_type

        if len(location_statuses) == 1:
            status_type = actual
            return list(location_statuses)[0], status_type

        # progression case
        if location_statuses == {"RECRUITING", "NOT_YET_RECRUITING"}:
            status_type = inferred
            return "RECRUITING", status_type

        final_statuses = ["COMPLETED", "TERMINATED", "WITHDRAWN"]

        if "RECRUITING" in location_statuses:
            for final_status in final_statuses:
                if final_status in location_statuses:
                    status_type = inferred
                    return final_status, status_type  # study ended, can't recruit

            # RECRUITING plus other ambiguous statuses
            return "RECRUITING_STATUS_UNCLEAR", inferred

        # Multiple non-recruiting statuses - anyone works. makes no difference
        return list(location_statuses)[0], inferred

    
