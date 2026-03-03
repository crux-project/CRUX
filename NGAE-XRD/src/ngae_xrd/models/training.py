"""Training helpers for NGAE with filename-matched clean/noisy pairing."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import tensorflow as tf

from ngae_xrd.models.autoencoder import build_ngae


def _load_and_preprocess_image(path: tf.Tensor, image_size: tuple[int, int]) -> tf.Tensor:
    img = tf.io.read_file(path)
    img = tf.image.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, image_size, method="lanczos3")
    return img


def _build_dataset(
    noisy_paths: list[str],
    clean_paths: list[str],
    image_size: tuple[int, int],
    batch_size: int,
    shuffle: bool,
) -> tf.data.Dataset:
    ds = tf.data.Dataset.from_tensor_slices((noisy_paths, clean_paths))
    if shuffle:
        ds = ds.shuffle(len(noisy_paths), reshuffle_each_iteration=True)

    ds = ds.map(
        lambda noisy, clean: (
            _load_and_preprocess_image(noisy, image_size),
            _load_and_preprocess_image(clean, image_size),
        ),
        num_parallel_calls=tf.data.AUTOTUNE,
    )
    ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds


def _paired_paths_by_name(noisy_dir: str | Path, clean_dir: str | Path) -> tuple[list[str], list[str]]:
    noisy_map = {p.stem: p for p in Path(noisy_dir).glob("*.png")}
    clean_map = {p.stem: p for p in Path(clean_dir).glob("*.png")}

    common = sorted(set(noisy_map).intersection(clean_map))
    if not common:
        raise ValueError("No filename matches between noisy and clean image folders.")

    noisy_paths = [str(noisy_map[k]) for k in common]
    clean_paths = [str(clean_map[k]) for k in common]
    return noisy_paths, clean_paths


def train_ngae(
    noisy_dir: str | Path,
    clean_dir: str | Path,
    image_size: tuple[int, int],
    batch_size: int,
    epochs: int,
    validation_split: float,
    learning_rate: float,
    checkpoint_path: str | Path,
) -> tf.keras.callbacks.History:
    """Train NGAE for noisy->clean RP reconstruction."""
    noisy_paths, clean_paths = _paired_paths_by_name(noisy_dir, clean_dir)

    n_total = len(noisy_paths)
    n_val = max(1, int(n_total * validation_split))
    n_train = n_total - n_val

    train_noisy, val_noisy = noisy_paths[:n_train], noisy_paths[n_train:]
    train_clean, val_clean = clean_paths[:n_train], clean_paths[n_train:]

    train_ds = _build_dataset(train_noisy, train_clean, image_size, batch_size, shuffle=True)
    val_ds = _build_dataset(val_noisy, val_clean, image_size, batch_size, shuffle=False)

    model = build_ngae(input_shape=(image_size[0], image_size[1], 1))
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.Huber(),
    )

    checkpoint_path = Path(checkpoint_path)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    log_dir = Path("logs") / "fit" / datetime.now().strftime("%Y%m%d-%H%M%S")

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
        tf.keras.callbacks.ModelCheckpoint(str(checkpoint_path), save_best_only=True, monitor="val_loss"),
        tf.keras.callbacks.TensorBoard(log_dir=str(log_dir), histogram_freq=1),
    ]

    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=callbacks)
    return history
