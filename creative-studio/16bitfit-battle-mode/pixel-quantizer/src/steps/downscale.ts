/** Step 1: Nearest-neighbor downscale to target size. */

import sharp from 'sharp';

export async function downscale(
  inputBuffer: Buffer,
  targetSize: number,
): Promise<Buffer> {
  return sharp(inputBuffer)
    .resize(targetSize, targetSize, {
      kernel: sharp.kernel.nearest,
      fit: 'fill',
    })
    .raw()
    .toBuffer();
}

export async function downscaleToRaw(
  inputBuffer: Buffer,
  targetSize: number,
): Promise<{ data: Buffer; info: sharp.OutputInfo }> {
  return sharp(inputBuffer)
    .resize(targetSize, targetSize, {
      kernel: sharp.kernel.nearest,
      fit: 'fill',
    })
    .ensureAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });
}
