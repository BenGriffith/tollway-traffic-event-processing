import uuid

from tables.table_manager import TableManager
from utils.helpers import hash_string
from utils.constants import TABLES


def insert_row(bigquery_client, message_data):

    event_id = str(uuid.uuid4())
    fact_tollway_event_row = {
        "event_id": event_id,
        "vehicle_id": hash_string(message_data.vin),
        "tollway_id": hash_string(message_data.tollway_name),
        "timestamp": message_data.timestamp,
    }

    table_manager = TableManager(
        client=bigquery_client, table=TABLES["fact_tollway_event"], row=fact_tollway_event_row
    )
    table_manager.insert
