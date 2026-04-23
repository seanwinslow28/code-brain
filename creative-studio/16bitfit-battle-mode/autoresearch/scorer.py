"""Autoresearch Scorer — fitness function for evaluating generated sprites.

Combines Pixel Quantizer gate check scores (primary) with frame-to-frame
consistency metrics (secondary) into a single 0-100 float.

Weighting: 70% primary (PQ gate) / 30% secondary (temporal consistency).

Logs every evaluation to results/experiment_log.jsonl.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RESULTS_DIR = Path(__file__).parent / "results"


@dataclass
class ScorerResult:
    """Complete scoring result for one trial."""
    trial_id: int
    params: dict[str, Any]
    primary_score: float  # 0-100: Pixel Quantizer gate check
    secondary_score: float  # 0-100: Frame-to-frame consistency
    combined_score: float  # 0-100: weighted combination
    details: dict[str, Any]
    timestamp: float


class Scorer:
    """Evaluates generated sprite frames and logs results."""

    PRIMARY_WEIGHT = 0.70
    SECONDARY_WEIGHT = 0.30

    def __init__(self, log_dir: Path | None = None):
        self.log_dir = log_dir or RESULTS_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / "experiment_log.jsonl"

    def score_frames(
        self,
        frames: list[bytes],
        trial_id: int,
        params: dict[str, Any],
        dry_run: bool = False,
    ) -> ScorerResult:
        """Score a set of generated frames.

        Args:
            frames: List of PNG frame bytes.
            trial_id: Optuna trial number.
            params: Parameters used to generate these frames.
            dry_run: If True, return synthetic scores.

        Returns:
            ScorerResult with combined score.
        """
        if dry_run:
            return self._score_dry_run(trial_id, params)

        primary = self._score_pixel_quantizer(frames)
        secondary = self._score_temporal_consistency(frames)
        combined = (primary * self.PRIMARY_WEIGHT) + (secondary * self.SECONDARY_WEIGHT)

        result = ScorerResult(
            trial_id=trial_id,
            params=params,
            primary_score=primary,
            secondary_score=secondary,
            combined_score=combined,
            details={
                "frame_count": len(frames),
                "primary_weight": self.PRIMARY_WEIGHT,
                "secondary_weight": self.SECONDARY_WEIGHT,
            },
            timestamp=time.time(),
        )

        self._log_result(result)
        return result

    def _score_pixel_quantizer(self, frames: list[bytes]) -> float:
        """Run Pixel Quantizer gate check scoring.

        Evaluates: palette compliance, outline quality, BG purity, character presence.
        """
        # TODO: Wire to actual Pixel Quantizer pipeline (evaluator.py)
        # For now, return a placeholder that would be replaced with real scoring
        if not frames:
            return 0.0

        # Placeholder scoring based on frame data validity
        scores = []
        for frame_data in frames:
            if len(frame_data) > 100:  # Non-trivial image data
                scores.append(75.0)
            else:
                scores.append(50.0)

        return sum(scores) / len(scores) if scores else 0.0

    def _score_temporal_consistency(self, frames: list[bytes]) -> float:
        """Score frame-to-frame consistency via SSIM + pixel identity ratio.

        Compares adjacent frames for smoothness and identity preservation.
        """
        if len(frames) < 2:
            return 100.0  # Single frame is perfectly consistent with itself

        # TODO: Implement real SSIM + pixel identity ratio comparison
        # Requires PIL/numpy for actual image comparison
        # Placeholder: assume reasonable consistency
        return 70.0

    def _score_dry_run(self, trial_id: int, params: dict[str, Any]) -> ScorerResult:
        """Generate synthetic scores for dry run mode."""
        import random

        # Simulate score variance based on parameter choices
        base = 60.0
        # Better RIFE models score higher
        if params.get("rife_model") == "rife49.pth":
            base += 10.0
        elif params.get("rife_model") == "rife47.pth":
            base += 5.0
        # More steps generally better (with diminishing returns)
        steps = params.get("ksampler_steps", 20)
        base += min((steps - 20) * 0.5, 5.0)
        # Add noise
        primary = min(max(base + random.gauss(0, 5), 0), 100)
        secondary = min(max(65 + random.gauss(0, 8), 0), 100)
        combined = (primary * self.PRIMARY_WEIGHT) + (secondary * self.SECONDARY_WEIGHT)

        result = ScorerResult(
            trial_id=trial_id,
            params=params,
            primary_score=round(primary, 2),
            secondary_score=round(secondary, 2),
            combined_score=round(combined, 2),
            details={"dry_run": True, "base_score": base},
            timestamp=time.time(),
        )

        self._log_result(result)
        return result

    def _log_result(self, result: ScorerResult) -> None:
        """Append result to JSONL log."""
        entry = {
            "trial_id": result.trial_id,
            "params": result.params,
            "primary_score": result.primary_score,
            "secondary_score": result.secondary_score,
            "combined_score": result.combined_score,
            "details": result.details,
            "timestamp": result.timestamp,
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
