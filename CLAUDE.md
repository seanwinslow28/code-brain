# CLAUDE.md

This is Code-Brain — Sean's personal command center, a second brain built on Claude Code.

## What This Repo Is

119 skills, 13 Claude Code subagents, 14 hooks, 18 autonomous SDK agents (9 active on launchd, 2 opt-in disabled-by-default, 1 manual-trigger), **3 primary domain folders** + cross-cutting infrastructure, an Obsidian vault, and an Agent SDK layer for autonomous operation. Everything is active and auto-loaded. The installer exports subsets to other projects.

As of v3.15.0, the repo is organized so that domain-owned folders live inside their domain. `the-block/` is Sean's day-job workspace (with `product-management/` nested inside). `creative-studio/` owns 16BitFit and the design-team workspace. `life-systems/` owns personal systems. Cross-cutting infra (`.claude/`, `agents-sdk/`, `vault/`, `claude-mastery/`, installer dirs) stays at root.

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

**Gemini Deep Research** is available via `agents-sdk/scripts/gemini_dr.py` (wrapping the `google-genai` SDK) and the `.claude/skills/gemini-deep-research` skill. The API key is stored in macOS Keychain as `com.sean.agents.gemini_api_key`. Use the `gemini-deep-research` skill to decide when to delegate to Gemini DR vs. run a local LDR query. Cost is self-policing: $7 per-task hard cap, $20 per-day circuit breaker, $50 per-month governor (bumped 2026-05-07 from $10 / $20 to absorb heavy DR Max runs) — tracked in `vault/health/gemini-spend-{YYYY-MM}.json`. The autonomous agent (`gemini_researcher.py`) is default disabled; opt in with `INSTALL_GEMINI=1` when running `install_schedules.sh`.

**LLM Council** (NEW v3.35.0; variance panel updated v3.37.1, 2026-05-16) is available via `tools/llm-council/council/` (a headless Python CLI wrapping OpenRouter) and the `.claude/skills/llm-council/` skill. Two profiles — `premium` (Claude Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20, chairman Opus 4.7, ~$0.29 typical) and `variance` (Claude Sonnet + GPT-5.4-mini + DeepSeek v4-pro + **Mistral medium-3-5** (Qwen 3.5 Plus swap, see [swap history](tools/llm-council/model-selection-2026-05-14.md#2026-05-16-qwen-35-plus--mistral-medium-3-5)), chairman Sonnet, ~$0.14 typical). Cost-disciplined: per-query caps ($1.00 / $0.40), $7/day circuit breaker, $40/month governor — spend tracked atomically in `vault/health/council-spend-*.json`. Use for high-variance critique (voice-mode calibration, cover-letter critique, decision pre-mortem, PRD stress-test) where different vendor RLHF biases produce useful spread or independent blind-spot coverage. Inspired by [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council) — his original web app remains usable unmodified at `tools/llm-council/upstream/`. Phase C (separate public MCP server at `seanwinslow28/llm-council-mcp`) is deferred until 5–10 real runs validate the API surface.

**Local TTS (NEW v3.36.0)** is available via [`agents-sdk/scripts/doc_to_audio.py`](agents-sdk/scripts/doc_to_audio.py) — verbatim narration of vault markdown using Kokoro-82M ONNX (Apache 2.0, ~310MB fp32 model, $0/run on Apple Silicon via `kokoro-onnx`). Single voice (default `af_heart`), strict UTF-8, sentence-level content preserved byte-for-byte; structural markdown (frontmatter, code fences, wikilinks, links, tables) is flattened or replaced with spoken cues. Output lands at `vault/90_system/audio/<source-stem>.mp3` and the CLI is idempotent on mtime. **Setup on a fresh machine (Mac Mini after `git pull`, or a re-clone): run [`agents-sdk/scripts/install_tts_models.sh`](agents-sdk/scripts/install_tts_models.sh)** — installs the two new Python deps, fetches the ~340MB model + voices binaries (gitignored), and verifies SHA-256 against the tracked `CHECKSUMS.txt`. Decision record + tradeoffs at [`agents-sdk/docs/local-tts-decision-record.md`](agents-sdk/docs/local-tts-decision-record.md). Rollback at [`agents-sdk/docs/local-tts-rollback.md`](agents-sdk/docs/local-tts-rollback.md). Spotify "Sean's Research Briefings" handoff sketched at [`agents-sdk/docs/local-tts-spotify-handoff.md`](agents-sdk/docs/local-tts-spotify-handoff.md), deferred until 10+ clean pipeline runs.

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

**Active agents (9 of 18 on launchd by default; 2 opt-in disabled-by-default; 1 manual-trigger):**

| Agent | Schedule | Skills/Model | Cost/Run |
|-------|----------|---------------|----------|
| Vault Indexer | 2:00 AM daily | nomic-embed-text (Mac Mini Ollama) | $0.00 (local) |
| Vault Synthesizer | 2:30 AM daily | Qwen3-14B on MBP (intermittent — succeeds only when MBP awake; v3.14.3 retired WOL) | $0.00 (local) |
| Deep Researcher (v3.23.0) | 2:45 AM daily | LDR + SearXNG + Qwen3-14B GGUF (Q4_K_M, `qwen3-14b-research:latest` Modelfile with `/no_think` patched into TEMPLATE) via Ollama on **Mac Mini** at `localhost:5050`. Hard 900s LDR timeout — heavy compound topics (≥3 sub-questions, multi-source cross-reference, due-diligence matrices) **must** route to Gemini DR / DR Max instead. See routing rule below. | $0.00 (local) |
| Vault Critic (NEW v4.1.0) | 3:30 AM daily | Codex CLI (gpt-5.5, ChatGPT Plus) + Anti-Gravity CLI (Gemini 3.1 Pro, Google personal OAuth) via parallel subprocess shell-out; no Claude SDK in the nightly path | $0 (subscriptions absorb) |
| Daily Driver (morning) | 8:30 AM daily (v3.38.0 — was 8:45; swapped with meta-agent so the writer runs first) | daily-driver, vault-read-write + operating-model HEARTBEAT awareness (v3.16.0) | ~$0.40 (cap $0.60) |
| Meta-Agent (fleet health) | 8:45 AM daily (v3.38.0 — was 8:35; now runs *after* daily-driver, eliminating the `Daily note exists: No` race) | gemma4:e4b (Mac Mini Ollama) for domain-aware insights summary + local health checks; + schedule-recommendations context (v3.17.0) | $0.00 (local) |
| Knowledge Lint | Sunday 22:00 | Tier 1 structural Python checks (Mac Mini); Tier 2 Qwen3-14B on MBP if awake; + 3-domain SOUL context for `soul-tier-a-conflict` issue kind (v3.17.0) | $0.00 (local) |
| Flush (SessionEnd) | hook-triggered | gemma4:e4b on Mac Mini via `inbox_triage` routing for <100-msg sessions; ≥100-msg sessions attempt Qwen3-14B on MBP if awake; + 3-domain SOUL prepend (v3.17.0) | $0.00 (local) |
| Gemini Researcher (NEW, **default disabled**) | 03:30 daily (when opted in via `INSTALL_GEMINI=1`) | Gemini Deep Research / DR Max via `gemini_dr.run` | $0–7/run; capped $7 task / $10 day / $20 month |
| Job Feed (NEW v3.28.0) | 8:00–11:00 AM (7 fires) | Qwen3-14B on MBP via HybridRouter (`fallback_disabled=true`); 4 free public feeds + ~40-company ATS watchlist; SQLite + Markdown roll-up | $0.00 |
| Skill Optimizer (v3.27.0, **manual-trigger only**) | manual (`agents-sdk/agents/skill_optimizer.py`) | Opus 4.7 generation + Qwen3-14B local judge (Ollama on Mac Mini) + Sonnet 4.6 sample-check every 5 iters; autoresearch loop on a single SKILL.md | $20–145/run (cap $200) |
| Substack-Drafter (NEW v3.33.0, **default disabled**) | Thursday 18:00 weekly (when opted in via `INSTALL_SUBSTACK_DRAFTER=1`) | HybridRouter (Qwen3-14B local → Sonnet 4.6 fallback); reads writing-voice-modes SKILL.md verbatim; 5-week voice rotation (sean/sedaris/kerouac/thompson/vonnegut) | $0–0.10/run (cap $0.10) |

**Research routing rule (v3.26.3, 2026-05-06):** Heavy multi-target research belongs on Gemini DR or DR Max, **not** local LDR. There are two independent reasons, both observed in the same week:

1. **Timeout** — local LDR has a hard 900s budget. Compound prompts (≥3 sub-questions, multi-target evaluations, due-diligence matrices) routinely exceed it. Topic 1b on 2026-05-06 stalled at 90 % from t=209s → t=900s and produced no output. Same prompt completed on Gemini DR in 406s.
2. **Citation quality collapse** — even when local LDR *does* finish, Qwen3-14B on the LDR loop can't ground citations across multiple targets at once. Topic 1a on 2026-05-05 finished cleanly at 280s and produced a confidently-formatted report containing fabricated entities (`PureMCPClient`, `MCPCatalog (Central)`, `MCP ADK`), the wrong owner for MCP (`github.com/microsoft/mcp` instead of `modelcontextprotocol`), fabricated `learn.microsoft.com` docs URLs, and missed the explicit "Anthropic Agent SDK changelog since 0.1.63" deliverable. The flawed file at [`vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md`](vault/20_projects/research/2026-05-05-topic-1a-mcp-sdk-toolkit-survey-catalog-mcp-cli-mcp-bridge-m.md) is retained with a `status: superseded` frontmatter as the canonical bad-output specimen.

**Triage rule when adding to `vault/00_inbox/research-queue.md`:** if the topic compounds three or more independent investigations, drop it via the `gemini-deep-research` skill (or `gemini_dr.py --tier dr|max`) rather than the queue. The queue is for single-shape topics (one target, one question, one pattern) — those Qwen3-14B + SearXNG can ground reliably at $0.



**Process Inbox: paused 2026-04-29 (v3.17.4) pending Path B rewrite to local `gemma4:e4b`.** Cloud-Sonnet path validated as functionally working (~3 files/run) but cost-inefficient ($1.16/file vs $0/file local). Manual triage via the `process-inbox` skill in an interactive Claude Code session is the working alternative. See `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md` for full history + Path B scope.

Phase 6 (v3.14.3) shipped the knowledge compounding loop producer side: SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint. The consumer side (autoresearch feedback, D.4) was **descoped** pending upstream autoresearch harness — re-open spec in `creative-studio/16bitfit-battle-mode/docs/plans/phase6-SUPER-PLAN-2026-04-17.md` §10.1. All agents run 100% local.

**6 of the 6 agents disabled in v3.12.3** (2026-04-09) remain disabled. `process_inbox` was briefly re-enabled 2026-04-28 → 2026-04-29 (v3.17.2 / v3.17.3) but paused again on 2026-04-29 in v3.17.4 — the cloud-Sonnet path works but at ~$1.16/file is cost-prohibitive vs the planned local-`gemma4:e4b` rewrite (~$0/file). See `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md` for the full re-enable + pause cycle and Path B rewrite scope. The other 5 (`daily-driver` evening, `daily-driver` weekly, `pr-digest`, `spending-analysis`, `health-audit`, `md-to-anki`) remain disabled — see `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`. Do NOT re-enable without Sean's explicit approval.

**Key limitation:** Headless SDK agents cannot access MCP servers (Slack, Google Calendar, Gmail, etc.) — those require browser-based OAuth only available in interactive sessions. The morning agent creates the daily note skeleton; Slack/calendar data is backfilled when Sean starts an interactive session.

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

Config: `agents-sdk/config.toml`. Auth: uses `claude login` OAuth (no API key needed). Safety: max 30 turns, default $0.50/run cap (daily-driver morning bumped to $0.60 to absorb the operating-model artifact preamble). SDK version: `0.1.63` (pinned in `agents-sdk/pyproject.toml`). Morning schedule: daily-driver 08:30 writes the note, meta-agent 08:45 reports on it. Full docs: `docs/agents-sdk.md`.

## Architecture decisions (current capabilities — full history in CHANGELOG.md)

| Subsystem | What it does | Where |
|---|---|---|
| Operating-model artifacts | HEARTBEAT/USER/SOUL/schedule-recs loaded on-demand into daily-driver, meta-agent, flush, knowledge_lint (`soul-tier-a-conflict` issue kind, HIGH). Toggle `[artifacts]` in `config.toml`. | [`agents-sdk/lib/artifact_loader.py`](agents-sdk/lib/artifact_loader.py) |
| Knowledge loop (producer) | SessionEnd flush → 02:30 synthesizer → 03:30 vault_critic → Sunday lint | see Active agents table above |
| Knowledge loop (consumer) | SessionStart hook injects `vault/knowledge/index.md` as additionalContext (15K cap, 5s timeout) | [`.claude/hooks/session-start-inject-index.sh`](.claude/hooks/session-start-inject-index.sh) |
| PreCompact safety net | Fires `flush.py --trigger pre-compact` before context auto-compaction (`tag:` field in daily-log distinguishes flush types) | [`.claude/hooks/pre-compact-flush.sh`](.claude/hooks/pre-compact-flush.sh) |
| Vault Synthesizer | T1 quote-first prompt + cross-domain preference, T1.5 `evaluate_article_depth()` gate with `rejected_reasons` in manifest, T2 HDBSCAN cluster-and-sample retrieval. T3 (EDC canonicalization) deferred; T4 (three-pass) post-employment. | [`agents-sdk/agents/vault_synthesizer.py`](agents-sdk/agents/vault_synthesizer.py), [`lib/retrieval_diversity.py`](agents-sdk/lib/retrieval_diversity.py). Plan: [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md) |
| Vault Critic | Codex CLI + Anti-Gravity CLI parallel critique per concept → `vault/knowledge/expansions/{slug}.md`. $0 incremental, 600s wall-clock budget, 120s per-CLI; both-rate-capped → `status: partial`. Per-run manifest at `vault/health/critic-manifest-{date}.json`. | [`agents-sdk/agents/vault_critic.py`](agents-sdk/agents/vault_critic.py); plan [`agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`](agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md) |
| Concept edges | SQLite table (6 relations: supports/contradicts/evolved_into/supersedes/depends_on/related_to); knowledge_lint Tier 2 queries active contradictions via SQL fast path | `vault/.vault-index.db`; [`agents-sdk/lib/concept_edges.py`](agents-sdk/lib/concept_edges.py) |
| Daily note as fleet console | Overnight digest injected at `<!-- fleet-overnight -->` anchor; Dataview blocks auto-surface today's new concepts/connections/research + latest lint report | [`agents-sdk/lib/fleet_summary.py`](agents-sdk/lib/fleet_summary.py), [`vault/90_system/templates/tpl-daily.md`](vault/90_system/templates/tpl-daily.md) |
| Knowledge Q&A tier | Two-pass orchestration against `vault/knowledge/index.md`; `--file-back` persists to `vault/knowledge/qa/<slug>.md` with chunk_id provenance and append-only JSONL manifest | [`agents-sdk/scripts/query.py`](agents-sdk/scripts/query.py) |
| Auto-stub people | SessionEnd hook auto-creates `vault/40_knowledge/people/<slug>.md` from new `author:` wikilinks (structured-signal filter, 1-3 capitalized tokens, 10/run cap) | [`.claude/hooks/session-end-auto-stub.sh`](.claude/hooks/session-end-auto-stub.sh), [`agents-sdk/scripts/auto_stub_people.py`](agents-sdk/scripts/auto_stub_people.py) |
| Knowledge Lint scope | Excludes `[[NNN]]` citation markers + `node_modules` + archived `the-block-meetings-granola-notes`; vault sits at 0 broken wikilinks | [`agents-sdk/agents/knowledge_lint.py`](agents-sdk/agents/knowledge_lint.py) |

**launchd requirement:** All plists must include `EnvironmentVariables` with `PATH` set to `/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Without this, the `claude` CLI is not discoverable and agents fail with `CLIConnectionError`. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`.

## Architecture

```
.claude/
├── skills/          # ALL 119 skills (canonical, auto-loaded)
├── agents/          # ALL 13 agents (8 domain + 5 design team) — Claude Code subagents, separate from the 14 SDK agents
├── hooks/           # 14 hooks (block-secrets, cost-watchdog, daily-note-appender,
│                    #           format-on-edit, log-tool-use, loop-detector,
│                    #           network-access-control, pre-compact-flush,
│                    #           require-confirm-highrisk, run-tests-on-stop,
│                    #           session-end-auto-stub, session-end-flush,
│                    #           session-start-inject-index, vault-integrity)
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
└── product-management/               # nested workspace (moved from root in v3.15.0)

creative-studio/                      # DOMAIN 2 — creative work
├── CLAUDE.md
├── README.md
├── 16bitfit-battle-mode/             # nested project (moved from root in v3.15.0)
├── design-team/                      # nested workspace (moved from root in v3.15.0)
└── (existing finance/, scripts/, templates/)

life-systems/                         # DOMAIN 3 — personal systems
├── CLAUDE.md
├── README.md
└── (existing reference/)

claude-mastery/      # cross-cutting Claude Code meta-reference (stays at root)
tools/                                # NEW v3.35.0 — sidecar tools (non-skill, non-agent)
└── llm-council/                      # Multi-vendor LLM council (inspired by karpathy/llm-council)
    ├── upstream/                     # Karpathy's reference web app, unmodified
    └── council/                      # Headless CLI used by .claude/skills/llm-council/
evals/
└── vault-synthesizer/   # NEW v3.30.1 — 10-case eval suite for the nightly synthesizer
vault/               # Obsidian vault (PARA + MOCs + operating-models + Prompts + RAG)
export-groups/       # Metadata-only manifests (for installer export)
shared/hooks/        # Hook source files (for installer)
shared/security/     # Security profiles (standard, enterprise)
presets/             # Export presets (starter, power, enterprise, creative)
scripts/             # install.sh, install.ps1, validate.py
plugin/              # Marketplace distribution
docs/                # Ecosystem documentation
```

## Non-Negotiable Rules

1. **Plan Mode vs Extended Thinking**: Plan Mode = double `Shift+Tab` or `/plan`. Extended Thinking = single `Tab`. Never confuse the two.
2. **Agent tool restrictions**: Use `disallowedTools` (deny-list), not allow-list.
3. **Hooks enforce; subagents judge**: PreToolUse for binary allow/deny; subagents for subjective reviews.
4. **Hook blocking**: Exit code **2** to deny (not 0 or 1).
5. **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
6. **Permission evaluation** (first match wins): Deny > Ask > Allow
7. **3-domain structure (v3.15.0)**: `the-block/`, `creative-studio/`, `life-systems/` are the only workspace folders that house domain-specific content. `product-management/` lives nested inside `the-block/`; `design-team/` and `16bitfit-battle-mode/` live nested inside `creative-studio/`. The prior rule that `product-management/` stayed at the root is **explicitly waived as of v3.15.0**.
8. **Vault sync owner (issue #22, 2026-04-23)**: The shell-level auto-commit hook is the **sole** owner of vault git operations. Obsidian-Git plugin auto-features (backup interval, auto-pull, auto-push, commit-on-change) must stay disabled on every machine — do not re-enable them. Running two auto-commit systems against the same vault caused the v3.15.0 merge conflicts. Obsidian-Git can be used for manual commits from the command palette if desired; it must never run automatically.

## Hook Exit Codes

- `0` = Allow
- `1` = Error (logged, operation allowed)
- `2` = **Deny** (blocks the operation)

## When Modifying

- Run `python3 scripts/validate.py` after changes (v3.15.0: validator hard-enforces the 3 primary domain folders)
- Skills live in `.claude/skills/` (not export-groups)
- Agents live in `.claude/agents/` (not shared/agents/)
- Update `export-groups/*/playground.json` manifests when adding/removing skills
- New domain-specific content goes inside the correct domain folder (`the-block/`, `creative-studio/`, or `life-systems/`)
- **Mandatory doc updates**: When creating a new Skill, Agent, Sub-Agent, Hook, or Script, you MUST update all three of these files:
  - `CHANGELOG.md` — Add entry under the current version's Added section
  - `CLAUDE.md` — Update counts (skill/agent/hook totals, domain table, architecture comment)
  - `README.md` — Update counts and any affected tables
