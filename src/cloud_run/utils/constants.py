import os

PROJECT_ID = os.getenv("PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLES = {
    "fact_tollway_event": os.getenv("FACT_TOLLWAY_EVENT"),
    "dim_tollway": os.getenv("DIM_TOLLWAY"),
    "dim_vehicle": os.getenv("DIM_VEHICLE"),
    "dim_make": os.getenv("DIM_MAKE"),
    "dim_model": os.getenv("DIM_MODEL"),
    "dim_category": os.getenv("DIM_CATEGORY"),
    "dim_state": os.getenv("DIM_STATE"),
}

KEYS = {
    "fact_tollway_event": "event_id",
    "dim_tollway": "tollway_id",
    "dim_vehicle": "vehicle_id",
    "dim_make": "make_id",
    "dim_model": "model_id",
    "dim_category": "category_id",
    "dim_state": "state_id",
}
