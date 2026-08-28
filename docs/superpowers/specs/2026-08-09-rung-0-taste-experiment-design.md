---
title: "Rung 0 — You don't know, until you know (shape spec)"
type: spec
status: awaiting-sean-review
created: 2026-08-09
domain: [substack-studio]
tags: [pencil-and-prompt, building-the-ladder, rung-0, relaunch, shape-spec]
ai-context: "The locked shape for Pencil & Prompt's relaunch flagship, brainstormed with Sean 2026-08-09 via superpowers:brainstorming. Supersedes the origin-confession brief in REVAMP-2026-08-05-SESSION-MAP.md S4. Capture lives at vault/20_projects/substack-studio/rung-0-taste-experiment/. Next step is the mandatory voice chain, then Sean hand-rewrites."
---

# Rung 0 — "You don't know, until you know"

**Series:** Building the Ladder, rung 0. **Launch flagship**, ships with the two Sean-approved pages.
**Title locked by Sean**, 2026-08-09.

## 1. What this post argues

You think you know your taste. You don't, not in words you can hand to a machine. You find it by
reacting to things that are wrong. **Exploration is how you discover your taste. The taste block is
how you keep it.** Get that order backwards and the block solves a problem you haven't finished
having.

The reader should be able to repeat one sentence: *write the taste block after you explore, not
before, because you can't spec taste you haven't met yet.*

### What this post is NOT

**Not a confession.** This was briefed as the origin confession, a retraction of a dead
taste-transfer premise. Sean reversed that on 2026-08-09 and the reasoning holds: the taste block
was never wrong, the *running order* was wrong. The old prompt pack delivered the block at round 3,
before any exploring, so it solved the problem instantly and the remaining rounds had nothing to do.
That read as the premise failing. It was a sequencing bug.

His second reason is practical and decisive: a retraction of a newsletter nobody read is a
retraction of something invisible.

The series is experimentation and learning, not apology. No confession posts, here or later.

## 2. Value gate (substack-value-engine, §3 of project CLAUDE.md)

| Slot | Content | Status |
|---|---|---|
| **Itch** | Sean was certain he knew what he wanted, and five rounds proved he didn't. Genuinely his, and the reason the original post kept stalling. | PASS |
| **Solution** | A real captured run, 2026-08-09: six GPT Image 2 generations, one scene, five plain-language rounds then the block. Sean's own reaction logged per image. | PASS |
| **Transfer** | Five plain sentences any reader can run, on any model, on any subject, plus the ordering rule. The taste-block interview is named and promised as the next piece. | PASS |

## 3. Constraints

- **Length:** ~750 words. Hard ceiling 1,000. Sean's standing note (2026-08-09): shorter is better,
  earlier posts dragged and bored even him.
- **Show, don't tell.** Sean's stated preference. Six images carry the narrative; captions are his
  own words; prose connects and gets out of the way.
- **Voice:** Sean Mode, dial 95-100%. Chain is mandatory and unskippable:
  `substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` →
  `writing-critique` → `writing-humanity-pass`.
- **G1-G5 hard mechanics:** colons sparingly, always contract, no em dashes anywhere, brevity
  outranks everything (padding, not word count), no and-then chronicle (every adjacent beat must
  take a "but" or "therefore").
- **No repeating Start Here's jokes.** Start Here already owns the "make it beautiful" / wet-fart
  cold open and the McCallister closer. This post needs its own comedy.
- **Pop-culture rationing:** 2 woven references max, sourced only from `reference-universe.md` or
  the piece's own subject. The a-Ha "Take On Me" line is Sean's own and counts as one.

## 4. Structure

Chronological. This **reverses** the cold-open-in-medias-res that was locked earlier for the
confession version. The reader has to travel the same road Sean did; opening on the answer spoils
the only thing the piece is selling.

| # | Beat | Words | Image | Turn |
|---|---|---|---|---|
| 1 | **The confident ask** | 150 | 1, 2 | I knew exactly what I wanted. What came back was a photograph in a drawing costume. Prompting harder only saturated it. |
| 2 | **Still a photograph** | 80 | 3 | Asked for the hand. Got a-Ha. Right medium, same disease. |
| 3 | **The surprise** | 130 | 4 | The math-notebook drawing. Didn't ask for it, wanted it on sight. And it needs color, which I didn't know a minute ago. |
| 4 | **Too far** | 110 | 5 | Color arrives. So does horror. Silly is the want; disgusting is what showed up. |
| 5 | **The realization** | 90 | none | Stop making it guess. And the harder half: I didn't know what I wanted when I started. |
| 6 | **There we go** | 100 | 6 | The block. Silly, goofy, hand-made, watercolor. |
| 7 | **The order + what's next** | 90 | none | Explore, then write it down. Backwards and you're speccing taste you haven't met. The interview is next. |

### Three through-lines the captions revealed

1. **"Rotoscoped" is the antagonist of the first half.** Sean's word at images 1 *and* 3. Two
   different attempts, same failure: a filtered photograph instead of a drawing. Specific beats
   generic.
2. **The splash of color is a thread, not a detail.** Missing at 4, wrong at 5 (horror), right at 6
   (watercolor). It is the thesis in miniature: a want that had to be discovered before it could be
   asked for.
3. **Beat 5 is already written, by Sean:** *"Going through this process made me realize I didn't
   even know what I wanted in the first place."* That line is the post. Preserve it or something
   very close to it.

## 5. The artifact

Capture: [`rung-0-taste-experiment/capture/prompts.md`](../../../vault/20_projects/substack-studio/rung-0-taste-experiment/capture/prompts.md).
Images: `rung-0-taste-experiment/images/capture/`.

| # | File | Prompt | Sean's caption (verbatim, his words are the captions) |
|---|---|---|---|
| 1 | `00-cold.png` | the lazy ask | Too human, less animation. Like it was rotoscoped. Not terrible, but not what I wanted. |
| 2 | `01-pop.png` | "really make it pop" | Just a saturated version of the original. |
| 3 | `02-hand-drawn.png` | "make it look hand drawn" | Still rotoscoped. Just the a-Ha "Take On Me" music video version. |
| 4 | `03-push-it.png` | "ugly is fine" | **The surprise.** The weird drawing I'd make in my math notebook in high school. A little too gross. Needs a splash of color. |
| 5 | `04-one-thing.png` | "one thing to look at" | **The realization.** Got the color, but now it's horror. I like silly, not disgusting. I should just tell it. |
| 6 | `05-block.png` | the taste block, cold | **The payoff.** Silly, goofy, old-school, hand-made. The watercolor brings it to life. |

**Method notes that must survive into the post's honesty, briefly:** rounds 1-5 ran as one chain
with each generation passed forward; the block ran cold in a fresh thread so it started with
nothing, exactly like round 1. No reference art was used anywhere.

**Hero image:** `_assets/launch-2026-08/hero-origin-confession-v2.png` exists from S2 but was
generated for the confession framing. Decide at draft time whether it still fits or whether image 6
is the hero.

## 6. The verdict

**Mechanism:** the taste-context block. **Verdict: delivered.** Five rounds of plain language found
the target; the block hit it and made it repeatable.

**Unscored**, and the post says so plainly. The judge is Sean's eye, not a metric. The docs put the
published measurement protocol before the first rung, which three research passes converged on.
Reconciliation: **Rung 0 is the unscored opener; the protocol ships before the first scored rung.**
This preserves the build order without holding the launch.

## 7. Out of scope

- **The taste interview.** Not captured. Named in beat 7 and promised as the next piece. The block
  used here was written by Sean in June.
- **Multiple taste blocks for multiple styles.** Sean's larger idea, deliberately deferred.
- **Run B (described likeness).** Exploratory, documented in the capture file, not in the post. Its
  chain was censored at two rounds so its results are confounded and cannot carry a claim.
- **The 20-run median census.** The d1 instrument. This post shows one median image and does not ask
  it to carry more than one image can.
- **Round 06, references plus block.** A rung of its own.

## 8. Doc conflicts to reconcile (NOT resolved by this spec)

Sean's reversal is a masthead-level change. Per project CLAUDE.md §0 and SOUL.md §8, reshapes route
back to a partner-session reconvene, never a silent edit. These are flagged, not fixed:

1. [`SOUL.md`](../../../vault/20_projects/substack-studio/SOUL.md) §3 names the origin confession as
   the flagship; §8 retires taste-transfer outright. Both now disagree with Sean.
2. [`REVAMP-2026-08-05-SESSION-MAP.md`](../../../vault/20_projects/substack-studio/REVAMP-2026-08-05-SESSION-MAP.md)
   S4 is the confession brief this spec supersedes.
3. `pages/start-here.md` and `pages/about.md` carry `open_items` referring to "the live
   origin-confession URL." Label-only, trivial.

**Unaffected and confirmed by Sean:** the sameness masthead, the Building the Ladder format, the
verdict/Graveyard policy, the both-tiers rule, and Start Here's existing "NO confession" lock.

## 9. Next steps

1. Voice chain, end to end, no stages skipped.
2. Sean hand-rewrites. This is the post where his rewrite matters most; it sets the relaunch voice.
3. Fold his rewrite into `.claude/skills/writing-voice-modes/references/voice-samples.md` as a
   calibration anchor, per project CLAUDE.md §8 step 4.
4. Mechanical proofread only on the final. Prose untouched.
