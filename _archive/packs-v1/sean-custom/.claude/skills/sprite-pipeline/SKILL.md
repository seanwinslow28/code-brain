---
name: sprite-pipeline
description: Automate sprite sheet generation, animation setup, and asset optimization for game development.
---

# Sprite Pipeline Skill

## Purpose

Streamline the path from raw art assets to game-ready sprite sheets. Covers generation, optimization, and Phaser/game engine integration.

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

## Pipeline Stages

### Stage 1: Asset Organization

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
├── processed/              # Intermediate files
└── output/                 # Game-ready assets
    ├── sprites.png         # Packed atlas
    ├── sprites.json        # Atlas metadata
    └── animations.json     # Animation definitions
```

### Stage 2: Sprite Sheet Generation

**Using TexturePacker (recommended):**
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

**Using free-tex-packer-core (free alternative):**
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

**Using Aseprite CLI (pixel art):**
```bash
# Export sprite sheet from Aseprite file
aseprite -b player.aseprite \
  --sheet output/player.png \
  --data output/player.json \
  --sheet-type packed \
  --format json-array
```

### Stage 3: Animation Definition

```json
// animations.json - Phaser 3 format
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

### Stage 4: Phaser Integration

```typescript
// In preload
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

### Stage 5: Optimization

```bash
# PNG optimization (lossless)
pngquant --quality=65-80 --ext=.png --force output/sprites.png

# Or with ImageOptim CLI
imageoptim output/sprites.png

# WebP conversion (50-80% smaller, good browser support)
cwebp -q 80 output/sprites.png -o output/sprites.webp
```

## Automation Script

```bash
#!/bin/bash
# build-sprites.sh

set -e

echo "🎨 Building sprite sheets..."

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
echo "📊 Output sizes:"
ls -lh output/sprites.*

echo "✅ Sprite pipeline complete!"
```

## Success Criteria

- [ ] All frames packed into single atlas (or minimal atlases)
- [ ] Atlas size is power of 2 (for GPU efficiency)
- [ ] No duplicate frames in atlas
- [ ] Animation JSON matches atlas frame names
- [ ] Total asset size < target budget (e.g., 2MB for mobile)

## Verification Steps

1. **Visual Check:** Open atlas in image viewer - any corruption or misalignment?
2. **JSON Check:** Does JSON reference all frames correctly?
3. **Engine Check:** Do animations play correctly in game?
4. **Size Check:** Is final file size acceptable for target platform?

## Common Frame Rates

| Animation Type | FPS | Notes |
|---------------|-----|-------|
| Idle | 6-8 | Subtle movement |
| Walk | 8-12 | Match movement speed |
| Run | 12-16 | Faster cycle |
| Attack | 12-24 | Snappy, responsive |
| Death | 8-12 | Dramatic timing |

## Copy/Paste Ready

```
/sprite-pipeline pack character sprites for Phaser 3
/sprite-pipeline convert Aseprite to sprite sheet
/sprite-pipeline optimize sprites for mobile
/sprite-pipeline setup animation config
```
