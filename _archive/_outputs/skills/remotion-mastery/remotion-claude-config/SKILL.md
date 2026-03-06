---
name: remotion-claude-config
description: CLAUDE.md configuration template and project conventions for Remotion. Provides a ready-to-paste CLAUDE.md that enforces deterministic animation rules, brand identity, spring physics presets, code organization, and performance guidelines. Use when setting up a new Remotion project for Claude Code to work on, or to establish coding standards for AI-assisted video production.
---

# CLAUDE.md and Remotion Configuration

## Purpose

Provide a complete CLAUDE.md template that configures Claude Code to produce high-quality, consistent Remotion videos. The template enforces deterministic animation logic, brand standards, project structure, and performance rules so every video Claude generates meets production quality without manual correction.

## When to Use

- Starting a new Remotion project that Claude Code will work on
- User says "set up CLAUDE.md", "configure Remotion for Claude", or "brand guidelines"
- Establishing coding standards for a Remotion video production pipeline
- Need to enforce brand colors, fonts, or animation style consistency

## Examples

**Example 1: New project setup**
```
User: "Set up CLAUDE.md for our Remotion video project"
Claude: [Uses remotion-claude-config] Generates a complete CLAUDE.md with brand colors, animation presets, file structure conventions, and deterministic animation rules. Places it in the project root.
```

**Example 2: Brand customization**
```
User: "Update CLAUDE.md with our brand colors #FF6B00 and #1D1D42"
Claude: [Uses remotion-claude-config] Updates the color palette section with the new brand colors and adjusts gradient and accent choices to complement them.
```

## CLAUDE.md Template

Copy and customize this for any Remotion project:

```markdown
# CLAUDE.md — Remotion Video Project

## Project Type
React + Remotion programmatic video generation. TypeScript only.

## Core Principle: Deterministic Animation
All visual output must be a pure function of frame number:
- ✅ ALWAYS use `useCurrentFrame()`, `interpolate()`, `spring()` for motion
- ❌ NEVER use `setTimeout`, `setInterval`, CSS `@keyframes`, or `requestAnimationFrame`
- ❌ NEVER use `Math.random()` — use `random("seed-string")` from Remotion
- ❌ NEVER use `Date.now()` or time-based logic for visual rendering

## Brand Identity

### Colors
```typescript
export const BRAND = {
  primary: "#E94560",
  secondary: "#0F3460",
  background: "#1A1A2E",
  surface: "#16213E",
  text: "#FFFFFF",
  textMuted: "#A0A8B8",
  accent: "#FF6B6B",
  success: "#00D2FF",
  gradient: ["#E94560", "#0F3460"],
} as const;
```

### Typography
- Headings: Inter (700, 900 weights)
- Body: Inter (400, 500 weights)
- Code: JetBrains Mono
- Load via Google Fonts in Root.tsx or use `@remotion/google-fonts`

### Logo
- Place logo files in `public/` directory
- Access via `staticFile("logo.svg")`

## Animation Preferences

### Default Spring Configs
```typescript
// Import from src/constants.ts
export const SPRINGS = {
  smooth: { damping: 200, stiffness: 100, mass: 1 },
  snappy: { damping: 40, stiffness: 150, mass: 1 },
  bouncy: { damping: 10, stiffness: 100, mass: 1 },
} as const;
```

### Standard Interpolation
Always use `extrapolateRight: "clamp"` to prevent value overshoot:
```typescript
interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" })
```

### Stagger Pattern
For sequential element reveals, delay each element by N frames:
```typescript
spring({ frame: frame - index * 5, fps, config: SPRINGS.smooth })
```

## Video Standards
- Default FPS: 30
- Default Resolution: 1920×1080 (landscape) or 1080×1920 (vertical)
- Default Duration: 10 seconds (300 frames at 30fps)
- Background: always set explicitly, never transparent

## Code Conventions

### File Structure
```
src/
  index.ts          # registerRoot only
  Root.tsx           # All Composition registrations
  scenes/           # One file per scene
  components/       # Shared components
  constants.ts      # Colors, springs, durations
  types.ts          # Shared TypeScript interfaces
public/             # Static assets: images, audio, fonts
```

### Component Rules
- One composition per file in `src/scenes/`
- All props must have TypeScript interfaces
- Use Zod schemas for props validated via `calculateMetadata`
- Export default props alongside component for Remotion Studio preview
- Use `AbsoluteFill` as root wrapper in every scene
- Use `Sequence` with `from` prop for timing, not conditional rendering

### Naming
- Compositions: PascalCase (`IntroScene`, `DataChart`)
- Files: PascalCase matching export (`IntroScene.tsx`)
- Props: `{ComponentName}Props` interface
- Constants: SCREAMING_SNAKE_CASE

## Performance Rules
- Prefer `transform` and `opacity` over `top`/`left`/`width`/`height` animation
- Use `useMemo()` for expensive calculations
- Use `React.memo()` for heavy sub-components
- Use `<OffthreadVideo>` instead of `<Video>` for embedded video files
- Avoid deep re-renders: keep the component tree shallow

## Assets
- All static files go in `public/`
- Access with `staticFile("filename.png")` — never use relative paths
- For images: use `<Img>` from Remotion (handles loading + errors)
- For video: use `<OffthreadVideo>` (offloads to separate thread)
- For audio: use `<Audio>` with volume prop for ducking

## Rendering
```bash
# Preview
npm start

# Render MP4
npx remotion render src/index.ts CompositionId out/video.mp4 --codec=h264 --crf=18

# Render vertical (override dimensions)
npx remotion render src/index.ts CompositionId out/reel.mp4 --width=1080 --height=1920
```
```

## Customization Guide

Adapt the template for your project:

1. **Colors**: Replace the BRAND object with your brand palette
2. **Fonts**: Change font families and add corresponding Google Font imports
3. **Springs**: Tune damping/stiffness to match your brand's motion feel
4. **FPS**: Use 60fps only for smooth motion-heavy content (doubles render time)
5. **Resolution**: Adjust defaults based on primary distribution channel

## Constants File (src/constants.ts)

Generate this alongside CLAUDE.md:

```typescript
export const BRAND = {
  primary: "#E94560",
  secondary: "#0F3460",
  background: "#1A1A2E",
  surface: "#16213E",
  text: "#FFFFFF",
  textMuted: "#A0A8B8",
  accent: "#FF6B6B",
  success: "#00D2FF",
  gradient: ["#E94560", "#0F3460"],
} as const;

export const SPRINGS = {
  smooth: { damping: 200, stiffness: 100, mass: 1 },
  snappy: { damping: 40, stiffness: 150, mass: 1 },
  bouncy: { damping: 10, stiffness: 100, mass: 1 },
  heavy: { damping: 200, stiffness: 100, mass: 2 },
  pop: { damping: 12, stiffness: 200, mass: 1 },
} as const;

export const DURATIONS = {
  quickReveal: 15,
  standardEntrance: 30,
  slowDramatic: 60,
  sceneLength: 90,
} as const;

export const STAGGER_DELAY = 5;
```

## Success Criteria

- [ ] CLAUDE.md placed in project root (same level as `package.json`)
- [ ] Brand colors, fonts, and motion preferences are defined
- [ ] Constants file created at `src/constants.ts` matching CLAUDE.md
- [ ] Deterministic animation rules are explicitly stated
- [ ] File structure conventions match project layout
- [ ] Performance constraints are documented

## Copy/Paste Ready

```
"Set up CLAUDE.md for my Remotion project"
"Create brand configuration for Remotion videos"
"Add coding standards for our video production pipeline"
"Configure Claude Code for Remotion development"
```
