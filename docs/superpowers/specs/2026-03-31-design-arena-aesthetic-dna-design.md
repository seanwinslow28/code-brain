# Design Arena Enhancement: Aesthetic DNA

**Date:** 2026-03-31
**Status:** Draft
**Approach:** A (Aesthetic DNA Layer) + elements of B (Enhanced Agent Prompt Template)

---

## Problem Statement

The design-arena skill deploys 3-4 agents to create competing UI interpretations, but all agents produce visually identical output. The screenshot evidence shows four "different" designs that are the same dark dashboard with green/orange accents, identical card chrome, same font, same visual language — the only difference is where the boxes go.

**Root cause:** The creative brief library differentiates agents on **layout and density** only (Dense Operator vs Breathing Room vs Split Cockpit). All agents share the same typography, color application, texture, and motion language. Layout-only variation produces format changes, not genuinely different design takes.

## Solution

Introduce **Aesthetic DNA** — a bundle of 7 visual identity dimensions assigned per-agent that makes it impossible for two agents to look alike. Each agent gets `Layout Brief + Aesthetic DNA = Unique Design`.

### The 7 Dimensions

| Dimension | What It Controls | Why It Matters |
|-----------|-----------------|----------------|
| Design Movement | Overall visual philosophy | Sets the entire worldview |
| Typography Pairing | Specific heading + body + mono fonts with weights | Fonts are the #1 differentiator — same font = same look |
| Color Application | How the shared palette gets used (not which colors) | Same hex values, wildly different results |
| Texture & Materiality | Surface treatment | Flat vs grain vs glass vs scanlines = instant differentiation |
| Motion Language | Easing, physics, entrance choreography | Motion is feel — spring bounce vs smooth decelerate vs sharp snap |
| Signature Interaction | One mandatory bespoke moment per agent | The thing that makes someone screenshot the design |
| Layout Philosophy | Pulled from existing layout briefs | Unchanged from current system |

**Key insight:** Agents share color palette tokens but apply them through completely different strategies. One agent uses the primary color as a single accent dot; another uses it as a full gradient wash.

## Deliverables

### 1. New File: `references/aesthetic-dna-library.md`

10 distinct Aesthetic DNA profiles, each specifying all 7 dimensions:

#### Profile 1: Editorial Swiss
- **Movement:** Strong typographic hierarchy, grid discipline, generous whitespace, serif headlines
- **Typography:** Instrument Serif 400 headings / DM Sans 400 body / JetBrains Mono data
- **Color Application:** Near-monochromatic. Primary color used only for one accent element per section. Tinted warm neutrals everywhere else. 95/4/1 ratio.
- **Texture:** Clean surfaces. No noise, no grain. Depth comes from whitespace and type scale alone.
- **Motion:** Smooth decelerate (`cubic-bezier(0, 0, 0, 1)`). Slow, confident entrances. 600ms stagger at 80ms intervals. No springs.
- **Signature Interaction:** Split-text line-by-line mask reveal on hero heading (GSAP SplitText style)
- **Feels like:** A beautifully typeset magazine spread. Stripe's documentation meets The New York Times.

#### Profile 2: Neobrutalist
- **Movement:** Thick borders, solid offset shadows, bright color blocks, raw unpolished energy
- **Typography:** Syne 700 headings / Space Grotesk 400 body / Fira Code mono
- **Color Application:** High-contrast color blocks. Primary as large solid fills, not subtle accents. Black borders (3-4px) on everything. Accent color as offset drop-shadow (4px 4px 0px).
- **Texture:** None. Flat, bold surfaces. Anti-texture is the texture.
- **Motion:** Sharp and abrupt. `steps(1)` or instant state changes. No easing — things appear, they don't glide. Hover = instant color inversion.
- **Signature Interaction:** Cards with draggable offset shadows that follow cursor position with spring return
- **Feels like:** A zine or protest poster. Raw, opinionated, impossible to mistake for template UI.

#### Profile 3: Glassmorphism Aurora
- **Movement:** Frosted glass surfaces, luminous gradient borders, animated aurora backgrounds
- **Typography:** Manrope 600 headings / Manrope 400 body / Geist Mono data
- **Color Application:** Gradient-heavy. Primary-to-accent gradient on aurora orbs (10-15% opacity). Glass cards with luminous 1px gradient borders via `mask-composite`. Tinted cool neutrals.
- **Texture:** Layered: SVG noise at 4% + backdrop-blur(16px) on cards + animated radial-gradient orbs behind content
- **Motion:** Gentle ambient. Orbs on slow 12s orbital loops (`transform` only). Cards enter with soft `spring(damping:25, stiffness:100)`. Everything breathes.
- **Signature Interaction:** Spotlight cursor — radial-gradient mask follows mouse, reveals hidden luminous content beneath glass cards
- **Feels like:** A premium fintech app at 2am. Calm, atmospheric, alive.

#### Profile 4: Terminal Operator
- **Movement:** Monospace everything, green-on-dark, CRT aesthetic, information-dense
- **Typography:** JetBrains Mono 600 headings / JetBrains Mono 400 body / JetBrains Mono data (all mono)
- **Color Application:** Near-monochrome. Primary color as text and thin borders only — never as fills. Background is true OLED dark (#050505). Accent only for status indicators (red/amber/green).
- **Texture:** Scanline overlay (repeating-linear-gradient, 2px, 3% opacity) + subtle CRT vignette (radial-gradient darkening edges)
- **Motion:** Typewriter-style. Text appears character-by-character. Data updates tick like a stock terminal. No smooth transitions — numbers snap to new values.
- **Signature Interaction:** Command-line input field that accepts text queries and filters dashboard data in real-time, with blinking cursor
- **Feels like:** Bloomberg Terminal if it were redesigned by a hacker with taste.

#### Profile 5: Minimal Luxury
- **Movement:** Extreme whitespace, thin serif type, muted earth tones, whisper-quiet animations
- **Typography:** Fraunces 500 headings / Satoshi 400 body / IBM Plex Mono data
- **Color Application:** Muted and desaturated. Primary at 30% saturation. Cream/warm white backgrounds (#FAFAF5). Accent used once per page — a single colored line, dot, or word.
- **Texture:** Subtle paper grain (feTurbulence at 2% opacity). Warm, organic feel.
- **Motion:** Ultra-slow and gentle. 800ms entrances with `cubic-bezier(0.33, 1, 0.68, 1)`. Elements drift into place. Hover states are barely perceptible opacity shifts (0.7 -> 1.0).
- **Signature Interaction:** Scroll-driven parallax where content layers separate at different depths as you scroll, creating a diorama effect
- **Feels like:** An Aesop product page. Quiet confidence. Every pixel earned its place.

#### Profile 6: Data Brutalism
- **Movement:** Data IS the design. Numbers are oversized. Charts are the hero. Metrics dominate.
- **Typography:** IBM Plex Sans 700 headings / IBM Plex Sans 400 body / IBM Plex Mono 500 data (data font bolder than body)
- **Color Application:** Functional color only. Green = up, red = down, amber = warning. Primary color reserved for the single most important metric. Everything else is neutral. Colored left-borders (3px) on cards to encode category.
- **Texture:** Dot-grid background (radial-gradient dots at 24px spacing, 5% opacity). Graph paper feel.
- **Motion:** Numbers animate with counting/ticking transitions. Charts draw on with `stroke-dashoffset`. Staggered but fast (40ms intervals, 300ms total).
- **Signature Interaction:** Hero metric with oversized `clamp(6rem, 15vw, 20rem)` number that animates counting from 0 to current value on page load, with trailing sparkline
- **Feels like:** A Bloomberg-meets-FT data visualization. The numbers are the art.

#### Profile 7: Kinetic Scroll
- **Movement:** Scroll IS the interaction. Pinned sections, scrub animations, parallax layers, horizontal scroll zones
- **Typography:** Geist Sans 600 headings / Geist Sans 400 body / Geist Mono data
- **Color Application:** Section-based color shifts. Each scroll section has its own color mood (dark -> light -> accent -> dark). Transitions happen on scroll position.
- **Texture:** Minimal. Clean surfaces so the motion is the texture. Optional grain during transitions only.
- **Motion:** Scroll-driven everything. CSS `animation-timeline: view()` for element entrances. GSAP ScrollTrigger for pinned sections with scrub. Lenis smooth scroll. This agent's motion budget is 3x the others.
- **Signature Interaction:** A pinned hero section where scrolling scrubs through a multi-stage reveal: background color shifts -> title types in -> data cards fly in from edges -> CTA pulses
- **Feels like:** An Apple product launch page. The scroll IS the experience.

#### Profile 8: Bento Garden
- **Movement:** Apple-style mixed-size card grid. Cards are varied sizes (span-2x2, span-1x2, span-2x1). Each card is a self-contained vignette.
- **Typography:** SF Pro Display (system) 600 headings / SF Pro Text 400 body / SF Mono data (fallback: Geist family)
- **Color Application:** Soft gradients within cards (very subtle, 2-3% opacity shift). Cards differentiated by surface tint — each card has a barely perceptible hue. Light mode preferred.
- **Texture:** Subtle inner shadows on cards. Layered shadow system: `shadow-sm ring-1 ring-black/5` at rest, `shadow-lg ring-1 ring-black/10` on hover. Smooth elevation.
- **Motion:** Spring-based hover: `spring(damping:20, stiffness:300)` scale(1.02) + shadow elevation lift. Staggered grid entrance with `animation-delay: calc(var(--index) * 60ms)`. Playful but controlled.
- **Signature Interaction:** 3D tilt on card hover — `perspective(800px) rotateX/rotateY` tracking mouse position, with inner content at different `translateZ` depths for parallax within each card
- **Feels like:** Apple's product comparison pages. Each card is a tiny world.

#### Profile 9: Retro Digital
- **Movement:** Pixel-grid nostalgia meets modern layout. Chunky elements, limited palette, 8-bit-inspired but executed with modern CSS.
- **Typography:** Press Start 2P (display only, headings) / Space Mono 400 body / Space Mono data
- **Color Application:** Strictly limited palette — max 4-5 colors total. Primary + accent + 2 neutrals + 1 status color. No gradients. Flat fills only. Dithering patterns via CSS for mid-tones.
- **Texture:** Pixel-grid overlay (1px repeating lines at 8px intervals, 3% opacity). Optional dithering via tiny repeating-radial-gradient patterns.
- **Motion:** Stepped. `steps(4)` or `steps(8)` timing functions. Things move in discrete jumps, not smooth curves. Loading bars fill in chunky increments.
- **Signature Interaction:** Loading states styled as retro progress bars with pixel-art fill animation and "LOADING..." blink
- **Feels like:** A modern take on a Game Boy Color interface. Constrained, charming, impossible to confuse with anything else.

#### Profile 10: Dark Cinematic
- **Movement:** Moody, dramatic, film-inspired. High contrast, deep shadows, selective lighting.
- **Typography:** Bricolage Grotesque 700 headings / DM Sans 400 body / JetBrains Mono data
- **Color Application:** Nearly monochrome with one hot accent. Background #09090B. Most UI in 5-15% white opacity levels. Accent color appears only on primary actions and key data — like a spotlight on a dark stage.
- **Texture:** Grain gradient on hero (feTurbulence + high contrast + mix-blend-mode). Vignette darkening at viewport edges. Subtle fog/mist effect via large blurred radial-gradient at 3% opacity.
- **Motion:** Dramatic entrances. `clip-path: inset(100% 0 0 0)` -> `inset(0)` reveals. 800ms, `cubic-bezier(0.05, 0.7, 0.1, 1)`. Elements emerge from darkness. Hover = spotlight illumination (radial gradient follows cursor on card surface).
- **Signature Interaction:** Image/card reveal with wipe — a colored overlay sweeps across, then the content fades in with slight scale(1.05) -> scale(1), like a film scene transition
- **Feels like:** A Nolan film's title sequence turned into a dashboard. Theatrical, moody, unforgettable.

### 2. Modified File: `SKILL.md`

#### Changes to Step 2 — Creative Brief Configuration (Act 1)

**Before:** "Propose 3-4 agent briefs based on the project type."

**After:** Two-step assignment:
1. Select layout briefs from the creative brief library (as before)
2. Assign an Aesthetic DNA profile to each agent from the DNA library — no two agents share a DNA profile in the same session

**DNA selection strategy:** Pick profiles that are maximally different from each other (different movements, different font families, different texture approaches). Use the pairing table to match DNA to layout briefs — default to one "natural" pairing and one "unexpected" pairing per session for creative range. If the user specified reference sites in the interview (e.g., "like Linear"), bias one profile toward that aesthetic and make the others deliberately different.

Present both assignments to the user for approval. The user may:
- Swap DNA profiles between agents
- Request a different DNA profile from the library
- Request an unexpected pairing for creative tension

#### Changes to Step 3 — Agent Team Deployment (Act 1)

Replace the current "Unique context" section with the enhanced agent prompt template:

```markdown
# Agent [X]: [Brief Name] — [DNA Name]

## Your Design Identity
You are designing with the **[DNA Name]** aesthetic. This is your visual worldview.
Everything you create must feel like it belongs to this movement.

### Design Movement
[Movement description from DNA profile]

### Typography (NON-NEGOTIABLE — use these exact fonts)
- Headings: [Font] [Weight]
- Body: [Font] [Weight]
- Data/Mono: [Font] [Weight]
- Hero scale: [clamp() value or specific sizing strategy]

### Color Application (same palette, YOUR interpretation)
[Color application strategy from DNA profile. Specify exact ratios,
where the primary color appears, how neutrals are tinted.]

### Texture & Materiality
[Texture approach from DNA profile. Be specific: what technique,
what opacity, what blend mode.]

### Motion Language
[Motion approach from DNA profile. Specify easing curves, durations,
stagger values, physics parameters.]

### Signature Interaction (REQUIRED — this is your showpiece)
[Signature interaction from DNA profile. This MUST be implemented.
It is the thing that makes someone screenshot your design.]

## Layout Brief
[Layout philosophy from the creative brief library]

## Banned Patterns (violating these = failed design)
- Inter/Roboto/Arial as your only font
- Purple/indigo gradients
- Cards nested inside cards with uniform padding
- Pure gray text (#666, #888) — use tinted neutrals
- Pure black (#000000) backgrounds — use near-black with tint
- shadow-lg on everything without elevation hierarchy
- "transition: all 0.3s ease" as the only animation
- Symmetric hero sections with even accent distribution
- Everything looking equally important (no hierarchy)
- Looking like the other agents' designs

## Anti-Convergence Rule
Before finalizing your design, verify:
1. Could someone tell your design apart from the other agents' in under 2 seconds?
2. Does your signature interaction exist and work?
3. Are you using YOUR fonts, not defaulting to system fonts?
4. Is your texture/materiality approach visible?
If any answer is "no," you have not differentiated enough. Revise.

## Shared Constraints (all agents must follow)
- Project design tokens: [from spec or interview]
- Tech stack: [React/Tailwind/etc.]
- Accessibility: WCAG AA, 44px touch targets, prefers-reduced-motion
- Performance: only animate transform and opacity, 60fps target
- Reference skills: `prompting-beautiful-ui` for techniques, `micro-interaction-patterns` for motion
```

#### New Section: "Aesthetic DNA Assignment" (between Steps 1 and 2)

Quick-reference table of all 10 profiles with pairing guidance:

| DNA Profile | Feels Like | Natural Layout Pairings | Unexpected (High-Creativity) Pairings |
|-------------|-----------|------------------------|--------------------------------------|
| Editorial Swiss | Magazine spread | Narrative Flow, Editorial Scroll | Dense Operator (tension: dense + elegant) |
| Neobrutalist | Zine / poster | Asymmetric Split, Micro-Site | Breathing Room (tension: raw + spacious) |
| Glassmorphism Aurora | Premium fintech at 2am | Command Center, Card Stack | Dense Operator (tension: glass + data) |
| Terminal Operator | Beautiful Bloomberg | Dense Operator, Split Cockpit | Museum Gallery (tension: terminal + art) |
| Minimal Luxury | Aesop product page | Breathing Room, Museum Gallery | Dense Operator (tension: luxury + data) |
| Data Brutalism | Bloomberg meets FT | Dense Operator, Command Center | Editorial Scroll (tension: data + story) |
| Kinetic Scroll | Apple product launch | Editorial Scroll, Narrative Flow | Split Cockpit (tension: scroll + panels) |
| Bento Garden | Apple comparison page | Command Center, Breathing Room | Narrative Flow (tension: grid + story) |
| Retro Digital | Modern Game Boy | HUD Overlay, Retro Console | Breathing Room (tension: pixel + space) |
| Dark Cinematic | Nolan title sequence | Split Cockpit, Immersive | Command Center (tension: drama + status) |

Guidance note: Natural pairings produce polished, coherent results. Unexpected pairings produce more creative tension and novel solutions — use them when the user wants to be surprised.

#### Updated Success Criteria

Add these to the existing checklist:
- [ ] Each agent used its assigned typography (not Inter/system defaults)
- [ ] Each agent's signature interaction is implemented and functional
- [ ] No two agents share the same Aesthetic DNA profile
- [ ] Banned patterns list was enforced (no AI slop)

#### Updated Skill Cross-References

Elevate `prompting-beautiful-ui` from optional reference to core dependency:

| Phase | Skills Referenced | Role |
|-------|-----------------|------|
| Act 1 (DNA Assignment) | `prompting-beautiful-ui` | **Core dependency** — DNA profiles draw from its design movements, font pairings, texture techniques, and banned patterns |
| Act 1 (Creative) | `prompting-beautiful-ui`, `micro-interaction-patterns` | Creative agents reference for implementation techniques |
| Act 2 (Evaluate) | `creative-director`, `visual-polish-checklist` | Lead agent (you + Claude) |
| Act 3 (Build) | `react-vite-tailwind`, `tailwind-advanced-patterns`, `animation-library-mastery` | Build agents |
| Act 3 (Review) | Design team agents | Read-only reviewers |

### 3. Modified File: `references/creative-brief-library.md`

Lightweight addition — a new section at the top noting that layout briefs are now paired with Aesthetic DNA profiles:

> **DNA Pairing:** Each layout brief is paired with an Aesthetic DNA profile (see `references/aesthetic-dna-library.md`) to create the full agent identity. The layout brief determines WHERE things go. The DNA profile determines HOW they look, move, and feel.

No changes to existing brief content.

## Files Changed Summary

| File | Action | Scope |
|------|--------|-------|
| `references/aesthetic-dna-library.md` | **Create** | 10 DNA profiles (~300 lines) |
| `SKILL.md` | **Modify** | Steps 2-3 rewrite, new DNA section, updated success criteria and cross-refs |
| `references/creative-brief-library.md` | **Modify** | Add DNA pairing note at top (~5 lines) |

## Out of Scope

- No changes to Act 2 (Synthesis Wall) or Act 3 (Build-Out)
- No changes to the evaluation rubric
- No changes to the condensed design interview
- No changes to other skills (prompting-beautiful-ui, micro-interaction-patterns, etc.)
- No new agents or hooks
