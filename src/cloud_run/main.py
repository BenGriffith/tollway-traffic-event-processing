from typing import NamedTuple
import json
import uuid

from google.cloud import pubsub_v1, bigquery

from src.cloud_run.constants import (
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


def messages_to_bigquery(messages):
    rows_to_insert = []

    for message in messages:
        message_data = json.loads(message.data.decode("utf-8"))
        message_data = TollwayEvent(**message_data)

    fact_tollway_event_row = {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": "",
        "tollway_id": "",
        "timestamp": ""
    }