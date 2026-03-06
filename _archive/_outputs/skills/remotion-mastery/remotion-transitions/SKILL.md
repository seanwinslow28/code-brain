---
name: remotion-transitions
description: Scene transitions and multi-scene composition orchestration for Remotion. Uses the @remotion/transitions package with TransitionSeries, presentations (fade, slide, wipe, flip, clockWipe, iris, none), timing presets, and overlays. Use when building multi-scene videos, explainer videos, or adding transitions between scenes in Remotion.
---

# Transitions and Multi-Scene Compositions

## Purpose

Orchestrate multi-scene Remotion videos using the `@remotion/transitions` package. Provide the complete API for TransitionSeries, all built-in presentations, timing options, overlays, and entry/exit choreography so Claude can build polished scene flows without manual frame math.

## When to Use

- User says "transition", "scene change", or "multi-scene video"
- Building explainer videos, presentation videos, or any content with multiple scenes
- User needs fade, slide, wipe, or other transition effects between scenes
- Planning scene timing and orchestration

## Examples

**Example 1: Multi-scene explainer**
```
User: "Create a 3-scene explainer video with slide transitions"
Claude: [Uses remotion-transitions] Creates a TransitionSeries with 3 sequences using slide({ direction: "from-right" }) transitions with springTiming, entry fade-in, and exit fade-out.
```

**Example 2: Adding a transition**
```
User: "Add a wipe transition between my intro and main content"
Claude: [Uses remotion-transitions] Inserts a TransitionSeries.Transition with wipe({ direction: "from-top" }) and linearTiming({ durationInFrames: 30 }) between the two sequences.
```

## TransitionSeries Basics

```tsx
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

export const MyVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={60}>
        <SceneA />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 30 })}
      />

      <TransitionSeries.Sequence durationInFrames={60}>
        <SceneB />
      </TransitionSeries.Sequence>
    </TransitionSeries>
  );
};
```

## Timing Math

Transitions overlap adjacent scenes, shortening total duration:

`Total = Duration(A) + Duration(B) - Duration(Transition)`

Example: Scene A (60f) + Scene B (60f) with 30f transition = 90 total frames.

Rules:
- A transition cannot exceed the duration of adjacent sequences
- Two transitions cannot be placed next to each other

## Presentations Reference

| Presentation | Import | Props | Description |
|-------------|--------|-------|-------------|
| `fade()` | `@remotion/transitions/fade` | none | Crossfade opacity |
| `slide()` | `@remotion/transitions/slide` | `direction` | Push old scene out, slide new in |
| `wipe()` | `@remotion/transitions/wipe` | `direction` | Linear reveal |
| `flip()` | `@remotion/transitions/flip` | none | 3D card flip |
| `clockWipe()` | `@remotion/transitions/clock-wipe` | none | Radial clock-hand reveal |
| `iris()` | `@remotion/transitions/iris` | none | Circular mask from center |
| `none()` | `@remotion/transitions/none` | none | Instant hard cut |

Direction options for slide/wipe: `"from-left"`, `"from-right"`, `"from-top"`, `"from-bottom"`.

## Timing Options

```tsx
import { linearTiming, springTiming } from "@remotion/transitions";

// Fixed duration, constant speed
const linear = linearTiming({ durationInFrames: 30 });

// Physics-based, natural snap
const spring = springTiming({
  config: { damping: 200, stiffness: 100 },
  durationInFrames: 30,
  durationRestThreshold: 0.001,
});

// Get exact frame count from spring timing
const exactFrames = spring.getDurationInFrames({ fps: 30 });
```

Set a low `durationRestThreshold` (0.001) to prevent abrupt cutoff at end of spring.

## Overlays (v4.0.415+)

Overlays add effects ON TOP of a scene cut without shortening the timeline.

```tsx
import { TransitionSeries } from "@remotion/transitions";
import { AbsoluteFill } from "remotion";

const FlashOverlay: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "white" }} />
);

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneA />
  </TransitionSeries.Sequence>

  <TransitionSeries.Overlay durationInFrames={10}>
    <FlashOverlay />
  </TransitionSeries.Overlay>

  <TransitionSeries.Sequence durationInFrames={60}>
    <SceneB />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

## Entry and Exit Animations

Place a Transition as the first or last child to animate the video's open/close.

```tsx
<TransitionSeries>
  {/* Entry: fade in from black */}
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 20 })}
  />

  <TransitionSeries.Sequence durationInFrames={100}>
    <MainContent />
  </TransitionSeries.Sequence>

  {/* Exit: fade out to black */}
  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 20 })}
  />
</TransitionSeries>
```

## Complete Multi-Scene Example

```tsx
import React from "react";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";

const Scene: React.FC<{ color: string; text: string }> = ({ color, text }) => (
  <AbsoluteFill
    style={{ backgroundColor: color, justifyContent: "center", alignItems: "center" }}
  >
    <h1 style={{ color: "white", fontSize: 80 }}>{text}</h1>
  </AbsoluteFill>
);

export const ExplainerVideo: React.FC = () => {
  return (
    <TransitionSeries>
      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 20 })}
      />

      <TransitionSeries.Sequence durationInFrames={90}>
        <Scene color="#1A1A2E" text="The Problem" />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={slide({ direction: "from-right" })}
        timing={springTiming({
          config: { damping: 200, stiffness: 100 },
          durationInFrames: 40,
        })}
      />

      <TransitionSeries.Sequence durationInFrames={90}>
        <Scene color="#0F3460" text="Our Solution" />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={wipe({ direction: "from-top" })}
        timing={linearTiming({ durationInFrames: 30 })}
      />

      <TransitionSeries.Sequence durationInFrames={90}>
        <Scene color="#E94560" text="Get Started" />
      </TransitionSeries.Sequence>

      <TransitionSeries.Transition
        presentation={fade()}
        timing={linearTiming({ durationInFrames: 30 })}
      />
    </TransitionSeries>
  );
};
```

Query the `remotion-docs` MCP server for the latest transition API changes in Remotion v4+.

## Success Criteria

- [ ] Multi-scene videos use TransitionSeries, not manual Sequence from-prop math
- [ ] Transitions placed between sequences with explicit timing
- [ ] Entry/exit animations placed as first/last TransitionSeries children
- [ ] Overlays used for effects that should not shorten timeline
- [ ] Spring timings use durationRestThreshold: 0.001 to prevent cutoff

## Copy/Paste Ready

```
"Create a multi-scene video with transitions"
"Add a slide transition between these two scenes"
"Build an explainer video with fade in, content scenes, and fade out"
"Add a flash overlay between scene cuts"
"Create a presentation video with wipe transitions"
```
