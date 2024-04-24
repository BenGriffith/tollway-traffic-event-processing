from utils.helpers import hash_string
from utils.constants import TABLES
from tables.table_manager import TableManager


def insert_row(bigquery_client, message_data):

    vehicle_id = hash_string(message_data.vin)
    dim_vehicle_row = {
        "vehicle_id": vehicle_id,
        "make_id": hash_string(message_data.make),
        "model_id": hash_string(message_data.model),
        "category_id": hash_string(message_data.category),
        "state_id": hash_string(message_data.state),
        "primary_color": message_data.primary_color,
        "vin": message_data.vin,
        "year": message_data.year,
        "license_plate": message_data.license_plate,
    }

    table_manager = TableManager(client=bigquery_client, table=TABLES["dim_vehicle"], row=dim_vehicle_row)
    vehicle_not_exist = table_manager.not_exist(key=vehicle_id)
    if vehicle_not_exist:
        table_manager.insert
