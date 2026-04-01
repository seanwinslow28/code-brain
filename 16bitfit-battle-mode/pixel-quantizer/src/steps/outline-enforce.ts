/** Step 4: Outline enforcement — apply bold outlines at sprite edges and color boundaries. */

import { hexToRgb } from '../palettes/index.js';

/**
 * Detect edges and apply outline color.
 *
 * Edge pixels: opaque pixels adjacent to transparent pixels,
 * or adjacent opaque pixels with very different colors.
 *
 * @param data Raw RGBA buffer
 * @param width Frame width
 * @param height Frame height
 * @param outlineColor Hex color for outlines (default "#272929")
 * @param weight Outline thickness in pixels (1-3)
 * @returns Modified buffer + outline pixel count
 */
export function outlineEnforce(
  data: Buffer,
  width: number,
  height: number,
  outlineColor: string = '#272929',
  weight: number = 2,
): { data: Buffer; outlinePixels: number } {
  const oc = hexToRgb(outlineColor);
  const channels = 4;
  let outlinePixels = 0;

  // Work on a copy to avoid contaminating neighbor checks
  const copy = Buffer.from(data);

  // Color distance threshold for "very different" adjacent colors
  const colorBoundaryThresholdSq = 80 * 80; // generous threshold

  const isTransparent = (x: number, y: number): boolean => {
    if (x < 0 || x >= width || y < 0 || y >= height) return true;
    return data[(y * width + x) * channels + 3] === 0;
  };

  const colorDistSq = (x1: number, y1: number, x2: number, y2: number): number => {
    const o1 = (y1 * width + x1) * channels;
    const o2 = (y2 * width + x2) * channels;
    const dr = data[o1] - data[o2];
    const dg = data[o1 + 1] - data[o2 + 1];
    const db = data[o1 + 2] - data[o2 + 2];
    return dr * dr + dg * dg + db * db;
  };

  // Pass 1: Find edge pixels
  const isEdge = new Uint8Array(width * height);

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const idx = y * width + x;
      const offset = idx * channels;
      if (data[offset + 3] === 0) continue; // Skip transparent

      // Check 4-connected neighbors
      const neighbors = [
        [x - 1, y],
        [x + 1, y],
        [x, y - 1],
        [x, y + 1],
      ] as const;

      for (const [nx, ny] of neighbors) {
        // Adjacent to transparent = edge
        if (isTransparent(nx, ny)) {
          isEdge[idx] = 1;
          break;
        }
        // Adjacent to very different color = internal edge
        if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
          if (colorDistSq(x, y, nx, ny) > colorBoundaryThresholdSq) {
            isEdge[idx] = 1;
            break;
          }
        }
      }
    }
  }

  // Pass 2: Dilate edges by weight-1 pixels
  const dilated = new Uint8Array(isEdge);
  for (let pass = 1; pass < weight; pass++) {
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        if (dilated[y * width + x]) continue;
        const offset = (y * width + x) * channels;
        if (data[offset + 3] === 0) continue;

        // Check if any neighbor is an edge
        for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]] as const) {
          const nx = x + dx;
          const ny = y + dy;
          if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
            if (isEdge[ny * width + nx]) {
              dilated[y * width + x] = 1;
              break;
            }
          }
        }
      }
    }
    // Copy dilated back to isEdge for next pass
    isEdge.set(dilated);
  }

  // Pass 3: Apply outline color
  for (let i = 0; i < width * height; i++) {
    if (dilated[i]) {
      const offset = i * channels;
      copy[offset] = oc.r;
      copy[offset + 1] = oc.g;
      copy[offset + 2] = oc.b;
      outlinePixels++;
    }
  }

  // Copy result back
  copy.copy(data);

  return { data, outlinePixels };
}
