import os
import tensorflow as tf


def main():
    model_file_name = str(os.getenv('MODEL_FILENAME_PREFIX')) + "_" + os.getenv('MODEL_FILE_NAME')
    saved_model_dir = os.getenv('EXPORTED_MODEL_SAVED_PATH')
    image_size = int(os.getenv('IMAGE_SIZE'))
    image_dir = os.getenv('IMAGE_DIR')
    image_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        image_dir,
        validation_split=None,
        label_mode=None,
        seed=1337,
        shuffle=True,
        image_size=(image_size, image_size),
        batch_size=1,
    )

    def representative_data_gen():
        for input_value in image_dataset.take(100):
            # Model has only one input so each data point has one element.
            yield [input_value]

    model = tf.saved_model.load(saved_model_dir)
    model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY].inputs[0].set_shape([1, image_size, image_size, 3])
    tf.saved_model.save(model, "saved_model_updated",
                        signatures=model.signatures[tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY])
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir='saved_model_updated', signature_keys=['serving_default'])
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_data_gen
    converter.experimental_new_converter = True
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8, tf.lite.OpsSet.SELECT_TF_OPS]
    converter.inference_input_type = tf.uint8
    converter.inference_output_type = tf.uint8
    tflite_model = converter.convert()

    model_file_path = os.path.join(saved_model_dir, model_file_name)

    with open(model_file_path, "wb") as f:
        f.write(tflite_model)


if __name__ == "__main__":
    main()
