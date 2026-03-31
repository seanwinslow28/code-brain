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
