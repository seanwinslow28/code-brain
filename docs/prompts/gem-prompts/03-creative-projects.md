# Creative Projects - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Creative Projects"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals. My main creative project is **16BitFit** — a Game Boy-inspired fitness RPG built with React Native + Phaser 3. I also do AI-assisted creative work: sprite generation, video content, music, and pixel art. My stack is React, Python, Supabase.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers my **creative projects and game development** workflows.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Creative Projects") contains deep research on using Claude Code for creative and game development work: Phaser 3 patterns, React Native mobile development, sprite/asset pipeline automation, AI creative tool integration (ComfyUI, ElevenLabs, image generation APIs), video/animation workflows, and pixel art creation. Sources include game dev tutorials, Phaser documentation, React Native guides, and creative AI workflow examples.

## Your Task

Analyze all sources in this notebook and generate **5-6 Claude Skills** that make Claude Code a creative development partner. These skills should help a beginner coder build games, create assets, and produce creative content.

## Target Skills to Extract

### 1. Phaser 3 Game Development Patterns
**Priority**: High
**What to extract**: Scene management patterns (boot, preload, menu, gameplay, pause), sprite animation setup, physics systems (Arcade vs Matter), game state management, input handling (touch + keyboard), tile map creation, Game Boy-style constraints (160x144 viewport, limited palette), and common Phaser 3 pitfalls for beginners. Focus on patterns Claude Code can implement correctly for a fitness RPG game.
**Trigger phrases**: "Phaser", "game scene", "sprite animation", "physics", "tile map", "game state", "16BitFit", "fitness RPG"

### 2. React Native + Phaser Integration
**Priority**: High
**What to extract**: Embedding Phaser in React Native via WebView, communication bridge patterns (React Native <-> Phaser postMessage), Expo setup, navigation patterns (React Navigation), state management (React Native side vs Phaser game state), debugging React Native + WebView issues, and building a mobile app wrapper around a Phaser game.
**Trigger phrases**: "React Native", "Expo", "mobile app", "WebView", "bridge to Phaser", "navigation", "mobile game"

### 3. Sprite & Asset Pipeline
**Priority**: High
**What to extract**: Sprite sheet generation workflows, animation frame conventions (walk cycles, idle, attack), pixel art constraints (8x8, 16x16, 32x32 tiles), asset organization patterns, texture atlas creation, importing AI-generated sprites into Phaser, and batch processing assets. Include tools and formats (TexturePacker, aseprite, PNG sequences).
**Trigger phrases**: "sprite sheet", "animation frames", "pixel art", "asset pipeline", "texture atlas", "game assets"

### 4. AI Creative Tool Integration
**Priority**: Medium
**What to extract**: ComfyUI workflow automation (API calls, queue management), image generation for game assets, AI music generation tools, ElevenLabs voice integration, video generation APIs, and orchestrating multi-tool creative pipelines where Claude Code coordinates between different AI services.
**Trigger phrases**: "ComfyUI", "generate images", "AI art", "ElevenLabs", "AI music", "creative AI", "generate assets"

### 5. Video & Animation Production
**Priority**: Medium
**What to extract**: ffmpeg automation patterns (common commands for game dev: GIF creation, video compression, format conversion, sprite sheet to animation), basic video editing workflows, subtitle generation, batch video processing, and creating game trailers or devlog content.
**Trigger phrases**: "ffmpeg", "create GIF", "video compression", "game trailer", "convert video", "animation export"

### 6. Pixel Art & Retro Aesthetic
**Priority**: Lower
**What to extract**: Pixel art fundamentals for non-artists (limited palettes, dithering patterns, sub-pixel animation), Game Boy color constraints (4 shades of green, 8x8 tiles), art style consistency rules, character sprite conventions (RPG characters, enemies, NPCs), and environment tile patterns. The skill should help Claude Code guide me in maintaining visual consistency even though I'm not an artist.
**Trigger phrases**: "pixel art", "retro style", "Game Boy aesthetic", "color palette", "character design", "tile design"

## Extraction Guidance

- **Beginner coder focus**: I'm learning. Skills should include explanations of WHY certain patterns are used, not just the code.
- **16BitFit context**: The primary game project is a fitness RPG with Game Boy aesthetics. Skills should default to this context when generating examples.
- **Practical over theoretical**: I need patterns I can implement today, not comprehensive game engine tutorials. Focus on the 20% of Phaser that covers 80% of use cases.
- **React Native specifics**: Include Expo-specific patterns where they differ from bare React Native. I'm using Expo.
- **AI asset quality**: When extracting AI creative tool patterns, include quality control steps — AI-generated assets often need post-processing.
- **File format awareness**: Include specific file formats, dimensions, and compression settings for each asset type.

## Cross-Domain Notes

- **Phaser skill** connects to Technical Stack (React/TypeScript) and Remotion Mastery (game trailer creation)
- **React Native skill** connects to Master Designer (mobile animations with Reanimated) and Technical Stack
- **Asset Pipeline** connects to Obsidian Integration (asset documentation) and Life Optimization (automation patterns)
- **AI Creative Tools** connects to Domain Specific (AI-native product development) and Technical Stack (API integration)
- **Video Production** overlaps with Remotion Mastery (which handles programmatic video) — this skill should focus on traditional ffmpeg/editing workflows, not Remotion

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include copy-paste code patterns that work in Phaser 3 and React Native
- Reference specific Phaser 3 API methods (not outdated Phaser 2 patterns)
- Be immediately usable in a React Native + Phaser project
- Include file structure conventions (where to put assets, scenes, components)
- Distinguish between Expo and bare React Native where relevant

---

## PROMPT END
