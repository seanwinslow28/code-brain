#!/usr/bin/env node
/** CLI entry point for the Pixel Quantizer. */

import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { mkdirSync } from 'fs';
import { loadPalette } from './palettes/index.js';
import { runPipeline } from './pipeline.js';
import type { QuantizerConfig } from './types.js';

const argv = yargs(hideBin(process.argv))
  .option('input', { type: 'string', demandOption: true, describe: 'Input frame directory' })
  .option('output', { type: 'string', demandOption: true, describe: 'Output frame directory' })
  .option('palette', { type: 'string', demandOption: true, describe: 'Palette name or JSON path' })
  .option('target-size', { type: 'number', default: 128, describe: 'Output frame size (square)' })
  .option('background-mode', { choices: ['chroma', 'auto'] as const, default: 'chroma' as const })
  .option('chroma-color', { type: 'string', default: '#00FF00' })
  .option('outline-weight', { type: 'number', default: 2 })
  .option('outline-color', { type: 'string', default: '#272929' })
  .option('static-threshold', { type: 'number', default: 15 })
  .option('skip-temporal', { type: 'boolean', default: false })
  .option('skip-outline', { type: 'boolean', default: false })
  .option('verbose', { type: 'boolean', default: false })
  .strict()
  .parseSync();

async function main() {
  const palette = loadPalette(argv.palette);
  mkdirSync(argv.output, { recursive: true });

  const config: QuantizerConfig = {
    inputDir: argv.input,
    outputDir: argv.output,
    palette,
    targetSize: argv['target-size'],
    backgroundMode: argv['background-mode'],
    chromaColor: argv['chroma-color'],
    outlineWeight: argv['outline-weight'],
    outlineColor: argv['outline-color'],
    staticThreshold: argv['static-threshold'],
    skipTemporal: argv['skip-temporal'],
    skipOutline: argv['skip-outline'],
    verbose: argv.verbose,
  };

  console.log(`Pixel Quantizer — processing ${config.inputDir} → ${config.outputDir}`);
  const report = await runPipeline(config);

  console.log('\n=== Pipeline Report ===');
  console.log(`Total frames: ${report.totalFrames}`);
  console.log(`Passed: ${report.passedFrames} / Failed: ${report.failedFrames}`);
  console.log(`Temporal jitter: ${report.temporalJitterScore}`);
  console.log(`Total time: ${report.totalTimeMs}ms`);

  if (report.failedFrames > 0) {
    console.log('\nFailed frames:');
    for (const f of report.frames.filter((fr) => !fr.pass)) {
      console.log(`  ${f.filename}: off-palette=${f.offPalettePixels} dims=${f.dimensions.width}x${f.dimensions.height}`);
    }
  }

  console.log(JSON.stringify(report, null, 2));

  process.exit(report.failedFrames > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error('Pipeline failed:', err);
  process.exit(1);
});
