---
name: storytelling-architecture
description: >
  Story shape that makes someone keep reading. Designs the narrative spine, the beat
  order, the open loops, and the tension arc BEFORE any sentence is written. Outputs
  a beat map (a step-outline), never finished prose. Use when asked to "make this
  addictive", "structure this story", "fix the hook", "why won't people finish this",
  "outline this essay/post", "shape the narrative", "add tension", "this drags", or
  as the first stage of the writing chain (pairs with substack-value-engine, then
  your generated voice skill, then writing-humanity-pass).
version: 0.1.0
---

# Storytelling Architecture

## Purpose

Own the WHAT-order and WHAT-shape of a story so a reader cannot stop. This skill
decides the beat sequence, where loops open and close, and how tension escalates. It
does NOT write sentences. Its output is a **beat map**: a step-outline (one or two
lines per beat saying what happens and how it turns), handed downstream to the voice
layer that writes the actual prose.

The load-bearing rule (McKee/Truby and the LinkedIn-broetry failure): **structure
owns ORDER, voice owns SENTENCES.** If this skill writes finished sentences, its
default phrasing survives into the final draft and flattens the writer's voice. So it
emits beats, never lines.

## The output: a beat map (never prose)

A numbered list of beats. Each beat is one or two plain lines: what happens, how it
turns (the but/therefore), any loop it opens or closes. Mark the hook, the turn, and
the payoff. Example shape (illustrative, not a template to fill):

```
BEAT MAP: working title
1. COLD OPEN [opens loop L1]: drop the reader into the concrete moment of failure.
2. THEREFORE: the stakes — what this failure cost or threatened.
3. BUT: the first fix fails / makes it worse. Escalate. [L1 still open]
4. THEREFORE: the real diagnosis surfaces. The turn.
5. PAYOFF [closes L1]: the fix that worked.
6. SO-CAN-YOU: hand-off point where the value layer's Transfer lands.
```

Write the beats. The voice layer authors every line fresh against this map.

## The six enforced mechanics

Each is a gate. Run the beat map against all six.

1. **But/Therefore beat test.** Between adjacent beats you must be able to insert
   *but* (conflict) or *therefore* (consequence). If only *and then* fits, the seam
   is dead: merge, cut, or add a reversal. Flag additive-only logic.
2. **Cold open / in medias res.** Open on a concrete moment or live tension, never on
   context, definitions, or "In this piece I'll...". The first beat raises ONE
   specific unanswered question.
3. **Open-loop budget.** Every loop opened must close later; in short form, within
   ~1-3 beats or the reader disengages. Track each loop; flag any left open.
4. **Closeable gap, not chasm.** The hook promises a payoff that feels imminent and
   attainable ("the one line that broke the build"), not vast and vague ("the secret
   of great writing").
5. **Withhold the rescue.** Don't resolve the central tension in the first beat and
   then merely explain. Escalate before the payoff.
6. **Slippery-slide section ends.** The last beat of each section creates forward
   pull, not a clean summary that gives the reader permission to stop. (When the voice
   layer realizes this, the natural punctuation is often an em dash — note it as a
   "forward-pull line" and let `writing-humanity-pass` handle the punctuation per the
   writer's preference. Don't pre-solve it.)

## Story scaffolds (pick one, apply as form not formula)

Set beat ORDER; never slots to fill with canonical connective tissue ("and that's
when I realized..."). See `references/story-mechanics.md` for the full set.

- **Problem-Struggle-Fix** (default for maker/technical posts): the real problem, the
  failed attempts, the fix that worked. Maps cleanly onto a post-mortem.
- **Before-After-Bridge**: the painful before, the better after, the bridge (the
  bridge is the value).
- **In-Medias-Res Quest**: cold open mid-crisis, backfill in fragments, resolve.
- **Pixar** (Once / Every day / Until one day / Because / Until finally): for
  arc-heavy personal narratives.

## Anti-formula guard (the seam must stay invisible)

- **Specificity check** (archetype vs stereotype): each beat carries a detail
  specific to THIS story, not a generality any template would produce.
- **Nameable-template check:** if the beat order is the obvious canonical shape with
  nothing bent, vary it (start later, reorder a reveal, fold two beats). The reader
  should *feel* the structure, never name it.

## The chain contract (what this skill must NOT do)

```
storytelling-architecture → substack-value-engine → [your voice skill] → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)     (RED-TEAM)        (scrub)
```

- Emit a beat map. **Never write finished sentences** or specify how a beat is phrased.
- `substack-value-engine` annotates the same map with the value gate. Still not prose.
- **Your generated voice skill** (the one VoicePrint built for you) writes 100% of the
  sentences fresh against the beats, and must never reorder them.
- `writing-humanity-pass` runs last.

Handoff is in-context: the beat map flows to the next stage in the working context.

## References

- `references/story-mechanics.md`: the full mechanic catalog with cited sources, the
  four scaffolds, the evidence floor (science vs craft vs lore), and the Zeigarnik
  honesty note.

## Success Criteria

- [ ] Output is a beat map (step-outline), not prose.
- [ ] Every adjacent beat passes the but/therefore test.
- [ ] Cold open raises one specific question; no throat-clearing.
- [ ] Every opened loop closes; short-form loops close within ~1-3 beats.
- [ ] The hook's gap is closeable; the central tension is withheld then escalated.
- [ ] Each section ends on forward pull, not a summary.
- [ ] Specificity check passes; the template is not nameable.
