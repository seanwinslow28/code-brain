/** Step 2: Force-snap every pixel to the nearest palette color (Euclidean RGB). */

import type { PaletteColor } from '../types.js';

export function findNearestColor(
  r: number,
  g: number,
  b: number,
  palette: PaletteColor[],
): PaletteColor {
  let bestDist = Infinity;
  let best = palette[0];
  for (const c of palette) {
    const dr = r - c.r;
    const dg = g - c.g;
    const db = b - c.b;
    const dist = dr * dr + dg * dg + db * db; // Skip sqrt for perf
    if (dist < bestDist) {
      bestDist = dist;
      best = c;
    }
  }
  return best;
}

/**
 * Quantize a raw RGBA pixel buffer to the given palette.
 * Modifies the buffer in-place and returns it.
 */
export function paletteQuantize(
  data: Buffer,
  palette: PaletteColor[],
): { data: Buffer; offPaletteCount: number } {
  let offPaletteCount = 0;
  const channels = 4; // RGBA
  for (let i = 0; i < data.length; i += channels) {
    const a = data[i + 3];
    if (a === 0) continue; // Skip fully transparent pixels

    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];

    const nearest = findNearestColor(r, g, b, palette);

    if (r !== nearest.r || g !== nearest.g || b !== nearest.b) {
      offPaletteCount++;
    }

    data[i] = nearest.r;
    data[i + 1] = nearest.g;
    data[i + 2] = nearest.b;
  }
  return { data, offPaletteCount };
}
