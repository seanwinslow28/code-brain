---
type: method-and-experiment
post: take-two-01-teach-the-model-your-hand
created: 2026-06-28
status: experiment-ready
purpose: "The character-sheet method as the real value of post #1, plus the before/after experiment that proves it. Grounded in anima's own reference-gap law and the multi-angle research."
related:
  - "true-pain-and-opportunity-map.md"
  - "matrix-results-scored.md"
  - "[[anima/docs/research/2026-05-30-nb2-editing-character-consistency-template]]"
  - "[[anima/characters/sean-anchor/character.yaml]]"
---

# The character-sheet method, and the experiment that proves it

## The reframe (the real value)

**Stop feeding AI a selfie. Build it a character sheet.**

A single headshot gives the model exactly one pose to work from. So it can only do two things: copy that pose with a thin coat of style (your "identical copy with a hint of art style" complaint), or invent the parts it cannot see the moment you ask for a new angle, expression, or scene, and that invention is where "you" turns into a stranger. A character sheet, multiple angles and expressions of the same person, removes both failures at once. It is the difference between a frozen photo and a controllable, reusable identity. It is the actual dial you have been reaching for, and it is the thing that makes wild style-range and believable world-insertion work downstream.

This is not a hunch. It is a law you already proved.

## Why it is true (your own evidence, plus the field)

- **anima's reference-gap law, verbatim:** "A front-only anchor is asked for a back view, the model invents anatomy. Prevention: supply a dedicated view reference for the new angle (the turnaround sheet); do not ask one anchor to imagine a view it does not contain." (2026-05-30 NB2 consistency template.) The single headshot IS the front-only anchor. The character sheet IS the fix.
- **The multi-angle sweet spot:** the discovery research converged on 3 to 6 clean, multi-angle references as the identity sweet spot, with a single front reference unable to separate legitimate view variation from drift. It is also why anima's similarity gate is record-only: one front anchor cannot police drift.
- **You have already done it:** the anima sean-anchor Bible is a finished character sheet of you, built by the exact turnaround workflow this post would teach. The proof is not theoretical; it is in your repo.

## The sharpest single proof (the killer before/after)

One image pair can carry the whole argument. Ask for the thing a selfie cannot give:

> "Give me a clean 3/4 profile of this person." (or a profile, or a specific new expression)

- **Control (single headshot):** the model invents a profile it never saw. The jaw, the hairline, the nose change. It is a different person from the side.
- **Treatment (character sheet):** it has the profile plate, so the side view is actually you.

That one pair is the post. Everything else is reinforcement.

## The experiment (run on the Mac)

Hold the person constant, change only the reference, measure the delta. Same discipline as the style matrix.

**Two reference conditions:**
- **A. Control:** the single `sean-headshot.jpg`.
- **B. Treatment:** a character sheet. Two ways to feed it, test both:
  - B1: the multi-angle plates as multiple reference images.
  - B2: the character sheet as ONE composite image (a turnaround sheet). This matters because GPT Image tends to muddy with several separate references ("style soup") but reads a single composite cleanly. anima already ingests turnaround sheets as one sheet with region crops, so this is a proven shape.

**The asks (where a selfie fails, ranked by how decisive):**
1. A non-front angle: 3/4 and full profile. (The killer demo.)
2. A new expression or head turn the headshot does not show.
3. A hard style AND a new angle together (e.g., woodblock profile, watercolor 3/4).
4. A 3-frame consistency run: same person, three different poses, is it the same him across all three?

**Tool plan:** run it in ChatGPT / GPT Image first, because that is the reader's tool and the post's premise. If the composite sheet (B2) does not visibly beat the headshot there, compare Nano Banana (the documented multi-angle champion). "Which tool the character-sheet method actually needs" is itself valuable content, not a detour. Be honest about it in the post.

**Scoring (the same 0 to 2 rubric, per output):**
- Identity holds on the markers (brow weight, eye spacing, jaw angle, cowlick, hair color)?
- Did it honor the new angle/expression, or freeze the front pose / invent badly?
- Still ownable (a deliberate result, not a lazy default)?

The control should fail asks 1 to 4. The treatment should pass. The gap is the proof.

## The transferable gift (so it travels to any reader)

The reader will not have an anima Bible. The gift is "how to build a character sheet from one photo," the method, made portable:

1. From the single selfie, generate a front plate you approve.
2. Derive each new view (3/4, profile, back) by editing, re-anchoring to the ORIGINAL photo each time, never chaining off a generated plate (drift compounds after a few chained edits).
3. Assemble the approved views into one composite sheet.
4. From then on, feed the sheet, not the selfie. Restate the identity markers, change one thing per generation, apply the style last.

That is exactly your anima Cy workflow, stripped of the code, runnable by a non-coder in ChatGPT. It is the over-deliver-on-a-narrow-promise gift the value engine wants.

## What you already have (so capture is cheap)

- `sean-headshot.jpg` (the control).
- `anima/characters/sean-anchor/`: 10 turnaround plates (head + body, all angles), 4 expressions, `anchor.png`, `character.yaml` (locked markers + palette), and the source turnaround sheets `sean-character-full-body-turnaround.png` and `sean-head-turnaround.png` (ready-made composite sheets for B2).
- The 12-style matrix from the headshot (a partial control already done).

Caveat: the anima plates are already in the pencil-test style, so they prove the principle but are not a clean photo-to-sheet control. For the reader-facing demo, building one fresh sheet from the real headshot is the honest, transferable version, and it is the step that becomes the gift.

## Value-gate framing (pre-filled; Solution needs the Mac capture)

- **Itch (genuinely Sean's):** "I fed it my face and got either a frozen copy I cannot move or a stranger the moment I asked for a new angle."
- **Solution (the real artifact, capture pending):** the before/after, single headshot vs character sheet, on the asks above, with the 3/4-profile pair as the hero.
- **Transfer (the gift):** "Build your subject a character sheet from one photo, feed it as one composite, and AI stops handing you a stranger. Here is the four-step recipe."

This is a narrow promise delivered deeply, the opposite of posting for the sake of posting.

## Recommended skill stack (you asked)

In sequence:
1. **`voiceprint:substack-value-engine` (next, before capture).** The gate for "is this worth posting." It owns Itch / Solution / Transfer, Rule-of-One, and over-deliver-on-a-narrow-promise. Run it on this character-sheet thesis to lock the value and the single promise before you spend capture effort. This is the direct answer to "I do not want to post for the sake of posting."
2. **`anthropic-skills:creative-director` (during capture).** Its critique rubric (identity / style / composition / continuity) is the scoring lens for the before/after, so the proof is judged, not vibed.
3. **`voiceprint:storytelling-architecture` then the voice chain** (`writing-voice-modes` Sean Mode, `voiceprint:writing-critique`, `voiceprint:writing-humanity-pass`) once the capture exists, per the mandated chain.
4. **On the Mac, for capture:** `gemini-pencil-animation-image-gen` / `openai-image-gen` / `image-generator-prompt-science`.

Optional: `pm-execution:test-scenarios` if you want the experiment written as formal test cases, but the design above is enough to run.

## The honest open question the experiment settles

Does a single composite character-sheet image meaningfully beat a single headshot inside ChatGPT / GPT Image specifically? The anima evidence is strong but tuned to Nano Banana. If GPT Image needs the multi-image path or underperforms, the post should say which tool the method actually needs. Either result is true and useful; do not pre-decide it.
