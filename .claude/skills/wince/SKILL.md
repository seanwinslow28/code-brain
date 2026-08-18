---
name: wince
description: Interview someone's visual taste out of them by showing options and reading their reactions, then emit a reusable taste block they can paste into any image model. Use when asked to "figure out my style", "build my taste block", "what's my aesthetic", "the model won't draw like me", "make it look like mine", "run the taste interview". If someone is stuck arguing an image toward what they want one adjective at a time, offer it, do not start the interview unasked. USER-INVOKED — do not invoke from another skill. Not for generating final art (use the image-gen skills); not for prose voice (use writing-voice-modes); not for fixing a single prompt or a drifted generation (use prompt-how-much).
---

# Wince

It shows you things, reads which ones you wince at, and writes the block that makes the machine draw like you.

## The one rule that makes this work

Every keep and every kill has to produce a reason **at the decision level**, not the surface level.

> **Surface:** "I love the texture and the grain."
> **Decision:** "I want the process to stay visible. The sketch marks aren't mistakes, they're evidence of thought. It's visual proof that art takes time."

The second one is portable. It tells a machine what to do in a situation the user never described. The first one does not.

Same on the negative side. Every ban carries its why, and the why is the negative of a value the keeps demonstrated:

> **Never do:** polished, surface-perfect rendering that erases the hand.
> **Why:** everything I love keeps the fingerprints in. A flawless surface means the process was hidden or never happened.

Never accept a bare preference. When someone says "I like that one," ask what decision the maker made. Keep going one level down until the answer would still be useful applied to a different subject. Two follow-ups is usually enough; four is an interrogation and people quit. If the third try still lands on surface, record the surface answer, mark it thin, and move on. A thin field is honest. A fabricated one is not.

### The test, run on every answer before you record it

Take the answer and apply it to a subject the user never mentioned. A dog at a bus stop, a kitchen at 2am, anything far from what's on screen. Now imagine two competent images of that subject. If the answer lets you reject one of them, it's a decision. Record it. If it only lets you add something to both, it's surface. Ask again.

Pick the pair the answer would have the hardest time telling apart, not the easiest. Two images that both already do the thing the answer names is the honest test. An answer that can only beat a foil nobody would have made hasn't chosen anything.

### Counting the tries

The user's first answer about a field is try 1 for that field. Every follow-up you ask about that field produces its next try. You get at most two follow-ups, so try 3 is the last. The count runs per field and resets when you move on. If an answer lands on a different field than the one you're digging, credit it there as that field's try 1 and leave the current field's count where it was. If the user dodges twice without landing on any field, that counts as your two follow-ups spent.

### How to ask the follow-up

Point at their own words and ask what choice the maker made to get that. "What is the grain doing for you that a clean surface wouldn't?" beats "can you say more?" Say back what you heard in their words before you ask again, so it reads as interest rather than doubt. Ask about the decision, not about their feelings. "Not about their feelings" means don't ask how it made them feel; asking what it reminds them of, or what would ruin it, is fair game and usually faster. Never hand them an answer to pick from, for the reason given in the examples guard in [references/block-schema.md](references/block-schema.md).

### Marking a field thin

Record the user's own words as the answer, with no marker inside the block. Track the thin fields outside the block body, after the closing NEVER DO section, as `Thin fields, next pass: <field names>`. The block itself has to survive being pasted into an image model, and a parenthetical that model doesn't understand is a parenthetical it will try to draw.

Never list a field the user did dig, and never fill a thin field with a plausible answer of your own.

### Where this rule stops

This rule governs the conversation. The schema's per-field "Accept when:" tests judge the finished answer, and they are stricter. When one of them fails, check why. If the decision is in what the user said and only the phrasing is loose, tighten the phrasing and move on. If it fails because information the user never gave is missing, that is not a wording job. Go back and ask, and it spends a try like any other. Never close that gap yourself.
