"""Evaluation metrics for peak-list comparisons."""

from __future__ import annotations

import numpy as np


def matched_fraction(gt: np.ndarray, pred: np.ndarray, tolerance_deg: float = 0.02) -> float:
    """Greedy one-to-one matching fraction (micro style over peaks)."""
    gt = np.sort(np.asarray(gt, dtype=float))
    pred = np.sort(np.asarray(pred, dtype=float))

    used = np.zeros(len(pred), dtype=bool)
    matches = 0

    for g in gt:
        diffs = np.abs(pred - g)
        candidates = np.where((diffs <= tolerance_deg) & (~used))[0]
        if len(candidates) == 0:
            continue
        best = candidates[np.argmin(diffs[candidates])]
        used[best] = True
        matches += 1

    if len(gt) == 0:
        return 0.0
    return matches / len(gt)


def missed_peaks_count(gt: np.ndarray, pred: np.ndarray, tolerance_deg: float = 0.02) -> int:
    frac = matched_fraction(gt, pred, tolerance_deg=tolerance_deg)
    return int(round((1.0 - frac) * len(gt)))
