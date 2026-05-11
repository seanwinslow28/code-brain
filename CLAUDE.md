# CLAUDE.md

This is Sean's personal command center — a second brain for Claude Code.

## What This Repo Is

117 skills, 13 Claude Code subagents, 13 hooks, 14 autonomous SDK agents (7 active), **3 primary domain folders** + cross-cutting infrastructure, an Obsidian vault, and an Agent SDK layer for autonomous operation. Everything is active and auto-loaded. The installer exports subsets to other projects.

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

**Gemini Deep Research** is available via `agents-sdk/scripts/gemini_dr.py` (wrapping the `google-genai` SDK) and the `.claude/skills/gemini-deep-research` skill. The API key is stored in macOS Keychain as `com.sean.agents.gemini_api_key`. Use the `gemini-deep-research` skill to decide when to delegate to Gemini DR vs. run a local LDR query. Cost is self-policing: $7 per-task hard cap, $10 per-day circuit breaker, $20 per-month governor — tracked in `vault/health/gemini-spend-{YYYY-MM}.json`. The autonomous agent (`gemini_researcher.py`) is default disabled; opt in with `INSTALL_GEMINI=1` when running `install_schedules.sh`.

## Commands

```bash
# Validate everything
python3 scripts/validate.py

# Export skills to another project
./scripts/install.sh /path/to/project --preset starter|power|enterprise|creative
./scripts/install.sh /path/to/project pm-workflows remotion-mastery
./scripts/install.sh --list
```

## Agents SDK (Autonomous Layer)

The `agents-sdk/` directory adds scheduled, autonomous agents powered by the Claude Agent SDK. These run **outside** Claude Code sessions on macOS launchd schedules. Skills are loaded as system prompts — no duplication.

**Active agents (8 of 15):**

| Agent | Schedule | Skills/Model | Cost/Run |
|-------|----------|---------------|----------|
| Vault Indexer | 2:00 AM daily | nomic-embed-text (Mac Mini Ollama) | $0.00 (local) |
| Vault Synthesizer | 2:30 AM daily | Qwen3-14B on MBP (intermittent — succeeds only when MBP awake; v3.14.3 retired WOL) | $0.00 (local) |
| Deep Researcher (v3.23.0) | 2:45 AM daily | LDR + SearXNG + Qwen3-14B GGUF (Q4_K_M, `qwen3-14b-research:latest` Modelfile with `/no_think` patched into TEMPLATE) via Ollama on **Mac Mini** at `localhost:5050`. Hard 900s LDR timeout — heavy compound topics (≥3 sub-questions, multi-source cross-reference, due-diligence matrices) **must** route to Gemini DR / DR Max instead. See routing rule below. | $0.00 (local) |
| Meta-Agent (fleet health) | 8:35 AM daily | gemma4:e4b (Mac Mini Ollama) for domain-aware insights summary + local health checks; + schedule-recommendations context (v3.17.0) | $0.00 (local) |
| Daily Driver (morning) | 8:45 AM daily | daily-driver, vault-read-write + operating-model HEARTBEAT awareness (v3.16.0) | ~$0.40 (cap $0.60) |
| Knowledge Lint | Sunday 22:00 | Tier 1 structural Python checks (Mac Mini); Tier 2 Qwen3-14B on MBP if awake; + 3-domain SOUL context for `soul-tier-a-conflict` issue kind (v3.17.0) | $0.00 (local) |
| Flush (SessionEnd) | hook-triggered | gemma4:e4b on Mac Mini via `inbox_triage` routing for <100-msg sessions; ≥100-msg sessions attempt Qwen3-14B on MBP if awake; + 3-domain SOUL prepend (v3.17.0) | $0.00 (local) |
| Gemini Researcher (NEW, **default disabled**) | 03:30 daily (when opted in via `INSTALL_GEMINI=1`) | Gemini Deep Research / DR Max via `gemini_dr.run` | $0–7/run; capped $7 task / $10 day / $20 month |
| Job Feed (NEW v3.28.0) | 8:00–11:00 AM (7 fires) | Qwen3-14B on MBP via HybridRouter (`fallback_disabled=true`); 4 free public feeds + ~40-company ATS watchlist; SQLite + Markdown roll-up | $0.00 |

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

Config: `agents-sdk/config.toml`. Auth: uses `claude login` OAuth (no API key needed). Safety: max 30 turns, default $0.50/run cap (daily-driver morning bumped to $0.60 in v3.16.0 to absorb the operating-model artifact preamble). SDK version: `0.1.63` (pinned in `agents-sdk/pyproject.toml` as of v3.15.0). Morning schedule: 8:45 AM (was 6:00 AM as of v3.12.2). Full docs: `docs/agents-sdk.md`.

**Operating-model artifact wiring (v3.16.0 Phase 1 + v3.17.0 Phase 2):** `agents-sdk/lib/artifact_loader.py` reads `vault/05_atlas/operating-models/{domain}/{kind}.md` artifacts on-demand with mtime-keyed caching. Daily-driver morning mode injects all three HEARTBEATs into the preamble plus on-demand Read pointers for USER / SOUL / operating-model / schedule-recommendations (Phase 1). Phase 2 wires three more agents — all local-only, no cloud egress: `meta_agent` calls gemma4:e4b on Mac Mini with all three `schedule-recommendations.md` bodies to produce a "Domain-Aware Insights" section ranking fleet activity against Sean's Protect / Automate / Decline lists; `flush.py` prepends all three domain SOULs to its `EXTRACTION_PROMPT` so the local model can cross-reference new entries against Tier-A items; `knowledge_lint.py` Tier-2 prompt gains a 3-domain SOUL context block plus a new `soul-tier-a-conflict` `LintIssue` kind at HIGH severity. Controlled by `[artifacts]` in `config.toml`; instant rollback = `enabled = false`. Phase 3 was closed 2026-04-27: `meeting_defender` deleted (Daily Driver morning already covers calendar surfacing); `sprint_health` autonomous wiring superseded by the new `sprint-health` skill (ad-hoc Block Jira status checks via interactive Atlassian MCP, no headless-MCP gymnastics required).

**Knowledge-loop consumer activation (Phase B, 2026-04-25):** The `.claude/hooks/session-start-inject-index.sh` SessionStart hook reads `vault/knowledge/index.md` and injects it as `additionalContext` on every new Claude Code session, so Claude opens each session knowing the vault's concept and connection articles before you type anything. File-read-only, 5-second timeout, 15,000-char cap. Controlled by `[knowledge_index]` in `agents-sdk/config.toml`; instant rollback = remove the SessionStart block from `.claude/settings.json`. This pairs with the producer side (Phase 6 SessionEnd flush → nightly synthesizer → weekly knowledge_lint) to close the consumer loop.

**Knowledge-loop Phase A — PreCompact safety net (v3.18.0, 2026-05-01):** The `.claude/hooks/pre-compact-flush.sh` hook fires before Claude Code auto-compacts a long session, spawning `flush.py --trigger pre-compact` so pre-compact knowledge isn't silently lost. `flush.py` gained `--trigger {session-end,pre-compact,manual}` (default `session-end`); the value flows into the daily-log session block's `tag:` field, replacing the prior `tag: auto` so post-hoc analysis can distinguish flush types. Hook count `12 → 13`. Rollback = remove the `PreCompact` block from `.claude/settings.json`.

**Knowledge-loop Phase D — typed reasoning edges + synthesizer manifest (v3.20.0, 2026-05-01):** Promotes contradiction / supersedence detection from "Sunday LLM lint scan that prose-writes findings to a report" to "queryable SQL row at synthesis time." `vault_indexer.init_db()` gained a `concept_edges` SQLite table (idempotent `CREATE TABLE IF NOT EXISTS`) with six allowed relation values (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`) — taxonomy mirrors OB1's [`schemas/typed-reasoning-edges/schema.sql`](https://github.com/NateBJones-Projects/OB1/blob/main/schemas/typed-reasoning-edges/schema.sql), SQLite-local. `vault_synthesizer.py`'s LLM prompt asks for an OPTIONAL `relations` array per connection (same call, richer parsing); the synthesizer parses each pair and `INSERT OR IGNORE`s a row inside the existing FileLock window. Bad relation values are logged + dropped via the new `agents-sdk/lib/concept_edges.py` helper (`insert_edge` raises `ValueError` so the article still writes). `knowledge_lint.py` Tier 2 gains a SQL fast path against `concept_edges` for `relation='contradicts' AND valid_until IS NULL` — third touch on this file (Phase 2 added soul-tier-a-conflict, Phase C added qa/ to `_ORPHAN_EXCLUDE_DIRS`, Phase D adds the SQL path). LLM and SQL contradictions are deduped by normalized `frozenset({from_slug, to_slug})`; SQL hits win when both surface the same pair. SOUL conflict detection (Phase 2 capability with no SQL substitute) is preserved unchanged across the dedupe boundary. `vault/health/synth-manifest-{date}.json` (NEW) captures per-run counts (concepts, connections, edges, rejected, duration, model, wol_status) and `daily_driver.py` morning brief surfaces them under Vault Health (second touch on this file: Phase 1 of agent-wiring added the artifact preamble, Phase D adds the synth line). Empty-vault verification chosen via pure unit tests (mocked LLM emits `relations`, in-memory SQLite verifies edge rows) — full pytest suite 204 → 241 (+37). Rollback = `DROP TABLE concept_edges` + revert the four MODIFY files; LLM still writes connection articles unchanged because `relations` is OPTIONAL in the prompt schema.

**Knowledge-loop Phase C — query.py + qa/ tier + OB1 provenance (v3.19.0, 2026-05-01):** `agents-sdk/scripts/query.py` adds terminal Q&A against `vault/knowledge/index.md` with two-pass orchestration: a selection pass picks 3-N article paths with similarity scores; an answer pass reads the selected bodies and emits a `[[wikilink]]`-citing answer. Local-first model routing via HybridRouter (`vault_synthesis` task → Qwen3-14B on MBP) with Anthropic Sonnet 4.6 fallback. `--file-back` persists answers as a third article tier at `vault/knowledge/qa/<slug>.md` and appends one JSONL record per run to `vault/knowledge/qa/.manifest.json`. Two OB1-inspired adds per the 2026-04-25 architectural review verdict: (C.M1) the qa/ frontmatter cites each consulted article with a 12-char SHA-256 chunk_id over `(file_path, chunk_index)` from `vault/.vault-index.db`'s `chunks` table plus the selection-pass similarity score, giving the synthesizer a cheap "did this specific chunk change?" check; (C.M2) the manifest is append-only JSONL matching the `lib/logging_setup.py:record_run` pattern. `vault_synthesizer.regenerate_index` learned a `## Q&A` section so qa/ articles surface in the SessionStart-injected index alongside concepts/connections. `knowledge_lint._ORPHAN_EXCLUDE_DIRS` gained `qa` because qa/ articles are answer endpoints (cite outward, never receive inbound wikilinks). Empty-state path (current live state — empty index until the synthesizer fires on an awake MBP) is explicit: zero candidates, no LLM call, no qa file written, exit 0. Rollback = delete `scripts/query.py` and revert the qa/ entries in `regenerate_index` + `_ORPHAN_EXCLUDE_DIRS`.

**launchd requirement:** All plists must include `EnvironmentVariables` with `PATH` set to `/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Without this, the `claude` CLI is not discoverable and agents fail with `CLIConnectionError`. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`.

## Architecture

```
.claude/
├── skills/          # ALL 117 skills (canonical, auto-loaded)
├── agents/          # ALL 13 agents (8 domain + 5 design team) — Claude Code subagents, separate from the 14 SDK agents
├── hooks/           # 13 hooks (block-secrets, cost-watchdog, daily-note-appender,
│                    #           format-on-edit, log-tool-use, loop-detector,
│                    #           network-access-control, pre-compact-flush,
│                    #           require-confirm-highrisk, run-tests-on-stop,
│                    #           session-end-flush, session-start-inject-index,
│                    #           vault-integrity)
└── settings.json    # Standard security profile

agents-sdk/          # Autonomous agents (Claude Agent SDK, Python)
├── agents/          # Agent scripts (daily_driver.py + scheduled launchd agents)
├── lib/             # Shared modules (config, skill loader, artifact loader, vault I/O, logging)
├── schedules/       # launchd plists + installer
├── tests/           # pytest suite
└── config.toml      # Agent config, paths, safety limits

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
