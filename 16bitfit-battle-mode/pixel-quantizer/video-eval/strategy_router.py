"""Strategy Router — selects generation strategy per animation type.

Routes manifest animation entries to the correct generation pipeline:
  - image_only: Static poses, idle, attacks → GeminiAdapter.generate_frame()
  - hybrid: Walk/run cycles, complex locomotion → keyframes + video interpolation
  - motion_transfer: (Experimental) Reference video + anchor → video model

The router reads the animation type from the manifest and returns a
GenerationPlan with the selected strategy and adapter configuration.

Four atomic operations (from hybrid-pipeline-plan.md):
  1. generate_frame — single frame from anchor + pose ref
  2. generate_keyframes — 3-5 keyframes for video interpolation
  3. interpolate_frames — video model fills between keyframes
  4. generate_video — motion transfer from reference video
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from adapters import (
    GeneratedFrame,
    GeneratedVideo,
    GeminiAdapter,
    GMFSSAdapter,
    KeyframeConfig,
    ReplicateAdapter,
    VideoModelAdapter,
    Wan22Adapter,
)


class GenerationStrategy(Enum):
    """Generation strategy selected per animation type."""
    IMAGE_ONLY = "image_only"
    HYBRID = "hybrid"
    MOTION_TRANSFER = "motion_transfer"


@dataclass
class GenerationPlan:
    """Execution plan for generating one animation's frames."""
    strategy: GenerationStrategy
    animation_type: str
    character_name: str

    # Adapter assignments
    keyframe_adapter: VideoModelAdapter | None = None  # For generate_frame / generate_keyframes
    interpolation_adapter: VideoModelAdapter | None = None  # For interpolate_frames
    video_adapter: VideoModelAdapter | None = None  # For generate_video (motion transfer)

    # Parameters
    target_frame_count: int = 8
    duration_secs: float = 2.0
    fps: int = 12  # Pixel art friendly
    keyframe_count: int = 3  # For hybrid strategy

    # Post-processing flags
    apply_green_screen: bool = True  # Chroma key #00FF00 before video
    apply_pixel_quantizer: bool = True  # Run through 7-step quantizer
    clip_duration_secs: float = 2.0  # 2s for walk, 1s for combat


# ─── Default Strategy Map ──────────────────────────────────────────────
# Maps animation type → generation strategy.
# This is the manifest-level default; can be overridden per-character.

DEFAULT_STRATEGY_MAP: dict[str, GenerationStrategy] = {
    # Image-only (proven working in v0.1.0)
    "idle": GenerationStrategy.IMAGE_ONLY,
    "crouch": GenerationStrategy.IMAGE_ONLY,
    "light_punch": GenerationStrategy.IMAGE_ONLY,
    "medium_punch": GenerationStrategy.IMAGE_ONLY,
    "heavy_punch": GenerationStrategy.IMAGE_ONLY,
    "light_kick": GenerationStrategy.IMAGE_ONLY,
    "block": GenerationStrategy.IMAGE_ONLY,
    "take_hit": GenerationStrategy.IMAGE_ONLY,
    "victory": GenerationStrategy.IMAGE_ONLY,
    "defeat": GenerationStrategy.IMAGE_ONLY,

    # Hybrid (keyframe → video interpolation)
    "walk_forward": GenerationStrategy.HYBRID,
    "walk_backward": GenerationStrategy.HYBRID,
    "jump": GenerationStrategy.HYBRID,
    "heavy_kick": GenerationStrategy.HYBRID,
    "special_move": GenerationStrategy.HYBRID,

    # Motion transfer (experimental — stub for now)
    # "walk_forward_mxfer": GenerationStrategy.MOTION_TRANSFER,
}

# Duration mapping: combat = 1s, locomotion = 2s
DURATION_MAP: dict[str, float] = {
    "idle": 2.0,
    "walk_forward": 2.0,
    "walk_backward": 2.0,
    "jump": 1.0,
    "crouch": 1.0,
    "light_punch": 1.0,
    "medium_punch": 1.0,
    "heavy_punch": 1.0,
    "light_kick": 1.0,
    "heavy_kick": 1.0,
    "block": 1.0,
    "take_hit": 1.0,
    "victory": 2.0,
    "defeat": 2.0,
    "special_move": 2.0,
}

# Frame count per animation type
FRAME_COUNT_MAP: dict[str, int] = {
    "idle": 4,
    "walk_forward": 8,
    "walk_backward": 8,
    "jump": 4,
    "crouch": 4,
    "light_punch": 6,
    "medium_punch": 8,
    "heavy_punch": 8,
    "light_kick": 6,
    "heavy_kick": 8,
    "block": 6,
    "take_hit": 6,
    "victory": 8,
    "defeat": 8,
    "special_move": 12,
}


class StrategyRouter:
    """Routes animation types to generation strategies and adapter configs.

    The router is the orchestration brain of the hybrid pipeline. It:
    1. Reads the animation type
    2. Selects the generation strategy (image-only vs hybrid)
    3. Assigns the correct adapters for each atomic operation
    4. Returns a GenerationPlan that the pipeline executor follows
    """

    def __init__(
        self,
        keyframe_model: str = "gemini-3.1-flash-image-preview",
        interpolation_backend: str = "wan22",
        strategy_overrides: dict[str, GenerationStrategy] | None = None,
    ):
        """Configure the router.

        Args:
            keyframe_model: Gemini model ID for keyframe generation.
                           Default: NB2 (Flash) for volume. Use
                           "gemini-3-pro-image-preview" for NB Pro quality.
            interpolation_backend: Which video model for hybrid strategy.
                                  "wan22" = local Wan 2.2 + LoRA on Alienware.
                                  "gmfss" = GMFSS Fortuna frame interpolation.
                                  "replicate" = rd-animation via Replicate API.
            strategy_overrides: Override the default strategy for specific
                               animation types.
        """
        self._keyframe_adapter = GeminiAdapter(model_id=keyframe_model)

        if interpolation_backend == "wan22":
            self._interpolation_adapter = Wan22Adapter()
        elif interpolation_backend == "gmfss":
            self._interpolation_adapter = GMFSSAdapter()
        elif interpolation_backend == "replicate":
            self._interpolation_adapter = ReplicateAdapter()
        else:
            raise ValueError(f"Unknown interpolation backend: {interpolation_backend}")

        self._replicate_adapter = ReplicateAdapter()
        self._strategy_map = {**DEFAULT_STRATEGY_MAP}
        if strategy_overrides:
            self._strategy_map.update(strategy_overrides)

    def route(
        self,
        animation_type: str,
        character_name: str,
        strategy_override: GenerationStrategy | None = None,
    ) -> GenerationPlan:
        """Create a generation plan for an animation.

        Args:
            animation_type: e.g., "walk_forward", "idle", "special_move".
            character_name: e.g., "Sean".
            strategy_override: Force a specific strategy (ignores map).

        Returns:
            GenerationPlan with adapters and parameters configured.
        """
        strategy = strategy_override or self._strategy_map.get(
            animation_type, GenerationStrategy.IMAGE_ONLY
        )

        duration = DURATION_MAP.get(animation_type, 1.0)
        frame_count = FRAME_COUNT_MAP.get(animation_type, 8)

        plan = GenerationPlan(
            strategy=strategy,
            animation_type=animation_type,
            character_name=character_name,
            target_frame_count=frame_count,
            duration_secs=duration,
            clip_duration_secs=duration,
        )

        if strategy == GenerationStrategy.IMAGE_ONLY:
            plan.keyframe_adapter = self._keyframe_adapter
            plan.apply_pixel_quantizer = False  # Image-only output is already pixel art
            plan.apply_green_screen = True

        elif strategy == GenerationStrategy.HYBRID:
            plan.keyframe_adapter = self._keyframe_adapter
            plan.interpolation_adapter = self._interpolation_adapter
            plan.keyframe_count = 3  # Start, mid, end poses
            plan.apply_pixel_quantizer = True  # Video output needs quantizing
            plan.apply_green_screen = True  # Green screen BEFORE feeding to video model

        elif strategy == GenerationStrategy.MOTION_TRANSFER:
            plan.video_adapter = self._replicate_adapter
            plan.apply_pixel_quantizer = True
            plan.apply_green_screen = True

        return plan

    def list_strategies(self) -> dict[str, str]:
        """Return the current strategy map as human-readable strings."""
        return {
            anim_type: strategy.value
            for anim_type, strategy in self._strategy_map.items()
        }


async def execute_plan(plan: GenerationPlan, config: KeyframeConfig) -> list[GeneratedFrame]:
    """Execute a generation plan and return the final frames.

    This is the top-level pipeline executor. It follows the plan's
    strategy and calls the assigned adapters in sequence.

    Args:
        plan: The GenerationPlan from StrategyRouter.route().
        config: KeyframeConfig with character/animation details.

    Returns:
        List of GeneratedFrame objects (post-quantized if applicable).
    """
    from evaluator import extract_frames_from_video

    if plan.strategy == GenerationStrategy.IMAGE_ONLY:
        if not plan.keyframe_adapter:
            raise RuntimeError("IMAGE_ONLY plan requires a keyframe_adapter")

        # Generate each frame individually
        frames = await plan.keyframe_adapter.generate_keyframes(config)
        return frames

    elif plan.strategy == GenerationStrategy.HYBRID:
        if not plan.keyframe_adapter or not plan.interpolation_adapter:
            raise RuntimeError(
                "HYBRID plan requires both keyframe_adapter and interpolation_adapter"
            )

        # Step 1: Generate keyframes with image model
        keyframes = await plan.keyframe_adapter.generate_keyframes(config)

        # Step 2: Interpolate between keyframes with video model
        video = await plan.interpolation_adapter.interpolate_frames(
            keyframes,
            duration_secs=plan.clip_duration_secs,
            fps=plan.fps,
        )

        # Step 3: Extract target frame count from video
        frames = extract_frames_from_video(video, plan.target_frame_count)
        return frames

    elif plan.strategy == GenerationStrategy.MOTION_TRANSFER:
        if not plan.video_adapter:
            raise RuntimeError("MOTION_TRANSFER plan requires a video_adapter")

        # Generate from single anchor + motion description
        anchor = GeneratedFrame(
            data=b"",  # Caller should provide anchor in config
            width=config.width,
            height=config.height,
        )

        motion_desc = (
            f"{config.animation_type} animation for {config.character_name}, "
            f"pixel art sprite, SF2 style"
        )

        video = await plan.video_adapter.generate_video(
            reference_image=anchor,
            motion_description=motion_desc,
            duration_secs=plan.clip_duration_secs,
        )

        frames = extract_frames_from_video(video, plan.target_frame_count)
        return frames

    else:
        raise ValueError(f"Unknown strategy: {plan.strategy}")


# ─── Quick Test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    router = StrategyRouter(
        keyframe_model="gemini-3.1-flash-image-preview",
        interpolation_backend="wan22",
    )

    print("Strategy Router — Animation Type Mapping:")
    print(f"{'Animation':<20} {'Strategy':<15} {'Duration':<10} {'Frames':<8}")
    print("-" * 55)

    for anim_type in sorted(DEFAULT_STRATEGY_MAP.keys()):
        plan = router.route(anim_type, "Sean")
        print(
            f"{anim_type:<20} {plan.strategy.value:<15} "
            f"{plan.duration_secs:<10.1f} {plan.target_frame_count:<8}"
        )

    # Test that hybrid routes correctly
    walk_plan = router.route("walk_forward", "Sean")
    assert walk_plan.strategy == GenerationStrategy.HYBRID
    assert walk_plan.keyframe_adapter is not None
    assert walk_plan.interpolation_adapter is not None
    assert walk_plan.apply_pixel_quantizer is True
    assert walk_plan.apply_green_screen is True
    assert walk_plan.clip_duration_secs == 2.0

    # Test that image-only routes correctly
    idle_plan = router.route("idle", "Sean")
    assert idle_plan.strategy == GenerationStrategy.IMAGE_ONLY
    assert idle_plan.keyframe_adapter is not None
    assert idle_plan.interpolation_adapter is None
    assert idle_plan.apply_pixel_quantizer is False

    # Test strategy override
    forced_plan = router.route("idle", "Sean", strategy_override=GenerationStrategy.HYBRID)
    assert forced_plan.strategy == GenerationStrategy.HYBRID

    print("\nAll router assertions PASSED")
