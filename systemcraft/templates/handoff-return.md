# Handoff return template

The inbound half of [the Systemcraft handoff contract](../../productcraft/templates/handoff-contract.md) — what Systemcraft sends back to the studio that handed it a brief. Owned by the **Design Strategist** (the seat that took the brief in), written at Close after **Gate 2 (design-complete)** passes; Gate 3 stays Systemcraft's to fire once the receiving studio's execution breakdown produces an implementation candidate. A typed packet: Systemcraft's five artifacts travel *beside* it as frozen, hashed copies in `handoff/outbound/artifacts/`, never inside it. The receiving seat (Productcraft's Delivery & Execution Lead) issues the state on arrival.

Filled returns are **private** (`ledger/engagements/<eng-id>/handoff/outbound/return.md`); this template is public machinery. Brevity law applies. The note carries answers and ids, never the reasoning behind them — that lives in Systemcraft's ledger, referenced by id.

```markdown
---
id: eng-005.return
engagement: eng-005-<slug>
date: 2026-10-03
seat: design-strategist
originates_from: pc-eng-001.handoff   # the brief this answers
answers_brief: pc-eng-001.handoff
gate2: PASS WITH ACCEPTANCES 2026-10-02   # the design-complete verdict, verbatim from its ledger entry
gate3: NOT FIRED — IMPLEMENTATION ABSENT  # stays so until candidate-note.md arrives
state: returned                       # returned | returned-partial
---

## Answers

One row per ask question, by the brief's id. The answer is one sentence; the entry holds the why.

| Ask id | Answer | Systemcraft entry |
|---|---|---|
| Q1 | | eng-005.d04 |

## Returned artifacts

The five frozen copies in `artifacts/`, by id. The manifest holds the hashes.

| Id | Artifact | What the receiving studio should take from it |
|---|---|---|
| eng-005.prd | PRD | |
| eng-005.adr | ADR | |
| eng-005.trust | Failure-UX spec + model card | |
| eng-005.eval | Eval plan | |
| eng-005.ops | Ops/economics model + incident runbook | |

## Overturned assumptions

Every Systemcraft decision that supersedes a product assumption. Systemcraft has already written `supersedes_external` on its entry; the receiving seat flips its own entry on reading this.

| Systemcraft entry | Supersedes (receiving studio's entry) | What changed, one line |
|---|---|---|

## Implementation holds

The Gate 2 holds the build must close before Gate 3 can pass: owner · trigger · required record · fail-closed consequence, one line each. "None" is a legal row.

## Deferred

Only on `returned-partial`: the lane deferred, why, and its rule-8 ticket.
```

## Filing

1. Freeze the five copies into `handoff/outbound/artifacts/<id>--<slug>.md` with `frozen_from`, `sha256`, `frozen_at`; one line each in `manifest.md`.
2. Copy `return.md`, `manifest.md` and `artifacts/` into the receiving studio's engagement `handoff/inbound/`; append `returned · <date> · design-strategist · <one line>` to `crossing.md` on both sides.
3. Close per the master skill; Gate 3 is recorded as not fired, waiting on the receiving studio's `candidate-note.md`.
