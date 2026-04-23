import { describe, it, expect } from 'vitest';
import { findNearestColor, paletteQuantize } from '../src/steps/palette-quantize.js';
import { temporalSmooth } from '../src/steps/temporal-smooth.js';
import { alphaRecover } from '../src/steps/alpha-recover.js';
import { outlineEnforce } from '../src/steps/outline-enforce.js';
import { gridAlign } from '../src/steps/grid-align.js';
import { validateFrame } from '../src/steps/validate.js';
import type { PaletteColor } from '../src/types.js';

const TEST_PALETTE: PaletteColor[] = [
  { hex: '#FF0000', r: 255, g: 0, b: 0, name: 'red' },
  { hex: '#00FF00', r: 0, g: 255, b: 0, name: 'green' },
  { hex: '#0000FF', r: 0, g: 0, b: 255, name: 'blue' },
  { hex: '#FFFFFF', r: 255, g: 255, b: 255, name: 'white' },
  { hex: '#000000', r: 0, g: 0, b: 0, name: 'black' },
  { hex: '#272929', r: 39, g: 41, b: 41, name: 'outline' },
];

// ── Palette Quantize ──────────────────────────────────────────────────

describe('findNearestColor', () => {
  it('returns exact match', () => {
    const result = findNearestColor(255, 0, 0, TEST_PALETTE);
    expect(result.hex).toBe('#FF0000');
  });

  it('snaps near-red to red', () => {
    const result = findNearestColor(240, 10, 5, TEST_PALETTE);
    expect(result.hex).toBe('#FF0000');
  });

  it('snaps mid-gray to black or white based on distance', () => {
    // rgb(200,200,200) is closer to white (255,255,255) than black
    const result = findNearestColor(200, 200, 200, TEST_PALETTE);
    expect(result.hex).toBe('#FFFFFF');
  });
});

describe('paletteQuantize', () => {
  it('quantizes all pixels to palette', () => {
    // 2x2 RGBA buffer with off-palette colors
    const data = Buffer.from([
      240, 10, 5, 255, // near-red → red
      5, 240, 10, 255, // near-green → green
      10, 5, 240, 255, // near-blue → blue
      0, 0, 0, 0,       // transparent → skip
    ]);
    const { offPaletteCount } = paletteQuantize(data, TEST_PALETTE);
    expect(offPaletteCount).toBe(3);
    // Verify first pixel became exact red
    expect(data[0]).toBe(255);
    expect(data[1]).toBe(0);
    expect(data[2]).toBe(0);
  });

  it('leaves exact palette colors unchanged', () => {
    const data = Buffer.from([255, 0, 0, 255]);
    const { offPaletteCount } = paletteQuantize(data, TEST_PALETTE);
    expect(offPaletteCount).toBe(0);
  });
});

// ── Temporal Smooth ───────────────────────────────────────────────────

describe('temporalSmooth', () => {
  it('locks static pixels to mode color', () => {
    const size = 2;
    // 3 frames, all with similar red at position 0
    const frame1 = Buffer.from([
      255, 0, 0, 255, 0, 255, 0, 255,
      0, 0, 255, 255, 0, 0, 0, 255,
    ]);
    const frame2 = Buffer.from([
      252, 3, 1, 255, 0, 255, 0, 255,
      0, 0, 255, 255, 0, 0, 0, 255,
    ]);
    const frame3 = Buffer.from([
      255, 0, 0, 255, 0, 255, 0, 255,
      0, 0, 255, 255, 0, 0, 0, 255,
    ]);

    const { pixelsSmoothed } = temporalSmooth([frame1, frame2, frame3], size, size, 15);
    // Position 0 should be locked to mode (255,0,0) — frame2 was close enough
    expect(frame2[0]).toBe(255);
    expect(frame2[1]).toBe(0);
    expect(frame2[2]).toBe(0);
    expect(pixelsSmoothed).toBeGreaterThan(0);
  });

  it('does not smooth single frame', () => {
    const frame = Buffer.from([255, 0, 0, 255]);
    const { pixelsSmoothed } = temporalSmooth([frame], 1, 1);
    expect(pixelsSmoothed).toBe(0);
  });
});

// ── Alpha Recover ─────────────────────────────────────────────────────

describe('alphaRecover', () => {
  it('removes chroma green background', () => {
    const data = Buffer.from([
      0, 255, 0, 255,   // Green bg → should become transparent
      255, 0, 0, 255,   // Red sprite → should stay
    ]);
    const { pixelsRemoved } = alphaRecover(data, 2, 1, 'chroma', '#00FF00');
    expect(pixelsRemoved).toBe(1);
    expect(data[3]).toBe(0);  // Green pixel now transparent
    expect(data[7]).toBe(255); // Red pixel still opaque
  });

  it('binarizes alpha', () => {
    const data = Buffer.from([255, 0, 0, 100]); // Semi-transparent
    alphaRecover(data, 1, 1, 'chroma', '#00FF00');
    // Alpha 100 < 128, but this pixel isn't green so it stays.
    // Actually 100 < 128 → transparent after binarization
    expect(data[3]).toBe(0);
  });
});

// ── Outline Enforce ───────────────────────────────────────────────────

describe('outlineEnforce', () => {
  it('adds outline at sprite edges', () => {
    // 3x3: center pixel is opaque, rest transparent
    const data = Buffer.alloc(3 * 3 * 4);
    // Center pixel = red, opaque
    const center = (1 * 3 + 1) * 4;
    data[center] = 255;
    data[center + 1] = 0;
    data[center + 2] = 0;
    data[center + 3] = 255;

    const { outlinePixels } = outlineEnforce(data, 3, 3, '#272929', 1);
    // Center pixel is adjacent to transparent → should become outline
    expect(outlinePixels).toBe(1);
    expect(data[center]).toBe(39);     // outline r
    expect(data[center + 1]).toBe(41); // outline g
    expect(data[center + 2]).toBe(41); // outline b
  });
});

// ── Grid Align ────────────────────────────────────────────────────────

describe('gridAlign', () => {
  it('aligns frames to consistent baseline', () => {
    const size = 4;
    const channels = 4;

    // Frame 1: sprite bottom at row 2
    const f1 = Buffer.alloc(size * size * channels);
    f1[(2 * size + 1) * channels + 3] = 255; // Opaque pixel at row 2

    // Frame 2: sprite bottom at row 3
    const f2 = Buffer.alloc(size * size * channels);
    f2[(3 * size + 1) * channels + 3] = 255; // Opaque pixel at row 3

    const { driftValues } = gridAlign([f1, f2], size, size);
    // Both should align to the mode baseline
    expect(driftValues).toHaveLength(2);
  });
});

// ── Validate ──────────────────────────────────────────────────────────

describe('validateFrame', () => {
  it('passes a clean frame', () => {
    // 2x2 with palette colors, some transparency
    const data = Buffer.from([
      255, 0, 0, 255,   // Red (in palette)
      0, 0, 0, 0,       // Transparent
      0, 0, 0, 255,     // Black (in palette)
      0, 0, 0, 0,       // Transparent
    ]);

    const report = validateFrame(
      data, 2, 2, TEST_PALETTE, 'test.png', 2,
      { r: 39, g: 41, b: 41 }, 10, [],
    );
    expect(report.pass).toBe(true);
    expect(report.offPalettePixels).toBe(0);
    expect(report.backgroundClean).toBe(true);
  });

  it('fails on off-palette pixels', () => {
    const data = Buffer.from([
      123, 45, 67, 255,  // Not in palette
      0, 0, 0, 0,
      0, 0, 0, 0,
      0, 0, 0, 0,
    ]);

    const report = validateFrame(
      data, 2, 2, TEST_PALETTE, 'test.png', 2,
      { r: 39, g: 41, b: 41 }, 10, [],
    );
    expect(report.pass).toBe(false);
    expect(report.offPalettePixels).toBe(1);
  });
});
