/** Step 7: Validation — generate per-frame and summary reports. */

import type { PaletteColor, FrameReport, PipelineReport } from '../types.js';

/**
 * Validate a single processed frame.
 */
export function validateFrame(
  data: Buffer,
  width: number,
  height: number,
  palette: PaletteColor[],
  filename: string,
  targetSize: number,
  outlineColor: { r: number; g: number; b: number },
  processingTimeMs: number,
  stepMetrics: FrameReport['stepMetrics'],
): FrameReport {
  const channels = 4;
  let offPalettePixels = 0;
  let outlinePixels = 0;
  let opaquePixels = 0;
  let transparentPixels = 0;
  let bottomEdge = 0;

  // Build a set of palette hex for fast lookup
  const paletteSet = new Set(palette.map((c) => `${c.r},${c.g},${c.b}`));

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const offset = (y * width + x) * channels;
      const a = data[offset + 3];

      if (a === 0) {
        transparentPixels++;
        continue;
      }

      opaquePixels++;
      const r = data[offset];
      const g = data[offset + 1];
      const b = data[offset + 2];

      const key = `${r},${g},${b}`;
      if (!paletteSet.has(key)) {
        offPalettePixels++;
      }

      if (r === outlineColor.r && g === outlineColor.g && b === outlineColor.b) {
        outlinePixels++;
      }

      if (a > 0) {
        bottomEdge = Math.max(bottomEdge, y);
      }
    }
  }

  const totalPixels = width * height;
  const outlineCoverage = opaquePixels > 0 ? outlinePixels / opaquePixels : 0;
  const backgroundClean = transparentPixels > 0; // At least some transparency

  const dimensionsOk = width === targetSize && height === targetSize;
  const paletteOk = offPalettePixels === 0;

  return {
    filename,
    dimensions: { width, height },
    offPalettePixels,
    outlineCoverage: Math.round(outlineCoverage * 1000) / 1000,
    backgroundClean,
    baselinePosition: bottomEdge,
    processingTimeMs: Math.round(processingTimeMs),
    pass: dimensionsOk && paletteOk && backgroundClean,
    stepMetrics,
  };
}

/**
 * Generate a summary report from individual frame reports.
 */
export function generateSummary(
  frameReports: FrameReport[],
  totalTimeMs: number,
): PipelineReport {
  const passedFrames = frameReports.filter((f) => f.pass).length;

  // Calculate temporal jitter: variance in baseline positions
  const baselines = frameReports.map((f) => f.baselinePosition);
  const meanBaseline = baselines.reduce((a, b) => a + b, 0) / baselines.length;
  const variance =
    baselines.reduce((sum, b) => sum + (b - meanBaseline) ** 2, 0) / baselines.length;
  const temporalJitterScore = Math.round(Math.sqrt(variance) * 100) / 100;

  return {
    totalFrames: frameReports.length,
    passedFrames,
    failedFrames: frameReports.length - passedFrames,
    frames: frameReports,
    temporalJitterScore,
    totalTimeMs: Math.round(totalTimeMs),
  };
}
