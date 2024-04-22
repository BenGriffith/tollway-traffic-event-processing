from google.api_core.exceptions import GoogleAPIError

from utils.constants import DATASET_ID, TABLES
from utils.table_logger import setup_logger


class TableManager:

    def __init__(self, client, table, row):
        self.bq_client = client
        self.table = table
        self.row = row

    def check_exits(self):
        pass

    def insert(self):
        table_ref = self.bq_client.dataset(DATASET_ID).table(TABLES[self.table])
        tollway_logger = setup_logger(True)

        try:

            # update TABLES in constants module to assist with logging

            table_insert = self.bq_client.insert_rows_json(table_ref, self.row)
            tollway_logger.info("Successfully inserted event into BigQuery")
        except (GoogleAPIError, Exception) as e:
            raise
