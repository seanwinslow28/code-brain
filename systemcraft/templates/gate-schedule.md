# Gate schedule and attack checklists

Systemcraft's own half of the red-team gate: when its gates fire, what each one demands, and what it attacks per artifact. The protocol itself (posture, what a gate may demand, typed verdicts, IMPLEMENTATION HOLD, the never-silently-skips fallback) is shared law at [craftwork/templates/red-team-protocol.md](../../craftwork/templates/red-team-protocol.md). This file was split out of that protocol unchanged when it moved to `craftwork/` on 2026-10-01 ([craftwork build 1](https://github.com/seanwinslow28/code-brain/issues/324)), because a gate schedule is each team's own.

## When gates fire

*(Amended 2026-08-29 — eng-003.d20, ratified: three typed gates replace the two-gate design; a paper gate may no longer demand runtime evidence.)*

| Engagement type | Gates |
|---|---|
| Design a new project | **Gate 1 — PRD sign-off** (after the Evals co-sign, before architecture) · **Gate 2 — design-complete** (after the ops/economics model, before design is declared complete) · **Gate 3 — pre-launch** (only after an implementation candidate exists, before live emission) |
| Audit an existing system | **One audit-close gate** — the audit's own findings are red-teamed before delivery |
| One-off question | No gate |

Outcomes are typed **PRD** / **DESIGN** / **LAUNCH** / **AUDIT**.

Gate 2 is a design gate: it attacks only claims an unimplemented design can prove, and records runtime evidence as IMPLEMENTATION HOLDs (protocol § What a gate may demand).

Gate 3 does not fire without an identified implementation candidate. It demands build identity, actual path/schema, migrations, end-to-end positive and negative tests, rollback/kill drills, production or production-representative instrument records, actual measurements where required, and closure of every hard IMPLEMENTATION HOLD. If no implementation candidate exists, its state is **NOT FIRED — IMPLEMENTATION ABSENT**.

## Attack checklists (per artifact type)

- **PRD** — unfalsifiable success claims; hidden user/data assumptions; missing non-goals; metrics that reward hurting users (the "assumed resolution" class); scope-creep vectors.
- **ADR** — unpriced alternatives; vendor lock-in; scale cliffs; single points of failure; complexity that serves the résumé, not the product.
- **Failure-UX spec + model card** — uncovered failure modes; overtrust surfaces; missing disclosure; escalation dead-ends (no path to a human).
- **Eval plan** — judge-gameable metrics; train/test leakage; unrepresentative golden sets; the metric-vs-user gap; missing negative/abuse cases.
- **Ops model + runbook** — unit economics that only work at best case; kill-switch theater (a switch nobody can actually pull); drift blind spots; runbook steps requiring a human who won't be there at 3 AM.
- **Whole design (gate passes)** — cross-artifact contradictions; the steel-man alternative; "name the most likely way this is quietly failing six months after launch."
