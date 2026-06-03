---
name: substack-value-engine
description: The gate that makes a post worth reading and worth coming back for. Enforces that every piece solves a real problem the author actually had, then hands the reader a concrete, usable solution. Owns the Value Gate (Itch / Solution / Transfer), the narrative-to-value seam, Rule-of-One, over-deliver-on-a-narrow-promise, scratch-your-own-itch sourcing, and hiring-signal-without-pitching. Use when asked to "is this worth posting", "what's the takeaway", "make this useful", "does this solve a real problem", "check the value", "add the so-can-you", "will this land with recruiters", or as the second stage of the Substack chain (after storytelling-architecture, before writing-voice-modes and writing-humanity-pass). Blocks content-for-content's-sake.
---

# Substack Value Engine

## Purpose

Make sure a post is a gift, not filler. The story (owned by `storytelling-architecture`) is the hook; this skill owns the payoff: the real problem solved and the value handed to the reader. It encodes the source thesis directly: *the #1 metric is building a library of things YOU genuinely found valuable; every post solves a real problem you actually had; content for content's sake is the failure mode.*

This skill operates on the **beat map** from `storytelling-architecture` (in-context, not a file). It annotates that map with the value gate and the narrative-to-value seam. It does **not** write prose and does **not** reorder beats. The voice layer writes sentences next.

## When to Use

- Second stage of the Substack chain, after the beat map exists, before `writing-voice-modes`.
- "Is this worth posting?", "what's the takeaway?", "make this useful", "does this solve a real problem?", "add the so-can-you", "will this land with recruiters?".
- Triaging an idea backlog: which itches are real enough to become posts.
- Gating an agent-drafted post (e.g. Substack-Drafter) before it ships.

## The Value Gate (the core primitive, a HARD gate)

A post may not proceed unless it names all three slots. If any slot is empty or vague, **block the piece and say why**. This is the anti-slop enforcement.

1. **Itch**: the specific, real, first-person problem the author actually had. Must be concrete enough to be checkable (a named tool, a dated incident, a real cost). If you cannot name a genuine itch, kill the piece: it is content for content's sake.
2. **Solution**: what the author actually did about it (the narrative payoff and the teaching). Must include at least one artifact the reader can see: a run, an eval, a number, a commit, a failed attempt.
3. **Transfer**: one sentence: *"After reading this, the reader can now ___."* If the Transfer is vague ("understand AI better"), the piece fails. It must be a concrete capability the reader gains.

Output the gate verdict explicitly: PASS (with the three slots filled) or BLOCK (with the missing slot named). A draft that started from "what's trending" or "I should post something" almost always fails the Itch slot, and that is the gate working.

## The Narrative-to-Value Seam

The single highest-craft moment. After the story crests (the beat map's turn/payoff), the instruction must read as *finishing the story*, not interrupting it. Spec:

1. The story's hook is a half-told problem. The loop stays open through the struggle.
2. At the crest, land ONE explicit declarative **pivot line** that names the lesson. (This skill marks WHERE the pivot lands and WHAT it must assert; the voice layer writes the actual sentence.)
3. The how-to is delivered as the *fulfillment of the hook*, the closing of the loop, not a topic change. The reader should feel the value section answers the question the story raised.

Anti-pattern: a clean essay that stops, then a bolted-on "Here are 5 tips." The teaching must be the payoff of the specific story, not a generic appendix.

## The Four Supporting Rules

1. **Rule of One.** One idea, one reader, one promise, one CTA per piece. The title/hook makes a promise; the body over-delivers on *exactly that* and nothing else. Scope-creep is a broken promise. Test: state the promise in one sentence; does every section serve it?

2. **Over-deliver on a narrow promise.** Earn trust with surplus on a *tight* surface, never breadth-for-coverage. A copy-pasteable artifact (a prompt, a checklist, a command), a real number, a named example. Gate: *"Does this contain one thing the reader can use in the next 10 minutes?"* Depth-on-one-thing beats a survey of ten.

3. **Scratch-your-own-itch sourcing.** Topics come from a running log of things that irritated or cost the author, problems actually solved, things found valuable. Reject any topic sourced from "what would rank / what's trending / what the audience wants to hear" (the audience-chasing failure mode). The first-person, real, specific itch IS the structural anti-AI-slop guardrail: a generic draft with no lived itch cannot fill the Itch slot.

4. **Brevity is the growth loop; cadence is the trust asset.** Default to the shortest form that keeps the promise (short reads get forwarded, and the forward is the growth loop). Pair with a predictable cadence: showing up reliably is itself a retention asset, independent of any single piece. Consistency beats intensity.

## Hiring Signal Without Pitching

For Sean's job-hunt context. The signal is shown, never claimed.

- **Narrate one real decision, not a list of accomplishments.** Center a specific choice, the tradeoffs weighed, what you'd do differently. Judgment is shown by reasoning. Test: strip every self-describing adjective; if the decision-reasoning still proves competence, it works. If removing the adjectives empties the piece, it is resume-speak.
- **Artifact + blameless self-post-mortem = the signal.** Link the run, the eval, the cost number, the failed attempt. A blameless post-mortem on your *own* work (focused on the system/decision, not self-flagellation) is the highest-leverage seniority signal available to a writer.
- **AI-PM substance:** lead with evals, cost discipline (draft-before-pro, cheaper-model routing), agentic shipping, and verified skepticism, as the *substance* of the story, never as bragging. These are the rare, differentiating signals in 2026.
- **The ask lands sideways.** Job-hunt context appears at most ONCE, mid-body, as a fact in passing ("...which I rebuilt after the layoff freed up the time"). Never as the closer, a standalone line, or a CTA. The piece ends on the **work or the lesson**. If the last sentence makes the reader feel they should *do* something for you, rewrite it. Confidence is shown by not needing to ask. (This reinforces, and defers to, the "Desperation Posing as Self-Deprecation" anti-pattern in `writing-voice-modes`.)

## The Chain Contract (what this skill must NOT do)

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- This skill runs the Value Gate, marks the seam, and annotates the beat map with Itch/Solution/Transfer and where the artifact/payoff/sideways-ask land. It does **not** write prose and does **not** reorder beats.
- If the Value Gate BLOCKS, the chain stops here. Do not pass a failing piece downstream to be dressed up in good voice. A well-voiced piece that solves nothing is the worst outcome (polished slop).
- On PASS, hand the annotated beat map to `writing-voice-modes`, which writes every sentence fresh.

Handoff is in-context, not a saved file.

## Related Skills

- `storytelling-architecture`: the prior stage. Produces the beat map this skill gates and annotates. Story makes them read; this makes it worth their time.
- `writing-voice-modes`: writes every sentence against the annotated beat map. This skill decides the pivot line's job; voice writes the line. Owns the "Desperation Posing as Self-Deprecation" anti-pattern this skill's sideways-ask rule defers to.
- `writing-critique`: red-teams the voiced draft. It checks whether the Value Gate and hiring signal actually landed (Itch/Solution/Transfer delivered, ask stays sideways) but defers to this skill on the gate itself; it critiques execution, not the verdict.
- `writing-humanity-pass`: the final scrub, runs last.
- `creative-writing`: owns format/length constraints the value gate operates within.

## References

- `references/value-and-signal.md`: the source thesis in full, cited sources for the Value Gate / seam / Rule-of-One / hiring-signal mechanics, the over-deliver and sideways-ask boundaries, and worked PASS/BLOCK examples. Read when a gate verdict is borderline or when calibrating the hiring signal.

## Success Criteria

- [ ] Value Gate verdict is explicit: PASS (3 slots filled) or BLOCK (missing slot named).
- [ ] Itch is real, first-person, and checkable; no content-for-content's-sake passes.
- [ ] Transfer is one concrete sentence ("the reader can now ___"), not vague.
- [ ] The seam is marked: the value reads as fulfilling the hook, not a bolted-on appendix.
- [ ] Rule of One holds; over-deliver test passes (one usable thing in 10 minutes).
- [ ] Hiring signal is shown via artifact + decision reasoning, never claimed.
- [ ] The ask stays sideways; the piece ends on work or lesson, never a request.
- [ ] No prose written; no beats reordered (chain contract honored).

## Copy/Paste Ready

```
"Run the value gate on this idea"
"Is this worth posting, or is it content for content's sake?"
"What's the Transfer? What can the reader do after reading?"
"Mark the narrative-to-value seam"
"Check the hiring signal, keep the ask sideways"
"Triage my idea backlog by real itch"
```
