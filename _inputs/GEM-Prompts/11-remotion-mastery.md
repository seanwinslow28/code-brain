# Remotion Mastery - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Remotion Mastery"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at The Block (crypto data/news company). I'm a beginner coder learning fundamentals. I want to use Claude Code + Remotion to create professional programmatic videos entirely through conversation: product demos, data visualizations, social media content, and game trailers. My stack is React, Python, Supabase. I have the `remotion-docs` MCP server installed globally on my Mac.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers mastering **Remotion for AI-assisted programmatic video creation**.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Remotion Mastery") contains deep research on the Remotion framework with Claude Code: core architecture (Compositions, Sequences, useCurrentFrame, spring/interpolate), the Remotion MCP server (@remotion/mcp), agent skills (remotion-best-practices), animation techniques (text, shapes, data viz, images, 3D, particles), professional video patterns (intros, social media formats, presentations), rendering and output options (codecs, Lambda, GIF, client-side), advanced patterns (multi-composition projects, AI media generation, dynamic data), and integration with my stack (Tailwind, Figma, ElevenLabs, ComfyUI, Phaser). Sources include Remotion official docs, community starter kits, case studies, and tutorial content.

## Your Task

Analyze all sources in this notebook and generate **6-8 Claude Skills** that make Claude Code a Remotion video production studio. The goal: I describe a video and Claude writes the React/TypeScript code that renders it — with correct timing, beautiful motion, and professional quality.

## Target Skills to Extract

### 1. Remotion Fundamentals & Project Setup
**Priority**: High
**What to extract**: Core mental model (frame-based thinking — you get a frame number and render React), Composition registration in Root.tsx, useCurrentFrame() and fps usage, spring() parameters and the interpolate() function, the Easing module (bezier, elastic, bounce, back), Sequence nesting with `from` prop for timing, project structure conventions (one composition per file, shared components in src/components/, constants in src/constants.ts), and the complete workflow: `npx create-video@latest` → code → `npm start` (preview) → `npx remotion render` (output).
**Trigger phrases**: "Remotion", "create a video", "programmatic video", "video project", "new Remotion project"

### 2. Text & Typography Animations
**Priority**: High
**What to extract**: Character-by-character reveals, word-by-word stagger animations, typewriter effects, kinetic typography, text along paths, animated captions/subtitles, fade + slide entry patterns, and the motion vocabulary: bouncy (`stiffness: 300, damping: 10`), smooth (`stiffness: 100, damping: 30`), snappy (`stiffness: 500, damping: 30`), cinematic (`Easing.bezier(0.4, 0, 0.2, 1)`). Include copy-paste patterns for each.
**Trigger phrases**: "text animation", "title card", "kinetic typography", "animated text", "typewriter", "subtitle animation"

### 3. Data Visualization Animations
**Priority**: High
**What to extract**: Animated bar charts (bars growing from zero), line chart drawing (path animation), pie/donut chart reveals, counter animations (number counting up), progress bars, comparison graphics (before/after, A vs B), and crypto-specific patterns: price chart animations, market cap comparisons, volume visualizations, portfolio performance reviews. Include patterns for feeding real data (API responses, JSON) into Remotion compositions.
**Trigger phrases**: "data visualization", "chart animation", "animated chart", "crypto data video", "market data", "metrics video", "counter animation"

### 4. Transitions & Multi-Scene Compositions
**Priority**: High
**What to extract**: The @remotion/transitions package: TransitionSeries component, all presentations (fade, slide, wipe, flip, clockWipe, iris, cube, none), timing presets, TransitionSeries.Overlay. Multi-scene orchestration: scene planning, timing math (when each scene starts/ends), shared state between scenes, and entry/exit choreography. The scene description pattern: what appears → how it enters → how long it stays → how it exits → what follows.
**Trigger phrases**: "transition", "scene change", "multi-scene", "video with scenes", "explainer video", "presentation video"

### 5. Social Media & Output Formats
**Priority**: Medium
**What to extract**: Format specifications for each platform: Instagram Reels/Stories (1080x1920, 9:16), YouTube Shorts (1080x1920), Twitter/X video (1280x720 or 1080x1080), LinkedIn (1920x1080), TikTok (1080x1920). Rendering command: `npx remotion render [composition] [output] --codec h264`. GIF creation (native GIF output, reduced fps for file size, 480px max width). Multi-format rendering from single compositions. Encoding settings for quality/size tradeoffs per platform.
**Trigger phrases**: "social media video", "Instagram Reel", "YouTube Short", "TikTok", "GIF", "render video", "output format", "video format"

### 6. CLAUDE.md & Remotion Configuration
**Priority**: Medium
**What to extract**: The complete CLAUDE.md template for Remotion projects: brand colors, animation preferences (default spring, text entrance style, scene transitions, things to never use), video standards (fps, resolution, social formats, GIF max), code conventions (file per composition, shared components path, TypeScript interfaces for props), interaction patterns (video entrance, scene transitions, text reveals, data point animations, exit animations), and performance rules (avoid box-shadow/blur in animated elements, use transform/opacity, memoize calculations, frame render time budget).
**Trigger phrases**: "Remotion CLAUDE.md", "configure Remotion project", "Remotion settings", "brand guidelines for video"

### 7. Advanced Patterns: Audio, 3D, and AI Media
**Priority**: Lower
**What to extract**: Audio integration (Audio component, per-frame volume control, syncing to music beats, ElevenLabs voiceover integration), 3D graphics (@remotion/three package, ThreeCanvas, React Three Fiber with useCurrentFrame()), AI media generation (remotion-media-mcp for AI images/videos/music, feeding AI-generated assets into compositions), and parametrized video templates (Input Props, calculateMetadata, dataset rendering for batch video generation).
**Trigger phrases**: "audio sync", "voiceover", "3D animation", "three.js", "AI generated assets", "batch video", "template video", "parametrized video"

### 8. Troubleshooting & Performance
**Priority**: Lower
**What to extract**: Common Remotion errors with Claude Code (version mismatch across @remotion/* packages, FFmpeg/FFprobe requirements, rendering failures), what Claude Code does well vs poorly with Remotion (clean: text, simple transitions, data viz; messy: overlapping complex animations, precise timing), debugging in Remotion Studio (frame-by-frame inspection, console logging within compositions), performance optimization (--log=verbose for slow frames, --open-perf-monitor, concurrency tuning, React.memo/useMemo), and the Mediabunny migration from Media Parser (February 2026).
**Trigger phrases**: "Remotion error", "render failed", "slow rendering", "performance", "version mismatch", "debugging Remotion"

## Extraction Guidance

- **Frame-based thinking**: Remotion is NOT a timeline editor. Skills should help Claude (and me) think in frames: "at frame 30, the title is fully visible" rather than "at 1 second."
- **Spring > linear**: Default to spring() animations for natural motion. Linear/easing should be explicitly justified when used.
- **The MCP server matters**: The `remotion-docs` MCP server gives Claude access to current Remotion documentation. Skills should reference this and remind Claude to use it for API details.
- **Copy-paste patterns**: Every animation technique should include actual TypeScript/React code that works in a Remotion project. No pseudocode.
- **Iteration is normal**: Sources say 4-6 turns typically produce a polished video. Skills should optimize for this loop, not try to eliminate it.
- **Remotion v4+**: Only include patterns for Remotion v4 and later. The Rust binary, static Studio export, and Mediabunny are all v4+ features.
- **TypeScript**: All code should be TypeScript, not JavaScript. Use proper interfaces for props.
- **The Block branding**: Include The Block's colors (Primary #1A1A2E, Accent #E94560, Background #0F3460, Text #FFFFFF) as default brand context in the configuration skill.

## Cross-Domain Notes

- **Fundamentals** connect to Technical Stack (React/TypeScript) and Core Features (MCP server setup)
- **Text Animations** connect to Master Designer (animation library patterns, spring parameters)
- **Data Visualization** connects to PM Workflows (metrics reporting), Domain Specific (crypto data), and Life Optimization (finance visualizations)
- **Social Media Formats** connect to PM Workflows (stakeholder communication) and Creative Projects (game trailers)
- **CLAUDE.md** connects to Advanced Techniques (CLAUDE.md optimization) and Core Features (configuration management)
- **Audio/AI Media** connects to Creative Projects (ElevenLabs, ComfyUI integration) and Domain Specific (AI-native products)
- **Troubleshooting** connects to Community Resources (debugging guide)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include working TypeScript/React code for Remotion v4+
- Reference the `remotion-docs` MCP server where Claude should look up current API details
- Include the motion vocabulary table (bouncy, smooth, snappy, etc.) where relevant
- Distinguish between what Claude generates well (text, simple transitions) and what needs extra guidance
- Be organized as quick-reference patterns, not tutorials — Claude needs to grab and use patterns fast during the iteration loop

---

## PROMPT END
