from typing import Tuple
import logging
import pandas as pd
import numpy as np
from include.etl.transformation.config import NON_SCALAR_FIELDS
from include.etl.transformation.utils import generate_key

log = logging.getLogger("airflow.task")


def transform_contacts_location_module(study_key: str, study_data: pd.Series) -> Tuple:
    central_contacts = []
    study_central_contacts = []
    locations = []
    study_locations = []

    contacts_locations_index = NON_SCALAR_FIELDS["contacts_location"]["index_field"]

    # contacts
    central_contacts_list = study_data.get(
        f"{contacts_locations_index}.centralContacts"
    )

    if (
        isinstance(central_contacts_list, (list, np.ndarray))
        and len(central_contacts_list) > 0
    ):

        for central_contact in central_contacts_list:
            name = central_contact.get("name")
            role = central_contact.get("role")
            phone = central_contact.get("phone")
            email = central_contact.get("email")

            central_contact_key = generate_key(name, role, phone, email)

            central_contacts.append(
                {
                    "contact_key": central_contact_key,
                    "contact_name": name,
                    "contact_role": role,
                    "contact_phone": phone,
                    "contact_email": email,
                }
            )

            study_central_contacts.append(
                {
                    "study_key": study_key,
                    "contact_key": central_contact_key,
                }
            )

    # locations
    locations_list = study_data.get(f"{contacts_locations_index}.locations")

    if isinstance(locations_list, (list, np.ndarray)) and len(locations_list) > 0:
        for location in locations_list:
            facility = location.get("facility")
            city = location.get("city")
            state = location.get("state")
            country = location.get("country")

            location_key = generate_key(facility, city, state, country)
            curr_location = {
                "location_key": location_key,
                "facility": facility,
                "city": city,
                "state": state,
                "country": state,
            }
            geopoint = location.get("geoPoint")

            if isinstance(geopoint, dict) and geopoint:
                curr_location["lat"] = (
                    float(geopoint.get("lat")) if geopoint.get("lat") else None
                )
                curr_location["lon"] = (
                    float(geopoint.get("lon")) if geopoint.get("lon") else None
                )

            locations.append(curr_location)

            study_locations.append(
                {
                    "study_key": study_key,
                    "location_key": location_key,
                    "status": location.get("status"),
                    "contacts": location.get("contacts"),  # json blob
                }
            )

    return central_contacts, study_central_contacts, locations, study_locations
