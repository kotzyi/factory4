import tensorflow as tf


class Dataset:
    def __init__(self, batch_size, image_size, num_classes, train_image_dir, val_image_dir):
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.image_size = (image_size, image_size)
        self.train_image_dir = train_image_dir
        self.val_image_dir = val_image_dir

    def build_dataset(self):
        self.train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
            self.train_image_dir,
            validation_split=None,
            label_mode='categorical',
            seed=1337,
            shuffle=True,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )
        self.val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
            self.val_image_dir,
            validation_split=None,
            label_mode='categorical',
            seed=1337,
            shuffle=False,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        return self.train_dataset, self.val_dataset
