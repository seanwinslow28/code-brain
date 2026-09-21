# Leadership packet template

Owned by the **Product Leadership & Org Designer** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 7, after the handoff verdict. A **packet** of three hard contracts — the **stakeholder map**, the **decision memos**, the **operating-model doc** — so the seat never drifts into advice. Craft rule: **no sentence without a field.** Prose not attached to a field is cut; an empty required field fails loudly. Audited fresh-context by the **Product Strategist** (anchor: the decision memos) — stake: *does the decision follow the strategy, and is the why-A-over-B honest rather than retrofitted?* Written after the brief crosses, about the org, not the system; it never freezes into a handoff.

Two of the seven gap templates live in this packet: the operating-model doc is Part 3 below; the **decision memo** is its own file, one per decision ([decision-memo.md](decision-memo.md)), indexed in Part 2. Header fields per [artifact-header.md](artifact-header.md).

**Solo-builder rule.** A *stakeholder* is anyone who can block, fund, use, or judge the thing; a *teammate* is whoever does the work. Agents do work, so they appear in the topology and never on the map. The map is never one row.

```markdown
---
id: pc-eng-001.leadership
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-26
seat: product-leadership
stage: 7
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: n/a
auditor: product-strategist
audit: pending
memos: [pc-eng-001.memo-01]        # every decision memo in this packet, by id
---

# Part 1 — Stakeholder map

One row per party. Done when no row has an empty field. Classes that are absent are **stated absent**, never omitted.

| Party | Class | Controls (decision right / veto / budget / team) | Needs from this design | Predicted stance (support / resist / neutral) — evidence | Ask | By when |
|---|---|---|---|---|---|---|
| Sean — decider | owner hat | | | | | |
| Sean — builder | owner hat | | | | | |
| Sean — funder | owner hat | | | | | |
| <named user panel> | users | | | | | |
| <app-store review / payment processor / platform terms> | gatekeeper | | | | | |
| <hiring managers / customers / investors> | judge | | | | | |
| Systemcraft | AI-layer holder | the handoff's decisions | | | the return, per the brief | <return date> — or "absent: no-handoff verdict pc-eng-001.dNN" |

Absent classes: <none | gatekeeper: none identified because …>

# Part 2 — Decision memos

One memo per decision, in [decision-memo.md](decision-memo.md) form, indexed here. Each memo's state mirrors its ledger entry.

| Memo id | Question | State (proposed / ratified / superseded) | Ledger entry |
|---|---|---|---|
| pc-eng-001.memo-01 | | proposed | pc-eng-001.d40 |

# Part 3 — Operating-model doc

## Team topology

Two entity types, never mixed. Never dress an agent as a person.

**Humans**

| Who | Owns | Decides | Reviewed by |
|---|---|---|---|

**Agents**

| Seat or skill | Baseline model | Owns | Cannot do | Reviewed by | Invocation record |
|---|---|---|---|---|---|
| discovery-lead | claude-opus-5 | the Discovery packet | decide, edit another seat's artifact | product-leadership (audit) | `trace/pass-NN-discovery-lead-draft.md` |

The `Invocation record` column points at the pass record (#272); it never narrates the run.

## Decision rights and escalation

"Agents propose, Sean decides." Then the table: what is decided where, by whom, and the path when a decision is contested or exceeds the decider's right.

| Decision class | Proposed by | Decided by | Escalates to | Recorded in |
|---|---|---|---|---|

## Cadences

Done when every ritual has an owner, a cadence, and the artifact it reads.

| Ritual | Owner | Cadence | Reads (artifact id or Insights view) | Produces |
|---|---|---|---|---|
| Discovery sync | | weekly | pc-eng-001.discovery Part 1 | |
| Planning | | | pc-eng-001.roadmap | |
| Review | | | Insights dashboard <id> | |

## Metrics reviewed

Pulled from the Insights plan by id, with when each is looked at and the decision it feeds. Never re-invented here.

| Metric (Insights id) | Reviewed at (ritual) | Feeds decision class |
|---|---|---|

## Delta from today

What changes in who, what, and when, versus how the org runs now; the first change and its date.

## Moves

<!-- MACHINE-READ. The rung-0 checker (productcraft/trace/check.py) parses this section line by line
     against the pass's recorded inputs. Move lines only, one per line, from the five-op grammar in
     artifact-header.md § Moves — or the single `origin draft, no upstream` line. A sentence of prose
     here is a malformed line and a finding, not a note: put the note in the record's ## Notes. -->

- kept — <upstream item> from pc-eng-001.roadmap
- added — <new item> from <source: evidence file, check record, gate finding, brief section>
- split — <upstream item> → <child>, <child> from pc-eng-001.roadmap
- merged — <upstream item> + <upstream item> → <item> from pc-eng-001.roadmap
- dropped — <upstream item> from pc-eng-001.roadmap; <why>

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (close gate; the Strategist's audit covers the memos)

- **Advice without a field** — a sentence not attached to a row or a named field.
- **The one-row map** — Sean as a single stakeholder; a user class with no named panel; an absent class not stated absent.
- **Agents as people** — an agent on the stakeholder map, or a topology row with no `Cannot do` or no invocation record.
- **Rituals without inputs** — a cadence with no artifact to read, or one reading a metric the Insights plan does not carry.
- **Retrofitted why** — a memo whose why-A-over-B was written after the choice (the Strategist's stake).
- **Systemcraft omitted** — neither a return-date ask nor a stated absence.
- **Discovery the org cannot run** — the plan's cadence has no ritual here (cross-artifact with the Discovery packet).
