/** Step 6: Grid alignment — snap sprite to consistent baseline within the canvas. */

/**
 * Detect the bottom edge of the sprite and shift it so feet align
 * to a consistent baseline across all frames.
 *
 * @param frames Array of raw RGBA buffers
 * @param width Frame width
 * @param height Frame height
 * @param targetBaseline Target baseline row (auto-detected from mode if not given)
 * @returns Aligned frames + per-frame drift values
 */
export function gridAlign(
  frames: Buffer[],
  width: number,
  height: number,
  targetBaseline?: number,
): { frames: Buffer[]; driftValues: number[] } {
  const channels = 4;

  // Detect bottom edge for each frame
  const bottomEdges: number[] = frames.map((frame) => {
    for (let y = height - 1; y >= 0; y--) {
      for (let x = 0; x < width; x++) {
        const offset = (y * width + x) * channels;
        if (frame[offset + 3] > 0) return y;
      }
    }
    return 0; // Fully transparent frame
  });

  // Use mode of bottom edges as target baseline (or provided value)
  if (targetBaseline === undefined) {
    const counts = new Map<number, number>();
    for (const edge of bottomEdges) {
      counts.set(edge, (counts.get(edge) ?? 0) + 1);
    }
    let maxCount = 0;
    targetBaseline = bottomEdges[0] ?? height - 1;
    for (const [edge, count] of counts) {
      if (count > maxCount) {
        maxCount = count;
        targetBaseline = edge;
      }
    }
  }

  const driftValues: number[] = [];

  for (let i = 0; i < frames.length; i++) {
    const drift = targetBaseline - bottomEdges[i];
    driftValues.push(drift);

    if (drift === 0) continue;

    const frame = frames[i];
    const aligned = Buffer.alloc(frame.length); // Start transparent

    if (drift > 0) {
      // Shift down: copy from top to bottom
      for (let y = height - 1; y >= drift; y--) {
        const srcOffset = (y - drift) * width * channels;
        const dstOffset = y * width * channels;
        frame.copy(aligned, dstOffset, srcOffset, srcOffset + width * channels);
      }
    } else {
      // Shift up: copy from bottom to top
      const absDrift = Math.abs(drift);
      for (let y = 0; y < height - absDrift; y++) {
        const srcOffset = (y + absDrift) * width * channels;
        const dstOffset = y * width * channels;
        frame.copy(aligned, dstOffset, srcOffset, srcOffset + width * channels);
      }
    }

    aligned.copy(frame);
  }

  return { frames, driftValues };
}
