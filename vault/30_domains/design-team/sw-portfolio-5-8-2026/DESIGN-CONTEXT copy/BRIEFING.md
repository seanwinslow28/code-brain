# BRIEFING — Sean Winslow PM Portfolio Frontend

> **For the agent / designer reading this cold:** This is everything you need to start designing Sean Winslow's Product Manager portfolio website. Read this whole document before opening any subfolder. Every file referenced lives inside `DESIGN-CONTEXT/`.

---

<role>
You are a senior product designer and frontend engineer building a portfolio site for an AI Product Manager. Your job is to produce distinctive, editorial-grade UI — not a template. The site has to feel like it was made by someone who could ship it, not someone who bought it.
</role>

---

<project_context>

## What this is

A portfolio site for **Sean Winslow** — Product Manager pivoting from a 10-week stint at a crypto media co (The Block, laid off 2026-05-04) toward AI PM / Tech PM / Creative PM roles. The portfolio is the public surface of an 8-week job-hunt sprint.

## Who Sean is (one paragraph)

11+ years in product, most recently shipping production Claude Skills, an MCP-flavored agent fleet, and a Polymarket B2B integration. Background blends crypto media, SaaS, and digital asset management with a parallel creative practice (illustration, animation, filmmaking). The resume in `resumes/` is the canonical content source — pull copy from there, don't invent it.

## Target archetype priority (from `brand-voice/USER-decisions-and-archetype.md`)

1. **AI PM** — strongest target. Lead the site with this.
2. **Tech PM** — second priority.
3. **Creative PM** — third, but the creative practice (animation pipeline, 2D animation principles, Adobe MCP work) is a real differentiator and should appear, not be hidden.

The site must read as **"AI PM with creative-technologist range,"** not "designer who also does PM."

## Walk-away constraints (don't undermine these in copy)

- $100k+ base. No 5-day-in-office. Remote preferred; hybrid Boston-metro acceptable.
- Tone is confident and specific, never apologetic, never "open to anything."

</project_context>

---

<design_direction>

## North Star: "The Iterative Blueprint"

Sean already has a complete design system. **Read `design-system/01-iterative-blueprint-design-system.md` in full before generating any UI.** Summary of what it enforces:

- **Visual philosophy:** the screen is a *living desk* — technical documentation, blueprint vellum, and hand-drawn concepts overlapping. Asymmetry is intentional.
- **Palette:** "Ink and Earth." Deep technical teals (`#00272a` primary) on warm paper surfaces (`#fff9f0` background). No `#000000`. No 1px solid borders for sectioning — use background-color shifts.
- **Type stack:** Newsreader (editorial serif) for narrative + display, Inter for body + titles, Space Grotesk for labels and metadata.
- **Depth:** tonal layering, not drop shadows. If a shadow is needed, it's "ambient" (`0px 20px 40px rgba(32, 27, 18, 0.06)`).
- **Components:** rounded `md` (0.5rem) buttons, `lg` (1rem) cards, `none` (0px) chips. Forbidden: divider lines between list items — use 3rem of vertical white space instead.
- **Signature moves:** "Glass & Gradient" for AI-driven insight surfaces (frosted vellum, 70% opacity + 20px backdrop blur), and **Blueprint Annotations** — small Space Grotesk callouts with a 0.5px leader line pointing at UI elements. The annotation pattern is the design system's signature; use it.

## Reference images (`reference-images/`)

- `sw-portfolio-light-1.png` — current light-mode mockup, in-progress. This is where Sean is **right now**.
- `sw-portfolio-dark-2.png` — current dark-mode mockup, in-progress. Same.
- `AI-PM-Portfolio-reference.png` — external inspiration / north-star reference for what "good" looks like.

The current mockups are the starting point, not the finish line. Iterate on them; don't reset to a generic template.

</design_direction>

---

<voice_and_copy>

Read `brand-voice/SOUL-voice-and-anti-patterns.md` for the full rules. Distilled:

## Tone

**Default:** "Story-driven Sean Mode" — Sedaris-tuned. Self-deprecating humor, hyper-specific details, mundane-accumulation that pivots to a real point. **No corporate veneer.** No buzzword soup.

For a portfolio specifically, dial Sean Mode to ~70% — keep the warmth and specificity, drop most of the self-deprecation (a portfolio is not the place to undersell). Confident, dry, specific.

## Anti-patterns (don't write these)

- Generic "passionate about" / "results-driven" / "synergy" PM copy.
- "Open to opportunities" — replace with specific role targeting.
- "Innovative solutions" without naming the actual thing built.
- Walls of bullet points. Mix prose and lists; lean prose for the narrative parts.
- Calling the creative practice a "hobby" or hedging it. It's a craft and a differentiator.

## Voice rules

- **Lead with what shipped.** The 3 Claude Skills, the Polymarket integration, the agent fleet — these are concrete and load-bearing. Use them.
- **Numbers when you have them, none when you don't.** "40% productivity lift" yes. Vague gestures no.
- **Show range.** AI PM craft + 11 years of cross-domain product + an actual creative practice. The combination is the pitch.

</voice_and_copy>

---

<must_have_sections>

The portfolio needs (at minimum):

1. **Hero** — name, title ("AI Product Manager / Agentic Engineering Practitioner" or similar — pull from resume summary), one-line pitch, contact. Should feel editorial, not "tech bro."
2. **Selected Work** — at least these 4, sourced from `resumes/Sean_Winslow_Resume_MASTER.md`:
   - The Block — 3 production Claude Skills + Polymarket integration + Pro 2.0 prototype
   - New York Life — DAM rollout, AI workflow integration team lead
   - Claude Code Superuser Pack — open-source toolkit (117 skills, agent fleet)
   - 2D Animation Pipeline — June 2026 portfolio short (creative-technologist proof)
3. **About / Story** — the bridge between PM and creative-technologist. This is where Sean Mode runs warmest.
4. **Skills / Stack** — but visually, not as a wall of logos. Treat skill names as Blueprint Annotations or Space Grotesk chips.
5. **Contact** — Gmail, LinkedIn, GitHub, Substack (when live), Boston / remote signal.

Optional, but high-value if scope allows:

- **Now / Building** section — what Sean is currently shipping (the Track-C MCP server, build-in-public posts).
- **Writing / Substack** feed when content exists.
- **Dark mode toggle** — both reference mockups exist; the design system supports it.

</must_have_sections>

---

<technical_constraints>

- **Stack:** open. React + Vite + Tailwind is the default for Sean's prototypes (`personal-app-patterns` skill). Next.js is fine if SSR/SEO is wanted. Astro is fine if static + content-heavy is the target.
- **Hosting:** Vercel or Netlify. The domain `seanwinslow.com` is referenced in the resume header — that's the eventual production URL.
- **Performance:** images optimized, fonts subset, Lighthouse ≥95 on a portfolio is table stakes.
- **Accessibility:** WCAG 2.1 AA minimum. The design system already specifies "Ghost Border" patterns for forms; respect them.
- **No CMS for v1.** Content lives in markdown / MDX in-repo. Portfolio entries should be parameterized so a new project ships as a new MDX file, not a new component.

</technical_constraints>

---

<self_check>

Before declaring a design or build "done," verify:

- [ ] Pulled copy from `resumes/Sean_Winslow_Resume_MASTER.md` rather than inventing it
- [ ] Used the "Iterative Blueprint" tokens (no off-palette colors, no `#000000` text)
- [ ] No 1px solid borders for sectioning
- [ ] No drop shadows on every card; relied on tonal layering first
- [ ] Used Newsreader for display/headlines, Inter for body, Space Grotesk for labels/metadata
- [ ] At least one Blueprint Annotation appears somewhere (it's the signature pattern)
- [ ] AI PM is the primary archetype the site reads as
- [ ] Creative practice is visible and not hedged
- [ ] No "open to opportunities" / corporate-PM filler copy
- [ ] Lighthouse ≥95 on the deployed build
- [ ] Dark mode works and uses the design system's dark tokens

</self_check>

---

<file_index>

| Path | Why it matters |
|---|---|
| `design-system/01-iterative-blueprint-design-system.md` | **The** spec. Tokens, type, components, do's/don'ts. Read before generating UI. |
| `reference-images/sw-portfolio-light-1.png` | Current light mockup (work-in-progress baseline). |
| `reference-images/sw-portfolio-dark-2.png` | Current dark mockup (work-in-progress baseline). |
| `reference-images/AI-PM-Portfolio-reference.png` | External inspiration — the bar to clear. |
| `resumes/Sean_Winslow_Resume_MASTER.md` | Canonical copy source. Pull from here. |
| `resumes/Sean_Winslow_Resume_AI_PM.md` | AI PM–targeted variant. |
| `resumes/Sean_Winslow_Resume_Tech_PM.md` | Tech PM–targeted variant. |
| `resumes/Sean_Winslow_Resume_Creative_PM.md` | Creative PM–targeted variant. |
| `brand-voice/SOUL-voice-and-anti-patterns.md` | Tone rules, sacred cows, anti-patterns, communication norms. |
| `brand-voice/USER-decisions-and-archetype.md` | Target archetype priority, walk-away constraints, prioritization filters. |
| `strategy/2026-05-06-unified-roadmap.md` | 8-week job-hunt sprint plan — context for what the portfolio is *for*. |

</file_index>

---

<starter_prompt>

Suggested seed prompt for a fresh Claude / Cursor / v0 session:

> You are designing the portfolio site for Sean Winslow, an AI Product Manager. Read the entire `DESIGN-CONTEXT/` folder before producing any output. Start with `BRIEFING.md`, then the design system at `design-system/01-iterative-blueprint-design-system.md`, then the master resume at `resumes/Sean_Winslow_Resume_MASTER.md`. Match the "Iterative Blueprint" design system exactly — including the no-1px-borders rule, tonal layering instead of drop shadows, and at least one Blueprint Annotation as the signature pattern. The site must read primarily as "AI PM with creative-technologist range," not as a designer's portfolio. Iterate on the existing mockups in `reference-images/` rather than starting from a generic template. Pull all copy from the resume — don't invent it. Confirm understanding before generating code.

</starter_prompt>
