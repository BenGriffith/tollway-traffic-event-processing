resource "google_storage_bucket" "tollway_traffic" {
    name = "tollway-traffic"
    location = "us"
}

resource "google_cloudfunctions_function" "tollway_event" {
    name = "process-tollway-event"
    description = "Processes tollway traffic events"
    runtime = "python39"
    available_memory_mb = 256
    timeout = "180s"
    source_archive_bucket = ""
    source_archive_object = ""
    entry_point = "process_streaming_data"
    trigger_topic = "tollway"
}

resource "google_redis_instance" "tollway_cache" {
    name = "tollway-traffic-cache"
    tier = "STANDARD_HA"
    memory_size_gb = 1
    location_id = "us-central1"
}

resource "google_bigquery_dataset" "tollway_traffic" {
    dataset_id = "tollway_traffic"
    location = "us-central1"
}

resource "google_bigquery_table" "fact_tollway_event" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "fact_tollway_event"
    deletion_protection = false

    time_partitioning {
      type = "DAY"
      field = "timestamp"
    }

    schema = jsonencode([
        {
            "name": "event_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "vehicle_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "tollway_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "timestamp",
            "type": "timestamp",
            "mode": "required"
        }
    ])
}

resource "google_bigquery_table" "dim_tollway" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "dim_tollway"
    deletion_protection = false

    schema = jsonencode([
        {
            "name": "tollway_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "tollway_name",
            "type": "string",
            "mode": "nullable"
        }
    ])
}

resource "google_bigquery_table" "dim_vehicle" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "dim_vehicle"
    deletion_protection = false

    schema = jsonencode([
        {
            "name": "vehicle_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "make_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "model_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "category_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "state_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "color",
            "type": "string",
            "mode": "nullable"
        },
        {
            "name": "vin",
            "type": "string",
            "mode": "nullable"
        },
        {
            "name": "year",
            "type": "string",
            "mode": "nullable"
        },
        {
            "name": "license_plate",
            "type": "string",
            "mode": "nullable"
        }
    ])
}

resource "google_bigquery_table" "dim_make" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "dim_make"
    deletion_protection = false

    schema = jsonencode([
        {
            "name": "make_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "make",
            "type": "string",
            "mode": "nullable"
        }
    ])
}

resource "google_bigquery_table" "dim_model" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "dim_model"
    deletion_protection = false

    schema = jsonencode([
        {
            "name": "model_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "model",
            "type": "string",
            "mode": "nullable"
        }
    ])
}

resource "google_bigquery_table" "dim_category" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "dim_category"
    deletion_protection = false

    schema = jsonencode([
        {
            "name": "category_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "category",
            "type": "string",
            "mode": "nullable"
        }
    ])
}

resource "google_bigquery_table" "dim_state" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "dim_state"
    deletion_protection = false

    schema = jsonencode([
        {
            "name": "state_id",
            "type": "integer",
            "mode": "required"
        },
        {
            "name": "state",
            "type": "string",
            "mode": "nullable"
        }
    ])
}
