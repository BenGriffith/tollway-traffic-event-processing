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


def _hash(input_string):
    full_hash = hashlib.sha256(input_string.encode("utf-8")).hexdigest()
    truncated_hash = int(full_hash[:12], 16)
    return truncated_hash
