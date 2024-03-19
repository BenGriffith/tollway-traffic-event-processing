#!/bin/bash

cd "$(dirname "$0")/.."

cp requirements.txt src/process_tollway_event/

cd src/process_tollway_event/

zip -r ../../process_tollway_event.zip .

cd ../../

gsutil cp process_tollway_event.zip gs://tollway_traffic/cloud_function/process_tollway_event.zip
