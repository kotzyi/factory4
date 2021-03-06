import os
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, TerminateOnNaN, LearningRateScheduler, ModelCheckpoint
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

    epochs = int(os.getenv("EPOCHS"))
    learning_rate = os.getenv("LEARNING_RATE")
    batch_size = int(os.getenv("BATCH_SIZE"))
    num_classes = int(os.getenv("NUM_CLASSES"))
    train_image_dir = os.getenv("TRAIN_IMAGE_DIR_PATH")
    val_image_dir = os.getenv("VAL_IMAGE_DIR_PATH")
    model_name = os.getenv("MODEL_NAME")
    pre_trained_model_path = os.getenv("PRE_TRAINED_MODEL_PATH")
    model_save_path = os.path.join(os.getenv("MODEL_SAVE_PATH"), "saved_model")

    classifier = Classifier(model_name, learning_rate, pre_trained_model_path)
    image_size = classifier.image_size

    dataset = Dataset(batch_size, image_size, num_classes, train_image_dir, val_image_dir)
    train_dataset, val_dataset = dataset.build_dataset()

    with strategy.scope():
        model = classifier.build_model(num_classes)

    classifier.unfreeze_model(model)

    # Adding Callbacks to model
    terminate_on_nan = TerminateOnNaN()
    learning_rate_scheduler = LearningRateScheduler(classifier.step_decay_scheduler, verbose=1)
    tensorboard = TensorBoard(
        log_dir='./logs',
        histogram_freq=0,
        batch_size=batch_size,
        write_graph=False,
        write_images=True,
        embeddings_freq=0,
        embeddings_layer_names=None,
        embeddings_metadata=None,
        embeddings_data=None,
        update_freq='epoch')

    model_checkpoint_callback = ModelCheckpoint(
        filepath=model_save_path,
        save_weights_only=False,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True)

    callbacks = [tensorboard, terminate_on_nan, learning_rate_scheduler, model_checkpoint_callback]

    model.fit(
        train_dataset,
        epochs=epochs,
        validation_data=val_dataset,
        verbose=1,
        callbacks=callbacks)


if __name__ == "__main__":
    main()
