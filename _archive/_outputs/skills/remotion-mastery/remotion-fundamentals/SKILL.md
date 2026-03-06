---
name: remotion-fundamentals
description: Remotion project setup and core animation fundamentals. Creates new video projects, registers Compositions, animates with useCurrentFrame, spring, and interpolate, nests Sequences for timing, and renders to MP4. Use when building a Remotion project from scratch, setting up compositions, or needing core animation patterns.
---

# Remotion Fundamentals and Project Setup

## Purpose

Bootstrap and structure Remotion video projects using frame-based thinking. Provide the core mental model, essential hooks, animation primitives, and the complete create-to-render workflow so Claude can scaffold production-ready video code in TypeScript.

## When to Use

- User says "create a video", "new Remotion project", or "programmatic video"
- Setting up Root.tsx with Composition registrations
- Writing any component that uses useCurrentFrame or spring
- Explaining frame-based animation to a beginner
- Rendering a composition to MP4 or other format

## Examples

**Example 1: New project scaffold**
```
User: "Create a new Remotion project for a product demo video"
Claude: [Uses remotion-fundamentals] Scaffolds project with npx create-video@latest, creates Root.tsx with a ProductDemo composition (1920x1080, 30fps, 300 frames), and generates a starter component using useCurrentFrame with spring-based fade-in.
```

**Example 2: Adding a composition**
```
User: "Add a 15-second intro scene to my Remotion project"
Claude: [Uses remotion-fundamentals] Creates src/scenes/Intro.tsx with useCurrentFrame/spring animations, registers it in Root.tsx as a Composition with id="Intro", durationInFrames={450}, fps={30}, width={1920}, height={1080}.
```

**Example 3: Rendering**
```
User: "Render my video to MP4"
Claude: [Uses remotion-fundamentals] Runs: npx remotion render src/index.ts MyComposition out/video.mp4 --codec=h264
```

## Core Mental Model

Remotion renders video as a function of frame number. Your React component receives a frame integer and returns the visual state for that frame. There is no timeline, no playhead — only `frame / fps = time`.

Rules:
- Drive ALL motion from `useCurrentFrame()` — never `useEffect`, `setTimeout`, or CSS `@keyframes`
- Components must be deterministic: same frame number = same output
- Use Remotion's `random("seed")` instead of `Math.random()`
- Use `staticFile("asset.png")` for files in `public/`

## Project Structure

```
my-video/
  src/
    index.ts          # registerRoot(RemotionRoot)
    Root.tsx           # Composition registrations
    scenes/            # One file per scene/composition
      Intro.tsx
      MainContent.tsx
    components/        # Shared reusable components
      Title.tsx
      Logo.tsx
    constants.ts       # Brand colors, spring configs
  public/              # Static assets (images, audio, fonts)
  remotion.config.ts   # Remotion configuration
```

## Workflow

```bash
# 1. Create project
npx create-video@latest

# 2. Preview in Remotion Studio
npm start
# Opens http://localhost:3000 with frame scrubber

# 3. Render to file
npx remotion render src/index.ts MyComposition out/video.mp4
```

## Composition Registration

```tsx
import { Composition } from "remotion";
import { Intro } from "./scenes/Intro";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Intro"
        component={Intro}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Hello Remotion",
          primaryColor: "#E94560",
        }}
      />
    </>
  );
};
```

Key Composition props: `id` (CLI render target), `component`, `durationInFrames`, `fps`, `width`, `height`, `defaultProps`.

## Essential Hooks

```tsx
const frame = useCurrentFrame();           // Current frame (relative to Sequence)
const { fps, width, height, durationInFrames } = useVideoConfig();
```

## Animation: interpolate

Map frame ranges to CSS values. Always clamp to prevent runaway values.

```tsx
import { interpolate, useCurrentFrame, Easing } from "remotion";

const frame = useCurrentFrame();

const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: "clamp",
});

const translateY = interpolate(frame, [0, 30], [50, 0], {
  extrapolateRight: "clamp",
  easing: Easing.out(Easing.ease),
});
```

## Animation: spring

Physics-based motion. Prefer spring over linear interpolation for natural feel.

```tsx
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({
  frame,
  fps,
  config: { damping: 200, stiffness: 100, mass: 1 },
});
```

For the spring parameter reference table, see `references/motion-vocabulary.md`.

## Sequencing and Layout

```tsx
import { Sequence, Series, AbsoluteFill } from "remotion";

// Sequence: offset children by frame number
<Sequence from={30} durationInFrames={60}>
  <Title text="Hello" />   {/* useCurrentFrame() returns 0 when global frame = 30 */}
</Sequence>

// Series: auto-chain sequences back-to-back
<Series>
  <Series.Sequence durationInFrames={60}><SceneA /></Series.Sequence>
  <Series.Sequence durationInFrames={60}><SceneB /></Series.Sequence>
</Series>

// AbsoluteFill: full-viewport positioning layer
<AbsoluteFill style={{ backgroundColor: "#1A1A2E" }}>
  {/* content */}
</AbsoluteFill>
```

## Complete Starter Component

```tsx
import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
} from "remotion";

interface IntroProps {
  title: string;
  primaryColor: string;
}

export const Intro: React.FC<IntroProps> = ({ title, primaryColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [0, 20], [30, 0], {
    extrapolateRight: "clamp",
  });

  const subtitleScale = spring({
    frame: frame - 15,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: primaryColor,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Sequence from={0}>
        <h1
          style={{
            opacity: titleOpacity,
            transform: `translateY(${titleY}px)`,
            color: "#FFFFFF",
            fontSize: 80,
            fontWeight: "bold",
          }}
        >
          {title}
        </h1>
      </Sequence>

      <Sequence from={15}>
        <p
          style={{
            transform: `scale(${subtitleScale})`,
            color: "#FFFFFF",
            fontSize: 40,
          }}
        >
          Powered by Remotion
        </p>
      </Sequence>
    </AbsoluteFill>
  );
};
```

Query the `remotion-docs` MCP server for current API syntax when using newer Remotion v4+ features.

## Success Criteria

- [ ] Project uses `npx create-video@latest` for scaffolding
- [ ] All animations driven by `useCurrentFrame()` — zero CSS animations or setTimeout
- [ ] All interpolations use `extrapolateRight: "clamp"`
- [ ] Compositions registered in Root.tsx with explicit fps, dimensions, and duration
- [ ] One file per scene in `src/scenes/`
- [ ] Renders successfully with `npx remotion render`

## Copy/Paste Ready

```
"Create a new Remotion video project"
"Set up a Remotion composition for a 30-second explainer"
"Add a spring animation to this Remotion component"
"Render my Remotion video to MP4"
"How does useCurrentFrame work in Remotion?"
```
