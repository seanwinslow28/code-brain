---
name: sprite-asset-pipeline
description: Automate the "Pixel Purity Pipeline" for game assets. Cleans AI-generated sprites, packs sprite sheets, optimizes output, and enforces strict naming conventions. Triggers on "clean this sprite", "pack texture atlas", "fix grid alignment", "pixel purity", "sprite pipeline", or "optimize sprites".
---

# Sprite & Asset Pipeline

## Purpose

Full sprite pipeline from raw art to game-ready assets. Enforce "pixel purity" for Game Boy style assets, convert noisy AI outputs into crisp grid-aligned sprites, pack sprite sheets with multiple tool options, optimize for size and performance, and maintain file conventions for batch processing.

## When to Use

- "Cleaning" AI-generated images to remove mixels/blur
- Batch processing raw PNGs into a texture atlas
- Generating Phaser-compatible JSON metadata
- Fixing grid misalignment in 16x16 or 8x8 assets
- Optimizing sprite sheets for file size / load time
- Converting Aseprite files to packed sprite sheets
- Setting up animation definitions and frame rate configs

## Clarifying Interview

```
Sprite Pipeline Setup:

1. **Source format:** Individual PNGs | Aseprite | Photoshop layers | AI-generated
2. **Target engine:** Phaser 3 | Unity | Godot | Custom
3. **Animation type:** Spritesheet | Spine | JSON atlas | Individual frames
4. **Art style:** Pixel art | Vector | HD | Mixed
5. **Platform:** Web | Mobile | Desktop
6. **Optimization priority:** File size | Quality | Load time
```

## Examples

**Example 1: Cleaning AI Assets**
```
User: "Clean these 4 generated slime sprites. They look blurry and off-grid."
Claude: [Uses sprite-asset-pipeline]
Running 'proper-pixel-art' to enforce 16-color palette and grid alignment:

# Command
python3 scripts/process_assets.py --input "./raw/slimes/*.png" --output "./processed/slimes/" --colors 16 --grid 16

# Result
- Fixed transparency artifacts
- Quantized to Game Boy palette
- Snapped to 16x16 grid
```

**Example 2: Creating a Sprite Sheet**
```
User: "Pack all player animations into a texture atlas for Phaser."
Claude: [Uses sprite-asset-pipeline]
Executing sharpsheet to pack 24 frames:

# Command
sharpsheet "./processed/player/*.png" --outputPath "./public/assets" --outputFilename "hero_atlas" --format "json"

# Output
Generated: public/assets/hero_atlas.png (256x256)
Generated: public/assets/hero_atlas.json (Phaser 3 compatible)
```

## Asset Directory Structure

```
assets/
├── raw/                    # Original files, never modify
│   ├── characters/
│   │   ├── player/
│   │   │   ├── idle/       # idle_01.png, idle_02.png, ...
│   │   │   ├── walk/
│   │   │   └── attack/
│   │   └── enemy/
│   ├── tiles/
│   └── ui/
├── processed/              # Intermediate files (after pixel purity)
└── output/                 # Game-ready assets
    ├── sprites.png         # Packed atlas
    ├── sprites.json        # Atlas metadata
    └── animations.json     # Animation definitions
```

## Core Workflows

### 1. The "Pixel Purity" Toolchain
Use this sequence to guarantee asset quality.

1.  **Draft:** Create raw assets (AI or manual) in `raw/`
2.  **Purify:** Run `proper-pixel-art` to fix grid/palette
3.  **Pack:** Use `sharpsheet` (or TexturePacker / free-tex-packer) to generate atlas
4.  **Optimize:** Run `pngquant` + `cwebp` for size reduction
5.  **Render:** Load in Phaser with `pixelArt: true`

### 2. File Naming Conventions
Use snake_case grouped by Entity -> Action -> Variation -> Frame.

| Component | Example | Description |
|-----------|---------|-------------|
| Entity | `hero` | The character or object name |
| Action | `walk` | Animation state (idle, run, attack) |
| Variation | `down` | Direction or variant |
| Frame | `01` | Zero-padded frame number |

**Valid Examples:**
- `hero_walk_down_00.png`
- `hero_attack_side_02.png`
- `ui_heart_full_00.png`

### 3. Sprite Sheet Generation Tools

#### sharpsheet (lightweight, npm)
```bash
sharpsheet "./processed/player/*.png" --outputPath "./public/assets" --outputFilename "hero_atlas" --format "json"
```

#### TexturePacker (industry-standard, GUI + CLI)
```bash
# Install: https://www.codeandweb.com/texturepacker
TexturePacker \
  --format phaser \
  --data output/sprites.json \
  --sheet output/sprites.png \
  --trim-sprite-names \
  --max-size 2048 \
  --size-constraints POT \
  raw/characters/
```

#### free-tex-packer-core (free Node.js alternative)
```javascript
// pack-sprites.js
const pack = require('free-tex-packer-core');
const fs = require('fs');
const path = require('path');

const images = [
  { path: 'idle_01.png', contents: fs.readFileSync('raw/player/idle/idle_01.png') },
  // ... more images
];

pack(images, {
  textureName: 'sprites',
  width: 2048,
  height: 2048,
  fixedSize: false,
  powerOfTwo: true,
  padding: 2,
  exporter: 'Phaser3',
  removeFileExtension: true,
}, (files) => {
  files.forEach(file => {
    fs.writeFileSync(`output/${file.name}`, file.buffer);
  });
});
```

#### Aseprite CLI (pixel art source files)
```bash
# Export sprite sheet from Aseprite file
aseprite -b player.aseprite \
  --sheet output/player.png \
  --data output/player.json \
  --sheet-type packed \
  --format json-array
```

### 4. PNG Optimization & WebP Conversion

```bash
# PNG optimization (lossy, significant size reduction)
pngquant --quality=65-80 --ext=.png --force output/sprites.png

# Or with ImageOptim CLI (lossless)
imageoptim output/sprites.png

# WebP conversion (50-80% smaller, good browser support)
cwebp -q 80 output/sprites.png -o output/sprites.webp
```

### 5. Animation JSON Definition

```json
{
  "anims": [
    {
      "key": "player_idle",
      "frames": [
        { "key": "sprites", "frame": "player_idle_01" },
        { "key": "sprites", "frame": "player_idle_02" },
        { "key": "sprites", "frame": "player_idle_03" }
      ],
      "frameRate": 8,
      "repeat": -1
    },
    {
      "key": "player_walk",
      "frames": [
        { "key": "sprites", "frame": "player_walk_01" },
        { "key": "sprites", "frame": "player_walk_02" },
        { "key": "sprites", "frame": "player_walk_03" },
        { "key": "sprites", "frame": "player_walk_04" }
      ],
      "frameRate": 12,
      "repeat": -1
    }
  ]
}
```

### 6. Phaser Animation Loading
Automatically slice grid-based sheets.

```typescript
// Preload (grid-based spritesheet)
this.load.spritesheet('hero', 'assets/hero_atlas.png', {
  frameWidth: 16,
  frameHeight: 16,
  margin: 0,
  spacing: 0
});

// Create Animation (from spritesheet indices)
this.anims.create({
  key: 'hero_walk_down',
  frames: this.anims.generateFrameNumbers('hero', {
    start: 0,
    end: 3
  }),
  frameRate: 10,
  repeat: -1
});
```

```typescript
// Alternative: Atlas-based loading (from JSON definition)
this.load.atlas('sprites', 'assets/sprites.png', 'assets/sprites.json');
this.load.json('anims', 'assets/animations.json');

// In create
const animsData = this.cache.json.get('anims');
animsData.anims.forEach((anim: any) => {
  this.anims.create(anim);
});

// Usage
this.player = this.add.sprite(100, 100, 'sprites', 'player_idle_01');
this.player.play('player_idle');
```

### 7. AI Asset Cleaning (Python Script)
Simulated logic for `fix_pixels.py`.

```python
# scripts/fix_pixels.py
import argparse
from PIL import Image

def quantize_image(input_path, output_path, colors=4):
    img = Image.open(input_path).convert('RGB')

    # 1. Enforce Palette (Game Boy 4-Greens)
    palette = [
        0x0f380f, # Darkest
        0x306230, # Dark
        0x8bac0f, # Light
        0x9bbc0f  # Lightest
    ]
    # ... quantization logic using P-mode ...

    # 2. Enforce 16x16 Grid Snap
    # Resample with NEAREST neighbor to kill anti-aliasing
    width, height = img.size
    img = img.resize((width, height), resample=Image.NEAREST)

    img.save(output_path)

if __name__ == "__main__":
    # parser setup...
    pass
```

## Automation Scripts

### package.json scripts
```json
{
  "scripts": {
    "//": "Pixel Purity Pipeline Commands",

    "assets:fix": "python3 scripts/fix_pixels.py --input './raw' --colors 4",

    "assets:pack": "sharpsheet './processed/*.png' --outputPath './public/assets' --outputFilename 'atlas'",

    "assets:watch": "nodemon --watch './raw' --exec 'npm run assets:fix && npm run assets:pack'"
  }
}
```

### build-sprites.sh (full pipeline)
```bash
#!/bin/bash
# build-sprites.sh -- Pack, optimize, and convert sprites in one pass

set -e

echo "Building sprite sheets..."

# Pack textures
TexturePacker \
  --format phaser \
  --data output/sprites.json \
  --sheet output/sprites.png \
  --trim-sprite-names \
  --max-size 2048 \
  raw/characters/

# Optimize
pngquant --quality=65-80 --ext=.png --force output/sprites.png

# Generate WebP variant
cwebp -q 80 output/sprites.png -o output/sprites.webp

# Report sizes
echo "Output sizes:"
ls -lh output/sprites.*

echo "Sprite pipeline complete!"
```

## Common Frame Rates

| Animation Type | FPS | Notes |
|---------------|-----|-------|
| Idle | 6-8 | Subtle movement |
| Walk | 8-12 | Match movement speed |
| Run | 12-16 | Faster cycle |
| Attack | 12-24 | Snappy, responsive |
| Death | 8-12 | Dramatic timing |

## Success Criteria

- [ ] All output PNGs are strictly 4-color (or designated palette)
- [ ] No anti-aliasing or "soft" pixels exist
- [ ] Sprites align perfectly to 16x16 or 8x8 grid
- [ ] Naming convention `entity_action_00.png` is enforced
- [ ] All frames packed into single atlas (or minimal atlases)
- [ ] Atlas size is power of 2 (for GPU efficiency)
- [ ] No duplicate frames in atlas
- [ ] Animation JSON matches atlas frame names
- [ ] Texture atlas JSON successfully loads in Phaser
- [ ] Total asset size < target budget (e.g., 2MB for mobile)

## Verification Steps

1. **Visual Check:** Open atlas in image viewer -- any corruption or misalignment?
2. **JSON Check:** Does JSON reference all frames correctly?
3. **Engine Check:** Do animations play correctly in game?
4. **Size Check:** Is final file size acceptable for target platform?

## Copy/Paste Ready

```
"Clean the slime sprites using the 4-color palette"
"Pack the processed folder into a texture atlas"
"Generate the package.json scripts for asset automation"
"Create a Phaser animation config for the hero walk cycle"
"Convert Aseprite file to packed sprite sheet"
"Optimize sprites for mobile with WebP fallback"
"Run the full build-sprites pipeline"
```
