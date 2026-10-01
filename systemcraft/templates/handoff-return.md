# Handoff return template

The return half of [the handoff contract](../../craftwork/handoff-contract.md) — what Systemcraft sends back to the studio that handed it a brief. It is the mirror of the sender's binding (for Productcraft, [handoff-binding-systemcraft.md](../../productcraft/templates/handoff-binding-systemcraft.md)), and it carries Systemcraft's own strip list for its five artifacts (below). Owned by the **Design Strategist** (the seat that took the brief in), written at Close after **Gate 2 (design-complete)** passes; Gate 3 stays Systemcraft's to fire once the receiving studio's execution breakdown produces an implementation candidate. A typed packet: Systemcraft's five artifacts travel *beside* it as frozen copies in `handoff/outbound/artifacts/`, stripped of their process parts and hashed, never inside it. The receiving seat (Productcraft's Delivery & Execution Lead) issues the state on arrival.

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

1. Freeze the five copies with the shared kit, using this file as the binding: `python3 craftwork/trace/freeze.py copy --binding systemcraft/templates/handoff-return.md --out <eng>/handoff/outbound/artifacts <artifact>=eng-NNN.<slug> …`. It writes `<id>--<slug>.md` stamped with `frozen_from`, `sha256` (the stripped copy), `source_sha256`, `frozen_at` and `stripped`, and prints the table that is `manifest.md`. Run `freeze.py show` first to see what each copy loses.
2. Copy `return.md`, `manifest.md` and `artifacts/` into the receiving studio's engagement `handoff/inbound/`; append `returned · <date> · design-strategist · <one line>` to `crossing.md` on both sides.
3. Close per the master skill; Gate 3 is recorded as not fired, waiting on the receiving studio's `candidate-note.md`.

## What is stripped from the copies

The process parts of Systemcraft's five artifacts, read from eng-004's set on 2026-10-01: the sections that route findings between seats or record audit, version and Sean-ruling history; the disposition sections a repair round adds; the `[Δ g2 — …]` repair tags on headings (the heading stays, the tag goes); the co-sign trail and contributor list in the frontmatter; and the toolbelt and end-of-pass lines. Implementation holds, ticket seeds and the model card stay: they are what Productcraft's Delivery seat builds from. Systemcraft's adoption of the shared law ([craftwork build 4](https://github.com/seanwinslow28/code-brain/issues/327)) may add lines here. The rule first applies to eng-005's return (due 2026-12-04).

```strip
heading: ## Routed to other seats
heading: ## Audit state
heading: ## Version history
heading: ## Sean rulings
heading: ## One decision for Sean
heading: ## Acceptances Sean must sign
heading: ## Grounding
heading: ## Moves
heading-ending: ## disposition
heading-ending: ## dispositions
heading-ending: ## dispositioned
heading-tag: [Δ
key: audit
key: cosign
key: evals_cosign
key: cosign_touch
key: criteria_contributors
paragraph: *Toolbelt note
paragraph: END-OF-PASS
paragraph: meter:
```
