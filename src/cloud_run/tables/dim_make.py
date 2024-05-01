from utils.helpers import hash_string
from utils.constants import TABLES
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    make_id = hash_string(message_data.make)
    dim_make_row = {
        "make_id": make_id,
        "make": message_data.make,
    }

    table_manager = TableManager(client=bigquery_client, table=TABLES["dim_make"], row=dim_make_row)
    make_not_exist = table_manager.not_exist(key=make_id)
    if make_not_exist:
        table_manager.insert
