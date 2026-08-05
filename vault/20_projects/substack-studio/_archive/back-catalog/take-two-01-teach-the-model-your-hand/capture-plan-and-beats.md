---
publication: pencil-and-prompt
format: take-two
title: "Take Two #1 — Teach the Model Your Hand (working)"
status: capture-pending
craft_lane: visual
discovery_angle: "A#4 personal style can't be enforced + A#2 surface vs essence + D#1 references don't stop revert-to-average; web supplement: identity anchoring + rubric-as-logic"
itch: "I fed the model my own face and it handed me a glossy stranger. It had my likeness, not my taste."
solution_artifact: "PENDING CAPTURE — the real run: before, the move-ladder steps (incl. rerolls), after + Sean's per-step notes. Write from the build (CLAUDE.md §3)."
transfer: "The gift is a fill-in Taste Rubric: name your style as visual LOGIC, feed 3-5 references, correct drift by drift. Run it on YOUR hand, in the tool you already have."
differentiation: "Nate's 'Power Steering' owns precision/correctness for commercial images (he brackets out creative style on purpose). We own soulless->soul taste-transfer for a personal style. Demo-first, not tool-first."
tool: "ChatGPT / GPT Image (the reader already has it; most transferable; conversational iteration is strong)"
hero_image: "the before/after pair (after = masthead-grade)"
voice_chain_run: n
---

# Take Two #1 — Teach the Model Your Hand

**Locked (2026-06-27 brainstorm + research pass):** flagship Take Two; the **lesson** is *how to teach the model a style it has no prior for*; the **demo vehicle** is a **self-portrait of Sean in his pencil-test hand**, **bust framing**; tool = **ChatGPT / GPT Image**; thesis = *it has my likeness, not my taste*; the **gift** is a reusable **Taste Rubric** template (Part C); house style is the example here, **not** a requirement for future posts.

The value gate is pre-cleared on Itch and Transfer. **Solution stays empty until the capture exists** — this doc is the shoot plan, the beats, and the gift, NOT a draft. Write from the build.

---

## Part 0 — The pre-flight research (why this post earns its slot)

This is the new standing pre-flight (now CLAUDE.md §8 Stage 0). Summary of what it surfaced:

- **Pain is real and in Sean's lane.** Run A: "personal drawing style cannot be reliably matched or enforced," "AI captures surface aesthetics but misses the emergent essence." Run D: "references and fine-tuning don't stop the revert-to-average." These are the loudest pains in visual, and they are exactly the gap Pencil & Prompt exists to close.
- **Competitive read (Executive Circle + web).** Nate Jones's [Power Steering for Nano Banana Pro](https://natesnewsletter.substack.com/p/no-one-wrote-a-pro-grade-control) is the closest comparable, and it is a gift: he solves **precision for commercial/technical images** (product labels, dashboard layouts, accurate infographic numbers) with JSON schemas, and he *explicitly* brackets out creative style ("exploration happens in natural language, execution happens in JSON; don't force structure onto a creative process"). He also owns "taste" and "you won't be replaced" ([Good Taste](https://natesnewsletter.substack.com/p/the-universal-ai-skill-good-taste)) — so we never lead with those. **Our uncontested wedge: soulless->soul taste-transfer for a personal, idiosyncratic style, shown move by move.** Correctness is his; soul is ours.
- **Craft accuracy (current, verified).** Generic styles (watercolor, anime) are now *easy* for AI; the hard, valuable problem is an out-of-distribution **personal** style. The working levers in 2026 are **reference images (3-5) + conversational, scoped iteration** ("make the lighting warmer, lose the steam" works reliably in ChatGPT). Identical-style reproduction is still imperfect — so the post is honest that the arc is a *story of corrections*, not a clean climb. Sources: [Kapwing — replicate ChatGPT image styles](https://www.kapwing.com/resources/how-to-replicate-popular-chatgpt-image-styles/), [OpenAI GPT image prompting guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide), discovery runs A + D + the 2026-06-27 web supplement.
- **PM lens.** *Jobs-to-be-done:* the reader is hiring this post to **"make AI produce work that's recognizably mine so I can actually use it without being embarrassed"** — NOT to learn the pencil-test look. So the post centers *their* outcome; pencil-test is just the worked example. *Red-team / pre-mortem:* the failure modes + mitigations are logged in the Risks section below and are baked into the plan.

---

## Part A — The capture plan (run on your Mac; image gen is firewalled off Cowork)

**Tool:** ChatGPT (GPT Image), web UI — conversational iteration gives you the move-by-move screenshots for free. House-style reference: [`playbook/image-house-style.md`](../playbook/image-house-style.md).

**Inputs to have ready:**
1. A clear, front-facing **photo of you** (good light, plain background) — the likeness reference.
2. **3-5 references of the target style** (your pencil-test work / portfolio illustrations from [`_assets/style-anchors/`](../_assets/style-anchors/) + `2D-Character-Sketch-Sean-v1.png`). Research is clear: 3-5 references beat one. This is also the reader's transferable move (gather examples of YOUR hand).

**Capture discipline (this IS the value gate):** save EVERY generation into `take-two-01-teach-the-model-your-hand/images/` as `NN-step.png`, **including the rerolls and the failures**, and jot ONE line per step on *why* you made that correction. Those one-liners are the post's narration. The honest mess ("tried this, it regressed the face, here's how I clawed it back") is the texture, not something to hide. The arc is a story of corrections, not a guaranteed monotone climb.

### The shot list (conversational, in one ChatGPT thread where possible)

| # | Step | What you do (the actual move) | Save as | Why it's in the post |
|---|---|---|---|---|
| 0 | **The soulless before** | Upload your selfie. Type the lazy skeptic prompt verbatim: *"make this a cool stylized portrait, make it look professional and artistic, make it beautiful."* | `00-before.png` | The cringe cold-open. It has your face and still misses you. |
| 1 | **Prove more prompting ≠ more you** | One or two lazy nudges in the same thread: *"make it more artistic," "add some style."* | `01-glossier.png` | The skeptic's exit point. It gets glossier, not closer to you. |
| 2 | **Feed the references (the first real move)** | New turn: attach the 3-5 style references + the selfie. *"Redraw the person in the photo in the hand-drawn pencil-test style of these reference images."* | `02-references.png` | Stop describing, start referencing. The lever the research confirms. |
| 3 | **Name the style as LOGIC, not motifs** | Add the rubric as rules (the master recipe below): cream paper, graphite + cross-hatching, faint blue construction lines, ONE amber accent, one watercolor bloom, no text. | `03-rubric.png` | Taste named as transferable *logic* (run A: surface motifs aren't the style). |
| 4 | **Kill the gradients** | *"No digital shading or gradients anywhere; graphite and cross-hatching only."* | `04-no-gradients.png` | The single most common AI-look tell, removed. |
| 5 | **Show the construction lines** | *"Leave the faint light-blue construction underdrawing visible."* | `05-construction.png` | The pencil-test tell: hand-made, in-process. |
| 6 | **Push the caricature** | *"More exaggerated and absurd: oversized head, rubbery features, extreme comic expression."* (realistic -> cartoonish -> absurd; absurd wins) | `06-caricature.png` | The lever is always *push further*, never *more realistic*. The decisive move. |
| 7 | **One accent + the bloom** | *"One warm amber accent on [the meaningful element]; everything else graphite; one soft amber watercolor bloom BEHIND the linework, never splatter."* | `07-accent-bloom.png` | The restraint that reads as taste. |
| 8 | **Steer the likeness back** | If your face drifted: *"keep the jaw, hair, and eyes from the reference photo."* Re-feed the selfie if needed. | `08-identity-lock.png` | Honest: even with references it drifts; you correct it. The revert-to-average, fought in public. |
| 9 | **The winner** | Lock the best result. | `09-after.png` | The pulse. The before/after contrast IS the argument. |

If a step takes three tries, save all three. Rerolls are evidence of iteration, not waste.

### The master recipe to paste (the rubric, as logic)

```
A hand-drawn pencil-and-ink portrait on warm cream paper (#FFF9F0), animator's pencil-test
feel: graphite linework, fine cross-hatching, faint light-blue construction underdrawing left
visible, warm paper grain, hole-punch marks along one margin. Wildly exaggerated, absurd
cartoon caricature of the person in the reference photo, never realistic.

SCENE: a bust portrait of [me], facing the viewer.

Monochrome graphite and ink throughout, with ONE restrained warm amber accent on [the element
that carries the meaning], plus a single soft amber watercolor bloom behind the head that bleeds
into the cream paper. The wash sits BEHIND the linework, never splatter, never on top.

Absolutely no text, words, letters, numbers, logos, or watermarks anywhere. Purely pictorial.
```

---

## Part B — The beat skeleton (lock the shape, then run the voice chain)

Chain (CLAUDE.md §8): `substack-value-engine` -> `storytelling-architecture` -> `writing-voice-modes` (Sean Mode) -> `writing-critique` -> `writing-humanity-pass`. Lock this shape first; draft only after Sean approves.

- **Tone dial:** Sean Mode, amber-warm, dive-bar grit, anti-hype, self-deprecating (you botched your *own* face). No em dashes.
- **Length:** flagship, ~1,100-1,500 words. One craft lane (visual), one idea, one promise.
- **JTBD anchor:** the reader's job = make AI output recognizably *theirs*. Every beat serves that, not "admire Sean's pencil style."

**The arc (but/therefore, cold-open to sideways-ask):**

1. **Cold open (the cringe):** you upload your own face, type "make it cool," and get a confident stranger wearing your face. Glossy, hoodie, dead eyes. *(The "stranger wearing my face" image is the locked Post-1 concept in the house-style doc.)*
2. **BUT** it had your literal photograph and still missed you. So the problem isn't the input. **THEREFORE** the gap is taste, not data.
3. **The exit point + the reframe:** this is where most people quit, and where someone tells them they're "prompting it wrong." They're not. They quit one step early. *(Show, don't preach — discovery Angle 5.)* One sideways line of contrast: the precision crowd will hand you a JSON schema to lock a product label; that's the wrong tool for soul. Soul is taught, not specified.
4. **The move ladder (the body):** narrate steps 2-8 as taste handed over one correction at a time — feed the references, name the style as *logic* not motifs, kill the gradients, show the construction lines, push the caricature, one accent + bloom, steer the likeness back when it reverts to the average. Each correction is a sentence of *why*, lifted from your capture notes. Include one honest reroll.
5. **The after (the pulse):** the before/after pair carries the argument. Don't oversell it.
6. **The gift (the recipe, made portable):** hand over the **Taste Rubric** (Part C) — references + your style named as logic + scoped correction — runnable today in plain ChatGPT, on *your* face or *your* style, whatever style the model keeps flattening on you.
7. **Closer (sideways ask):** the hybrid callback. You taught the intern your hand; go teach it yours. Cereal-on-the-floor invitation, the ask lands sideways, ends on the work.

---

## Part C — The gift: the Taste Rubric (the post's reusable artifact)

Ship this as a fill-in template (the reader completes it for their own style). This is what makes the method travel — it generalizes the house-style constants into reader-agnostic slots, the "style as visual logic" lesson made copy-pasteable. Nate ends every big post with a reusable artifact; this is ours.

```
MY TASTE RUBRIC (fill this in, then feed it to the model with 3-5 references of your work)

1. REFERENCES: 3-5 images of MY own work (or the exact style I want). Attach them every time.
2. MEDIUM / SUBSTRATE: what is it physically made of?  (e.g., graphite on cream paper / oil on canvas / risograph / felt-tip)
3. THE HAND (mark-making): how do my lines/marks behave?  (e.g., cross-hatching, visible construction lines, loose gesture, hard ink)
4. COLOR RULE: the discipline, stated as a rule.  (e.g., monochrome + ONE accent / a strict 3-color palette / muted earth tones only)
5. THE "SHOW THE WORK" TELL: what signals hand-made, not rendered?  (e.g., construction lines left in, brush texture, deckled edge)
6. REGISTER: where do I sit on realistic <-> exaggerated?  (e.g., absurd caricature / grounded / stylized-but-anatomical)
7. THE ONE MOVE THAT CARRIES MEANING: the focal treatment.  (e.g., a single watercolor bloom behind the subject)
8. NEVER DO (the negative list, 5-10 items): the AI-look tells to ban.  (e.g., no gradients, no glossy 3D, no airbrush, no text, no symmetry)

Then iterate: change ONE thing per turn, keep what works, re-feed the references when it drifts.
```

---

## Risks / pre-mortem (baked into the plan)

| Risk | Mitigation (already in the plan) |
|---|---|
| The "before" comes out *competent*, not cringe, undercutting the open | The thesis still holds: competent-but-generic is not YOU. Frame the before as "good, and still a stranger." Likeness vs taste. |
| The arc isn't a clean monotone improvement (model is stochastic) | Plan says capture rerolls + narrate the honest claw-back; the corrections are the story, not a guaranteed climb. |
| The recipe reads as "do what Sean did" (doesn't transfer) | Part C ships a fill-in rubric for the reader's OWN style; the gift is the form, not the pencil-test. |
| Reads like a house-style ad | Lesson reframed to "teach a style with no prior"; pencil-test is explicitly the example, not the point. |
| Looks like Nate's precision/JSON post | One sideways line draws the line: schemas lock correctness; soul is taught. Demo-first, not tool-first. |
| Likeness needs a selfie; reader can't transfer | The reader's analog is 3-5 references of THEIR work; the rubric makes that step 1. |

---

## What's next

1. **Sean runs Part A on the Mac** -> drops numbered images (incl. rerolls) + per-step notes into `images/`.
2. That fills the Solution slot -> the value gate clears for real.
3. We draft from the capture via the voice chain (Part B is the skeleton, Part C ships as the gift), Sean hand-rewrites, fold the rewrite into `voice-samples.md`, mechanical proofread, fill the `[Take Two #1]` links in Start Here + About, ship.
