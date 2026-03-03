"""Orchestration entrypoint for the full NGAE-XRD pipeline."""

from __future__ import annotations

from pathlib import Path

from ngae_xrd.config import PipelineConfig
from ngae_xrd.extraction.lsd_peaks import extract_folder_to_csv
from ngae_xrd.io.peak_io import load_input_tables
from ngae_xrd.models.inference import run_inference_folder
from ngae_xrd.models.training import train_ngae
from ngae_xrd.simulation.gaussian import batch_generate_profile_pairs
from ngae_xrd.transforms.recurrence import batch_profiles_to_recurrence_images


def run_pipeline(config: PipelineConfig) -> None:
    """Run the configured workflow without hardcoded data paths."""
    output_root = Path(config.io.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)

    tables = load_input_tables(config.io.input_dir, config.io.input_mode)

    if config.io.input_mode == "peak_list":
        clean_profiles_dir, noisy_profiles_dir = batch_generate_profile_pairs(
            peak_tables=tables,
            output_dir=output_root,
            sigma_clean=config.simulation.sigma_clean,
            sigma_noisy=config.simulation.sigma_noisy,
            two_theta_min=config.simulation.two_theta_min,
            two_theta_max=config.simulation.two_theta_max,
            step=config.simulation.step,
            wavelength_angstrom=config.simulation.wavelength_angstrom,
        )
    else:
        # If users already provide profile CSVs, this repo assumes those are noisy inputs.
        # For training, users should also provide matching clean profile images externally.
        noisy_profiles_dir = Path(config.io.input_dir)
        clean_profiles_dir = Path(config.io.input_dir)

    clean_rp_dir = batch_profiles_to_recurrence_images(
        profile_dir=clean_profiles_dir,
        output_dir=output_root / "rp_clean",
        threshold=config.recurrence.threshold,
    )
    noisy_rp_dir = batch_profiles_to_recurrence_images(
        profile_dir=noisy_profiles_dir,
        output_dir=output_root / "rp_noisy",
        threshold=config.recurrence.threshold,
    )

    if config.training.enabled:
        train_ngae(
            noisy_dir=noisy_rp_dir,
            clean_dir=clean_rp_dir,
            image_size=config.training.image_size,
            batch_size=config.training.batch_size,
            epochs=config.training.epochs,
            validation_split=config.training.validation_split,
            learning_rate=config.training.learning_rate,
            checkpoint_path=config.training.checkpoint_path,
        )

    extraction_source = noisy_rp_dir
    if config.inference.enabled:
        denoised_dir = run_inference_folder(
            model_path=config.inference.model_path,
            input_dir=noisy_rp_dir,
            output_dir=output_root / "rp_denoised",
            image_size=config.training.image_size,
        )
        extraction_source = denoised_dir

    extract_folder_to_csv(
        image_dir=extraction_source,
        output_dir=output_root / "predicted_peaks",
        threshold=config.inference.lsd_threshold,
        pixel_step=config.inference.pixel_step,
        origin_two_theta=config.inference.origin_two_theta,
        min_segment_len=config.inference.min_segment_len,
        win_gap=config.inference.win_gap,
    )
