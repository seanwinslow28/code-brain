---
name: sprite-asset-pipeline
description: Automate the "Pixel Purity Pipeline" for game assets. Cleans AI-generated sprites, packs sprite sheets, and enforces strict naming conventions. Triggers on "clean this sprite", "pack texture atlas", "fix grid alignment", or "pixel purity".
---

# Sprite & Asset Pipeline

## Purpose

Enforce strict "pixel purity" for Game Boy style assets. Convert noisy AI outputs into crisp, grid-aligned sprites, automate sprite sheet packing, and maintain file conventions for batch processing.

## When to Use

- "Cleaning" AI-generated images to remove mixels/blur
- Batch processing raw PNGs into a texture atlas
- Generating Phaser-compatible JSON metadata
- Fixing grid misalignment in 16x16 or 8x8 assets

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

## Core Workflows

### 1. The "Pixel Purity" Toolchain
Use this sequence to guarantee asset quality.

1.  **Draft:** Create raw assets (AI or manual) in `raw/`
2.  **Purify:** Run `proper-pixel-art` to fix grid/palette
3.  **Pack:** Use `sharpsheet` to generate atlas
4.  **Render:** Load in Phaser with `pixelArt: true`

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

### 3. Automation Scripts
Add these to `package.json` to automate the pipeline.

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

### 4. Phaser Animation Loading
Automatically slice grid-based sheets.

```typescript
// Preload
this.load.spritesheet('hero', 'assets/hero_atlas.png', {
  frameWidth: 16,
  frameHeight: 16,
  margin: 0,
  spacing: 0
});

// Create Animation
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

### 5. AI Asset Cleaning (Python Script)
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

## Success Criteria

- [ ] All output PNGs are strictly 4-color (or designated palette)
- [ ] No anti-aliasing or "soft" pixels exist
- [ ] Sprites align perfectly to 16x16 or 8x8 grid
- [ ] Naming convention `entity_action_00.png` is enforced
- [ ] Texture atlas JSON successfully loads in Phaser

## Copy/Paste Ready

```
"Clean the slime sprites using the 4-color palette"
"Pack the processed folder into a texture atlas"
"Generate the package.json scripts for asset automation"
"Create a Phaser animation config for the hero walk cycle"
```
