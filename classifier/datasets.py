import tensorflow as tf


class Dataset:
    def __init__(self, batch_size, image_size, num_classes, image_dir):
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.image_size = (image_size, image_size)
        self.image_dir = image_dir

    def build_dataset(self):
        self.train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
            self.image_dir,
            validation_split=0.1,
            subset="training",
            label_mode='categorical',
            seed=1337,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )
        self.val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
            self.image_dir,
            validation_split=0.1,
            subset="validation",
            label_mode='categorical',
            seed=1337,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        return self.train_dataset, self.val_dataset
