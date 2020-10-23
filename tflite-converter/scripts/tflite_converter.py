import os
import argparse
import tensorflow as tf


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--saved_model_dir", default="", type=str,
                        help="Path to the folder where the exported model files are stored")
    parser.add_argument("-f", "--model_file_name", default="model.tflite", type=str,
                        help="File name of converted model")
    args = parser.parse_args()

    converter = tf.lite.TFLiteConverter.from_saved_model(args.saved_model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.experimental_new_converter = True
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    tflite_model = converter.convert()

    model_file_path = os.path.join(args.saved_model_dir, args.model_file_name)

    with open(model_file_path, "wb") as f:
        f.write(tflite_model)


if __name__ == "__main__":
    main()
