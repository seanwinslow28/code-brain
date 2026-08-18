---
name: wince
description: Interview someone's visual taste out of them by showing options and reading their reactions, then emit a reusable taste block they can paste into any image model. Use when asked to "figure out my style", "build my taste block", "what's my aesthetic", "the model won't draw like me", "make it look like mine", "run the taste interview". If someone is stuck arguing an image toward what they want one adjective at a time, offer it, do not start the interview unasked. USER-INVOKED — do not invoke from another skill. Not for generating final art (use the image-gen skills); not for prose voice (use writing-voice-modes); not for fixing a single prompt or a drifted generation (use prompt-how-much).
---

# Wince

It shows you things, reads which ones you wince at, and writes the block that makes the machine draw like you.

## The one rule that makes this work

Every keep and every kill has to produce a reason at the decision level, not the surface level.

> **Surface:** "I love the texture and the grain."
> **Decision:** "I want the process to stay visible. The sketch marks aren't mistakes, they're evidence of thought. It's visual proof that art takes time."

The second one is portable. It tells a machine what to do in a situation the user never described. The first one does not.

Same on the negative side. Every ban carries its why, and the why is the negative of a value the keeps demonstrated:

> **Never do:** polished, surface-perfect rendering that erases the hand.
> **Why:** everything I love keeps the fingerprints in. A flawless surface means the process was hidden or never happened.

Never accept a bare preference. When someone says "I like that one," ask what decision the maker made. Keep going one level down until the answer would still be useful applied to a different subject. Two follow-ups is usually enough; four is an interrogation and people quit. If the third try still lands on surface, record the surface answer, mark it thin, and move on. A thin field is honest. A fabricated one is not.

### The test, run on every answer before you record it

Take the answer and apply it to a subject the user never mentioned. A dog at a bus stop, a kitchen at 2am, anything far from what's on screen. If it still tells you what to do, it's a decision. Record it. If it only describes what was on screen, it's surface. Ask again.

### Counting the tries

The user's first answer is try 1. Every follow-up you ask produces the next try. You get at most two follow-ups, so try 3 is the last one, and there is never a third follow-up. The count runs per field, and it resets when you move to a new field.

### How to ask the follow-up

Point at their own words and ask what choice the maker made to get that. "What is the grain doing for you that a clean surface wouldn't?" beats "can you say more?" Ask about the decision, not about their feelings, and never hand them a decision-level answer to pick from. The examples in [references/block-schema.md](references/block-schema.md) exist to calibrate you, not to read aloud.

### Marking a field thin

Record the user's own words as the answer, then on the next line under it, write exactly:

```
(thin: surface answer, not dug to a decision)
```

Plain English, so it survives being pasted into any chat window, and it tells whoever reads the block next that this field carries less authority than the rest. Thin fields are what the next version of the block goes after. Never write the marker on a field the user did dig, and never fill a thin field with a plausible answer of your own.

### What this rule is not

It is not a quality bar on the wording. The schema's per-field "Accept when:" tests judge a finished answer; this rule only governs how the conversation gets there. An answer can pass the transfer test here and still need rewriting to satisfy its field. That is a wording job, not a reason to reopen the interview.
