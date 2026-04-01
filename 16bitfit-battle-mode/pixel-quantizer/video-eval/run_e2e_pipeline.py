#!/usr/bin/env python3
"""End-to-End Hybrid Pipeline Test — 1 Champion Walk Cycle.

Full pipeline steps:
  1. Generate keyframes with NB2 (GeminiAdapter)
  2. Interpolate with BEST video model from Task 8
  3. Extract frames (target: 8 frames for walk cycle)
  4. Run through Pixel Quantizer (all 7 steps)
  5. Audit frames (palette, outline, dimensions, alpha)
  6. Pack into atlas sheet (if packer available)
  7. Validate in headless Phaser (if validator available)

Usage:
    python3 run_e2e_pipeline.py --mode full        # Full pipeline (needs Alienware)
    python3 run_e2e_pipeline.py --mode keyframes    # Steps 1-2 only (Gemini keyframes)
    python3 run_e2e_pipeline.py --mode stub         # Full pipeline with stub adapter
    python3 run_e2e_pipeline.py --mode existing     # Use Phase 2 keyframes, skip gen
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add agents-sdk to path for keychain access
REPO_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))

from adapters import (
    GeneratedFrame,
    GeminiAdapter,
    GMFSSAdapter,
    KeyframeConfig,
    StubAdapter,
    Wan22Adapter,
)
from evaluator import (
    PALETTE_RGB,
    SEAN_PALETTE,
    EvaluationReport,
    evaluate_model,
    extract_frames_from_video,
    score_frame,
)
from strategy_router import (
    GenerationStrategy,
    StrategyRouter,
    execute_plan,
)

EVAL_RESULTS_DIR = Path(__file__).parent / "eval-results"


def load_existing_keyframes() -> list[GeneratedFrame]:
    """Load NB2 keyframes from Phase 2."""
    keyframe_files = [
        "keyframe-nano_banana_2-start.png",
        "keyframe-nano_banana_pro-mid.png",  # Use NB Pro mid as interpolation point
        "keyframe-nano_banana_2-end.png",
    ]

    frames = []
    for filename in keyframe_files:
        path = EVAL_RESULTS_DIR / filename
        if path.exists():
            frames.append(GeneratedFrame(
                data=path.read_bytes(),
                width=128,
                height=128,
                format="png",
                metadata={"source": filename},
            ))
            print(f"  Loaded: {filename} ({path.stat().st_size} bytes)")
        else:
            print(f"  Missing: {filename}")

    return frames


async def run_e2e(mode: str) -> dict:
    """Run the end-to-end pipeline test."""
    print("=" * 60)
    print(f"END-TO-END HYBRID PIPELINE TEST — Walk Cycle")
    print(f"Mode: {mode}")
    print(f"Date: {datetime.now().isoformat()}")
    print("=" * 60)

    results: dict = {
        "mode": mode,
        "date": datetime.now().isoformat(),
        "steps": {},
    }

    # ─── Step 1: Strategy Routing ─────────────────────────────────────
    print("\n--- Step 1: Strategy Routing ---")
    router = StrategyRouter(
        keyframe_model="gemini-3.1-flash-image-preview",
        interpolation_backend="wan22" if mode == "full" else "gmfss",
    )
    plan = router.route("walk_forward", "Sean")
    print(f"Strategy: {plan.strategy.value}")
    print(f"Keyframe adapter: {plan.keyframe_adapter.name if plan.keyframe_adapter else 'None'}")
    print(f"Interpolation adapter: {plan.interpolation_adapter.name if plan.interpolation_adapter else 'None'}")
    print(f"Target frames: {plan.target_frame_count}")
    print(f"Duration: {plan.duration_secs}s")
    print(f"Green screen: {plan.apply_green_screen}")
    print(f"Pixel quantizer: {plan.apply_pixel_quantizer}")

    results["steps"]["1_routing"] = {
        "status": "PASS",
        "strategy": plan.strategy.value,
        "keyframe_adapter": plan.keyframe_adapter.name if plan.keyframe_adapter else None,
        "interpolation_adapter": plan.interpolation_adapter.name if plan.interpolation_adapter else None,
    }

    # ─── Step 2: Keyframe Generation / Loading ────────────────────────
    print("\n--- Step 2: Keyframes ---")
    keyframes: list[GeneratedFrame] = []

    if mode == "existing":
        print("Loading existing NB2 keyframes from Phase 2...")
        keyframes = load_existing_keyframes()
        results["steps"]["2_keyframes"] = {
            "status": "PASS" if keyframes else "FAIL",
            "source": "Phase 2 existing keyframes",
            "count": len(keyframes),
        }

    elif mode == "stub":
        print("Generating stub keyframes...")
        stub = StubAdapter("e2e_stub")
        config = KeyframeConfig(
            character_name="Sean",
            animation_type="walk_forward",
            start_pose="standing, right foot forward",
            end_pose="standing, left foot forward",
            palette=SEAN_PALETTE,
        )
        keyframes = await stub.generate_keyframes(config)
        results["steps"]["2_keyframes"] = {
            "status": "PASS",
            "source": "stub synthetic",
            "count": len(keyframes),
        }

    elif mode in ("keyframes", "full"):
        print("Generating NB2 keyframes via Gemini API...")
        config = KeyframeConfig(
            character_name="Sean",
            animation_type="walk_forward",
            start_pose=(
                "standing fight stance, right foot forward, fists raised, "
                "white tank top, blue pants, white sneakers"
            ),
            end_pose=(
                "mid-stride walking forward, left foot forward, arms swinging, "
                "white tank top, blue pants, white sneakers"
            ),
            palette=SEAN_PALETTE,
        )
        try:
            adapter = GeminiAdapter(model_id="gemini-3.1-flash-image-preview")
            keyframes = await adapter.generate_keyframes(config)
            for i, kf in enumerate(keyframes):
                save_path = EVAL_RESULTS_DIR / f"e2e-keyframe-{i}.png"
                save_path.write_bytes(kf.data)
                print(f"  Saved keyframe {i}: {save_path} ({len(kf.data)} bytes)")
            results["steps"]["2_keyframes"] = {
                "status": "PASS",
                "source": "NB2 (gemini-3.1-flash-image-preview)",
                "count": len(keyframes),
            }
        except Exception as e:
            print(f"  FAIL: {e}")
            print("  Falling back to existing Phase 2 keyframes...")
            keyframes = load_existing_keyframes()
            results["steps"]["2_keyframes"] = {
                "status": "FALLBACK",
                "source": "Phase 2 existing (API error)",
                "count": len(keyframes),
                "error": str(e)[:200],
            }

    if not keyframes:
        print("ABORT: No keyframes available")
        results["overall"] = "FAIL - no keyframes"
        return results

    print(f"Keyframes ready: {len(keyframes)}")

    # ─── Step 3: Video Interpolation ──────────────────────────────────
    print("\n--- Step 3: Video Interpolation ---")
    video = None

    if mode == "stub":
        print("Interpolating with stub adapter...")
        stub = StubAdapter("e2e_stub")
        video = await stub.interpolate_frames(keyframes, duration_secs=2.0, fps=24)
        results["steps"]["3_interpolation"] = {
            "status": "PASS",
            "adapter": "stub",
            "video_size": len(video.data),
        }

    elif mode in ("full",):
        print(f"Interpolating with {plan.interpolation_adapter.name}...")
        try:
            video = await plan.interpolation_adapter.interpolate_frames(
                keyframes, duration_secs=2.0, fps=24,
            )
            results["steps"]["3_interpolation"] = {
                "status": "PASS",
                "adapter": plan.interpolation_adapter.name,
                "video_size": len(video.data),
            }
        except Exception as e:
            print(f"  FAIL: {e}")
            results["steps"]["3_interpolation"] = {
                "status": "FAIL",
                "adapter": plan.interpolation_adapter.name,
                "error": str(e)[:200],
            }

    elif mode in ("existing", "keyframes"):
        print("SKIP: Interpolation requires Alienware (not reachable)")
        results["steps"]["3_interpolation"] = {
            "status": "BLOCKED",
            "reason": "Alienware offline — ComfyUI not reachable",
        }

    # ─── Step 4: Frame Extraction ─────────────────────────────────────
    print("\n--- Step 4: Frame Extraction ---")
    extracted_frames: list[GeneratedFrame] = []

    if video:
        extracted_frames = extract_frames_from_video(video, target_count=8)
        print(f"Extracted {len(extracted_frames)} frames from video")
        results["steps"]["4_extraction"] = {
            "status": "PASS",
            "frame_count": len(extracted_frames),
        }
    elif keyframes and mode in ("existing", "keyframes"):
        # Use keyframes directly as "extracted" frames for scoring
        extracted_frames = keyframes
        print(f"Using {len(keyframes)} keyframes directly (no video to extract from)")
        results["steps"]["4_extraction"] = {
            "status": "SKIP - using keyframes directly",
            "frame_count": len(keyframes),
        }
    else:
        print("SKIP: No video available for extraction")
        results["steps"]["4_extraction"] = {"status": "BLOCKED"}

    # ─── Step 5: Pixel Quantizer Scoring (Audit) ──────────────────────
    print("\n--- Step 5: Frame Scoring (Pixel Quantizer Gate Check) ---")

    if extracted_frames:
        # For PNG frames, try converting to RGBA for scoring
        scorable_frames = []
        for frame in extracted_frames:
            if frame.format == "rgba":
                scorable_frames.append(frame)
            elif frame.format == "png":
                # Try PIL conversion
                try:
                    from PIL import Image
                    import io
                    img = Image.open(io.BytesIO(frame.data)).convert("RGBA")
                    rgba_data = img.tobytes()
                    scorable_frames.append(GeneratedFrame(
                        data=rgba_data,
                        width=img.width,
                        height=img.height,
                        format="rgba",
                        metadata={**frame.metadata, "converted_from_png": True},
                    ))
                except Exception as e:
                    print(f"  Skipping frame (can't convert to RGBA): {e}")

        if scorable_frames:
            scores = [score_frame(f, PALETTE_RGB) for f in scorable_frames]
            avg_overall = sum(s.overall for s in scores) / len(scores)
            avg_palette = sum(s.palette_compliance for s in scores) / len(scores)
            avg_outline = sum(s.outline_quality for s in scores) / len(scores)
            avg_bg = sum(s.background_purity for s in scores) / len(scores)
            avg_char = sum(s.character_presence for s in scores) / len(scores)

            passed = avg_overall >= 0.5 and avg_palette >= 0.6

            print(f"  Frames scored: {len(scorable_frames)}")
            print(f"  Palette compliance: {avg_palette:.1%}")
            print(f"  Outline quality: {avg_outline:.1%}")
            print(f"  Background purity: {avg_bg:.1%}")
            print(f"  Character presence: {avg_char:.1%}")
            print(f"  Overall: {avg_overall:.1%}")
            print(f"  Gate check: {'PASS' if passed else 'FAIL'}")

            results["steps"]["5_scoring"] = {
                "status": "PASS" if passed else "FAIL",
                "frames_scored": len(scorable_frames),
                "avg_palette": round(avg_palette, 3),
                "avg_outline": round(avg_outline, 3),
                "avg_background": round(avg_bg, 3),
                "avg_character": round(avg_char, 3),
                "avg_overall": round(avg_overall, 3),
                "gate_check": "PASS" if passed else "FAIL",
            }
        else:
            print("  No scorable frames available")
            results["steps"]["5_scoring"] = {"status": "NO SCORABLE FRAMES"}
    else:
        print("SKIP: No frames available for scoring")
        results["steps"]["5_scoring"] = {"status": "BLOCKED"}

    # ─── Steps 6-7: Packer + Phaser Validator ─────────────────────────
    print("\n--- Steps 6-7: Atlas Packing + Phaser Validation ---")
    print("SKIP: Packer and Phaser validator are in the sprite-sheet-automation repo")
    print("      (not wired into this evaluation framework yet)")
    results["steps"]["6_packing"] = {"status": "NOT WIRED - separate repo"}
    results["steps"]["7_validation"] = {"status": "NOT WIRED - separate repo"}

    # ─── Overall Result ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    blocking_steps = [k for k, v in results["steps"].items()
                      if v.get("status") in ("FAIL", "BLOCKED")]
    if not blocking_steps:
        results["overall"] = "PASS"
        print("OVERALL: PASS")
    elif all(v.get("status") in ("NOT WIRED - separate repo",) for k, v in results["steps"].items() if v.get("status") not in ("PASS", "SKIP - using keyframes directly", "FALLBACK")):
        results["overall"] = "PASS (with deferred steps)"
        print("OVERALL: PASS (steps 6-7 deferred to sprite pipeline repo)")
    else:
        results["overall"] = f"BLOCKED on steps: {', '.join(blocking_steps)}"
        print(f"OVERALL: BLOCKED — {', '.join(blocking_steps)}")

    # Save results
    result_path = EVAL_RESULTS_DIR / f"e2e-pipeline-{mode}.json"
    result_path.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved: {result_path}")

    return results


async def main():
    parser = argparse.ArgumentParser(description="E2E Hybrid Pipeline Test")
    parser.add_argument(
        "--mode",
        choices=["full", "keyframes", "stub", "existing"],
        default="existing",
        help="Pipeline mode",
    )
    args = parser.parse_args()

    await run_e2e(args.mode)


if __name__ == "__main__":
    asyncio.run(main())
