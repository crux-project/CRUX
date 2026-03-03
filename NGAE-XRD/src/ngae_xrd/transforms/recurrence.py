"""Recurrence-plot transforms for 1D intensity profiles."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyts.image import RecurrencePlot

from ngae_xrd.io.peak_io import iter_csv_files, load_profile_csv


def profile_to_recurrence(profile_df: pd.DataFrame, threshold: int = 5) -> np.ndarray:
    """Convert a profile dataframe to a binary recurrence matrix."""
    x = profile_df["intensity"].to_numpy(dtype=float)
    rp = RecurrencePlot(threshold=threshold)
    mat = rp.fit_transform(x.reshape(1, -1))[0]
    return mat


def save_recurrence_image(matrix: np.ndarray, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.imsave(output_path, matrix, cmap="gray")


def batch_profiles_to_recurrence_images(
    profile_dir: str | Path,
    output_dir: str | Path,
    threshold: int = 5,
) -> Path:
    """Convert every profile CSV in profile_dir into RP PNG images."""
    profile_dir = Path(profile_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for csv_path in iter_csv_files(profile_dir):
        profile = load_profile_csv(csv_path)
        rp = profile_to_recurrence(profile, threshold=threshold)
        save_recurrence_image(rp, output_dir / f"{csv_path.stem}.png")

    return output_dir
