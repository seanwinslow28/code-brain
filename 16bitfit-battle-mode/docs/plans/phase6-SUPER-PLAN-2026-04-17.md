# Phase 6 Super Plan — Gemma 4 Benchmarking + Knowledge Compounding Loop

**Window:** Jun 19 – Jul 17 (Weeks 13–16), parallel with Phase 5 autoresearch.
**Spec source:** [16bitfit-battle-mode/SOURCE-OF-TRUTH.md](../../SOURCE-OF-TRUTH.md) lines 413–577 (do not modify).
**Execution host:** MacBook Pro M4 Pro 48GB (this machine) for all dev, tests, and MLX-LM synthesis/benchmarks. Mac Mini hosts launchd + Ollama + always-on orchestration. Alienware is a read-only D.4 consumer.
**Plan authors:** Claude Opus 4.7 · merge of `phase6-gemma4-benchmarking-and-knowledge-compounding-loop.md` (Apr 16) + `phase6-implementation-plan-2026-04-17.md` (Apr 17).

**Revision notes:**
- **2026-04-18 (AM):** Workstream E (Fleet Self-Monitoring / Meta-Agent) retroactively adopted. The meta-agent was built and deployed between the Apr 17 plan authoring and the Apr 18 audit; it is the natural complement to Workstream D (D writes knowledge; E observes fleet health). See §E.
- **2026-04-18 (PM):** **D.4 (Autoresearch Feedback Loop) DESCOPED.** Blocked on upstream autoresearch work that is in flight on a separate plan and would require ≥1 week to reach readiness. Decision: ship Phase 6 without D.4 and revisit when autoresearch convergence harness is ready. Gate #6 marked DESCOPED in `phase6_gatecheck.py`. All D.1–D.3 infrastructure remains live; the knowledge graph will simply not feed autoresearch until a future phase wires it in. See §7.10 Decision and §10 Descope Log.

---

## Context

Phases 1–5 shipped the agent fleet (2 active after the April 9 downsizing), the sprite pipeline (180 animations, 1,835 frames, ~$12.60), and the Phase 5 autoresearch loop (currently running on Alienware). Phase 6 adds the meta-layer:

1. **Workstream A — Gemma 4 model swap.** Gemma 4's 6 native function-calling tokens and 27B-MoE/3.8B-active efficiency make it a credible replacement for `phi4-mini-reasoning` (Mac Mini) and benchmark challenger to `Qwen3-14B` (MacBook Pro). Veto gate: ≥5% quality regression = keep incumbent.
2. **Workstream D — Knowledge Compounding Loop.** Four components (SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint → autoresearch feedback) convert the vault from static archive into a living knowledge graph (Karpathy LLM-Wiki + claude-memory-compiler pattern) that feeds Phase 5 autoresearch.
3. **Workstream E — Fleet Self-Monitoring (added 2026-04-18).** A local, zero-cost Meta-Agent that runs each morning before Daily Driver, verifies agent-fleet and infrastructure health, and publishes a fleet-status note that surfaces in the morning brief. Closes the observability gap left by the April 9 downsizing. See §E.

All Phase 6 code runs 100% local ($0.00 API). Adds 4 agents + 1 hook to the fleet (15 steady-state: 2 pre-existing + flush + synthesizer + lint + meta-agent). Respects April 9 audit: no new launchd MCP dependencies.

**Previously-resolved ambiguities (locked):**
- A and D run in **parallel**, not serially.
- Daily logs **excluded** from nomic-embed index (SOT D.1 line 482).
- WOL failure → **PushNotification to Sean** (overrides SOT's "silent defer").
- Flush routing = **message count threshold** (<100 → phi4-mini; ≥100 → Qwen3-14B).
- Convergence metric = **trials-to-best-fitness**, Wilcoxon signed-rank paired nights.

**Gate Check (SOT line ~419):**
1. Gemma 4 benchmarks complete on all 3 routing tasks with head-to-head scoring
2. ≥1 model swap approved and deployed
3. SessionEnd hook capturing ≥3 sessions/week
4. Vault Indexer v2 producing ≥2 concept + ≥1 connection article per nightly run
5. Knowledge Lint ≥95% recall on synthetic test vault
6. ~~Autoresearch convergence improves ≥10% (trials-to-best-fitness)~~ **DESCOPED 2026-04-18** — see §10
7. **Meta-Agent produces ≥5 fleet-status artifacts in any 7-day window, with ≥1 containing an actionable alert that surfaced in the Daily Driver morning brief.**

Every bullet maps to ≥1 task below.

---

## P0 — Critical Pre-Requisites (fix before any Phase 6 work)

Both of these were discovered by searching the current codebase; SOT language assumed they already existed. They don't.

### P0.1 — Build `agents-sdk/lib/filelock.py`

**Finding:** SOT line 481 says "Uses existing `lib/filelock` from Phase 1." A grep across [agents-sdk/lib/](../../../agents-sdk/lib/) and [agents-sdk/lib/vault_io.py](../../../agents-sdk/lib/vault_io.py) returns **zero hits** for `filelock`, `FileLock`, `flock`. It does not exist.

**Action:** Create `agents-sdk/lib/filelock.py` (~40 lines) using `fcntl.flock(LOCK_EX)` with a context manager. Must support both `LOCK_EX` (synthesizer writes) and `LOCK_SH` (lint Tier 2 reads). Add `test_filelock.py` with contention tests.

**Blocks:** D.1 (flush.py needs `vault/daily/.lock`), D.2 (synthesizer needs `vault/knowledge/.lock`).

### P0.2 — MacBook Pro WOL path

**Finding:** [agents-sdk/config.toml:119-125](../../../agents-sdk/config.toml) has `wol_mac` only on Alienware. MacBook Pro has `always_on = false` but no MAC address.

**Action:** Two options — decide with Sean:
- **(a) Always-on path:** If Sean keeps the MacBook Pro lid open with `caffeinate -dimsu` running a daemon, mark `always_on = true` in config. No WOL needed. Simpler.
- **(b) WOL path:** Add `wol_mac = "<MBP-MAC>"` to config, extend [hybrid_router.py](../../../agents-sdk/lib/hybrid_router.py) with MBP WOL trigger (reuse Alienware pattern), create new `lib/wol.py` helper (see §3).

Plan assumes **(b)** — safer for robustness. Easy to simplify to (a) if Sean prefers.

**Blocks:** D.2 synthesis (nightly 2:30 AM), D.1 complex flush route, D.3 Tier 2 lint.

**Machine:** MacBook Pro (both P0 tasks are pure dev). **Cost:** $0.00. **Est:** ½ day combined.

---

## 1. Dependency Graph

```
                Phase 5 autoresearch running (prerequisite for D.4 only)
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ P0 prereqs (½ day on MBP) — filelock.py + MBP WOL in config              │
└──────────────────────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌─── WEEK 13 ────────────────────┐  ┌─── WEEK 13 ───────────────────┐
│ Workstream A (parallel)        │  │ Workstream D.1 (parallel)     │
│   A.1  ollama pull gemma4:27b  │  │   D.1.a  session-end-flush.sh │
│   A.2  mlx_lm pull gemma4:31b  │  │   D.1.b  flush.py + filelock  │
│   A.3  lib/gemma4_benchmark.py │  │   D.1.c  routing by msg count │
│   A.4  3 golden sets (20 ea)   │  │                               │
│   A.5  60-sample run (2 nights)│  │                               │
└────────────────┬───────────────┘  └───────────────┬───────────────┘
                 ▼                                  ▼
┌─── WEEK 14 ──────────────────────────────────────────────────────┐
│   A.6 swap decision (veto gate ≥5%)   D.2.a hash-state tracking  │
│   A.7 config.toml swap + regression   D.2.b vault_synthesizer.py │
│                                       D.2.c WOL + PushNotification│
└──────────────────────────────┬───────────────────────────────────┘
                               ▼
┌─── WEEK 15 ──────────────────────────────────────────────────────┐
│   D.3.a Tier 1 lint (Mac Mini)                                   │
│   D.3.b Tier 2 lint (MBP via hybrid_router)                      │
│   D.3.c synthetic 30-file vault (≥95% recall gate)               │
│   D.3.d daily_driver.py Vault Health section                     │
└──────────────────────────────┬───────────────────────────────────┘
                               ▼
┌─── WEEK 16 ──────────────────────────────────────────────────────┐
│   ~~D.4.a orchestrator reads vault/knowledge/concepts/~~ DESCOPED│
│   ~~D.4.b articles_used logging~~                        DESCOPED│
│   ~~D.4.c 7-night A/B + Wilcoxon~~                       DESCOPED│
│   Gate check (6 of 7 gates, #6 parked) + doc updates             │
│   + v3.14.0 tag (re-numbered from 3.13.0 during merge)           │
└──────────────────────────────────────────────────────────────────┘
```

**Parallelism flags:**
- A.1 ∥ A.2 (downloads on different machines)
- A track ∥ D.1 (different files, no shared state)
- D.3 starts after D.2 has produced ≥1 synthesis run
- D.4 is the only task with a hard Phase 5 dependency (blocked until autoresearch ships)

**Riskiest component (de-risk first):** **D.2 Vault Synthesizer.** 45-min budget, WOL cold start, MBP MLX-LM must be up, largest prompt surface. Mitigation: run against a 5-file `vault/_sandbox/` mini-vault end-to-end before pointing at the real vault. Enforce "≥2 wikilinks per article" as a hard validator so no orphan nodes.

---

## 2. Machine + Schedule Map

| Task | Machine | Model | Schedule / Trigger | Runtime |
|------|---------|-------|-------------------|---------|
| P0.1 filelock.py | MacBook Pro (dev) | N/A | One-shot | ~2h dev + tests |
| P0.2 MBP WOL wiring | MacBook Pro (dev) | N/A | One-shot | ~2h dev |
| A.1 Gemma 4 27B MoE pull | Mac Mini | `gemma4:27b` via Ollama | One-shot | ~15 min |
| A.2 Gemma 4 31B pull | MacBook Pro | `gemma4-31b` via MLX-LM | One-shot | ~20 min |
| A.3 Build benchmark harness | MacBook Pro (dev) | N/A | One-shot | ~10h dev |
| A.4 Golden sets | MacBook Pro (dev) | N/A | One-shot | ~6h curation |
| A.5 60-sample benchmark | Mac Mini + MBP | All 3 models | One-shot, 2 nights | ~4h total |
| A.6 Swap decision | Human + harness output | N/A | After A.5 | ~30 min |
| A.7 Config swap + regression | All machines | Touched agents | One-shot | ~1h + overnight regression |
| D.1 SessionEnd hook | Any CC host | N/A | On session close (detached) | Hook <100ms |
| D.1 flush.py (simple <100 msg) | Mac Mini | `phi4-mini-reasoning` | Async | 5–10s |
| D.1 flush.py (complex ≥100 msg) | MacBook Pro (WOL) | `Qwen3-14B` via MLX-LM | Async | 30–90s |
| D.2.a Hash-state scan | Mac Mini | N/A (python) | Nightly 02:15 | <30s |
| D.2.b Synthesizer | MacBook Pro (WOL) | `Qwen3-14B` or `gemma4-31b`* | Nightly 02:30 → 03:15 | ~45 min |
| D.2.c WOL fallback | Mac Mini → PushNotification | N/A | On WOL timeout | <5s |
| D.3 Lint Tier 1 | Mac Mini | `phi4-mini-reasoning` | Sunday 22:00 | ~5 min |
| D.3 Lint Tier 2 | MacBook Pro (WOL, conditional) | `Qwen3-14B` | Sun 22:05 iff Tier 1 flags issues | ~15 min |
| D.3 Daily Driver alert | Mac Mini | (existing model) | Next morning 08:45 | +0s |
| D.4 Orchestrator read | Mac Mini | N/A (python) | Nightly 23:30 | <10s |
| D.4 Autoresearch body | Alienware | ComfyUI + Qwen3-VL (existing) | Nightly 00:00–06:00 | Unchanged |

*D.2 synthesizer model is **not hardcoded** — read from `routing.task_map["vault_synthesis"]` so A.6 swap decision flows through without code change.

**Cross-machine handoffs:**
- **D.2:** Mac Mini detects changes 02:15 → `wakeonlan <MBP-MAC>` → health-check MBP (port 8080) → synthesizer runs via `hybrid_router.route_to_macbook("vault_synthesis", payload)` → results written to `vault/knowledge/` (shared via existing vault path — no rsync).
- **D.3:** Mac Mini Tier 1 writes `tier1-issues.json` → if non-empty, trigger MBP Tier 2 via same hybrid_router path.
- **D.4:** Alienware autoresearch orchestrator reads `vault/knowledge/concepts/index.json` at 23:30 (reuses existing Phase 5 vault-read pattern — no new endpoint).

---

## 3. File-by-File Change List

### New agent files

| Path | State | ~Lines | Purpose | Imports |
|------|-------|--------|---------|---------|
| [agents-sdk/agents/flush.py](../../../agents-sdk/agents/flush.py) | **NEW** | 280 | Session transcript → daily log extractor (5-section structured output). Routes by message count. | `lib.config`, `lib.vault_io`, `lib.hybrid_router`, `lib.logging_setup`, `lib.filelock`, `lib.session_transcript`, `lib.skill_loader` (loads `preserve-session` skill) |
| [agents-sdk/agents/vault_synthesizer.py](../../../agents-sdk/agents/vault_synthesizer.py) | **NEW** | 420 | Concept + connection article generator. Reads changed files + nomic retrieval → LLM synthesis → writes `vault/knowledge/concepts/*.md` and `connections/*.md`. ≥2 wikilinks invariant enforced. | `lib.config`, `lib.vault_io`, `lib.hybrid_router`, `lib.filelock`, `lib.logging_setup`, `agents.vault_indexer` (reuses `search()` + `blob_to_embedding()`) |
| [agents-sdk/agents/knowledge_lint.py](../../../agents-sdk/agents/knowledge_lint.py) | **NEW** | 360 | Two-tier vault health scan. Tier 1 structural, Tier 2 semantic via hybrid_router. | `lib.config`, `lib.vault_io`, `lib.hybrid_router`, `lib.filelock`, `lib.logging_setup` |

### New library / tooling

| Path | State | ~Lines | Purpose | Imports |
|------|-------|--------|---------|---------|
| `agents-sdk/lib/filelock.py` | **NEW (P0.1)** | 40 | `fcntl.flock` context manager, LOCK_EX + LOCK_SH. | stdlib only |
| `agents-sdk/lib/session_transcript.py` | **NEW** | 120 | Parse Claude Code session transcripts (JSONL). Exposes `parse_transcript(path)`, `message_count()`, `extract_tool_calls()`. | stdlib only |
| `agents-sdk/lib/wol.py` | **NEW** | 90 | Wake-on-LAN + MBP health check + PushNotification fallback. Wraps `wakeonlan` binary. | `httpx`, `subprocess`, push-notification helper |
| `agents-sdk/lib/gemma4_benchmark.py` | **NEW** | 340 | Multi-model benchmark harness. p50/p95 latency, tok/s, Jaccard entity-similarity vs golden set. Writes `results/gemma4-benchmark-YYYY-MM-DD.json`. | `lib.hybrid_router`, `lib.config`, `httpx`, `time` |
| `agents-sdk/benchmarks/golden_sets/inbox_triage.json` | **NEW** | — | 20 email samples + expected categories + action items. |
| `agents-sdk/benchmarks/golden_sets/financial_analysis.json` | **NEW** | — | 20 CSV rows + expected categorization. Seed from Sean's sanitized finance CSVs via [lib/csv_sanitizer.py](../../../agents-sdk/lib/csv_sanitizer.py). |
| `agents-sdk/benchmarks/golden_sets/code_review.json` | **NEW** | — | 20 ~50-line Python snippets + expected issue lists. |
| `agents-sdk/scripts/phase6_gatecheck.py` | **NEW** | 150 | One-liner that runs all 6 gate-check verifications and emits pass/fail per criterion + overall verdict. |
| `agents-sdk/scripts/compare_convergence.py` | **NEW** | 120 | D.4 A/B harness. Wilcoxon signed-rank, paired nights, ≥10% gate. |

### New hook

| Path | State | ~Lines | Purpose |
|------|-------|--------|---------|
| `.claude/hooks/session-end-flush.sh` | **NEW** | 40 | SessionEnd hook. Checks `$CLAUDE_INVOKED_BY` for recursion guard (exit 0 if set). Else spawns `flush.py` detached via `nohup … &`. Hook returns <100ms so session close isn't blocked. Follows [run-tests-on-stop.sh](../../../.claude/hooks/run-tests-on-stop.sh) pattern (non-blocking bash, `exit 0` on success). Uses **exit code 2** only in recursion-guard-can't-log corner cases per [CLAUDE.md](../../../CLAUDE.md) hook rules. |

### Modified files

| Path | Delta | Purpose |
|------|-------|---------|
| [agents-sdk/agents/vault_indexer.py](../../../agents-sdk/agents/vault_indexer.py) | +130 lines | Hash-based state tracking (`vault/.indexer-state.json`), change detection, exclusion of `vault/daily/*` (extend `exclude_dirs` at [line 92](../../../agents-sdk/agents/vault_indexer.py#L92)), trigger synthesizer via hybrid_router when changes detected. |
| [agents-sdk/agents/daily_driver.py](../../../agents-sdk/agents/daily_driver.py) | +60 lines | In `build_preamble()` for `morning` mode, add Vault Health section: read latest `vault/health/YYYY-MM-DD-lint-report.md`, surface CRITICAL/HIGH counts + deep link. No report or all PASS → "Vault health: PASS ✓". Also surface WOL-failure PushNotifications since last run. |
| [agents-sdk/config.toml](../../../agents-sdk/config.toml) | +50 lines | Add `[agents.flush]`, `[agents.vault_synthesizer]`, `[agents.knowledge_lint]`. Add `[vault_indexer]` sub-config per SOT D.2 schema. Add `machines.macbook_pro.wol_mac` (P0.2). Update `[routing.task_map]` with `vault_synthesis`, `daily_flush_simple`, `daily_flush_complex`, `lint_tier1`, `lint_tier2`. Post-A.7: flip `inbox_triage` + (maybe) `financial_analysis`. |
| [agents-sdk/lib/hybrid_router.py](../../../agents-sdk/lib/hybrid_router.py) | +40 lines | Add `route_to_macbook(task_name, payload, timeout_s)` wrapper: WOL → health-check → POST. On WOL failure: call `wol.notify_wol_failure()` → raise `WOLUnavailable`. Callers handle: flush.py retries next session; synthesizer defers one night; lint Tier 2 skips. |
| [agents-sdk/schedules/install_schedules.sh](../../../agents-sdk/schedules/install_schedules.sh) | +30 lines | Add 2 plists: `com.sean.vault-synthesizer.plist` (02:30 daily), `com.sean.knowledge-lint.plist` (Sun 22:00). Flush is hook-triggered, NOT launchd. |
| [.claude/settings.json](../../../.claude/settings.json) | +8 lines | Register SessionEnd hook under `hooks.SessionEnd`. Path: `.claude/hooks/session-end-flush.sh`. |
| [CHANGELOG.md](../../../CHANGELOG.md) | +30 lines | v3.13.0 entry (see §8). |
| [CLAUDE.md](../../../CLAUDE.md) | +15 lines | Counts 13→16 agents, 7→8 hooks. Active-agents table. Architecture note. |
| [README.md](../../../README.md) | +10 lines | Counts + table rows matching CLAUDE.md. Knowledge compounding loop mention. |
| [SOURCE-OF-TRUTH.md](../../SOURCE-OF-TRUTH.md) | **NOT MODIFIED** | Spec is source of truth, not output. Open Questions 12–16 resolved here; SOT update deferred to post-phase-6 per "After finishing a Phase" rule in [16bitfit-battle-mode/CLAUDE.md](../../CLAUDE.md). |

### New directories

- `vault/daily/` — session logs (excluded from embed index)
- `vault/daily/INDEX.md` — MOC auto-maintained by flush.py
- `vault/knowledge/concepts/` — concept articles
- `vault/knowledge/connections/` — connection articles
- `vault/knowledge/index.md` — master catalog
- `vault/health/` — lint reports
- `agents-sdk/benchmarks/golden_sets/` — 3 golden sets
- `agents-sdk/benchmarks/results/` — benchmark JSON + MD outputs
- `agents-sdk/tests/fixtures/synthetic_vault/` — 30-file lint test vault
- `agents-sdk/tests/fixtures/transcripts/` — 3 synthetic CC transcripts

---

## 4. Test Strategy

### pytest additions

| New test file | Key cases | Fixtures |
|---------------|-----------|----------|
| `tests/test_filelock.py` | `test_ex_blocks_ex`, `test_sh_allows_concurrent_sh`, `test_context_manager_releases_on_exception`, `test_blocking_timeout` | `tmp_path` |
| `tests/test_flush.py` | `test_parses_short_transcript`, `test_routes_long_to_macbook`, `test_recursion_guard_blocks_nested_call`, `test_writes_5_sections`, `test_filelock_contention`, `test_daily_log_append_idempotent` | 3 synthetic transcripts (20/50/200 msg) in `fixtures/transcripts/`. Mock `hybrid_router.route_to_macbook`. |
| `tests/test_vault_synthesizer.py` | `test_detects_changed_files_via_hash`, `test_generates_concept_article`, `test_every_article_has_two_wikilinks`, `test_skips_excluded_paths`, `test_wol_failure_raises_and_notifies`, `test_index_md_regenerates`, `test_45min_budget_cap` | Synthetic 20-file vault in `tmp_path`. Mock MLX-LM endpoint with deterministic JSON. |
| `tests/test_knowledge_lint.py` | `test_tier1_broken_wikilink_caught`, `test_tier1_orphan_detected`, `test_tier1_kebab_case`, `test_tier2_contradiction_detected`, `test_tier2_stale_model_reference`, `test_recall_on_synthetic_vault` | **30-file synthetic vault with 20 planted issues** (see below). |
| `tests/test_gemma4_benchmark.py` | `test_latency_p50_p95`, `test_jaccard_entity_extraction`, `test_model_swap_veto_at_5pct`, `test_results_json_schema` | Stub Ollama/MLX responses. Golden sets from `benchmarks/golden_sets/`. |
| `tests/test_session_transcript.py` | `test_parse_jsonl`, `test_message_count_excludes_system`, `test_extract_tool_calls` | 3 transcripts in `fixtures/transcripts/`. |
| `tests/test_wol.py` | `test_magic_packet_format`, `test_health_check_timeout`, `test_pushnotification_on_failure` | Mock `subprocess` + `httpx.get`. |
| `tests/integration/test_hook_no_recursion.sh` | Shell test: start CC session, flush.py spawns sub-query with `CLAUDE_INVOKED_BY=flush`, hook exits 0, no second flush.py in `pgrep`, exactly 1 daily-log entry. |

### Synthetic 30-file vault (the ≥95% recall gate)

**Finding from Plan A:** with only 10 planted issues, the next integer threshold above 90% is 100% — making 95% impossible to hit precisely. Expand to 20 issues across 30 files so 19/20 = 95% is a clean pass.

**Location:** `agents-sdk/tests/fixtures/synthetic_vault/` — 20 markdown files with issues, 10 clean files as false-positive controls.

**Planted issue matrix (oracle):**

| Issue type | Count | Tier | Severity |
|---|---|---|---|
| Orphan files (0 inbound links) | 3 | Tier 1 | HIGH |
| Broken wikilinks `[[nonexistent]]` | 3 | Tier 1 | HIGH |
| Broken wikilinks to moved files | 2 | Tier 1 | HIGH |
| Missing YAML frontmatter | 2 | Tier 1 | MEDIUM |
| CamelCase filenames (kebab-case violation) | 2 | Tier 1 | LOW |
| Contradiction pairs | 2 pairs = 4 | Tier 2 | CRITICAL |
| Stale model references (Opus 4.1, Wan 2.2 5B, etc.) | 3 | Tier 2 | HIGH |
| **Total planted** | **20** | | |
| Clean controls | 10 | — | — |

**Gate:** ≥19/20 = 95% recall. Zero false positives on the 10 clean files.

### Integration tests

1. **SessionEnd hook recursion guard** (`tests/integration/test_hook_no_recursion.sh`): see above.
2. **WOL fallback** (`tests/integration/test_wol_fallback.py`): monkey-patch `wol.wake()` → False. Assert `WOLUnavailable` raised, PushNotification called with `title="MacBook WOL failed"`, body includes task + timestamp. Agent log records `"deferred"`, not `"error"`.
3. **D.2 mini-vault end-to-end** (`tests/integration/test_synthesizer_sandbox.py`): run synthesizer against 5-file `vault/_sandbox/` before real vault. Assert ≥1 concept article generated, all articles have ≥2 wikilinks, `index.md` updated.
4. **Autoresearch convergence A/B** (D.4 measurement): baseline 7 nights with `articles_used=0` enforced, treatment 7 nights with article injection. Metric: median trials-to-best-fitness (fitness exceeding run's median baseline + 1σ). Paired Wilcoxon signed-rank. **Gate: treatment median ≥10% lower than baseline, p < 0.1.** Artifacts → `vault/90_system/autoresearch-convergence-ab.md`.

---

## 5. Gate-Check Verification Plan

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | Gemma 4 benchmarks on 3 tasks with head-to-head scoring | `ls agents-sdk/benchmarks/results/gemma4-benchmark-*.json` ≥1 file; schema has `inbox_triage`, `financial_analysis`, `code_review` × 3–4 models; 60 samples total. |
| 2 | ≥1 model swap approved and deployed | `git log config.toml` shows Phase-6-window commit changing ≥1 `[routing.task_map]` entry; post-swap regression: 5/5 agents pass. Fallback if Gemma 4 loses all: commit benchmark doc + mark this bullet PARTIAL (see §7.1). |
| 3 | SessionEnd hook capturing ≥3 sessions/week | `ls vault/daily/ \| wc -l` ≥ 3 in any 7-day Phase 6 window; `grep -l "## Sessions" vault/daily/2026-07-*.md \| wc -l` ≥ 3. |
| 4 | ≥2 concept + ≥1 connection article per nightly run | `find vault/knowledge/concepts -newer vault/knowledge/.last-run -name "*.md" \| wc -l` ≥ 2 AND `find vault/knowledge/connections -newer … \| wc -l` ≥ 1, averaged across 7 nights. |
| 5 | Lint ≥95% recall on synthetic vault | `cd agents-sdk && .venv/bin/pytest tests/test_knowledge_lint.py::test_recall_on_synthetic_vault -v` reports recall ≥ 0.95 against 20-issue oracle. |
| 6 | Autoresearch convergence ≥10% improvement | `python3 agents-sdk/scripts/compare_convergence.py --baseline-dir results/baseline-week13 --treatment-dir results/treatment-week16` reports median improvement ≥10%, p<0.1. |

**One-liner:** `agents-sdk/scripts/phase6_gatecheck.py` runs all 6 and prints verdict.

---

## 6. Rollout Sequence (Jun 19 – Jul 17)

| Week | Dates | Workstream A | Workstream D | Deliverable |
|------|-------|--------------|--------------|-------------|
| 12.5 | Jun 16–18 | — | **P0.1 filelock.py + P0.2 MBP WOL** (½ day on MBP) | Blockers cleared. |
| 13 | Jun 19–25 | A.1 pull 27B MoE (Mon). A.2 pull 31B (Mon). A.3 harness (Tue–Thu). A.4 golden sets × 3 (Thu–Fri). | D.1.a hook + recursion guard (Mon). D.1.b flush.py + filelock + daily log format (Tue–Fri). D.1.c msg-count routing (Fri). | Harness + golden sets ready. Flush hook live for Sean's dogfooding. |
| 14 | Jun 26 – Jul 2 | A.5 60-sample run (Mon–Tue, 2 nights). A.6 swap decision (Wed). A.7 config.toml swap + overnight regression (Thu–Fri). | D.2.a hash tracking + `vault/daily/` exclusion (Mon). D.2.b `vault_synthesizer.py` on MBP (Tue–Thu). D.2.c WOL + PushNotification wiring (Fri). | Swap deployed (or PARTIAL doc). Synthesizer producing articles. |
| 15 | Jul 3–9 | — | D.3.a Tier 1 (Mon). D.3.b Tier 2 via hybrid_router (Tue–Wed). D.3.c synthetic 30-file vault + 95% recall (Thu). D.3.d daily_driver.py Vault Health (Fri). | Lint running Sun 22:00. Morning brief shows Vault Health. |
| 16 | Jul 10–17 | — | D.4.a orchestrator reads `vault/knowledge/concepts/` (Mon). D.4.b `articles_used` logging (Tue). D.4.c 7-night A/B + Wilcoxon (Wed–Fri). Gate check + doc updates (Mon Jul 14). Buffer (Tue–Thu Jul 17). | **Phase 6 PASS. v3.13.0 tagged.** |

**Constraints respected:**
- **Phase 5 runs in parallel** — only D.4.a modifies autoresearch orchestrator's startup read (additive).
- **Alienware stays focused** — no Phase 6 agent scheduled there; D.4 reads from Mac Mini vault.
- **No new API spend** — all local; monthly cost stays ~$12/mo (daily-driver morning unchanged).

---

## 7. Rollback & Open Decisions

### Rollback plan (per component — each disable-able in isolation)

| Component | Rollback |
|---|---|
| P0.1 filelock.py | Delete file. No agent will import it if P0.1 is rolled back pre-D.1. |
| P0.2 MBP WOL | Remove `wol_mac` from config. If always-on proves reliable, this is the happy path. |
| Gemma 4 swap (A.7) | Revert [config.toml](../../../agents-sdk/config.toml) `[routing.task_map]` to phi4/Qwen3. No schema change. |
| flush.py + SessionEnd hook | Remove `SessionEnd` block from [.claude/settings.json](../../../.claude/settings.json). Agent silent; daily logs are append-only (no downstream breakage). |
| vault_synthesizer.py | Set `synthesis_enabled = false` in `[vault_indexer]`. v2 falls back to v1 embedding-only. Existing articles preserved. |
| knowledge_lint.py | `launchctl bootout` the Sunday plist. Daily Driver integration guarded by "if report exists" — no report, no UI change. |
| D.4 wiring | Revert autoresearch orchestrator's vault-read step. `articles_used` counter drops to 0. |

### Open decisions

| # | SOT ref | Decision | Default | Flip evidence |
|---|---------|----------|---------|---------------|
| 7.1 | Q12 | Run A.7 optional autoresearch function-calling test? | **Defer to post-A.6.** Run only if Gemma 4 wins inbox triage ≥5% AND function-call success ≥98% on harness. | Benchmarks show Gemma 4 ≤ phi4-mini-reasoning → skip entirely. |
| 7.2 | Q13 | Daily logs inside vault vs parallel | **`vault/daily/` (inside)** — confirmed. | Indexer exclusion fails OR filelock contention >1/week in first month → move to parallel. |
| 7.3 | Q14 | Flush agent routing | **≥100 msgs → MBP Qwen3-14B** — confirmed. | phi4-mini extraction accuracy <85% on Decisions/Actions vs Preserve Session baseline → drop threshold to 50 or force all to Qwen3-14B. |
| 7.4 | Q16 | Convergence metric | **trials-to-best-fitness primary + final-fitness-delta secondary**, Wilcoxon paired — confirmed. | If σ > 0.3 × mean across nights, switch primary to final-fitness-delta. |
| 7.5 | D.3 line 544 | 95% recall requires ≥20 planted issues | **Oracle expanded to 20 issues / 30 files.** Test-design choice. | — |
| 7.6 | D.2 line 493 | WOL-failure behavior | **PushNotification (overrides SOT silent-defer)** — confirmed. | If push frequency >2/week for 1 month, add debounce (push only if failures ≥2 in 7 days). |
| 7.7 | Synthesis model | D.2 uses whatever A.6 picks | **Read from `routing.task_map["vault_synthesis"]` — never hardcoded.** | — |
| 7.8 | Hook registration | SessionEnd event reliability | Plan adds `hooks.SessionEnd` to settings.json. | If `claude --debug` shows SessionEnd doesn't fire reliably, fallback: wrapper tailing `~/.claude/logs/` for session-close. |
| 7.9 | P0.2 | MBP always-on vs WOL | **Plan assumes WOL (safer).** | If Sean confirms lid-open + caffeinate is reliable → simplify to `always_on = true`, remove `lib/wol.py` MBP path. |
| 7.10 | D.4 | Autoresearch feedback loop | **DESCOPED 2026-04-18.** Upstream autoresearch convergence harness is on a separate plan and not ready in the Phase 6 window. Knowledge graph ships without consumer; will be wired in a future phase when autoresearch is stable. | When autoresearch Phase 1+ lands a stable convergence harness with paired-nights data, re-open D.4 as a standalone mini-plan (est. ≤1 week: orchestrator read + `articles_used` logging + 7-night A/B + Wilcoxon). |

---

## E. Workstream E — Fleet Self-Monitoring (Meta-Agent)

**Status at adoption (2026-04-18):** Already implemented, deployed, dry-run verified. This section retroactively documents the component to match the rigor of A and D.

### E.0 Motivation

The April 9 audit left two active agents (`vault_indexer`, `daily_driver`) and six disabled. Phase 6 D adds three more writers (`flush`, `vault_synthesizer`, `knowledge_lint`) — growing the fleet to five active. Without a monitor, silent failures (the same class of failure that produced the April 9 audit) will recur.

Meta-Agent closes the loop: a morning health check that verifies each active agent ran successfully in the last 24 hours, checks the three-machine infrastructure (Mac Mini Ollama, Alienware Ollama + ComfyUI), and writes a human-readable status note into the vault. The Daily Driver morning brief surfaces any alerts.

### E.1 Spec

| Field | Value |
|---|---|
| Path | [agents-sdk/agents/meta_agent.py](../../../agents-sdk/agents/meta_agent.py) |
| Plist | [agents-sdk/schedules/com.sean.agent.meta-agent.plist](../../../agents-sdk/schedules/com.sean.agent.meta-agent.plist) |
| Machine | Mac Mini |
| Model | `phi4-mini-reasoning` (Ollama, local) — inference only for summary polish; most logic is deterministic Python |
| Schedule | 08:35 daily (10 minutes before Daily Driver at 08:45) |
| Safety | MAX_TURNS=10, MAX_BUDGET_USD=$0.10 (hard-coded in script; plist invokes script directly — no CLI budget flags) |
| Cost | $0.00 (local) |
| Deliverable | `vault/02_Areas/Agent-Fleet/daily-fleet-status-YYYY-MM-DD.md` + update `vault/02_Areas/Agent-Fleet/fleet-state.md` |
| Config section | `[agents.meta_agent]` in [agents-sdk/config.toml](../../../agents-sdk/config.toml), `enabled = true` |

### E.2 Health Checks

1. **Per-agent 24h recency check** — reads `vault/90_system/agent-logs/agent-run-history.csv`, confirms each `ACTIVE_AGENTS` entry ran in the last 24h with `status=success`.
2. **Infrastructure probes** — HTTP HEAD `{MINI_IP}:11434` (Mac Mini Ollama), `{ALIENWARE_IP}:11434` (Alienware Ollama), `{ALIENWARE_IP}:8188` (ComfyUI). Times out at 3s. Alienware being asleep is not an alert — WOL-on-demand is expected.
3. **Disabled-agent drift guard** — hard-coded `DISABLED_AGENT_COUNT = 6` per audit. If any disabled agent shows a `status=success` within 24h, raise a CRITICAL alert (someone re-enabled an agent without updating the audit).
4. **Alert surface** — any non-healthy finding → write to fleet-status note's "## Alerts" section → Daily Driver morning preamble pulls the most recent status file's alerts.

### E.3 Dependencies & Integration

- **Upstream:** depends on [agents-sdk/lib/logging_setup.py](../../../agents-sdk/lib/logging_setup.py)'s `record_run` CSV schema (already present).
- **Downstream (small modification to D.1 D.2 D.3):** each new Phase 6 agent's `record_run` call must include a consistent `agent_name` so Meta-Agent's per-agent recency check can match. Already satisfied — all three use the `AGENT_NAME` module constant.
- **No MCP dependencies** — pure file-reads + `httpx` for local LAN probes. Aligns with April 9 audit rule.
- **No WOL trigger** — Meta-Agent does not wake Alienware or MacBook Pro. Not finding them up is just "asleep, skipping probe" in the report, not a failure.

### E.4 Test Strategy

| Test file | Cases |
|---|---|
| `tests/test_meta_agent.py` | `test_recency_check_detects_stale_agent`, `test_recency_check_passes_on_fresh_run`, `test_infra_probe_timeouts_handled`, `test_disabled_agent_drift_raises_critical`, `test_fleet_status_markdown_structure`, `test_dry_run_does_not_write` |

Fixtures: synthetic `agent-run-history.csv` with mixed timestamps; mock `httpx` for infra probes.

### E.5 Gate #7 Verification

```bash
# Gate: ≥5 fleet-status artifacts in any 7-day window
find vault/02_Areas/Agent-Fleet -name "daily-fleet-status-*.md" -mtime -7 | wc -l  # ≥ 5

# Gate: ≥1 artifact in the window contains an actionable alert
grep -l "## Alerts" $(find vault/02_Areas/Agent-Fleet -name "daily-fleet-status-*.md" -mtime -7) | \
  xargs grep -L "No alerts" | wc -l  # ≥ 1
```

Added to `agents-sdk/scripts/phase6_gatecheck.py` as criterion #7.

### E.6 Rollback

- `launchctl bootout gui/$(id -u) com.sean.agent.meta-agent` to unload the schedule
- Set `enabled = false` in `[agents.meta_agent]`
- Daily Driver preamble must degrade gracefully when no fleet-status note exists for today — falls through to the existing "no fleet status" branch (already handled by "if report exists" guard pattern from D.3.d)

### E.7 Known Deviations from Pre-Existing Implementation

| Item | Planned here | Current state | Action |
|---|---|---|---|
| Plist invocation | Script via venv python | Previously called `claude -p` with invalid flags (exit 1) | **FIXED** 2026-04-18 in commit `9f7d85b` — plist now invokes `agents/meta_agent.py` via venv, PYTHONPATH set. Verified: `python3 agents/meta_agent.py --dry-run` → exit 0. |
| Active agents list | `["vault_indexer", "daily_driver"]` | Matches current script (line 41) | — |
| Disabled count | 6 | Matches current script (line 42) | If Phase 6 D ships, meta_agent.py needs update: `ACTIVE_AGENTS` gains `flush`, `vault_synthesizer`, `knowledge_lint`; disabled count stays 6. Track as **§E Week 16 task**. |

### E.8 Week 16 Task (post-D.3 ship)

Update [agents-sdk/agents/meta_agent.py](../../../agents-sdk/agents/meta_agent.py):
```python
ACTIVE_AGENTS = ["vault_indexer", "daily_driver", "flush", "vault_synthesizer", "knowledge_lint", "meta_agent"]
```
Plus a `test_active_agents_matches_config` that reads `config.toml` and fails if divergent. ~15 min of work; gates on Week 16 D.3 completion.

---

## 8. Doc-Update Checklist

Per [CLAUDE.md](../../../CLAUDE.md) "When Modifying" rules:

### `CHANGELOG.md` — add under `## [3.13.0] - 2026-07-17`

```
### Added
- lib/filelock.py — fcntl-based lock context manager (P0 blocker resolved)
- lib/session_transcript.py — CC session transcript parser
- lib/wol.py — Wake-on-LAN + MBP health check + PushNotification helper
- lib/gemma4_benchmark.py — multi-model benchmark harness
- 3 golden sets (inbox_triage, financial_analysis, code_review)
- 4 new agents: flush.py, vault_synthesizer.py, knowledge_lint.py, meta_agent.py (all $0.00 API)
- 1 new hook: session-end-flush.sh (SessionEnd, detached, recursion-guarded)
- Knowledge compounding loop: vault/daily/, vault/knowledge/concepts/, connections/, vault/health/
- scripts/compare_convergence.py + scripts/phase6_gatecheck.py

### Changed
- vault_indexer.py: hash-based change detection, vault/daily/* exclusion
- daily_driver.py morning mode: adds Vault Health section
- config.toml: new agent sections, [vault_indexer] block, macbook_pro.wol_mac, new task_map entries
- [routing.task_map]: <record actual A.7 swap, e.g., "inbox_triage now uses gemma4:27b (+18% speedup)">
- hybrid_router.py: adds route_to_macbook() with WOL + PushNotification fallback
```

### `CLAUDE.md`

- Intro line: **111 skills, 13 agents, 7 hooks** → **111 skills, 13 Claude Code subagents, 11 hooks, 13 autonomous SDK agents (6 active)** (updated 2026-04-18 to reflect actual file counts)
- Agents SDK table: add 4 rows (flush, vault_synthesizer, knowledge_lint, meta_agent) with schedule + $0.00 cost
- [16bitfit-battle-mode/CLAUDE.md](../../CLAUDE.md) Model-to-Machine Routing: update per A.7

### `README.md`

- Top-level counts: 13→16 agents, 7→8 hooks
- Mention knowledge compounding loop

### `export-groups/*/playground.json`

- No update — new items are agents + hooks, not skills. Export groups track skills only.

### Validation

- `python3 scripts/validate.py` → 0 errors.
- `cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/ -v` → all green (8 new test files).

---

## 9. Critical files to open first (implementation kickoff order)

When coding begins, load in this order on the MacBook Pro:

1. [SOURCE-OF-TRUTH.md](../../SOURCE-OF-TRUTH.md) lines 413–577 (spec re-read)
2. [agents-sdk/lib/vault_io.py](../../../agents-sdk/lib/vault_io.py) (confirm no hidden filelock before writing P0.1)
3. [agents-sdk/agents/vault_indexer.py](../../../agents-sdk/agents/vault_indexer.py) (the v1 you'll extend)
4. [agents-sdk/agents/daily_driver.py](../../../agents-sdk/agents/daily_driver.py) lines 1–120 (preamble pattern)
5. [agents-sdk/lib/hybrid_router.py](../../../agents-sdk/lib/hybrid_router.py) (extending with route_to_macbook)
6. [agents-sdk/lib/config.py](../../../agents-sdk/lib/config.py) (AgentConfig shape for new sections)
7. [agents-sdk/lib/baton.py](../../../agents-sdk/lib/baton.py) (dependency chain for indexer → synthesizer handoff)
8. [.claude/hooks/run-tests-on-stop.sh](../../../.claude/hooks/run-tests-on-stop.sh) (hook pattern to copy)
9. [agents-sdk/config.toml](../../../agents-sdk/config.toml) (sections you'll extend)

---

## 10. Descope Log

Items removed from Phase 6 scope mid-execution. Each retains a fully-specified re-open path so it can be picked up cleanly as a follow-on mini-plan.

### 10.1 D.4 — Autoresearch Feedback Loop (descoped 2026-04-18)

**Status:** Code not written. Knowledge graph (D.1–D.3) ships without a consumer.

**Reason for descope:** The upstream autoresearch convergence harness is being iterated on a separate plan and is not in a stable state. Integrating against a moving target would either:
- block Phase 6 indefinitely (wait for harness stability), or
- generate churn as we refactor against each new harness version.

Instead, we ship D.1–D.3 now, let the knowledge graph accumulate data nightly, and re-wire D.4 as a standalone one-week mini-plan once autoresearch is ready.

**What was planned (for when this is re-opened):**
- D.4.a: autoresearch orchestrator reads `vault/knowledge/concepts/index.json` at 23:30 nightly
- D.4.b: `articles_used` counter logged per autoresearch trial
- D.4.c: 7-night baseline (no articles) + 7-night treatment (articles injected) A/B
- Success metric: paired Wilcoxon signed-rank, ≥10% improvement in trials-to-best-fitness, p<0.1
- Rollback: revert orchestrator vault-read step; `articles_used` drops to 0

**Dependencies for re-opening:**
1. Autoresearch convergence harness lands on main with a stable API
2. Phase 6 D.2 has produced ≥14 concept articles and ≥7 connection articles (Gate #4 PASS for real)
3. Baseline convergence data exists for ≥7 nights

**Artifacts preserved:**
- `agents-sdk/scripts/compare_convergence.py` — already written, ready to use
- §3 of this plan still documents the intended file-change list
- Gate #6 marked `DESCOPED` in `phase6_gatecheck.py` (stays as a non-PASS indicator until the mini-plan executes)

**Impact on Phase 6 exit:**
- Phase 6 ships with 5 of 7 gates PASSing (1, 2, 5, plus 3, 4 once production runs accrue data) + Gate 7 PASSing after one week of meta-agent runs. Gate 6 parked.
- No blocker for v3.14.0 tag. CHANGELOG v3.14.0 explicitly calls out D.4 descope.

---

## Verification (this plan is ready when…)

- [x] All SOT tasks A.1–A.7 and D.1–D.4 covered with a specific file or action
- [x] Workstream E (Meta-Agent / Fleet Self-Monitoring) documented with spec, tests, gate, and rollback (retroactive adoption 2026-04-18)
- [x] D.4 descope documented with re-open plan, dependency list, and preserved artifacts (§10.1, 2026-04-18)
- [x] Every new agent is 100% local ($0.00 API)
- [x] Zero new MCP dependencies for launchd agents (April 9 audit respected)
- [x] Hooks use correct exit codes (0=continue, 2=deny) per CLAUDE.md
- [x] `SOURCE-OF-TRUTH.md` not modified
- [x] All 6 gate-check criteria have concrete verification commands
- [x] Doc updates scoped (CHANGELOG, CLAUDE.md, README.md)
- [x] P0 blockers (missing filelock + missing MBP WOL) surfaced before coding starts
- [x] 20-issue / 30-file oracle fixes the 95% integer-math problem
- [x] Wilcoxon + paired nights for D.4 statistical rigor
- [x] Rollback path per component, disable-able in isolation
- [x] Previously-resolved Sean ambiguities locked in (WOL→push, ≥100-msg, trials-to-best, inside-vault, A∥D)

When approved, coding starts with **P0.1 + P0.2 on MacBook Pro (Jun 16–18)**, then forks into A track + D.1 track Jun 19.
