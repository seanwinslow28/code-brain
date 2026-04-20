---
type: operating-model
artifact: SOUL
domain: [creative-studio]
status: draft
last_interviewed: 2026-04-20
created: 2026-04-18
review-date: null
ai-context: "People, tools, and tacit/tribal knowledge for creative work. Solo practice by design — Claude is the only collaborator dependency. Three-machine topology is not a single point of failure. Populated by the work-operating-model skill. Consumed by sprint-health, pr-digest, process-inbox, and as context layer."
---

# SOUL — Creative Studio

## Part A — Dependencies (Layer 3)

### Critical-Path Collaborators
Solo practice by design. 2D animation is partly chosen because it *doesn't* require others — past collaborations led to frustration and creative differences. I share finished work with friends and family; creation is mine alone.

| "Person" | What I go to them for | Blocker if unavailable |
|---|---|---|
| Claude (Code, Desktop, Cowork) | Brainstorming, drafting, skill-building, research synthesis, concept exploration, pipeline orchestration | Yes — the only dependency whose outage actually stops creative momentum |

### Load-Bearing Tools
**Hard-dependencies (if this breaks today, I'm stopped or severely slowed):**
- Claude Code + skill system (and Claude ecosystem generally — anything Anthropic ships)
- Adobe Creative Suite (Illustrator, Photoshop, After Effects, Premiere) — primary video/image editing surface
- Procreate (iPad) — illustration and animation practice

**Heavy-use staples (flow degrades significantly without them):**
- ComfyUI
- Remotion
- Adobe MCP (via adb-mcp for Illustrator / Photoshop / After Effects / Premiere)
- Obsidian vault
- Pencil (.pen files)
- Autoresearch harness
- NotebookLM (research + Skill-building source material)
- Google AI Studio
- Gemini Deep Research
- Perplexity Deep Research
- Google Antigravity IDE _(replaces Cursor as of this interview)_

**Situational:** Figma, Blender — project-dependent.

### Load-Bearing External APIs / Models
| Model / API | Weight | Notes |
|---|---|---|
| Nano Banana 2 (Gemini) | Pipeline staple | Image gen — most projects |
| Nano Banana Pro (Gemini) | Pipeline staple | Image gen — most projects |
| Seedance 2.0 | Pipeline staple | Current best video gen |
| GPT Image 1.5 | Active | Image gen, proven on animation styles |
| Kling | Active | Video gen |
| Veo 3.1 | Active | Video gen |
| ElevenLabs | Active | Voice/audio |
| Hugging Face (Z-Image, ERNIE, etc.) | Exploratory | Test the latest/greatest regardless of LoRA status |
| Wan 2.5 | Exploratory | Cheaper than Seedance/Kling/Veo — worth testing, don't burn hours without proven workflow |

**Direction (not yet in place):**
- Prefer Ollama / LM Studio for local open-source models where viable — cost savings.
- Consolidate deep research into a single **Claude Research Skill** that wires Perplexity API + Google search MCP + NotebookLM MCP. Goal: do all research inside Claude Code / Cowork / Desktop instead of context-switching between Perplexity, Gemini, NotebookLM, and Google Search.

### Three-Machine Topology
**No single point of failure for creative work.** Each machine can pick up the others' load — slower, but not blocked. Projects are backed up across GitHub + Google Drive + external hard drive.

- **Mac Mini (primary station, 2 displays)** — runs the 6 active SDK agents (vault indexer, synthesizer, meta-agent, daily driver, knowledge lint, flush). Creative halt radius: none specific; losing it degrades the agent fleet but creative work continues on MBP or Alienware.
- **MacBook Pro** — travel + couch-work. Hosts intermittent Qwen3-14B inference (vault synthesizer + knowledge-lint Tier 2 when awake). Creative halt radius: none specific.
- **Alienware (RTX 5080, CUDA)** — ComfyUI experimentation and planned heavy Adobe / Blender rendering. "The beast." Creative halt radius when down: pipelines slow, not stopped — Mac Mini and MBP can run the same ComfyUI workflows, just slower. "Down for a day" is tolerable; "down for a week" shifts everything to cloud APIs and slower local machines but doesn't break the pipeline.

### Single Source of Truth
**Currently no unified SSoT for creative work. Building one is an open architecture task.**

- **2D animation pipeline:** `sw-portfolio-animation-pipeline/CLAUDE.md` + `CHANGELOG.md` — project-scoped. Plan: extract the reusable pipeline into its own project so it serves multiple 2D animations, not just the current portfolio short's style.
- **16BitFit:** `CLAUDE.md` in `16BitFit-V3/`, accessible on Mac Mini and via Google Drive mirror at `/Users/seanwinslow/Library/CloudStorage/GoogleDrive-sean.winslow28@gmail.com/Other computers/My Mac Mini/Code-Brain/16BitFit-V3/CLAUDE.md`. Currently stale relative to the planned simplification pivot.
- **`claude-code-superuser-pack`:** hosts editing / motion-graphics / Adobe skills — distinct from `sw-portfolio-animation-pipeline` skills (2D animation + image gen). The two sets of creative Skills need differentiation so they don't compete or duplicate.
- **Target:** build out the Vault as the creative-studio SSoT — connecting related projects by shared theme, tool, idea, or style. The Vault-as-SSoT is itself a work product.

### Who Depends On Me
Nobody right now. Experimentation phase — creating for the sake of creating, finding tools, building pipeline. No external deadlines beyond the self-imposed June 11 portfolio-short target.

### Self-Blocking Decisions
Current queue: **just one active blocker** — finishing the three-domain operating-model interviews so Claude Code and the Agent SDK fleet know me well enough to act effectively. Creative-scoped blockers (hero style picks, narrative-beat locks, video-model standardization) are not bottlenecking right now because the pipeline is still exploratory; they'll accumulate once production kicks in.

---

## Part B — Institutional Knowledge (Layer 4)

_To be filled by interview (Layer 4, upcoming)._
