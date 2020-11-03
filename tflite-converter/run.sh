#!/bin/bash
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
MODEL_FILE_NAME=block_model_2.tflite \
AZURE_STORAGE_CONNECTION_STRING="" \
EXPORTED_MODEL_SAVED_PATH=/home/tflite-converter/exported-models/saved_model \
docker-compose up --build