# Rules-off experiment — session 1 record (2026-08-31)

Design ratified by Sean 2026-08-31 (this session): arms A and B side by side, redrafting
transcript #2 (`deleted-the-author-modes`, the four-authors pivot). Research basis:
[../../research/2026-08-31-content-machine-rules-off-research.md](../../research/2026-08-31-content-machine-rules-off-research.md).
Also ratified and applied the same session: the origin gate moved to **post-draft advisory**
(content-machine SKILL.md amended, dated).

## Setup

Both arms: fresh subagents, same model (session default), identical file context —
transcript #2 + corpus 01–06 + `voice-samples.md` + `reference-universe.md` + `do-not-promote.md`.
NO origin law, no 36-move roster, no anti-pattern table, no licensing matrix, no medium
contract, no gate chain, no lessons. Explicitly barred from reading anything else (including
the run-#2 draft/final, which were verified absent from the corpus and samples — no
contamination of the pre-test).

- **Arm A (rules-off):** "induce the voice entirely from his writing… there are no style rules."
- **Arm B (claims-locked, texture-free):** same, plus one positive rule: facts/numbers/names/events
  from the transcript only; images, jokes, framing, hook, closer are the writer's job.
- **Control:** the original run-#2 machine draft (full rule stack, same transcript) —
  `../author-modes-deleted/draft.md`.

## Instruments ($0, all local)

`diff_pieces.py` (vs Sean's existing run-#2 final), `origin_check.py` (traceability),
`writing-critique` analyzer (rhythm/MATTR), plus a short/long sentence-share pass.
Arize skills judged unnecessary at this scale; revisit if the experiment grows to
multi-run batches.

## Numbers

| | Control (rules-on) | Arm A | Arm B | Sean's final (target) |
|---|---:|---:|---:|---:|
| Sentences | 56 | 60 | 68 | 50 |
| Mean length | 12.9 | 14.0 | 13.4 | 17.3 |
| Median | 11 | 12 | 11 | 15 |
| CV (burstiness) | 0.68 | 0.59 | 0.68 | 0.57 |
| MATTR@50 | 0.843 | 0.855 | 0.860 | 0.843 |
| ≤6-word share | 28.6% | 18.3% | 22.1% | 9.4% (target 10–16%) |
| ≥35-word share | 1.8% | 3.3% | 4.4% | 5.7% (target 4–9%) |
| Sentences matching his final | 14 | 4 | 2 | — |
| Fabricated claims (hand-read) | 0 | 0 | 0 | — |

**Read the match-to-final row with care: it is biased toward the control by construction** —
Sean's final was produced by editing that exact draft, so its surviving sentences ARE control
sentences. It measures anchoring, not quality. The real instrument remains Sean's hand-rewrite
of whichever arm he picks (`diff_pieces.py <arm> <his-rewrite>`); above 64% untouched beats the
machine's best, below 38% and the hypothesis is in trouble.

**Origin/claims read:** the checker's claim flags on both arms are false positives (title verbs;
the OpenAI/ChatGPT fact, which arrived via the interviewer's Q13 and was ruled into the story in
run #2 per L2-09). Neither arm fabricated an event, number, or name. Closest borderline, worth
Sean's eye: Arm B's "For about three months I convinced myself the next tweak would fix it"
attributes an interior state he didn't quite say.

**What changed qualitatively:** both arms did what the three machine drafts never did — invented
texture. Arm A: "The two collided somewhere over the harbor", "You can shrug off a bad output
when it's sitting in a folder. You can't publish one", the Kerouac-back-on-the-shelf closer.
Arm B: "I sat there admiring the bruises", "Quick roster check", "OpenAI needed lawyers to reach
that conclusion. I just needed three months and a fictional set of sisters", the Mom closer.
Both honored the transcript's in-band instructions (the caffeine substitution, the "I have I
have" fix, the CORRECTIONS rewording).

**What didn't change:** both arms still run shorter sentences than Sean's rewrites (mean 13–14
vs his 16.6–17.3) and overuse the ≤6-word punch. Consistent with the research prediction that
rules-off removes the texture/lexis ceiling but does not by itself supply the register repack
(speech→prose clause-packing) — that layer is still owned by nobody in the pipeline.

## Result (2026-08-31 evening)

Sean read both arms, called both "SO much better than what I was getting before," leaned Arm B
(two ear-level flaws found in Arm A: "started… starting" doubling, "sounded like everything"),
and hand-rewrote Arm B (`arm-b-sean-final.md`).

**Survival: 59 of 69 sentences untouched — 86%.** Machine's previous best was 64% (ep. 1);
runs #2 and #3 scored 25% and 38%. Six changes total, catalogued as Run #4 candidates
(L4-01…L4-06, pending) in the gitignored ledger. Two of the six re-import beats from his
run-#2 final — a document the arms were deliberately blinded to for pre-test cleanliness —
so 86% likely *understates* production survival, where prior finals of the same story would be
in context. One change needs his reason before it teaches anything (L4-03, "injected more
rules" → "removed most of the rules" — a timeline change). The new-invention channel showed up
again on his side (the hot-chocolate Mother line exists in no source), re-confirming L3-05.

## Status

- Origin gate: post-draft advisory, applied to the standing machine (ruled and done).
- **RATIFIED AND APPLIED (2026-08-31 evening).** Sean: "Let's make Arm B the standing machine."
  Applied to content-machine SKILL.md (law re-scoped, clean shaping context, mechanical proofread
  added to ship stage at his request), writing-voice-modes SKILL.md (scope note), substack-studio
  CLAUDE.md §1 (chain retired to post-draft advisory), CHANGELOG.md. L4-03 reason recorded (the
  timeline change is deliberate: the piece must not lead readers down the rule-filled path).
  `arm-b-publish-ready.md` carries the proofread final (3 mechanical fixes, prose untouched).
  Still open: scope tags for L4-01/L4-05/L4-06 routing, the unrouted run-#3 entries, and his
  named roadmap — fold/swap writing samples as volume grows, try different models and harnesses
  on the same transcript (the Substack experimentation theme feeds on exactly this).
