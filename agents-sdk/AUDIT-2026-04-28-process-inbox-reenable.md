# AUDIT — Re-enable `process-inbox` Agent (2026-04-28)

**Status:** Re-enabled with operating-model artifact wiring.
**Cadence:** Twice weekly — Sundays 09:00 ET + Wednesdays 09:00 ET.
**Cost ceiling per run:** $1.20 (was $0.25 when disabled).
**Disabled since:** 2026-04-09 (`AUDIT-2026-04-09-agent-downsizing.md`).

## Why now

Three things changed since the April 9 disable:

1. **SDK transport bug fixed.** The `CLIConnectionError: ProcessTransport is not ready for writing` failure mode that produced 0/6 success rate on v0.1.56 is gone in v0.1.63 (current pin in `agents-sdk/pyproject.toml`). Two live test runs on 2026-04-28 connected cleanly and ran to completion — no transport errors.
2. **launchd PATH fix is in.** `BUGFIX-2026-04-07-launchd-path.md` is applied to all plists.
3. **Operating-model artifacts are confirmed.** All three life-systems artifacts (HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations) carry `status: confirmed` as of 2026-04-22. The life-systems `SOUL.md` frontmatter explicitly names `process-inbox` as a designated consumer.

## What changed in this re-enable

| Area | Before (disabled) | After (re-enabled) |
|---|---|---|
| `enabled` | `false` | `true` |
| Schedule | Daily 05:30 (one-shot) | Sun 09:00 + Wed 09:00 (`StartCalendarInterval` array) |
| `max_turns` | 15 | 25 |
| `max_budget_usd` | $0.25 | $1.20 |
| Operating-model wiring | none | HEARTBEATs always-on (3 domains); on-demand pointers to SOUL + operating-model |
| Empty-inbox behavior | LLM-decided (cost ~$0.65 on first test) | Python short-circuit, $0 cost |
| Docstring claim | "100% local via phi4-mini-reasoning" | Honest: "Cloud Sonnet via `claude_agent_sdk.query()`" |
| Research-candidate flag | none | Tag `#triage/research-candidate` for items matching the future research fleet (crypto, prediction markets, x402, agentic commerce, AI tooling, autoresearch) |

## Files modified

- `agents-sdk/agents/process_inbox.py` — added `build_artifact_preamble()` (mirrors `daily_driver.build_artifact_preamble`); added Python empty-inbox short-circuit before SDK call; added STEP 0 in task prompt; bumped MAX_TURNS / MAX_BUDGET_USD; corrected docstring + dry-run routing print.
- `agents-sdk/config.toml` — `[agents.process_inbox] enabled = true`, schedule comment, `max_turns = 25`, `max_budget_usd = 1.20`. Added `process_inbox = { heartbeats = true, on_demand = ["SOUL", "operating-model"] }` under `[artifacts.per_agent]`.
- `agents-sdk/schedules/com.sean.agent.process-inbox.plist` — `StartCalendarInterval` is now an array of two dicts (Weekday=0 + Weekday=3, both at 09:00). `plutil -lint` passes.

## Operating-model wiring rationale

**Why HEARTBEATs are always-on:** Inbox triage's first decision per file is "what domain does this belong to" — having all 3 domain HEARTBEATs in the system prompt gives the agent the cadence + scope context to route accurately. ~5K tokens cached, ~$0.01/turn after first turn. Mirrors the daily-driver Phase 1 pattern.

**Why SOUL + operating-model are on-demand (not always-on):**
- `life-systems/SOUL.md` line 9 explicitly says "Consumed by … process-inbox". Tier-A learned items (no scolding, capture-and-defer, every-dollar-counts) shape tone and tagging.
- `life-systems/operating-model.md` Active Leverage Point #1 enumerates the future research fleet (Perplexity API, Gemini Deep Research MCP, NotebookLM MCP, agentkit). When the agent encounters a research-worthy capture, this is the artifact that defines what "research-worthy" looks like → drives the `#triage/research-candidate` tag.

These are loaded only when actually needed, not on every turn — keeps per-turn cost low.

**Why USER + schedule-recommendations are NOT wired:** they don't shape triage decisions. USER overlaps with SOUL for tone purposes; schedule-recommendations is about cadence, which is irrelevant to per-file routing.

## Test runs (2026-04-28)

| Run | Inbox state | Turns | Cost | Status | Notes |
|---|---|---|---|---|---|
| Dry-run | empty | n/a | $0 | OK | Artifact preamble loads cleanly; all 3 HEARTBEATs visible. |
| Live #1 | empty | 21 | $0.65 | `error_max_budget_usd` | Agent over-read on-demand artifacts despite empty inbox. **Root cause of Python short-circuit fix.** |
| Live #2 | empty (post early-exit-prompt fix) | 19 | $0.91 | `error_max_budget_usd` | Prompt-level early-exit didn't stick. **Root cause of moving short-circuit out of LLM into Python.** |
| Live #3 | 9 files | 22 | $0.87 | `error_max_budget_usd` | Real load — agent ran out of budget mid-batch. **Root cause of MAX_BUDGET_USD bump from 0.85 → 1.20 + MAX_TURNS 15 → 25.** |

## Cost projections (after fixes)

| Scenario | Cost/run | Frequency | Monthly |
|---|---|---|---|
| Empty inbox (Python short-circuit) | $0.00 | 2/week | $0.00 |
| Light load (1-3 files) | ~$0.40 | (subset of runs) | — |
| Typical load (5-7 files) | ~$0.80 | (subset of runs) | — |
| Heavy load (8-10 files) | ~$1.10 | (subset of runs) | — |
| **Worst-case month** (every run is heavy) | $1.20 × 8 runs | — | **$9.60/month** |
| **Realistic month** (mix of empty/light/typical) | weighted | — | **~$3-5/month** |

For comparison: pre-disable the agent burned $9.30/month for **zero output**.

## Past Landmines respected (per `life-systems/SOUL.md` Part B)

- ✅ **#1 Going too big too fast.** This is one validated agent at a time, not a fleet expansion.
- ✅ **#4 Budget caps too tight.** Cap raised proactively after the live tests showed real load exceeds the original.
- ✅ **No-scolding tone rule** carried into the preamble.

## Remaining gates (mark each as it clears)

- [ ] **Bootstrap launchd plist.** Run `launchctl bootstrap gui/$(id -u) agents-sdk/schedules/com.sean.agent.process-inbox.plist` (or full re-install via `agents-sdk/schedules/install_schedules.sh`).
- [ ] **First scheduled run clean.** First fire is 2026-04-29 09:00 ET (Wednesday). Watch `vault/90_system/agent-logs/process-inbox-2026-04-29.log` for `status=success`.
- [ ] **Second scheduled run clean.** Sunday 2026-05-03 09:00 ET.
- [ ] **3-run soak.** Sun 2026-05-03 + Wed 2026-05-06 + Sun 2026-05-10. If all three under cap, declare stable and remove this re-enable from "soak" status.

## Rollback options (in order of escalation)

1. **One-config flip (instant):** `[artifacts].enabled = false` in `config.toml` — disables artifact preamble for ALL agents (also kills daily-driver, meta-agent, flush, knowledge-lint wiring). Use only if artifact loading itself is the problem.
2. **Per-agent disable:** remove the `process_inbox = ...` line from `[artifacts.per_agent]`. Keeps wiring for other agents.
3. **Drop on-demand pointers (cost-only):** change `on_demand = ["SOUL", "operating-model"]` to `on_demand = []`. Keeps HEARTBEATs (cheap) but stops the agent from being tempted to read full artifact bodies.
4. **Disable agent entirely:** `[agents.process_inbox] enabled = false`. Same as pre-2026-04-28 state.
5. **launchctl bootout:** `launchctl bootout gui/$(id -u) agents-sdk/schedules/com.sean.agent.process-inbox.plist` — stops scheduled fires without touching code or config.

## Open questions for soak review

1. **Is the $1.20 cap holding under real load?** ❌ First scheduled fire (2026-04-29 09:00) hit $1.23 / 30 turns and moved zero files. See "Round 2 adjustments" below.
2. **Are `#triage/research-candidate` tags landing correctly?** Pending — round 1 produced no triaged files to review.
3. **Does the agent over-read on-demand artifacts?** ❌ Confirmed yes. Rollback option 3 applied in round 2.

---

## Round 2 adjustments (2026-04-29, after first scheduled fire)

**First scheduled fire result:** `status=error_max_budget_usd, turns=30, cost=$1.2301` — and **0 files moved**. All 9 files still in inbox.

**Root cause analysis:**
- Per-file workflow is ~4-5 tool calls (Read → Edit → Write → optional verify). 9 files needs ~36-45 turns minimum.
- The agent additionally read on-demand SOUL.md and operating-model.md before touching the inbox, burning ~5-8 turns on context exploration.
- 30 turns at $1.23 with cap = no completed work.

**Three changes applied (matches rollback option 3 + cap bump + prompt tightening):**

| Change | Before | After |
|---|---|---|
| `max_turns` | 25 | 40 |
| `max_budget_usd` | $1.20 | $1.80 |
| `[artifacts.per_agent.process_inbox]` | `{ heartbeats = true, on_demand = ["SOUL", "operating-model"] }` | `{ heartbeats = true }` (on_demand removed) |
| Task prompt | "Step 2: For each file:" | New `BUDGET DISCIPLINE` block + explicit `PROCESS FILES SERIALLY — one at a time` directive + cap on tool-calls-per-file |

**What's preserved:**
- All 3 domain HEARTBEATs still always-on (routing context).
- `#triage/research-candidate` flag rule still in `build_artifact_preamble()`.
- Python empty-inbox short-circuit still active ($0 cost on empty runs).

**Cost projection after round 2:**
- 40 turns × ~$0.04/turn = ~$1.60 worst-case real-load run.
- Empty runs: $0.00 (Python short-circuit).
- Worst-case month: $1.80 × 8 runs = $14.40. Down from no-functional-output. Realistic mix: ~$5-8/month.

**If round 2 ALSO trips the cap:** the next move is NOT a third bump. It's a Path B rewrite to local `gemma4:e4b` via `routing.task_map.inbox_triage` (validated +7.5pp quality vs phi4-mini in Phase 6 A.7, $0.00/run). Path B is a rewrite, not a config tweak — separate work.

**Next gate:** Sunday 2026-05-03 09:00 ET. Watch for `status=success` and `cost < $1.80`, plus actual files moved out of inbox.

---

## Round 2 followup runs (2026-04-29 PM, two manual triggers)

| Run | Inbox | Turns | Cost | Files moved | Failure mode |
|---|---|---|---|---|---|
| Manual #1 (post round-2 config) | 9 | 41 | $1.49 | **3 of 9** ✅ | `error_max_turns` (UNDER budget cap — leaner per-turn cost confirms preamble fix) |
| Manual #2 (clear remaining backlog) | 6 | 49 | $1.82 | **3 of 6** ✅ | `error_max_budget_usd` (real-load avg ~8 turns/file, not the 4 the prompt aimed for) |

**Pattern across all runs:** the agent moves ~3 files per run regardless of cap. Per-file averages 5-8 turns (~$0.20-$0.30/file). Steady-state arrival rate of ~3 files/day exceeds the throughput of twice-weekly cloud runs.

**Cumulative cloud spend (6 SDK invocations):** ~$6.97 / 6 files moved = ~$1.16/file via cloud Sonnet.

## Decision: Pause cloud path, switch to Path B

**2026-04-29:** Audit doc threshold was crossed twice. Agent disabled in `config.toml` (`enabled = false`); launchd job unloaded via `launchctl bootout`. The remaining 3 inbox files were cleared via the `process-inbox` skill in an interactive Claude Code session ($0).

**Path B is the architecturally correct fix:**
- Local `gemma4:e4b` via `routing.task_map.inbox_triage` (config.toml line 200) — already defined, just unused.
- Validated +7.5pp quality vs phi4-mini in Phase 6 A.7 benchmarks (the same benchmark that drove the `flush.py` / `vault_synthesizer.py` / `meta_agent.py` routing).
- Cost: $0.00/run regardless of file count.
- No turn caps to manage — local inference has no per-call billing pressure.
- Pattern already proven in 3 active agents using `lib/hybrid_router.py`.

**Path B scope (estimated 3-4 hours):**
1. Replace `claude_agent_sdk.query()` invocation in `process_inbox.py` with a `lib/hybrid_router.py` call routed via `routing.task_map.inbox_triage`.
2. Convert the agentic loop into a deterministic Python loop: for each inbox file, call the local model once with `(file content + classification schema)`, parse the JSON response, apply the move via `pathlib`. No multi-turn agentic flow needed for this task.
3. Drop the artifact preamble's research-candidate flag rule into the same single-turn prompt — it's small enough to inline.
4. Re-enable in config.toml; re-bootstrap launchd plist.
5. Test on a fresh inbox.

**Manual fallback meanwhile:** the `process-inbox` skill in an interactive Claude Code session works perfectly (it's how `vault/00_inbox/` was cleared on 2026-04-25 and again on 2026-04-29). Run `/process-inbox` whenever the inbox starts feeling cluttered.
