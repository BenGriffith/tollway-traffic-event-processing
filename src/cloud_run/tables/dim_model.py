from utils.helpers import hash_string
from utils.constants import TABLES
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    model_id = hash_string(message_data.model)
    dim_model_row = {
        "model_id": model_id,
        "model": message_data.model,
    }

    table_manager = TableManager(client=bigquery_client, table=TABLES["dim_model"], row=dim_model_row)
    model_not_exist = table_manager.not_exist(key=model_id)
    if model_not_exist:
        table_manager.insert
