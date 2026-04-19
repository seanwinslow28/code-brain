"""Autoresearch Search Space — defines mutable parameters for Optuna.

Each parameter is either categorical (pick from list) or numerical (range).
The search space maps to ComfyUI workflow nodes + NB2 prompt variables.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import optuna


class ParamType(str, Enum):
    CATEGORICAL = "categorical"
    INT = "int"
    FLOAT = "float"


@dataclass
class SearchParam:
    """One tunable parameter in the search space."""
    name: str
    param_type: ParamType
    choices: list[Any] | None = None  # For categorical
    low: float | None = None  # For numerical
    high: float | None = None
    step: float | None = None
    description: str = ""


# ─── NB2 Prompt Parameters ───────────────────────────────────────────

PROMPT_PARAMS = [
    SearchParam(
        name="style_descriptor",
        param_type=ParamType.CATEGORICAL,
        choices=[
            "SF2 pixel art",
            "arcade fighter pixel art",
            "16-bit fighting game sprite",
            "Capcom CPS2 pixel art",
            "retro arcade pixel sprite",
        ],
        description="Style descriptor token in the generation prompt",
    ),
    SearchParam(
        name="pose_phrasing",
        param_type=ParamType.CATEGORICAL,
        choices=[
            "detailed_anatomical",  # "left foot forward, right arm back, torso rotated"
            "action_verb",  # "striding forward with arms swinging"
            "reference_based",  # "matching the pose in the reference image"
        ],
        description="How to describe the character pose",
    ),
    SearchParam(
        name="negative_emphasis",
        param_type=ParamType.CATEGORICAL,
        choices=[
            "standard",  # base negative prompt
            "anti_3d",  # extra "no 3D, no smooth shading, no gradient"
            "anti_anime",  # extra "no anime, no chibi, no manga proportions"
            "strict_pixel",  # extra "exact pixel placement, no sub-pixel blending"
        ],
        description="Negative prompt variant to use",
    ),
]

# ─── RIFE VFI Parameters ─────────────────────────────────────────────

RIFE_PARAMS = [
    SearchParam(
        name="rife_multiplier",
        param_type=ParamType.CATEGORICAL,
        choices=[2, 4, 8],
        description="RIFE interpolation multiplier (frames between keyframes)",
    ),
    SearchParam(
        name="rife_model",
        param_type=ParamType.CATEGORICAL,
        choices=["rife46.pth", "rife47.pth", "rife49.pth"],
        description="RIFE model checkpoint variant",
    ),
]

# ─── Pixel Quantizer Parameters ──────────────────────────────────────

QUANTIZER_PARAMS = [
    SearchParam(
        name="palette_size",
        param_type=ParamType.CATEGORICAL,
        choices=[16, 24, 32],
        description="Number of colors in quantized palette",
    ),
    SearchParam(
        name="outline_thickness",
        param_type=ParamType.CATEGORICAL,
        choices=[1, 2, 3],
        description="Outline thickness in pixels",
    ),
    SearchParam(
        name="temporal_smoothing_window",
        param_type=ParamType.CATEGORICAL,
        choices=[3, 5, 7],
        description="Temporal smoothing window size (frames)",
    ),
]

# ─── KSampler / ComfyUI Parameters ──────────────────────────────────

COMFYUI_PARAMS = [
    SearchParam(
        name="ksampler_steps",
        param_type=ParamType.INT,
        low=20,
        high=40,
        step=5,
        description="KSampler denoising steps",
    ),
    SearchParam(
        name="ksampler_cfg",
        param_type=ParamType.FLOAT,
        low=5.0,
        high=12.0,
        step=0.5,
        description="KSampler CFG guidance scale",
    ),
]

# ─── Combined Space ──────────────────────────────────────────────────

ALL_PARAMS = PROMPT_PARAMS + RIFE_PARAMS + QUANTIZER_PARAMS + COMFYUI_PARAMS


def suggest_params(trial: optuna.Trial) -> dict[str, Any]:
    """Sample a full parameter set from the search space using Optuna trial.

    Returns:
        Dict mapping param name → sampled value.
    """
    params = {}
    for p in ALL_PARAMS:
        if p.param_type == ParamType.CATEGORICAL:
            params[p.name] = trial.suggest_categorical(p.name, p.choices)
        elif p.param_type == ParamType.INT:
            params[p.name] = trial.suggest_int(p.name, int(p.low), int(p.high), step=int(p.step))
        elif p.param_type == ParamType.FLOAT:
            params[p.name] = trial.suggest_float(p.name, p.low, p.high, step=p.step)
    return params


def get_param_names() -> list[str]:
    """Return all parameter names in the search space."""
    return [p.name for p in ALL_PARAMS]
