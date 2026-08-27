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
| 2 | **Interview** — one lens, one question at a time, read-back at the close | `interview/` | live, six lenses |
| 3 | **Shape** — the transcript becomes prose | `writing-voice-modes` | live |
| 4 | **Gates** — value, structure, critique, humanity, origin | chain skills + `gates/` | live |
| 5 | **Ship** — the author publishes | the author | live |
| 6 | **Lessons** — his corrections become rules, with his consent | `lessons/` + `ledger/` | live |

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
ASK LIST: <untraced phrases the draft is better with. One question each, for him to answer.>
  - "<phrase>" — <what the beat is doing, and the question that would get him to say it>
Verdict: clean | <n> leaks
```

Untraced does not mean "delete silently". It means show the author, so he can say the line himself
or strike it.

**The ASK LIST exists because deleting is the more expensive mistake.** On the first real run the
gate cut a flat under-reaction after a bad output ("Cool. Thanks.") for having no transcript source.
Sean put the beat back on rewrite, in his own words, better. The beat was right; only the invented
wording was wrong. A gate that silently cuts loses material the interview simply failed to reach.
So: anything the draft is genuinely better with goes on the ASK LIST as a question, not into a
diff as a deletion.

## The origin gate

Two layers, because the law has two halves and only one of them is mechanical.

**Layer 1, mechanical** (`gates/origin_check.py`, stdlib, no model, $0):

```bash
python3 .claude/skills/content-machine/gates/origin_check.py <draft.md> <transcript.md> --lane expressive
```

It reports every atom in the draft with no counterpart in the transcript, ranked by how hard the
law is on that kind of atom. Numbers, dates, and proper nouns are **claims** (the law names them
explicitly). Everything else is an **image** at most. Connective tissue is exempt by construction,
via a stoplist, because the law already permits it.

**Layer 2, reading.** The mechanical layer cannot tell an invention from a legitimate connective
phrase, and it is blind to the whole class below. Whoever shapes the draft reads the flags, writes
the ORIGIN LEDGER, and puts anything worth keeping on the ASK LIST.

### What layer 1 can and cannot see

Measured against the first real run, whose leaks are pinned in `gates/test_origin_check.py`:

- **7 of 10** real inventions caught, **0** false positives on Sean's own material.
- **Blind to recombination.** All three misses were built entirely from words he did say, put
  together in a way he never did: "it had no table to get anything from" (a pun on his phrase),
  "the research, the ideas, the notes" (his word, wrong speaker), "the actual thinking". A token
  check cannot see these and never will. **Layer 2 owns recombination.** When reading, the question
  is not "is this word his" but "did he put these words in this order."
- It also caught a leak the hand-check missed: the draft had expanded his "WOL" into "wake-on-LAN",
  a word he never said.

Re-run the fixture after any change to the checker: `python3 gates/test_origin_check.py`.

### Lane behavior

| Lane | On an untraced claim | Why |
|---|---|---|
| **Expressive** | Advises. Never blocks, never rewrites. | L8. Sean ratifies; a made-up joke costs a rewrite. |
| **Professional** | **Blocks delivery** (exit 1) while any claim is untraced. | A fabricated number on a resume is a different class of harm. The block is on the document, not on his judgment: he clears it by confirming the fact or striking it. |

The gate reports. It does not revise, does not score, and does not loop.

### The one-artifact rule for coined lines

**A coined line lives in exactly one artifact and is never recycled across mediums.** Reusing the
good line is the most tempting thing the machine can do, because it already worked once. It is also
what turns a body of work into a bag of catchphrases.

Recorded in `coined-lines.md` in the private brain, git-ignored, in the same shape as the corpus so
there is one convention to remember: a `## ` heading names the artifact, every `>` line beneath it is
a coined line that artifact spent.

```bash
python3 .claude/skills/content-machine/gates/coined_lines.py <draft.md> \
    --lane expressive --artifact <this-piece-slug>
```

Stdlib, $0, no model. It catches exact reuse and the more likely case, a line lightly reworded:
below 80% token overlap a shared phrase is just shared vocabulary. `--artifact` exempts the piece's
own lines, so a draft can be re-checked as it evolves. Lane behaviour matches the origin gate:
Expressive advises, Professional exits 1.

It runs inside the **do-not-promote sweep** rather than as a gate of its own. Both ask the same
question at the same moment: is there something in this draft that is true, and good, and still
should not be here.

### Stage 4 → GATE RECORD

One line per gate: which ran, verdict, what changed. A gate that could not run says so.

### Stage 5 → SHIP PACKET

Final text, images, frontmatter, and the open items the author has to settle himself. On an
Expressive medium with a reply surface, the **REPLY-HOOK MEMO** rides along: three lines of advice
about what would draw a reply, binding on nothing (`contracts/expressive/LANE.md`).

## Running a piece

1. Name the topic and emit the TOPIC CARD. If the medium has no contract yet, say so and write the
   piece against the lane's general rules rather than inventing a contract mid-run.
2. Read the medium contract in `contracts/<lane>/<medium>.md`, the licensing matrix it inherits
   (`contracts/move-licensing.md`), the lane law it inherits
   (`contracts/<lane>/LANE.md`), and the publication's or the application's own house rules
   before the interview, not after. The contract decides which moves are licensed and what the
   piece has to deliver; the interview has to go get that material. The lane's **first-screen test**
   is an interview instruction as much as a shape rule: if no beat in the transcript can carry the
   first screen, the interview did not reach far enough.
3. Interview with one lens. One question at a time. Never answer for him, never offer him a menu of
   answers to pick from, never write his line and ask him to approve it. A lens that answers its own
   questions has broken the machine as thoroughly as a draft written from nothing.
4. Shape. Gate. Hand him the draft with both records attached.
5. He rewrites by hand. That rewrite is the highest-value artifact the machine produces — it is
   corpus, and once the lessons loop exists it is also the lesson.

## The lessons loop

The machine learns only from what he actually changed, and only with his reason attached.

**1. Diff** (`lessons/diff_pieces.py`, stdlib, $0):

```bash
python3 .claude/skills/content-machine/lessons/diff_pieces.py <handoff.md> <final.md>
```

Sentence-aligned, not word-aligned, because a lesson is about a beat rather than a token. A reworded
sentence arrives as one change to ratify instead of six insertions and four deletions. Block-quote
markers and smart quotes are normalized away so formatting never registers as an edit he made.

**2. Propose.** The machine reads the change list and writes one candidate lesson per change into
`ledger/lessons.md` with `Status: pending`. A pending candidate has changed nothing.

**3. Ratify.** He supplies the two things the machine may not infer: **his reason, verbatim**, and a
**scope tag** (permanent rule vs one-off exception). No lesson enters any file without both.

**4. Route.** A ratified permanent lesson goes to exactly one home:

| Lesson is about | Home |
|---|---|
| How he writes | the voice guide |
| How a story is built | `storytelling-architecture` |
| How this medium works | `contracts/<lane>/<medium>.md` |
| Something never to say again | `cheese-bank/cheese-bank.md` |

The structure home was added on the first ratification (2026-08-25), when three of nine lessons
turned out to be about beat order and none of the original three homes fit. A but/therefore rule
filed in the voice guide is filed where nobody will look for it.

**A ratified lesson is not automatically a new rule.** On that same run, the lesson Sean cared most
about turned out to already exist in two skills, and the draft had broken it anyway. The honest
routing was to promote the existing rule and record that a self-run gate had missed it, not to add
a duplicate. Check whether the rule already exists before writing one.

Write the ledger entry first, then make the edit, then record the amended file back in the entry.
Ledger-first means a failed edit still leaves a record of what he ratified.

**Rejected candidates stay in the ledger.** A rejection is the more useful of the two records: it
stops the machine proposing the same wrong lesson next week. Deleting rejections means re-learning
them forever.

**Run it on Professional-lane documents too.** His edits to a resume carry the same signal, under
the facts-only form of the law.

## The private brain

Read-only inputs, all git-ignored, all local:

| Path | Read it when |
|---|---|
| `creative-studio/content-machine/corpus/` | Calibrating any claim about how the author writes |
| `creative-studio/content-machine/reference-universe.md` | The piece will use a pop-culture anchor or a personal-history detail. References come from here or from the piece's actual subject. Never invented. |
| `creative-studio/content-machine/cheese-bank/` | Before shipping any Expressive draft |
| `creative-studio/content-machine/coined-lines.md` | Every piece, at the final sweep. The one-artifact rule: a coined line lives in exactly one artifact and is never recycled. |
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
