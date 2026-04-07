#!/usr/bin/env python3
"""
LoRA Training Dataset Generator — 16BitFit Battle Mode
========================================================
Generates additional training images using Gemini (Nano Banana 2) to fill
gaps in the LoRA training dataset. Uses existing character images as style
references so Gemini maintains the established 16BitFit aesthetic.

This script follows the 7-Layer Prompt Framework from the
image-generator-prompt-science skill and the Battle Mode style cluster
from 16bitfit-styles.md.

Why we're generating these:
- The sliced dataset is heavy on neutral standing poses (turnaround sheets)
  and Sean's action poses. We need action poses for the OTHER 11 characters.
- The LoRA needs to see the 16BitFit style across different characters,
  poses, and actions — not just standing turnarounds.
- All generated images use green screen (#00FF00) backgrounds for consistency
  with the sprite pipeline.

Usage:
    python3 generate_dataset.py --list              # Show all prompts (no generation)
    python3 generate_dataset.py --run               # Generate all images
    python3 generate_dataset.py --run --character sean  # Generate only Sean's poses
    python3 generate_dataset.py --run --index 0 3 5     # Generate specific prompt indices

Prerequisites:
    pip install google-genai
    GEMINI_API_KEY in environment or .env file
"""

import argparse
import sys
import os
import time
from pathlib import Path

# Output directory for generated images
OUTPUT_DIR = Path(__file__).parent / "generated-dataset"

# Reference images directory (for identity locking)
REF_DIR = Path(__file__).parent / "LoRA-Training-Dataset" / "Sprite Sheet Reference Images"

# ============================================================================
# STYLE FOUNDATION
# ============================================================================
# This is the core style cluster that anchors every prompt. Pulled directly
# from the 16bitfit-styles.md reference and the image-generator-prompt-science
# 7-Layer Framework.

STYLE_CLUSTER = (
    "Street Fighter II arcade aesthetic with bold #272929 dark outlines (2-3px), "
    "3-4 tone cel shading showing form and bone structure, top-front lighting, "
    "16-bit pixel rendering, full-color palette, crisp pixel edges"
)

BG_INSTRUCTION = (
    "The background must be solid bright green (#00FF00) chroma key. "
    "Fill the entire background with exactly this color. No floor, no shadows on ground."
)

NEGATIVE_CONSTRAINTS = (
    "No anti-aliasing on sprite edges. No gradients. No blur. No motion blur. "
    "No 3D rendering. No smooth vector art. Must look like hand-pixeled 16-bit arcade art."
)

# ============================================================================
# CHARACTER DEFINITIONS
# ============================================================================
# Each character has: description, colors, and a reference image path.
# Colors are from the 16bitfit-styles.md Champion/Boss Color Palettes.

CHARACTERS = {
    # === CHAMPIONS (128x128) ===
    "sean": {
        "type": "champion",
        "desc": "muscular blonde man with spiky hair, blue eyes, wearing white tank top and blue pants with white sneakers",
        "colors": "skin #F5D6C6, hair #C2A769, eyes #4682B4, white #F2F0EF tank top, blue #2323FF pants",
        "ref": "champions/Sean/Champion-Sean-Turnaround-Sheet.png",
    },
    "aria": {
        "type": "champion",
        "desc": "athletic woman with brown skin and dark brown hair in a high ponytail, wearing magenta crop top and blue-grey pants",
        "colors": "skin #C68642, hair #4B3621, eyes #06402B, magenta #9A2257 top, blue-grey #5577AA pants",
        "ref": "champions/Aria/Champion-Aria-Turnaround-Sheet.png",
    },
    "kenji": {
        "type": "champion",
        "desc": "lean Japanese man with black hair in a bun, wearing light grey gi top with dark grey belt and dark pants",
        "colors": "skin #FFDBAC, hair #212121, eyes #4A4A4A, light grey #B0BEC5 gi top, dark #424242 pants",
        "ref": "champions/Kenji/Champion-Kenji-Turnaround-Sheet.png",
    },
    "marcus": {
        "type": "champion",
        "desc": "muscular Black man with short black hair and glasses, wearing dark grey tank top and light grey pants with yellow boxing gloves",
        "colors": "skin #8D5524, hair #212121, eyes #4A4A4A, dark grey #545454 tank, yellow #FFD700 gloves",
        "ref": "champions/Marcus/Champion-Marcus-Turnaround-Sheet-2.png",
    },
    "mary": {
        "type": "champion",
        "desc": "fit woman with brown hair in a ponytail with purple headband, wearing pink crop top and purple shorts with white sneakers",
        "colors": "skin #F5D6C6, hair #6D4C41, eyes #654321, pink #FF7BAC top, purple #7E57C2 shorts",
        "ref": "champions/Mary/Champion-Mary-Turnaround-Sheet-2.png",
    },
    "zara": {
        "type": "champion",
        "desc": "strong woman with olive skin and dark dreadlocks, wearing dark grey tank top and black pants with white sneakers",
        "colors": "skin #CBB59D, hair #3B2F2F, eyes #654321, dark grey #545454 tank, black #212121 pants",
        "ref": "champions/Zara/Champion-Zara-Turnaround-Sheet.png",
    },
    # === BOSSES (256x256) ===
    "training-dummy": {
        "type": "boss",
        "desc": "wooden training dummy with grey padding and metal joints, humanoid robot-like appearance",
        "colors": "wood #8B5A2B body, padding #A9A9A9, joints #696969 metal",
        "ref": "bosses/Training Dummy/Create_a_professional_2k_202602121754.jpeg",
    },
    "sloth-demon": {
        "type": "boss",
        "desc": "large menacing sloth creature with brown fur, glowing amber eyes, wearing steel-blue armor plates",
        "colors": "fur #8D6E63, eyes #FFCC80 amber glow, armor #90A4AE steel-blue",
        "ref": "bosses/Sloth Demon/Create_a_professional_2k_202602121756.jpeg",
    },
    "stress-titan": {
        "type": "boss",
        "desc": "massive armored humanoid with grey-white skin, glowing red eyes, dark charcoal armor with orange energy conduits",
        "colors": "armor #263238 dark charcoal, conduits #FFC107 orange, eyes #FF5722 red glow",
        "ref": "bosses/Stress Titan/Create_a_professional_2k_202602121755.jpeg",
    },
    "gym-bully": {
        "type": "boss",
        "desc": "intimidating muscular man with black pompadour hair and silver sunglasses, wearing dark grey tank top and grey pants with red wristbands",
        "colors": "tank #545454 dark grey, sunglasses #C0C0C0 silver, wristbands red",
        "ref": "bosses/Gym Bully/Create_a_professional_2k_202602121755 (1).jpeg",
    },
    "procrastination-phantom": {
        "type": "boss",
        "desc": "ethereal ghostly figure in white martial arts gi surrounded by pale blue mist and cyan aura",
        "colors": "mist #B3E5FC, gi #ECEFF1, aura #80DEEA cyan",
        "ref": "bosses/Procrastination Phantom/Create_a_professional_2k_202602121756 (1).jpeg",
    },
    "ultimate-slump": {
        "type": "boss",
        "desc": "heavy-set disheveled figure with messy dark hair, sunken blue-tinted eyes, wearing torn dark grey clothes",
        "colors": "body #8D6E63, clothes #545454 dark grey, eyes blue-tinted",
        "ref": "bosses/Ultimate Slump/Create_a_professional_2k_202602121757.jpeg",
    },
}

# ============================================================================
# POSE DEFINITIONS
# ============================================================================
# Each pose uses the 7-Layer Prompt Framework:
# Layer 1: Task Declaration
# Layer 2: Context Foundation (green screen)
# Layer 3: Style Definition (STYLE_CLUSTER)
# Layer 4: Compositional Layout (single character, facing right)
# Layer 5: Consistency Constraints (match reference)
# Layer 6: Technical Uniformity (lighting, shadows)
# Layer 7: Output Specs + Negatives

CHAMPION_POSES = [
    {
        "name": "fighting-stance",
        "action": "in a fighting stance with fists raised and weight on back foot, body slightly turned, facing right",
        "note": "This is the default battle pose — the idle animation anchor",
    },
    {
        "name": "kick-high",
        "action": "executing a high roundhouse kick with right leg extended horizontally at head height, arms pulled back for balance, facing right",
        "note": "Dynamic action pose — tests the LoRA on extended limbs",
    },
    {
        "name": "punch-jab",
        "action": "throwing a straight jab punch with right arm fully extended forward, left arm guarding chin, legs in lunge position, facing right",
        "note": "Forward-reaching pose — different silhouette from standing",
    },
    {
        "name": "block-stance",
        "action": "in a defensive block position with both arms raised to protect head and torso, knees slightly bent, facing right",
        "note": "Compact defensive pose — teaches the LoRA about guarding",
    },
]

BOSS_POSES = [
    {
        "name": "menacing-idle",
        "action": "standing in a menacing idle pose with fists clenched at sides, chest puffed out, looking directly at the viewer with an intimidating expression, facing right",
        "note": "Boss idle pose — larger, more imposing than champions",
    },
    {
        "name": "attack-windup",
        "action": "in an attack windup pose with one arm pulled far back ready to strike, weight shifting forward, expression fierce and aggressive, facing right",
        "note": "Boss attack anticipation — shows the character about to unleash",
    },
]


def build_prompt(character: dict, char_name: str, pose: dict) -> str:
    """
    Build a complete prompt using the 7-Layer Framework.

    This is the core prompt engineering logic. Each layer adds specificity
    to ensure Gemini generates exactly the right style, pose, and character.
    """
    tile_size = "128x128" if character["type"] == "champion" else "256x256"
    char_type = character["type"].capitalize()

    prompt = (
        # Layer 1: Task Declaration
        f"Create a single pixel art {char_type} sprite of {character['desc']}, "
        f"{pose['action']}. "
        # Layer 2: Context Foundation
        f"{BG_INSTRUCTION} "
        # Layer 3: Style Definition
        f"Match the {STYLE_CLUSTER}. "
        f"Use these exact character colors: {character['colors']}. "
        # Layer 4: Compositional Layout
        f"Show the full body of the character centered in the frame as a single sprite, "
        f"with the character taking up approximately 75-80% of the frame height. "
        f"Target canvas size is {tile_size} pixels. "
        # Layer 5: Consistency Constraints
        f"Maintain perfect consistency with the reference image provided. "
        f"Same character design, same outfit, same proportions, same pixel art style. "
        f"The character must be immediately recognizable as the same person from the reference. "
        # Layer 6: Technical Uniformity
        f"Consistent top-front lighting across the entire sprite. "
        f"Natural shadows that follow the character's form. "
        f"Bold dark outlines (#272929) at 2-3px weight defining every major form. "
        # Layer 7: Output Specs + Negatives
        f"{NEGATIVE_CONSTRAINTS}"
    )
    return prompt


def build_generation_plan() -> list:
    """Build the full list of images to generate."""
    plan = []

    for char_name, char_data in CHARACTERS.items():
        poses = CHAMPION_POSES if char_data["type"] == "champion" else BOSS_POSES

        for pose in poses:
            ref_path = REF_DIR / char_data["ref"]
            output_filename = f"{char_name}_{pose['name']}.png"
            prompt = build_prompt(char_data, char_name, pose)

            plan.append({
                "index": len(plan),
                "character": char_name,
                "pose": pose["name"],
                "prompt": prompt,
                "ref_path": str(ref_path),
                "output_path": str(OUTPUT_DIR / output_filename),
                "aspect_ratio": "1:1",
                "note": pose["note"],
            })

    return plan


def main():
    parser = argparse.ArgumentParser(description="Generate LoRA training images with Gemini")
    parser.add_argument("--list", action="store_true", help="List all prompts without generating")
    parser.add_argument("--run", action="store_true", help="Actually generate images")
    parser.add_argument("--character", type=str, help="Generate only for this character")
    parser.add_argument("--index", nargs="+", type=int, help="Generate only these prompt indices")
    parser.add_argument("--no-reference", action="store_true",
                        help="Don't use reference images (for testing)")
    parser.add_argument("--delay", type=float, default=3.0,
                        help="Seconds between API calls (default: 3.0, avoids rate limits)")
    args = parser.parse_args()

    plan = build_generation_plan()

    # Filter by character if specified
    if args.character:
        plan = [p for p in plan if p["character"] == args.character.lower()]
        if not plan:
            print(f"No prompts found for character: {args.character}")
            print(f"Available: {', '.join(CHARACTERS.keys())}")
            sys.exit(1)

    # Filter by index if specified
    if args.index:
        plan = [p for p in plan if p["index"] in args.index]

    print(f"{'='*60}")
    print(f"16BitFit Battle Mode — LoRA Dataset Generator")
    print(f"{'='*60}")
    print(f"Total images to generate: {len(plan)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    for item in plan:
        ref_exists = Path(item["ref_path"]).exists()
        ref_status = "OK" if ref_exists else "MISSING"

        print(f"[{item['index']:2d}] {item['character']} — {item['pose']}")
        print(f"     Reference: {ref_status} ({Path(item['ref_path']).name})")
        if args.list:
            print(f"     Note: {item['note']}")
            print(f"     Prompt: {item['prompt'][:150]}...")
        print()

    if args.list or not args.run:
        print(f"This was a listing only. Use --run to generate images.")
        print(f"\nExamples:")
        print(f"  python3 generate_dataset.py --run                    # Generate all {len(plan)} images")
        print(f"  python3 generate_dataset.py --run --character aria    # Generate only Aria's poses")
        print(f"  python3 generate_dataset.py --run --index 0 1 2      # Generate specific indices")
        return

    # === ACTUALLY GENERATE ===
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Import generate_image from local copy (lives alongside this script)
    from generate_image import generate_image

    successes = 0
    failures = 0

    for i, item in enumerate(plan):
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(plan)}] Generating: {item['character']} — {item['pose']}")
        print(f"{'='*60}")

        ref_images = None
        if not args.no_reference:
            ref_path = Path(item["ref_path"])
            if ref_path.exists():
                ref_images = [str(ref_path)]
            else:
                print(f"  WARNING: Reference image not found: {ref_path.name}")
                print(f"  Generating without reference (quality may vary)")

        try:
            generate_image(
                prompt=item["prompt"],
                output_path=item["output_path"],
                aspect_ratio=item["aspect_ratio"],
                reference_images=ref_images,
            )
            successes += 1
            print(f"  SUCCESS: {Path(item['output_path']).name}")
        except Exception as e:
            failures += 1
            print(f"  FAILED: {e}")

        # Rate limit delay between calls
        if i < len(plan) - 1:
            print(f"  Waiting {args.delay}s before next generation...")
            time.sleep(args.delay)

    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"  Successes: {successes}")
    print(f"  Failures:  {failures}")
    print(f"  Output:    {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
