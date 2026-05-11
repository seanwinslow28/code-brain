---
name: The Iterative Blueprint
colors:
  surface: '#fff9f0'
  surface-dim: '#dfd9d1'
  surface-bright: '#fff9f0'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f9f3ea'
  surface-container: '#f3ede4'
  surface-container-high: '#ede7df'
  surface-container-highest: '#e7e2d9'
  on-surface: '#1d1b16'
  on-surface-variant: '#404849'
  inverse-surface: '#32302a'
  inverse-on-surface: '#f6f0e7'
  outline: '#707979'
  outline-variant: '#c0c8c9'
  surface-tint: '#386569'
  primary: '#00272a'
  on-primary: '#ffffff'
  primary-container: '#0a3e42'
  on-primary-container: '#7ba9ad'
  inverse-primary: '#a0cfd3'
  secondary: '#48626e'
  on-secondary: '#ffffff'
  secondary-container: '#cbe7f5'
  on-secondary-container: '#4e6874'
  tertiary: '#10252e'
  on-tertiary: '#ffffff'
  tertiary-container: '#263b44'
  on-tertiary-container: '#8fa5b0'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#bcebef'
  primary-fixed-dim: '#a0cfd3'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#1e4d51'
  secondary-fixed: '#cbe7f5'
  secondary-fixed-dim: '#afcbd8'
  on-secondary-fixed: '#021f29'
  on-secondary-fixed-variant: '#304a55'
  tertiary-fixed: '#cfe6f2'
  tertiary-fixed-dim: '#b4cad6'
  on-tertiary-fixed: '#071e27'
  on-tertiary-fixed-variant: '#354a53'
  background: '#fff9f0'
  on-background: '#1d1b16'
  surface-variant: '#e7e2d9'
typography:
  display-lg:
    fontFamily: Newsreader
    fontSize: 3.5rem
    fontWeight: '400'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Newsreader
    fontSize: 2rem
    fontWeight: '400'
    lineHeight: '1.3'
  title-lg:
    fontFamily: Inter
    fontSize: 1.375rem
    fontWeight: '500'
    lineHeight: '1.5'
  body-lg:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Space Grotesk
    fontSize: 0.75rem
    fontWeight: '500'
    lineHeight: '1.4'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
---

# Design System: The Iterative Blueprint

## 1. Overview & Creative North Star

### Creative North Star: "The Iterative Blueprint"
This design system navigates the tension between the analog soul of a filmmaker and the digital precision of a Product Manager. It celebrates the journey from the first pencil sketch to the final AI-augmented technical execution. We avoid the "template" look by treating the screen not as a flat grid, but as a living desk—a place where technical documentation, blueprint vellum, and hand-drawn concepts overlap.

**Visual Philosophy:**
*   **Intentional Asymmetry:** Layouts should feel like a storyboard or a technical manual, with purposeful "white space" that allows the eye to rest.
*   **The Bridge:** We use high-end editorial serifs (the narrative) alongside monospaced-style technical labels (the data).
*   **Layered Reality:** Use depth to show the evolution of work. Backgrounds feel like heavy paper; foreground elements feel like light, digital overlays.

---

## 2. Colors

The palette is a sophisticated blend of "Ink and Earth." It utilizes deep, technical teals against a warm, textural paper base to evoke a premium, archival feel.

### Core Palette
*   **Surface (Paper):** `#fff8f2` (Surface) and `#fdf2e2` (Surface Container Low). This is our "analog" base.
*   **Ink (Technical):** `#00272a` (Primary) and `#0a3e42` (Primary Container). These represent the depth of the technical mind.
*   **Graphite:** `#48626e` (Secondary) for mid-tones and structural elements.

### The "No-Line" Rule
To maintain a high-end editorial feel, **prohibit 1px solid borders for sectioning.** Boundaries must be defined through background color shifts. For example, a project showcase section should transition from `surface` to `surface-container-low` to define its start, rather than using a horizontal rule.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers:
1.  **Base Layer:** `surface` (The desk).
2.  **Middle Layer:** `surface-container` (The paper sheet).
3.  **Top Layer:** `surface-container-highest` (The sticky note or callout).

### The "Glass & Gradient" Rule
To inject "Digital Innovation" into the "Blueprint" aesthetic:
*   **Glassmorphism:** Use `surface-container-lowest` with a 70% opacity and a `20px` backdrop-blur for floating navigation or AI-driven insights. This creates a "frosted vellum" effect.
*   **Signature Gradients:** Use a subtle radial gradient transitioning from `primary` to `primary-container` for main CTAs to give them a "lit from within" technical glow.

---

## 3. Typography

The typography is a dialogue between the storyteller (Newsreader) and the technologist (Inter & Space Grotesk).

*   **Display & Headlines (Newsreader):** Used for narrative headers and personal reflections. It should feel like a high-end magazine.
    *   *Token:* `display-lg` (3.5rem) / `headline-lg` (2rem).
*   **Titles & Body (Inter):** The "Workhorse." Used for project descriptions and technical specs. It provides the clean, brutalist clarity found in modern technical documentation.
    *   *Token:* `title-lg` (1.375rem) / `body-lg` (1rem).
*   **Technical Labels (Space Grotesk):** Used for metadata, tags, and "Blueprint" annotations. This adds a subtle monospaced flavor without the clunkiness of a typewriter font.
    *   *Token:* `label-md` (0.75rem).

---

## 4. Elevation & Depth

We eschew traditional drop shadows in favor of **Tonal Layering** to create a modern, "flat-but-deep" aesthetic.

*   **The Layering Principle:** Depth is achieved by stacking. A card component (`surface-container-lowest`) placed on a section background (`surface-container-low`) creates a natural, soft lift.
*   **Ambient Shadows:** If a floating element (like a modal) requires a shadow, it must be "Ambient."
    *   **Spec:** `0px 20px 40px rgba(32, 27, 18, 0.06)`. It should be a tinted version of the `on-surface` color to mimic natural light hitting paper.
*   **The "Ghost Border" Fallback:** For accessibility in forms, use a "Ghost Border": `outline-variant` at **15% opacity**. This provides a guide without the "boxy" feel of standard UI.

---

## 5. Components

### Buttons
*   **Primary:** Solid `primary` background with `on-primary` (white) text. Shape: `md` (0.5rem) to reflect a more approachable, rounded technical aesthetic.
*   **Secondary:** `surface-container-highest` background with `primary` text. No border.
*   **Tertiary (The Sketch Link):** Text only in `primary`, with a custom 2px underline that looks like a hand-drawn stroke (use an SVG mask if possible).

### Chips (Technical Tags)
*   **Style:** `surface-variant` background with `label-md` (Space Grotesk) text.
*   **Corner:** `none` (0px) to lean into the brutalist aesthetic. These should look like cut-out pieces of tape or technical labels.

### Cards & Lists
*   **Rule:** Forbid divider lines.
*   **Separation:** Use `spacing-12` (3rem) of vertical white space to separate list items.
*   **Hover State:** On hover, a card should shift its background color from `surface-container` to `surface-container-highest`—a subtle "highlight" effect.
*   **Corner:** `lg` (1rem) for standard containers.

### Blueprint Annotations (New Component)
*   **Role:** Small, floating text snippets in `label-sm` (Space Grotesk) with a thin `primary` leader line (0.5px) pointing to UI elements. This mimics the "sketch-like" annotations from the reference character image.

---

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical margins. Align some text to a strict grid while letting images/sketches break the "gutter."
*   **Do** integrate hand-drawn elements (pencil textures, rough circles) sparingly over very clean, technical layouts to emphasize the "Creative Technologist" persona.
*   **Do** use the `surface-dim` token for footer areas to create a sense of groundedness.

### Don't
*   **Don't** use 100% black (`#000000`) for text. Use `on-surface` (`#201b12`) for a softer, premium ink feel.
*   **Don't** use rounded corners above `1.5rem` (xl). We want the system to feel architectural and precise, not overly bubbly.
*   **Don't** use standard "drop shadows" on every card. Rely on the "Paper-on-Paper" background shifts first.
*   **Don't** use generic icons. If an icon is needed, use thin-stroke (1px) technical icons that look like blueprint symbols.

---
**Director's Closing Note:** This system is about the "In-Between." It is the moment where the artist's sketch becomes the engineer's requirement. By shifting to a more rounded geometry, we embrace a friendlier technical interface while keeping the backgrounds warm and human.