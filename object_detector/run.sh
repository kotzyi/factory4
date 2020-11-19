#!/bin/bash

NUM_CLASS=2 \
IMAGE_SIZE=512 \
BATCH_SIZE=16 \
TOTAL_STEP=500 \
NUM_BOXES=10 \
REPLICAS_TO_AGGREGATE=8 \
MODEL_TYPE=detection \
WARMUP_STEP=0 \
CLASSIFICATION_WEIGHT=0.0 \
LOCALIZATION_WEIGHT=1.0 \
IMAGE_PATH=/home/detector/images \
IMAGE_LABEL_DIR=/home/detector/annotations/ \
TRAIN_IMAGE_PATH=/home/detector/images/train \
TRAIN_IMAGE_LABEL_PATH=/home/detector/annotations/label_map.pbtxt \
TRAIN_IMAGE_TFRECORD_PATH=/home/detector/annotations/train.record \
TEST_IMAGE_PATH=/home/detector/images/tester \
TEST_IMAGE_LABEL_PATH=/home/detector/annotations/label_map.pbtxt \
TEST_IMAGE_TFRECORD_PATH=/home/detector/annotations/tester.record \
TEST_IMAGE_RATIO=0.1 \
MODEL_PATH=/home/detector/models/trained-models \
MODEL_PIPELINE_CONFIG_PATH=/home/detector/models/trained-models/pipeline.config \
INPUT_TYPE=image_tensor \
MODEL_SAVE_PATH=/home/detector/models/exported-models \
TRAINED_CHECKPOINT_PATH=/home/detector/models/trained-models \
PRE_TRAINED_MODEL_PATH=/home/detector/models/pre-trained-models \
AZURE_STORAGE_CONNECTION_STRING="" \
MODEL_NAME=efficientdet_d0_coco17_tpu-32 \
AZURE_SHARE_NAME=models \
AZURE_OBJECT_IMAGE_DIR_PATH=detach/images \
AZURE_LABEL_DIR_PATH=detach/annotations \
AZURE_MODEL_DIR_PATH=detach/models \
docker-compose up --build