#!/bin/bash

echo "CLEAR EX-TRAINED-MODEL AND IMAGES"
rm -rf $MODEL_SAVE_PATH/*

echo "UPDATE EFFICIENT-NET LATEST WEIGHT"
python /home/classifier/efficient_weight_update.py \
  --model $MODEL_NAME \
  --notop \
  --ckpt $PRE_TRAINED_MODEL_PATH/noisy-student-efficientnet-$MODEL_NAME/model.ckpt \
  --o $PRE_TRAINED_MODEL_PATH/$MODEL_NAME.h5

echo "TRAIN CLASSIFIER"
python /home/classifier/train.py
