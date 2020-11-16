import os
import tensorflow as tf
from datasets import Dataset
from model import Classifier


def main():
    try:
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
        print("Running on TPU ", tpu.cluster_spec().as_dict()["worker"])
        tf.config.experimental_connect_to_cluster(tpu)
        tf.tpu.experimental.initialize_tpu_system(tpu)
        strategy = tf.distribute.experimental.TPUStrategy(tpu)
    except ValueError:
        print("Not connected to a TPU runtime. Using CPU/GPU strategy")
        strategy = tf.distribute.MirroredStrategy()

    batch_size = int(os.getenv("BATCH_SIZE"))
    num_classes = int(os.getenv("NUM_CLASSES"))
    image_dir = os.getenv("IMAGE_DIR_PATH")
    model_name = os.getenv("MODEL_NAME")

    classifier = Classifier(model_name, num_classes)
    image_size = classifier.image_size

    dataset = Dataset(batch_size, image_size, num_classes, image_dir)
    train_dataset, val_dataset = dataset.build_dataset()

    with strategy.scope():
        model = classifier.build_model()

    classifier.unfreeze_model(model)

    epochs = 10  # @param {type: "slider", min:8, max:50}
    hist = model.fit(train_dataset, epochs=epochs, validation_data=val_dataset, verbose=2)


if __name__ == "__main__":
    main()
