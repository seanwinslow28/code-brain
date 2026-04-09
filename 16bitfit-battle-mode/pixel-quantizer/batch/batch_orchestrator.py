"""Batch Generation Orchestrator — generates ALL animation frames for a character.

Takes a character manifest JSON and drives each animation through the correct
pipeline (IMAGE_ONLY or HYBRID) using the strategy router, prompt library,
and adapter layer.

Usage:
    # Dry run (no API calls)
    python3 batch/batch_orchestrator.py manifests/champion_sean.json --dry-run

    # Live run
    python3 batch/batch_orchestrator.py manifests/champion_sean.json

    # Resume (skips completed animations)
    python3 batch/batch_orchestrator.py manifests/champion_sean.json --resume
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
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
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))


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

        self.output_dir = output_dir or Path("output") / self._slug()
        self.status_path = self.output_dir / "batch_status.json"

        self.status = BatchStatus(
            character_name=self.char_name,
            character_type=self.char_type,
            tile_size=self.tile_size,
            total_animations=len(self.animations),
        )

        # Load previous status if resuming
        if self.resume and self.status_path.exists():
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
        from adapters import KeyframeConfig, StubAdapter
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
            # Use stub adapters for dry run
            stub = StubAdapter("dry-run-stub")
            router = StrategyRouter(
                interpolation_backend="rife",
            )
            # Override router's adapters with stubs for dry run
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

        print(f"\n{'=' * 70}")
        print(f"BATCH GENERATION: {self.char_name} ({self.char_type}, {self.tile_size}x{self.tile_size})")
        print(f"Animations: {len(self.animations)} | Dry run: {self.dry_run} | Resume: {self.resume}")
        print(f"{'=' * 70}\n")

        for anim_type in self.animations:
            # Skip if already complete and resuming
            if self.resume and anim_type in self.status.animations:
                prev = self.status.animations[anim_type]
                if prev.status == AnimStatus.COMPLETE:
                    print(f"  SKIP {anim_type} — already complete (score: {prev.score:.1f})")
                    continue

            result = AnimationResult(animation_type=anim_type)
            start_time = time.monotonic()

            try:
                # Route animation through strategy map
                plan = router.route(anim_type, self.char_name)
                result.strategy = plan.strategy.value
                result.frame_count = plan.target_frame_count

                strategy = DEFAULT_STRATEGY_MAP.get(anim_type, GenerationStrategy.IMAGE_ONLY)

                anim_output_dir = self.output_dir / anim_type
                anim_output_dir.mkdir(parents=True, exist_ok=True)

                if strategy == GenerationStrategy.IMAGE_ONLY:
                    # Generate each frame individually
                    for frame_idx in range(plan.target_frame_count):
                        prompt = prompt_lib.get_prompt(
                            anim_type, char_config, frame_idx, plan.target_frame_count
                        )

                        if self.dry_run:
                            print(f"    [{anim_type}] Frame {frame_idx + 1}/{plan.target_frame_count} "
                                  f"IMAGE_ONLY → GeminiAdapter.generate_frame()")
                            print(f"      Prompt: {prompt[:100]}...")
                        else:
                            # Real generation: create KeyframeConfig per frame
                            poses = prompt_lib.get_template(anim_type).frame_poses
                            config = KeyframeConfig(
                                character_name=self.char_name,
                                animation_type=anim_type,
                                start_pose=poses[frame_idx] if frame_idx < len(poses) else "",
                                end_pose=poses[frame_idx] if frame_idx < len(poses) else "",
                                width=self.tile_size,
                                height=self.tile_size,
                            )
                            frames = await plan.keyframe_adapter.generate_keyframes(config)
                            # Save frame
                            frame_path = anim_output_dir / f"frame_{frame_idx:02d}.png"
                            if frames:
                                frame_path.write_bytes(frames[0].data)

                        result.frames_generated += 1

                elif strategy == GenerationStrategy.HYBRID:
                    # Generate keyframes then interpolate
                    kf_prompts = prompt_lib.get_keyframe_prompts(anim_type, char_config)

                    if self.dry_run:
                        print(f"    [{anim_type}] HYBRID — {len(kf_prompts)} keyframes → RIFE interpolation")
                        for kf in kf_prompts:
                            print(f"      KF {kf['keyframe_index'] + 1}: {kf['pose'][:80]}...")
                        print(f"      → RIFEAdapter.interpolate_frames() → Pixel Quantizer")
                        result.frames_generated = plan.target_frame_count
                    else:
                        # Real generation
                        config = KeyframeConfig(
                            character_name=self.char_name,
                            animation_type=anim_type,
                            start_pose=kf_prompts[0]["pose"],
                            end_pose=kf_prompts[-1]["pose"],
                            width=self.tile_size,
                            height=self.tile_size,
                        )
                        keyframes = await plan.keyframe_adapter.generate_keyframes(config)
                        video = await plan.interpolation_adapter.interpolate_frames(
                            keyframes,
                            duration_secs=plan.clip_duration_secs,
                            fps=plan.fps,
                        )
                        # TODO: Extract frames from video, run Pixel Quantizer, score
                        result.frames_generated = plan.target_frame_count

                result.status = AnimStatus.COMPLETE
                result.score = 100.0 if self.dry_run else 0.0  # Placeholder for real scoring
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

        self._save_status()

        print(f"\n{'─' * 70}")
        print(f"BATCH COMPLETE: {self.status.completed}/{self.status.total_animations} passed, "
              f"{self.status.failed} failed")
        print(f"Status saved: {self.status_path}")

        return self.status


async def main():
    parser = argparse.ArgumentParser(description="Batch generate sprite animations")
    parser.add_argument("manifest", type=Path, help="Path to character manifest JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without calling APIs")
    parser.add_argument("--resume", action="store_true", help="Skip completed animations")
    parser.add_argument("--output-dir", type=Path, help="Override output directory")
    args = parser.parse_args()

    orchestrator = BatchOrchestrator(
        manifest_path=args.manifest,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        resume=args.resume,
    )

    await orchestrator.run()


if __name__ == "__main__":
    asyncio.run(main())
