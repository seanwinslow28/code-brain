"""Test all 12 characters — generates one sprite sheet per character.

Instead of running every animation, this generates a single composite
sprite sheet image for each character showing multiple poses in one frame.
This lets us quickly evaluate character consistency and style quality
across the entire roster.

Usage:
    python3 batch/test_all_characters.py
    python3 batch/test_all_characters.py --characters sean aria
    python3 batch/test_all_characters.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PIXEL_QUANTIZER_DIR = SCRIPT_DIR.parent
VIDEO_EVAL_DIR = PIXEL_QUANTIZER_DIR / "video-eval"
REPO_ROOT = PIXEL_QUANTIZER_DIR.parent.parent.parent  # post-v3.15.0: 16bitfit nested under creative-studio/
MANIFESTS_DIR = PIXEL_QUANTIZER_DIR / "manifests"
OUTPUT_DIR = PIXEL_QUANTIZER_DIR / "output" / "_character_tests"

sys.path.insert(0, str(PIXEL_QUANTIZER_DIR))
sys.path.insert(0, str(VIDEO_EVAL_DIR))
sys.path.insert(0, str(REPO_ROOT / "agents-sdk"))

# How many seconds to wait between characters to avoid rate limiting
INTER_CHARACTER_DELAY = 10

SPRITE_SHEET_PROMPT = (
    "Generate a pixel art sprite sheet of THIS EXACT CHARACTER from the reference images. "
    "The sprite sheet should show the character in 6 poses arranged in a 3x2 grid: "
    "(1) neutral fighting stance, (2) punch with right arm extended, "
    "(3) high kick with right leg, (4) crouching guard, "
    "(5) jumping with arms raised, (6) victory pose with fist pumped. "
    "MATCH THE CHARACTER EXACTLY: {description}. "
    "Same hair, clothing, body type, and color palette as the reference images. "
    "Style: SF2 pixel art, bold #272929 dark outlines, clean pixel edges. "
    "Each pose in a {tile_size}x{tile_size} cell. "
    "Background: solid #00FF00 green for each cell. "
    "Character facing RIGHT in every pose. "
    "No anti-aliasing, no gradients, no background scenery."
)


async def test_character(manifest_path: Path, dry_run: bool = False) -> dict:
    """Generate a sprite sheet test for one character."""
    import httpx

    manifest = json.loads(manifest_path.read_text())
    name = manifest["name"]
    tile_size = manifest["tile_size"]
    description = manifest["description"]
    anchor_paths = manifest["anchor_images"]
    char_type = manifest["type"]

    result = {
        "name": name,
        "type": char_type,
        "tile_size": tile_size,
        "status": "pending",
        "output_path": "",
        "duration_ms": 0,
        "error": "",
    }

    if dry_run:
        print(f"  [DRY RUN] {name} ({char_type}, {tile_size}x{tile_size}) — {len(anchor_paths)} anchors")
        result["status"] = "dry_run"
        return result

    # Load anchor images
    anchor_parts = []
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
        anchor_parts.append({"inlineData": {"mimeType": mime, "data": img_b64}})

    if not anchor_parts:
        result["status"] = "failed"
        result["error"] = "No anchor images found"
        print(f"  FAIL {name}: No anchor images found")
        return result

    # Build prompt
    prompt = SPRITE_SHEET_PROMPT.format(
        description=description,
        tile_size=tile_size,
    )

    # Get API key
    from lib.keychain import get_credential
    api_key = get_credential("google-ai-key")
    if not api_key:
        result["status"] = "failed"
        result["error"] = "google-ai-key not in Keychain"
        return result

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent"
    parts = list(anchor_parts) + [{"text": prompt}]

    start = time.monotonic()

    # Call with retry
    max_retries = 3
    backoff = [5, 15, 30]
    last_error = None

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
                    print(f"    {name}: Gemini {resp.status_code}, retrying in {wait}s ({attempt + 1}/{max_retries + 1})")
                    await asyncio.sleep(wait)
                    continue

                resp.raise_for_status()
                data = resp.json()

                # Extract image
                image_data = None
                for candidate in data.get("candidates", []):
                    for part in candidate.get("content", {}).get("parts", []):
                        if "inlineData" in part:
                            image_data = base64.b64decode(part["inlineData"]["data"])
                            break

                if image_data:
                    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    slug = name.lower().replace(" ", "_")
                    out_path = OUTPUT_DIR / f"{char_type}_{slug}_sheet.png"
                    out_path.write_bytes(image_data)

                    duration = (time.monotonic() - start) * 1000
                    result["status"] = "pass"
                    result["output_path"] = str(out_path)
                    result["duration_ms"] = duration
                    print(f"  PASS {name:<30} {char_type:<10} {tile_size}x{tile_size}  ({duration / 1000:.1f}s)")
                    return result
                else:
                    last_error = "No image in Gemini response"
                    if attempt < max_retries:
                        wait = backoff[min(attempt, len(backoff) - 1)]
                        print(f"    {name}: Empty response, retrying in {wait}s")
                        await asyncio.sleep(wait)
                        continue

        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                wait = backoff[min(attempt, len(backoff) - 1)]
                print(f"    {name}: {e}, retrying in {wait}s")
                await asyncio.sleep(wait)
                continue

    duration = (time.monotonic() - start) * 1000
    result["status"] = "failed"
    result["error"] = str(last_error)
    result["duration_ms"] = duration
    print(f"  FAIL {name:<30} {char_type:<10} {tile_size}x{tile_size}  ({last_error})")
    return result


async def main():
    parser = argparse.ArgumentParser(description="Test sprite sheet generation for all characters")
    parser.add_argument("--characters", nargs="*", help="Specific character slugs to test (e.g., sean aria)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Load all manifests
    manifest_files = sorted(MANIFESTS_DIR.glob("champion_*.json")) + sorted(MANIFESTS_DIR.glob("boss_*.json"))

    if args.characters:
        # Filter to requested characters
        slugs = {s.lower() for s in args.characters}
        manifest_files = [
            f for f in manifest_files
            if any(s in f.stem.lower() for s in slugs)
        ]

    print(f"{'=' * 70}")
    print(f"CHARACTER SPRITE SHEET TEST — {len(manifest_files)} characters")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'=' * 70}\n")

    results = []
    for i, mf in enumerate(manifest_files):
        result = await test_character(mf, dry_run=args.dry_run)
        results.append(result)

        # Delay between characters to avoid rate limiting
        if not args.dry_run and i < len(manifest_files) - 1:
            print(f"    (waiting {INTER_CHARACTER_DELAY}s before next character...)")
            await asyncio.sleep(INTER_CHARACTER_DELAY)

    # Summary
    passed = sum(1 for r in results if r["status"] == "pass")
    failed = sum(1 for r in results if r["status"] == "failed")

    print(f"\n{'─' * 70}")
    print(f"RESULTS: {passed}/{len(results)} passed, {failed} failed")

    if failed:
        print("\nFailed characters:")
        for r in results:
            if r["status"] == "failed":
                print(f"  {r['name']}: {r['error']}")

    # Save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results_path = OUTPUT_DIR / "test_results.json"
    results_path.write_text(json.dumps(results, indent=2) + "\n")
    print(f"\nResults saved: {results_path}")


if __name__ == "__main__":
    asyncio.run(main())
