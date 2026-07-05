# Pencil & Prompt — About page "Matched-Angle Appetite" prompts (2026-06-27)

The autobiographical hero for the **About** page: a matched-cut that makes the appetite spine literal.
Same camera, two times in one life. The kid mainlining cartoons becomes the adult mainlining model
output, and the only constants are the hunched, rapt posture and the pencil. Loops with the About
closer ("grab a bowl of cereal and pull up a spot on the floor").

House style is the same as the mascot doc (`pencil-and-prompt-mascot-prompts.md`): pencil-test +
watercolor, cream paper, ONE accent, no text. This is NOT the Pencil + Intern duo. The subject is Sean.

---

## How to use this

1. **Engine:** `openai-image-gen` (GPT Image 2, `--quality high`) or ChatGPT image gen. Image gen can't
   run in Cowork, so run these on your Mac.
2. **Identity anchor (one only):** feed the hand-drawn Sean pencil character as the single `--reference`
   so the adult reads as you and the medium stays on-model: `sw-ai-pm-portfolio/reference-images/2D-Character-Sketch-Sean-v1.png`
   (or `anima/characters/sean-anchor/anchor.png`). One anchor only; the kid is just a younger, huskier
   version of the same character. Multiple anchors muddy the style.
3. **The match is the whole point.** Panels 1 and 2 MUST share the exact camera: locked, low, close,
   shot from BEHIND the subject, head-and-shoulders lower-center, the glowing screen upper-center. Only
   the contents change (TV -> wall of monitors, kid -> adult, cereal+notebook on the carpet -> mugs+desk
   clutter, pencil on the floor -> pencil behind the ear). If a render drifts the framing, re-prompt
   "keep the identical camera angle and composition as the first image," and feed Panel 1 as a second
   reference when generating Panel 2.
4. **Accent:** amber in BOTH panels (the screen glow). Keep it amber across the pair so they read as one
   shot across time. One accent per image, never two.
5. **No text.** Screens show only an illegible abstract glow, never readable letters. If a render returns
   legible text/code/logos: "replace all screen content with an abstract illegible glow, no letters,
   words, or numbers anywhere."
6. **Stiff render? Crank the caricature** ("more exaggerated and absurd"), never "more realistic." Other
   dials: "warmer bloom," "heavier construction lines," "more rapt, hunched-forward posture."
7. **Lock it.** Once Panel 1 is right, save it and feed it as the reference for Panel 2 so build, posture,
   and framing carry over.

---

## Shared house-style preamble (paste at the top of every prompt below)

```
A hand-drawn pencil-and-ink illustration on warm cream paper (#FFF9F0), animator's pencil-test feel:
graphite linework, fine cross-hatching, faint light-blue construction underdrawing left visible, warm
paper grain, hole-punch marks along one margin. Wildly exaggerated, absurd cartoon caricature, never
realistic. Shot from BEHIND the subject so we see the back of the head and shoulders, camera locked
low and close, the figure silhouetted against the glow of the screen in front of them.
```

---

## PANEL 1 — The kid (the cold open)

```
[paste shared house-style preamble]

SCENE: a husky young boy sits cross-legged on a living-room carpet, seen from behind, three feet from
a boxy old static TV that fills his view. An extra-large bowl of cereal sits in his lap. A single
yellow No. 2 pencil and an open sketch notebook lie on the carpet beside him. The TV throws a warm glow
over the back of him; its screen shows only an abstract, illegible blur of Saturday-morning-cartoon
shapes, no readable text. His posture is rapt, hunched forward, completely absorbed. Exaggerated
caricature, faint blue construction lines visible.

ONE restrained warm amber accent, the TV's glow, plus a single soft amber watercolor bloom behind the
TV that bleeds into the cream paper. The wash sits BEHIND the linework, never splatter.

Landscape 16:9, the boy's head-and-shoulders lower-center, the glowing TV upper-center. No text, words,
letters, numbers, or logos anywhere. Purely pictorial.
```

## PANEL 2 — The adult (same angle, years later)

```
[paste shared house-style preamble]
[also feed the approved Panel 1 as a reference so framing + build carry over]

SCENE: the EXACT same camera and composition as Panel 1, years later. The same person, grown, same
husky build, sits in the same hunched, rapt, totally-absorbed posture, seen from behind, but now facing
a wall of several glowing computer monitors instead of the TV. A yellow No. 2 pencil is tucked behind
his ear. The desk is cluttered with coffee mugs and loose paper. The monitors show only abstract,
illegible glowing panels of code-like scribbles and little busy shapes (agents at work), no readable
text. Exaggerated caricature, faint blue construction lines visible.

ONE restrained warm amber accent, the monitors' glow, plus a single soft amber watercolor bloom behind
the screens. Behind the linework, no splatter.

Landscape 16:9, framing IDENTICAL to Panel 1 (head-and-shoulders lower-center, glowing screens
upper-center) so the two images cut or cross-fade cleanly. No text, words, letters, numbers, or logos
anywhere. Purely pictorial.
```

---

## SINGLE-IMAGE DIPTYCH — if you want one static hero instead of a pair

```
[paste shared house-style preamble]

SCENE: a single illustration split into two side-by-side panels sharing one cream sheet, same camera
height and distance in both halves so the eye reads them as the same shot across time. LEFT PANEL: the
husky boy from behind, cross-legged on the carpet, cereal bowl in his lap, a yellow pencil and open
notebook beside him, three feet from a glowing boxy static TV. RIGHT PANEL: the same person grown, same
from-behind hunched posture, a yellow pencil behind his ear, facing a wall of glowing monitors at a
cluttered desk. Both screens show only illegible abstract glow (cartoon shapes on the left, code-like
scribbles on the right), no readable text. Exaggerated caricature, faint blue construction lines in both.

ONE warm amber accent, the screen glow in both panels, plus a soft amber watercolor bloom behind each
screen. Behind the linework, no splatter.

Landscape 16:9 overall, a thin hand-drawn vertical gutter line between the two panels. No text, words,
letters, numbers, or logos anywhere. Purely pictorial.
```

---

## Making it loop (the transition video)

- Generate Panel 1 and Panel 2 with identical framing, then in any editor do a slow cross-dissolve or a
  hard match-cut between them. Because only the screen, the age, and the props change, the cut lands.
- For a fancier morph, generate 2-3 in-between stills (same camera) where the TV widens into the monitor
  wall and the boy "grows" into the adult, then tween. Keep the pencil on-screen the whole time as the
  one prop that never leaves (childhood pencil on the carpet -> pencil behind the ear).
- Pair it with the closer line on the page so the loop and the words rhyme.

## Dials to play with

- **Caricature:** "more exaggerated and absurd" (fix for stiff). Never "more realistic."
- **The pencil is the brand match-prop:** keep the same yellow No. 2 pencil visible in both panels (on
  the carpet as a kid, behind the ear as an adult). It is the literal "Pencil" of Pencil & Prompt.
- **Posture is the match, not the face:** "rapt, hunched-forward, totally absorbed" in both. The
  from-behind angle means you never need facial likeness.
- **Optional mascot Easter egg:** in Panel 2, "tiny terminal-headed pixel-faced intern figures busy
  inside the monitor glow" ties the autobiographical shot to the brand mascots. Optional, keep it subtle.
- **Accent:** amber in both for unity. (Teal would techify Panel 2, but it breaks the pair, so stick to
  amber.)
- **Construction lines:** keep them faint-blue and visible in both; the pencil-test tell that reads as
  "still being drawn."
```
