"""Simple baseline wrappers for direct 1D peak detection."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import find_peaks, find_peaks_cwt


def scipy_peaks(profile_df: pd.DataFrame, prominence: float | None = None, distance: int | None = None) -> np.ndarray:
    y = profile_df["intensity"].to_numpy(dtype=float)
    x = profile_df["2theta"].to_numpy(dtype=float)
    peaks, _ = find_peaks(y, prominence=prominence, distance=distance)
    return x[peaks]


def cwt_peaks(profile_df: pd.DataFrame, widths: np.ndarray | None = None) -> np.ndarray:
    y = profile_df["intensity"].to_numpy(dtype=float)
    x = profile_df["2theta"].to_numpy(dtype=float)
    if widths is None:
        widths = np.arange(1, 16)
    peaks = find_peaks_cwt(y, widths)
    return x[np.asarray(peaks, dtype=int)]
