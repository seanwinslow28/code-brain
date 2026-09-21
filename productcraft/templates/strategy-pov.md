# Strategy & POV doc template

Owned by the **Product Strategist** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 1, the origin draft: written from the engagement brief and relevant past ledger entries, with no upstream artifact. Every downstream seat receives it in full, so it must stand alone. **Positioning is authored here and nowhere else** — Growth quotes it verbatim; a disagreement is a loopback with evidence. **OKR outcomes are drafted here and owned jointly**: Insights bounces any outcome it cannot give a metric (stage 3); Delivery translates them into key results (stage 6) and never sets a goal that is not signed here. Audited fresh-context by the **Discovery Lead** once stage 2's evidence exists — stake: *is the point of view grounded in customer evidence, or in the founder's wish?* Anchor artifact of **Gate 1**.

The **point-of-view statement** is one of the seven gap templates; it lives here as a required section, not a separate file. Header fields per [artifact-header.md](artifact-header.md).

```markdown
---
id: pc-eng-001.strategy
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-20
seat: product-strategist
stage: 1
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: n/a
auditor: discovery-lead
audit: pending
gate_1: pending                    # pending | STRATEGY PASS <date> | STRATEGY PASS WITH ACCEPTANCES <date> | STRATEGY FAIL <date> → pc-eng-001.gate-1
---

## Diagnosis  ⟵ Rumelt's kernel; the POV answers it

What is actually going on here, in prose — the **binding constraint**, named as one thing, before any statement of what to do. A diagnosis that lists five problems has not diagnosed; pick the one whose resolution unlocks the others and say why the rest follow. Cite the evidence ids the brief supplies; a diagnosis resting on the founder's account of his own project is a finding the Discovery Lead's audit will raise.

Close with a **guiding policy**: one sentence, the approach that follows from the diagnosis, stated so a later seat can tell whether an action obeys it or not. The bets below are the coherent actions; each must obey this policy.

## Point of view

Four lines, each a field. **Who** — the customer, in a situation, not a demographic. **What they are trying to get done** — in their words or their observed behavior. **What stands in the way today** — the specific failure of the current options. **What we believe** — the bet, stated so it could be wrong. A POV that could not be wrong is a wish.

## Vision

Where the product is in three years if the bet is right, one paragraph, in customer terms. If it needs two paragraphs the point of view is not done.

## Positioning  ⟵ authoritative; Growth quotes this verbatim

| Field | Statement |
|---|---|
| Competitive alternatives | what the customer does today if this did not exist |
| Unique attributes | what this has that the alternatives do not |
| Value | what those attributes let the customer do |
| Best-fit customer | who cares most about that value |
| Market category | the frame the customer already understands |

## Strategic bets

Three at most. Each names the option chosen, the strongest option not chosen, and the reason — a bet without a rejected alternative is not yet a decision. Mark each bet's dependence on the point of view: which line of the POV, if false, kills it.

| # | Bet | Rejected alternative | Why A over B | Dies if |
|---|---|---|---|---|

## Non-goals

What this deliberately does not do, and for whom it is not. A missing non-goal is a scope-creep vector, so name them; the handoff brief inherits them and Systemcraft may not design around them.

## OKR outcomes (draft)  ⟵ Insights bounces any it cannot measure; Delivery translates, never sets

Outcomes only — customer or business results, no key results, no dates, no numbers. One per line, each with the bet it serves.

| Id | Outcome | Serves bet |
|---|---|---|
| O1 | | |

## Framing only — what this bench does not answer

The questions this engagement **frames rather than answers**, because they are craft decisions outside every seat's lane — combat design, visual direction, copy, sound. One block each: name the question, state the bar the strategy needs it to clear (what a good answer would let a downstream seat conclude), and name who owns it. Nothing here becomes a bet, an outcome or a key result; a seat that quietly answers one of these has left its lane.

Write the section even when it is empty — `none: every open question here sits inside a seat's lane` — so a reader can tell the difference between a bench that stayed in its lane and one that never checked.

## Evidence this rests on

What grounded the point of view: past ledger entries by id, raw-evidence pointers, market facts with a source. The Discovery Lead audits against this section; "we believe" with nothing beneath it is the finding.

## Harm check

Could any outcome above reward hurting the customer or a third party (the "assumed resolution" class)? State the check even when the answer is no.

## Moves

<!-- MACHINE-READ. The rung-0 checker (productcraft/trace/check.py) parses this section line by line
     against the pass's recorded inputs. Move lines only, one per line, from the five-op grammar in
     artifact-header.md § Moves — or the single `origin draft, no upstream` line. A sentence of prose
     here is a malformed line and a finding, not a note: put the note in the record's ## Notes. -->

origin draft, no upstream — leaned on: <ledger ids, brief sections>
<!-- a repair after Gate 1 or a loopback uses the five move lines instead, against pc-eng-001.strategy revision N and the finding: grammar in artifact-header.md § Moves -->

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (Gate 1 anchor; the close gate re-runs it)

- **A conclusion with no diagnosis** — `## Diagnosis` names more than one binding constraint, or names none and opens with what to do; a guiding policy that no action could disobey.
- **A craft question answered anyway** — a bet, outcome or key result that decides something `## Framing only` says this bench does not answer.
- **A point of view that cannot be wrong** — every line of `## Point of view` must be falsifiable by evidence Discovery could collect.
- **Founder's wish dressed as evidence** — `## Evidence this rests on` cites nothing observed, or cites a summary where a pointer should be.
- **Hidden assumptions** — a bet's `Dies if` names nothing, or names something no seat will ever test.
- **Missing non-goals** — a plausible adjacent scope with no non-goal ruling it out.
- **Outcomes that reward harm** — an outcome met by making the customer worse off; `## Harm check` says "no" without saying how it checked.
- **Positioning by assertion** — a `Unique attributes` row an alternative already has.
- **Unmeasurable outcomes** — an outcome that survived stage 3 without a metric in the Insights plan (cross-artifact).
