---
name: storytelling-architecture
description: Story shape that makes someone keep reading. Designs the narrative spine, the beat order, the open loops, and the tension arc BEFORE any sentence is written. Outputs a beat map (a step-outline), never finished prose. Use when asked to "make this addictive", "structure this story", "fix the hook", "why won't people finish this", "outline this essay/post/case study", "shape the narrative", "add tension", "this drags", or as the first stage of the Substack chain (pairs with substack-value-engine, then writing-voice-modes, then writing-humanity-pass). Reusable for essays, talks, and case studies, not just newsletters.
---

# Storytelling Architecture

## Purpose

Own the WHAT-order and WHAT-shape of a story so a reader cannot stop. This skill decides the beat sequence, where loops open and close, and how tension escalates. It does NOT write sentences. Its output is a **beat map**: a step-outline (one or two lines per beat saying what happens and how it turns), handed downstream to the voice layer that writes the actual prose.

**Terminology, corrected 2026-08-28.** What this skill calls a **beat** is what McKee calls a **scene** — a unit whose value-charge changes end to end. McKee's *beat* is an action/reaction exchange **inside** a scene. The file used to say "McKee-style beat", which made the citation wrong and, worse, hid mechanic 7 from view: if the unit is a scene, then McKee's gate on it is the **turn**, and nothing here was testing for it.

The load-bearing rule (from the research, McKee/Truby/the broetry failure): **structure owns ORDER, voice owns SENTENCES.** If this skill writes finished sentences, its default phrasing survives into the final draft and flattens the writer's voice. So it emits beats, never lines.

## When to Use

- First stage of the Substack chain, before `substack-value-engine` adds the value gate and `writing-voice-modes` writes the prose.
- "Make this addictive", "fix the hook", "why won't people finish this", "this drags", "shape the narrative", "outline this".
- Structuring essays, conference talks, case studies, post-mortems, threads: anywhere a reader needs to be pulled forward.

## The Output: A Beat Map (never prose)

A beat map is a numbered list of beats. Each beat is one or two plain lines: what happens, how it turns (the but/therefore), and any loop it opens or closes. Mark the hook, the turn, and the payoff. Example shape (content is illustrative, not a template to fill):

```
BEAT MAP: working title
1. COLD OPEN [opens loop L1]: drop reader into the concrete moment of failure. Raises the question: why did this break?
2. THEREFORE: the stakes, what this failure cost / threatened.
3. BUT: the first fix fails / makes it worse. Escalate. [L1 still open]
4. THEREFORE: the real diagnosis surfaces. The turn.
5. PAYOFF [closes L1]: the fix that worked.
6. SO-CAN-YOU: hand-off point where value-engine's Transfer lands.
```

Do not write the sentences. Write the beats. The voice layer authors every line fresh against this map.

## The Handoff Block (required — travels with the beat map)

The beat map is stage 1 of a five-stage chain, and its decisions have to survive four stages to the final draft, past the locked voice stage that can only act on what physically arrives in context. A loop or a crest tracked only in your reasoning dies at the voice stage. So every beat map ends with an explicit Handoff Block: emitted text the next stages consume **by name**, never the skill's private notes.

- **Open-loop ledger.** Every loop the map opens, listed with where it opens and where it is scheduled to close: `L1 — opens at beat 1 (why did the build break?) → closes at beat 5`. This is the open-loop budget (mechanic 3) made durable. `writing-critique`, four stages downstream, checks loop closure against this ledger; a loop with no scheduled close is a bug in the map, not a style choice.
- **Central loop.** Which ledger loop is the story's spine: the half-told problem the hook opens and the payoff closes. `substack-value-engine` lands its value payoff on exactly this loop.
- **Crest beat.** The beat where tension peaks and the turn lands. `substack-value-engine` attaches its pivot line here; don't make it re-find the crest.
- **Seam beat.** The beat where value / the Transfer lands (the SO-CAN-YOU beat).
- **The spine, in one sentence.** Gornick's distinction: the **situation** is what happened; the **story** is what the writer has come to say about it. The other four fields are positional coordinates and none of them states this. A map with no spine produces a competent sequence of events that is about nothing, which is the flat-draft failure wearing a different mask. Write it as a sentence, not a topic.
- **Opening stage-set.** Whatever concrete material the opening puts on stage has to recur. The open-loop ledger tracks *questions*; nothing tracked the *props*. An opening that introduces a thing the piece then abandons is a bait-and-switch the reader feels even when every loop closes.

Name all six explicitly. The downstream stages are instructed to consume this block by name; when it is missing they re-derive it by eye and drift, which is the "explicit handoff notes the next stage actually consumes" this skill exists to provide.

## The Eight Enforced Mechanics

Each is a gate. Run the beat map against all eight.

1. **But/Therefore beat test.** Between any two adjacent beats you must be able to insert *but* (conflict) or *therefore* (consequence). If only *and then* fits, the seam is dead: merge the beats, cut one, or add a reversal/consequence. Flag additive-only logic ("Also", "Additionally", "Next", "And then").

2. **Cold open / in medias res.** Two obligations in one opening, and the skill used to gate only the first.

   **(a) The question.** Open on a concrete moment, scene, or live tension. Never on context, definitions, or "In this piece I'll...". The first beat raises ONE specific unanswered question. Throat-clearing openings are a fail.

   **(b) The promise, and orientation.** An opening also signs a contract about what the whole piece will *feel* like — Poe's unity of effect, 1846: *"If his very initial sentence tend not to the outbringing of this effect, then he has failed in his first step."* And it has to orient: who, when, what is happening right now.

   **The dimension asymmetry (the actionable part).** Readers measurably slow at temporal, causal, protagonist and goal discontinuities, and **not** at spatial ones (event-indexing model; Rinck & Weber). So **place is the one thing you can leave vague cheaply. Protagonist, time, causality and goal are not.**

   **The given-new check.** Every referent the opening treats as already-known must actually be known to a cold reader. Anything else forces a *bridging inference* (Clark & Haviland 1977), which costs measurable processing time and eventually fails outright. This is the precise mechanism behind an opening that reads as rambling: the writer holds a complete situation model and packages all of it as given; the reader holds none and bridges on every clause until they quit. Run it literally, referent by referent, on the first beat.

   **In medias res is licensed. Entering after the turn is not.** The enforceable test is not scene-vs-result, it is: **is the reader inside something still happening, or being told about something that already finished?** Vonnegut's "start as close to the end as possible" and enter-late/leave-early both mean late *within an unresolved moment*. A result can open a piece; a *finished* result cannot.

3. **Open-loop budget.** Every loop the map opens must be closed by a later beat. In short form, a loop closes within ~1-3 beats/paragraphs or the reader disengages from frustration. Record each loop in the **open-loop ledger** (emitted in the Handoff Block above), not just in your head; flag any left open at the end. Tracking a loop only in reasoning is the failure mode: it dies at the locked voice stage and `writing-critique` has nothing to check closure against four stages later. (Justify loops by *motivational tension*, not memory. The Zeigarnik "you'll remember it" claim fails replication: see `references/story-mechanics.md`.)

4. **Closeable gap, not chasm.** The hook promises a payoff that feels imminent and attainable ("the one line that broke the build"), not vast and vague ("the secret of great writing"). Flag hooks that promise more than the beats can pay off.

5. **Withhold the rescue.** Don't resolve the central tension in the first beat and then merely explain. Escalate (progressive complication) before the payoff. The opening question must outlive its introduction.

6. **The turn test (inside a beat).** But/therefore tests the seam *between* beats. This tests *inside* one. McKee: if the value-charged condition is unchanged from one end of a scene to the other, nothing meaningful happened — it is a nonevent. **A map of well-connected nonevents passes every but/therefore seam and still reads as "I did this, then this, then this."** That is not a hypothetical; it is the diagnosed failure of the 2026-08-27 draft, whose seams all passed. For each beat, name what is charged at the start and what is charged at the end. Same value → merge it, cut it, or find the turn that is actually in the material.

7. **Scene / summary budget.** Mark every beat SCENE or SUMMARY. Turning points, confrontations and crises must be SCENE. Summary is legitimate and necessary for background, motive, pacing, transitions and time-leaps — this is not a rule against it. **A map that is all SUMMARY is the flat draft; a map that is all SCENE is hooptedoodle.** Per beat, the Le Guin framing is the useful one: is this a moment to *crowd* (slow down, dramatize) or to *leap* (compress, move)?

8. **Slippery-slide section ends.** The last beat of each section creates forward pull (a teased turn, a withheld answer), not a clean summary that gives the reader permission to stop. (When the voice layer realizes this, the natural punctuation is an em dash, which is banned downstream. Note it as "forward-pull line"; let `writing-humanity-pass` enforce the punctuation. Don't pre-solve it.)

## Ratified lessons from shipped pieces

Routed here by the content-machine lessons loop. Sean's ratified reasons live in the gitignored
ledger; only the rule travels into this file.

- **A quoted bit needs framing before it and a response after it.** Quote, aside about the quote,
  quote again reads as a random jump. The narrator has to react to what he just showed the reader,
  or the bit sits there unclaimed. (Raising Agents ep. 1, 2026-08-25: the chain draft ran two
  quoted exchanges back to back with only a description between them; his rewrite added a setup
  line and a reaction.)
- **The callback closer is licensed, never automatic.** Returning to the opening image is a
  favourite move and a real wink, but a forced callback is worse than a plain ending. If it does
  not fit, do not build one.
- **When the callback does fit, it can carry the retitle with it.** On the same piece the closer
  and the title turned out to be one decision, both built off the strongest image in the middle of
  the story rather than off the lesson at the end.

- **The through-line is this skill's job, not the reader's.** A map that hands over a set of true
  events and expects the reader to assemble the story has not done the work. (Run #2, 2026-08-28:
  *"You hopped all over the place and expected the reader to keep up and understand."* Stated three
  separate times about three different passages, which is why it is filed as structural rather than
  local.) The failure is invisible to the but/therefore test and is what mechanics 6 and 7 exist to
  catch.
- **In medias res is licensed; a bad execution of it is not a reason to retire it.** The author's
  standard is an opening that tells you in one sentence what the whole ride will feel like. A cold
  open that drops the reader into a result with no runway is not the technique failing, it is
  mechanic 2(b) unrun. Do not respond to a bad in-medias-res draft by going chronological by
  default.
- **Do not re-establish what the piece already established.** A beat that re-states a point an
  earlier beat already landed is a nonevent by mechanic 6, and it reads as padding even when every
  sentence is true. (Run #2: *"We already established the I didn't think the jokes were funny and
  they were trying to hard with the David Sedaris lines earlier."*) The map is where this gets
  caught, because by the sentence stage it looks like emphasis.

## Story Scaffolds (pick one, apply as form not formula)

These set beat ORDER. Treat them as a checklist of pressures the piece should satisfy, never as slots to fill with canonical connective tissue ("and that's when I realized..."). If a beat can only be hit one canonical way, it has become formula. See `references/story-mechanics.md` for the full set and when each fits.

- **Problem-Struggle-Fix** (default for maker/technical posts): the real problem, the failed attempts, the fix that worked. Maps cleanly onto a post-mortem.
- **Before-After-Bridge**: the painful before, the better after, the bridge that connects them (the bridge is the value).
- **In-Medias-Res Quest**: cold open mid-crisis, backfill context in fragments, resolve.
- **Pixar (Once / Every day / Until one day / Because / Until finally)**: for arc-heavy personal narratives.

## Anti-Formula Guard (the seam must stay invisible)

The failure mode is structure leaking into the surface until a reader can name your template (the LinkedIn broetry trap). Two checks, applied to the beat map:

- **Specificity gate (hard — McKee archetype vs stereotype):** each beat must carry a detail specific to THIS story, not a generality any template would produce. Generic beat = formula has leaked. Concrete, lived, idiosyncratic beat = sound. This is a blocking output gate, not an advisory pass: the map is not done while any beat is a generic shape (hook/tension/payoff boilerplate) that would fit any post. A beat you could paste into a different piece unchanged is tension not yet welded to THIS material; rewrite it before emitting the map.

  **The abstraction-rung half (added 2026-08-28).** The gate above catches *generic* beats. It does not catch **mid-rung reporting** — a beat that is entirely specific to this piece and still inert, because it sits at the altitude of summary-about-events rather than at either the concrete moment or the earned meaning. "The model kept producing bad output" is specific to the piece and dead on the page. Reject beats written on the middle rung; send them down to the moment or up to the point.
- **Nameable-template check:** if the beat order is the obvious canonical shape with nothing bent, vary it (start later, reorder a reveal, fold two beats). The reader should *feel* the structure, never name it.

## The Chain Contract (what this skill must NOT do)

```
storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass
   (beat SHAPE + order)       (value GATE + payoff)    (every SENTENCE)      (RED-TEAM, advisory)  (scrub + no em dash)
```

- This skill emits a beat map. It is **forbidden from writing finished sentences** or specifying how a beat is phrased.
- `substack-value-engine` annotates the same map with the value gate (Itch / Solution / Transfer) and the narrative-to-value seam. Still not prose.
- `writing-voice-modes` writes 100% of the sentences fresh against the beats. It must never reorder beats.
- `writing-humanity-pass` runs last.

Handoff is in-context: the beat map **and its Handoff Block** flow to the next stage in the working context, not as a saved file. The open-loop ledger and the crest / central-loop / seam markers travel with the map through the (locked) voice stage, so `substack-value-engine` can attach the value gate to the coordinates it names, and `writing-critique` can check loop closure against the ledger four stages later.

## Related Skills

- `substack-value-engine`: the next stage. Adds the value gate and the narrative-to-value seam to the beat map. Story makes them read; value-engine makes it worth their time.
- `writing-voice-modes`: writes every sentence against this beat map. This skill owns ORDER; voice owns SENTENCES. Never let voice reorder beats; never let this skill phrase a line.
- `writing-critique`: red-teams the voiced draft between voice and humanity-pass. It critiques structural execution (hook, but/therefore seams, loop closure) but never re-litigates the beat map this skill committed. It checks loop closure against this skill's **open-loop ledger** when the ledger is present in context.
- `writing-humanity-pass`: the final scrub. Realizes forward-pull lines without em dashes.
- `creative-writing`: owns format/word-count/platform constraints. Beat maps fit within those.

## References

- `references/story-mechanics.md`: the full mechanic catalog with cited sources, the four scaffolds and when each fits, the evidence floor (what's science vs craft vs lore), and the Zeigarnik honesty note. Read when designing a non-obvious arc or debugging why a structure feels flat.

## Success Criteria

- [ ] Output is a beat map (step-outline), not prose.
- [ ] Every adjacent beat passes the but/therefore test (no and-then seams).
- [ ] Cold open raises one specific question; no throat-clearing.
- [ ] Every opened loop closes; short-form loops close within ~1-3 beats.
- [ ] The hook's gap is closeable, and the central tension is withheld then escalated.
- [ ] Each section ends on forward pull, not a summary.
- [ ] Specificity gate passes (no generic beats; no beat pasteable into another piece); template is not nameable.
- [ ] A Handoff Block is emitted: open-loop ledger (each loop, where it opens and closes) + central loop + crest beat + seam beat.

## Copy/Paste Ready

```
"Build a beat map for this post"
"Make this story addictive, structure only"
"Fix the hook and the tension arc"
"Why won't people finish this? Restructure it"
"Outline this as a problem-struggle-fix"
"Run the storytelling chain on this idea"
```
