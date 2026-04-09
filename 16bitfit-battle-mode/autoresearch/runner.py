"""Autoresearch CLI Runner — entry point for parameter search.

Usage:
    # Dry run (no API calls, mock adapters)
    python3 runner.py --animation-type walk_forward --character sean --max-trials 3 --dry-run

    # Real run (connects to Gemini + RIFE + Pixel Quantizer)
    python3 runner.py --animation-type walk_forward --character sean --max-trials 50

    # Resume a previous study
    python3 runner.py --animation-type walk_forward --character sean --max-trials 100
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add paths for imports
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "pixel-quantizer" / "video-eval"))
sys.path.insert(0, str(REPO_ROOT.parent / "agents-sdk"))


def main():
    parser = argparse.ArgumentParser(description="Autoresearch parameter optimization")
    parser.add_argument("--animation-type", required=True, help="Animation type to optimize")
    parser.add_argument("--character", required=True, help="Character name")
    parser.add_argument("--max-trials", type=int, default=50, help="Max Optuna trials")
    parser.add_argument("--timeout-hours", type=float, default=4.0, help="Max runtime in hours")
    parser.add_argument("--dry-run", action="store_true", help="Use mock adapters")
    args = parser.parse_args()

    # Import here to avoid import issues when checking CLI help
    from autoresearch.optimizer import AutoresearchOptimizer

    print(f"{'=' * 60}")
    print(f"AUTORESEARCH — {args.character} / {args.animation_type}")
    print(f"Max trials: {args.max_trials} | Timeout: {args.timeout_hours}h | Dry run: {args.dry_run}")
    print(f"{'=' * 60}\n")

    optimizer = AutoresearchOptimizer(
        animation_type=args.animation_type,
        character_name=args.character,
        max_trials=args.max_trials,
        timeout_hours=args.timeout_hours,
        dry_run=args.dry_run,
    )

    best_params = optimizer.optimize()
    summary = optimizer.get_results_summary()

    print(f"\n{'─' * 60}")
    print("OPTIMIZATION COMPLETE")
    print(f"  Trials: {summary['total_trials']}")
    print(f"  Best score: {summary['best_score']:.2f}")
    print(f"  Mean score: {summary['mean_score']:.2f}")
    print(f"  Score range: {summary['min_score']:.2f} — {summary['max_score']:.2f}")
    print(f"\nBest parameters:")
    for k, v in best_params.items():
        print(f"  {k}: {v}")
    print(f"\nResults saved to: {optimizer.results_dir}/")
    print(f"  best_params.json — optimal parameter set")
    print(f"  experiment_log.jsonl — full trial log")
    print(f"  study_*.db — Optuna SQLite (resumable)")


if __name__ == "__main__":
    main()
