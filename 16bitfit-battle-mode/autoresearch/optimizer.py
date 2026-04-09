"""Autoresearch Optimizer — Optuna TPE search wrapper.

Uses Tree-structured Parzen Estimator (TPE) to intelligently explore the
parameter space. TPE learns which regions produce good scores and samples
more from those regions, converging faster than random search.

Supports resumable runs via SQLite storage backend.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable

import optuna

from autoresearch.search_space import suggest_params
from autoresearch.scorer import Scorer, ScorerResult


RESULTS_DIR = Path(__file__).parent / "results"


class AutoresearchOptimizer:
    """Optuna TPE optimizer for the sprite generation pipeline."""

    def __init__(
        self,
        animation_type: str,
        character_name: str,
        max_trials: int = 50,
        timeout_hours: float = 4.0,
        dry_run: bool = False,
        results_dir: Path | None = None,
    ):
        self.animation_type = animation_type
        self.character_name = character_name
        self.max_trials = max_trials
        self.timeout_secs = timeout_hours * 3600
        self.dry_run = dry_run
        self.results_dir = results_dir or RESULTS_DIR
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.scorer = Scorer(log_dir=self.results_dir)

        # SQLite storage for resumable studies
        storage_path = self.results_dir / f"study_{animation_type}_{character_name}.db"
        self.storage = f"sqlite:///{storage_path}"

        study_name = f"{character_name}_{animation_type}"
        self.study = optuna.create_study(
            study_name=study_name,
            storage=self.storage,
            direction="maximize",
            sampler=optuna.samplers.TPESampler(seed=42),
            load_if_exists=True,  # Resume if study exists
        )

    def optimize(
        self,
        generate_fn: Callable[[dict[str, Any]], list[bytes]] | None = None,
    ) -> dict[str, Any]:
        """Run the optimization loop.

        Args:
            generate_fn: Callable that takes params dict, returns list of frame bytes.
                         If None (dry run), uses mock generation.

        Returns:
            Best parameters found.
        """
        def objective(trial: optuna.Trial) -> float:
            params = suggest_params(trial)

            if self.dry_run or generate_fn is None:
                frames = [b"mock_frame_data_" + str(i).encode() * 100 for i in range(8)]
            else:
                frames = generate_fn(params)

            result = self.scorer.score_frames(
                frames=frames,
                trial_id=trial.number,
                params=params,
                dry_run=self.dry_run,
            )

            return result.combined_score

        # Suppress Optuna's verbose logging for cleaner output
        optuna.logging.set_verbosity(optuna.logging.WARNING)

        self.study.optimize(
            objective,
            n_trials=self.max_trials,
            timeout=self.timeout_secs,
        )

        # Save best params
        best = self.study.best_params
        best_path = self.results_dir / "best_params.json"
        best_data = {
            "animation_type": self.animation_type,
            "character_name": self.character_name,
            "best_params": best,
            "best_score": self.study.best_value,
            "total_trials": len(self.study.trials),
            "timestamp": time.time(),
        }
        best_path.write_text(json.dumps(best_data, indent=2) + "\n")

        return best

    def get_results_summary(self) -> dict[str, Any]:
        """Return a summary of the optimization results."""
        trials = self.study.trials
        scores = [t.value for t in trials if t.value is not None]

        return {
            "study_name": self.study.study_name,
            "total_trials": len(trials),
            "best_score": self.study.best_value if scores else None,
            "best_params": self.study.best_params if scores else None,
            "mean_score": sum(scores) / len(scores) if scores else 0,
            "min_score": min(scores) if scores else 0,
            "max_score": max(scores) if scores else 0,
        }
