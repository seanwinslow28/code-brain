---
name: content-machine
description: Interview-first writing orchestrator. Runs a piece from topic to shipped draft through five stages - topic, interview, shape, gates, ship - under one law, that the draft's words come only from the interview transcript. Use when writing anything for publication in the author's own voice, and when asked to "run the content machine", "interview me about", "write this the interview-first way", or "draft from my transcript". Not for neutral technical docs, code, or anything the author has no first-person stake in.
---

# Content Machine

The machine does not write from a topic. It interviews the author, then shapes what he actually
said. Everything below exists to keep that constraint enforced.

Background and the public/private split: [`creative-studio/content-machine/README.md`](../../../creative-studio/content-machine/README.md).
Build map: [GitHub #158](https://github.com/seanwinslow28/code-brain/issues/158).

## The law

**The interview transcript is the only permitted source of draft words.**

A model asked to write about a topic fills the gaps with the average of its training data. The
output passes every style rule and still belongs to nobody. Removing the gap-fill step is the
entire design.

What the law permits and forbids:

| | |
|---|---|
| **Permitted** | Anything the author said in the interview, in any order, cut, compressed, re-punctuated, or re-cased. Connective tissue that carries no claim and no image ("and then", "so", "the next morning"). Facts the author stated. Structural labels the contract requires (a title, a section header). |
| **Forbidden** | Any image, joke, metaphor, number, name, place, or claim the author did not say. A better verb for a thing he described plainly, where the better verb adds color he didn't supply. A reference he didn't reach for. A closing line assembled from nothing. |
| **The test** | Point at any vivid phrase in the draft and name the transcript line it came from. Can't name one? It's an invention. Cut it or go ask him. |

Professional-lane documents (resume, cover letter, questionnaire) run the **facts-only** form of the
law: every claim traces to the transcript, phrasing may be conventional. Nobody wants a resume
written in dive-bar register.

**No autonomous revision loops.** The machine writes candidates; the author ratifies. There is no
score-until-good cycle, no persona panel, no numeric quality mean. A gate may route exactly one
grounded revise request; the author decides everything else.

## Stages

| # | Stage | Owner | Status |
|---|---|---|---|
| 0 | **Oracle** — proposes what's worth writing from the author's recent work | `/content-oracle` | not built ([#169](https://github.com/seanwinslow28/code-brain/issues/169)) |
| 1 | **Topic** — one piece, one lane, one medium, named before anything else | this skill | live |
| 2 | **Interview** — one lens, one question at a time, read-back at the close | `interview/` | storyteller lens only ([#165](https://github.com/seanwinslow28/code-brain/issues/165)) |
| 3 | **Shape** — the transcript becomes prose | `writing-voice-modes` | live |
| 4 | **Gates** — value, structure, critique, humanity, origin | chain skills | origin gate hand-run ([#164](https://github.com/seanwinslow28/code-brain/issues/164)) |
| 5 | **Ship** — the author publishes | the author | live |
| 6 | **Lessons** — his corrections become rules, with his consent | `ledger/` | not built ([#168](https://github.com/seanwinslow28/code-brain/issues/168)) |

Stage 0 is skippable by design: a hand-picked topic is a legitimate input. Stage 6 is not skippable
once built, because a machine that never learns from his rewrites makes the same mistake weekly.

## Handoffs

Each stage emits one labeled block and consumes the one before it. The blocks are metadata; none of
them is ever part of the published text.

### Stage 1 → TOPIC CARD

```
TOPIC CARD
Piece: <one line, the thing itself>
Lane: Expressive | Professional
Medium: <which contract governs>
Why now: <what makes this worth the author's hour>
Constraints: <editorial law that binds this piece; series, order, house rules>
```

### Stage 2 → TRANSCRIPT

Stored under `creative-studio/content-machine/transcripts/` (git-ignored — it is verbatim author).
Never pasted into a tracked file, an issue, or a commit message.

```
TRANSCRIPT — <slug> — <date>
Lens: <which interviewer lens>
Duration: <real elapsed time>

Q1: <question asked>
A1: <answer, verbatim, uncorrected>
...

READ-BACK
<the interviewer's summary of the story back to the author>
CORRECTIONS
<what he changed, verbatim>
```

Verbatim means verbatim. Do not tidy his grammar, complete his sentences, or drop his false starts:
the false starts are where the voice lives, and a tidied transcript quietly re-introduces the
gap-fill the law exists to prevent.

### Stage 3 → DRAFT + ORIGIN LEDGER

The draft ships with two attachments. The Voice Decision Record is `writing-voice-modes`' own
(mode, dial, moves deployed, sweeps run). The Origin Ledger is this machine's:

```
ORIGIN LEDGER
Traced: <count> vivid phrases, each to a transcript line
Untraced: <every phrase that entered the draft from somewhere other than the transcript>
  - "<phrase>" — <where it came from, and why it was kept or cut>
Verdict: clean | <n> leaks
```

Untraced does not mean "delete silently". It means show the author, so he can say the line himself
or strike it. The leaks are the signal — they are what the automated origin gate ([#164](https://github.com/seanwinslow28/code-brain/issues/164))
gets built to catch.

### Stage 4 → GATE RECORD

One line per gate: which ran, verdict, what changed. A gate that could not run says so.

### Stage 5 → SHIP PACKET

Final text, images, frontmatter, and the open items the author has to settle himself.

## Running a piece

1. Name the topic and emit the TOPIC CARD. If the medium has no contract yet, say so and write the
   piece against the lane's general rules rather than inventing a contract mid-run.
2. Read the medium contract in `contracts/<lane>/<medium>.md` and the publication's own house rules
   before the interview, not after. The contract decides which moves are licensed and what the
   piece has to deliver; the interview has to go get that material.
3. Interview with one lens. One question at a time. Never answer for him, never offer him a menu of
   answers to pick from, never write his line and ask him to approve it. A lens that answers its own
   questions has broken the machine as thoroughly as a draft written from nothing.
4. Shape. Gate. Hand him the draft with both records attached.
5. He rewrites by hand. That rewrite is the highest-value artifact the machine produces — it is
   corpus, and once the lessons loop exists it is also the lesson.

## The private brain

Read-only inputs, all git-ignored, all local:

| Path | Read it when |
|---|---|
| `creative-studio/content-machine/corpus/` | Calibrating any claim about how the author writes |
| `creative-studio/content-machine/reference-universe.md` | The piece will use a pop-culture anchor or a personal-history detail. References come from here or from the piece's actual subject. Never invented. |
| `creative-studio/content-machine/cheese-bank/` | Before shipping any Expressive draft |
| `creative-studio/content-machine/do-not-promote.md` | Every piece, at the final sweep |
| `creative-studio/content-machine/transcripts/` | The interview record, and later corpus |
| `creative-studio/content-machine/ledger/` | Ratified lessons (once #168 lands) |

Nothing from these paths is ever quoted into a tracked file, a GitHub issue, or a commit message.
The repo is public.

## Related skills

- `writing-voice-modes` — Stage 3. The transcript-shaper. Owns sentences, not story order.
- `storytelling-architecture` — beat map. Owns story order.
- `substack-value-engine` — the value gate. Owns whether the piece is worth a reader's time.
- `writing-critique` — adversarial gate. Never rewrites; routes one grounded revise.
- `writing-humanity-pass` — final scrub. Owns the AI-tell sweep and the no-em-dash rule.
- `grilling` — when the author wants the *plan* stress-tested rather than the story drawn out.
