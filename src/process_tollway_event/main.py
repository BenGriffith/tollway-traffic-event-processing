from datetime import datetime
import base64
import os
import json
import redis

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, ssl=True)

def process_tollway_traffic(event, context):
    message = base64.b64decode(event["data"]).decode("utf-8")
    message_data = json.loads(message)

    vehicle_id = message_data.get("vin")
    timestamp = message_data.get("timestamp")

    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f %z")
    timestamp_key = timestamp.strftime("%Y%m%d%H%M%S")

    redis_key = f"{vehicle_id}:{timestamp_key}"
    message_json = json.dumps(message_data)
    redis_client.setex(redis_key, 1800, message_json)

    print(f"Stored data in Redis with key: {redis_key}")
