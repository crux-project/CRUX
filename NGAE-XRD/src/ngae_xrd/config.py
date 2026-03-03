from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class IOConfig:
    input_mode: str
    input_dir: str
    output_dir: str


@dataclass
class SimulationConfig:
    wavelength_angstrom: float
    two_theta_min: float
    two_theta_max: float
    step: float
    sigma_clean: float
    sigma_noisy: float


@dataclass
class RecurrenceConfig:
    threshold: int


@dataclass
class TrainingConfig:
    enabled: bool
    image_size: tuple[int, int]
    batch_size: int
    epochs: int
    validation_split: float
    learning_rate: float
    checkpoint_path: str


@dataclass
class InferenceConfig:
    enabled: bool
    model_path: str
    lsd_threshold: int
    pixel_step: float
    origin_two_theta: float
    min_segment_len: int
    win_gap: int


@dataclass
class EvaluationConfig:
    tolerance_deg: float


@dataclass
class PipelineConfig:
    io: IOConfig
    simulation: SimulationConfig
    recurrence: RecurrenceConfig
    training: TrainingConfig
    inference: InferenceConfig
    evaluation: EvaluationConfig


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(config_path: str | Path) -> PipelineConfig:
    """Load YAML config into strongly typed dataclasses."""
    path = Path(config_path)
    raw = _read_yaml(path)

    return PipelineConfig(
        io=IOConfig(**raw["io"]),
        simulation=SimulationConfig(**raw["simulation"]),
        recurrence=RecurrenceConfig(**raw["recurrence"]),
        training=TrainingConfig(
            enabled=raw["training"]["enabled"],
            image_size=tuple(raw["training"]["image_size"]),
            batch_size=raw["training"]["batch_size"],
            epochs=raw["training"]["epochs"],
            validation_split=raw["training"]["validation_split"],
            learning_rate=raw["training"]["learning_rate"],
            checkpoint_path=raw["training"]["checkpoint_path"],
        ),
        inference=InferenceConfig(**raw["inference"]),
        evaluation=EvaluationConfig(**raw["evaluation"]),
    )
