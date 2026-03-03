"""Inference helpers for applying trained NGAE models to RP images."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


def _read_image(path: str | Path, image_size: tuple[int, int]) -> np.ndarray:
    img = Image.open(path).convert("L")
    img = img.resize(image_size)
    arr = np.asarray(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=-1)
    return arr


def _write_image(arr: np.ndarray, path: str | Path) -> None:
    out = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(out.squeeze(), mode="L").save(path)


def run_inference_folder(
    model_path: str | Path,
    input_dir: str | Path,
    output_dir: str | Path,
    image_size: tuple[int, int],
) -> Path:
    """Apply trained model to all PNG files in input_dir and save outputs."""
    model = tf.keras.models.load_model(model_path)
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for img_path in sorted(input_dir.glob("*.png")):
        arr = _read_image(img_path, image_size)
        pred = model.predict(np.expand_dims(arr, axis=0), verbose=0)[0]
        _write_image(pred, output_dir / f"{img_path.stem}_denoised.png")

    return output_dir
