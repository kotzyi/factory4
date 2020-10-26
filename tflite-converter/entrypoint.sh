#!/bin/bash

echo "CONVERTING MODEL TO TF-LITE MODEL"
python /home/tflite-converter/scripts/tflite_converter.py -d $EXPORTED_MODEL_SAVED_PATH

echo "UPLOADING TO AZURE FILESHARE"
python /home/tflite-converter/scripts/upload_by_fileshare.py -s $AZURE_SHARE_NAME -d $AZURE_DIR_PATH -l $EXPORTED_MODEL_SAVED_PATH