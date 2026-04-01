# Design Arena Aesthetic DNA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Aesthetic DNA profiles to the design-arena skill so each agent produces a visually distinct design, not just a layout variation.

**Architecture:** Create a new reference file with 10 Aesthetic DNA profiles (visual identity bundles). Modify SKILL.md to add a DNA assignment step, rewrite the agent prompt template to enforce visual commitments, and update success criteria. Light touch on creative-brief-library.md to note the pairing concept.

**Tech Stack:** Markdown only (skill files, reference docs). No code changes.

**Spec:** `docs/superpowers/specs/2026-03-31-design-arena-aesthetic-dna-design.md`

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `.claude/skills/design-arena/references/aesthetic-dna-library.md` | Create | 10 Aesthetic DNA profiles with all 7 dimensions |
| `.claude/skills/design-arena/SKILL.md` | Modify | DNA assignment section, agent prompt rewrite, success criteria, cross-refs |
| `.claude/skills/design-arena/references/creative-brief-library.md` | Modify | Add DNA pairing note at top |

---

### Task 1: Create the Aesthetic DNA Library

**Files:**
- Create: `.claude/skills/design-arena/references/aesthetic-dna-library.md`

- [ ] **Step 1: Create the file with header and profile structure**

Create `.claude/skills/design-arena/references/aesthetic-dna-library.md` with this exact content:

```markdown
# Aesthetic DNA Library

> Visual identity profiles that define HOW a design looks, moves, and feels — independent of WHERE things are placed (which is the layout brief's job). Each profile specifies 7 dimensions: design movement, typography, color application, texture, motion, signature interaction, and a "feels like" anchor.
>
> **Rules:**
> - No two agents in the same arena session share a DNA profile
> - Agents share the project's color palette tokens but apply them through their DNA's color application strategy
> - The signature interaction is MANDATORY — it must be implemented, not just described
> - Typography assignments are NON-NEGOTIABLE — agents must use their assigned fonts, not default to Inter/system

---

## Quick Reference

| # | Profile | Feels Like | Key Differentiator |
|---|---------|-----------|-------------------|
| 1 | Editorial Swiss | Magazine spread | Typography IS the design; extreme restraint |
| 2 | Neobrutalist | Zine / protest poster | Thick borders, offset shadows, raw energy |
| 3 | Glassmorphism Aurora | Premium fintech at 2am | Frosted glass, luminous borders, aurora orbs |
| 4 | Terminal Operator | Beautiful Bloomberg | All-monospace, CRT scanlines, ticker data |
| 5 | Minimal Luxury | Aesop product page | Extreme whitespace, whisper-quiet animation |
| 6 | Data Brutalism | Bloomberg meets FT | Numbers are oversized art, functional color |
| 7 | Kinetic Scroll | Apple product launch | Scroll IS the interaction, pinned sections |
| 8 | Bento Garden | Apple comparison page | Mixed-size card grid, 3D tilt hover |
| 9 | Retro Digital | Modern Game Boy | Pixel grid, stepped animation, limited palette |
| 10 | Dark Cinematic | Nolan title sequence | Film grain, clip-path reveals, spotlight hover |

---

## Profiles

### 1. Editorial Swiss

- **Design Movement:** Strong typographic hierarchy, grid discipline, generous whitespace, serif headlines. The typography IS the design — layout serves the type, not the other way around.
- **Typography:** Instrument Serif 400 headings / DM Sans 400 body / JetBrains Mono data
- **Color Application:** Near-monochromatic. Primary color used only for one accent element per section. Tinted warm neutrals everywhere else. 95/4/1 ratio (neutral/primary/accent).
- **Texture:** Clean surfaces. No noise, no grain. Depth comes from whitespace and type scale alone.
- **Motion:** Smooth decelerate (`cubic-bezier(0, 0, 0, 1)`). Slow, confident entrances. 600ms stagger at 80ms intervals. No springs — everything glides.
- **Signature Interaction:** Split-text line-by-line mask reveal on hero heading (GSAP SplitText style). Lines slide up from behind a clip-path mask with 80ms stagger.
- **Feels like:** A beautifully typeset magazine spread. Stripe's documentation meets The New York Times.

### 2. Neobrutalist

- **Design Movement:** Thick borders, solid offset shadows, bright color blocks, raw unpolished energy. Deliberately anti-polished — the roughness is the aesthetic.
- **Typography:** Syne 700 headings / Space Grotesk 400 body / Fira Code mono
- **Color Application:** High-contrast color blocks. Primary as large solid fills, not subtle accents. Black borders (3-4px) on everything. Accent color as offset drop-shadow (`4px 4px 0px`). No gradients — flat fills only.
- **Texture:** None. Flat, bold surfaces. Anti-texture is the texture. The border weight and shadow offset provide all the depth.
- **Motion:** Sharp and abrupt. `steps(1)` or instant state changes. No easing — things appear, they don't glide. Hover = instant color inversion or border-width jump.
- **Signature Interaction:** Cards with draggable offset shadows that follow cursor position with spring return. Shadow offset tracks mouse delta, snaps back on leave.
- **Feels like:** A zine or protest poster. Raw, opinionated, impossible to mistake for template UI.

### 3. Glassmorphism Aurora

- **Design Movement:** Frosted glass surfaces, luminous gradient borders, animated aurora backgrounds. Layered transparency creates depth and atmosphere.
- **Typography:** Manrope 600 headings / Manrope 400 body / Geist Mono data
- **Color Application:** Gradient-heavy. Primary-to-accent gradient on aurora orbs (10-15% opacity). Glass cards with luminous 1px gradient borders via `mask-composite`. Tinted cool neutrals. Background shows through everything.
- **Texture:** Layered: SVG noise at 4% opacity + `backdrop-filter: blur(16px)` on cards + animated radial-gradient orbs behind content (2-3 orbs, 300-400px, `filter: blur(80px)`).
- **Motion:** Gentle ambient. Orbs on slow 12s orbital loops (`transform` only). Cards enter with soft `spring(damping:25, stiffness:100)`. Everything breathes — nothing snaps.
- **Signature Interaction:** Spotlight cursor — radial-gradient mask follows mouse position, reveals hidden luminous content beneath glass cards. Content glows where the cursor touches.
- **Feels like:** A premium fintech app at 2am. Calm, atmospheric, alive.

### 4. Terminal Operator

- **Design Movement:** Monospace everything, green-on-dark, CRT aesthetic, information-dense. The interface IS a terminal — elevated to art.
- **Typography:** JetBrains Mono 600 headings / JetBrains Mono 400 body / JetBrains Mono data (yes, all monospace — this is the point)
- **Color Application:** Near-monochrome. Primary color as text and thin borders only — never as fills or backgrounds. Background is true OLED dark (#050505). Accent only for status indicators (red/amber/green semantic colors).
- **Texture:** Scanline overlay (`repeating-linear-gradient(transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px)`) + subtle CRT vignette (radial-gradient darkening edges at 5% opacity).
- **Motion:** Typewriter-style. Text appears character-by-character (30-50ms per char). Data updates tick like a stock terminal — numbers snap to new values, no interpolation. Cursor blinks at 530ms interval.
- **Signature Interaction:** Command-line input field that accepts text queries and filters/searches dashboard data in real-time. Blinking block cursor. Autocomplete dropdown styled as terminal suggestions.
- **Feels like:** Bloomberg Terminal if it were redesigned by a hacker with taste.

### 5. Minimal Luxury

- **Design Movement:** Extreme whitespace, thin serif type, muted earth tones, whisper-quiet animations. Every element earns its place through restraint.
- **Typography:** Fraunces 500 headings / Satoshi 400 body / IBM Plex Mono data
- **Color Application:** Muted and desaturated. Primary at 30% saturation. Cream/warm white backgrounds (#FAFAF5). Accent used once per page — a single colored line, dot, or word. The restraint IS the luxury.
- **Texture:** Subtle paper grain (`feTurbulence` at 2% opacity, `mix-blend-mode: multiply`). Warm, organic feel — surfaces feel like heavy stock paper.
- **Motion:** Ultra-slow and gentle. 800ms entrances with `cubic-bezier(0.33, 1, 0.68, 1)`. Elements drift into place like settling dust. Hover states are barely perceptible opacity shifts (0.7 → 1.0).
- **Signature Interaction:** Scroll-driven parallax where content layers separate at different depths as you scroll, creating a diorama/shadowbox effect. Foreground text, midground cards, background texture all move at different rates.
- **Feels like:** An Aesop product page. Quiet confidence. Every pixel earned its place.

### 6. Data Brutalism

- **Design Movement:** Data IS the design. Numbers are oversized. Charts are the hero. Metrics dominate the visual hierarchy — decoration is irrelevant.
- **Typography:** IBM Plex Sans 700 headings / IBM Plex Sans 400 body / IBM Plex Mono 500 data (data font is intentionally bolder than body — numbers outrank prose)
- **Color Application:** Functional color only. Green = up, red = down, amber = warning. Primary color reserved for the single most important metric on the page. Everything else is neutral. Colored left-borders (3px) on cards to encode category.
- **Texture:** Dot-grid background (`radial-gradient(circle, currentColor 1px, transparent 1px)` at 24px spacing, 5% opacity). The page feels like graph paper.
- **Motion:** Numbers animate with counting/ticking transitions (requestAnimationFrame counter). Charts draw on with `stroke-dashoffset` animation. Staggered but fast (40ms intervals, 300ms total duration).
- **Signature Interaction:** Hero metric with oversized `clamp(6rem, 15vw, 20rem)` number that animates counting from 0 to current value on page load (1.2s duration, decelerate easing), with a trailing inline sparkline SVG.
- **Feels like:** A Bloomberg-meets-FT data visualization. The numbers are the art.

### 7. Kinetic Scroll

- **Design Movement:** Scroll IS the interaction. The page is a choreographed sequence, not a static layout. Pinned sections, scrub animations, parallax layers.
- **Typography:** Geist Sans 600 headings / Geist Sans 400 body / Geist Mono data
- **Color Application:** Section-based color shifts. Each scroll section has its own color mood (dark → light → accent → dark). Color transitions are tied to scroll position, not state changes.
- **Texture:** Minimal. Clean surfaces so the motion is the texture. Optional grain (3% opacity) only during color transitions as a blending aid.
- **Motion:** Scroll-driven everything. CSS `animation-timeline: view()` for element entrances. GSAP ScrollTrigger for pinned sections with `scrub: true`. Lenis smooth scroll (`lerp: 0.1, duration: 1.2`). This agent's motion budget is 3x the others.
- **Signature Interaction:** A pinned hero section where scrolling scrubs through a multi-stage reveal sequence: background color shifts → title types in character-by-character → data cards fly in from edges → CTA pulses with scale. Full sequence takes ~3 viewport-heights of scroll distance.
- **Feels like:** An Apple product launch page. The scroll IS the experience.

### 8. Bento Garden

- **Design Movement:** Apple-style mixed-size card grid. Cards are varied sizes (span-2x2, span-1x2, span-2x1). Each card is a self-contained vignette with its own internal composition.
- **Typography:** System UI (SF Pro / Segoe UI / system-ui) 600 headings / system-ui 400 body / ui-monospace data. Fallback: Geist family.
- **Color Application:** Soft gradients within cards (very subtle, 2-3% opacity shift from top to bottom). Cards differentiated by surface tint — each card has a barely perceptible warm/cool hue shift. Light mode preferred. Primary color for interactive elements only.
- **Texture:** Subtle inner shadows on cards (`inset 0 1px 2px rgba(0,0,0,0.06)`). Layered external shadow system: `shadow-sm ring-1 ring-black/5` at rest → `shadow-lg ring-1 ring-black/10` on hover. Smooth elevation creates physicality.
- **Motion:** Spring-based hover: `spring(damping:20, stiffness:300)` with `scale(1.02)` + shadow elevation lift. Staggered grid entrance: `animation-delay: calc(var(--index) * 60ms)`. Playful but controlled — nothing overshoots.
- **Signature Interaction:** 3D tilt on card hover — `perspective(800px) rotateX/rotateY` tracking mouse position (max ±5deg), with inner content elements at different `translateZ` depths (0px, 20px, 40px) for parallax within each card. Spring return to flat on mouse leave.
- **Feels like:** Apple's product comparison pages. Each card is a tiny world.

### 9. Retro Digital

- **Design Movement:** Pixel-grid nostalgia meets modern layout. Chunky elements, limited palette, 8-bit-inspired constraints executed with modern CSS. The constraint IS the creativity.
- **Typography:** Press Start 2P (display only — headings and labels) / Space Mono 400 body / Space Mono data. Press Start 2P is tiny at body size, so use it only for headings and key labels.
- **Color Application:** Strictly limited palette — max 4-5 colors total. Primary + accent + 2 neutrals + 1 status color. No gradients whatsoever. Flat fills only. CSS dithering patterns (`repeating-radial-gradient` at 2px intervals) for mid-tone simulation.
- **Texture:** Pixel-grid overlay (1px lines at 8px intervals via `repeating-linear-gradient`, 3% opacity). Background has subtle grid structure. All border-radius values are 0 — sharp corners only.
- **Motion:** Stepped timing functions. `steps(4)` or `steps(8)` on all transitions. Things move in discrete jumps, never smooth curves. Loading bars fill in chunky increments. State changes feel like frame-by-frame animation.
- **Signature Interaction:** Loading states styled as retro progress bars — pixelated fill animation with chunky `steps(10)` timing, "LOADING..." text with 530ms blink, optional 8-bit-style sound via Web Audio (short square wave beep on completion).
- **Feels like:** A modern take on a Game Boy Color interface. Constrained, charming, impossible to confuse with anything else.

### 10. Dark Cinematic

- **Design Movement:** Moody, dramatic, film-inspired. High contrast, deep shadows, selective lighting. The UI is a dark stage — content appears in spotlights.
- **Typography:** Bricolage Grotesque 700 headings / DM Sans 400 body / JetBrains Mono data
- **Color Application:** Nearly monochrome with one hot accent. Background #09090B. Most UI rendered in 5-15% white opacity levels (`rgba(255,255,255,0.05)` to `rgba(255,255,255,0.15)`). Accent color appears only on primary actions and key data — like a spotlight on a dark stage. 90/2/8 ratio (dark/accent/light-text).
- **Texture:** Film grain on hero section (`feTurbulence baseFrequency="0.65"` + `feColorMatrix` for contrast + `mix-blend-mode: overlay` at 8% opacity). Vignette at viewport edges (`radial-gradient(ellipse, transparent 60%, rgba(0,0,0,0.4) 100%)`). Optional fog via large blurred radial-gradient at 3% opacity.
- **Motion:** Dramatic entrances. `clip-path: inset(100% 0 0 0)` → `inset(0)` reveals over 800ms with `cubic-bezier(0.05, 0.7, 0.1, 1)`. Elements emerge from darkness. Hover on cards = spotlight illumination (radial-gradient at pointer position, 10% opacity white, 200px radius).
- **Signature Interaction:** Card/image reveal with cinematic wipe — a colored overlay (accent at 80% opacity) sweeps left-to-right across the element, then the content beneath fades in with slight `scale(1.05)` → `scale(1)` over 600ms. Like a film scene transition.
- **Feels like:** A Nolan film's title sequence turned into a dashboard. Theatrical, moody, unforgettable.

---

## DNA Pairing Guidance

Each DNA profile pairs with a layout brief from `creative-brief-library.md`. Some pairings are natural (similar philosophy), others create productive creative tension.

| DNA Profile | Natural Layout Pairings | Unexpected (High-Creativity) Pairings |
|-------------|------------------------|--------------------------------------|
| Editorial Swiss | Narrative Flow, Editorial Scroll | Dense Operator (tension: dense + elegant) |
| Neobrutalist | Asymmetric Split, Micro-Site | Breathing Room (tension: raw + spacious) |
| Glassmorphism Aurora | Command Center, Card Stack | Dense Operator (tension: glass + data) |
| Terminal Operator | Dense Operator, Split Cockpit | Museum Gallery (tension: terminal + art) |
| Minimal Luxury | Breathing Room, Museum Gallery | Dense Operator (tension: luxury + data) |
| Data Brutalism | Dense Operator, Command Center | Editorial Scroll (tension: data + story) |
| Kinetic Scroll | Editorial Scroll, Narrative Flow | Split Cockpit (tension: scroll + panels) |
| Bento Garden | Command Center, Breathing Room | Narrative Flow (tension: grid + story) |
| Retro Digital | HUD Overlay, Retro Console | Breathing Room (tension: pixel + space) |
| Dark Cinematic | Split Cockpit, Immersive | Command Center (tension: drama + status) |

**Selection strategy:** For a 4-agent arena, pick profiles that are maximally different from each other (different font families, different texture approaches, different motion languages). Default to 2 natural pairings + 1-2 unexpected pairings per session for creative range. If the user named reference sites in the interview, bias one profile toward that aesthetic and make the others deliberately different.

## How to Customize

If none of the 10 profiles fit a project's needs, create a custom DNA using this template:

### [Profile Name]
- **Design Movement:** [One sentence — the visual worldview]
- **Typography:** [Heading font + weight] / [Body font + weight] / [Mono/data font + weight]
- **Color Application:** [How palette tokens get applied — ratios, where primary appears, neutral tinting strategy]
- **Texture:** [Surface treatment — technique, opacity, blend mode. Or "None" if flat is the point]
- **Motion:** [Easing curves, durations, stagger values, physics params. Or "Instant" if no-motion is the point]
- **Signature Interaction:** [One bespoke moment — what it does, how it works]
- **Feels like:** [Two reference anchors — "X meets Y"]
```

- [ ] **Step 2: Verify the file was created correctly**

Run: `wc -l .claude/skills/design-arena/references/aesthetic-dna-library.md`
Expected: ~170-180 lines

Run: `head -5 .claude/skills/design-arena/references/aesthetic-dna-library.md`
Expected: `# Aesthetic DNA Library` on line 1

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/design-arena/references/aesthetic-dna-library.md
git commit -m "feat(design-arena): add Aesthetic DNA library with 10 visual identity profiles

New reference file with 10 distinct Aesthetic DNA profiles that define
visual identity across 7 dimensions: design movement, typography, color
application, texture, motion, signature interaction, and feel-like anchor.
Includes pairing guidance table and custom profile template."
```

---

### Task 2: Add DNA Pairing Note to Creative Brief Library

**Files:**
- Modify: `.claude/skills/design-arena/references/creative-brief-library.md:1-3`

- [ ] **Step 1: Add DNA pairing note after the existing header**

In `.claude/skills/design-arena/references/creative-brief-library.md`, replace:

```markdown
# Creative Brief Library

> Reusable agent personas organized by project type. Select 3-4 briefs per arena session. Mix and match across categories — a dashboard project might benefit from one dashboard-specific brief and one borrowed from the editorial category for fresh perspective.
```

With:

```markdown
# Creative Brief Library

> Reusable agent personas organized by project type. Select 3-4 briefs per arena session. Mix and match across categories — a dashboard project might benefit from one dashboard-specific brief and one borrowed from the editorial category for fresh perspective.
>
> **DNA Pairing:** Each layout brief is now paired with an Aesthetic DNA profile (see `references/aesthetic-dna-library.md`) to create the full agent identity. The layout brief determines WHERE things go. The DNA profile determines HOW they look, move, and feel. See the pairing guidance table in the DNA library for recommended and unexpected combinations.
```

- [ ] **Step 2: Verify the change**

Run: `head -7 .claude/skills/design-arena/references/creative-brief-library.md`
Expected: Should show the header with the new DNA Pairing note in the blockquote.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/design-arena/references/creative-brief-library.md
git commit -m "docs(design-arena): add DNA pairing note to creative brief library"
```

---

### Task 3: Add Aesthetic DNA Assignment Section to SKILL.md

**Files:**
- Modify: `.claude/skills/design-arena/SKILL.md:74-76` (between Step 1 Context Assessment and Step 2 Creative Brief Configuration)

- [ ] **Step 1: Insert the new Aesthetic DNA Assignment section**

In `.claude/skills/design-arena/SKILL.md`, find this text (around line 86):

```markdown
**Step 2 — Creative Brief Configuration**
Propose 3-4 agent briefs based on the project type. Pull from `references/creative-brief-library.md` and customize to the specific project.
```

Insert the following **before** that block (between the end of Step 1 and start of Step 2):

```markdown
**Step 1.5 — Aesthetic DNA Assignment**

Each agent needs a unique visual identity — not just a different layout. Assign an **Aesthetic DNA profile** from `references/aesthetic-dna-library.md` to each agent. DNA profiles define 7 dimensions of visual identity:

| Dimension | What It Controls |
|-----------|-----------------|
| Design Movement | Overall visual philosophy (Editorial Swiss, Neobrutalist, etc.) |
| Typography | Specific fonts with weights — NON-NEGOTIABLE, agents must use their assigned fonts |
| Color Application | How shared palette tokens get applied (monochromatic vs gradient-heavy vs functional-only) |
| Texture & Materiality | Surface treatment (grain, glass, scanlines, dot-grid, or intentionally flat) |
| Motion Language | Easing, physics, entrance choreography, timing |
| Signature Interaction | One mandatory bespoke moment that makes someone screenshot the design |

**DNA selection rules:**
- No two agents in the same session share a DNA profile
- Pick profiles that are maximally different from each other (different font families, different texture approaches, different motion languages)
- Default to 2 natural pairings + 1-2 unexpected pairings for creative range
- If the user named reference sites in the interview, bias one profile toward that aesthetic and make the others deliberately different

Quick reference (full profiles in `references/aesthetic-dna-library.md`):

| DNA Profile | Feels Like | Key Differentiator |
|-------------|-----------|-------------------|
| Editorial Swiss | Magazine spread | Typography IS the design; extreme restraint |
| Neobrutalist | Zine / poster | Thick borders, offset shadows, raw energy |
| Glassmorphism Aurora | Premium fintech at 2am | Frosted glass, luminous borders, aurora orbs |
| Terminal Operator | Beautiful Bloomberg | All-monospace, CRT scanlines, ticker data |
| Minimal Luxury | Aesop product page | Extreme whitespace, whisper-quiet animation |
| Data Brutalism | Bloomberg meets FT | Numbers are oversized art, functional color |
| Kinetic Scroll | Apple product launch | Scroll IS the interaction, pinned sections |
| Bento Garden | Apple comparison page | Mixed-size card grid, 3D tilt hover |
| Retro Digital | Modern Game Boy | Pixel grid, stepped animation, limited palette |
| Dark Cinematic | Nolan title sequence | Film grain, clip-path reveals, spotlight hover |

```

- [ ] **Step 2: Update Step 2 to include DNA approval**

Replace the existing Step 2 text:

```markdown
**Step 2 — Creative Brief Configuration**
Propose 3-4 agent briefs based on the project type. Pull from `references/creative-brief-library.md` and customize to the specific project.

Present briefs to the user for approval. The user may:
- Approve all briefs as-is
- Swap out a brief for a different one
- Modify a brief's creative direction
- Add or remove agents (3-4 is the sweet spot)
```

With:

```markdown
**Step 2 — Creative Brief Configuration**
Propose 3-4 agent assignments, each combining a **layout brief** (from `references/creative-brief-library.md`) with an **Aesthetic DNA profile** (from `references/aesthetic-dna-library.md`). Present both together, e.g.:

> - **Agent A:** Dense Operator layout + Terminal Operator DNA
> - **Agent B:** Narrative Flow layout + Editorial Swiss DNA
> - **Agent C:** Split Cockpit layout + Dark Cinematic DNA
> - **Agent D:** Command Center layout + Glassmorphism Aurora DNA

Present assignments to the user for approval. The user may:
- Approve all assignments as-is
- Swap a DNA profile for a different one
- Swap a layout brief for a different one
- Request an unexpected pairing for creative tension
- Modify a brief or DNA's creative direction
- Add or remove agents (3-4 is the sweet spot)
```

- [ ] **Step 3: Verify changes**

Run: `grep -n "Aesthetic DNA" .claude/skills/design-arena/SKILL.md`
Expected: Multiple hits — the new section header, DNA selection rules, quick reference table, and the updated Step 2.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/design-arena/SKILL.md
git commit -m "feat(design-arena): add Aesthetic DNA assignment step and update brief configuration"
```

---

### Task 4: Rewrite Agent Prompt Template in SKILL.md

**Files:**
- Modify: `.claude/skills/design-arena/SKILL.md:96-119` (Step 3 — Agent Team Deployment)

- [ ] **Step 1: Replace the Shared Context and Unique Context sections**

Find the current Step 3 content that starts with "Create the Agent Team" and contains the numbered items for shared context and unique context. Replace from this block:

```markdown
**Step 3 — Agent Team Deployment**
Create the Agent Team. The lead agent (you) coordinates. Each creative agent receives:

1. **Shared context** (identical for all agents):
   - The project's design constraint document (existing spec or interview output)
   - Anti-patterns list (what NOT to do)
   - Target tech stack and component library
   - Instruction to reference `prompting-beautiful-ui` skill for visual vocabulary
   - Instruction to reference `micro-interaction-patterns` skill for motion design

2. **Unique context** (different per agent):
   - Their specific creative brief (layout philosophy, density, hierarchy emphasis)
   - A unique design frame name in the `.pen` file (e.g., `arena-agent-a-dense`, `arena-agent-b-spacious`)
   - Instruction: "Your design must be meaningfully different from the other agents. You share the same color palette, typography, and spacing tokens. Your creative freedom is in composition, layout, information hierarchy, component arrangement, and interaction patterns."

3. **Output target**:
   - **Pencil mode (default):** Each agent designs on a separate frame in the Pencil canvas using the Pencil MCP tools. Designs are visible to you in real-time.
   - **Code mode (fallback):** Each agent generates a standalone React + Tailwind page in a `/design-arena/` subdirectory. Run `npm run dev` to view.
```

With:

```markdown
**Step 3 — Agent Team Deployment**
Create the Agent Team. The lead agent (you) coordinates. Each creative agent receives a structured prompt built from their layout brief + Aesthetic DNA profile.

**Agent Prompt Template** (fill in per agent from their assignments):

~~~markdown
# Agent [X]: [Layout Brief Name] — [DNA Profile Name]

## Your Design Identity
You are designing with the **[DNA Profile Name]** aesthetic. This is your
visual worldview. Everything you create must feel like it belongs to this
movement. Read your full DNA profile in `references/aesthetic-dna-library.md`.

### Design Movement
[Movement description from DNA profile]

### Typography (NON-NEGOTIABLE — use these exact fonts)
- Headings: [Font] [Weight]
- Body: [Font] [Weight]
- Data/Mono: [Font] [Weight]

### Color Application (same palette, YOUR interpretation)
[Color application strategy from DNA profile — ratios, where primary
appears, neutral tinting approach]

### Texture & Materiality
[Texture approach from DNA profile — technique, opacity, blend mode]

### Motion Language
[Motion approach from DNA profile — easing, duration, stagger, physics]

### Signature Interaction (REQUIRED — this is your showpiece)
[Signature interaction from DNA profile — MUST be implemented, not just
described. This is the thing that makes someone screenshot your design.]

## Layout Brief
[Layout philosophy from creative-brief-library.md — structure, density,
information hierarchy approach]

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

## Anti-Convergence Self-Check
Before finalizing, verify:
1. Could someone tell your design apart from the others in under 2 seconds?
2. Is your signature interaction implemented and functional?
3. Are you using YOUR assigned fonts, not system defaults?
4. Is your texture/materiality approach visible in the output?
If any answer is "no," revise until all are "yes."

## Shared Constraints
- Project design tokens: [from spec or interview — palette, spacing scale]
- Tech stack: [React/Tailwind/etc.]
- Accessibility: WCAG AA, 44px touch targets, prefers-reduced-motion
- Performance: only animate transform and opacity, 60fps target
- Reference: `prompting-beautiful-ui` skill for techniques, `micro-interaction-patterns` for motion code
~~~

Each agent also receives:
- A unique design frame name in the `.pen` file (e.g., `arena-agent-a-terminal-operator`, `arena-agent-b-editorial-swiss`)
- The project's design constraint document (existing spec or interview output)

**Output target:**
- **Pencil mode (default):** Each agent designs on a separate frame in the Pencil canvas using the Pencil MCP tools. Designs are visible to you in real-time.
- **Code mode (fallback):** Each agent generates a standalone React + Tailwind page in a `/design-arena/` subdirectory. Run `npm run dev` to view.
```

- [ ] **Step 2: Verify the template is in place**

Run: `grep -n "Anti-Convergence" .claude/skills/design-arena/SKILL.md`
Expected: One hit in the new agent prompt template section.

Run: `grep -n "NON-NEGOTIABLE" .claude/skills/design-arena/SKILL.md`
Expected: Two hits — one in the DNA assignment section (Step 1.5), one in the agent prompt template (Step 3).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/design-arena/SKILL.md
git commit -m "feat(design-arena): rewrite agent prompt template with Aesthetic DNA and anti-convergence rules"
```

---

### Task 5: Update Success Criteria and Skill Cross-References in SKILL.md

**Files:**
- Modify: `.claude/skills/design-arena/SKILL.md:227-241` (Success Criteria)
- Modify: `.claude/skills/design-arena/SKILL.md:215-225` (Skill Cross-References)

- [ ] **Step 1: Update Success Criteria**

Find the existing success criteria block:

```markdown
## Success Criteria

- [ ] Context assessment completed before any agent deployment
- [ ] User approved all creative briefs before agents started
- [ ] Each agent produced a meaningfully different layout interpretation
- [ ] User evaluated every agent's output with specific keep/reject decisions
- [ ] A `design-direction.md` document was saved to the project directory
- [ ] Option B prototype was offered for interaction-heavy projects
- [ ] Build-out agents referenced the locked design direction, not their own creativity
- [ ] Design team reviewers ran on the final output before shipping
```

Replace with:

```markdown
## Success Criteria

- [ ] Context assessment completed before any agent deployment
- [ ] User approved all layout brief + Aesthetic DNA assignments before agents started
- [ ] Each agent used its assigned typography (not Inter/system defaults)
- [ ] Each agent's signature interaction is implemented and functional
- [ ] No two agents share the same Aesthetic DNA profile
- [ ] Banned patterns list was enforced (no AI slop indicators)
- [ ] Each agent produced a meaningfully different visual interpretation (not just layout variation)
- [ ] User evaluated every agent's output with specific keep/reject decisions
- [ ] A `design-direction.md` document was saved to the project directory
- [ ] Option B prototype was offered for interaction-heavy projects
- [ ] Build-out agents referenced the locked design direction, not their own creativity
- [ ] Design team reviewers ran on the final output before shipping
```

- [ ] **Step 2: Update Skill Cross-References**

Find the existing cross-references table:

```markdown
| Phase | Skills Referenced | Assigned To |
|---|---|---|
| Act 1 (Creative) | `prompting-beautiful-ui`, `micro-interaction-patterns` | Creative agents |
| Act 2 (Evaluate) | `creative-director`, `visual-polish-checklist` | Lead agent (you + Claude) |
| Act 3 (Build) | `react-vite-tailwind`, `tailwind-advanced-patterns`, `animation-library-mastery` | Build agents |
| Act 3 (Review) | Design team agents (UI Reviewer, Accessibility, Enforcer, Polish) | Read-only reviewers |
```

Replace with:

```markdown
| Phase | Skills Referenced | Role |
|---|---|---|
| Act 1 (DNA Assignment) | `prompting-beautiful-ui` | **Core dependency** — DNA profiles draw from its design movements, font pairings, texture techniques, and banned patterns list |
| Act 1 (Creative) | `prompting-beautiful-ui`, `micro-interaction-patterns` | Creative agents reference for implementation techniques |
| Act 2 (Evaluate) | `creative-director`, `visual-polish-checklist` | Lead agent (you + Claude) |
| Act 3 (Build) | `react-vite-tailwind`, `tailwind-advanced-patterns`, `animation-library-mastery` | Build agents |
| Act 3 (Review) | Design team agents (UI Reviewer, Accessibility, Enforcer, Polish) | Read-only reviewers |
```

- [ ] **Step 3: Verify changes**

Run: `grep -n "Aesthetic DNA" .claude/skills/design-arena/SKILL.md | wc -l`
Expected: 3+ hits (DNA assignment section, success criteria, cross-references)

Run: `grep -n "signature interaction" .claude/skills/design-arena/SKILL.md | wc -l`
Expected: 3+ hits (DNA section, prompt template, success criteria)

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/design-arena/SKILL.md
git commit -m "feat(design-arena): update success criteria and cross-references for Aesthetic DNA"
```

---

### Task 6: Final Validation

**Files:**
- All modified files

- [ ] **Step 1: Run the project validator**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && python3 scripts/validate.py
```

Expected: 0 errors. Warnings are acceptable (block-secrets hook warnings are known).

- [ ] **Step 2: Verify all references resolve**

Check that the SKILL.md references to the new file exist:

```bash
test -f .claude/skills/design-arena/references/aesthetic-dna-library.md && echo "OK: DNA library exists" || echo "FAIL: DNA library missing"
test -f .claude/skills/design-arena/references/creative-brief-library.md && echo "OK: Brief library exists" || echo "FAIL: Brief library missing"
test -f .claude/skills/design-arena/references/evaluation-rubric.md && echo "OK: Rubric exists" || echo "FAIL: Rubric missing"
```

Expected: All three print "OK".

- [ ] **Step 3: Verify no duplicate DNA profile names**

```bash
grep "^### [0-9]" .claude/skills/design-arena/references/aesthetic-dna-library.md | sort | uniq -d
```

Expected: No output (no duplicates).

- [ ] **Step 4: Verify banned patterns list is in the agent template**

```bash
grep -c "Banned Patterns" .claude/skills/design-arena/SKILL.md
```

Expected: 1 (in the agent prompt template).

- [ ] **Step 5: Final commit if any fixes were needed**

Only if validation or checks revealed issues that needed fixing:

```bash
git add -A
git commit -m "fix(design-arena): address validation issues from Aesthetic DNA implementation"
```

- [ ] **Step 6: Summary verification**

Confirm the final state matches the spec:
- `.claude/skills/design-arena/references/aesthetic-dna-library.md` — 10 profiles, pairing table, custom template
- `.claude/skills/design-arena/SKILL.md` — Step 1.5 (DNA assignment), Step 2 (dual assignment approval), Step 3 (new agent prompt template), updated success criteria, updated cross-references
- `.claude/skills/design-arena/references/creative-brief-library.md` — DNA pairing note at top
