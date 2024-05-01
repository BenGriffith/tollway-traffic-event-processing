import json

from google.cloud import pubsub_v1, bigquery
from fastapi import FastAPI, BackgroundTasks

from utils.helpers import TollwayEvent, create_rows
from utils.constants import TABLES, PROJECT_ID, SUBSCRIPTION_ID
from utils.table_logger import setup_logger
from tables.table_manager import TableManager


app = FastAPI()


def message_to_bigquery(message):
    bigquery_client = bigquery.Client()

    # row creation for each table
    message_data = json.loads(message.data.decode("utf-8"))
    rows = create_rows(message_data=TollwayEvent(**message_data))

    # table manager for each table
    for table, row in rows.items():
        table_manager = TableManager(
            client=bigquery_client,
            table=TABLES[table],
            row=row,
        )
        check = True if table != "fact_tollway_event" else False

        table_manager.execute(perform_check=check)


def process_messages():
    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path(project=PROJECT_ID, subscription=SUBSCRIPTION_ID)

    def callback(message):
        tollway_logger = setup_logger(True)
        tollway_logger.info(f"Received message: {message.data.decode('utf-8')}")
        message_to_bigquery(message)
        message.ack()

    streaming_pull = subscriber_client.subscribe(subscription_path, callback)
    try:
        streaming_pull.result(timeout=30)
    except Exception as e:
        print("Error or timeout occurred", e)
    finally:
        streaming_pull.cancel()

    return {"status": "Completed processing messages"}


@app.post("/trigger-processing/")
async def trigger_processing(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_messages)
    return {"message": "Processing started"}
