# Growth model & GTM plan template

Owned by the **Growth & Distribution Architect** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 4. Receives the Strategy doc, the co-signed Discovery packet and the Metrics & evidence plan in full. **Quotes the positioning verbatim** from the Strategy doc — a disagreement is a loopback with evidence, never an in-place rewrite. **Designs the money loops** (conversion, upsell, referral) and quotes the price; Business designs the price and packaging at stage 5, so the price here is a **hypothesis** until then. Audited fresh-context by **Insights & Analytics** (anchor: the experiment section) — stake: *are the experiments measurable, statistically powered, and honestly read — the designer never grades?*

Two of the seven gap templates live here as required sections: the **activation and retention playbook** and the **growth-experiment design**. The experiment section is checked by Insights' trailing audit, not by a fourth co-sign touch (the train has three: #266). Header fields per [artifact-header.md](artifact-header.md).

```markdown
---
id: pc-eng-001.growth
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-23
seat: growth-distribution
stage: 4
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: n/a
auditor: insights-analytics
audit: pending
price_source: hypothesis           # hypothesis | business-case <date> — flipped by the coordinator when stage 5 lands
---

## Positioning (quoted)

The Strategy doc's positioning table, verbatim, with its id. Nothing here is this seat's to change.

## Beachhead and ideal customer

The first segment, why it over the next-best segment, and the observable traits that identify a member. Every trait points at a Discovery claim id.

## Growth loops

Each loop as a closed cycle: the input, the action, the output that becomes the next input, and the metric from the Insights plan that measures each step. A loop with a step that no metric measures is a funnel, not a loop.

| Loop | Input → action → output | Step metrics (Insights ids) | Where it leaks |
|---|---|---|---|

## Channels

| Channel | Why this customer is there | Cost to reach (order of magnitude) | Owner | What kills it |
|---|---|---|---|---|

## Activation and retention playbook

**Activation** — the moment a new user has had the value the point of view promised, as an observable event; the steps to it; where the drop-off is and what the evidence says causes it. **Retention** — the natural frequency of the job; what a retained user looks like at day 7, 30 and 90 in events; the cohort view the Insights plan provides and the intervention per drop-off cause. Each intervention names the loop or channel it feeds. Interpreting a curve into an intervention is this seat's craft; producing the curve is Insights'.

| Stage | Observable event | Current or expected rate | Cause (claim id) | Intervention | Feeds |
|---|---|---|---|---|---|

## Monetization loops

Conversion, upsell, referral — each a loop above, with the **price quoted as a hypothesis** (`price_source`). Business confirms or replaces it in the business case. A replacement that breaks a loop is raised in this seat's audit of the business case; the repair is Business's unless the loop itself must change, in which case this artifact is redrafted and the cascade below it fires.

## Growth-experiment design

One block per experiment, written so Insights can power and read it without asking:

| Id | Hypothesis (if we change X, metric Y moves because Z) | Primary metric (Insights id) | Guardrails | Minimum detectable effect | Sample and duration | Reader (never this seat) | Decision it feeds |
|---|---|---|---|---|---|---|---|

## Moves

<!-- MACHINE-READ. The rung-0 checker (productcraft/trace/check.py) parses this section line by line
     against the pass's recorded inputs. Move lines only, one per line, from the five-op grammar in
     artifact-header.md § Moves — or the single `origin draft, no upstream` line. A sentence of prose
     here is a malformed line and a finding, not a note: put the note in the record's ## Notes. -->

- kept — <upstream item> from pc-eng-001.strategy
- added — <new item> from <source: evidence file, check record, gate finding, brief section>
- split — <upstream item> → <child>, <child> from pc-eng-001.strategy
- merged — <upstream item> + <upstream item> → <item> from pc-eng-001.strategy
- dropped — <upstream item> from pc-eng-001.strategy; <why>

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (close gate; Insights' audit covers the experiments)

- **Positioning drift** — the quoted table differs from the Strategy doc's by a word.
- **Funnels called loops** — a loop with no output-to-input step, or a step no Insights metric measures.
- **Self-graded experiments** — a `Reader` cell naming this seat, or an experiment with no guardrail.
- **Underpowered by design** — a sample or duration the beachhead cannot supply.
- **Activation by assertion** — an activation event no Discovery claim supports.
- **Channel economics that only work at best case** — a reach cost with no `What kills it`.
- **Price laundering** — a monetization loop that depends on a price this seat set as fact rather than hypothesis.
