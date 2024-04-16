import json

from google.cloud import pubsub_v1, bigquery

from tables import (
    fact_tollway_event,
    dim_tollway,
)

subscriber_client = pubsub_v1.SubscriberClient()
bigquery_client = bigquery.Client()


def messages_to_bigquery(bigquery_client, messages):

    for message in messages:
        message_data = json.loads(message.data.decode("utf-8"))

        fact_tollway_event.insert_row(bigquery_client, message_data)
        dim_tollway.insert_row(bigquery_client, message_data)
