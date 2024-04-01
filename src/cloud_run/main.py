import json

from google.cloud import pubsub_v1, bigquery

from src.cloud_run.constants import (
    PROJECT_ID,
    SUBSCRIPTION_ID,
    DATASET_ID,
    TABLES,
)

subscriber_client = pubsub_v1.SubscriberClient()
bigquery_client = bigquery.Client()

def messages_to_bigquery(messages):
    ...