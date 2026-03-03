# Campus Design System

**Product:** Campus — A cryptocurrency education platform by The Block
**Version:** 1.0
**Last Updated:** February 2026

---

## 1. Overview

Campus is a cryptocurrency learning platform developed by The Block. It provides structured coursework (101 and 201 levels), assessments (Digital Assets Essentials — D.A.E.), team management dashboards, and candidate tracking. This design system documents every visual standard — colors, typography, iconography, logo usage, layout patterns, and UI components — so that any designer, developer, or content creator can produce work that feels consistent with the Campus brand.

---

## 2. Brand Identity

### 2.1 Brand Positioning

Campus sits at the intersection of professional education and crypto-native culture. The visual language should feel modern, authoritative, and approachable — never intimidating.

### 2.2 Logo

The Campus logo system includes multiple variants organized by three axes: **layout**, **color theme**, and **shape**.

#### Layouts

| Layout | Description |
|---|---|
| **Stacked** | "Campus" above "Developed by The Block" — primary lockup for headers |
| **Horizontal** | "Campus" to the left, "Developed by The Block" to the right — used when vertical space is limited |
| **Wordmark Only** | The word "Campus" alone — for in-app navigation bars |
| **Icon Only (Hexagon)** | The hexagonal badge with the "C" cube mark — favicons, app icons, avatars |
| **Icon Only (C Mark)** | The standalone "C" letterform with cube — compact contexts |

#### Color Themes

| Theme | When to Use |
|---|---|
| **White** | On dark backgrounds (Dark Teal, Black) |
| **Black** | On light backgrounds (White, Light Gray) |
| **Highlighter (Lime)** | For accent or brand-forward moments on dark backgrounds |

#### Clear Space & Minimum Size

- Maintain clear space equal to the height of the "C" in "Campus" on all sides.
- Minimum size for the full lockup: 120 px wide on screen.
- Minimum size for the icon mark: 24 px.

#### Prohibited Uses

- Do not rotate, stretch, or recolor the logo outside the three approved themes.
- Do not place the logo on busy photographic backgrounds without a solid overlay.
- Do not use the hexagonal icon at sizes below 24 px.

---

## 3. Color Palette

The palette is organized into five functional groups. Every color includes a 10-step ramp (50–900) for flexibility in tints and shades.

### 3.1 White & Black

**Usages:** Backgrounds, text.

| Token | Hex |
|---|---|
| White | `#FFFFFF` |
| Black | `#000000` |

### 3.2 Concrete (Neutral Grays)

**Usages:** Borders, backgrounds, secondary text, dividers.

| Step | Hex | Typical Use |
|---|---|---|
| 50 | `#F2F2F2` | Page backgrounds, light cards |
| 100 | `#EAEBEB` | Subtle borders, disabled states |
| 200 | `#D9DCDD` | Divider lines |
| 300 | `#C1C5C7` | Placeholder text |
| 400 | `#9DA4A6` | Secondary icons |
| 500 | `#73787A` | Body text on light backgrounds |
| 600 | `#55595A` | Strong secondary text |
| 700 | `#3A3C3D` | Emphasis text |
| 800 | `#1D1E1E` | Near-black text |
| 900 | `#101111` | Deepest dark — use sparingly |

### 3.3 Highlighter (Brand Lime/Yellow-Green)

**Usages:** Brand color, primary buttons, accent color, CTAs, active navigation tabs.

| Step | Hex | Typical Use |
|---|---|---|
| 50 | `#FDFFE7` | Lightest tint |
| 100 | `#F8FFC4` | Hover backgrounds |
| 200 | `#F1FF9C` | Light accent fills |
| 300 | `#E6FF64` | **Primary brand accent** — buttons, active tabs, highlights |
| 400 | `#C6DB58` | Pressed/active state of primary buttons |
| 500 | `#A7B94C` | Secondary accent on dark backgrounds |
| 600 | `#8B9266` | Muted accent |
| 700 | `#51582A` | Dark accent for text on light backgrounds |
| 800 | `#373B1F` | Very dark accent |
| 900 | `#272917` | Deepest accent — use sparingly |

### 3.4 Mint (Teal/Cyan)

**Usages:** Accent color, backgrounds, success states, data visualizations, progress indicators.

| Step | Hex | Typical Use |
|---|---|---|
| 50 | `#ECFBFE` | Lightest tint |
| 100 | `#D7F6FB` | Light card backgrounds |
| 200 | `#BCF1FA` | Subtle accent fills |
| 300 | `#95E7F3` | Light diagram elements |
| 400 | `#65D0E0` | Medium accent — chart bars, progress rings |
| 500 | `#00A8C2` | **Primary teal accent** — links, interactive elements |
| 600 | `#006372` | Dark accent |
| 700 | `#002B33` | **Primary dark background** — app shell, headers, lesson chrome |
| 800 | `#081C20` | Deeper dark background |
| 900 | `#0A1719` | Deepest dark |

### 3.5 Red

**Usages:** Error states, failed tests, warning indicators.

| Step | Hex | Typical Use |
|---|---|---|
| 50 | `#FECFCF` | Error tint backgrounds |
| 100 | `#FDF4F4` | Light warning backgrounds |
| 200 | `#FAE6E6` | Subtle error fills |
| 300 | `#F0BABA` | Error borders |
| 400 | `#E17979` | Error icons |
| 500 | `#D84F4F` | **Primary error red** — error text, failed-state icons |
| 600 | `#9E3D3C` | Dark error accents |
| 700 | `#682C29` | Very dark error text |
| 800 | `#532522` | Deep error |
| 900 | `#2C1715` | Deepest error |

### 3.6 Semantic Color Assignments

| Role | Color Token | Hex |
|---|---|---|
| Primary Background (Dark) | Mint 700 | `#002B33` |
| Primary Background (Light) | White | `#FFFFFF` |
| Surface / Card | Concrete 50 | `#F2F2F2` |
| Primary Brand Accent | Highlighter 300 | `#E6FF64` |
| Primary Interactive (Links) | Mint 500 | `#00A8C2` |
| Success / Correct | Mint 500 | `#00A8C2` |
| Error / Incorrect | Red 500 | `#D84F4F` |
| Primary Text (on dark) | White | `#FFFFFF` |
| Primary Text (on light) | Black | `#000000` |
| Secondary Text | Concrete 500 | `#73787A` |

---

## 4. Typography

Campus uses the **Geller** typeface family. Three width variants are used: **Standard (Geller)**, **Condensed**, and **Wide**.

### 4.1 Type Scale

#### Display (Hero / Marketing)

| Token | Size | Weight | Width | Line Height |
|---|---|---|---|---|
| D1 | 120 px | Medium | Condensed | — |
| D2 | 80 px | SemiBold | Condensed | 110% |
| D3 | 64 px | Bold | Wide | — |

#### Headings

| Token | Size | Weight | Width | Line Height |
|---|---|---|---|---|
| H1 | 40 px | SemiBold | Geller (standard) | 140% |
| H2 | 40 px | SemiBold | Condensed | 140% |
| H3 | 32 px | SemiBold | Geller (standard) | 140% |
| H4 | 32 px | SemiBold | Condensed | 140% |
| H5 | 20 px | SemiBold | Geller (standard) | 140% |

#### Paragraphs (Body)

| Token | Size | Weight | Width | Line Height |
|---|---|---|---|---|
| P1 | 22 px | SemiCondensed | — | 150% |
| P2 | 16 px | SemiCondensed | — | 150% |

#### Captions

| Token | Size | Weight | Width | Line Height | Transform |
|---|---|---|---|---|---|
| C1 | 24 px | Bold | Condensed | 140% | — |
| C2 | 20 px | Bold | Condensed | 140% | UPPERCASE |
| C3 | 20 px | Bold | Condensed | 140% | — |
| C4 | 20 px | Medium | Condensed | — | — |
| C5 | 16 px | Bold | Condensed | 140% | UPPERCASE |
| C6 | 16 px | Medium | Condensed | 140% | — |
| C7 | 14 px | Bold | Condensed | 140% | UPPERCASE |
| C8 | 12 px | SemiCondensed | — | 140% | — |
| C9 | 10 px | Medium | Condensed | — | — |

#### UI Elements

| Token | Size | Weight | Width | Line Height | Transform |
|---|---|---|---|---|---|
| Button / Medium | 16 px | Bold | Condensed | 130% | UPPERCASE |
| Button / Small | 12 px | Bold | Condensed | 120% | — |
| Input / Medium | 16 px | — | SemiCondensed | 150% | — |
| Input / Small | 14 px | Medium | SemiCondensed | 140% | — |
| Nav / M | 20 px | SemiBold | Condensed | 140% | — |

### 4.2 Typography Rules

- **Dark backgrounds** → White text (`#FFFFFF`)
- **Light backgrounds** → Black text (`#000000`) or Concrete 800 (`#1D1E1E`)
- Labels, buttons, and eyebrow text use **bold uppercase** Condensed.
- Body copy uses SemiCondensed at regular weight for readability.
- Lesson slide titles use the Display scale (D1–D3) in serif (Geller standard).
- Never use more than two type widths (e.g., Condensed + Standard) on a single screen.

### 4.3 Fallback Fonts

If Geller is unavailable, fall back to a clean sans-serif for body text and a transitional serif for display:

- Display fallback: Georgia, "Times New Roman", serif
- Body/UI fallback: "Helvetica Neue", Arial, sans-serif

---

## 5. Iconography

### 5.1 General Icon Set

Campus uses a custom set of approximately **140+ outlined icons** in a consistent stroke style. Icons are monochrome (black on light, white on dark) and designed on a uniform grid.

**Key characteristics:**

- Stroke-based, not filled (except for a few solid variants like filled star, filled checkbox).
- Consistent 2 px stroke weight at the default 24 px size.
- Square bounding box — icons sit on a 24 × 24 grid with 2 px padding.
- Common categories include: navigation (arrows, chevrons, home, menu), content (documents, images, code, charts), actions (download, upload, share, edit, delete, plus, search), social (users, groups, user-plus), media (play, volume), system (settings, gear, lock, eye, warning, close/X), and data (bar chart, line chart, trending).

### 5.2 Status Icons

Status icons use a **hexagonal badge** shape (matching the Campus logo mark) and come in two sizes — small (inline with text) and large (standalone badges).

| State | Small | Large | Color |
|---|---|---|---|
| Success / Correct | ✓ circle | Hexagon with ✓ | Mint 500 `#00A8C2` (colored variant) or Black (monochrome) |
| Error / Incorrect | ✗ circle | Hexagon with ✗ | Red 500 `#D84F4F` (colored variant) or Black (monochrome) |

- Colored variants: Mint hexagon for success, Red hexagon for error.
- Monochrome variants: Black hexagon for both — used in contexts where color is not available.

---

## 6. Layout & Spacing

### 6.1 App Shell

The Campus web app uses a consistent shell:

- **Top Navigation Bar:** Dark teal (`#002B33`) background. "Campus" wordmark left-aligned. Navigation tabs centered: "My Campus", "Summary", "My Team", "My Candidates", "Send Test". Active tab highlighted with Highlighter 300 (`#E6FF64`) background and black text. Inactive tabs use white text.
- **User sidebar (My Campus page):** Left column with user avatar, name, company, search, and completed-courses list.
- **Content area:** Right-side main content area with course cards, test results, and data visualizations.

### 6.2 Spacing System

Based on an 8 px base unit:

| Token | Value | Usage |
|---|---|---|
| xs | 4 px | Tight inner padding (icon-to-label) |
| sm | 8 px | Default inner padding |
| md | 16 px | Card padding, section gaps |
| lg | 24 px | Between major sections |
| xl | 32 px | Page margins |
| 2xl | 48 px | Hero spacing, large section breaks |
| 3xl | 64 px | Generous padding on lesson slides |

### 6.3 Grid

- Content max-width: ~1440 px
- 12-column grid with 24 px gutters
- Lesson slides are full-bleed within the content area

---

## 7. UI Components

### 7.1 Navigation Tabs

- Shape: Rounded-rectangle pill
- Active: Highlighter 300 (`#E6FF64`) fill, Black text, Bold Condensed uppercase
- Inactive: Transparent fill, White text
- Hover: Subtle Highlighter 50 overlay

### 7.2 Buttons

| Variant | Background | Text | Border |
|---|---|---|---|
| Primary | Highlighter 300 `#E6FF64` | Black | None |
| Secondary / Outline | Transparent | White or Highlighter 300 | 1 px solid White or Highlighter |
| Disabled | Concrete 200 | Concrete 400 | None |

- Shape: Rounded rectangle, moderate border-radius (~8 px)
- Text style: Button / Medium (16 px Bold Condensed, UPPERCASE)
- Padding: 12 px vertical, 24 px horizontal

### 7.3 Course Cards

- Dark background card (`#002B33` or Concrete 800)
- Left: Course thumbnail image (rounded corners)
- Right: Course title (H4 Condensed SemiBold), description (P2), metadata row (subjects count, estimated hours)
- Bottom-right: "VIEW COURSE" button (Primary style)
- Status badge: Hexagonal status icon at top-left of card

### 7.4 Progress / Score Visualization

- **Donut Chart:** Large circular ring displaying score percentage. Ring color: Highlighter 300 on success, gradient through Mint tones. Center text: large score number in Highlighter 300.
- **Horizontal Bars:** Subject-by-subject breakdown. Bar fills use Mint 400–500 (`#65D0E0` to `#00A8C2`). Background track: Concrete 700.
- **Score Scale:** Linear 0–10 with labeled ranges (Beginner, Intermediate, Advanced, Expert, Genius).

### 7.5 Data Summary Cards (Summary Page)

- Light background (White) with dark text
- Large stat number (D2-scale: 80 px Condensed SemiBold)
- Label above in C5 (uppercase, Condensed Bold, Concrete 500)
- Arranged in a 3-column grid

---

## 8. Lesson Slide System (201 Deck Template)

Lesson content is presented in a slide-based format. The deck template defines how educational diagrams and interactive content are displayed.

### 8.1 Slide Chrome

- **Header Bar:** Dark teal (`#002B33`). Breadcrumb navigation: "Campus | … > Lesson > SECTION" (Section label in Highlighter 300). Right side: MENU button, settings icon, slide counter (e.g., "99/99").
- **Footer:** "< PREV" button left, "NEXT >" button right. Both are outlined pill buttons.
- **Content area:** Light gray (`#F2F2F2`) background.

### 8.2 Slide Title Area

- Title in Display scale (D1 — 120 px Condensed Medium), positioned left.
- Description paragraph to the right of the title, set in P1 (22 px SemiCondensed), white text on dark teal header area.

### 8.3 Process Diagram Pattern (Horizontal)

The primary visual pattern for educational content is the **Horizontal Process Diagram** — a left-to-right flow of concept blocks connected by arrows.

**Structure:**

- 3–5 rectangular blocks in a horizontal row
- Connected by thin black right-pointing arrows
- Each block contains: a bold uppercase "CONCEPT" label and a short description sentence

**Block Color Progression (left to right):**

| Position | Background | Text Color |
|---|---|---|
| 1 (leftmost) | Mint 50 / very light teal `#ECFBFE` | Black |
| 2 | Mint 100 / light cyan `#D7F6FB` | Black |
| 3 | Mint 500 `#00A8C2` | White |
| 4 | Mint 700 `#002B33` | White |
| 5 (rightmost / emphasis) | Highlighter 300 `#E6FF64` | Black |

The progression moves from light to dark teal, then culminates in the brand lime for the final/key concept.

**Interactive Features:**

- **Tooltip (ⓘ):** Some blocks include an info icon. On hover, a dark tooltip appears with additional context.
- **"Read more" expandable:** The final (Highlighter) block may include a "+ Read more" link at the bottom. Clicking expands to a full white card overlay with a title and body text in serif (Geller standard), plus a collapse (−) button.

---

## 9. Educational Graphics System

For AI-generated and designer-created educational graphics, the following rules apply (sourced from the Campus graphics system prompt).

### 9.1 Style

Flat, geometric, vector-style illustration. No photorealism, no gradients, no 3D effects, no drop shadows. Think clean educational diagrams with bold shapes and clear labels.

### 9.2 Graphics Color Palette

Use **only** these colors in educational graphics:

| Color | Hex | Role |
|---|---|---|
| Dark teal background | `#002B33` | Default background |
| Teal accent | `#00A8C2` | Diagram elements |
| Light teal | `#65D0E0` | Secondary diagram elements |
| Very light teal | `#BCF1FA` | Tertiary fills |
| Pale cyan | `#D7F6FB` | Lightest fills |
| Bright lime | `#E6FF64` | Primary brand accent / call-out |
| Dark lime | `#C6DB58` | Secondary accent |
| White | `#FFFFFF` | Text, lines, arrows |
| Black | `#000000` | Text only |
| Light gray | `#F2F2F2` | Alternate light backgrounds |
| Medium gray | `#73787A` | Subdued text |
| Dark gray | `#1D1E1E` | Dark text |
| Red | `#D84F4F` | Warnings/errors only |

### 9.3 Graphics Typography

Clean sans-serif font. Bold uppercase for labels. White text on dark backgrounds, black text on light backgrounds.

### 9.4 Graphics Composition

- Centered composition with generous padding.
- Elements clearly separated with white space.
- Use white arrows or lines for connections between elements.

### 9.5 Graphics Format

- Aspect ratio: **16:9**
- Resolution: **2K** (2560 × 1440)
- Background: Transparent or Dark teal (`#002B33`)

---

## 10. Accessibility Guidelines

### 10.1 Color Contrast

- All text must meet WCAG 2.1 AA minimum contrast ratios: 4.5:1 for normal text, 3:1 for large text (18 px+ or 14 px bold+).
- White text on Mint 700 (`#002B33`) passes AA at all sizes.
- Black text on Highlighter 300 (`#E6FF64`) passes AA at all sizes.
- Avoid placing text directly on Mint 300–400 without verifying contrast.

### 10.2 Status Indicators

- Never rely on color alone to communicate status. Always pair color with an icon (checkmark for success, X for error) and/or text label.
- The hexagonal status icons satisfy this requirement by combining shape + symbol + color.

### 10.3 Interactive Elements

- All clickable elements must have a visible focus indicator.
- Tooltip content (ⓘ) must also be accessible via keyboard focus, not just hover.
- "Read more" expandable sections should use proper ARIA attributes (`aria-expanded`, etc.).

---

## 11. File Naming Conventions

### 11.1 Educational Graphics

Pattern: `[COURSE_CODE]-[NUMBER]-[Short-Description].[ext]`

Examples: `B201-01-Incentives.png`, `MS201-04-Price-Gaps.png`

### 11.2 UI Screenshots

Pattern: `[PageName]-[View]-[Year].[ext]`

Examples: `MyCampusPage-Profile-2026.png`, `MyCampusPage-Summary-2026.png`

### 11.3 Design Assets

Organized into subfolders: `/Colors`, `/Typography`, `/Icons`, `/Logo`

---

## 12. Quick Reference Cheat Sheet

| Element | Value |
|---|---|
| Primary dark background | `#002B33` (Mint 700) |
| Primary brand accent | `#E6FF64` (Highlighter 300) |
| Primary interactive color | `#00A8C2` (Mint 500) |
| Error color | `#D84F4F` (Red 500) |
| Body font | Geller SemiCondensed, 16 px |
| Heading font | Geller Condensed SemiBold |
| Display font | Geller Condensed Medium/SemiBold |
| Button text | 16 px Condensed Bold UPPERCASE |
| Icon size | 24 × 24 default |
| Spacing base unit | 8 px |
| Graphics aspect ratio | 16:9 @ 2K |
| Graphics style | Flat vector, no gradients |
