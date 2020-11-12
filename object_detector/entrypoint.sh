#!/bin/bash

echo "CLEAR EX-TRAINED-MODEL AND IMAGES"
rm -rf $MODEL_OUTPUT_PATH/*
rm -rf $IMAGE_LABEL_DIR/*
rm -rf $IMAGE_PATH/*
rm -rf $TRAIN_IMAGE_PATH/*
rm -rf $TEST_IMAGE_PATH/*
rm -rf $MODEL_PATH/*

echo "EDIT PIPELINE CONFIGURATION"
python /home/detector/scripts/edit_pipeline.py

echo "DOWNLOAD IMAGES FROM FILESHARE"
python /home/detector/scripts/download_from_fileshare.py

echo "DEVIDE IMAGES INTO TRAIN AND TEST"
python /home/detector/scripts/partition_dataset.py -x -i $IMAGE_PATH -r $TEST_IMAGE_RATIO

echo "CREATE TRAIN TFRECORD"
python /home/detector/scripts/generate_tfrecord.py -x $TRAIN_IMAGE_PATH -l $TRAIN_IMAGE_LABEL_PATH -o $TRAIN_IMAGE_TFRECORD_PATH

echo "CREATE TEST TFRECORD"
python /home/detector/scripts/generate_tfrecord.py -x $TEST_IMAGE_PATH -l $TEST_IMAGE_LABEL_PATH -o $TEST_IMAGE_TFRECORD_PATH

echo "TRAIN A MODEL"
python /home/detector/models/research/object_detection/model_main_tf2.py --model_dir=$MODEL_PATH --pipeline_config_path=$MODEL_PIPELINE_CONFIG_PATH

echo "EXPORTING"
python /home/detector/models/research/object_detection/exporter_main_v2.py --input_type=$INPUT_TYPE --pipeline_config_path=$MODEL_PIPELINE_CONFIG_PATH --trained_checkpoint_dir=$TRAINED_CHECKPOINT_PATH --output_directory=$MODEL_OUTPUT_PATH

echo "EVALUATE A MODEL"
python /home/detector/models/research/object_detection/model_main_tf2.py --model_dir=$MODEL_PATH --pipeline_config_path=$MODEL_PIPELINE_CONFIG_PATH --checkpoint_dir=$MODEL_PATH
