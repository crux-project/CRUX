"""Simulation utilities for building 1D diffraction profiles from peak lists."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def d_to_two_theta(d_spacing: np.ndarray, wavelength_angstrom: float = 1.5406) -> np.ndarray:
    """Convert d spacing to 2theta via Bragg's law for first-order reflections."""
    theta = np.arcsin(np.clip(wavelength_angstrom / (2.0 * d_spacing), -1.0, 1.0))
    return np.degrees(2.0 * theta)


def simulate_profile_from_peaks(
    peaks: pd.DataFrame,
    sigma: float,
    two_theta_min: float,
    two_theta_max: float,
    step: float,
    wavelength_angstrom: float = 1.5406,
) -> pd.DataFrame:
    """Generate a Gaussian-summed profile from peak positions/intensities."""
    if "2theta" in peaks.columns:
        centers = peaks["2theta"].to_numpy(dtype=float)
    elif "d" in peaks.columns:
        centers = d_to_two_theta(peaks["d"].to_numpy(dtype=float), wavelength_angstrom=wavelength_angstrom)
    else:
        raise ValueError("peaks must include '2theta' or 'd'")

    amps = peaks["intensity"].to_numpy(dtype=float)
    grid = np.arange(two_theta_min, two_theta_max + (step / 2.0), step)
    signal = np.zeros_like(grid)

    for center, amp in zip(centers, amps):
        signal += amp * np.exp(-0.5 * ((grid - center) / sigma) ** 2)

    if np.max(signal) > 0:
        signal = signal / np.max(signal)

    return pd.DataFrame({"2theta": grid, "intensity": signal})


def save_profile_csv(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def batch_generate_profile_pairs(
    peak_tables: dict[str, pd.DataFrame],
    output_dir: str | Path,
    sigma_clean: float,
    sigma_noisy: float,
    two_theta_min: float,
    two_theta_max: float,
    step: float,
    wavelength_angstrom: float = 1.5406,
) -> tuple[Path, Path]:
    """Write clean/noisy simulated profiles for each input table.

    Returns paths to `(clean_dir, noisy_dir)`.
    """
    output_dir = Path(output_dir)
    clean_dir = output_dir / "profiles_clean"
    noisy_dir = output_dir / "profiles_noisy"
    clean_dir.mkdir(parents=True, exist_ok=True)
    noisy_dir.mkdir(parents=True, exist_ok=True)

    for sample_id, peaks in peak_tables.items():
        clean_df = simulate_profile_from_peaks(
            peaks=peaks,
            sigma=sigma_clean,
            two_theta_min=two_theta_min,
            two_theta_max=two_theta_max,
            step=step,
            wavelength_angstrom=wavelength_angstrom,
        )
        noisy_df = simulate_profile_from_peaks(
            peaks=peaks,
            sigma=sigma_noisy,
            two_theta_min=two_theta_min,
            two_theta_max=two_theta_max,
            step=step,
            wavelength_angstrom=wavelength_angstrom,
        )

        save_profile_csv(clean_df, clean_dir / f"{sample_id}.csv")
        save_profile_csv(noisy_df, noisy_dir / f"{sample_id}.csv")

    return clean_dir, noisy_dir
