#!/bin/bash

PROJECT_ID="playground"
IMAGE_NAME="tollway-traffic"
TAG="latest"

cd "$(dirname "$0")/.."

cp requirements.txt src/cloud_run/

cd src/cloud_run/

gcloud auth configure-docker

docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG} .

docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG}
