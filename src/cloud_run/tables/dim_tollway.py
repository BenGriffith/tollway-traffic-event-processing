from constants import DATASET_ID, PROJECT_ID, TABLES
from table_logging import table_logger
from utils import hash_string


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

    if message_data.tollway_name in tollway_names:
        tollway_logger = table_logger.setup_logger(True)
        tollway_logger.info(f"{message_data.tollway_name} exists in dim_tollway")
        return

    dim_tollway_row = {
        "tollway_id": hash_string(message_data.tollway_name),
        "tollway_name": message_data.tollway_name,
    }

    table_ref = bigquery_client.dataset(DATASET_ID).table(TABLES["dim_tollway"])
    dim_tollway_errors = bigquery_client.insert_rows_json(table_ref, [dim_tollway_row])

    if dim_tollway_errors:
        ...
    else:
        ...
