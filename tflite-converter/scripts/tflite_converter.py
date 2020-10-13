import argparse
import tensorflow as tf


parser = argparse.ArgumentParser()

parser.add_argument("-d", "--saved_model_dir", default="", type=str, help="Path to the folder where the exported model files are stored")
# parser.add_argument("-u", "--upload_model_path", type=str, help="Path ot the blob path where the tensorflow lite model files are stored")

args = parser.parse_args()

converter = tf.lite.TFLiteConverter.from_saved_model(args.saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.experimental_new_converter = True
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
tflite_model = converter.convert()

open("/home/tflite-converter/exported-models/model.tflite", "wb").write(tflite_model)
