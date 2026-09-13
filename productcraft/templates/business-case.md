# Business case template

Owned by the **Business & Economics Modeler** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 5. Receives everything above it in full. Systemcraft's Ops & Economics analogue and the bench's tool-poorest seat, so this template is authored, not borrowed. **Designs price and packaging**; Growth quotes the price into its loops, and a disagreement loops back here. Two required sections are gap templates: the **unit-economics model** and the **business case** proper. Audited fresh-context by the **Growth & Distribution Architect** — stake: *do the unit economics survive the real acquisition channels and the real retention curve?* The Business seat in turn audits the roadmap for payback and cash.

Header fields per [artifact-header.md](artifact-header.md). Inherited from Systemcraft's ops model: **a number that only works at best case is an audit defect — show expected, best and worst.**

```markdown
---
id: pc-eng-001.business
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-24
seat: business-economics
stage: 5
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: n/a
auditor: growth-distribution
audit: pending
---

## The case in one breath

What is being asked for (money, time, a bet), what it returns, by when, and what has to be true. If Sean reads only this section, the decision is still possible.

## Pricing and packaging

| Package | Who it is for (Growth's segment) | What is in it | Price and metric (per seat, per use, flat) | Why this price and not the nearest alternative |
|---|---|---|---|---|

State the pricing *model* chosen and the strongest rejected model. Growth's `price_source` flips to `business-case` when this lands; a price that breaks a Growth loop is Growth's audit finding to raise and this seat's to repair.

## Unit-economics model

Per unit of value (a user-month, a transaction, a seat), at three scenarios. Every input names its source: a Growth channel cost, an Insights retention curve, a live fact with a date.

| Input | Source | Worst | Expected | Best |
|---|---|---|---|---|
| Acquisition cost per customer | Growth channels | | | |
| Gross margin per unit | | | | |
| Retention (Insights curve) | Insights plan | | | |
| Lifetime value | derived | | | |
| Payback (months) | derived | | | |

State the arithmetic once so the gate can redo it. A derived row with no formula is a finding.

## Market and volume

Bottom-up: the beachhead's size in units, the reachable share per channel, the volume each scenario assumes. Top-down numbers may appear only beside a bottom-up one they are checked against.

## Cash and runway

Cost to build and run per scenario, cash need over time, and the month the case turns. The roadmap's sequencing is audited against this section.

## Risks and the kill condition

The three ways this case fails, the observable sign of each, and the number at which the bet is stopped. A case with no kill condition is a hope.

## Moves

- kept — <upstream item> from pc-eng-001.growth
- added — <new item> from <source: evidence file, check record, gate finding, brief section>
- split — <upstream item> → <child>, <child> from pc-eng-001.growth
- merged — <upstream item> + <upstream item> → <item> from pc-eng-001.growth
- dropped — <upstream item> from pc-eng-001.growth; <why>

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (close gate; Growth's audit covers channels and retention)

- **Best-case-only economics** — a scenario column left blank, or a worst case that is the expected case renamed.
- **Retention borrowed, not measured** — a lifetime value using a curve the Insights plan does not provide.
- **Channel cost fiction** — an acquisition cost below what Growth's channel table says.
- **Arithmetic that cannot be redone** — a derived row with no stated formula, or one the gate recomputes differently.
- **Top-down laundering** — a market size with no bottom-up check.
- **No kill condition** — or one no metric in the Insights plan can trigger.
- **Price without a rejected model** — packaging by assertion.
