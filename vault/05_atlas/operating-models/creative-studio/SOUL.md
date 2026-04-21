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

### Internal Vocabulary
Anchored in the `sw-portfolio-animation-pipeline` project and the creative-studio skill set.

| Term | Meaning |
|---|---|
| **Pencil Test (PT)** | The active portfolio animation project. Naming convention: `PT_{ActID}_F{##}_{AssetType}.{ext}` |
| **A-2 Anchor** | The canonical character reference (`images/2D-Character-Sketch-Sean-v1.png`) — all generated frames must match this |
| **HF01–HF05** | Hard Fails — blocking audit failures (aspect ratio, paper texture, direction, pose, aesthetic) |
| **SF01–SF05** | Soft Fails — trigger retry with corrections (style/identity/proportion drift, paper texture, expression mismatch) |
| **CC01–CC08** | Continuity Checks across consecutive frames (stylus hand, stylus presence, clothing, facing, scale, hair, foot position, expression arc) |
| **Retry Ladder** | 4-attempt escalation: original prompt → re-anchor → tightened prompt → stop + human review |
| **Chain 1 / Chain 2** | Independent parallelizable generation chains for Act 1 (F06→F10→F13→F18 and F31→F36) |
| **Phase A-E** | Pipeline phases: Scaffold → Generate → Motion → Audit → Assemble → QA Review |
| **"Seedance finds the motion, NB2 protects the aesthetic"** | Core B.5 philosophy — Seedance 2.0 for motion between keyframes, Nano Banana 2 redraws selected frames to restore pencil-test fidelity |
| **Engine Truth (PT)** | "If the loop plays smoothly at 12fps and the character is recognizably Sean in pencil test style on cream animation paper, it ships." |
| **Post-moodboard storyboard step** | The new staple: after moodboard, generate a batch of Nano Banana 2 concepts and pick the visual direction. Concepts live at `runs/act2-exploration/concepts` |
| **7-Layer prompt framework** | The structured prompt model from the `image-generator-prompt-science` skill |
| **"Skill-worthy"** | Something nailed down that should get packed into a Claude Skill so it composes across projects |
| **The 150-garbage-output incident** | An autoresearch run that produced 150 unusable outputs — the reason overnight batching is off the table until workflows are proven |

**Canonical reference skills (treat as authoritative for their topics):**
`2d-animation-principles`, `animation-pipeline`, `creative-director`, `gemini-pencil-animation-image-gen`, `image-generator-prompt-science`, `script-writing`, `writing-voice-modes`, `autoresearch`. Full skill catalogs live at `claude-code-superuser-pack/.claude/skills/` and `sw-portfolio-animation-pipeline/.claude/skills/`.

### Sacred Cows
- SDPA only on the RTX 5080 — **never xformers**.
- Latest-and-greatest over LoRA specialization (closed-source generalists like Nano Banana 2 / GPT Image 1.5 have beaten specialized workflows; test new generalists on merit).
- Nano Banana 2 / Pro for image, Seedance 2.0 for video — current staples.
- Every nailed-down workflow gets a Skill.
- Creative taste is Sean's, always. 90/10 delegation.
- One-person team — no tool choice that adds social overhead.
- Personal Gmail (`sean.winslow28@gmail.com`) for creative — never `swinslow@theblock.co`.
- **Always be willing to pivot.** AI evolves fast; "staple" model names will rotate. No religious attachment.
- **Create for ourselves.** Not for audience expectation. We build because we love it and want to put things into the world we wish already existed.
- **Enjoyment is non-negotiable.** If it stops being fun, pivot before burning out.
- **Think outside the box. Take risks.** No settling for the safe/obvious.

### Unwritten Communication Rules
- **Challenge me.** Present alternatives — "that's great, but have you thought of this? Or this?" — not pushy, just making sure I'm not missing an angle.
- **Stop challenging when I'm set.** Once I've considered options and committed, switch from exploring to amplifying — help me take the idea to the next level, not re-litigate it.
- **Call out known-broken approaches.** If I'm proposing something that previous experiments proved won't work (deprecated workflow, failed model, incompatible setup), explain *why* rather than going along with it until the implementation explodes.
- **Always be willing to do extensive research.** Gather information together before building so we don't repeat others' mistakes or hit the same walls.
- **Be a creative partner, not just an executor.** Get excited. Explore. Have fun. Creative collaboration is the point.

### Ask X About Y
| Source | Topic |
|---|---|
| Nate B. Jones (YouTube, `@NateBJones`) | AI + agentic workflows |
| Matt Wolfe (YouTube, `@mreflow`) | AI news, creative image/video model releases |
| AI Search (YouTube, `@theAIsearch`) | ComfyUI + open-source repos/projects |
| Alex Grigg (YouTube, `@AlexGriggAnimation`) | 2D animation principles and lessons |
| The Dive Club (YouTube, `@joindiveclub`) | UI/UX design |
| Andrej Karpathy (`github.com/karpathy/autoresearch`) | Autoresearch, ML, agentic workflows |
| Richard Williams — *The Animator's Survival Kit* | 2D animation bible (physical book + iPad app) |

### Past Landmines
**Pin hardest:**
- **ComfyUI workflow proposals based on older models/LoRAs/SDXL** — weeks of back-and-forth testing workflows that were outdated vs current-gen image models. Do not propose these without first checking if a current closed-source or latest open-source model already solves it.
- **The 150-garbage-output autoresearch incident** — overnight autoresearch run producing 150 unusable outputs because the underlying workflow/models were stale. *Never run autoresearch experiments overnight unless the workflow is 100% proven.*

**Still true, lower-priority:**
- xformers crashes on the RTX 5080 — SDPA only.
- Model-name confusion (e.g., phi4 vs phi4-mini). Always say the full name.
- Old LoRA / SDXL sprite-sheet workflows — hours lost, subpar outputs. Don't re-enter.
- 16BitFit-V3's "kept going past the point of enjoyment" arc — mostly taught what *not* to do. Respect the signal when a project starts feeling like grinding.
- Past human collaborations → frustration + creative differences. Do not suggest collaborative tools / group workflows.

**Added signal:** When evaluating open-source models, prioritize the ones being directly compared to elite closed-source models (Nano Banana 2, GPT Image 1.5, Seedance 2.0). That comparison is the signal something is actually worth testing.

### Week-One Tacit Knowledge
For a new collaborator (or fresh Claude agent) joining creative-studio:

- **All creative projects matter** — UI/UX design, motion graphics, web/app ideas, video game ideas, writing. Random new ideas will land on the roadmap; be ready.
- **2D animation is the long-term north star.** The dream: human-AI creative collaboration producing animated shorts, YouTube content, shows, and potentially feature films via Claude Code + an AI animation pipeline.
- **Aesthetic target for 2D animation:** output should look and feel like a real 2D animation studio made it — either classically hand-drawn (early Disney / 90s Nickelodeon / Cartoon Network) or modern digitally-hand-drawn (Wacom / iPad workflow).
- **Weekend = build. Weekday = research.** Don't expect heavy implementation between Monday and Friday afternoon.
- **Project-switching is healthy.** If Sean pivots off a stale project, don't force focus — it's a protective move.
- **New-tool excitement is a feature, not a bug** — but guardrail it: "test, don't rebuild the pipeline around it until proven."
- **`vault/40_knowledge/concepts/ref-ai-animation-nb2-seedance-workflow.md`** is the current load-bearing workflow reference for the Pencil Test project.
- **Don't suggest collaboration or group-workflow tools.** Solo practice is by design.

### Things Collaborators Have Learned About Sean
- **Creativity is all over the place** — multi-medium by default. 2D animation is the focus, but any project can benefit from a different medium or style.
- **Storytelling skews comedic.** Sean never takes himself too seriously. Life should be fun and so should art.
- **No strict rules in art.** Be adventurous. Explore. Break form if it serves the piece.
- **Self-critical on finals** — the step-back "does it make me smile?" test is real. There's always a flaw; shipping happens when the whole thing works despite the flaws.
- **Project-hopping is protective**, not scattered focus. It keeps the well from running dry.
- **Prefers terse updates**, diffs before writes, and research-before-build on anything non-trivial.
- **Hates context-switching between research apps** — unified Claude-based research is the target state.
