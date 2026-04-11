"""Batch Generation Orchestrator — generates ALL animation frames for a character.

Takes a character manifest JSON and drives each animation through the correct
pipeline (IMAGE_ONLY or HYBRID) using the strategy router, prompt library,
and adapter layer.

IMAGE_ONLY: Generates all frames as a single sprite sheet via one Gemini call,
then splits into individual frame PNGs (proven in Phase 5B to maintain character
consistency across frames).

HYBRID: Generates keyframes via sprite sheet, interpolates with RIFE on Alienware,
then extracts individual frames from the resulting MP4.

Usage:
    # Dry run (no API calls)
    python3 batch/batch_orchestrator.py manifests/champion_sean.json --dry-run

    # Live run
    python3 batch/batch_orchestrator.py manifests/champion_sean.json

    # Resume (skips completed animations)
    python3 batch/batch_orchestrator.py manifests/champion_sean.json --resume

    # Force re-run (ignores COMPLETE status)
    python3 batch/batch_orchestrator.py manifests/champion_sean.json --force
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path

# Add parent dirs to path for imports
SCRIPT_DIR = Path(__file__).parent
PIXEL_QUANTIZER_DIR = SCRIPT_DIR.parent
VIDEO_EVAL_DIR = PIXEL_QUANTIZER_DIR / "video-eval"
REPO_ROOT = PIXEL_QUANTIZER_DIR.parent.parent

sys.path.insert(0, str(PIXEL_QUANTIZER_DIR))
sys.path.insert(0, str(VIDEO_EVAL_DIR))
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))

from generate_sheet_split import (
    build_sheet_prompt,
    call_gemini,
    detect_grid,
    get_grid_layout,
    load_anchors,
    split_sheet,
)


class AnimStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class AnimationResult:
    animation_type: str
    status: str = AnimStatus.PENDING
    strategy: str = ""
    frame_count: int = 0
    frames_generated: int = 0
    score: float = 0.0
    error: str = ""
    duration_ms: float = 0.0


@dataclass
class BatchStatus:
    character_name: str
    character_type: str
    tile_size: int
    total_animations: int = 0
    completed: int = 0
    failed: int = 0
    animations: dict[str, AnimationResult] = field(default_factory=dict)


class BatchOrchestrator:
    """Drives batch generation for a single character's full animation set."""

    def __init__(
        self,
        manifest_path: Path,
        output_dir: Path | None = None,
        dry_run: bool = False,
        resume: bool = False,
        force: bool = False,
    ):
        self.manifest = json.loads(manifest_path.read_text())
        self.char_name = self.manifest["name"]
        self.tile_size = self.manifest["tile_size"]
        self.char_type = self.manifest["type"]
        self.description = self.manifest["description"]
        self.anchor_images = self.manifest["anchor_images"]
        self.animations = self.manifest["animations"]
        self.pose_overrides = self.manifest.get("pose_overrides", {})
        self.dry_run = dry_run
        self.resume = resume
        self.force = force

        self.output_dir = output_dir or Path("output") / self._slug()
        self.status_path = self.output_dir / "batch_status.json"

        self.status = BatchStatus(
            character_name=self.char_name,
            character_type=self.char_type,
            tile_size=self.tile_size,
            total_animations=len(self.animations),
        )

        # Load previous status if resuming (but not if forcing)
        if self.resume and not self.force and self.status_path.exists():
            self._load_status()

    def _slug(self) -> str:
        return self.char_name.lower().replace(" ", "_")

    def _load_status(self) -> None:
        data = json.loads(self.status_path.read_text())
        for anim_type, result_data in data.get("animations", {}).items():
            self.status.animations[anim_type] = AnimationResult(**result_data)
        self.status.completed = data.get("completed", 0)
        self.status.failed = data.get("failed", 0)

    def _save_status(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "character_name": self.status.character_name,
            "character_type": self.status.character_type,
            "tile_size": self.status.tile_size,
            "total_animations": self.status.total_animations,
            "completed": self.status.completed,
            "failed": self.status.failed,
            "animations": {
                k: asdict(v) for k, v in self.status.animations.items()
            },
        }
        self.status_path.write_text(json.dumps(data, indent=2) + "\n")

    async def run(self) -> BatchStatus:
        """Execute the full batch generation pipeline."""
        from adapters import StubAdapter
        from strategy_router import (
            DEFAULT_STRATEGY_MAP,
            DURATION_MAP,
            FRAME_COUNT_MAP,
            GenerationStrategy,
            StrategyRouter,
        )
        from prompts.prompt_library import PromptLibrary

        # Initialize components
        prompt_lib = PromptLibrary(
            pose_overrides={self.char_name: self.pose_overrides} if self.pose_overrides else None
        )

        if self.dry_run:
            stub = StubAdapter("dry-run-stub")
            router = StrategyRouter(interpolation_backend="rife")
            router._keyframe_adapter = stub
            router._interpolation_adapter = stub
        else:
            router = StrategyRouter(
                keyframe_model="gemini-3.1-flash-image-preview",
                interpolation_backend="rife",
            )

        char_config = {
            "name": self.char_name,
            "description": self.description,
            "tile_size": self.tile_size,
        }

        # Load anchor images once for all animations (GOLDEN RULE)
        anchor_parts = None
        api_key = None
        if not self.dry_run:
            from lib.keychain import get_credential
            api_key = get_credential("google-ai-key")
            if not api_key:
                raise RuntimeError("google-ai-key not found in Keychain")
            anchor_parts = load_anchors(self.anchor_images)
            if not anchor_parts:
                raise RuntimeError(
                    f"GOLDEN RULE VIOLATION: No anchor images found for {self.char_name}: "
                    f"{self.anchor_images}"
                )

        print(f"\n{'=' * 70}")
        print(f"BATCH GENERATION: {self.char_name} ({self.char_type}, {self.tile_size}x{self.tile_size})")
        print(f"Animations: {len(self.animations)} | Dry run: {self.dry_run} | Resume: {self.resume} | Force: {self.force}")
        print(f"{'=' * 70}\n")

        for anim_type in self.animations:
            # Skip if already complete and resuming (unless --force)
            if self.resume and not self.force and anim_type in self.status.animations:
                prev = self.status.animations[anim_type]
                if prev.status == AnimStatus.COMPLETE:
                    print(f"  SKIP {anim_type} — already complete (score: {prev.score:.1f})")
                    continue

            result = AnimationResult(animation_type=anim_type)
            start_time = time.monotonic()

            try:
                plan = router.route(anim_type, self.char_name)
                result.strategy = plan.strategy.value
                result.frame_count = plan.target_frame_count

                strategy = DEFAULT_STRATEGY_MAP.get(anim_type, GenerationStrategy.IMAGE_ONLY)

                anim_output_dir = self.output_dir / anim_type
                anim_output_dir.mkdir(parents=True, exist_ok=True)

                if strategy == GenerationStrategy.IMAGE_ONLY:
                    # ── Sheet → Split approach (Phase 5B validated) ──
                    # Generate ALL frames as a single sprite sheet in one Gemini call,
                    # then split into individual frame PNGs. This maintains character
                    # consistency across frames (unlike per-frame calls).
                    template = prompt_lib.get_template(anim_type)
                    frame_poses = template.frame_poses
                    frame_count = template.frame_count
                    cols, rows = get_grid_layout(frame_count)

                    prompt = build_sheet_prompt(
                        anim_type, char_config, frame_poses, cols, rows
                    )

                    if self.dry_run:
                        print(f"    [{anim_type}] IMAGE_ONLY sheet→split: "
                              f"{frame_count} frames in {cols}x{rows} grid (1 Gemini call)")
                        print(f"      Prompt: {prompt[:120]}...")
                        result.frames_generated = frame_count
                    else:
                        print(f"    [{anim_type}] Generating {cols}x{rows} sprite sheet ({frame_count} frames)...")
                        image_data = await call_gemini(anchor_parts, prompt, api_key)

                        # Save full sheet for debugging
                        sheet_path = anim_output_dir / f"{anim_type}_sheet.png"
                        sheet_path.write_bytes(image_data)

                        # Auto-detect grid (Gemini may produce more cells than requested)
                        actual_cols, actual_rows = detect_grid(image_data, frame_count)
                        if (actual_cols, actual_rows) != (cols, rows):
                            print(f"      Grid auto-corrected: {cols}x{rows} → {actual_cols}x{actual_rows}")
                            cols, rows = actual_cols, actual_rows

                        # Split into individual frames
                        frames = split_sheet(image_data, cols, rows, frame_count)
                        for idx, frame_data in enumerate(frames):
                            frame_path = anim_output_dir / f"frame_{idx:02d}.png"
                            frame_path.write_bytes(frame_data)

                        result.frames_generated = len(frames)
                        print(f"      Sheet saved: {sheet_path}")
                        print(f"      Split into {len(frames)} frames")

                elif strategy == GenerationStrategy.HYBRID:
                    # ── Keyframes via sheet → RIFE interpolation → frame extraction ──
                    kf_prompts = prompt_lib.get_keyframe_prompts(anim_type, char_config)
                    kf_count = len(kf_prompts)
                    kf_poses = [kf["pose"] for kf in kf_prompts]

                    if self.dry_run:
                        print(f"    [{anim_type}] HYBRID — {kf_count} keyframes (sheet) → RIFE → {plan.target_frame_count} frames")
                        for kf in kf_prompts:
                            print(f"      KF {kf['keyframe_index'] + 1}: {kf['pose'][:80]}...")
                        print(f"      → RIFEAdapter.interpolate_frames() → extract frames")
                        result.frames_generated = plan.target_frame_count
                    else:
                        # Step 1: Generate keyframes as a sprite sheet (same proven approach)
                        kf_cols, kf_rows = get_grid_layout(kf_count)
                        kf_sheet_prompt = build_sheet_prompt(
                            anim_type, char_config, kf_poses, kf_cols, kf_rows
                        )
                        print(f"    [{anim_type}] Generating {kf_count} keyframes as {kf_cols}x{kf_rows} sheet...")
                        kf_image_data = await call_gemini(anchor_parts, kf_sheet_prompt, api_key)

                        # Save keyframe sheet
                        kf_sheet_path = anim_output_dir / f"{anim_type}_keyframes_sheet.png"
                        kf_sheet_path.write_bytes(kf_image_data)

                        # Split keyframes
                        actual_kf_cols, actual_kf_rows = detect_grid(kf_image_data, kf_count)
                        kf_frames_data = split_sheet(kf_image_data, actual_kf_cols, actual_kf_rows, kf_count)

                        # Save individual keyframes and build GeneratedFrame list for RIFE
                        from adapters import GeneratedFrame
                        keyframes = []
                        for idx, kf_data in enumerate(kf_frames_data):
                            kf_path = anim_output_dir / f"keyframe_{idx:02d}.png"
                            kf_path.write_bytes(kf_data)
                            keyframes.append(GeneratedFrame(
                                data=kf_data,
                                width=self.tile_size,
                                height=self.tile_size,
                            ))
                        print(f"      {len(keyframes)} keyframes saved")

                        # Step 2: RIFE interpolation
                        try:
                            video = await plan.interpolation_adapter.interpolate_frames(
                                keyframes,
                                duration_secs=plan.clip_duration_secs,
                                fps=plan.fps,
                            )

                            # Step 3: Extract frames from MP4
                            extracted = self._extract_frames_from_video(
                                video.data, anim_output_dir
                            )
                            result.frames_generated = extracted
                            print(f"      RIFE → {extracted} interpolated frames extracted")
                        except Exception as rife_err:
                            # RIFE/Alienware may be offline — save keyframes anyway
                            print(f"      RIFE failed ({rife_err}), saving keyframes only")
                            result.frames_generated = len(keyframes)

                result.status = AnimStatus.COMPLETE
                result.score = 100.0 if self.dry_run else 0.0
                self.status.completed += 1

            except Exception as e:
                result.status = AnimStatus.FAILED
                result.error = str(e)
                self.status.failed += 1
                print(f"  FAIL {anim_type}: {e}")

            result.duration_ms = (time.monotonic() - start_time) * 1000
            self.status.animations[anim_type] = result

            status_icon = "PASS" if result.status == AnimStatus.COMPLETE else "FAIL"
            print(f"  {status_icon} {anim_type:<20} {result.strategy:<12} "
                  f"{result.frames_generated}/{result.frame_count} frames "
                  f"({result.duration_ms:.0f}ms)")

            # Rate limiting delay between animations (skip in dry run)
            if not self.dry_run and result.status == AnimStatus.COMPLETE:
                await asyncio.sleep(10)

        self._save_status()

        print(f"\n{'─' * 70}")
        print(f"BATCH COMPLETE: {self.status.completed}/{self.status.total_animations} passed, "
              f"{self.status.failed} failed")
        print(f"Status saved: {self.status_path}")

        return self.status

    @staticmethod
    def _extract_frames_from_video(video_bytes: bytes, output_dir: Path) -> int:
        """Extract individual PNG frames from MP4 video bytes using ffmpeg."""
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_path = Path(tmp.name)

        try:
            frame_pattern = str(output_dir / "frame_%02d.png")
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(tmp_path), "-vsync", "0", frame_pattern],
                capture_output=True,
                check=True,
            )
            # Count extracted frames
            extracted = sorted(output_dir.glob("frame_*.png"))
            return len(extracted)
        finally:
            tmp_path.unlink(missing_ok=True)


async def main():
    parser = argparse.ArgumentParser(description="Batch generate sprite animations")
    parser.add_argument("manifest", type=Path, help="Path to character manifest JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without calling APIs")
    parser.add_argument("--resume", action="store_true", help="Skip completed animations")
    parser.add_argument("--force", action="store_true", help="Force re-run even if marked COMPLETE")
    parser.add_argument("--output-dir", type=Path, help="Override output directory")
    args = parser.parse_args()

    orchestrator = BatchOrchestrator(
        manifest_path=args.manifest,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        resume=args.resume,
        force=args.force,
    )

    await orchestrator.run()


if __name__ == "__main__":
    asyncio.run(main())
