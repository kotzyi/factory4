#!/bin/bash
EPOCHS=10 \
MODEL_SAVE_PATH=/home/classifier/models/exported-models/ \
PRE_TRAINED_MODEL_PATH=/home/classifier/models/pre-trained-models/ \
IMAGE_DIR_PATH=/home/classifier/images \
MODEL_NAME=efficientnet-b1 \
BATCH_SIZE=32 \
NUM_CLASSES=2 \
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
AZURE_STORAGE_CONNECTION_STRING="" \
docker-compose up --build