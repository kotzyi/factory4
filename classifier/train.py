import os
import time
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard, TerminateOnNaN
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

    unixtime = str(int(time.time()))
    epochs = int(os.getenv("EPOCHS"))
    batch_size = int(os.getenv("BATCH_SIZE"))
    num_classes = int(os.getenv("NUM_CLASSES"))
    image_dir = os.getenv("IMAGE_DIR_PATH")
    model_name = os.getenv("MODEL_NAME")
    pre_trained_model_path = os.getenv("PRE_TRAINED_MODEL_PATH")
    model_save_path = os.path.join(os.getenv("MODEL_SAVE_PATH"), model_name + "-" + unixtime + ".hdf5")

    classifier = Classifier(model_name, num_classes, pre_trained_model_path)
    image_size = classifier.image_size

    dataset = Dataset(batch_size, image_size, num_classes, image_dir)
    train_dataset, val_dataset = dataset.build_dataset()

    with strategy.scope():
        model = classifier.build_model()

    classifier.unfreeze_model(model)

    terminate_on_nan = TerminateOnNaN()
    checkpointer = ModelCheckpoint(filepath=model_save_path, verbose=1, save_best_only=True)
    tensorboard = TensorBoard(
        log_dir='./logs',
        histogram_freq=0,
        batch_size=batch_size,
        write_graph=True,
        write_grads=False,
        write_images=False,
        embeddings_freq=0,
        embeddings_layer_names=None,
        embeddings_metadata=None,
        embeddings_data=None,
        update_freq='epoch')
    history = model.fit(
        train_dataset,
        epochs=epochs,
        validation_data=val_dataset,
        verbose=1,
        callbacks=[checkpointer, tensorboard, terminate_on_nan])


if __name__ == "__main__":
    main()
