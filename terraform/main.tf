resource "google_storage_bucket" "tollway-traffic" {
    name = "tollway-traffic"
    location = "us"
}

resource "google_cloudfunctions_function" "tollway_event" {
    name = "tollway_event"
    description = "Cloud Function to process Pub/Sub Topic ID - tollway"
    runtime = "python39"
    entry_point = "main"
    timeout = "120s"
    available_memory_mb = "256"
    service_account_email = ""
    source_archive_object = ""
    trigger {
        pubsub = {
            topic = "tollway"
        }
    }
}
