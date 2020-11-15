import tensorflow as tf


class Dataset:
    def __init__(self, batch_size, image_size, num_classes, image_dir):
        self.batch_size = batch_size
        self.num_classes = num_classes
        self.image_size = image_size
        self.image_dir = image_dir

    def input_preprocess(self, image, label):
        label = tf.one_hot(label, self.num_classes)
        return image, label

    def build_dataset(self):
        self.train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
            self.image_dir,
            validation_split=0.2,
            subset="training",
            seed=1337,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )
        self.val_dataset = tf.keras.preprocessing.image_dataset_from_directory(
            self.image_dir,
            validation_split=0.2,
            subset="validation",
            seed=1337,
            image_size=self.image_size,
            batch_size=self.batch_size,
        )

        self.train_dataset = self.train_dataset.map(lambda image, label: (tf.image.resize(image, self.image_size), label))
        self.val_dataset = self.val_dataset.map(lambda image, label: (tf.image.resize(image, self.image_size), label))

        self.train_dataset = self.train_dataset.map(
            self.input_preprocess, num_parallel_calls=tf.data.experimental.AUTOTUNE
        )
        self.train_dataset = self.train_dataset.batch(batch_size=self.batch_size, drop_remainder=True)
        self.train_dataset = self.train_dataset.prefetch(tf.data.experimental.AUTOTUNE)

        self.val_dataset = self.val_dataset.map(self.input_preprocess)
        self.val_dataset = self.val_dataset.batch(batch_size=self.batch_size, drop_remainder=True)

        return self.train_dataset, self.val_dataset
