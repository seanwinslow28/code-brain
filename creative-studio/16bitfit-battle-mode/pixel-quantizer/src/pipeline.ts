/** Main Pixel Quantizer pipeline — orchestrates all 7 steps. */

import sharp from 'sharp';
import { readdir } from 'fs/promises';
import { join } from 'path';
import type { QuantizerConfig, FrameReport, PipelineReport, StepMetrics } from './types.js';
import { downscaleToRaw } from './steps/downscale.js';
import { paletteQuantize } from './steps/palette-quantize.js';
import { temporalSmooth } from './steps/temporal-smooth.js';
import { outlineEnforce } from './steps/outline-enforce.js';
import { alphaRecover } from './steps/alpha-recover.js';
import { gridAlign } from './steps/grid-align.js';
import { validateFrame, generateSummary } from './steps/validate.js';
import { hexToRgb } from './palettes/index.js';

export async function runPipeline(config: QuantizerConfig): Promise<PipelineReport> {
  const pipelineStart = performance.now();
  const size = config.targetSize;
  const outlineRgb = hexToRgb(config.outlineColor);

  // Load input frames (sorted for deterministic ordering)
  const files = (await readdir(config.inputDir))
    .filter((f) => /\.(png|jpg|jpeg|webp)$/i.test(f))
    .sort();

  if (files.length === 0) {
    throw new Error(`No image files found in ${config.inputDir}`);
  }

  if (config.verbose) {
    console.log(`Processing ${files.length} frames at ${size}x${size}`);
  }

  // Step 1: Downscale all frames
  const rawFrames: { data: Buffer; filename: string }[] = [];
  for (const file of files) {
    const inputBuffer = await sharp(join(config.inputDir, file)).toBuffer();
    const { data } = await downscaleToRaw(inputBuffer, size);
    rawFrames.push({ data, filename: file });
  }

  // Step 5 (run before palette to remove background colors from quantization):
  // Alpha recovery
  for (const frame of rawFrames) {
    alphaRecover(
      frame.data,
      size,
      size,
      config.backgroundMode,
      config.chromaColor,
    );
  }

  // Step 2: Palette quantize all frames
  for (const frame of rawFrames) {
    paletteQuantize(frame.data, config.palette);
  }

  // Step 3: Temporal smoothing (across all frames)
  if (!config.skipTemporal && rawFrames.length > 1) {
    const buffers = rawFrames.map((f) => f.data);
    temporalSmooth(buffers, size, size, config.staticThreshold);
  }

  // Step 4: Outline enforcement
  if (!config.skipOutline) {
    for (const frame of rawFrames) {
      outlineEnforce(frame.data, size, size, config.outlineColor, config.outlineWeight);
    }
  }

  // Step 6: Grid alignment (baseline registration)
  {
    const buffers = rawFrames.map((f) => f.data);
    gridAlign(buffers, size, size);
  }

  // Write output and validate
  const frameReports: FrameReport[] = [];

  for (const frame of rawFrames) {
    const frameStart = performance.now();

    // Write to output
    const outputPath = join(config.outputDir, frame.filename.replace(/\.[^.]+$/, '.png'));
    await sharp(frame.data, { raw: { width: size, height: size, channels: 4 } })
      .png()
      .toFile(outputPath);

    const processingTimeMs = performance.now() - frameStart;

    // Step 7: Validate
    const report = validateFrame(
      frame.data,
      size,
      size,
      config.palette,
      frame.filename,
      size,
      outlineRgb,
      processingTimeMs,
      [],
    );
    frameReports.push(report);

    if (config.verbose) {
      const status = report.pass ? 'PASS' : 'FAIL';
      console.log(`  ${frame.filename}: ${status} (off-palette: ${report.offPalettePixels})`);
    }
  }

  const totalTimeMs = performance.now() - pipelineStart;
  return generateSummary(frameReports, totalTimeMs);
}
