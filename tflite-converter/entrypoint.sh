#!/bin/bash
python /home/tflite-converter/scripts/tflite_converter.py -d $EXPORTED_MODEL_SAVED_PATH
python /home/tflite-converter/scripts/upload_by_fileshare.py
