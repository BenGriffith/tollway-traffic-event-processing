import os

PROJECT_ID = os.getenv("PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLES = [
    os.getenv("FACT_TOLLWAY_EVENT"),
    os.getenv("DIM_TOLLWAY"),
    os.getenv("DIM_VEHICLE"),
    os.getenv("DIM_MAKE"),
    os.getenv("DIM_MODEL"),
    os.getenv("DIM_CATEGORY"),
    os.getenv("DIM_STATE"),
]
KEYS = "event_id tollway_id vehicle_id make_id model_id category_id state_id".split(" ")
TABLES_KEYS = dict(zip(TABLES, KEYS))
MAX_MESSAGES = 5
STREAM_TIMEOUT = 300
