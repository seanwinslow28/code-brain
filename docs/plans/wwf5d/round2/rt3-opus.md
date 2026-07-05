<!-- RT3 portfolio explainer-graphics enhancement spec · OPUS baseline · 2026-07-05 · model=opus · harness=intent-engineering scaffold + research · agentId aac435cde417a0735 · 24 tool-uses / 322s -->

# Enhancement Spec — Explainer Graphics Elevation ("Second-Read" Explainers)

**Profile:** 4-element floor, escalated to carry Strategic Context (the shared client-script contract), Constraints (perf/a11y/preservation), and Edge Cases — because the change alters a downstream contract (the `interactive-explainer.ts` shape + the harness posture) and touches the accessibility/performance surface. Sized via the intent-engineering Right-Sizing Decision Rule row 0, escalated per its "alters a downstream contract" clause.

**Target surface:** the case-study explainer figure on `/work/<slug>` (between the 4Q and Methods bands) — the five `*Explainer.astro` islands, the `ExplainerGraphic.astro` registry, and the shared `InteractiveExplainer.astro` base + `src/scripts/interactive-explainer.ts`.

**Audience the spec serves:** two readers at once — a **recruiter** (fast, phone, ~4-second scan, wants the point) and a **creative technologist** (curious, will hover/drag/inspect, wants to see craft the reader could not fake). The current graphics serve the first adequately and the second not at all. This is the gap Sean is naming as "sub-par/basic."

---

## Part 1 — System-Level Elevation Pattern

### 1.0 The diagnosis (ground before proposing)

The five explainers are already *good architecture*: real interactivity, a per-project gesture chosen to dramatize *that* system, a clean progressive-enhancement contract, honest reduced-motion fallbacks, screen-reader narration. They are not broken. What makes them read as "basic" is that they were built under a **deliberately self-imposed austerity doctrine** — documented verbatim in `docs/specs/interactive-explainer-rollout-v1.md` §7: *"WAAPI + stroke-dashoffset… CSS mask-image… keep doing Nano Banana… Confirmed skip list: GSAP / Three.js / Lenis (banned + heavy + template-y), Lottie, Rive, roughViz."* Every technique that produces a *memorable* motion signature was on that skip-list. The result is a set of figures whose ceiling is "a clean SVG that reacts to a slider" — legible, but visually indistinguishable from any competent dev's CSS work. Nothing on the page makes a creative technologist stop and think *"how did they do that?"*

Three specific ceilings the austerity doctrine imposed:

1. **Motion is linear-feeling and unchoreographed.** Each render(t) is a set of independent opacity/transform lerps keyed off one `easeInOut`. There is no *timeline* — no overlapping action, no secondary motion, no anticipation-and-settle across elements, no staggered cascade. Real motion craft (the thing Sean's own `2d-animation-principles` skill preaches) lives in *choreography between elements over time*, and WAAPI-by-hand makes that expensive enough that it wasn't attempted.
2. **The art is flat.** Keyed graphite rasters composited on paper with live SVG on top. No depth, no lighting response, no material. For a portfolio whose thesis is *"a creative who ships,"* the figures under-sell the creative half.
3. **The "wow" is rationed to one callout.** The rollout doc caps it: *"one callout per explainer, max."* That was the right call under austerity. It is the wrong call now that the goal is "attention-grabbing."

Sean has lifted the constraint. The elevation is therefore **not** "add more diagrams" — it is "raise the motion-craft and material ceiling of the figures that already carry the right intent, using the harnesses the austerity doctrine forbade."

### 1.1 The pattern: the "Second-Read Explainer"

Every explainer must now work at **two depths**, and the enhancement is about building the second:

- **First read (recruiter, 4s, static/reduced-motion floor):** the honest final-state figure, unchanged in *meaning*. Title → the one-sentence mechanic → the payoff number/state. This already exists as the `.webp` floor and must survive byte-for-byte in intent. **The elevation must not cost the first read.**
- **Second read (creative technologist, engaged):** the reader drives the mechanic and the figure responds with *choreographed, materially-richer motion* that demonstrates craft — a timeline, not a lerp; depth, not a flat composite; a signature moment, not a generic reveal. This is the layer being added.

The discipline that keeps this from becoming AI-slop motion: **the second read must still dramatize the same system the first read states.** A shader that looks cool but detaches from "the fleet inks the in-betweens" fails. The bar from the pattern doc — *"if the interaction would fit any project, it's wrong"* — is retained and, if anything, tightened: now it reads *"if the motion signature would fit any project, it's wrong."*

### 1.2 Recommended harness — and the reasoning

**Primary harness: GSAP 3 + its (now-free) plugin suite — ScrollTrigger, DrawSVG, MorphSVG, MotionPath — as the timeline engine for all five islands.**

Why GSAP is the right call:

1. **The skip-list's core rationale is void.** The rollout doc banned GSAP as *"banned + heavy + template-y."* As of the Webflow acquisition (all Club plugins free for commercial use, April 2025), the *cost/license* half of "banned" no longer exists — GSAP core + ScrollTrigger + MorphSVG + DrawSVG + MotionPath are 100% free for billed commercial work ([Webflow](https://webflow.com/blog/gsap-becomes-free), [CSS-Tricks](https://css-tricks.com/gsap-is-now-completely-free-even-for-commercial-use/)). "Heavy" is answerable by Astro islands (§1.4): GSAP ships *only* in the islands that import it, one route at a time, tree-shaken to the plugins used. "Template-y" is a *usage* failure, not a library property.
2. **It solves the exact ceiling.** The three ceilings in §1.0 are precisely what GSAP timelines are built for: overlapping/staggered choreography (`gsap.timeline()` + `stagger`), draw-on line art (`DrawSVGPlugin`), shape interpolation (`MorphSVGPlugin`), and path travel with proper easing/rotation (`MotionPathPlugin` — replaces the hand-computed `offset-path` math in the Code Brain dial).
3. **It preserves the scrub contract.** GSAP's `ScrollTrigger` with `scrub` — or, keeping the existing range input, a `gsap.timeline({paused:true})` whose `.progress(t)` is driven by the range's `render(t)` — plugs into the *existing* `wireScrubber` seam with a minimal change (§1.5).
4. **It is the industry-standard production stack for exactly this.** Current best-practice for premium scroll/scrub-driven explainer figures is Lenis + GSAP ScrollTrigger (+ Three.js where 3D is warranted) ([Medium — scrollytelling libraries 2026](https://sajanmangattu.medium.com/best-javascript-scroll-animation-scrollytelling-libraries-2026-5d63f67a1dca), [Maglr](https://www.maglr.com/blog/best-scrollytelling-examples)). A creative technologist recognizes GSAP-grade choreography on sight.

**Selective second harness — WebGL/shader, one island only (`animation-pipeline`), via a lazy `<canvas>` React island.** Recommended library: a thin OGL or raw-WebGL fragment-shader island (~5–8kB), **not** full Three.js, because the effect needed (a graphite "ink-in" dissolve / paper-grain displacement over a texture) is a single full-screen fragment shader, and pulling Three.js (~150kB) for one quad is the "heavy" the austerity doctrine rightly feared.

**Explicitly NOT recommended, with reasons:**
- **Rive** — 200kB runtime + editor-authoring workflow outside the repo (breaks the "committed generator script" reproducibility).
- **Lottie** — requires an After Effects → `.json` pipeline Sean doesn't run; the motion is *baked* (not reader-driven), which violates the "reader agency, never autoplay" non-negotiable.
- **Locomotive Scroll / Lenis as a *site-wide* smooth-scroll** — do not retrofit smooth-scroll onto the whole portfolio; it fights the newsroom/editorial feel and the existing View Transitions. If a *single* scroll-scrubbed explainer wants smoothing, scope Lenis to that island's scroll trigger, not the document.

### 1.3 When each harness applies (the routing rule)

| Figure need | Harness | Why |
|---|---|---|
| Choreographed multi-element timeline scrubbed by the reader (all five) | **GSAP timeline + `.progress()`** | Overlap, stagger, anticipation/settle |
| Line "inks itself" | **GSAP DrawSVGPlugin** | Authentic draw-on; replaces `stroke-dashoffset` hand-rolls |
| Shape A becomes shape B | **GSAP MorphSVGPlugin** | True interpolation; replaces cross-fades that read as "two PNGs" |
| Object travels a curved path (dial card) | **GSAP MotionPathPlugin** | Replaces the hand-computed `offset-path`/trig in Code Brain |
| Material/depth: texture dissolving, paper grain, ink bleeding | **Lazy WebGL fragment-shader `<canvas>` island** | The one thing SVG/CSS *cannot* do — reserved for `animation-pipeline` |
| Discrete DOM state (switchboard toggles, Game Boy toggle) | **Keep DOM + Rough.js; add GSAP only for the transition polish** | Already correct |

### 1.4 How it fits the Astro explainer registry (no architecture change)

- `ExplainerGraphic.astro` stays the null-guarded `INTERACTIVE` map (slug → component). No edit.
- Each `*Explainer.astro` stays a slotted layer set inside `InteractiveExplainer.astro`. Its `<script>` still selects on `[data-interactive-explainer="<slug>"]`. The *only* change inside a component is that its render logic builds a **GSAP timeline** instead of a bag of lerps.
- **Hydration/perf posture (load-bearing):** GSAP is imported *inside the island's `<script>`* (Astro ships it only on routes that use it). For the one WebGL island, make it a React island with **`client:visible`** so the shader `<canvas>` and its code do not load until the figure scrolls into view.
- **`prefers-reduced-motion` / no-JS remain the hard floor.** Every island's `<script>` still early-returns before building any GSAP timeline or WebGL context when `prefersReducedMotion()` is true (or JS is absent), leaving the static `.webp`. The elevation is *strictly* additive on top of the honest final state.

### 1.5 The shared client-script shape (the one contract change)

`src/scripts/interactive-explainer.ts` currently exports `easeInOut`, `prefersReducedMotion`, `enableInteractive`, `wireScrubber`. That seam is kept and *extended*, not replaced:

- **Add `wireTimeline(root, timeline, opts)`** — a sibling to `wireScrubber` that takes a GSAP `timeline` (paused) and drives `timeline.progress(t)` from the range input, reusing the identical reduced-motion gate, `is-interactive` opt-in, and track-fill logic. `wireScrubber` stays byte-identical so nothing that already uses it regresses.
- **Add `whenVisible(el, cb)`** — a tiny shared IntersectionObserver helper (the 16BitFit island already hand-rolls one; centralize it) so GSAP timelines and the WebGL island only *build/start* when the figure is near the viewport, and pause when it leaves.
- **Keep `easeInOut` exported** — the discrete-state islands and any hand-rolled fallback still use it.

### 1.6 Fallback / performance / accessibility posture (retained invariants)

- **Fallback:** unchanged and non-negotiable. `prefers-reduced-motion` and no-JS render the static `.webp` (continuous/scrub islands) or the operable un-tweened DOM (discrete-state islands). No GSAP timeline, no WebGL context, no MorphSVG is constructed on that path. *A weaker implementing model must not "simplify" by making the enhanced motion the only path.*
- **Performance budget (hard):** the enhancement adds **zero bytes to any route that doesn't render that island**. GSAP core+plugins used stay under ~40kB gzipped *on the case-study route only*; the WebGL island stays under ~10kB and loads `client:visible`. CLS stays zero.
- **Accessibility:** every current a11y affordance preserved — real `<input>`/`<button>` controls, `aria-label`, `aria-live` state narration, the amber `:focus-visible` ring, keyboard operability. New motion is *only* reachable when the reader has not asked to reduce it; the *meaning* stays in the live text and the alt. Color-as-actor beats stay on the audited token palette.

### 1.7 The doctrine edit this implies

`docs/specs/interactive-explainer-rollout-v1.md` §7's skip-list and §1's austerity note must be **superseded, not silently contradicted** — otherwise the next session re-imposes the ban. The implementing change updates that doc (and `CHANGELOG.md`) to record: *GSAP + free plugin suite promoted from skip-list to primary timeline harness; WebGL fragment-shader island admitted for `animation-pipeline` only; the "one callout max" and "CSS-first" caps are lifted in favor of the §1.1 Second-Read bar.*

---

## Part 2 — Two Worked Exemplars in Depth

### Exemplar A — `animation-pipeline` ("Anima")

**Communicative intent (grounded in `four_q`):** *The human owns timing and taste and makes the ship call; the fleet does the volume — the in-betweens.* To a recruiter in 4 seconds: **"human draws the key poses, AI fills the gap between them, and it still looks hand-drawn."** To a creative technologist: **this person understands animation at the craft level.** This is the flagship project — it earns the one WebGL budget.

**Current realization:** two copies of a keyed graphite run-cycle raster; a CSS `mask-image` wipes left-to-right as the reader scrubs; a tiny SVG pencil rides the reveal edge; an amber check fades in past 90%. It communicates the *what* competently. It does not *feel* like drawing.

**Proposed realization — "The fleet inks the in-betweens, for real":**

1. **The reveal becomes a graphite *ink-bleed dissolve* (WebGL fragment shader).** Replace the `linear-gradient` mask with a lazy `<canvas>` fragment-shader island (`client:visible`) sampling the same keyed run-cycle texture. The shader dissolves the ink in along the reveal edge using a **paper-fiber noise displacement** — graphite bleeding into the tooth of the cream paper, edge slightly ragged and grain-modulated. `t` drives the dissolve front. This is on-thesis: the whole project is about a pencil medium surviving an AI pipeline.
2. **The pencil rides the front on a GSAP MotionPath with acting.** The pencil is put on a short `MotionPathPlugin` path tracking the dissolve front with a subtle **anticipation dip before each in-between resolves and a settle after** (Sean's `2d-animation-principles`). Secondary motion: a faint graphite-dust puff at the tip on each frame-resolve (GSAP `stagger`).
3. **The HUMAN keyframe and the SHIP frame are the timeline's anchors.** The leftmost figure *pulses once* at t=0; the SHIP frame's approval stamp **draws on with DrawSVGPlugin**; the "10-phase" ticks light in a `stagger` as the front passes each.
4. **Reduced-motion/no-JS:** the existing static `.webp` — the fully-inked, stamped final state. Zero WebGL, zero GSAP on that path.

**Technique/library and WHY:** WebGL fragment shader for the ink-bleed (the sole material effect on the site — reserved for the flagship) + GSAP MotionPath+DrawSVG for the pencil acting + stamp draw-on. The shader carries *material*, GSAP carries *timing* — the project's literal thesis.

**Before → after, recruiter:** the figure now *looks drawn* — graphite bleeding onto paper as they drag — instead of a picture sliding behind a wipe. **Creative technologist:** a real-time paper-fiber dissolve shader (not a CSS mask), a pencil with anticipation-and-settle acting, a DrawSVG stamp — the single most technically impressive object on the site.

---

### Exemplar B — `intent-engineering-mcp` ("Intent Engineering MCP")

**Communicative intent (grounded in `four_q`):** *agent failures are intent failures; the tool audits a spec against a 9-section template and scores it; predict-then-check.* To a recruiter in 4 seconds: **"tighten the spec → the score climbs → the agent builds the right thing."** To a creative technologist: **this AI PM understands agent reliability as a structural discipline and can build the tooling that enforces it.**

**Current realization:** a slider cross-fades a scribble card into a checklist PNG, checks fade in one at a time, a live `7/25 → 23/25` counter recolors, an agent glyph swaps wrong→right past t≈0.8, and rough-notation circles the final score. This is already the most recruiter-legible interaction on the site and should *stay* legible. What makes it read as basic: the scribble→checklist is a *cross-fade of two rasters*, the checks *fade* rather than *get checked*, the agent flip is an opacity swap.

**Proposed realization — "Watch the spec resolve, section by section":**

1. **The scribble morphs into structure (GSAP MorphSVG), it doesn't cross-fade.** Author the vague card and the 9-section checklist as two SVG path sets and `MorphSVGPlugin` from scribble→clean-lines as the reader drags. The chaotic spec *reorganizes itself into order* — the visual literally performs "vague becomes structured."
2. **Each section gets *checked*, staggered, with a settle (GSAP DrawSVG + timeline stagger).** The nine checkmarks **draw on** one at a time in a GSAP `stagger` with a tiny overshoot-settle.
3. **The score is the hero and behaves like an instrument.** Keep the live `7→23/25` text (`aria-live`), but drive its recolor and a subtle scale-tick on each increment through the *same timeline*. rough-notation circles `23/25` as the *close* of the timeline.
4. **The agent flip earns its moment.** The "wrong" output *glitches/jitters* (a 2–3px GSAP shake) right up until the spec is tight, **then** snaps to "right" with a settle — dramatizing the causal claim.
5. **Reduced-motion/no-JS:** the existing static `.webp` showing the `23/25` tight end-state.

**Technique/library and WHY:** GSAP MorphSVG (scribble→structure *is* the message) + DrawSVG + a single paused GSAP timeline the range scrubs via the new `wireTimeline` seam. No WebGL here — this figure's job is *legible structural rigor*, and a shader would muddy the recruiter read. The restraint is the correct technical judgment.

**Before → after, recruiter:** the same reassuring "I drag, the number climbs to 23/25" — but now the scribble visibly *organizes into a checklist* and the checks *tick*, so cause-and-effect is even clearer. **Creative technologist:** SVG path *morphing* + *DrawSVG* check-ons on a single scrubbable GSAP timeline, plus an agent glyph that *jitters while the spec is vague and snaps when it's tight*.

---

## Part 3 — Intent-Carrying Spec Body

### Objective
The five case-study explainer figures carry the right *intent* but were built under a now-lifted austerity doctrine that capped their motion-craft and material ceiling. The result reads as "sub-par/basic" and fails the **creative-technologist** half of the audience. Raise the ceiling so each figure works at **two reads** — instant and legible for a **recruiter**, choreographed and technically impressive for a **creative technologist** — *without* costing the first read or the honest fallback.

**When facing trade-offs, prioritize (a) the recruiter's 4-second first read and the honest reduced-motion/no-JS floor over any enhancement, and (b) motion that dramatizes the specific system over motion that is merely impressive.**

### Desired Outcome
- A creative technologist who hovers/drags/inspects any explainer sees choreographed, materially-richer motion (a GSAP timeline; draw-on and morph where the mechanic calls for it; on the flagship, a real graphite-on-paper shader) — and can tell the author knows both animation craft and front-end engineering. Observable: the figure no longer reduces to "a slider over a PNG."
- A recruiter's first read is unchanged or *clearer*: title → one-sentence mechanic → payoff, in ~4 seconds, on the static/reduced-motion floor. Observable: meaning still lands with JS off / reduced-motion on.
- No route regresses in performance or accessibility: zero bytes to routes that don't render the island, CLS zero, Lighthouse materially unchanged, every a11y affordance preserved.
- The austerity doctrine is superseded in writing.

### The change, with reasoning-to-carry (per exemplar)
**Shared:** Promote **GSAP 3 + free plugins** to the primary timeline harness, imported inside each island's script (route-isolated). Add **`wireTimeline`** + **`whenVisible`** to `interactive-explainer.ts` (additive; existing exports byte-identical). Reasoning: the GSAP ban was a license/cost + "template-y" call now void; "template-y" is a usage failure defended by the §1.1 rule.
**`animation-pipeline`:** WebGL ink-bleed shader + GSAP MotionPath pencil + DrawSVG stamp. Reasoning: the only figure that gets a shader, because depth-of-medium **is** this project's message.
**`intent-engineering-mcp`:** GSAP MorphSVG + DrawSVG + jitter-then-snap agent, no shader. Reasoning: this figure's job is legible structural rigor and it is the site's most recruiter-legible interaction — protect that.
**The other three:** carry the pattern scoped to their gesture (code-brain MotionPath dial; the-block + 16bitfit discrete-state keep DOM + Rough.js, GSAP only for toggle→settle). Lower priority than the two exemplars.

### What NOT to change (Preservation Constraints)
- **The progressive-enhancement contract is inviolable** — reduced-motion and no-JS MUST render the static `.webp` / operable un-tweened DOM. No GSAP/Morph/WebGL on that path. *Protected because this floor is the product for a real fraction of readers and the entire first read.*
- **`ExplainerGraphic.astro`'s registry shape and `InteractiveExplainer.astro`'s base API.** *Protected because five islands + regression proofs depend on it.*
- **`wireScrubber` / `enableInteractive` / `easeInOut`** stay byte-identical. *Protected because the discrete-state islands consume them; the new helpers are additive siblings.*
- **The audited token palette + color-as-actor semantics.** *Protected because contrast ratios are WCAG-AA-verified and color carries meaning.*
- **Each figure's `four_q`-grounded meaning and one-sentence caption.** *Protected because the enhancement dramatizes existing intent — it does not change what any figure says.*
- **Route-isolated bundling.** *Protected because the perf posture depends on heavy code never touching routes that don't use it.*

### Done looks like
- On each enhanced case study, scrubbing produces a single authored choreography rather than independent lerps; `animation-pipeline` renders graphite dissolving into paper (shader); `intent-engineering-mcp` shows a scribble *morphing* into a checklist whose items *check on*.
- With JS disabled or reduced-motion, every figure shows its honest final state, no console error — verified per island.
- Per-route bundle check confirms GSAP/WebGL ships only on the case-study route and only for the islands that use it; Lighthouse Performance materially unchanged; CLS zero.
- Accessibility pass confirms controls, `aria-live`, focus ring, keyboard, reduced-motion respect intact; new motion is `aria-hidden` decoration over live-text meaning.
- The rollout spec §7 skip-list + §1 austerity note are superseded in the doc and logged in `CHANGELOG.md`.

---

## VALIDATION VERDICT — hand-run
- **Objective:** pass — problem + why + trade-off line (first read + floor over enhancement; system-specific over impressive).
- **Outcome:** pass — four observable states, verifiable without author self-report (bundle check, Lighthouse, JS-off render, a11y pass, doc diff).
- **Constraint (escalated):** pass — preservation constraints name the thing + why; harm-causing constraints (broken floor, cross-route bundle bleed) enforced structurally.
- **Edge Case (escalated):** pass — no-JS, reduced-motion, off-screen, below-fold lazy-load, and the "weaker model collapses to a single enhanced path" failure mode each handled; WebGL budget scoped to one named island.
- **Handoff rehearsal:** *"the implementer wants to add a Lenis site-wide smooth-scroll."* Objective trade-off + §1.2's explicit "do not retrofit smooth-scroll onto the whole portfolio; scope to the island" force scoping/rejecting it. No Objective strengthening needed.

**VALIDATION: PASS** (floor + escalated Constraint/Edge-Case groups). Ready to hand to an implementing session.
