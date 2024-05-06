# Overview

This project is designed to automate the collection, processing, and analysis of tollway traffic data using a fully managed, serverless architecture on Google Cloud Platform (GCP). The solution leverages multiple GCP services, including Pub/Sub for data ingestion, Cloud Run and Cloud Functions for data processing, Cloud Memorystore for data storage, and BigQuery for data storage and analytics. The use of Terraform allows for efficient infrastructure as code, enabling reproducible deployments.

# Architecture

## Diagrams
1. **Entity Relationship Diagram (ERD)**: This diagram provides a visual representation of the data model used within BigQuery. It details how different entities such as vehicles, tollways, and events are interlinked.

![ERD](assets/erd.png "Entity Relationship Diagram")

2. **System Workflow**: This diagram outlines the complete data flow through the system, from the initial data generation by the Tollway Traffic Generator through to data processing and storage.

![System Workflow](assets/mind-map.png "System Workflow")
