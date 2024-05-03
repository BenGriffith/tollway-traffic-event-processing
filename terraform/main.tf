provider "google" {
    project = var.project_id
}

resource "google_storage_bucket" "tollway_traffic" {
    name = "tollway_traffic"
    location = "us"
    force_destroy = true

    provisioner "local-exec" {
      command = "${path.module}/../scripts/deploy_function.sh"
    }
}

resource "google_redis_instance" "tollway_cache" {
    name = "tollway-traffic-cache"
    tier = "STANDARD_HA"
    memory_size_gb = 1
    region = var.region
}

resource "google_vpc_access_connector" "serverless_connector" {
    name = "serverless-connector"
    region = var.region
    network = "default"
    ip_cidr_range = "10.8.0.0/28"
}

resource "google_cloudfunctions_function" "tollway_event" {
    name = "process-tollway-event"
    region = var.region
    description = "Processes tollway traffic events"
    runtime = "python39"
    available_memory_mb = 128
    timeout = 180
    source_archive_bucket = google_storage_bucket.tollway_traffic.name
    source_archive_object = "cloud_function/process_tollway_event.zip"
    entry_point = "process_tollway_traffic"
    vpc_connector = google_vpc_access_connector.serverless_connector.name

    environment_variables = {
        REDIS_HOST = google_redis_instance.tollway_cache.host
        REDIS_PORT = tostring(google_redis_instance.tollway_cache.port)
    }

    event_trigger {
        event_type = "google.pubsub.topic.publish"
        resource = "tollway"
    }
}

resource "null_resource" "docker_image" {
    triggers = {
      always_run = "${timestamp()}"
    }

    provisioner "local-exec" {
      command = "${path.module}/../scripts/cloud_run.sh"
    }
}

resource "google_cloud_run_service" "tollway_service" {
    depends_on = [ null_resource.docker_image ]

    name = "tollway-service"
    location = var.region

    template {
        spec {
          containers {
            image = "gcr.io/${var.project_id}/tollway-traffic:latest"

            env {
                name = "PROJECT_ID"
                value = var.project_id
            }
            env {
                name = "SUBSCRIPTION_ID"
                value = var.subscription_id
            }
            env {
                name = "DATASET_ID"
                value = "tollway_traffic"
            }
            env {
                name = "FACT_TOLLWAY_EVENT"
                value = "fact_tollway_event"
            }
            env {
                name = "DIM_TOLLWAY"
                value = "dim_tollway"
            }
            env {
                name = "DIM_VEHICLE"
                value = "dim_vehicle"
            }
            env {
                name = "DIM_MAKE"
                value = "dim_make"
            }
            env {
                name = "DIM_MODEL"
                value = "dim_model"
            }
            env {
                name = "DIM_CATEGORY"
                value = "dim_category"
            }
            env {
                name = "DIM_STATE"
                value = "dim_state"
            }
            command = ["uvicorn"]
            args = ["main:app", "--host", "0.0.0.0", "--port", "8080"]
          }
        }
    }

    traffic {
      percent = 100
      latest_revision = true
    }
}

resource "google_cloud_run_service_iam_member" "unauth_invoker" {
    project = var.project_id
    location = google_cloud_run_service.tollway_service.location
    service = google_cloud_run_service.tollway_service.name
    role = "roles/run.invoker"
    member = "allUsers"
}

resource "google_bigquery_dataset" "tollway_traffic" {
    dataset_id = "tollway_traffic"
    location = var.region
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
            "type": "string",
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
        },
        {
            "name": "state_id",
            "type": "integer",
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
            "name": "primary_color",
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
