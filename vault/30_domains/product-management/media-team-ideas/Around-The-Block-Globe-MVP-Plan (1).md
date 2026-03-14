# Around The Block — Interactive Globe MVP
## Execution Plan & Perplexity Computer Build Strategy

**Date:** March 13, 2026
**Team:** Davis (Media Lead), Jordan (Production), Sean (Product/Build)
**Status:** Pre-build planning — "Build in stealth" mode

---

## 1. What We're Building

A single-page interactive 3D globe web app that visualizes global crypto adoption country-by-country. Users spin the globe, click a country, and see a panel showing its crypto adoption stage (0–6), key regulatory details, and recent news. Styled with The Block's design system.

This is the visual centerpiece that Davis described in the March 9 meeting — the thing you show Larry and say "here's what Around The Block becomes as a product, not just a podcast."

### What the MVP includes:
- 3D globe with country boundaries (Three.js / Globe.gl)
- Countries color-coded by adoption stage (7-stage framework from Davis's strategy doc)
- Click-to-zoom on a country → info panel slides in
- Info panel shows: country name, flag, current stage, stage description, last stage change, and 2-3 key facts
- Seeded database of 50+ countries with real adoption data
- The Block's dark mode design (brand colors, typography)
- Deployed as a live URL you can share

### What the MVP does NOT include (Phase 2+):
- Ambassador program or user-generated content
- News API integration or live data feeds
- Stage-change notification system
- Content management / tagging system
- Digital collectibles or community features
- Around The Block video/podcast integration

---

## 2. The Three Layers (How Everything Connects)

Davis's full vision has three layers. The MVP builds layers 1 and 2. Layer 3 is operational and comes after the product is validated.

### Layer 1: The Visual Shell (3D Globe)
The "wow factor" — the interactive globe that makes people want to click and explore. This is what gets shared on Twitter, shown in meetings, and makes the concept tangible. Jordan's original vibe-coded globe prototype is the starting point. The Polyglobe reference (pizzint.watch/polyglobe) and the 3D city visualization are design inspiration.

### Layer 2: The Data Backbone (Adoption Tracker)
The 7-stage classification framework that gives the globe meaning. Each country gets a stage (0–6), a color, and structured metadata. This is what turns a pretty globe into an actual product. Davis's "Global Crypto Adoption Tracker — Strategy & Agent Blueprint" document defines the full framework, stage definitions, and initial country seedings.

### Layer 3: The Human Network (Ambassador Program)
The 30-50 person global correspondent network that feeds local content into the tracker. This is what makes the product impossible for competitors to replicate. Davis's "Around The Block — Ambassador Program Plan" defines the full structure, tiers, compensation, and sponsorship model. **This layer comes AFTER the MVP proves the concept.**

### How they connect over time:
```
Phase 1 (NOW): Globe + Tracker data → Scrappy MVP to demo internally
Phase 2: + News scanning agent → Auto-populating content via APIs
Phase 3: + Ambassador network → Human-verified, locally-sourced content
Phase 4: + Community features → Digital collectibles, user submissions
Phase 5: + Block integration → Media hub, app integration, podcast tie-in
```

---

## 3. Technical Architecture

### Why These Technology Choices

**Globe.gl (built on Three.js)** — This is an open-source library specifically designed for 3D globe visualizations on the web. It handles the hard parts (WebGL rendering, country geometry, camera controls, zoom animations) out of the box, so we don't have to build a 3D engine from scratch. Jordan's original prototype and the Polyglobe reference both use similar underlying tech. It works in any modern browser with no plugins.

**React** — The UI framework for the info panels and controls around the globe. React is the standard for interactive web apps, it's what Perplexity Computer generates most fluently, and it means any future developer at The Block can pick up the code.

**JSON data file** — For the MVP, the country database is just a JSON file bundled with the app. No backend, no database server, no API to maintain. Simple to edit, simple to deploy. When the project scales, this gets replaced with Supabase or Airtable (as Davis's strategy doc recommends).

**Vite** — The build tool that bundles everything into a deployable app. Fast, modern, zero-config. Perplexity Computer handles this automatically.

### Component Structure
```
/src
  App.jsx              — Main layout (globe + side panel)
  Globe.jsx            — 3D globe component (Globe.gl wrapper)
  CountryPanel.jsx     — Slide-in info panel when country is clicked
  StageIndicator.jsx   — Visual badge showing Stage 0-6
  StageBar.jsx         — Color-coded progress bar for adoption stages
  data/
    countries.json     — The country database (50+ entries)
    stages.json        — Stage definitions and descriptions
  styles/
    theme.js           — Block design tokens (colors, fonts)
```

### The Block Design System Application

From TheBlock-Design-System.md, here's how we map the design tokens:

| Element | Design Token | Value |
|---------|-------------|-------|
| Background | Dark mode base | `#0A0A0A` (near-black) |
| Globe ocean | Dark neutral | `#1A1A1A` |
| Primary accent | Brand blue | `#0066FF` |
| Negative/hostile stages | Brand coral-red | `#FF4D5A` |
| Positive/advanced stages | Green scale | Green mid-tones |
| Highlight/new changes | Brand lime | `#D4FF00` |
| Text (primary) | Soft white | `#E0E0E0` |
| Text (secondary) | Mid gray | `#808080` |
| Font | Sans-serif system | Match Block's geometric sans |
| Data text | Tabular/mono | For stage numbers and stats |

### Stage-to-Color Mapping
This maps directly from Davis's strategy doc color system:

| Stage | Name | Globe Color | Hex |
|-------|------|-------------|-----|
| 0 | Dark Zone | Dark gray | `#333333` |
| 1 | Restricted/Hostile | Red | `#FF4D5A` |
| 2 | Under Watch | Amber/Orange | `#FF8C00` |
| 3 | Regulatory Drafting | Yellow | `#FFD700` |
| 4 | Licensed & Regulated | Green | `#00CC66` |
| 5 | Institutionally Integrated | Bright green | `#00FF88` |
| 6 | National Strategy | Gold | `#D4FF00` (Block lime) |
| No data | Untracked | Very dark gray | `#1A1A1A` |

---

## 4. Country Database (Initial Seed)

From Davis's strategy doc, here's the starting classification. Perplexity Computer will research and verify/expand this during the build using its live web search.

### Stage 6 — National Strategy
El Salvador

### Stage 5 — Institutionally Integrated
United States (spot BTC/ETH ETFs approved and trading)

### Stage 4 — Licensed & Regulated
EU member states (all 27 via MiCA), UK, Brazil, Japan, Singapore, UAE, South Korea, Australia, Hong Kong, Canada

### Stage 3 — Regulatory Drafting
India, Saudi Arabia, Qatar, South Africa, Thailand, Philippines, Mexico, Colombia, Argentina, Turkey, Indonesia, Vietnam, Malaysia, Nigeria

### Stage 2 — Under Watch
Kenya, Ghana, Tanzania, Morocco, Pakistan, Sri Lanka, Kazakhstan, Uzbekistan, Rwanda, many smaller nations with CBDC research but no crypto framework

### Stage 1 — Restricted/Hostile
Algeria, China (trading/mining ban maintained), Egypt, Bangladesh (historically)

### Stage 0 — Dark Zone
Various small nations with no formal engagement — Perplexity Computer will research and fill these during build

**Target: 50-80 countries seeded for MVP.**

**Important note for Perplexity Computer:** These seed classifications come from Davis's strategy document. When Computer's live research finds more current data (March 2026), **prefer the most recent credible source** (official government announcements, FATF reports, central bank statements). If research contradicts the seed data, update the classification and note what changed in the country's "last_event" field.

---

## 5. Perplexity Computer Build Strategy

### Why Perplexity Computer

Based on your Perplexity-Computer-Overview.md research:

1. **Multi-model orchestration** — Opus handles the React/Globe.gl architecture, Gemini can research live country adoption data, Nano Banana can generate any stage-change graphics or icons
2. **Live deployment** — Computer can deploy the app to a live URL directly from the sandbox, no hosting setup needed
3. **Research + build in one session** — Computer can research current adoption data for 50+ countries AND build the app in the same workflow
4. **Brand memory** — Upload TheBlock-Design-System.md as a reference file so Computer maintains design consistency throughout

### Prompt Strategy: The Master Prompt

This is the prompt you'll paste into Perplexity Computer to kick off the build. It's structured to give Computer everything it needs to work autonomously.

---

#### PRE-FLIGHT: Before pasting the prompt below, upload TheBlock-Design-System.md as a reference file in Perplexity Computer so it stays in persistent memory throughout the build.

#### MASTER PROMPT (copy this into Perplexity Computer):

```
PROJECT: "Around The Block" — Interactive 3D Globe for Global Crypto Adoption Tracking

CONTEXT:
I'm building an interactive 3D globe web app for The Block (theblock.co), a crypto news and research platform. The globe visualizes which countries are crypto-friendly vs hostile, using a 7-stage adoption framework. Users spin the globe, click a country, and see an info panel with adoption data.

This is a scrappy MVP / internal demo — functional and good-looking, not production-grade.

DESIGN SYSTEM (apply these throughout):
- Dark mode: background #0A0A0A, cards #1A1A1A
- Primary blue: #0066FF (links, interactive elements)
- Coral-red: #FF4D5A (negative indicators, hostile stages)
- Lime accent: #D4FF00 (highlights, top-stage countries)
- Text: soft white #E0E0E0, secondary #808080
- Font: clean geometric sans-serif (Inter or similar)
- Data/numbers: tabular/monospace figures
- Style: professional, data-first, high information density — NOT casual or playful

TECH STACK:
- React + Vite
- Globe.gl (https://globe.gl) for the 3D globe — this library handles Three.js under the hood
- Single JSON file for the country database (no backend needed for MVP)
- Deploy to a shareable live URL

THE 7-STAGE ADOPTION FRAMEWORK:
Each country is classified into one of these stages:

Stage 0 — Dark Zone: No legal framework, crypto in gray area. Color: #333333
Stage 1 — Restricted/Hostile: Active bans or criminalization. Color: #FF4D5A
Stage 2 — Under Watch: Government studying crypto, no position yet. Color: #FF8C00
Stage 3 — Regulatory Drafting: Active legislation underway. Color: #FFD700
Stage 4 — Licensed & Regulated: Comprehensive framework live. Color: #00CC66
Stage 5 — Institutionally Integrated: Crypto woven into mainstream finance (ETFs, bank custody). Color: #00FF88
Stage 6 — National Strategy: Legal tender, national reserves, state policy. Color: #D4FF00

STAGE CHANGE TRIGGERS (what justifies a classification):
- New comprehensive legislation passed → moves UP (e.g., US GENIUS Act)
- Exchange licenses granted at scale → moves UP (e.g., MiCA authorizing CASPs)
- CBDC pilot launched → moves UP
- Spot ETF approved → moves UP (e.g., US approving BTC/ETH ETFs)
- Crypto declared legal tender → moves UP (e.g., El Salvador)
- Trading/mining ban enacted → moves DOWN (e.g., Algeria criminalizing all crypto)
- Major exchange shut down by regulators → moves DOWN
- Reversal of existing crypto-friendly policy → moves DOWN

When classifying a country, cite the specific trigger event that justifies its stage.

CONFLICT RESOLUTION: If sources disagree on a country's status, prefer official government sources and FATF reports over news articles. Use the most recent credible source (March 2026 data preferred).

BUILD STEPS:

1. RESEARCH PHASE: Using your web search capabilities, research and classify 50-80 countries into the 7 stages above based on their CURRENT (March 2026) crypto regulatory status. For each country, capture:
   - Country name and ISO code
   - Current stage (0-6)
   - One-line reason for classification
   - Key regulator(s)
   - CBDC status (if any)
   - Last major regulatory event and date
   Store this as a countries.json file.

2. BUILD THE GLOBE:
   - Use Globe.gl to render a 3D globe with dark styling
   - Color each country polygon by its adoption stage using the color map above
   - Countries with no data should be very dark (#1A1A1A), almost blending with the ocean
   - Globe should auto-rotate slowly, stop on user interaction
   - Hovering a country shows its name and stage as a tooltip
   - Clicking a country zooms the camera to center on it and opens the info panel

3. BUILD THE INFO PANEL:
   - Slides in from the right side when a country is clicked
   - Shows: Country name (large), flag emoji, Stage badge (colored, with stage number and name)
   - Below that: stage description, key facts (regulator, CBDC status, last event)
   - A "Stage History" section if the country has moved stages
   - Close button returns to the full globe view
   - Styled with the dark mode design system above

4. BUILD THE LEGEND/CONTROLS:
   - Bottom-left: stage legend showing all 7 stages with their colors
   - Top-left: "Around The Block" title + "Global Crypto Adoption Tracker" subtitle
   - Top-right: stats summary (e.g., "78 countries tracked • 12 at Stage 4+")
   - Optional: filter buttons to highlight countries at a specific stage

5. DEPLOY: Deploy to a live, shareable URL (Vercel, Netlify, or whatever you have access to — any static hosting works since this is a client-side React app with no backend).

REFERENCE LINKS (for design inspiration):
- 3D Globe reference: https://www.pizzint.watch/polyglobe
- The app should feel like a Bloomberg terminal meets a National Geographic interactive — data-dense but visually compelling

OUTPUT:
A deployed, interactive web app at a live URL. Also provide the full source code.
```

---

### Tips for Using This in Perplexity Computer

1. **Upload TheBlock-Design-System.md first** as a reference file before pasting the prompt. This lets Computer's persistent memory maintain brand consistency.

2. **Start with the research phase.** If Computer tries to skip the country research and use placeholder data, redirect it: "Before building, please research and classify at least 50 countries based on their current March 2026 crypto regulatory status."

3. **Pin models if needed.** If you notice the research quality is weak, pin Gemini to the research sub-tasks (it's strongest at deep research with current data). Pin Opus to the code generation.

4. **Iterate in the same session.** After the first build, you can say things like:
   - "The globe is too bright — darken the ocean and make untracked countries almost invisible"
   - "Add a subtle glow effect to Stage 6 countries"
   - "The info panel needs more padding and the stage badge should be bigger"
   - "Add South Korea, I see it's missing from the data"

5. **Credit budget estimate:** Based on the Perplexity Computer overview, this build involves heavy research (Gemini) + code generation (Opus) + possible image generation (Nano Banana for graphics). Estimate 200-400 credits for the full build with iterations. Well within the 10,000 monthly allowance.

---

## 6. After the MVP: What Comes Next

### Immediate next steps (after MVP is live):
1. **Show Davis and Jordan** — Get their feedback on the globe, colors, data accuracy
2. **Record a screen capture** — 30-second video of spinning the globe and clicking countries for Twitter/Slack
3. **Show Josh** — He's been championing the media hub; this could BE the hub centerpiece
4. **Seed the internal conversation** — Share in #general or with Larry directly

### Phase 2 features (next build session):
- Connect to news APIs (CryptoPanic, NewsAPI) so country panels show live news
- Add stage-change animation (countries visually "level up" or "level down")
- The stage-change graphic template system from Davis's content strategy
- Mobile responsive version
- "Race" view — regional leaderboards (APAC, LATAM, etc.)

### Phase 3 features (requires organizational buy-in):
- Ambassador submission portal
- Content management system for tagging stories to countries
- Integration with The Block's website / media hub
- The automated news-scanning agent (Davis's 5-stage pipeline)
- Sponsorship integration

---

## 7. Key Decisions Needed from Davis

Before or during the build, flag these with Davis:

1. **Border sensitivity** — Jordan mentioned he had to manually fix controversial borders (Crimea, etc.) on his globe prototype. We need to decide: use UN-recognized borders, or let Globe.gl defaults stand and fix case-by-case?

2. **Stage classification disputes** — Some countries are judgment calls (e.g., China is Stage 1 for trading but exploring seized-asset reserves). Does the MVP need "split stage" handling, or just pick the dominant classification?

3. **Branding** — Is this "Around The Block" branded, "The Block" branded, or neutral for now? Affects the header/logo treatment.

4. **The Wazee** — Davis mentioned wanting to eventually integrate his Wazee animated character. Not for MVP, but worth knowing if we should leave space for a mascot element.

---

## 8. Reference Files Summary

| File | What It Contains | How We Use It |
|------|-----------------|---------------|
| global-crypto-adoption-tracker-strategy.md | 7-stage framework, content strategy, agent architecture, database schema | The data model and classification system for the entire globe |
| around-the-block-ambassador-program.md | 3-tier ambassador network, sponsorship model, content workflow | Phase 3 planning — NOT needed for MVP but informs the product vision |
| TheBlock-Design-System.md | Colors, typography, layout patterns, data viz palettes | Upload to Perplexity Computer for brand consistency |
| Perplexity-Computer-Overview.md | Platform capabilities, model roster, credit system, limitations | Guides our build strategy and prompt engineering |
| Media Team References.md | Polyglobe link, 3D city viz, anime news account | Design inspiration for the globe interaction model |
| Jordan Davis and Sean-transcript.md | Full meeting transcript | Context for decisions, priorities, and the broader "Block Labs" vision |

---

*Built by Sean in collaboration with the media team. This is a "Block Labs" stealth project.*
