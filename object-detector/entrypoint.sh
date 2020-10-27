#!/bin/bash

echo "DOWNLOAD IMAGES FROM FILESHARE"
python /home/detector/scripts/download_from_fileshare.py

echo "CREATE TRAIN TFRECORD"
python /home/detector/scripts/generate_tfrecord.py -x $TRAIN_IMAGE_PATH -l $TRAIN_IMAGE_LABEL_PATH -o $TRAIN_IMAGE_TFRECORD_PATH

echo "CREATE TEST TFRECORD"
python /home/detector/scripts/generate_tfrecord.py -x $TEST_IMAGE_PATH -l $TEST_IMAGE_LABEL_PATH -o $TEST_IMAGE_TFRECORD_PATH

echo "TRAINING A MODEL"
python /home/detector/models/research/object_detection/model_main_tf2.py --model_dir=$MODEL_PATH --pipeline_config_path=$MODEL_PIPELINE_CONFIG_PATH

echo "EXPORTING"
python /home/detector/models/research/object_detection/exporter_main_v2.py --input_type=$INPUT_TYPE --pipeline_config_path=$MODEL_PIPELINE_CONFIG_PATH --trained_checkpoint_dir=$TRAINED_CHECKPOINT_PATH --output_directory=$MODEL_OUTPUT_PATH
