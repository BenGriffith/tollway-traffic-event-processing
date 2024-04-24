from utils.helpers import hash_string
from utils.constants import TABLES
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    category_id = hash_string(message_data.category)
    dim_category_row = {
        "category_id": category_id,
        "category": message_data.category,
    }

    table_manager = TableManager(client=bigquery_client, table=TABLES["dim_category"], row=dim_category_row)
    category_not_exist = table_manager.not_exist(key=category_id)
    if category_not_exist:
        table_manager.insert
