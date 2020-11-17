import os
import tensorflow as tf


def main():
    model_file_name = os.getenv('MODEL_FILE_NAME')
    saved_model_dir = os.getenv('EXPORTED_MODEL_SAVED_PATH')

    model = tf.saved_model.load(saved_model_dir)
    model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs[0].set_shape([1, 224, 224, 3])
    tf.saved_model.save(model, "saved_model_updated",
                        signatures=model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY])
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir='saved_model_updated', signature_keys=['serving_default'])
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.experimental_new_converter = True
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
    tflite_model = converter.convert()

    model_file_path = os.path.join(saved_model_dir, model_file_name)

    with open(model_file_path, "wb") as f:
        f.write(tflite_model)


if __name__ == "__main__":
    main()
