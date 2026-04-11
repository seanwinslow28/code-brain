import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import type { PaletteColor } from '../types.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

const BUILT_IN: Record<string, string> = {
  sean: resolve(__dirname, 'sean.json'),
  sf2_pixel_art: resolve(__dirname, 'sf2_pixel_art.json'),
};

export function loadPalette(nameOrPath: string): PaletteColor[] {
  const filePath = BUILT_IN[nameOrPath] ?? resolve(nameOrPath);
  const raw = JSON.parse(readFileSync(filePath, 'utf-8'));
  return raw as PaletteColor[];
}

export function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const h = hex.replace('#', '');
  return {
    r: parseInt(h.slice(0, 2), 16),
    g: parseInt(h.slice(2, 4), 16),
    b: parseInt(h.slice(4, 6), 16),
  };
}
