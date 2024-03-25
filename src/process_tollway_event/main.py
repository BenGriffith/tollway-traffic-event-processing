import base64


def process_tollway_traffic(data, context):
    tollway_event = base64.b64decode(data["data"]).decode("utf-8")
    print(f"tollway event: {tollway_event}")
