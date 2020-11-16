#!/bin/bash

echo "UPDATE EFFICIENT-NET LATEST WEIGHT"
python /home/classifier/efficient_weight_update.py \
  --model b1 \
  --notop \
  --ckpt $PRE_TRAINED_MODEL_PATH/noisy-student-efficientnet-b1/model.ckpt \
  --o $PRE_TRAINED_MODEL_PATH/$MODEL_NAME.h5

echo "TRAIN CLASSIFIER"
python /home/classifier/train.py
