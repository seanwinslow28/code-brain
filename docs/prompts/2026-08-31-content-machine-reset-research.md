# Content machine: research pause and rules-off experiment

Continuation prompt for a fresh session. Written 2026-08-31 after three runs through the machine.
Read this whole file before touching anything.

---

## The one-line diagnosis

**The machine has the same defect as the thing it was writing about.**

Run #3's piece was about a vault synthesizer that summarized Sean's notes instead of expanding
them. Sean's verdict on the draft the machine produced:

> "You're essentially just having the issue that the vault synthesizer had. You're summarizing and
> re-reading my brain dump notes back to me."

And the mechanism, in his words:

> "The problem is that I'm doing a brain dump and you're organizing the brain dump, but not doing
> an actual re-write. You're just taking the same words I had just word vomited and separated the
> paragraphs. A writer does that to get things out of his brain and on to the page. Then they start
> making it more interesting and molding it to feel more coherent and add their style to it.
> You're not adding any style to it at all."

His summary of three rounds: *"I've given you piles of writing samples and I'm still reading your
outputs and feel like an alien is trying to learn how to write English by taking the brain dump I
gave it and giving it back to me in a somewhat structured brain dump."*

**Do not open this session by defending the machine.** The verdict is his and it stands.

---

## What he asked for, verbatim

> "We need to take a step back and do research... Please provide me with a continuation prompt that
> I can bring into a fresh session that will have us do the research, look at Liebermans approach,
> remove all of the rules, keep my writing samples, and try to go down a path that leads to better
> output."

Four parts: **research**, **re-examine Lieberman**, **remove the rules**, **keep the samples**.

---

## His hypothesis, which is the thing to test

> "We took the laws from my previous writing skill and then added them to this one. I think that
> might be part of the problem. We ended up taking Lieberman's approach, but mixed it with the
> approach I took last time by adding a bunch of restrictions and making you think too hard about
> what NOT to do. We should consider taking the laws away completely and just using a topic and my
> writing samples to see what another session can come up with."

The claim: the machine is a hybrid of Lieberman's interview-first pattern and a large
prohibition layer inherited from the old `writing-voice-modes`, and the prohibition layer is what
produces flat output.

**Suggestive evidence, stated honestly as suggestive and not proof.** Sentence survival through
his hand-rewrite, across three runs, as the rule count grew:

| Run | What was in place | Survival |
|---|---|---|
| Ep. 1, walking skeleton | interview + origin gate + chain | **64%** (38 of 59) |
| Run #2 | + wave-1 contracts, licensing matrix, five gate amendments | **25%** (14 of 57) |
| Run #3 | + hardened structure stage, dictation, beat-map checkpoint | **38%** (14 of 37) |

**The confounds are real and must not be waved away.** Different topics, different lenses, ep. 1
was typed and run #3 dictated, different piece lengths, and the denominators differ. This table is
a reason to run the experiment, not a result.

---

## The research brief

### 1. Re-read Lieberman, looking for one specific thing

Two transcripts at `vault/20_projects/prj-job-hunt-2026-REVAMP/docs/alex-lieberman/`.

**The lead worth chasing first.** Lieberman describes his machine's job as taking the words
you gave it and *"not change your words but just make sure your words flow, that they transition
well, and that you have an editor who's checking what you've said, **to add in places where you
need to provide more context because you didn't share it with your initial thoughts** or where you
need to make other tweaks."*

**His machine ADDS. Ours forbids adding.** Our L2 constitution says any image, joke, metaphor,
number, name or claim the author did not say is forbidden. If Lieberman's editor layer is
permitted to add context and ours is not, that is the misinterpretation Sean suspects, and it is
checkable against the source. Chase this before anything else.

Also re-check: the six interviewer personas, the writer's council, the lessons loop, and what
his voice/style-guide files actually contain versus what ours do.

### 2. Dig through GitHub for how other people build AI writing systems

Sean asked for this specifically: *"We have to dig through Github to find good writing skills and
do research on how others construct their AI writing set up."*

Questions worth answering: do they use prohibition lists or exemplars? Do they show the model
finished writing and ask for imitation, or give rules and ask for compliance? Where does style
live — in instructions, in samples, in few-shot examples? What does anyone do about the
brain-dump-to-prose gap?

### 3. Craft research on structure and grammar

He asked for it and did not narrow it: *"I think another thing we have to do is look at different
structures and proper grammar. Or something."* Read this as: the drafts read as competently
assembled and stylistically dead, and he wants to know what the missing craft layer is called.

There is already one research note in the vault from 2026-08-28 on hooks, in-medias-res, the
through-line and scene-vs-summary:
`vault/20_projects/research/2026-08-28-story-hooks-and-narrative-through-line.md`. It is
evidence-tagged and has a `[science]/[craft]/[lore]` floor. **Extend it; do not redo it.**

### 4. The question the research should actually answer

Not "what are the rules of good writing." It is: **what does a human writer do between the brain
dump and the finished piece, and which of those operations is the machine structurally forbidden
from performing?**

---

## The experiment

**Strip the rules. Keep the samples. One topic. Measure against run #3.**

Concretely: a session that has the corpus and the voice samples and a transcript, and does NOT
have the origin law, the 36-move roster, the anti-pattern table, the licensing matrix, the medium
contract, or the gate chain. Draft the same piece or a fresh one. Compare.

**This is a real experiment, so let it be able to fail.** Two ways it can:

- The rules-off draft invents things Sean never said and never would say, and the origin law turns
  out to have been load-bearing. The gates caught real fabrications in runs #2 and #3 — an invented
  claim that his writing "needed fixing", a contradicted claim that three months were wasted, a
  nightly schedule he never stated. Removing the law removes that too.
- The rules-off draft is *also* flat, which would mean the prohibition layer was never the cause
  and the problem is somewhere else entirely.

**The measurable outcome is his hand-rewrite survival rate**, on the same instrument used three
times now (`.claude/skills/content-machine/lessons/diff_pieces.py`). Above 64% beats the best the
machine has done. Below 38% and the hypothesis is in trouble.

---

## Calibration already measured — do not re-derive

**Sean's target rhythm**, from two independent hand-rewrites:

| | mean | median | <=6 words | >=35 words |
|---|---|---|---|---|
| His rewrite, run #2 | 16.9 | 14 | 10% | 4% |
| His rewrite, run #3 | 16.6 | 13 | 16% | 9% |
| Machine draft, run #2 | 12.8 | 11 | 29% | 2% |
| Machine draft, run #3 | 21.1 | 17 | 17% | 17% |

The machine overshot in both directions. His rewrites land in the same place twice. His own
*speech* runs `[1, 7, 65, 12, 5, 56, 9, ...]` — long accumulating runs punctuated by very short
punches, both registers alternating. The machine keeps collapsing to one.

**Dictation (#197), measured:** 145 words per answer against 59 typed, from five fewer questions.
It works. **Its measured cost:** his dictated speech scores MATTR 0.733 against his written prose
at 0.843. Speech is lexically narrower than prose.

**A live conflict between two of the machine's own rules.** The `writing-critique` analyzer gates
MATTR at 0.807, calibrated on his finished prose. A draft restricted to a dictated transcript
starts near 0.733 and cannot reach 0.807 without inventing, which the origin law forbids. **The
analyzer currently asks for something the constitution prohibits.** Unresolved. If the law goes,
this conflict goes with it; if the law stays, the gate needs a transcript-relative floor.

---

## What must not be lost

- **The corpus.** `creative-studio/content-machine/corpus/` — 9,804 provenance-audited verbatim
  words, plus 44,928 words of pre-AI screenplay registered as a pointer vein. Git-ignored. This is
  the irreplaceable asset and the "keep my writing samples" half of the instruction.
- **`voice-samples.md`** in `.claude/skills/writing-voice-modes/references/` — the calibration
  authority, which the skill's own text says outranks its rules. Includes his full hand-rewrite of
  the Start Here page (PRIME ANCHOR) and the edit-diffs behind G1-G5.
- **Three transcripts and three hand-rewrites**, in `creative-studio/content-machine/transcripts/`
  and `vault/20_projects/substack-studio/{author-modes-deleted,what-are-these-guys-doing}/`.
  Draft-and-final pairs are the highest-signal calibration data in the project.
- **The ledger.** `creative-studio/content-machine/ledger/lessons.md` holds every ratified reason
  from three rounds, including run #3's, which are recorded and deliberately unrouted.
- **`do-not-promote.md`** and the privacy law (CLAUDE.md rule 9). These are not style rules and do
  not come off in the experiment.

---

## Things that are true and that a fresh session will be tempted to get wrong

- **The interview is not the problem.** Dictation fixed the thin-answer problem measurably. The
  material coming out of Sean is good. The failure is downstream, at the shaping.
- **The ASK LIST premise is partly false.** Sean, on the two best images in his run #3 rewrite:
  *"you asking me what the vault looked like wouldn't have had what I wrote down. That only came to
  me while I was making the re-write"* and *"this probably wouldn't come out in the interview. It
  would come from my own writing samples."* **Some material cannot be interviewed out of him.** It
  arrives at the writing. A machine forbidden to write cannot reach it.
- **"Remove the rules" and "keep the samples" are in tension, and that tension is the experiment.**
  The rules were derived FROM the samples. Removing the rules while keeping the samples means
  trusting the model to *induce* the voice from exemplars rather than *comply* with instructions.
  That is a real and interesting question about how style transfers, and it is worth naming as the
  actual subject of the test.
- **He is not asking to abandon the machine.** He is asking to find out whether one layer of it is
  hurting. Everything else — the Oracle, dictation, the beat-map checkpoint, the lessons loop —
  measured well and stays.

---

## Suggested order

1. Read this file, the three draft/final pairs, and the ledger. Do not re-derive the measurements.
2. Research, in the order above. Lieberman's add-vs-forbid question first, because it is the
   cheapest and most likely to be decisive.
3. Report findings to Sean before building anything. He has been handed three drafts he had to
   rewrite; do not hand him a fourth on a hunch.
4. Design the rules-off experiment with him, run it, measure survival on the same instrument.

---

## State as of this prompt

- Build map: [#158](https://github.com/seanwinslow28/code-brain/issues/158). Open tickets: #171
  (wave-2 contracts), #172 (wave-3), #197 (dictation, measured and working), #198 (beat-map
  checkpoint, measured and working).
- Last commits: `712b4430` (run #3 draft), `973e5570` (hardened structure stage).
- Nothing from run #3 has been routed into any skill file. The machine is exactly as it was when
  run #3 was drafted.
- The Substack launch order is unchanged and none of these pieces is the first post. See
  `vault/20_projects/substack-studio/SERIES-COMMAND-CENTER.md`.
