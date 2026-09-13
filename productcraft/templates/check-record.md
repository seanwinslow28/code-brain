# Check record template — co-signs and audits

The artifact of a **co-sign** or **audit** pass: what the checking seat saw, what it passed or bounced, what it attacked and what held. Written by the checking seat in a fresh-context invocation that receives artifacts only, never the drafting conversation. Two of the train's three co-sign touches use it (Insights on the Discovery evidence, `<eng>.cosign-discovery`; the Strategist on the OKR translation, `<eng>.cosign-okr`); the third — Insights on the Strategist's outcomes — is the outcome-to-metric table inside the [metrics & evidence plan](metrics-evidence-plan.md). Every trailing audit uses it (`<eng>.audit-<artifact-slug>`). The record travels beside the checked artifact through the train (a downstream seat reads the grades) and **stays behind at a handoff**, per the contract. The coordinator transcribes the verdict into the checked artifact's `cosign:` or `audit:` field and into the pass record's `checks`.

A check never edits the checked artifact: a bounce or a material defect is a loopback to its drafting seat. Header fields per [artifact-header.md](artifact-header.md).

```markdown
---
id: pc-eng-001.cosign-discovery    # cosign-<slug> | audit-<slug>
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-21
seat: insights-analytics           # the checking seat
kind: cosign                       # cosign | audit
stage: 2                           # the checked artifact's stage
model: claude-opus-5
grounding: full
checked: pc-eng-001.discovery      # artifact id and revision checked
checked_revision: 1
anchor: Part 3 — Evidence          # co-sign: the section; audit: the packet part the stake anchors on
stake: null                        # audit only — the seat's one-sentence stake, verbatim from its seat file
verdict: CO-SIGN BOUNCE — 2 claims # see Verdict lines
---

## Verdict line

One of: `CO-SIGN PASS` · `CO-SIGN BOUNCE — <n> claims` · `AUDIT CLEAN — stake held` · `AUDIT LOOPBACK — <n> material` · `AUDIT NOTES ONLY`. Rendered per Systemcraft's status vocabulary: the line, then **Means**, then **Does not mean / Next**.

## Claims or findings

Co-sign: one row per claim in the anchor section. Audit: one row per finding, severity **MATERIAL** (loops back) or **NOTE**.

| # | Claim or finding | Section | Grade or severity | Evidence pointer opened | Verdict | What would pass |
|---|---|---|---|---|---|---|
| C1 | | Part 3 | observed-behavior | `evidence/…` | pass | |
| C4 | | Part 3 | stated-preference | `evidence/…` | bounce | a past-behavior instance from ≥ 3 participants |

## What was attacked and held

Being unable to find a defect is a finding: name what was attacked, how, and why it held.

## Loopback

The one message to the drafting seat: which rows, what evidence, what would pass. Empty on a clean check — say "none".

meter: <runtime> · <tokens> · <wall-clock>
```

## Evidence-strength grades

The four-rung scale Insights attaches at touch one and every seat uses to grade its own inputs before Insights audits them. Named for what the evidence *is*, never for how confident anyone feels.

| Grade | The evidence is | May carry |
|---|---|---|
| `observed-behavior` | Past behavior seen directly — usage data, a transcript of the act, an observed session — with a pointer | a bet, an opportunity, a solution |
| `reported-behavior` | A participant's account of a specific past instance, in their words, with a pointer | a bet or opportunity when ≥ 3 participants report it unprompted; else a hypothesis |
| `stated-preference` | An opinion, a "would you", a rating | a hypothesis only — never a bet |
| `inferred` | The team's inference with no participant source | a hypothesis only, labeled as the team's |

A claim graded `stated-preference` or `inferred` that sits under a bet in the Discovery tree **bounces**. The grade is written here and transcribed into the Discovery packet's `Grade (Insights)` column on the redraft.

## Red-team checklist (the close gate reads every check record)

- **Generous grading** — a `reported-behavior` grade on a claim whose pointer is a summary, or whose participants are unnamed.
- **A check that saw the conversation** — inputs listing anything but artifacts (the pass record's `withheld` must include the drafting conversation).
- **Silent pass** — `What was attacked and held` empty on a clean verdict.
- **Severity laundering** — a material defect filed as a NOTE to avoid the cascade.
- **The stake not answered** — an audit record whose rows never address the stake sentence.
