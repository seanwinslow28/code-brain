---
type: research-and-scaffold
post: take-two-01-teach-the-model-your-hand
created: 2026-06-28
status: ready-to-test
purpose: "The prompt scaffold that teaches the model your hand: a constant likeness-lock + a swappable style-logic block, plus the morph-matrix test set to discover what good looks like across styles, then reverse-engineer the step-by-step."
tool: "ChatGPT / GPT Image (gpt-image-2). Cross-tool notes included."
related:
  - "capture-plan-and-beats.md"
  - "../playbook/image-house-style.md"
  - "[[anima/docs/research/2026-05-30-nb2-editing-character-consistency-template]]"
---

# Teach the Model Your Hand: the likeness-lock + style-logic scaffold

This is the research-backed engine for the post's demo. The deep-research pass (six angles, web + your own fleet, adversarially verified) all points at one shape: a **modular prompt** where identity is a constant you lock and restate every turn, and style is a swappable slot you describe as visual logic, never as an artist's name. Below: the findings that matter, the paste-ready scaffold, the morph-matrix to run on the Mac, and how the results reverse-engineer into the post's step-by-step.

---

## Part 1 — The seven findings that shape the scaffold

1. **Identity and style trade off directly. There is no setting that maximizes both.** The dial that holds a face is the same dial that suppresses a new look. So "good" is a sweet spot you find per style, not a global win. This is the whole reason the post is a *story of corrections*, not a clean climb.

2. **Edit-from-photo holds likeness better than generate-from-text. Generate wins when you need to escape the photo.** For a specific real person, starting from the actual headshot pins the "facial fingerprint." Text-only generation of a named real face is the weakest path and the most prone to revert-to-average. You chose to weigh both equally, so the scaffold ships both, with a decision rule (Part 4) and a note that running both on the same style *is the experiment*.

3. **3 to 5 clean references beat 1, and beat 16.** Past ~6, the model averages conflicting details and likeness degrades. The references must be clean, single-subject, ideally multi-angle. Piling on muddy refs is a documented failure path, not a free boost.

4. **Name a short set of unique markers. Do not prose-describe the whole face.** Text and reference compete: the more words you spend re-describing the face, the more it drifts toward the generic thing your words spell. Enumerate 5 to 7 *distinctive* markers and stop.

5. **"In the style of [living artist]" is weaker, riskier, and unswappable.** ChatGPT silently rewrites a living-artist name into roughly three style adjectives you do not control (DALL-E system card behavior), individual living artists are an explicit content-policy block, and naming a working artist carries IP exposure. A name is opaque, so you cannot swap one field of it. Describe the **visual logic** instead.

6. **A look resolves from five describable fields: medium, mark-making, palette rule, register, signature move.** These are the levers the model actually responds to, and the split between subject-tokens and style-tokens is mechanically real inside the model, not just prompt hygiene. Hold the subject block constant, overwrite the style block, get a controlled swap.

7. **Order is load-bearing: identity first, style last, invariants restated every turn.** Models show a first-position attention bias, OpenAI's own structure leads with subject and ends with constraints, and your anima pipeline learned the hard way that a style token placed early competes with the identity markers. Lead with the lock, tail with the style, and repeat the lock verbatim on every iteration. (One source argued the reverse "style-first" ordering; it is an outlier against three converging lines of evidence, so we do not adopt it.)

### Caricature, specifically (top-pick #2, the dial)
Faces are encoded as **deviations from an average face**, and caricature works by exaggerating exactly those deviations, which is why a good caricature is recognized as fast or faster than a photo. But the benefit is **bounded** (a "peak shift"): recognition improves with moderate exaggeration, then degrades past an optimum (the classic window is roughly +16% to +50%, not infinite distortion). Translation for the dial: exaggerate only the 2 to 3 features where the face most differs from average, leave average features alone, and never let the dial touch the locked features.

### Which features carry identity (so the lock names the right ones)
From face-recognition research, in priority order: **eyebrows** (at least as important as eyes, and the most under-specified high-value lock), **eyes and eye-spacing**, the **configural spacing** between eyes-nose-mouth, the **jaw and face outline**, the **hairline and hair**, then skin tone and any signature accessory. The **nose carries little identity**, so it is a safe feature to exaggerate on the dial. For a viewer who does not know Sean (most readers), the **external** cues (outline, hairline) matter even more, which is an argument for keeping those firmly in the lock.

### Tool reality (gpt-image-2, current as of mid-2026)
ChatGPT's live image model is **gpt-image-2** ("ChatGPT Images 2.0"). It takes reference images and multiple inputs, and it processes inputs at **high fidelity automatically** (the old `input_fidelity` knob is locked on, good for likeness). It has **no seed or reproducibility control**, so you cannot regenerate an identical image. Same-conversation iteration drifts far less than fresh sessions, but it is not a guaranteed pixel reuse. Character consistency is "improved" but still listed as a known limitation, not a guaranteed feature. Engineer for **re-anchoring**, not reproducibility.

---

## Part 2 — The scaffold (paste-ready, three blocks)

Fixed order. Block 1 leads (identity), Block 2 is the swap (style), Block 3 tails (constraints). Restate Block 1 and Block 3 verbatim on every turn.

### BLOCK 1 — LIKENESS-LOCK (constant, filled for Sean)

```
SUBJECT: a portrait of the same adult man in the reference photo. Keep him
unmistakably recognizable as the same person. Preserve, in this priority:

- Eyebrows: strong, fairly straight horizontal brows with a heavier line weight.
- Eyes: blue, set about one eye-width apart at the inner corners; keep that spacing.
- Proportions: keep the relative spacing between eyes, nose, and mouth unchanged.
- Jaw and face outline: angular jaw, squared chin (a roughly 100 to 110 degree
  corner at the jaw); do not round the face.
- Hair: dirty-blonde / warm light-brown, medium-short and tousled, with a small
  upward cowlick at the crown; not platinum, not flat, not a clean helmet.
- Skin: fair and warm, with light stubble across the jaw and upper lip.
- Build: a grown man, athletic, head-to-body about 1 to 7.
- Expression baseline: an easy, closed-mouth smile (change only when a step asks).
```

Why these and not more: every line is a distinctive marker, named once. There is deliberately no full-face prose description (it competes with the photo) and the nose is deliberately omitted from the lock (low identity value, safe to exaggerate later).

### BLOCK 2 — STYLE-LOGIC (the swappable slot, five fields)

This is the only block that changes between renders. Fill all five fields. Never put an artist's name here.

```
STYLE:
- Medium / substrate: <what it is physically made of and the surface it sits on>
- Mark-making / technique: <how the lines or marks behave>
- Palette rule: <the color discipline, stated as a rule, not a swatch>
- Register: <where it sits realistic -> stylized -> exaggerated; the caricature dial>
- Signature move: <the one treatment that makes this look read as itself>
```

#### Four worked examples (from the brainstorm top picks)

**A. Animator's pencil-test (your house anchor, the control)**
```
STYLE:
- Medium / substrate: graphite-and-ink drawing on warm cream paper with visible grain.
- Mark-making: confident graphite linework, fine cross-hatching for shadow, faint
  light-blue construction underdrawing left visible.
- Palette rule: monochrome graphite throughout, plus exactly ONE warm amber accent.
- Register: a wildly exaggerated, absurd cartoon caricature, never realistic.
- Signature move: a single soft amber watercolor bloom behind the head, sitting
  behind the linework, bleeding into the paper, never on top, never splatter.
```

**B. Charcoal life-study (tonal hand)**
```
STYLE:
- Medium / substrate: vine and compressed charcoal on toned gray newsprint.
- Mark-making: loose gestural strokes, smudged tonal masses, sharp eraser highlights,
  built from shadow shapes rather than outline.
- Palette rule: monochrome charcoal, no color at all.
- Register: grounded and expressive, lightly exaggerated, an observed life-drawing.
- Signature move: visible smudge and the rough torn edge of the newsprint.
```

**C. Mid-century flat / paper-cut (flat vector)**
```
STYLE:
- Medium / substrate: flat printed shapes, the look of cut-and-layered colored paper.
- Mark-making: clean hard-edged shapes, minimal interior detail, subtle paper texture
  inside each shape; features built from shape, not line.
- Palette rule: a strict limited palette of three or four muted, slightly retro colors.
- Register: simplified and geometric, stylized well away from realism.
- Signature move: bold negative space and one shape that overlaps another for depth.
```

**D. Risograph two-color (print)**
```
STYLE:
- Medium / substrate: a risograph print on off-white stock.
- Mark-making: grainy halftone dot shading, slight ink misregistration, visible
  paper texture.
- Palette rule: exactly two inks (one warm, one ink-dark), allowed to overlap into
  a third tone where they cross.
- Register: stylized and graphic, a touch exaggerated.
- Signature move: the deliberate off-register edge where the two ink layers do not
  quite line up.
```

The schema generalizes to any of the 70-plus styles from the brainstorm: fill the five fields, never reach for a name.

### BLOCK 3 — CONSTRAINTS / NEVER-DO (mostly constant)

```
CONSTRAINTS:
- Change only what the STYLE block names. Keep the face geometry, hair, and the
  features listed in SUBJECT exactly as in the reference. Re-read SUBJECT before drawing.
- Render fully in the named medium. Do not retain photographic shading, lighting,
  or texture from the reference; redraw it in the medium.
- No text, no words, no letters, no numbers, no captions, no labels, no logos,
  no watermarks, no signatures anywhere. Purely pictorial.
- Composition: a head-and-shoulders bust, facing the viewer, centered.
```

Note on negatives: the only safe negatives are **abstract artifacts** (text, watermark, signature). The "no text" exclusion is the one ChatGPT obeys reliably. Do **not** negative-list concrete objects ("no hoodie", "no glasses"): naming an object to exclude can summon it (the documented "pink elephant" negation problem). Positive-frame those instead ("a plain crew tee").

### The RENDER line (the per-step delta)

After the three blocks, add one line naming only what this specific step changes. This is the "only change X" idiom that keeps a swap from leaking into identity.

```
RENDER: <e.g. "3/4 profile, looking off to the left"> ... change only this; keep
everything in SUBJECT and CONSTRAINTS the same.
```

---

## Part 3 — The caricature dial (the register field, operationalized)

Drop these into the **Register** field of Block 2. The dial only ever moves the 2 to 3 most distinctive features (for Sean: the **brow**, the **cowlick**, the **jaw**). It never moves the locked configural spacing, the eyes, or the hair color.

- **Step 0, grounded:** "proportions true to the reference, a faithful likeness."
- **Step 1, cartoon (the sweet spot):** "a cartoon caricature: exaggerate his most distinctive features (the strong brow, the crown cowlick, the angular jaw) by a moderate amount; leave average features alone; keep him clearly recognizable."
- **Step 2, absurd (past peak):** "a wildly exaggerated, absurd caricature: push the brow, cowlick, and jaw hard, but hold the eye-spacing, the face proportions, and the hair so it is still unmistakably him."

The decisive house move ("push the caricature, never make it more realistic") is Step 1 to Step 2. The research says likeness survives that push only while the locked features hold, which is exactly why the dial and the lock are separate blocks.

---

## Part 4 — Edit vs generate: the decision rule

You weighed both equally. Use this to pick per render, and run both on at least a few styles so the matrix shows you where "good" lives.

| Situation | Path | Why |
|---|---|---|
| Likeness is the priority; realistic to mid register | **Edit-from-photo** | The photo pins identity; gpt-image-2's automatic high-fidelity input does the work. |
| Heavy stylization, flat/vector/pixel, or large structural change | **Generate-from-description** (Block 1 markers carry identity) | A photographic reference fights a flat or abstract look; the named markers travel better. |
| You want maximum likeness inside a stylized look | **Hybrid:** edit-from-photo, then push the register hard in text | Start from the face, then force the medium so the photo's realism does not leak. |
| Producing many frames of one locked style | Edit, re-anchored each time | Consistency without a trained model. |

Two rules that apply to **both** paths:
- **Re-anchor, never chain.** For each new style, point back to the original headshot, not the last stylized output. Drift compounds after a handful of chained edits.
- **Repeat the load-bearing constraint twice.** GPT silently revises prompts, so state the medium and the lock once up top and once in CONSTRAINTS so the revision cannot drop it.

---

## Part 5 — The morph matrix (run this on the Mac)

The experiment that produces "what good looks like." Hold Block 1 and Block 3 constant. Swap Block 2 across styles. Where useful, run the same style on both paths. Save every output (and every reroll) numbered, with a one-line note on what you changed, exactly per the capture discipline in the capture plan.

**Run plan:**
1. Open one ChatGPT thread. Upload the headshot.
2. Establish with the pencil-test style block (A) as the control, edit path.
3. For each subsequent style (B, C, D, then any others from the brainstorm), paste the **same Block 1 + Block 3**, swap in the new Block 2, re-anchor to the headshot.
4. For 2 or 3 styles, also run the **generate path** (no photo, Block 1 markers only) to compare.
5. For your 2 or 3 finalists, run the **caricature dial** (Step 0, 1, 2) to find where likeness survives exaggeration.

**Score every cell on the "good" rubric (Part 6).** The pattern across the matrix is the answer.

**Starter style blocks to paste** (beyond A to D above), as five-field fills:
- **Woodblock relief:** carved black ink / bold reductive cuts with visible grain / black on cream, one spot color / stylized and graphic / the chunky hand-carved edge.
- **Blueprint schematic:** white line on cyan ground / thin technical linework with callout ticks / cyan and white only / clean and diagrammatic / faint construction guides as if drafted.
- **Stained glass:** leaded glass panel / bold black lead lines enclosing flat color cells / jewel tones in segments / stylized and iconic / light glowing through the glass.
- **16-bit pixel sprite:** pixel art on a grid / hard pixel edges with ordered dithering / a tight limited palette / heavily stylized, low resolution / readable silhouette at small size (ties to 16BitFit).

---

## Part 6 — The "good" rubric (score each matrix cell 0 to 2)

A render is good only when all three hold. Scoring every cell is how you turn the matrix into the method.

1. **Likeness holds** (0 to 2): is it recognizably Sean without a caption? Check the brow, eye-spacing, jaw, cowlick, hair color.
2. **A hand shows** (0 to 2): does it read as a deliberate style with logic (real mark-making, a palette rule, restraint), not a default the model reaches for?
3. **Ownable** (0 to 2): could a stranger get here by typing "make it artistic"? If yes, score low. The gap between a real method and a lazy prompt is the whole point of the post.

Cells that score 5 to 6 are the shortlist. The five-field fills and the path and the dial position that produced them **are the step-by-step** the post teaches.

---

## Part 7 — How the matrix reverse-engineers into the post

This closes the loop back to the capture plan. Once the matrix is scored:
- The **winning five-field fills** show which fields did the work for each style. That is the evidence for "name the style as logic," and it populates the reader's **Taste Rubric** slots (medium, mark-making, color rule, register, signature move map one-to-one).
- The **path that won per style** (edit vs generate) becomes a line in the move ladder: "feed the photo for these looks, describe yourself for those."
- The **dial position** that held likeness becomes the "push the caricature, here is how far" beat.
- The **rerolls and claw-backs** are the honest texture (the revert-to-average, fought in public).

So the deliverable order is: run the matrix, score it, then write the move ladder *from what actually happened*, which is the project's "write from the build" rule.

---

## Stale-risk flags (re-verify before you lean on these)

- **Model name and defaults churn fast.** gpt-image-2 is current; OpenAI shipped four image models in about 14 months. Re-confirm the live model string before relying on a specific behavior.
- **`input_fidelity` is locked-high on gpt-image-2 but was a tunable knob on older models.** If ChatGPT swaps the backing model, the automatic high-fidelity input could change.
- **No seed today.** If OpenAI adds seed/style-locking, the "engineer for re-anchoring" advice gets a cheaper alternative.
- **The living-artist policy line moves.** Studio styles are allowed, individual living artists blocked, as of early 2025, and OpenAI said it would keep refining. The visual-logic approach sidesteps this entirely, which is the point.
- **The 3-to-6 reference sweet spot and the ~87% same-thread consistency figure are strong third-party heuristics, not official benchmarks.** Treat as directional.
- **Cross-tool numbers** (Midjourney `--cw`, omni-strength, IP-Adapter ~0.6, Nano Banana ~6 high-fidelity refs) are version- and checkpoint-specific.

---

## Sources

Tool mechanics and prompting (OpenAI):
- OpenAI GPT Image prompting guide: https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- OpenAI image generation API guide: https://developers.openai.com/api/docs/guides/image-generation
- ChatGPT Images 2.0 announcement: https://openai.com/index/introducing-chatgpt-images-2-0/
- DALL-E 3 system card (artist-name substitution): https://openai.com/index/dall-e-3-system-card/

Likeness, references, cross-tool:
- Nano Banana Pro character-consistency guide (reference-count sweet spot): https://prompting.systems/blog/nano-banana-pro-character-consistency-guide
- Google Cloud Nano Banana prompting guide (role-tagging, positive framing): https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana
- Identity-vs-style tradeoff survey: https://arxiv.org/pdf/2502.13081
- Midjourney character reference docs: https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference

Style as logic, policy, mechanism:
- OpenAI safeguards / living-artist line (TechCrunch, Mar 2025): https://techcrunch.com/2025/03/28/openai-peels-back-chatgpts-safeguards-around-image-creation/
- Local Prompt Adaptation (content vs style tokens are separable): https://arxiv.org/abs/2507.20094

Caricature and face-identity:
- Rhodes, Brennan & Carey 1987 (caricature effect): https://www.sciencedirect.com/science/article/pii/0010028587900168
- Sadr, Jarudi & Sinha 2003 (eyebrows): https://web.mit.edu/sinhalab/Papers/sinha_eyebrows.pdf
- Peak shift in face recognition: https://www.researchgate.net/publication/232918637_Are_Caricatures_Special_Evidence_of_Peak_Shift_in_Face_Recognition

Negation / prompt structure:
- "Do Not Think About Pink Elephant" (CVPR 2024, negation problem): https://arxiv.org/abs/2404.15154

Internal fleet (your own solved pattern):
- anima five-slot consistency template: `anima/docs/research/2026-05-30-nb2-editing-character-consistency-template.md`
- anima prompt style-neutrality doctrine: `anima/docs/architecture/prompt-style-neutrality-doctrine.md`
- sean-anchor identity rules + palette: `anima/characters/sean-anchor/{acceptance_criteria.json,character.yaml}`
- openai-image-gen skill: `code-brain/.claude/skills/openai-image-gen/`
