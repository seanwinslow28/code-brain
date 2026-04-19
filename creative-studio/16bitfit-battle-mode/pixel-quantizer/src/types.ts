/** Shared types for the Pixel Quantizer pipeline. */

export interface RGB {
  r: number;
  g: number;
  b: number;
}

export interface RGBA extends RGB {
  a: number;
}

export interface PaletteColor extends RGB {
  hex: string;
  name?: string;
}

export interface QuantizerConfig {
  inputDir: string;
  outputDir: string;
  palette: PaletteColor[];
  targetSize: number;
  backgroundMode: 'chroma' | 'auto';
  chromaColor: string;
  outlineWeight: number;
  outlineColor: string;
  staticThreshold: number;
  skipTemporal: boolean;
  skipOutline: boolean;
  verbose: boolean;
}

export interface StepMetrics {
  stepName: string;
  durationMs: number;
  details?: Record<string, unknown>;
}

export interface FrameReport {
  filename: string;
  dimensions: { width: number; height: number };
  offPalettePixels: number;
  outlineCoverage: number;
  backgroundClean: boolean;
  baselinePosition: number;
  processingTimeMs: number;
  pass: boolean;
  stepMetrics: StepMetrics[];
}

export interface PipelineReport {
  totalFrames: number;
  passedFrames: number;
  failedFrames: number;
  frames: FrameReport[];
  temporalJitterScore: number;
  totalTimeMs: number;
}
