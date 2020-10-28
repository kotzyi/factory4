#!/bin/bash

TRAIN_IMAGE_PATH=/home/detector/workspace/images/train \
TRAIN_IMAGE_LABEL_PATH=/home/detector/workspace/annotations/label_map.pbtxt \
TRAIN_IMAGE_TFRECORD_PATH=/home/detector/workspace/annotations/train.record \
TEST_IMAGE_PATH=/home/detector/workspace/images/test \
TEST_IMAGE_LABEL_PATH=/home/detector/workspace/annotations/label_map.pbtxt \
TEST_IMAGE_TFRECORD_PATH=/home/detector/workspace/annotations/test.record \
MODEL_PATH=/home/detector/workspace/models/trained-models \
MODEL_PIPELINE_CONFIG_PATH=/home/detector/workspace/models/trained-models/pipeline.config \
INPUT_TYPE=image_tensor \
MODEL_OUTPUT_PATH=/home/detector/workspace/models/exported-models \
TRAINED_CHECKPOINT_PATH=/home/detector/workspace/models/trained-models \
PRE_TRAINED_MODEL_PATH=/home/detector/workspace/models/pre-trained-models \
AZURE_STORAGE_CONNECTION_STRING= \
MODEL_NAME=efficientdet_d0_coco17_tpu-32 \
docker-compose up --build