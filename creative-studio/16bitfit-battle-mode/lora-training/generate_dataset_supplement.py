#!/usr/bin/env python3
"""
LoRA Training Dataset Generator — SUPPLEMENT (15 additional images)
====================================================================
Generates 15 more training images to bring the total dataset to ~51.
These use NEW poses not in the original 36 (crouch, uppercut, jump,
getting hit, victory) to give the LoRA more pose diversity.

Each image uses the best available reference image for identity locking:
- "facing-right" single sprites where available (cleaner reference)
- Turnaround sheets as fallback

Usage:
    python3 generate_dataset_supplement.py --list          # Show all prompts
    python3 generate_dataset_supplement.py --run           # Generate all 15
    python3 generate_dataset_supplement.py --run --index 0 3 5  # Specific indices

Prerequisites:
    pip install google-genai
    GEMINI_API_KEY in environment or .env file
"""

import argparse
import sys
import os
import time
from pathlib import Path

# Output directory (same as main script — all images land together)
OUTPUT_DIR = Path(__file__).parent / "generated-dataset"

# Reference images directory
REF_DIR = Path(__file__).parent / "LoRA-Training-Dataset" / "Sprite Sheet Reference Images"

# ============================================================================
# STYLE FOUNDATION (same as main script for consistency)
# ============================================================================

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
# SUPPLEMENT IMAGE PLAN — 15 images with NEW poses
# ============================================================================
# Each entry has: character info, pose, and the best reference image to use.
# We pick the "facing-right" single sprite where available because it gives
# Gemini a cleaner single-character reference vs the multi-view turnaround sheet.

SUPPLEMENT_PLAN = [
    # --- CHAMPIONS: New poses (crouch, uppercut, jump, getting hit, victory) ---
    {
        "index": 0,
        "character": "sean",
        "type": "champion",
        "desc": "muscular blonde man with spiky hair, blue eyes, wearing white tank top and blue pants with white sneakers",
        "colors": "skin #F5D6C6, hair #C2A769, eyes #4682B4, white #F2F0EF tank top, blue #2323FF pants",
        "ref": "champions/Sean/Champion-Guard-Up-Facing-Right-Green-Sean.png",
        "pose_name": "crouch-duck",
        "action": "in a low crouching position ducking under an attack, knees deeply bent, torso leaning forward, arms protecting head, facing right",
        "note": "Low crouch — teaches compact body silhouette",
    },
    {
        "index": 1,
        "character": "sean",
        "type": "champion",
        "desc": "muscular blonde man with spiky hair, blue eyes, wearing white tank top and blue pants with white sneakers",
        "colors": "skin #F5D6C6, hair #C2A769, eyes #4682B4, white #F2F0EF tank top, blue #2323FF pants",
        "ref": "champions/Sean/Champion-Guard-Up-Facing-Right-Green-Sean.png",
        "pose_name": "jump-airborne",
        "action": "mid-jump airborne with both feet off the ground, knees tucked up, fists raised overhead ready to strike downward, facing right",
        "note": "Airborne — teaches full body off ground plane",
    },
    {
        "index": 2,
        "character": "aria",
        "type": "champion",
        "desc": "athletic woman with brown skin and dark brown hair in a high ponytail, wearing magenta crop top and blue-grey pants",
        "colors": "skin #C68642, hair #4B3621, eyes #06402B, magenta #9A2257 top, blue-grey #5577AA pants",
        "ref": "champions/Aria/facing-right-aria.png",
        "pose_name": "uppercut",
        "action": "throwing a rising uppercut with right fist driving upward from below, body rising on toes, left arm pulled back, facing right",
        "note": "Vertical attack — extends body upward, different silhouette",
    },
    {
        "index": 3,
        "character": "aria",
        "type": "champion",
        "desc": "athletic woman with brown skin and dark brown hair in a high ponytail, wearing magenta crop top and blue-grey pants",
        "colors": "skin #C68642, hair #4B3621, eyes #06402B, magenta #9A2257 top, blue-grey #5577AA pants",
        "ref": "champions/Aria/facing-right-aria.png",
        "pose_name": "getting-hit",
        "action": "recoiling backward from being hit in the torso, upper body arching back, face showing pain, arms thrown to the sides, one foot lifted off ground, facing right",
        "note": "Damage reaction — asymmetric off-balance pose",
    },
    {
        "index": 4,
        "character": "kenji",
        "type": "champion",
        "desc": "lean Japanese man with black hair in a bun, wearing light grey gi top with dark grey belt and dark pants",
        "colors": "skin #FFDBAC, hair #212121, eyes #4A4A4A, light grey #B0BEC5 gi top, dark #424242 pants",
        "ref": "champions/Kenji/facing-right-kenji.png",
        "pose_name": "crouch-duck",
        "action": "in a low crouching position with one leg extended forward in a sweep stance, torso low to the ground, arms in guard position, facing right",
        "note": "Low sweep crouch — different character same pose type as Sean's crouch",
    },
    {
        "index": 5,
        "character": "kenji",
        "type": "champion",
        "desc": "lean Japanese man with black hair in a bun, wearing light grey gi top with dark grey belt and dark pants",
        "colors": "skin #FFDBAC, hair #212121, eyes #4A4A4A, light grey #B0BEC5 gi top, dark #424242 pants",
        "ref": "champions/Kenji/facing-right-kenji.png",
        "pose_name": "jump-airborne",
        "action": "mid-jump airborne performing a flying kick with right leg extended forward and left leg tucked back, arms in martial arts guard, facing right",
        "note": "Flying kick — full body airborne in extended pose",
    },
    {
        "index": 6,
        "character": "marcus",
        "type": "champion",
        "desc": "muscular Black man with short black hair and glasses, wearing dark grey tank top and light grey pants with yellow boxing gloves",
        "colors": "skin #8D5524, hair #212121, eyes #4A4A4A, dark grey #545454 tank, yellow #FFD700 gloves",
        "ref": "champions/Marcus/facing-right-marcus.png",
        "pose_name": "uppercut",
        "action": "throwing a powerful uppercut with left yellow boxing glove driving upward, body rotating into the punch, right glove guarding chin, legs in wide power stance, facing right",
        "note": "Boxing uppercut — showcases yellow gloves prominently",
    },
    {
        "index": 7,
        "character": "marcus",
        "type": "champion",
        "desc": "muscular Black man with short black hair and glasses, wearing dark grey tank top and light grey pants with yellow boxing gloves",
        "colors": "skin #8D5524, hair #212121, eyes #4A4A4A, dark grey #545454 tank, yellow #FFD700 gloves",
        "ref": "champions/Marcus/facing-right-marcus.png",
        "pose_name": "victory-pose",
        "action": "standing tall in a victory pose with both yellow boxing gloves raised above head triumphantly, chest puffed out, confident expression, feet planted wide, facing right",
        "note": "Victory celebration — upright proud pose, arms overhead",
    },
    {
        "index": 8,
        "character": "mary",
        "type": "champion",
        "desc": "fit woman with brown hair in a ponytail with purple headband, wearing pink crop top and purple shorts with white sneakers",
        "colors": "skin #F5D6C6, hair #6D4C41, eyes #654321, pink #FF7BAC top, purple #7E57C2 shorts",
        "ref": "champions/Mary/facing-right-mary.png",
        "pose_name": "jump-airborne",
        "action": "mid-jump airborne with a spinning kick, body horizontal in the air, right leg extended in a flying roundhouse, hair and ponytail flowing with momentum, facing right",
        "note": "Aerial spinning kick — dynamic airborne pose",
    },
    {
        "index": 9,
        "character": "zara",
        "type": "champion",
        "desc": "strong woman with olive skin and dark dreadlocks, wearing dark grey tank top and black pants with white sneakers",
        "colors": "skin #CBB59D, hair #3B2F2F, eyes #654321, dark grey #545454 tank, black #212121 pants",
        "ref": "champions/Zara/facing-right-zara.png",
        "pose_name": "getting-hit",
        "action": "stumbling backward from a hit to the face, head snapped to the side, body leaning back off-balance, one arm reaching out for balance, expression of pain, facing right",
        "note": "Hit reaction — teaches asymmetric damage pose on different body type",
    },

    # --- BOSSES: New poses (ground slam, charge, energy attack, taunt, stomp) ---
    {
        "index": 10,
        "character": "training-dummy",
        "type": "boss",
        "desc": "wooden training dummy with grey padding and metal joints, humanoid robot-like appearance",
        "colors": "wood #8B5A2B body, padding #A9A9A9, joints #696969 metal",
        "ref": "bosses/Training Dummy/Create_a_professional_2k_202602121754.jpeg",
        "pose_name": "ground-slam",
        "action": "slamming both fists down into the ground with tremendous force, body bent forward at the waist, arms fully extended downward, impact cracks radiating from fists on the ground, facing right",
        "note": "Ground slam — boss attack with downward force",
    },
    {
        "index": 11,
        "character": "sloth-demon",
        "type": "boss",
        "desc": "large menacing sloth creature with brown fur, glowing amber eyes, wearing steel-blue armor plates",
        "colors": "fur #8D6E63, eyes #FFCC80 amber glow, armor #90A4AE steel-blue",
        "ref": "bosses/Sloth Demon/Create_a_professional_2k_202602121756.jpeg",
        "pose_name": "charging-forward",
        "action": "charging forward in a bull rush with head lowered, shoulder leading, massive arms swept back behind the body building momentum, amber eyes glowing intensely, facing right",
        "note": "Charge attack — horizontal momentum pose",
    },
    {
        "index": 12,
        "character": "stress-titan",
        "type": "boss",
        "desc": "massive armored humanoid with grey-white skin, glowing red eyes, dark charcoal armor with orange energy conduits",
        "colors": "armor #263238 dark charcoal, conduits #FFC107 orange, eyes #FF5722 red glow",
        "ref": "bosses/Stress Titan/Create_a_professional_2k_202602121755.jpeg",
        "pose_name": "energy-blast",
        "action": "firing an energy blast from both outstretched hands, orange energy conduits on armor glowing brightly, legs planted in wide power stance, red eyes blazing, beam of orange energy shooting forward from palms, facing right",
        "note": "Ranged attack — energy effects test the LoRA on special FX",
    },
    {
        "index": 13,
        "character": "gym-bully",
        "type": "boss",
        "desc": "intimidating muscular man with black pompadour hair and silver sunglasses, wearing dark grey tank top and grey pants with red wristbands",
        "colors": "tank #545454 dark grey, sunglasses #C0C0C0 silver, wristbands red",
        "ref": "bosses/Gym Bully/Create_a_professional_2k_202602121755 (1).jpeg",
        "pose_name": "flexing-taunt",
        "action": "flexing both biceps in a taunting double bicep pose, chest puffed way out, smirking arrogantly, sunglasses gleaming, legs planted wide in a power stance, facing right",
        "note": "Taunt pose — arrogant personality expressed through pose",
    },
    {
        "index": 14,
        "character": "procrastination-phantom",
        "type": "boss",
        "desc": "ethereal ghostly figure in white martial arts gi surrounded by pale blue mist and cyan aura",
        "colors": "mist #B3E5FC, gi #ECEFF1, aura #80DEEA cyan",
        "ref": "bosses/Procrastination Phantom/Create_a_professional_2k_202602121756 (1).jpeg",
        "pose_name": "vanishing-dodge",
        "action": "mid-teleport dodge with body partially transparent and fading, trails of cyan mist behind the movement path, ghostly afterimage visible, one arm reaching forward through the fade, facing right",
        "note": "Ethereal dodge — tests LoRA on transparency/ghost effects",
    },
]


def build_prompt(item: dict) -> str:
    """Build a complete prompt using the 7-Layer Framework."""
    tile_size = "128x128" if item["type"] == "champion" else "256x256"
    char_type = item["type"].capitalize()

    prompt = (
        # Layer 1: Task Declaration
        f"Create a single pixel art {char_type} sprite of {item['desc']}, "
        f"{item['action']}. "
        # Layer 2: Context Foundation
        f"{BG_INSTRUCTION} "
        # Layer 3: Style Definition
        f"Match the {STYLE_CLUSTER}. "
        f"Use these exact character colors: {item['colors']}. "
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


def main():
    parser = argparse.ArgumentParser(description="Generate 15 supplemental LoRA training images")
    parser.add_argument("--list", action="store_true", help="List all prompts without generating")
    parser.add_argument("--run", action="store_true", help="Actually generate images")
    parser.add_argument("--index", nargs="+", type=int, help="Generate only these prompt indices")
    parser.add_argument("--no-reference", action="store_true",
                        help="Don't use reference images (for testing)")
    parser.add_argument("--delay", type=float, default=4.0,
                        help="Seconds between API calls (default: 4.0)")
    args = parser.parse_args()

    plan = SUPPLEMENT_PLAN[:]

    # Filter by index if specified
    if args.index:
        plan = [p for p in plan if p["index"] in args.index]

    print(f"{'='*60}")
    print(f"16BitFit Battle Mode — SUPPLEMENT Dataset Generator")
    print(f"{'='*60}")
    print(f"Total images to generate: {len(plan)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*60}\n")

    for item in plan:
        ref_path = REF_DIR / item["ref"]
        ref_exists = ref_path.exists()
        ref_status = "OK" if ref_exists else "MISSING"

        print(f"[{item['index']:2d}] {item['character']} — {item['pose_name']}")
        print(f"     Reference: {ref_status} ({Path(item['ref']).name})")
        if args.list:
            print(f"     Note: {item['note']}")
            prompt = build_prompt(item)
            print(f"     Prompt: {prompt[:150]}...")
        print()

    if args.list or not args.run:
        print(f"This was a listing only. Use --run to generate images.")
        print(f"\nExamples:")
        print(f"  python3 generate_dataset_supplement.py --run             # Generate all {len(plan)}")
        print(f"  python3 generate_dataset_supplement.py --run --index 0 1 # Specific indices")
        return

    # === ACTUALLY GENERATE ===
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    from generate_image import generate_image

    successes = 0
    failures = 0

    for i, item in enumerate(plan):
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(plan)}] Generating: {item['character']} — {item['pose_name']}")
        print(f"{'='*60}")

        ref_images = None
        if not args.no_reference:
            ref_path = REF_DIR / item["ref"]
            if ref_path.exists():
                ref_images = [str(ref_path)]
            else:
                print(f"  WARNING: Reference image not found: {ref_path.name}")
                print(f"  Generating without reference (quality may vary)")

        prompt = build_prompt(item)

        try:
            output_filename = f"{item['character']}_{item['pose_name']}.png"
            generate_image(
                prompt=prompt,
                output_path=str(OUTPUT_DIR / output_filename),
                aspect_ratio="1:1",
                reference_images=ref_images,
            )
            successes += 1
            print(f"  SUCCESS: {output_filename}")
        except Exception as e:
            failures += 1
            print(f"  FAILED: {e}")

        # Rate limit delay between calls
        if i < len(plan) - 1:
            print(f"  Waiting {args.delay}s before next generation...")
            time.sleep(args.delay)

    print(f"\n{'='*60}")
    print(f"SUPPLEMENT GENERATION COMPLETE")
    print(f"  Successes: {successes}")
    print(f"  Failures:  {failures}")
    print(f"  Output:    {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
