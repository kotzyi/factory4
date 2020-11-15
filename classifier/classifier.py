import tensorflow as tf
from tensorflow.keras.applications import (
    EfficientNetB0,
    EfficientNetB1,
    EfficientNetB2,
    EfficientNetB3,
    EfficientNetB4
)
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

base_model = {
    'efficientnetb0': (EfficientNetB0, 224),
    'efficientnetb1': (EfficientNetB1, 240),
    'efficientnetb2': (EfficientNetB2, 260),
    'efficientnetb3': (EfficientNetB3, 300),
    'efficientnetb4': (EfficientNetB4, 380),
}


class Classifier:
    def __init__(self, model_name, num_classes):
        self.model_name = model_name
        self.base_model, self.image_size = base_model[model_name]
        self.num_classes = num_classes
        self.img_augmentation = Sequential(
            [
                preprocessing.RandomRotation(factor=0.15),
                preprocessing.RandomTranslation(height_factor=0.1, width_factor=0.1),
                preprocessing.RandomFlip(),
                preprocessing.RandomContrast(factor=0.1),
            ],
            name="img_augmentation",
        )

    def build_model(self):
        inputs = layers.Input(shape=(self.image_size, self.image_size, 3))
        x = self.img_augmentation(inputs)
        model = self.base_model(include_top=False, input_tensor=x, weights="imagenet")

        # Freeze the pretrained weights
        model.trainable = False

        # Rebuild top
        x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
        x = layers.BatchNormalization()(x)

        top_dropout_rate = 0.2
        x = layers.Dropout(top_dropout_rate, name="top_dropout")(x)
        outputs = layers.Dense(self.num_classes, activation="softmax", name="pred")(x)

        # Compile
        model = tf.keras.Model(inputs, outputs, name=self.model_name)
        optimizer = tf.keras.optimizers.Adam(learning_rate=1e-2)
        model.compile(
            optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
        )
        return model

    def unfreeze_model(self, model):
        # We unfreeze the top 20 layers while leaving BatchNorm layers frozen
        for layer in model.layers[-20:]:
            if not isinstance(layer, layers.BatchNormalization):
                layer.trainable = True

        optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
        model.compile(
            optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
        )
