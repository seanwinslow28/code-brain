"""Generate character manifests for all 12 fighters.

Generates one JSON manifest per character + an all_characters.json index.
Run this script to create/update all manifests:
    python3 manifests/build_manifests.py
"""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST_DIR = Path(__file__).parent
ANCHOR_BASE = "16bitfit-battle-mode/lora-training/dataset/16BitFit-Reference-Images"

ALL_ANIMATIONS = [
    "idle", "walk_forward", "walk_backward", "jump", "crouch",
    "light_punch", "medium_punch", "heavy_punch",
    "light_kick", "heavy_kick",
    "block", "take_hit", "victory", "defeat", "special_move",
]

# ─── Character Definitions ────────────────────────────────────────────

CHAMPIONS = [
    {
        "name": "Sean",
        "slug": "champion_sean",
        "folder": "champions/Sean",
        "prefix": "champion_sean_anchor",
        "description": "Muscular build, blonde hair, white tank top, blue pants, white shoes",
    },
    {
        "name": "Aria",
        "slug": "champion_aria",
        "folder": "champions/Aria",
        "prefix": "champion_aria_anchor",
        "description": "Athletic build, brown hair in ponytail, purple crop top, light jeans, white shoes",
    },
    {
        "name": "Kenji",
        "slug": "champion_kenji",
        "folder": "champions/Kenji",
        "prefix": "champion_kenji_anchor",
        "description": "Lean build, black hair in bun, gray gi top, dark gray pants, white shoes",
    },
    {
        "name": "Marcus",
        "slug": "champion_marcus",
        "folder": "champions/Marcus",
        "prefix": "champion_marcus_anchor",
        "description": "Heavy muscular build, dark skin, short hair, gray tank top, yellow boxing gloves, gray pants, gray shoes",
    },
    {
        "name": "Mary",
        "slug": "champion_mary",
        "folder": "champions/Mary",
        "prefix": "champion_mary_anchor",
        "description": "Athletic build, brown hair in ponytail, purple headband, purple sports bra, purple shorts, gray shoes",
    },
    {
        "name": "Zara",
        "slug": "champion_zara",
        "folder": "champions/Zara",
        "prefix": "champion_zara_anchor",
        "description": "Athletic build, dark hair in low bun, dark gray tank top, dark cargo pants, white shoes",
    },
]

BOSSES = [
    {
        "name": "Gym Bully",
        "slug": "boss_gym_bully",
        "folder": "bosses/Gym Bully",
        "prefix": "boss_gym_bully_anchor",
        "description": "Muscular build, dark hair, sunglasses, olive tank top, red wristbands, gray pants, gray shoes",
    },
    {
        "name": "Procrastination Phantom",
        "slug": "boss_procrastination_phantom",
        "folder": "bosses/Procrastination Phantom",
        "prefix": "boss_procrastination_phantom_anchor",
        "description": "Ghostly figure, white hoodie, blue-gray skin, glowing orange eyes, spectral tail (no legs)",
        "pose_overrides": {
            "walk_forward": "floating forward with spectral trail instead of walking",
            "walk_backward": "floating backward with ghostly retreat instead of stepping",
            "jump": "surging upward with spectral energy instead of jumping",
        },
    },
    {
        "name": "Sloth Demon",
        "slug": "boss_sloth_demon",
        "folder": "bosses/Sloth Demon",
        "prefix": "boss_sloth_demon_anchor",
        "description": "Stocky beast, brown fur, gray armor plates, yellow eyes, clawed feet",
        "pose_overrides": {
            "walk_forward": "lumbering forward with heavy clawed steps instead of walking",
            "jump": "powerful beast leap with claws spread instead of standard jump",
        },
    },
    {
        "name": "Stress Titan",
        "slug": "boss_stress_titan",
        "folder": "bosses/Stress Titan",
        "prefix": "boss_stress_titan_anchor",
        "description": "Tall armored figure, gray skin, white hair, black and orange power suit",
    },
    {
        "name": "Training Dummy",
        "slug": "boss_training_dummy",
        "folder": "bosses/Training Dummy",
        "prefix": "boss_training_dummy_anchor",
        "description": "Wooden/leather training dummy, metal face plate, brown leather straps, bolted construction",
        "pose_overrides": {
            "walk_forward": "rocking forward in pendulum motion instead of walking",
            "jump": "spring-loaded launch from base instead of standard jump",
        },
    },
    {
        "name": "Ultimate Slump",
        "slug": "boss_ultimate_slump",
        "folder": "bosses/Ultimate Slump",
        "prefix": "boss_ultimate_slump_anchor",
        "description": "Hulking figure, pale green-gray skin, long dark hair, hunched posture, minimal clothing",
    },
]


def build_manifest(char: dict, char_type: str, tile_size: int) -> dict:
    anchor_paths = [
        f"{ANCHOR_BASE}/{char['folder']}/{char['prefix']}-{i}.png"
        for i in range(1, 4)
    ]

    manifest = {
        "name": char["name"],
        "tile_size": tile_size,
        "type": char_type,
        "description": char["description"],
        "anchor_images": anchor_paths,
        "animations": ALL_ANIMATIONS,
    }

    if "pose_overrides" in char:
        manifest["pose_overrides"] = char["pose_overrides"]

    return manifest


def main():
    all_files = []

    for char in CHAMPIONS:
        manifest = build_manifest(char, "champion", 128)
        filename = f"{char['slug']}.json"
        filepath = MANIFEST_DIR / filename
        filepath.write_text(json.dumps(manifest, indent=2) + "\n")
        all_files.append(filename)
        print(f"  Created {filename} ({manifest['name']}, 128x128, {len(manifest['animations'])} anims)")

    for char in BOSSES:
        manifest = build_manifest(char, "boss", 256)
        filename = f"{char['slug']}.json"
        filepath = MANIFEST_DIR / filename
        filepath.write_text(json.dumps(manifest, indent=2) + "\n")
        all_files.append(filename)
        print(f"  Created {filename} ({manifest['name']}, 256x256, {len(manifest['animations'])} anims)")

    # Create all_characters.json index
    index = {
        "total_characters": len(all_files),
        "champions": [f for f in all_files if f.startswith("champion_")],
        "bosses": [f for f in all_files if f.startswith("boss_")],
        "animations_per_character": len(ALL_ANIMATIONS),
        "total_animations": len(all_files) * len(ALL_ANIMATIONS),
    }
    index_path = MANIFEST_DIR / "all_characters.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n")
    print(f"\n  Created all_characters.json — {index['total_characters']} characters, {index['total_animations']} total animations")


if __name__ == "__main__":
    print("Building character manifests...")
    main()
    print("\nDone.")
