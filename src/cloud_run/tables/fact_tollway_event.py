import uuid

from constants import DATASET_ID, TABLES

from cloud_run.utils import hash_string


def insert_row(bigquery_client, message_data):

    fact_tollway_event_row = {
        "event_id": str(uuid.uuid4()),
        "vehicle_id": hash_string(message_data.vin),
        "tollway_id": hash_string(message_data.tollway_name),
        "timestamp": message_data.timestamp,
    }

    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLES["fact_tollway_event"])
    fact_tollway_event_errors = bigquery_client.insert_rows_json(table_ref, [fact_tollway_event_row])
    if fact_tollway_event_errors:
        ...
        # implement logger
    else:
        ...
        # implement logger
