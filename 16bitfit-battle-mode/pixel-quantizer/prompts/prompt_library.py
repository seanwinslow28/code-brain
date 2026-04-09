"""NB2 Prompt Template Library for sprite generation.

Structured prompt templates for each animation type. Replaces ad-hoc
prompt strings with frame-aware, strategy-aware templates that include
all required style tokens, green screen directive, and facing direction.

Usage:
    from prompts.prompt_library import PromptLibrary

    lib = PromptLibrary()
    prompt = lib.get_prompt(
        animation_type="walk_forward",
        character_config={"name": "Sean", "description": "...", "tile_size": 128},
        frame_index=0,
        total_frames=8,
        strategy="hybrid",
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ─── Style Constants ──────────────────────────────────────────────────

STYLE_TOKENS = "SF2 pixel art, bold #272929 outlines, clean pixel edges"
GREEN_SCREEN = "solid #00FF00 green background"
FACING = "facing right"
NEGATIVE_PROMPT = (
    "blurry, anti-aliased, gradient, smooth shading, 3D render, "
    "realistic, photographic, watermark, text, HUD, UI elements, "
    "anime proportions, chibi, background scenery, multiple characters"
)


# ─── Pose Descriptions per Animation ─────────────────────────────────

@dataclass
class AnimationTemplate:
    """Template for one animation type."""
    name: str
    frame_count: int
    strategy: str  # "image_only" or "hybrid"
    frame_poses: list[str]  # One pose description per frame
    keyframe_indices: list[int] = field(default_factory=list)  # For HYBRID: which frames are keyframes
    keyframe_descriptions: list[str] = field(default_factory=list)  # Keyframe-specific poses


def _lerp_poses(poses: list[tuple[int, str]], total: int) -> list[str]:
    """Distribute named poses across frame indices, filling gaps with interpolation labels."""
    result = [""] * total
    for idx, desc in poses:
        if idx < total:
            result[idx] = desc
    # Fill gaps
    last = ""
    for i in range(total):
        if result[i]:
            last = result[i]
        else:
            result[i] = f"transitioning from previous pose — {last}" if last else "neutral stance"
    return result


# ─── Animation Templates ─────────────────────────────────────────────

ANIMATION_TEMPLATES: dict[str, AnimationTemplate] = {}


def _register(name: str, frame_count: int, strategy: str,
              pose_map: list[tuple[int, str]],
              keyframe_indices: list[int] | None = None,
              keyframe_descs: list[str] | None = None) -> None:
    poses = _lerp_poses(pose_map, frame_count)
    ANIMATION_TEMPLATES[name] = AnimationTemplate(
        name=name,
        frame_count=frame_count,
        strategy=strategy,
        frame_poses=poses,
        keyframe_indices=keyframe_indices or [],
        keyframe_descriptions=keyframe_descs or [],
    )


# IDLE (4 frames, IMAGE_ONLY) — subtle breathing cycle
_register("idle", 4, "image_only", [
    (0, "neutral fighting stance, weight centered, arms at guard position"),
    (1, "slight chest expansion, breathing in, arms relaxed slightly"),
    (2, "neutral fighting stance, weight centered, arms at guard position"),
    (3, "slight chest compression, breathing out, shoulders lower"),
])

# WALK_FORWARD (8 frames, HYBRID) — classic walk cycle
_register("walk_forward", 8, "hybrid", [
    (0, "right foot contact, heel striking ground, left arm forward"),
    (1, "right foot flat, weight shifting forward, left arm swinging back"),
    (2, "right foot passing, left foot lifting off, arms at sides"),
    (3, "right foot reaching forward, left foot pushing off, right arm forward"),
    (4, "left foot contact, heel striking ground, right arm forward"),
    (5, "left foot flat, weight shifting forward, right arm swinging back"),
    (6, "left foot passing, right foot lifting off, arms at sides"),
    (7, "left foot reaching forward, right foot pushing off, left arm forward"),
], keyframe_indices=[0, 2, 4, 6], keyframe_descs=[
    "right foot contact pose, heel on ground, left arm forward",
    "right foot passing pose, mid-stride, arms at sides",
    "left foot contact pose, heel on ground, right arm forward",
    "left foot passing pose, mid-stride, arms at sides",
])

# WALK_BACKWARD (8 frames, HYBRID)
_register("walk_backward", 8, "hybrid", [
    (0, "right foot stepping back, toe touching ground behind, arms at guard"),
    (1, "weight shifting to right foot behind, left foot lifting"),
    (2, "left foot passing, mid-step backward, arms at guard"),
    (3, "left foot stepping back, toe touching ground behind"),
    (4, "weight shifting to left foot behind, right foot lifting"),
    (5, "right foot passing, mid-step backward, arms at guard"),
    (6, "right foot stepping back, toe touching ground behind"),
    (7, "weight shifting to right foot behind, returning to start position"),
], keyframe_indices=[0, 2, 4, 6], keyframe_descs=[
    "right foot stepping back, toe on ground, arms guarding",
    "left foot passing backward, mid-step",
    "left foot stepping back, toe on ground",
    "right foot passing backward, mid-step",
])

# JUMP (4 frames, HYBRID)
_register("jump", 4, "hybrid", [
    (0, "crouching pre-jump, knees bent, arms pulled back"),
    (1, "launching upward, legs extending, arms thrusting up"),
    (2, "apex of jump, legs tucked, arms raised above head"),
    (3, "descending, legs extending downward, arms lowering"),
], keyframe_indices=[0, 1, 2, 3], keyframe_descs=[
    "crouching pre-jump, knees deeply bent",
    "launching upward, full body extension",
    "apex of jump, tucked legs, arms up",
    "descending with legs extending down",
])

# CROUCH (4 frames, IMAGE_ONLY)
_register("crouch", 4, "image_only", [
    (0, "standing, beginning to lower body"),
    (1, "half-crouch, knees bending, torso lowering"),
    (2, "full crouch, knees fully bent, low center of gravity, arms guarding"),
    (3, "full crouch held, stable low position, arms at guard"),
])

# LIGHT_PUNCH (6 frames, IMAGE_ONLY)
_register("light_punch", 6, "image_only", [
    (0, "fighting stance, lead hand chambered at chin"),
    (1, "lead hand beginning to extend, shoulder rotating forward"),
    (2, "jab fully extended, fist at target height, rear hand guarding chin"),
    (3, "jab at full extension, snapping impact pose"),
    (4, "fist retracting, pulling back to guard"),
    (5, "returned to fighting stance, both hands at guard"),
])

# MEDIUM_PUNCH (8 frames, IMAGE_ONLY)
_register("medium_punch", 8, "image_only", [
    (0, "fighting stance, rear hand chambered at chin"),
    (1, "rear shoulder rotating, hip turning, hand starting to extend"),
    (2, "cross punch mid-extension, torso rotating"),
    (3, "cross punch fully extended, full body rotation, rear fist at target"),
    (4, "impact pose, fist pressing forward, body weight behind punch"),
    (5, "beginning retraction, fist pulling back"),
    (6, "torso rotating back, hand returning to guard"),
    (7, "returned to fighting stance"),
])

# HEAVY_PUNCH (8 frames, IMAGE_ONLY)
_register("heavy_punch", 8, "image_only", [
    (0, "fighting stance, winding up, rear hand pulling back"),
    (1, "deep wind-up, rear hand far back, torso coiled, knees slightly bent"),
    (2, "explosive forward rotation begins, hips leading"),
    (3, "powerful overhand punch mid-swing, arm arcing overhead"),
    (4, "overhand punch at full extension, devastating downward impact"),
    (5, "follow-through, fist continuing past target, body leaning forward"),
    (6, "recovery, pulling back from overextension"),
    (7, "returning to fighting stance"),
])

# LIGHT_KICK (6 frames, IMAGE_ONLY)
_register("light_kick", 6, "image_only", [
    (0, "fighting stance, weight shifting to rear leg"),
    (1, "lead knee lifting, chambering kick"),
    (2, "low kick extending, foot snapping toward shin height"),
    (3, "kick at full extension, foot at target"),
    (4, "leg retracting, pulling foot back"),
    (5, "returned to fighting stance"),
])

# HEAVY_KICK (8 frames, HYBRID)
_register("heavy_kick", 8, "hybrid", [
    (0, "fighting stance, shifting weight to plant foot"),
    (1, "kicking leg chambering high, knee raised to chest"),
    (2, "powerful roundhouse beginning, leg swinging"),
    (3, "roundhouse kick mid-arc, leg horizontal"),
    (4, "roundhouse at full extension, foot at head height"),
    (5, "follow-through, leg continuing past target"),
    (6, "leg retracting from kick"),
    (7, "returning to fighting stance"),
], keyframe_indices=[0, 2, 4, 6], keyframe_descs=[
    "fighting stance, weight on plant foot",
    "roundhouse beginning, leg swinging outward",
    "roundhouse at full extension, leg horizontal at head height",
    "leg retracting, returning to guard",
])

# BLOCK (6 frames, IMAGE_ONLY)
_register("block", 6, "image_only", [
    (0, "fighting stance, arms beginning to raise"),
    (1, "arms crossing in front of face and chest, defensive posture"),
    (2, "full high block, arms crossed, absorbing impact, body braced"),
    (3, "holding block, absorbing follow-up, stable stance"),
    (4, "block releasing, arms beginning to lower"),
    (5, "returning to fighting stance"),
])

# TAKE_HIT (6 frames, IMAGE_ONLY)
_register("take_hit", 6, "image_only", [
    (0, "moment of impact, head snapping back, body jolting"),
    (1, "recoiling from hit, torso bending backward, arms flailing"),
    (2, "maximum recoil, body bent back, pain expression"),
    (3, "beginning recovery, body straightening"),
    (4, "nearly recovered, shaking off hit"),
    (5, "returned to fighting stance, slightly dazed"),
])

# VICTORY (8 frames, IMAGE_ONLY)
_register("victory", 8, "image_only", [
    (0, "standing tall, fists at sides, beginning celebration"),
    (1, "right fist pumping upward, triumphant expression"),
    (2, "right fist raised high above head, chest puffed out"),
    (3, "both arms raised in victory V pose, wide stance"),
    (4, "holding victory pose, flexing"),
    (5, "arms lowering, confident stance"),
    (6, "crossing arms, smug victory pose"),
    (7, "final victory pose, arms crossed, standing dominant"),
])

# DEFEAT (8 frames, IMAGE_ONLY)
_register("defeat", 8, "image_only", [
    (0, "staggering, off balance, about to fall"),
    (1, "knees buckling, body crumpling"),
    (2, "falling sideways, arms limp"),
    (3, "hitting the ground, body sprawled"),
    (4, "lying on ground, face down, defeated"),
    (5, "slight twitch, attempting to rise"),
    (6, "collapsed back down, fully defeated"),
    (7, "lying still on ground, KO pose"),
])

# SPECIAL_MOVE (12 frames, HYBRID)
_register("special_move", 12, "hybrid", [
    (0, "fighting stance, beginning power-up, aura gathering"),
    (1, "crouching low, hands pulling back, energy charging"),
    (2, "deep charge pose, hands cupped at side, energy glowing"),
    (3, "explosive launch, hands thrusting forward, energy releasing"),
    (4, "projectile/blast at full extension, body stretched forward"),
    (5, "energy wave traveling, arms still extended"),
    (6, "follow-through, energy dissipating"),
    (7, "arms beginning to retract"),
    (8, "body straightening, returning from attack"),
    (9, "nearly recovered, stance widening"),
    (10, "settling back to guard position"),
    (11, "returned to fighting stance, ready"),
], keyframe_indices=[0, 2, 4, 8, 11], keyframe_descs=[
    "fighting stance, beginning power-up",
    "deep charge pose, hands cupped, energy glowing",
    "blast at full extension, energy projectile visible",
    "recovery, body straightening from attack",
    "returned to fighting stance",
])


# ─── Non-humanoid Pose Overrides ─────────────────────────────────────

# Characters with non-standard body types need different pose descriptions
# for locomotion animations. These override the default frame_poses.
NON_HUMANOID_OVERRIDES: dict[str, dict[str, list[str]]] = {
    "Procrastination Phantom": {
        "walk_forward": [
            "floating forward, spectral tail trailing, ghostly drift right",
            "slight bob upward, tail undulating, forward momentum",
            "hovering at apex, body tilted forward, spectral trail",
            "dipping down, ghostly surge forward",
            "floating forward, spectral tail trailing, ghostly drift",
            "slight bob upward, tail curling, forward momentum",
            "hovering at apex, body shifting forward",
            "dipping down, completing forward glide cycle",
        ],
        "walk_backward": [
            "floating backward, spectral tail leading, ghostly retreat",
            "slight bob upward, drifting back, tail extending forward",
            "hovering at apex, body tilted back, spectral trail",
            "dipping down, ghostly retreat pulse",
            "floating backward, spectral tail sweeping",
            "slight bob upward, continuing retreat",
            "hovering, body pulling back",
            "completing backward glide cycle",
        ],
        "jump": [
            "hovering low, spectral energy gathering below",
            "surging upward, spectral tail stretching, ghostly ascent",
            "apex of ascent, body fully elongated, tail whipping",
            "descending, compressing, spectral form contracting",
        ],
    },
    "Sloth Demon": {
        "walk_forward": [
            "heavy right claw slamming forward, armor plates shifting",
            "weight dragging onto right side, left claw lifting",
            "lumbering mid-stride, claws scraping ground",
            "left claw reaching forward, heavy body lurching",
            "left claw slamming down, ground impact",
            "weight shifting to left, right claw lifting",
            "lumbering mid-stride, armor rattling",
            "right claw reaching forward, completing cycle",
        ],
        "jump": [
            "crouching low, clawed feet gripping ground, armor bracing",
            "powerful leap, stocky body airborne, claws spread",
            "apex, heavy body suspended, fur bristling",
            "crashing down, clawed feet slamming, ground shaking",
        ],
    },
    "Training Dummy": {
        "walk_forward": [
            "wooden body tipping forward, pivoting on base",
            "rocking forward momentum, leather straps swaying",
            "center of gravity shifting, metal face plate glinting",
            "tipping back slightly, pendulum motion",
            "forward rock continuing, bolts rattling",
            "straps snapping taut, wooden body creaking",
            "rocking forward again, mechanical sway",
            "completing pendulum walk cycle, settling",
        ],
        "jump": [
            "spring-loaded base compressing, wooden body lowering",
            "spring releasing, wooden body launching upward",
            "apex, wooden body spinning slightly, straps flailing",
            "crashing down, base absorbing impact, bolts rattling",
        ],
    },
}


# ─── Prompt Builder ───────────────────────────────────────────────────

class PromptLibrary:
    """Generates structured prompts for NB2 sprite generation."""

    def __init__(self, pose_overrides: dict[str, dict[str, list[str]]] | None = None):
        self._overrides = {**NON_HUMANOID_OVERRIDES}
        if pose_overrides:
            for char, anims in pose_overrides.items():
                self._overrides.setdefault(char, {}).update(anims)

    def get_template(self, animation_type: str) -> AnimationTemplate | None:
        return ANIMATION_TEMPLATES.get(animation_type)

    def list_animations(self) -> list[str]:
        return sorted(ANIMATION_TEMPLATES.keys())

    def get_prompt(
        self,
        animation_type: str,
        character_config: dict[str, Any],
        frame_index: int,
        total_frames: int | None = None,
        strategy: str | None = None,
    ) -> str:
        """Generate a complete NB2 prompt for a specific frame.

        Args:
            animation_type: e.g. "walk_forward", "idle"
            character_config: Must have "name", "description", "tile_size"
            frame_index: 0-indexed frame number
            total_frames: Override template frame count
            strategy: Override template strategy

        Returns:
            Fully formatted prompt string.
        """
        template = ANIMATION_TEMPLATES.get(animation_type)
        if not template:
            raise ValueError(f"Unknown animation type: {animation_type}")

        char_name = character_config["name"]
        char_desc = character_config.get("description", char_name)
        tile_size = character_config.get("tile_size", 128)
        frames = total_frames or template.frame_count

        # Get pose — check for character-specific overrides first
        pose = self._get_pose(animation_type, char_name, frame_index, frames, template)

        prompt = (
            f"Generate a {tile_size}x{tile_size} pixel art sprite, {STYLE_TOKENS}. "
            f"Character: {char_name} — {char_desc}. "
            f"Animation: {animation_type}, frame {frame_index + 1} of {frames}. "
            f"Pose: {pose}. "
            f"{FACING}. "
            f"Background: {GREEN_SCREEN}. "
            f"No anti-aliasing, no gradients, no transparency outside character silhouette."
        )
        return prompt

    def get_negative_prompt(self) -> str:
        return NEGATIVE_PROMPT

    def get_keyframe_prompts(
        self,
        animation_type: str,
        character_config: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Generate prompts for HYBRID keyframes only.

        Returns list of dicts with 'frame_index', 'prompt', 'pose' for each keyframe.
        """
        template = ANIMATION_TEMPLATES.get(animation_type)
        if not template:
            raise ValueError(f"Unknown animation type: {animation_type}")

        if not template.keyframe_indices:
            raise ValueError(f"{animation_type} has no keyframe definitions (IMAGE_ONLY?)")

        char_name = character_config["name"]
        char_desc = character_config.get("description", char_name)
        tile_size = character_config.get("tile_size", 128)

        keyframes = []
        for i, (kf_idx, kf_desc) in enumerate(
            zip(template.keyframe_indices, template.keyframe_descriptions)
        ):
            # Use keyframe-specific description if character has overrides
            if char_name in self._overrides and animation_type in self._overrides[char_name]:
                overrides = self._overrides[char_name][animation_type]
                if kf_idx < len(overrides):
                    kf_desc = overrides[kf_idx]

            prompt = (
                f"Generate a {tile_size}x{tile_size} pixel art sprite, {STYLE_TOKENS}. "
                f"Character: {char_name} — {char_desc}. "
                f"Animation keyframe: {animation_type}, keyframe {i + 1} of {len(template.keyframe_indices)}. "
                f"Pose: {kf_desc}. "
                f"{FACING}. "
                f"Background: {GREEN_SCREEN}. "
                f"No anti-aliasing, no gradients, no transparency outside character silhouette."
            )
            keyframes.append({
                "frame_index": kf_idx,
                "keyframe_index": i,
                "prompt": prompt,
                "pose": kf_desc,
            })

        return keyframes

    def _get_pose(
        self,
        animation_type: str,
        char_name: str,
        frame_index: int,
        total_frames: int,
        template: AnimationTemplate,
    ) -> str:
        """Get pose description, checking character overrides first."""
        if char_name in self._overrides and animation_type in self._overrides[char_name]:
            overrides = self._overrides[char_name][animation_type]
            if frame_index < len(overrides):
                return overrides[frame_index]

        if frame_index < len(template.frame_poses):
            return template.frame_poses[frame_index]

        # Fallback: wrap around
        return template.frame_poses[frame_index % len(template.frame_poses)]


# ─── Verification ─────────────────────────────────────────────────────

if __name__ == "__main__":
    lib = PromptLibrary()

    sean_config = {
        "name": "Sean",
        "description": "Muscular build, blonde hair, white tank top, blue pants, white shoes",
        "tile_size": 128,
    }

    print("=" * 80)
    print("PROMPT LIBRARY VERIFICATION — Sean (Champion, 128x128)")
    print("=" * 80)

    hybrid_anims = {"walk_forward", "walk_backward", "jump", "heavy_kick", "special_move"}
    all_pass = True

    for anim_type in sorted(ANIMATION_TEMPLATES.keys()):
        template = lib.get_template(anim_type)
        assert template is not None

        # Get first and last frame prompts
        first_prompt = lib.get_prompt(anim_type, sean_config, 0)
        last_prompt = lib.get_prompt(anim_type, sean_config, template.frame_count - 1)

        # Check required tokens
        for prompt in [first_prompt, last_prompt]:
            if "#00FF00" not in prompt:
                print(f"  FAIL: {anim_type} missing green screen directive")
                all_pass = False
            if "facing right" not in prompt:
                print(f"  FAIL: {anim_type} missing facing directive")
                all_pass = False
            if "SF2 pixel art" not in prompt:
                print(f"  FAIL: {anim_type} missing style tokens")
                all_pass = False
            if "#272929" not in prompt:
                print(f"  FAIL: {anim_type} missing outline color")
                all_pass = False

        # Check frame descriptions differ
        if first_prompt == last_prompt:
            print(f"  FAIL: {anim_type} first and last frame prompts are identical!")
            all_pass = False

        # Check HYBRID has keyframe prompts
        strategy_label = "HYBRID" if anim_type in hybrid_anims else "IMAGE_ONLY"
        kf_info = ""
        if anim_type in hybrid_anims:
            kf_prompts = lib.get_keyframe_prompts(anim_type, sean_config)
            kf_info = f" | {len(kf_prompts)} keyframes"
            if not kf_prompts:
                print(f"  FAIL: {anim_type} is HYBRID but has no keyframe prompts")
                all_pass = False

        print(f"  {anim_type:<20} {strategy_label:<12} {template.frame_count} frames{kf_info}")
        print(f"    Frame 1: ...{first_prompt[-80:]}")
        print(f"    Frame {template.frame_count}: ...{last_prompt[-80:]}")

    print()
    if all_pass:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED — see above")

    # Verify non-humanoid overrides
    print("\n" + "=" * 80)
    print("NON-HUMANOID OVERRIDE CHECK — Procrastination Phantom")
    print("=" * 80)
    phantom_config = {
        "name": "Procrastination Phantom",
        "description": "Ghostly figure, white hoodie, blue-gray skin, glowing orange eyes, spectral tail",
        "tile_size": 256,
    }
    walk_prompt = lib.get_prompt("walk_forward", phantom_config, 0)
    assert "floating" in walk_prompt.lower() or "spectral" in walk_prompt.lower(), \
        "Phantom walk should use floating override, not standard walking"
    print(f"  walk_forward frame 1: ...{walk_prompt[-100:]}")
    print("  PASS: Non-humanoid overrides applied")
