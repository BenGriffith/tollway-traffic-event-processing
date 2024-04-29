import uuid
import hashlib
from typing import NamedTuple


class TollwayEvent(NamedTuple):
    year: str
    make: str
    model: str
    category: str
    license_plate: str
    vin: str
    state: str
    primary_color: str
    tollway_state: str
    tollway_name: str
    timestamp: str


def hash_string(input_string):
    full_hash = hashlib.sha256(input_string.encode("utf-8")).hexdigest()
    truncated_hash = int(full_hash[:12], 16)
    return truncated_hash


def create_rows(message_data):

    fact_tollway_event_row = {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": hash_string(message_data.vin),
        "tollway_id": hash_string(message_data.tollway_name),
        "timestamp": message_data.timestamp,
    }

    dim_vehicle_row = {
        "vehicle_id": hash_string(message_data.vin),
        "make_id": hash_string(message_data.make),
        "model_id": hash_string(message_data.model),
        "category_id": hash_string(message_data.category),
        "state_id": hash_string(message_data.state),
        "primary_color": message_data.primary_color,
        "vin": message_data.vin,
        "year": message_data.year,
        "license_plate": message_data.license_plate,
    }

    dim_tollway_row = {
        "tollway_id": hash_string(message_data.tollway_name),
        "tollway_name": message_data.tollway_name,
        "state_id": hash_string(message_data.state),
    }

    dim_state_row = {
        "state_id": hash_string(message_data.state),
        "state": message_data.state,
    }

    dim_model_row = {
        "model_id": hash_string(message_data.model),
        "model": message_data.model,
    }

    dim_category_row = {
        "category_id": hash_string(message_data.category),
        "category": message_data.category,
    }

    dim_make_row = {
        "make_id": hash_string(message_data.make),
        "make": message_data.make,
    }

    return {
        "fact_tollway_event": fact_tollway_event_row,
        "dim_vehicle": dim_vehicle_row,
        "dim_tollway": dim_tollway_row,
        "dim_state": dim_state_row,
        "dim_model": dim_model_row,
        "dim_category": dim_category_row,
        "dim_make": dim_make_row,
    }
