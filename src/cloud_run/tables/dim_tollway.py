from google.api_core.exceptions import GoogleAPIError

from utils.table_logger import setup_logger
from utils.constants import DATASET_ID, PROJECT_ID, TABLES
from utils.helpers import hash_string


def get_tollway_names(bigquery_client):
    table = f"{PROJECT_ID}.{DATASET_ID}.{TABLES['dim_tollway']}"
    query = f"""
        SELECT DISTINCT tollway_name
        FROM `{table}`
    """
    tollway_names = bigquery_client.query(query).result()
    return [row["tollway_name"] for row in tollway_names]


def insert_row(bigquery_client, message_data):

    tollway_names = get_tollway_names(bigquery_client)
    tollway_logger = setup_logger(True)

    if message_data.tollway_name in tollway_names:
        tollway_logger.info(f"{message_data.tollway_name} exists in dim_tollway")
        return

    dim_tollway_row = {
        "tollway_id": hash_string(message_data.tollway_name),
        "tollway_name": message_data.tollway_name,
    }

    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLES["dim_tollway"])

    try:
        dim_tollway_errors = bigquery_client.insert_rows_json(table_ref, [dim_tollway_row])
        tollway_logger.info(f"Successfully inserted {message_data.tollway_name} into BigQuery")
    except GoogleAPIError as ge:
        tollway_logger.error(
            "Encountered errors while inserting tollway " f"{message_data.tollway_name} into BigQuery: {ge}"
        )
        raise
    except Exception as e:
        tollway_logger.error(
            "An unexpected error occurred while inserting tollway "
            f"{message_data.tollway_name} into BigQuery: {e}",
            exc_info=True,
        )
        raise
