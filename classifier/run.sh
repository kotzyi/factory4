#!/bin/bash
PYTHONPATH=/home/classifier/ \
IMAGE_DIR_PATH=/home/classifier/images \
MODEL_NAME=efficientnetb0 \
BATCH_SIZE=16 \
NUM_CLASSES=2 \
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
AZURE_STORAGE_CONNECTION_STRING="" \
docker-compose up --build