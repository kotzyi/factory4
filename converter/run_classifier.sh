#!/bin/bash
IMAEG_SIZE=300 \
MODEL_FILENAME_PREFIX=b0 \
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
MODEL_FILE_NAME=classifier_with_block_1125_1_with_images_1.tflite \
AZURE_STORAGE_CONNECTION_STRING="" \
EXPORTED_MODEL_SAVED_PATH=/home/converter/exported-models/saved_model \
docker-compose -f docker-compose-classifier.yml up --build