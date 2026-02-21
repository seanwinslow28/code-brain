# Anti-Gravity Agent Kickoff: Batch NotebookLM Fast Research for Remotion Mastery

**Target Notebook:** Claude Code - Remotion Mastery
**Status:** Sections 1.1–1.6 and 2.1–2.3 already completed. Resume from 2.4.
**Tool:** `notebooklm-mcp` (already configured)

---

## Kickoff Prompt

```
You are batch-executing NotebookLM Fast Research prompts into an existing notebook called "Claude Code - Remotion Mastery". Sections 1.1 through 2.3 have already been researched and imported — do NOT re-run those.

Your job: run each remaining prompt below as a separate Fast Research query against the "Claude Code - Remotion Mastery" notebook, wait for each to complete, then import its sources. Process them in the batches listed below. After each batch, confirm completion before moving to the next.

IMPORTANT RULES:
- Use research_start with mode="fast" and source="web" for each prompt
- Poll research_status until complete before moving to the next prompt
- Import ALL discovered sources using research_import after each completes
- Do NOT skip any prompts — run every single one in order
- If a research task fails, retry once, then log it and move on
- The notebook_id for "Claude Code - Remotion Mastery" should be identified first using notebook_list

---

### BATCH 1: Sections 2.4–2.6 (Claude Code + Remotion Integration)

**2.4:** End-to-end workflow for creating Remotion videos with Claude Code: from project initialization through prompting, previewing in Remotion Studio (localhost:3000), iterating, and final rendering with npx remotion render. Include time estimates, common pitfalls, and optimization strategies for the iteration loop.

**2.5:** CLAUDE.md configuration for Remotion projects: what to include (design tokens, animation preferences, brand guidelines, component conventions), the official Remotion CLAUDE.md from their GitHub repo, and how to encode your personal animation style so Claude generates on-brand video code consistently.

**2.6:** Remotion + Claude Code starter kits and templates 2025-2026: claude-remotion-kickstart, Claude-x-Remotion, Remotion-Claude-Code tutorial repo, official Remotion templates, and pre-built component libraries. Compare which starter kit is best for beginners and what each includes.

---

### BATCH 2: Section 3.1–3.4 (Animation Techniques — Part 1)

**3.1:** Text animation techniques in Remotion with Claude Code: character-by-character reveals, word-by-word animations, typewriter effects, text morphing, kinetic typography, text along paths, and animated captions. Include copy-paste patterns and prompt examples that produce each effect.

**3.2:** Shape and SVG animation in Remotion: path drawing effects, SVG morphing between shapes, geometric pattern animations, logo reveals, icon animations, and creating motion graphics with vector shapes. Focus on techniques a non-artist can describe to Claude Code.

**3.3:** Animated data visualizations in Remotion: chart animations (bar, line, pie, area), counter animations, progress bars, comparison graphics, and real-time-style data reveals. Focus on creating engaging data videos for crypto market data, product metrics, and stakeholder presentations.

**3.4:** Image animation techniques in Remotion: Ken Burns effect (pan and zoom), photo slideshows with transitions, image reveals, parallax layering, split-screen comparisons, and creating engaging visual stories from static images. Include how to handle aspect ratios and responsive sizing.

---

### BATCH 3: Section 3.5–3.8 (Animation Techniques — Part 2)

**3.5:** Particle systems and generative visual effects in Remotion: confetti animations, falling particles, noise-based backgrounds, generative patterns, grid animations, and creating visually complex effects through code. Focus on effects that look impressive but are simple for Claude Code to generate.

**3.6:** Remotion @remotion/three package for 3D animations: ThreeCanvas component, React Three Fiber integration, using useCurrentFrame() within 3D scenes, video textures, and creating 3D title sequences or product visualizations. Include the Three.js template and beginner-friendly 3D patterns.

**3.7:** Creating UI demo and screen recording-style animations in Remotion: simulated cursor movements, typing animations, UI element highlights, browser mockups, and product walkthrough videos. Focus on creating polished product demos for The Block's products.

**3.8:** Animation staggering and orchestration in Remotion: cascading element entrances, coordinated multi-element animations, timeline choreography, delay patterns, and creating complex sequences that feel cohesive. Include timing formulas and spring parameter combinations.

---

### BATCH 4: Section 4.1–4.3 (Professional Production — Part 1)

**4.1:** Creating professional video intros and outros with Remotion + Claude Code: logo animations, brand reveals, title cards, lower thirds, end cards, subscribe/CTA animations, and building reusable intro/outro templates. Include examples for corporate, creative, and educational contexts.

**4.2:** Remotion templates for social media video formats: Instagram Reels/Stories (9:16), YouTube Shorts, TikTok, Twitter/X video, LinkedIn video, and Facebook. Cover aspect ratio handling, platform-specific best practices, and creating multi-format renders from single compositions.

**4.3:** Creating animated presentation and explainer videos with Remotion: slide-style compositions, animated bullet points, diagram reveals, concept explanations with motion, and turning static presentations into engaging video content. Focus on use cases for product updates and stakeholder communication.

---

### BATCH 5: Section 4.4–4.6 (Professional Production — Part 2)

**4.4:** Remotion for personalized video generation at scale: template-driven workflows, dataset rendering, dynamic content injection, batch processing patterns, and creating thousands of video variations. Include examples like GitHub Unwrapped and marketing personalization.

**4.5:** Audio-synced animations in Remotion: syncing visuals to music beats, audio waveform visualization, timed text reveals to voiceover, audio ducking, and creating music videos or podcast visualizations. Include patterns for working with ElevenLabs-generated audio.

**4.6:** Creating cryptocurrency and financial data visualization videos with Remotion: price chart animations, market cap comparisons, portfolio performance reviews, trading volume visualizations, and news summary videos. Focus on automated content for The Block's audience.

---

### BATCH 6: Section 5.1–5.3 (Rendering & Performance — Part 1)

**5.1:** Remotion encoding options and output formats: video codecs (h264, h265, vp8, prores), audio formats (aac, mp3, wav, opus), container formats (MP4, WebM, MOV, GIF), image sequences, and the CLI render command. Include when to use each format and quality/size tradeoffs.

**5.2:** Creating GIFs with Remotion: native GIF output format, the @remotion/gif package, the Gif component synced with useCurrentFrame(), AnimatedImage component, reducing frame rate for smaller file sizes, and practical GIF creation workflows for social media and documentation.

**5.3:** Remotion rendering performance optimization: identifying slow frames with --log=verbose, the --open-perf-monitor flag, concurrency tuning with npx remotion benchmark, React.memo() and useMemo() for preventing re-renders, avoiding GPU bottlenecks (box-shadow, blur, gradients), and Player optimization.

---

### BATCH 7: Section 5.4–5.6 (Rendering & Performance — Part 2)

**5.4:** Remotion Lambda for serverless video rendering on AWS: distributed rendering across Lambda functions, cost model (pay only while rendering), the Rust binary speed improvements in v4.0, light client for reduced bundle size, and integration with SQS/EC2. Focus on when Lambda makes sense vs local rendering.

**5.5:** Remotion Studio and Player components: previewing videos before rendering, parameter editing without code changes, deploying Studio as a static website for team/client sharing, embedding Remotion Player in React apps, custom controls, and real-time parametrization.

**5.6:** Remotion @remotion/web-renderer for browser-based rendering: rendering videos directly in the browser without server infrastructure, use cases (user-generated content, real-time previews), limitations, and when client-side rendering is appropriate vs server-side.

---

### BATCH 8: Section 6.1–6.3 (Advanced Techniques — Part 1)

**6.1:** Organizing large Remotion projects with multiple compositions: project structure conventions, shared component libraries, composition registries in Root.tsx, and managing complex video suites. Include patterns for a project with dozens of video templates.

**6.2:** Building reusable Remotion component libraries: animated text components, transition wrappers, layout templates, and creating a personal animation toolkit that Claude Code can reference across projects. Include component design patterns for maximum reusability.

**6.3:** Combining Remotion with AI media generation tools: remotion-media-mcp for AI images/videos/music/speech, integrating AI-generated assets into Remotion compositions, Nano Banana Pro for images, Veo for video, and automated asset pipelines. Focus on end-to-end AI-powered video creation.

---

### BATCH 9: Section 6.4–6.6 (Advanced Techniques — Part 2)

**6.4:** Dynamic data fetching in Remotion compositions: fetching API data during render, real-time data integration, webhook-triggered video generation, and creating videos that automatically update with fresh data (crypto prices, analytics, etc.).

**6.5:** Claude Code subagent patterns for Remotion workflows: using parallel subagents for component generation, architecture planning agents, animation research agents, and multi-agent orchestration for complex video projects. Include practical examples of agent specialization.

**6.6:** Claude Code hooks for Remotion development: PostToolUse hooks for auto-previewing changes, PreToolUse hooks for validating Remotion patterns, build verification loops, and automated testing of video compositions. Include hook configurations.

---

### BATCH 10: Section 7.1–7.3 (Real-World Applications — Part 1)

**7.1:** Remotion community showcase projects and case studies 2025-2026: GitHub Unwrapped (10,000+ personalized videos), Spotify Wrapped recreations, corporate training videos, educational content (50 anatomy videos in 2 weeks with 92% cost savings), and other notable implementations. Analyze what made each successful.

**7.2:** Creating product demo and marketing videos with Remotion + Claude Code: SaaS product tours, feature announcements, comparison videos, testimonial animations, and marketing campaign content. Focus on patterns relevant to crypto/fintech products like The Block's.

**7.3:** Remotion for educational and training video production: lesson animations, concept explanations, onboarding videos, tutorial sequences, and creating a library of reusable educational templates. Focus on Campus education platform content for The Block.

---

### BATCH 11: Section 7.4–7.6 (Real-World Applications — Part 2)

**7.4:** Creating game-related video content with Remotion: game trailers, gameplay animations, character showcases, update announcement videos, and retro-style pixel art animations. Focus on content for a Game Boy-inspired fitness RPG (16BitFit).

**7.5:** Building automated video content pipelines with Remotion + Claude Code: scheduled video generation, data-driven content creation, CI/CD integration for video rendering, and creating "set and forget" content systems. Include examples of fully automated video workflows.

**7.6:** Compilation of the most effective Claude Code prompts for Remotion video creation across the web 2025-2026: what language produces the cleanest code, what level of detail is optimal, prompt patterns from community power users, and before/after examples of prompt refinement.

---

### BATCH 12: Section 8.1–8.3 (Troubleshooting)

**8.1:** Common Remotion errors when working with Claude Code and how to fix them: version mismatch issues (all @remotion/* packages must match), FFmpeg/FFprobe requirements, rendering failures, performance bottlenecks, and the most frequent mistakes AI-generated code makes.

**8.2:** Honest assessment of what Claude Code does well vs poorly with Remotion: types of animations that generate cleanly (text, simple transitions, data viz) vs what gets messy (overlapping complex animations, precise timing), and strategies for working around limitations.

**8.3:** Debugging Remotion projects generated by Claude Code: using Remotion Studio for visual debugging, isolating composition issues, frame-by-frame inspection, console logging within compositions, and strategies for diagnosing animation problems when you're not an expert coder.

---

### BATCH 13: Section 9.1–9.5 (Stack Integration)

**9.1:** Integrating Remotion with React/Vite/Tailwind projects: shared component libraries, using Tailwind within Remotion compositions, Vite configuration for Remotion, and maintaining consistent design language between your web apps and video content.

**9.2:** Figma to Remotion design-to-animation workflow: extracting design tokens from Figma MCP, translating static designs into animated compositions, maintaining design fidelity, and using Figma as the source of truth for video branding.

**9.3:** ElevenLabs AI voice integration with Remotion: generating voiceovers, syncing narration to animated content, creating narrated explainer videos, and building an end-to-end AI voice + AI animation pipeline.

**9.4:** ComfyUI AI image generation combined with Remotion video creation: generating custom assets with ComfyUI, sprite and character animations, AI-generated backgrounds and textures, and building visual content pipelines that feed into Remotion compositions.

**9.5:** Creating game assets and trailers with Remotion for Phaser 3 projects: exporting animation frames, sprite sheet generation from Remotion compositions, game trailer creation, and bridging Remotion video output with Phaser game input.

---

### BATCH 14: Section 10.1–10.3 (Learning Path & Mastery)

**10.1:** Learning path for a beginner coder to become proficient at creating Remotion videos with Claude Code. Structure as weekly milestones: Week 1 (frame-based thinking, first text animation), Week 2 (springs and easing, multi-element timing), Week 3 (data visualizations and charts), Week 4 (multi-scene compositions with transitions). Include specific practice exercises for each week, what to learn first vs what can wait, and deliberate practice patterns for building animation intuition without formal animation training.

**10.2:** Core animation principles for programmers who aren't animators: the 12 principles of animation adapted for code, timing and spacing concepts, easing functions explained visually, and building an intuition for what makes motion feel natural without formal animation training.

**10.3:** Remotion version history and recent changes 2025-2026: major feature releases (v4.0 Rust binary, Mediabunny migration, static Studio export), breaking changes, deprecated features, and what's coming next. Focus on staying current with the latest capabilities.

---

After ALL batches are complete, provide a final summary:
- Total prompts executed successfully
- Any prompts that failed and need manual retry
- Total sources imported across all batches
- The notebook is now ready for synthesis questions
```
