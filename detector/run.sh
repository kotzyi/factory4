#!/bin/bash

NUM_CLASSES=2 \
IMAGE_SIZE=320 \
BATCH_SIZE=16 \
TOTAL_STEP=5000 \
NUM_BOXES=100 \
REPLICAS_TO_AGGREGATE=8 \
MODEL_TYPE=detection \
WARMUP_STEP=1000 \
CLASSIFICATION_WEIGHT=1.0 \
LOCALIZATION_WEIGHT=1.0 \
IMAGE_PATH=/home/detector/workspace/images \
IMAGE_LABEL_DIR=/home/detector/workspace/annotations/ \
TRAIN_IMAGE_PATH=/home/detector/workspace/images/train \
TRAIN_IMAGE_LABEL_PATH=/home/detector/workspace/annotations/label_map.pbtxt \
TRAIN_IMAGE_TFRECORD_PATH=/home/detector/workspace/annotations/train.record \
TEST_IMAGE_PATH=/home/detector/workspace/images/tester \
TEST_IMAGE_LABEL_PATH=/home/detector/workspace/annotations/label_map.pbtxt \
TEST_IMAGE_TFRECORD_PATH=/home/detector/workspace/annotations/tester.record \
TEST_IMAGE_RATIO=0.1 \
MODEL_PATH=/home/detector/workspace/models/trained-models \
MODEL_PIPELINE_CONFIG_PATH=/home/detector/workspace/models/trained-models/pipeline.config \
INPUT_TYPE=image_tensor \
MODEL_SAVE_PATH=/home/detector/workspace/models/exported-models \
TRAINED_CHECKPOINT_PATH=/home/detector/workspace/models/trained-models \
PRE_TRAINED_MODEL_PATH=/home/detector/workspace/models/pre-trained-models \
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=storagefactory4kr;AccountKey=Q9dUPJxdR3a5RU4F0r3lhK9r9ajKmbASVLx3uxclkRvwLDW2FOx9T+9uvoK6tVRxPy4/9Mi64pP/tbfAf5Ncnw==;EndpointSuffix=core.windows.net" \
MODEL_NAME=ssd_mobilenet_v2_320x320_coco17_tpu-8 \
AZURE_SHARE_NAME=models \
AZURE_OBJECT_IMAGE_DIR_PATH=detach/images \
AZURE_LABEL_DIR_PATH=detach/annotations \
AZURE_MODEL_DIR_PATH=detach/models \
docker-compose up --build
