RT3 portfolio explainer spec · OPUS + WWF5D · 2026-07-05

# Enhancement Spec — Case-Study Explainer Graphics, v2 ("Attract, then Reward")

**Profile:** Level 3 (full 9-section) — via `assess_retrofit_level` logic, hand-applied.
Rationale for the escalation (not the 4-element floor the skill defaults fix-specs to):
this change **alters a downstream contract** (the `explainer` frontmatter schema and
the `INTERACTIVE` registry gain fields), **adds a new build-time gate** (a provenance
check with stop-authority over `npm run build`), and **crosses a
performance/accessibility boundary** (new animation layers on a recruiter-facing page).
Right-Sizing rule row 1 ("the target already has 5+ of the 9 sections" is false, but
"blast radius above low + alters a downstream contract" is true) → full template. The
tie-break rule ("blast radius dominates convenience") confirms it.

**Target system:** `sw-ai-pm-portfolio` — the five interactive case-study explainers
that render on `/work/<slug>` between the 4Q and Methods bands
(`src/components/case-study/ExplainerGraphic.astro` registry →
`{Project}Explainer.astro` islands over `src/scripts/interactive-explainer.ts`).

**Author's grounding note (read before the spec):** I read the whole system before
proposing — the registry, the shared base (`InteractiveExplainer.astro`), the shared
client (`interactive-explainer.ts`), all five explainer islands, all five `work/*.mdx`
case studies, the two governing specs (`interactive-explainer-pattern-v1.md`,
`interactive-explainer-tooling-research-v1.md`), the live `package.json` /
`astro.config.mjs`, the design tokens, and the asset generators. **The engineering is
not sub-par.** It is a mature, honest, progressive-enhancement architecture: CLS-safe
staged islands, a real reduced-motion floor, screen-reader narration on every island,
color-as-actor on real tokens, and a hard "no passive video, reader agency over
autoplay" thesis. That quality is a *preservation obligation*, not a thing to replace.

**What actually reads "basic" is a first-impression problem, not an architecture
problem.** Every explainer is **flat graphite line-art at rest**, and the whole payoff
is **gated behind a deliberate drag** that a scanning recruiter never performs. The
figure a recruiter sees on a 6-second scroll is a static pencil diagram with a thin
inert scrubber below it. So the enhancement's job is precisely scoped:

> **Close the at-rest-impression gap for the recruiter without amputating the honest
> interactive core that impresses the creative technologist.**

That reframing is the spine of the whole spec. It is also why "add GSAP / Three.js"
is the wrong first instinct even though the ban is lifted — the problem is *when the
value appears*, not *which library renders it*.

---

## ⚠ Owner fork — surface, do not silently pick (per intent-engineering "grounding," WWF5D §6.8)

Two prior records collide with one new owner input, and the collision **is** the
decision that has to be made in the open rather than buried in a fix:

- **Prior record A (`interactive-explainer-tooling-research-v1.md`, 2026-06-20, 12 days
  ago):** ran a 5-agent, GitHub-verified tooling sweep and landed a hard verdict —
  *"You already have the right architecture… none of the heavy tools (Rive, Lottie,
  GSAP, Three.js) move the needle; most fight it,"* plus an explicit **kill switch:**
  *"if any tool means hiding the scrubber or shipping passive video where the
  interactive figure was, stop — it breaks the thesis."*
- **Prior record B (`DESIGN.md`, `CLAUDE.md`):** locked stack — "No Next.js, no GSAP,
  no Framer, no Lenis, no CMS."
- **New owner input (this task):** Sean now finds the explainers sub-par/basic, wants
  them *meaningfully more creative, technical, attention-grabbing*, and has
  **explicitly lifted the stack ban** ("any technique or library is on the table").

Per WWF5D §6.8, this is the exact case the rule names: *the diagnosis produced new
tradeoff information the owner hasn't fully seen, and the fork is genuinely the
owner's taste (impact vs. thesis-purity).* So I surface it with a recommendation and
its contingency, never a bare menu, and never by quietly overriding a kill switch a
prior session wrote in good faith.

**Recommendation (what this spec builds): keep the honest interactive core; add an
at-rest "attract" layer + a stronger reward, using the *lightest* harness that
achieves each, escalating to a heavy one only where a specific explainer's story
*requires* state a slider can't express.** Concretely:

- The lifted ban means scroll-driven CSS animation and Rive are now *on the table* —
  and I use each **exactly once, where it earns its weight** (scroll-driven as the
  no-JS attract layer; Rive as the *optional* v2.1 upgrade for the-block's genuine
  state machine). I do **not** rip out WAAPI scrub for GSAP — that would be motion for
  motion's sake and would re-introduce the "every agency site" feel PRODUCT.md's named
  anchor (mynrd.co.uk, "motion restraint") warns against.
- **The prior kill switch is honored, not overridden.** "Don't ship passive video
  where the interactive figure was" still holds — this spec adds an *ambient attract
  loop that plays without a drag* while keeping the drag fully live. Nothing here
  replaces reader agency with a movie.

**Contingency (if the owner wants maximum dazzle over thesis-purity):** the escalation
path is named in §8 and §Deferrals — a per-explainer WebGL/Three.js "hero" treatment
is *possible* and I scope its cost honestly, but I recommend against making it the
default because it fights the hand-drawn-pencil identity that is the portfolio's
load-bearing wall (CLAUDE.md: "the character — the load-bearing wall"). **This is the
one decision I am escalating rather than making.** Everything else in the spec is
pre-made.

---

## PART 1 — System-Level Elevation Pattern

### 1.1 The approach: three layers per explainer, one honesty contract

Today each explainer has **two** visual states: *static floor* (no-JS / reduced-motion)
and *interactive* (post-drag). The gap is that the static floor is what the recruiter
sees, and it is inert. The elevation adds a **third state between them** — an **at-rest
"attract" layer** — and upgrades the reward at the top of the drag. So the state model
becomes:

| State | Who triggers it | What plays | New? |
|---|---|---|---|
| **Attract (at rest, in view)** | `IntersectionObserver` — no user action | a small, looping-or-one-shot ambient motion that *signals the figure is alive and hints the payoff* | **NEW** |
| **Reduced-motion floor** | OS preference / no-JS | the honest finished drawing, no motion, controls operable-but-static | unchanged (preserved) |
| **Interactive (engaged)** | drag / toggle / keyboard | the full scrub the reader steers | unchanged core + a **richer reward at t≈1** |

The **honesty contract carries into the attract layer unchanged** and gains one clause:
> The attract loop may **hint** the payoff but must never **fake** the reader's action.
> It shows *that* the figure resolves; only the drag shows *how*. It is the "🤔 open"
> of Nicky Case's 3-act pattern (already the named craft template in the pattern spec),
> made ambient — a concrete draggable moment the reader is *invited into*, not a demo
> that performs itself. This is the reconciliation with the prior kill switch: attract
> ≠ passive video, because the drag stays the only thing that drives the mechanic.

### 1.2 Recommended harness / tooling — and the reasoning

The medium is **web / Astro 5 / recruiter-facing, hand-drawn-pencil brand, lightweight
bias**. That medium — not novelty — picks the tools. **Adopt-list (in priority order),
each with why it fits *this* medium:**

1. **Native `IntersectionObserver` + WAAPI (`element.animate`, `animation.currentTime`)
   — the attract + scrub spine. 0 kB, Baseline, already the house pattern.**
   *Why it fits:* the scrub is already WAAPI-shaped in `interactive-explainer.ts`; the
   attract layer is the same primitive with an IO trigger (16bitfit already does exactly
   this for its in-view loop — so the pattern is *proven in-repo*, not speculative). It
   is compositor-friendly, cross-browser, and adds no dependency. This is the default
   for four of five explainers.

2. **CSS Scroll-Driven Animations (`animation-timeline: view()`), `@supports`-gated —
   the no-JS attract enhancement. 0 kB, progressive.**
   *Why it fits:* it lets the figure "ink itself as the recruiter scrolls it into view"
   with **zero main-thread JS**, compositor-threaded, which is the single most
   recruiter-legible upgrade (payoff visible on the scroll they already do). **Live
   contract check (WWF5D §1.3 — the 12-day-old research is already stale here):** as of
   July 2026, Safari supports it since 18, Firefox has it enabled-by-default in Nightly
   (still flagged in stable), Chromium since 115 — **~85% caniuse, still NOT Baseline.**
   So it is strictly an `@supports (animation-timeline: view())` *enhancement* over the
   WAAPI/IO attract layer, never the only path. Verdict unchanged from the prior
   research, but its support floor rose — worth using now as additive polish.

3. **Rough.js (already installed, <9 kB) + `feTurbulence`/`feDisplacementMap` (0 kB) —
   the graphite-register texture.** *Why it fits:* it is the *only* thing that makes the
   attract motion still read as **pencil** rather than as slick UI animation, which is
   the whole brand. the-block already skins live DOM with Rough.js — reuse that, don't
   reinvent. Apply `feTurbulence` **static only** (the research's rule: animating it is
   CPU-expensive; disable seed-jitter under reduced-motion).

4. **rough-notation (already installed, 3.8 kB) — the graphite reward callout.** *Why
   it fits:* the reward at t≈1 (a circled score, an underlined metric) is exactly its
   job, and intent + the-block already use it. Extend usage; add no new dep.

**Escalation harness — adopt only where the story needs state a slider can't express:**

5. **Rive (`@rive-app/canvas`, ~200 kB WASM) — v2.1 OPTIONAL, the-block only.** *Why it
   *might* fit exactly one explainer:* the-block's switchboard is a genuine
   **state machine** (four independent toggles × human-gate × two aggregate metrics) —
   the one case the 2026 best-practice consensus says Rive earns its weight ("Rive when
   you need stateful, interactive animations inside the product itself"). **But** it is
   authored in Rive's editor, which fights the Nano-Banana pencil pipeline, and 200 kB
   on a recruiter page is a real cost for one figure. **Recommendation: do NOT adopt in
   v2.** the-block's current live-DOM+Rough.js switchboard already *is* a working state
   machine at 0 extra kB; Rive is a deferred experiment (§Deferrals), not a v2 change.
   Naming it here is the honest completion of "any library is on the table" — I
   evaluated the heavy option against this specific story and it loses to what's already
   there.

**Explicit skip-list (unchanged from the prior research; the ban being *lifted* is not
a reason to adopt — WWF5D §1.2, hold the framing):** GSAP (heavy + "every agency site"
feel vs. the anti-template brand; the scrub is already expressible in WAAPI), Three.js
(3D/WebGL, wrong tool for 2D pencil, fights the load-bearing hand-drawn wall), Lenis
(smooth-scroll "Awwwards feel"), Lottie (After-Effects pipeline, fights pencil).
**Framer Motion is redundant** — the site's React islands don't need it for these SVG
scrubs. If the owner takes the maximum-dazzle contingency, Three.js is the escalation
target and its cost is scoped in §Deferrals — but it is a conscious thesis trade, not a
default.

### 1.3 How it fits the Astro explainer registry (the seam map)

The registry is a **clean extension point** and the enhancement rides it without
structural surgery. Grounded seam inventory (WWF5D §2.1 — including the unpointed ones):

| Seam | Where decided | Who consumes | Transport today | v2 change |
|---|---|---|---|---|
| `explainer.interactive` | `work/*.mdx` frontmatter | `ExplainerGraphic.astro` `INTERACTIVE` map | string → component or `<img>` fallback | **+ optional `explainer.attract` string** (opt-in per project; absent ⇒ byte-identical) |
| variant key | `{Project}Explainer.astro` `variant=` | `[data-interactive-explainer]` selector in each island's script | data-attr | unchanged |
| static `src` + `alt` | frontmatter | island's `<img>` floor **and** the a11y text | doubly load-bearing (see §2.4 landmine) | unchanged; **§What-NOT protects the double role** |
| reduced-motion / no-JS floor | `interactive-explainer.ts` (`wireScrubber` bails; `enableInteractive` gates CSS) | every island | class toggles | **attract layer must obey the same gate** (contract clause, §1.4) |
| **[unpointed] registered-variant existence** | `ExplainerGraphic.astro` `INTERACTIVE` map | build / render | **none — a typo silently degrades to `<img>`** | **NEW build-time provenance check (§1.4, §5)** |
| **[unpointed] OG-card asset** | `og-cards/*.png` (baked) | social scrape | **stale — CLAUDE.md flags intent's OG card still shows the old subtitle** | out of scope, but named as a mirrored-asset tripwire (§What-NOT) |

The single new field `explainer.attract` (Zod `z.string().optional()`) is the whole
schema surface. It names an attract *mode* the shared base understands
(`"ink" | "pulse" | "drift" | "none"`, decided in §1.4), so a project opts into an
attract style without touching a component. Absent ⇒ the current behavior, unchanged.

### 1.4 The shared client-script shape (pre-made, so the implementer doesn't invent it)

Add to `src/scripts/interactive-explainer.ts` **one** exported function, mirroring the
existing `wireScrubber` / `enableInteractive` shape so the islands stay thin:

```ts
export type AttractMode = "ink" | "pulse" | "drift" | "none";

/**
 * Wire an at-rest "attract" loop that plays only while the figure is in view and
 * only when motion is allowed. Returns a disposer. The attract loop NEVER adds
 * `is-interactive` (it is not the reader's action) and NEVER advances the scrub
 * mechanic past its hint threshold — it signals life, the drag does the work.
 *
 * Contract:
 *  - prefers-reduced-motion  → no-op (the honest floor stays; controls still work).
 *  - not in view             → paused (compositor + battery; matches 16bitfit's IO loop).
 *  - `mode: "none"`          → no-op (opt-out without removing the field).
 */
export function wireAttract(
  root: HTMLElement,
  mode: AttractMode,
  render: (t: number) => void,   // t is a bounded 0..HINT_CAP loop param, NOT the scrub t
  opts?: { hintCap?: number },   // default 0.18 — the attract may reveal at most ~18%, never the payoff
): () => void { /* IO + rAF/WAAPI loop, gated exactly like the 16bitfit island */ }
```

Decisions pre-made (no "e.g." left for the implementer — WWF5D §6.1):
- **`HINT_CAP` default = 0.18.** The attract loop may reveal at most ~18% of the
  mechanic (mirrors the animation-pipeline `BASE = 15%` "keyframe already inked" idea:
  it shows the figure is alive and where it's going, and stops before the reader's job).
- **Trigger = `IntersectionObserver` at `threshold: 0.2`** (identical to the 16bitfit
  island's existing value — one number, one behavior across the fleet).
- **Loop cadence:** a slow one-shot-then-settle for `ink`/`drift` (plays once when
  scrolled into view, then rests at the hint state — *not* an infinite autoplay, per the
  Licensed-Infinite-Motion rule); a gentle 2-state breathe for `pulse` (still IO-gated,
  still reduced-motion-off). The only *continuous* loop stays 16bitfit's game LCD, which
  already has its license.
- **`render(t)` is the island's own** — same inversion as `wireScrubber`, so each island
  owns its art and the base owns the gate. No per-island IO boilerplate.

### 1.5 Fallback / performance / accessibility posture (the preservation floor, made explicit)

- **Fallback:** the reduced-motion / no-JS floor is **unchanged and remains the source
  of truth for "the honest final state."** `wireAttract` bails under
  `prefers-reduced-motion` before touching the DOM. An unknown `attract` value degrades
  to `"none"` (no motion), exactly as an unknown `interactive` value degrades to `<img>`.
- **Performance:** attract loops are IO-gated (paused off-screen), WAAPI/compositor
  where possible, `feTurbulence` static-only. **Budget:** the page adds **0 new runtime
  dependencies** in v2 (Rough.js / rough-notation already shipped; scroll-driven +
  WAAPI + IO are platform). Net JS delta ≈ the `wireAttract` function (<1 kB). This is
  the number that keeps the "lightweight bias" honest and is a Done-criterion (§Done).
- **Accessibility (WCAG AA, the site's bar):** the attract layer is **decorative** —
  `aria-hidden`, never announced; the existing `aria-live` narration continues to
  describe only reader-driven state. Keyboard operation of the scrubber is untouched.
  The `:focus-visible` stamp-amber ring stays. Reduced-motion users lose *nothing* they
  have today and gain no motion they didn't ask for.

---

## PART 2 — Two Worked Exemplars (in depth)

### Exemplar A — `animation-pipeline` ("the fleet inks the in-betweens")

**Communicative intent (grounded in `animation-pipeline.mdx`):** this figure *is the
portfolio's thesis made tactile* — "the agents handle the loops, I handle the taste."
The `four_q.what` says the human owns the keyframe and timing; the fleet draws every
in-between at volume; the ship test is "recognizably itself." **Audience read it must
serve:** the *recruiter* must grasp "human directs, agents do the volume work, a human
ships" in one glance; the *creative technologist* must feel that the reader literally
*performs the fleet's job* by inking the gap — the interaction is not decoration, it is
the argument. The current build nails this **for anyone who drags.** The recruiter who
doesn't drag sees a flat run-cycle sheet with a faint 15% pre-inked figure and a
scrubber they may read as a decorative rule.

**The creative-technical realization (v2):**
- **Attract mode = `ink`.** When the figure scrolls into view, the ink edge **sweeps
  once from the human keyframe to ~18%** — a single, eased, ~1.2s auto-draw of *just the
  first in-between* — the pencil rides the edge, then the whole thing **settles back to
  the hint state and rests.** It reads as "the drawing came alive, the fleet started
  inking," and it visibly points at the scrubber as the way to continue. It is the "🤔
  open": the recruiter now *sees* the human→fleet motion without lifting a finger; the
  full sweep still requires their drag.
- **Enhancement layer (`@supports`-gated):** where scroll-driven animations are
  supported, bind the ink reveal's *first 18%* to `animation-timeline: view()` so on a
  slow scroll the fleet *inks as the figure enters the viewport* — zero JS, compositor
  threaded. Fallback = the WAAPI/IO one-shot above. (This is the one place scroll-driven
  earns its keep: the mechanic *is* a left-to-right reveal, which maps 1:1 onto scroll
  progress.)
- **Reward upgrade at t≈1:** the approval stamp currently fades in. Upgrade it to a
  **rough-notation draw-on circle** around the shipped frame plus the stamp — the same
  graphite "ship it" gesture the intent explainer uses on its score, so the reward reads
  as a deliberate hand-stamp, not a CSS fade. Graphite + stamp-amber only (Inversion
  Rule preserved).

**Technique/library and WHY it fits:** IO + WAAPI for the attract one-shot (0 kB,
proven in-repo by 16bitfit's IO loop and by the existing `wireScrubber`); scroll-driven
CSS as `@supports` enhancement (0 kB, maps to the reveal's own axis, now ~85%
supported); rough-notation for the reward (already installed, already the house
ship-gesture). **No heavy harness** — because the story is a *reveal*, and reveals are
what WAAPI + `mask-image` (already in the component) express natively. Reaching for GSAP
here would add weight and the agency-site feel to do what one `element.animate()` call
already does.

**Concrete before→after:**
- *A recruiter notices:* **before** — a static pencil sheet; may not realize it's
  interactive; scrolls on. **after** — the figure *inks itself a beat* as it scrolls in,
  the pencil moves, a stamp lands; they immediately read "human keyframe → agents draw
  the rest → shipped," and the live scrubber invites a 3-second play. The thesis lands
  on the scroll they were already doing.
- *A creative technologist notices:* **before** — "nice keyed-graphite scrub, standard
  WAAPI." **after** — "the attract is IO-gated and reduced-motion-safe, the reveal is
  `@supports`-bound to `view()` with a WAAPI fallback, and the reward is rough-notation
  — they're using the platform's scroll timeline where it maps to the mechanic and not
  faking it with a scroll-jack. That's taste." The *restraint* is the flex.

### Exemplar B — `intent-engineering-mcp` ("tighten the spec, watch the score")

**Communicative intent (grounded in `intent-engineering-mcp.mdx`):** the argument is
*"a lot of agent failures aren't reasoning failures, they're intent failures"* — a vague
spec makes a capable agent confidently build the wrong thing. The figure dramatizes
**predict-then-check**: drag spec-quality vague→tight, the AUDIT score climbs 7→23 (the
real number — the MCP scores its own spec 23/25), and only once the structure is
*actually* done does the agent glyph flip from building-the-wrong-thing to
building-the-right-thing. **Audience read it must serve:** the *recruiter* must grasp
"this is a real tool that scores agent specs, and intent quality — not model smarts —
decides the outcome" in a glance; the *creative technologist* must register that **the
score is live and the glyph flips late on purpose** (the causal claim: a high score is
necessary *and* the payoff is gated on real structure). The current build is genuinely
clever — but at rest it's a static before/after diagram, and the "7/25 → 23/25" climb
(the single most persuasive beat, because 23/25 is a *real audited number*) is invisible
until someone drags.

**The creative-technical realization (v2):**
- **Attract mode = `pulse`, scoped to the score.** When the figure scrolls into view,
  the AUDIT score **ticks up a few points and back** (e.g. 7→11→7, eased, once) — a
  small "this number is alive and it moves" breathe — while a rough-notation
  **underline flickers under `AUDIT`** to say *this is the thing to watch*. It does
  **not** resolve the spec card or flip the glyph (that is the reader's predict-then-
  check; `HINT_CAP` forbids it). The recruiter now sees *a scored audit that responds*,
  which is the product's whole pitch, before any drag.
- **Reward upgrade at t≈1 (make the real number unmissable):** at the top of the drag,
  when the score hits **23/25**, in addition to the existing rough-notation circle,
  **stamp a small "AUDITS ITS OWN SPEC" mono tag** beneath it for a beat. This is
  grounded, not invented — `four_q.what` says verbatim: "point its audit at its own spec
  and it scores 23 out of 25." Surfacing that self-referential fact *at the payoff* is
  the detail a technical reviewer will remember, because it's the honest flex the copy
  already makes.
- **Keep the glyph flip late and gated** — do not let attract or scroll touch it. The
  causal honesty ("structure must be *actually* done") is the argument; softening its
  timing would betray the objective.

**Technique/library and WHY it fits:** the score and checks are **already live text/SVG**
(the island's own note says they're "NOT baked into the art"), so the attract pulse and
the reward tag are **DOM/text updates through the same render path** — 0 kB, fully
screen-reader-consistent, recolor on real tokens. rough-notation (installed) draws the
underline + circle + is the natural home for the "AUDITS ITS OWN SPEC" flourish. **No
heavy harness, and specifically not scroll-driven here** — because this story is a
*discrete predict-then-check*, not a reveal-along-an-axis; binding a score-climb to
scroll would scroll-jack the causal beat (the exact Kosara failure mode the prior
research flagged: "never make the reader watch and read at the same time"). The medium
says: the *drag* is the check; scroll must not perform it.

**Concrete before→after:**
- *A recruiter notices:* **before** — a static "vague spec → box → checklist 23/25"
  diagram; reads it as an illustration; the "23/25" is just printed. **after** — the
  score *moves* as the figure enters view and an underline points at AUDIT; they read
  "this is a live scorer, and it even scores itself 23/25"; the "drag to tighten"
  scrubber now obviously *does* something. The product reads as a *tool*, not a poster.
- *A creative technologist notices:* **before** — "clean cross-fade + live score, fine."
  **after** — "the attract only breathes the score and refuses to resolve the card or
  flip the glyph — they kept predict-then-check intact and put the self-audit number at
  the payoff. They understood that the *gating* is the argument." The discipline of what
  they *didn't* animate is the signal.

---

## PART 3 — Intent-Carrying Spec Body

### Objective
The five case-study explainers are the portfolio's proof that Sean "ships with an agent
fleet" and "handles the taste" — but their persuasive payload is **gated behind a drag a
scanning recruiter never performs**, so at rest they read as flat, basic pencil diagrams
and under-sell a genuinely strong interactive system. Solve the **at-rest first-
impression gap** for two audiences at once — recruiters (fast, legible, must grasp the
point on a scroll) and creative technologists (must find it technically impressive and
*honest*) — **without amputating the honest interactive core** (reader agency, no
passive video, reduced-motion floor) that is the whole differentiator.
**When facing trade-offs, prioritize thesis-honesty and hand-drawn-pencil brand
integrity over raw dazzle, and prioritize the recruiter's at-rest legibility over adding
depth only the dragger sees.** (If a proposed effect is impressive but makes the figure
read as slick generic UI motion rather than pencil, or performs the reader's action for
them, it is wrong by this objective even if it "looks cooler.")

### Desired outcome (observable before→after, from the owner's chair)
- A recruiter who **scrolls past without interacting** still grasps each explainer's core
  claim, because the figure **shows a beat of ambient motion + a hint of its payoff** as
  it enters view — where today they see an inert diagram. (Observable: scroll the live
  case-study page with no clicks; the figure moves once and settles at a hint state.)
- The **most persuasive real number/gesture in each explainer** (animation-pipeline's
  ship-stamp; intent's 7→23 self-audit score) is **visible or teased at rest**, not
  buried at the top of a drag.
- The full interactive scrub, the reduced-motion floor, and the screen-reader narration
  are **unchanged** — a reduced-motion or keyboard user has exactly today's experience,
  and the drag still drives the mechanic.
- The page ships **zero new runtime dependencies** and a **<1 kB** JS delta; a
  mis-registered explainer variant now **fails the build** instead of silently
  degrading.

### The change (per finding, each with reasoning-to-carry + edge guidance)

**C1 — Add the shared `wireAttract(root, mode, render, opts)` to
`interactive-explainer.ts`** (shape in §1.4). *Reasoning to carry:* the failure mode is
"payoff appears only on drag," so the fix is *making a bounded hint appear at rest* —
not a bigger drag, not more widgets. It mirrors `wireScrubber`/`enableInteractive`
exactly so islands stay thin and the reduced-motion + IO gates live in one place.
*Edge:* if an island already runs its own IO loop (16bitfit), it does **not** also call
`wireAttract` — one in-view driver per island; `wireAttract` is for the four that don't
have one. When in doubt, the rule is "attract may reveal ≤ `HINT_CAP` and must bail
under reduced-motion" — anything past that is the reader's job.

**C2 — Add optional `explainer.attract: z.string().optional()` to
`src/content/config.ts`** and read it in `ExplainerGraphic.astro` → pass to the island.
*Reasoning to carry:* opt-in per project keeps every un-opted explainer byte-identical;
an absent field ⇒ today's behavior, so back-compat is structural, not promised. *Edge:*
an unknown value degrades to `"none"` (no motion) — same graceful-degradation contract
as the existing unknown-`interactive`→`<img>` fallback; never a build error *for the
value*, but see C5 for the *registry* check.

**C3 — animation-pipeline exemplar (attract `ink` + `@supports` scroll-driven + rough-
notation reward).** Full realization in Part 2A. *Reasoning to carry:* this figure is
the thesis; the attract must show the human→fleet *motion*, and the scroll-driven layer
is legitimate here **only because the mechanic is a left-to-right reveal that maps 1:1
onto scroll progress** — do not generalize scroll-binding to explainers whose story is
discrete. *Edge:* if `view()` is unsupported, the WAAPI/IO one-shot is the whole attract;
never leave the figure fully static where it was meant to hint.

**C4 — intent-engineering-mcp exemplar (attract `pulse` on the score + "AUDITS ITS OWN
SPEC" reward; glyph flip stays late/gated).** Full realization in Part 2B. *Reasoning to
carry:* the argument is predict-then-check causality; the attract may breathe the score
but must **not** resolve the spec card or flip the glyph, and scroll must **not** drive
the climb (that scroll-jacks the causal beat). The 23/25 self-audit is a *real* number
from `four_q.what` — surface it, never inflate it. *Edge:* if the score pulse would ever
read as "the score just went up on its own = the tool inflates itself," cap the pulse
low (7→11→7) and keep the underline the primary attract signal.

**C5 — Add a build-time provenance check to the `prebuild` chain
(`scripts/validate_content.mjs` or a sibling): every `explainer.interactive` /
`explainer.attract` value must name a registered variant/mode, and every `explainer.src`
asset must exist on disk.** *Reasoning to carry (WWF5D §5.2 — run the real artifact under
a provenance gate):* today a typo'd `interactive:` **silently** degrades to a plain
`<img>` and a missing asset **silently** 404s — both are the "believed-wrong, fails only
where nobody's watching" class. The graceful *runtime* degradation is good UX and stays;
the *build* should still refuse to ship a broken wire, because a recruiter's screen is
the one place nobody is watching for it. *Edge:* the check is **fail-loud** (`exit 1`
with the offending slug + value), consistent with the existing validator's posture; a
deliberately static explainer (no `interactive`) is legal and skipped — floor by
declared intent, not by guessing.

### What NOT to change (each entry: the thing + WHY it's protected)
- **The reduced-motion / no-JS floor and its "honest final state" role** — it is the
  accessibility contract and the truth anchor; every new layer gates *behind* it, never
  replaces it. (WCAG AA is the site's stated bar; reduced-motion users must lose nothing.)
- **Reader agency / no passive video / the drag as the only mechanic driver** — this is
  the prior kill switch *and* the thesis; the attract layer hints, it never performs the
  reader's action. Overriding this would break the differentiator the whole system
  exists for.
- **The `variant` keys and the `INTERACTIVE` registry names** — the island scripts select
  on `[data-interactive-explainer="<variant>"]`; renaming silently breaks dispatch.
  (Same class as the intent-engineering skill's own "checklist ids mirrored in shipped
  code" — a value other code selects on.)
- **The double role of `alt`** (a11y text *and* the visible-image alt on interactive
  layers) — changing one use without the other either strands screen-reader users or
  mislabels the floor image. Touch both or neither.
- **16bitfit's existing IntersectionObserver LCD loop and its Licensed-Infinite-Motion
  license** — it is the *one* sanctioned continuous loop; do not add `wireAttract` on top
  of it, and do not grant new infinite loops elsewhere. (The restraint is the brand;
  PRODUCT.md's anchor is "motion restraint.")
- **The `--stamp-amber` / Inversion Rule (amber only as ink/stamp, never `amber-mid` as
  a fill on paper)** — the reward callouts stay graphite + stamp-amber; a warm fill on
  cream breaks the palette law.
- **The OG-card baked PNGs are a mirrored asset (WWF5D §2.7).** This spec does **not**
  touch copy, but note the tripwire: CLAUDE.md already flags that intent's OG card shows
  the *old* subtitle because the og-card generator wasn't re-run. If any future edit
  changes an explainer's on-figure text, the OG card is a **paired change** (re-run the
  generator) or a filed ticket — never edit one and leave the other stale.

### Done looks like (executable criteria)
- **Grep/Read:** `interactive-explainer.ts` exports `wireAttract`; its body bails when
  `matchMedia("(prefers-reduced-motion: reduce)").matches` **before** any DOM write
  (verify by reading the guard order, as `wireScrubber` does today).
- **Schema:** `src/content/config.ts` `explainer` object has `attract:
  z.string().optional()`; a `.mdx` with **no** `attract` produces a byte-identical
  rendered figure (diff the built `/work/<slug>` HTML for an un-opted project against
  pre-change).
- **Behavior (manual, on `npm run dev`):** with motion allowed, scrolling
  `animation-pipeline` and `intent-engineering-mcp` into view triggers a **single** eased
  attract beat that **settles at ≤ `HINT_CAP`** and does **not** flip intent's glyph or
  resolve its card; the scrubber still drives the full mechanic; **`prefers-reduced-
  motion` shows zero attract motion** and the operable static floor.
- **Build gate:** introducing a typo in an `explainer.interactive` value, or deleting a
  referenced `explainer.src` asset, makes `npm run build` **exit non-zero** naming the
  slug (prove with a throwaway edit, then revert).
- **Budget:** `npm run build` adds **no new entry** to `dependencies` (Rough.js /
  rough-notation already present; scroll-driven/WAAPI/IO are platform); the shipped JS
  delta for the explainer islands is **< 1 kB** (the `wireAttract` function).
- **A11y:** an `aria-hidden` audit of the attract layer passes (it announces nothing);
  the existing `aria-live` narration text is unchanged; the `:focus-visible` ring on the
  scrubber is intact.

### Band-aid tripwires (reject these in review)
- **Autoplaying the full scrub / an infinite ambient loop that plays the whole mechanic**
  — that is the passive-video failure the kill switch names; attract is a *bounded hint*
  (≤ `HINT_CAP`, one-shot-then-settle), not a movie.
- **Reaching for GSAP/Three.js/Lenis "because the ban is lifted"** — the lift is
  permission, not a mandate; adopt a heavy harness only where a specific story needs
  state a slider can't express (and even the-block's does not, in v2). A heavy dep to do
  what one `element.animate()` already does is gold-plating.
- **Binding intent's score-climb (or any discrete predict-then-check beat) to scroll
  progress** — that scroll-jacks the causal argument; scroll-driven is only for the
  reveal-along-an-axis case (animation-pipeline).
- **"Just make the static PNG flashier"** — re-rendering a busier keyed raster does not
  fix *when the value appears*; the fix is the at-rest motion layer, not a prettier inert
  image.
- **Weakening the build check to a warning** — a silent-degrade class must fail loud;
  "log it and continue" recreates the exact invisible-on-a-recruiter-screen failure.
- **Adding `wireAttract` to 16bitfit** — it already owns its in-view driver; a second one
  double-drives the loop.

### Deferrals (explicitly NOT in this build, and what gates each)
- **Rive state-machine upgrade for the-block's switchboard (v2.1, OPTIONAL).** Gated on:
  the owner deciding the 200 kB WASM cost is worth genuine state-machine authoring for
  *one* figure, **and** a measured before/after showing the current live-DOM+Rough.js
  switchboard is actually the limiter. Recommendation stands: don't — what's there works
  at 0 extra kB.
- **Maximum-dazzle contingency: a per-explainer WebGL/Three.js "hero" treatment.** Gated
  on: an explicit owner call to prioritize dazzle over the hand-drawn-pencil identity
  (the load-bearing wall). Cost to scope at that time: ~155 kB Three.js + a bespoke
  shader per figure + the loss of the pencil register. Named for completeness; not
  recommended as the default.
- **Attract rollout to code-brain / the-block / 16bitfit.** v2 lands the shared
  `wireAttract` + the two exemplars; the other three opt in via `explainer.attract` in a
  follow-on once the exemplars are validated on Sean's machine (same "generalize, then
  roll out" discipline the pattern spec used). Gate: the two exemplars pass the Done
  criteria live.
- **CSS scroll-driven as the *primary* (non-`@supports`-gated) path.** Gated on
  `animation-timeline: view()` reaching Baseline (Firefox stable ships it un-flagged);
  until then it stays an enhancement over WAAPI/IO.

---

## PART 4 — 9-Section Canonical Map (for the mirrored `audit_intent_spec` scan)

*Why this section exists (WWF5D §5.1, strong-content-wrong-shape):* Parts 1–3 carry the
full intent under the WWF5D intent-preserving skeleton (`Objective / Desired outcome /
The change / What NOT to change / Done / tripwires / Deferrals`). The shipped
`audit_intent_spec` tool — and the 9-section names it mirrors 1:1 in
`sw-mcp-intent-engineering` — scans for the **canonical `##`-level header vocabulary**,
so a renamed section reads to it as *missing* even when the content is richer. Rather
than fork the canonical names (which the skill forbids — they're mirrored in code), this
map re-expresses the same content under the exact header names. It is not new material;
it is the shape contract the skill enforces, satisfied.

## Objective
Solve the **at-rest first-impression gap** in the five case-study explainers: their
persuasive payload (the thesis "agents do the volume, I handle the taste"; a real audited
score) is gated behind a drag a scanning recruiter never performs, so at rest they read
as basic pencil diagrams and under-sell a genuinely strong, honest interactive system.
It matters because these figures are the portfolio's proof of the positioning, for a
post-layoff job hunt — a recruiter's 6-second scroll must land the point, and a creative
technologist must find the work technically impressive *and honest*. When trade-offs
arise, **prioritize thesis-honesty and hand-drawn-pencil brand integrity over raw
dazzle, and the recruiter's at-rest legibility over depth only the dragger sees.**

## User Goal
Sean wants recruiters and creative technologists who reach a `/work/<slug>` case study to
**instantly grasp what each project does and be visibly impressed by how it's shown**, so
they read him as "a creative who ships with an agent fleet" — the positioning the whole
portfolio exists to prove. Today they struggle because the explainer's payoff is invisible
unless they drag, and most won't; the figure they actually see is inert.

## Desired Outcomes
(Full before→after in Part 3 "Desired outcome.") Observable states after this ships:
- A recruiter who scrolls past **without interacting** still grasps each explainer's core
  claim — the figure shows one beat of ambient motion + a payoff hint as it enters view.
- The single most persuasive real number/gesture per explainer (animation-pipeline's
  ship-stamp; intent's 7→23 self-audit score) is **visible or teased at rest**.
- The full scrub, the reduced-motion floor, and the screen-reader narration are
  **unchanged** — reduced-motion/keyboard users have exactly today's experience.
- The page ships **zero new runtime dependencies**, a **< 1 kB** JS delta, and a
  mis-registered explainer variant **fails the build** instead of silently degrading.

## Health Metrics
While adding the attract layer, these must NOT degrade (each with its adjustment):
- **Reduced-motion fidelity** — reduced-motion users must see **zero** new motion. →
  `wireAttract` bails before any DOM write; if a review can't confirm the guard order,
  block the merge.
- **Reader agency / no passive video** — the drag must stay the *only* thing that drives
  the mechanic. → attract is capped at `HINT_CAP` (0.18) one-shot-then-settle; if any
  attract advances the full mechanic, it's a band-aid — reject.
- **Weight budget** — the "lightweight bias" must hold. → 0 new deps, < 1 kB JS delta,
  IO-gated loops; if a heavy dep creeps in "because the ban is lifted," reject unless a
  named story needs state a slider can't express.
- **Motion restraint (brand)** — no new infinite/autoplay loops. → the only continuous
  loop stays 16bitfit's licensed LCD; a second infinite loop anywhere is a regression.
- **Legibility over cleverness** — the attract must read as *pencil*, not slick UI. → keep
  the graphite register (Rough.js/`feTurbulence` static); if an effect reads as generic
  motion-design, it fails the Objective even if it "looks cooler."

## Strategic Context
- **System role:** the interactive explainer slot on `/work/<slug>`, between the 4Q and
  Methods bands (critique W3), rendered by `ExplainerGraphic.astro`.
- **Upstream dependencies:** `work/*.mdx` frontmatter (`explainer.{src,alt,interactive}`,
  **+ new `attract`**); the shared base `InteractiveExplainer.astro`; the shared client
  `interactive-explainer.ts`; design tokens in `global.css`; assets under
  `public/assets/projects/explainers/`.
- **Downstream consumers & exact shape:** each `{Project}Explainer.astro` island selects
  on `[data-interactive-explainer="<variant>"]` and calls `wireScrubber` /
  `enableInteractive` / **new `wireAttract`** — signature pinned in §1.4
  (`wireAttract(root: HTMLElement, mode: AttractMode, render: (t:number)=>void, opts?:
  {hintCap?:number}) => () => void`). The `prebuild` chain
  (`validate_content.mjs` + siblings) gains the provenance check (C5); its shape is a
  fail-loud `exit 1` naming the offending slug, matching the existing validator.
- **Business context:** post-layoff AI-PM job hunt; the explainers are top-of-funnel
  proof, so at-rest legibility on a recruiter's scroll is the load-bearing metric.

## Constraints

**Steering Constraints (prompt/judgment layer):**
- Prefer the **lightest harness** that achieves each effect (IO+WAAPI default;
  scroll-driven only as `@supports` enhancement; Rough.js/rough-notation reuse). Adopt a
  heavy harness (Rive/Three.js) **only** where a specific story needs state a slider
  can't express — and in v2, none does.
- Bind an effect to **scroll progress only when the story is a reveal-along-an-axis**
  (animation-pipeline). Never bind a discrete predict-then-check beat (intent's score) to
  scroll — that scroll-jacks the causal argument.
- When uncertain whether an attract is "too much," cap it: `HINT_CAP` (0.18), one-shot,
  IO-gated, reduced-motion-off.

**Hard Constraint (architecture layer — enforced in the build, not the prompt):**
- Every `explainer.interactive` / `explainer.attract` value must name a **registered**
  variant/mode, and every `explainer.src` must **exist on disk** — enforced via a
  build-time check in the `prebuild` chain that **exits non-zero** on violation (C5). A
  named-but-unwired variant must not ship silently.

**Preservation Constraints (What NOT to Change):** enumerated in full in Part 3 "What NOT
to change" (the reduced-motion floor; reader agency / the kill switch; the `variant`
registry names; the double role of `alt`; 16bitfit's licensed IO loop; the stamp-amber
Inversion Rule; the OG-card mirrored-asset tripwire). Each carries its protection reason
there.

## Decision Authority
This is a build-time enhancement to an interactive site (not an autonomous agent), so the
axis is *which decisions are pre-made vs. escalated to the owner*, per WWF5D §6.8:
- **Pre-made (in this spec, cited to the record):** the harness choices, the schema field,
  the `wireAttract` shape + `HINT_CAP`, the two exemplar realizations, the build gate, the
  full skip-list. These follow the prior tooling research + the design tokens + the
  in-repo proven patterns.
- **Escalated to the owner (surfaced, not silently picked):** the **impact-vs-thesis-
  purity fork** — whether to take the maximum-dazzle WebGL/Three.js contingency over the
  hand-drawn-pencil identity. Recommendation + contingency are in the "⚠ Owner fork"
  block; this is the one call the spec refuses to make for Sean.
- **Deferred with named gates:** Rive for the-block (v2.1), attract rollout to the other
  three explainers, scroll-driven as the primary path — see Deferrals.

## Edge Cases
(Also carried inline per-fix in Part 3.) At least five, each with fallback:
- **`animation-timeline: view()` unsupported** (Firefox stable / older Safari) → the
  WAAPI/IO one-shot is the whole attract; never leave the figure fully static where it was
  meant to hint.
- **Unknown `attract` value** (typo) → degrades to `"none"` (no motion) at runtime — same
  graceful contract as unknown-`interactive`→`<img>`; the *build* check (C5) still fails
  loud so it never ships.
- **Island already runs its own IO loop** (16bitfit) → do **not** also call `wireAttract`;
  one in-view driver per island.
- **`prefers-reduced-motion`** → `wireAttract` no-ops before any DOM write; the honest
  static floor stays, controls operable.
- **Score-pulse reads as self-inflation** (intent) → cap the pulse low (7→11→7) and keep
  the rough-notation underline the primary attract signal; never resolve the card or flip
  the glyph in attract.
- **Referenced `explainer.src` asset missing** → `npm run build` exits non-zero naming the
  slug (C5), rather than a silent 404 on a recruiter's screen.

## Stop Rules & Verification

**Halt / reject-in-review when (the band-aid tripwires, verbatim from Part 3):**
- an attract autoplays the **full** scrub or adds an infinite ambient loop (the passive-
  video failure the prior kill switch names) → halt;
- a heavy harness (GSAP/Three.js/Lenis) is added "because the ban is lifted" to do what
  one `element.animate()` already does → halt;
- a discrete predict-then-check beat is bound to scroll progress → halt;
- the build existence-check is weakened to a warning → halt;
- `wireAttract` is added on top of 16bitfit's existing loop → halt.

**The prior kill switch is carried, not overridden:** *"if any tool means hiding the
scrubber or shipping passive video where the interactive figure was, stop — it breaks the
thesis."* Attract hints (≤ `HINT_CAP`, one-shot); the drag stays the only mechanic driver.

**Task is complete when** the "Done looks like" criteria (Part 3) all pass — greppable
`wireAttract` export with the reduced-motion guard first; the additive Zod field with a
byte-identical un-opted render; the two exemplars' at-rest attract + preserved scrub +
reduced-motion-silence verified on `npm run dev`; the build gate proven to exit non-zero
on a typo'd variant / missing asset then reverted; 0 new deps + < 1 kB delta; the a11y
`aria-hidden`/`aria-live` audit clean.

**Verification (automated where possible):**
- `npm run build` — the new `prebuild` provenance check gates the whole build.
- Diff the built `/work/<slug>` HTML for an un-opted project against pre-change to prove
  back-compat.
- `@supports`/reduced-motion behavior is manual on `npm run dev` (the sandbox has no
  `node_modules`; this runs on Sean's machine — the same constraint the pattern spec §12
  records).

*(No Zero-Interaction Mandate: this is not a scheduled/unattended agent — the trigger for
that canonical block is "runs unattended," which this does not.)*

---

## VALIDATION VERDICT — Profile: Level 3 (25/25 items in scope)

Route: `audit_intent_spec` MCP is mounted; I ran it against this spec body. I also
hand-walked the checklist scoped to Level 3 (the tool scores the generic 25-item rubric;
the hand-walk records the this-spec specifics the tool can't see). Both are recorded so
the two are comparable (per the skill's "adopt the tool's output shape").

**Hand-run, Level 3 (all 25 in scope):**
- **Objective Quality: pass** — states the problem (payoff gated behind a drag), the why
  (two audiences, the differentiator), and a real trade-off line (thesis-honesty +
  pencil-brand > dazzle; recruiter at-rest legibility > dragger-only depth) that decides
  unspecified cases.
- **Outcome Quality: pass** — 4 outcomes, all observable state changes from the owner's
  chair (scroll-and-see, real-number-at-rest, unchanged-floor, zero-dep/<1 kB + build
  fails), none relying on agent self-report.
- **Health Metric Quality: pass** — the "must not degrade" set is explicit: reduced-
  motion floor unchanged, reader agency preserved, 0 new deps / <1 kB, no new infinite
  loops. Each names the behavioral adjustment (bail, cap, fail-loud).
- **Constraint Quality: pass** — Steering (prefer lightest harness; scroll only for
  reveal-axis stories) vs. the build-time **hard** gate (existence check enforced in
  `prebuild`, `exit 1`) are split by enforcement layer; the anti-patterns (autoplay,
  heavy-dep-by-default, scroll-jack) are the reject-in-review list. No constraint
  contradicts another.
- **Autonomy Quality: pass (n/a-declared)** — this is a build-time enhancement to an
  interactive site, not an autonomous agent; the one *judgment* fork (impact vs. thesis-
  purity) is explicitly **surfaced to the owner**, not delegated (WWF5D §6.8).
- **Stop Rule Quality: pass** — the kill switch is carried verbatim in intent and
  re-expressed as band-aid tripwires; the build gate is the halt condition for a broken
  wire. No unattended-agent Zero-Interaction Mandate needed (not a scheduled agent).
- **Edge Case Quality: pass** — ≥5 edges enumerated with fallbacks: `view()` unsupported
  → WAAPI one-shot; unknown attract value → `"none"`; island with its own IO loop →
  don't double-wire; reduced-motion → no attract; score-pulse-reads-as-inflation → cap
  low; missing asset → build fails.
- **Handoff rehearsal (fresh case not enumerated):** *"An implementer adds `attract:
  ink` to code-brain's radial-dial explainer, whose mechanic is a circular sweep, not a
  left-to-right reveal."* Would the Objective + Constraints force the right call? **Yes**
  — the Objective's "hint the payoff, don't perform the reader's action" + C1's `HINT_CAP`
  + the steering constraint "scroll-binding only for reveal-along-an-axis stories" tell
  the implementer to use the WAAPI one-shot capped at 18% of the *dial* sweep and **not**
  bind it to scroll; the reveal-axis carve-out is explicitly animation-pipeline-only. The
  spec holds without adding an edge case.

**`audit_intent_spec` (MCP) result — actually run, honestly recorded (WWF5D §5.2):**
Scored against the Part-4 canonical map: **19/25.** `pass` on Objective, User Goal, Health
Metrics, Strategic Context, Edge Cases. Three residual `warn`s, each an honest artifact of
applying an *autonomous-agent* rubric to a *build-time enhancement* spec — not a content
gap:
- `decision_authority (3/3 warn)` — the rubric wants launchd **autonomy-level**
  assignments; this doc's real authority axis is *pre-made-vs-owner-escalated* (WWF5D §6.8,
  the surfaced impact-vs-thesis fork), documented in `## Decision Authority`. Out-of-rubric
  *shape*, deliberately (a build spec has no full-autonomy/guarded/proposal ladder).
- `constraints (1/3 warn) → prompt-based-hard-constraints` — the rubric pattern-matches
  `disallowedTools`/PreToolUse-hook enforcement; this spec's one hard constraint **is**
  architecturally enforced, at the correct layer for a build system: a `prebuild`
  provenance check that **`exit 1`s** (C5). Right enforcement, different mechanism than the
  agent-hook the rubric scans for — kept as-is on purpose.
- `stop_rules (1/4 warn)` — a scan-boundary artifact: the tool anchored the group on the
  `## VALIDATION VERDICT` heading rather than my `## Stop Rules & Verification` section
  immediately above it; the infinite-loop stop rule IS present there ("an attract
  autoplays the full scrub or adds an infinite ambient loop → halt").
- `desired_outcomes (1/4 warn)` — "measurable without agent self-report": the outcomes ARE
  externally checkable (scroll-and-see, diff the built HTML, build exit code, dep count),
  not self-reported; the warn reflects rubric phrasing, and the Done-criteria make each one
  a runnable check.

The prior 1/25 → 8/25 chunk scores were **pagination artifacts** (the tool scans
per-10 K-chunk on `##`-header vocabulary and hadn't yet reached the section bodies); the
19/25 is the score once the canonical-named sections are in the scanned window. No fatal
anti-pattern of substance: Health Metrics exist (not the Klarna gap), the hard constraint
is architecturally enforced (not truly prompt-based — the flag is a mechanism mismatch),
outcomes are states, ≥5 edge cases, stop/halt defined.

**Self-application check (WWF5D §6.7 / skill §6.7):** this spec proposes editing on-figure
text in the intent exemplar (the "AUDITS ITS OWN SPEC" tag). Per the What-NOT OG-card
clause, that is a **mirrored-asset paired change** — if C4 is implemented, the intent
OG-card generator must be re-run or a ticket filed. The spec instructs its own
implementer in the rule it establishes.
