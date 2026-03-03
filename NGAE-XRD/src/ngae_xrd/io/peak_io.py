"""I/O helpers for profile and peak-list CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def iter_csv_files(directory: str | Path) -> list[Path]:
    return sorted(Path(directory).glob("*.csv"))


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    renamed = {
        c: c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns
    }
    return df.rename(columns=renamed)


def load_profile_csv(path: str | Path) -> pd.DataFrame:
    """Load a 1D profile CSV with 2theta and intensity columns."""
    df = _canonicalize_columns(pd.read_csv(path))
    two_theta_col = "2theta" if "2theta" in df.columns else "two_theta"
    if two_theta_col not in df.columns or "intensity" not in df.columns:
        raise ValueError(f"Profile CSV must include 2theta/two_theta and intensity: {path}")

    out = df[[two_theta_col, "intensity"]].copy()
    out.columns = ["2theta", "intensity"]
    out = out.sort_values("2theta").reset_index(drop=True)
    return out


def load_peak_list_csv(path: str | Path) -> pd.DataFrame:
    """Load a peak-list CSV with either 2theta or d spacing and intensity."""
    df = _canonicalize_columns(pd.read_csv(path))
    has_two_theta = "2theta" in df.columns or "two_theta" in df.columns
    has_d = "d" in df.columns or "d_spacing" in df.columns

    if not has_two_theta and not has_d:
        raise ValueError(f"Peak-list CSV must include 2theta/two_theta or d/d_spacing: {path}")
    if "intensity" not in df.columns and "i" not in df.columns:
        raise ValueError(f"Peak-list CSV must include intensity or i: {path}")

    intensity_col = "intensity" if "intensity" in df.columns else "i"
    out = pd.DataFrame()

    if "2theta" in df.columns:
        out["2theta"] = df["2theta"]
    elif "two_theta" in df.columns:
        out["2theta"] = df["two_theta"]

    if "d" in df.columns:
        out["d"] = df["d"]
    elif "d_spacing" in df.columns:
        out["d"] = df["d_spacing"]

    out["intensity"] = df[intensity_col]
    return out.reset_index(drop=True)


def load_input_tables(input_dir: str | Path, mode: str) -> dict[str, pd.DataFrame]:
    """Load all CSV files from input_dir keyed by filename stem."""
    files = iter_csv_files(input_dir)
    tables: dict[str, pd.DataFrame] = {}

    for file_path in files:
        key = file_path.stem
        if mode == "profile":
            tables[key] = load_profile_csv(file_path)
        elif mode == "peak_list":
            tables[key] = load_peak_list_csv(file_path)
        else:
            raise ValueError("mode must be 'profile' or 'peak_list'")

    return tables
