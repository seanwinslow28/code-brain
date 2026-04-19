"""Generate animation frames via sprite sheet → split approach.

Instead of making individual API calls per frame (which loses character
consistency), this generates all frames for one animation as a single
sprite sheet image, then splits it into individual frame PNGs.

This leverages the within-image consistency that proved strong in the
Phase 5A sprite sheet test (12/12 characters passed).

Usage:
    python3 batch/generate_sheet_split.py manifests/champion_sean.json idle
    python3 batch/generate_sheet_split.py manifests/champion_sean.json light_punch
    python3 batch/generate_sheet_split.py manifests/champion_sean.json idle --approach sequential
    python3 batch/generate_sheet_split.py manifests/champion_sean.json idle --approach reinforced
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import math
import sys
import time
from io import BytesIO
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PIXEL_QUANTIZER_DIR = SCRIPT_DIR.parent
VIDEO_EVAL_DIR = PIXEL_QUANTIZER_DIR / "video-eval"
REPO_ROOT = PIXEL_QUANTIZER_DIR.parent.parent.parent  # post-v3.15.0: 16bitfit nested under creative-studio/

sys.path.insert(0, str(PIXEL_QUANTIZER_DIR))
sys.path.insert(0, str(VIDEO_EVAL_DIR))
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))

from prompts.prompt_library import (
    FACING,
    GREEN_SCREEN,
    NEGATIVE_PROMPT,
    STYLE_TOKENS,
    PromptLibrary,
)


def get_grid_layout(frame_count: int) -> tuple[int, int]:
    """Determine grid layout (cols x rows) for a given frame count."""
    if frame_count <= 2:
        return (frame_count, 1)
    elif frame_count <= 4:
        return (2, 2)
    elif frame_count <= 6:
        return (3, 2)
    elif frame_count <= 8:
        return (4, 2)
    elif frame_count <= 9:
        return (3, 3)
    elif frame_count <= 12:
        return (4, 3)
    else:
        cols = math.ceil(math.sqrt(frame_count))
        rows = math.ceil(frame_count / cols)
        return (cols, rows)


def build_sheet_prompt(
    animation_type: str,
    char_config: dict,
    frame_poses: list[str],
    cols: int,
    rows: int,
) -> str:
    """Build a sprite sheet prompt that requests all frames in a grid."""
    tile_size = char_config.get("tile_size", 128)
    description = char_config.get("description", char_config["name"])
    frame_count = len(frame_poses)

    # Build pose list
    pose_lines = []
    for i, pose in enumerate(frame_poses):
        row_idx = i // cols + 1
        col_idx = i % cols + 1
        pose_lines.append(f"({i + 1}) Row {row_idx}, Column {col_idx}: {pose}")

    pose_text = "\n".join(pose_lines)

    return (
        f"Generate a pixel art sprite sheet of THIS EXACT CHARACTER from the reference images. "
        f"The sprite sheet must show {frame_count} frames of the '{animation_type}' animation, "
        f"arranged in a {cols}x{rows} grid (columns x rows). "
        f"Each cell is {tile_size}x{tile_size} pixels. "
        f"\n\n"
        f"Frames in order:\n{pose_text}\n\n"
        f"MATCH THE CHARACTER EXACTLY: {description}. "
        f"Same hair, clothing, body type, and color palette as the reference images. "
        f"Style: {STYLE_TOKENS}. "
        f"Background: {GREEN_SCREEN} for each cell. "
        f"Character {FACING} in every frame. "
        f"No {NEGATIVE_PROMPT}."
    )


def build_sequential_prompt(
    animation_type: str,
    char_config: dict,
    frame_pose: str,
    frame_index: int,
    total_frames: int,
) -> str:
    """Build a per-frame prompt with enhanced character reinforcement."""
    tile_size = char_config.get("tile_size", 128)
    description = char_config.get("description", char_config["name"])

    return (
        f"Generate a {tile_size}x{tile_size} pixel art sprite of THIS EXACT CHARACTER "
        f"from the reference images. "
        f"MATCH THE CHARACTER EXACTLY: {description}. "
        f"Same hair, clothing, body type, and color palette as the reference. "
        f"\n"
        f"Animation: {animation_type}, frame {frame_index + 1} of {total_frames}. "
        f"Pose: {frame_pose}. "
        f"Style: {STYLE_TOKENS}. "
        f"Background: {GREEN_SCREEN}. "
        f"Character {FACING}. "
        f"\n"
        f"CRITICAL: This character has {description}. Do NOT change the character's appearance "
        f"from the reference images. The character must look IDENTICAL across all frames. "
        f"No {NEGATIVE_PROMPT}."
    )


async def call_gemini(
    anchor_parts: list[dict],
    prompt: str,
    api_key: str,
    prev_frame_parts: list[dict] | None = None,
) -> bytes:
    """Call Gemini API with anchors + prompt, return image bytes."""
    import httpx

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent"

    # Build parts: anchors + optional previous frame + prompt text
    parts = list(anchor_parts)
    if prev_frame_parts:
        parts.extend(prev_frame_parts)
    parts.append({"text": prompt})

    max_retries = 3
    backoff = [5, 15, 30]

    for attempt in range(max_retries + 1):
        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                resp = await client.post(
                    url,
                    params={"key": api_key},
                    json={
                        "contents": [{"parts": parts}],
                        "generationConfig": {
                            "responseModalities": ["IMAGE", "TEXT"],
                        },
                    },
                )

                if resp.status_code in (503, 429):
                    wait = backoff[min(attempt, len(backoff) - 1)]
                    print(f"    Gemini {resp.status_code}, retrying in {wait}s ({attempt + 1}/{max_retries + 1})")
                    await asyncio.sleep(wait)
                    continue

                resp.raise_for_status()
                data = resp.json()

                for candidate in data.get("candidates", []):
                    for part in candidate.get("content", {}).get("parts", []):
                        if "inlineData" in part:
                            return base64.b64decode(part["inlineData"]["data"])

                raise RuntimeError("No image in Gemini response")

        except Exception as e:
            if attempt < max_retries:
                wait = backoff[min(attempt, len(backoff) - 1)]
                print(f"    Error: {e}, retrying in {wait}s")
                await asyncio.sleep(wait)
            else:
                raise


def detect_grid(image_data: bytes, requested_frames: int) -> tuple[int, int]:
    """Auto-detect grid layout from image dimensions.

    Gemini often generates more cells than requested (e.g., 4x2=8 for 4 requested).
    Detect the actual grid by checking cell aspect ratios and penalizing grids
    that have far more cells than requested.
    """
    from PIL import Image

    img = Image.open(BytesIO(image_data))
    w, h = img.width, img.height

    # First, try the requested grid layout (from get_grid_layout).
    # This is what we ASKED Gemini to produce, so it's the best default.
    expected_cols, expected_rows = get_grid_layout(requested_frames)

    candidates = []
    for cols in range(1, 8):
        for rows in range(1, 5):
            total_cells = cols * rows
            if total_cells < requested_frames:
                continue
            cell_w = w / cols
            cell_h = h / rows

            # Strongly prefer the exact grid layout we requested from Gemini
            if cols == expected_cols and rows == expected_rows:
                layout_penalty = 0.0
            elif total_cells == requested_frames:
                # Right number of cells but different arrangement
                layout_penalty = 0.3
            else:
                # Excess cells — almost certainly a wrong grid
                excess = total_cells - requested_frames
                layout_penalty = 1.0 + excess * 0.5

            # Mild preference for cells closer to square (tiebreaker only)
            cell_aspect = cell_w / cell_h
            aspect_penalty = abs(cell_aspect - 1.0) * 0.1

            # Penalize tiny cells (likely over-subdivided)
            min_cell_dim = min(cell_w, cell_h)
            size_penalty = 0.5 if min_cell_dim < 100 else 0.0

            score = layout_penalty + aspect_penalty + size_penalty
            candidates.append((score, cols, rows))

    if candidates:
        candidates.sort()
        _, best_cols, best_rows = candidates[0]
        return best_cols, best_rows

    return get_grid_layout(requested_frames)


def split_sheet(image_data: bytes, cols: int, rows: int, total_frames: int) -> list[bytes]:
    """Split a sprite sheet into individual frame PNGs."""
    from PIL import Image

    img = Image.open(BytesIO(image_data))
    cell_w = img.width // cols
    cell_h = img.height // rows

    frames = []
    for i in range(total_frames):
        row = i // cols
        col = i % cols
        x0 = col * cell_w
        y0 = row * cell_h
        cell = img.crop((x0, y0, x0 + cell_w, y0 + cell_h))

        buf = BytesIO()
        cell.save(buf, format="PNG")
        frames.append(buf.getvalue())

    return frames


def load_anchors(anchor_paths: list[str]) -> list[dict]:
    """Load anchor images as Gemini inlineData parts."""
    parts = []
    for img_path in anchor_paths:
        p = Path(img_path)
        if not p.exists():
            p = REPO_ROOT / img_path
        if not p.exists():
            print(f"    WARNING: Anchor not found: {img_path}")
            continue
        img_b64 = base64.b64encode(p.read_bytes()).decode()
        suffix = p.suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        parts.append({"inlineData": {"mimeType": mime, "data": img_b64}})
    return parts


async def approach_sheet(
    manifest: dict,
    animation_type: str,
    output_dir: Path,
    anchor_parts: list[dict],
    api_key: str,
) -> list[Path]:
    """Approach B: Generate sprite sheet → split into frames."""
    prompt_lib = PromptLibrary()
    template = prompt_lib.get_template(animation_type)
    frame_poses = template.frame_poses
    frame_count = template.frame_count

    cols, rows = get_grid_layout(frame_count)
    char_config = {
        "name": manifest["name"],
        "description": manifest["description"],
        "tile_size": manifest["tile_size"],
    }

    prompt = build_sheet_prompt(animation_type, char_config, frame_poses, cols, rows)
    print(f"  Generating {cols}x{rows} sprite sheet for {animation_type} ({frame_count} frames)...")
    print(f"  Prompt: {prompt[:120]}...")

    start = time.monotonic()
    image_data = await call_gemini(anchor_parts, prompt, api_key)
    duration = time.monotonic() - start
    print(f"  Sheet generated in {duration:.1f}s")

    # Save the full sheet for inspection
    sheet_path = output_dir / f"{animation_type}_sheet.png"
    sheet_path.write_bytes(image_data)
    print(f"  Sheet saved: {sheet_path}")

    # Auto-detect actual grid (Gemini may produce more cells than requested)
    actual_cols, actual_rows = detect_grid(image_data, frame_count)
    if (actual_cols, actual_rows) != (cols, rows):
        print(f"  Grid auto-corrected: requested {cols}x{rows}, detected {actual_cols}x{actual_rows}")
        cols, rows = actual_cols, actual_rows

    # Split into individual frames
    frames = split_sheet(image_data, cols, rows, frame_count)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = []
    for i, frame_data in enumerate(frames):
        frame_path = output_dir / f"frame_{i:02d}.png"
        frame_path.write_bytes(frame_data)
        saved.append(frame_path)
        print(f"    Frame {i}: {frame_path}")

    return saved


async def approach_sequential(
    manifest: dict,
    animation_type: str,
    output_dir: Path,
    anchor_parts: list[dict],
    api_key: str,
) -> list[Path]:
    """Approach B (sequential conditioning): each frame sees previous frame."""
    prompt_lib = PromptLibrary()
    template = prompt_lib.get_template(animation_type)
    frame_poses = template.frame_poses
    frame_count = template.frame_count

    char_config = {
        "name": manifest["name"],
        "description": manifest["description"],
        "tile_size": manifest["tile_size"],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    prev_frame_parts = None

    for i in range(frame_count):
        pose = frame_poses[i] if i < len(frame_poses) else frame_poses[-1]
        prompt = build_sequential_prompt(
            animation_type, char_config, pose, i, frame_count
        )
        if prev_frame_parts:
            prompt = (
                f"Here is the PREVIOUS frame of this animation. Generate the NEXT frame "
                f"maintaining the EXACT same character appearance. " + prompt
            )

        print(f"  Frame {i + 1}/{frame_count}: {pose[:60]}...")
        start = time.monotonic()
        image_data = await call_gemini(anchor_parts, prompt, api_key, prev_frame_parts)
        duration = time.monotonic() - start
        print(f"    Generated in {duration:.1f}s")

        frame_path = output_dir / f"frame_{i:02d}.png"
        frame_path.write_bytes(image_data)
        saved.append(frame_path)

        # Prepare previous frame for next iteration
        img_b64 = base64.b64encode(image_data).decode()
        prev_frame_parts = [
            {"inlineData": {"mimeType": "image/png", "data": img_b64}},
            {"text": "This is the previous animation frame. The next frame must show the EXACT SAME CHARACTER."},
        ]

    return saved


async def approach_reinforced(
    manifest: dict,
    animation_type: str,
    output_dir: Path,
    anchor_parts: list[dict],
    api_key: str,
) -> list[Path]:
    """Approach C: Enhanced prompt reinforcement (character desc repeated)."""
    prompt_lib = PromptLibrary()
    template = prompt_lib.get_template(animation_type)
    frame_poses = template.frame_poses
    frame_count = template.frame_count

    char_config = {
        "name": manifest["name"],
        "description": manifest["description"],
        "tile_size": manifest["tile_size"],
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []

    for i in range(frame_count):
        pose = frame_poses[i] if i < len(frame_poses) else frame_poses[-1]
        prompt = build_sequential_prompt(
            animation_type, char_config, pose, i, frame_count
        )

        print(f"  Frame {i + 1}/{frame_count}: {pose[:60]}...")
        start = time.monotonic()
        image_data = await call_gemini(anchor_parts, prompt, api_key)
        duration = time.monotonic() - start
        print(f"    Generated in {duration:.1f}s")

        frame_path = output_dir / f"frame_{i:02d}.png"
        frame_path.write_bytes(image_data)
        saved.append(frame_path)

    return saved


async def main():
    parser = argparse.ArgumentParser(description="Generate animation via sheet-split or sequential approach")
    parser.add_argument("manifest", type=Path, help="Character manifest JSON")
    parser.add_argument("animation", type=str, help="Animation type (e.g., idle, light_punch)")
    parser.add_argument(
        "--approach", choices=["sheet", "sequential", "reinforced"],
        default="sheet",
        help="Generation approach (default: sheet)",
    )
    parser.add_argument("--output-dir", type=Path, help="Override output directory")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text())
    name = manifest["name"]
    slug = name.lower().replace(" ", "_")

    # API key
    from lib.keychain import get_credential
    api_key = get_credential("google-ai-key")
    if not api_key:
        print("ERROR: google-ai-key not found in Keychain")
        sys.exit(1)

    # Load anchors
    anchor_parts = load_anchors(manifest["anchor_images"])
    if not anchor_parts:
        print("ERROR: No anchor images found")
        sys.exit(1)

    approach_suffix = f"_{args.approach}" if args.approach != "sheet" else ""
    output_dir = args.output_dir or Path("output") / slug / f"{args.animation}{approach_suffix}"

    print(f"\n{'=' * 70}")
    print(f"ANIMATION GENERATION: {name} / {args.animation} (approach: {args.approach})")
    print(f"Output: {output_dir}")
    print(f"Anchors: {len(anchor_parts)} loaded")
    print(f"{'=' * 70}\n")

    approach_fn = {
        "sheet": approach_sheet,
        "sequential": approach_sequential,
        "reinforced": approach_reinforced,
    }[args.approach]

    start = time.monotonic()
    saved = await approach_fn(manifest, args.animation, output_dir, anchor_parts, api_key)
    total = time.monotonic() - start

    print(f"\n{'─' * 70}")
    print(f"DONE: {len(saved)} frames in {total:.1f}s → {output_dir}")


if __name__ == "__main__":
    asyncio.run(main())
