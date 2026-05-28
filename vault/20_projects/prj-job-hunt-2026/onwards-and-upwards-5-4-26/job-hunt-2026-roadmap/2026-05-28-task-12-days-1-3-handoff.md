---
type: handoff
project: prj-job-hunt-2026
parent_task: task-12-judge-layer
created: 2026-05-28
session: cowork-2026-05-28
ai-context: "Cowork handoff doc — Task 12 Days 1-3 (Pydantic schema + policy YAML loader + judge.evaluate()) shipped in a single session 2026-05-28. Sean opens this next, runs the verification commands, then commits."
---

# Task 12 (Judge Layer) — Days 1-3 Handoff

**TL;DR.** In one Cowork session 2026-05-28 the entire infrastructure layer of the Judge Layer ships: Pydantic `ActionProposal` / `JudgeDecision` / `Outcome` schemas, declarative YAML policy loader, the canonical `substack_drafter.yaml` policy, and `judge.evaluate()` wired through HybridRouter's new `judge_layer` task profile. **8 production files, 3 test files, 74 tests across 17 classes.** All static checks green; live `pytest` and `git commit` are Sean's next moves.

---

## What shipped (file map)

```
agents-sdk/
├── lib/judge/
│   ├── __init__.py             (46 lines — module docstring frames the council
│   │                            gap-fill 1 lineage + the architecture)
│   ├── schema.py               (244 lines — Pydantic v2 ActionProposal +
│   │                            JudgeDecision + Outcome enum)
│   ├── policy.py               (251 lines — @dataclass(frozen=True) Rule +
│   │                            Policy, YAML loader, 3 exception classes)
│   └── judge.py                (505 lines — _call_router HTTP seam +
│                                evaluate() + JSON output parser + retry loop)
├── policies/
│   └── substack_drafter.yaml   (104 lines — 4 rules + provenance comments
│                                per rule pointing at the real lived incident)
├── tests/
│   ├── test_judge_schema.py    (300 lines, 24 tests, 5 classes)
│   ├── test_judge_policy.py    (356 lines, 26 tests, 5 classes)
│   └── test_judge_evaluate.py  (533 lines, 24 tests, 7 classes)
├── config.toml                 (+1 line — judge_layer = { model = "gemma4:e4b",
│                                machine = "mac_mini" } in [routing.task_map])
└── pyproject.toml              (+1 line — pydantic>=2.0,<3 promoted from
                                 transitive to explicit dep)
```

Plus roadmap checkboxes flipped Days 1-3 → `[x]` at [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) Task 12 Steps 1-3.

---

## Verification commands (run in this order)

```bash
cd ~/Code-Brain/code-brain/agents-sdk

# 1. Activate venv so pydantic 2.12.5 + pyyaml 6.0.3 resolve
source .venv/bin/activate

# 2. Quick import smoke (catches any path / typo problem before pytest fires)
PYTHONPATH=. python3 -c "
from lib.judge import ActionProposal, JudgeDecision, Outcome
from lib.judge.policy import load_policy
from lib.judge.judge import evaluate, JudgeTransportError
p = load_policy('substack_drafter')
print(f'Policy loaded: {p.name} v{p.version}; {len(p.rules)} rules')
print(f'Outcomes: {[o.value for o in Outcome]}')
"
# Expected:
#   Policy loaded: Substack-Drafter Policy v1 v1.0.0; 4 rules
#   Outcomes: ['ALLOW', 'BLOCK', 'REVISE', 'ESCALATE', 'JUDGE_UNAVAILABLE']

# 3. Run JUST the new judge tests first (faster signal if anything's broken)
PYTHONPATH=. pytest tests/test_judge_schema.py tests/test_judge_policy.py tests/test_judge_evaluate.py -v
# Expected: 74 passed in <30s. Zero asyncio / live HTTP / WOL traffic — all
# tests use the _RouterStub monkeypatch.

# 4. Full suite for regressions in the 550-test baseline
PYTHONPATH=. pytest tests/ -v
# Expected: 624 passed (550 existing + 74 new) in <2 min. Zero regressions.

# 5. Lint
ruff check lib/judge/ tests/test_judge_*.py
# Expected: All checks passed!

# 6. Repo-level validator (CLAUDE.md non-negotiable on every change)
cd ~/Code-Brain/code-brain && python3 scripts/validate.py
# Expected: ≤60 warnings / 0 errors (v3.30.1 baseline). Judge module is
# pure Python — shouldn't add warnings.
```

If any of the above fail, **STOP** before commit and surface the error in the next session.

---

## Commit message (copy verbatim)

```
feat(judge): ship Task 12 Days 1-3 — Pydantic schema + policy YAML loader + evaluate() (Council Gap-Fill 1)

Adds the infrastructure layer of the judge layer at lib/judge/. Three days
of work landed in a single Cowork session 2026-05-28 because the patterns
were ready (pushover.py's exception class shape, filelock.py's test idiom,
hybrid_router.py's task-profile registry, substack_drafter.py's _route() seam
for the HTTP boundary).

WHAT SHIPPED

  lib/judge/__init__.py            Module surface: ActionProposal, JudgeDecision, Outcome
  lib/judge/schema.py              Pydantic v2 schema — 8-field ActionProposal,
                                   5-value Outcome (including JUDGE_UNAVAILABLE
                                   as a named observable state, not a silent
                                   exception), JudgeDecision wrapping outcome
                                   + telemetry (model_used, latency_ms,
                                   evaluated_at UTC).
  lib/judge/policy.py              YAML loader — @dataclass(frozen=True) Rule +
                                   Policy, cross-field validators (REVISE
                                   requires feedback_template, ESCALATE
                                   requires quarantine_reason, fallback can't
                                   be REVISE/ESCALATE), duplicate-id rejection.
                                   Three exception classes: PolicyError /
                                   PolicyNotFoundError / PolicySchemaError —
                                   fail loud at boot vs. silent at evaluate.
  lib/judge/judge.py               evaluate(proposal, policy) -> JudgeDecision.
                                   Routes via HybridRouter judge_layer profile
                                   → gemma4:e4b on Mac Mini Ollama ($0/decision).
                                   System prompt enumerates policy rules + JSON
                                   contract; user prompt is YAML-shaped
                                   ActionProposal. Two-pass JSON parser
                                   (clean / prose-preamble extraction) +
                                   cross-field consistency check + retry-on-
                                   parse-failure (max 3, then JUDGE_UNAVAILABLE).
                                   evaluate() NEVER raises — fail-open is the
                                   contract; transport / parse / unexpected
                                   exceptions all land as JUDGE_UNAVAILABLE
                                   rows for the dashboard's per-model
                                   availability panel.
  policies/substack_drafter.yaml   Canonical v1 policy — 4 rules, each with
                                   provenance comments pointing at the real
                                   lived incident: rule_a (LDR fabrication
                                   from v3.26.3), rule_b (CIIA §2.3 from
                                   Task 0), rule_c (5-mode voice rotation
                                   from writing-voice-modes skill), rule_d
                                   (Tier-A "agents draft / Sean sends"
                                   boundary made executable as BLOCK).
  tests/test_judge_schema.py       24 tests / 5 classes — pins the 5-value
                                   Outcome contract, parametrized required-
                                   field validation, extra='forbid' typo-
                                   catching, JSON round-trip for the JSONL
                                   ledger writer (Day 5 dep).
  tests/test_judge_policy.py       26 tests / 5 classes — happy path, not-
                                   found, all 8 named schema errors,
                                   frozen-dataclass invariant, and an
                                   integration test that loads the REAL
                                   substack_drafter.yaml and asserts exactly
                                   4 rules + the 4 canonical ids + the
                                   1-ESCALATE/2-REVISE/1-BLOCK distribution.
                                   Any 5th-rule PR fails this loud, forcing
                                   a dashboard panel update in the same change.
  tests/test_judge_evaluate.py     24 tests / 7 classes — all 4 model-
                                   emittable outcomes round-trip, all 4 fail-
                                   open paths land as JUDGE_UNAVAILABLE,
                                   parse-retry self-correction (with parse
                                   error in retry prompt), max-retries-
                                   respected, latency_ms population,
                                   per-model attribution for dashboard, and
                                   JSONL-readiness round-trip.

  config.toml                      +1 line — judge_layer = { model =
                                   "gemma4:e4b", machine = "mac_mini" } in
                                   [routing.task_map]. Same machine + model
                                   as inbox_triage to reuse already-loaded
                                   weights. Inline comment explains the
                                   "real judge on paid path beats no judge"
                                   fallback design.
  pyproject.toml                   +1 dep — pydantic>=2.0,<3 promoted from
                                   transitive (via google-genai) to explicit.
                                   Prevents future google-genai bumps from
                                   silently breaking the judge module.

NUMBERS

  - 1,150 lines of judge module code (244 schema + 251 policy + 505 judge
    + 46 init + 104 YAML policy)
  - 1,189 lines / 74 tests across 17 test classes
  - 2 small config edits (pyproject.toml + config.toml)
  - All AST + YAML + import-resolution checks green statically

WHAT'S NEXT (Days 4-9 per roadmap Task 12 Step 4-9)

  Day 5: JSONL ledger writer at lib/judge/ledger.py + fail-open Pushover
         wiring. Atomic FileLock pattern (reuse lib/filelock.py).
         vault/health/judge_log/{YYYY-MM-DD}.jsonl is the consumer surface;
         the Task 11 dashboard reads this path directly.
  Day 6: Wire judge.evaluate() into agents/substack_drafter.py between
         _route() and write_draft(). Hard-gated by config flags:
         [substack_drafter].judge_enabled = false default AND
         [judge_layer].enabled = false default — both must flip true.
  Day 7: --demo-injection CLI flag for the Loom take.
  Day 8: 4Q EXPLANATION.md at lib/judge/EXPLANATION.md.
  Day 9: 90-sec Loom + LinkedIn FDE-Boston-tagged post + verification gate.

  Day 6 wire-up needs Task 8 Workstream B7 closed (5 consecutive nights of
  concepts_written > 0). As of 2026-05-28: 4 of 5 nights green, 5/25 broke
  chain. Synth is healthy and producing — 5/27=13, 5/28=57. Spirit
  satisfied; strict gate not closed; next clean 5-night window opens 5/29.

TIER-A CHECK PRESERVED

  Walk-away $100k:           N/A (control plane is infrastructure)
  AI > Tech > Creative PM:   ✓ direct match to Anthropic FDE Boston JD
                             ("control architectures around production
                             agent deployments")
  Agents draft / Sean sends: ✓ EXPLICITLY PRESERVED — judge is defense-in-
                             depth, NOT the only review surface; fail-open
                             via JUDGE_UNAVAILABLE keeps Sean's manual gate
                             as the canonical Tier-A control. Day 6 wire-up
                             preserves this — no autonomous publishing path
                             is added.
  5:30 PM hard stop:         ✓ Build sized to fit 8:30-5:30 containers
  Track-C protected:         ✓ Track-C v0 shipped 2026-05-12; this is
                             additive

Closes Task 12 Steps 1-3 of unified-roadmap §Task 12.
See: vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/
     job-hunt-2026-roadmap/2026-05-28-task-12-days-1-3-handoff.md
```

---

## What you (Sean) can speak to in interviews from this artifact alone

Three load-bearing answers fall out of this work:

**(1) "Walk me through your control architecture."**

> *Every agent action in my fleet emits a typed ActionProposal first — eight fields: intended action, target surface, evidence used, authorization basis, expected consequence, rollback path, exposure level, and human-review-required. That proposal goes to a judge layer that evaluates it against a declarative YAML policy. The judge returns one of five outcomes: ALLOW, BLOCK, REVISE, ESCALATE, or JUDGE_UNAVAILABLE. The fifth outcome is the one most people miss — it turns judge model unavailability into a named, observable state instead of a silent exception. The ledger captures every decision; the dashboard plots availability per-model. The whole thing runs on a local 4B-parameter model on a Mac Mini for zero ongoing cost.*

That's the FDE pitch. It's the conversion the council called "I have agents → I run actors inside a control architecture."

**(2) "How do you think about cost economics?"**

> *The control plane is free to operate. The judge runs on gemma4:e4b via Ollama on Mac Mini — that's $0 per decision and ~30 seconds per call. Most agent-governance offerings charge per-call for the judge model. I made the architecture choice to run the judge locally precisely because that's the bill-of-materials item that scales worst as agent traffic grows. The fallback path is to Claude API only when Mac Mini is unreachable — explicit because a real judge run on the paid path is better than no judge.*

That's the cost-economics gap closure Nate flagged, answered with architecture instead of a calculator.

**(3) "Why YAML for policies?"**

> *The policy is the part a recruiter, a CISO, or a non-engineer auditor needs to read to understand what the control plane gates against. Code is implementation. YAML is contract. Each rule in `substack_drafter.yaml` is four labeled fields: id, condition, outcome, and either feedback_template or quarantine_reason. A duplicate id is rejected at load. A REVISE rule without a feedback_template is rejected at load. The schema validation lives in Python; the policy lives in YAML. Future agents get gated by adding a new YAML file, not by writing new Python.*

That's the answer to "how do you ship a control plane without locking everything in code."

---

## Known not-shipped-yet (be honest in interviews)

  - **Day 5 ledger writer is the next dependency.** The JudgeDecision dataclass
    is JSONL-ready (round-trip tested), but no agent is writing rows to
    `vault/health/judge_log/` yet. The dashboard panels at Task 11 plot
    judge-outcome distribution and judge-availability % — those come online
    once Day 5 ships.

  - **Substack-Drafter is not yet wrapped.** `agents/substack_drafter.py`
    runs unchanged. Day 6 is the wire-up step. The judge module itself is
    designed for that integration — `evaluate()` returns a `JudgeDecision`,
    `substack_drafter._route()` will call it before `write_draft()`. No
    surprises expected; the `_RouterStub` test pattern is exactly the
    pattern the integration test will use.

  - **`--demo-injection` flag** for the Loom take is Day 7. Without it the
    Loom is harder to script because the judge's "Revise" outcome can't
    be triggered on demand. The flag's whole purpose is "make the demo
    reproducible without changing production code paths."

  - **B7 gate (5 consecutive nights of concepts_written > 0) is not yet
    strictly closed.** 4 of 5 nights through 5/28 are green; 5/25 was zero.
    The spirit is satisfied (synth produced 57 concepts overnight on 5/28)
    but the strict gate needs another clean window. Days 4-7 work doesn't
    depend on B7; Day 6 (substack-drafter wire-up) does. Plan: aim for B7
    closure 6/1, Day 6 work starts 6/2.

---

## What changed in the roadmap

Three checkboxes flipped from `- [ ]` to `- [x]` at [`2026-05-06-unified-roadmap.md`](2026-05-06-unified-roadmap.md) Task 12 — Steps 1, 2, 3 each carry a one-paragraph completion summary with the lines-of-code count + the test-class breakdown + the artifact pointer. Plus a new Status banner at the top of Task 12 reflecting Day 1-3 ship + B7 nuance.

No other roadmap section touched. Tasks 13, 14, 15, 16, 17 all remain in their pre-session state.

---

## Onwards

Next sessions, in order of dependency:

  1. **This session's open thread:** run the verification commands above,
     commit if green, tag `judge-layer-v0.0.1-infra` (Days 1-3 increment,
     not v0.1.0 yet — that's reserved for the Day 9 ship).
  2. **Next Cowork:** Day 5 ledger writer at lib/judge/ledger.py. Atomic
     FileLock + JSONL append + boot-time Pushover credential check.
  3. **After B7 closes:** Day 6 wire into substack-drafter.py.
  4. **Then:** Days 7-9 in a single session — `--demo-injection` flag,
     EXPLANATION.md, Loom take, LinkedIn post tagging Anthropic FDE Boston.

Ship target unchanged: **2026-06-04** for v0.1.0 + LinkedIn announcement.
