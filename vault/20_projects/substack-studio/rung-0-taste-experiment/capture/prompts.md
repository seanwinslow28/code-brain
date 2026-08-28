# Rung 0 capture — the prompt set, as run

**Run date:** 2026-08-09. **Engine:** GPT Image 2 via Higgsfield CLI. **Cost:** 77 credits (both runs).
**Aspect:** 16:9, quality high, 2k, every round.

Post title (Sean, 2026-08-09): **"You don't know, until you know"**

Supersedes the taste-transfer-era set at
[`_archive/back-catalog/01-make-the-agents-taste-yours/surface-2-prompts.md`](../../_archive/back-catalog/01-make-the-agents-taste-yours/surface-2-prompts.md),
which is left intact as the record of the original running order.

**What changed and why.** The old set handed over the taste-context block at step 02, the second
real move. That is what kept killing the post: the block landed before any exploring had happened,
so it solved the problem immediately and the remaining rounds had nothing left to do. The block was
never wrong. The running order was. Here the block goes last, after natural language has had a
genuine run at the job, and both halves earn their place: the plain-language rounds are how you
find out what you want, the block is how you keep it.

**Thread A is the post.** Run B (below) is exploratory only.

---

## Rules of the run

**Thread A — rounds 00 through 04.** Continuous. Each round passed the *previous generation* as
`--image`. That is thread continuity in a CLI that has no threads, not a style reference. Sean's own
artwork never entered the run. Words only.

**Thread B — round 05.** Fresh and cold. **No reference image of any kind.** The block got exactly
the same starting conditions round 00 got: nothing. Running it inside Thread A would have handed it
four rounds of steering and then credited it with the result.

**Scene held constant** across all six rounds.

---

## Run finding: the subject had to change, and why that is worth a Note

The set was written for a kid, matching the About page. GPT Image 2 refused it.

| Run | Prompt | Reference | Result |
|---|---|---|---|
| 00 | the lazy ask | none | flagged NSFW once, passed on retry |
| 01 | "more artistic and polished, more vibrant, more detail, really make it pop" | 00 (kid) | **flagged 3/3** |
| diagnostic | "keep everything the same, make the room slightly darker" | 00 (kid) | passed |
| 01 reworded | "more artistic, more vibrant, really make it pop" | 00 (kid) | flagged |

Not the image, and not the scene. The diagnostic passed with the same kid in frame. The trigger is
**enhancement language aimed at an image containing a child**. Probing stopped there.

**Resolution:** the subject aged up to a grown man. Same room, same TV, same cereal, same early
Saturday. Every prompt survived word-for-word except the two that said "kid." Round 01 then passed
first try with identical wording, which confirms the diagnosis. Superseded kid cold-open kept at
`../images/capture/_rerolls/00-cold-kid-superseded.png`.

---

# THREAD A — the post

## 1. `00-cold.png` · the lazy ask

```
Make me a warm, nostalgic illustration of a grown man watching Saturday morning cartoons.
A man sitting on the living room floor with a bowl of cereal, lit by the glow of the TV,
early morning. Make it cozy, beautiful, and professional.
```

> **Sean:** It felt too human and less animation. Like it was rotoscoped. Not terrible, but not what
> I wanted.

## 2. `01-pop.png` · prompt harder

```
Make it more artistic and polished. More vibrant, more detail, really make it pop.
```

> **Sean:** It's just a saturated version of the original.

## 3. `02-hand-drawn.png` · kill the finish

```
This looks like an ad. I want it to look like a person actually drew it by hand.
Rough it up. Show me the pencil underneath, the lines that didn't make the cut, the stuff
you'd normally erase. Leave it looking unfinished.
```

> **Sean:** It's still rotoscoped animation. Just the a-Ha "Take On Me" music video version.

## 4. `03-push-it.png` · stop being nice  ← **THE SURPRISE**

```
Still too sweet. Push the guy way further. Make him a real cartoon, exaggerate him,
give him a weird face. I don't want a nice picture of a nice man. Ugly is fine.
Go too far and I'll pull you back.
```

> **Sean:** Now we're getting somewhere. THIS ONE surprised me. This is the weird interesting drawing
> that I would create in my math notebook in high school. Just a little too gross and disturbing for
> what I'm going for. It also needs a splash of color.

## 5. `04-one-thing.png` · one decision  ← **THE REALIZATION**

```
Too much going on. Strip the room out. The TV glow should be the only warm thing in the
frame and everything else can sit in the dark. Give him room. One thing to look at.
```

> **Sean:** Definitely getting there. We have that splash of color, but now it's just a horror
> animation. I like silly and exaggerated. Not disgusting and horrifying. You know what? I should
> tell the model that instead of having it guess or try to describe it. Going through this process
> made me realize I didn't even know what I wanted in the first place. I think I'll make a taste
> block from that interview so I can use it for future generations and not go down this long road
> again.

---

# THREAD B — the block

## 6. `05-block.png` · the block, cold  ← **THE PAYOFF**

Fresh thread, nothing before it, no images attached.

```
Here is my taste-context block. Read all of it, then draw the scene applying it exactly.

MY TASTE-CONTEXT BLOCK
1. MEDIUM / SUBSTRATE: warm cream paper, graphite and ink, animator's pencil-test feel,
   visible paper grain.
2. THE HAND (mark-making): graphite linework, fine cross-hatching for shadow, a faint
   light-blue construction underdrawing left visible.
3. COLOR RULE: monochrome graphite and ink throughout, with exactly ONE restrained warm
   amber accent. Never a second accent color.
4. THE SHOW-THE-WORK TELL: leave the construction lines in, keep the paper grain. It should
   look hand-made and in-process, not rendered.
5. REGISTER: wildly exaggerated, absurd cartoon caricature. Never realistic, never photographic.
6. THE ONE MOVE THAT CARRIES MEANING: one warm amber accent on the single element that holds
   the feeling (here, the glow of the TV), plus one soft amber watercolor bloom behind the
   figure that bleeds into the cream paper. The wash sits BEHIND the linework, never on top,
   never splatter.
7. NEVER DO: no gradients, no glossy 3D, no airbrush, no smooth digital shading, no Pixar
   polish, no dead-eyed heartwarming, no text or letters or logos, no symmetry.

THE SCENE: a grown man, cross-legged on the living room floor in pajamas, a bowl of cereal in
his lap, lit by the glow of an old TV playing cartoons, early Saturday morning, the rest of
the room dark. Keep the TV glow as the one amber accent.

Apply the block exactly. No text anywhere.
```

> **Sean:** THERE WE GO! Silly, goofy, old school animation that feels hand made. The splash of
> watercolor to bring it to life.

---

## The verdict

**Mechanism:** the taste-context block. **Verdict: it delivered.** Five rounds of plain language
found the target; the block hit it. Unscored (Sean's own eye, no metric) — the measurement protocol
lands before the first *scored* rung.

**The through-lines the captions revealed, which the post is built on:**

1. **"Rotoscoped."** Rounds 1 and 3 both fail the same way. The machine kept handing back a filtered
   photograph when what was wanted was a drawing.
2. **The splash of color.** Named as missing at round 4, arrives wrong at round 5 (horror), arrives
   right at round 6 (watercolor). A want that had to be discovered before it could be asked for.
3. **The realization, in Sean's own words at round 5:** *"Going through this process made me realize
   I didn't even know what I wanted in the first place."* That sentence is the post.

---

# RUN B — the described likeness (exploratory, not used)

Run 2026-08-09, 35 credits, images at `../images/capture-b/`. **No reference photo was used.** The
headshot at `_assets/references/sean-headshot.jpg` was read and turned into words; the words went in
the prompt at round 00 and rode the chain.

```
THE MAN: lean and wiry, fair skin with light freckling across the nose and cheeks. Thick
dirty-blond hair swept straight up and back off a high forehead into a tall quiff, cropped short
at the sides. A long, straight, narrow nose. Blue-grey eyes under pale sandy eyebrows so light
they nearly disappear. Sparse blond stubble along the jaw and a patchy mustache that never quite
fills in. Narrow face, hollow cheeks, a jaw tapering to a pointed chin with a faint cleft.
Slightly prominent ears.
```

## Run B finding: a described likeness locks the face

| Round | Prompt | Result |
|---|---|---|
| 00 | the lazy ask + the description | passed, likeness landed |
| **01** | "more vibrant, more detail, really make it pop" | **blocked 3/3** |
| diagnostic | "make the room slightly darker" | passed |
| 02 | "make it look hand drawn" | passed |
| **03** | "exaggerate him, give him a weird face, ugly is fine" | **blocked 2/2** |
| 04 | "strip the room out" | passed |
| 05 | the block, cold, description folded into the scene | passed |

With a generic adult, 01 and 03 passed first try. With a described likeness, **both blocked**: the
model will not make him prettier and will not make him uglier. Anything compositional sails through.
The face is what's fenced. Probing stopped at the second refusal each time.

**Confound, stated plainly.** Run B never got the caricature push at 03, so its 04 lands weaker than
Run A's. Its 05 got the full block, caricature instruction included, and fired properly. Run B's
block appearing to "win" is an artifact of the censored chain, not a result. Run A is the post.

---

## `06-block-plus-refs.png` · not run

Adds Sean's own references on top of the block. Deliberately skipped: it answers a different
question (do references beat words), and that question is a rung of its own.
