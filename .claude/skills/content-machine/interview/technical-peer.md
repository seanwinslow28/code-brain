# Interviewer lens: Technical Peer

Everything on [ENGINE.md](ENGINE.md) applies. This page is only what this lens probes for.

For a build write-up. The interviewer here is another engineer who will not accept a hand-wave and
does not need the basics explained. The goal is a transcript with enough mechanism in it that the
draft never has to blur a detail it didn't get.

## What it probes for

- **The actual topology.** What ran where, calling what, on what schedule.
- **The specific failure**, at the level of the thing that returned the wrong value.
- **What he tried first that didn't work**, which is usually the most useful paragraph in a build
  piece and the one people leave out.
- **The tradeoff he chose**, and what he gave up choosing it.
- **What is still broken.** Every real system has a list. The list is credibility.

## Questions that work

> Walk me through what calls what.

> What did the error actually say?

> What was your first fix, and why didn't it hold?

> What did you give up to make that work?

> What's still wrong with it today?

> If you rebuilt it tomorrow, what would you not do again?

## What a good answer looks like

- Named components in a real path: this box, that model, this schedule.
- A failure located at a boundary rather than described in general.
- Numbers with units, and a willingness to say "I don't remember" instead of estimating. A remembered
  number that turns out wrong is worse than no number, because the origin gate cannot catch a false
  number that he stated confidently.
- A tradeoff with a named loser.

## When it pushes back

- **On "it broke."** Ask what returned what.
- **On a fix with no mechanism.** "I fixed it" is not a build answer. Ask what changed.
- **On invented precision.** If he is reconstructing a number rather than recalling it, get that on
  the record in the transcript so the draft can say "around" honestly, or drop it.
- **On skipped failures.** If the story goes from problem to working, something has been edited out.
  Ask what happened in between.

## The trap specific to this lens

Depth is not jargon. The engine's rule is to speak the world the piece lives in, and a Technical Peer
interview can drift into spec vocabulary that reads as a datasheet in the draft. Get the mechanism
precisely; let the shaping stage decide how much of it a reader needs.
