---
type: handoff
project: prj-job-hunt-2026
parent_task: task-12-judge-layer
created: 2026-05-28
session: cowork-2026-05-28-day-5
ai-context: "Cowork handoff doc — Task 12 Day 5 (JSONL ledger writer + boot-time readiness check + judge_action Option-B wrapper) shipped 2026-05-28. Sean opens this next, runs the full-suite verification on the Mac host, then commits."
---

# Task 12 (Judge Layer) — Day 5 Handoff

**TL;DR.** Day 5 turns a JudgeDecision from an in-memory return value into an
observable telemetry stream. Three deliverables landed: `lib/judge/ledger.py`
(atomic-FileLock JSONL writer + `ensure_ledger_ready()` boot check),
`lib/judge/action.py` (the `judge_action()` Option-B wrapper — `evaluate()`
stays pure, the wrapper does the I/O + fires Pushover on `JUDGE_UNAVAILABLE`),
and `tests/test_judge_ledger.py` (19 tests across 7 classes). **Sean picked
Option B** (pure wrapper) over Option A (I/O inside `evaluate()`) — so the 24
Day-3 `test_judge_evaluate.py` tests stayed green untouched. Judge suite now
**106 passed** in the sandbox (87 prior + 19 new); `validate.py` PASSED / 0
errors; smoke import green. **The full 802-suite regression check is the one
gate that must run on your Mac host** (the sandbox venv is macOS-native and
won't execute on Linux). Live `pytest` (full suite) + `git commit` are your
next moves.

---

## Decision locked this session

**Integration shape: Option B — pure wrapper.** `evaluate(proposal, policy)`
is unchanged and still never does I/O. A new `judge_action(proposal, policy, *,
agent_name, ledger_dir=None) -> JudgeDecision` is the effects layer: it calls
`evaluate()`, writes the ledger row, and fires the Pushover alert on
`JUDGE_UNAVAILABLE`. This matches the agents-sdk convention (pure logic + a
wrapper for effects) and kept all 24 Day-3 `evaluate` tests green with zero
edits. Day 6's substack-drafter wire-up calls `judge_action()`, not `evaluate()`.

**One trade-off Option B forces, surfaced + accepted:** `evaluate()` swallows
the raw model/transport error text to the logger and returns only a
`JudgeDecision` (which is frozen — no error field). So the wrapper can't put
the raw failure tail into the Pushover alert. The alert instead carries the
actionable identifiers it does have — `agent_name`, attempted `model_used`,
`latency_ms` — and points the operator at the agent logs for the detail. If you
ever want the raw error tail in the alert itself, that's the argument for
Option A; it would require touching `evaluate()` + re-mocking the Day-3 tests.

---

## What shipped (file map)

```
agents-sdk/
├── lib/judge/
│   ├── ledger.py        (258 lines — NEW. write_decision() atomic-FileLock
│   │                     JSONL append + UTC-midnight date bucketing +
│   │                     matched_rule_id derivation; ensure_ledger_ready()
│   │                     boot check; LedgerError / LedgerWriteError)
│   ├── action.py        (112 lines — NEW. judge_action() Option-B wrapper:
│   │                     evaluate() + ledger write + best-effort severity-0
│   │                     Pushover on JUDGE_UNAVAILABLE; never raises)
│   └── __init__.py      (61 lines — MODIFY, +15. Exports judge_action,
│                         write_decision, ensure_ledger_ready, LedgerError,
│                         LedgerWriteError alongside the schema surface)
└── tests/
    └── test_judge_ledger.py  (436 lines — NEW. 19 tests / 7 classes)
```

No other files touched. `evaluate()` / `schema.py` / `policy.py` /
`substack_drafter.yaml` / `config.toml` all unchanged (design invariants 1-6
preserved — schema frozen, 5-outcome enum frozen, 4-rule policy untouched,
`judge_layer` routing untouched).

### The JSONL row schema (`vault/health/judge_log/<YYYY-MM-DD>.jsonl`)

```json
{
  "evaluated_at":      "2026-05-28T12:00:00+00:00",
  "agent_name":        "substack_drafter",
  "outcome":           "ALLOW | BLOCK | REVISE | ESCALATE | JUDGE_UNAVAILABLE",
  "matched_rule_id":   "rule_d_publish_verb_at_top_level | null",
  "model_used":        "gemma4:e4b",
  "latency_ms":        412,
  "feedback":          "text | null",
  "quarantine_reason": "text | null",
  "proposal":          { "...full ActionProposal model_dump..." }
}
```

`matched_rule_id` is **derived** from `proposal.authorization_basis` (fragment
after `#`, else first `rule_…` token, else `null`) — the judge never echoes a
rule id, and the proposal's authorization_basis is the one place a rule is
referenced. It is a reference to an existing rule, never a 5th rule.

### Test-class breakdown (`test_judge_ledger.py`, 19 tests / 7 classes)

| Class | Covers |
|---|---|
| `TestWriteDecision` | one valid JSON line, all 9 required keys, proposal round-trips via `model_validate`, returns absolute path |
| `TestWriteDecisionAppend` | two writes → 2 lines, in order, same UTC-date bucket |
| `TestWriteDecisionBucketsByUtcMidnight` | same PST calendar date but cross-UTC-midnight → 05-28 vs 05-29 files; naive datetime treated as UTC |
| `TestWriteDecisionAtomicity` | monkeypatched `FileLock` → `LockTimeout` → `LedgerWriteError`; subclass invariant |
| `TestEnsureLedgerReady` | creates missing dir; read-only parent → `LedgerWriteError` (skipped under root); absent creds → `PushoverConfigurationError` via env-override pattern |
| `TestMatchedRuleIdDerivation` | `#`-fragment, bare token, no-reference→None, empty→None |
| `TestJudgeActionIntegration` | ALLOW → row + no push; JUDGE_UNAVAILABLE → row + 1 push (severity 0, correct title/message); push-send failure logged not raised; ledger-write failure logged not raised |

---

## Verification commands (run in this order on the Mac host)

```bash
cd ~/Code-Brain/code-brain/agents-sdk
source .venv/bin/activate

# 1. New ledger tests + all judge tests
PYTHONPATH=. pytest tests/test_judge_ledger.py -v
PYTHONPATH=. pytest tests/test_judge_*.py -v
# Expected: all green. Sandbox counted 106 for the judge group
# (79 Day-1-3 baseline + ... your Mac's collection count + 19 new).

# 2. FULL SUITE — the gate the sandbox could not run
PYTHONPATH=. pytest tests/ -v
# Expected: prior 802-passed / 2-pre-existing-fleet-memory-reds baseline
# holds, + 19 new ledger tests. Zero judge-induced regressions.

# 3. Smoke import of the new public surface
PYTHONPATH=. python3 -c "
from lib.judge.ledger import write_decision, ensure_ledger_ready, LedgerError, LedgerWriteError
from lib.judge import judge_action
print('Day 5 imports green')
"

# 4. Repo validator (from repo root)
cd ~/Code-Brain/code-brain && python3 scripts/validate.py
# Expected: Validation PASSED, warnings <= 62, 0 errors.
```

### What ran in the Cowork sandbox this session (signal, not the host gate)

The Mac `.venv` is Apple-Silicon-native and can't execute under the Linux
workspace, so the sandbox stood up its own Python 3.10 with pydantic/pyyaml/
httpx/pytest and ran against the mounted source tree:

  - `pytest tests/test_judge_ledger.py` → **19 passed**.
  - `pytest tests/test_judge_*.py` → **106 passed** (87 prior + 19 new).
  - `python3 scripts/validate.py` → **Validation PASSED (60 warning(s))**, 0 errors.
  - smoke import → **Day 5 imports green**.

The full `pytest tests/` was NOT run in the sandbox (45s wall-clock cap; many
unrelated agent tests need deps/network the sandbox doesn't have). Run it on the
Mac — it's gate #2 above.

---

## Commit message (copy verbatim)

```
feat(judge): ship Task 12 Day 5 — JSONL ledger writer + boot check + judge_action wrapper (Council Gap-Fill 1)

Day 5 makes judge decisions observable. Adds the JSONL ledger writer, the
boot-time readiness check, and the Option-B effects wrapper that records every
decision and alerts on JUDGE_UNAVAILABLE — without touching the pure evaluate().

OPTION B (locked by Sean this session): evaluate() stays pure and unchanged;
the new judge_action() wrapper does the I/O. All 24 Day-3 evaluate tests stay
green untouched.

WHAT SHIPPED

  lib/judge/ledger.py    write_decision(decision, proposal, *, agent_name,
                         ledger_dir=None) -> Path. Atomic append under
                         lib.filelock.FileLock(exclusive, timeout=5s) →
                         LedgerWriteError on LockTimeout / OSError. Date bucket
                         rolls at UTC midnight off JudgeDecision.evaluated_at,
                         not local time. Row carries the 9-key schema incl.
                         matched_rule_id derived from authorization_basis and
                         the full ActionProposal model_dump. ensure_ledger_ready()
                         mkdir+writable-probe+pushover.ensure_credentials_or_raise()
                         — fail loud at boot. LedgerError / LedgerWriteError
                         mirror pushover.py's exception shape.
  lib/judge/action.py    judge_action(proposal, policy, *, agent_name,
                         ledger_dir=None) -> JudgeDecision. Calls evaluate(),
                         writes the ledger (LedgerError caught + logged),
                         fires a best-effort severity-0 Pushover ping on
                         JUDGE_UNAVAILABLE (PushoverError caught + logged).
                         Never raises — takes over the never-raises contract
                         for the I/O it adds. Default ledger dir resolves to
                         <vault_root>/health/judge_log/.
  lib/judge/__init__.py  +15 lines — exports judge_action, write_decision,
                         ensure_ledger_ready, LedgerError, LedgerWriteError.
  tests/test_judge_ledger.py  19 tests / 7 classes — write/append/UTC-bucket/
                         atomicity/boot-check/rule-id-derivation/judge_action
                         integration. All tmp_path; never touches real
                         vault/health/.

NUMBERS

  - 370 lines of new module code (258 ledger + 112 action) + 15 in __init__
  - 436 lines / 19 tests across 7 test classes
  - judge group: 106 passed in the sandbox (zero regressions in the judge surface)

DESIGN INVARIANTS PRESERVED

  - JudgeDecision schema FROZEN (no field added for the ledger's convenience)
  - 5-value Outcome enum FROZEN (JUDGE_UNAVAILABLE still load-bearing)
  - evaluate() never-raises contract preserved (Option B: untouched)
  - substack_drafter.yaml stays at exactly 4 rules; matched_rule_id is a
    reference to an existing rule, not a 5th
  - judge_layer routing (gemma4:e4b / mac_mini) unchanged

Closes Task 12 Step 4 (Day 5) of unified-roadmap §Task 12.
See: vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/
     job-hunt-2026-roadmap/2026-05-28-task-12-day-5-handoff.md
```

**DO NOT let the commit auto-fire.** Per the Day-1-3 surprise, Obsidian-Git
auto-committed judge-module work outside `vault/` as `5406a17`. This session
verified the **two auto-commits after the judge tag (`cd93048`, `0a229ce`)
touched only `vault/` paths** — strong evidence the plugin's "Files to ignore"
scope was narrowed between 15:08 and 15:53 on 5/28. The new Day-5 files under
`agents-sdk/` should therefore stay out of Obsidian-Git's reach. Confirm before
you commit: `git status` should show the four Day-5 files as untracked/modified
and NOT already swept into a `vault: auto-commit`. If you find them
auto-committed, the scope narrowing didn't stick — fix it before tagging.

Branch note (unchanged from Days 1-3): work is on
`feature/fleet-memory-phase-1`. If you want a clean `feature/judge-layer-v0` PR
boundary, cherry-pick the judge commits onto a fresh branch from `main`.

---

## Pending items (Days 6-9 + B7 gate watch)

  - **Day 6 — substack-drafter wire-up.** Call `judge_action()` between
    `_route()` and `write_draft()` in `agents/substack_drafter.py`; build the
    ActionProposal from the draft + voice-mode metadata + concept cluster;
    dispatch ALLOW/REVISE/BLOCK/ESCALATE. Gated by `[substack_drafter]
    judge_enabled = false` AND `[judge_layer] enabled = false` — both must flip.
    **Hard precondition: B7 synthesizer gate must close first** (5 consecutive
    nights of `concepts_written > 0`). As of 2026-05-28: **4 of 5 green; 5/25
    broke the chain.** Next clean window opens 5/29; target B7 closure ~6/2.
    **Do not start Day 6 in a session before B7 closes**, even if there's time.
  - **Day 7** — `--demo-injection` CLI flag for the Loom take.
  - **Day 8** — 4Q `EXPLANATION.md` at `lib/judge/EXPLANATION.md`.
  - **Day 9** — 90-sec Loom + LinkedIn FDE-Boston-tagged post + final
    verification gate + tag `judge-layer-v0.1.0`. Ship target **2026-06-04**.

  - **`vault/health/judge_log/.gitkeep`** (in the roadmap's full file list) was
    intentionally NOT created — Day 5 scope was the three deliverables + tests,
    and `ensure_ledger_ready()` mkdir's the dir at runtime so the `.gitkeep` is
    not functionally required. Add it at the Day 9 close-out if you want the
    empty dir tracked in the repo.

---

## What interview answer this artifact unlocks

Day 5 is the **observability** beat of the control-architecture story. Days 1-3
gave you the typed proposal and the five-outcome verdict — but the verdict was
an in-memory return value that vanished the moment the function returned. Day 5
makes it a **durable, append-only telemetry stream**: every decision lands one
JSON line at `vault/health/judge_log/<date>.jsonl`, bucketed by UTC date,
written concurrent-safe under an advisory lock, carrying the outcome, the
attempted model, the latency, and the full proposal. That single file is what
the Task 11 dashboard's "judge-outcome distribution" and "judge-availability %"
panels read directly. The FDE framing tightens from *"my agents emit typed
proposals to a judge"* to *"…and every verdict, including the judge's own
unavailability, is recorded as an observable event I can plot — the control
plane isn't just enforcing, it's auditable."* The `JUDGE_UNAVAILABLE` row is the
quietly load-bearing part: most governance demos hide judge downtime as an
exception; here it's a first-class line in the ledger and a severity-0 Pushover
ping, so availability is a number on a dashboard instead of a vibe — while
Sean's manual publish gate stays the canonical Tier-A control underneath it.
