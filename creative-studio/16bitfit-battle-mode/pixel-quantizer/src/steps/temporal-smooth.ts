/** Step 3: Temporal smoothing — lock static regions to mode color across frames. */

import type { PaletteColor } from '../types.js';

/**
 * For each pixel position, if the color barely changes across frames
 * (RGB distance < threshold), lock it to the most common color.
 *
 * @param frames Array of raw RGBA buffers (all same dimensions)
 * @param width Frame width
 * @param height Frame height
 * @param threshold RGB distance threshold (default 15)
 * @returns Smoothed frames (same buffers, modified in-place)
 */
export function temporalSmooth(
  frames: Buffer[],
  width: number,
  height: number,
  threshold: number = 15,
): { frames: Buffer[]; pixelsSmoothed: number } {
  if (frames.length < 2) return { frames, pixelsSmoothed: 0 };

  const channels = 4;
  const pixelCount = width * height;
  let pixelsSmoothed = 0;
  const thresholdSq = threshold * threshold;

  for (let px = 0; px < pixelCount; px++) {
    const offset = px * channels;

    // Collect all colors at this position across frames
    const colors: Array<{ r: number; g: number; b: number }> = [];
    for (const frame of frames) {
      if (frame[offset + 3] === 0) continue; // Skip transparent
      colors.push({
        r: frame[offset],
        g: frame[offset + 1],
        b: frame[offset + 2],
      });
    }

    if (colors.length < 2) continue;

    // Check if this pixel is "static" (all colors within threshold of each other)
    const ref = colors[0];
    const isStatic = colors.every((c) => {
      const dr = c.r - ref.r;
      const dg = c.g - ref.g;
      const db = c.b - ref.b;
      return dr * dr + dg * dg + db * db < thresholdSq;
    });

    if (!isStatic) continue;

    // Find mode color (most frequent)
    const colorCounts = new Map<string, { count: number; r: number; g: number; b: number }>();
    for (const c of colors) {
      const key = `${c.r},${c.g},${c.b}`;
      const existing = colorCounts.get(key);
      if (existing) {
        existing.count++;
      } else {
        colorCounts.set(key, { count: 1, ...c });
      }
    }

    let modeColor = colors[0];
    let maxCount = 0;
    for (const entry of colorCounts.values()) {
      if (entry.count > maxCount) {
        maxCount = entry.count;
        modeColor = entry;
      }
    }

    // Lock all frames to mode color at this position
    for (const frame of frames) {
      if (frame[offset + 3] === 0) continue;
      const r = frame[offset];
      const g = frame[offset + 1];
      const b = frame[offset + 2];
      if (r !== modeColor.r || g !== modeColor.g || b !== modeColor.b) {
        frame[offset] = modeColor.r;
        frame[offset + 1] = modeColor.g;
        frame[offset + 2] = modeColor.b;
        pixelsSmoothed++;
      }
    }
  }

  return { frames, pixelsSmoothed };
}
