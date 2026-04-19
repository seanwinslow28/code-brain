/** Generate synthetic test frames for the Pixel Quantizer gate check. */

import sharp from 'sharp';
import { mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = join(__dirname, '..', 'test-frames', 'input');

// Use palette colors from Sean's palette
const COLORS = {
  skin: { r: 245, g: 214, b: 198 },
  hair: { r: 194, g: 167, b: 105 },
  pants: { r: 35, g: 35, b: 255 },
  outline: { r: 39, g: 41, b: 41 },
  bg: { r: 0, g: 255, b: 0 }, // Chroma green
  shoes: { r: 245, g: 245, b: 245 },
};

function createFrame(
  width: number,
  height: number,
  offsetX: number = 0,
  offsetY: number = 0,
  colorDrift: number = 0,
): Buffer {
  const channels = 4;
  const data = Buffer.alloc(width * height * channels);

  const drift = () => colorDrift > 0 ? Math.floor(Math.random() * colorDrift * 2) - colorDrift : 0;
  const clamp = (v: number) => Math.max(0, Math.min(255, v));

  // Fill background with chroma green
  for (let i = 0; i < data.length; i += channels) {
    data[i] = COLORS.bg.r;
    data[i + 1] = COLORS.bg.g;
    data[i + 2] = COLORS.bg.b;
    data[i + 3] = 255;
  }

  const setPixel = (x: number, y: number, color: { r: number; g: number; b: number }) => {
    if (x < 0 || x >= width || y < 0 || y >= height) return;
    const offset = (y * width + x) * channels;
    data[offset] = clamp(color.r + drift());
    data[offset + 1] = clamp(color.g + drift());
    data[offset + 2] = clamp(color.b + drift());
    data[offset + 3] = 255;
  };

  const fillRect = (
    x: number,
    y: number,
    w: number,
    h: number,
    color: { r: number; g: number; b: number },
  ) => {
    for (let dy = 0; dy < h; dy++) {
      for (let dx = 0; dx < w; dx++) {
        setPixel(x + dx + offsetX, y + dy + offsetY, color);
      }
    }
  };

  // Draw a simple humanoid figure (centered in a 512x512 canvas)
  const cx = Math.floor(width / 2);
  const cy = Math.floor(height / 2);

  // Head (skin)
  fillRect(cx - 30, cy - 120, 60, 60, COLORS.skin);
  // Hair
  fillRect(cx - 32, cy - 125, 64, 20, COLORS.hair);
  // Body (outline border + skin fill)
  fillRect(cx - 40, cy - 60, 80, 100, COLORS.outline);
  fillRect(cx - 38, cy - 58, 76, 96, COLORS.skin);
  // Pants
  fillRect(cx - 38, cy + 10, 76, 40, COLORS.pants);
  // Legs
  fillRect(cx - 30, cy + 40, 25, 60, COLORS.pants);
  fillRect(cx + 5, cy + 40, 25, 60, COLORS.pants);
  // Shoes
  fillRect(cx - 32, cy + 100, 29, 12, COLORS.shoes);
  fillRect(cx + 3, cy + 100, 29, 12, COLORS.shoes);

  return data;
}

async function generate() {
  mkdirSync(OUTPUT_DIR, { recursive: true });

  const size = 512;

  // Frame 1: base position
  const frame1 = createFrame(size, size, 0, 0, 0);
  await sharp(frame1, { raw: { width: size, height: size, channels: 4 } })
    .png()
    .toFile(join(OUTPUT_DIR, 'frame-001.png'));

  // Frame 2: slight shift right + down (simulating motion)
  const frame2 = createFrame(size, size, 2, 1, 5);
  await sharp(frame2, { raw: { width: size, height: size, channels: 4 } })
    .png()
    .toFile(join(OUTPUT_DIR, 'frame-002.png'));

  // Frame 3: shift back with color drift (simulating video model artifacts)
  const frame3 = createFrame(size, size, -1, 2, 15);
  await sharp(frame3, { raw: { width: size, height: size, channels: 4 } })
    .png()
    .toFile(join(OUTPUT_DIR, 'frame-003.png'));

  console.log(`Generated 3 test frames in ${OUTPUT_DIR}`);
}

generate().catch(console.error);
