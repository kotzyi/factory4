#!/bin/bash
IMAGE_DIR_PATH=/datadrive/jlee/images \
MODEL_NAME=efficientnetb0 \
BATCH_SIZE=16 \
NUM_CLASSES=2 \
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
AZURE_STORAGE_CONNECTION_STRING="" \

docker-compose up --build