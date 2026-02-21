---
name: remotion-troubleshooting
description: Troubleshooting common Remotion errors and performance optimization. Covers timeout debugging (delayRender), version compatibility, asset path issues, React rendering optimizations (useMemo, React.memo, OffthreadVideo), memory issues, verbose logging, and working with Claude Code effectively. Use when a Remotion project has build errors, rendering is slow, or components misbehave.
---

# Troubleshooting and Performance

## Purpose

Diagnose and fix common Remotion errors, optimize rendering performance, and configure Claude Code to work effectively with Remotion projects. Provides a decision-tree approach to debugging so Claude can rapidly identify and resolve issues.

## When to Use

- User reports a Remotion error, crash, or timeout
- Rendering is slow or memory usage is high
- User says "delayRender timeout", "black frame", or "render fails"
- Optimizing render speed for production pipelines
- Setting up Remotion development with Claude Code

## Examples

**Example 1: Timeout error**
```
User: "I'm getting a delayRender timeout error"
Claude: [Uses remotion-troubleshooting] Checks for missing continueRender calls, unresolved fetch promises, and asset loading failures. Adds timeout parameter and error handling to the identified delayRender call.
```

**Example 2: Slow render**
```
User: "My render is taking 20+ minutes for a 30 second video"
Claude: [Uses remotion-troubleshooting] Audits for layout-thrashing CSS properties, switches to OffthreadVideo, adds useMemo for calculations, and wraps heavy sub-components in React.memo.
```

## Error Decision Tree

```
Render fails?
├── "delayRender() timed out"
│   ├── Check: continueRender() called for every delayRender()
│   ├── Check: fetch() has error handling + cancelRender()
│   ├── Fix: Increase timeout → delayRender("Loading", { timeoutInMilliseconds: 30000 })
│   └── Debug: Add console.log before each continueRender
│
├── "could not find an element with id"
│   ├── Check: Root.tsx has registerRoot(RemotionRoot)
│   └── Check: index.ts imports and calls registerRoot
│
├── "Cannot use Composition outside Root"
│   └── Fix: Only use <Composition> inside the registered Root component
│
├── Black/blank frames
│   ├── Check: AbsoluteFill has explicit backgroundColor
│   ├── Check: Assets loaded correctly (staticFile paths exist in public/)
│   └── Check: Conditional rendering gates aren't hiding content
│
├── "Module not found"
│   ├── Check: Remotion version matches package versions
│   ├── Fix: npx remotion upgrade (upgrades all @remotion/* packages in sync)
│   └── Check: Bundler config in remotion.config.ts
│
└── Visual glitches (flickering, jumps)
    ├── Check: All interpolations have extrapolateRight: "clamp"
    ├── Check: No CSS @keyframes or transitions used
    └── Check: No useState for visual state (use frame math instead)
```

## Verbose Debugging

```bash
# Render with verbose output
npx remotion render src/index.ts MyComp out/debug.mp4 --log=verbose

# Frame-by-frame inspection in Studio
npm start
# Use the frame scrubber slider to step through individual frames

# Check Remotion version
npx remotion --version

# Upgrade all Remotion packages atomically
npx remotion upgrade
```

## delayRender Patterns

### Correct Pattern

```tsx
import { useState, useEffect } from "react";
import { delayRender, continueRender, cancelRender, staticFile } from "remotion";

export const DataScene: React.FC = () => {
  const [handle] = useState(() => delayRender("Loading data", {
    timeoutInMilliseconds: 15000,
  }));
  const [data, setData] = useState<unknown>(null);

  useEffect(() => {
    fetch(staticFile("data.json"))
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        setData(json);
        continueRender(handle);
      })
      .catch((err) => {
        console.error("Data load failed:", err);
        cancelRender(err);
      });
  }, [handle]);

  if (!data) return null;
  return <div>{/* render data */}</div>;
};
```

### Common Mistakes

```tsx
// ❌ Missing continueRender — will always timeout
const [handle] = useState(() => delayRender());
useEffect(() => {
  fetch(url).then(/* ... no continueRender call */);
}, []);

// ❌ No error handling — silently hangs on failure
fetch(url).then(res => res.json()).then(data => continueRender(handle));

// ✅ Always pair delayRender with both continueRender AND error handling
```

## Performance Optimization

### CSS Property Performance Tiers

| Tier | Properties | Performance |
|------|-----------|-------------|
| **Fast** (compositor) | `transform`, `opacity` | GPU-accelerated, no layout recalc |
| **Medium** (paint) | `color`, `background-color`, `box-shadow` | Repaint only |
| **Slow** (layout) | `width`, `height`, `top`, `left`, `margin`, `padding` | Full layout recalculation |

RULE: Animate only `transform` and `opacity`. Move position with `translateX/Y/Z`, scale with `scale()`, rotate with `rotate()`.

```tsx
// ❌ SLOW: Animating layout properties
<div style={{ width: `${interpolatedWidth}px`, left: `${interpolatedX}px` }} />

// ✅ FAST: Animating transform + opacity
<div style={{
  transform: `translateX(${x}px) scale(${s})`,
  opacity: o,
}} />
```

### React Optimizations

```tsx
import React, { useMemo } from "react";

// useMemo for expensive calculations
const chartPoints = useMemo(() => {
  return data.map((d, i) => ({
    x: (i / data.length) * width,
    y: height - (d.value / maxValue) * height,
  }));
}, [data, width, height]); // Only recalculate when inputs change

// React.memo for heavy sub-components
const HeavyChart = React.memo<{ data: number[] }>(({ data }) => {
  // Complex SVG rendering
  return <svg>{/* ... */}</svg>;
});
```

### Media Optimizations

```tsx
import { OffthreadVideo, Img, staticFile } from "remotion";

// ✅ OffthreadVideo: decodes video in separate thread
<OffthreadVideo src={staticFile("background.mp4")} />

// ❌ Video: decodes in main thread, can cause frame drops
// <Video src={staticFile("background.mp4")} />

// ✅ Img: handles loading and error states
<Img src={staticFile("photo.jpg")} style={{ width: "100%" }} />
```

### Memory Management

- Avoid loading all data frames into memory at once — paginate or stream
- Use `--concurrency=2` for renders on memory-limited machines
- Large Lottie files: load each animation individually with delayRender, not all at once

## Working with Claude Code

### Strengths
Claude Code works well for:
- Generating Remotion compositions from scratch
- Writing type-safe props and Zod schemas
- Creating spring/interpolate animation logic
- Building data-driven chart components
- Setting up multi-scene TransitionSeries videos

### Common Mistakes to Correct
When Claude Code generates Remotion code, watch for:

| Mistake | Fix |
|---------|-----|
| Uses CSS `@keyframes` | Replace with interpolate/spring |
| Uses `Math.random()` | Replace with `random("seed")` |
| Uses `setTimeout` | Replace with Sequence + frame math |
| Uses relative image paths | Use `staticFile("name.png")` |
| Missing `extrapolateRight: "clamp"` | Add to all interpolate calls |
| Uses `<Video>` tag | Replace with `<OffthreadVideo>` |
| Missing error handling in data fetch | Add cancelRender in catch block |

### Version Compatibility

Keep all `@remotion/*` packages at the same version. Check with:

```bash
npm ls | grep @remotion
```

If versions are mismatched:

```bash
npx remotion upgrade
```

## Mediabunny Migration Note

`@remotion/media-parser` is deprecated and migrated to the Mediabunny standalone package. If you encounter import errors from `@remotion/media-parser`, check the Remotion docs MCP server for the migration path.

## Success Criteria

- [ ] delayRender always paired with continueRender + cancelRender (error)
- [ ] No layout-thrashing CSS properties animated
- [ ] Heavy sub-components wrapped in React.memo
- [ ] OffthreadVideo used instead of Video for media playback
- [ ] All @remotion/* packages at matching versions
- [ ] Verbose logging enabled when debugging render failures

## Copy/Paste Ready

```
"Fix this delayRender timeout error"
"Why is my Remotion render so slow?"
"Debug blank frames in my Remotion video"
"Optimize my Remotion project for render speed"
"Fix version mismatch errors in Remotion"
```
