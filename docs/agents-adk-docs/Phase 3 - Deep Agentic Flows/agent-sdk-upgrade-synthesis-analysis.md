# Claude Agent SDK — Gemini Deep Think Synthesis & Best-Fit Analysis

**Date:** 2026-02-23
**Purpose:** Synthesize the two Gemini 3.0 Pro Deep Think responses (Option 1: Claude Desktop prompt, Option 2: Claude Code project-aware prompt) into a single, definitive architectural plan tailored to Sean's goals, codebase, and constraints.

---

## Executive Summary

Both responses are strong but solve the problem from different angles. **Option 1** (Claude Desktop) provides broader strategic thinking with senior architect insights. **Option 2** (Claude Code) provides more implementation-ready specifications because it scanned your actual repo and understood your existing code patterns. The optimal plan cherry-picks from both, and this document tells you exactly what to take from where.

**The biggest insight from comparing them:** Option 2's aggressive local-first routing (targeting $0.00/run for 8+ agents) is the correct financial strategy. Option 1's prompt caching scheduling trick and "context poisoning" warning are architectural gems that Option 2 missed. Combined, you get a system that's both cheap and resilient.

**Critical hardware correction (post-synthesis):** Both Gemini responses designed for a two-machine setup. Sean actually has **three machines** — a Mac Mini M4 Pro (24GB, always-on), a MacBook Pro M4 Pro (48GB, daily driver), and an Alienware with an RTX 5080 (16GB VRAM, not 24GB as Option 2 assumed). This fundamentally changes the architecture: the Mac Mini becomes the always-on agent orchestrator, the MacBook Pro becomes the heavyweight local inference machine (48GB unified memory runs 32B models via MLX), and the Alienware is reserved for CUDA-specialized tasks (ComfyUI, vision models). The three-machine topology provides triple-redundancy for local inference, meaning agents almost never need to fall back to paid API calls.

### Hardware Inventory

| Machine | CPU | Memory | GPU | Role in Agent System |
|---------|-----|--------|-----|----------------------|
| **Mac Mini M4 Pro** | 12-core | 24GB unified | 16-core Apple GPU | Always-on orchestrator: runs launchd schedules 24/7, lightweight local inference (≤7B models), embedding generation. Low power (~10-15W idle). |
| **MacBook Pro M4 Pro** | 14-core | 48GB unified | 20-core Apple GPU | Heavy local inference via MLX/Ollama Metal: 14B-32B models fit comfortably. Available during work hours when laptop is open. |
| **Alienware Aurora** | Intel Ultra 9 (24-core) | 64GB DDR5 | RTX 5080 16GB GDDR7 | CUDA-specialized: ComfyUI sprite generation, vision model QA (Qwen2.5-VL), GPU-accelerated inference when VRAM is free. 1TB NVMe, 1000W PSU. |

---

## Section-by-Section Verdict

### 1. Agent Fleet Specification

**Winner: Option 2**, with select additions from Option 1.

**Why Option 2 wins:** It was built with awareness of your actual file structure. It uses your real vault paths, references `config.toml` fields that actually exist in your codebase, and specifies Python filenames (`agents/process_inbox.py`) that match your existing `agents/daily_driver.py` pattern. Option 1 uses plausible but sometimes wrong vault paths (e.g., `01_Daily/` vs your actual `0_Daily/` or `10_timeline/daily/`).

Option 2 also includes two agents Option 1 missed that are genuinely high-value:

- **Meeting Defender** — This is brilliant for your situation. You spend 35% of your time in meetings. An agent that audits your calendar weekly, identifies declinable meetings, and *drafts* Slack DMs (never auto-declines) could reclaim 3+ hours/week. That's worth more than most other agents combined.
- **Vault Embedding Indexer** — A nightly agent that embeds modified notes into a local SQLite vector DB using nomic-embed-text. This gives every other agent semantic search over your 1,431 notes at zero API cost. It's infrastructure, not a standalone agent — it makes all other agents smarter.

**Take from Option 1:**
- The **Boston Move Coordinator** name and `EXPIRES MAR 21, 2026` concept both responses have, but Option 2's `expires_on` field in `config.toml` is the cleaner implementation.
- Option 1's **Meal Planner** (experimental tier) is worth noting for later but shouldn't distract from Phase 1-2.

**Discard from both:**
- Both suggest a "Knowledge Synthesizer" agent that reads related notes and generates connection insights. At $0.25/run (Option 1) or requiring Opus (Option 2), this is the lowest ROI agent in either fleet. Your vault's Dataview dashboards and MOC structure already handle discovery. Defer this to "experimental" at minimum.

**Recommendation:** Use Option 2's agent specs as your implementation base. Cross-reference Option 1's table format for any agents Option 2 didn't cover (Festival Tracker, Stale Note Detector, Vault Health Reporter). Validate all vault paths against your actual vault structure before building.

---

### 2. MCP Integration Roadmap

**Winner: Option 2**, with Option 1's credential strategy.

Option 2 provides actual `mcp_servers` config snippets that match your `ClaudeAgentOptions` patterns. Option 1 provides the same services but wrapped in a more readable table format.

**Critical agreement between both:** The `ENABLE_TOOL_SEARCH="true"` flag for Zapier MCP is non-negotiable. Without it, all 175 tool schemas get injected into every prompt, burning thousands of tokens per run. Both responses flag this — take it seriously.

**Where Option 1 wins on MCP:**
- The **macOS Keychain** credential strategy is superior. Option 1 provides an actual code snippet (`security find-generic-password`) that pulls secrets at runtime without touching `.env`. This respects your `block-secrets.py` hook while keeping credentials secure. Option 2 says "put Jira tokens in `.env`, protected by block-secrets hook" — but that's contradictory since the hook's whole purpose is blocking `.env` access.
- The **Filmfreeway via Puppeteer MCP** idea is creative but fragile. Option 1 correctly flags this as "High complexity, notoriously brittle." Go with a simpler Google Sheets tracker that you manually update after submissions — the Festival Tracker agent reads the sheet via Zapier.

**Where Option 2 wins on MCP:**
- The **Ollama MCP** (`@rawveg/ollama-mcp`) configuration is production-ready. With three machines, you now need three Ollama endpoints: Mac Mini (`localhost:11434`, always available), MacBook Pro (`192.168.1.X:11434`, available when open), and Alienware (`192.168.1.Y:11434`, health-checked before routing). The hybrid router selects the best endpoint per task.
- The **ComfyUI custom MCP wrapper** approach is correct for your sprite pipeline — it's a Python wrapper that hits ComfyUI's REST API on the Alienware, not a third-party package.

**Recommendation:** Use Option 2's MCP configs, but replace the `.env` credential approach with Option 1's macOS Keychain pattern for Jira, GitHub, and ElevenLabs tokens.

---

### 2b. Google Drive Integration Strategy (30TB Cloud Storage)

**Neither Gemini response addressed this.** Sean has 30TB of Google Cloud storage with Google Drive synced across all three machines (Mac Mini, MacBook Pro, Alienware). This is a significant infrastructure asset that complements the agent system — but only when used for the right layers.

**Critical rule: The Obsidian vault must NOT live in Google Drive.** Obsidian's community has extensively documented sync conflicts when vaults live in cloud-synced folders. The failure mode is specific and destructive: when the Mac Mini writes to a daily note via `vault_inject` at 5:30 AM, Google Drive sync isn't instant. If the MacBook Pro's local Ollama inference reads that same note seconds later, it may get the stale pre-write version. Worse, if two machines write to the same file before sync completes, Google Drive creates duplicate conflict files (`daily-note (1).md`) instead of merging — this would corrupt the HTML anchor-based PATCH system that the entire agent fleet depends on. The `filelock` pattern is a local OS construct and does not work across machines via cloud sync. Use git or Obsidian Sync for vault replication instead.

**Where Google Drive IS genuinely useful in the agentic workflow:**

**1. Creative Asset Storage (Write-Once-Read-Many)** — 30TB is ideal for ComfyUI sprite outputs, animation renders, video exports, Procreate source files, and Adobe project files. These are large files that agents write on the Alienware and read from any machine later. Having sprite batches, render outputs, and animation frames automatically available across all three machines without custom file transfer scripts is a real workflow win. Agents can write completed assets to `Google Drive/Creative/16BitFit/Sprites/` on the Alienware, and the Mac Mini's Festival Tracker or Portfolio Generator can reference them without cross-machine networking.

**2. Financial CSV Drop Zone** — Instead of monitoring `~/Downloads/BankCSVs/` locally (Option 2's WatchPaths approach), use `Google Drive/Finance/CSVs/` as the bank export landing zone. Download Chase/Bilt exports from any browser on any machine, they sync everywhere, and the Mac Mini's `csv_anonymizer.py` picks them up via launchd WatchPaths on the synced folder. The raw CSVs never touch the vault, and Google Drive's version history provides automatic backup of every export — useful for tax prep and dispute resolution.

**3. Google Sheets as Structured Data Backend** — This is the highest-value integration. Agents already access Google Sheets via Zapier MCP. Use Sheets for structured data that isn't well-suited to markdown files: monthly budget tracking and debt paydown projections (Spending Analysis writes here), festival submission tracker with deadlines, statuses, and fees (Festival Tracker reads/writes here), sprint velocity metrics over time (Sprint Health Monitor appends here), agent fleet cost tracking and trends (Fleet Monitor logs here), and meal planning / grocery lists (future Meal Planner writes here). Agents write to Sheets via Zapier MCP, and you get Google's built-in charting, formulas, and sharing for free.

**4. Google Docs for Shareable Outputs** — When the Stakeholder Report Generator creates a biweekly update, writing it to a Google Doc (via Zapier MCP) makes it immediately shareable with your VP and team without exporting from the vault. Same for portfolio case studies targeted at animation industry hiring managers, meeting briefs that need to be shared before a meeting, and any agent output destined for an audience beyond yourself.

**5. Large Model & Dataset Backup** — Your Ollama models (Phi-4, DeepSeek-R1, Qwen2.5-Coder, etc.) are multi-gigabyte downloads. Back them up to `Google Drive/AI/Models/` so that if you need to reinstall Ollama on any machine (or after the Boston move), you can restore from Drive instead of re-downloading everything. Same for ComfyUI checkpoints and LoRA files.

**6. Agent Log Archival** — The `agent-run-history.csv` that tracks every agent run, cost, and outcome should be periodically archived to Google Drive for long-term trend analysis. The Meta-Agent's monthly "State of Sean" report can pull from months of archived CSVs stored in `Google Drive/Agent-System/Logs/` to detect patterns across longer time horizons than the local vault retains.

**What to avoid storing in Google Drive:** The Obsidian vault (sync conflicts), inter-agent communication files like Baton flags or Fleet State notes (latency-sensitive), credentials or secrets of any kind, and any file that multiple agents write to within the same scheduling window.

---

### 3. Skills Audit for Autonomous Operation

**Winner: Option 1** — more specific and actionable.

Option 1 gives you exact text to find-and-replace in your skill files:
- `daily-driver`: Remove "Ask the user what they want to focus on" → Replace with autonomous decision criteria using `02_Areas/Focus.md`
- `process-inbox`: Remove "Confirm the tags with me" → Replace with confidence-threshold routing (`<80%` → `#triage/human`)
- `personal-finance`: Remove "Review these anomalies with the user" → Replace with structured markdown table output

Option 2 doesn't provide a skills audit section at all — it assumes skills are ready and focuses on model routing instead.

**Key insight from Option 1:** Skills that say "ask the user" will cause the SDK agent to hang, draining your budget until the turn limit kills it. This is real money at risk. Audit your skills before building new agents.

**Recommendation:** Follow Option 1's skills audit completely. Before building any new agent, grep your skill files for interactive patterns: "ask me", "confirm with", "review with the user", "what would you like". Replace each with autonomous decision criteria and fallback behaviors.

---

### 4. Safety & Guardrails

**Winner: Tie** — each covers different critical gaps.

**Take from Option 1:**
- The **Financial Data Airgap Pattern** is well-designed: a dumb Python script (`sanitize_finance.py`) pre-processes raw CSVs, drops account numbers, hashes transaction IDs, outputs sanitized JSON. The Spending Analysis agent only ever sees the JSON. Raw CSVs stay gitignored.
- The **Deployment Checklist** (`safety-checklist.md`) is immediately useful — add it to your vault today.
- The **token velocity check**: if `turn_count > 5` but no vault file modified, kill the agent. This prevents confused agents from burning budget.

**Take from Option 2:**
- The **filelock pattern** using Python's `filelock` library is essential and Option 1 only mentions it briefly. Option 2 provides actual code: `FileLock(f"{path}.lock", timeout=10)` wrapping vault_inject calls.
- The `vault-integrity.py` hook that blocks vault_inject if the anchor string is empty (which would overwrite the whole file) is a critical safety catch.
- The `loop-detector.py` hook using a sliding window hash of tool calls is elegant — if `hash(call[n]) == hash(call[n-2])`, the agent is stuck in a loop.

**Where both agree (take seriously):**
- **Never use `dangerouslySkipPermissions`** for scheduled agents. Option 1 suggests it for creative pipeline agents needing heavy Bash — but Option 2 correctly pushes back: no agent should get raw bash access. If ComfyUI needs bash commands, wrap them in a custom MCP tool with restricted command whitelists.
- **Never auto-retry failed agents.** Log the error, send a Slack notification, move on. Retries on API failures can cascade costs.

**Recommendation:** Merge both safety architectures. Use Option 1's financial data airgap and deployment checklist. Use Option 2's filelock implementation, vault-integrity hook, and loop-detector hook. Never grant `dangerouslySkipPermissions` to any autonomous agent.

---

### 5. Hooks

**Winner: Option 2** — more practical, fewer hooks that do more.

Option 1 proposes 5 hooks. Option 2 proposes 3 that are tighter:
- `loop-detector.py` (PostToolUse) — catches stuck agents
- `cost-watchdog.py` (PreRun) — blocks agent launch if daily fleet spend exceeds $2.00
- `vault-integrity.py` (PreToolUse) — prevents empty-anchor overwrites

Option 1's `pii-filter.py` (regex scanning for SSNs and card numbers) is worth adding as a 4th hook, specifically for the Spending Analysis agent.

**Recommendation:** Build Option 2's three hooks first. Add Option 1's PII filter as a 4th, scoped to financial agents only.

---

### 6. Multi-Agent Coordination

**Winner: Option 1's concepts + Option 2's implementation.**

Option 1 introduces the **"Baton File" (Semaphore) pattern** — this is the right approach for launchd dependency chains:
1. Process Inbox runs at 5:30 AM. On success, its Stop hook touches `~/.claude/batons/inbox_done.flag`
2. Daily Driver's launchd plist uses `WatchPaths` targeting that flag file, triggering instantly instead of guessing a time

Option 2 provides the same concept but with a more detailed DAG (Directed Acyclic Graph) schedule and the Wake-on-LAN pattern for when the Alienware is asleep during morning agent runs — a real-world edge case Option 1 doesn't address.

**The Fleet State note** (`99_Meta/Fleet_State.md` in Option 1) is a simple, elegant way for agents to communicate asynchronously through the vault. Both responses converge on this pattern.

**Recommendation:** Use Option 1's Baton File pattern for dependency chains. Use Option 2's WOL (Wake-on-LAN) pattern for cross-machine resilience. Implement the shared Fleet State note for inter-agent awareness.

**Three-machine coordination advantage:** With the Mac Mini as the always-on orchestrator, launchd schedules run reliably 24/7 regardless of whether the MacBook is open or the Alienware is awake. The Mac Mini executes the Python agent scripts, which then route inference calls to whichever machine is best suited and available. Morning agents at 5:30 AM no longer depend on leaving a laptop open overnight. The WOL pattern applies specifically to the Alienware — the Mac Mini sends a magic packet to wake it before CUDA-dependent tasks (sprite QA, ComfyUI orchestration).

---

### 7. Cost Projections

**Winner: Option 2** — more realistic and aggressive on savings.

| Metric | Option 1 | Option 2 | **Revised (3-Machine)** |
|--------|----------|----------|------------------------|
| Phase 1 monthly | ~$7.50 | ~$3.00 | ~$2.50 |
| Steady state | ~$10.00 | ~$4.50 | ~$3.50 |
| Local offload savings | ~$13/mo estimated | ~$14/mo itemized | ~$15/mo (more tasks stay local) |
| Electricity cost | Not mentioned | ~$2.50/mo (Alienware) | ~$4/mo total (see below) |

The three-machine setup changes the electricity math. The Mac Mini runs 24/7 at ~10-15W idle, costing roughly $1-2/month. The Alienware only needs to wake for CUDA tasks (ComfyUI renders, vision QA), drawing ~300W under load but only for ~30 min-1 hour/day, adding ~$1.50-2/month. The MacBook draws from battery during the day and charges at night — negligible incremental cost. Total electricity: ~$3-4/month.

Option 2's projections are lower because it routes more agents to local models (Process Inbox, Spending Analysis, PR Digest, Health Audit, Preserve Session, MD to Anki — all $0.00/run). Option 1 keeps some of these on Haiku, which is cheap but not free. With three machines, even more tasks stay local because the Mac Mini handles lightweight inference (Phi-4, nomic-embed-text) while the MacBook handles heavyweight inference (14B-32B) without needing the Alienware at all.

**The "Rocket Money Math" from Option 2 is compelling:** If your agent fleet costs less than $12/month (Rocket Money subscription), and the Spending Analysis agent replaces Rocket Money's functionality, the entire system pays for itself from Day 1.

**Recommendation:** Target Option 2's cost model. Route every agent that doesn't need multi-tool orchestration to local models. Reserve Claude API calls for agents that need Jira/Zapier/Calendar MCP orchestration.

---

### 8. Open-Source Models & Local Inference

**Winner: Neither as-is** — both designed for two machines. The three-machine topology requires a revised strategy that's stronger than either response alone.

**VRAM correction:** The RTX 5080 has **16GB VRAM** (confirmed from Alienware specs: "NVIDIA GeForce RTX 5080 16GB GDDR7"), not 24GB as Option 2 assumed. This means 14B models at Q4 quantization (~9.5GB) **cannot** run alongside ComfyUI (8-12GB). Only 7B models fit concurrently on the Alienware. However, the Alienware's 64GB system RAM allows CPU-offloaded inference as a slower fallback.

**The MacBook Pro is actually the best local LLM machine.** This is the biggest insight neither response caught. Apple Silicon's unified memory means the GPU and CPU share the same 48GB pool. With MLX (Apple's ML framework) or Ollama's Metal backend, the MacBook runs 32B models at Q4 quantization (~20GB) with room to spare — no VRAM partition needed. The Alienware can't match this because its 16GB VRAM is a hard ceiling for GPU inference.

Both responses agree on the core model stack, which remains valid:

| Task | Model | Both Agree? |
|------|-------|-------------|
| Fast triage/logic | Phi-4 (14B, Q4) | Yes |
| Heavy reasoning/finance | DeepSeek-R1-Distill-Qwen-14B | Yes |
| Code review | Qwen2.5-Coder-14B | Yes |
| Vision/sprite QA | Qwen2.5-VL-7B | Yes |
| Embeddings | nomic-embed-text | Yes |
| Heavy synthesis (offline) | Qwen2.5-32B | Option 2 only |

**Revised model-to-machine routing:**

| Task | Best Machine | Model | Why This Machine |
|------|-------------|-------|------------------|
| Process Inbox triage | Mac Mini | Phi-4 (7B) via Ollama | Always available, low power, fits in 24GB easily |
| Vault embedding indexer | Mac Mini | nomic-embed-text via Ollama | Tiny model (<1GB), runs nightly on always-on machine |
| Anki card generation | Mac Mini | Phi-4 (7B) via Ollama | Simple structured output, no need for heavy model |
| Financial CSV analysis | MacBook Pro | DeepSeek-R1:14B via MLX | Needs reasoning power + data never leaves your LAN |
| PR Digest / Code review | MacBook Pro | Qwen2.5-Coder:14B via MLX | Large diffs need 14B quality, 48GB handles it easily |
| Heavy synthesis (Meta-Agent) | MacBook Pro | Qwen2.5-32B via MLX | Only machine with enough memory for 32B |
| Preserve Session | MacBook Pro | DeepSeek-R1:14B via MLX | Session capture happens when laptop is open (you just closed Claude Code) |
| Sprite vision QA | Alienware | Qwen2.5-VL-7B via Ollama CUDA | GPU-optimized vision inference, runs after ComfyUI finishes a batch |
| ComfyUI orchestration | Alienware | N/A (REST API) | ComfyUI is already running here |
| Meeting pre-classification | Mac Mini | Phi-4 (7B) via Ollama | Sunday evening task, laptop might be closed |

**Revised Alienware VRAM strategy (16GB, not 24GB):**

| Scenario | Available VRAM | Max Model Size |
|----------|---------------|----------------|
| ComfyUI active (heavy workflow) | 4-8GB free | 7B Q4 only, or route to MacBook instead |
| ComfyUI active (light workflow) | 8-10GB free | 7B Q5 comfortably |
| ComfyUI inactive | Full 16GB | 14B Q4 (~9.5GB) with headroom |
| Nighttime (nothing running) | Full 16GB | 14B Q4 max on GPU, or CPU-offloaded 32B using 64GB RAM (slower) |

**The `hybrid_router.py` needs three tiers:**

```
Mac Mini:    http://localhost:11434        (always available, lightweight models)
MacBook Pro: http://192.168.1.X:11434      (available when laptop is open, heavyweight models)
Alienware:   http://192.168.1.Y:11434      (health check before routing, CUDA-specialized)
```

The fallback chain: try preferred machine → try secondary machine → fall back to Claude Haiku API. This triple-redundancy means agents almost never need the paid API for local-capable tasks.

**Option 2's `OLLAMA_KEEP_ALIVE=2m`** remains important for the Alienware specifically: Ollama automatically unloads models from VRAM after 2 minutes of inactivity, returning 100% GPU memory to ComfyUI.

**Option 1's local TTS recommendation** (Kokoro TTS or Parler TTS instead of ElevenLabs) is worth investigating for animation animatics and should run on the MacBook Pro where the 48GB unified memory provides ample headroom.

**Recommendation:** Install Ollama on all three machines. Use MLX on the MacBook Pro for heavyweight models (14B-32B) — MLX is Apple's native ML framework and extracts significantly better performance from Apple Silicon than Ollama alone for large models. Use Ollama on the Mac Mini for lightweight always-available inference. Use Ollama with CUDA on the Alienware strictly for vision models and tasks that benefit from NVIDIA GPU acceleration. The Mac Mini is the orchestrator that decides where to route each task.

---

### 9. 90-Day Timeline

**Winner: Option 2** — more granular (5 phases vs 3) and accounts for real constraints.

Option 2 splits the 90 days into 5 phases with specific milestones. The key structural advantage: it separates "PM Layer" (Phase 2) from "Meta & Memory" (Phase 3) and "Creative Pipeline" (Phase 4), rather than lumping them together.

**Critical detail Option 2 handles:** During the Boston move (roughly Days 24-28), the Alienware will be boxed up. Option 2 configures `fallback_to_api = True` so agents gracefully shift to 100% Claude API during transit. The Spending Analysis agent queues CSVs until the PC reconnects. Option 1 mentions a "system freeze" but doesn't design for graceful degradation.

**Three-machine move advantage:** The Mac Mini is small, portable, and can be set up immediately in the new apartment — just plug in power, ethernet, and it's running agents again within minutes. The MacBook travels with you. So during the move, two of three machines remain operational. Only Alienware-dependent tasks (ComfyUI, vision QA) go offline. This is far less disruptive than either Gemini response anticipated.

**Recommendation:** Follow Option 2's 5-phase timeline with one modification: Week 1 infrastructure should include setting up Ollama on the Mac Mini (always-on orchestrator) and MacBook Pro (MLX heavyweight inference), not just the Alienware. The Mac Mini becomes the launchd host immediately, freeing the MacBook for interactive work.

---

### 10. SDK vs Agent Teams

**Both agree:** SDK agents for 90% of use cases. Agent Teams only for complex, exploratory, one-off tasks like a full 16BitFit sprint rebuild.

**Option 1 adds a useful detail:** Use Claude Code's `worktree` feature so Agent Teams build in a Git sandbox without breaking your main branch. Worth noting when you eventually use Teams.

---

### 11. "Things I Haven't Thought Of"

**Option 1 wins decisively here** with three insights Option 2 doesn't surface:

1. **Context Poisoning Loop** — Agents reading daily notes will eventually read their own previous outputs and hallucinate loops. Fix: write agent outputs in distinct blockquotes (`> [!bot] Agent Output`) and instruct Read tools to ignore them. *This is a real, non-obvious failure mode that could corrupt your vault over time.*

2. **Prompt Caching Scheduling Trick** — Anthropic charges $3.75/MTok to write to the 5-minute cache, but reads are $0.30/MTok. If your agents run 2 hours apart, you pay the expensive write fee every time. Fix: schedule morning agents back-to-back within the same 5-minute window so Agents 2 and 3 get the 90% cache discount. *This alone could cut your API costs by 30-40% on cache-eligible agents.*

3. **Cursor IDE Workspace Prep** — Have an overnight SDK agent generate a `.cursorrules` file based on the current Jira sprint, so when you sit down at 5 AM your IDE is pre-primed. *Clever cross-pollination between PM automation and creative dev workflow.*

**Recommendation:** Implement all three. The context poisoning fix should be built into vault_inject as a standard pattern. The cache scheduling trick should inform your launchd timing architecture.

**Post-synthesis addition — neither Gemini response caught:**

4. **Mac Mini as Dedicated Orchestrator** — Both responses assumed launchd runs on your daily driver laptop, creating a fragile dependency (laptop must be open for morning agents). Your Mac Mini M4 Pro is purpose-built for always-on headless operation at ~10-15W. Moving all agent schedules to the Mac Mini eliminates the single biggest reliability risk in the system. It also means the MacBook Pro's 48GB unified memory is available for heavyweight MLX inference without competing with orchestration overhead — a clean separation of concerns that mirrors your hexagonal architecture philosophy.

5. **MLX vs Ollama on Apple Silicon** — Neither response mentions MLX, Apple's native ML framework. On Apple Silicon, MLX extracts significantly better performance than Ollama for large models because it's optimized for unified memory architecture. For 14B-32B models on the MacBook Pro, MLX can deliver 2-3x faster token generation than Ollama's Metal backend. Worth benchmarking both during Week 1-2 infrastructure setup.

---

## The Definitive Build Order

Based on synthesizing both responses against your actual codebase, three-machine topology, and goals:

**Week 1-2 (Infrastructure — Three-Machine Setup):**
1. Install Ollama on **Mac Mini** (always-on orchestrator): pull Phi-4 (7B) + nomic-embed-text. Configure as launchd host — migrate all schedules here.
2. Install Ollama on **MacBook Pro**: pull DeepSeek-R1:14b + Qwen2.5-Coder:14b. Investigate MLX for better Apple Silicon performance on 14B+ models.
3. Install Ollama on **Alienware**: pull Qwen2.5-VL-7B (vision). Set `OLLAMA_HOST=0.0.0.0:11434`, `OLLAMA_KEEP_ALIVE=2m`. Configure Windows Firewall for LAN-only access.
4. Build `lib/hybrid_router.py` with **three-tier routing**: Mac Mini (localhost) → MacBook Pro (LAN) → Alienware (LAN + health check) → Claude API (fallback). Include WOL for Alienware.
5. Build `lib/csv_anonymizer.py` (Option 1's airgap pattern)
6. Implement filelock in vault_io.py
7. Audit and fix interactive-language in skills (Option 1's audit)
8. Add macOS Keychain credential helper (Option 1's pattern)
9. Build 3 new hooks: loop-detector, cost-watchdog, vault-integrity

**Week 3-4 (First Agents — Pre-Move):**
10. Process Inbox → Mac Mini, 100% local (Phi-4 7B)
11. Spending Analysis → MacBook Pro, 100% local (DeepSeek-R1:14B) + CSV sanitizer
12. Boston Move Coordinator → Claude Sonnet via Mac Mini orchestration (expires March 22)
13. Implement Baton File dependency chain: Process Inbox → Daily Driver
14. Verify Mac Mini runs all morning schedules reliably without laptop open

**Week 5-6 (PM Layer — Post-Move):**
15. Set up Mac Mini in Boston apartment first (plug and play, agents resume immediately)
16. Reconnect Alienware once unpacked, verify WOL from Mac Mini, test three-machine routing
17. Sprint Health Monitor → Claude Sonnet via Mac Mini (needs Jira MCP)
18. Meeting Defender → Mac Mini routes pre-classification to Phi-4, synthesis to Claude Haiku
19. Set up mcp-atlassian with Keychain credentials

**Week 7-8 (Retrieval & Memory):**
20. Vault Embedding Indexer → Mac Mini nightly, 100% local (nomic-embed-text to SQLite)
21. Preserve Session → MacBook Pro, 100% local (DeepSeek-R1:14B) — triggers when you close Claude Code on laptop
22. PR Digest → MacBook Pro, 100% local (Qwen2.5-Coder:14B)

**Week 9-10 (Creative Pipeline):**
23. Pull Qwen2.5-VL-7B on Alienware for vision QA
24. ComfyUI Sprite Orchestrator → Mac Mini orchestrates, Alienware runs ComfyUI + vision QA, Claude Sonnet for high-level decisions
25. Festival Tracker → Mac Mini, Claude Haiku + Google Sheets via Zapier

**Week 11-12 (Meta & Optimization):**
26. Meta-Agent / Chief of Staff → Mac Mini orchestrates map-reduce: MacBook Pro runs local summaries (Qwen2.5-32B via MLX), Claude Opus synthesizes
27. Full fleet token audit across all three machines
28. Implement prompt caching scheduling (cluster API agents in 5-min windows on Mac Mini)

---

## Key Numbers

| Metric | Target |
|--------|--------|
| Total agents at steady state | 15-18 |
| Agents running 100% local | 10-12 (up from 8-10, thanks to Mac Mini + MacBook capacity) |
| Monthly API cost (steady state) | $3-6 |
| Monthly electricity — Mac Mini (24/7) | ~$1.50 |
| Monthly electricity — Alienware (on-demand) | ~$1.50-2.00 |
| Monthly electricity — MacBook Pro | Negligible (battery + charging) |
| Total monthly system cost | **~$6-10** |
| Rocket Money cost replaced | $12/mo |
| Net savings from Day 1 | **$2-6/mo positive** |
| Machines running Ollama | 3 (triple redundancy) |
| Move disruption window | Minimal — Mac Mini + MacBook operational immediately, only Alienware needs unpacking |

The three-machine topology makes the system more resilient, more capable, and slightly cheaper than either Gemini response projected. The Mac Mini's always-on nature eliminates the laptop-must-be-open constraint that both responses designed around, while the MacBook Pro's 48GB unified memory unlocks 32B model inference that neither response thought was possible on the Mac side.
