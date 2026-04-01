#!/usr/bin/env python3
"""Run the video model evaluation framework.

Usage:
    # Stub adapter (test the pipeline end-to-end)
    python3 run_eval.py --adapter stub

    # Gemini Nano Banana Pro vs NB2 comparison
    python3 run_eval.py --adapter gemini-pro --adapter gemini-flash

    # Pika interpolation test (requires keyframes)
    python3 run_eval.py --adapter pika --keyframes /path/to/frames/

    # Full comparison
    python3 run_eval.py --adapter stub --adapter gemini-pro --adapter gemini-flash
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Add the video-eval directory to path
sys.path.insert(0, str(Path(__file__).parent))

from adapters import (
    GeminiAdapter,
    KeyframeConfig,
    KlingAdapter,
    PikaAdapter,
    ReplicateAdapter,
    StubAdapter,
    Wan22Adapter,
)
from evaluator import evaluate_model, run_comparison

# Sean character palette (from project spec)
SEAN_PALETTE = {
    "skin": "#F5D6C6",
    "hair": "#C2A769",
    "eyes": "#4682B4",
    "tank_top": "#F2F0EF",
    "pants": "#2323FF",
    "shoes": "#F5F5F5",
}

ADAPTER_MAP = {
    "stub": lambda: StubAdapter("Stub (Synthetic)"),
    "gemini-pro": lambda: GeminiAdapter("gemini-3-pro-image-preview"),
    "gemini-flash": lambda: GeminiAdapter("gemini-3.1-flash-image-preview"),
    "pika": lambda: PikaAdapter(),
    "kling": lambda: KlingAdapter(),
    "rd-animation": lambda: ReplicateAdapter(),
    "wan22": lambda: Wan22Adapter(),
}


def main():
    parser = argparse.ArgumentParser(description="Video Model Evaluation Framework")
    parser.add_argument(
        "--adapter",
        action="append",
        default=[],
        choices=list(ADAPTER_MAP.keys()),
        help="Adapter(s) to evaluate (can specify multiple)",
    )
    parser.add_argument(
        "--animation",
        default="walk",
        help="Animation type to test (default: walk)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=1.0,
        help="Video duration in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--frames",
        type=int,
        default=8,
        help="Target frame count to extract (default: 8)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for reports (default: ./eval-results/)",
    )
    args = parser.parse_args()

    if not args.adapter:
        args.adapter = ["stub"]

    output_dir = Path(args.output) if args.output else Path(__file__).parent / "eval-results"

    # Build keyframe config for walk cycle test
    config = KeyframeConfig(
        character_name="Sean",
        animation_type=args.animation,
        start_pose="Standing upright, weight on left foot, right foot slightly forward, arms at sides, facing right",
        end_pose="Mid-stride, right foot forward, left foot back, arms swinging opposite to legs, facing right",
        width=128,
        height=128,
        style="SF2 pixel art",
        background_color="#00FF00",
        palette=SEAN_PALETTE,
    )

    adapters = [ADAPTER_MAP[name]() for name in args.adapter]

    if len(adapters) == 1:
        report = asyncio.run(
            evaluate_model(
                adapters[0], config, args.duration, args.frames, output_dir
            )
        )
        print(report.to_markdown())
        print(f"\n{'='*60}")
        print(f"Gate Check: {'PASS' if report.passed_gate_check else 'FAIL'}")
        print(f"Reason: {report.gate_check_reason}")
        print(f"Report saved to: {output_dir}")
    else:
        reports = asyncio.run(
            run_comparison(
                adapters, config, args.duration, args.frames, output_dir
            )
        )
        print("\n=== COMPARISON RESULTS ===\n")
        for r in reports:
            gate = "PASS" if r.passed_gate_check else "FAIL"
            print(f"  {r.model_name}: {r.overall_score:.1%} overall [{gate}]")
        print(f"\nReports saved to: {output_dir}")


if __name__ == "__main__":
    main()
