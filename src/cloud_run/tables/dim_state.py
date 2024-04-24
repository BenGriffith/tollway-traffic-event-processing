from utils.helpers import hash_string
from utils.constants import TABLES
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    state_id = hash_string(message_data.state)
    dim_state_row = {
        "state_id": state_id,
        "state": message_data.state,
    }

    table_manager = TableManager(client=bigquery_client, table=TABLES["dim_state"], row=dim_state_row)
    state_not_exist = table_manager.not_exist(key=state_id)
    if state_not_exist:
        table_manager.insert
