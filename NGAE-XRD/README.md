# NGAE-XRD

Reusable, data-path-agnostic pipeline for the Chapter 6 LAPeX/CRUX XRD workflow.

This repository refactors the implemented workflow into modular Python functions:
- CSV ingest for peak lists and intensity profiles
- Gaussian profile simulation (paired widths)
- Recurrence-plot conversion
- NGAE (autoencoder) training/inference
- LSD-based vertical-segment peak extraction
- Basic evaluation utilities for matched-fraction analysis

## Quick start
1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
   - `pip install -e .`
3. Copy `configs/pipeline.example.yaml` to `configs/pipeline.yaml` and edit paths.
4. Run:
   - `python scripts/run_pipeline.py --config configs/pipeline.yaml`

## Developer workflow
- Install developer tools: `make install-dev`
- Lint: `make lint`
- Format: `make format`
- Test: `make test`
- Run all checks: `make check`

## CI
- GitHub Actions workflow: `.github/workflows/ci.yml`
- Triggers on push, pull request, and manual dispatch.
- Runs `make install-dev`, `make lint`, and `make test` on Python 3.10.

## Input expectations
- Peak-list CSV mode: columns include either `2theta` or `d`, plus `intensity`.
- Profile CSV mode: columns include `2theta` and `intensity`.

## Notes
- No direct absolute data paths are used.
- The package is designed so users can run on their own CSV data.
- Data from ICDD PDF5+ is not redistributed here.
