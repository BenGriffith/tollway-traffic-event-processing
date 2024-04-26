from utils.constants import TABLES
from utils.helpers import hash_string
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    tollway_id = hash_string(message_data.tollway_name)
    state_id = hash_string(message_data.tollway_state)
    dim_tollway_row = {
        "tollway_id": tollway_id,
        "tollway_name": message_data.tollway_name,
        "state_id": state_id,
    }

    dim_tollway_manager = TableManager(
        client=bigquery_client, table=TABLES["dim_tollway"], row=dim_tollway_row
    )
    tollway_not_exist = dim_tollway_manager.not_exist(key=tollway_id)
    if tollway_not_exist:
        dim_tollway_manager.insert

    dim_state_manager = TableManager(
        client=bigquery_client,
        table=TABLES["dim_state"],
        row={"state_id": state_id, "state": message_data.tollway_state},
    )
    state_not_exist = dim_state_manager.not_exist(key=state_id)
    if state_not_exist:
        dim_state_manager.insert
