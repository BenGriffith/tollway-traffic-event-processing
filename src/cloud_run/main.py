import json
from concurrent.futures import TimeoutError

from google.cloud import pubsub_v1, bigquery
from fastapi import FastAPI, BackgroundTasks

from utils.helpers import TollwayEvent, create_rows
from utils.constants import PROJECT_ID, SUBSCRIPTION_ID, STREAM_TIMEOUT, MAX_MESSAGES
from utils.table_logger import setup_logger
from tables.table_manager import TableManager


app = FastAPI()


def message_to_bigquery(message):
    bigquery_client = bigquery.Client(project=PROJECT_ID)

    # row creation for each table
    message_data = json.loads(message.data.decode("utf-8"))
    rows = create_rows(message_data=TollwayEvent(**message_data))

    # table manager for each table
    for table, row in rows.items():
        table_manager = TableManager(
            client=bigquery_client,
            table=table,
            row=row,
        )
        check = True if table != "fact_tollway_event" else False
        table_manager.execute(perform_check=check)


def process_messages():
    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path(project=PROJECT_ID, subscription=SUBSCRIPTION_ID)
    flow_control = pubsub_v1.types.FlowControl(max_messages=MAX_MESSAGES)
    tollway_logger = setup_logger(True)

    def callback(message):
        tollway_logger.info(f"Received message: {message.data.decode('utf-8')}")
        message_to_bigquery(message)
        message.ack()

    streaming_pull = subscriber_client.subscribe(
        subscription=subscription_path,
        callback=callback,
        flow_control=flow_control,
    )

    with subscriber_client:
        try:
            streaming_pull.result(timeout=STREAM_TIMEOUT)
        except TimeoutError:
            streaming_pull.cancel()
            tollway_logger.info("Completed processing messages")


@app.post("/trigger-processing/")
async def trigger_processing(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_messages)
    return {"message": "Processing started"}
