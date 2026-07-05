# Pencil & Prompt — Mascot Prompt Playground (v1, 2026-06-23)

Prompts to play with for the **signature masthead motif**: the duo. Run them on your Mac
(GPT Image 2 via `openai-image-gen`, or the ChatGPT web app). Image gen can't run in Cowork,
so these are copy-paste fodder for you to experiment with and dial in.

House style is unchanged (pencil-test + watercolor, per `playbook/image-house-style.md`).
What's new here is a **recurring brand character**, a deliberate layer on top of the
medium-only consistency the house style usually relies on.

---

## How to use this

1. **Engine:** `openai-image-gen` (GPT Image 2, `--quality high`) or ChatGPT image gen. Feed
   **one** style anchor (a portfolio pencil illustration) with `--reference` so it inherits the
   look. One anchor only; multiple muddy the style.
2. **Iterate, never restart.** When a render is stiff, the lever is always **"crank the
   caricature, more exaggerated and absurd,"** never "make it more realistic." Other dials:
   "warmer bloom," "heavier construction lines," "goofier pixel face."
3. **Accent:** amber is the default (warm, human, inviting to a skeptic). One variant below is
   teal so you can compare. **One accent per image, never two.**
4. **Aspect:** generate the masthead at **16:9** (Substack header) and a **1:1** crop for the
   avatar / Notes. Variant 6 is built square.
5. **The shirt-emblem exception + warning.** House style says no text in the art. The only
   exception here is the small emblem on the intern's shirt, and even that should be a **simple
   hand-drawn shape (a four-point sparkle / sunburst), not real lettering or a real brand logo.**
   Image models reliably botch literal text and logos. If a render returns gibberish letters,
   re-prompt: "replace any lettering with a single simple drawn sparkle, no text."
6. **Lock it as an anchor.** Once you get a duo you love, save that PNG as the mascot style
   anchor and feed IT as the reference for future generations, so the characters stay on-model
   (same Character-Bible logic as the pipeline).

---

## The two characters (keep these consistent across every prompt)

**THE PENCIL (mentor, the "taste" half).** A tall anthropomorphic No. 2 wooden pencil standing
upright, sharpened graphite tip, slightly chewed pink eraser for a head-top, two thin rubber-hose
arms, small round wire-frame glasses, a few expressive eyebrow strokes, the patient bemused air
of a veteran art teacher who has seen every bad first draft.

**THE INTERN (the "prompt"/machine half, the apprentice).** A short and chubby, overeager apprentice whose
HEAD is a boxy retro computer terminal / CRT monitor with a blocky pixel face (wide pixel eyes, a
little pixel mouth, a blinking block cursor), on a short and chubby cartoon human body with
too-big sneakers, wearing an oversized graphic tee with a small drawn sparkle emblem on the chest
(a wink at AI assistants). Eager, clueless, trying way too hard. **Its faint blue construction
lines still show, because it isn't finished being taught yet.**

---

## DUO PROMPTS (the masthead motif)

### V1 — Mentor-and-apprentice portrait (the iconic masthead)

```
A hand-drawn pencil-and-ink illustration on warm cream paper (#FFF9F0), animator's pencil-test
feel: graphite linework, fine cross-hatching, faint light-blue construction underdrawing left
visible, warm paper grain, hole-punch marks along one margin. Wildly exaggerated, absurd cartoon
caricature, never realistic.

SCENE: a posed two-character portrait. A tall anthropomorphic wooden pencil with small round
glasses and thin rubber-hose arms stands beside a much-taller, gangly apprentice whose head is a
boxy retro computer terminal with a goofy wide-eyed pixel face on a lanky human body in too-big
sneakers and an oversized tee with a small drawn sparkle emblem. The pencil reaches up to rest one
arm on the intern's shoulder like a proud mentor; the intern grins a dopey pixel grin and clutches
a crayon-clumsy first drawing. Both face the viewer. The intern's blue construction lines still show.

Monochrome graphite and ink throughout, with ONE restrained warm amber accent on the intern's
glowing screen-face and the pencil's graphite tip, plus a single soft amber watercolor bloom behind
the pair that bleeds into the cream paper. The watercolor sits BEHIND the linework, never splatter.

Landscape 16:9 for a Substack header, the duo centered in the safe zone. No text, words, letters,
numbers, or real logos anywhere, EXCEPT the single simple drawn sparkle on the shirt. Purely pictorial.
```

### V2 — The lesson (thesis in action)

```
[same house-style preamble as V1]

SCENE: an art lesson. The glasses-wearing anthropomorphic pencil stands on a stack of books,
pointing a stern little arm at a big easel where the terminal-headed intern has drawn a generic,
soulless smiley-face blob, the exact same-y AI thing. The lanky intern stands sheepish beside it,
scratching its boxy head, a little spinning "loading" wheel hovering over it as a thought bubble.
Construction lines still visible on the intern.

Monochrome graphite and ink, ONE warm amber accent on the soulless easel drawing and the loading
spinner, plus a soft amber watercolor bloom behind the easel. Wash behind the linework, no splatter.

Landscape 16:9, no text or logos except the simple drawn sparkle on the intern's shirt. Purely pictorial.
```

### V3 — Over-the-shoulder direction (teal comparison)

```
[same house-style preamble]

SCENE: the terminal-headed intern hunched at a cluttered drawing desk mid-scribble, tongue-out
concentration on its pixel face; the glasses-wearing pencil perched on the desk edge leaning in
over its shoulder, gesturing at the page giving notes. Eraser shavings, stray pencils, a chewed
coffee cup. Both rendered as absurd caricatures. Construction lines on the intern.

Monochrome graphite and ink, ONE restrained cool teal-cyan accent on the screen-face glow and the
desk lamp, plus a single soft teal watercolor bloom behind the desk. Behind the linework, no splatter.

Landscape 16:9, no text or logos except the simple drawn sparkle on the shirt. Purely pictorial.
```

### V4 — Crank the absurd (max silly)

```
[same house-style preamble]

SCENE: glorious chaos. The terminal-headed intern has drawn the SAME generic smiley blob a dozen
times and taped every copy to the wall behind it; it sweats, pixel eyes spinning out of sync, arms
full of more identical drawings. The glasses-wearing pencil face-palms with one rubber-hose arm,
glasses knocked askew, utterly exasperated. Pushed-as-far-as-it-goes caricature. Intern construction
lines visible.

Monochrome graphite and ink, ONE warm amber accent on the wall of identical blobs, plus a soft amber
watercolor bloom behind the wall. Wash behind the linework, no splatter.

Landscape 16:9, no text or logos except the simple drawn sparkle on the shirt. Purely pictorial.
```

### V5 — The handoff (a nod to "Take Two")

```
[same house-style preamble]

SCENE: the glasses-wearing pencil hands the terminal-headed intern a fresh blank sheet of paper like
a relay baton; the lanky intern reaches for it with both hands, pixel face lit up with hope, mid-motion.
A clumsy crumpled first draft lies discarded at their feet. Both absurd caricatures, intern's
construction lines showing.

Monochrome graphite and ink, ONE warm amber accent on the fresh sheet of paper changing hands, plus a
soft amber watercolor bloom behind the handoff. Behind the linework, no splatter.

Landscape 16:9, no text or logos except the simple drawn sparkle on the shirt. Purely pictorial.
```

### V6 — Square avatar / Notes mark (tight brand face)

```
[same house-style preamble]

SCENE: a tight bust portrait, the terminal-headed intern's boxy screen-head and shoulders fill the
frame wearing the sparkle-emblem tee, goofy hopeful pixel face; the glasses-wearing pencil leans into
frame from the side, one arm resting on the intern's shoulder. Intern construction lines visible.

Monochrome graphite and ink, ONE warm amber accent on the screen-face glow, plus a soft amber
watercolor bloom behind the heads. Behind the linework, no splatter.

Square 1:1 for an avatar, subjects centered. No text or logos except the simple drawn sparkle on the
shirt. Purely pictorial.
```

---

## FALLBACK PROMPTS — the lone Intern (motif A)

Use these if the duo gets too busy and you want the single-character mascot instead.

### F1 — Intern solo, holding its first draft

```
[same house-style preamble]

SCENE: the gangly apprentice alone, head a boxy retro terminal with a wide-eyed hopeful pixel face,
lanky human body in too-big sneakers and a sparkle-emblem tee, proudly holding up a crayon-clumsy,
soulless first drawing for approval. Eager and clueless. Faint blue construction lines still show.

Monochrome graphite and ink, ONE warm amber accent on the screen-face and the held-up drawing, plus a
soft amber watercolor bloom behind the figure. Behind the linework, no splatter.

Landscape 16:9 (and try a 1:1 crop), figure centered. No text or logos except the simple drawn sparkle
on the shirt. Purely pictorial.
```

### F2 — Taste being transferred (the "ghost hand")

```
[same house-style preamble]

SCENE: the terminal-headed intern at a desk drawing, and a faint translucent graphite "ghost hand"
(an unfinished pencil sketch of a guiding hand) gently steers its hand across the page, taste being
handed over. The intern's pixel face is calm, finally getting it. Construction lines on the intern,
the ghost hand even rougher and more sketch-like.

Monochrome graphite and ink, ONE warm amber accent on the line the intern is drawing, plus a soft amber
watercolor bloom behind the desk. Behind the linework, no splatter.

Landscape 16:9, no text or logos except the simple drawn sparkle on the shirt. Purely pictorial.
```

### F3 — Hopeful thumbs-up

```
[same house-style preamble]

SCENE: the terminal-headed intern facing the viewer giving an enthusiastic two-thumbs-up, dopey
hopeful pixel grin, sparkle-emblem tee, one single soulless smiley-blob drawing crumpled at its feet.
Absurd caricature. Construction lines visible.

Monochrome graphite and ink, ONE warm amber accent on the screen-face, plus a soft amber watercolor
bloom behind the figure. Behind the linework, no splatter.

Square 1:1 for an avatar, figure centered. No text or logos except the simple drawn sparkle on the
shirt. Purely pictorial.
```

---

## MEDIUM-FLEX SECTION PROMPTS (the mascot per craft lane)

For **section headers and recurring brand moments**, not per-post Take Two heroes (those stay
bespoke, the real soulless→art piece, per `image-house-style.md`). Each uses the **same house-style
preamble and the same two-character spec** above; only the SCENE changes. Amber default; swap to teal
for the techier lanes if you like. Keep the intern's construction lines showing.

### Writing lane

```
SCENE: the short, stout terminal-headed intern hunched over a clattering old typewriter, pecking the
keys with stubby fingers, tongue-out concentration on its pixel face, a small drift of crumpled bad-prose
pages around its big sneakers. The glasses-wearing pencil leans on the typewriter carriage reading the
page coming out, one eyebrow raised, unimpressed. ONE warm amber accent on the page in the typewriter
plus a soft amber bloom behind it.
```

### Animation lane (a nod to anima: timing is the human's job)

```
SCENE: the terminal-headed intern at an animation light-table / disc, flipping a thick stack of drawing
paper into a flipbook, faint motion-smear lines trailing off the pages, delighted pixel grin. The
glasses-wearing pencil stands beside it holding up a little stopwatch, calling the timing like a
director. ONE warm amber accent on the glowing light-table plus a soft amber bloom behind the desk.
```

### Music lane

```
SCENE: the short, stout terminal-headed intern fumbling an acoustic guitar far too big for it, pixel
face mid-wince on a sour note, a couple of sheet-music pages fluttering down. The glasses-wearing pencil
perches on a stool conducting with a tiny baton and a patient grimace. ONE warm amber accent on the
guitar's sound hole plus a soft amber bloom behind the pair.
```

### Design lane (the "stop it with these damn gradients" gag)

```
SCENE: the terminal-headed intern proud at a drafting table showing off a poster mockup that is pure
generic, same-y gradient mush; the glasses-wearing pencil jabs one rubber-hose arm at the gradient,
exasperated. A clean hand-drawn alternative sits ignored to the side. ONE cool teal-cyan accent on the
gradient mockup plus a soft teal bloom behind the table.
```

### Generic "any lane" placeholder

```
SCENE: the duo working together at a shared table, the glasses-wearing pencil directing while the short,
stout terminal-headed intern leans in eager to learn, a fresh blank page between them ready for whatever
the post is about. ONE warm amber accent on the blank page plus a soft amber bloom behind them.
```

---

## Dials to play with (the wording knobs)

- **Caricature:** "more exaggerated and absurd" (the fix for stiff). Never "more realistic."
- **Accent:** `warm amber` (default) ↔ `cool teal-cyan` (technical). One only.
- **The emblem:** keep it "a single simple drawn sparkle / four-point sunburst." If it renders as
  gibberish text, add "no lettering anywhere, replace with one simple drawn sparkle."
- **Pencil:** glasses on/off; tiny legs vs floating gloved hands; mustache for extra-professor.
- **Pixel face:** wide-eyed eager / sheepish / spinning-loading / blank-and-clueless.
- **Composition:** posed portrait (masthead) vs a scene (the lesson, the chaos).
- **Running gag:** the clumsy generic first-draft blob is the "no taste yet" proof, keep reusing it.
- **Construction lines:** "let the blue construction lines show" is the tell that reads as pencil-test
  AND doubles as "the intern isn't finished being taught." Lean on it.
```
