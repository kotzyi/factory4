#!/bin/bash

echo "CONVERTING MODEL TO TF-LITE MODEL"
python /home/tflite_converter/scripts/tflite_converter.py

echo "UPLOADING TO AZURE FILESHARE"
python /home/tflite_converter/scripts/upload_by_fileshare.py