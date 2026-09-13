# Decision memo template

One of the **Product Leadership & Org Designer**'s three hard contracts (seat contract, [#266](https://github.com/seanwinslow28/code-brain/issues/266)) and one of the seven gap templates. **One decision per memo**, one file per memo, indexed in the [leadership packet](leadership-packet.md). It is the decision's face for Sean; the [ledger entry](ledger-entry.md) is its record — so **the fields align with the ledger schema** and the memo never carries a section the entry lacks. Leadership writes the memo and its entry in the same pass with `status: proposed`; Sean's signature sets the entry's `ratified:` date and the memo's state to `ratified`. A changed mind is a new memo and a new entry that supersedes the old — never a suffix, never an edit.

Craft rule: no sentence without a field. Header fields per [artifact-header.md](artifact-header.md), plus the memo's own.

```markdown
---
id: pc-eng-001.memo-01             # permanent, citable; numbered within the engagement
engagement: pc-eng-001-16bitfit-revisit
date: 2026-09-26
seat: product-leadership
stage: 7
model: claude-opus-5
grounding: full
revision: 1
status: draft
auditor: product-strategist        # the packet's auditor; the memo is its anchor
ledger_entry: pc-eng-001.d40       # the entry this memo mirrors — same decision, same options, same why
state: proposed                    # proposed | ratified | superseded — mirrors the entry's status + ratified: field
supersedes: null                   # memo id this replaces
owner: sean                        # who carries the decision after ratification
---

## Question

The one question this memo answers, as a question. If it needs "and", it is two memos.

## Options

At least two real options. The losers are what "why" is measured against; an option nobody would choose is not an option.

| Option | What it commits us to | Cost or risk | Reversible? |
|---|---|---|---|

## Choice

One sentence, active voice.

## Why A over B

One breath, in the strategy's own terms (cite the Strategy doc's bet or outcome by id). The Strategist audits this line for honesty: written before the choice, not after.

## From the canon

*Title* (Author) — the idea, in this seat's words, and what this decision did with it. Never the book's text. "None — reasoning from the evidence" is written, not omitted.

## Consulted and informed

Consulted (two-way): <seat ids>. Informed (one-way): <seat ids>. Mirrors the entry's `consulted:` / `informed:`.

## Reversal condition

The named observation, metric mark, or date that reopens this. Mirrors the entry's `## Revisit when`.

## Ask of Sean

Ratify, amend, or reject — one line, with what happens on each.

meter: <runtime> · <tokens> · <wall-clock>
```

## Red-team checklist (close gate; the Strategist's audit of the packet anchors here)

- **A straw-man option** — a loser nobody would have chosen; the memo was a rationalization.
- **Why written after the choice** — a why-A-over-B that restates the choice or cites nothing from the strategy.
- **Drift from the ledger** — a memo whose options, why, or reversal condition differ from its entry's.
- **No reversal condition** — or one no metric or event can trigger.
- **Two questions in one memo** — an "and" in the question.
- **The canon line as citation** — quoted or paraphrased text instead of a named idea in the seat's words.
