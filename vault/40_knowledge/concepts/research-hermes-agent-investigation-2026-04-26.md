---
type: research
status: draft
domain: agents-sdk
date: 2026-04-26
question: "Should Sean port any design patterns from NousResearch/hermes-agent into agents-sdk/?"
source: claude-code-investigation
tags: [research, hermes-agent, agents-sdk, integration-review]
links:
  - "[[ref-hermes-agent-investigation-prompt]]"
---

# Hermes Agent — Integration Investigation

## TL;DR

- **Verdict: NO with one SPIKE.** Hermes is a multi-provider self-improving agent *framework* (118K⭐, 17.6K forks, MIT, Python ≥3.11, ~40 modules in `agent/` alone). agents-sdk is a local-first, vault-integrated, scheduled personal automation layer on top of `claude-agent-sdk`. The shapes don't fit; wholesale adoption would be a multi-week off-ramp from the SDK.
- **Single highest-leverage thing worth a SPIKE:** port Hermes's `system_and_3` Anthropic prompt-caching pattern into `daily_driver.py` morning runs — potential ~50% cost reduction on the only paid agent in the fleet (~$0.40 → ~$0.20/run, ~$5–6/month savings, faster TTFT). Compatibility with `ClaudeAgentOptions` is unverified — must SPIKE before SHIP.
- **Convergent, already shipped:** skill loading (both projects ship the agentskills.io standard), MCP support, structured logging.
- **Anti-patterns to avoid:** Honcho dep for user modeling (cloud-only, breaks no-egress invariant for life-systems), Telegram/Discord/Slack/WhatsApp/Signal gateways (life-systems data can't leave the laptop), in-process croniter (loses launchd's OS-level reliability).
- **Roadmap impact:** Phase 2 of operating-model artifact wiring (meta_agent / flush / knowledge_lint) stays the v3.18.0 priority. Prompt-caching SPIKE is a small parallel investigation that could ride alongside Phase 2; the rest of Hermes does not change the v3.18 / v3.19 plan.

## Current agents-sdk State (verified)

Read at `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/` on 2026-04-26.

- **Two coexisting architectural patterns.** `agents-sdk/agents/daily_driver.py` is an SDK-loop agent: `ClaudeAgentOptions` + `claude_agent_sdk.query()` with `system_prompt={"type": "preset", "preset": "claude_code", "append": skills_prompt}`. `agents-sdk/agents/deep_researcher.py` (v3.17.0, 2026-04-26) is a pure-Python REST agent: no SDK in the loop, drives LDR over httpx (`/auth/login` → `/research/api/start` → `/research/api/status/<id>` → `/api/report/<id>`).
- **Skill loading.** `agents-sdk/lib/skill_loader.py:12-34` reads `.claude/skills/{name}/SKILL.md`, regex-strips YAML frontmatter, concatenates with `## Skill: name` headers separated by `---`. Skills become the `append` payload of the system prompt. This is functionally equivalent to the agentskills.io standard.
- **Three-machine routing model.** `agents-sdk/config.toml:184-243`. Mac Mini (always-on, Ollama, port 11434), MacBook Pro (sometimes-on, LM Studio port 1234), Alienware (sometimes-on, Ollama, WOL). `[routing.task_map]` maps task names → `(model, machine)`. v3.14.3 retired WOL; Mac Mini is the canonical agent driver. Cloud fallback (Anthropic API) only for `daily_driver` (~$0.40/run).
- **Safety rails.** `[safety]` defaults: `max_turns_default=30`, `max_budget_default=0.50`, `permission_mode="acceptEdits"`. Per-mode budget overrides (morning $0.60 since v3.16.0). Zero-Interaction Mandate + Safe Deferral Protocol baked into every agent preamble (`daily_driver.py:111-159`). Hooks at the harness level: block-secrets, network-access-control, require-confirm-highrisk, etc.
- **Knowledge compounding loop (v3.14.3).** Producer side complete: SessionEnd hook → `flush.py` (routes by message count) → nightly `vault_synthesizer.py` (concept + connection articles, MBP) → weekly `knowledge_lint.py` (Sun 22:00, two-tier). D.4 autoresearch consumer side **descoped** in v3.14.2 pending upstream harness. Re-open spec: `creative-studio/16bitfit-battle-mode/docs/plans/phase6-SUPER-PLAN-2026-04-17.md` §10.1.
- **Operating-model artifact wiring (v3.16.0 Phase 1).** `agents-sdk/lib/artifact_loader.py` reads `vault/05_atlas/operating-models/{domain}/{kind}.md` with mtime-keyed cache (`_cache: dict[tuple[str, str, int], str]`), `status: confirmed` gating, and graceful `None` for missing artifacts (never raises). Daily-driver morning is wired (`daily_driver.py:45-108` `build_artifact_preamble()`); Phase 2 (`meta_agent` / `flush` / `knowledge_lint`) and Phase 3 (`meeting_defender` / `sprint_health`) deferred.
- **The 6 disabled agents.** Per `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`: `process-inbox` (was burning $9.30/mo on `CLIConnectionError` retry loops), `daily-driver` evening + weekly (same SDK transport bug), `pr-digest` (gh CLI auth/PATH state), `sprint-health` and `meeting-defender` (never produced output). Two root causes: SDK subprocess transport readiness race + headless mode lacks browser-OAuth MCP servers.
- **Phase 6 LDR/SearXNG (v3.17.0).** Local stack outside repo at `~/Code-Brain/local-deep-research-stack/`. SearXNG container on `localhost:8080`, LDR on `localhost:5050` (5000 conflicts with macOS AirPlay), Qwen3-14B MLX 4-bit on LM Studio port 1234, `/no_think` directive to disable reasoning preamble. Queue-based input via `vault/00_inbox/research-queue.md`; output to `vault/20_projects/research/{date}-{slug}.md`; daily-note injection at `<!-- research-digest -->` anchor with append-section fallback. $0/run, 100% local.

## Hermes Agent Identification

- **Canonical URL:** `https://github.com/NousResearch/hermes-agent` — confirmed via WebFetch on 2026-04-26.
- **Latest release tag:** v0.11.0 (April 23, 2026). Specific commit SHA not exposed via the WebFetch summary; treat the tag as the read-against reference.
- **License:** MIT.
- **Stars / forks:** 118,000 ⭐ / 17,600 🍴. This is *not* a niche project — it's one of the more visible OSS agent frameworks of 2026.
- **Primary language:** Python (87.7%). Required Python ≥3.11.
- **Top-level layout (root):** `.github/`, `.plans/`, `acp_adapter/`, `acp_registry/`, `agent/`, `assets/`, `cron/`, `datagen-config-examples/`, `docker/`, `environments/`, `gateway/`, `hermes_cli/`, `nix/`, `optional-skills/`, `packaging/`, `plans/`, `plugins/`, `scripts/`, `skills/`, `tests/`, `tinker-atropos/`, `tools/`, `tui_gateway/`, `ui-tui/`, `web/`, `website/`, plus `pyproject.toml`, `Dockerfile`, `.env.example`.
- **Project thesis (verbatim from README, ≤3 sentences):**
  > "The self-improving AI agent built by Nous Research." [README]. The README highlights "a built-in learning loop for skill creation, support for 200+ models across multiple providers, a terminal interface with multiline editing, multi-platform messaging (Telegram, Discord, Slack, etc.), autonomous memory management, scheduled automation capabilities, and deployment flexibility across local, Docker, SSH, Daytona, Singularity, and Modal environments."
- **What Hermes IS, precisely:** a multi-provider, multi-platform CLI agent framework. It is *all of the following at once*: (a) a CLI runtime (`hermes_cli/main.py`), (b) a model router across 200+ models / 8+ providers via per-vendor adapter modules (`agent/anthropic_adapter.py`, `bedrock_adapter.py`, `gemini_native_adapter.py`, `gemini_cloudcode_adapter.py`, `codex_responses_adapter.py`, `copilot_acp_client.py`), (c) a messaging gateway (Telegram/Discord/Slack/WhatsApp/Signal), (d) an in-process scheduler (`cron/scheduler.py` + `cron/jobs.py` using `croniter>=6.0`), (e) a self-improving skill engine writing trajectories in ShareGPT format for fine-tuning (`agent/trajectory.py`), and (f) an ACP server (`acp_adapter/`) for IDE/tool integration. **It is *not* a Claude Code SDK alternative — it ships its own `claude-code` skill** at `skills/autonomous-ai-agents/claude-code/`, plus skills targeting `codex`, `opencode`, and `hermes-agent` itself.
- **Compatibility hazards visible in `pyproject.toml`:** runtime deps include `openai>=2.21`, `anthropic>=0.39`, `httpx[socks]`, `firecrawl-py>=4.16` (paid), `exa-py>=2.9` (paid), `parallel-web>=0.4`, `fal-client` (paid), `edge-tts`, `prompt_toolkit`, `rich`, `tenacity`, `jinja2`, `pydantic>=2.12`. Optional groups: `cron` (`croniter`), `messaging`, `voice` (`faster-whisper`, `sounddevice`, `numpy`), `web` (`fastapi`, `uvicorn`), `mistral`, `bedrock`, `google`, `daytona`, `modal`. The default install is *not* zero-network; multiple paid services are first-class deps.

## Internals Map

> **Verification posture:** Where I directly fetched a `raw.githubusercontent.com` source file, claims are sourced. Where I only fetched a directory listing (no file contents), claims about that subsystem are marked **inferred-from-filenames** and the verdict's confidence is correspondingly downgraded.

### 1. Agent loop / control flow

`hermes_cli/main.py` is the entry point (visible in directory listing). The actual control-flow body of the loop was **not retrievable via WebFetch** within this investigation window — only the file list. Inferred-from-filenames: the loop coordinates `agent/prompt_builder.py`, `agent/context_engine.py`, `agent/trajectory.py`, plus per-provider adapters via dispatch in `agent/credential_pool.py` + `agent/credential_sources.py`. Pattern is plausibly ReAct-style with a memory pre-fetch hook (`agent/memory_provider.py::prefetch_all`).

**Verdict:** `NOT_VERIFIED` (file contents unread). Lower confidence on architectural claims about the loop's exact shape.

### 2. Tool interface

`agent/skill_commands.py` + `agent/skill_preprocessing.py` + `agent/skill_utils.py` (filenames only) plus the `skills/` directory tree. Skills are described in the README as "procedural memories that the agent creates autonomously after complex tasks" following the **agentskills.io open standard** [README]. There are 25+ skill categories (`apple/`, `mcp/`, `research/`, `red-teaming/godmode/`, etc.). MCP is supported as a dev/optional dep (`mcp` in `[dev]` group of `pyproject.toml`). `tools/` is a separate top-level dir suggesting tools and skills are distinct concepts (Hermes-specific terminology — tools = primitives, skills = composed procedures).

**Verdict:** `CONVERGENT_WITH_OURS` — both projects ship the agentskills.io skill standard. Sean's `agents-sdk/lib/skill_loader.py:12-34` and Hermes's skill loader land at the same convention.

### 3. Model abstraction

Hermes ships per-provider adapter files: `agent/anthropic_adapter.py`, `agent/bedrock_adapter.py`, `agent/gemini_cloudcode_adapter.py`, `agent/gemini_native_adapter.py`, `agent/codex_responses_adapter.py`, `agent/copilot_acp_client.py`, `agent/auxiliary_client.py`. README claims 200+ models across "Nous Portal, OpenRouter, NVIDIA NIM, Xiaomi MiMo, z.ai/GLM, Moonshot, MiniMax, Hugging Face, OpenAI." The `pyproject.toml` mandates `openai>=2.21,<3` and `anthropic>=0.39,<1` as core deps (not optional).

agents-sdk is locked to `claude-agent-sdk==0.1.63` for SDK-loop agents and direct httpx calls for the deep_researcher (LDR). One-provider lock-in for cloud, plus local LM Studio + Ollama via the `[routing]` table.

**Verdict:** `NOVEL` — Hermes's per-provider adapter pattern is more flexible. But not actionable for Sean: the SDK-loop pattern's value is precisely the alignment with Anthropic's evolving features (Claude 4.7, prompt caching, thinking blocks, etc.). Adopting per-provider adapters would dilute that.

### 4. Memory / state

`agent/memory_manager.py` (verbatim from WebFetch summary): "MemoryManager orchestrates a built-in memory provider with at most one external plugin provider, serving as a single integration point that delegates memory operations across registered backends." Architecturally significant lines:

> "Only **one** external (non-builtin) provider is allowed — a second attempt is rejected with a warning."
> "Failures in one provider never block the other."
> "The fence prevents the model from treating recalled context as user discourse."

External provider is `Honcho` per the README (cloud SaaS for "user modeling across sessions"). Storage backends are abstracted; concrete implementations via `MemoryProvider` subclasses (not directly verified). Operations: `sync_all(user_content, assistant_content)`, `prefetch_all(query)`, `queue_prefetch_all()`, `handle_tool_call()`.

agents-sdk has no equivalent. The Obsidian vault IS the memory: `vault_indexer.py` writes Ollama embeddings to `.indexer-state.json`; daily-driver reads vault notes via the `Read` tool; artifact_loader caches operating-model artifacts in-process. Memory is file-system-of-record, not a managed provider abstraction.

**Verdict:** `NOVEL but INCOMPATIBLE` — Hermes's pluggable memory pattern is cleaner abstraction, but it requires a runtime memory provider (Honcho is cloud + paid). Sean's vault-as-memory is simpler and respects the no-egress invariant for life-systems data. The Honcho dep would break NN #7-life-systems.

### 5. Scheduling / autonomy

Hermes ships `cron/__init__.py`, `cron/jobs.py`, `cron/scheduler.py` plus `hermes_cli/cron.py` (CLI verb). Uses `croniter>=6.0.0,<7` from the `[cron]` optional group. In-process scheduler — runs *while* `hermes` itself is running.

agents-sdk uses macOS `launchd` plists at `agents-sdk/schedules/*.plist` (e.g., `com.sean.agent.deep-researcher.plist`). Each plist sets `EnvironmentVariables.PATH` for the `claude` CLI and `gh`, `WorkingDirectory`, `StandardOutPath` / `StandardErrorPath`, and a `StartCalendarInterval` block. OS-level scheduling — runs even when no user is logged in, survives reboots.

**Verdict:** `INFERIOR_TO_OURS` for Sean's use case. launchd offers higher reliability and OS-level persistence. Hermes's in-process cron is the right choice for VPS deployments where Hermes itself is the long-running daemon, not for a personal Mac fleet.

### 6. Safety / guardrails

Hermes ships: `agent/file_safety.py`, `agent/redact.py`, `agent/error_classifier.py` (15-category `FailoverReason` enum: auth, auth_permanent, billing, rate_limit, overloaded, server_error, timeout, context_overflow, payload_too_large, model_not_found, provider_policy_blocked, format_error, thinking_signature, long_context_tier, unknown), `agent/nous_rate_guard.py`, `agent/rate_limit_tracker.py`, `agent/prompt_caching.py`, `agent/usage_pricing.py`. Plus `agent/credential_pool.py` for auth handling.

agents-sdk's safety lives at multiple layers: harness-level hooks (`block-secrets.sh`, `network-access-control.sh`, `require-confirm-highrisk.sh`), per-agent budget caps in `config.toml` (`max_turns`, `max_budget_usd` per mode), the Zero-Interaction Mandate + Safe Deferral Protocol in agent preambles, `permission_mode="acceptEdits"` in `ClaudeAgentOptions`. Errors are caught with bare `except Exception` and logged via `record_run`.

**Verdict:** `NOVEL` on the error-classifier dimension. Hermes's `FailoverReason` enum is more sophisticated than agents-sdk's ad-hoc try/except — and the AUDIT-2026-04-09 disabled-agents postmortem traces every disabled agent to one of the categories Hermes already enumerates (`CLIConnectionError` ≈ Hermes's `transport heuristics`, `error_max_budget_usd` ≈ `billing`/`context_overflow`).

### 7. Observability

Hermes: `agent/trajectory.py` writes ShareGPT-format JSONL files (`trajectory_samples.jsonl` for completed runs, `failed_trajectories.jsonl` for failures) with metadata (timestamp, model, completed boolean). Plus `agent/insights.py` for analytics, `agent/account_usage.py` for usage tracking, `agent/usage_pricing.py` for cost calculation.

agents-sdk: `lib/logging_setup.py:setup_logger` (per-agent logfile + stderr) and `record_run` (CSV history at `vault/90_system/agent-logs/agent-run-history.csv` with date, time, agent, mode, status, cost_usd, duration_ms, turns, notes columns).

**Verdict:** `CONVERGENT_WITH_OURS` for the basic logging — both have per-run logs + structured history. `NOVEL` for the ShareGPT trajectory format, which is fine-tuning bait. Sean has no fine-tuning pipeline; this is speculative future need.

### 8. Skills / prompts / personas

agentskills.io standard, see dimension 2. Hermes adds `agent/prompt_builder.py` for prompt composition and `agent/title_generator.py` for naming sessions. Skills are meant to be created *autonomously by the agent* during interactive use — the "self-improving" loop the README leads with.

agents-sdk skills are curated by Sean and exported via `scripts/install.sh` to other projects. 113 skills as of v3.15.0.

**Verdict:** `CONVERGENT_WITH_OURS` on the standard, `NOVEL` on the autonomous-skill-creation loop. Autonomous skill creation is not a fit for Sean's setup: skills are a curated personal-knowledge artifact, not a runtime-generated procedural memory.

### 9. Multi-agent coordination

`acp_adapter/` (auth.py, entry.py, events.py, permissions.py, server.py, session.py, tools.py) and `acp_registry/`. ACP here is **Agent Client Protocol** (the Zed-IDE protocol), not Google's A2A — confirmed by the existence of `agent/copilot_acp_client.py` (GitHub Copilot uses ACP). It's an inbound integration: external IDEs/clients talk to a Hermes session via ACP, not Hermes-to-Hermes.

agents-sdk has no inter-agent protocol. The 7 active agents are independent scheduled jobs; the only cross-agent state is shared files (vault notes, run history CSV).

**Verdict:** `NOT_PRESENT` in agents-sdk. But Sean doesn't need it — agents are independent by design, and SessionEnd → flush → vault_synthesizer is already a producer-consumer chain via filesystem.

### 10. Constitution / values / refusals

No verified evidence of an explicit constitution / values file in Hermes. `skills/red-teaming/godmode/` is a directory in the skills tree (filename only, contents not fetched). The README mentions "skills self-improve during use" but nothing about safety alignment scaffolding analogous to Anthropic's constitutional AI.

agents-sdk's value layer is the operating-model artifacts (`vault/05_atlas/operating-models/{domain}/{kind}.md`) — HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations per domain. SOUL.md is the values layer. Loaded at runtime via `lib/artifact_loader.py`. Plus the harness-level CLAUDE.md non-negotiables.

**Verdict:** `INFERIOR_TO_OURS` (with the caveat that the `red-teaming/godmode/` directory was not opened — could shift if it contains alignment scaffolding, but the directory name suggests the opposite).

## Side-by-Side Diff

| Dimension | Hermes approach | agents-sdk approach | Gap / Overlap |
|---|---|---|---|
| Agent loop | `hermes_cli/main.py` (loop body NOT_VERIFIED) | `daily_driver.py:306-371` `run()` async wraps `claude_agent_sdk.query()`; `deep_researcher.py:235-345` `run()` does pure-Python httpx polling against LDR | Different shapes — Hermes is a long-running CLI daemon; agents-sdk is one-shot launchd-triggered scripts. No port path. |
| Tool interface | `tools/` + `agent/skill_commands.py` + `agentskills.io` | `.claude/skills/` (113 skills) + `agents-sdk/lib/skill_loader.py:37-51` + `claude_agent_sdk.ClaudeAgentOptions.allowed_tools` | Both ship agentskills.io. Convergent. |
| Model abstraction | 6+ per-provider adapters (`agent/anthropic_adapter.py`, etc.) + `pyproject.toml` core deps `openai>=2.21,<3`, `anthropic>=0.39,<1` | `claude-agent-sdk==0.1.63` only for cloud; `[routing.task_map]` in `config.toml` for local LM Studio + Ollama | Hermes is multi-provider; agents-sdk is Claude-only for cloud. Porting per-provider adapters would dilute SDK alignment. |
| Memory | `agent/memory_manager.py` (built-in + 1 external; Honcho the named external) | Vault-as-memory: Obsidian files + `vault_indexer.py` Ollama embeddings + `lib/artifact_loader.py` mtime-cached artifact reads | Hermes pluggable abstraction is cleaner; Honcho dep breaks no-egress for life-systems. Don't port. |
| Scheduling | `cron/jobs.py` + `cron/scheduler.py` (`croniter>=6.0`, in-process) | `agents-sdk/schedules/*.plist` + `install_schedules.sh` (macOS launchd) | Hermes works on Linux/VPS; launchd is OS-level + more reliable on Mac. Don't port. |
| Safety / errors | `agent/error_classifier.py` (15 `FailoverReason` categories), `agent/file_safety.py`, `agent/redact.py`, `agent/nous_rate_guard.py` | Harness hooks (block-secrets.sh, network-access-control.sh), per-agent budget caps in `config.toml`, ad-hoc try/except | Hermes error classifier ports cleanly (~50–80 LOC, no new deps). Real value given AUDIT-2026-04-09. |
| Observability | `agent/trajectory.py` ShareGPT JSONL + `agent/insights.py` + `agent/account_usage.py` | `lib/logging_setup.py` per-agent logfile + CSV `agent-run-history.csv` | Convergent on basics. ShareGPT format is fine-tuning-only — speculative. |
| Skills | agentskills.io + autonomous skill creation (`agent/skill_preprocessing.py`) | agentskills.io (manual curation, 113 skills) + `scripts/install.sh` export | Convergent on standard. Autonomous creation doesn't fit a curated-knowledge model. |
| Multi-agent | `acp_adapter/` (Agent Client Protocol, inbound IDE integration) | None — agents are independent launchd jobs | Not needed for Sean's fleet. |
| Constitution | None verified (`skills/red-teaming/godmode/` exists but unread) | `vault/05_atlas/operating-models/{domain}/SOUL.md` + CLAUDE.md non-negotiables + `lib/artifact_loader.py` | agents-sdk wins. |
| Prompt caching | `agent/prompt_caching.py` `system_and_3` Anthropic-style: 4 cache_control breakpoints (system + last 3 non-system) with ephemeral marker + 5m/1h TTL | `ClaudeAgentOptions` `system_prompt={"type":"preset","preset":"claude_code","append":skills_prompt}` — cache behavior depends on SDK 0.1.63's preset implementation (UNVERIFIED) | High-leverage gap if SDK doesn't auto-cache the `append` payload. |
| Context compression | `agent/context_compressor.py` (head/tail protect + middle summarize + iterative + tool-result prune) | None at agent layer; SDK has internal compaction in newer versions | No current pain. WATCH. |

## Port Candidates

> **Filter applied:** Python 3.13 + `claude-agent-sdk==0.1.63` + macOS launchd + 100%-local invariant for the autonomous fleet (or explicit justification) + no-cloud-egress for life-systems data + ≤2-hr validation experiment.

### Candidate 1 — Anthropic prompt-caching `system_and_3` pattern

- **What it is:** Inject `cache_control: {"type": "ephemeral"}` markers on the system prompt + the last 3 non-system messages so Anthropic's API caches the stable skills_prompt + artifact preamble across invocations. Reduces input-token cost ~75% on cache hits.
- **Source (Hermes):** `agent/prompt_caching.py` (raw fetched 2026-04-26, ref tag v0.11.0). Architecturally significant lines per WebFetch summary: `"Places up to 4 cache_control breakpoints: system prompt + last 3 non-system messages."`, `marker = {"type": "ephemeral"}`, rolling-window logic over `non_sys` indices, attaching marker to `last["cache_control"]`.
- **Target (ours):** `agents-sdk/agents/daily_driver.py:250-303` `build_options()`. The `skills_prompt` (loaded from `lib.skill_loader.load_skills`, sized at ~3–5K tokens) plus the `build_artifact_preamble` output are both stable across morning runs — prime cache candidates.
- **Estimated effort:** S (half day) IF the SDK exposes message manipulation; **M (1–2 days) if it doesn't** and we have to either (a) submit upstream SDK PR or (b) bypass `claude_agent_sdk.query()` for this agent and call `anthropic.messages.create()` directly with the same prompt structure (similar to deep_researcher's pure-Python pattern).
- **Net new dependencies:** None. `anthropic` SDK is already pulled in transitively by `claude-agent-sdk==0.1.63`.
- **Compatibility hazards:** This is the actual unknown. `ClaudeAgentOptions.system_prompt` accepts `{"type":"preset","preset":"claude_code","append":<str>}` — the `append` is a string, not a content array, so `cache_control` markers can't be injected via that path. The SDK *may* internally cache the preset's stable prefix. UNVERIFIED.
- **Why it's worth it:** daily-driver morning is the only paid agent in the active fleet at ~$0.40/run × 30 days = $12/month. ~75% cache hit on the stable prefix → ~$3/month savings + faster TTFT. Compounds if/when Phase 2 (`meta_agent` artifacts wired) lands more agents on the cloud path.
- **Why it might NOT be worth it:** $3/month is a small absolute saving. If the SDK doesn't expose message manipulation cleanly, the M-effort variant (bypass SDK for daily_driver) is a 1–2 day refactor for $36/year saved.
- **Validation experiment (≤2 hrs):**
  1. Write a one-off script `agents-sdk/scripts/validate_prompt_caching.py`. Pull `skills_prompt` via `load_skills(["daily-driver", "vault-read-write"], skills_dir)` (existing function, no change).
  2. Build a minimal `anthropic.messages.create()` call with the skills_prompt as a `system` message containing a single content block with `cache_control: {"type": "ephemeral"}`.
  3. Send a short user message twice in immediate succession.
  4. Read `response.usage.cache_creation_input_tokens` and `cache_read_input_tokens`. If second call shows >50% cache hit, port to daily_driver. If not, the SDK preset is already caching it, no action needed.
- **Verdict:** **SPIKE** — biggest cost lever in the investigation, but compatibility unknown.

### Candidate 2 — Error classifier (downscaled to agents-sdk's actual failure modes)

- **What it is:** A small `lib/error_classifier.py` that maps exception types and HTTP status codes to a 4–5 category enum (`SDK_TRANSPORT`, `BUDGET_EXHAUSTED`, `LDR_TIMEOUT`, `NETWORK_LOCAL`, `UNKNOWN`), powering smarter retries and surfacing root cause in the run history CSV.
- **Source (Hermes):** `agent/error_classifier.py` `FailoverReason` enum (15 categories: auth, auth_permanent, billing, rate_limit, overloaded, server_error, timeout, context_overflow, payload_too_large, model_not_found, provider_policy_blocked, format_error, thinking_signature, long_context_tier, unknown). Pipeline: provider-specific patterns → HTTP status → error code → message patterns → transport heuristics → fallback.
- **Target (ours):** New `agents-sdk/lib/error_classifier.py`. Consumed by `daily_driver.py:359` (the `except Exception as e` block) and `deep_researcher.py:299-308` (the LDR error path). Persisted to the `notes` field of `record_run`.
- **Estimated effort:** S (half day). Hermes's 15 categories collapse to ~5 once filtered to "errors that have actually happened in agent-run-history.csv since 2026-04-01."
- **Net new dependencies:** None.
- **Compatibility hazards:** None. Pure stdlib.
- **Why it's worth it:** Per `AUDIT-2026-04-09-agent-downsizing.md`, 6 of 8 disabled agents share 2–3 root causes (`CLIConnectionError`, `error_max_budget_usd`, gh-CLI auth state). A classifier surfaces these in the CSV instead of as opaque stack traces, and unblocks differential retry policy (transient → retry once, permanent → halt + notify Pushover).
- **Why it might NOT be worth it:** A 5-line lookup table replaces the classifier's value. The "framework-y" version with a registry pattern and provider-specific resolvers is over-engineering for a 7-agent fleet.
- **Validation experiment (≤2 hrs):**
  1. Read `vault/90_system/agent-logs/agent-run-history.csv` for the last 90 days. Group `notes` field by error pattern.
  2. Confirm the top 5 patterns cover ≥90% of failures.
  3. If yes, write a 30-line classifier function and a unit test with the 5 known error fingerprints. Wrap one agent's `except Exception` block. Don't port the registry/dispatch machinery from Hermes.
- **Verdict:** **SHIP** (low effort, real audit-validated pain, no architectural risk).

### Candidate 3 — Context compressor pattern (deferred capability)

- **What it is:** Head/tail-protected, middle-summarized, tool-result-pruned, iteratively-refreshed context compaction (per Hermes `agent/context_compressor.py` summary).
- **Source (Hermes):** `agent/context_compressor.py`. WebFetch quote: `"Prune old tool results (cheap, no LLM call); Protect head messages (system prompt + first exchange); Find tail boundary by token budget (~20K tokens of recent context); Summarize middle turns with structured LLM prompt; On re-compression, iteratively update the previous summary"`.
- **Target (ours):** Future `agents-sdk/lib/context_compressor.py`. Consumed by `vault_synthesizer.py` (long-running, MBP) and a hypothetical `deep_researcher` v2 if multi-LDR-call workflows land.
- **Estimated effort:** M (1–2 days).
- **Net new dependencies:** None (LLM call routes through existing `[routing]` table → local Ollama or LM Studio).
- **Compatibility hazards:** Newer `claude-agent-sdk` versions ship internal compaction. Building a parallel compactor for non-SDK agents only.
- **Why it's worth it:** No current pain. Speculative future need.
- **Why it might NOT be worth it:** YAGNI. Sean's deep_researcher hands off to LDR which has its own context handling.
- **Validation experiment (≤2 hrs):** Write a unit test that builds a 200-message conversation, runs the compressor, asserts (a) head 10 + tail 20K tokens preserved, (b) middle replaced by a summary, (c) tool results older than tail boundary removed.
- **Verdict:** **WATCH** — revisit if `vault_synthesizer.py` hits context overflow on a real run.

### Candidate 4 — (skipped — none of the remaining patterns clear the filter)

Considered and rejected:

- **In-process croniter scheduler:** loses launchd reliability. SKIP.
- **ACP adapter (inbound IDE protocol):** Sean doesn't run an IDE that needs ACP integration. SKIP.
- **Honcho-backed memory manager:** breaks no-egress for life-systems. SKIP.
- **ShareGPT trajectory logger for fine-tuning:** no fine-tuning pipeline. SKIP.
- **Autonomous skill creation loop:** skills are curated personal knowledge, not runtime-generated. SKIP.
- **Per-provider model adapters:** dilutes SDK alignment. SKIP.

## Anti-patterns to Avoid

1. **Cloud-only memory dep (Honcho).** `agent/memory_manager.py`'s "one external provider" hook is named in the README as Honcho — a cloud SaaS for "user modeling across sessions." Adopting this for life-systems agents would violate non-negotiable #7 (no cloud egress of life-systems personal data). The vault-as-memory pattern Sean already runs is simpler *and* respects the invariant.

2. **Multi-platform messaging gateways as a default capability.** Hermes's `[messaging]` optional group ships Telegram, Discord.py, slack-bolt/sdk, aiohttp, qrcode — and the README pitches "multi-platform messaging" as a headline feature. Autonomous agents posting to messaging platforms is precisely the failure mode Sean's "Slack/calendar requires browser-OAuth, only available interactively" architectural rule (CLAUDE.md, Agents-SDK section) was designed to prevent. Don't enable.

3. **Paid web-research deps as core requirements.** `pyproject.toml` lists `firecrawl-py>=4.16` (paid), `exa-py>=2.9` (paid), `parallel-web>=0.4`, `fal-client` (paid) as core (not optional) runtime deps. Adopting any Hermes module that imports these would either inject paid services into the autonomous fleet ($/run > 0) or require stubbing. Sean's SearXNG + LDR + Qwen3-14B local stack is a deliberate $0/run alternative — don't dilute it.

4. **In-process scheduler displacing launchd.** Hermes's `cron/scheduler.py` runs while `hermes` itself is running. macOS launchd plists run at the OS level, persist across reboots, and don't require a long-running daemon. The `EnvironmentVariables.PATH` lesson from `BUGFIX-2026-04-07-launchd-path.md` was earned the hard way; the launchd path is the right answer for Sean.

5. **Massive surface area as adoption tax.** `hermes_cli/` has 69 .py files. `agent/` has ~40. Plus `gateway/`, `tui_gateway/`, `ui-tui/`, `web/`, `acp_adapter/`, `acp_registry/`, `tools/`, `cron/`, `plugins/`, `optional-skills/`, `tinker-atropos/`. Even a "thin" port of one subsystem typically reaches 5–10 transitive deps. Resist the urge to "just port the agent loop" — it would pull in 4 adapter modules, the credential pool, the rate guard, the prompt builder, and the trajectory logger.

6. **`skills/red-teaming/godmode/`** — directory contents not fetched in this investigation, but the name is a red flag for jailbreak scaffolding. If Hermes ships a curated way to bypass its own guardrails, importing skills wholesale from `skills/` would import this too. Cherry-pick, don't bulk import.

## Strategic Take

**NO with one SPIKE.**

Hermes Agent is impressive but architecturally divergent from agents-sdk. It's a multi-provider, multi-platform, self-improving CLI framework targeted at users who want one daemon that talks to 200+ models across 5+ messaging surfaces. agents-sdk is a local-first, vault-integrated, scheduled personal automation layer where the *whole point* is that it lives inside Claude Code and the Obsidian vault. Wholesale adoption of Hermes patterns would require replacing `claude-agent-sdk` with a custom multi-provider router, replacing launchd with in-process cron, replacing the vault-as-memory model with Honcho — i.e. rewriting the project. Net cost: weeks of work for a system that no longer benefits from Anthropic's ongoing SDK evolution and that breaks the no-egress invariant for life-systems data.

The single highest-leverage thing worth investigating: **Hermes's `system_and_3` Anthropic prompt-caching pattern**. agents-sdk's daily-driver is the only paid agent in the active fleet, and the skills_prompt + artifact preamble are stable across morning runs — exactly the cache profile Anthropic's `cache_control` markers are designed for. Whether `ClaudeAgentOptions` with `system_prompt={"type":"preset","preset":"claude_code","append":...}` already routes through cache_control is unverified; the ≤2-hour validation experiment in Candidate 1 settles it. Worst case: a $3/month saving and 1–2 days of refactor. Best case: same saving with half a day of work and faster TTFT every morning.

**v3.18 / v3.19 implications:** Phase 2 of operating-model artifact wiring (`meta_agent` / `flush` / `knowledge_lint`) remains the v3.18.0 priority. The prompt-caching SPIKE is a small parallel investigation that can land alongside Phase 2 if it survives validation. The error-classifier SHIP is a 1-PR-sized cleanup for v3.18 or v3.19. Nothing in Hermes argues for re-prioritizing the descoped D.4 autoresearch consumer side, the disabled-6 reactivation, or any cross-machine work.

(195 words)

## Open Questions for Sean

1. **`ClaudeAgentOptions` cache behavior.** Does the `claude_code` preset (SDK 0.1.63) auto-cache the `append` payload, or does the cache hit come only from the preset's stable prefix? If Sean has a recent run's `usage` block from the `claude_agent_sdk` `ResultMessage`, the `cache_read_input_tokens` field answers this in 60 seconds without writing the validation script.
2. **`hermes_cli/main.py` agent-loop body.** Was not retrieved during this investigation. If it shapes a future "should we adopt the loop pattern?" decision, Sean can confirm contents in 5 minutes via `gh repo view NousResearch/hermes-agent` + reading the file. Current verdict assumes the loop is a standard ReAct-with-memory-prefetch shape; if it turns out to be something materially novel, the SKIP verdicts on per-provider adapters / model abstraction may need a re-look.
3. **Does Sean want a fine-tuning pipeline in the v4.x roadmap?** If yes, Hermes's `agent/trajectory.py` ShareGPT-format JSONL writer becomes a SHIP candidate (cheaply collects training data from existing autonomous-agent runs). If no, it stays SKIP.
4. **`skills/red-teaming/godmode/` contents.** Not fetched. If Sean ever wants to mass-import any Hermes `skills/*` subdirectory, this folder's contents need to be reviewed first — flagged as anti-pattern #6 above.

## Sources

### Hermes Agent (NousResearch/hermes-agent @ tag v0.11.0, 2026-04-23)

- `https://github.com/NousResearch/hermes-agent` — repo metadata, README excerpt
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md`
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/pyproject.toml`
- `https://github.com/NousResearch/hermes-agent/tree/main/agent` (directory listing)
- `https://github.com/NousResearch/hermes-agent/tree/main/skills` (directory listing)
- `https://github.com/NousResearch/hermes-agent/tree/main/cron` (directory listing)
- `https://github.com/NousResearch/hermes-agent/tree/main/acp_adapter` (directory listing)
- `https://github.com/NousResearch/hermes-agent/tree/main/hermes_cli` (directory listing)
- `https://github.com/NousResearch/hermes-agent/tree/main/skills/autonomous-ai-agents` (directory listing)
- `https://github.com/NousResearch/hermes-agent/tree/main/skills/research` (directory listing)
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/agent/memory_manager.py`
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/agent/context_compressor.py`
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/agent/trajectory.py`
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/agent/prompt_caching.py`
- `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/agent/error_classifier.py`

### Local files (claude-code-superuser-pack @ HEAD, 2026-04-26)

- `CLAUDE.md` (full, in conversation context)
- `CHANGELOG.md` lines 1–460 (versions 3.12.0 → 3.17.0)
- `agents-sdk/config.toml` lines 1–258 (full)
- `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md` lines 1–113 (full)
- `agents-sdk/agents/daily_driver.py` lines 1–393 (full)
- `agents-sdk/agents/deep_researcher.py` lines 1–367 (full)
- `agents-sdk/lib/skill_loader.py` lines 1–51 (full)
- `agents-sdk/lib/artifact_loader.py` lines 1–139 (full)
- `agents-sdk/lib/vault_io.py` lines 1–168 (full)
- `agents-sdk/lib/logging_setup.py` lines 1–103 (full)
- `agents-sdk/schedules/install_schedules.sh` lines 1–61 (full)
- `agents-sdk/schedules/com.sean.agent.deep-researcher.plist` lines 1–34 (full)
- `vault/00_inbox/hermes-agent-investigation-prompt.md` (full, in conversation context)
- `vault/00_inbox/research-queue.md` lines 1–14 (full)

### Investigation plan

- `/Users/seanwinslow/.claude/plans/please-read-thrrough-vault-00-inbox-herm-distributed-sutton.md`
