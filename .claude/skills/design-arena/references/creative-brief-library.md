# Creative Brief Library

> Reusable agent personas organized by project type. Select 3-4 briefs per arena session. Mix and match across categories — a dashboard project might benefit from one dashboard-specific brief and one borrowed from the editorial category for fresh perspective.
>
> **DNA Pairing:** Each layout brief is now paired with an Aesthetic DNA profile (see `references/aesthetic-dna-library.md`) to create the full agent identity. The layout brief determines WHERE things go. The DNA profile determines HOW they look, move, and feel. See the pairing guidance table in the DNA library for recommended and unexpected combinations.

---

## Dashboard / Data App Briefs

### Dense Operator
**Philosophy:** Maximum information per pixel. The user is a power user who wants everything visible without scrolling.
**Layout direction:** Compact rows, multi-column grids, inline data, minimal card chrome. Think Linear's issue list or Bloomberg Terminal (but beautiful).
**Density:** High. 12-16px row heights, tight padding, data tables over cards.
**Best for:** Agent dashboards, financial trackers, admin panels.

### Breathing Room
**Philosophy:** Each metric earns its own space. Visual hierarchy through scale, not density.
**Layout direction:** Card-per-metric, generous whitespace, clear visual grouping. Think Apple Health dashboard or Stripe dashboard.
**Density:** Low-medium. Generous padding, one clear focal point per card.
**Best for:** Personal dashboards, health trackers, habit apps.

### Split Cockpit
**Philosophy:** Persistent context on one side, detail on the other. No page transitions needed.
**Layout direction:** Fixed left panel (navigation or list), scrollable right panel (detail view). Master-detail pattern. Think Slack, Linear, or email clients.
**Density:** Medium. List side is compact, detail side has room to breathe.
**Best for:** Apps with list → detail workflows (agent runs, transactions, notes).

### Narrative Flow
**Philosophy:** The page tells a story from top to bottom. Summary → breakdown → detail.
**Layout direction:** Single-column vertical scroll. Hero summary at top, category sections below, granular data at the bottom. Almost editorial in feel.
**Density:** Progressive — starts spacious (summary), gets denser (detail tables).
**Best for:** Financial overviews, weekly reviews, progress reports.

### Command Center
**Philosophy:** Everything is a status readout. The page is a grid of live monitoring panels.
**Layout direction:** CSS Grid of equal-weight status cards. Each card is self-contained with its own mini-chart or indicator. No single focal point — the layout is the overview.
**Density:** Medium-high. Cards are compact but internally well-spaced.
**Best for:** Agent monitoring, system status, operations dashboards.

---

## Portfolio / Marketing Site Briefs

### Museum Gallery
**Philosophy:** The work is the art. The UI is the white walls. Maximum restraint, maximum content impact.
**Layout direction:** Clean grid of project cards, generous margins, content floats in space. Navigation nearly invisible. Think a physical gallery where you focus on the pieces, not the building.
**Density:** Very low. Spacious to the point of feeling luxurious.
**Best for:** Creative portfolios, photography sites, case study collections.

### Editorial Scroll
**Philosophy:** The page is a magazine feature. The visitor is guided through a narrative.
**Layout direction:** Single-column cinematic scroll. Full-width media, pull quotes, section transitions. Scroll-triggered reveals. Think a New York Times interactive feature or Apple product page.
**Density:** Low-medium. Text blocks are narrow (600-720px), media is full-width.
**Best for:** Case studies, product launches, long-form storytelling.

### Asymmetric Split
**Philosophy:** Break the grid. Create visual tension through unequal composition.
**Layout direction:** Two unequal columns (60/40 or 70/30). One side anchors (text/nav), the other side flows (images/media). Diagonal eye movement. Unexpected but controlled.
**Density:** Medium. The asymmetry creates natural breathing room.
**Best for:** Agency sites, creative portfolios, landing pages that need personality.

### Micro-Site
**Philosophy:** One page, no navigation, everything above the fold matters.
**Layout direction:** Vertical sections that each fill the viewport. Snap-scrolling or smooth section transitions. Each section is a self-contained message. Think product landing pages.
**Density:** Low per section, but many sections.
**Best for:** Launch pages, product pages, event pages.

---

## Mobile App / React Native Briefs

### Tab-First
**Philosophy:** Bottom tab bar drives navigation. Each tab is a distinct view.
**Layout direction:** Bottom navigation with 3-5 tabs. Content fills the screen above the tab bar. Pull-to-refresh patterns. Cards stack vertically.
**Density:** Medium. Touch-friendly spacing (44px minimum targets).
**Best for:** Standard mobile apps, fitness trackers, habit apps.

### Card Stack
**Philosophy:** Content is a stack of cards you scroll through vertically.
**Layout direction:** Full-width cards with generous internal padding. Swipe actions on cards (archive, complete, delete). Bottom sheet for details instead of page transitions.
**Density:** Medium. One card per concept, vertical scrolling.
**Best for:** Feed-style apps, task lists, notification-heavy apps.

### Immersive
**Philosophy:** Minimal chrome. Content fills the entire screen. Navigation is gestural.
**Layout direction:** Edge-to-edge media/content. Floating action buttons. Gesture-based navigation (swipe back, pull down to dismiss). Status bar and nav bar blend into content.
**Density:** Low chrome, high content.
**Best for:** Media apps, game UI, photo/video-centric apps.

---

## Game UI Briefs

### HUD Overlay
**Philosophy:** Game UI sits on top of the game world. Minimal, transparent, always available but never blocking.
**Layout direction:** Corner-anchored elements (health top-left, inventory top-right, actions bottom-center). Semi-transparent backgrounds. Information appears on hover/tap and fades when not needed.
**Density:** Minimal — only essential info visible at all times.
**Best for:** HUD overlays, in-game status, real-time displays.

### RPG Menu
**Philosophy:** The menu IS the experience. Character sheets, inventory grids, skill trees.
**Layout direction:** Tabbed sections (Character, Inventory, Skills, Settings). Grid layouts for inventory. Stat displays with progress bars. Panel-based with clear borders.
**Density:** High within each panel, but panels are clearly separated.
**Best for:** Character screens, inventory systems, stat displays.

### Retro Console
**Philosophy:** Constrained display area, like a handheld console screen.
**Layout direction:** Fixed-size viewport, pixel-grid alignment, limited color palette. UI elements are chunky and clearly defined. Think Game Boy or GBA menu screens — but rendered in modern CSS/HTML with the constraint as a design choice, not a limitation.
**Density:** Medium. Constrained viewport forces efficient layouts.
**Best for:** Retro-themed apps, gamified interfaces, 16BitFit-style projects.

---

## Component / Section-Level Briefs

Use these when the arena is scoped to a single component or section rather than a full page.

### Hero Variants
Each agent creates a different hero section approach:
- Agent A: Typography-forward (headline dominates, minimal media)
- Agent B: Media-forward (full-bleed image/video, text overlay)
- Agent C: Interactive (animated element, scroll-triggered reveal)
- Agent D: Data-driven (live metric or counter as the focal point)

### Navigation Variants
Each agent creates a different navigation approach:
- Agent A: Minimal top bar (logo left, links right, hides on scroll)
- Agent B: Full sidebar (always visible, collapsible to icons)
- Agent C: Bottom tab bar (mobile-first, floating)
- Agent D: Command palette only (no visible nav — keyboard shortcut opens search)

### Card Variants
Each agent creates a different card treatment for the same data:
- Agent A: Compact list row (icon + title + metadata inline)
- Agent B: Full card with preview (image/chart thumbnail + metadata below)
- Agent C: Expandable accordion (summary visible, detail on click)
- Agent D: Status-first (large status indicator, metadata secondary)

---

## How to Customize Briefs

If none of the library briefs fit, create a custom one using this template:

```markdown
### [Brief Name]
**Philosophy:** [One sentence — the core belief about how this layout serves the user]
**Layout direction:** [Specific structural approach — columns, panels, scroll behavior]
**Density:** [Low / Medium / High + what that means for this project]
**Best for:** [Project types this works well for]
```

The philosophy statement is the most important line — it prevents the agent from drifting during implementation. An agent told "maximize information per pixel" makes different decisions than one told "each metric earns its own space," even when building from the same design tokens.
