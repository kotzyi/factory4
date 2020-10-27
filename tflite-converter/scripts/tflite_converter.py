import os
import tensorflow as tf


def main():
    model_file_name = os.getenv('MODEL_FILE_NAME')
    saved_model_dir = os.getenv('EXPORTED_MODEL_SAVED_PATH')
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.experimental_new_converter = True
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    tflite_model = converter.convert()

    model_file_path = os.path.join(saved_model_dir, model_file_name)

    with open(model_file_path, "wb") as f:
        f.write(tflite_model)


if __name__ == "__main__":
    main()
