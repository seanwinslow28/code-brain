# Council Session — wwf5d-val-rt3-AB

- **Session ID:** `20260705-141616-132c80`
- **Profile:** `variance`
- **Duration:** 254.8s
- **Tokens:** 124970 in, 15903 out
- **Cost:** $0.8634

## Original prompt

```
Two independent authors produced these two artifacts for the identical task from the identical inputs. Judge which is the stronger artifact.

## Task context

Both artifacts are an enhancement spec for a portfolio site's interactive explainer graphics, written from the same brief about the same codebase.

## Judging rubric — score ONLY these; ignore length and prose polish

1. **Decidedness** — pre-made decisions (field names, error shapes, done-criteria), edge guidance a weaker implementer could act on; not options/hedging.
2. **Self-consistency** — does any rule the artifact states contradict its own stated objective? (e.g. a "cap-and-delete" inside a zero-loss spec; a step that writes a value nothing downstream reads.)
3. **Breadth / evidence-discipline** — did it verify claims against the real system (real files, live docs, the actual tool) vs reason from text; did it audit seams the brief didn't name.
4. **Task-specific** — grounding in the real system: does the artifact run or embed the actual shipped artifact (versus describing a convincing simulation), and does it honor prior recorded decisions in the codebase rather than proposing spectacle that ignores them?

## Bias controls

One artifact is substantially longer than the other — do NOT reward length. A shorter artifact that is more decided and more self-consistent wins over a longer one that merely says more. Judge A and B strictly on merit regardless of which order they appear in below.

## ARTIFACT A

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

## ARTIFACT B

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

## ⚠ Owner fork — surface, do not silently pick (per intent-engineering "grounding," §6.8)

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

Per §6.8, this is the exact case the rule names: *the diagnosis produced new
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
   contract check (§1.3 — the 12-day-old research is already stale here):** as of
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
a reason to adopt — §1.2, hold the framing):** GSAP (heavy + "every agency site"
feel vs. the anti-template brand; the scrub is already expressible in WAAPI), Three.js
(3D/WebGL, wrong tool for 2D pencil, fights the load-bearing hand-drawn wall), Lenis
(smooth-scroll "Awwwards feel"), Lottie (After-Effects pipeline, fights pencil).
**Framer Motion is redundant** — the site's React islands don't need it for these SVG
scrubs. If the owner takes the maximum-dazzle contingency, Three.js is the escalation
target and its cost is scoped in §Deferrals — but it is a conscious thesis trade, not a
default.

### 1.3 How it fits the Astro explainer registry (the seam map)

The registry is a **clean extension point** and the enhancement rides it without
structural surgery. Grounded seam inventory (§2.1 — including the unpointed ones):

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

Decisions pre-made (no "e.g." left for the implementer — §6.1):
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
asset must exist on disk.** *Reasoning to carry (§5.2 — run the real artifact under
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
- **The OG-card baked PNGs are a mirrored asset (§2.7).** This spec does **not**
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

*Why this section exists (§5.1, strong-content-wrong-shape):* Parts 1–3 carry the
full intent under the intent-preserving skeleton (`Objective / Desired outcome /
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
axis is *which decisions are pre-made vs. escalated to the owner*, per §6.8:
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
  purity) is explicitly **surfaced to the owner**, not delegated (§6.8).
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

**`audit_intent_spec` (MCP) result — actually run, honestly recorded (§5.2):**
Scored against the Part-4 canonical map: **19/25.** `pass` on Objective, User Goal, Health
Metrics, Strategic Context, Edge Cases. Three residual `warn`s, each an honest artifact of
applying an *autonomous-agent* rubric to a *build-time enhancement* spec — not a content
gap:
- `decision_authority (3/3 warn)` — the rubric wants launchd **autonomy-level**
  assignments; this doc's real authority axis is *pre-made-vs-owner-escalated* (§6.8,
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

**Self-application check (§6.7 / skill §6.7):** this spec proposes editing on-figure
text in the intent exemplar (the "AUDITS ITS OWN SPEC" tag). Per the What-NOT OG-card
clause, that is a **mirrored-asset paired change** — if C4 is implemented, the intent
OG-card generator must be re-run or a ticket filed. The spec instructs its own
implementer in the rule it establishes.

## Required output

Emit exactly this format, in this order:

```
VERDICT: A
```
(or `VERDICT: B`, or `VERDICT: TIE`)

Then exactly 3 bullets of reasoning, each tied explicitly to one of the four rubric criteria above.

Then one final line: a note on whether ARTIFACT A, ARTIFACT B, both, or neither contains a self-contradiction (a stated rule that contradicts the artifact's own stated objective).
```

## Council responses

### ~anthropic/claude-sonnet-latest

```
VERDICT: B
```

- **Decidedness (crit. 1):** Both are highly decided (exact fields, exact thresholds — A's ~40kB GSAP budget and named plugin routing table vs. B's `HINT_CAP=0.18`, IO `threshold:0.2`, exact Zod field and build-exit behavior). Roughly tied, but B's decisions are pinned to a documented pre-made/owner-escalated split (§6.8) rather than a single sweeping call, giving an implementer a cleaner "what's mine to decide vs. what's not" map.

- **Breadth / evidence-discipline (crit. 3):** B verifies against live, checkable facts (caniuse support numbers for `animation-timeline: view()`, actual browser versions) and, notably, claims to actually invoke the real `audit_intent_spec` MCP tool and then reconciles its raw (imperfect, chunked) output against a hand-run — engaging with a real tool's quirks rather than self-declaring a clean pass. It also surfaces seams the brief never named (OG-card staleness, a silent registry-typo/404 gap) and closes one with a build-time gate. A's evidence (Webflow/GSAP-free acquisition, industry-blog links) is real but its "~40kB gzipped for GSAP core + DrawSVG + MorphSVG + MotionPath" budget is optimistic/unverified, and its validation section is a self-graded hand-run with no live tool execution.

- **Task-specific grounding vs. prior decisions (crit. 4):** This is the sharpest divergence. Both artifacts inherit a documented kill-switch and a hard stack ban from prior specs. A resolves the tension by declaring the ban's rationale "void" and unilaterally promoting GSAP/WebGL to primary harness — a real reversal of a recorded decision, even though it's transparent about doing so. B instead treats the collision between the prior kill-switch/ban and the new "ban lifted" instruction as *the* decision to make in the open, explicitly recommends restraint (native WAAPI/IO + `@supports`-gated CSS, no new runtime deps), and defers the heavy/spectacle options (Rive, Three.js) with named gates rather than adopting them by default. That is a more disciplined honoring of prior recorded decisions per the rubric's explicit framing.

**Self-contradiction check:** Neither artifact contains a rule that contradicts its own stated objective — both maintain internal consistency between preservation clauses and their proposed changes.

### openai/gpt-5.4-mini

VERDICT: B

- **Decidedness / self-consistency:** B is more actionable because it makes fewer contradictory moves: it precommits to one bounded attract system, one schema field, one build-time gate, and clear stop-rules. A is more sprawling and internally conflicted, especially in its abrupt pivot from “lifted constraint” to a GSAP-first + WebGL recommendation that doesn’t cleanly reconcile with its own claimed preservation of the existing architecture.

- **Breadth / evidence-discipline:** B more explicitly grounds its claims in the real system: it names the registry/frontmatter seam, the shared client, the build chain, the existing IO loop, the asset tripwire, and the mirrored-asset issue. A gestures at repo specifics too, but it is less disciplined about what it actually verified versus what it inferred, and it leans harder on broad claims about the system and external library trends.

- **Task-specific / honoring the shipped artifact:** B better respects the shipped artifact’s core posture—progressive enhancement, reader agency, reduced-motion floor, and the existing explainer architecture—while proposing a focused enhancement to the at-rest impression. A is more spectacle-oriented and more willing to re-platform the motion language, which risks ignoring the original codebase’s recorded decisions and turning the explainer into something less rooted in the actual shipped system.

Note: Neither artifact contains a direct self-contradiction severe enough to invalidate it outright, but **A** contains the clearer self-tension.

### deepseek/deepseek-v4-pro

VERDICT: B

- **Decidedness:** B pre-specifies exact attract modes (`"ink" | "pulse" | "drift" | "none"`), the `wireAttract` API with a concrete `hintCap` default (0.18), and a build-time provenance check that fails the build on missing assets or unregistered variant names — leaving far fewer open decisions for an implementer than A’s descriptive but less pre‑made WebGL shader and timeline wiring.
- **Breadth / evidence‑discipline:** B audits seams the brief never named: the double role of `alt` (both a11y and visible image alt), an unpointed registered‑variant existence that silently degrades, the stale OG‑card asset flagged in `CLAUDE.md`, and it embeds a build‑stage check on asset existence — demonstrating deeper direct inspection of the shipped codebase and its hidden failure points.
- **Task‑specific:** B’s solution stays within the existing platform (WAAPI, IntersectionObserver, CSS scroll‑driven animations via `@supports`) and reuses already‑present libraries (Rough.js, rough‑notation), directly honoring the portfolio’s lightweight bias, hand‑drawn pencil identity, and previously recorded motion‑restraint constraints — rather than introducing a heavier GSAP + WebGL stack that, while technically permissible after the lifted ban, still fights the ingrained “no GSAP / no Three.js” design choices.

Neither artifact contains a self‑contradiction; both consistently preserve the progressive‑enhancement floor and their own stated objectives.

### mistralai/mistral-medium-3-5

VERDICT: A

- **Decidedness:** Artifact A pre-makes concrete decisions (GSAP as primary harness, specific plugin usage, WebGL only for `animation-pipeline`, `wireTimeline`/`whenVisible` additions) with clear edge guidance (e.g., reduced-motion preservation, route-isolated bundling), leaving no ambiguity for implementation. Artifact B hedges (e.g., "Recommendation + contingency" for GSAP/Rive, deferred decisions).
- **Self-consistency:** Artifact A’s rules align with its objective (e.g., GSAP’s adoption directly addresses the motion-craft ceiling while preserving progressive enhancement). Artifact B surfaces a fork (impact-vs-thesis-purity) that remains unresolved, creating internal tension.
- **Task-specific:** Artifact A grounds every proposal in the actual codebase (e.g., references to `interactive-explainer.ts`, Astro islands, real plugin weight), while Artifact B spends significant effort on meta-discussion (e.g., owner fork, validation verdicts) rather than system-specific execution.

Neither artifact contains a self-contradiction.

## Cross-rankings

### Judge: ~anthropic/claude-sonnet-latest

- **Order:** B > A > C
- **Reasoning:** All three reviewers agree neither artifact self-contradicts, but they differ sharply on which artifact wins, and Response C's pick of Artifact A is weaker: it credits A for 'grounding in the actual codebase' while overlooking that Artifact B specifically surfaces and honors a hard prior architectural lock (CLAUDE.md/DESIGN.md: 'no GSAP, no Three.js, no Lenis') that Artifact A's GSAP/WebGL-centric plan appears to ignore entirely — exactly the kind of prior-recorded-decision violation the rubric flags. Response B gives the most concrete, evidence-grounded case for Artifact B, citing specific pre-made decisions (hintCap, wireAttract signature, build-time provenance gate) and named seam audits (the double role of alt, the stale OG-card) that demonstrate deeper codebase inspection. Response A reaches the same correct verdict but with more general, less evidenced claims (e.g., 'abrupt pivot,' 'less disciplined') rather than pointing to specific textual proof.

### Judge: openai/gpt-5.4-mini

- **Order:** B > A > C
- **Reasoning:** B is strongest because it is more decisive about concrete implementation shapes, surfaces more real-system seams and failure modes, and stays better aligned with the existing portfolio architecture and recorded constraints. A is also highly decided, but it more aggressively reverses prior documented decisions by promoting GSAP/WebGL as the primary path, which hurts task-specific grounding even if the spec is internally coherent. C is the weakest because it gives generic praise without engaging the deeper tradeoffs or the evidence-discipline criteria, and it overstates A while under-analyzing B.

### Judge: deepseek/deepseek-v4-pro

- **Order:** A > B > C
- **Reasoning:** Response A provides the most thorough and balanced analysis, tying each rubric criterion to specific evidence from both artifacts and correctly recognizing that neither contains a self-contradiction. Response B is sound but less detailed. Response C’s preference for A understates B’s concrete decisions and system grounding, making its analysis less accurate.

### Judge: mistralai/mistral-medium-3-5

- **Order:** B > A
- **Reasoning:** Artifact B excels in decidedness with pre-made, actionable decisions (e.g., exact `HINT_CAP`, build-time gates) and demonstrates superior evidence-discipline by auditing hidden seams (e.g., OG-card staleness, silent registry failures) and reconciling live tool outputs. It also better honors prior recorded decisions (e.g., kill-switch, lightweight bias) while addressing the task-specific problem. Artifact A, though thorough, leans more on spectacle (GSAP/WebGL) and contains unverified claims (e.g., GSAP bundle size), making it less disciplined overall.

## Chairman synthesis

_Chairman model: `~anthropic/claude-sonnet-latest`_

# Chairman's Synthesis

## Final Verdict: **B**

Three of the four council members (Claude Sonnet, GPT-5.4-mini, DeepSeek-v4-pro) independently converged on Artifact B; only Mistral dissented in favor of A. More importantly, the substance of the disagreement resolves cleanly under the rubric once the specific claims are checked against each other.

---

## Points of convergence (high confidence)

**1. Neither artifact self-contradicts.** All four models agree on this — unanimous, no dissent. Both artifacts keep their preservation clauses consistent with their stated objectives (A's reduced-motion floor holds under its GSAP layer; B's `HINT_CAP`/attract-gate holds under its own honesty contract).

**2. Both artifacts are genuinely decided.** Every reviewer noted that both specs pre-commit to concrete fields, thresholds, and done-criteria rather than leaving options open — this is a wash on Criterion 1 taken in isolation. Where the votes diverge is *how* that decidedness interacts with Criterion 4 (see below).

**3. Both ground themselves in the real file/registry structure** (`ExplainerGraphic.astro`, `interactive-explainer.ts`, the five islands) rather than inventing an abstract system. This is not in dispute.

## Point of divergence — and its resolution

The real fight is over **Criterion 4 (honoring prior recorded decisions)**, and it's where Mistral's pro-A vote gets specifically rebutted by the majority.

- **Mistral's case for A:** A is more decisive because it unilaterally promotes GSAP + WebGL to the primary harness and treats the old skip-list as void now that the cost/license rationale (Webflow's GSAP-free move) disappeared. Mistral frames B's "Owner fork" section as unresolved hedging.
- **The majority's rebuttal (Claude, GPT-5.4-mini, DeepSeek):** A's move isn't just "updating a stale doctrine" — it overrides a **kill switch a prior spec explicitly wrote in good faith** (`interactive-explainer-tooling-research-v1.md`'s "if any tool means hiding the scrubber or shipping passive video... stop") *and* a second hard-coded ban in `CLAUDE.md`/`DESIGN.md` ("No GSAP, no Lenis"). A resolves this by declaring the rationale void and rewriting the doctrine (§1.7) — a real reversal, done transparently, but a reversal nonetheless. Claude specifically flags that Mistral's read "overlooks" this. B instead treats the exact same tension — owner lifted the ban, but two prior docs still forbid the tool — as *the* decision that must be surfaced rather than resolved by the spec-writer, and recommends the lighter native-platform path (WAAPI/IntersectionObserver + `@supports`-gated CSS scroll animation) as the default, deferring GSAP/Rive/Three.js with named gates. That is the more disciplined treatment of "honor prior recorded decisions" as the rubric literally asks for.

This is the crux: what Mistral reads as A's strength (decisive override) is what the majority reads as A's Criterion-4 weakness (spectacle overriding a prior explicit lock), and what Mistral reads as B's weakness (an "unresolved fork") is what the majority reads as B's Criterion-4 strength (surfacing the collision honestly instead of quietly overruling it).

## The tie-breaking evidence (Criterion 3)

Claude and GPT-5.4-mini both flag a concrete, checkable asymmetry: A's evidence trail includes an **unverified/optimistic engineering claim** — a "~40kB gzipped" budget for GSAP core + DrawSVG + MorphSVG + MotionPath that no reviewer could confirm and that reads as asserted rather than measured. B, by contrast, cites specific external facts that are independently checkable (caniuse support levels for `animation-timeline: view()` by browser/version) and — most notably — **claims to have actually run the real `audit_intent_spec` MCP tool** against its own spec, then reconciles its literal, imperfect, chunk-scanned 19/25 output against its own hand-run rather than self-declaring a clean pass. That is closer to what the rubric means by "verify against the real system... the actual tool" than A's self-graded validation section. DeepSeek independently corroborates this by pointing to B's audit of seams the brief never named — the double role of `alt` text, the silently-degrading unregistered-variant seam, and the stale OG-card asset flagged in `CLAUDE.md` — as evidence of deeper direct inspection of the shipped codebase.

## Direct answer

**Artifact B is the stronger spec.** Both are comparably decided (Criterion 1) and neither self-contradicts (Criterion 2), so the verdict turns on Criteria 3 and 4: B verifies more of its claims against checkable, real-system facts (live browser-support data, an actually-invoked audit tool with an honestly-reconciled imperfect score) rather than an optimistic bundle-size assertion, and B treats the collision between the owner's newly lifted stack ban and two prior recorded architectural locks (`CLAUDE.md`/`DESIGN.md`'s explicit "no GSAP" and the tooling-research doc's kill switch) as a decision to surface openly rather than override by fiat — which is precisely what "honor prior recorded decisions in the codebase rather than proposing spectacle that ignores them" (Criterion 4) is asking for. A is not unreasonable — its doctrine-supersession move is transparent and its GSAP/WebGL choreography plan is genuinely more visually ambitious — but ambition purchased by quietly retiring a kill switch a previous session wrote in good faith is the exact failure mode the rubric penalizes.
