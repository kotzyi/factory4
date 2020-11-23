#!/bin/bash

echo "CONVERTING MODEL TO TF-LITE MODEL"
python /home/converter/scripts/tflite_converter.py

echo "UPLOADING TO AZURE FILESHARE"
python /home/converter/scripts/upload_by_fileshare.py