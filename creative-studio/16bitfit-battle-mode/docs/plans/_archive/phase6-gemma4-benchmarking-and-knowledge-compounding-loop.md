# Phase 6 Execution Plan — Gemma 4 Benchmarking + Knowledge Compounding Loop

**Window:** Jun 19 – Jul 17 (Weeks 13–16), parallel with Phase 5 autoresearch.
**Spec source:** `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` lines 413–577 (do not modify).
**Plan author:** Claude Opus 4.7 · Plan Mode · 2026-04-16.

---

## Context

Phases 1–5 delivered agents, sprite pipeline, and the Phase 5 autoresearch loop. Phase 6 adds the meta-layer:

1. **Workstream A — Gemma 4 model swap.** Gemma 4's 6 native function-calling tokens and 27B-MoE/3.8B-active efficiency make it a credible replacement for `phi4-mini-reasoning` (Mac Mini) and a benchmark challenger to `Qwen3-14B` (MacBook Pro). We must benchmark before swapping — veto gate is ≥5% quality regression.
2. **Workstream D — Knowledge Compounding Loop.** Four new components (SessionEnd flush → Vault Synthesizer v2 → Knowledge Lint → autoresearch feedback) transform the vault from static archive into a living knowledge graph (Karpathy LLM-Wiki / cole's claude-memory-compiler pattern). Feeds Phase 5 autoresearch for faster Optuna convergence.

All Phase 6 code runs 100% local ($0.00 API). Adds 3 agents + 1 hook to the fleet (14 total steady-state). Respects the April 9 audit: no new launchd MCP dependencies.

**Sean's resolved ambiguities (captured in AskUserQuestion):**
- A and D run in **parallel**, not serially.
- Daily logs **excluded** from nomic-embed index (SOT D.1 line 482).
- WOL failure → **PushNotification to Sean** (override SOT's "silent defer").
- Flush routing = **message count threshold** (<100 → phi4-mini; ≥100 → Qwen3-14B).
- Convergence metric = **trials-to-best-fitness** (SOT D.4 line 558).

---

## 1. Dependency Graph

```
                Phase 5 autoresearch running (prerequisite for D.4 only)
                          │
                          ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ WEEK 13 (Jun 19-25) — Parallel tracks                                    │
└──────────────────────────────────────────────────────────────────────────┘
   ┌──────────── Workstream A ────────────┐       ┌──────────── Workstream D ───────────┐
   │                                      │       │                                      │
   │   A.1  A.2                           │       │   D.1.a  flush.py skeleton          │
   │   (Ollama pull) (MLX-LM download)    │       │   (hook + recursion guard)          │
   │        │                             │       │                                      │
   │        ▼                             │       │        ▼                             │
   │   A.3  gemma4_benchmark.py harness   │       │   D.1.b  transcript extractor +     │
   │        │                             │       │        filelock + daily log format  │
   │        ▼                             │       │        │                             │
   │   A.4  golden test sets (3×20)       │       │        ▼                             │
   │        │                             │       │   D.1.c  routing (<100 vs ≥100)    │
   │        ▼                             │       │                                      │
   │   A.5  60-sample benchmark run  ─────┼───────┤                                      │
   └──────────────────────────────────────┘       └──────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ WEEK 14 (Jun 26 - Jul 2) — Results + Synthesizer                         │
└──────────────────────────────────────────────────────────────────────────┘
   A.6  swap decision ──────┐                D.2.a  vault_indexer.py hash state tracking
         │ (veto gate)      │                      │
         ▼                  │                      ▼
   A.7  config.toml swap ───┼────────► ◄─── D.2.b  vault_synthesizer.py (concept+connect)
         + regression test  │                      │
                            │                      ▼
                            │                D.2.c  WOL + PushNotification fallback
                            │                      │
                            └──► synthesis_model ──┘ (Qwen3-14B or Gemma4-31B if A wins)

┌──────────────────────────────────────────────────────────────────────────┐
│ WEEK 15 (Jul 3-9) — Lint + Integration                                   │
└──────────────────────────────────────────────────────────────────────────┘
   D.3.a  knowledge_lint.py Tier 1 (structural)
          │
          ▼
   D.3.b  Tier 2 (semantic, via hybrid_router)
          │
          ▼
   D.3.c  synthetic 20-file test vault (95% recall gate)
          │
          ▼
   D.3.d  daily_driver.py morning Vault Health section

┌──────────────────────────────────────────────────────────────────────────┐
│ WEEK 16 (Jul 10-17) — Feedback Loop + Gate Check                         │
└──────────────────────────────────────────────────────────────────────────┘
   D.4.a  autoresearch orchestrator reads vault/knowledge/concepts/
          │  (needs Phase 5 autoresearch live + D.2 producing articles for ≥3 nights)
          ▼
   D.4.b  log articles_used in run metadata
          │
          ▼
   D.4.c  A/B trials-to-best-fitness comparison (≥10% improvement gate)
          │
          ▼
   Gate check: all 6 Phase 6 success criteria verified
```

**Parallelism flags:**
- A.1 ∥ A.2 (model downloads on different machines)
- A track ∥ D.1 (different files, no shared state)
- D.3 can begin once D.2 has produced ≥1 synthesis run (Week 15)
- D.4 is the only task with a hard Phase 5 dependency

---

## 2. Machine + Schedule Map

| Task | Machine | Model | Schedule / Trigger | Runtime |
|------|---------|-------|-------------------|---------|
| A.1 Gemma 4 27B MoE pull | Mac Mini | `gemma4:27b` via Ollama | One-shot | ~15 min download |
| A.2 Gemma 4 31B pull | MacBook Pro | `gemma4-31b` via MLX-LM | One-shot | ~20 min download |
| A.3 Build harness | MacBook Pro (dev) | N/A | One-shot | ~10h dev |
| A.4 Golden sets | MacBook Pro (dev) | N/A | One-shot | ~6h curation |
| A.5 60-sample benchmark | Mac Mini + MacBook Pro | All 3 models | One-shot, 2 nights | ~4h total |
| A.6 Swap decision | Human + harness output | N/A | After A.5 | ~30 min review |
| A.7 Config swap + regression | All machines | Touched agents | One-shot | ~1h + overnight regression |
| D.1 SessionEnd hook | Whichever host ran Claude Code | N/A | On session close (detached bg) | Hook <100ms |
| D.1 flush.py (simple) | Mac Mini | `phi4-mini-reasoning` | Async, <100 msg sessions | 5–10s |
| D.1 flush.py (complex) | MacBook Pro (WOL) | `Qwen3-14B` via MLX-LM | Async, ≥100 msg sessions | 30–90s |
| D.2.a Hash-state scan | Mac Mini | N/A (python) | Nightly 02:15 (after embedding) | <30s |
| D.2.b Synthesizer | MacBook Pro (WOL) | `Qwen3-14B` or `gemma4-31b` | Nightly 02:30 → done by 03:15 | ~45 min |
| D.2.c WOL fallback | Mac Mini → PushNotification | N/A | On WOL timeout | <5s |
| D.3 Lint Tier 1 | Mac Mini | `phi4-mini-reasoning` | Sunday 22:00 | ~5 min |
| D.3 Lint Tier 2 | MacBook Pro (WOL, conditional) | `Qwen3-14B` | Sun 22:05 iff Tier 1 flagged issues | ~15 min |
| D.3 Daily Driver alert | Mac Mini | Opus 4.6 (existing) | Next morning 08:45 | +0s (reads report) |
| D.4 Orchestrator read | Mac Mini | N/A (python) | Nightly 23:30 (before autoresearch) | <10s |
| D.4 Autoresearch body | Alienware | ComfyUI + Qwen3-VL (existing) | Nightly 00:00–06:00 | Unchanged |

**Cross-machine handoffs:**
- D.2: Mac Mini detects changes 02:15 → `wakeonlan B4:E9:B8:F7:71:47` → health-check MacBook Pro (8080) → synthesizer runs remotely via `hybrid_router.route()` → results written back to `vault/knowledge/` (local disk share or rsync).
- D.3: Mac Mini Tier 1 writes `tier1-issues.json` → if non-empty, triggers MacBook Pro Tier 2 via same hybrid_router path.
- D.4: Alienware autoresearch orchestrator polls Mac Mini for `vault/knowledge/concepts/index.json` at 23:30 (existing Phase 5 REST endpoint pattern).

---

## 3. File-by-File Change List

### New agent files

| Path | State | ~Lines | Purpose | Imports from |
|------|-------|--------|---------|--------------|
| `agents-sdk/agents/flush.py` | **NEW** | 280 | Session transcript → daily log extractor (5-section structured output). Routes by message count. | `lib.config`, `lib.vault_io`, `lib.hybrid_router`, `lib.logging_setup`, `lib.skill_loader` (loads `preserve-session` skill) |
| `agents-sdk/agents/vault_synthesizer.py` | **NEW** | 420 | Concept + connection article generator. Reads changed files + nomic retrieval → LLM synthesis → writes `vault/knowledge/concepts/*.md` and `connections/*.md`. | `lib.config`, `lib.vault_io`, `lib.hybrid_router`, `lib.logging_setup`, `agents.vault_indexer` (reuses `search()` and `blob_to_embedding()`) |
| `agents-sdk/agents/knowledge_lint.py` | **NEW** | 360 | Two-tier vault health scan. Tier 1: structural (wikilinks, orphans, frontmatter). Tier 2: semantic (contradictions, staleness) via hybrid_router. | `lib.config`, `lib.vault_io`, `lib.hybrid_router`, `lib.logging_setup` |

### New library / tooling

| Path | State | ~Lines | Purpose | Imports |
|------|-------|--------|---------|---------|
| `agents-sdk/lib/gemma4_benchmark.py` | **NEW** | 340 | Multi-model benchmark harness. Runs same prompt across N models; measures p50/p95 latency, tok/s, Jaccard entity-similarity vs golden set. Writes `results/gemma4-benchmark-YYYY-MM-DD.json`. | `lib.hybrid_router`, `lib.config`, `httpx`, `time`, standard JSON |
| `agents-sdk/lib/session_transcript.py` | **NEW** | 120 | Helper to parse Claude Code session transcripts (JSON Lines format). Exposes `parse_transcript(path)`, `message_count()`, `extract_tool_calls()`. | stdlib only |
| `agents-sdk/lib/wol.py` | **NEW** | 90 | Wake-on-LAN helper + MacBook Pro health check + PushNotification fallback. Wraps `wakeonlan` binary. | `httpx`, `subprocess`, push-notification helper |
| `agents-sdk/benchmarks/golden_sets/inbox_triage.json` | **NEW** | n/a | 20 email samples + expected categories + action items. | — |
| `agents-sdk/benchmarks/golden_sets/financial_analysis.json` | **NEW** | n/a | 20 CSV rows + expected categorization. | — |
| `agents-sdk/benchmarks/golden_sets/code_review.json` | **NEW** | n/a | 20 50-line Python snippets + expected issue lists. | — |

### New hook

| Path | State | ~Lines | Purpose | Convention match |
|------|-------|--------|---------|------------------|
| `.claude/hooks/session-end-flush.sh` | **NEW** | 40 | SessionEnd hook. Reads `$CLAUDE_INVOKED_BY` env var; if set, `exit 0` (recursion guard). Else spawns `flush.py` detached via `nohup … &`. Hook returns immediately so session close isn't blocked. | Follows `run-tests-on-stop.sh` pattern: bash, non-blocking, `exit 0` on success. Uses **exit code 2** only for recursion-guard-but-can't-log situations. |

### Modified files

| Path | State | Delta | Purpose |
|------|-------|-------|---------|
| `agents-sdk/agents/vault_indexer.py` | **MODIFIED** | +130 lines | Add hash-based state tracking (`vault/.indexer-state.json`), change detection, exclusion of `vault/daily/*`, trigger synthesizer via hybrid_router when changes detected. Exclusion list in `discover_vault_files()` already excludes `.obsidian` — extend to add `daily`. |
| `agents-sdk/agents/daily_driver.py` | **MODIFIED** | +60 lines | In `build_preamble()` for `morning` mode, add Vault Health section: read latest `vault/health/YYYY-MM-DD-lint-report.md`, surface CRITICAL/HIGH counts + deep link. If no report or all PASS → "Vault health: PASS ✓". Also surface any WOL-failure PushNotification summaries since last run. |
| `agents-sdk/config.toml` | **MODIFIED** | +50 lines | Add `[agents.flush]`, `[agents.vault_synthesizer]`, `[agents.knowledge_lint]` sections. Add `[vault_indexer]` sub-config per SOT D.2 schema. Update `[routing.task_map]` with `vault_synthesis`, `daily_flush_simple`, `daily_flush_complex`, `lint_tier1`, `lint_tier2` entries. Post-A.7: flip model assignments in `inbox_triage` and (maybe) `financial_analysis`. |
| `agents-sdk/lib/hybrid_router.py` | **MODIFIED** | +40 lines | Add `route_to_macbook(task_name, payload, timeout_s)` helper that wraps WOL → health-check → POST. On WOL failure: call `wol.notify_wol_failure()` → raise `WOLUnavailable`. Callers decide: flush.py retries next session; synthesizer defers one night; lint Tier 2 skips. |
| `agents-sdk/schedules/install_schedules.sh` | **MODIFIED** | +30 lines | Add 3 new plists: `com.sean.vault-synthesizer.plist` (02:30 daily), `com.sean.knowledge-lint.plist` (Sunday 22:00 weekly). Flush agent is NOT a launchd entry — it's hook-triggered. |
| `.claude/settings.json` | **MODIFIED** | +8 lines | Register the new SessionEnd hook under `hooks.SessionEnd`. Path: `.claude/hooks/session-end-flush.sh`. |
| `CHANGELOG.md` | **MODIFIED** | +30 lines | v3.13.0 entry: 3 new agents, 1 new hook, Gemma 4 benchmark, vault knowledge graph. |
| `CLAUDE.md` | **MODIFIED** | +15 lines | Update agent/hook counts (13→16, 7→8). Update "Active agents" table. Update architecture tree. |
| `README.md` | **MODIFIED** | +10 lines | Update counts and table rows matching CLAUDE.md. |
| `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` | **NOT MODIFIED** | 0 | Spec is source of truth, not output. Open Questions 12–16 resolved in this plan, but SOT update deferred to post-phase-6-completion per the "After finishing a Phase, update the checklist" rule in `16bitfit-battle-mode/CLAUDE.md`. |

### New directories created

- `vault/daily/` — daily session logs (excluded from embed index)
- `vault/daily/INDEX.md` — MOC listing logs by date (auto-maintained by flush.py)
- `vault/knowledge/` — synthesizer output root
- `vault/knowledge/concepts/` — concept articles
- `vault/knowledge/connections/` — connection articles
- `vault/knowledge/index.md` — master catalog (auto-maintained)
- `vault/health/` — lint reports
- `agents-sdk/benchmarks/` — golden sets + results
- `agents-sdk/benchmarks/results/` — Gemma 4 benchmark run outputs

---

## 4. Test Strategy

### pytest additions (`agents-sdk/tests/`)

| New test file | Key test cases | Fixture strategy |
|---------------|----------------|------------------|
| `tests/test_flush.py` | `test_parses_short_transcript`, `test_routes_long_to_macbook`, `test_recursion_guard_blocks_nested_call`, `test_writes_5_sections`, `test_filelock_contention`, `test_daily_log_append_idempotent` | `tmp_path` fixture with 3 synthetic transcripts: 20-msg, 50-msg, 200-msg. Mock `hybrid_router.route_to_macbook` to return canned extraction. |
| `tests/test_vault_synthesizer.py` | `test_detects_changed_files_via_hash`, `test_generates_concept_article_for_new_topic`, `test_every_article_has_two_wikilinks`, `test_skips_excluded_paths`, `test_wol_failure_raises_and_notifies`, `test_index_md_regenerates` | Synthetic 20-file vault in `tmp_path`. Mock MLX-LM endpoint with deterministic JSON response. |
| `tests/test_knowledge_lint.py` | `test_tier1_broken_wikilink_caught`, `test_tier1_orphan_detected`, `test_tier1_kebab_case_violation`, `test_tier2_contradiction_detected`, `test_tier2_stale_model_reference`, `test_report_severity_format` | **20-file synthetic vault with planted issues** (see below) — used for 95% recall gate. |
| `tests/test_gemma4_benchmark.py` | `test_latency_p50_p95_calculation`, `test_jaccard_entity_extraction`, `test_model_swap_veto_at_5pct_regression`, `test_results_json_schema` | Stub Ollama/MLX-LM responses. Golden-set fixtures copied from `agents-sdk/benchmarks/golden_sets/`. |
| `tests/test_session_transcript.py` | `test_parse_jsonl_transcript`, `test_message_count_excludes_system`, `test_extract_tool_calls` | 3 synthetic transcript fixtures in `tests/fixtures/transcripts/`. |
| `tests/test_wol.py` | `test_wol_magic_packet_format`, `test_health_check_timeout`, `test_pushnotification_sent_on_failure` | Mock `subprocess` and `httpx.get`; assert PushNotification called with correct payload. |
| `tests/test_hook_recursion_guard.py` | `test_hook_exits_0_when_claude_invoked_by_set`, `test_hook_spawns_flush_when_unset`, `test_hook_never_blocks_session_close` | Shell test using `bash -c` subprocess; set/unset env var; assert exit code + pgrep for detached process. |

### Synthetic 20-file vault for D.3 (the 95% recall gate)

**Location:** `agents-sdk/tests/fixtures/synthetic_vault/` (20 markdown files planted with known issues).

**Planted issue matrix (the oracle):**

| File | Planted issue | Detector tier | Expected severity |
|------|--------------|---------------|-------------------|
| `concepts/orphan-a.md` | Zero inbound links | Tier 1 | HIGH |
| `concepts/orphan-b.md` | Zero inbound links | Tier 1 | HIGH |
| `concepts/broken-link-1.md` | `[[nonexistent-target]]` | Tier 1 | HIGH |
| `concepts/broken-link-2.md` | `[[concepts/moved-file]]` (moved elsewhere) | Tier 1 | HIGH |
| `concepts/no-frontmatter.md` | Missing YAML header | Tier 1 | MEDIUM |
| `concepts/CamelCaseName.md` | Violates kebab-case | Tier 1 | LOW |
| `concepts/contradicts-a.md` | Says "RIFE is the primary" | Tier 2 | CRITICAL (pair) |
| `concepts/contradicts-b.md` | Says "GMFSS is the primary" | Tier 2 | CRITICAL (pair) |
| `concepts/stale-opus-4.1.md` | References deprecated model, date 2025-06 | Tier 2 | HIGH |
| `concepts/stale-wan-2.2-5b.md` | References deprecated model | Tier 2 | HIGH |
| `concepts/healthy-1.md` through `healthy-10.md` | NO issues (false-positive control) | — | — |

**Oracle total:** 10 planted issues across 20 files. **Recall gate:** ≥9 of 10 caught = 90% (the ≥95% SOT target is a stretch; with 10 issues, next valid integer pass is 10/10). **Assumption:** oracle expanded to 20 planted issues across a 30-file vault to make 95% (19/20) a valid integer threshold. Flagged in Section 7.

### Integration tests (end-to-end)

1. **SessionEnd hook recursion guard** (`tests/integration/test_hook_no_recursion.sh`):
   - Start a mock Claude Code session, have flush.py spawn its own sub-query with `CLAUDE_INVOKED_BY=flush` set.
   - Sub-query's SessionEnd hook must exit 0 without spawning another flush.
   - Verify: exactly 1 entry in daily log, no zombie processes, no second flush.py in `pgrep`.

2. **WOL fallback** (`tests/integration/test_wol_fallback.py`):
   - Monkey-patch `wol.wake()` to return False.
   - Call `hybrid_router.route_to_macbook("vault_synthesis", payload)`.
   - Assert `WOLUnavailable` raised, PushNotification helper called with `title="MacBook WOL failed"`, `body` includes task name + timestamp.
   - Assert agent-log records "deferred" status, not "error".

3. **Autoresearch convergence A/B** (D.4 measurement):
   - **Baseline capture (Week 13–14, overlaps Phase 5):** Run Phase 5 autoresearch for 7 nights with `articles_used=0` enforced. Record trials-to-best-fitness (where "best" = fitness score exceeding the run's median baseline + 1σ).
   - **Treatment capture (Week 16):** Run 7 nights with D.4 article injection active. Record same metric.
   - **Metric:** median trials-to-best-fitness, paired-nights comparison via Wilcoxon signed-rank test. **Gate: treatment median ≥10% lower than baseline, p < 0.1.**
   - **Artifacts:** `vault/90_system/autoresearch-convergence-ab.md` with raw per-night numbers + test output.

---

## 5. Gate-Check Verification Plan

Each of SOT's 6 success criteria (lines 420–425) mapped to a concrete command or artifact:

| # | Success criterion | Verification |
|---|------------------|--------------|
| 1 | Gemma 4 benchmarks complete on all 3 routing tasks with head-to-head scoring | `ls agents-sdk/benchmarks/results/gemma4-benchmark-*.json` shows ≥1 file; JSON schema has entries for `inbox_triage`, `financial_analysis`, `code_review` across `phi4-mini-reasoning`, `qwen3-14b`, `gemma4-27b`, `gemma4-31b`; 60 samples total. |
| 2 | ≥1 model swap approved and deployed based on winning benchmark | `git log config.toml` shows a commit in the Phase 6 window changing at least one entry in `[routing.task_map]`; regression test run afterwards shows 5/5 agents pass. |
| 3 | SessionEnd hook active and capturing ≥3 sessions/week | `ls vault/daily/ | wc -l` ≥ 3 for any 7-day window within Phase 6. `grep -l "## Sessions" vault/daily/2026-07-*.md | wc -l` ≥ 3. |
| 4 | Vault Indexer synthesis producing ≥2 concept articles + ≥1 connection article per nightly run | `find vault/knowledge/concepts -newer vault/knowledge/.last-run -name "*.md" | wc -l` ≥ 2 AND `find vault/knowledge/connections -newer vault/knowledge/.last-run -name "*.md" | wc -l` ≥ 1, averaged across 7 nights. |
| 5 | Knowledge Lint detecting structural issues with ≥95% recall on synthetic test vault | `cd agents-sdk && .venv/bin/pytest tests/test_knowledge_lint.py::test_recall_on_synthetic_vault -v` reports recall ≥ 0.95 (given expanded 20-issue oracle — see assumption in §7). |
| 6 | Autoresearch convergence improves ≥10% | `python3 agents-sdk/scripts/compare_convergence.py --baseline-dir results/baseline-week13 --treatment-dir results/treatment-week16` reports median improvement ≥10% with p<0.1. |

**One-liner phase-6-gatecheck script:** `agents-sdk/scripts/phase6_gatecheck.py` runs all 6 checks and emits pass/fail per criterion + overall verdict. Deliverable: committed as part of D.4.

---

## 6. Rollout Sequence (Jun 19 – Jul 17)

| Week | Dates | Workstream A | Workstream D | Deliverable |
|------|-------|--------------|--------------|-------------|
| 13 | Jun 19–25 | A.1 pull Gemma 4 27B MoE (Mon). A.2 pull Gemma 4 31B (Mon). A.3 build `gemma4_benchmark.py` (Tue–Thu). A.4 golden sets × 3 (Thu–Fri). | D.1.a `session-end-flush.sh` + recursion guard (Mon). D.1.b `flush.py` + filelock + `vault/daily/` format (Tue–Fri). D.1.c routing by message count (Fri). | Harness + golden sets ready. Flush hook live for Sean's dogfooding. |
| 14 | Jun 26 – Jul 2 | A.5 run 60 benchmark samples (Mon–Tue, 2 nights). A.6 review results + swap decision (Wed). A.7 config.toml swap + overnight regression (Thu–Fri). | D.2.a `vault_indexer.py` hash tracking + daily-exclusion (Mon). D.2.b `vault_synthesizer.py` on MacBook Pro (Tue–Thu). D.2.c WOL + PushNotification wiring (Fri). | Swap deployed. Synthesizer producing articles nightly. |
| 15 | Jul 3–9 | — (A complete) | D.3.a Tier 1 lint (Mon). D.3.b Tier 2 lint via hybrid_router (Tue–Wed). D.3.c synthetic vault + 95% recall (Thu). D.3.d `daily_driver.py` Vault Health section (Fri). | Lint running Sun 22:00. Morning brief shows Vault Health. |
| 16 | Jul 10–17 | — | D.4.a autoresearch orchestrator reads `vault/knowledge/concepts/` (Mon). D.4.b `articles_used` logging (Tue). D.4.c A/B comparison against Week 13–14 baseline (Wed–Fri). Gate check + doc updates (Mon Jul 14). Contingency + cleanup (Tue–Thu Jul 17). | Phase 6 gate check **PASS**. v3.13.0 tagged. |

**Respecting the constraints:**
- **Phase 5 runs in parallel:** Phase 5 autoresearch continues uninterrupted on Alienware; only D.4.a modifies the orchestrator's startup-read to include `vault/knowledge/concepts/` (additive, not destructive).
- **Alienware stays focused on autoresearch:** No Phase 6 agent is scheduled on Alienware. Only D.4 reads from vault on Mac Mini; Alienware workload unchanged.
- **No new API spend:** All 3 new agents are local-only. Gemma 4 benchmarks use local Ollama/MLX-LM. Monthly API cost stays at ~$12/mo (daily-driver morning, unchanged).

---

## 7. Open Decisions To Resolve Before Coding

Plan assumptions that should be confirmed before the first commit. **Flag each with Sean in the first coding session.**

| # | SOT ref | Assumption this plan makes | Why to double-check |
|---|---------|----------------------------|---------------------|
| 7.1 | SOT Q12 (line 603) | Gemma 4 function-calling benefit is **measured in A.5** (quality/latency), not a separate autoresearch-specific benchmark. If Gemma 4 27B MoE wins inbox triage but Sean wants specific autoresearch-orchestrator benchmarking, add an A.8 task. | A.7 (optional) in SOT is conditional on A.6 outcome. |
| 7.2 | SOT Q13 (line 605) | Daily logs live at `vault/daily/` **inside** the vault (Obsidian-visible). Filelock coordinates with Vault Indexer via existing `lib/filelock`. | Confirmed by user answer: "Exclude (per SOT D.1 line 482)" implies inside-vault placement. Plan treats this as locked. |
| 7.3 | SOT Q14 (line 607) | Flush uses **message count ≥100** as routing threshold, NOT token count, tag metadata, or transcript size. | **Confirmed by Sean.** |
| 7.4 | SOT Q16 (line 611) | Convergence measured via **trials-to-best-fitness**, compared paired-nights with Wilcoxon. 7-night baseline + 7-night treatment = 14 nights of runtime inside Phase 6 window. | **Confirmed by Sean.** Risk: if Phase 5 autoresearch isn't producing stable baselines by Jun 19, baseline capture slips. |
| 7.5 | SOT D.3 line 544 | 95% recall on synthetic vault requires ≥20 planted issues (can't hit 95% with 10). Plan expands oracle to 20 issues across a 30-file vault. | Pure test-design choice; not covered in SOT. Flagging for visibility. |
| 7.6 | SOT D.2 line 493 vs user answer | **User overrode SOT's silent-defer to PushNotification on WOL failure.** Plan uses push. If chronic WOL failures begin paging Sean too often, add a debounce (e.g., push only if failures ≥2 in 7 days). | Confirmed. Debounce logic is a stretch goal. |
| 7.7 | D.2 synthesis model | If A.6 swap decision ships Gemma 4 31B to MacBook Pro, D.2 uses Gemma 4 31B. If A.6 keeps Qwen3-14B, D.2 uses Qwen3-14B. **D.2 code must be model-agnostic via hybrid_router** — not hardcoded. | Plan addresses by using `routing.task_map["vault_synthesis"]` to drive the choice. |
| 7.8 | Hook vs event | SOT says "SessionEnd hook." The `.claude/hooks/` directory currently has no `SessionEnd` event registered in `settings.json`. Plan adds one. | Verify with `claude --debug` that SessionEnd fires reliably in Sean's current harness version before committing — otherwise fall back to a wrapper script that tails `~/.claude/logs/` for session-close events. |

---

## 8. Doc-Update Checklist

Per `CLAUDE.md` "When Modifying" rules, these edits MUST ship with the phase-6 completion commit:

### `CHANGELOG.md`
Add under a new `## [3.13.0] - 2026-07-17` heading:
```
### Added
- 3 new agents: flush.py, vault_synthesizer.py, knowledge_lint.py (all 100% local, $0.00 API)
- 1 new hook: session-end-flush.sh (SessionEnd, detached background, recursion-guarded)
- Gemma 4 model benchmark harness (lib/gemma4_benchmark.py) + 3 golden sets
- Knowledge compounding loop: vault/daily/, vault/knowledge/concepts/, vault/knowledge/connections/, vault/health/
- Autoresearch convergence A/B measurement script (scripts/compare_convergence.py)
- Phase 6 gate check script (scripts/phase6_gatecheck.py)

### Changed
- vault_indexer.py: adds hash-based change detection, excludes vault/daily/*
- daily_driver.py morning mode: adds Vault Health section
- config.toml: new [agents.flush/vault_synthesizer/knowledge_lint], new [vault_indexer] block, new task_map entries
- [routing.task_map]: <record the actual A.7 swap decision here, e.g., "inbox_triage now uses gemma4:27b (+18% speedup)">
- hybrid_router.py: adds route_to_macbook() with WOL + PushNotification fallback
```

### `CLAUDE.md`
- Line ~9 (intro paragraph): update counts from **111 skills, 13 agents, 7 hooks** → **111 skills, 16 agents, 8 hooks**
- "Domain Workspaces" table: unchanged (agents live in `.claude/agents/`, not domains)
- "Agents SDK (Autonomous Layer) Active agents" table: add 3 rows (flush, vault_synthesizer, knowledge_lint) with schedule + cost
- "When Modifying" section: no structural change
- Model-to-Machine Routing table inside **16bitfit-battle-mode/CLAUDE.md** (lines 54–70): update per A.7 outcome
- Architecture comment block (~line 110): note new vault subdirectories

### `README.md`
- Top-level counts line: update 13 agents → 16, 7 hooks → 8
- Any table row referencing `.claude/agents/` count
- Mention knowledge compounding loop in feature list

### `export-groups/*/playground.json`
- No update needed — new items are **agents + hooks**, not skills. Export groups track skills only.

### Validation
- Run `python3 scripts/validate.py` — must return 0 errors post-merge.
- Run `cd agents-sdk && PYTHONPATH=. .venv/bin/pytest tests/ -v` — all green (including the 6 new test files).

---

## Critical files to open first (in order)

When implementation begins, load these files in the first coding session:

1. `16bitfit-battle-mode/SOURCE-OF-TRUTH.md` lines 413–577 (spec, re-read)
2. `agents-sdk/agents/vault_indexer.py` (the v1 you'll extend)
3. `agents-sdk/agents/daily_driver.py` lines 1–120 (preamble-building pattern)
4. `agents-sdk/lib/hybrid_router.py` (extending with route_to_macbook)
5. `agents-sdk/lib/config.py` (AgentConfig shape for new sections)
6. `.claude/hooks/run-tests-on-stop.sh` (hook pattern to copy)
7. `agents-sdk/tests/conftest.py` (fixture patterns)
8. `agents-sdk/config.toml` (the section you'll extend)

---

## Verification (this plan is ready when…)

- [x] All SOT tasks A.1–A.7 and D.1–D.4 covered with a specific file or action
- [x] Every new agent is 100% local ($0.00 API)
- [x] Zero new MCP dependencies for launchd agents (April 9 audit respected)
- [x] Hooks use `disallowedTools` deny-list, exit code 2 for deny
- [x] `SOURCE-OF-TRUTH.md` not modified
- [x] All 6 gate-check criteria have concrete verification commands
- [x] Doc updates (CHANGELOG.md, CLAUDE.md, README.md) scoped
- [x] 5 clarifying questions resolved with Sean (captured in §7)

When Sean approves via ExitPlanMode, coding starts with Week 13, Monday morning: A.1/A.2 (model pulls) + D.1.a (hook skeleton) in parallel.
