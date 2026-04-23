#!/usr/bin/env python3
"""
Turnaround Sheet Slicer for LoRA Training Dataset
===================================================
Takes composite turnaround sheets (4 body views + 3 head close-ups) and
multi-frame action sheets, and slices them into individual training images.

Why this matters for LoRA training:
- LoRA learns from individual images, not composite sheets
- If you feed in the full sheet, the LoRA learns "turnaround sheet layout"
  instead of "16BitFit pixel art style"
- Slicing gives us 7 images from each turnaround sheet (4 body + 3 head)
- Multi-frame action sheets give us 4-8 individual pose images each

Usage:
    python3 slice_turnarounds.py                    # Dry run (shows what would be sliced)
    python3 slice_turnarounds.py --run              # Actually slice and save
    python3 slice_turnarounds.py --run --skip-heads  # Skip head close-ups (body poses only)
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image

# === CONFIGURATION ===

# Base paths
DATASET_DIR = Path(__file__).parent / "LoRA-Training-Dataset" / "Sprite Sheet Reference Images"
OUTPUT_DIR = Path(__file__).parent / "sliced-dataset"

# Turnaround sheet layout (2752x1536 images)
# Top row: 4 full-body views evenly spaced
# Bottom row: 3 head close-ups evenly spaced
# These ratios work for all the turnaround sheets in the dataset
TURNAROUND_LAYOUT = {
    "body_row": {
        "top_pct": 0.0,       # Top of body row
        "bottom_pct": 0.57,   # Body row takes ~57% of height
        "columns": 4,
        "labels": ["front", "side-left", "side-right", "back"],
        "padding_pct": 0.02,  # Trim 2% from edges of each cell
    },
    "head_row": {
        "top_pct": 0.60,      # Head row starts at ~60% (small gap avoids body bleed)
        "bottom_pct": 0.98,   # Trim bottom slightly to avoid edge artifacts
        "columns": 3,
        "labels": ["head-front", "head-side", "head-back"],
        "padding_pct": 0.03,  # Slightly more padding on heads for cleaner crops
    },
}

# Multi-frame action sheet layouts (1376x768 images)
# These have characters in a horizontal strip, typically 4 or 8 frames
MULTI_FRAME_LAYOUTS = {
    4: {"columns": 4, "rows": 1},   # 4 frames in a single row (jump animation)
    8: {"columns": 4, "rows": 2},   # 8 frames in 2 rows of 4 (roundhouse kick, light punch)
}


def classify_image(filepath: Path, img: Image.Image) -> str:
    """
    Classify an image by its type so we know how to slice it.

    Returns one of:
    - "turnaround"    : 7-panel turnaround sheet (4 body + 3 head)
    - "multi_frame_8" : 8-frame action sheet (2 rows x 4 cols)
    - "multi_frame_4" : 4-frame action sheet (1 row x 4 cols)
    - "single"        : Already a single character image (no slicing needed)
    - "skip"          : Not suitable for slicing
    """
    w, h = img.size
    name = filepath.name.lower()

    # Turnaround sheets: 2752x1536, named with "turnaround" or "Create_a_professional"
    if w == 2752 and h == 1536:
        if "turnaround" in name:
            return "turnaround"
        if "create_a_professional" in name:
            return "turnaround"
        # "facing-right" images and "Generate_a_single" are single characters
        if "facing-right" in name or "generate_a_single" in name:
            return "single"
        # Guard-up poses are single characters
        if "guard" in name:
            return "single"
        # facing-right-mary.jpeg is also single
        return "single"

    # Multi-frame action sheets: 1376x768
    if w == 1376 and h == 768:
        if "roundhouse" in name or "light_punch" in name:
            return "multi_frame_8"
        if "jump" in name:
            return "multi_frame_4"
        # Fighting stance images are single characters
        if "fighting" in name:
            return "single"
        return "single"

    # Small images (512x512, etc.) are already individual
    if w <= 1024 and h <= 1024:
        return "single"

    # Walk cycle reference - special case, skip for now
    if "walk-cycle" in name.lower():
        return "skip"

    return "skip"


def slice_turnaround(img: Image.Image, character_name: str, output_dir: Path,
                     skip_heads: bool = False) -> list:
    """Slice a turnaround sheet into individual body views and head close-ups."""
    w, h = img.size
    results = []

    for row_name, row_config in TURNAROUND_LAYOUT.items():
        if skip_heads and row_name == "head_row":
            continue

        top = int(h * row_config["top_pct"])
        bottom = int(h * row_config["bottom_pct"])
        cols = row_config["columns"]
        col_width = w // cols
        padding = int(col_width * row_config["padding_pct"])

        for i, label in enumerate(row_config["labels"]):
            left = i * col_width + padding
            right = (i + 1) * col_width - padding
            top_padded = top + padding
            bottom_padded = bottom - padding

            cell = img.crop((left, top_padded, right, bottom_padded))

            filename = f"{character_name}_{label}.png"
            out_path = output_dir / filename
            cell.save(out_path, "PNG")
            results.append(out_path)

    return results


def slice_multi_frame(img: Image.Image, character_name: str, action_name: str,
                      num_frames: int, output_dir: Path) -> list:
    """Slice a multi-frame action sheet into individual pose images."""
    w, h = img.size
    layout = MULTI_FRAME_LAYOUTS[num_frames]
    cols = layout["columns"]
    rows = layout["rows"]

    cell_w = w // cols
    cell_h = h // rows
    padding = int(min(cell_w, cell_h) * 0.02)

    results = []
    frame_num = 0

    for row in range(rows):
        for col in range(cols):
            left = col * cell_w + padding
            top = row * cell_h + padding
            right = (col + 1) * cell_w - padding
            bottom = (row + 1) * cell_h - padding

            cell = img.crop((left, top, right, bottom))

            filename = f"{character_name}_{action_name}_frame{frame_num:02d}.png"
            out_path = output_dir / filename
            cell.save(out_path, "PNG")
            results.append(out_path)
            frame_num += 1

    return results


def get_character_name(filepath: Path) -> str:
    """Extract a clean character name from the file path."""
    # Use the parent directory name as the character name
    parent = filepath.parent.name.lower().replace(" ", "-")
    return parent


def get_action_name(filepath: Path) -> str:
    """Extract action name from filename."""
    name = filepath.stem.lower()
    if "roundhouse" in name:
        return "roundhouse-kick"
    if "light_punch" in name or "punch" in name:
        return "light-punch"
    if "jump" in name:
        return "jump"
    if "fighting" in name:
        return "fighting-stance"
    return "action"


def main():
    parser = argparse.ArgumentParser(description="Slice turnaround sheets for LoRA training")
    parser.add_argument("--run", action="store_true", help="Actually slice (default: dry run)")
    parser.add_argument("--skip-heads", action="store_true", help="Skip head close-up crops")
    args = parser.parse_args()

    if not DATASET_DIR.exists():
        print(f"ERROR: Dataset directory not found: {DATASET_DIR}")
        sys.exit(1)

    # Collect all images
    images = []
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        images.extend(DATASET_DIR.rglob(ext))
    images = sorted(images)

    print(f"Found {len(images)} images in dataset\n")

    # Classify and plan
    plan = {"turnaround": [], "multi_frame_8": [], "multi_frame_4": [], "single": [], "skip": []}

    for img_path in images:
        if img_path.name.startswith("."):
            continue
        img = Image.open(img_path)
        img_type = classify_image(img_path, img)
        plan[img_type].append((img_path, img.size))
        img.close()

    # Report
    print("=== CLASSIFICATION REPORT ===\n")

    total_sliced = 0

    print(f"TURNAROUND SHEETS ({len(plan['turnaround'])}) → 7 crops each:")
    for path, size in plan["turnaround"]:
        n = 4 if args.skip_heads else 7
        print(f"  {path.relative_to(DATASET_DIR)} ({size[0]}x{size[1]}) → {n} individual images")
        total_sliced += n

    print(f"\n8-FRAME ACTION SHEETS ({len(plan['multi_frame_8'])}) → 8 crops each:")
    for path, size in plan["multi_frame_8"]:
        print(f"  {path.relative_to(DATASET_DIR)} ({size[0]}x{size[1]}) → 8 individual images")
        total_sliced += 8

    print(f"\n4-FRAME ACTION SHEETS ({len(plan['multi_frame_4'])}) → 4 crops each:")
    for path, size in plan["multi_frame_4"]:
        print(f"  {path.relative_to(DATASET_DIR)} ({size[0]}x{size[1]}) → 4 individual images")
        total_sliced += 4

    print(f"\nSINGLE CHARACTER IMAGES ({len(plan['single'])}) → copy as-is:")
    for path, size in plan["single"]:
        print(f"  {path.relative_to(DATASET_DIR)} ({size[0]}x{size[1]})")
        total_sliced += 1

    if plan["skip"]:
        print(f"\nSKIPPED ({len(plan['skip'])}):")
        for path, size in plan["skip"]:
            print(f"  {path.relative_to(DATASET_DIR)} ({size[0]}x{size[1]})")

    print(f"\n{'='*50}")
    print(f"TOTAL OUTPUT IMAGES: {total_sliced}")
    print(f"{'='*50}")

    if not args.run:
        print(f"\nThis was a DRY RUN. Use --run to actually slice and save to:\n  {OUTPUT_DIR}")
        return

    # Actually slice
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_outputs = []

    # Slice turnaround sheets
    for img_path, _ in plan["turnaround"]:
        img = Image.open(img_path)
        char_name = get_character_name(img_path)

        # Disambiguate if multiple turnarounds for same character
        stem = img_path.stem.lower()
        if "create_a_professional" in stem:
            char_name = f"{char_name}-turnaround"

        results = slice_turnaround(img, char_name, OUTPUT_DIR, args.skip_heads)
        all_outputs.extend(results)
        print(f"Sliced {img_path.name} → {len(results)} images")
        img.close()

    # Slice multi-frame sheets
    for img_path, _ in plan["multi_frame_8"]:
        img = Image.open(img_path)
        char_name = get_character_name(img_path)
        action_name = get_action_name(img_path)
        results = slice_multi_frame(img, char_name, action_name, 8, OUTPUT_DIR)
        all_outputs.extend(results)
        print(f"Sliced {img_path.name} → {len(results)} images")
        img.close()

    for img_path, _ in plan["multi_frame_4"]:
        img = Image.open(img_path)
        char_name = get_character_name(img_path)
        action_name = get_action_name(img_path)
        results = slice_multi_frame(img, char_name, action_name, 4, OUTPUT_DIR)
        all_outputs.extend(results)
        print(f"Sliced {img_path.name} → {len(results)} images")
        img.close()

    # Copy single images
    for img_path, _ in plan["single"]:
        img = Image.open(img_path)
        char_name = get_character_name(img_path)
        stem = img_path.stem.lower().replace(" ", "-")

        # Clean up filename
        if "generate_a_single" in stem:
            filename = f"{char_name}-idle-green.png"
        elif "facing-right" in stem:
            filename = f"{char_name}-facing-right.png"
        elif "guard" in stem:
            filename = f"{char_name}-guard-up.png"
        elif "fighting" in stem:
            filename = f"{char_name}-fighting-stance.png"
        else:
            filename = f"{char_name}-{stem}.png"

        # Avoid duplicate filenames
        out_path = OUTPUT_DIR / filename
        counter = 1
        while out_path.exists():
            name_no_ext = filename.rsplit(".", 1)[0]
            out_path = OUTPUT_DIR / f"{name_no_ext}-{counter}.png"
            counter += 1

        img.save(out_path, "PNG")
        all_outputs.append(out_path)
        print(f"Copied {img_path.name} → {out_path.name}")
        img.close()

    print(f"\n{'='*50}")
    print(f"DONE: {len(all_outputs)} images saved to {OUTPUT_DIR}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
