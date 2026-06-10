# NotebookLM Notebook: Claude Code + Remotion Mastery

**Purpose:** Deep Research prompts and synthesis questions for mastering the Remotion SKILL in Claude Code — making Claude your personal animator
**Vision:** Transform Claude Code into a programmatic video production studio using Remotion's React-based framework, for creative projects and APM work at The Block
**Profile Source:** Sean Winslow's Research Profile Templates

---

## Understanding This Notebook

### The Goal
Master using Claude Code + Remotion to create professional programmatic videos, animations, and motion graphics entirely through conversation. Instead of learning After Effects or Premiere, you describe what you want and Claude writes the React code that renders your vision frame by frame.

### What Remotion IS
Remotion is a React framework for creating videos programmatically. You write TypeScript/React components that describe what appears on each frame, and Remotion renders those components into MP4, WebM, GIF, or other formats. The core idea: you get a frame number and a blank canvas, then render anything using React.

### Why This Matters for You
- **Creative projects**: Animated intros, data visualizations, social content, game trailers for 16BitFit
- **APM work at The Block**: Crypto market data videos, product demos, stakeholder update videos, Campus explainers
- **Skill stacking**: React knowledge you already have + AI assistance = video production without learning traditional editing

### Your Setup
- `remotion-docs` MCP server installed globally on Mac
- Claude Code with paid subscription
- React/Vite/Tailwind stack (already familiar)

---

## How to Use This Notebook

### Step 1: Create the Notebook
Create a NotebookLM notebook called **"Claude Code + Remotion Mastery"**

### Step 2: Seed It with Key Sources
Before running Deep Research, manually add these sources:
- https://www.remotion.dev/docs/ai/claude-code (Claude Code integration guide)
- https://www.remotion.dev/docs/ai/mcp (MCP server documentation)
- https://www.remotion.dev/docs/ai/skills (Agent skills for Remotion)
- https://www.remotion.dev/docs/the-fundamentals (Core concepts)
- https://www.remotion.dev/docs/transitions/ (Transitions package)
- https://github.com/remotion-dev/remotion (Main repository)
- https://www.remotion.dev/llms.txt (System prompt for LLMs)

### Step 3: Run Deep Research Prompts
Run the prompts below one at a time, import each report + sources.

### Step 4: Ask Synthesis Questions
After importing, use the Chat feature with the synthesis questions at the bottom.

### Step 5: Generate Learning Materials
Create Audio Overviews, Flashcards, Quizzes, and Study Guides from the imported sources.

---

## Quick Start: Your First Remotion Video with Claude Code

### Phase 1: Foundation (30 minutes)
1. Verify your `remotion-docs` MCP server is active (run `claude` and check MCP tools)
2. Create a new Remotion project: `npx create-video@latest` (or clone a starter kit)
3. Open in Claude Code and confirm MCP connection (green dot or tool listing)
4. Preview the default composition: `npm start` → opens Remotion Studio at localhost:3000

### Phase 2: First Video (30-45 minutes)
5. Prompt Claude: "Create a 5-second composition with my name fading in, then sliding up and out"
6. Preview the result in Remotion Studio (hot reloads on save)
7. Iterate 2-3 times: adjust timing, add color, change easing
8. Render: `npx remotion render MyComposition out/first-video.mp4`
9. Watch your first programmatic video

### Phase 3: Build Your Toolkit (Ongoing)
10. Create your CLAUDE.md with brand colors and animation preferences (use the template below)
11. Build 3-5 reusable components: AnimatedText, FadeIn wrapper, DataBar, SceneTransition
12. Try each video type: text animation → data viz → image slideshow → multi-scene explainer
13. Run Deep Research prompts to level up technique knowledge

---

## Motion Vocabulary: Describing Animation to Claude Code

Use these terms when prompting Claude Code for specific motion styles:

| You Say | Claude Generates | Spring Parameters |
|---------|-----------------|-------------------|
| "bouncy" | Overshoot with oscillation | `{ stiffness: 300, damping: 10 }` |
| "smooth" | Gradual ease-out, no overshoot | `{ stiffness: 100, damping: 30 }` |
| "snappy" | Fast start, abrupt stop | `{ stiffness: 500, damping: 30 }` |
| "gentle" | Slow, soft motion | `{ stiffness: 50, damping: 20 }` |
| "dramatic" | Large-scale with tension | `{ stiffness: 200, damping: 8 }` |
| "elastic" | Stretchy, rubber-band feel | Easing.elastic() with interpolate() |
| "cinematic" | Slow in, slow out (S-curve) | Easing.bezier(0.4, 0, 0.2, 1) |
| "playful" | Bounce at the end | Easing.bounce with interpolate() |
| "mechanical" | Linear, robotic motion | Easing.linear (no spring) |
| "organic" | Slightly irregular, natural | Spring with low stiffness, medium damping |

### Timing Language
| You Say | Approximate Duration |
|---------|---------------------|
| "quick flash" | 5-10 frames (0.15-0.33s at 30fps) |
| "fast" | 10-15 frames (0.33-0.5s) |
| "standard" | 15-25 frames (0.5-0.83s) |
| "deliberate" | 25-45 frames (0.83-1.5s) |
| "slow reveal" | 45-90 frames (1.5-3s) |

### Scene Description Pattern
When describing a scene to Claude, follow this order:
1. **What appears** → "Title text 'Hello World' in white Inter Bold"
2. **How it enters** → "fades in while sliding up 40px"
3. **How long it stays** → "holds for 2 seconds"
4. **How it exits** → "slides left while fading out"
5. **What follows** → "then the subtitle appears with a bouncy spring"

---

# DEEP RESEARCH PROMPTS

---

## SECTION 1: Remotion Fundamentals for AI-Assisted Video Creation

### 1.1 Remotion Core Architecture
```
Remotion framework architecture and core concepts 2025-2026: Compositions, Sequences, useCurrentFrame(), fps systems, and the frame-based rendering pipeline. Focus on how these concepts work together for programmatic video creation, especially when Claude Code is generating the code. Include mental models for thinking in frames instead of timelines.
```

### 1.2 Spring Animations & Interpolation
```
Remotion spring() and interpolate() animation primitives: physics-based springs (stiffness, damping, mass, overshoot), the interpolate() function for mapping value ranges, and the complete Easing module (bezier, elastic, bounce, back, etc.). Include the Spring Editor tool at springs.remotion.dev and practical parameter combinations for common motion effects.
```

### 1.3 Sequences & Timing Control
```
Remotion Sequences for timeline control: nesting Sequences with the from prop, time-shifting useCurrentFrame() values, durationInFrames for component mounting, and orchestrating complex multi-element timelines. Focus on patterns that help a beginner coder think about video timing as component composition.
```

### 1.4 Audio & Video Embedding
```
Audio and video integration in Remotion 2025-2026: OffthreadVideo component for frame-accurate video embedding, Audio and Html5Audio components, per-frame volume control, staticFile() for public folder assets, and the recent Mediabunny migration (replacing Media Parser as of February 2026). Include synchronization patterns.
```

### 1.5 Transitions Package Deep Dive
```
Remotion @remotion/transitions package: TransitionSeries component, all available presentations (fade, slide, wipe, flip, clockWipe, iris, cube, none), timing presets, TransitionSeries.Overlay, and creating custom transition effects. Include side-by-side comparisons and when to use each transition type.
```

### 1.6 Input Props & Parametrized Videos
```
Remotion parametrized video system: Input Props for dynamic content, getInputProps(), calculateMetadata() for dynamic duration/dimensions, making videos template-driven, data fetching during render, and dataset rendering for batch video generation. Focus on creating reusable video templates that Claude Code can populate with different data.
```

---

## SECTION 2: Claude Code + Remotion Integration

### 2.1 The Remotion MCP Server
```
Remotion MCP server (@remotion/mcp) deep dive: what it exposes to Claude Code, CrawlChat vector database indexing, how documentation is made available, content negotiation via Accept headers, the remotion-documentation tool, and how it prevents LLM hallucinations. Include setup verification and troubleshooting steps.
```

### 2.2 Agent Skills for Remotion
```
Remotion agent skills for Claude Code: the remotion-best-practices skill (which went viral with 8.3 million views), SKILL.md structure for Remotion projects, the .claude folder configuration, and how skills teach Claude Code to write correct Remotion patterns. Include examples of effective vs ineffective skill configurations.
```

### 2.3 Prompting Strategies for Remotion Videos
```
Prompting strategies for generating Remotion videos with Claude Code: describing animations in natural language, iterative refinement (typical 4-6 turns), what types of videos Claude generates well vs poorly, and prompt templates for common video types. Include real examples of prompts and their results. Focus on what a beginner coder needs to specify.
```

### 2.4 The Claude Code + Remotion Workflow
```
End-to-end workflow for creating Remotion videos with Claude Code: from project initialization through prompting, previewing in Remotion Studio (localhost:3000), iterating, and final rendering with npx remotion render. Include time estimates, common pitfalls, and optimization strategies for the iteration loop.
```

### 2.5 CLAUDE.md for Remotion Projects
```
CLAUDE.md configuration for Remotion projects: what to include (design tokens, animation preferences, brand guidelines, component conventions), the official Remotion CLAUDE.md from their GitHub repo, and how to encode your personal animation style so Claude generates on-brand video code consistently.
```

### 2.6 Community Starter Kits & Templates
```
Remotion + Claude Code starter kits and templates 2025-2026: claude-remotion-kickstart, Claude-x-Remotion, Remotion-Claude-Code tutorial repo, official Remotion templates, and pre-built component libraries. Compare which starter kit is best for beginners and what each includes.
```

---

## SECTION 3: Animation Techniques & Motion Design

### 3.1 Text Animations
```
Text animation techniques in Remotion with Claude Code: character-by-character reveals, word-by-word animations, typewriter effects, text morphing, kinetic typography, text along paths, and animated captions. Include copy-paste patterns and prompt examples that produce each effect.
```

### 3.2 Shape & SVG Animations
```
Shape and SVG animation in Remotion: path drawing effects, SVG morphing between shapes, geometric pattern animations, logo reveals, icon animations, and creating motion graphics with vector shapes. Focus on techniques a non-artist can describe to Claude Code.
```

### 3.3 Data Visualization Animations
```
Animated data visualizations in Remotion: chart animations (bar, line, pie, area), counter animations, progress bars, comparison graphics, and real-time-style data reveals. Focus on creating engaging data videos for crypto market data, product metrics, and stakeholder presentations.
```

### 3.4 Image & Photo Animations
```
Image animation techniques in Remotion: Ken Burns effect (pan and zoom), photo slideshows with transitions, image reveals, parallax layering, split-screen comparisons, and creating engaging visual stories from static images. Include how to handle aspect ratios and responsive sizing.
```

### 3.5 Particle & Generative Effects
```
Particle systems and generative visual effects in Remotion: confetti animations, falling particles, noise-based backgrounds, generative patterns, grid animations, and creating visually complex effects through code. Focus on effects that look impressive but are simple for Claude Code to generate.
```

### 3.6 3D Graphics with Three.js
```
Remotion @remotion/three package for 3D animations: ThreeCanvas component, React Three Fiber integration, using useCurrentFrame() within 3D scenes, video textures, and creating 3D title sequences or product visualizations. Include the Three.js template and beginner-friendly 3D patterns.
```

### 3.7 Screen Recording & UI Demo Animations
```
Creating UI demo and screen recording-style animations in Remotion: simulated cursor movements, typing animations, UI element highlights, browser mockups, and product walkthrough videos. Focus on creating polished product demos for The Block's products.
```

### 3.8 Stagger & Orchestration Patterns
```
Animation staggering and orchestration in Remotion: cascading element entrances, coordinated multi-element animations, timeline choreography, delay patterns, and creating complex sequences that feel cohesive. Include timing formulas and spring parameter combinations.
```

---

## SECTION 4: Professional Video Production Patterns

### 4.1 Video Intro & Outro Templates
```
Creating professional video intros and outros with Remotion + Claude Code: logo animations, brand reveals, title cards, lower thirds, end cards, subscribe/CTA animations, and building reusable intro/outro templates. Include examples for corporate, creative, and educational contexts.
```

### 4.2 Social Media Video Formats
```
Remotion templates for social media video formats: Instagram Reels/Stories (9:16), YouTube Shorts, TikTok, Twitter/X video, LinkedIn video, and Facebook. Cover aspect ratio handling, platform-specific best practices, and creating multi-format renders from single compositions.
```

### 4.3 Presentation & Explainer Videos
```
Creating animated presentation and explainer videos with Remotion: slide-style compositions, animated bullet points, diagram reveals, concept explanations with motion, and turning static presentations into engaging video content. Focus on use cases for product updates and stakeholder communication.
```

### 4.4 Personalized Videos at Scale
```
Remotion for personalized video generation at scale: template-driven workflows, dataset rendering, dynamic content injection, batch processing patterns, and creating thousands of video variations. Include examples like GitHub Unwrapped and marketing personalization.
```

### 4.5 Music & Audio Synchronization
```
Audio-synced animations in Remotion: syncing visuals to music beats, audio waveform visualization, timed text reveals to voiceover, audio ducking, and creating music videos or podcast visualizations. Include patterns for working with ElevenLabs-generated audio.
```

### 4.6 Crypto & Finance Data Videos
```
Creating cryptocurrency and financial data visualization videos with Remotion: price chart animations, market cap comparisons, portfolio performance reviews, trading volume visualizations, and news summary videos. Focus on automated content for The Block's audience.
```

---

## SECTION 5: Rendering, Performance & Output

### 5.1 Encoding & Output Formats
```
Remotion encoding options and output formats: video codecs (h264, h265, vp8, prores), audio formats (aac, mp3, wav, opus), container formats (MP4, WebM, MOV, GIF), image sequences, and the CLI render command. Include when to use each format and quality/size tradeoffs.
```

### 5.2 GIF Generation
```
Creating GIFs with Remotion: native GIF output format, the @remotion/gif package, the Gif component synced with useCurrentFrame(), AnimatedImage component, reducing frame rate for smaller file sizes, and practical GIF creation workflows for social media and documentation.
```

### 5.3 Performance Optimization
```
Remotion rendering performance optimization: identifying slow frames with --log=verbose, the --open-perf-monitor flag, concurrency tuning with npx remotion benchmark, React.memo() and useMemo() for preventing re-renders, avoiding GPU bottlenecks (box-shadow, blur, gradients), and Player optimization.
```

### 5.4 Remotion Lambda (Serverless Rendering)
```
Remotion Lambda for serverless video rendering on AWS: distributed rendering across Lambda functions, cost model (pay only while rendering), the Rust binary speed improvements in v4.0, light client for reduced bundle size, and integration with SQS/EC2. Focus on when Lambda makes sense vs local rendering.
```

### 5.5 Remotion Studio & Player
```
Remotion Studio and Player components: previewing videos before rendering, parameter editing without code changes, deploying Studio as a static website for team/client sharing, embedding Remotion Player in React apps, custom controls, and real-time parametrization.
```

### 5.6 Client-Side Rendering
```
Remotion @remotion/web-renderer for browser-based rendering: rendering videos directly in the browser without server infrastructure, use cases (user-generated content, real-time previews), limitations, and when client-side rendering is appropriate vs server-side.
```

---

## SECTION 6: Advanced Techniques & Power User Patterns

### 6.1 Multi-Composition Projects
```
Organizing large Remotion projects with multiple compositions: project structure conventions, shared component libraries, composition registries in Root.tsx, and managing complex video suites. Include patterns for a project with dozens of video templates.
```

### 6.2 Custom Components & Libraries
```
Building reusable Remotion component libraries: animated text components, transition wrappers, layout templates, and creating a personal animation toolkit that Claude Code can reference across projects. Include component design patterns for maximum reusability.
```

### 6.3 Remotion + AI Media Generation
```
Combining Remotion with AI media generation tools: remotion-media-mcp for AI images/videos/music/speech, integrating AI-generated assets into Remotion compositions, Nano Banana Pro for images, Veo for video, and automated asset pipelines. Focus on end-to-end AI-powered video creation.
```

### 6.4 Dynamic Data Fetching
```
Dynamic data fetching in Remotion compositions: fetching API data during render, real-time data integration, webhook-triggered video generation, and creating videos that automatically update with fresh data (crypto prices, analytics, etc.).
```

### 6.5 Subagent Patterns for Video Production
```
Claude Code subagent patterns for Remotion workflows: using parallel subagents for component generation, architecture planning agents, animation research agents, and multi-agent orchestration for complex video projects. Include practical examples of agent specialization.
```

### 6.6 Hooks for Remotion Workflows
```
Claude Code hooks for Remotion development: PostToolUse hooks for auto-previewing changes, PreToolUse hooks for validating Remotion patterns, build verification loops, and automated testing of video compositions. Include hook configurations.
```

---

## SECTION 7: Real-World Applications & Case Studies

### 7.1 Community Showcase Projects
```
Remotion community showcase projects and case studies 2025-2026: GitHub Unwrapped (10,000+ personalized videos), Spotify Wrapped recreations, corporate training videos, educational content (50 anatomy videos in 2 weeks with 92% cost savings), and other notable implementations. Analyze what made each successful.
```

### 7.2 Product Demo & Marketing Videos
```
Creating product demo and marketing videos with Remotion + Claude Code: SaaS product tours, feature announcements, comparison videos, testimonial animations, and marketing campaign content. Focus on patterns relevant to crypto/fintech products like The Block's.
```

### 7.3 Educational & Training Content
```
Remotion for educational and training video production: lesson animations, concept explanations, onboarding videos, tutorial sequences, and creating a library of reusable educational templates. Focus on Campus education platform content for The Block.
```

### 7.4 Game Development Content
```
Creating game-related video content with Remotion: game trailers, gameplay animations, character showcases, update announcement videos, and retro-style pixel art animations. Focus on content for a Game Boy-inspired fitness RPG (16BitFit).
```

### 7.5 Automated Content Pipelines
```
Building automated video content pipelines with Remotion + Claude Code: scheduled video generation, data-driven content creation, CI/CD integration for video rendering, and creating "set and forget" content systems. Include examples of fully automated video workflows.
```

### 7.6 Best Prompts That Produced Best Results
```
Compilation of the most effective Claude Code prompts for Remotion video creation across the web 2025-2026: what language produces the cleanest code, what level of detail is optimal, prompt patterns from community power users, and before/after examples of prompt refinement.
```

---

## SECTION 8: Troubleshooting & Common Pitfalls

### 8.1 Common Errors & Fixes
```
Common Remotion errors when working with Claude Code and how to fix them: version mismatch issues (all @remotion/* packages must match), FFmpeg/FFprobe requirements, rendering failures, performance bottlenecks, and the most frequent mistakes AI-generated code makes.
```

### 8.2 What Claude Code Does Well vs Poorly
```
Honest assessment of what Claude Code does well vs poorly with Remotion: types of animations that generate cleanly (text, simple transitions, data viz) vs what gets messy (overlapping complex animations, precise timing), and strategies for working around limitations.
```

### 8.3 Debugging Remotion Projects
```
Debugging Remotion projects generated by Claude Code: using Remotion Studio for visual debugging, isolating composition issues, frame-by-frame inspection, console logging within compositions, and strategies for diagnosing animation problems when you're not an expert coder.
```

---

## SECTION 9: Integration with Your Stack & Workflow

### 9.1 React/Vite/Tailwind Integration
```
Integrating Remotion with React/Vite/Tailwind projects: shared component libraries, using Tailwind within Remotion compositions, Vite configuration for Remotion, and maintaining consistent design language between your web apps and video content.
```

### 9.2 Figma to Remotion Workflow
```
Figma to Remotion design-to-animation workflow: extracting design tokens from Figma MCP, translating static designs into animated compositions, maintaining design fidelity, and using Figma as the source of truth for video branding.
```

### 9.3 ElevenLabs + Remotion
```
ElevenLabs AI voice integration with Remotion: generating voiceovers, syncing narration to animated content, creating narrated explainer videos, and building an end-to-end AI voice + AI animation pipeline.
```

### 9.4 ComfyUI + Remotion
```
ComfyUI AI image generation combined with Remotion video creation: generating custom assets with ComfyUI, sprite and character animations, AI-generated backgrounds and textures, and building visual content pipelines that feed into Remotion compositions.
```

### 9.5 Remotion + Phaser Game Assets
```
Creating game assets and trailers with Remotion for Phaser 3 projects: exporting animation frames, sprite sheet generation from Remotion compositions, game trailer creation, and bridging Remotion video output with Phaser game input.
```

---

## SECTION 10: Learning Path & Mastery Roadmap

### 10.1 Beginner to Animator Learning Path
```
Learning path for a beginner coder to become proficient at creating Remotion videos with Claude Code. Structure as weekly milestones: Week 1 (frame-based thinking, first text animation), Week 2 (springs and easing, multi-element timing), Week 3 (data visualizations and charts), Week 4 (multi-scene compositions with transitions). Include specific practice exercises for each week, what to learn first vs what can wait, and deliberate practice patterns for building animation intuition without formal animation training.
```

### 10.2 Animation Principles for Programmers
```
Core animation principles for programmers who aren't animators: the 12 principles of animation adapted for code, timing and spacing concepts, easing functions explained visually, and building an intuition for what makes motion feel natural without formal animation training.
```

### 10.3 Version Updates & Changelog
```
Remotion version history and recent changes 2025-2026: major feature releases (v4.0 Rust binary, Mediabunny migration, static Studio export), breaking changes, deprecated features, and what's coming next. Focus on staying current with the latest capabilities.
```

---

# SYNTHESIS QUESTIONS

---

## Part 1: Understanding the System

### Architecture & Concepts

```
Create a visual mental model of how Remotion works: Component → Frame → Canvas → Video. How does each piece connect?
```

```
Explain Remotion's frame-based system as if I'm a beginner coder. How is it different from timeline-based editors like Premiere?
```

```
What's the execution lifecycle when I type npx remotion render? Walk me through every step from command to MP4.
```

```
How do Compositions, Sequences, useCurrentFrame(), and spring() work together? Create a relationship diagram.
```

### MCP & Claude Code Integration

```
How does the remotion-docs MCP server actually work under the hood? What happens when Claude Code queries it?
```

```
What's in the remotion-best-practices skill that went viral? Extract the key rules and patterns it teaches Claude.
```

```
Compare the official @remotion/mcp with community MCP servers (remotion-media-mcp, Rodumani). What does each add?
```

```
What should my CLAUDE.md include for Remotion projects? Create a template based on sources.
```

---

## Part 2: Mastering the Prompting Loop

### Prompt Engineering for Videos

```
What makes a good Remotion prompt vs a bad one? Extract patterns from successful community examples.
```

```
Create a prompt template for each video type: intro, explainer, data viz, social media, product demo.
```

```
What level of detail should I specify in prompts? When does more detail help vs hurt?
```

```
What types of animations should I ask for vs what types should I avoid? Map the "sweet spot" of AI-generated video.
```

### Iteration Strategies

```
What's the optimal iteration flow? How many turns typically produce a polished video (sources say 4-6)?
```

```
What kinds of feedback produce the best Claude refinements? ("Move the text 20px up" vs "make it feel more dynamic")
```

```
How do I describe motion to Claude Code effectively? Build a vocabulary list for animation descriptions.
```

```
What are the most common things I'll need to fix after Claude's first generation?
```

---

## Part 3: Animation Technique Library

### Core Techniques

```
Create a cheat sheet of Remotion animation techniques with the exact code patterns. Group by category: text, shapes, data, images, 3D.
```

```
What spring() parameter combinations produce common motion styles? Map: bouncy, smooth, snappy, gentle, dramatic.
```

```
What are the most visually impressive animations that are also simple to code? Rank by impact:complexity ratio.
```

```
Compile all Easing functions with descriptions of what motion each produces. When use each?
```

### Advanced Patterns

```
How do I create staggered animations where elements enter one after another? Show the timing math.
```

```
What techniques make Remotion videos feel "professional" vs "amateur"? Extract quality markers.
```

```
How do I animate data charts that look like they belong on Bloomberg or CoinDesk? Compile financial data viz patterns.
```

```
What are the best transition effects between scenes? Compare all TransitionSeries presentations.
```

---

## Part 4: Production Workflow

### Project Setup

```
What's the ideal Remotion project structure for someone using Claude Code? Folder organization, file naming, component patterns.
```

```
Which starter kit should I use? Compare claude-remotion-kickstart, Claude-x-Remotion, and official templates.
```

```
What reusable components should I build first to speed up all future video projects?
```

### Rendering & Output

```
What encoding settings produce the best quality/size ratio for each platform (YouTube, Twitter, Instagram, Slack)?
```

```
When should I use Lambda vs local rendering? Create a decision framework based on video count and urgency.
```

```
How do I create GIFs from Remotion for documentation, Slack, and social media? What settings keep file size reasonable?
```

```
How do I render multiple formats (landscape + portrait + square) from a single composition?
```

---

## Part 5: The Block & APM-Specific Applications

### Work Applications

```
What types of videos would be most valuable for a crypto data/news company? Brainstorm 10 specific use cases.
```

```
How can I automate recurring video content (weekly market summaries, monthly metrics, quarterly reviews)?
```

```
What video formats work best for stakeholder updates? How do I turn a status email into an engaging video?
```

```
How can I create product demo videos for Campus education platform or Simon AI?
```

### Content Strategy

```
How do I build a video template library that covers my most common needs at The Block?
```

```
What's the ROI of programmatic video vs traditional editing for recurring content?
```

```
How can I combine Remotion with data feeds (crypto prices, on-chain metrics) for automated data videos?
```

---

## Part 6: Creative Project Applications

### 16BitFit & Game Dev

```
How can I create a retro pixel-art style game trailer with Remotion? What visual techniques emulate Game Boy aesthetics?
```

```
Can Remotion generate sprite sheet frames or animation sequences usable in Phaser 3?
```

```
What game-related video content should I create: trailers, devlogs, feature showcases, app store previews?
```

### Personal Creative Work

```
What types of creative videos can Remotion produce that would be impossible or impractical with traditional editors?
```

```
How do I build a personal brand video style that Claude Code can replicate consistently?
```

```
What AI-generated asset pipelines (ComfyUI images + ElevenLabs audio + Remotion video) work end to end?
```

---

## Part 7: Source Quality & Filtering

### Evaluating What You Found

```
Rank all sources from most to least useful for a beginner coder learning Remotion with Claude Code. Explain ranking.
```

```
Which sources have actual working code examples I can copy and run today?
```

```
Which sources are from the Remotion team vs community users vs AI-generated content farms? Assess reliability.
```

```
Flag any sources referencing deprecated APIs, outdated versions (pre-v4.0), or incorrect patterns.
```

```
If I could only keep 5 sources in this notebook, which should they be and why?
```

### Finding Contradictions

```
What do sources disagree about regarding best practices for Remotion + AI workflows?
```

```
Are there performance recommendations that conflict between sources? Which approach is more validated?
```

```
What limitations do some sources mention that others ignore? Build a realistic picture.
```

---

## Part 8: Building Your System

### Personal Animation Toolkit

```
Based on all sources, design my ideal Remotion + Claude Code setup: MCP config, CLAUDE.md, skills, project template, and component library.
```

```
Create a "Day 1 Setup Checklist" that configures Remotion optimally for Claude Code animation work.
```

```
What's the minimum viable setup (get a video rendered today) vs the full power-user setup? Compare both.
```

### Learning Plan

```
Create a 30-day learning plan for Remotion mastery with Claude Code, progressing from "Hello World" to complex animations.
```

```
What are the 5 videos I should create first to build core skills in order of difficulty?
```

```
What practice drills build animation intuition? (e.g., "recreate this effect," "animate this dataset," etc.)
```

---

## Part 9: Cross-Notebook Integration

### Connecting to Other Notebooks

```
How does Remotion connect to my Design Excellence notebook? What animation principles apply to both UI and video?
```

```
How can my Obsidian knowledge vault store Remotion patterns, templates, and component references for Claude Code retrieval?
```

```
What skills from my Claude Code Core Features notebook apply directly to Remotion workflows?
```

### Output Generation

```
Create a podcast-style audio overview explaining Remotion to a PM who codes as a hobby.
```

```
Generate flashcards for all Remotion core APIs and their purposes.
```

```
Create a quiz testing my understanding of Remotion's rendering pipeline and animation primitives.
```

```
Generate a study guide structured as a weekly progression from beginner to confident animator.
```

---

## Quick Reference: High-Impact Prompts

### Start Here (Top 10 Priority Prompts)
1. **2.3 Prompting Strategies** - How to talk to Claude about videos
2. **1.1 Core Architecture** - Mental model for frame-based thinking
3. **2.1 MCP Server** - Understanding your installed tool
4. **3.1 Text Animations** - Most common first video type
5. **1.2 Spring Animations** - The secret to natural-feeling motion
6. **4.3 Presentation & Explainer Videos** - Immediate work application
7. **3.3 Data Visualization** - Crypto data videos for The Block
8. **2.6 Community Starter Kits** - Don't start from scratch
9. **7.6 Best Prompts** - Learn from what worked for others
10. **10.1 Learning Path** - Structured roadmap to mastery

### Quick Win Prompts (Fastest to Value)
- **2.4 Workflow** - Get your first video rendered today
- **5.2 GIF Generation** - Small, shareable output
- **4.2 Social Media Formats** - Immediately useful content

### Deep Dive Prompts (For After Basics)
- **6.3 AI Media Generation** - Full AI pipeline
- **5.4 Lambda Rendering** - Scale up production
- **3.6 Three.js 3D** - Next-level visual effects

---

## Prompt Template for Asking Claude Code to Create Videos

Use this template when prompting Claude Code in a Remotion project:

```
Create a Remotion composition that:

VIDEO SPECS:
- Duration: [e.g., "10 seconds at 30fps"]
- Resolution: [e.g., "1920x1080" or "1080x1920 for Reels"]
- Output: [e.g., "MP4 with h264"]

CONTENT:
- [Scene 1 description with timing]
- [Scene 2 description with timing]
- [Scene 3 description with timing]

VISUAL STYLE:
- Aesthetic: [e.g., "clean corporate", "retro pixel art", "modern gradient"]
- Colors: [brand colors or palette]
- Typography: [font preferences, sizing]
- Background: [solid, gradient, animated, image]

ANIMATIONS:
- Entry effects: [e.g., "text fades in word by word"]
- Transitions: [e.g., "slide transitions between scenes"]
- Micro-interactions: [e.g., "subtle bounce on data points"]
- Easing: [e.g., "spring with slight overshoot" or "smooth ease-out"]

DATA (if applicable):
- [Data source or hardcoded values]
- [Chart/visualization type]
- [What story the data should tell]

AUDIO (if applicable):
- [Background music, voiceover, sound effects]
- [Timing sync requirements]

TECHNICAL:
- Use spring() for natural motion
- Use Sequences for timing control
- Use TransitionSeries for scene changes
- Optimize for rendering performance
```

---

## Sample CLAUDE.md for Remotion Projects

```markdown
## Remotion Project Configuration

### Brand
- Company: The Block
- Colors: Primary #1A1A2E, Accent #E94560, Background #0F3460, Text #FFFFFF
- Font: Inter (headings: 700, body: 400)

### Animation Preferences
- Default spring: { stiffness: 200, damping: 20 }
- Text entrance: fade + slide up, staggered 3 frames apart
- Scene transitions: fade() with 15 frame overlap
- Never use: jarring cuts, excessive bounce, slow dissolves

### Video Standards
- Default FPS: 30
- Default resolution: 1920x1080
- Social format: 1080x1920
- GIF max: 480px wide, 15fps

### Code Conventions
- One composition per file
- Shared components in src/components/
- Constants in src/constants.ts
- Use absolute imports
- Always type props with TypeScript interfaces

### Interaction Patterns
- Video entrance: fade + zoom from 95% to 100%, 20 frames
- Scene transitions: fade() with 15 frame overlap via TransitionSeries
- Text reveals: stagger word-by-word, 3 frames apart, spring entry
- Data points: scale from 0 to 1 with bouncy spring, staggered 5 frames
- Logos/images: fade in + subtle slide up (20px), smooth easing
- Exit animations: fade out + slide in exit direction, faster than entrance

### Performance Rules
- Avoid box-shadow, filter: blur() in animated elements
- Use transform and opacity for animations (GPU-accelerated)
- Memoize expensive calculations
- Keep frame render time under 100ms
```

---

## Sources

This notebook was informed by research on:
- [Remotion Official Documentation](https://www.remotion.dev/)
- [Remotion + Claude Code Guide](https://www.remotion.dev/docs/ai/claude-code)
- [Remotion MCP Server](https://www.remotion.dev/docs/ai/mcp)
- [Remotion Agent Skills](https://www.remotion.dev/docs/ai/skills)
- [Remotion System Prompt for LLMs](https://www.remotion.dev/llms.txt)
- [Remotion Transitions Package](https://www.remotion.dev/docs/transitions/)
- [Remotion Lambda Documentation](https://www.remotion.dev/docs/lambda)
- [Remotion Community Showcase](https://www.remotion.dev/showcase)
- [claude-remotion-kickstart Starter Kit](https://github.com/jhartquist/claude-remotion-kickstart)
- [remotion-media-mcp AI Assets](https://github.com/stephengpope/remotion-media-mcp)
- [Remotion GitHub Repository](https://github.com/remotion-dev/remotion)
- [Making Videos with Code: Remotion + Claude Guide](https://medium.com/@creativeaininja/making-videos-with-code-the-complete-guide-to-remotion-and-claude-code-82892e21d022)
- [How Remotion Uses CrawlChat for MCP](https://crawlchat.app/blog/how-remotion-uses-crawlchat)
- [Remotion Skills: AI-Powered Video Creation 2026](https://gaga.art/blog/remotion-skills/)
