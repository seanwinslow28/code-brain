# Outcome roadmap template

Owned by the **Delivery & Execution Lead** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 6. Receives everything above it in full. **Delivery owns the roadmap; the Strategist owns the outcomes.** The **OKR translation** is a required section, written against the Insights plan's metrics and **co-signed by the Product Strategist**, key result by key result, in a fresh-context pass ([check-record.md](check-record.md)) — the train's third co-sign touch. Delivery never sets an unsigned goal; the Strategist never sets a date. Audited fresh-context by the **Business & Economics Modeler** — stake: *does the sequencing protect payback and cash, or front-load cost?*

Right after the co-sign lands, this seat writes the **handoff verdict**: a [handoff brief](handoff-brief.md) if the first shipping slice has a Systemcraft-owned layer, else a recorded no-handoff entry. Stories, sprint plans, release notes and retros are **not** in this artifact — they belong to the [execution breakdown](execution-breakdown.md) after the return. Header fields per [artifact-header.md](artifact-header.md).

```markdown
---
id: pc-eng-001.roadmap
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-25
seat: delivery-execution
stage: 6
model: claude-sonnet-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: pending                    # → pc-eng-001.cosign-okr, Strategist on the OKR translation
auditor: business-economics
audit: pending
handoff_verdict: pending           # pending | brief → pc-eng-001.handoff | no-handoff → pc-eng-001.dNN
---

## Now / next / later

Outcomes, not features, in three horizons. Each row names the Strategy outcome it serves and the Discovery opportunity it pursues; a row with neither is a feature that walked in.

| Horizon | Outcome (id) | Opportunity (id) | What we will learn or earn | Owner |
|---|---|---|---|---|

## OKR translation  ⟵ co-signed by the Strategist, key result by key result

| Outcome (Strategist id) | Key result | Metric (Insights id) | From → to, by when | Verdict (Strategist) |
|---|---|---|---|---|
| O1 | KR1.1 | | | |

Key results use the Insights plan's metrics only. A key result the Strategist bounces is rewritten here; an outcome that cannot be translated is a loopback to the Strategist, not a key result invented to fill the row.

## First shipping slice

What ships first, by when, and why this slice over the next-best one. Names every layer inside it and whether any is **Systemcraft-owned** (an AI system, a platform, a technical architecture) — this line is the handoff trigger. The brief's `First shipping slice` constraint quotes this section.

## Sequencing and cash

Order of the slices with the reason for the order; the cash each slice consumes before it earns, read from the business case; the payback the sequence protects. Business audits this section.

## Dependencies and holds

What waits on Systemcraft's return, what waits on a gatekeeper, what waits on a purchase or a hire. Each with an owner and a date. Design-set work is a **flagged placeholder** until a Designcraft team exists.

## Risks to the plan

Three, observable, each with the roadmap change it would force.

## Moves

<!-- MACHINE-READ. The rung-0 checker (productcraft/trace/check.py) parses this section line by line
     against the pass's recorded inputs. Move lines only, one per line, from the five-op grammar in
     artifact-header.md § Moves — or the single `origin draft, no upstream` line. A sentence of prose
     here is a malformed line and a finding, not a note: put the note in the record's ## Notes. -->

- kept — <upstream item> from pc-eng-001.business
- added — <new item> from <source: evidence file, check record, gate finding, brief section>
- split — <upstream item> → <child>, <child> from pc-eng-001.business
- merged — <upstream item> + <upstream item> → <item> from pc-eng-001.business
- dropped — <upstream item> from pc-eng-001.business; <why>

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (close gate; the Strategist's co-sign and Business's audit cover the rest)

- **Features in outcome clothing** — a row whose outcome id is decorative; the "what we will learn or earn" cell describes shipping.
- **Unsigned goals** — a key result without a Strategist verdict, or one whose metric the Insights plan does not carry.
- **Dates on outcomes** — the Strategist's outcomes given deadlines here.
- **Front-loaded cost** — a sequence whose first two slices consume most of the cash before any slice earns (Business's stake).
- **A silent Systemcraft layer** — a first slice with an AI or platform component and `handoff_verdict: no-handoff`.
- **Holds without owners** — a dependency row with no date or no name.
- **Stories smuggled in** — implementation detail that belongs to the execution breakdown.
