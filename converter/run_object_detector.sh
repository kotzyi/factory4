#!/bin/bash
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
MODEL_FILE_NAME=detector_1.tflite \
AZURE_STORAGE_CONNECTION_STRING="" \
EXPORTED_MODEL_SAVED_PATH=/home/converter/exported-models/saved_model \
docker-compose -f docker-compose-object-detector.yml up --build