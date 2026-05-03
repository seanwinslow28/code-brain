---
type: plan
domain:
  - claude-mastery
  - life-systems
status: proposed
context: superuser-pack
created: 2026-05-03
source: claude-code-plan-mode
references:
  - vault/20_projects/prj-superuser-pack/prj-knowledge-loop-consumer.md (§Phase E)
  - vault/20_projects/prj-superuser-pack/open-source-deep-research/macmini-migration-plan-2026-05-02.md
  - vault/40_knowledge/references/ref-gemini-deep-research-api.md
  - vault/40_knowledge/references/ref-deep-research-max-gemini.md
  - vault/40_knowledge/references/ref-google-interactions-api.md
  - .claude/skills/last30days/SKILL.md
  - .claude/skills/deep-research-queue/SKILL.md
sibling-docs:
  - macmini-migration-plan-2026-05-02.md (v3.23.0 shipped — extends, does not modify)
---

# Gemini Deep Research Integration + Phase E Research Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` when implementing. Phases are independently shippable; each has a Test that produces a binary pass/fail signal and a single-command Rollback.

**Goal:** Wire Gemini Deep Research + Deep Research Max into the repo as first-class research tools alongside the v3.23.0 local LDR stack, AND use the existing local LDR path to actually execute research on the seven parked Phase E sub-topics so future-Sean has a fact base when revisiting Phase E around 2026-05-15.

**Architecture:** Mirror the v3.23.0 deep-research pattern (skill + autonomous SDK agent + queue file + vault landing) with Gemini-specific guardrails (per-task and per-month USD caps, mandatory user confirmation for Deep Research Max tier, separate queue file). Defer the `mcp_server`-as-tool composition (LDR or vault gateway inside Gemini DR runs) to v2 because the LDR wrapper is stdio-only while Gemini's `mcp_server` tool requires a remote HTTP endpoint.

**Tech Stack:** `google-genai` Python SDK · Gemini Interactions API (`/v1beta/interactions`, `background=true` polling) · `agents-sdk/.venv` Python 3.13 · `agents-sdk/lib/keychain.py` for `gemini_api_key` (mirrors `ldr_username` / `anthropic_api_key`) · macOS launchd at 03:30 daily (Mac Mini, default disabled) · vault landing at `vault/20_projects/research/` with `source: gemini-deep-research[-max]` frontmatter.

---

## 1. Executive Summary

Three streams in one plan:

- **Stream A (5 nights of Mac Mini compute, ~$5 expected):** Queue the seven Phase E topics, refactored into seven shippable research runs: topic 1 splits into 1a (MCP/SDK toolkits survey) and 1b (CLI agentic-workflow repo audit + Gemini CLI extensions + pinning patterns); topic 4 absorbs the reframed topic 6 to become a single comprehensive auth-mode-and-key-generation matrix; topic 6 disappears as standalone. Final distribution: **five local LDR runs ($0/each)** for 1a, 1b, 3, 5, 7; **one Gemini Deep Research run ($1–3)** for topic 2; **one Gemini Deep Research Max run ($3–7)** for topic 4. Total ceiling **$10**; expected **~$5**.
- **Stream B (~14 engineering hours):** Ship a new `gemini-deep-research` skill + sibling `gemini_researcher.py` autonomous SDK agent + `gemini_dr.py` Python helper invoking the Gemini Interactions API with polling. Skill is the interactive primary path; agent runs scheduled (default disabled). Defer stdio MCP wrapper to v2.
- **Stream C (decision, 0 engineering hours):** `last30days` stays standalone — different question type (social-media trend signal, last 30 days) than LDR / Gemini DR (authoritative-source synthesis with citations).

Why now: v3.23.0 deep_researcher is shipped + soaking; the Phase E parking lot is the natural use case for the new tier (DR Max for the auth-mode taxonomy matrix); `ref-gemini-deep-research-api.md` was clipped 2026-05-03 confirming public-preview availability.

---

## 2. Discovery Findings

### What already exists in the repo (cite-then-extend, do not duplicate)

| Artifact | Path | State |
|---|---|---|
| Local autonomous research agent | `agents-sdk/agents/deep_researcher.py` | **Shipped v3.23.0.** Pure Python httpx loop against LDR `localhost:5050` on Mac Mini. Reads queue, writes topical note, injects daily-digest, marks done. **Out of bounds:** plan §constraints forbids modifying its runtime behavior — extend with siblings, do not refactor. |
| Local interactive write-side skill | `.claude/skills/deep-research-queue/SKILL.md` | **Shipped v3.23.0.** Edits `vault/00_inbox/research-queue.md`. Allowed tools: `Read`, `Edit` only. New Gemini skill mirrors this shape but adds `Bash` + `AskUserQuestion`. |
| Local research queue | `vault/00_inbox/research-queue.md` | Live. Empty Pending section as of 2026-05-03 (two recent items already `[x]`-completed). Stream A appends here. |
| Local research output dir | `vault/20_projects/research/` | Live. Two LDR reports filed. Frontmatter pattern established. Gemini reports land in same dir, distinguished by `source:` field. |
| Daily-note digest anchor | `vault/90_system/templates/tpl-daily.md:37` | `<!-- research-digest -->` shipped in v3.21.0. Reused unchanged by Gemini path. |
| Keychain helper | `agents-sdk/lib/keychain.py` | Service prefix `com.sean.agents`. Existing entries: `anthropic_api_key`, `ldr_username`, `ldr_password`, `pushover_*`. New entry: `gemini_api_key`. |
| Cost-watchdog hook | `.claude/hooks/cost-watchdog.sh` (assumed; ledger pattern in `agents-sdk/lib/logging_setup.py` `record_run`) | Watches Anthropic spend per-agent. Out of scope for Gemini — different vendor, separate ledger. **Decision:** new Gemini ledger at `vault/health/gemini-spend-{YYYY-MM}.json`; cost-watchdog hook unchanged. |
| `last30days` skill | `.claude/skills/last30days/SKILL.md` | Shipped (community import v3.12.0). Social-media + 30-day window. **Stream C decision:** stays standalone, not folded in. |
| Mac Mini 02:00–09:00 schedule | `agents-sdk/schedules/*.plist` | 02:00 vault-indexer (15m) · 02:30 vault-synthesizer (MBP, irrelevant) · 02:45 deep-researcher (15m cap) · 06:30 meta-agent (5m) · 08:45 daily-driver morning (10m). **Verified non-overlap with proposed 03:30 gemini-researcher slot:** §6 Phase 6. |
| Mac Mini memory headroom budget | macmini-migration-plan §1 | Peak ~22 GB during LDR run (14B model + KV + Docker + Ollama + macOS), ~1.4–1.9 GB margin. **gemini_researcher does NOT load any local model** — it's a pure httpx polling loop, ~0.2 GB. The 24 GB ceiling math is unaffected. |
| **Gemini SDK / API key / Python helper** | n/a | **DOES NOT EXIST.** Genuinely new in this plan. |

### Gemini Interactions API constraints (from `ref-gemini-deep-research-api.md`, §Limitations)

- **Beta status** — schemas may change; pin `google-genai` version, document re-test on upgrade.
- `background=true` is **required** for the Deep Research agent — synchronous calls will time out.
- `store=true` is required when `background=true`.
- **Max research time: 60 minutes.** Most tasks complete in <20 min. Plan must accommodate up-to-60-min polling windows.
- **No custom Function Calling tools** (today). Only built-in tools (`google_search`, `url_context`, `code_execution`, `file_search`) and **remote** `mcp_server` tools (HTTP, not stdio).
- **No structured output** — output is conversational text + optional images.
- Default tools (when `tools` omitted): `google_search`, `url_context`, `code_execution`. Plan: leave defaults on.
- Two agent IDs: `deep-research-preview-04-2026` (DR) and `deep-research-max-preview-04-2026` (DR Max).
- Pricing per `ref-gemini-deep-research-api.md` §Estimated costs:
  - DR: ~80 search queries, ~250k input tokens (50–70% cached), ~60k output tokens → **~$1.00–$3.00 per task**
  - DR Max: ~160 search queries, ~900k input tokens (50–70% cached), ~80k output tokens → **~$3.00–$7.00 per task**

---

## 3. Stream A — Phase E Research Execution Plan

### Source of topics

Verbatim from `prj-knowledge-loop-consumer.md` §Phase E "Topics to research before scoping Phase E" (1–7).

### Routing table (seven runs after refactoring)

Topic 1 splits in two (Sean's Round-2 feedback called for explicit CLI repo audit beyond the MCP-only framing). Topic 6 is reframed and merged into topic 4 (Sean's Round-2 feedback: don't research what Block permits, but DO research which keys exist for each service and where to generate them — that's a public matrix and belongs inside the topic-4 DR Max call).

| # | Topic (paraphrased) | Tool | Why this tier | Predicted cost | Predicted wall time |
|---|---|---|---|---|---|
| **1a** | **MCP / SDK toolkit survey:** catalog `mcp-cli`, `mcp-bridge`, `mcp-proxy`, third-party MCP gateways (e.g., MCP-Hub patterns), and Anthropic Agent SDK features added since 0.1.63 (current pin) that bear on headless tool access. For each: license, last-commit recency, open-issue velocity, headless-friendliness | **Local LDR** | Open-source landscape with strong public coverage; 14B can synthesize a tools-survey table from SearXNG hits. Low recency requirement. | **$0.00** | 5–12 min |
| **1b** | **CLI-driven agentic-workflow repo audit + pinning patterns + Gemini CLI extensions:** evaluate `https://github.com/jackwener/OpenCLI.git` and `https://github.com/google-gemini/gemini-cli.git` for license, maintenance signal, security-review surface (does the repo execute model-output as code?), and fit for invocation from a Python wrapper script per the `gemini-image-gen` skill pattern. Catalog Gemini CLI extensions from `https://geminicli.com/extensions/` for research / agentic-workflow / data-tooling relevance — including any Deep Research extension. Document patterns for pinning/vendoring third-party CLI repos (git submodule pinned to commit SHA, `pip install git+url@sha`, vendored-copy approach used by `last30days/scripts/lib/vendor/bird-search/`) so a repo update doesn't break Sean's workflow | **Local LDR** | GitHub repo / docs synthesis; SearXNG handles GitHub well. If local output is thin on the Gemini CLI extensions catalog (which lives behind a JS-rendered gallery page that SearXNG may not index well), escalate to Gemini DR ($1–3) on retry. | **$0.00** (with possible $1–3 escalation) | 5–12 min |
| **2** | Anthropic API "MCP connector" mode (`mcp_servers` parameter, headless `claude login` OAuth inheritance) | **Gemini Deep Research** | API-doc heavy + 2026-recent; 14B's training cutoff and SearXNG's general index are weaker on fast-moving Anthropic API changes than Gemini DR's grounded Google-Search path. Single-tier escalation justified; DR Max overkill. | **$1.00–$3.00** | 5–20 min |
| **3** | Open-source model tool-calling (Qwen3-14B, Phi-4, Gemma 4 OpenAI-format function calling; bypass-MCP vs in-process MCP vs OS-model MCP patterns) | **Local LDR** | Same family as 1a — public docs + GitHub issue threads, well-indexed by SearXNG. Defer escalation to DR if local output is thin. | **$0.00** (with possible $1–3 escalation) | 5–12 min |
| **4 (absorbs 6)** | **Comprehensive auth-mode + key-generation matrix** for each of Slack, Google Calendar, Gmail, Jira, Confluence, GitHub, Linear. Six axes per service: (a) all available auth modes (PAT, OAuth refresh token, OAuth user token, OAuth bot token, service account with/without domain-wide delegation); (b) **generation URL/path** for each (e.g., `https://github.com/settings/tokens` for GitHub PATs); (c) scope/permission picker mechanics; (d) rotation/expiration model (default lifetime, programmatic rotation availability); (e) headless-friendliness (works without browser-redirect handling?); (f) typical admin restrictions (which modes commonly require workspace-admin enablement). Output ranks the headless-friendliest path per service. Cite official docs for each mode. | **Gemini Deep Research Max** | This is the 7-service × ~5-mode × 6-attribute matrix DR Max is literally pitched for ("nightly cron job triggering exhaustive due diligence reports"). Local LDR's 2-iteration / 5-results-per-query budget would produce a thin matrix; DR Max consults ~160 search queries per task and weighs conflicting evidence. The single load-bearing answer of Phase E — **Sean uses this output to decide which keys to try generating; Block IT permission discovery is a separate manual step Sean handles outside the agent fleet** (try → if blocked, ask the lead developer). | **$3.00–$7.00** | 20–60 min |
| **5** | Local MCP gateway patterns (single process holding OAuth tokens once, serving multiple agents/clients via stdio) | **Local LDR** | Niche / community-maintained / well-covered in GitHub READMEs and a few blog posts. Local pass should land it. | **$0.00** | 5–12 min |
| **7** | Daily Driver cost-benefit. Frame as: *"Across published case studies of personal autonomous-agent fleets in 2025–2026, what ROI is reported for adding read-only access to Slack/Calendar/Gmail vs. retaining manual handoff?"* — the *external* lens. The *internal* decision lens (worth Sean's 15h+) stays Sean's. | **Local LDR** | Cheap external-lens framing; Gemini DR / DR Max would burn money on a question the model can't conclude. | **$0.00** | 5–12 min |

**Total predicted cost: $4.00–$10.00 (worst case).** Of which $4–10 is Gemini API spend (topic 2 + topic 4); $0 is local Mac Mini compute.

### Queue-load instructions (executed in Phase 4 of §6)

After Stream B Phase 0–3 ship (`GEMINI_API_KEY` in Keychain, helper script + skill in place):

1. Topics 1a, 1b, 3, 5, 7 → append to `vault/00_inbox/research-queue.md` under `## Pending`. Refined wording locked at queue time per the existing `deep-research-queue` skill rules. Use the verbatim wording from §3 routing-table column 2 (the long-form prompts include the exact GitHub URLs and comparison rubrics LDR needs to ground the synthesis).
2. Topic 2 → append to the new `vault/00_inbox/gemini-research-queue.md` with `tier: dr` marker.
3. Topic 4 → append to `vault/00_inbox/gemini-research-queue.md` with `tier: dr-max` marker. Wording must include all six axes from the routing table (auth modes, generation URLs, scope mechanics, rotation, headless-friendliness, admin restrictions) — DR Max output quality scales with prompt-precision.
4. Topic 6 → does not exist as standalone (folded into Topic 4 per Sean's Round-2 reframing). The Block-permission discovery step is a Sean-side manual workflow: Sean reads Topic 4's matrix, picks a target auth mode, attempts to generate the key, and if blocked asks the lead developer. Document this explicitly in the Topic 4 report's "Recommended Next Steps" section so future-Sean has the workflow inline.

### Vault landing for Stream A reports

- Topics 1, 3, 5, 7 → `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` with `source: ldr-local` (existing pattern).
- Topics 2, 4 → `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` with `source: gemini-deep-research` or `source: gemini-deep-research-max`. **Same directory** so `grep -l 'phase-e' vault/20_projects/research/` finds all Stream A outputs in one shot. Frontmatter discrimination handles the comparison.

### Total budget for Stream A

- Local: **5 nights** × ~10 min Mac Mini compute = ~50 min runtime. **$0.**
- Gemini DR: 1 task. **$1–3.**
- Gemini DR Max: 1 task. **$3–7.**
- **Sum: $4–10.** Hard cap: enforce `[gemini.budget].max_per_task_usd = 7` and `[gemini.budget].monthly_cap_usd = 20` in config — prevents accidental fan-out (see §8 Cost Model).
- Stream A wall time: **5 nights** (1a, 1b, 3, 5, 7 process one-per-night through `deep_researcher` 02:45 schedule; topics 2 and 4 fire same-day via interactive skill or manual `gemini_researcher --mode oneshot`). Pre-read assembly: night 6.

---

## 4. Stream B — Gemini DR Integration Architecture

### Chosen shape: Skill (primary) + Autonomous SDK agent (secondary, default-disabled) + DEFER MCP wrapper to v2

Specifically:

1. **`.claude/skills/gemini-deep-research/SKILL.md`** — interactive entrypoint. Triggered by phrases like "deep research", "gemini research", "comprehensive analysis with citations", "due diligence on X", or any question Sean explicitly tags `--gemini`. Skill calls Bash → `agents-sdk/.venv/bin/python3 agents-sdk/scripts/gemini_dr.py "..." --tier {dr|max}`. Skill MUST gate DR Max calls behind `AskUserQuestion` showing predicted cost ($3–7). Skill MUST refuse if month-to-date Gemini spend ≥ `monthly_cap_usd`.
2. **`agents-sdk/scripts/gemini_dr.py`** — Python helper. Loads `GEMINI_API_KEY` via `lib.keychain.get_credential("gemini_api_key")`. Calls Gemini Interactions API with `background=True`, polls every 10s, writes ledger entry on success. Reads/writes `vault/health/gemini-spend-{YYYY-MM}.json` for cap enforcement. Writes report to `vault/20_projects/research/{date}-{slug}.md`. Reused by both the skill (interactive) and the agent (scheduled).
3. **`agents-sdk/agents/gemini_researcher.py`** — autonomous SDK agent, **default disabled** in `config.toml` (`enabled = false`). When enabled, reads `vault/00_inbox/gemini-research-queue.md`, picks first unchecked, calls into `gemini_dr.py` shared library functions, marks done. Mirrors `deep_researcher.py` structure (no Claude SDK loop — Gemini IS the synthesis engine).
4. **launchd plist `agents-sdk/schedules/com.sean.agent.gemini-researcher.plist`** — committed to repo, **NOT loaded** by default. Schedule `03:30` daily. Documented in `install_schedules.sh` as opt-in.

### Rejected alternatives

| Alternative | Why rejected |
|---|---|
| (a) **Skill alone (no agent, no helper script — pure Bash + curl in the skill body)** | Polling logic in Bash is fragile (timeout handling, JSON parsing, ledger writes); 60-min wall conflicts with Bash heredoc cleanliness; cost-cap math wants the typed structure of Python. |
| (b) **Agent alone (no skill — queue-only)** | Loses the interactive use case ("research this NOW with DR Max for tomorrow's stakeholder review"). The skill is the natural pair to the existing `deep-research-queue` skill — Sean expects symmetry. |
| (c) **stdio MCP server (port the LDR wrapper pattern to Gemini)** | **Deferred to v2.** Reasons: (1) Gemini DR's `mcp_server` tool requires *remote HTTP* endpoints (`url`, `headers`), not stdio — you can't put a stdio MCP behind it; (2) within Claude Code itself, an MCP-shaped Gemini call hides the cost-confirm prompt that DR Max needs; (3) the skill+Bash path delivers the same interactive access via a simpler call site. Revisit when Sean has a second consumer (e.g., Cursor) that wants Gemini DR via MCP. |
| (d) **Combination of MCP + skill + agent** | Scope creep for v1; ship the skill+agent path first, observe usage, then add MCP if a second consumer demands it. |

### Files-to-create / files-to-modify table

| File | Type | Phase | Notes |
|---|---|---|---|
| `.claude/skills/gemini-deep-research/SKILL.md` | NEW | 2 | Interactive primary; full spec in §7 |
| `.claude/skills/gemini-deep-research/decision-table.md` | NEW | 2 | Routing decision content the skill loads (last30days vs deep-research-queue vs DR vs DR Max) |
| `agents-sdk/scripts/gemini_dr.py` | NEW | 1 | Helper; reused by skill + agent |
| `agents-sdk/agents/gemini_researcher.py` | NEW | 3 | Autonomous queue agent (default disabled) |
| `agents-sdk/schedules/com.sean.agent.gemini-researcher.plist` | NEW | 3 | launchd schedule, 03:30 daily, NOT loaded by default |
| `agents-sdk/tests/test_gemini_dr.py` | NEW | 1 | Mocks the `google.genai.Client`; verifies polling loop, ledger write, cap refusal, frontmatter shape |
| `agents-sdk/tests/test_gemini_researcher.py` | NEW | 3 | Mocks gemini_dr; verifies queue parsing, tier-marker extraction, marks-done writeback |
| `vault/00_inbox/gemini-research-queue.md` | NEW | 1 | Queue file with explicit `tier: dr` / `tier: dr-max` markers per line |
| `vault/health/gemini-spend-{YYYY-MM}.json` | NEW (created on first call) | 1 | Append-style ledger; cap-check reads sum(`tasks[*].cost_usd`) |
| `agents-sdk/config.toml` | MODIFY | 1 | Add `[agents.gemini_researcher]` (enabled=false), `[gemini]` block with budget caps + agent IDs + queue path |
| `agents-sdk/.venv` (`pip install google-genai`) | MODIFY (env) | 0 | Pin version; document in `agents-sdk/pyproject.toml` |
| `agents-sdk/pyproject.toml` | MODIFY | 0 | Add `google-genai = ">=2.0.0,<3.0.0"` (or whatever is current at exec time) |
| Keychain entry `com.sean.agents.gemini_api_key` | NEW | 0 | `python3 agents-sdk/lib/keychain.py set gemini_api_key '<key>'` |
| `vault/00_inbox/research-queue.md` | MODIFY | 4 | Append topics 1, 3, 5, 7 (Stream A queue load) |
| `CHANGELOG.md`, `CLAUDE.md`, `README.md` | MODIFY | 5 | Per §10 Mandatory Doc Updates |
| `scripts/validate.py` | RUN (no edit) | 5 | Confirm 0 errors after count bumps |
| `export-groups/02-pm-workflows/playground.json` | MODIFY | 5 | Add `"gemini-deep-research"` (alphabetical sibling to `"deep-research-queue"` and `"research-synthesis"`) |

---

## 5. Stream C — `last30days` Composition Decision

**Decision: keep standalone, do not fold in, do not chain by default.**

### Rationale

`last30days` answers a fundamentally different question than LDR or Gemini DR:

| Skill | Question type | Window | Sources | Output flavor |
|---|---|---|---|---|
| `last30days` | "What are people *saying* about X?" — social signal, recency | Last 30 days (configurable `--days=N`) | Reddit, X, YouTube, TikTok, Instagram, HN, Polymarket, Bluesky, Truth Social, web | Trend brief with engagement metrics |
| `deep-research-queue` (LDR) | "What is *true* about X based on authoritative public web sources?" — synthesis | All time | SearXNG (general web) | Topical report with citations |
| `gemini-deep-research` (DR / DR Max) | Same as LDR but cloud-grounded with bigger search budget + matrix synthesis | All time | Google Search + URL Context + optional MCP / files | Long-form report with optional charts |

Last30days is **complementary, not competitive**. It surfaces "what's hot on Reddit this week"; the LDR/Gemini path produces "what does the literature say." Different shaped answers, different consumption patterns, different output destinations (`~/Documents/Last30Days/` vs `vault/20_projects/research/`).

### What we explicitly DO NOT do in v1

- **Do not chain** `last30days` → `gemini-deep-research` automatically (e.g., last30days produces trending sources → DR consumes them as URL Context). Tempting, but: (a) doubles the per-question wall time, (b) confuses cost forecasting, (c) cross-platform engagement noise leaks into authoritative-source synthesis. Document as a **v2 candidate**: a wrapper skill `trending-deep-research` that does last30days → harvest top URLs → pass to Gemini DR with `url_context` + `mcp_server` tools. Not in this plan.
- **Do not deprecate** any of the three skills. All three live alongside.

### What we DO do

Add a 1-line cross-reference to the new `gemini-deep-research` skill's `decision-table.md` directing Claude to last30days for trend questions, and a sibling note in the existing `last30days` SKILL.md (1-line, end of "When to Queue vs Answer in Session"-equivalent section) directing Claude to `gemini-deep-research` for citation-grounded synthesis. **Two 1-line edits, no logic changes.**

---

## 6. Phased Execution Plan

Each phase: **Goal · Steps · Test · Time · Rollback.**

### Phase 0 — Discovery + auth setup + ecosystem inventory (35 min)

- **Goal:** Confirm preconditions for the Gemini path; stash `GEMINI_API_KEY` in Keychain; pin `google-genai` SDK in `agents-sdk/.venv`. Also: inventory Sean's existing Gemini CLI install + extensions so future v2 swap to a CLI-extension-based path is informed (Sean's Round-2 ask: he has Gemini CLI installed and uses it for `gemini-image-gen`); decide whether to also stash `OPENAI_API_KEY` (Sean's Round-2 ask: low-stakes optional add for `last30days` Reddit-discovery fallback).
- **Steps:**
  1. Verify Mac Mini schedule conflict check: `launchctl list | grep com.sean` (expect 12 plists; 11 loaded). Confirm 03:30 slot is unclaimed; record in `vault/90_system/agent-logs/gemini-baseline-2026-MM-DD.txt`.
  2. Verify `agents-sdk/.venv/bin/python3 -c "import google.genai"` fails (precondition: not yet installed).
  3. Install: `cd agents-sdk && uv pip install "google-genai"`. Pin the resolved version in `pyproject.toml` under `[project.dependencies]` as `google-genai = ">=X,<Y"` where X/Y are the resolved major.
  4. Stash key: Sean obtains a Gemini API key from `aistudio.google.com` (paid tier — DR is paid-tier-only per `ref-deep-research-max-gemini.md`). Then `python3 agents-sdk/lib/keychain.py set gemini_api_key '<key>'`.
  5. Confirm: `python3 agents-sdk/lib/keychain.py get gemini_api_key | head -c 5` echoes the key prefix.
  6. Document the resolved `google-genai` version + install date in `vault/90_system/agent-logs/gemini-baseline-{date}.txt`.
  7. **Gemini CLI ecosystem inventory (NEW per Sean's Round-2):**
     - `gemini --version` — record version. Compare against the upstream `https://github.com/google-gemini/gemini-cli.git` HEAD commit date to flag staleness.
     - `gemini extensions list` — capture full list. Any extension whose name or description contains "research", "deep", "search", or "browse" is a v2-candidate alternate path to Gemini DR. Record each finding in the baseline file with: extension name, version, what it claims to do, whether it appears to wrap the Interactions API or uses a different endpoint.
     - If a Deep Research–shaped extension exists: append a §11 line "v2 candidate: swap `gemini_dr.py` direct API path for `gemini extensions run <ext-name>` per the `gemini-image-gen` CLI-wrap pattern; advantage = inherits Gemini CLI's existing auth (no separate Keychain entry); disadvantage = less control over polling / cost gating / ledger." Do NOT swap in v1 — direct SDK path keeps cost gating tight.
     - Browse `https://geminicli.com/extensions/` manually (page is JS-rendered; SearXNG can't reliably index it — a one-time manual look is cheaper than escalating Topic 1b to Gemini DR). Note any extension Sean wants flagged for the Topic 1b LDR run prompt.
  8. **OpenAI key handling (NEW per Sean's Round-2):**
     - `python3 agents-sdk/lib/keychain.py list | grep openai` — if `openai_api_key` already exists, `last30days` already has its Reddit-discovery fallback; nothing to add.
     - If absent and Sean already has an OpenAI key from another use: `python3 agents-sdk/lib/keychain.py set openai_api_key '<key>'`. `last30days` reads `OPENAI_API_KEY` per `last30days/SKILL.md:22`; the Keychain entry will need to be exported as an env var by the script that invokes last30days (out of scope for this plan — last30days runs interactively via Sean's shell env, not via this plan's Python helpers).
     - If Sean does NOT have an OpenAI key: skip. Adding one purely for last30days's secondary Reddit-discovery path (when ScrapeCreators is unset, which it is not — Sean already has SC per the v3.12.0 setup) is premature.
- **Test:** `agents-sdk/.venv/bin/python3 -c "from google import genai; c=genai.Client(); print(c)"` exits 0 with a Client repr (no API call yet). Baseline file at `vault/90_system/agent-logs/gemini-baseline-{date}.txt` has: `gemini --version` output, `gemini extensions list` output, OpenAI-key disposition note.
- **Time:** 35 min (was 20 min before the inventory + OpenAI steps).
- **Rollback:** `python3 agents-sdk/lib/keychain.py delete gemini_api_key && uv pip uninstall google-genai`. No vault writes (the baseline file is append-only diagnostic; safe to leave); no schedule changes.

### Phase 1 — `gemini_dr.py` helper + ledger + queue file + config block (3.5 hours)

- **Goal:** A self-policing Python helper that calls Gemini DR / DR Max via the Interactions API with background polling, writes a topical report to the vault, updates the spend ledger, and refuses when caps are hit. Used by both the skill (Phase 2) and the agent (Phase 3).
- **Steps:**
  1. Create `agents-sdk/scripts/gemini_dr.py` with argparse interface: `--query "..."`, `--tier {dr,max}`, `--dry-run`, `--no-confirm` (default: prompt before DR Max), `--output-dir vault/20_projects/research`, `--ledger vault/health/gemini-spend-{YYYY-MM}.json`, `--max-poll-seconds 3900` (65 min hard wall — beats Gemini's 60 min ceiling + 5 min cushion).
  2. Helper responsibilities:
     a. Load config + Keychain key.
     b. Read this month's ledger; sum `cost_usd`; refuse if `monthly_cap_usd` (config) is hit. Predict cost from tier (DR: $2 midpoint; DR Max: $5 midpoint). Refuse if `(month_to_date + predicted) > monthly_cap_usd`.
     c. Call `client.interactions.create(input=query, agent="deep-research-preview-04-2026" or "deep-research-max-preview-04-2026", background=True, agent_config={"type": "deep-research", "thinking_summaries": "auto"})`.
     d. Poll `client.interactions.get(id)` every 10s; abort at `max_poll_seconds`; capture `interaction.outputs[-1].text` on `status == "completed"`; surface `interaction.error` on `failed`.
     e. Slugify query; write `vault/20_projects/research/{YYYY-MM-DD}-{slug}.md` with frontmatter `source: gemini-deep-research[-max]`, `cost_usd: <reported or estimated>`, `wall_seconds`, `interaction_id`, `agent_id`, `created`. Body: the report text.
     f. Inject one-line digest into today's daily note under `<!-- research-digest -->` via `lib/vault_io.inject_at_anchor` (existing helper).
     g. Append to ledger atomically (read → mutate → tmp-then-rename).
     h. Log run via `lib.logging_setup.record_run`.
  3. Create `vault/00_inbox/gemini-research-queue.md` with header + `## Pending` + empty `## Done` sections. Format: `- [ ] {tier: dr|max} {refined question}` per line.
  4. Add to `agents-sdk/config.toml`:
     - New section `[gemini]`: `agent_id_dr = "deep-research-preview-04-2026"`, `agent_id_max = "deep-research-max-preview-04-2026"`, `default_tier = "dr"`, `poll_interval_seconds = 10`, `max_poll_seconds = 3900`, `output_dir = "vault/20_projects/research"`, `output_anchor = "research-digest"`, `ledger_dir = "vault/health"`.
     - New section `[gemini.budget]`: `max_per_task_usd = 7.00`, `monthly_cap_usd = 20.00`, `dr_predicted_usd = 2.00`, `max_predicted_usd = 5.00`.
     - New section `[agents.gemini_researcher]`: `enabled = false`, `queue_path = "vault/00_inbox/gemini-research-queue.md"`, `max_budget_usd = 0.00` (decorative — real cap is `[gemini.budget]`).
  5. Create `agents-sdk/tests/test_gemini_dr.py` with mocked `google.genai.Client`. Tests: argparse shape, slug derivation, frontmatter shape, ledger append, cap-refusal at month-to-date threshold, polling-loop happy path, polling-loop timeout path, frontmatter source field per tier, `--dry-run` writes nothing.
- **Test:**
  - `agents-sdk/.venv/bin/python3 agents-sdk/scripts/gemini_dr.py --query "test" --tier dr --dry-run` — prints intended call, exits 0, no vault writes, no API call.
  - `pytest agents-sdk/tests/test_gemini_dr.py -v` — all green.
  - `python3 scripts/validate.py` — exits 0.
- **Time:** 3.5 hours (helper: 2.5h · queue file + config: 0.5h · tests: 0.5h).
- **Rollback:** `git restore agents-sdk/config.toml && rm agents-sdk/scripts/gemini_dr.py agents-sdk/tests/test_gemini_dr.py vault/00_inbox/gemini-research-queue.md`. No external state.

### Phase 2 — `gemini-deep-research` skill (2 hours)

- **Goal:** Interactive entrypoint. Sean says "deep research" / "gemini research" / etc., Claude loads the skill, walks the decision tree, prompts for tier confirmation, invokes `gemini_dr.py` via Bash. Skill spec in §7.
- **Steps:**
  1. Create `.claude/skills/gemini-deep-research/SKILL.md` per §7 spec (full frontmatter + body).
  2. Create `.claude/skills/gemini-deep-research/decision-table.md` — routing rules (last30days vs deep-research-queue vs DR vs DR Max) + cost expectations + 3 worked examples.
  3. Add 1-line cross-reference to `.claude/skills/last30days/SKILL.md` (end of skill body, "## Related" section if present, else append): "For citation-grounded synthesis questions (not social-trend questions), see `gemini-deep-research`."
  4. Add 1-line cross-reference to `.claude/skills/deep-research-queue/SKILL.md` (existing "## Related" section): "For paid cloud research (Gemini DR / DR Max) when local LDR is too thin, see `gemini-deep-research`."
- **Test:**
  - In a fresh interactive Claude Code session in this repo, ask: *"Run a Gemini deep research on the LDR project's release cadence over the last year."* — Claude must (a) load the skill, (b) classify as DR (not DR Max), (c) NOT prompt for cost confirmation (DR is below the confirmation threshold), (d) invoke `gemini_dr.py --tier dr`, (e) wait for completion, (f) confirm vault landing path back to Sean.
  - In a second session: *"Run a Gemini Deep Research Max on competitive landscape of cloud GPUs."* — Claude must (a) load skill, (b) classify DR Max, (c) **PROMPT with AskUserQuestion** showing predicted $5 cost + 20–60 min wall, (d) on YES, invoke `gemini_dr.py --tier max`.
  - In a third session: ask a social-media-trend question (e.g., *"What's people saying about Claude Code skills on Reddit this week?"*) — Claude routes to `last30days`, NOT to `gemini-deep-research`.
- **Time:** 2 hours.
- **Rollback:** `rm -rf .claude/skills/gemini-deep-research/` and `git restore .claude/skills/last30days/SKILL.md .claude/skills/deep-research-queue/SKILL.md`.

### Phase 3 — `gemini_researcher.py` autonomous agent + plist (default disabled) (3 hours)

- **Goal:** Autonomous queue agent that processes `vault/00_inbox/gemini-research-queue.md` via the existing helper. Default disabled — Sean opts in by editing `config.toml` and running `launchctl load`.
- **Steps:**
  1. Create `agents-sdk/agents/gemini_researcher.py`. Mirror `deep_researcher.py` structure: argparse with `--mode {queue,oneshot}`, `--query`, `--tier {dr,max}`, `--dry-run`. Logic: read queue, parse first unchecked, extract `tier:` marker (default `dr`), call `gemini_dr.py` shared functions (NOT subprocess — import directly), mark done with timestamp + wikilink. Honor `[agents.gemini_researcher].enabled`.
  2. Create `agents-sdk/schedules/com.sean.agent.gemini-researcher.plist`. `StartCalendarInterval` `Hour=3 Minute=30`. `EnvironmentVariables` `PATH=/Users/seanwinslow/.local/bin:/opt/homebrew/bin:...` per CLAUDE.md launchd-PATH requirement. `WorkingDirectory` repo root. `ProgramArguments`: `[agents-sdk/.venv/bin/python3, agents-sdk/agents/gemini_researcher.py, --mode, queue]`. `RunAtLoad=false`. **NOT loaded by default.**
  3. Update `agents-sdk/schedules/install_schedules.sh` to **EXCLUDE** `com.sean.agent.gemini-researcher.plist` from the bulk-load loop unless `INSTALL_GEMINI=1` env var is set. Document this in the script's comment header.
  4. Create `agents-sdk/tests/test_gemini_researcher.py` mocking `gemini_dr.run_research()`. Tests: queue parsing with tier marker, default tier when marker absent, empty-queue path (exit 0, history.csv `empty-queue` row), `enabled=false` path (exit 0, no work done), tier-marker passthrough.
  5. Schedule conflict check (final): document in `vault/90_system/agent-logs/gemini-schedule-check-{date}.txt`:
     - 02:00 vault-indexer (Mac Mini, ~15 min, frees 02:15) ✓
     - 02:45 deep-researcher (Mac Mini, 15-min cap, frees ≤03:00; gemini-researcher does NOT load a local model so no memory contention even if overlap occurred) ✓
     - 03:30 **gemini-researcher (NEW)** — pure cloud-API client, ~0.2 GB local memory, can run up to 65 min worst case (60 min API + 5 min cushion); finishes ≤04:35 worst case ✓
     - 06:30 meta-agent (Mac Mini, ~5 min) — clear 1h55m gap from worst-case gemini-researcher end ✓
     - 08:45 daily-driver morning — clear 4h15m gap ✓
     - **Verdict: 03:30 stays. Memory headroom math (macmini-migration §1) unchanged because gemini-researcher loads no local model.**
- **Test:**
  - `pytest agents-sdk/tests/test_gemini_researcher.py -v` — green.
  - `agents-sdk/.venv/bin/python3 agents-sdk/agents/gemini_researcher.py --mode queue --dry-run` — prints first queued item or "empty queue", no API call.
  - `launchctl list | grep gemini` — empty (default not loaded). Manually load via `launchctl load ~/Library/LaunchAgents/com.sean.agent.gemini-researcher.plist` ONLY when Sean opts in; verify with `launchctl list | grep gemini` returning one line.
- **Time:** 3 hours.
- **Rollback:** `git restore agents-sdk/agents/gemini_researcher.py agents-sdk/schedules/com.sean.agent.gemini-researcher.plist agents-sdk/schedules/install_schedules.sh agents-sdk/tests/test_gemini_researcher.py`. If user opted in: `launchctl unload ~/Library/LaunchAgents/com.sean.agent.gemini-researcher.plist && rm ~/Library/LaunchAgents/com.sean.agent.gemini-researcher.plist`.

### Phase 4 — Stream A queue load + monitored execution (5 nights of compute, ~40 min Sean-time)

- **Goal:** Get all seven Phase E research runs (1a, 1b, 2, 3, 4, 5, 7) into queues; monitor first execution; capture cost actuals.
- **Steps:**
  1. Append topics 1a, 1b, 3, 5, 7 to `vault/00_inbox/research-queue.md` `## Pending` per the verbatim long-form wording in §3 routing-table column 2. Use the `deep-research-queue` skill (canonical write path). Order matters — `deep_researcher` picks first-unchecked, so order shapes the 5-night cadence.
  2. Append topic 2 to `vault/00_inbox/gemini-research-queue.md` `## Pending` with `tier: dr` marker.
  3. Append topic 4 to `vault/00_inbox/gemini-research-queue.md` `## Pending` with `tier: dr-max` marker. **Topic 4 is the load-bearing call** — confirm prompt wording captures all six axes before queuing.
  4. **Night 1 (LDR + DR same day):**
     - `launchctl start com.sean.agent.deep-researcher` — local LDR processes topic 1a. Verify next morning: new file at `vault/20_projects/research/` with `source: ldr-local`; queue line marked `[x]`.
     - In parallel (cloud, no Mac Mini contention): `agents-sdk/.venv/bin/python3 agents-sdk/agents/gemini_researcher.py --mode oneshot --query "<topic 2 wording>" --tier dr` — synchronous run, watch polling output, confirm cost ≤ $3, verify vault file with `source: gemini-deep-research`.
  5. **Night 2 (LDR + DR Max with manual confirmation):**
     - Topic 1b auto-fires via 02:45 schedule.
     - Sean manually invokes the `gemini-deep-research` skill in an interactive session for topic 4 (DR Max). Walk through the `AskUserQuestion` cost-confirm flow — this validates the skill's user-facing path. Expected: 20–60 min wall, $3–7 cost.
  6. **Night 3:** Topic 3 (LDR) auto-fires.
  7. **Night 4:** Topic 5 (LDR) auto-fires.
  8. **Night 5:** Topic 7 (LDR) auto-fires.
  9. After all 7 land, produce a 1-page Phase E pre-read at `vault/20_projects/prj-superuser-pack/phase-e-research-prereads-2026-MM-DD.md` linking to all seven reports. Group by question shape: §"Tooling landscape" (1a + 1b), §"Anthropic API + OS-model tool-calling" (2 + 3), §"Cross-service auth matrix" (4), §"Gateway pattern" (5), §"Cost-benefit external lens" (7). **This is the artifact Sean reads on or after 2026-05-15** when revisiting Phase E scoping.
- **Test:**
  - `find vault/20_projects/research -newer vault/00_inbox/research-queue.md -name '2026-*.md'` returns 7 reports (5 LDR + 2 Gemini).
  - Both queues' `## Pending` sections empty; `## Done` sections each have appropriate entries with timestamps + wikilinks.
  - `vault/health/gemini-spend-{YYYY-MM}.json` shows 2 task entries totaling $4–10.
  - The Phase E pre-read artifact exists and links to all seven reports.
- **Time:** 40 min Sean active time across 5 days (mostly night 2 DR Max walkthrough); 5 days of overnight compute.
- **Rollback:** Topics can be re-queued by re-uncheck-ing them. Cost is sunk — Gemini API spend is non-refundable. No code rollback needed; this is data execution.

### Phase 5 — Mandatory doc updates + validation (45 min)

- **Goal:** Ship the v3.24.0 release notes and update all required cross-references.
- **Steps:**
  1. `CHANGELOG.md`: new `## [3.24.0] - 2026-MM-DD` section per §10 below.
  2. `CLAUDE.md`: skill count `115 → 116`; add a `Gemini Researcher` row to the active-SDK-agents table marked as "default disabled" (active count stays 7); architecture comment skill count `(115 skills) → (116 skills)`; add a 1-paragraph note under "Connected MCPs" or a new "Connected External Research APIs" section documenting Gemini DR availability + cost gating.
  3. `README.md`: header line `115 skills` → `116 skills`; Agent table row updates if any.
  4. `export-groups/02-pm-workflows/playground.json`: append `"gemini-deep-research"` (alphabetical insertion sibling to `"deep-research-queue"` and `"research-synthesis"`).
  5. `python3 scripts/validate.py` — confirm 0 errors.
  6. `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -v` — confirm full suite green.
- **Test:** Counts match across the 3 doc files; validator passes; pytest passes.
- **Time:** 45 min.
- **Rollback:** `git restore CHANGELOG.md CLAUDE.md README.md export-groups/02-pm-workflows/playground.json`.

### Phase 6 — End-to-end smoke test + Phase E pre-read assembly (45 min)

- **Goal:** Final pass on the full chain. See §12 Verification for the runnable sequence.
- **Steps:** Per §12 Verification.
- **Test:** All §12 steps pass binary.
- **Time:** 45 min.
- **Rollback:** N/A (verification only).

### Time totals

- Phase 0: 35 min (was 20 min — added Gemini CLI inventory + OpenAI key check)
- Phase 1: 3.5 hr
- Phase 2: 2 hr
- Phase 3: 3 hr
- Phase 4: 40 min Sean-time + 5 days overnight
- Phase 5: 45 min
- Phase 6: 45 min
- **Engineering total: ~11 hours.** Stream A wall time: 5 days. Total active Sean time including Phase 4 monitoring: ~12 hours.

---

## 7. New Skill Specs

### `.claude/skills/gemini-deep-research/SKILL.md`

```yaml
---
name: gemini-deep-research
description: Invoke Google's Gemini Deep Research or Deep Research Max APIs for paid, comprehensive research with web grounding, citations, and optional charts. Use when Sean asks for "deep research", "gemini research", "deep research max", "comprehensive analysis with citations", "due diligence on X", or surfaces a question that needs ≥20 sources cross-referenced, recent (post-2025) authoritative content, or a structured matrix that the local LDR + Qwen3-14B path can't produce reliably. Skip for simple lookups (answer in-session), social-media trend questions (use last30days), or questions answerable by the local deep-research-queue at $0/run. Always prompts for cost confirmation before invoking Deep Research Max ($3-7/task).
allowed-tools: Bash, Read, Edit, AskUserQuestion
---
```

**Body sections (concrete content, not placeholders):**

1. **When to use this skill vs. the alternatives.** Decision table loaded from `decision-table.md`:
   | Question shape | Tool | Cost | Wall |
   |---|---|---|---|
   | "What's hot on Reddit / X / TikTok about X this week?" | `last30days` | $0 (or SC API) | 2–8 min |
   | "What are the practical differences between A and B?" with general web coverage | `deep-research-queue` (LDR) | $0 | 5–12 min overnight |
   | "Recent (post-2025), authoritative, ≥10 sources, citation quality matters" | **`gemini-deep-research` DR tier** | $1–3 | 5–20 min |
   | "Cross-service matrix / due-diligence / comprehensive landscape" | **`gemini-deep-research` DR Max tier** | $3–7 | 20–60 min |

2. **Tier picker.** When the user's request maps to DR or DR Max, surface the predicted cost AND ask via `AskUserQuestion`:
   - DR: predicted $2 (range $1–3). No confirmation needed if `[gemini.budget].monthly_cap_usd` headroom > $5.
   - DR Max: predicted $5 (range $3–7). **MANDATORY** `AskUserQuestion` confirmation showing predicted cost + estimated wall time + month-to-date Gemini spend.

3. **How to invoke.** `Bash`-call `agents-sdk/.venv/bin/python3 agents-sdk/scripts/gemini_dr.py --query "<refined question>" --tier {dr|max}`. The helper handles polling, ledger, vault landing.

4. **What happens after.** Report lands at `vault/20_projects/research/{date}-{slug}.md` with `source: gemini-deep-research[-max]` frontmatter; daily-note digest under `<!-- research-digest -->`.

5. **Cost-cap behavior.** If month-to-date spend ≥ `monthly_cap_usd` ($20 default), the helper REFUSES the call and exits non-zero. The skill must surface the refusal and offer alternatives (queue to local `deep-research-queue` instead, or ask Sean to raise the cap in `config.toml`).

6. **Refusal cases.** Skill MUST decline (return without invoking) when:
   - Question is a single-fact lookup → suggest in-session WebSearch.
   - Question is about social-media trends → route to `last30days`.
   - Cost cap is hit and user declines to raise it.
   - User declines DR Max confirmation prompt.

7. **Allowed tools rationale.** `Bash` to invoke the helper · `Read` to inspect the ledger and queue files · `Edit` to append to `gemini-research-queue.md` if the user asks to queue rather than run-now · `AskUserQuestion` for the DR Max cost confirmation.

8. **Related.**
   - `deep-research-queue` — sibling for $0 local LDR queue.
   - `last30days` — sibling for social-trend questions.
   - `agents-sdk/scripts/gemini_dr.py` — the actual runner.
   - `vault/health/gemini-spend-{YYYY-MM}.json` — the spend ledger.

### `.claude/skills/gemini-deep-research/decision-table.md`

A standalone reference file the skill reads on activation. Contains the decision table from §7.1, three worked examples (one per tool), and the cost-cap escape paths. Mirrors the OB1-inspired pattern of "skill body cites a separate reference file" used by `last30days/CLAUDE.md`.

---

## 8. Cost Model

### Per-call costs (from `ref-gemini-deep-research-api.md` §Estimated costs)

| Tier | Search queries | Input tokens | Output tokens | Cost range | Plan midpoint |
|---|---|---|---|---|---|
| Deep Research (`deep-research-preview-04-2026`) | ~80 | ~250k (50–70% cached) | ~60k | $1.00–$3.00 | **$2.00** |
| Deep Research Max (`deep-research-max-preview-04-2026`) | ~160 | ~900k (50–70% cached) | ~80k | $3.00–$7.00 | **$5.00** |

### Caps (config defaults)

| Cap | Value | Where enforced |
|---|---|---|
| Per-task ceiling | **$7.00** | `gemini_dr.py` predicts cost from tier midpoint × 1.4; refuses if estimate > `max_per_task_usd`. (Practical effect: blocks anything above DR Max's known ceiling.) |
| Daily cap | **$10.00** | Helper sums today's ledger entries; refuses if `(today_so_far + predicted) > daily_cap_usd`. |
| Monthly cap | **$20.00** | Helper sums month's ledger; refuses if `(mtd + predicted) > monthly_cap_usd`. **Hard kill switch.** |
| Mandatory confirm tier | DR Max | Skill MUST `AskUserQuestion` showing predicted cost before any DR Max call, even if all caps have headroom. |

### Worst-case scenario analysis

Sean queues 30 questions overnight with `tier: dr-max` markers, gemini-researcher fires at 03:30:

- **Without caps:** 30 × $7 = **$210** in one night.
- **With $20 monthly cap:** First 4 tasks succeed (~$20 mtd). 5th task refused. Remaining 25 stay in `## Pending`. **Damage capped at $20.**
- **With $10 daily cap:** 2 tasks succeed (~$10). 3rd refused. Remaining 28 stay queued. **Damage capped at $10/day.**

Combined effect: **the absolute worst case is one $7 task that exceeds the daily cap by $7 in one transaction**, since the cap-check predicts conservatively (1.4× midpoint) and refuses the next call. **Practical worst case: $10–14 in one day.**

### Kill switch

Three layers:

1. `[agents.gemini_researcher].enabled = false` in `config.toml` — instant agent disable. (Default: false.)
2. `[gemini.budget].monthly_cap_usd = 0` in `config.toml` — instant API disable for both skill and agent (helper refuses every call).
3. `python3 agents-sdk/lib/keychain.py delete gemini_api_key` — nuclear option; helper raises on credential lookup, no calls succeed.

### Alert triggers

The helper logs WARN to stderr (which `record_run` captures) when:
- `mtd_total > 0.7 * monthly_cap_usd` (warn at 70% of cap)
- A single task's actual cost exceeds 1.5× its tier midpoint (model-misclassification or pricing-change signal)

Daily-driver morning brief surfaces `mtd_total` from `gemini-spend-{YYYY-MM}.json` alongside the existing synth-manifest line per the `agents-sdk/lib/lint_report.synth_health_summary` pattern. **NO extension to the cost-watchdog hook needed** — Gemini spend is a separate vendor and lives in its own ledger; the existing hook continues to watch only Anthropic spend.

### Stream A predicted spend (recap)

| Topic | Tier | Predicted cost |
|---|---|---|
| 1, 3, 5, 7 | Local LDR | $0.00 each |
| 2 | DR | $1.00–$3.00 |
| 4 | DR Max | $3.00–$7.00 |
| 6 | (skip) | $0.00 |
| **Total** | | **$4.00–$10.00** |

Comfortably below `monthly_cap_usd = $20` even at worst case.

---

## 9. Risks + Decision Points

### Risks

| Risk | Likelihood | Blast radius | Mitigation | Rollback |
|---|---|---|---|---|
| `google-genai` SDK schema change (Interactions API in public beta per Google's own docs) | Medium | Helper fails silently or with type errors | Pin SDK version in `pyproject.toml`; smoke-test on every upgrade; monitor Google's release notes | Revert to pinned version |
| Gemini API pricing changes between plan write (2026-05-03) and execution | Low | Cost predictions in helper drift from reality | `gemini_dr.py` reads tier midpoints from `[gemini.budget]`, not from code constants; one config edit corrects | Update `dr_predicted_usd` / `max_predicted_usd` in config.toml |
| Sean queues 30 DR-Max questions accidentally | Low | Daily cap stops at $10/day | Daily + monthly + per-task caps stack; agent processes one per night anyway | Edit queue to flip tier marker to `dr` or `--skip-` prefix |
| Helper writes corrupt ledger mid-run (process killed) | Low | Spend tracking off-by-one for that month | Atomic tmp-then-rename pattern; helper reads tolerantly (missing ledger = $0 mtd) | Manually edit JSON or delete; helper auto-recovers next run |
| `vault/00_inbox/gemini-research-queue.md` and `research-queue.md` confusion (Claude queues to wrong file) | Medium | Topic routes to wrong tool | Skill explicitly names the destination queue; queue files have distinct headers and frontmatter `type:` values | Move misplaced line to correct queue manually |
| 60-min API ceiling exceeded by DR Max on a complex matrix | Low | Single task fails; cost may still be charged | Helper polls up to 65 min; on timeout, logs partial state and raises; Sean retries with narrower scope | Re-queue with refined wording |
| Stream A topic 6 (Block IT posture) accidentally re-queued by future automation | Low | Wasted DR Max call on un-researchable question | Document the skip in the queue file's `## Done` section with explicit reason | Mark as `[skip]` not `[ ]`; add to `gemini_dr.py` ignore list |
| Daily-driver morning brief grows unbounded as ledger appends | Low | Cosmetic | Per-month ledger files; daily-driver reads only the current month | Delete old `gemini-spend-YYYY-MM.json` files |
| Scheduled gemini-researcher fires while Sean is asleep, hits a DR Max task that needs confirmation | Medium | Without `--no-confirm` agent would block forever; with `--no-confirm` skips the prompt | Agent runs with `--no-confirm` (default); cost gate is the per-task + daily caps, NOT user confirmation | Disable `[agents.gemini_researcher].enabled = false` |

### Genuine forks for Sean to decide before execution

- **D1 — Per-call cost ceiling: keep at $7 (DR Max range) or raise to $10 with safety margin?** Recommend **$7** (matches Google's published ceiling; a >$7 result is a pricing surprise that should fail loudly).
- **D2 — Monthly cap: $20 (proposed) or higher?** Plan-A allows **3 DR Max + 7 DR or 20 DR** per month. If Sean expects to use Gemini DR weekly, $20 is plenty. If he expects daily heavy use, raise to $50. Recommend **$20** for v1; revisit after 30 days of usage data in the ledger.
- **D3 — Default tier when skill is invoked without explicit tier marker?** Recommend **DR (cheaper)**, with Sean opting up to DR Max via "use DR Max" in the prompt or adding `tier: dr-max` to the queue line. The skill's `decision-table.md` codifies this.
- **D4 — Should the gemini-researcher autonomous agent ship enabled by default?** Recommend **disabled by default.** Sean must opt in by editing `config.toml` and `launchctl load`. Reduces blast radius of a queue-stuffing accident.
- **D5 — MCP composition (LDR or vault as `mcp_server` tool inside Gemini DR runs)?** **Defer to v2.** Reasoning written up in §4 "Rejected alternatives" (c). Concrete trigger to revisit: a second consumer (e.g., Cursor MCP client) demands Gemini DR access AND a remote-HTTP MCP gateway is independently justified.
- **D6 — Should the existing `last30days` skill be folded into a chained "trending-deep-research" wrapper in v1?** **No** — keep standalone (§5 decision). Revisit in v2 if usage shows Sean repeatedly chains them manually.
- **D7 — Add Perplexity API as a fourth research tier (alongside last30days / LDR / Gemini DR / Gemini DR Max)?** **Recommend SKIP for v1.** Reasoning: (1) Perplexity Deep Research's Sonar lineage is a different model family but produces output of comparable shape to Gemini DR — no documented gap in Gemini DR's coverage that Perplexity uniquely fills; (2) adding a fourth tier raises the per-call decision burden on Claude (4 tiers requires the skill to disambiguate at every invocation, blunting the quality-vs-cost rule); (3) `last30days` already gets Perplexity Sonar Pro coverage indirectly via OpenRouter (`OPENROUTER_API_KEY` route per `last30days/SKILL.md:162`) — that channel doesn't compete with Gemini DR for the synthesis tier. Concrete trigger to revisit: after 2+ weeks of Stream B usage, if ≥2 Gemini DR runs return demonstrably thin output that Perplexity would plausibly land. Then add as `--provider perplexity` flag on `gemini_dr.py` (rename helper to `cloud_dr.py`), not as a new skill.
- **D8 — Stash an `OPENAI_API_KEY` in Keychain for `last30days` Reddit-discovery fallback?** **Recommend OPTIONAL low-stakes add only if Sean already has an OpenAI key.** Reasoning: `last30days` reads `OPENAI_API_KEY` (per `last30days/SKILL.md:22`) but only as a fallback when `SCRAPECREATORS_API_KEY` is unset, which it isn't (Sean has SC per the v3.12.0 setup). The OpenAI path would only fire on SC outage. If Sean has a spare key from another use case (Codex, ChatGPT API access for other projects), 30 seconds to `keychain.py set openai_api_key '...'`. If not, skip — a key purely for this fallback-of-a-fallback is not worth the registration overhead.
- **D9 — Swap to a Gemini CLI extension–based Deep Research path instead of the direct `google-genai` SDK?** **Recommend SKIP for v1, decide in v2 based on Phase 0 inventory.** Reasoning: (a) Phase 0 step 7 will inventory whether such an extension exists today — if absent, the decision is moot; (b) if present, the CLI-wrap pattern per `gemini-image-gen` is appealing (inherits Gemini CLI auth, less SDK surface) but historically gives less control over polling, cost gating, and ledger writes — exactly the surfaces this plan needs strict; (c) v1 ships the direct SDK path with explicit per-task / daily / monthly caps, then v2 can swap if the Phase 0 inventory turns up a capable extension AND production usage shows the extension's auth model is meaningfully simpler.

---

## 10. Mandatory Doc Updates

Per CLAUDE.md non-negotiable §"When Modifying" — when adding any Skill, Agent, Sub-Agent, Hook, or Script.

| File | Specific change | Counts before → after |
|---|---|---|
| `CHANGELOG.md` | New `## [3.24.0] - 2026-MM-DD` section. **Added:** `gemini-deep-research` skill at `.claude/skills/gemini-deep-research/`; `gemini_researcher` SDK agent at `agents-sdk/agents/gemini_researcher.py` (default disabled); `gemini_dr.py` helper at `agents-sdk/scripts/`; `gemini-research-queue.md` at `vault/00_inbox/`; `gemini-spend-{YYYY-MM}.json` ledger at `vault/health/`; launchd plist at `agents-sdk/schedules/com.sean.agent.gemini-researcher.plist` (NOT loaded by default); Keychain entry `com.sean.agents.gemini_api_key`; `[gemini]` + `[gemini.budget]` + `[agents.gemini_researcher]` blocks in `agents-sdk/config.toml`; `google-genai` dep in `agents-sdk/pyproject.toml`. **Changed:** `last30days/SKILL.md` (1-line cross-ref), `deep-research-queue/SKILL.md` (1-line cross-ref). **Notes:** Stream A executed Phase E research at total cost $4–10. | n/a |
| `CLAUDE.md` | Header skill count `115 → 116`; architecture comment `(115 skills) → (116 skills)`; add `gemini_researcher` row to the active-SDK-agents table marked **disabled by default** (active SDK count stays at **7 active**, total grows `13 → 14`); add 1-paragraph "Cloud Research Tools" note under existing "Connected MCPs" section documenting Gemini DR availability + cost gating + skill name. | Skills: 115 → **116**. SDK agents (total): 13 → **14**. SDK agents (active): 7 → **7** (unchanged — new agent disabled by default). |
| `README.md` | Header line `115 skills, 13 Claude Code subagents, 13 hooks, 13 autonomous SDK agents (7 active)` → `**116** skills, 13 Claude Code subagents, 13 hooks, **14** autonomous SDK agents (7 active)`. Update agent table row count if present. | Skills: 115 → **116**. SDK agents: 13 → **14**. |
| `scripts/validate.py` | RUN after edits; expect 0 errors. The validator hard-enforces 3 primary domain folders + skill counts referenced in playground manifests. | n/a |
| `export-groups/02-pm-workflows/playground.json` | Append `"gemini-deep-research"` (alphabetical insertion sibling to `"deep-research-queue"` and `"research-synthesis"`). | One manifest entry. |
| `agents-sdk/pyproject.toml` | Add `google-genai = ">=X,<Y"` to `[project.dependencies]` with version pin resolved at Phase 0. | One dep. |
| `.claude/skills/last30days/SKILL.md` | One-line cross-ref to `gemini-deep-research`. | n/a |
| `.claude/skills/deep-research-queue/SKILL.md` | One-line cross-ref to `gemini-deep-research`. | n/a |

**Hooks: NO change** — the existing `cost-watchdog.sh` hook continues to watch Anthropic spend only. Gemini spend lives in its own per-month ledger written by `gemini_dr.py` and surfaced by daily-driver morning brief. Hook count stays **13**.

**Total artifacts touched by Phase 5:** 6 repo files + 1 export-group manifest + the new `pyproject.toml` line.

---

## 11. Out of Scope

Explicit non-goals so future-Sean doesn't think something was missed:

- **Modifying `deep_researcher.py` runtime behavior.** Per plan constraints. v3.23.0 is in soak; new agents are siblings, not refactors.
- **Re-enabling any disabled SDK agent** from `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`. Per CLAUDE.md non-negotiable.
- **Stdio MCP wrapper around Gemini DR** for Claude Code interactive sessions. Deferred to v2 — see §4 Rejected (c) and §9 D5.
- **Remote HTTP MCP gateway around LDR or vault** to use as an `mcp_server` tool inside Gemini DR runs. Deferred to v2 — §9 D5.
- **`trending-deep-research` chain skill** (last30days → harvest URLs → Gemini DR with `url_context`). Deferred to v2 — §5.
- **Visualization / chart generation** via Gemini DR's `visualization: "auto"` mode. Helper passes through any visualizations the API generates as base64 image blocks in the report file, but does NOT process or display them in v1. Future enhancement: render to inline `![image](attachments/...)` references and save companion files in `vault/20_projects/research/attachments/`.
- **`File Search` tool** to give Gemini DR access to vault docs. Real cost-benefit but requires uploading vault content to Google's file_search store; defer until a concrete use case demands it. v1 leaves Gemini DR's tool set at the defaults (`google_search`, `url_context`, `code_execution`).
- **Collaborative planning mode** (`collaborative_planning=true`) for multi-turn plan refinement before research. Useful for high-stakes DR Max calls; defer to v2 — adds 2 extra API round-trips and complicates the skill's UX.
- **Streaming output** to a Claude Code session via `stream=true`. The skill's interactive UX is "fire and wait"; streaming would change the call shape. v2 candidate.
- **Phase E itself.** This plan generates the *fact base* for Phase E (Stream A), not the Phase E implementation. Phase E scoping is a separate plan that future-Sean writes after reading the Stream A pre-read on or after 2026-05-15.
- **A URL-checker post-processor** for the Gemini path. Same risk as LDR (citation hallucination); same v1 stance — defer; treat reports as drafts.
- **Removing the LDR install or Mac Mini scheduled deep-researcher.** Both stay; Gemini is additive, not replacement.
- **Gemini cost metering on a per-skill / per-agent basis** beyond the single monthly ledger. v1 attributes all spend to "gemini" globally. Per-caller attribution is v2.
- **Perplexity Deep Research API integration as a fourth research tier.** Per §9 D7. Concrete trigger to revisit documented in D7.
- **Gemini CLI extension–based Deep Research path** as a v1 alternative to the direct `google-genai` SDK call. Per §9 D9. Phase 0 step 7 inventories the extension landscape; if a credible extension exists, it becomes a v2 swap candidate documented in `vault/90_system/agent-logs/gemini-baseline-{date}.txt`.
- **Auto-pinning third-party CLI repos** discovered by Topic 1b research. Pinning *patterns* are part of the research output (Topic 1b prompt explicitly requests them); actually adopting any specific repo + applying the pattern is a separate decision Sean makes after reading the Topic 1b report.
- **Independent verification of Block IT's permitted auth modes.** Per Sean's Round-2 reframing: this plan produces the Topic 4 matrix (which keys exist + where to generate them); Sean's manual workflow (try → if blocked, ask the lead developer) determines what's permitted. The agent fleet does not attempt to discover Block-internal policy.

---

## 12. Verification

End-to-end smoke test sequence, runnable post-Phase 5. Each step produces a binary pass/fail.

```bash
# 1. Repo-wide validator
python3 scripts/validate.py
# Expected: PASSED, 0 errors. Same baseline warning count as v3.23.0.

# 2. Full agents-sdk test suite (gains 2 new test files: test_gemini_dr, test_gemini_researcher)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 -m pytest tests/ -v
# Expected: all green. Pre-Stream-B count + ~25 new tests (gemini_dr ~15, gemini_researcher ~10).

# 3. Gemini SDK + auth smoke
agents-sdk/.venv/bin/python3 -c "from google import genai; from lib.keychain import get_credential; c = genai.Client(api_key=get_credential('gemini_api_key')); print('OK')"
# Expected: prints "OK". No API call.

# 4. Helper dry-run (DR tier, no API call, no vault writes)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/gemini_dr.py --query "smoke test" --tier dr --dry-run
# Expected: prints intended call (agent_id deep-research-preview-04-2026, predicted_cost_usd 2.00, output_path), exits 0.

# 5. Helper cap-refusal smoke (set monthly_cap_usd = 0.01 temporarily, retry)
# Manually edit config.toml: [gemini.budget].monthly_cap_usd = 0.01
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/gemini_dr.py --query "smoke test" --tier dr
# Expected: exits non-zero with "monthly cap would be exceeded" message. NO API call. NO vault file. NO ledger entry.
# Restore monthly_cap_usd = 20.00 before continuing.

# 6. Live DR call (small scope to keep cost ≤ $1.50)
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/gemini_dr.py --query "What are the supported tools in the Gemini Interactions API as of April 2026?" --tier dr
# Expected: polls for 5-15 min; exits 0 with "report written to <path>"; ledger has 1 entry; vault has new file with frontmatter source: gemini-deep-research.

# 7. Skill activation in fresh interactive session
#   Open Claude Code in this repo. Ask: "Run a Gemini deep research on the Anthropic SDK release notes from January 2026 onward."
#   Expected: Claude loads gemini-deep-research skill, classifies as DR (no confirmation prompt), invokes helper via Bash, returns report.

# 8. Skill DR Max confirmation flow
#   Ask: "Run a Gemini Deep Research Max on cross-service auth-mode taxonomy for Slack, Calendar, Gmail, Jira, GitHub, Linear."
#   Expected: Claude prompts via AskUserQuestion showing predicted $5 cost + 20-60 min wall + month-to-date spend.
#   Decline. Verify NO API call, NO vault write.
#   Re-ask, accept. Verify ledger updates, vault file lands.

# 9. Stream A queue load + first night execution
#   Phase 4 step 1-3: queue all 7 topics into the appropriate queues.
#   Manually fire deep-researcher (topic 1) AND gemini-researcher --mode oneshot --query "<topic 2>" --tier dr in parallel.
#   Expected next morning: 2 new files in vault/20_projects/research/, both queues' first items marked done with backlinks.

# 10. Autonomous gemini-researcher path (opt-in)
#   launchctl load ~/Library/LaunchAgents/com.sean.agent.gemini-researcher.plist
#   launchctl start com.sean.agent.gemini-researcher
#   Expected: runs against gemini-research-queue.md; processes one item; logs to agent-run-history.csv.

# 11. Daily-driver morning brief Gemini spend surfacing
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run
# Expected: Vault Health section now includes "gemini-spend-{YYYY-MM}: $X.XX of $20.00 cap".

# 12. Phase E pre-read assembly
#   File exists at vault/20_projects/prj-superuser-pack/phase-e-research-prereads-2026-MM-DD.md.
#   Wikilinks resolve to all 6 expected reports + the topic-6 skip note.
#   ls vault/20_projects/research/2026-* | wc -l shows ≥ 6 new files created post-Phase-4.

# 13. Doc cross-references resolve
grep -l "gemini-deep-research" .claude/skills/last30days/SKILL.md .claude/skills/deep-research-queue/SKILL.md
# Expected: both files match.

# 14. Cost ledger health
cat vault/health/gemini-spend-2026-05.json | python3 -c "import sys, json; d=json.load(sys.stdin); print('total:', d['total_usd'], 'tasks:', d['task_count'])"
# Expected: total ≤ $10.00 after Stream A; task_count = 2.
```

If steps 1–14 all pass, the integration is production-ready, Stream A's fact base is in place, and Phase E can be revisited around 2026-05-15 with concrete data instead of guesses.

---

## Self-Check (per writing-plans skill)

- [x] Read all 9 files listed in the input (`CLAUDE.md`, top of `CHANGELOG.md`, `prj-knowledge-loop-consumer.md` §Phase E, `macmini-migration-plan-2026-05-02.md`, the three Gemini reference clips, and both deep-research skills).
- [x] Each of the 7 Phase E topics individually addressed in §3 routing table after Round-2 refactor (1a + 1b + 2 + 3 + 4-absorbing-6 + 5 + 7) with predicted cost, predicted wall, and rationale. Topic 6's reframed scope (key-generation matrix, not Block-policy discovery) is folded into Topic 4 explicitly.
- [x] Stream B architecture decision (skill + agent + DEFER MCP) has a written-out comparison in §4 with rejected alternatives explicitly labeled.
- [x] Stream C decision is concrete: keep `last30days` standalone; document via two 1-line cross-references.
- [x] §10 Mandatory Doc Updates names every file with explicit count deltas (115 → 116 skills, 13 → 14 SDK agents total).
- [x] No phase has a "configure as needed" or "tune later" step. Every step is executable with a concrete artifact.
- [x] Cost model has hard numbers: per-task $7, daily $10, monthly $20. Worst-case scenario (queue-stuffing fan-out to DR Max) explicitly analyzed: practical worst case $10–14/day under caps.
- [x] Schedule conflict against the Mac Mini 02:45 deep-researcher window verified in Phase 3 step 5; recorded that gemini-researcher loads no local model so memory headroom is unaffected.
- [x] §12 Verification is runnable end-to-end after Phase 5 lands.
- [x] "What does Phase 3 cost in dollars and minutes?" — 3 hours engineering, $0 API spend (no live Gemini calls in Phase 3; first live call is Phase 4 verification step 6).
- [x] Round-2 feedback addressed: Gemini CLI inventory in Phase 0 step 7, OpenAI key check in Phase 0 step 8, CLI agentic-repo audit + pinning patterns in Topic 1b, key-generation matrix in Topic 4, Perplexity SKIP rationale in D7, OpenAI optional-add rationale in D8, Gemini CLI extension v2-swap rationale in D9.

---

End of plan. Ready to execute on Sean's approval.
