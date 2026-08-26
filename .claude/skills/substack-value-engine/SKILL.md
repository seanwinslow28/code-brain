---
name: substack-value-engine
description: The gate that makes a post worth reading and worth coming back for. Enforces that every piece solves a real problem the author actually had, then hands the reader a concrete, usable solution. Owns the Value Gate (Itch / Solution / Transfer), the narrative-to-value seam, Rule-of-One, over-deliver-on-a-narrow-promise, scratch-your-own-itch sourcing, the durability question, and hiring-signal-without-pitching. Use when asked to "is this worth posting", "what's the takeaway", "make this useful", "does this solve a real problem", "check the value", "add the so-can-you", "will this land with recruiters", "will this still be worth reading in a year", or as the second stage of the Substack chain (after storytelling-architecture, before writing-voice-modes and writing-humanity-pass). Blocks content-for-content's-sake.
---

# Substack Value Engine

## Purpose

Make sure a post is a gift, not filler. The story (owned by `storytelling-architecture`) is the hook; this skill owns the payoff: the real problem solved and the value handed to the reader. It encodes the source thesis directly: *the #1 metric is building a library of things YOU genuinely found valuable; every post solves a real problem you actually had; content for content's sake is the failure mode.*

This skill operates on the **beat map** and its **Handoff Block** from `storytelling-architecture` (in-context, not a file). It annotates that map with the value gate and the narrative-to-value seam, attaching to the crest beat and central loop the Handoff Block names rather than re-deriving them. It does **not** write prose and does **not** reorder beats. The voice layer writes sentences next.

## When to Use

- Second stage of the Substack chain, after the beat map exists, before `writing-voice-modes`.
- "Is this worth posting?", "what's the takeaway?", "make this useful", "does this solve a real problem?", "add the so-can-you", "will this land with recruiters?".
- Triaging an idea backlog: which itches are real enough to become posts.
- Gating an agent-drafted post (e.g. Substack-Drafter) before it ships.

## The Value Gate (the core primitive, a HARD gate)

A post may not proceed unless it names all three slots. If any slot is empty or vague, **block the piece and say why**. This is the anti-slop enforcement.

1. **Itch**: the specific, real, first-person problem the author actually had. Must be concrete enough to be checkable (a named tool, a dated incident, a real cost). If you cannot name a genuine itch, kill the piece: it is content for content's sake.
2. **Solution**: what the author actually did about it (the narrative payoff and the teaching). Must include at least one artifact the reader can see: a run, an eval, a number, a commit, a failed attempt.
3. **Transfer**: one sentence: *"After reading this, the reader can now ___."* If the Transfer is vague ("understand AI better"), the piece fails. It must be a concrete capability the reader gains, **delivered by a specific artifact named in the Solution slot**: the reader can now [do X] *using* [the prompt / checklist / command / eval you shipped]. A Transfer that names a capability but no artifact that delivers it is the vague-value pass this gate exists to stop; weld the capability to the copy-pasteable thing, or the slot is not filled.

Output the **Value Gate verdict** explicitly: PASS (with the three slots filled) or BLOCK (with the missing slot named). A draft that started from "what's trending" or "I should post something" almost always fails the Itch slot, and that is the gate working. This named verdict travels forward through the (locked) voice stage: `writing-critique` re-checks the same three slots against the voiced draft (it verifies the slots actually landed; it does not re-run the gate).

On PASS, ask the **durability question** of the Transfer (supporting rule 4) before
locking it. Then **lock the Transfer as the single takeaway** and hand it to the voice stage: one sentence, the capability welded to its delivering artifact, marked as the spine every section serves. Sharpen it until the draft nearly writes itself from it. This locked takeaway is what shapes the draft downstream; a fuzzy takeaway here becomes a fuzzy piece four stages later, when it is far more expensive to fix.

## The Narrative-to-Value Seam

The single highest-craft moment. After the story crests (the beat map's turn/payoff), the instruction must read as *finishing the story*, not interrupting it. Spec:

1. The story's hook is a half-told problem: storytelling's **central loop** from the open-loop ledger. The loop stays open through the struggle.
2. At the **crest beat** storytelling marks in its Handoff Block, land ONE explicit declarative **pivot line** that names the lesson. (This skill marks WHERE the pivot lands and WHAT it must assert; the voice layer writes the actual sentence.) Attach to the crest storytelling handed over; do not re-derive it.
3. The how-to is delivered as the *fulfillment of the hook*, the closing of the **central loop**, not a topic change. The reader should feel the value section answers the question the story raised. The Transfer's artifact is what closes that loop: if closing the central loop and landing the Transfer are not the same beat, the seam is bolted-on.

Anti-pattern: a clean essay that stops, then a bolted-on "Here are 5 tips." The teaching must be the payoff of the specific story, not a generic appendix.

## The Five Supporting Rules

1. **Rule of One (one itch, hard).** One idea, one reader, one promise, one CTA per piece. The title/hook makes a promise; the body over-delivers on *exactly that* and nothing else. Scope-creep is a broken promise. Test: state the promise in one sentence; does every section serve it? **The common failure is three half-itches wearing one title.** If triage surfaces more than one candidate itch, the gate BLOCKS until exactly one survives: pick the realest and cut the rest, or split them into separate posts. Three half-solved problems is three broken promises, not one rich piece; depth on one itch beats coverage of three.

2. **Over-deliver on a narrow promise.** Earn trust with surplus on a *tight* surface, never breadth-for-coverage. A copy-pasteable artifact (a prompt, a checklist, a command), a real number, a named example. Gate: *"Does this contain one thing the reader can use in the next 10 minutes?"* Depth-on-one-thing beats a survey of ten.

3. **Scratch-your-own-itch sourcing.** Topics come from a running log of things that irritated or cost the author, problems actually solved, things found valuable. Reject any topic sourced from "what would rank / what's trending / what the audience wants to hear" (the audience-chasing failure mode). The first-person, real, specific itch IS the structural anti-AI-slop guardrail: a generic draft with no lived itch cannot fill the Itch slot.

4. **Durability: the lesson has to outlive the artifact.** One question, asked of
   the locked Transfer before it locks: *is this still worth reading in a year, or
   does it expire with the news cycle?*

   **This does not block the piece.** A publication built on running experiments
   with this month's tools is *supposed* to be pinned to this month's tools; a
   durability gate on the piece would block the publication's own premise. What
   may not expire is the **Transfer**. If the capability the reader gains dies
   with a model version, a pricing page, or a product release, the Transfer is
   pinned, and the durable capability underneath it has to be named before the
   lock. The question binds the Transfer, not the piece.

   Worked shape. Pinned: *"the reader can cut their image-gen bill using the
   draft-then-pro escalation in gemini-2.9."* Durable underneath: *"the reader can
   cut a generation bill by routing the cheap model first and escalating only on
   the keeper — shown here in gemini-2.9."* Same artifact, same numbers, same
   dated specifics. The capability survives the version.

   Two failure modes, and the second is the sneaky one. **Expiring**: the Transfer
   is a fact about a product that will be false next quarter. **Laundered**: the
   Transfer is rewritten so vague it cannot expire because it never said anything
   ("the reader can think more carefully about cost"). A durable Transfer is
   specific *and* survives the version; buying durability with vagueness fails the
   Transfer slot instead. Never strip the dated specifics to sound timeless — the
   version numbers, prices and dates are the evidence, and they stay.

5. **Brevity is the growth loop; cadence is the trust asset.** Default to the shortest form that keeps the promise (short reads get forwarded, and the forward is the growth loop). Pair with a predictable cadence: showing up reliably is itself a retention asset, independent of any single piece. Consistency beats intensity.

## Hiring Signal Without Pitching

For Sean's job-hunt context. The signal is shown, never claimed.

- **Narrate one real decision, not a list of accomplishments.** Center a specific choice, the tradeoffs weighed, what you'd do differently. Judgment is shown by reasoning. Test: strip every self-describing adjective; if the decision-reasoning still proves competence, it works. If removing the adjectives empties the piece, it is resume-speak.
- **Artifact + blameless self-post-mortem = the signal.** Link the run, the eval, the cost number, the failed attempt. A blameless post-mortem on your *own* work (focused on the system/decision, not self-flagellation) is the highest-leverage seniority signal available to a writer.
- **AI-PM substance:** lead with evals, cost discipline (draft-before-pro, cheaper-model routing), agentic shipping, and verified skepticism, as the *substance* of the story, never as bragging. These are the rare, differentiating signals in 2026.
- **The ask lands sideways, and the layoff is omitted by default.** The layoff / job-loss is **suppressed** (see `writing-voice-modes` Do-Not-Promote Topics): do NOT use it as backstory, stakes, or a sideways aside, even once, unless Sean explicitly asks for it in a specific piece. Job-hunt context more broadly appears at most ONCE, mid-body, as a fact in passing about the *work* ("...which I rebuilt when I had the time"), never the predicament. Never as the closer, a standalone line, or a CTA. The piece ends on the **work or the lesson**. If the last sentence makes the reader feel they should *do* something for you, rewrite it. Confidence is shown by not needing to ask. (This reinforces, and defers to, the "Desperation Posing as Self-Deprecation" anti-pattern in `writing-voice-modes`.)

## The Chain Contract (what this skill must NOT do)

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- This skill runs the Value Gate, marks the seam, and annotates the beat map with Itch/Solution/Transfer and where the artifact/payoff/sideways-ask land. It does **not** write prose and does **not** reorder beats.
- If the Value Gate BLOCKS, the chain stops here. Do not pass a failing piece downstream to be dressed up in good voice. A well-voiced piece that solves nothing is the worst outcome (polished slop).
- On PASS, hand the annotated beat map — plus the **locked single takeaway** and the named **Value Gate verdict** — to `writing-voice-modes`, which writes every sentence fresh against the takeaway. These travel in-context through the voice stage; `writing-critique` consumes the Value Gate verdict downstream.

Handoff is in-context, not a saved file.

## Related Skills

- `storytelling-architecture`: the prior stage. Produces the beat map this skill gates and annotates. Story makes them read; this makes it worth their time.
- `writing-voice-modes`: writes every sentence against the annotated beat map. This skill decides the pivot line's job; voice writes the line. Owns the "Desperation Posing as Self-Deprecation" anti-pattern this skill's sideways-ask rule defers to.
- `writing-critique`: red-teams the voiced draft. It re-checks the named **Value Gate verdict** (Itch/Solution/Transfer delivered, ask stays sideways) against the voiced draft but defers to this skill on the gate itself; it critiques execution, not the verdict.
- `writing-humanity-pass`: the final scrub, runs last.
- `creative-writing`: owns format/length constraints the value gate operates within.

## References

- `references/value-and-signal.md`: the source thesis in full, cited sources for the Value Gate / seam / Rule-of-One / hiring-signal mechanics, the over-deliver and sideways-ask boundaries, and worked PASS/BLOCK examples. Read when a gate verdict is borderline or when calibrating the hiring signal.

## Success Criteria

- [ ] Value Gate verdict is explicit: PASS (3 slots filled) or BLOCK (missing slot named).
- [ ] Itch is real, first-person, and checkable; no content-for-content's-sake passes.
- [ ] Transfer is one concrete sentence welded to a delivering artifact ("the reader can now ___ using ___"), not vague.
- [ ] On PASS, the Transfer is locked as the single takeaway and handed forward as the draft's spine.
- [ ] The seam is marked: the value reads as fulfilling the hook, closing storytelling's central loop, not a bolted-on appendix.
- [ ] The durability question was asked of the Transfer before it locked; a
      Transfer that dies with a version names the durable capability underneath
      it, without laundering into vagueness or stripping the dated evidence.
- [ ] Rule of One holds: exactly one itch survives (multi-itch pieces are blocked or split); over-deliver test passes (one usable thing in 10 minutes).
- [ ] Hiring signal is shown via artifact + decision reasoning, never claimed.
- [ ] The ask stays sideways; the piece ends on work or lesson, never a request.
- [ ] No prose written; no beats reordered (chain contract honored).

## Copy/Paste Ready

```
"Run the value gate on this idea"
"Is this worth posting, or is it content for content's sake?"
"What's the Transfer? What can the reader do after reading?"
"Mark the narrative-to-value seam"
"Will this still be worth reading in a year?"
"Check the hiring signal, keep the ask sideways"
"Triage my idea backlog by real itch"
```
