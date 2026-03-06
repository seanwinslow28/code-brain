# Motion Vocabulary Reference

## Spring Parameter Configs

Use these tested `spring()` config values to achieve specific motion feels.

| Feel | damping | stiffness | mass | Use Case |
|------|---------|-----------|------|----------|
| Smooth / Elegant | 200 | 100 | 1 | Corporate intros, luxury branding, professional motion |
| Snappy | 40 | 150 | 1 | Tech demos, UI element reveals, fast energetic motion |
| Bouncy / Playful | 10 | 100 | 1 | Fun content, emphasis, cartoons, social media |
| Heavy / Cinematic | 200 | 100 | 2 | Slow dramatic zoom, product hero shots, weight |
| Pop / Impact | 12 | 200 | 1 | Text slam, logo bounce, attention-grabbing entrance |
| Gentle Float | 30 | 50 | 1 | Subtle background motion, ambient elements |

## Usage Pattern

```tsx
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

// Smooth entrance (no bounce)
const smooth = spring({
  frame,
  fps,
  config: { damping: 200, stiffness: 100, mass: 1 },
});

// Bouncy pop
const bouncy = spring({
  frame,
  fps,
  config: { damping: 10, stiffness: 100, mass: 1 },
});

// Heavy cinematic zoom
const cinematic = spring({
  frame,
  fps,
  config: { damping: 200, stiffness: 100, mass: 2 },
});
```

## Easing Module Reference

For non-spring animations, use `Easing` with `interpolate()`.

| Easing Function | Effect | Example Use |
|----------------|--------|-------------|
| `Easing.linear` | Constant speed | Progress bars, tickers |
| `Easing.ease` | CSS ease equivalent | General purpose |
| `Easing.in(Easing.ease)` | Slow start | Exit animations |
| `Easing.out(Easing.ease)` | Slow end | Entry animations |
| `Easing.inOut(Easing.ease)` | Slow both ends | Smooth transitions |
| `Easing.bezier(0.4, 0, 0.2, 1)` | Material Design curve | Cinematic feel |
| `Easing.bounce` | Bounce at end | Playful landing |
| `Easing.elastic(1)` | Overshoot + settle | Attention-grabbing |
| `Easing.back(1.5)` | Pull back then forward | Anticipation effect |

## Usage with interpolate

```tsx
import { interpolate, Easing, useCurrentFrame } from "remotion";

const frame = useCurrentFrame();

// Cinematic ease (Material Design motion)
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
  easing: Easing.bezier(0.4, 0, 0.2, 1),
});

// Bounce landing
const y = interpolate(frame, [0, 30], [100, 0], {
  extrapolateRight: "clamp",
  easing: Easing.bounce,
});
```

## When to Use Spring vs Easing

- **Spring**: Default choice. Natural motion, no fixed duration required.
- **Easing + interpolate**: When you need exact frame-count duration or CSS-like curves.
- **Rule**: If it should feel organic, use spring. If it must hit a precise frame, use interpolate + Easing.
