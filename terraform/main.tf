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
