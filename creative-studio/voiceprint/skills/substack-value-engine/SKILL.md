---
name: substack-value-engine
description: >
  The gate that makes a post worth reading and worth coming back for. Enforces that
  every piece solves a real problem the author actually had, then hands the reader a
  concrete, usable solution. Owns the Value Gate (Itch / Solution / Transfer), the
  narrative-to-value seam, Rule-of-One, over-deliver-on-a-narrow-promise, and
  scratch-your-own-itch sourcing. Use when asked to "is this worth posting", "what's
  the takeaway", "make this useful", "does this solve a real problem", "check the
  value", or as the second stage of the writing chain (after storytelling-
  architecture, before your voice skill and writing-humanity-pass).
version: 0.1.0
---

# Substack Value Engine

## Purpose

Make sure a post is a gift, not filler. The story (owned by
`storytelling-architecture`) is the hook; this skill owns the payoff: the real
problem solved and the value handed to the reader. The source thesis: *the #1 metric
is building a library of things YOU genuinely found valuable; every post solves a real
problem you actually had; content for content's sake is the failure mode.*

This skill operates on the **beat map** from `storytelling-architecture` (in-context).
It annotates that map with the value gate and the narrative-to-value seam. It does
**not** write prose and does **not** reorder beats.

## The Value Gate (the core primitive, a HARD gate)

A post may not proceed unless it names all three slots. If any is empty or vague,
**block the piece and say why.**

1. **Itch**: the specific, real, first-person problem the author actually had. Must be
   concrete enough to be checkable (a named tool, a dated incident, a real cost). No
   genuine itch → kill the piece; it's content for content's sake.
2. **Solution**: what the author actually did about it. Must include at least one
   artifact the reader can see: a run, a number, a commit, a screenshot, a failed
   attempt.
3. **Transfer**: one sentence: *"After reading this, the reader can now ___."* Vague
   Transfer ("understand X better") fails. It must be a concrete capability gained.

Output the verdict explicitly: PASS (three slots filled) or BLOCK (missing slot
named). A draft that started from "what's trending" almost always fails the Itch slot
— that is the gate working.

## The Narrative-to-Value Seam

The highest-craft moment. After the story crests, the instruction must read as
*finishing the story*, not interrupting it.

1. The hook is a half-told problem; the loop stays open through the struggle.
2. At the crest, land ONE explicit declarative **pivot line** that names the lesson.
   (This skill marks WHERE it lands and WHAT it asserts; the voice layer writes it.)
3. The how-to is delivered as the *fulfillment of the hook*, not a topic change.

Anti-pattern: a clean essay that stops, then a bolted-on "Here are 5 tips."

## The Four Supporting Rules

1. **Rule of One.** One idea, one reader, one promise, one CTA. The hook makes a
   promise; the body over-delivers on *exactly that* and nothing else.
2. **Over-deliver on a narrow promise.** Earn trust with surplus on a *tight* surface.
   A copy-pasteable artifact, a real number, a named example. Gate: *"one thing the
   reader can use in the next 10 minutes?"* Depth-on-one beats a survey of ten.
3. **Scratch-your-own-itch sourcing.** Topics come from a running log of things that
   irritated or cost the author. Reject topics sourced from "what would rank / what's
   trending." The first-person real itch IS the anti-slop guardrail.
4. **Brevity is the growth loop; cadence is the trust asset.** Default to the
   shortest form that keeps the promise (short reads get forwarded). Pair with a
   predictable cadence; consistency beats intensity.

## Credibility Without Pitching

When a piece doubles as a reputation signal (job hunt, building an audience, landing
clients), the signal is **shown, never claimed.**

- **Narrate one real decision, not a list of accomplishments.** Center a specific
  choice, the tradeoffs weighed, what you'd do differently. Judgment is shown by
  reasoning. Test: strip every self-describing adjective; if the decision-reasoning
  still proves competence, it works. If removing the adjectives empties the piece,
  it's resume-speak.
- **Artifact + blameless self-post-mortem = the signal.** Link the run, the number,
  the failed attempt. A blameless post-mortem on your *own* work (focused on the
  system/decision, not self-flagellation) is the highest-leverage seniority signal a
  writer has.
- **Any ask — and any sensitive personal fact — lands sideways, and the piece ends on
  the work or the lesson.** Sensitive facts the writer would rather not foreground
  (see the writer's Off-limits list in their voice skill) stay out by default;
  they are never used as backstory, stakes, or a sympathy beat. A direct ask appears
  at most once, mid-body, phrased as a fact about the *work*, never as a closer or a
  CTA. If the last sentence makes the reader feel they should *do* something for the
  author, rewrite it. Confidence is shown by not needing to ask. (This defers to the
  "Desperation Posing as Self-Deprecation" idea in the writer's own voice skill.)

## The Chain Contract (what this skill must NOT do)

```
storytelling-architecture → substack-value-engine → [your voice skill] → writing-critique → writing-humanity-pass
```

- Run the Value Gate, mark the seam, annotate the beat map. Do **not** write prose;
  do **not** reorder beats.
- If the gate BLOCKS, the chain stops here. A well-voiced piece that solves nothing is
  the worst outcome (polished slop).
- On PASS, hand the annotated beat map to the voice layer.

## References

- `references/value-and-signal.md`: the source thesis in full, cited sources for the
  Value Gate / seam / Rule-of-One / credibility mechanics, and worked PASS/BLOCK
  examples.

## Success Criteria

- [ ] Value Gate verdict explicit: PASS (3 slots) or BLOCK (missing slot named).
- [ ] Itch is real, first-person, checkable; no content-for-content's-sake passes.
- [ ] Transfer is one concrete sentence, not vague.
- [ ] The seam reads as fulfilling the hook, not a bolted-on appendix.
- [ ] Rule of One holds; the over-deliver test passes.
- [ ] Credibility is shown via artifact + decision reasoning, never claimed.
- [ ] The ask stays sideways; the piece ends on work or lesson.
- [ ] No prose written; no beats reordered.
