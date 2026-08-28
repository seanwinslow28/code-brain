# Presentation Format Library

Seven presentation formats, each with the format-specific brief, the structural pattern, and the trade-offs to navigate. Read this file when the user has named a format — or when the user has described what they need and you're matching it to a format.

---

## 1. Multi-Slide Deck (`deck`)

**Use when:** Internal team presentation, customer briefing, board update, training, sales deck — any multi-slide presentation that's *not* an investor pitch (those go to `pitch`) or a conference talk (those go to `talk`).

**The brief:** Design a multi-slide presentation using Excalidraw-style frame-based layout. Apply audience-appropriate visual hierarchy, enforce the 3-second rule on every frame, and use consistent visual language throughout.

**Structural pattern:**
- Cover frame — title, subtitle, presenter, date
- Agenda or roadmap frame
- Section openers between major chapters (single concept, large type)
- Content frames — one core idea per frame, max
- Summary / call-to-action frame

**Frame-level rules:**
- 3-second rule: someone glancing at any frame can grasp the core idea in three seconds
- One job per frame — inform, persuade, transition, or cut it
- Generous white space — cramming kills comprehension
- Consistent type ramp, color, and grid throughout
- Visual hierarchy drives the eye's journey deliberately

**Trade-offs:**
- Frame count vs. cohesion: more frames = easier to skim but harder to maintain narrative tension
- Type-heavy vs. visual-heavy: lean visual unless the audience will read this without you presenting

---

## 2. YouTube / Video Explainer (`explainer`)

**Use when:** Short-form video (3–10 min), educational or product explainer, YouTube channel content, embedded explainer video. Engagement is the metric.

**The brief:** Design a YouTube explainer layout. Produce a visual script with engagement hooks at 0s, 3s, and every 15–30s; specify on-screen visuals per beat; apply bold, casual typographic style appropriate to the platform.

**Structural pattern:**
- 0–3s — **The hook.** Concrete, specific, surprising. Stop the scroll.
- 3–15s — Promise the payoff. Why should the viewer stay?
- 15s onward — Build in beats. New visual or structural moment every 15–30s. Pattern interrupts.
- Final 30s — Payoff + clear next action.

**Beat-level rules:**
- Every beat has on-screen visuals (don't make audio the whole job)
- Typography is bold, casual, platform-native — not corporate
- Engagement hooks roughly every 15–30 seconds: cut to a new visual, change pace, ask a question, reveal a surprise, show a prop
- Cut anything that doesn't earn its runtime

**Trade-offs:**
- Polish vs. authenticity: over-produced explainers can underperform vs. authentic-feeling ones, especially on YouTube
- Density vs. accessibility: density kills retention on a channel for a general audience

---

## 3. Investor Pitch Deck (`pitch`)

**Use when:** Fundraising pitch (seed, Series A, etc.), board pitch for a major bet, partnership pitch where capital or commitment is on the line.

**The brief:** Craft an investor pitch presentation. Build a narrative arc (problem → solution → traction → ask), design data visualizations that make the numbers pop, and enforce a polished, professional visual language.

**Structural pattern (the canonical 10–12 slide arc):**
1. Title — company, tagline, presenter
2. Problem — visceral, specific, big
3. Solution — what we do, in one sentence + one image
4. Why now — what changed in the world that makes this possible/inevitable
5. Market — TAM/SAM/SOM with credible sourcing
6. Product — live demo or screenshot, what makes it different
7. Traction — numbers, growth curve, logos, milestones
8. Business model — how we make money
9. Competition — who else is here, why we win (positioning map, not feature table)
10. Team — why this team can execute this
11. The ask — how much, used for what, what runway it buys
12. Vision (optional close) — what the world looks like if we win

**Slide-level rules:**
- One headline insight per slide (not a topic, an *insight*)
- Data visualizations that make the number obvious — no chart that requires squinting
- Polished, professional visual language — not flashy, not corporate-bland
- Speaker carries the story; slides support the speaker, not vice versa

**Trade-offs:**
- Optimism vs. honesty on traction: investors discount obvious puffery; honesty about where you are now beats vague hand-waves
- Polish vs. progress: highly polished decks can suggest more time on the deck than the product; balance matters

---

## 4. Conference Talk / Workshop (`talk`)

**Use when:** Live conference talk (15–45 min), workshop session, keynote, internal all-hands. Live audience, large room.

**The brief:** Build a conference talk or workshop presentation. Include speaker notes per slide, design for a live audience (large type, minimal text on slide), and structure a hook-build-payoff narrative.

**Structural pattern:**
- **Hook** (first 60s) — a story, a provocation, a contrarian claim, or a vivid example
- **Premise** — what you're going to argue or teach
- **Build** — the three or four moves that earn the conclusion
- **Payoff** — the specific takeaway the audience leaves with
- **Call to action** (optional) — what they should do next

**Slide-level rules:**
- Slides are *poster art*, not documents. One image, one phrase, large type.
- Body type: 32pt minimum, ideally 40–60pt+
- Minimal text per slide — if you need bullets, you're writing, not presenting
- Speaker notes capture what you'll *say* per slide. The slide is the prompt; the human is the message.
- High contrast — large rooms with bright projectors murder subtle palettes
- One idea per slide; build progressive reveals if needed instead of dense single slides

**Trade-offs:**
- Detail vs. memorability: most talks try to teach too much. Three points well earned beat seven half-explained
- Slide count: more slides ≠ more value; a skilled speaker can use one slide for ten minutes

---

## 5. Infographic / Information Visualization (`infographic`)

**Use when:** Data-heavy explanation, standalone-readable visualization, content marketing, embedded chart in an article, single-image data story.

**The brief:** Design a creative information visualization. Choose the chart/diagram type that lets the data tell the story, layer visual storytelling on top of the data, and cut every pixel that doesn't inform-persuade-or-transition.

**Structural pattern:**
- Headline — the insight in one phrase (the headline IS the insight, not a topic)
- Subhead — context the headline depends on
- Primary visual — the chart, diagram, or hierarchy that *earns* the headline
- Supporting visuals — only if they answer a question the primary visual raises
- Source line — small but present (data lineage matters for credibility)

**Chart-type matching:**
- Comparison across categories → bar chart
- Composition / parts of whole → stacked bar (rarely pie)
- Distribution → histogram or strip plot
- Correlation → scatter
- Change over time → line (single series) or small multiples (many series)
- Hierarchy → tree map or org chart
- Flow → Sankey or process diagram

**Pixel-level rules:**
- Cut anything that doesn't *inform*, *persuade*, or *transition*
- Don't decorate — design
- Annotations earn their space by adding insight, not labels
- Color used semantically (categorical, sequential, diverging) — never decoratively

**Trade-offs:**
- Density vs. legibility: cramming all data on one image kills it
- Standalone-readable vs. presenter-explained: standalone needs more annotation; presenter-explained can stay clean

---

## 6. Visual Metaphor / Conceptual Illustration (`metaphor`)

**Use when:** Explaining a complex concept memorably — Rube Goldberg machine, journey map, creative process diagram, system architecture as metaphor. Memorability over comprehensiveness.

**The brief:** Create a conceptual illustration — Rube Goldberg machine, journey map, or creative-process diagram. Use visual metaphor to explain the concept; prioritize memorability over comprehensiveness.

**Structural pattern:**
- The metaphor (the borrowed structure: machine, map, kitchen, garden, theater, etc.)
- The mapping (which concept = which part of the metaphor)
- The takeaway (what the metaphor lets the viewer *see* about the concept)

**Pattern rules:**
- The metaphor should add insight, not just decoration
- Pick a metaphor where the structure aligns — don't force-fit
- Memorable beats comprehensive — pick the three things to encode and let the rest go
- Hand-drawn or pencil-test aesthetic often beats slick — feels human, easier to engage

**Trade-offs:**
- Wit vs. clarity: a clever metaphor that obscures the concept fails; clarity wins
- Comprehensiveness vs. memorability: don't try to encode everything; pick the three things that matter

---

## 7. Single Concept Visual (`visual`)

**Use when:** A single image that *is* the explanation — Twitter/social hero image, blog header, slide thumbnail, single-frame "what is this?" answer.

**The brief:** Generate a single expressive image (concept visual) that explains the idea creatively and memorably. Apply visual metaphor, test the 3-second comprehension rule, and make the image the explanation — not a decoration on top of one.

**Structural pattern:** there's no structure; there's one image and a brief.

**Image-level rules:**
- The 3-second comprehension rule applies absolutely — if a viewer can't get it in three seconds, the image isn't doing its job
- Visual metaphor where possible — the image *is* the explanation, not decoration on top of one
- High contrast, clear focal point, deliberate eye journey
- One concept; if you're encoding two ideas, you're making two images
- Type, if used, is part of the image — not a caption stapled below

**Trade-offs:**
- Cleverness vs. instant-grasp: clever images can fail the 3-second rule; instant-grasp images can feel basic
- Stand-alone vs. context-needing: clarify which one this is in the brief

---

## Choosing a Format

If the user named the format, use it. Otherwise, match the brief to the format:

| User describes... | Format |
|---|---|
| "A deck for a meeting / sales / training" | `deck` |
| "A YouTube video / explainer / short-form video" | `explainer` |
| "An investor pitch / fundraising deck" | `pitch` |
| "A conference talk / keynote / workshop" | `talk` |
| "An infographic / data visualization / chart" | `infographic` |
| "A diagram / journey map / system illustration / Rube Goldberg" | `metaphor` |
| "A single image / hero visual / social card" | `visual` |
