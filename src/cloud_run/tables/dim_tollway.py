from utils.constants import TABLES
from utils.helpers import hash_string
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    tollway_id = hash_string(message_data.tollway_name)
    dim_tollway_row = {
        "tollway_id": tollway_id,
        "tollway_name": message_data.tollway_name,
    }

    table_manager = TableManager(client=bigquery_client, table=TABLES["dim_tollway"], row=dim_tollway_row)
    tollway_exists = table_manager.not_exists(key=tollway_id)
    if tollway_exists:
        table_manager.insert
