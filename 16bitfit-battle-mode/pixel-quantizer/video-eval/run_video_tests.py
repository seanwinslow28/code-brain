#!/usr/bin/env python3
"""Phase 3 Video Model Tests — real output through the Pixel Quantizer.

Three tests:
  1. NB2 keyframes → Wan 2.2 + pixel animate LoRA → extract → score
  2. NB2 keyframes → GMFSS Fortuna interpolation → extract → score
  3. rd-animation via Replicate → evaluate output directly

Each test uses the evaluation framework from Phase 2 to score:
  palette compliance, outline quality, character consistency, background removal.

Green screen technique: chroma key (#00FF00) on keyframes BEFORE video models.
Walk cycle = 2s clips, combat = 1s clips.

Usage:
    python3 run_video_tests.py --test wan22
    python3 run_video_tests.py --test gmfss
    python3 run_video_tests.py --test replicate
    python3 run_video_tests.py --test all
    python3 run_video_tests.py --test stub  # Pipeline validation with synthetic data
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

# Add agents-sdk to path for keychain access
REPO_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))

from adapters import (
    GeneratedFrame,
    GMFSSAdapter,
    KeyframeConfig,
    ReplicateAdapter,
    StubAdapter,
    Wan22Adapter,
)
from evaluator import (
    PALETTE_RGB,
    SEAN_PALETTE,
    evaluate_model,
    extract_frames_from_video,
    score_frame,
)

EVAL_RESULTS_DIR = Path(__file__).parent / "eval-results"
KEYFRAME_DIR = EVAL_RESULTS_DIR  # NB2 keyframes from Phase 2


def load_keyframe(filename: str) -> GeneratedFrame:
    """Load a keyframe PNG from eval-results/ as a GeneratedFrame."""
    path = KEYFRAME_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Keyframe not found: {path}")

    png_data = path.read_bytes()
    return GeneratedFrame(
        data=png_data,
        width=128,
        height=128,
        format="png",
        metadata={"source": filename},
    )


def load_keyframe_rgba(filename: str) -> GeneratedFrame:
    """Load a keyframe PNG and convert to RGBA for scoring."""
    import subprocess
    import tempfile

    path = KEYFRAME_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Keyframe not found: {path}")

    # Convert PNG to raw RGBA using ffmpeg
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(path),
            "-pix_fmt", "rgba",
            "-f", "rawvideo",
            "pipe:1",
        ],
        capture_output=True,
        timeout=10,
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg conversion failed: {result.stderr.decode()[:200]}")

    # Get dimensions from ffmpeg
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )
    dims = probe.stdout.strip().split(",")
    width = int(dims[0]) if dims[0] else 128
    height = int(dims[1]) if len(dims) > 1 and dims[1] else 128

    return GeneratedFrame(
        data=result.stdout,
        width=width,
        height=height,
        format="rgba",
        metadata={"source": filename, "converted": True},
    )


async def test_stub():
    """Pipeline validation with synthetic data (no external deps)."""
    print("\n" + "=" * 60)
    print("TEST: Stub Adapter (Pipeline Validation)")
    print("=" * 60)

    adapter = StubAdapter("stub_validation")
    config = KeyframeConfig(
        character_name="Sean",
        animation_type="walk",
        start_pose="standing, right foot forward, arms at sides",
        end_pose="standing, left foot forward, arms swinging",
        palette=SEAN_PALETTE,
    )

    report = await evaluate_model(
        adapter, config,
        duration_secs=2.0,
        target_frames=8,
        output_dir=EVAL_RESULTS_DIR,
    )

    print(f"\nResult: {'PASS' if report.passed_gate_check else 'FAIL'}")
    print(f"Overall: {report.overall_score:.1%}")
    print(f"Palette: {report.avg_palette_compliance:.1%}")
    print(f"Reason: {report.gate_check_reason}")
    return report


async def test_wan22():
    """Test 1: NB2 keyframes → Wan 2.2 + pixel animate LoRA."""
    print("\n" + "=" * 60)
    print("TEST 1: Wan 2.2 + Pixel Animation LoRA")
    print("=" * 60)

    # Load NB2 keyframes from Phase 2
    try:
        start_kf = load_keyframe("keyframe-nano_banana_2-start.png")
        end_kf = load_keyframe("keyframe-nano_banana_2-end.png")
    except FileNotFoundError as e:
        print(f"SKIP: {e}")
        return None

    adapter = Wan22Adapter(lora_strength=0.85)

    print(f"Adapter: {adapter.name}")
    print(f"Target: {adapter.COMFYUI_HOST}:{adapter.COMFYUI_PORT}")
    print(f"Keyframes: start + end from NB2 Phase 2")
    print(f"Duration: 2s (walk cycle)")

    try:
        video = await adapter.interpolate_frames(
            [start_kf],  # Wan 2.2 I2V takes single input
            duration_secs=2.0,
            fps=24,
        )
        print(f"Video generated: {len(video.data)} bytes, {video.format}")

        # Extract frames and score
        frames = extract_frames_from_video(video, target_count=8)
        print(f"Extracted {len(frames)} frames")

        scores = [score_frame(f, PALETTE_RGB) for f in frames]
        avg_overall = sum(s.overall for s in scores) / len(scores)
        avg_palette = sum(s.palette_compliance for s in scores) / len(scores)

        passed = avg_overall >= 0.5 and avg_palette >= 0.6
        print(f"\nResult: {'PASS' if passed else 'FAIL'}")
        print(f"Overall: {avg_overall:.1%}")
        print(f"Palette: {avg_palette:.1%}")

        # Save results
        import json
        result = {
            "model": "Wan 2.2 + pixel animate LoRA",
            "overall": round(avg_overall, 3),
            "palette_compliance": round(avg_palette, 3),
            "passed": passed,
            "frames_scored": len(scores),
        }
        result_path = EVAL_RESULTS_DIR / "eval-wan22-walk.json"
        result_path.write_text(json.dumps(result, indent=2))
        print(f"Results saved: {result_path}")

        return result

    except Exception as e:
        print(f"FAIL: {e}")
        return {"model": "Wan 2.2", "error": str(e), "passed": False}


async def test_gmfss():
    """Test 2: NB2 keyframes → GMFSS Fortuna interpolation."""
    print("\n" + "=" * 60)
    print("TEST 2: GMFSS Fortuna Frame Interpolation")
    print("=" * 60)

    # Load NB2 keyframes
    keyframe_files = [
        "keyframe-nano_banana_2-start.png",
        "keyframe-nano_banana_2-end.png",
    ]
    # Also check for NB Pro mid keyframe as a third point
    if (KEYFRAME_DIR / "keyframe-nano_banana_pro-mid.png").exists():
        keyframe_files.insert(1, "keyframe-nano_banana_pro-mid.png")

    try:
        keyframes = [load_keyframe(f) for f in keyframe_files]
    except FileNotFoundError as e:
        print(f"SKIP: {e}")
        return None

    adapter = GMFSSAdapter(multiplier=4)

    print(f"Adapter: {adapter.name}")
    print(f"Target: {adapter.COMFYUI_HOST}:{adapter.COMFYUI_PORT}")
    print(f"Keyframes: {len(keyframes)} ({', '.join(keyframe_files)})")
    print(f"Multiplier: 4x")

    try:
        video = await adapter.interpolate_frames(
            keyframes,
            duration_secs=2.0,
            fps=12,
        )
        print(f"Video generated: {len(video.data)} bytes, {video.format}")

        frames = extract_frames_from_video(video, target_count=8)
        print(f"Extracted {len(frames)} frames")

        scores = [score_frame(f, PALETTE_RGB) for f in frames]
        avg_overall = sum(s.overall for s in scores) / len(scores)
        avg_palette = sum(s.palette_compliance for s in scores) / len(scores)

        passed = avg_overall >= 0.5 and avg_palette >= 0.6
        print(f"\nResult: {'PASS' if passed else 'FAIL'}")
        print(f"Overall: {avg_overall:.1%}")
        print(f"Palette: {avg_palette:.1%}")

        import json
        result = {
            "model": "GMFSS Fortuna",
            "overall": round(avg_overall, 3),
            "palette_compliance": round(avg_palette, 3),
            "passed": passed,
            "frames_scored": len(scores),
        }
        result_path = EVAL_RESULTS_DIR / "eval-gmfss-walk.json"
        result_path.write_text(json.dumps(result, indent=2))
        print(f"Results saved: {result_path}")

        return result

    except Exception as e:
        print(f"FAIL: {e}")
        return {"model": "GMFSS Fortuna", "error": str(e), "passed": False}


async def test_replicate():
    """Test 3: rd-animation via Replicate."""
    print("\n" + "=" * 60)
    print("TEST 3: rd-animation via Replicate")
    print("=" * 60)

    # Use NB2 start keyframe as anchor
    try:
        anchor = load_keyframe("keyframe-nano_banana_2-start.png")
    except FileNotFoundError as e:
        print(f"SKIP: {e}")
        return None

    adapter = ReplicateAdapter()

    print(f"Adapter: {adapter.name}")
    print(f"Anchor: keyframe-nano_banana_2-start.png")
    print(f"Motion: walk cycle animation")

    try:
        video = await adapter.generate_video(
            reference_image=anchor,
            motion_description=(
                "pixel art sprite walk cycle animation, "
                "fighting game character walking forward, "
                "8 frames, transparent or green background, "
                "SF2 Street Fighter style"
            ),
            duration_secs=2.0,
        )
        print(f"Output: {len(video.data)} bytes, {video.format}")
        print(f"Frames: {video.metadata.get('frame_count', 'unknown')}")

        # Score frames if available
        if video.format == "raw_frames" and "frames" in video.metadata:
            frames = extract_frames_from_video(video, target_count=8)
            scores = [score_frame(f, PALETTE_RGB) for f in frames]
            avg_overall = sum(s.overall for s in scores) / len(scores) if scores else 0
            avg_palette = sum(s.palette_compliance for s in scores) / len(scores) if scores else 0
            passed = avg_overall >= 0.5 and avg_palette >= 0.6
        else:
            # rd-animation may output images directly — save and report
            avg_overall = 0.0
            avg_palette = 0.0
            passed = False
            print("Note: rd-animation output not in raw_frames format — manual review needed")

            # Save output for manual inspection
            output_path = EVAL_RESULTS_DIR / "rd-animation-walk-output.bin"
            output_path.write_bytes(video.data)
            print(f"Output saved for manual review: {output_path}")

        print(f"\nResult: {'PASS' if passed else 'NEEDS MANUAL REVIEW'}")
        print(f"Overall: {avg_overall:.1%}")
        print(f"Palette: {avg_palette:.1%}")

        import json
        result = {
            "model": "rd-animation (Replicate)",
            "overall": round(avg_overall, 3),
            "palette_compliance": round(avg_palette, 3),
            "passed": passed,
            "frame_count": video.metadata.get("frame_count", 0),
            "note": "rd-animation may produce native pixel art — may bypass quantizer",
        }
        result_path = EVAL_RESULTS_DIR / "eval-rd_animation-walk.json"
        result_path.write_text(json.dumps(result, indent=2))
        print(f"Results saved: {result_path}")

        return result

    except Exception as e:
        print(f"FAIL: {e}")
        return {"model": "rd-animation", "error": str(e), "passed": False}


async def main():
    parser = argparse.ArgumentParser(description="Phase 3 Video Model Tests")
    parser.add_argument(
        "--test",
        choices=["wan22", "gmfss", "replicate", "stub", "all"],
        default="stub",
        help="Which test to run",
    )
    args = parser.parse_args()

    results = {}

    if args.test in ("stub", "all"):
        results["stub"] = await test_stub()

    if args.test in ("wan22", "all"):
        results["wan22"] = await test_wan22()

    if args.test in ("gmfss", "all"):
        results["gmfss"] = await test_gmfss()

    if args.test in ("replicate", "all"):
        results["replicate"] = await test_replicate()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for name, result in results.items():
        if result is None:
            print(f"  {name}: SKIPPED (missing keyframes or deps)")
        elif isinstance(result, dict) and "error" in result:
            print(f"  {name}: FAIL — {result['error'][:80]}")
        elif hasattr(result, "passed_gate_check"):
            status = "PASS" if result.passed_gate_check else "FAIL"
            print(f"  {name}: {status} (overall: {result.overall_score:.1%})")
        elif isinstance(result, dict):
            status = "PASS" if result.get("passed") else "FAIL/REVIEW"
            print(f"  {name}: {status} (overall: {result.get('overall', 0):.1%})")


if __name__ == "__main__":
    asyncio.run(main())
