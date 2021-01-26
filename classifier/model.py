import os
import math
import tensorflow as tf
from tensorflow.keras.applications import (
    EfficientNetB0,
    EfficientNetB1,
    EfficientNetB2,
    EfficientNetB3,
    EfficientNetB4,
    EfficientNetB5,
    EfficientNetB6,
    EfficientNetB7,
)
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

base_model = {
    'b0': (EfficientNetB0, 224),
    'b1': (EfficientNetB1, 240),
    'b2': (EfficientNetB2, 260),
    'b3': (EfficientNetB3, 300),
    'b4': (EfficientNetB4, 380),
    'b5': (EfficientNetB5, 456),
    'b6': (EfficientNetB6, 528),
    'b7': (EfficientNetB7, 600),
}


class Classifier:
    def __init__(self, model_name, learning_rate, pre_trained_model_path):
        self.model_name = model_name
        self.lr = float(learning_rate)
        self.base_model, self.image_size = base_model[model_name]
        self.weight_path = os.path.join(pre_trained_model_path, self.model_name+".h5")
        self.img_augmentation = Sequential(
            [
                preprocessing.RandomRotation(factor=0.15),
                preprocessing.RandomTranslation(height_factor=0.1, width_factor=0.1),
                preprocessing.RandomFlip(),
                preprocessing.RandomContrast(factor=0.1),
            ],
            name="img_augmentation",
        )

    def build_model(self, num_classes):
        inputs = layers.Input(shape=(self.image_size, self.image_size, 3))
        # x = self.img_augmentation(inputs)
        model = self.base_model(include_top=False, input_tensor=inputs, weights=self.weight_path)

        # Freeze the pretrained weights
        model.trainable = False

        # Rebuild top
        x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
        x = layers.BatchNormalization()(x)

        top_dropout_rate = 0.2
        x = layers.Dropout(top_dropout_rate, name="top_dropout")(x)
        outputs = layers.Dense(num_classes, activation="softmax", name="pred")(x)

        # Compile
        model = tf.keras.Model(inputs, outputs, name=self.model_name)
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.lr)
        model.compile(
            optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    def unfreeze_model(self, model):
        # We unfreeze the top 20 layers while leaving BatchNorm layers frozen
        for layer in model.layers[-20:]:
            if not isinstance(layer, layers.BatchNormalization):
                layer.trainable = True

        optimizer = tf.keras.optimizers.Adam(learning_rate=self.lr)
        model.compile(
            optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
        )

    def step_decay_scheduler(self, epoch):
        drop = 0.7
        epochs_drop = 20.0
        return self.lr * math.pow(drop, math.floor((1 + epoch) / epochs_drop))
