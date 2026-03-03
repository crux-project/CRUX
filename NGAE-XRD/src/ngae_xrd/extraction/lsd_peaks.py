"""LSD-based peak extraction from recurrence images."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pandas as pd


def detect_vertical_segments(image: np.ndarray, threshold: int = 125) -> list[tuple[float, float, float, float]]:
    """Detect near-vertical segments using OpenCV LSD."""
    if image.dtype != np.uint8:
        image = np.clip(image * 255.0, 0, 255).astype(np.uint8)

    _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    lsd = cv2.createLineSegmentDetector(0)
    lines = lsd.detect(binary)[0]

    if lines is None:
        return []

    segments: list[tuple[float, float, float, float]] = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x1 - x2) <= 2.0:
            segments.append((x1, y1, x2, y2))
    return segments


def merge_vertical_segments(segments: list[tuple[float, float, float, float]], x_gap: int = 3) -> list[tuple[float, float, float, float]]:
    """Merge vertical segments that are close in x-space."""
    if not segments:
        return []

    items = sorted(segments, key=lambda s: (s[0] + s[2]) / 2.0)
    merged: list[tuple[float, float, float, float]] = []

    current = [items[0]]
    for seg in items[1:]:
        curr_x = np.mean([current[-1][0], current[-1][2]])
        seg_x = np.mean([seg[0], seg[2]])
        if abs(seg_x - curr_x) <= x_gap:
            current.append(seg)
        else:
            xs = [np.mean([s[0], s[2]]) for s in current]
            ys = [s[1] for s in current] + [s[3] for s in current]
            x = float(np.mean(xs))
            merged.append((x, float(min(ys)), x, float(max(ys))))
            current = [seg]

    xs = [np.mean([s[0], s[2]]) for s in current]
    ys = [s[1] for s in current] + [s[3] for s in current]
    x = float(np.mean(xs))
    merged.append((x, float(min(ys)), x, float(max(ys))))
    return merged


def pairs_to_two_theta(
    merged_segments: list[tuple[float, float, float, float]],
    pixel_step: float,
    origin_two_theta: float,
    min_len: int,
    win_gap: int,
) -> pd.DataFrame:
    """Convert merged segment x-positions to peak centers in 2theta."""
    if not merged_segments:
        return pd.DataFrame({"2theta": []})

    # Keep only long vertical segments to reduce spurious detections.
    long_x = []
    for x1, y1, x2, y2 in merged_segments:
        if abs(y2 - y1) >= min_len:
            long_x.append(float((x1 + x2) / 2.0))

    if not long_x:
        return pd.DataFrame({"2theta": []})

    long_x = sorted(long_x)
    groups: list[list[float]] = [[long_x[0]]]
    for x in long_x[1:]:
        if abs(x - groups[-1][-1]) <= win_gap:
            groups[-1].append(x)
        else:
            groups.append([x])

    centers = [float(np.mean(g)) for g in groups]
    two_theta = [origin_two_theta + pixel_step * c for c in centers]
    return pd.DataFrame({"2theta": two_theta})


def extract_peaks_from_image(
    image: np.ndarray,
    threshold: int,
    pixel_step: float,
    origin_two_theta: float,
    min_segment_len: int,
    win_gap: int,
) -> pd.DataFrame:
    segments = detect_vertical_segments(image=image, threshold=threshold)
    merged = merge_vertical_segments(segments)
    return pairs_to_two_theta(
        merged_segments=merged,
        pixel_step=pixel_step,
        origin_two_theta=origin_two_theta,
        min_len=min_segment_len,
        win_gap=win_gap,
    )


def extract_folder_to_csv(
    image_dir: str | Path,
    output_dir: str | Path,
    threshold: int,
    pixel_step: float,
    origin_two_theta: float,
    min_segment_len: int,
    win_gap: int,
) -> Path:
    """Run LSD extraction on every PNG image and save peak CSV outputs."""
    image_dir = Path(image_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for image_path in sorted(image_dir.glob("*.png")):
        image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        peaks = extract_peaks_from_image(
            image=image,
            threshold=threshold,
            pixel_step=pixel_step,
            origin_two_theta=origin_two_theta,
            min_segment_len=min_segment_len,
            win_gap=win_gap,
        )
        peaks.to_csv(output_dir / f"{image_path.stem}.csv", index=False)

    return output_dir
