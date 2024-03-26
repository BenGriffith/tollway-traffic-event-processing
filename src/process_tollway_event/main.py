import base64
import os

from google.cloud import redis_v1
import redis

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")


def process_tollway_traffic(data, context):
    tollway_event = base64.b64decode(data["data"]).decode("utf-8")