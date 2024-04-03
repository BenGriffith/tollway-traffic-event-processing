from typing import NamedTuple
import json
import uuid
import hashlib

from google.cloud import pubsub_v1, bigquery

from constants import (
    PROJECT_ID,
    SUBSCRIPTION_ID,
    DATASET_ID,
    TABLES,
)

subscriber_client = pubsub_v1.SubscriberClient()
bigquery_client = bigquery.Client()

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


def messages_to_bigquery(messages):
    rows_to_insert = []

    for message in messages:
        message_data = json.loads(message.data.decode("utf-8"))
        message_data = TollwayEvent(**message_data)

    fact_tollway_event_row = {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": _hash(message_data.vin),
        "tollway_id": _hash(message_data.tollway_name),
        "timestamp": message_data.timestamp
    }