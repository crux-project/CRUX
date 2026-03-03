"""Command-line interface for running NGAE-XRD."""

from __future__ import annotations

import argparse

from ngae_xrd.config import load_config
from ngae_xrd.pipeline.run_pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run NGAE-XRD workflow on user-provided CSV data.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = load_config(args.config)
    run_pipeline(config)


if __name__ == "__main__":
    main()
