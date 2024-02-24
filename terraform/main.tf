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

resource "google_bigquery_table" "fact_tollway_events" {
    dataset_id = google_bigquery_dataset.tollway_traffic.dataset_id
    table_id = "fact_tollway_events"
    deletion_protection = false

    time_partitioning {
      type = "DAY"
      field = "timestamp"
    }

    schema = <<EOF
    [
        {
            "name": "event_id",
            "type": "string",
            "mode": "required"
        },
        {
            "name": "vehicle_id",
            "type": "string",
            "mode": "required"
        },
        {
            "name": "tollway_id",
            "type": "string",
            "mode": "required"
        },
        {
            "name": "timestamp",
            "type": "timestamp",
            "mode": "required"
        }
    ]
}
