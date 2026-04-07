#!/usr/bin/env python3
"""LoRA Training Dataset Preparation Script.

Takes a directory of source PNGs, nearest-neighbor upscales to 1024×1024,
generates caption .txt files from a template, and validates output.

Usage:
    python3 prepare_dataset.py --input ./source-sprites --output ./dataset/10_16bitfit_style
    python3 prepare_dataset.py --input ./source-sprites --output ./dataset/10_16bitfit_style --dry-run

CRITICAL: Nearest-neighbor upscaling ONLY. Never use bicubic/bilinear —
          they blur pixel art and destroy the hard edges we want the LoRA to learn.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)


# Trigger word — unique token the LoRA will associate with the style
TRIGGER_WORD = "16bitfit_style"

# Default caption template
# Caption EVERYTHING that isn't part of the style you want learned.
# Describe subjects, poses, backgrounds — the model learns style from what remains.
DEFAULT_CAPTION_TEMPLATE = (
    "{trigger}, pixel art fighting game character, {pose_desc}, "
    "bold outlines, flat cel shading, {bg_desc}, SF2 style, 128x128 sprite"
)

# Per-image customization: map filename patterns to pose/background descriptions
CAPTION_OVERRIDES: dict[str, dict[str, str]] = {
    # Add overrides here as you add images to the dataset:
    # "idle_001": {"pose_desc": "idle stance, arms at sides", "bg_desc": "transparent background"},
    # "walk_003": {"pose_desc": "walking forward, mid-stride", "bg_desc": "green screen background"},
}

# Example captions for reference:
EXAMPLE_CAPTIONS = [
    f"{TRIGGER_WORD}, pixel art fighting game character, idle stance, bold outlines, flat cel shading, transparent background, SF2 style, 128x128 sprite",
    f"{TRIGGER_WORD}, pixel art warrior, walking forward, side view, dark outlines, limited color palette, chroma key green background, retro arcade style",
    f"{TRIGGER_WORD}, pixel art fighter, throwing a punch, dynamic pose, bold outlines, flat shading, transparent background, Street Fighter style",
    f"{TRIGGER_WORD}, pixel art character, crouching, defensive pose, 2-3px dark outlines, cel shaded, green screen background, 16-bit style",
    f"{TRIGGER_WORD}, pixel art boss character, 256x256 sprite, heavy build, menacing stance, bold outlines, limited palette, transparent background",
]


def validate_image(path: Path) -> tuple[bool, str]:
    """Validate that an image is suitable for training.

    Returns:
        (is_valid, message)
    """
    if not path.exists():
        return False, f"File not found: {path}"

    if path.suffix.lower() not in (".png",):
        return False, f"Not a PNG: {path.suffix}. JPEG compression destroys pixel art."

    try:
        img = Image.open(path)
    except Exception as e:
        return False, f"Cannot open image: {e}"

    w, h = img.size
    if w < 32 or h < 32:
        return False, f"Too small: {w}x{h}. Minimum 32x32."

    if img.mode not in ("RGB", "RGBA", "P"):
        return False, f"Unusual mode: {img.mode}. Expected RGB/RGBA/P."

    return True, f"OK ({w}x{h}, {img.mode})"


def nearest_neighbor_upscale(img: Image.Image, target_size: int = 1024) -> Image.Image:
    """Upscale image to target_size using nearest-neighbor interpolation.

    CRITICAL: Never use BILINEAR, BICUBIC, or LANCZOS — they blur pixel art.
    """
    return img.resize((target_size, target_size), Image.NEAREST)


def generate_caption(filename: str) -> str:
    """Generate a caption for an image based on its filename.

    Uses CAPTION_OVERRIDES for per-image customization, falls back to template.
    """
    stem = Path(filename).stem.lower()

    # Check for per-image override
    for pattern, overrides in CAPTION_OVERRIDES.items():
        if pattern in stem:
            pose = overrides.get("pose_desc", "standing pose")
            bg = overrides.get("bg_desc", "transparent background")
            return DEFAULT_CAPTION_TEMPLATE.format(
                trigger=TRIGGER_WORD, pose_desc=pose, bg_desc=bg
            )

    # Auto-detect pose from filename keywords
    pose_desc = "standing pose"
    bg_desc = "transparent background"

    if "fighting-stance" in stem or "fighting_stance" in stem:
        pose_desc = "fighting stance, fists raised, weight on back foot"
    elif "menacing-idle" in stem or "menacing_idle" in stem:
        pose_desc = "menacing idle stance, fists clenched, intimidating"
    elif "idle" in stem:
        pose_desc = "idle stance, arms at sides"
    elif "walk" in stem:
        pose_desc = "walking forward, mid-stride"
    elif "uppercut" in stem:
        pose_desc = "throwing a rising uppercut, fist driving upward"
    elif "punch" in stem or "jab" in stem:
        pose_desc = "throwing a punch, arm extended forward"
    elif "ground-slam" in stem or "ground_slam" in stem:
        pose_desc = "slamming fists into the ground, bent forward"
    elif "energy-blast" in stem or "energy_blast" in stem:
        pose_desc = "firing energy blast from outstretched hands"
    elif "attack-windup" in stem or "attack_windup" in stem:
        pose_desc = "winding up for a heavy attack, arm pulled back"
    elif "kick" in stem:
        pose_desc = "executing a kick, leg extended"
    elif "block" in stem or "defend" in stem:
        pose_desc = "blocking stance, arms raised to protect"
    elif "crouch" in stem or "duck" in stem:
        pose_desc = "crouching low, ducking under attack"
    elif "jump" in stem or "airborne" in stem:
        pose_desc = "jumping, airborne mid-air pose"
    elif "hit" in stem or "hurt" in stem:
        pose_desc = "taking a hit, recoiling backward in pain"
    elif "victory" in stem or "win" in stem:
        pose_desc = "victory pose, arms raised celebrating"
    elif "charging" in stem or "charge" in stem:
        pose_desc = "charging forward aggressively, head lowered"
    elif "flexing" in stem or "taunt" in stem:
        pose_desc = "flexing muscles, taunting arrogantly"
    elif "vanishing" in stem or "dodge" in stem:
        pose_desc = "dodging with ethereal vanishing effect"
    elif "facing-right" in stem or "facing_right" in stem:
        pose_desc = "standing pose, facing right, neutral stance"
    elif "defeat" in stem or "ko" in stem:
        pose_desc = "defeated, falling down"

    # All generated images have green backgrounds; only override if filename says otherwise
    bg_desc = "chroma key green background"

    return DEFAULT_CAPTION_TEMPLATE.format(
        trigger=TRIGGER_WORD, pose_desc=pose_desc, bg_desc=bg_desc
    )


def prepare_dataset(
    input_dir: Path,
    output_dir: Path,
    target_size: int = 1024,
    dry_run: bool = False,
) -> dict:
    """Process all PNGs in input_dir and prepare them for LoRA training.

    Returns:
        Summary dict with counts and any errors.
    """
    summary = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "target_size": target_size,
        "images_found": 0,
        "images_processed": 0,
        "images_skipped": 0,
        "captions_generated": 0,
        "errors": [],
    }

    # Find all PNGs
    source_files = sorted(input_dir.glob("*.png"))
    summary["images_found"] = len(source_files)

    if not source_files:
        print(f"No PNG files found in {input_dir}")
        return summary

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nProcessing {len(source_files)} images → {target_size}x{target_size}")
    print(f"Trigger word: {TRIGGER_WORD}")
    print(f"Output: {output_dir}")
    print()

    for src_path in source_files:
        # Validate
        is_valid, msg = validate_image(src_path)
        if not is_valid:
            print(f"  SKIP {src_path.name}: {msg}")
            summary["images_skipped"] += 1
            summary["errors"].append({"file": src_path.name, "error": msg})
            continue

        # Generate caption
        caption = generate_caption(src_path.name)

        if dry_run:
            img = Image.open(src_path)
            w, h = img.size
            print(f"  {src_path.name} ({w}x{h}) → {target_size}x{target_size}")
            print(f"    Caption: {caption[:80]}...")
            summary["images_processed"] += 1
            summary["captions_generated"] += 1
            continue

        # Upscale with nearest-neighbor
        img = Image.open(src_path).convert("RGBA")
        upscaled = nearest_neighbor_upscale(img, target_size)

        # Save image
        out_img_path = output_dir / src_path.name
        upscaled.save(out_img_path, "PNG")

        # Save caption
        out_txt_path = output_dir / f"{src_path.stem}.txt"
        out_txt_path.write_text(caption, encoding="utf-8")

        # Verify output
        result_img = Image.open(out_img_path)
        assert result_img.size == (target_size, target_size), f"Size mismatch: {result_img.size}"

        print(f"  OK {src_path.name} → {out_img_path.name} + {out_txt_path.name}")
        summary["images_processed"] += 1
        summary["captions_generated"] += 1

    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Prepare LoRA training dataset from source PNGs"
    )
    parser.add_argument(
        "--input", type=str, required=True,
        help="Directory containing source PNG sprites",
    )
    parser.add_argument(
        "--output", type=str, required=True,
        help="Output directory for prepared dataset (e.g., dataset/10_16bitfit_style)",
    )
    parser.add_argument(
        "--target-size", type=int, default=1024,
        help="Output image size (default: 1024x1024)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be done without writing files",
    )
    parser.add_argument(
        "--show-examples", action="store_true",
        help="Print example captions and exit",
    )
    args = parser.parse_args()

    if args.show_examples:
        print("Example captions for LoRA training:\n")
        for i, caption in enumerate(EXAMPLE_CAPTIONS, 1):
            print(f"  {i}. {caption}")
        print(f"\nTrigger word: {TRIGGER_WORD}")
        print("Customize per-image captions in CAPTION_OVERRIDES dict.")
        return

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}")
        sys.exit(1)

    summary = prepare_dataset(input_dir, output_dir, args.target_size, args.dry_run)

    print(f"\n=== Dataset Preparation Summary ===")
    print(f"Images found: {summary['images_found']}")
    print(f"Images processed: {summary['images_processed']}")
    print(f"Images skipped: {summary['images_skipped']}")
    print(f"Captions generated: {summary['captions_generated']}")
    if summary["errors"]:
        print(f"Errors: {len(summary['errors'])}")
        for err in summary["errors"]:
            print(f"  {err['file']}: {err['error']}")

    # Estimate training steps
    if summary["images_processed"] > 0:
        repeats = 10
        epochs = 10
        batch = 1
        steps = (summary["images_processed"] * repeats * epochs) // batch
        time_min = steps * 0.5 / 60  # ~0.5s per step on RTX 5080
        time_max = steps * 1.5 / 60
        print(f"\nEstimated training steps: ~{steps}")
        print(f"Estimated training time: {time_min:.0f}-{time_max:.0f} minutes")


if __name__ == "__main__":
    main()
