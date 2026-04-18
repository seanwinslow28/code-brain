# Phase 6 Implementation Plan — Gemma 4 Benchmarking + Knowledge Compounding Loop

## Context

Phases 0–5 shipped a 12-character, 180-animation sprite pipeline (1,835 frames, ~$12.60) and an autonomous agent layer (2 active agents after the April 9 downsizing). Phase 1 autoresearch is currently running on the Alienware in a separate session.

Phase 6 adds the **meta-layer** missing from steady state: (a) a model-currency benchmark so we don't ossify on today's local models, and (b) a self-maintaining knowledge graph so sessions stop evaporating and autoresearch gets smarter over time. Both live 100% local ($0.00 API). Together they are what closes the "living knowledge graph" gap called out in the SOT (Part 4, line 415) — Karpathy-style LLM Wiki + claude-memory-compiler pattern.

Gate Check criteria (six bullets, SOT line ~419):
1. Gemma 4 benchmarks complete on all 3 routing tasks with head-to-head scoring
2. ≥1 model swap approved and deployed
3. SessionEnd hook capturing ≥3 sessions/week
4. Vault Indexer v2 producing ≥2 concept + ≥1 connection article per nightly run
5. Knowledge Lint ≥95% recall on synthetic test vault
6. Autoresearch convergence improves ≥10% (Optuna trials-to-best-fitness)

Every one of these six is mapped to at least one task below.

---

## Critical Pre-Requisite (before any Phase 6 work)

**P0 — Confirm or build `lib/filelock` + document MacBook Pro WOL path.**
The SOT (line 481) says "Uses existing `lib/filelock` from Phase 1" — but a grep across [agents-sdk/lib/](agents-sdk/lib/) shows **no filelock module exists**. `vault_io.py` has no `flock`/`FileLock` either. This is a blocker for D.1 and D.2 (both need vault write coordination).

- [ ] **P0.1** — Grep the repo one more time for any ad-hoc lock pattern; if none, add `agents-sdk/lib/filelock.py` using `fcntl.flock(LOCK_EX)` with a context manager. Target: ~40 lines. Write before D.1.
- [ ] **P0.2** — MacBook Pro WOL: [agents-sdk/config.toml:119-125](agents-sdk/config.toml) has `wol_mac` only on Alienware. Either (a) MacBook Pro is always-on when lid is open and WOL is unnecessary, or (b) we need `wol_mac` + WOL trigger in `hybrid_router.py`. Confirm with Sean. If (b), add prereq task to extend [hybrid_router.py](agents-sdk/lib/hybrid_router.py) and write MAC address to config.

**Machine:** MacBook Pro (coding). **Cost:** $0.00. **Blocks:** D.1, D.2.

---

## Section 1 — Dependency Graph & Critical Path

### Independence matrix (can run parallel to Phase 1 autoresearch?)

| Task | Parallel-safe? | Blocks | Blocked by |
|---|---|---|---|
| P0.1 filelock | ✅ yes | D.1, D.2 | — |
| P0.2 WOL path | ✅ yes | D.2 synthesis | — |
| A.1 Gemma 4 27B download (Mac Mini) | ✅ yes | A.3, A.5 | — |
| A.2 Gemma 4 31B download (MBP MLX-LM) | ✅ yes | A.3, A.5 | — |
| A.3 benchmark harness (`lib/gemma4_benchmark.py`) | ✅ yes | A.4, A.5 | A.1, A.2 |
| A.4 golden test sets (20×3) | ✅ yes | A.5 | — (data-only) |
| A.5 run 60 samples | ✅ yes | A.6 | A.1, A.2, A.3, A.4 |
| A.6 swap decision + config.toml edit | ✅ yes | — | A.5 |
| D.1 SessionEnd hook + flush.py | ✅ yes | D.2 benefit (not block) | P0.1 |
| D.2 Vault Indexer v2 + synthesizer | ✅ yes | D.3 real-world test, D.4 | P0.1, P0.2 |
| D.3 knowledge_lint.py Tier 1+2 | ✅ yes (synthetic vault) | daily_driver integration | D.2 for real content; synthetic works without |
| D.3 daily_driver.py integration | ✅ yes | — | D.3 lint live |
| **D.4 autoresearch feedback** | ❌ **BLOCKED** | Gate Check #6 | **Phase 1 autoresearch shipping + D.2 producing articles** |

### Wall-clock sequencing (4 weeks)

- **Week 13** — P0 prereqs (½ day). Then fork two parallel tracks:
  - Track A: A.1+A.2 downloads → A.3 harness scaffolding → A.4 golden sets
  - Track D: D.1 flush hook + flush.py end-to-end
- **Week 14** — A.5 benchmark run (overnight) → A.6 swap decision. Track D: D.2 synthesizer (largest surface area — de-risk first on 5-file mini-vault before full vault).
- **Week 15** — D.3 lint Tier 1+2 + synthetic test vault validation. Daily Driver integration. Wait for Phase 1 autoresearch completion.
- **Week 16** — D.4 feedback wiring (2–3h of work, mostly measurement). Side-by-side convergence comparison across ≥2 nights. Gate Check writeup.

### Critical path
`P0 → A.1+A.2 (downloads, overnight) → A.3 harness → A.5 benchmark → A.6 swap` runs in parallel with `P0 → D.1 → D.2 synthesizer → D.3 lint → daily_driver integration`. **D.4 is off the critical path but gates the final Gate Check bullet**; start it the day Phase 1 autoresearch ships.

### Riskiest component (de-risk first)
**D.2 Vault Synthesizer.** Reasons: 45-min runtime budget, WOL cold-start adds latency, depends on MLX-LM being up on MBP at 2:30 AM, largest prompt surface (concept + connection generation), and it's the only component with a clear fail mode that silently degrades the whole loop. De-risking: stand up a 5-file mini-vault in `vault/_sandbox/`, run synthesizer end-to-end on that before pointing at the real vault. Also: require the "≥2 wikilinks" graph invariant as a hard validator so nodes are never orphaned.

---

## Section 2 — Workstream A Plan (Gemma 4 Benchmarking)

### A.1 + A.2 — Downloads with pre-flight checks

**Pre-flight (must pass before pulling):**
- Mac Mini: `df -h /` → require ≥40 GB free. `ollama list` → ensure phi4-mini-reasoning present (fallback if benchmark fails). RAM: 24 GB total; Gemma 4 27B MoE activates only 3.8B, so ~8 GB peak is fine.
- MacBook Pro: `df -h /` → require ≥80 GB free (31B dense 4bit ≈ 18 GB + cache). RAM: 48 GB unified — 31B 4bit fits with room. Check `mlx_lm.generate --help` available.

**Commands (documented in the plan, not executed now):**
- Mac Mini: `ollama pull gemma4:27b` → verify with test prompt containing function-call tokens.
- MBP: `mlx_lm.convert --hf-path google/gemma-4-31b -q` (or equivalent Gemma 4 31B path once released) → benchmark tok/s baseline.

**Machine:** Mac Mini (A.1), MacBook Pro (A.2). **Cost:** $0.00.

### A.3 — Benchmark harness

**File:** `agents-sdk/lib/gemma4_benchmark.py` (new, ~200 lines).

**Structure:**
```
lib/gemma4_benchmark.py
  class BenchmarkHarness:
    run(task_name, model_spec, golden_samples, n_runs=10) → BenchmarkResult
  class BenchmarkResult:
    latency_p50_ms, latency_p95_ms, tokens_per_sec, quality_score
  quality metrics:
    - Jaccard similarity on extracted entities vs golden set (inbox, financial)
    - Structural match on issue categories (code review)
```

**Reuse:** Import `HybridRouter` from [lib/hybrid_router.py](agents-sdk/lib/hybrid_router.py) for the Ollama/MLX HTTP calls — do not reinvent the transport layer. Import `setup_logger` and `record_run` from [lib/logging_setup.py](agents-sdk/lib/logging_setup.py).

### A.4 — Golden test sets

**Location:** `agents-sdk/benchmarks/golden/` (new dir).
- `inbox_triage.jsonl` — 20 samples. Schema: `{input_email, expected_category, expected_actions}`.
- `financial.jsonl` — 20 samples. Schema: `{csv_row, expected_category, expected_budget_note}`.
- `code_review.jsonl` — 20 samples. Schema: `{snippet, expected_issues, expected_rating_1_5}`.

Seed from real vault data where possible (Sean's finance CSVs → sanitize via [lib/csv_sanitizer.py](agents-sdk/lib/csv_sanitizer.py)).

### A.5 — Run 60 samples

**Output:** `agents-sdk/benchmarks/results/gemma4-benchmark-YYYY-MM-DD.json` + `.md` summary table. Run overnight; 60 samples × ~3 models × ≤10 runs each ≈ 1–3 hours total.

### A.6 — Veto gate + swap decision

**Pass/fail rule (SOT line 436):**
> If Gemma 4 quality ≥5% worse than incumbent → **keep incumbent**. Quality over speed.

**Decision matrix (documented in a new `decisions/2026-06-gemma4-swap.md`):**
| Task | Incumbent | Candidate | Swap if |
|---|---|---|---|
| Inbox triage (Mac Mini) | phi4-mini-reasoning | gemma4:27b-moe | quality ≥95% of incumbent AND latency within 2× |
| Anki cards (Mac Mini) | phi4-mini | gemma4:27b-moe | same rule |
| Financial analysis (MBP) | Qwen3-14B | Gemma 4 31B | quality ≥99% of Qwen3-14B (tighter — Qwen is performing) |
| Code review (MBP) | Qwen2.5-Coder-32B | Gemma 4 31B | expected to fail gate — keep Qwen coder-specialist |

**Fallback if Gemma 4 fails all tasks:** No-op. Commit the benchmark report as evidence of the evaluation, update `SOURCE-OF-TRUTH.md` Part 5 Q12 to RESOLVED (incumbents retained), move on. Gate Check #1 (benchmarks complete) still passes; Gate Check #2 (≥1 swap) doesn't — flag as partial. Confirmed: this is the intended fallback per the veto gate.

**Config edit:** [config.toml](agents-sdk/config.toml) lines 137–145 `[routing.task_map]` — update only the tasks that won their benchmark.

---

## Section 3 — Workstream D Plan (Knowledge Compounding Loop)

### D.1 — SessionEnd Hook + flush.py

**New files:**
- `.claude/hooks/session-end-flush.sh` — matches `SessionEnd` event in [settings.json](.claude/settings.json) (currently only Stop is wired; add SessionEnd section).
- `agents-sdk/agents/flush.py` — new agent, ~300 lines.

**Modified files:**
- [.claude/settings.json](.claude/settings.json) — add `"SessionEnd"` hooks block with matcher `command: .claude/hooks/session-end-flush.sh`.

**Hook contract (exit-code rules from [CLAUDE.md](CLAUDE.md)):**
- `0` = allow/continue (hook is advisory, not a gate)
- `2` = deny (never used here — we never want to block session end)
- Hook spawns `flush.py` **detached** (`nohup … &` or `setsid`) so session close is never blocked.

**Recursion guard (SOT line 451):** hook checks `CLAUDE_INVOKED_BY` env var at entry; if set, `exit 0` immediately without spawning. `flush.py` itself exports `CLAUDE_INVOKED_BY=flush` before any sub-session it might need.

**flush.py routing logic:**
- Read session transcript (passed as arg from hook).
- Count messages. If `≤100`: route to Mac Mini phi4-mini via `HybridRouter.route("flush_simple")`. If `>100`: route to MacBook Pro Qwen3-14B via `HybridRouter.route("flush_complex")`.
- Add two new task_map entries to [config.toml](agents-sdk/config.toml): `flush_simple = { model = "phi4-mini", machine = "mac_mini" }`, `flush_complex = { model = "Qwen3-14B", machine = "macbook_pro" }`.
- Extract 5 sections per SOT line 452 (Decisions/Lessons/Actions/Patterns/Quotes) using structured output.
- Append to `vault/daily/YYYY-MM-DD.md` under `<!-- claude-sessions -->` anchor (reusing Daily Driver's existing anchor pattern from [daily_driver.py:133](agents-sdk/agents/daily_driver.py)).

**Filelock:** `flush.py` acquires `vault/daily/.lock` via `lib/filelock` (built in P0.1) before write, releases after close. Prevents collision with Daily Driver morning run (8:45 AM) and Vault Indexer (2 AM).

**Vault Indexer exclusion:** Add `vault/daily/` to `exclude_dirs` in [vault_indexer.py:92](agents-sdk/agents/vault_indexer.py) — daily logs feed synthesis, not search.

**Safety:** `max_turns=15`, `max_budget_usd=0.00`, `permission_mode="acceptEdits"`, no `dangerouslySkipPermissions`.

**Machine:** Mac Mini (default) / MacBook Pro (>100 msg route). **Cost:** $0.00.

**Success criteria (maps to Gate Check #3):** Hook fires on ≥5 session closes/week without errors, recursion guard blocks self-calls, daily log appends are atomic.

### D.2 — Vault Indexer v2 + vault_synthesizer.py

**Modified files:**
- [agents-sdk/agents/vault_indexer.py](agents-sdk/agents/vault_indexer.py) — add change-detection + baton-trigger at the end of `index_vault()`. Add `.indexer-state.json` (sha256 + timestamp per file) alongside existing SQLite store. Add `vault/daily/` exclusion.

**New files:**
- `agents-sdk/agents/vault_synthesizer.py` — ~400 lines.
- `agents-sdk/schedules/com.sean.agent.vault-synthesizer.plist` — 2:30 AM trigger on MBP.
- `vault/knowledge/index.md` — auto-maintained catalog.
- `vault/knowledge/concepts/` + `vault/knowledge/connections/` — output dirs.

**Config additions** ([config.toml](agents-sdk/config.toml)): add `[vault_indexer]` block per SOT line 519 with `synthesis_enabled`, `synthesis_machine = "macbook_pro"`, `synthesis_model = "qwen3-14b"`, `synthesis_max_minutes = 45`, `exclude_paths`, `state_file`.

**Orchestration:**
- Mac Mini runs indexer at 2:00 AM (embedding pass, existing).
- At 2:15 AM, indexer writes baton file via [lib/baton.py](agents-sdk/lib/baton.py) with list of changed files.
- Mac Mini issues WOL packet to MBP (requires P0.2).
- MBP launchd agent fires at 2:30 AM, reads baton, runs `vault_synthesizer.py`.
- Fallback: if MBP unreachable, `vault_synthesizer.py` defers via baton-retry pattern; log warning, do not block. Reuse [hybrid_router.py](agents-sdk/lib/hybrid_router.py) health check (line 108 `health_check_timeout_secs = 3`).

**Synthesizer logic (per SOT line 495):**
1. Read each changed file + retrieve 5 similar vault files via existing `search()` at [vault_indexer.py:190](agents-sdk/agents/vault_indexer.py).
2. Extract 2–5 key concepts.
3. For each concept with 2+ related files → write `vault/knowledge/concepts/<name>.md` (template per SOT line 497).
4. Cross-cutting themes across 3+ concepts → `vault/knowledge/connections/<theme>.md`.
5. **Hard invariant:** every article contains ≥2 wikilinks to other articles. Validator refuses to write an article that would be an orphan node.

**Safety:** `max_turns=25`, `max_budget_usd=0.00`, 45-min wall clock cap, filelock on `vault/knowledge/`.

**Machine:** Mac Mini (embeddings) → MacBook Pro (synthesis via WOL). **Cost:** $0.00.

**Success criteria (Gate Check #4):** ≥2 concept articles + ≥1 connection article per nightly run, all articles have ≥2 wikilinks, `index.md` auto-updates.

### D.3 — knowledge_lint.py (2-tier)

**New files:**
- `agents-sdk/agents/knowledge_lint.py` — ~350 lines.
- `agents-sdk/schedules/com.sean.agent.knowledge-lint.plist` — Sunday 22:00.
- `agents-sdk/tests/fixtures/synthetic_vault/` — 20 files with planted issues.

**Modified files:**
- [agents-sdk/agents/daily_driver.py](agents-sdk/agents/daily_driver.py) — morning prompt (around line 100) adds: "Check `vault/health/` for latest lint report. If CRITICAL/HIGH issues exist, surface a 'Vault Health' section with deep link. Otherwise print 'Vault health: PASS ✓'."

**Tier 1 (Mac Mini, phi4-mini-reasoning, ~5 min):**
- Broken wikilinks: regex scan `[[...]]` → verify target exists. Pure Python, no LLM needed for the scan itself.
- Orphan files: 0 inbound links.
- Missing YAML frontmatter in `vault/knowledge/`.
- Kebab-case file-name enforcement.

**Tier 2 (MacBook Pro, Qwen3-14B, triggered on Tier 1 issues OR weekly full scan):**
- Contradiction detection across related articles.
- Staleness detection: flag articles >30 days old referencing time-sensitive items (model releases, APIs).
- SOT drift: compare SOURCE-OF-TRUTH.md Part 1–2 vs vault articles.

**Output:** `vault/health/YYYY-MM-DD-lint-report.md` with CRITICAL/HIGH/MEDIUM/LOW.

**Recursion/filelock concern:** Tier 2 runs on MBP via WOL — same WOL infra as D.2. If D.2 is mid-run at 22:00 Sunday (shouldn't be, D.2 is nightly 2:30 AM), filelock on `vault/knowledge/` serializes them. Acquire read-lock for lint, write-lock for synthesizer.

**Safety:** Tier 1 `max_turns=20`, Tier 2 `max_turns=30`, `max_budget_usd=0.00`.

**Machine:** Mac Mini (Tier 1) + MacBook Pro (Tier 2). **Cost:** $0.00.

**Success criteria (Gate Check #5):** ≥95% recall on synthetic 20-file vault, report renders correctly, Daily Driver surfaces alerts.

### D.4 — Knowledge → Autoresearch Feedback Loop

**Modified files:**
- The autoresearch orchestrator (Alienware side) — **read-only change** per scope: add a vault-concept-article read step at startup (23:30), filter by tags `#autoresearch`, `#comfyui`, `#optimization`, `#rife`, `#pixel-quantizer`, inject top-N into Optuna DSPy prompt context.
- Log `articles_used: N` in run metadata.

**No new agent code on this side — D.4 is wiring, not building.** Autoresearch lives on Alienware as a consumer only (per scope statement).

**Measurement harness (on MBP):**
- Run Optuna convergence comparison: 2 nights with articles injected vs 2 nights without. Metric: trials-to-best-fitness (primary), final-fitness-delta (secondary — per Q16).
- Hypothesis: ≥10% convergence improvement.

**Machine:** Alienware (consumer) + Mac Mini (vault read orchestration). **Cost:** $0.00.

**Success criteria (Gate Check #6):** `articles_used > 0` in autoresearch logs, convergence improves ≥10%.

**Dependency callout:** This task is **BLOCKED UNTIL Phase 1 autoresearch ships** on the Alienware and D.2 has produced ≥5 concept articles. Start the day Phase 1 completes.

---

## Section 4 — Integration, Testing, Scheduling, Rollback

### End-to-end flow (the virtuous cycle, SOT line 559)

```
Night 1: autoresearch runs 50 Optuna trials
   ↓
Morning: SessionEnd hook → flush.py → vault/daily/2026-06-21.md
   ↓
2:00 AM Night 2: Vault Indexer v2 embeds + detects changes
   ↓
2:30 AM Night 2: WOL → MBP → vault_synthesizer.py → vault/knowledge/concepts/rife-temporal-smoothing.md
   ↓
23:30 Night 3: autoresearch reads vault/knowledge/concepts/ with #autoresearch tag
   ↓
Better prior → faster Optuna convergence → repeat
```

### Test plan

- **Synthetic vault (D.3):** 20 files in `tests/fixtures/synthetic_vault/` with planted broken wikilinks, orphans, stale articles, contradictions. Target ≥95% recall.
- **Benchmark run (A.5):** 60 samples, documented JSON + MD output.
- **Hook + flush dry-run:** Invoke `session-end-flush.sh` manually with a captured transcript; verify detachment, recursion guard, and daily log append without blocking.
- **D.2 mini-vault dry-run:** Synthesizer against 5-file `vault/_sandbox/` before pointing at real vault.
- **D.4 side-by-side:** 2 nights × {with articles, without articles}, ≥4 runs total before concluding convergence delta.

### launchd schedule changes

| Time | Existing | New | Collision? |
|---|---|---|---|
| 02:00 | vault-indexer (Mac Mini) | — | indexer runs first |
| 02:15 | — | indexer writes baton, triggers WOL | baton wait pattern handles |
| 02:30 | — | vault-synthesizer.plist (MBP) | no collision — MBP is idle |
| 06:30 | meta-agent (Mac Mini) | — | no change |
| 08:45 | daily-driver morning | — | reads lint report if present |
| Sun 22:00 | — | knowledge-lint.plist | no collision |
| Session close | Stop hook (run-tests) | SessionEnd hook (flush, detached) | additive; different event type |

All new plists include `EnvironmentVariables > PATH` per [CLAUDE.md](CLAUDE.md) launchd requirement. Model on [com.sean.agent.vault-indexer.plist](agents-sdk/schedules/com.sean.agent.vault-indexer.plist).

### Rollback plan (per component)

Every new agent must be disable-able in isolation without breaking the others:

| Component | Rollback |
|---|---|
| Gemma 4 swap (A.6) | Revert [config.toml](agents-sdk/config.toml) `[routing.task_map]` to phi4/Qwen3 entries. No schema change. |
| flush.py + SessionEnd hook | Remove `SessionEnd` block from [settings.json](.claude/settings.json). Agent goes silent; no downstream breakage (daily logs are append-only). |
| vault_synthesizer.py | Set `synthesis_enabled = false` in `[vault_indexer]` config block. Indexer v2 falls back to embedding-only behavior identical to v1. Knowledge articles stop refreshing but existing ones remain. |
| knowledge_lint.py | `launchctl bootout` the Sunday plist. Daily Driver integration is guarded by "if lint report exists" — no report → no UI change. |
| D.4 wiring | Revert autoresearch orchestrator's vault-read step. `articles_used` counter drops to 0. |

---

## Section 5 — Open Decisions (SOT Part 5 Q12/13/14/16)

### Q12 — Gemma 4 native function calling benefit for autoresearch

**Decision needed:** Whether to run the optional Week 16 function-calling reliability test (SOT line 441) and swap Gemma 4 into the Mac Mini orchestrator role for autoresearch.
**Recommendation:** **Defer to after A.5 benchmarks.** Run only if Gemma 4 wins inbox triage with ≥5% margin AND function-call success rate ≥98% on harness tests.
**Flip evidence:** If benchmarks show Gemma 4 equal-or-worse than phi4-mini-reasoning, skip the test entirely — marginal upside, real integration cost.

### Q13 — Daily logs location (inside vault vs parallel)

**Decision needed:** `vault/daily/` (inside) vs `agents-sdk/daily-logs/` (parallel).
**Recommendation:** **`vault/daily/` (inside).** Enables Obsidian MOC cross-linking, Dataview queries, and lets `vault/daily/INDEX.md` auto-index via existing patterns.
**Flip evidence:** If the Vault Indexer exclusion doesn't hold (daily logs accidentally re-embedded) or filelock contention causes >1 write conflict/week during the first month, move to parallel.

### Q14 — Flush agent machine (Mac Mini phi4-mini vs MBP Qwen3-14B)

**Decision needed:** Single-machine or hybrid routing for flush.py.
**Recommendation:** **Hybrid with msg-count threshold.** Default Mac Mini phi4-mini for ≤100 messages; route >100 to MBP Qwen3-14B. Matches SOT line 452.
**Flip evidence:** Measure extraction accuracy (compare flush.py output against manual Preserve Session outputs on 10 reference sessions). If phi4-mini accuracy <85% on the Decisions/Actions sections, drop threshold to 50 or route everything to Qwen3-14B.

### Q16 — Autoresearch convergence metric

**Decision needed:** Trials-to-best-fitness vs final-fitness-delta.
**Recommendation:** **Primary: trials-to-best-fitness; secondary: final-fitness-delta.** Report both in D.4 success evidence.
**Flip evidence:** If trials-to-best variance across nights is too high (σ > 0.3× mean), switch primary to final-fitness-delta which is more stable.

---

## Section 6 — Mandatory Doc Updates (per [CLAUDE.md](CLAUDE.md))

Per the "Mandatory doc updates" rule — 3 new agents + 1 new hook means all three of these files MUST be edited in the execution commit:

### CHANGELOG.md
Add entries under the next version section:
- `Added: Gemma 4 benchmark harness (lib/gemma4_benchmark.py) + 60-sample evaluation across inbox/financial/code tasks`
- `Added: SessionEnd flush hook (.claude/hooks/session-end-flush.sh) + flush.py agent for automatic session knowledge capture`
- `Added: Vault Indexer v2 — synthesis pass producing concept + connection articles (vault_synthesizer.py)`
- `Added: knowledge_lint.py — 2-tier vault health checks (Tier 1 structural, Tier 2 semantic)`
- `Added: lib/filelock.py for coordinated vault writes` (if P0.1 confirms it's missing)
- `Changed: [routing.task_map] in config.toml per Gemma 4 benchmark results` (if A.6 swaps anything)
- `Changed: vault_indexer.py adds vault/daily/ exclusion + change-detection state file`

### CLAUDE.md
Update counts in the opening line ("111 skills, 13 agents, 7 hooks..."):
- Agents: **13 → 16** (flush, vault_synthesizer, knowledge_lint)
- Hooks: **7 → 8** (session-end-flush.sh)
- Under "Agents SDK (Autonomous Layer)": update the "Active agents (2 of 10)" table — new total "Active agents (5 of 13)". Add rows for flush, vault_synthesizer, knowledge_lint with schedule/skills/cost.

### README.md
Update top-level counts (agents, hooks) to match CLAUDE.md. Update any skill/agent tables that enumerate the fleet.

### export-groups/*/playground.json manifests
For any export group that includes agents-sdk or hooks, add:
- `hooks/session-end-flush.sh`
- Agent entries for flush, vault_synthesizer, knowledge_lint (if the preset covers autonomous agents)

Specifically check `presets/power/`, `presets/enterprise/`, and `presets/creative/`.

### Validation
Run `python3 scripts/validate.py` after all edits. Per [CLAUDE.md](CLAUDE.md), this is mandatory after skill/agent/hook changes.

---

## Verification (end-to-end test sequence before claiming Gate Check)

1. **A.6 evidence:** `cat agents-sdk/benchmarks/results/gemma4-benchmark-*.md` shows 3-task × 3-model matrix with verdicts. Swap decision doc committed.
2. **D.1 evidence:** Close 3 sessions, then `ls vault/daily/` shows dated files, each with all 5 sections populated. `grep "CLAUDE_INVOKED_BY" vault/90_system/agent-logs/flush-*.log` confirms recursion guard fires.
3. **D.2 evidence:** After one nightly run, `ls vault/knowledge/concepts/ vault/knowledge/connections/` shows ≥2 + ≥1 new files. Every article grep'd for `[[` count ≥2.
4. **D.3 evidence:** Run `python3 agents-sdk/agents/knowledge_lint.py --dry-run --vault agents-sdk/tests/fixtures/synthetic_vault` — report catches ≥19/20 planted issues.
5. **D.4 evidence:** `grep "articles_used" agents-sdk/benchmarks/autoresearch/*.json` shows >0. Convergence metric shows ≥10% delta across matched pairs.
6. **Schedule evidence:** `launchctl list | grep com.sean.agent` lists the new plists. Each fires successfully on next cadence.

Self-check against the `<validation>` block: (1) every Gate Check bullet has ≥1 task ✅. (2) every task has a machine assignment ✅. (3) D.4 explicitly marked blocked-until-Phase-1 ✅. (4) filelock + recursion guard called out in D.1 ✅. (5) rollback explicit for each component ✅.
