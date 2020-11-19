#!/bin/bash
LEARNING_RATE=1e-3 \
EPOCHS=3 \
MODEL_SAVE_PATH=/home/classifier/models/exported-models \
PRE_TRAINED_MODEL_PATH=/home/classifier/models/pre-trained-models \
IMAGE_DIR_PATH=/home/classifier/images \
MODEL_NAME=b0 \
BATCH_SIZE=1 \
NUM_CLASSES=2 \
AZURE_SHARE_NAME=models \
AZURE_CLASS_IMAGE_DIR_PATH=detach/train_images \
AZURE_MODEL_DIR_PATH=detach/models \
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=storagefactory4kr;AccountKey=Q9dUPJxdR3a5RU4F0r3lhK9r9ajKmbASVLx3uxclkRvwLDW2FOx9T+9uvoK6tVRxPy4/9Mi64pP/tbfAf5Ncnw==;EndpointSuffix=core.windows.net" \
docker-compose up --build