import uuid

from google.api_core.exceptions import GoogleAPIError

from utils.constants import DATASET_ID, TABLES
from utils.helpers import hash_string
from utils.table_logger import setup_logger


def insert_row(bigquery_client, message_data):

    event_id = str(uuid.uuid4())
    fact_tollway_event_row = {
        "event_id": event_id,
        "vehicle_id": hash_string(message_data.vin),
        "tollway_id": hash_string(message_data.tollway_name),
        "timestamp": message_data.timestamp,
    }

    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLES["fact_tollway_event"])
    tollway_logger = setup_logger(True)

    try:
        fact_tollway_event_errors = bigquery_client.insert_rows_json(table_ref, [fact_tollway_event_row])
        tollway_logger.info(f"Successfully inserted event {event_id} into BigQuery")
    except GoogleAPIError as ge:
        tollway_logger.error(f"Encountered errors while inserting event {event_id} into BigQuery: {ge}")
        raise
    except Exception as e:
        tollway_logger.error(
            f"An unexpected error occurred while inserting event {event_id} into BigQuery: {e}", exc_info=True
        )
        raise
