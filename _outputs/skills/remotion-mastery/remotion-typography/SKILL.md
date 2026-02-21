---
name: remotion-typography
description: Text and typography animation patterns for Remotion. Builds typewriter effects, character-by-character reveals, word stagger animations, kinetic typography, TikTok-style captions, and text along SVG paths. Use when animating text, creating title cards, subtitle animations, or kinetic typography in Remotion videos.
---

# Text and Typography Animations

## Purpose

Provide complete, copy-paste text animation patterns for Remotion. Every text effect uses `useCurrentFrame()` and `spring()`/`interpolate()` to drive motion deterministically. Organize patterns by visual effect so Claude can match user intent to the right component.

## When to Use

- User requests "text animation", "title card", or "animated text"
- Building typewriter effects, kinetic typography, or subtitle animations
- User says "character reveal", "word stagger", or "text along path"
- Creating TikTok-style karaoke captions synced to audio timestamps

## Examples

**Example 1: Title card with stagger**
```
User: "Create a title card where each word fades in one by one"
Claude: [Uses remotion-typography] Creates a WordStagger component that splits text by space, wraps each word in a span with spring-delayed opacity and translateY, using staggerFrames=8 for timing.
```

**Example 2: Typewriter effect**
```
User: "Make a typewriter animation for this code snippet"
Claude: [Uses remotion-typography] Creates a Typewriter component using text.substring(0, charsToShow) with a blinking cursor span, at 15 characters per second.
```

## Typewriter Effect

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

interface TypewriterProps {
  text: string;
  charsPerSecond?: number;
}

export const Typewriter: React.FC<TypewriterProps> = ({
  text,
  charsPerSecond = 15,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const charsToShow = Math.floor((frame / fps) * charsPerSecond);
  const textToShow = text.substring(0, charsToShow);
  const cursorOpacity = Math.sin(frame * 0.5) > 0 ? 1 : 0;

  return (
    <div style={{ fontFamily: "monospace", fontSize: 60 }}>
      {textToShow}
      <span style={{ opacity: cursorOpacity }}>|</span>
    </div>
  );
};
```

## Character-by-Character Reveal

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface CharRevealProps {
  text: string;
  staggerFrames?: number;
}

export const CharReveal: React.FC<CharRevealProps> = ({
  text,
  staggerFrames = 5,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", justifyContent: "center", fontSize: 80, fontWeight: "bold" }}>
      {text.split("").map((char, i) => {
        const delay = i * staggerFrames;
        const progress = spring({
          frame: frame - delay,
          fps,
          config: { damping: 200, stiffness: 100 },
        });
        const translateY = interpolate(progress, [0, 1], [30, 0]);

        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              opacity: progress,
              transform: `translateY(${translateY}px)`,
            }}
          >
            {char === " " ? "\u00A0" : char}
          </span>
        );
      })}
    </div>
  );
};
```

## Word-by-Word Stagger

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

interface WordStaggerProps {
  text: string;
  startFrame?: number;
  staggerFrames?: number;
}

export const WordStagger: React.FC<WordStaggerProps> = ({
  text,
  startFrame = 0,
  staggerFrames = 8,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <div style={{ display: "flex", gap: 12, flexWrap: "wrap", justifyContent: "center" }}>
      {text.split(" ").map((word, i) => {
        const delay = startFrame + i * staggerFrames;
        const progress = spring({
          frame: frame - delay,
          fps,
          config: { damping: 30, stiffness: 100 },
        });
        const y = interpolate(progress, [0, 1], [20, 0]);

        return (
          <span
            key={i}
            style={{
              opacity: progress,
              transform: `translateY(${y}px)`,
              fontSize: 60,
              fontWeight: "bold",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};
```

## Kinetic Impact Text

For "slam" or "BOOM" effects where text scales down dramatically.

```tsx
import React from "react";
import { spring, useCurrentFrame, useVideoConfig, interpolate } from "remotion";

export const KineticImpact: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const spr = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 200 },
  });
  const scale = interpolate(spr, [0, 1], [3, 1]);

  return (
    <h1
      style={{
        transform: `scale(${scale})`,
        textAlign: "center",
        fontSize: 100,
        fontWeight: 900,
      }}
    >
      {text}
    </h1>
  );
};
```

## TikTok-Style Captions

Highlights words as they are spoken. Requires word-level timestamps (from subtitles or ElevenLabs).

```tsx
import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

interface CaptionWord {
  word: string;
  start: number;
  end: number;
}

interface CaptionsProps {
  words: CaptionWord[];
}

export const Captions: React.FC<CaptionsProps> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const time = frame / fps;

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center" }}>
      {words.map((w, i) => {
        const isActive = time >= w.start && time <= w.end;
        const scale = isActive
          ? spring({
              frame: frame - w.start * fps,
              fps,
              config: { damping: 200 },
            })
          : 0;

        return (
          <span
            key={i}
            style={{
              color: isActive ? "#E94560" : "#FFFFFF",
              transform: isActive ? `scale(${1 + scale * 0.15})` : "scale(1)",
              display: "inline-block",
              fontSize: 48,
              fontWeight: "bold",
            }}
          >
            {w.word}
          </span>
        );
      })}
    </div>
  );
};
```

## Text Along SVG Path

Animate text flowing along a curve by driving `startOffset`.

```tsx
import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const TextOnPath: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const startOffset =
    interpolate(frame, [0, durationInFrames], [0, 100], {
      extrapolateRight: "clamp",
    }) + "%";

  return (
    <svg viewBox="0 0 1000 300" width="100%">
      <path id="curve" d="M 50 150 Q 500 0 950 150" fill="transparent" />
      <text style={{ fontSize: 50, fill: "white" }}>
        <textPath href="#curve" startOffset={startOffset}>
          {text}
        </textPath>
      </text>
    </svg>
  );
};
```

For the complete spring parameter reference, see the motion vocabulary table in `remotion-fundamentals/references/motion-vocabulary.md`.

## Success Criteria

- [ ] All text animations driven by useCurrentFrame — zero CSS @keyframes
- [ ] Character/word staggers use spring with frame offset, not setTimeout
- [ ] Typewriter uses substring math, not DOM manipulation
- [ ] All components export proper TypeScript interfaces for props
- [ ] Caption components accept timestamp arrays, not hardcoded values

## Copy/Paste Ready

```
"Create a typewriter animation for this text"
"Animate the title with word-by-word stagger"
"Build a kinetic typography slam effect"
"Add TikTok-style animated captions to my video"
"Make text flow along a curved path"
```
