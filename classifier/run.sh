#!/bin/bash
LEARNING_RATE=1e-3 \
EPOCHS=100 \
MODEL_SAVE_PATH=/home/classifier/models/exported-models \
PRE_TRAINED_MODEL_PATH=/home/classifier/models/pre-trained-models \
TRAIN_IMAGE_DIR_PATH=/home/classifier/images/train \
VAL_IMAGE_DIR_PATH=/home/classifier/images/val \
MODEL_NAME=b7 \
BATCH_SIZE=16 \
NUM_CLASSES=2 \
AZURE_SHARE_NAME=models \
AZURE_CLASS_IMAGE_DIR_PATH=detach/images_1 \
AZURE_MODEL_DIR_PATH=detach/models \
AZURE_STORAGE_CONNECTION_STRING="" \
docker-compose up --build