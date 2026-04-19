# Technical Validation Audit — Sean's Agentic Frameworks & Creative Pipeline
**Date:** March 27, 2026
**Scope:** All tools, models, frameworks, APIs, and technical decisions across three workstreams
**Verdict Legend:** CURRENT = no changes needed | UPDATE NEEDED = newer version or important change | REPLACED = significantly better alternative exists

---

## Category 1: Video Generation Models for Sprite Interpolation

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **Pika Pikaframes 2.2 via fal.ai** | CURRENT | v2.2, still on fal.ai. $0.04/sec (720p), $0.06/sec (1080p). 2-5 keyframes, max 25 seconds total. | Pricing stable. API unchanged. Still the cleanest multi-keyframe interpolation API available. No v2.3 or v3.0 announced. | None — proceed as planned. |
| **Kling 3.0** | CURRENT | Launched Feb 4, 2026. Start/end frame control confirmed working. Multi-Shot "AI Director" feature added. 3-15 second flexible duration. Native audio generation. | Elements feature provides character consistency (replaces Elements 3.0 naming). Multi-shot storyboarding is new — enables multiple camera angles in single 15-sec generation. | Test Multi-Shot feature for animation sequences. Start/end frame API confirmed viable. |
| **Kling 2.6** | CURRENT | Launched Dec 2025. Motion transfer from reference video confirmed. Simultaneous audio-visual generation. Up to 2 minutes at 1080p/30fps. | No changes since your assessment. Motion transfer feature remains available. | Test motion transfer with canonical walk cycle video as planned. |
| **Google Veo 3.1** | UPDATE NEEDED | `veo-3.1-generate-preview` and `veo-3.1-fast-generate-preview` available via Gemini API. Updated January 2026. Native 4K, vertical video, character consistency improvements. | Your docs reference "Veo 2/3" — the current version is **Veo 3.1**. Native 4K resolution and synchronized audio are new. However, 4K is overkill for 128px sprites. Resolution mismatch concern from your docs remains valid. | Update model reference to Veo 3.1. Low priority for sprite work due to resolution mismatch — test last. |
| **Wan 2.5** | UPDATE NEEDED | Wan 2.2 is the latest **open-source** version. Wan 2.5/2.6 exist as proprietary models but Alibaba has NOT open-sourced them. Community is skeptical they ever will. Previous open-sourcing promises were deleted. | Your docs assume Wan 2.5 is open source. It is NOT publicly available. **Wan 2.2 is the open-source option** — it does 1080p 10-second videos with audio. | Downgrade to Wan 2.2 in your plans, or monitor for a potential Wan 2.5 open release. Don't count on it. |
| **Retro Diffusion rd-animation** | UPDATE NEEDED | **Released and live on Replicate** (`retro-diffusion/rd-animation`). 4.9K runs. Also available on Scenario platform. Generates animated pixel art sprite sheets with low frame counts matching game engine conventions. | Your docs said "monitor for release" — **it has released**. Available via Replicate API and Scenario. Purpose-built for pixel art sprite sheets. Style presets include `four_angle_walking`. | **Evaluate immediately.** This could bypass post-processing entirely for certain animations. Test via Replicate API before building complex hybrid pipeline. |

**New video models since February 2026:**

| Item | Status | Details | Relevance |
|------|--------|---------|-----------|
| **Seedance 2.0** | NEW | Launched Feb 7, 2026 by ByteDance. Reference-to-video: upload reference image + prompt. Expression/motion transfer from reference video. 3D scene input support. | Strong character consistency. Expression transfer onto new characters. Worth testing for sprite animation if it handles pixel art. |
| **LTX-2** | NEW | Open-source. Native 4K@50fps, 20-second videos, synchronized audio. Apache 2.0 license. NVIDIA-optimized (NVFP8). Runs on consumer RTX GPUs. | True open-source alternative to Wan 2.2 with better specs. Could run locally on RTX 5080. Worth evaluating for local video generation. |

---

## Category 2: Google Image Generation Models

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **Nano Banana Pro** (`gemini-3-pro-image-preview`) | CURRENT | Active, fully documented. ~$0.035/image at 1024×1024. ELO 1235 (ranked #2 on LM Arena March 2026). | Still top-tier. No deprecation notices. Costs stable. | None — still your anchor/keyframe generator. |
| **Nano Banana 2** (`gemini-3.1-flash-image-preview`) | CURRENT | Released Feb 26, 2026. 4K resolution support. Image Search Grounding. ~$0.01-0.02/image. "Pro quality at Flash speed." | This is newer than your docs indicate (your docs say "March 2026 model update" — it actually landed late February). Key new capability: **4K output** — first Flash model with Ultra HD. | Benchmark against Pro for sprite keyframes as planned. The 3-5x cost savings are significant for volume generation. |
| **Gemini 2.0/2.5 models** | UPDATE NEEDED | `gemini-2.0-flash-001` deprecated as of March 6, 2026 for new customers. Full retirement June 1, 2026. `gemini-2.5-flash` retires June 17, 2026. `gemini-2.5-flash-image` retires October 2, 2026. | If any pipeline code references 2.0 or 2.5 model IDs, they will break. The base "Nano Banana" (`gemini-2.5-flash-image`) has a retirement date. | Ensure all code uses `gemini-3-pro-image-preview` or `gemini-3.1-flash-image-preview`. Do not reference older model IDs. |
| **@google/genai SDK** (Node.js) | UPDATE NEEDED | **New package name**: `@google/genai` (v1.20.0). Requires Node.js 20+. Uses `GoogleGenAI` class, not `GoogleGenerativeAI`. | Your docs reference `@google/genai` which is correct — but verify your import path matches the new API. The old `@google/generative-ai` package is deprecated. Key change: `ai.models.generateContent()` method pattern. API defaults to beta endpoints. | Verify pipeline uses `@google/genai` (not `@google/generative-ai`). Check import patterns match v1.x API. |

**New image generation models worth noting:**

| Item | Details | Relevance |
|------|---------|-----------|
| **GPT Image 1.5** | ELO 1264, #1 on LM Arena. Best text rendering. ~$0.04-0.17/image. | Not useful for sprites (OpenAI, not in your adapter layer). Note for awareness only. |
| **Flux 2 (Max/Pro/Dev)** | Black Forest Labs. Dev variant is open-weight and self-hostable. ELO 1149-1168. | Flux 2 Dev could be self-hosted on RTX 5080 as an alternative to Illustrious XL for certain tasks. Monitor. |

---

## Category 3: LoRA Training Stack (RTX 5080 / Blackwell sm_120)

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **kohya_ss** | CURRENT | Dev branch still required for RTX 5080. `gui-uv.bat` launcher remains the recommended install path. Main repo actively maintained. | No stable release with native sm_120 support yet. The dev branch + `gui-uv.bat` approach is still the path of least resistance. Community reports are consistent with your docs. | None — proceed with dev branch as planned. |
| **PyTorch for sm_120** | UPDATE NEEDED | **PyTorch 2.7.0 stable with CUDA 12.8 now supports sm_120 officially.** Confirmed by PyTorch team (Feb 2026). PyTorch 2.10.0+cu128 confirmed working on RTX 5060 Ti with native sm_120 kernels. | Your docs say "need nightly cu128" — this is no longer true. **Stable releases ≥2.7.0 built with cu128 work.** The key is the CUDA toolkit version in the wheel name: `cu128` = sm_120 support. `cu126` and below = no support regardless of PyTorch version. | Update docs: recommend `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128` (stable, not nightly). |
| **xformers on Blackwell** | CURRENT | Still causes `cutlassF: no kernel found` on some setups. SDPA remains the safe path. Some users report success with `pip3 install --pre -U --no-deps xformers` but inconsistent. | No fix landed. Your recommendation to avoid xformers and use SDPA is still correct. | None — continue recommending SDPA. |
| **Illustrious XL** | UPDATE NEEDED | **v2.0 is now available** on HuggingFace (`OnomaAIResearch/Illustrious-XL-v2.0`). Includes v2.0 BASE and v2.0 STABLE variants. A **v3 series** also exists (v3.0 Creative, v3.0 Expressive, v3.5, v3.6) available on illustrious-xl.ai. | Your docs reference v0.1 — there are now significantly newer versions. v2.0 uses cosine annealing LR schedule. v3.x series is described as "high-fidelity." The platform now has 91 finetunes and 208 merges. | **Evaluate Illustrious XL v2.0-STABLE** as your new base model. It should produce better results with fewer training steps. v3.x may be available through their platform but check if weights are downloadable for local ComfyUI use. |
| **Adafactor optimizer** | CURRENT | Still required for fused backward pass on 16GB VRAM. No new optimizer options that change this constraint. | Prodigy is still pathologically slow on Blackwell. AdamW works but uses more VRAM without fused backward pass. | None. |
| **OneTrainer** | UPDATE NEEDED | Confirmed working on RTX 5080 with PyTorch nightly cu128 alongside ComfyUI. RTX 5090 requires PyTorch 2.8+ with CUDA 12.8. | Better 5080 support than when you last assessed. Community suggests it may have better 50-series optimization than kohya_ss for some configurations. | Keep as secondary option. If kohya_ss gives you trouble, OneTrainer is now a viable fallback on your 5080. |
| **ComfyUI** | UPDATE NEEDED | v0.18.2 (March 25, 2026). Now has NanoBanana2 API node built-in. FP16 support fixes. CacheProvider API for distributed caching. Python 3.13 support. NVFP4 checkpoint support added. 50xx GPU support confirmed in community builds. | Significant updates since your planning. NanoBanana2 API node means you can call Gemini image generation directly from ComfyUI workflows. REST API still stable (`POST /prompt`, `GET /history`). | Update ComfyUI to v0.18.2. The built-in NanoBanana2 node could simplify your pipeline integration. |

**New SDXL base models for 2D illustration:**

| Item | Details | Relevance |
|------|---------|-----------|
| **NoobAI XL** | Illustrious finetune with broader stylistic range. Cross-compatible with Illustrious LoRAs. | Already in your docs as an alternative. Still valid. |
| **Flux 2 Dev** (12B) | Open-weight, self-hostable. Better text rendering and anatomy than SDXL. NF4 quantization fits ~9GB VRAM. | ControlNet/IP-Adapter ecosystem still less mature than SDXL. Monitor but don't switch yet. |

---

## Category 4: Local Inference Stack

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **Ollama** | UPDATE NEEDED | v0.5.x (March 2026). Compiled for NVIDIA Blackwell. Improved model scheduling, multi-GPU support, structured outputs. New web search API. Cloud models in preview. Default context window now 4096. Llama 4, Phi 4 reasoning models, Qwen3-VL all supported. | Major improvements since your planning. Blackwell compilation = better RTX 5080 performance. New model scheduler reduces OOM crashes. Structured outputs are native. | Update Ollama on all three machines to latest 0.5.x. Take advantage of structured outputs for agent responses. |
| **MLX** | UPDATE NEEDED | v0.29.2 (latest). Apple published research on "Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU" — MLX now supports M5 Neural Accelerators. Works with all Apple Silicon. Install: `pip install mlx`. MLX LM for chat: `pip install mlx-lm`. | MLX continues to improve but v0.29.2 is an incremental update. The M4 Pro performance gains you anticipated are real. `mlx-lm` package handles model loading from HuggingFace directly. | Benchmark MLX vs Ollama on MacBook Pro during Phase 1 as planned. Use `mlx-lm` for inference. |
| **Phi-4 (7B via Ollama)** | UPDATE NEEDED | Phi-4 is now a 14B model (not 7B as in your docs). **Phi-4-mini** is the 3.8B lightweight variant. **Phi-4-mini-reasoning** (3.8B) is new — outperforms models 2x its size on math/reasoning, comparable to OpenAI o1-mini. **Phi-4-reasoning** is 14B — rivals DeepSeek-R1 Distill 70B. | Your docs assign "Phi-4 (7B)" to Mac Mini tasks. The actual models available are: `phi4-mini` (3.8B, general), `phi4-mini-reasoning` (3.8B, reasoning), `phi4-reasoning` (14B, heavy reasoning). | Replace "Phi-4 (7B)" references with `phi4-mini` (3.8B) for Mac Mini lightweight tasks. Consider `phi4-mini-reasoning` for inbox triage — it's better at structured reasoning. |
| **DeepSeek-R1:14B** | UPDATE NEEDED | Still available. But **Qwen3 14B (Reasoning)** now outperforms it on most benchmarks: MATH 500 (96.1% vs 93.5%), LiveCodeBench (52.3% vs 26.6%), AIME (76.3% vs 67.0%). Also, **DeepSeek R2** has been announced. | Qwen3 14B reasoning variant is stronger across the board at similar size. DeepSeek R2 successor is coming but not yet widely available for local use. | Evaluate **Qwen3-14B** as replacement for DeepSeek-R1:14B on the MacBook Pro for financial analysis. Pull via Ollama: `ollama pull qwen3:14b`. |
| **Qwen2.5-Coder:14B** | UPDATE NEEDED | Still available. But **Qwen3-Coder-Next** (80B total, 3B active via MoE) now exists — scores 44.3% on SWE-Bench Pro vs Sonnet 4.5's 46.1%. Requires 64GB RAM. **Qwen2.5-Coder-32B** is noted as "beats larger models at code" in comparisons. | The 14B coder is still solid, but the landscape has shifted. Qwen3-Coder-Next is too large for your MacBook (needs 64GB+). Qwen2.5-Coder-32B fits on MacBook Pro's 48GB via MLX. | Consider upgrading to **Qwen2.5-Coder-32B** on MacBook Pro for code review. It fits in 48GB unified memory via MLX and is meaningfully better than the 14B. |
| **Qwen2.5-VL-7B** | UPDATE NEEDED | Still available. But **Qwen3-VL** series has launched. Qwen3-VL features DeepStack for better image-text correlation, Interleaved-MRoPE for spatial encoding, text-timestamp alignment for video. Sizes include smaller variants. Also **Qwen3.5 VL** family announced March 2026. | Qwen3-VL is meaningfully better at visual understanding. The 7B size class should have a Qwen3-VL equivalent. | Check if `qwen3-vl:7b` is available in Ollama for sprite vision QA. If so, upgrade. |
| **Qwen2.5-32B** | UPDATE NEEDED | Still available. But **Qwen3.5-122B** (MoE, only 10B active) now exists — runs on 64GB MacBook, beats GPT-5-mini, Apache 2.0 license. Also **Qwen3.5-9B** rivals larger models. | Qwen3.5 at 122B with only 10B active is very interesting for your MacBook Pro, but verify it fits in 48GB. Qwen3.5-9B could replace the 32B for lighter synthesis tasks. | Test whether **Qwen3.5** variants run on MacBook Pro via MLX. The 10B-active MoE could be faster than Qwen2.5-32B while being smarter. |
| **nomic-embed-text** | CURRENT | Still recommended. Nomic Embed Text V2 available with multilingual support and Matryoshka representation learning. Max 512 tokens input. | V2 exists with improvements but V1 is fine for vault embeddings. Alternatives include GemmaEmbedding (308M, 100+ languages, 2000 tokens) and Arctic Embed 2.0. | None for now. V1 is sufficient for vault embedding. Consider V2 if you hit multilingual needs. |

---

## Category 5: Claude Agent SDK + Claude Code

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **Claude Agent SDK Python** | UPDATE NEEDED | Latest release March 20, 2026 on PyPI. Package renamed from `claude-code-sdk` to `claude-agent-sdk`. `ClaudeCodeOptions` renamed to `ClaudeAgentOptions`. New features: `fork_session` for resuming sessions, programmatic subagents, custom tools as Python functions (no subprocess), settings isolation, `create_sdk_mcp_server()` for in-process MCP tools. Requires Python 3.10+. CLI auto-bundled. | **Breaking changes**: Class renames (`ClaudeCodeOptions` → `ClaudeAgentOptions`), merged system_prompt config, package name change. New capabilities: in-process MCP server (no IPC overhead), dynamic permission mode, model switching. | Update all imports. Use `claude_agent_sdk` and `ClaudeAgentOptions`. The in-process MCP server is a significant improvement for custom tools — rewrite ComfyUI MCP wrapper to use `create_sdk_mcp_server()`. |
| **Claude Code CLI** | UPDATE NEEDED | v2.1.81+ (bundled). **Agent Teams now available** since v2.1.32 (Feb 5, 2026). Teams are no longer experimental — full documentation exists. Shared task lists, direct teammate messaging, plan approval workflow, display modes (tmux split-pane). | Your docs say "Agent Teams are experimental, use subagents for 90%." Teams are now production-ready with proper coordination primitives. Lead creates team, spawns teammates, shared task list, plan approval gates. One team per session, no nested teams. | Update your assessment: Agent Teams are ready for complex multi-agent work (sprint rebuilds, parallel research). Still use subagents for focused single tasks. |
| **launchd scheduling** | CURRENT | No changes to macOS launchd patterns. Your Baton File / WatchPaths approach remains best practice. | No updates. | None. |
| **Claude API Pricing** | UPDATE NEEDED | **Haiku 4.5**: $1/$5 per MTok. **Sonnet 4.6**: $3/$15 per MTok (1M context at standard pricing). **Opus 4.6**: $5/$25 per MTok (1M context at standard pricing, 67% cheaper than Opus 4.1's $15/$75). Batch: 50% discount. Prompt caching: $3.75/MTok write, $0.30/MTok read (5-min TTL). | Opus pricing dropped dramatically — $5/$25 vs old $15/$75. Both Sonnet 4.6 and Opus 4.6 include **full 1M context at standard pricing** (no surcharge). This changes your cost model significantly — Opus is now viable for more agent tasks. | Recalculate cost projections. At $5/$25, Opus 4.6 may be worth using for synthesis tasks instead of routing to local 32B models. The prompt caching 5-min window trick from your docs is still valid. |

---

## Category 6: Autoresearch (Karpathy)

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **karpathy/autoresearch** | CURRENT | 42,000+ GitHub stars. 36 commits. Three-file architecture unchanged. Metric: `val_bpb`. 5-minute time budget per experiment. Uses `uv` for dependency management. | Stable. Karpathy hasn't made structural changes — the repo is intentionally minimal. Community adoption is massive (Fortune called it "The Karpathy Loop"). Shopify CEO used it to get 53% faster rendering from 93 automated commits. | None — your ComfyUI mapping of the three-file architecture is sound. |
| **miolini/autoresearch-macos** | CURRENT | Supports macOS (Apple Silicon / MPS) and CPU. Removes FlashAttention-3 dependency, falls back to PyTorch SDPA. Adapts for Metal memory bounds. Platform verification at startup. | No major updates. The fork is stable and functional for Mac. `uv sync` to install, runs on MPS. | Viable for Mac Mini overnight runs as planned. |
| **trevin-creator/autoresearch-mlx** | CURRENT | Runs natively on Apple Silicon through MLX with no PyTorch dependency. | No updates found. Still an option for pure MLX inference. | Lower priority — the macOS fork with MPS is more battle-tested. |
| **ComfyUI-specific forks** | NOT FOUND | No dedicated autoresearch fork for ComfyUI or image generation was found. | The community is applying the pattern broadly (prompt optimization, skill improvement, code optimization) but no one has published a ComfyUI-specific implementation. | **You'll be building this from scratch.** The PM's Guide to Autoresearch confirms the pattern works on "anything you can score" — your ComfyUI mapping is the right approach. Use `optuna` for Bayesian optimization as planned. |

---

## Category 7: Pipeline Dependencies

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **Node.js LTS** | CURRENT | **v24 "Krypton"** is Active LTS. v22 "Jod" is Maintenance LTS. v25 is Current. v20 still in Maintenance. Starting with v27 (April 2027), every release becomes LTS. | v24 is the recommended LTS. Security patches released March 24, 2026 for all active lines. | Ensure pipeline runs on Node.js 24.x LTS. The `@google/genai` SDK requires Node.js 20+. |
| **TypeScript** | CURRENT | **v5.8** is the current widely-adopted version. No breaking changes for your use case. Improvements in control flow analysis, exact optional property types. | Incremental improvements. No TypeScript 6.x announced. | None. Ensure `tsconfig.json` uses recommended 2026 settings (target ES2022, module NodeNext). |
| **Oclif** | CURRENT | **v4.17.46** (April 2026). Regular dependency bumps. Core at v4.2.10+. Plugin ecosystem active. | No breaking changes. Dependency updates only. | None — your CLI framework is stable. |
| **Sharp** | CURRENT | **v0.34.5**. Supports Node-API v9 (Node.js ≥18.17.0). libvips v8.17.2 under the hood. WEBP, AVIF support. `kernel.nearest` for nearest-neighbor still available. | No breaking changes. Performance improvements. | None — `sharp.kernel.nearest` for your pixel quantizer downscale step is still available. |
| **TexturePacker CLI** | CURRENT | **v7.12.0** (Feb 4, 2026). Perpetual single-user license. Supports macOS 26. CLI and batch processing available in all paid licenses. Phaser exporter with 9-slice scaling support. | Minor version update. Pricing model unchanged (perpetual license). | None. |
| **Puppeteer** | CURRENT | **v24.40.0** (March 19, 2026). Supports Chrome 146 and Firefox 148. New APIs: Browser window bounds, focused page emulation, heap snapshots. | Active development, no breaking changes for headless Phaser validation. | None — your headless Phaser validation workflow is unaffected. |
| **Phaser 3** | UPDATE NEEDED | Phaser 3 is stable but **Phaser 4 is at Release Candidate 7** (March 25, 2026). RC7 includes better pixel art controls, 6 tint modes, performance improvements. "Already more powerful and more reliable than Phaser 3 ever was." | Phaser 4 is close to full release. RC3 specifically improved pixel art options. However, Phaser 3 is not deprecated and your pipeline uses it for headless validation only. | **No action now**, but monitor Phaser 4 stable release. When 16BitFit Battle Mode ships, it should target Phaser 4. Your headless validation can stay on Phaser 3 for now. |

---

## Category 8: API Platforms & Cloud Infrastructure

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **fal.ai** | CURRENT | Active platform. H100s from $1.89/hr, H200s and B200s available. Pika v2.2 Pikaframes confirmed available. Competitive pricing across 300+ models. Alternatives emerging (Atlas Cloud claims 30-50% cheaper for high volume). | Stable. No outages or deprecations affecting your pipeline. Seedream V4, Flux Kontext Pro, and other models also available. | None — continue using for Pika Pikaframes API access. |
| **Google AI Studio / Vertex AI** | UPDATE NEEDED | `@google/genai` SDK provides unified interface to both Gemini Developer API and Vertex AI. API defaults to beta endpoints. Set `apiVersion: 'v1'` for stable. Model lifecycle page shows retirement dates for all models. | Unified SDK means you can prototype on AI Studio and migrate to Vertex AI without code changes. Check model retirement dates — `gemini-2.0-flash-001` retires June 1, 2026. | Ensure pipeline uses stable model IDs (`gemini-3-pro-image-preview`, `gemini-3.1-flash-image-preview`). Consider setting `apiVersion: 'v1'` for production stability. |
| **Replicate** | CURRENT | Active. Retro Diffusion suite (rd-fast, rd-plus, rd-tile, **rd-animation**) all available. Wan 2.1/2.2 models available. Active ecosystem. | Retro Diffusion rd-animation has 4.9K runs — community validated. | Use Replicate API for rd-animation testing. |

---

## Category 9: Scoring/Evaluation Models for Autoresearch Loop

| Item | Status | Current Version/State | What Changed | Action Required |
|------|--------|-----------------------|--------------|-----------------|
| **CLIP models** | CURRENT | OpenAI CLIP remains the standard for multimodal image-text embeddings. Still rated 4.8/5 in 2026 embedding rankings. `transformers` library for inference. SigLIP and EVA-CLIP are alternatives with improvements in some domains. | No paradigm shift. CLIP cosine similarity remains the standard approach for image similarity scoring. | None — use CLIP via `transformers` library as planned. |
| **SSIM implementations** | CURRENT | `scikit-image` (`skimage.metrics.structural_similarity`) remains the standard Python implementation. | No changes. | None. |
| **LAION aesthetic predictor** | CURRENT | Still available and functional. Architecture: linear MLP on top of CLIP embeddings. A January 2026 academic audit paper analyzed its biases but didn't replace it. No better single-score aesthetic predictor has emerged. | The model has known biases (documented in arxiv.org/html/2601.09896v2) but no superior replacement exists for automated aesthetic scoring of generated images. | Use as planned. Be aware of biases — calibrate with manual review of scores against your specific pixel art style. |
| **LPIPS** | CURRENT | `lpips` library for perceptual similarity. Still the primary metric for style/perceptual consistency. | No changes. | None. |
| **New in 2026** | NEW | Multi-model scoring approaches are trending: "multi-index embeddings" (global + object-crop + domain-specific embeddings per item). Vision LLM grading (Claude/GPT-4V) for subjective quality is becoming more practical. | The composite metric approach in your docs (CLIP + SSIM + aesthetic) is aligned with best practices. Vision LLM batch grading adds a useful human-like evaluation layer. | Consider adding a Qwen3-VL local vision scoring step as a 4th metric (runs free on Alienware). |

---

## CRITICAL CHANGES (Ranked by Impact)

### 1. **Retro Diffusion rd-animation Has Released** (Workstream B — HIGH IMPACT)
Your docs say "monitor for release." It's live on Replicate with 4.9K runs. Purpose-built for animated pixel art sprite sheets. This could bypass your entire pixel quantizer for certain animations. **Test this before building complex hybrid pipeline infrastructure.** It may reduce the scope of the Pixel Quantizer to only video model outputs, not all outputs.

### 2. **Illustrious XL v2.0 and v3.x Released** (Workstream C — HIGH IMPACT)
You're planning to train on v0.1. There are now v2.0-STABLE and v3.x variants available. Training on a newer base model will likely produce significantly better LoRA results with fewer steps. **Download and test v2.0-STABLE before beginning LoRA training.**

### 3. **Claude Agent SDK Breaking Renames** (Workstream A — MEDIUM-HIGH IMPACT)
Package renamed from `claude-code-sdk` to `claude-agent-sdk`. Classes renamed. All your Python agent scripts need import updates before they'll work with the latest SDK. **Must fix before any agent development begins.**

### 4. **Wan 2.5 is NOT Open Source** (Workstream B — MEDIUM IMPACT)
Your docs assume Wan 2.5 is available as an open-source option. It isn't. Wan 2.2 is the latest open-source version. Adjust plans or evaluate **LTX-2** (Apache 2.0, 4K@50fps, runs on consumer GPUs) as the open-source video model option.

### 5. **Phi-4 Model Naming Mismatch** (Workstream A — MEDIUM IMPACT)
Your docs reference "Phi-4 (7B)" — the actual available models are `phi4-mini` (3.8B) and `phi4-reasoning` (14B). Your Mac Mini tasks should use `phi4-mini` or `phi4-mini-reasoning`, not a 7B model that doesn't exist.

### 6. **PyTorch Stable Now Supports sm_120** (Workstream C — MEDIUM IMPACT)
No longer need nightly builds. PyTorch ≥2.7.0 with cu128 wheels supports Blackwell natively. Simplifies your Alienware setup.

### 7. **Opus 4.6 Price Drop (67% cheaper)** (Workstream A — MEDIUM IMPACT)
At $5/$25 per MTok with 1M context, Opus is now in the same price range as your local inference electricity costs for heavyweight tasks. Recalculate which tasks are worth running locally vs. routing to Opus.

### 8. **Qwen3 Model Family Upgrades** (Workstream A — LOW-MEDIUM IMPACT)
Qwen3 14B reasoning outperforms DeepSeek-R1:14B. Qwen3-VL improves on Qwen2.5-VL for vision. Qwen3.5-122B MoE (10B active) could run on MacBook Pro. These are upgrades, not blockers — evaluate during Phase 1 benchmarking.

---

## NEW OPPORTUNITIES

### 1. **Retro Diffusion rd-animation as Primary Sprite Generator** (HIGH CONFIDENCE)
Available now on Replicate. Generates animated sprite sheets natively at game-engine-compatible frame counts. If quality is sufficient for your SF2-style sprites, this could dramatically simplify your pipeline by eliminating the keyframe-to-video-to-quantizer path for standard animations. Keep the hybrid pipeline for complex animations where rd-animation falls short.
Sources: [Replicate](https://replicate.com/retro-diffusion/rd-animation), [Scenario](https://help.scenario.com/en/articles/retro-diffusion-models-the-essentials/)

### 2. **LTX-2 as Local Open-Source Video Model** (MEDIUM CONFIDENCE)
Apache 2.0 licensed, native 4K@50fps, 20-second videos, NVIDIA-optimized with NVFP8 quantization. Could run locally on your RTX 5080 for video interpolation without API costs. True replacement for the Wan 2.5 gap.
Source: [Pinggy](https://pinggy.io/blog/best_video_generation_ai_models/)

### 3. **Seedance 2.0 Reference-to-Video for Motion Transfer** (MEDIUM CONFIDENCE)
ByteDance's model (launched Feb 7, 2026) does expression and motion transfer from reference videos onto new characters. Similar to Kling 2.6's motion transfer but with 3D scene input support. Worth testing alongside Kling 2.6 in your Phase 2 video model sprint.
Source: [Genra.ai](https://genra.ai/blog/top-6-ai-video-generators-2026)

### 4. **ComfyUI NanoBanana2 API Node** (HIGH CONFIDENCE)
ComfyUI v0.18.x has a built-in NanoBanana2 API node. This means you can call Gemini 3.1 Flash image generation directly from ComfyUI workflows — potentially simplifying your autoresearch loop by keeping everything in the ComfyUI ecosystem rather than using separate API calls.
Source: [ComfyUI Changelog](https://docs.comfy.org/changelog)

### 5. **Claude Agent SDK In-Process MCP Server** (HIGH CONFIDENCE)
The new `create_sdk_mcp_server()` function lets you define custom tools as Python functions running in the same process — no subprocess management, no IPC overhead. Your ComfyUI MCP wrapper should use this instead of an external MCP server. Simpler, faster, easier to debug.
Source: [PyPI](https://pypi.org/project/claude-agent-sdk/)

### 6. **Phaser 4 RC7 with Pixel Art Improvements** (MEDIUM CONFIDENCE)
Phaser 4 RC3-RC7 specifically improved pixel art controls and performance. When 16BitFit ships, Phaser 4 will be the better runtime. Your headless validation can stay on Phaser 3 for now, but plan the game itself for Phaser 4.
Source: [Phaser](https://phaser.io/news/2026/03/phaser-v4-release-candidate-7)

---

*This audit covers every item in the original 9 categories. Last updated: March 27, 2026.*
