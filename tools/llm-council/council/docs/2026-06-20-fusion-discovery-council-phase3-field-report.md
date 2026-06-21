---
title: fusion-discovery-council — Phase 3 (Live Reliability) Field Report
date: 2026-06-20
status: complete
branch: feat/fusion-discovery-council
plan: ../../../../docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase3.md
phase2_report: 2026-06-20-fusion-discovery-council-phase2-field-report.md
baseline_commit: 86388c3
head_commit: 23ecc57
test_status: 93 passed, 1 skipped
validate: PASSED
live_e2e: confirmed ($0.3617, exit 0)
---

# fusion-discovery-council — Phase 3 Field Report (detailed)

**One-line:** All six Phase-3 tasks landed green via subagent-driven TDD (implement → spec review → code-quality review per task), and the **live e2e payoff confirmed end-to-end**: the exact `obsidian plugins` / `quick` run that crashed twice at FUSE in Phase 2 now survives OpenRouter's SSE keep-alive padding and writes a real $0.36 idea ledger with spend correctly recorded. The two Phase-3 live blockers (Fusion-response robustness + unrecorded failure spend) plus the bundled diagnosability/budget nits are closed. Suite **93 passed, 1 skipped**; `scripts/validate.py` **PASSED**. §7 below is the carry-forward backlog for the next phase.

---

## 1. Executive summary

Phase 2 hardened the slice in code (76 tests) but a live e2e then surfaced two real blockers for *live* discovery: `fuse()`'s unguarded `resp.json()` choking on OpenRouter's `: OPENROUTER PROCESSING` SSE keep-alive padding, and the fact that a failed Fusion call bills OpenRouter but recorded $0 locally with no session artifact. Phase 3 was surgical hardening of the FUSE/failure path — **no new stages, sources, or lenses**.

- **7 commits** off plan baseline `86388c3` (6 task commits + this report). Touches `fusion.py`, `pipeline.py`, `__main__.py`, `gather/last30.py`, three doc files, and test files.
- **Test suite: 76 → 93 passed, 1 skipped** (+17 net-new tests). The single skip is the pre-existing `INTEGRATION=1`-gated live test (`test_e2e.py`), unrelated to this work.
- **`scripts/validate.py`: PASSED** (exit 0; 62 pre-existing secret-pattern warnings, none in any Phase-3-changed file).
- **Every task passed both review stages.** Spec-compliance review found zero missing/extra/wrong items on all six. Code-quality review returned approve / approve-with-nits (8/10) on every task; each task's safe, additive nits were applied and re-verified before the next task started.
- **Method:** `superpowers:subagent-driven-development`. Fresh implementer subagent per task; two independent reviewers per task (a spec-compliance reader + the `Code Reviewer` agent), each verifying against the real code rather than the implementer's report. Tasks ran **strictly sequentially** (file overlap: `fusion.py` in Tasks 1+2; `pipeline.py`/`__main__.py` in Task 3).

## 2. What shipped, by commit

| Commit | Task | What |
|---|---|---|
| `3114feb` | 1 | SSE-padding-safe Fusion decode — new `_strip_sse_padding`, `_first_json_object` (string-aware balanced-brace scanner), `_decode_payload` (3-tier: `json.loads` → strip-then-parse → first-object → raise `FusionError`) replacing the unguarded `resp.json()`; `_parse` falls back to `_first_json_object` for prose-wrapped JSON. + review nits: `resp: httpx.Response` annotation, docstring accuracy, direct decode-failure unit test. |
| `7b9b6dc` | 2 | `FusionError(message, *, cost=0.0)` carries incurred cost; `fuse` accumulates `usage.cost` across attempts **before** the parse gate; success overrides `res.cost` with the summed total; both raises carry `cost=`. + review nits: unconditional override for site-consistency, "4xx-on-retry carries prior attempt's cost" test. |
| `169dc05` | 3 | `DiscoveryFailed(cost_usd, session)`; `run_discovery` persists a failure session JSON (`gather_status`/`failed_stage="fuse"`/`error`/`cost_usd`) and raises it; CLI records the billed spend (`tool="discovery"`), echoes status, exits 3. + review fix: failure-path session write wrapped in try/except so a write error can't eat the spend record (regression-tested); $0 cost-line honesty fix. |
| `1cd2fbc` | 4 | last30 `_subprocess_runner` `proc.kill()` + reap on timeout; stderr breadcrumbs on empty-stdout (exit code + stderr tail) and non-JSON output; still degrades to `[]`. + review nit: two real-runner tests (kill/reap + breadcrumb), mutation-verified load-bearing. |
| `f8e4564` | 5 | Test-only: monthly cross-depletion isolation guard (a $30 discovery spend must not deplete council's monthly headroom). Closes the Phase-2 review nit that only the daily path was guarded. |
| `23ecc57` | 6 | Docs reconciliation — SKILL.md §8 failure modes, CHANGELOG Phase-3 entry, Phase-2 field-report RESOLVED notes. |
| `6af0d0a` | 6 | This field report. |

**Backlog coverage from the Phase-2 field report's "promote to Phase-3" list:** Fusion SSE-padding robustness ✅ (Task 1) · failed-Fusion spend recording ✅ (Tasks 2+3) · `gather_status` persisted on failure ✅ (Task 3) · last30 kill-on-timeout + breadcrumbs ✅ (Task 4) · monthly cross-deplete guard ✅ (Task 5) · echo gather_status to console ✅ (Task 3 CLI) · docs reconciliation + live re-test ✅ (Task 6).

## 3. How the execution went

Smooth and disciplined. The plan was unusually complete — every task carried verbatim, current-file-grounded code and tests — so implementers reconciled-and-verified against the live files rather than designing. TDD discipline held on all six (each test confirmed red before the implementation made it green; Task 5, a guard for existing-correct behavior, was verified non-vacuous by simulating broken isolation and confirming the `council == 0.0` assertion is load-bearing). The two-stage review is where the value showed up — it surfaced and let us correctly act on three findings that genuinely strengthened the cost-integrity guarantees:

1. **Durable-spend fix (Task 3, Important).** The reviewer caught that a failure-path session-write error (read-only dir, disk full, sessions_dir-is-a-file) would propagate *before* `raise DiscoveryFailed`, landing in the generic `except` and never recording the billed spend — re-opening the exact bug Phase 3 closes. Fixed: the mkdir+write is wrapped so the cost record always survives a diagnostic-write failure. Regression-tested with `sessions_dir` pointed at a file (red → green, mutation-confirmed).
2. **Kill/reap test coverage (Task 4, Important).** The plan's tests routed around the real `_subprocess_runner` via the injected `runner=` seam, leaving the timeout→kill→reap path (the whole point of the task) untested. Added two real-runner tests; a mutation test (removing `await proc.wait()`) confirmed the reap assertion is load-bearing, not vacuous.
3. **Cost-line honesty (Task 3, Minor).** The "Recorded spend: $0.00 (billed even though FUSE failed)" line printed even when nothing was billed; now it prints only when cost > 0, else "No spend recorded (FUSE failed before billing)."

One simplification: Task 2's `if total_cost:` guard on the success override was dropped for an unconditional `res.cost = round(total_cost, 6)` — provably equivalent on every current path (the total already includes this attempt's `usage.cost`), and it makes all three recording sites consistent. All applied nits were additive/equivalent and re-verified green before moving on. No scope drift; **`verify.py` (the fabrication gate) was never touched.**

## 4. Live e2e — the payoff (2026-06-20, Sean-approved spend)

Command (plan Task-6 Step-5):
```bash
uv run python -m council.discovery "obsidian plugins" --lens pm --tier quick --output /tmp/p3-ledger.md
```
Console output — **exit 0**, the run survived FUSE end-to-end:
```
[last30] empty stdout (exit 1); stderr tail: AttributeError: 'NoneType' object has no attribute 'split'
Idea ledger written: /tmp/p3-ledger.md
Verified ideas: 2 · dropped: 3 · $0.36
```

**What it confirmed:**
- ✅ **SSE-padding decode works against the live API** — the unguarded `resp.json()` crash mode (Phase-2 §5/§6) is closed in practice, not just in mocks. The previously-inferred wire-format hypothesis is now effectively confirmed by a surviving run (byte-level capture no longer needed).
- ✅ **Real ledger** (`/tmp/p3-ledger.md`): 2 ranked, evidence-linked opportunities — (1) *Performance Bloat and Core Feature Gaps* (score 12.0; evidence: HN `item?id=48109970`, xda-developers), (2) *Security Risks and Lack of Sandboxing* (score 10.0; evidence: HN `item?id=48218092`) — 3 pain points dropped by the verification gate, plus blind-spot + contradiction maps. Every pain point traces to a real fetched URL; anti-fabrication gate held.
- ✅ **Per-collector `gather_status`** (session JSON `/tmp/.discovery-sessions/20260620-201446-6e095e.json`, `failed_stage: none`): `sonar: ok 15 records · web: ok 6 records · last30: ok 0 records`. Two live sources; last30 degraded safely. `evidence_count: 21`, `cost_usd: 0.3617`.
- ✅ **Spend recorded**: `{amount: 0.3617, profile: quick, tag: discovery-pm, tool: discovery}` row in `vault/health/council-spend-2026-06-20.json`.
- ✅ **Task-4 breadcrumb fired live** for the upstream `INCLUDE_SOURCES=null` crash — exactly the diagnosability the task added.

No new failure signature surfaced. The Phase-2 "live discovery intermittently fails today" blocker is resolved and live-confirmed.

## 5. Verification evidence

| Gate | Command (from `tools/llm-council/`) | Result |
|---|---|---|
| Unit/integration suite | `uv run --extra dev python -m pytest -q` | **93 passed, 1 skipped** |
| Repo validator | `python3 scripts/validate.py` (repo root) | **PASSED**, exit 0 (62 pre-existing warnings, none in changed files) |
| Live e2e | `uv run python -m council.discovery "obsidian plugins" --lens pm --tier quick …` | **exit 0**, $0.3617 ledger |

> Test-command gotcha (carry to every future phase): it is `uv run --extra dev python -m pytest` — plain `uv run pytest` does **not** work because pytest lives in the `dev` extra.

## 6. State of the branch

All work is on `feat/fusion-discovery-council`. **Not merged, no PR opened, fabrication gate untouched.** The 6 task commits + this report sit on top of plan baseline `86388c3`. The vault is intentionally not staged by this work (CLAUDE.md rule 8 — Obsidian-Git owns vault commits); the new ticket in §7 and the spend-ledger row were written to disk for Obsidian-Git to commit, not `git add`-ed here.

---

## 7. Carry-forward into the next phase (the actionable backlog)

Everything below is **out of Phase-3 scope and intentionally deferred** — nothing here is a Phase-3 regression. Grouped by what should fold into Phase 4 vs Phase 5 vs "external / ticketed."

### 7a. Open tickets (in `vault/00_inbox/tickets.md`)

| Ticket | Status | Action for next phase |
|---|---|---|
| **discovery Fusion response robustness (Phase-3, HIGH)** | ✅ **RESOLVED + live-confirmed** by this phase | Ready to move Todo → Done. Left in place to respect the hand-curated board. |
| **discovery last30 live-blocked by upstream `INCLUDE_SOURCES=null` crash** | 🔴 **STILL OPEN (external/config)** | last30 yields **0 live evidence** until fixed (re-confirmed in the live run — the breadcrumb fired). Fix is config, not code: set a non-null `INCLUDE_SOURCES` (e.g. `reddit,hackernews`) in `~/.config/last30days/.env`, or patch/report the upstream plugin. Doing this turns GATHER from 2 live sources (Sonar + Brave web) into 3. **Recommend resolving before Phase 4's extended collectors** so last30 is contributing when the collector fan-out is widened. |
| **discovery GATHER-stage spend invariant (Phase-3 review follow-up, LOW)** | 🟡 **NEW — filed this session** | The `except DiscoveryFailed` cost path covers FUSE only; the generic `except` assumes "no spend pre-fuse." True today (FUSE/OpenRouter is the only billable stage), but if a Sonar/web call is ever instrumented to bill, a gather-stage failure would silently record $0 — re-opening the cost-integrity bug one stage upstream. **Fold into Phase 4 only if Phase 4's new collectors introduce paid calls:** thread gather-stage incurred cost into a typed failure the same way `FusionError.cost → DiscoveryFailed.cost_usd` does. |

### 7b. Deferred code-quality nits (each has a safe failure mode today)

These were flagged by the two-stage reviews and consciously not acted on in Phase 3 (either plan-specified behavior or genuinely low-value-now). Pick up opportunistically:

- **`_first_json_object` stops at the first balanced `{…}` span even if it fails to parse** (`fusion.py`, Task 1 review, Important-deferred). For the documented "prose-wrapped single object" case this is fine, and the live run confirms the common path works. But as the *last-resort* decoder it would silently fail on a malformed leading object followed by a good one. A `continue`-to-next-`{` scan-forward strategy is strictly more robust at negligible cost. **Best folded into Phase 4** alongside any further Fusion-response hardening. *Note: Task 1's other Important item — "wire format inferred, not byte-captured" — is now effectively closed by the surviving live run.*
- **last30 timeout is a hardcoded `300`** (`gather/last30.py`, Task 4 review, Minor). Untestable without monkeypatching and not configurable per-tier. Hoist to a module constant (`_LAST30_TIMEOUT_S`) or a `collect_last30` param. Cheap; do it when Phase 4 touches the collectors.
- **Failure-session JSON is written with plain `write_text`, not the atomic tmp+rename the spend file uses** (`pipeline.py`, Task 3 review, Minor). Low stakes for a diagnostic artifact (a crash mid-write truncates a debug file, not money), but inconsistent with the cost-file discipline. Consider matching it if/when a session-reader is added.
- **Success vs failure session JSON have a non-uniform schema** (`pipeline.py`, Task 3 review, Minor). Failure sessions omit post-fuse fields (`verified`/`dropped`/`blind_spots`/`contradictions`). Fine today (no reader consumes both), but **if Phase 4/5 adds a session-reader, document the union schema** (or write `verified: null`/`dropped: null` on failure) so the reader treats post-fuse fields as optional and `failed_stage`/`error` as present-only-on-failure.
- **Unused `attempt` loop variable** in `fuse` (`fusion.py`, Task 2 review, trivial). `for attempt in range(2)` → `for _ in range(2)`. Pre-existing; cosmetic.

### 7c. Phase 4 scope (per the plan's phasing reminder)

- **Extended tier-gated collectors:** review sites + competitor-weakness mining, GitHub Issues / Canny / public roadmaps, demand/intent signals, Q&A sites, trend velocity. (This is the big one — widens GATHER beyond Sonar + Brave web + last30.)
- **`_simple_fetch` SSRF / redirect allow-list** (`web.py`). Consciously deferred in Phase 2/3 as low-risk on a personal machine where fetch targets come from Brave, not an attacker — but it is the right security hardening before any collector fans out to a wider, less-trusted URL surface. **Do this in the same phase that adds the new collectors**, since those expand the fetch surface.
- **Quote-verbatim hardening** — WebFetch the Sonar citations to confirm quotes verbatim rather than trusting the model's paraphrase.

### 7d. Phase 5 scope

- **The `substack` lens** (`frame_substack` + handoff into the `substack-value-engine` skill).
- **The `--segment` creative-signal qualifier.**

### 7e. Phase-1 Minor punch-list still open (items 5–8)

Carried since Phase 1, still unaddressed (all low-value, safe today): frame quote-bank positional pairing; Sonar verbatim WebFetch (overlaps 7c quote-hardening); URL escaping in the ledger render; `web_calls` factored into the cost *estimate* (the live `usage.cost` path made this less urgent, but the pre-flight estimate still ignores web-tool calls).

### 7f. Observations from the live run worth keeping

- **GATHER currently draws on 2 live sources** (Sonar 15 records, Brave web 6 records in this run). last30 is the third, gated on the §7a upstream config fix. The pipeline is healthy with 2; fixing last30 is additive, not blocking.
- **The fabrication gate is doing real work** — 3 of 5 candidate pain points were dropped by verification in this run. That ratio is a useful signal to watch as collectors widen in Phase 4 (more raw evidence should mean more drops, not fewer).
- **Cost landed at $0.3617 for `quick`**, well under the $0.50 quick cap. Phase 4's extra collectors + any new paid calls will push per-run cost up — re-check the tier caps when the collector fan-out lands.
