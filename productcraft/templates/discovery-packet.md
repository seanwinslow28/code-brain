# Discovery packet template

Owned by the **Discovery Lead** (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)). Stage 2. A **packet**: three fixed parts that ship as one unit — the discovery plan, the opportunity solution tree, and the evidence section. Receives the Strategy & POV doc in full. **Not done until the Insights & Analytics seat's touch-one co-sign lands** ([check-record.md](check-record.md)): fresh-context, grading stance, sees the Strategy doc and this whole packet *including the raw-evidence pointers*, attaches an evidence-strength grade to every claim in `## Evidence`, passes or bounces each. Audited fresh-context by **Product Leadership & Org Design** (anchor: the plan) — stake: *can this org actually run continuous discovery, and who will resist it?* This seat audits the Strategy doc once this packet exists.

Header fields per [artifact-header.md](artifact-header.md). Raw evidence (interview notes, transcripts, data) stays on disk under the engagement folder and is **pointed at, never pasted**; it never crosses a handoff.

```markdown
---
id: pc-eng-001.discovery
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-21
seat: discovery-lead
stage: 2
model: claude-opus-5
grounding: full
thin_lane: []
adjacent_lanes: []
revision: 1
stale_from: null
status: draft
cosign: pending                    # → pc-eng-001.cosign-discovery, Insights touch one
auditor: product-leadership
audit: pending
---

# Part 1 — Discovery plan

## Desired outcome

The Strategy doc's outcome (by id, `O1`…) this discovery serves. One. A plan serving three outcomes is three plans.

## Participants

Who is interviewed or observed, how they are recruited, and what past behavior qualifies them. Friends and family answer past-behavior questions only, never "would you use it". Cadence: how many conversations a week, for how long.

## Methods

| Method | What it can show | What it cannot show | Owner | Cadence |
|---|---|---|---|---|

## Assumptions to test first

The riskiest assumptions under the Strategy doc's bets, ranked, each with the test that retires it and the evidence that would kill it.

| # | Assumption | From bet | Test | Kills it if |
|---|---|---|---|---|

# Part 2 — Opportunity solution tree

## Tree

Outcome at the root (by id); opportunities as customer needs, pains or desires in the customer's words; solutions beneath the opportunity they serve; assumption tests beneath the solution they de-risk. Render as an indented list; every opportunity node carries the claim ids from Part 3 that support it.

- **O1** <outcome>
  - **Opp-1** <opportunity> — claims: C1, C2
    - **Sol-1a** <solution> — tests: T1

## Target opportunity

Which opportunity is being pursued now and why it over the others — the comparison, in one breath, of size, reach, and evidence strength.

# Part 3 — Evidence  ⟵ co-signed by Insights, claim by claim

Each row is one claim a bet, an opportunity, or a solution rests on. The `Grade` column is **reserved for Insights**: it is written in the co-sign record and transcribed here on the redraft, never filled by this seat. A claim with no raw-evidence pointer bounces. "Customers want faster onboarding" bounces; "six of eight interviewees described abandoning setup unprompted, transcripts linked" passes.

| Id | Claim | Supports | Source (pointer to raw evidence) | Participants (n) | Grade (Insights) |
|---|---|---|---|---|---|
| C1 | | Opp-1 | `evidence/interviews/2026-09-18-p03.md` §2 | 6 of 8 | |

## What the evidence does not show

The claims the team wanted to make and could not. Named, so the Strategist and Growth do not make them later.

## Moves

- kept — <upstream item> from pc-eng-001.strategy
- added — <new item> from <source: evidence file, check record, gate finding, brief section>
- split — <upstream item> → <child>, <child> from pc-eng-001.strategy
- merged — <upstream item> + <upstream item> → <item> from pc-eng-001.strategy
- dropped — <upstream item> from pc-eng-001.strategy; <why>

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (close gate; Leadership's audit and Insights' co-sign cover the rest)

- **Summaries where pointers should be** — a `Source` cell that names a synthesis, a deck, or "interviews" with no file.
- **Preference sold as behavior** — a claim graded `stated-preference` or `inferred` carrying a bet in `Supports`.
- **The convenient sample** — participants who could not have failed to agree; recruiting that filters for enthusiasm.
- **A tree with one branch** — one opportunity, one solution, no rejected alternatives; the plan was a pitch.
- **Assumptions nobody will test** — a `Test` cell with no owner, no date, or a method Part 1 does not list.
- **An unrunnable plan** — cadence, recruiting or methods this org cannot sustain (Leadership's stake, checked cross-artifact against the operating-model doc).
