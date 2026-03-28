# CLAUDE.md — 16BitFit Battle Mode

This is the project command center for 16BitFit Battle Mode: a 12-week build spanning autonomous agent infrastructure, a hybrid AI sprite sheet pipeline, and an autoresearch/LoRA training system.

## How to Use This Project

**Start every session** by reading `SOURCE-OF-TRUTH.md` (the master reference, ~450 lines). Then load ONLY the specific `docs/` files relevant to your current task — see the Session Loading Guide in Part 7 of the SOT.

**Never dump all docs at once.** The SOT is the compression layer. Go to source files only when you need implementation details.

## Three Workstreams

| Workstream | What | Where Code Lives |
|---|---|---|
| A: Agent SDK Infrastructure | Three-machine orchestration, autonomous agents, safety hooks | `../agents-sdk/` (sibling directory in superuser pack) |
| B: Sprite Pipeline Upgrade | Hybrid keyframe-to-video, Pixel Quantizer, adapter layer | Separate repo (`16BitFit-V3` or `16BitFit-Asset-Creation`) |
| C: Autoresearch + LoRA | ComfyUI workflow optimization, style LoRA training | Alienware local (ComfyUI), orchestrated by agents-sdk |

## Non-Negotiable Rules

1. **Gemini image models stay in the pipeline.** Nano Banana Pro (`gemini-3-pro-image-preview`) and/or Nano Banana 2 (`gemini-3.1-flash-image-preview`) are the primary image generators. Non-negotiable regardless of cost.
2. **RTX 5080 constraints:** CUDA 12.8+, PyTorch ≥2.7.0 stable cu128, SDPA attention (NO xformers — it crashes on sm_120), kohya_ss dev branch only.
3. **SDK names:** Package = `claude-agent-sdk`. Class = `ClaudeAgentOptions`. NOT the old names (`claude-code-sdk`, `ClaudeCodeOptions`).
4. **Never use `dangerouslySkipPermissions`** for autonomous agents.
5. **Credentials via macOS Keychain** (not .env files). Use `lib/keychain.py`.
6. **Hexagonal/Ports & Adapters architecture** for the sprite pipeline. Core logic never touches external tools directly. All generators (Gemini, Pika, Kling, rd-animation, etc.) go behind typed Adapter interfaces.
7. **LoRA base model:** Train on Illustrious XL v0.1. Infer on v2.0-STABLE or v3.x. v0.1 LoRAs have the best cross-compatibility.
8. **Phi-4 on Mac Mini:** Use `phi4-mini-reasoning` (3.8B) or `phi4-mini` (3.8B). NOT "Phi-4" (that's 14B, too big for 24GB with headroom).

## Three-Machine Topology

| Machine | Role | Models | Access |
|---|---|---|---|
| Mac Mini M4 Pro (24GB) | Always-on orchestrator, launchd host | phi4-mini-reasoning, nomic-embed-text via Ollama | LAN: `{MINI_IP}:11434` |
| MacBook Pro M4 Pro (48GB) | Heavyweight local inference, development | Qwen3-14B, Qwen2.5-Coder-32B via MLX-LM | Local only |
| Alienware RTX 5080 (16GB VRAM) | CUDA: ComfyUI, LoRA training, vision QA | Qwen3-VL-7B via Ollama CUDA, ComfyUI REST | LAN: `{ALIENWARE_IP}:11434`, WOL |

## Model-to-Machine Routing

| Task | Machine | Model |
|---|---|---|
| Inbox triage | Mac Mini | phi4-mini-reasoning (3.8B) via Ollama |
| Vault embeddings | Mac Mini | nomic-embed-text via Ollama |
| Financial analysis | MacBook Pro | Qwen3-14B via MLX-LM |
| Code review / PR digest | MacBook Pro | Qwen2.5-Coder-32B via MLX-LM |
| Heavy synthesis | MacBook Pro | Qwen3.5 (evaluate 122B MoE or 9B) via MLX-LM |
| Sprite vision QA | Alienware | Qwen3-VL-7B via Ollama CUDA |
| ComfyUI orchestration | Alienware | N/A (REST API to ComfyUI) |
| Complex / fallback | Any → Claude API | Opus 4.6 ($5/$25 per MTok) or Sonnet |

## Architecture Patterns

**Sprite Pipeline (4 atomic adapter operations):**
- `generateFrame` — single frame from anchor + pose ref (image-only strategy)
- `generateKeyframes` — 3-5 keyframes for video interpolation (hybrid strategy)
- `interpolateFrames` — video model fills between keyframes
- `generateVideo` — motion transfer from reference video (experimental)

**Agent SDK patterns:**
- Three-tier routing: Mac Mini (light) → MacBook Pro (heavy local) → Claude API (fallback)
- Baton File dependency chains between agents
- Fleet State note in vault for cross-agent coordination
- Safety hooks: loop-detector, cost-watchdog, vault-integrity
- Filelock for all vault writes

**Pixel Quantizer Pipeline (7 steps):**
1. Nearest-neighbor downscale → 128×128
2. Palette quantization (force-snap to LUT)
3. Temporal smoothing (mode-color locking)
4. Outline enforcement (#272929, 2-3px)
5. Alpha recovery (background removal)
6. Grid alignment (snap to pixel grid)
7. Format validation (dimensions, alpha, palette)

## File Reference

```
16bitfit-battle-mode/
├── CLAUDE.md               ← You are here
├── SOURCE-OF-TRUTH.md      ← Master reference (read first, always)
├── execution-blueprint.md  ← Exact terminal commands, ~102.5h total
├── docs/
│   ├── agent-sdk/          ← Workstream A reference
│   ├── sprite-pipeline/    ← Workstream B reference
│   ├── lora-autoresearch/  ← Workstream C reference
│   └── validation/         ← March 2026 audit + opportunity scan
└── _archive/               ← Original research (deep dives only)
```

## Anti-Patterns

- **Don't install xformers on RTX 5080.** It crashes on sm_120 architecture. Use SDPA (PyTorch native).
- **Don't use `ollama pull phi4`** on Mac Mini. That's the 14B model. Use `phi4-mini-reasoning`.
- **Don't use `claude-code-sdk` or `ClaudeCodeOptions`.** These are the old names before the SDK rename.
- **Don't train LoRAs on Illustrious XL v2.0+.** Community evidence shows reduced cross-compatibility. Train on v0.1.
- **Don't dump all 28+ docs into a single Claude Code session.** Use the Session Loading Guide.
- **Don't use Wan 2.5** in the pipeline. It's NOT open source. Wan 2.2 is the latest open-source version.
- **Don't skip the Pixel Quantizer gate check.** If the quantizer can't convert video output to clean pixel art, the hybrid approach is dead. Build and validate this FIRST.

## Future: 2D Animation Pipeline

This sprite pipeline is designed to also serve as the foundation for a general 2D animation pipeline for Sean's animated short films. The shared core (adapter layer, manifest system, video model clients, quality audit framework, Agent SDK orchestration) is reusable across both. The Pixel Quantizer is the divergence point — sprites go through pixel-art post-processing, animation frames would go through a different chain (upscaling, color correction, temporal smoothing without pixel constraints, compositing).

**Design implication for current build:** When hardcoding sprite-specific values (tile size, palette, pixel grid), prefer making them configurable options rather than constants. This small habit now saves weeks later. The hexagonal architecture already supports this — adapters and post-processing steps are swappable by design.

**Timing:** Build and prove the sprite pipeline first (Phases 1-5). Then extract the shared core into a library and build the animation pipeline as a second consumer. Do not attempt both simultaneously.

## Session Loading Guide (Quick Reference)

| Task | Load from docs/ |
|---|---|
| Build hybrid_router.py | `agent-sdk/phase-2-synthesis.md` + `agent-sdk/tech-stack-specs.md` |
| Build Pixel Quantizer | `sprite-pipeline/pipeline-CLAUDE.md` + `sprite-pipeline/hybrid-pipeline-plan.md` + `sprite-pipeline/pixel-quantizer-kickoff.md` |
| Test video models | `sprite-pipeline/workflow-operations-guide.md` + `validation/opportunity-scan.md` |
| Train LoRA | `lora-autoresearch/rtx5080-lora-training.md` + `lora-autoresearch/rtx5080-compatibility.md` |
| Build autoresearch loop | `lora-autoresearch/autoresearch-overview.md` + `validation/opportunity-scan.md` |
| Full execution steps | `execution-blueprint.md` (top-level) |

## When Modifying

- After completing a gate check or major decision, update `SOURCE-OF-TRUTH.md` Part 5 (Open Questions) to mark it resolved.
- After finishing a Phase, update the checklist in `SOURCE-OF-TRUTH.md` Part 4.
- If a tool/model is replaced or deprecated, update both the SOT and this CLAUDE.md.
