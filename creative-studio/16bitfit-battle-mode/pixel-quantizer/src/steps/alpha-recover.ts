/** Step 5: Alpha recovery — remove background and binarize alpha. */

import { hexToRgb } from '../palettes/index.js';

/**
 * Remove background color and enforce binary alpha (0 or 255).
 *
 * @param data Raw RGBA buffer
 * @param width Frame width
 * @param height Frame height
 * @param mode 'chroma' (specific color) or 'auto' (dominant bg color)
 * @param chromaColor Hex color for chroma key (default "#00FF00")
 * @param threshold Color distance threshold for background detection
 */
export function alphaRecover(
  data: Buffer,
  width: number,
  height: number,
  mode: 'chroma' | 'auto' = 'chroma',
  chromaColor: string = '#00FF00',
  threshold: number = 50,
): { data: Buffer; pixelsRemoved: number } {
  const channels = 4;
  let pixelsRemoved = 0;
  const thresholdSq = threshold * threshold;

  let bgColor: { r: number; g: number; b: number };

  if (mode === 'chroma') {
    bgColor = hexToRgb(chromaColor);
  } else {
    bgColor = detectDominantBackground(data, width, height);
  }

  // Pass 1: Remove background pixels
  for (let i = 0; i < data.length; i += channels) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];

    const dr = r - bgColor.r;
    const dg = g - bgColor.g;
    const db = b - bgColor.b;
    const distSq = dr * dr + dg * dg + db * db;

    if (distSq < thresholdSq) {
      data[i + 3] = 0; // Make transparent
      pixelsRemoved++;
    }
  }

  // Pass 2: Binarize alpha (no semi-transparency in pixel art)
  for (let i = 0; i < data.length; i += channels) {
    data[i + 3] = data[i + 3] >= 128 ? 255 : 0;
  }

  return { data, pixelsRemoved };
}

function detectDominantBackground(
  data: Buffer,
  width: number,
  height: number,
): { r: number; g: number; b: number } {
  // Sample border pixels (top/bottom rows, left/right columns)
  const channels = 4;
  const colorCounts = new Map<string, { count: number; r: number; g: number; b: number }>();

  const samplePixel = (x: number, y: number) => {
    const offset = (y * width + x) * channels;
    if (data[offset + 3] === 0) return;
    const key = `${data[offset]},${data[offset + 1]},${data[offset + 2]}`;
    const existing = colorCounts.get(key);
    if (existing) {
      existing.count++;
    } else {
      colorCounts.set(key, {
        count: 1,
        r: data[offset],
        g: data[offset + 1],
        b: data[offset + 2],
      });
    }
  };

  // Sample all 4 borders
  for (let x = 0; x < width; x++) {
    samplePixel(x, 0);
    samplePixel(x, height - 1);
  }
  for (let y = 0; y < height; y++) {
    samplePixel(0, y);
    samplePixel(width - 1, y);
  }

  // Find most common border color
  let dominant = { r: 0, g: 255, b: 0 }; // Default to green
  let maxCount = 0;
  for (const entry of colorCounts.values()) {
    if (entry.count > maxCount) {
      maxCount = entry.count;
      dominant = entry;
    }
  }

  return dominant;
}
