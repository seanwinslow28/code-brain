---
type: design-doc
artifact: substack-image-generation-pipeline
created: 2026-05-23
updated: 2026-06-10
status: v2 — supersedes the v1 Steadman/voice-mode design
ai-context: |
  v2 (2026-06-10) replaces the entire v1 design. v1 mapped Sean's 5 voice modes to 5
  Ralph Steadman ink-splatter aesthetics. Both halves are now dead: (1) the Steadman
  "deliberate ink splatter and drips" IS the "ink blotting" Sean dislikes; (2)
  writing-voice-modes is no longer 5 equal modes — it is Sean Mode (90%) + 4 borrowed
  techniques (10%), so there is no 5-aesthetic mapping to make. v2 adopts the
  seanwinslow.com portfolio pencil-test look as a single house style with one accent
  color per post and a minimal watercolor wash. v1 is preserved in git history.
related:
  - "[[.claude/skills/gemini-pencil-animation-image-gen/SKILL]]"
  - "[[.claude/skills/writing-voice-modes/SKILL]]"
  - "_assets/style-anchors/portfolio-pencil-anchor-prompts.md"
---

# Substack Image House Style — v2 ("Pencil Test, Pinned to the Page")

## What changed from v1 (read this first)

v1 (2026-05-23) was a Ralph-Steadman-gonzo pipeline: india-ink + watercolor + **deliberate
splatter**, with a different reference image and ink density per voice mode. It is retired
for two reasons:

1. **The splatter was the problem.** "Deliberate ink splatter and drips running off the
   page" is the *ink blotting* that never sat right. Sean's actual taste is the calm,
   precise pencil-test look on his portfolio — zero splatter.
2. **Voice-modes changed.** The skill is now Sean Mode (90%) + four borrowed techniques
   (10%), not five equal identities. Mapping "Sedaris → sepia, Thompson → acid neon" has
   no foundation left. There is **one house style**, not five.

The four Steadman reference images are archived at
`vault/.../substack-drafts/_archive/steadman-refs-deprecated/`. The new anchors are Sean's
three portfolio illustrations (recipes saved at
`_assets/style-anchors/portfolio-pencil-anchor-prompts.md`).

## The house style

The look is the portfolio's: **an animator's pencil test, mounted in a frame.** Every
Substack hero is the same hand.

### Constants (never vary — this is the consistency engine)

1. **Substrate:** warm cream paper `#FFF9F0`, visible paper grain, hole-punch marks along
   one margin (the binder / pencil-test framing — signals hand-made, in-process, real).
2. **Medium:** graphite + ink linework, fine cross-hatching for shadow, **faint light-blue
   construction underdrawing left visible** (the "show the work" tell that makes it read as
   a pencil test, not a finished render).
3. **Monochrome + exactly ONE accent color** that carries the meaning. Everything else is
   grayscale graphite. Never two accents in one image.
4. **The watercolor accent** (see below): one soft bloom of the accent color, behind the
   focal point, sitting behind the linework.
5. **No text in the art.** Purely pictorial. Titles/captions live in Substack's title
   field. (One exception: the grotesque sub-format below, where the cheesy caption IS the
   joke.)

**Consistency comes from the MEDIUM (1–4), not from a recurring character or composition.**
Every hero is the same *hand* — never the same *scene*. The portfolio's blob-baby agents and
amber thread are the **portfolio home page's** motif, not a Substack fixture. They appear in a
Substack hero ONLY when a post is actually about the agent fleet (e.g., Post 6). Importing
them onto a post they have nothing to do with is the exact mistake to avoid.

**Figure register: WILDLY exaggerated, absurd cartoon caricature — not realistic** (locked
2026-06-10 on the Post-1 trials). The people are pushed-as-far-as-they-go silly caricatures —
oversized heads, rubbery over-the-top features, extreme comic expressions — rendered *in* the
pencil-test medium (graphite, cross-hatching, blue construction lines), never realistic or
photorealistic. The medium is serious; the characters are absurd.

> **Iteration finding (Post 1, 2026-06-10):** the dial landed in three steps —
> realistic figures (flat) → "more cartoonish and silly" (closer) → **"more exaggerated and
> absurd"** (the winner). Bake "wildly exaggerated, absurd" into the *base* prompt so a first
> run lands there directly instead of needing the follow-up edit. When a render feels stiff,
> the lever is always "push the caricature further," never "make it more realistic."

### The watercolor element (LOCKED: minimal)

A soft accent-color **watercolor bloom that sits BEHIND the pencil linework**, bleeding into
the cream paper. One bloom, placed where the meaning/light lives (behind whatever the
concept's focal point is). Wet-on-dry, controlled, calm. **Never splatter, never on top of
the ink, never gonzo.** This is the clean replacement for v1's drips. (We can dial up to
corner-blooms later if it reads too sparse; minimal is the default.)

### Concept comes from the post (the most important rule)

The medium is shared; the **idea is bespoke to each post.** Read the draft, find its single
sharpest image or metaphor, and render THAT in the pencil-test medium. Don't reach for a
stock composition.

Method: **post → one sentence naming its sharpest visual → that is the SCENE.**

| Post | Sharpest image in the story | Candidate hero concept |
|---|---|---|
| 1 · Can't Prompt Taste | "a confident stranger wearing my face" | LOCKED: the rough, honest pencil character meets a glossy motivational-poster impostor of himself in a part-mirror-part-screen; the drawing-style contrast (rough graphite vs. too-smooth) is the thesis. No desk, no blobs, no thread. |
| 7 · Judgment Layer | the bouncer at the door of "save" | a small figure turning a glossy output away at a threshold |

Examples, not a menu. Derive each post's own.

### The variation axis (replaces voice-modes): one accent color per post

| Accent | Use for | Hex |
|---|---|---|
| **Amber** (default) | Warm / human / personal / human-in-the-loop posts | `#B45309` |
| **Teal** (technical alt) | System / control-layer / thesis posts | `#0A3E42` |

One accent per image, never both. The **scene** changes to the post's subject; the
**medium** never changes.

Per-post assignment:

| Post | Accent | Why |
|---|---|---|
| 1 · Can't Prompt Taste | amber | personal, voice, human |
| 2 · Machine to Sound Like You | amber | personal, voice |
| 3 · Correct Was Never Defined | teal | intent/system layer |
| 4 · Eval Tools Wrong People | teal | eval/system |
| 5 · Content Tripled | amber | human cost of slop |
| 6 · Stop Building Agents | teal | agent architecture |
| 7 · The Judgment Layer | teal | the control-layer thesis |
| bonus · Vault Said Nothing | amber | the lonely-night discovery |

### The grotesque sub-format (one hand, when satire calls for it)

The cheese-bank's "cheesy caption + grotesque image" satire survives — but rendered **in the
pencil-test medium**, not as a separate glossy engine. A Ren & Stimpy-grade grotesque (e.g.,
a hustle-guru) drawn in graphite on the same cream paper, with the cheesy caption as the one
licensed place text appears (the caption is the joke). Same substrate, same accent, same
hand. Reserve it for posts that are explicitly satirical; the default hero is the elegant
pencil-test scene, not the grotesque.

## Engine

OpenAI GPT Image 2, via the **`openai-image-gen`** skill — the same engine family that
produced the three portfolio anchors Sean loves, and the validated Substack-header engine.
The pencil-test style names no artist, so there is no safety-filter issue (the v1 reason for
forcing Nano Banana is gone).

- **Primary (scriptable): `openai-image-gen`** — `.claude/skills/openai-image-gen/scripts/generate_image.py`,
  model `gpt-image-2`, needs `OPENAI_API_KEY` in `.env`. Pass ONE style anchor with
  `--reference` to route through `images.edit` and inherit the pencil-test look; use
  `--quality high` when the scene carries fine detail.
- **Manual: ChatGPT image gen** (same OpenAI family) — paste the recipe and iterate
  conversationally when you'd rather work in the web UI.
- **Retired:** the grotesque Nano Banana path that produced the outputs Sean rejected, plus
  the v1 Steadman / `gemini-image-gen` routing.

> Note: image generation cannot run inside Cowork (the sandbox is firewalled off the image
> APIs). Generate on the Mac.

## Style anchors

| Anchor | What it locks | Where |
|---|---|---|
| The 3 portfolio illustrations (desk-kid, spear-warrior, trader) | the overall look | drop the PNGs at `_assets/style-anchors/` (Mac-side); recipes saved alongside |
| `2D-Character-Sketch-Sean-v1.png` | the blob-baby character | `sw-ai-pm-portfolio/reference-images/` |
| `portfolio-pencil-anchor-prompts.md` | the exact phrasing that worked | `_assets/style-anchors/` |

Feed exactly ONE anchor image as a reference per generation. Multiple references muddy the
style.

## The master prompt recipe

Fill the `{BRACKETS}`. Keep the constants verbatim — they are doing the consistency work.

```
A hand-drawn pencil-and-ink illustration on warm cream paper (#FFF9F0), animator's
pencil-test feel: graphite linework, fine cross-hatching, faint light-blue construction
underdrawing left visible, warm paper grain, hole-punch marks along one margin.

SCENE: {THE BESPOKE CONCEPT, DERIVED FROM THE POST — one or two sentences naming the subject,
the action, and the setting}.

Monochrome graphite and ink throughout, with ONE restrained {ACCENT} accent on {THE ELEMENT
THAT CARRIES THE MEANING}, plus a single soft {ACCENT} watercolor bloom behind {THE FOCAL
POINT} that bleeds into the cream paper. The watercolor wash sits BEHIND the linework, never
splatter, never on top.

Landscape 16:9 for a Substack header, the focal subject centered in the safe zone. Absolutely
no text, no words, no letters, no numbers, no logos, no watermarks anywhere — purely
pictorial.
```

- `{ACCENT}` = `warm amber` (most posts) or `cool teal-cyan` (technical posts), per the table.
- `{SCENE}` is the **derived concept**, not a template — see "Concept comes from the post."
- Substack header ratio is **16:9 landscape** (`openai-image-gen` maps this to 1536×864; the
  portfolio's 4:5 is for on-page tiles, not headers). Compose wide; keep the focal subject in
  the center safe zone so the feed crop never cuts it.

## Workflow

1. Pull the post's accent from the table; write the one-sentence `{SCENE}`.
2. Fill the recipe; generate via `openai-image-gen` (primary) or ChatGPT (manual).
3. Iterate conversationally ("warmer bloom," "more construction lines," "calmer thread").
   Never restart from scratch.
4. Save to `01-…/images/hero.png` (and old versions to `images/_superseded/`).
5. Write `hero_image:` into the post's frontmatter.

## Migration / rollback

- v1 content is in git history (this file was overwritten 2026-06-10).
- Steadman refs: `_archive/steadman-refs-deprecated/` (restore if ever needed).
- The deprecated grotesque Post-1 prompt is replaced by the pencil-test version in
  `01-cant-prompt-taste/images/hero-prompt.txt`.
