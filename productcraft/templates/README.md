# Templates

Public machinery; filled artifacts are private (`ledger/engagements/<eng-id>/artifacts/`). Every seat artifact opens with the shared header and closes with `## Moves` and a meter line — defined once in [artifact-header.md](artifact-header.md) — and ends with its own red-team checklist, so every attack the gate runs has a named home (ratified 2026-09-13, map ticket [#274](https://github.com/seanwinslow28/code-brain/issues/274)).

**Law and standing behavior**

- [artifact-header.md](artifact-header.md) — the shared frontmatter (`status`, fixed `auditor`, `cosign`, `grounding`, `thin_lane`, `revision` / `stale_from`), who writes which field, the status lifecycle, the artifact-id table.
- [seat-preamble.md](seat-preamble.md) — the standing behavior every seat invocation carries; prepended verbatim to every dispatch (#273).
- [ledger-entry.md](ledger-entry.md) — the decision-ledger entry with the canon line (#268).
- [handoff-contract.md](handoff-contract.md) — the Systemcraft handoff, both directions (#271).

**The seven seat artifacts, in train order**

| Stage | Seat | Template | Gap templates it carries |
|---|---|---|---|
| 1 | Product Strategist | [strategy-pov.md](strategy-pov.md) | point-of-view statement |
| 2 | Discovery Lead | [discovery-packet.md](discovery-packet.md) | — |
| 3 | Insights & Analytics | [metrics-evidence-plan.md](metrics-evidence-plan.md) | — |
| 4 | Growth & Distribution Architect | [growth-gtm.md](growth-gtm.md) | activation and retention playbook; growth-experiment design |
| 5 | Business & Economics Modeler | [business-case.md](business-case.md) | business case; unit-economics model |
| 6 | Delivery & Execution Lead | [outcome-roadmap.md](outcome-roadmap.md), then [handoff-brief.md](handoff-brief.md) | — |
| 7 | Product Leadership & Org Designer | [leadership-packet.md](leadership-packet.md) + [decision-memo.md](decision-memo.md) | decision memo; operating-model doc |

**Engagements beyond the train, and the checks**

- [execution-breakdown.md](execution-breakdown.md) — the Delivery-only engagement after Systemcraft's return: intake check, epics → stories (design set flagged, implementation set) → first sprint plan → filed issues.
- [check-record.md](check-record.md) — the artifact of every co-sign and trailing audit, plus the four-rung evidence-strength scale.
- [gate-findings.md](gate-findings.md) — the red-team gate's findings file with Productcraft's typed verdicts (`STRATEGY | HANDOFF | TRAIN | AUDIT`) and the whole-train attacks.

**Written for Sean, never handed to a seat**

- [readout.md](readout.md) — the human version of a final, past-gate artifact; derivative, lives in the private ledger at `readout/`, never hashed as a pass input and never a trigger for a repair (ruled 2026-09-14 at pc-eng-001's Gate 1). The master skill's Gate and Close steps say when each one is written.
- [readout-glossary.md](readout-glossary.md) — the standing language bridge every readout copies its terms from, so a term is never defined two ways.

Systemcraft's [red-team-protocol](../../systemcraft/templates/red-team-protocol.md), [close-digest](../../systemcraft/templates/close-digest.md) and [status-vocabulary](../../systemcraft/templates/status-vocabulary.md) are inherited by link until `craftwork` extracts them.
