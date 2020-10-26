#!/bin/bash

echo "CONVERTING MODEL TO TF-LITE MODEL"
python /home/tflite-converter/scripts/tflite_converter.py -d $EXPORTED_MODEL_SAVED_PATH

echo "UPLOADING TO AZURE FILESHARE"
python /home/tflite-converter/scripts/upload_by_fileshare.py -l $EXPORTED_MODEL_SAVED_PATH