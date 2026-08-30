# CLAUDE.md

This is Code-Brain — Sean's personal command center, a second brain built on Claude Code.

## What This Repo Is

**2 active domain folders** (`creative-studio/`, `life-systems/`) + archived `the-block/` reference + cross-cutting infrastructure, an Obsidian vault, and an autonomous Agent SDK layer. Everything in `.claude/` auto-loads. The installer exports subsets to other projects. Live counts via `ls .claude/{skills,agents,hooks}/`.

## Non-Negotiable Rules

1. **Plan Mode vs Extended Thinking**: Plan Mode = double `Shift+Tab` or `/plan`. Extended Thinking = single `Tab`. Never confuse the two.
2. **Agent tool restrictions**: Use `disallowedTools` (deny-list), not allow-list.
3. **Hooks enforce; subagents judge**: PreToolUse for binary allow/deny; subagents for subjective reviews.
4. **Hook blocking**: Exit code **2** to deny (not 0 or 1).
5. **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
6. **Permission evaluation** (first match wins): Deny > Ask > Allow
7. **Domain structure**: Active domain content goes in `creative-studio/` or `life-systems/` only. `the-block/` is archived reference — don't add new content there. Nested: `product-management/` under `the-block/`; `design-team/` and `16bitfit-battle-mode/` under `creative-studio/`.
8. **Capture deferred work as tickets**: When work surfaces a follow-up that won't finish in the current session (cost incidents, deferred fixes, "do this later," scoped-but-not-started redesigns), append a one-line `- ` bullet under `## Todo` in [vault/00_inbox/tickets.md](vault/00_inbox/tickets.md) **before wrapping up** — don't let it get lost in the shuffle. One ticket per bullet; optional ` — assigned: {name}` suffix; sub-bullets are ignored. This file is the Manual lane of the Agent Fleet Observability kanban board (`agent-fleet-observability/`, schema at `agent-fleet-observability/docs/manual-tickets-schema.md`) and is auto-injected into every session by [.claude/hooks/session-start-inject-tickets.sh](.claude/hooks/session-start-inject-tickets.sh), so open tickets are always in context.
9. **Privacy layer (2026-06-10)**: This is a public repo. Personal and employer-confidential material lives on local disk only, gitignored under the `PRIVATE LAYER` block in [.gitignore](.gitignore) — the job-hunt home (`vault/20_projects/prj-job-hunt-2026/`, incl. `source-material/` and its own private `tickets.md`), operating models (`vault/05_atlas/operating-models/`), timeline notes (`vault/10_timeline/`), skill reference profiles (`.claude/skills/{personal-finance,life-admin}/references/`, `.claude/skills/writing-voice-modes/{references,drafts}/`), and The Block archives (`the-block/`, granola notes, media-team-ideas, `vault/60_archive/operating-models-the-block-2026-05/`). **Never `git add` these paths, never weaken these ignore rules, and never write real income/medical/contact/employer data into tracked files** — public skills point at their local-only reference files instead. History was scrubbed via git filter-repo (see [docs/2026-06-10-code-brain-recruiter-readiness-audit-plan.md](docs/2026-06-10-code-brain-recruiter-readiness-audit-plan.md)).

### Hook Exit Codes

- `0` = Allow
- `1` = Error (logged, operation allowed)
- `2` = **Deny** (blocks the operation)

## Domain Workspaces

| Domain | CLAUDE.md | What lives here |
|--------|-----------|----------------|
| `the-block/` | [the-block/CLAUDE.md](the-block/CLAUDE.md) | **Archived 2026-05** — reference templates from prior role at The Block. |
| `creative-studio/` | [creative-studio/CLAUDE.md](creative-studio/CLAUDE.md) | Phaser game dev, Remotion video, pixel art, Adobe MCP, animation, writing. Nested: `16bitfit-battle-mode/` (project), `design-team/` (design system + review agent support) |
| `life-systems/` | [life-systems/CLAUDE.md](life-systems/CLAUDE.md) | Finance, health, learning, tasks, time, career transition |
| `claude-mastery/` | (no CLAUDE.md — cross-cutting reference) | CLI, hooks, MCP, settings, tech stack, prompt-engineering reference |
| `vault/` | (Obsidian, not a workspace) | PARA notes, prompts, RAG, Granola meeting sync, operating-model artifacts. Active job-hunt project at `vault/20_projects/prj-job-hunt-2026/` |

## Domain Routing

Use this table to decide which CLAUDE.md to load for a given task:

| Task type | Load this CLAUDE.md |
|---|---|
| PM / day-job / Block work *(archived)* | [the-block/CLAUDE.md](the-block/CLAUDE.md) |
| Creative work (Remotion, art, writing, animation) | [creative-studio/CLAUDE.md](creative-studio/CLAUDE.md) |
| 16BitFit Battle Mode specifically | [creative-studio/16bitfit-battle-mode/CLAUDE.md](creative-studio/16bitfit-battle-mode/CLAUDE.md) |
| Personal systems (finance, health, learning, time) | [life-systems/CLAUDE.md](life-systems/CLAUDE.md) |
| Job-hunt work | `vault/20_projects/prj-job-hunt-2026/` |
| Claude Code CLI / hooks / MCP / settings reference | [claude-mastery/](claude-mastery/) |

## Design Team Agents

| Agent | Role |
|-------|------|
| UI Reviewer | Layout, spacing, color, typography, hierarchy |
| Accessibility Checker | WCAG 2.1 AA, contrast, keyboard nav, ARIA |
| Design System Enforcer | Token compliance, naming, component patterns |
| Visual Polish Auditor | Animations, loading/empty/error states, polish |

All read-only (disallowedTools: Edit, Write, Bash).

## Connected MCPs (Native — No Zapier)

Skills and agents prefer native MCPs over Zapier. When both exist, always use native first.

| Service | Native MCP | Zapier Fallback |
|---------|-----------|----------------|
| Google Calendar | `claude.ai Google Calendar` / `google-workspace` | `google_calendar_*` |
| Gmail | `claude.ai Gmail` / `google-workspace` | `gmail_*` |
| Google Sheets/Docs/Drive | `google-workspace` | `google_sheets_*` / `google_docs_*` |
| Jira + Confluence | `mcp-atlassian` / `claude.ai Atlassian` | `jira_software_cloud_*` |
| Slack | Slack plugin (pending Block admin approval) | `slack_*` |
| GitHub | `github` MCP (Docker) | N/A |

**Still Zapier-only:** Salesforce, GA4, Webhooks, Code execution.

**Calendar rule:** Single calendar — `sean.winslow28@gmail.com`. The Block work calendar archived 2026-05.

## Connected External Research APIs

**Gemini Deep Research** — `agents-sdk/scripts/gemini_dr.py` + `.claude/skills/gemini-deep-research` skill. **Requires `google-genai >= 2.0.0`** (2026-08-05: Google hard-rejects the legacy 1.x Interactions schema with a 400; 2.x returns `interaction.steps`, and a DR report is chunked across *multiple* `model_output` steps — all of them must be concatenated or the note silently loses part of its body). Credential resolution: Keychain (`com.sean.agents.gemini_api_key`) → `GEMINI_API_KEY` env → `agents-sdk/.env` → repo-root `.env`. Caps: $7/task, $20/day, $50/month — tracked in `vault/health/gemini-spend-{YYYY-MM}.json`. Autonomous agent (`gemini_researcher.py`) is default-disabled; opt in with `INSTALL_GEMINI=1` when running `install_schedules.sh`.

**Before citing any DR figure, tier-audit it** — `agents-sdk/scripts/audit_dr_citations.py <report.md>` resolves the opaque `vertexaisearch` grounding-redirect URLs and classifies each source (A academic / B primary / C trade / D forum). $0, read-only. **Query shape drives source tier:** research-shaped questions ("what does the literature measure") pull ~90% academic sources; market-shaped questions ("what exists in this category") pull mostly vendor SEO marketing — fresh marketing, which recency instructions cannot filter out. DR also cannot prove a negative; for "does anything like X exist", falsify a named candidate list instead.

**LLM Council** — `tools/llm-council/council/` + `.claude/skills/llm-council/` skill. Two profiles: `premium` (Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20, Opus 4.7 chairman, ~$0.29/run) and `variance` (Sonnet + GPT-5.4-mini + DeepSeek v4-pro + Mistral medium-3-5, Sonnet chairman, ~$0.14/run). Caps: $1.00 / $0.40 per query, $7/day, $40/month — tracked in `vault/health/council-spend-*.json`. Use for high-variance critique (voice calibration, cover-letter critique, decision pre-mortem, PRD stress-test) where vendor RLHF spread gives independent blind-spot coverage. Karpathy's original web app remains usable at `tools/llm-council/upstream/`.

**fusion-discovery-council** — `tools/llm-council/` (`uv run python -m council.discovery`) + `.claude/skills/fusion-discovery-council/` skill. Evidence→idea discovery: mines real, freshly-fetched user pain points and frames them as ranked, evidence-linked PM opportunities. Four stages — GATHER (last30days + Perplexity Sonar + web) → FUSE (OpenRouter Fusion panel + judge) → VERIFY (anti-fabrication gate, drops any pain point not traceable to a real fetched URL) → FRAME (pm lens → idea ledger; substack lens → post-angle ledger + substack-value-engine handoff brief). Tiers: `quick` $0.50 / `standard` $1.50 / `deep` $4.00 per run; caps $30/day, $100/month (cap policy v3, enforced from `tools/llm-council/council/cap_policy.json`), **separate from council** — spend lands in the shared `vault/health/council-spend-*.json` tagged `tool="discovery"`. Reuses the council client/budget spine (`client.py`/`budget.py`) under the new `council/discovery/` subpackage. Run history persists to vault/20_projects/research/.discovery-sessions/ by default ($DISCOVERY_SESSIONS_DIR overrides); render the run-history dashboard with 'uv run python -m council.discovery.dashboard --output <path>' ($0, self-contained HTML).

**Local TTS** — [`agents-sdk/scripts/doc_to_audio.py`](agents-sdk/scripts/doc_to_audio.py) renders vault markdown to verbatim narration via Kokoro-82M ONNX (Apache 2.0, $0/run on Apple Silicon). Single voice (default `af_heart`); structural markdown is flattened or spoken-cued; output at `vault/90_system/audio/<source-stem>.mp3`; CLI is idempotent on mtime. Fresh-machine setup: [`agents-sdk/scripts/install_tts_models.sh`](agents-sdk/scripts/install_tts_models.sh). Decision record: [`agents-sdk/docs/local-tts-decision-record.md`](agents-sdk/docs/local-tts-decision-record.md). Spotify handoff sketched at [`agents-sdk/docs/local-tts-spotify-handoff.md`](agents-sdk/docs/local-tts-spotify-handoff.md), deferred until 10+ clean pipeline runs.

## Commands

```bash
# Validate everything
python3 scripts/validate.py

# Export skills to another project
./scripts/install.sh /path/to/project --preset starter|power|enterprise|creative
./scripts/install.sh /path/to/project pm-workflows remotion-mastery
./scripts/install.sh --list

# Render a vault doc to a verbatim local-TTS MP3 (Kokoro-82M, $0/run, Apple Silicon)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/doc_to_audio.py \
  --source ../vault/20_projects/research/2026-05-13-foo.md
```

## Agents SDK (Autonomous Layer)

The `agents-sdk/` directory adds scheduled, autonomous agents powered by the Claude Agent SDK. These run **outside** Claude Code sessions on macOS launchd schedules. Skills are loaded as system prompts — no duplication.

**Agent inventory** (status indicated inline — `default disabled` / `manual-trigger only`; everything else runs on launchd):

| Agent | Schedule | Skills/Model | Cost/Run |
|-------|----------|---------------|----------|
| Vault Indexer | 2:00 AM daily | nomic-embed-text (Mac Mini Ollama) | $0.00 (local) |
| Vault Synthesizer | 2:30 AM daily | `qwen3.6_35b-a3b-32k` on MBP-Ollama (Tier-2; WOL retired). Off-LAN nights defer cleanly (BT5, 2026-07-05): one 90s route pre-flight → typed `wol-deferred` manifest, exit 0, indexer state held so the work self-re-queues — **not** the old poll-storm `error`. A mid-run host loss trips a circuit breaker → `partial`. | $0.00 (local) |
| Deep Researcher | 2:45 AM daily | LDR + SearXNG + Qwen3-14B GGUF (Q4_K_M, `qwen3-14b-research:latest` Modelfile with `/no_think`) via Ollama on Mac Mini at `localhost:5050`. Hard 900s timeout — heavy compound topics must route to Gemini DR/DR Max (see routing rule below). | $0.00 (local) |
| Vault Critic | 3:30 AM daily | Codex CLI (gpt-5.5, ChatGPT Plus) + Anti-Gravity CLI (Gemini 3.1 Pro, Google personal OAuth) via parallel subprocess shell-out; no Claude SDK in the nightly path | $0 (subscriptions absorb) |
| Daily Driver (morning) | 8:30 AM daily | daily-driver, vault-read-write + operating-model HEARTBEAT awareness | ~$0.40 (cap $0.60) |
| Meta-Agent (fleet health) | 8:45 AM daily (runs *after* daily-driver to eliminate the `Daily note exists: No` race) | gemma4:e4b (Mac Mini Ollama) + local health checks + schedule-recommendations context | $0.00 (local) |
| Knowledge Lint | Sunday 22:00 | Tier 1 structural Python checks (Mac Mini); Tier 2 = staleness regex + `concept_edges` SQL fast path (Mac-Mini-local, always run) + an LLM leg (`qwen3.6_35b-a3b-32k` on MBP, probe-first) that injects the `knowledge/concepts` corpus in 32K-context batches for contradiction discovery + `soul-tier-a-conflict` (3-domain SOUL context). BT5 C3 wired this leg into production 2026-07-05 (it had never run); a down host defers honestly with a report line, not a silent skip. | $0.00 (local) |
| Flush (SessionEnd) | hook-triggered | gemma4:e4b on Mac Mini via `inbox_triage` routing for <100-msg sessions; ≥100-msg sessions attempt `qwen3.6_35b-a3b-32k` on MBP if awake; 3-domain SOUL prepend | $0.00 (local) |
| Gemini Researcher (**default disabled**) | 03:30 daily (when `INSTALL_GEMINI=1`) | Gemini DR / DR Max via `gemini_dr.run` | $0–7/run; capped $7 task / $10 day / $20 month |
| Job Feed | 8:00–11:00 AM (7 fires) | Qwen3-14B on MBP via HybridRouter (`fallback_disabled=true`); 4 free public feeds + ~40-company ATS watchlist; SQLite + Markdown roll-up; optional Gmail email digest (`[notifications.email]`, opt-in, `lib/job_email.py`) + instant Pushover push on strong fits (`[notifications.push_strong_fits]`, opt-in) | $0.00 |
| Skill Optimizer (**manual-trigger only**) | manual (`agents-sdk/agents/skill_optimizer.py`) | Opus 4.7 generation + Qwen3-14B local judge + Sonnet 4.6 sample-check every 5 iters; autoresearch loop on a single SKILL.md | $20–145/run (cap $200) |
| Substack-Drafter (**default disabled**) | Thursday 18:00 weekly (when `INSTALL_SUBSTACK_DRAFTER=1`) | HybridRouter (Qwen3-14B local → Sonnet 4.6 fallback); reads writing-voice-modes SKILL.md verbatim; 5-week voice rotation (sean/sedaris/kerouac/thompson/vonnegut) | $0–0.10/run (cap $0.10) |

**Research routing rule:** Heavy multi-target research belongs on Gemini DR or DR Max, **not** local LDR. Two independent reasons:

1. **Timeout** — local LDR has a hard 900s budget. Compound prompts (≥3 sub-questions, multi-target evaluations, due-diligence matrices) routinely exceed it.
2. **Citation quality collapse** — even when LDR finishes, Qwen3-14B can't ground citations across multiple targets at once. Canonical bad-output specimen retained at [`vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md`](vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md) (`status: superseded`, contains fabricated entities like `PureMCPClient` and fabricated `learn.microsoft.com` URLs).

**Triage rule for `vault/00_inbox/research-queue.md`:** if the topic compounds three or more independent investigations, drop it via the `gemini-deep-research` skill (or `gemini_dr.py --tier dr|max`) rather than the queue. The queue is for single-shape topics (one target, one question, one pattern) — Qwen3-14B + SearXNG can ground those reliably at $0.

**Process Inbox: paused 2026-04-29 pending Path B rewrite to local `gemma4:e4b`.** Cloud-Sonnet path validated as working (~3 files/run) but cost-inefficient ($1.16/file vs $0/file local). Manual triage via the `process-inbox` skill in interactive sessions is the working alternative. Full history + Path B scope: [`agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`](agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md).

**8 agents disabled 2026-04-09 remain disabled** — `process-inbox`, `daily-driver` evening, `daily-driver` weekly, `pr-digest`, `sprint-health`, `meeting-defender`, `preserve-session`, `spending-analysis`. Do NOT re-enable without Sean's explicit approval. See [`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`](agents-sdk/AUDIT-2026-04-09-agent-downsizing.md) — its summary is unambiguous: *"Of 10 enabled agents, only 2 were producing value. The other 8 were disabled."*

*(Corrected 2026-08-11 during WS2 archaeology. This line previously said "6" and named `health-audit` and `md-to-anki`, which the audit never mentions and which have **never existed as code** — `git log --diff-filter=AD` returns nothing for `agents/health_audit.py` or `agents/md_to_anki.py`; they are unimplemented entrypoints in `pyproject.toml` and stanzas in `config.toml` only. This is a public-facing count on the fleet board, so the audit's eight is canonical.)*

**Key limitation:** Headless SDK agents cannot access MCP servers (Slack, Google Calendar, Gmail, etc.) — those require browser-based OAuth only available in interactive sessions. The morning agent creates the daily-note skeleton; Slack/calendar data is backfilled when Sean starts an interactive session.

```bash
# Dry run (free, prints prompt)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run

# Live run
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning

# Install/remove launchd schedules
./agents-sdk/schedules/install_schedules.sh
./agents-sdk/schedules/install_schedules.sh --remove

# Run tests
cd agents-sdk && PYTHONPATH=. pytest tests/ -v
```

Config: `agents-sdk/config.toml`. Auth: `claude login` OAuth (no API key). For unattended launchd runs, prefer a long-lived `claude setup-token` token stored in Keychain (`python3 agents-sdk/lib/keychain.py set claude_code_oauth_token <token>`) — [lib/auth.py](agents-sdk/lib/auth.py)'s `resolve_oauth_token()` injects it as `CLAUDE_CODE_OAUTH_TOKEN`, so headless runs don't 401 when the interactive credential expires (root cause of the 2026-06-20 morning 401). Safety: max 30 turns, default $0.50/run cap (daily-driver morning bumped to $0.60 to absorb the operating-model artifact preamble). SDK version: `0.1.63` (pinned in `agents-sdk/pyproject.toml`). Morning schedule: daily-driver 08:30 writes the note, meta-agent 08:45 reports on it. Full docs: `docs/agents-sdk.md`.

## Architecture decisions (current capabilities — full history in CHANGELOG.md)

| Subsystem | What it does | Where |
|---|---|---|
| Operating-model artifacts | HEARTBEAT/USER/SOUL/schedule-recs loaded on-demand into daily-driver, meta-agent, flush, knowledge_lint (`soul-tier-a-conflict` issue kind, HIGH). Toggle `[artifacts]` in `config.toml`. | [`agents-sdk/lib/artifact_loader.py`](agents-sdk/lib/artifact_loader.py) |
| Knowledge loop (producer) | SessionEnd flush → 02:30 synthesizer → 03:30 vault_critic → Sunday lint | see Active agents table above |
| Knowledge loop (consumer) | SessionStart hook injects `vault/knowledge/index.md` as additionalContext (**80K cap**, 5s timeout). **Renders compact slug rows, not the file's wikilinks** (#202) — the file's format averages 116 chars/row and says the slug twice, a bare slug 50. Cap raised from 15K on 2026-08-29 so the **whole graph lands: 218/218 concepts + 694/694 connections, 45,671 chars (~11.4K tokens), 43% headroom.** The cap is a ceiling, not a cost. If the graph ever outgrows it, the truncated section is selected by `updated:`/`created:` frontmatter (never mtime — a sync rewrites every mtime at once) and the hook states how many rows it dropped. `index.md` itself is untouched so Obsidian still navigates by wikilink; a headroom test fails at 20% so the next crossing is loud. | [`.claude/hooks/session-start-inject-index.sh`](.claude/hooks/session-start-inject-index.sh) |
| PreCompact safety net | Fires `flush.py --trigger pre-compact` before context auto-compaction (`tag:` field in daily-log distinguishes flush types) | [`.claude/hooks/pre-compact-flush.sh`](.claude/hooks/pre-compact-flush.sh) |
| Vault Synthesizer | T1 quote-first prompt + cross-domain preference, T1.5 `evaluate_article_depth()` gate with `rejected_reasons` in manifest, T2 HDBSCAN cluster-and-sample retrieval. T3 (EDC canonicalization) deferred; T4 (three-pass) post-employment. | [`agents-sdk/agents/vault_synthesizer.py`](agents-sdk/agents/vault_synthesizer.py), [`lib/retrieval_diversity.py`](agents-sdk/lib/retrieval_diversity.py). Plan: [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md) |
| Vault Critic | Codex CLI + Anti-Gravity CLI parallel critique → concepts land at `vault/knowledge/expansions/{slug}.md`, connections at `vault/knowledge/expansions/connections/{slug}.md` (collision-namespaced). $0 incremental, 600s wall-clock budget, 120s per-CLI; both-rate-capped → `status: partial`. Nightly manifest at `vault/health/critic-manifest-{date}.json`. **Manual mode** (`--target <path>` repeatable / `--from-list <file>` / `--force`) bypasses the manifest gate to critique any existing concept or connection on-demand; writes to `critic-manifest-{date}-manual-{HHMMSS}.json` so it never clobbers the nightly file the meta-agent reads. **Round-3 enrichment is the default** (validated 2026-05-24 across 12 articles, 0 failures): every prompt auto-prepends the [vault-critic-standing-context.md](agents-sdk/prompts/vault-critic-standing-context.md) "About Sean" preamble plus the project files listed in `[agents.vault_critic].default_context_files` (CLAUDE.md + 16BitFit CLAUDE.md + intent-engineering overview). Critics therefore reference Sean's actual fleet topology, file paths, and lived incidents by name instead of giving generic recommendations. Disable per-run with `--no-standing-context` / `--no-default-context`; add more files with `--context <path>` (appends to defaults). | [`agents-sdk/agents/vault_critic.py`](agents-sdk/agents/vault_critic.py); plan [`agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`](agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md) |
| Concept edges | SQLite table (6 relations: supports/contradicts/evolved_into/supersedes/depends_on/related_to); knowledge_lint Tier 2 queries active contradictions via SQL fast path | `vault/.vault-index.db`; [`agents-sdk/lib/concept_edges.py`](agents-sdk/lib/concept_edges.py) |
| Daily note as fleet console | Overnight digest injected at `<!-- fleet-overnight -->` anchor; Dataview blocks auto-surface today's new concepts/connections/research + latest lint report | [`agents-sdk/lib/fleet_summary.py`](agents-sdk/lib/fleet_summary.py), [`vault/90_system/templates/tpl-daily.md`](vault/90_system/templates/tpl-daily.md) |
| Knowledge Q&A tier | Two-pass orchestration against `vault/knowledge/index.md`; `--file-back` persists to `vault/knowledge/qa/<slug>.md` with chunk_id provenance and append-only JSONL manifest | [`agents-sdk/scripts/query.py`](agents-sdk/scripts/query.py) |
| Auto-stub people | SessionEnd hook auto-creates `vault/40_knowledge/people/<slug>.md` from new `author:` wikilinks (structured-signal filter, 1-3 capitalized tokens, 10/run cap) | [`.claude/hooks/session-end-auto-stub.sh`](.claude/hooks/session-end-auto-stub.sh), [`agents-sdk/scripts/auto_stub_people.py`](agents-sdk/scripts/auto_stub_people.py) |
| Knowledge Lint scope | Excludes `[[NNN]]` citation markers + `node_modules` + archived `the-block-meetings-granola-notes`; vault sits at 0 broken wikilinks | [`agents-sdk/agents/knowledge_lint.py`](agents-sdk/agents/knowledge_lint.py) |
| Fleet memory (Phase 1) | Shared filesystem-memory layer at `vault/90_system/fleet-memory/`. `BetaAbstractMemoryTool` subclass with realpath-prefix-checked path guard, per-agent namespacing, explicit promote_to_shared(). Pilot agents: `vault_synthesizer` (read-and-inject) + `daily_driver` (MCP-server bridge). Default-disabled; opt in via `[fleet_memory.per_agent.{agent_id}].enabled=true`. | [`agents-sdk/lib/fleet_memory.py`](agents-sdk/lib/fleet_memory.py); plan [`agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md`](agents-sdk/docs/plans/2026-05-27-fleet-memory-phase-1-plan.md) |
| Tier C batch route | Fleet's **first Tier C production model**: `gemma4_26b-32k` @ Alienware (RTX 5080 16GB, Ollama `192.168.68.201:11434`). **Batch / async only** (~30 tok/s sustained — NOT interactive), **Pattern-E-gated** (Alienware reachable ~7am–5pm via manual wake only; remote wake architecturally impossible). Exposed as `task_map` route `tier_c_batch_summarize` with `fallback = "none"` — an off-hours miss raises `RouteUnavailable`, never the paid Claude API (cost-safety) and never a dead WoL packet. **No auto-consumer wired** (2026-06-03) — manual / opt-in route. Soak verdict: 17/17 datapoints clean. | [`agents-sdk/lib/hybrid_router.py`](agents-sdk/lib/hybrid_router.py); soak closeout [`vault/20_projects/research/2026-06-03-topic-20-tier-c-soak-closeout.md`](vault/20_projects/research/2026-06-03-topic-20-tier-c-soak-closeout.md); plan [`agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md`](agents-sdk/docs/plans/2026-06-03-tier-c-batch-route-wiring-plan.md) |
| Portfolio daily-dated layer | Daily Driver morning post-step renders the live portfolio's four `public/api/*.json` (dateline + about-pulse from fleet data + measured ex-vault commit count; next-piece editorial from `[portfolio.next_piece]`; shipped-stats live npm+GitHub per `[portfolio.shipped_stats]`), runs the portfolio's `npm run validate`, and **only on pass** commits `chore(daily): fleet refresh <date>` to a `main`-pinned worktree → push → Vercel auto-deploy. Honesty-preserving: stale/failed → evergreen fallbacks, never fabricated; a failed shipped-stats fetch skips the file (never zeroes). Trigger is **push-only** (no deploy hook). | [`agents-sdk/lib/portfolio_dateline.py`](agents-sdk/lib/portfolio_dateline.py); runbook [`agents-sdk/docs/portfolio-refresh-runbook.md`](agents-sdk/docs/portfolio-refresh-runbook.md) |

**launchd requirement:** All plists must include `EnvironmentVariables` with `PATH` set to `/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Without this, the `claude` CLI is not discoverable and agents fail with `CLIConnectionError`. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`.

## Architecture

```
.claude/
├── skills/          # Canonical skill store (auto-loaded)
├── agents/          # Claude Code subagents (domain + design team) — separate from agents-sdk/
├── hooks/           # PreToolUse/PostToolUse/SessionStart/SessionEnd/PreCompact hooks
└── settings.json    # Standard security profile

agents-sdk/          # Autonomous agents (Claude Agent SDK, Python) + local CLIs
├── agents/          # Agent scripts (daily_driver.py + scheduled launchd agents)
├── lib/             # Shared modules (config, skill loader, artifact loader, vault I/O, logging, markdown_to_speech, kokoro_synth)
├── docs/            # Decision records, rollback guides, handoff sketches (e.g., local-tts-*)
├── models/          # Local model weights (gitignored; populated by install_tts_models.sh)
├── scripts/         # CLI tools (query.py, doc_to_audio.py, install_tts_models.sh, gemini_dr.py, etc.)
├── schedules/       # launchd plists + installer
├── tests/           # pytest suite
└── config.toml      # Agent + CLI config, paths, safety limits

the-block/                            # DOMAIN 1 — day job
├── CLAUDE.md
├── README.md
└── product-management/               # nested workspace

creative-studio/                      # DOMAIN 2 — creative work
├── CLAUDE.md
├── README.md
├── 16bitfit-battle-mode/             # nested project
├── design-team/                      # nested workspace
└── (existing finance/, scripts/, templates/)

life-systems/                         # DOMAIN 3 — personal systems
├── CLAUDE.md
├── README.md
└── (existing reference/)

claude-mastery/      # cross-cutting Claude Code meta-reference (stays at root)
systemcraft/         # AI PM system design studio — public machinery (bench, templates, README);
                     # corpus/ + ledger/ gitignored local-only. Build map: GitHub issue #142
tools/                                # sidecar tools (non-skill, non-agent)
├── llm-council/                      # Multi-vendor LLM council (inspired by karpathy/llm-council)
│   ├── upstream/                     # Karpathy's reference web app, unmodified
│   └── council/                      # Headless CLI used by .claude/skills/llm-council/
└── governance-demo/                  # Authority/Recovery/Audit demo (Task 14) — replay_budget_breach.py + fixtures + tests; pairs with agents-sdk/docs/CONTROL_ARCHITECTURE.md
evals/
└── vault-synthesizer/   # 10-case eval suite for the nightly synthesizer
vault/               # Obsidian vault (PARA + MOCs + operating-models + Prompts + RAG)
export-groups/       # Metadata-only manifests (for installer export)
shared/hooks/        # Hook source files (for installer)
shared/security/     # Security profiles (standard, enterprise)
presets/             # Export presets (starter, power, enterprise, creative)
scripts/             # install.sh, install.ps1, validate.py
plugin/              # Marketplace distribution
docs/                # Ecosystem documentation
├── prompts/         #   cross-cutting kickoff/continuation prompts (project-local prompts stay co-located)
└── plans/           #   cross-cutting plans & audits (mirrors agents-sdk/docs/plans/; skill-session plans stay in docs/superpowers/)
```

## When Modifying

- Run `python3 scripts/validate.py` after changes (validator hard-enforces the 3 primary domain folders)
- Skills live in `.claude/skills/` (not export-groups)
- Agents live in `.claude/agents/` (not shared/agents/)
- Update `export-groups/*/playground.json` manifests when adding/removing skills
- New domain-specific content goes inside the correct domain folder (`the-block/`, `creative-studio/`, or `life-systems/`)
- Cross-cutting kickoff/continuation prompts go in `docs/prompts/`; cross-cutting plans/audits in `docs/plans/` (`YYYY-MM-DD-slug.md`). Never at repo root. Project-local prompts/plans stay co-located (`agents-sdk/docs/plans/`, `creative-studio/16bitfit-battle-mode/prompts-and-summaries/`, `docs/superpowers/`)
- **Doc updates on new Skill/Agent/Hook/Script**: add a CHANGELOG.md entry and update any count tables in CLAUDE.md and README.md

## Agent skills

### Issue tracker

Issues, PRDs, and wayfinder maps live in GitHub Issues (`seanwinslow28/code-brain`) via the `gh` CLI; external PRs are NOT a triage surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Canonical vocabulary, unmodified: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Multi-context: `CONTEXT-MAP.md` at root routes to per-domain `CONTEXT.md` files (created lazily by `/domain-modeling`). See `docs/agents/domain.md`.
