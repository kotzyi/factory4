#!/bin/bash
IMAGE_SIZE=640 \
IMAGE_DIR=/home/converter/images \
MODEL_FILENAME_PREFIX=mobilenet_v2 \
AZURE_SHARE_NAME=models \
AZURE_MODEL_DIR_PATH=detach/models \
MODEL_FILE_NAME=detector_640_0303.tflite \
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=storagefactory4kr;AccountKey=Q9dUPJxdR3a5RU4F0r3lhK9r9ajKmbASVLx3uxclkRvwLDW2FOx9T+9uvoK6tVRxPy4/9Mi64pP/tbfAf5Ncnw==;EndpointSuffix=core.windows.net" \
EXPORTED_MODEL_SAVED_PATH=/home/converter/exported-models/saved_model \
docker-compose -f docker-compose-object-detector.yml up --build