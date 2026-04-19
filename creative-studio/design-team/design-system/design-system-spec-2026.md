# Sean Winslow — Unified Design System Specification

> **Version:** 1.0
> **Date:** March 2, 2026
> **Source:** Design Discovery Interview — Claude × Sean Winslow
> **Purpose:** Hand this document directly to Claude Code, Perplexity Computer, or any development tool to begin building. Every decision here has been deliberately chosen and committed to. No reworking.

---

## 1. Design Philosophy

**"Engineered precision that rewards you with moments of warmth."**

This design system powers three interconnected projects through a single visual language inspired by the aesthetic of a **tech-filled art museum** — pristine, minimal containers that let expressive content shine. The system draws from Linear and Vercel's engineering-grade UI patterns while introducing a signature blue-and-orange color identity rooted in Sean's creative background and NYC roots.

A narrative duality runs through the system: **light mode tells the origin story** (the artist — tactile, warm, pencils on construction paper), while **dark mode represents the present** (the creative technologist — precise, engineered, cool). This isn't decoration; it's storytelling through interface design.

---

## 2. Color System

### Design Rationale
Blue and orange are complementary colors (opposite on the color wheel), creating natural visual tension and balance. This pairing is used extensively in film color grading for the same reason — it's dynamic without being chaotic. The 80/20 usage ratio (blue primary, orange accent) prevents the palette from reading as a sports jersey and ensures orange moments feel intentional and meaningful.

### Primary Palette

| Role | Token | Light Mode | Dark Mode | Usage |
|------|-------|------------|-----------|-------|
| Primary Blue | `--color-primary` | `#2563EB` | `#3B82F6` | Links, active states, primary buttons, selected items |
| Primary Blue Muted | `--color-primary-muted` | `#1E40AF` | `#60A5FA` | Hover states, secondary emphasis |
| Accent Orange | `--color-accent` | `#C2410C` | `#F97316` | CTAs, notifications, celebrations, attention signals |
| Accent Orange Muted | `--color-accent-muted` | `#9A3412` | `#FB923C` | Hover states on accent elements |

### Semantic Colors

| Role | Token | Value | Usage |
|------|-------|-------|-------|
| Success | `--color-success` | `#22C55E` | Agent running, habit completed, positive trends |
| Warning | `--color-warning` | `#F97316` | Maps to accent orange — attention needed |
| Error | `--color-error` | `#EF4444` | Agent failed, critical alerts |
| Info | `--color-info` | `#3B82F6` | Maps to primary blue — informational states |

### Dark Mode Surfaces (Home Base)

These are the primary surfaces for the Life Systems Hub and Agent Control Center. Inspired by Linear/Vercel's layered dark UI.

| Token | Hex | Usage |
|-------|-----|-------|
| `--surface-0` | `#09090B` | App background (near-black, not pure black) |
| `--surface-1` | `#18181B` | Cards, sidebar background |
| `--surface-2` | `#27272A` | Elevated cards, dropdowns, modals |
| `--surface-3` | `#3F3F46` | Borders, dividers, subtle separators |
| `--text-primary` | `#FAFAFA` | Primary text |
| `--text-secondary` | `#A1A1AA` | Secondary/muted text |
| `--text-tertiary` | `#71717A` | Placeholder text, disabled states |

### Light Mode Surfaces (Portfolio)

The portfolio's light mode uses an off-white canvas with subtle warmth — evoking construction paper, not sterile white. This supports the "origin story" narrative.

| Token | Hex | Usage |
|-------|-----|-------|
| `--surface-0-light` | `#FAFAF8` | Page background (warm off-white) |
| `--surface-1-light` | `#F5F5F0` | Card backgrounds |
| `--surface-2-light` | `#EBEBE4` | Elevated elements, hover states |
| `--surface-3-light` | `#D4D4CC` | Borders, dividers |
| `--text-primary-light` | `#18181B` | Primary text |
| `--text-secondary-light` | `#52525B` | Secondary text |
| `--text-tertiary-light` | `#A1A1AA` | Captions, metadata |

### Color Behavior Across Modes

The accent colors shift between modes to reinforce the narrative:

- **Light mode (Portfolio):** Blues and oranges are **deeper/muted** — slate-blue (`#1E40AF`), terracotta-orange (`#C2410C`). Sophisticated, earthy, analog.
- **Dark mode (All projects):** Blues and oranges are **brighter/saturated** — electric blue (`#3B82F6`), vivid amber-orange (`#F97316`). The creative technologist wakes up.

### Usage Ratio
- **Blue: ~80% of accent usage.** It's the infrastructure color — links, selections, primary actions, active states.
- **Orange: ~20% of accent usage.** It's the event color — something happened, look here, celebrate this. Used for CTAs, level-ups, agent alerts, notifications.

---

## 3. Typography

### Design Rationale
The portfolio gets a distinctive heading typeface (Sora) to create an editorial, "museum title card" quality — personality that still reads as modern and clean. The dashboards use Inter exclusively for pure engineering-grade clarity. This typographic split reinforces the light/dark narrative: Sora is the creative voice, Inter is the systems voice.

### Font Stack

| Role | Font | Source | Weight Range |
|------|------|--------|--------------|
| Portfolio Display/Headings | **Sora** | [Google Fonts](https://fonts.google.com/specimen/Sora) | 500 (Medium), 600 (SemiBold), 700 (Bold) |
| Portfolio Body | **Inter** | [Google Fonts](https://fonts.google.com/specimen/Inter) | 400 (Regular), 500 (Medium) |
| Dashboard Everything | **Inter** | [Google Fonts](https://fonts.google.com/specimen/Inter) | 400, 500, 600 |
| Monospace (all projects) | **JetBrains Mono** | [Google Fonts](https://fonts.google.com/specimen/JetBrains+Mono) | 400, 500 |

### Type Scale

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `--text-display` | 48px / 3rem | 1.1 | Portfolio hero headings only |
| `--text-h1` | 36px / 2.25rem | 1.2 | Page titles |
| `--text-h2` | 28px / 1.75rem | 1.3 | Section headings |
| `--text-h3` | 22px / 1.375rem | 1.4 | Subsection headings |
| `--text-h4` | 18px / 1.125rem | 1.4 | Card titles, labels |
| `--text-body` | 16px / 1rem | 1.6 | Body text |
| `--text-small` | 14px / 0.875rem | 1.5 | Metadata, captions, secondary info |
| `--text-caption` | 12px / 0.75rem | 1.4 | Labels, badges, timestamps |
| `--text-mono` | 14px / 0.875rem | 1.6 | Code, agent logs, data values |

### Font Weight Rules
- **Headings (Portfolio):** Sora Medium 500 for most headings. SemiBold 600 for hero/display only.
- **Headings (Dashboards):** Inter SemiBold 600.
- **Body:** Inter Regular 400. Use Medium 500 sparingly for inline emphasis instead of bold where possible.
- **Monospace:** JetBrains Mono Regular 400. Medium 500 for highlighted log entries.
- **Never use font weights below 400.** Light/thin weights break readability on dark backgrounds.

---

## 4. Spacing & Layout

### Base Unit
**4px base unit.** All spacing derives from multiples of 4px.

| Token | Value | Common Use |
|-------|-------|------------|
| `--space-1` | 4px | Tight internal padding (badge padding) |
| `--space-2` | 8px | Icon gaps, compact element spacing |
| `--space-3` | 12px | Default internal padding |
| `--space-4` | 16px | Standard element spacing |
| `--space-5` | 20px | Card internal padding |
| `--space-6` | 24px | Section padding, card gaps |
| `--space-8` | 32px | Major section gaps |
| `--space-10` | 40px | Large section dividers |
| `--space-12` | 48px | Page section spacing |
| `--space-16` | 64px | Hero spacing, major section breaks |

### Grid System

**Portfolio (public-facing):**
- Max content width: `1200px`
- Single column for case study scroll (720px max for text, full-width for media)
- Homepage project grid: responsive, 1-2 columns
- Horizontal padding: `24px` (mobile), `48px` (tablet), `64px` (desktop)

**Dashboards (private tools):**
- Sidebar width: `240px` (expanded), `64px` (collapsed/icon-only)
- Main content area: fluid, fills remaining space
- Card grid: CSS Grid, auto-fill, `minmax(320px, 1fr)`
- Max content width: none (dashboards use full viewport)

### Breakpoints

| Token | Value | Target |
|-------|-------|--------|
| `--bp-mobile` | 640px | Mobile devices |
| `--bp-tablet` | 768px | Tablets |
| `--bp-desktop` | 1024px | Desktop |
| `--bp-wide` | 1280px | Wide screens |

### Information Density
- **Portfolio:** Spacious. Generous whitespace. Content breathes. The museum analogy — space between exhibits.
- **Dashboards:** Comfortable-to-compact. More data density than the portfolio, but never cramped. Think Linear's issue list — readable rows with clear hierarchy.

---

## 5. Component Patterns

### Cards

```
Portfolio Cards (Light Mode):
- Background: var(--surface-1-light)
- Border: 1px solid var(--surface-3-light)
- Border Radius: 12px
- Shadow: 0 1px 3px rgba(0,0,0,0.04)
- Hover: subtle lift (translateY -2px) + shadow increase
- Padding: var(--space-6)

Dashboard Cards (Dark Mode):
- Background: var(--surface-1)
- Border: 1px solid var(--surface-3)
- Border Radius: 8px
- Shadow: none (borders define edges in dark mode)
- Hover: border color lightens to var(--text-tertiary)
- Padding: var(--space-5)
```

### Buttons

| Variant | Background | Text | Border | Usage |
|---------|-----------|------|--------|-------|
| Primary | `var(--color-primary)` | `#FFFFFF` | none | Main actions, submit, save |
| Accent | `var(--color-accent)` | `#FFFFFF` | none | CTAs on portfolio, celebration actions |
| Secondary | transparent | `var(--text-primary)` | 1px `var(--surface-3)` | Cancel, secondary actions |
| Ghost | transparent | `var(--text-secondary)` | none | Tertiary actions, icon buttons |

- Border radius: `6px` (all buttons)
- Padding: `8px 16px` (default), `6px 12px` (compact/dashboard)
- Transition: `150ms ease` on background and border color
- No pill-shaped buttons. Slightly rounded rectangles only.

### Input Fields
- Background: `var(--surface-0)` with 1px border `var(--surface-3)`
- Focus: border color transitions to `var(--color-primary)`
- Border radius: `6px`
- Height: `40px` (default), `36px` (compact/dashboard)
- Placeholder text: `var(--text-tertiary)`

### Navigation

**Portfolio — Minimal Top Bar:**
- Position: fixed top, hides on scroll down, reveals on scroll up
- Left: "Sean Winslow" in Sora Medium 500
- Right: Work | About | Contact — Inter Medium 500
- Background: `var(--surface-0-light)` with subtle backdrop-blur
- Height: `64px`
- Dark mode toggle: small icon in nav, transitions smoothly

**Dashboards — Sidebar Navigation:**
- Position: fixed left rail, always visible
- Width: `240px` expanded, `64px` collapsed (icon-only mode)
- Background: `var(--surface-1)`
- Border right: 1px `var(--surface-3)`
- Items: icon + label, active state uses `var(--color-primary)` text with subtle background highlight
- Style: Linear-inspired — clean, minimal, functional

### Data Display Preferences
- **Tables:** For structured data (agent run history, financial transactions). Clean rows, subtle row dividers, no alternating row colors.
- **Cards:** For entity display (agent profiles, project summaries, habit categories).
- **Lists:** For sequential/log data (activity feeds, agent logs). Monospace font for log content.

---

## 6. Motion & Interaction

### Design Rationale
Motion is purposeful — it tells stories and rewards engagement, never decorates. The portfolio uses cinematic scroll-triggered reveals. The dashboards use snappy micro-interactions. The Life Systems Hub adds celebration moments for gamification. All motion respects the `prefers-reduced-motion` media query as a hard requirement.

### Global Rules
- **Max transition duration:** 400ms. Nothing longer — it feels sluggish.
- **Micro-interactions (hover, focus):** 150-200ms.
- **Easing:** `ease-out` for entrances, `ease-in` for exits, `ease-in-out` for state changes.
- **GPU-only properties:** Only animate `transform` and `opacity`. Never animate `height`, `width`, or `margin`.
- **Accessibility kill switch (mandatory):**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Portfolio Motion
- **Scroll-triggered reveals:** Content sections fade in and translate up slightly as they enter the viewport. Staggered timing for multi-element sections.
- **Video-as-hero thumbnails:** Project cards show a static image by default. On hover, they autoplay a short loop of the project in action. This proves the work is real, not just mockups.
- **Cinematic scroll flow:** Lenis for smooth scrolling. GSAP ScrollTrigger for parallax and timeline-based scroll sequences. Content reads like a visual essay from top to bottom.
- **Metric count-up:** Key metrics (e.g., "+40% Efficiency") count up from 0 when entering the viewport. Max 2.0s duration, ease-out curve.
- **Page transitions:** Subtle crossfade between pages (200-300ms). Nothing flashy.

### Dashboard Motion
- **Snappy and immediate.** Interactions feel instant. No scroll animations.
- **Hover states:** Border/background color transitions at 150ms.
- **Panel/modal opens:** Scale from 0.98 to 1.0 + opacity 0 to 1. Duration: 200ms.
- **Tab/view switching:** Crossfade at 150ms. No sliding.
- **Data loading:** Skeleton placeholders that pulse subtly, never spinner-based.

### Life Systems Hub — Celebration Motion
- **XP bar fill:** Animated width transition with a slight glow effect on the fill edge. Duration: 600ms, ease-out.
- **Level up:** Brief color shift on the level badge + subtle scale pulse (1.0 → 1.05 → 1.0). Optional sound effect trigger.
- **Streak milestone:** The streak counter briefly glows with the accent orange. Satisfying but not disruptive.
- **Habit completion:** Checkbox fills with primary blue, subtle checkmark draw-in animation.

### Agent Control Center — Status Motion
- **Agent status change:** Card border/indicator color transitions smoothly (300ms) when status changes (running → complete → error).
- **No urgent alarms.** A failed agent shifts to amber/orange calmly. You notice it, you click in, you fix it. Nobody's life is in danger.
- **Log streaming:** New log entries slide in from the top with a subtle fade. Monospace text, contained scroll area.

---

## 7. Project-Specific Adaptations

### PM Portfolio (Public-Facing)

**Mode:** Light mode primary, dark mode toggle available.

**Narrative:** "A creative who learned to think like a product manager." Creativity leads, PM rigor supports. The first 5 seconds should feel *creative* — visual, intriguing, alive. The PM substance reveals itself as you scroll deeper into case studies.

**Structure:**
- **Homepage = Museum Lobby.** A curated gallery of 5-6 project cards. Each card is a "door" to a room/exhibit. Clean grid, generous spacing, project thumbnails that animate on hover (video loops).
- **Case Studies = Museum Rooms.** Each project is entered and experienced as a cinematic linear scroll. Hero visual at top → context/problem → process artifacts (sketches, wireframes, iterations) → creative deliverables (animations, illustrations, screenshots) → outcomes/metrics → learnings. Every case study blends multiple mediums (illustration, animation, photography, product thinking) into one narrative.
- **About Page:** Sean's story — the 12-year creative journey into PM. This is where the "pencils and paint on construction paper → code and AI" narrative lives.
- **Navigation:** Minimal top bar. "Sean Winslow" (Sora Medium) left, Work | About | Contact right. Hides on scroll down, reveals on scroll up.

**Content Organization:** By project/story, not by medium. Each project is its own room that may include pixel art, 2D illustration, animation, photography, motion graphics, and product thinking — all in service of one narrative.

**Typography:** Sora for headings (the museum's exhibition titles), Inter for body (the exhibition descriptions). This typographic pairing exists only on the portfolio.

**Color Treatment (Light Mode):** Off-white textured canvas (`#FAFAF8`). Muted/deeper blue (`#1E40AF`) and terracotta-orange (`#C2410C`) accents. The palette feels warm, tactile, analog.

**Color Treatment (Dark Mode):** When toggled, blues and oranges brighten and saturate. The same portfolio content now feels contemporary and electric. The creative technologist version of the same story.

**CTA Approach:** "View Project" buttons use accent orange on light mode, brighter orange on dark. Contact CTA is prominent but not aggressive — this is a museum, not a used car lot.

### Life Systems Hub (Private, Local-First)

**Mode:** Dark mode only. Always.

**Narrative:** "You are the main character." This is a personal RPG dashboard that gamifies life. Opening it should feel like loading your save file — energized, motivated, ready to play.

**Structure — Hub and Spoke:**
- **Hub = Character Screen.** The landing page is your profile: avatar/photo, current level and title (Recruit → Immortal), XP bar with animated fill, today's active quests (habits/tasks), streak status, and a motivational at-a-glance summary. This is what greets you at 5am with coffee.
- **Spokes (via sidebar navigation):**
  - **Finances:** Bank CSV imports, spending categories, trends over time. Data is sensitive and never leaves the browser (IndexedDB + Dexie.js). Hidden behind a click — not staring at you every morning.
  - **Fitness:** Apple Watch data integration, PPL workout split tracking, exercise history.
  - **Habits:** Daily/weekly habit tracker with XP rewards, streak tracking, completion animations.
  - **Vault:** Obsidian vault visualization and note connections.

**Gamification Visual Treatment:**
- Game elements have slightly more visual weight than standard UI. The XP bar, level badge, and streak counter are prominent — they're the *point*.
- Level-up celebrations include color shifts, subtle glow effects, animated XP bar fills, and optional sound effects (chime on habit completion, satisfying tone on level-up).
- RPG labels (Recruit, Immortal, etc.) appear in standard Inter — the gamification is in the *system*, not the typography. No pixel fonts.
- The game layer is warm and rewarding without being loud or flashy.

**Data Visualization Style:** Clean charts (Recharts or similar). Blue as the default data color, orange to highlight targets/milestones/anomalies. Dark chart backgrounds blending with the surface.

**Navigation:** Slim sidebar, always visible. Icons + labels. Active state: primary blue text with a subtle highlight background. Matches the Agent Control Center's navigation pattern exactly.

### Agent Control Center (Private, Local-First)

**Mode:** Dark mode only. Always.

**Soul:** Retro-futuristic mission control translated into a clean, modern dark-mode dashboard. The *feeling* of sitting at a 1960s command console (deliberate, calm, in control) expressed through Vercel-grade UI. Think Kubrick corridor meets Linear dashboard.

**Visual Cues (Subtle, Not Cosplay):**
- A faint grid pattern on the background (à la Vercel) — evokes control room grids without being literal.
- Status indicators that glow softly — blue for nominal, orange/amber for attention needed, red for failure. These echo the warm instrument lighting in the retro-future inspiration images.
- Agent cards that feel like station monitors — each card is a self-contained status readout.
- Monospace font (JetBrains Mono) for log displays and data readouts — echoing terminal screens without pretending to be one.

**Structure:**
- **Dashboard Home:** Overview of all agents and their current status. Agent cards in a grid, each showing: agent name, last run time, status indicator, cost since last check. Sidebar navigation matches the Life Systems Hub.
- **Agent Detail View:** Click into an agent to see run history (table format), log output (monospace scrolling area), configuration/skills, cost tracking. Linear scroll within the detail view.
- **Data Source:** CSV run logs and markdown files from Obsidian vault. All local, client-side parsing.

**Alert Treatment:**
- **Urgent but contained.** A failed agent's card shifts to amber/orange with a clear status badge. It stands out from the "all systems nominal" blue, but it doesn't feel like a fire alarm.
- **No hierarchical severity tiers.** Keep it simple: running (blue), completed (green), needs attention (orange), failed (red). You notice it, you click in, you see the logs, you fix it. Calm operator energy.
- **No one's life is in danger.** These are helpful Claude agents reading Slack messages and running tasks. The aesthetic is mission control; the reality is a personal automation dashboard.

---

## 8. Anti-Patterns

These are specific things to **never do** across any of the three projects, based on what Sean explicitly expressed disliking or what contradicts the design direction.

1. **No Cheesecake Factory menus.** Never overwhelm with equally-weighted options. If everything is prominent, nothing is. Curate ruthlessly.

2. **No shader/gradient hero backgrounds.** Sean's old portfolio had a moving shader hero. That's been explicitly rejected. Heroes should be clean with intentional content, not decorative effects.

3. **No pixel fonts or retro UI chrome.** The design system is modern. Retro/pixel art appears only as *content* (portfolio case studies, 16BitFit screenshots), never as UI decoration, buttons, icons, or typography.

4. **No fire-alarm alerts.** Agent failures are communicated calmly. No flashing red, no pulsing animations, no sound alarms on the Agent Control Center.

5. **No pure white backgrounds.** The portfolio uses warm off-white (`#FAFAF8`), never `#FFFFFF`. Pure white feels sterile and doesn't support the "construction paper" narrative.

6. **No pure black backgrounds.** Dashboard surfaces use near-black (`#09090B`), never `#000000`. Pure black creates excessive contrast and feels harsh.

7. **No choose-your-own-adventure case studies.** Case studies are cinematic linear scrolls — the visitor is guided through a narrative, not given a tabbed interface to explore out of order.

8. **No excessive bold text, bullet-point-heavy layouts, or overly formatted content.** Keep text natural and readable. The museum lets the art speak.

9. **No gratuitous animation.** Every animation must serve a purpose: guide attention, reward progress, or support the narrative. If you can't explain why something moves, it shouldn't.

10. **No competing accent colors.** Blue and orange at approximately 80/20 ratio. Never use them at equal weight or the visual identity breaks down.

---

## 9. Reference Board

A curated list of references that capture the target aesthetic, with notes on what specifically to draw from each.

### Structural & UI References

| Reference | What to Draw From | Link |
|-----------|------------------|------|
| **Linear** (app UI) | Dark mode surface hierarchy, sidebar navigation pattern, information density, card/list patterns. The gold standard for clean engineering-grade UI. | [linear.app](https://linear.app) |
| **Linear Style** | Actual design tokens and color system — searchable. Use as a technical reference for surface colors and spacing. | [linear.style](https://linear.style) |
| **Vercel** (dashboard + marketing) | Dark background grid patterns, deployment status cards, the "clean engineering" feel. Also reference for how to make dark marketing pages feel premium. | [vercel.com](https://vercel.com) |
| **Raycast** (marketing site) | Glowing accent colors on dark backgrounds. How to use reds/blues/greens purposefully against black. "Mission control" energy done cleanly. | [raycast.com](https://www.raycast.com) |

### Portfolio References

| Reference | What to Draw From | Link |
|-----------|------------------|------|
| **Brittany Chiang** | Dark portfolio, clean hierarchy, monospace accents, lets work speak. The "Linear-meets-portfolio" benchmark. | [brittanychiang.com](https://brittanychiang.com) |
| **Fine Thought (Nathan Leigh Davis)** | Minimal, experimental, subtle interactivity. Clean canvas for creative work. | [finethought.com.au](https://finethought.com.au) |
| **Keita Yamada** | Clean, concise, light/dark toggle. Demonstrates tasteful restraint. | [keitayamada.com](https://www.keitayamada.com) |

### Mood & Soul References

| Reference | What to Draw From | Link |
|-----------|------------------|------|
| **Sean's Image 3 (illustrated mission control)** | The overall composition — blue and orange on dark, multiple monitors, operators at stations. This IS the Agent Control Center in one picture. | (Sean's uploaded reference) |
| **1960s/70s retro-futuristic imagery** | The *soul* of the Agent Control Center. Warm amber instrument lighting, clean geometric architecture, analog-meets-future warmth. Kubrick's *2001* energy. | (Sean's uploaded references, images 5-7) |
| **Cyberpunk coding setups** | The *feeling* only — dense, glowing, alive — but not the chaos. Extract the atmosphere, discard the noise. | (Sean's uploaded references, images 1-2) |

### Typography References

| Reference | What to Draw From | Link |
|-----------|------------------|------|
| **Sora** | Portfolio heading font. Geometric precision with human warmth. "A creative who thinks systematically." | [Google Fonts — Sora](https://fonts.google.com/specimen/Sora) |
| **Inter** | Body text and dashboard everything. The engineering standard. | [Google Fonts — Inter](https://fonts.google.com/specimen/Inter) |
| **JetBrains Mono** | Monospace for code, logs, agent data. Highly readable developer font. | [Google Fonts — JetBrains Mono](https://fonts.google.com/specimen/JetBrains+Mono) |

---

## 10. Technical Stack Summary

Based on the interview decisions and the Creative-Native Architecture Specification Sean researched, here is the recommended stack per project:

### Portfolio

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | **Astro 6** | Ships zero JS by default — creative assets load instantly. "Islands Architecture" hydrates only interactive components. Ideal for a content-heavy cinematic portfolio. |
| Interactive Islands | **React** (within Astro) | Reuse React skills for interactive pieces (swipeable galleries, AI demos) while keeping static content fast. |
| Styling | **Tailwind CSS v4** | Shared across all projects. Tiny CSS payload (~12KB), leaves bandwidth for high-res creative assets. |
| Scroll/Animation | **GSAP** + **Lenis** | GSAP for scroll-triggered storytelling and timeline control. Lenis for smooth, accessible scrolling (~3KB). |
| Micro-interactions | **Motion One** | 65% smaller than Framer Motion. For button hovers, card interactions, UI transitions. |
| Hosting | **Netlify** (free tier) | Simple, fast CDN deployment. |

### Life Systems Hub & Agent Control Center

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | **React + Vite** | These are interactive apps with complex state management — they need a full SPA framework. Sean's existing skillset. |
| Styling | **Tailwind CSS v4** | Same config and design tokens as the portfolio. Unified visual language. |
| Local Data | **IndexedDB + Dexie.js** | Financial data never leaves the browser. Dexie provides a clean API over IndexedDB. |
| Data Parsing | **PapaParse** | CSV parsing for bank imports and agent run logs. |
| Charts | **Recharts** | React-native charting library. Clean, customizable, works with dark mode. |
| Micro-interactions | **Motion One** or **Framer Motion** | For dashboard transitions, XP bar animations, celebration effects. |
| Hosting | **Netlify** (free tier) | Same deployment pipeline as portfolio. |

### Shared Across All Projects

| Resource | Details |
|----------|---------|
| Design Tokens | CSS custom properties (variables) defined in a shared `tokens.css` file. Colors, typography, spacing, and breakpoints. |
| Tailwind Config | Shared `tailwind.config.js` extending default theme with custom colors, fonts, and spacing tokens. |
| Font Loading | Google Fonts — Sora (portfolio only), Inter (all), JetBrains Mono (all). Use `font-display: swap` and preload critical fonts. |
| Accessibility | `prefers-reduced-motion` kill switch. WCAG AA contrast ratios minimum. Semantic HTML. Keyboard navigation support. |

---

## 11. Implementation Priority

A suggested build order that prevents the rework loop:

**Phase 1 — Foundation (Week 1-2)**
Set up the shared design tokens (colors, typography, spacing) in a Tailwind config. Build a small component library: buttons, cards, inputs, sidebar nav. Test in both light and dark mode. This is the museum architecture before any art goes on the walls.

**Phase 2 — Agent Control Center (Week 3-4)**
Start here because it's the simplest in terms of content (CSV data, status cards, logs) and lets you validate the dark-mode dashboard patterns. Sidebar nav, agent status grid, detail view with log display.

**Phase 3 — Life Systems Hub (Week 5-7)**
Build on the same dashboard patterns from Phase 2. Add the character screen/hub, financial data import, gamification layer (XP, levels, streaks). Layer in celebration animations once the core data views work.

**Phase 4 — Portfolio (Week 8-12)**
This one takes longest because the content requires the most craft. Set up Astro, build the homepage gallery, then focus on one case study at a time. Cinematic scroll, video thumbnails, motion reveals. Ship the clean version first, then layer in parallax and advanced scroll physics.

**Phase 5 — Polish (Ongoing)**
Magnetic buttons, scroll-velocity parallax, sound effects, advanced transitions. These are "nice to have" — never prioritize them over shipping core pages with real content.

---

*This specification represents committed decisions. Every choice was made deliberately through an interview process designed to surface Sean's authentic design taste and prevent the rework loop. When in doubt, return to the core philosophy: "Engineered precision that rewards you with moments of warmth."*
