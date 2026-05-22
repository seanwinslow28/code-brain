# CLAUDE.md

This is Code-Brain — Sean's personal command center, a second brain built on Claude Code.

## What This Repo Is

118 skills, 13 Claude Code subagents, 14 hooks, 18 autonomous SDK agents (9 active on launchd, 2 opt-in disabled-by-default, 1 manual-trigger), **3 primary domain folders** + cross-cutting infrastructure, an Obsidian vault, and an Agent SDK layer for autonomous operation. Everything is active and auto-loaded. The installer exports subsets to other projects.

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

Config: `agents-sdk/config.toml`. Auth: uses `claude login` OAuth (no API key needed). Safety: max 30 turns, default $0.50/run cap (daily-driver morning bumped to $0.60 in v3.16.0 to absorb the operating-model artifact preamble). SDK version: `0.1.63` (pinned in `agents-sdk/pyproject.toml` as of v3.15.0). Morning schedule: 8:45 AM (was 6:00 AM as of v3.12.2). Full docs: `docs/agents-sdk.md`.

**Operating-model artifact wiring (v3.16.0 Phase 1 + v3.17.0 Phase 2):** `agents-sdk/lib/artifact_loader.py` reads `vault/05_atlas/operating-models/{domain}/{kind}.md` artifacts on-demand with mtime-keyed caching. Daily-driver morning mode injects all three HEARTBEATs into the preamble plus on-demand Read pointers for USER / SOUL / operating-model / schedule-recommendations (Phase 1). Phase 2 wires three more agents — all local-only, no cloud egress: `meta_agent` calls gemma4:e4b on Mac Mini with all three `schedule-recommendations.md` bodies to produce a "Domain-Aware Insights" section ranking fleet activity against Sean's Protect / Automate / Decline lists; `flush.py` prepends all three domain SOULs to its `EXTRACTION_PROMPT` so the local model can cross-reference new entries against Tier-A items; `knowledge_lint.py` Tier-2 prompt gains a 3-domain SOUL context block plus a new `soul-tier-a-conflict` `LintIssue` kind at HIGH severity. Controlled by `[artifacts]` in `config.toml`; instant rollback = `enabled = false`. Phase 3 was closed 2026-04-27: `meeting_defender` deleted (Daily Driver morning already covers calendar surfacing); `sprint_health` autonomous wiring superseded by the new `sprint-health` skill (ad-hoc Block Jira status checks via interactive Atlassian MCP, no headless-MCP gymnastics required).

**Knowledge-loop consumer activation (Phase B, 2026-04-25):** The `.claude/hooks/session-start-inject-index.sh` SessionStart hook reads `vault/knowledge/index.md` and injects it as `additionalContext` on every new Claude Code session, so Claude opens each session knowing the vault's concept and connection articles before you type anything. File-read-only, 5-second timeout, 15,000-char cap. Controlled by `[knowledge_index]` in `agents-sdk/config.toml`; instant rollback = remove the SessionStart block from `.claude/settings.json`. This pairs with the producer side (Phase 6 SessionEnd flush → nightly synthesizer → weekly knowledge_lint) to close the consumer loop.

**Knowledge-loop Phase A — PreCompact safety net (v3.18.0, 2026-05-01):** The `.claude/hooks/pre-compact-flush.sh` hook fires before Claude Code auto-compacts a long session, spawning `flush.py --trigger pre-compact` so pre-compact knowledge isn't silently lost. `flush.py` gained `--trigger {session-end,pre-compact,manual}` (default `session-end`); the value flows into the daily-log session block's `tag:` field, replacing the prior `tag: auto` so post-hoc analysis can distinguish flush types. Hook count `12 → 13`. Rollback = remove the `PreCompact` block from `.claude/settings.json`.

**Vault Synthesizer Tier-1.5 retrofit — insight-depth gate + prompt v2 (v3.38.0, 2026-05-20):** Born from Sean's 2026-05-20 review surfacing the "I'm not getting a thinking partner" complaint. Tier 2 retrieval was healthy (3 consecutive nights of `clusters_sampled ≥ 3`: 5/18=38, 5/19=56, 5/20=37) but `vault/knowledge/concepts/automation-routines.md` (written 5/19) revealed the median article was still structurally shallow — CLI-snippet "evidence", restatement-shape definitions ("a collection of automated processes designed to support Sean's job-hunting efforts"), missing `## Threads` substance, casual one-liner implications. Prior Verification Log spot-checks were cherry-picks of each night's best output, not the median. Tier 1.5 adds three structural pieces: (1) a new `evaluate_article_depth(body) -> (passed, reason)` semantic gate alongside `validate_article_body` — concept articles must have Definition ≥3 sentences AND ≥250 chars AND no restatement-tell phrases (collected from real bad output: "a collection of …", "designed to support …", "streamlines his workflow", "ensures consistency", "is a process for …", "this would benefit Sean"), Evidence ≥2 prose quotes each ≥60 chars not classified as CLI/code by `_is_code_or_cli_quote` (prefix-match + symbol-density >30% — replaced an earlier verb-marker heuristic that false-positived on prose like "RIFE controls how the model bridges keyframes"), and Examples can't 100%-duplicate Evidence; connection articles must have Synthesis ≥3 sentences AND ≥200 chars naming a *tension* + *consequence* (not "Three producers share an MBP dependency"-shape descriptions), each per-concept thread has ≥1 substantive ≥60-char prose quote, and ≥2 implications each ≥80 chars. (2) Prompt v2 — Definition demands the *mechanism* not the surface description with a worked GOOD vs BAD example block (the bad example paraphrases the actual 5/19 `automation-routines.md` shape), Synthesis demands the cross-domain tension + consequence, explicit "REJECTED-SHAPE EXAMPLES" anti-pattern block, explicit OMIT-when-thin instruction. (3) Skip-thin-source path — when the diversified pool returns `< _MIN_SIMILAR_FOR_LLM` (default 2) chunks, the LLM call is skipped entirely; `result.skipped_thin_source` surfaces in manifest. Two new `SynthesisResult` fields (`rejected_reasons: dict[str,int]` keyed by stable reason codes `thin-definition`/`restatement-definition`/`thin-evidence`/`code-only-evidence`/`duplicate-examples`/`thin-synthesis`/`thin-threads`/`thin-implications`/`wikilinks-or-placeholder` + `skipped_thin_source: int`) persisted by `write_synth_manifest` give the daily-driver brief operator-grade signal about *why* output volume changed night to night. **Test coverage:** 12 new tests in `test_vault_synthesizer.py`; synthesizer suite 27 → 28; synthesizer-neighborhood (synthesizer + retrieval-diversity + concept-edges + knowledge-lint + synth-manifest) **91 passed, 0 regressions**. Existing happy-path + Phase-D fixtures rewritten to use production-shape content. **Tier 3 (EDC canonicalization) is now formally deferred** — slug-dedup trigger doesn't fire (96 concepts after 3 Tier-2-live nights with ~71 attempted writes = strong reuse signal; pre-existing dupe groups flat at 5/17 baseline) and the real defect is insight-depth, which EDC cosine-merge wouldn't touch. **First production signal arrives at 2026-05-21 02:30 AM**; verification gate is (a) `synth-manifest-2026-05-21.json` carries non-zero `rejected_reasons` (validator gating, not silent-passing) AND (b) Sean reads ≥2 randomly sampled articles from 5/21's output and confirms thinking-partner shape. Rollback: `git checkout agents-sdk/agents/vault_synthesizer.py agents-sdk/tests/test_vault_synthesizer.py` — pure text + test changes, no new deps, no schema migrations. Plan + Status Tracker: [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md) §Tier 1.5.

**Vault Critic — generative critique layer (NEW v4.1.0, 2026-05-21):** Born from Sean's 2026-05-21 review surfacing the next-tier complaint after Tier 1.5 landed: the synthesizer describes what exists but can't tell him what's missing. Pure-Python orchestration agent at [`agents-sdk/agents/vault_critic.py`](agents-sdk/agents/vault_critic.py) that runs on launchd at 03:30 daily (after vault_synthesizer 02:30, deep_researcher 02:45, before daily-driver 08:30 and meta-agent 08:45). Reads today's Mac-Mini-canonical synth-manifest (PR-contamination-filtered per [`feedback_synth_verify_filter_to_manifest.md`](.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_filter_to_manifest.md)), selects up to 3 newly-written concept articles, and for each fans out two parallel subprocess critiques — Codex CLI (gpt-5.5 with `--sandbox read-only --skip-git-repo-check`, cwd=$HOME) and Anti-Gravity CLI (Gemini 3.1 Pro with `--output-format json --approval-mode plan`, `GEMINI_CLI_TRUST_WORKSPACE=true` set explicitly per invocation). Writes sibling expansion files at `vault/knowledge/expansions/{slug}.md` naming 3 specific things Sean is missing with named-author + named-work + sentence-pattern + genre-unlock specificity. First live smoke fire on 2026-05-21 14:46 produced [`vault/knowledge/expansions/writing-voice-modes.md`](vault/knowledge/expansions/writing-voice-modes.md) — Codex named Janet Malcolm (Forensic Plainstyle), Annie Dillard (Procedural Voice), and Raymond Queneau (Constraint-Based Anti-Voice), none of which appear in the synthesizer-described article. Per-run manifest at `vault/health/critic-manifest-{date}.json`. Cost: $0 incremental on existing personal subscriptions; no Anthropic SDK calls in the nightly path. Sonnet fallback is **out of scope for v1** — both-CLIs-rate-capped marks the run `status: partial` and exits cleanly, isolating Pattern 1 from any cloud-API blast radius. Wall-clock budget: 600s soft cap; per-CLI timeout: 120s. First-fire status was `partial` because Anti-Gravity hit the 120s timeout (Codex succeeded with 18,344 tokens) — the graceful-partial behavior the plan's Risk #1 anticipated. Surfaces in daily-driver morning brief under Vault Health + in meta-agent fleet overnight digest + in vault `02_Areas/Agent-Fleet/` snapshots. Patterns 2 (zero-cost LLM council profile) and 3 (HybridRouter CLI routing) are deferred per [`agents-sdk/docs/multi-cli-integration-patterns.md`](agents-sdk/docs/multi-cli-integration-patterns.md). Rollback: `./agents-sdk/schedules/install_schedules.sh --remove` + set `[agents.vault_critic].enabled = false` in `config.toml`; existing expansion files preserved. Plan + Status Tracker: [`agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md`](agents-sdk/docs/plans/vault-critic-plan-2026-05-21.md).

**Morning schedule swap — daily-driver 8:30 / meta-agent 8:45 (v3.38.0, 2026-05-20):** The prior order (meta-agent 8:35, daily-driver 8:45) caused a race: meta-agent's `Daily note exists` check ran 10 minutes *before* daily-driver wrote the day's note, so the fleet-status report routinely surfaced "Daily note exists: No · status=error" while the underlying agent was healthy. Swapped per Sean's 2026-05-20 direction. Daily-driver now writes first at 08:30, meta-agent reports on the fresh state at 08:45. Both plists updated under `agents-sdk/schedules/`, symlinks at `~/Library/LaunchAgents/` already point at the repo plists, reload via `launchctl bootout && launchctl bootstrap`. Verified live via `launchctl print`.

**Vault Synthesizer Tier-2 retrofit — cluster-and-sample retrieval (v3.37.0, 2026-05-16):** Shipped after three nights of Tier 1 produced a clean signal (formatter fix confirmed live in 5/14 and 5/16 output, validator actively rejecting placeholder articles at the write boundary, 5/15 error explainable as expected NY-trip MBP-offline state) but a 2026-05-16 cluster-diversity diagnostic via [`agents-sdk/scripts/query.py`](agents-sdk/scripts/query.py) proved the remaining bias was retrieval-level: 7 of 9 consulted chunks still came from the densest concept region (agent-health / agent-fleet / automation-reliability) even when the prompt explicitly asked for career-cluster + creative-cluster chunks. Tier 2 attacks the bias structurally per the TopClustRAG pattern ([SIGIR 2025](https://arxiv.org/html/2506.15246v1)). New module [`agents-sdk/lib/retrieval_diversity.py`](agents-sdk/lib/retrieval_diversity.py) exports `cluster_and_sample(embeddings, ...) -> DiversifiedPool` (HDBSCAN with `min_cluster_size=3`, euclidean metric, ≤2 per cluster + ≤3 noise points, max 15 total; graceful fall-back when hdbscan unavailable / pool too small / <2 real clusters / degenerate input — every fall-back returns the top-N slice by input rank with `fell_back=True` set) and `build_embedding_query(primary_text)` (H1/H2 headings + first non-list paragraph + frontmatter `type`/`tags` for both inline `[a, b]` and YAML-block forms — replaces the v1 `primary_text[:2000]` slice that biased toward "files that begin similarly" rather than "files about similar things"). [`agents-sdk/agents/vault_indexer.py::search()`](agents-sdk/agents/vault_indexer.py) gained keyword-only `include_embeddings: bool = False`; when True each result dict carries the stored embedding under `"embedding"` so the synthesizer can cluster the pool. [`vault_synthesizer.py`](agents-sdk/agents/vault_synthesizer.py)'s retrieval block now (1) builds the query via `build_embedding_query`, (2) retrieves `RETRIEVAL_POOL_SIZE = 50` chunks with `include_embeddings=True`, (3) calls `cluster_and_sample` to diversify and accumulates `clusters_found` into the new `SynthesisResult.clusters_sampled` field that surfaces in the synth-manifest JSON, (4) strips the `embedding` field from chunks before passing them to the prompt builder so 50 × 768-dim vectors don't balloon the LLM context budget. Includes a `TypeError` guard for backward-compat with legacy test-mock retrievers that don't accept `include_embeddings`. `pyproject.toml` adds `hdbscan>=0.8.40,<0.9` (pulls scikit-learn / scipy / joblib / threadpoolctl, ~30MB, installs in ~10s on macOS arm64). **14 new tests** in [`agents-sdk/tests/test_retrieval_diversity.py`](agents-sdk/tests/test_retrieval_diversity.py) covering the contract end-to-end; synthesizer-neighborhood suite stays green at **76 passed** with zero regressions; full pytest suite **550 passed** (3 pre-existing failures unrelated to Tier 2: `test_doc_to_audio_cli` missing `soundfile`, `test_job_feed_e2e`, `test_route_to_macbook` — confirmed pre-existing on `main` via `git stash` round-trip). First production signal arrives at the **2026-05-17 02:30 AM nightly synth run** — verification gate is `clusters_sampled ≥ 3` in `vault/health/synth-manifest-2026-05-17.json`. Tier 3 (EDC canonicalization at >0.85 cosine) remains gated behind Tier 2 stability + continued slug-duplication signal; Tier 4 (three-pass agentic synthesis) post-employment only. Plan + Verification Log + Status Tracker: [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md). Rollback = `git checkout agents-sdk/agents/vault_indexer.py agents-sdk/agents/vault_synthesizer.py agents-sdk/pyproject.toml && rm agents-sdk/lib/retrieval_diversity.py agents-sdk/tests/test_retrieval_diversity.py` + `pip uninstall hdbscan` (the indexer's `include_embeddings` kwarg is the only schema-adjacent change and is backward compatible — legacy callers ignore the new field).

**Vault Synthesizer Tier-1 retrofit — quote-first prompt + canonicalization + cross-domain preference (v3.34.0, 2026-05-13):** Born from a 2026-05-13 diagnostic session where `scripts/query.py` proved the post-v3.33.0 synthesizer was producing shallow, cluster-biased, duplicate-prone output even though the eval suite passed 7/10. Root-cause read of `vault_synthesizer.py` surfaced a structural defect: [`format_connection_article`](agents-sdk/agents/vault_synthesizer.py#L174) hardcoded `"Evidence pending."` in every per-concept thread — the LLM was never asked for evidence, and the formatter discarded any it might have provided. Tier 1 of a four-tier retrofit plan replaces that with three steering rules baked into the LLM prompt: **evidence-first** (every claim grounded in a verbatim quote, no quote → no claim), **reuse > remint** (existing concept titles loaded once per run via the new `_load_existing_concept_titles()` helper and injected verbatim into the prompt so the LLM reuses canonical slugs rather than minting near-duplicates like `daily-drive-agent` vs `daily-driver-agent`), and **cross-domain > within-domain** (connections preferring concepts whose source files span different top-level vault folders — the new `_CROSS_DOMAIN_FOLDERS` tuple). Both formatters gained optional `evidence` parameters; `validate_article_body` gained the new `_FORBIDDEN_PLACEHOLDERS` rejection (catches `"Evidence pending"` and `"(to be filled)"` as defense in depth). Chunk excerpts grew 200 → 800 chars so the LLM sees arguments, not fragments. **62 tests pass across the synthesizer's neighborhood** (vault_synthesizer + synth_manifest + concept_edges + knowledge_lint suites); eval suite stays at 7/10 (same baseline). Pure text changes — no new dependencies, no schema changes, no config changes. Tiers 2-4 are specced + gated behind the Status Tracker in the retrofit plan: Tier 2 = cluster-and-sample retrieval (TopClustRAG, adds `hdbscan` dep), Tier 3 = EDC canonicalization (pre-write cosine-merge at >0.85), Tier 4 = three-pass agentic synthesis (post-employment only). First real signal arrives at the 2026-05-14 02:30 AM nightly run. Full plan + intent spec + Status Tracker: [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md`](vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md). Rollback = `git checkout agents-sdk/agents/vault_synthesizer.py`.

**Knowledge-loop Phase D — typed reasoning edges + synthesizer manifest (v3.20.0, 2026-05-01):** Promotes contradiction / supersedence detection from "Sunday LLM lint scan that prose-writes findings to a report" to "queryable SQL row at synthesis time." `vault_indexer.init_db()` gained a `concept_edges` SQLite table (idempotent `CREATE TABLE IF NOT EXISTS`) with six allowed relation values (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`) — taxonomy mirrors OB1's [`schemas/typed-reasoning-edges/schema.sql`](https://github.com/NateBJones-Projects/OB1/blob/main/schemas/typed-reasoning-edges/schema.sql), SQLite-local. `vault_synthesizer.py`'s LLM prompt asks for an OPTIONAL `relations` array per connection (same call, richer parsing); the synthesizer parses each pair and `INSERT OR IGNORE`s a row inside the existing FileLock window. Bad relation values are logged + dropped via the new `agents-sdk/lib/concept_edges.py` helper (`insert_edge` raises `ValueError` so the article still writes). `knowledge_lint.py` Tier 2 gains a SQL fast path against `concept_edges` for `relation='contradicts' AND valid_until IS NULL` — third touch on this file (Phase 2 added soul-tier-a-conflict, Phase C added qa/ to `_ORPHAN_EXCLUDE_DIRS`, Phase D adds the SQL path). LLM and SQL contradictions are deduped by normalized `frozenset({from_slug, to_slug})`; SQL hits win when both surface the same pair. SOUL conflict detection (Phase 2 capability with no SQL substitute) is preserved unchanged across the dedupe boundary. `vault/health/synth-manifest-{date}.json` (NEW) captures per-run counts (concepts, connections, edges, rejected, duration, model, wol_status) and `daily_driver.py` morning brief surfaces them under Vault Health (second touch on this file: Phase 1 of agent-wiring added the artifact preamble, Phase D adds the synth line). Empty-vault verification chosen via pure unit tests (mocked LLM emits `relations`, in-memory SQLite verifies edge rows) — full pytest suite 204 → 241 (+37). Rollback = `DROP TABLE concept_edges` + revert the four MODIFY files; LLM still writes connection articles unchanged because `relations` is OPTIONAL in the prompt schema.

**SessionEnd auto-stub for new person wikilinks (v3.28.0, 2026-05-11):** New `agents-sdk/scripts/auto_stub_people.py` + `.claude/hooks/session-end-auto-stub.sh` close the regression risk: when a new clip lands with `author: - "[[Some New Author]]"`, the SessionEnd hook auto-creates `vault/40_knowledge/people/<slug>.md` before the next Sunday lint run. Two filters prevent garbage stubs — the wikilink must appear in `author:` YAML frontmatter (structured signal, ignores body-text + `related:` fields), and the target must match the person-name shape (`^[A-ZÀ-Ý][A-Za-zÀ-ÿ.'\-]*( ...){0,2}$` — 1-3 capitalized tokens, latin diacritics OK, accepts "Ali Çevik" / "RT Watson" / rejects "stage" / "10" / "intent-engineering"). Stubs use `status: unverified` and prompt Sean to fill in identity. Dedup via filename + title. Recursion-safe (skips `40_knowledge/people/`). Per-run safety cap of 10 stubs prevents runaway. Hook count `13 → 14`. Validated live by catching a missed `[[Lenny Rachitsky]]` reference across three inbox clips that the v3.27.2 manual sweep didn't surface. Rollback = remove the entry from `.claude/settings.json` SessionEnd block.

**Broken-wikilink cleanup sweep (v3.27.2, 2026-05-11):** Took the post-filter lint count from 37 → 0 by fixing the real issues plus one more exclusion. Added `node_modules` to the lint scanner's directory exclusion set (kills vendored-JS false positive). Created two concept hubs at `vault/40_knowledge/concepts/`: `intent-engineering.md` (resolves 11 stale wikilinks across the references/intent-engineering/ folder) and `writing-voice-modes.md` (resolves 1 from job-hunt operating-model). Created `vault/40_knowledge/people/` with 10 person stubs (`nate.md`, `rt-watson.md`, `daniel-kuhn.md`, `yogita-khatri.md`, `ali-cevik.md`, `lukas-haas.md`, `vivek-trivedy.md`, `timmy-shen.md`, `callum-howe.md`, `brian-danga.md`) — each uses `title:` frontmatter matching the wikilink target so `[[Nate]]` etc. resolve. Five targeted edits cleaned up the remaining real bugs (SOUL.md backslash escape, hermes prompt prefix, prj-job-hunt-2026 title frontmatter + folder→file rewrite, intent-eng folder-style link basename, Stripe web-clip artifact). Net result of v3.27.1 + v3.27.2: 348 → 0 broken wikilinks. Every vault wikilink now resolves and every previously-orphan target is a real node the synthesizer can cluster on.

**Knowledge Lint broken-wikilink filters (v3.27.1, 2026-05-11):** `find_broken_wikilinks` now drops two well-understood false-positive sources before reporting — numeric `[[NNN]]` citation markers from LLM research output (Gemini DR / local LDR) and the entire `the-block-meetings-granola-notes` folder (stale slug-rename cross-references in an archived read-only meeting trove). Net effect: 348 broken-wikilink issues → 37 on the live vault (89% reduction). Remaining 37 are all real signal — mostly `[[Person Name]]` wikilinks from research notes citing people who don't have stub files yet (`Nate`, `RT Watson`, `Daniel Kuhn` etc.). New constants: `_CITATION_TARGET_RE`, `_BROKEN_LINK_EXCLUDE_DIRS`, `_is_broken_link_excluded`. Two new tests in `tests/test_knowledge_lint.py`. Rollback = revert the three new constants + the helper, restore the un-filtered `find_broken_wikilinks` body.

**Fleet output consolidation in the daily note (v3.27.0, 2026-05-11):** Every agent's overnight activity now surfaces in the daily note instead of being scattered across `vault/health/`, `vault/02_Areas/Agent-Fleet/`, `vault/knowledge/`, and `vault/20_projects/research/`. New helper `agents-sdk/lib/fleet_summary.py:build_fleet_overnight_digest` reads the last 24h of `vault/90_system/agent-logs/agent-run-history.csv` plus the latest synth-manifest and lint report, returns a 7-line markdown block (one per active agent). Daily Driver's morning prompt (`agents/daily_driver.py`) gained a Step 4 that instructs Claude to inject the digest verbatim at the `<!-- fleet-overnight -->` anchor (BEGIN/END fenced for unambiguous boundaries). Template `vault/90_system/templates/tpl-daily.md` adds the anchor section plus a **Fleet Activity Today** section with four Dataview blocks that auto-refresh as agents write files: today's `daily-fleet-status-*.md`, new files in `knowledge/concepts/` or `knowledge/connections/` (last 24h), new files in `20_projects/research/` (last 24h), latest `vault/health/*-lint-report.md`. Meta-agent is special-cased — it reads the CSV but doesn't write to it, so today's fleet-status file existence is the success proxy. Rollback = remove the new sections from the template + revert Step 4 in `build_prompt`.

**Knowledge-loop Phase C — query.py + qa/ tier + OB1 provenance (v3.19.0, 2026-05-01):** `agents-sdk/scripts/query.py` adds terminal Q&A against `vault/knowledge/index.md` with two-pass orchestration: a selection pass picks 3-N article paths with similarity scores; an answer pass reads the selected bodies and emits a `[[wikilink]]`-citing answer. Local-first model routing via HybridRouter (`vault_synthesis` task → Qwen3-14B on MBP) with Anthropic Sonnet 4.6 fallback. `--file-back` persists answers as a third article tier at `vault/knowledge/qa/<slug>.md` and appends one JSONL record per run to `vault/knowledge/qa/.manifest.json`. Two OB1-inspired adds per the 2026-04-25 architectural review verdict: (C.M1) the qa/ frontmatter cites each consulted article with a 12-char SHA-256 chunk_id over `(file_path, chunk_index)` from `vault/.vault-index.db`'s `chunks` table plus the selection-pass similarity score, giving the synthesizer a cheap "did this specific chunk change?" check; (C.M2) the manifest is append-only JSONL matching the `lib/logging_setup.py:record_run` pattern. `vault_synthesizer.regenerate_index` learned a `## Q&A` section so qa/ articles surface in the SessionStart-injected index alongside concepts/connections. `knowledge_lint._ORPHAN_EXCLUDE_DIRS` gained `qa` because qa/ articles are answer endpoints (cite outward, never receive inbound wikilinks). Empty-state path (current live state — empty index until the synthesizer fires on an awake MBP) is explicit: zero candidates, no LLM call, no qa file written, exit 0. Rollback = delete `scripts/query.py` and revert the qa/ entries in `regenerate_index` + `_ORPHAN_EXCLUDE_DIRS`.

**launchd requirement:** All plists must include `EnvironmentVariables` with `PATH` set to `/Users/seanwinslow/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`. Without this, the `claude` CLI is not discoverable and agents fail with `CLIConnectionError`. See `agents-sdk/BUGFIX-2026-04-07-launchd-path.md`.

## Architecture

```
.claude/
├── skills/          # ALL 118 skills (canonical, auto-loaded)
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
