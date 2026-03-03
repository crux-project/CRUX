"""TensorFlow NGAE model definition used for RP reconstruction."""

from __future__ import annotations

import tensorflow as tf


def build_ngae(input_shape: tuple[int, int, int] = (1000, 1000, 1)) -> tf.keras.Model:
    """Build a convolutional autoencoder matching the notebook structure."""
    inp = tf.keras.layers.Input(shape=input_shape)

    # Encoder
    x = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(inp)
    x = tf.keras.layers.MaxPooling2D((2, 2), padding="same")(x)
    x = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = tf.keras.layers.MaxPooling2D((2, 2), padding="same")(x)
    x = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    encoded = tf.keras.layers.MaxPooling2D((2, 2), padding="same")(x)

    # Decoder
    x = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(encoded)
    x = tf.keras.layers.UpSampling2D((2, 2))(x)
    x = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = tf.keras.layers.UpSampling2D((2, 2))(x)
    x = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(x)
    x = tf.keras.layers.UpSampling2D((2, 2))(x)
    out = tf.keras.layers.Conv2D(1, (3, 3), activation="sigmoid", padding="same")(x)

    model = tf.keras.Model(inp, out, name="ngae")
    return model
