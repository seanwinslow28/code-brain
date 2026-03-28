# Perplexity Computer Prompts — Stack Validation, Execution Planning, Opportunity Scanning

**Created:** 2026-03-27
**Purpose:** Three focused prompts for Perplexity Computer to validate, plan, and expand Sean's three-workstream project (Agent SDK + Sprite Pipeline + Autoresearch/LoRA).
**How to use:** Run each prompt as a separate Perplexity Computer task. Attach the specified context files to each. Run Prompt 1 first — its output feeds into Prompt 2.

---

## Files to Prepare Before Running Any Prompt

You'll reference these across the three prompts. Have them ready to upload:

**Always attach (to all 3 prompts):**
- `SOURCE-OF-TRUTH.md` — Your compressed master reference

**Prompt-specific attachments listed below each prompt.**

---

## Prompt 1: Stack Validation Audit — "Is Everything Still Current?"

### What to Attach (up to 10 files)
1. `SOURCE-OF-TRUTH.md`
2. `Claude-Agents-SDK-Info/agent-sdk-upgrade-phase-2-synthesis-analysis.md`
3. `Claude-Agents-SDK-Info/tech-stack-specs.md`
4. `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/*SPRITE SHEET COUNCIL RESULTS/Perplexity-Final-Results-Analysis.md`
5. `LoRA Training Research - Perplexity Computer/ref-lora-training-rtx5080-sprite-pipeline.md`
6. `LoRA Training Research - Perplexity Computer/LoRA-training-perplexity-computer-follow-up.md`
7. `Autoresearch-ComfyUI-Overview.md`

### The Prompt

```
You are a senior technical research analyst conducting a comprehensive validation audit for a multi-workstream creative technology project. Your job is to verify whether every tool, model, framework, API, and technical decision referenced in my attached planning documents is still accurate, available, and represents the best option as of today (March 2026).

<context>
I've spent the last 2+ months researching and planning three interconnected workstreams:

WORKSTREAM A — AGENT SDK INFRASTRUCTURE: Building an autonomous agent orchestration layer using the Claude Agent SDK (Python), running across three machines: Mac Mini M4 Pro (24GB, always-on orchestrator), MacBook Pro M4 Pro (48GB, daily driver + heavyweight local inference), and Alienware Aurora with RTX 5080 16GB GDDR7 (CUDA-specialized: ComfyUI, LoRA training, vision QA). Uses Ollama for local inference, MLX on Apple Silicon for 14B-32B models.

WORKSTREAM B — SPRITE SHEET PIPELINE: A Node.js/TypeScript/Oclif CLI pipeline for AI-generated sprite sheet animations for a 2D fighting game (16BitFit Battle Mode, SF2-style). Currently uses Google's Gemini image models (Nano Banana Pro / Nano Banana 2) for single-frame generation. Upgrading to a hybrid keyframe-to-video approach using video models (Pika Pikaframes 2.2, Kling 3.0, Veo) to solve walk cycle temporal coherence. Key component: a Pixel Quantizer that converts video output back to clean pixel art.

WORKSTREAM C — AUTORESEARCH + LoRA TRAINING: Applying Karpathy's autoresearch pattern to automate ComfyUI workflow optimization overnight. Training a style LoRA on Illustrious XL using kohya_ss (dev branch) on the RTX 5080 for sprite generation acceleration.

The attached SOURCE-OF-TRUTH.md contains the full compressed plan. The other attached files contain the detailed technical specs and decisions.
</context>

<task>
Conduct a thorough web research audit covering every category below. For EACH item, search for the latest information and report one of three verdicts:

- CURRENT — Still accurate, still the best option, no changes needed
- UPDATE NEEDED — Still exists but there's a newer version, changed API, or important update
- REPLACED — A significantly better alternative now exists that should be evaluated

Structure your findings in a table per category, then provide a summary of critical changes.
</task>

<categories>

1. VIDEO GENERATION MODELS FOR SPRITE INTERPOLATION
Research the current state of each model as of March 2026:
- Pika Pikaframes 2.2 via fal.ai — Is this still the cleanest multi-keyframe API? Any newer version? Pricing changes?
- Kling 3.0 and Kling 2.6 — Current API availability, start/end frame control, Elements 3.0 character lock status, motion transfer feature
- Google Veo 2/3 — Current version, API access status, any improvements for low-resolution / pixel art use cases
- Wan 2.5 (open source) — Still best open-source option? Any newer I2V models worth testing?
- Retro Diffusion rd-animation — Has this released? Current status for pixel art sprite sheets?
- Any NEW video generation models released since February 2026 that support start/end frame conditioning and could work for sprite interpolation

2. GOOGLE IMAGE GENERATION MODELS (NON-NEGOTIABLE IN PIPELINE)
- Nano Banana Pro (gemini-3-pro-image-preview) — Current status, pricing, any deprecation notices
- Nano Banana 2 (gemini-3.1-flash-image-preview) — Current capabilities, quality benchmarks vs Pro, pricing
- Any NEWER Gemini image models released or announced since March 2026
- Current state of the @google/generative-ai SDK for Node.js — latest version, any breaking changes

3. LoRA TRAINING STACK (RTX 5080 / BLACKWELL sm_120)
- kohya_ss — Is dev branch still required for RTX 5080? Any stable release with sm_120 support yet?
- PyTorch version for sm_120 — Still need nightly cu128? Has a stable release landed?
- xformers vs SDPA — Still need to avoid xformers on Blackwell? Any fixes?
- Illustrious XL v0.1 — Still the best base model for 2D illustration LoRAs? Any v0.2 or alternatives?
- Adafactor optimizer — Still required for fused backward pass on 16GB? Any new optimizer options?
- OneTrainer as alternative — Current RTX 5080 compatibility status
- ComfyUI — Current version, any major updates, RTX 5080 compatibility status, REST API stability
- Any new SDXL base models released since January 2026 that are better than Illustrious XL for 2D illustration / pixel art style LoRAs (check CivitAI, HuggingFace, community discussions)

4. LOCAL INFERENCE STACK
- Ollama — Current version, any major updates, Metal/MPS performance on Apple Silicon
- MLX framework — Current version, performance benchmarks vs Ollama on M4 Pro for 14B-32B models
- Phi-4 (7B via Ollama) — Still best lightweight reasoning model? Any newer small models?
- DeepSeek-R1:14B — Current status, any newer distills or alternatives for reasoning
- Qwen2.5-Coder:14B — Still best local code model at 14B? Any Qwen 3 releases?
- Qwen2.5-VL-7B — Still best local vision model for sprite QA? Any updates?
- Qwen2.5-32B — Still best heavyweight local model for synthesis? Alternatives?
- nomic-embed-text — Still recommended for local embeddings? Any better options?

5. CLAUDE AGENT SDK + CLAUDE CODE
- Claude Agent SDK Python package — Current version, any API changes since Feb 2026
- Claude Code CLI — Current version, any major updates (Agent Teams status, subagent improvements)
- launchd scheduling patterns — Any new best practices for autonomous agent scheduling on macOS
- Claude API pricing — Current Haiku/Sonnet/Opus pricing, any changes to prompt caching

6. AUTORESEARCH (KARPATHY)
- The original autoresearch repo — Any major updates since March 2026 launch?
- The macOS fork (miolini/autoresearch-macos) — Current status, any improvements
- The MLX fork (trevin-creator/autoresearch-mlx) — Current status
- Any new forks or adaptations specifically for image generation or ComfyUI workflows
- Community projects applying the autoresearch pattern to non-LLM-training use cases

7. PIPELINE DEPENDENCIES
- Node.js LTS — Current LTS version
- TypeScript 5.x — Current version, any breaking changes
- Oclif 4.x — Current version, any major updates
- Sharp (image processing) — Current version, any API changes
- TexturePacker CLI — Current version, pricing, any changes
- Puppeteer — Current version, any major updates
- Phaser 3 — Current version, any major updates or Phaser 4 status

8. API PLATFORMS & CLOUD INFRASTRUCTURE
- fal.ai — Current status, pricing model, Pika Pikaframes availability, any outages or deprecations
- Google AI Studio / Vertex AI — Current Gemini API access method, rate limits, any changes to image generation endpoints
- Replicate — Current status for Retro Diffusion, Wan 2.5, or other models used in the pipeline

9. SCORING/EVALUATION MODELS FOR AUTORESEARCH LOOP
- CLIP models — Best current model for image similarity scoring (for the autoresearch composite metric)
- SSIM implementations — Best Python library for structural similarity
- LAION aesthetic predictor — Current status, any better aesthetic scoring models
- Any new image quality assessment models released in 2026

</categories>

<output_format>
For each category, provide a table with columns: Item | Status (CURRENT/UPDATE NEEDED/REPLACED) | Current Version/State | What Changed | Action Required

Then provide a "CRITICAL CHANGES" summary section listing only the items that require action, ranked by impact on the project.

Finally, provide a "NEW OPPORTUNITIES" section listing any tools, models, or approaches you discovered during research that weren't in the original plans but could significantly improve the project.
</output_format>

<validation>
Before finalizing your response:
1. Verify you checked EVERY item listed in the categories above — do not skip any
2. For any item marked UPDATE NEEDED or REPLACED, confirm you've provided the specific version number or link to verify
3. For the NEW OPPORTUNITIES section, only include items you found strong evidence for — no speculative recommendations
4. If you cannot find current information on an item, say so explicitly rather than guessing
</validation>
```

---

## Prompt 2: Execution Blueprint — "How Does This All Come Together?"

### What to Attach (up to 10 files)
1. `SOURCE-OF-TRUTH.md`
2. The output from Prompt 1 (copy-paste or save as a file)
3. `Claude-Agents-SDK-Info/agents-sdk.md`
4. `Claude-Agents-SDK-Info/agent-sdk-upgrade-phase-2-synthesis-analysis.md`
5. `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/hybrid-pipeline-plan.md`
6. `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/claude-code-kickoff-prompt.md`
7. `LoRA Training Research - Perplexity Computer/ref-lora-training-rtx5080-sprite-pipeline.md`
8. `Autoresearch-ComfyUI-Overview.md`
9. `Current-Sprite-Sheet-Pipeline-Workflow-Docs/CLAUDE.md`

### The Prompt

```
You are a senior technical project manager and systems architect creating a detailed execution blueprint for a multi-workstream creative technology project. You have deep expertise in Python automation, Node.js CLI tools, local AI inference, ComfyUI workflows, and LoRA training.

<context>
I'm a solo developer (Associate PM by day, creative technologist by night) executing three interconnected workstreams over the next 12 weeks. I'm a beginner-to-intermediate coder — I know fundamentals but need clear, step-by-step guidance with commands I can copy-paste and explanations of WHY each step matters.

I've attached my SOURCE-OF-TRUTH.md (the master plan) and the validation audit results from my previous research session (Prompt 1 output). I've also attached the detailed technical specs for each workstream.

My hardware:
- Mac Mini M4 Pro (24GB) — always-on, Boston apartment, will be the orchestrator
- MacBook Pro M4 Pro (48GB) — daily driver, portable
- Alienware Aurora RTX 5080 16GB — Windows 11, CUDA workloads, Boston apartment

All three machines are on the same local network. I'm starting from scratch in Boston (just moved, fresh setups needed).

CRITICAL CONSTRAINT: Google's Gemini image generation models (Nano Banana Pro and/or Nano Banana 2) are NON-NEGOTIABLE in the sprite pipeline. They produce the best results for my use case and cost is not a concern for this component. Any execution plan must keep these as the primary image generator.
</context>

<task>
Create a comprehensive, step-by-step execution blueprint that I can follow over the next 12 weeks. This is NOT a high-level plan (I already have that in SOURCE-OF-TRUTH.md). This is the DETAILED HOW — the actual commands, configurations, file contents, and decision points.

For each phase, I need:
1. EXACT setup commands (what to type in terminal, what to install, what config files to create)
2. VERIFICATION steps (how to confirm each setup step worked before moving on)
3. DECISION GATES (points where I need to evaluate results before proceeding)
4. GOTCHAS (common failure modes and how to avoid them, especially for RTX 5080 / sm_120 compatibility)
5. TIME ESTIMATES (realistic hours per task for a beginner-to-intermediate developer)
6. DEPENDENCIES (what must be done before this step, what can run in parallel)

Incorporate any updates from the attached validation audit — if tools have new versions or better alternatives were identified, use those instead of the original specs.
</task>

<phases>

PHASE 1 (Weeks 1-2): FOUNDATION
- Mac Mini setup: Ollama installation, model pulls, launchd configuration, network exposure for LAN access
- MacBook Pro setup: Ollama installation, MLX installation and benchmarking vs Ollama for 14B+ models
- Alienware setup: Ollama with CUDA, ComfyUI fresh install with RTX 5080 compatibility, network configuration
- Three-machine networking: LAN discovery, firewall rules, WOL configuration for Alienware
- hybrid_router.py: Complete implementation with health checking, fallback chain, WOL integration
- Safety hooks: loop-detector.py, cost-watchdog.py, vault-integrity.py — full implementations
- macOS Keychain credential helper setup
- Pixel Quantizer prototype: Full standalone implementation in TypeScript (this runs on MacBook, independent of Agent SDK)

PHASE 2 (Weeks 3-4): FIRST AGENTS + VIDEO MODEL TESTING
- First autonomous agents: Process Inbox + Spending Analysis with launchd schedules on Mac Mini
- Baton File dependency chain implementation
- Nano Banana 2 vs Pro benchmarking methodology for sprite quality
- Video model API setup: fal.ai account, Pika/Kling/Veo API access
- Video model evaluation sprint: exact test methodology, scoring rubric, comparison framework
- Pixel Quantizer integration with video model output

PHASE 3 (Weeks 5-6): PIPELINE INTEGRATION + PM AGENTS
- Generator adapter interface implementation (4 atomic operations in TypeScript)
- Best-performing video model wired into hybrid pipeline
- End-to-end hybrid test: 1 Champion walk cycle through full pipeline
- PM agents: Sprint Health Monitor, Meeting Defender
- Jira MCP setup with Keychain credentials

PHASE 4 (Weeks 7-8): LoRA + MEMORY LAYER
- kohya_ss dev branch installation on Alienware (exact steps for RTX 5080)
- Dataset preparation: image selection, captioning, directory structure
- First LoRA training run with monitoring
- LoRA integration into ComfyUI pipeline
- Memory agents: Vault Embedding Indexer, Preserve Session, PR Digest

PHASE 5 (Weeks 9-12): AUTORESEARCH + SCALE
- autoresearch-loop/ scaffolding: generic loop_runner.py + ComfyUI experiment module
- Overnight optimization configuration
- Pipeline scaling: batch generation for additional Champions
- Meta-Agent implementation
- Fleet optimization: prompt caching scheduling, token audit

</phases>

<output_format>
Structure the document as a step-by-step manual with this format for each task:

### [Task Name] — [Time Estimate]
**Depends on:** [list prerequisites]
**Can parallel with:** [list independent tasks]
**Machine:** [which machine this runs on]

**Steps:**
1. [Command or action]
   ```
   [exact terminal command if applicable]
   ```
   **Why:** [brief explanation of what this does and why it matters]
   **Verify:** [how to confirm it worked]

2. [Next command...]

**Decision Gate:** [if applicable — what to evaluate before proceeding]
**Gotchas:** [common failure modes and fixes]
</output_format>

<validation>
Before finalizing:
1. Verify every command is compatible with the correct OS (macOS for Mac Mini/MacBook, Windows 11 for Alienware)
2. Verify RTX 5080 commands use CUDA 12.8+ and PyTorch nightly cu128 (or stable if available per the validation audit)
3. Verify no step assumes tools or accounts that haven't been set up in a previous step
4. Verify the Gemini image models are used as primary generators — never replaced or made optional
5. Verify time estimates are realistic for someone who knows coding fundamentals but isn't an expert
6. Check that parallel tasks are truly independent (no hidden dependencies)
</validation>
```

---

## Prompt 3: Opportunity Scanner — "What Am I Missing?"

### What to Attach (up to 10 files)
1. `SOURCE-OF-TRUTH.md`
2. The output from Prompt 1 (validation audit)
3. `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/*SPRITE SHEET COUNCIL RESULTS/Perplexity-Final-Results-Analysis.md`
4. `Autoresearch-ComfyUI-Overview.md`
5. `*2-12-UPDATED SpriteSheet Workflow-Perplexity-Council-Review/workflow-operations-guide.md`

### The Prompt

```
You are a creative technology strategist and AI workflow researcher. Your specialty is finding non-obvious connections between emerging tools, novel techniques, and existing project architectures. You think like a product manager who also builds things — you balance ambition with practicality.

<context>
I'm building a three-workstream creative technology project:

1. AN AUTONOMOUS AGENT SYSTEM using the Claude Agent SDK, orchestrated across three machines (Mac Mini M4 Pro, MacBook Pro M4 Pro, Alienware RTX 5080), handling everything from daily task automation to creative pipeline management.

2. A HYBRID AI SPRITE SHEET PIPELINE for a 2D fighting game (Street Fighter II style, 12 fighters × 13 animations). Uses Google's Gemini image models (Nano Banana Pro/2) for keyframe generation and video models for motion interpolation, with a Pixel Quantizer to convert video output back to pixel art. Full audit pipeline, retry logic, Phaser 3 validation.

3. AN AUTORESEARCH OPTIMIZATION LOOP inspired by Karpathy's autoresearch, adapted for ComfyUI workflow parameter optimization. Runs overnight on the RTX 5080, automatically tuning sampler settings, CFG scale, LoRA weights, etc.

I've also trained (or plan to train) a style LoRA on Illustrious XL for sprite generation acceleration.

The attached files contain my complete plans and a validation audit of the current tool landscape. My plans were mostly finalized in February 2026, so they're about 6 weeks old.
</context>

<task>
Conduct deep research across the web to find opportunities I may be missing. I want you to search aggressively — GitHub repos, Twitter/X threads, Reddit posts, blog posts, research papers, product launches, and community discussions from the last 60 days (February-March 2026).

Search for opportunities in EACH of these categories:
</task>

<categories>

1. SPRITE GENERATION BREAKTHROUGHS
- Any new AI models, tools, or techniques specifically for generating consistent 2D game sprites or sprite sheet animations
- New approaches to temporal coherence in AI-generated frame sequences
- Novel pixel art generation or conversion techniques
- Any projects combining video models with sprite sheet output
- Community solutions for the "walk cycle problem" in AI sprite generation
- New ControlNet models or techniques relevant to pose-controlled sprite generation

2. COMFYUI ECOSYSTEM UPDATES
- New ComfyUI custom nodes released in Feb-March 2026 that could benefit sprite generation
- ComfyUI workflow automation tools or API improvements
- New ComfyUI-native video generation or frame interpolation nodes
- Community ComfyUI workflows specifically for game asset creation
- Any ComfyUI + autoresearch integrations others have built

3. AUTORESEARCH ADAPTATIONS
- Projects that have adapted Karpathy's autoresearch pattern for image generation, ComfyUI, or creative workflows (not just LLM training)
- Novel evaluation metrics for image quality that could serve as the "val_bpb equivalent" for sprite generation
- Automated prompt optimization tools or techniques
- Any research on automated hyperparameter tuning specifically for diffusion models

4. AGENT ORCHESTRATION INNOVATIONS
- New patterns or tools for multi-machine AI agent orchestration
- Better alternatives to launchd for scheduling autonomous agents on macOS
- Novel approaches to agent-to-agent communication or coordination
- New local inference optimization techniques for Apple Silicon (M4 Pro specifically)
- Any Claude Agent SDK community projects, patterns, or tools released since Feb 2026

5. PIPELINE ARCHITECTURE PATTERNS
- Other projects building manifest-driven creative asset pipelines (games, animation, or otherwise)
- Novel approaches to quality gating / automated visual QA for AI-generated images
- Better image similarity metrics than CLIP + SSIM for pixel art specifically
- Tools for automated sprite sheet validation or game engine integration testing
- Post-processing pipelines others have built for converting AI output to game-ready assets

6. LoRA AND FINE-TUNING ADVANCES
- New base models better than Illustrious XL for 2D illustration/pixel art (released Feb-March 2026)
- New training techniques that reduce VRAM requirements below 10GB for SDXL LoRAs
- Novel approaches to style transfer that don't require LoRA training at all
- IP-Adapter or similar reference-based generation improvements
- Any community LoRAs specifically for fighting game sprites or pixel art animation

7. CROSS-POLLINATION OPPORTUNITIES
- Tools or techniques from adjacent domains (film VFX, motion capture, traditional animation) that could apply to this pipeline
- Novel uses of AI agents for creative production that I might adapt
- Any interesting integrations between Claude Code / Claude Agent SDK and creative tools
- Emerging platforms or services that could replace multiple tools in my stack

</categories>

<output_format>
For each category, provide:

**[Category Name]**

For each finding:
- **What:** [Name of tool/technique/project]
- **Where:** [Link — GitHub, blog post, tweet, etc.]
- **Relevance:** [Specific explanation of how this connects to my project]
- **Effort to Integrate:** Low / Medium / High
- **Impact:** Low / Medium / High
- **Recommendation:** [Should I pursue this? When in the timeline? What would it replace or enhance?]

End with a **TOP 5 HIGHEST-IMPACT OPPORTUNITIES** ranked list, explaining which are "do now" vs "monitor for later."
</output_format>

<constraints>
- Only include findings with verifiable links or sources — no speculative suggestions
- Prioritize findings from the last 60 days (Feb-March 2026) — the landscape moves fast
- Don't suggest replacing Google's Gemini image models — those are locked in as non-negotiable
- Be honest when a finding is interesting but impractical for a solo developer
- If you find something that directly contradicts a decision in my plans, flag it explicitly
</constraints>

<validation>
Before finalizing:
1. Verify every link you provide is to a real, accessible resource
2. Verify your "Effort to Integrate" assessments account for the fact that I'm a beginner-to-intermediate developer
3. Verify your TOP 5 list doesn't include items that would derail the core timeline — they should enhance it, not replace it
4. Check that you've searched all 7 categories — don't skip any
</validation>
```

---

## Execution Order

```
STEP 1: Run Prompt 1 (Stack Validation Audit)
         ↓
         Save output as a file
         ↓
STEP 2: Run Prompt 2 (Execution Blueprint) — attach Prompt 1 output
         ↓
STEP 3: Run Prompt 3 (Opportunity Scanner) — attach Prompt 1 output
         (Prompts 2 and 3 can run in parallel if you want)
         ↓
STEP 4: Bring outputs back to Claude Cowork or Claude Code
         for final synthesis into your SOURCE-OF-TRUTH.md update
```

---

## Optional: Model Council Bonus Prompt

If you want to validate the most contentious decisions using Perplexity's Model Council feature (runs your query through Claude Opus, GPT-5.2, and Gemini 3 Pro simultaneously), here's a focused prompt:

### What to Attach
1. `SOURCE-OF-TRUTH.md`

### The Prompt (Use Model Council mode, not Computer)

```
I'm building a hybrid AI sprite sheet pipeline for a 2D fighting game (Street Fighter II style, 128×128 pixel art). I generate keyframes with Google Gemini's image models, then interpolate motion with video models, then convert video output back to pixel art through a "Pixel Quantizer" (nearest-neighbor downscale, palette snap, temporal smoothing, outline enforcement, alpha recovery).

I need you to evaluate THREE specific decisions and tell me if they're the right call as of March 2026:

DECISION 1: For video model interpolation of walk cycles, should I prioritize Pika Pikaframes 2.2 (via fal.ai, multi-keyframe), Kling 3.0 (start/end frame + Elements character lock), or Kling 2.6 (motion transfer from reference video)? Which gives me the best temporal coherence for 4-8 frame walk cycle sequences at 128×128 pixel art?

DECISION 2: For my Pixel Quantizer's composite scoring metric (used in the autoresearch optimization loop), I'm planning: 0.4 × CLIP_similarity + 0.3 × SSIM_to_anchor + 0.3 × aesthetic_score. Is this the right metric weighting? Are there better metrics specifically for pixel art quality evaluation in 2026?

DECISION 3: For LoRA training on my RTX 5080 (16GB GDDR7), should I use Illustrious XL v0.1 as the base model with kohya_ss, or is there a better base model for 2D illustration/pixel art style LoRAs that's released since January 2026?

For each decision, tell me: what you recommend, your confidence level (high/medium/low), and what you'd test first.
```

---

*Generated by Claude Cowork using the prompt-engineering skill. Prompts follow the 9-technique checklist: clarity, context, XML structure, role assignment, output format specification, constraints, and validation steps.*
