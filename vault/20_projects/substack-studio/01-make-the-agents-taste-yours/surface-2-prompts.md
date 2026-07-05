# Surface 2 prompts, ready to paste (the image render)

The render half of the capture, for "Teach the Agent Your Craft." Worked example tool: ChatGPT / GPT Image (use whatever you like; the prompts are tool-agnostic). These are a starting point, tweak freely. The scene is held constant (the Saturday-morning-cartoon moment) so the only thing that changes between cold and with-craft is the context you hand it.

**Capture discipline:** save every generation including rerolls and flops, and write one line of *why* next to each. Those one-liners are the post's narration.

**Thread logic:** steps 0 and 1 share one fresh thread (the cold run). Step 2 onward can stay in that thread (so the contrast is visible) or start fresh, your call. Save each result under the filename in its heading.

---

## `render/00-before.png` · the cold skeptic prompt

Fresh thread, no context. Type it lazy, the way someone would right before they give up.

```
Make me a warm, nostalgic illustration of a kid watching Saturday morning cartoons.
A child sitting on the living room floor with a bowl of cereal, lit by the glow of the TV,
early morning. Make it cozy, beautiful, and professional.
```

*Why it's in the post: the cringe "before." It will come back glossy, Pixar-adjacent, heartwarming, dead. Competent, and nobody's.*

---

## `render/01-glossier.png` · prove more prompting is not more you

Same thread, one or two lazy nudges.

```
Make it more artistic and polished. More vibrant, more detail, really make it pop.
```

*Why: the skeptic's exit point. It gets glossier, not closer to you.*

---

## `render/02-with-block.png` · paste the craft block, then the scene

The real move. Paste your full taste-context block (your durable hand), then the short, disposable scene line. If you have your refs handy, attach them here too (or save that for step 3).

```
Here is my taste-context block. Read all of it, then redraw the same scene applying it exactly.

MY TASTE-CONTEXT BLOCK
1. REFERENCES: [attach 3-5 images of my own pencil-test work]
2. MEDIUM / SUBSTRATE: warm cream paper (#FFF9F0), graphite and ink, animator's pencil-test
   feel, visible paper grain, hole-punch marks along one margin.
3. THE HAND (mark-making): graphite linework, fine cross-hatching for shadow, a faint
   light-blue construction underdrawing left visible.
4. COLOR RULE: monochrome graphite and ink throughout, with exactly ONE restrained warm
   amber accent. Never a second accent color.
5. THE SHOW-THE-WORK TELL: leave the construction lines in, keep the paper grain and the
   hole-punch marks. It should look hand-made and in-process, not rendered.
6. REGISTER: wildly exaggerated, absurd cartoon caricature. Never realistic, never photographic.
7. THE ONE MOVE THAT CARRIES MEANING: one warm amber accent on the single element that
   holds the feeling (here, the glow of the TV), plus one soft amber watercolor bloom behind
   the figure that bleeds into the cream paper. The wash sits BEHIND the linework, never on
   top, never splatter.
8. NEVER DO: no gradients, no glossy 3D, no airbrush, no smooth digital shading, no Pixar
   polish, no dead-eyed heartwarming, no text or letters or logos, no symmetry.

THE SCENE: a kid, around eight, cross-legged on the living room floor in pajamas, a bowl of
cereal in their lap, lit by the glow of an old TV playing cartoons, early Saturday morning,
the rest of the room dark. Keep the TV glow as the one amber accent.

Apply the block exactly. No text anywhere.
```

*Why: the delta, and the hero "after" candidate. Stop describing, start handing over your craft as context.*

---

## `render/03-refs.png` · optional, references plus the block (max fidelity)

New turn. Use it if step 2 still felt generic; this is the research-backed lever (3-5 refs beat words).

```
I've attached 3-5 references of my own hand. Use them as the reference for HOW I draw, together
with the taste block above. Redraw the same scene so the linework, the cross-hatching, and the
visible construction lines match my references, not a generic illustration style. Keep the one
amber accent on the TV glow.
```

*Why: refs plus block together. Optional, so the block stays the clean hero of the delta.*

---

## `render/04-reroll.png` · the honest scoped correction (save every try)

When it drifts back toward the average (it will). Correct ONE thing at a time. Save `04-reroll.png`, `04b.png`, `04c.png` for each attempt.

```
Close, but it drifted back toward a smooth, polished look. Fix only this: bring back the faint
blue construction lines and leave them visible, use graphite and cross-hatching for all shading,
and remove every gradient and smooth fill. Keep the one amber accent on the TV glow and the soft
amber bloom behind the figure. Do not smooth the linework, it should look hand-drawn.
```

If the figure goes realistic or off-model, add:

```
Also push the caricature further: exaggerated, absurd proportions, not realistic.
```

*Why: fighting the regression to the mean, in public. The rerolls are the texture, not waste.*

---

## `render/05-after.png` · lock the winner

Final. Lock it, light polish only.

```
This is the one. Keep the composition, the linework, and the amber accent exactly as they are.
The only change: deepen the cross-hatching in the shadows slightly, and make sure the amber
bloom sits behind the linework, not over it. Nothing else.
```

*Why: the pulse. The before/after pair is the whole argument.*

---

## Quick tweak notes

- The scene is yours to adjust (the exact framing, the kid's pose, what's on the TV). Just keep it the SAME across 00 and 02 so the delta reads as craft, not composition.
- Field 1 of the block (REFERENCES) is the one part you fill with your actual images. The other seven are pre-filled with your pencil-test hand; edit them if the interview surfaced something sharper.
- If GPT Image fights the "no text" rule, repeat "no text, letters, numbers, or logos anywhere" at the very end of the prompt.
- Keep the cold prompt (00) genuinely lazy. The worse it is, the truer the before.
