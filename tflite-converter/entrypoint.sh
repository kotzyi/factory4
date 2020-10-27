#!/bin/bash

echo "CONVERTING MODEL TO TF-LITE MODEL"
python /home/tflite-converter/scripts/tflite_converter.py

echo "UPLOADING TO AZURE FILESHARE"
python /home/tflite-converter/scripts/upload_by_fileshare.py