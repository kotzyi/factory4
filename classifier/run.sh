#!/bin/bash
LEARNING_RATE=1e-4 \
EPOCHS=30 \
MODEL_SAVE_PATH=/home/classifier/models/exported-models \
PRE_TRAINED_MODEL_PATH=/home/classifier/models/pre-trained-models \
IMAGE_DIR_PATH=/home/classifier/images \
MODEL_NAME=b0 \
BATCH_SIZE=16 \
NUM_CLASSES=2 \
AZURE_SHARE_NAME=models \
AZURE_CLASS_IMAGE_DIR_PATH=detach/block_images \
AZURE_MODEL_DIR_PATH=detach/models \
AZURE_STORAGE_CONNECTION_STRING="" \
docker-compose up --build