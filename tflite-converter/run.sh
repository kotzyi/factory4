#!/bin/bash
MODEL_FILE_NAME=model.tflite \
AZURE_STORAGE_CONNECTION_STRING= \
EXPORTED_MODEL_SAVED_PATH=/home/tflite-converter/exported-models/saved_model \
docker-compose up --build

