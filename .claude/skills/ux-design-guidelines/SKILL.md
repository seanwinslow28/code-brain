---
name: ux-design-guidelines
description: "Priority-ranked UX design rules for web and mobile apps. 99 guidelines across 10 categories: accessibility, touch/interaction, performance, style selection, layout/responsive, typography/color, animation, forms/feedback, navigation, and charts/data. Includes pre-delivery checklist. Use when designing UI, reviewing UX quality, building components, or checking accessibility, interaction patterns, animation timing, or responsive behavior."
---

# UX Design Guidelines

99 priority-ranked UX rules for building professional web and mobile interfaces. Organized by impact (CRITICAL > HIGH > MEDIUM > LOW) so you address the most impactful issues first.

## When to Use

- Designing new pages, components, or layouts
- Reviewing UI code for user experience and accessibility
- Implementing navigation, animations, or responsive behavior
- Choosing interaction patterns, timing values, or touch targets
- Pre-delivery quality checks before shipping UI code
- When UI looks "unprofessional" but the reason is unclear

## Rule Categories by Priority

| Priority | Category | Impact | Key Checks | Anti-Patterns |
|----------|----------|--------|------------|---------------|
| 1 | Accessibility | CRITICAL | Contrast 4.5:1, Alt text, Keyboard nav, Aria-labels | Removing focus rings, Icon-only buttons without labels |
| 2 | Touch & Interaction | CRITICAL | Min size 44x44px, 8px+ spacing, Loading feedback | Reliance on hover only, Instant state changes (0ms) |
| 3 | Performance | HIGH | WebP/AVIF, Lazy loading, Reserve space (CLS < 0.1) | Layout thrashing, Cumulative Layout Shift |
| 4 | Style Selection | HIGH | Match product type, Consistency, SVG icons (no emoji) | Mixing flat & skeuomorphic, Emoji as icons |
| 5 | Layout & Responsive | HIGH | Mobile-first breakpoints, Viewport meta, No h-scroll | Horizontal scroll, Fixed px widths, Disabled zoom |
| 6 | Typography & Color | MEDIUM | Base 16px, Line-height 1.5, Semantic tokens | Text < 12px, Gray-on-gray, Raw hex in components |
| 7 | Animation | MEDIUM | Duration 150-300ms, transform/opacity only | Decorative-only animation, Animating width/height |
| 8 | Forms & Feedback | MEDIUM | Visible labels, Error near field, Progressive disclosure | Placeholder-only labels, Errors only at top |
| 9 | Navigation Patterns | HIGH | Predictable back, Bottom nav <= 5, Deep linking | Overloaded nav, Broken back behavior |
| 10 | Charts & Data | LOW | Legends, Tooltips, Accessible colors | Color-only meaning, No screen reader summary |

---

## 1. Accessibility (CRITICAL)

- **color-contrast** - Minimum 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold)
- **focus-states** - Visible focus rings on interactive elements (2-4px)
- **alt-text** - Descriptive alt text for meaningful images; decorative images use alt=""
- **aria-labels** - aria-label for icon-only buttons; accessibilityLabel in native
- **keyboard-nav** - Tab order matches visual order; full keyboard support
- **form-labels** - Use label with for attribute; never placeholder-only
- **skip-links** - Skip to main content for keyboard users
- **heading-hierarchy** - Sequential h1-h6, no level skip
- **color-not-only** - Don't convey info by color alone (add icon/text)
- **dynamic-type** - Support system text scaling; avoid truncation as text grows
- **reduced-motion** - Respect prefers-reduced-motion; reduce/disable animations when requested
- **voiceover-sr** - Meaningful accessibilityLabel/accessibilityHint; logical reading order
- **escape-routes** - Provide cancel/back in modals and multi-step flows
- **keyboard-shortcuts** - Preserve system and a11y shortcuts; offer keyboard alternatives for drag-and-drop

## 2. Touch & Interaction (CRITICAL)

- **touch-target-size** - Min 44x44pt (Apple) / 48x48dp (Material); extend hit area beyond visual bounds if needed
- **touch-spacing** - Minimum 8px/8dp gap between touch targets
- **hover-vs-tap** - Use click/tap for primary interactions; don't rely on hover alone
- **loading-buttons** - Disable button during async operations; show spinner or progress
- **error-feedback** - Clear error messages near problem
- **cursor-pointer** - Add cursor-pointer to clickable elements (Web)
- **gesture-conflicts** - Avoid horizontal swipe on main content; prefer vertical scroll
- **tap-delay** - Use touch-action: manipulation to reduce 300ms delay (Web)
- **standard-gestures** - Use platform standard gestures consistently; don't redefine
- **system-gestures** - Don't block system gestures (Control Center, back swipe, etc.)
- **press-feedback** - Visual feedback on press (ripple/highlight; MD state layers)
- **haptic-feedback** - Use haptic for confirmations and important actions; avoid overuse
- **gesture-alternative** - Don't rely on gesture-only interactions; provide visible controls
- **safe-area-awareness** - Keep primary touch targets away from notch, Dynamic Island, gesture bar
- **no-precision-required** - Avoid requiring pixel-perfect taps on small icons or thin edges
- **swipe-clarity** - Swipe actions must show clear affordance or hint (chevron, label)
- **drag-threshold** - Use a movement threshold before starting drag to avoid accidental drags

## 3. Performance (HIGH)

- **image-optimization** - Use WebP/AVIF, responsive images (srcset/sizes), lazy load non-critical
- **image-dimension** - Declare width/height or use aspect-ratio to prevent layout shift (CLS)
- **font-loading** - Use font-display: swap/optional to avoid invisible text (FOIT)
- **font-preload** - Preload only critical fonts; avoid overusing preload on every variant
- **critical-css** - Prioritize above-the-fold CSS (inline critical CSS or early-loaded stylesheet)
- **lazy-loading** - Lazy load non-hero components via dynamic import / route-level splitting
- **bundle-splitting** - Split code by route/feature to reduce initial load and TTI
- **third-party-scripts** - Load third-party scripts async/defer; audit and remove unnecessary
- **reduce-reflows** - Avoid frequent layout reads/writes; batch DOM reads then writes
- **content-jumping** - Reserve space for async content to avoid layout jumps (CLS)
- **lazy-load-below-fold** - Use loading="lazy" for below-the-fold images and heavy media
- **virtualize-lists** - Virtualize lists with 50+ items for memory efficiency and scroll performance
- **main-thread-budget** - Keep per-frame work under ~16ms for 60fps; move heavy tasks off main thread
- **progressive-loading** - Use skeleton screens / shimmer instead of long blocking spinners for >1s operations
- **input-latency** - Keep input latency under ~100ms for taps/scrolls
- **tap-feedback-speed** - Provide visual feedback within 100ms of tap
- **debounce-throttle** - Use debounce/throttle for high-frequency events (scroll, resize, input)
- **offline-support** - Provide offline state messaging and basic fallback (PWA / mobile)
- **network-fallback** - Offer degraded modes for slow networks (lower-res images, fewer animations)

## 4. Style Selection (HIGH)

- **style-match** - Match style to product type (SaaS = clean/minimal, entertainment = bold/vibrant)
- **consistency** - Use same style across all pages
- **no-emoji-icons** - Use SVG icons (Heroicons, Lucide), not emojis
- **color-palette-from-product** - Choose palette from product/industry context
- **effects-match-style** - Shadows, blur, radius aligned with chosen style
- **platform-adaptive** - Respect platform idioms (iOS HIG vs Material): navigation, controls, typography
- **state-clarity** - Make hover/pressed/disabled states visually distinct while staying on-style
- **elevation-consistent** - Use a consistent elevation/shadow scale; avoid random shadow values
- **dark-mode-pairing** - Design light/dark variants together to keep brand and contrast consistent
- **icon-style-consistent** - Use one icon set/visual language (stroke width, corner radius) across product
- **system-controls** - Prefer native/system controls over fully custom ones; customize only when branding requires
- **blur-purpose** - Use blur to indicate background dismissal (modals, sheets), not as decoration
- **primary-action** - Each screen should have only one primary CTA; secondary actions visually subordinate

## 5. Layout & Responsive (HIGH)

- **viewport-meta** - width=device-width initial-scale=1 (never disable zoom)
- **mobile-first** - Design mobile-first, then scale up to tablet and desktop
- **breakpoint-consistency** - Use systematic breakpoints (e.g. 375 / 768 / 1024 / 1440)
- **readable-font-size** - Minimum 16px body text on mobile (avoids iOS auto-zoom)
- **line-length-control** - Mobile 35-60 chars per line; desktop 60-75 chars
- **horizontal-scroll** - No horizontal scroll on mobile; ensure content fits viewport width
- **spacing-scale** - Use 4pt/8dp incremental spacing system
- **touch-density** - Keep component spacing comfortable for touch: not cramped, not causing mis-taps
- **container-width** - Consistent max-width on desktop (max-w-6xl / 7xl)
- **z-index-management** - Define layered z-index scale (e.g. 0 / 10 / 20 / 40 / 100 / 1000)
- **fixed-element-offset** - Fixed navbar/bottom bar must reserve safe padding for underlying content
- **scroll-behavior** - Avoid nested scroll regions that interfere with main scroll
- **viewport-units** - Prefer min-h-dvh over 100vh on mobile
- **orientation-support** - Keep layout readable and operable in landscape mode
- **content-priority** - Show core content first on mobile; fold or hide secondary content
- **visual-hierarchy** - Establish hierarchy via size, spacing, contrast - not color alone

## 6. Typography & Color (MEDIUM)

- **line-height** - Use 1.5-1.75 for body text
- **line-length** - Limit to 65-75 characters per line
- **font-pairing** - Match heading/body font personalities
- **font-scale** - Consistent type scale (e.g. 12 14 16 18 24 32)
- **contrast-readability** - Darker text on light backgrounds (e.g. slate-900 on white)
- **text-styles-system** - Use platform type system (iOS Dynamic Type / Material type roles)
- **weight-hierarchy** - Bold headings (600-700), Regular body (400), Medium labels (500)
- **color-semantic** - Define semantic color tokens (primary, secondary, error, surface) not raw hex
- **color-dark-mode** - Dark mode uses desaturated/lighter tonal variants, not inverted colors
- **color-accessible-pairs** - Foreground/background pairs must meet 4.5:1 (AA) or 7:1 (AAA)
- **color-not-decorative-only** - Functional color (error red, success green) must include icon/text
- **truncation-strategy** - Prefer wrapping over truncation; when truncating use ellipsis + tooltip
- **letter-spacing** - Respect default letter-spacing per platform; avoid tight tracking on body text
- **number-tabular** - Use tabular/monospaced figures for data columns, prices, and timers
- **whitespace-balance** - Use whitespace intentionally to group related items and separate sections

## 7. Animation (MEDIUM)

- **duration-timing** - Use 150-300ms for micro-interactions; complex transitions <= 400ms; avoid >500ms
- **transform-performance** - Use transform/opacity only; avoid animating width/height/top/left
- **loading-states** - Show skeleton or progress indicator when loading exceeds 300ms
- **excessive-motion** - Animate 1-2 key elements per view max
- **easing** - Use ease-out for entering, ease-in for exiting; avoid linear for UI transitions
- **motion-meaning** - Every animation must express a cause-effect relationship, not just be decorative
- **state-transition** - State changes should animate smoothly, not snap
- **continuity** - Page/screen transitions should maintain spatial continuity (shared element, directional slide)
- **parallax-subtle** - Use parallax sparingly; must respect reduced-motion
- **spring-physics** - Prefer spring/physics-based curves over linear or cubic-bezier for natural feel
- **exit-faster-than-enter** - Exit animations shorter than enter (~60-70% of enter duration)
- **stagger-sequence** - Stagger list/grid item entrance by 30-50ms per item
- **shared-element-transition** - Use shared element / hero transitions for visual continuity between screens
- **interruptible** - Animations must be interruptible; user tap/gesture cancels in-progress animation
- **no-blocking-animation** - Never block user input during an animation; UI must stay interactive
- **fade-crossfade** - Use crossfade for content replacement within the same container
- **scale-feedback** - Subtle scale (0.95-1.05) on press for tappable cards/buttons
- **gesture-feedback** - Drag, swipe, and pinch must provide real-time visual response tracking the finger
- **hierarchy-motion** - Use translate/scale direction to express hierarchy: enter from below = deeper
- **motion-consistency** - Unify duration/easing tokens globally; all animations share same rhythm
- **opacity-threshold** - Fading elements should not linger below opacity 0.2
- **modal-motion** - Modals/sheets should animate from their trigger source for spatial context
- **navigation-direction** - Forward navigation animates left/up; backward animates right/down
- **layout-shift-avoid** - Animations must not cause layout reflow or CLS; use transform for position changes

## 8. Forms & Feedback (MEDIUM)

- **input-labels** - Visible label per input (not placeholder-only)
- **error-placement** - Show error below the related field
- **submit-feedback** - Loading then success/error state on submit
- **required-indicators** - Mark required fields (e.g. asterisk)
- **empty-states** - Helpful message and action when no content
- **toast-dismiss** - Auto-dismiss toasts in 3-5s
- **confirmation-dialogs** - Confirm before destructive actions
- **input-helper-text** - Persistent helper text below complex inputs, not just placeholder
- **disabled-states** - Disabled elements use reduced opacity (0.38-0.5) + cursor change + semantic attribute
- **progressive-disclosure** - Reveal complex options progressively; don't overwhelm users upfront
- **inline-validation** - Validate on blur (not keystroke); show error only after user finishes input
- **input-type-keyboard** - Use semantic input types (email, tel, number) for correct mobile keyboard
- **password-toggle** - Provide show/hide toggle for password fields
- **autofill-support** - Use autocomplete / textContentType attributes for system autofill
- **undo-support** - Allow undo for destructive or bulk actions (e.g. "Undo delete" toast)
- **success-feedback** - Confirm completed actions with brief visual feedback (checkmark, toast)
- **error-recovery** - Error messages must include a clear recovery path (retry, edit, help link)
- **multi-step-progress** - Multi-step flows show step indicator or progress bar; allow back navigation
- **form-autosave** - Long forms should auto-save drafts to prevent data loss
- **sheet-dismiss-confirm** - Confirm before dismissing a sheet/modal with unsaved changes
- **error-clarity** - Error messages must state cause + how to fix (not just "Invalid input")
- **field-grouping** - Group related fields logically (fieldset/legend or visual grouping)
- **read-only-distinction** - Read-only state should be visually and semantically different from disabled
- **focus-management** - After submit error, auto-focus the first invalid field
- **error-summary** - For multiple errors, show summary at top with anchor links to each field
- **touch-friendly-input** - Mobile input height >= 44px for touch target requirements
- **destructive-emphasis** - Destructive actions use semantic danger color and are visually separated
- **toast-accessibility** - Toasts must not steal focus; use aria-live="polite" for screen reader
- **aria-live-errors** - Form errors use aria-live region or role="alert" for screen readers
- **contrast-feedback** - Error and success state colors must meet 4.5:1 contrast ratio
- **timeout-feedback** - Request timeout must show clear feedback with retry option

## 9. Navigation Patterns (HIGH)

- **bottom-nav-limit** - Bottom navigation max 5 items; use labels with icons
- **drawer-usage** - Use drawer/sidebar for secondary navigation, not primary actions
- **back-behavior** - Back navigation must be predictable and consistent; preserve scroll/state
- **deep-linking** - All key screens must be reachable via deep link / URL
- **tab-bar-ios** - iOS: use bottom Tab Bar for top-level navigation
- **top-app-bar-android** - Android: use Top App Bar with navigation icon for primary structure
- **nav-label-icon** - Navigation items must have both icon and text label
- **nav-state-active** - Current location must be visually highlighted in navigation
- **nav-hierarchy** - Primary nav vs secondary nav must be clearly separated
- **modal-escape** - Modals and sheets must offer a clear close/dismiss affordance
- **search-accessible** - Search must be easily reachable; provide recent/suggested queries
- **breadcrumb-web** - Web: use breadcrumbs for 3+ level deep hierarchies
- **state-preservation** - Navigating back must restore previous scroll position, filter state, input
- **gesture-nav-support** - Support system gesture navigation without conflict
- **tab-badge** - Use badges on nav items sparingly for unread/pending; clear after user visits
- **overflow-menu** - When actions exceed available space, use overflow/more menu
- **bottom-nav-top-level** - Bottom nav is for top-level screens only; never nest sub-navigation
- **adaptive-navigation** - Large screens (>= 1024px) prefer sidebar; small screens use bottom/top nav
- **back-stack-integrity** - Never silently reset the navigation stack or jump to home
- **navigation-consistency** - Navigation placement must stay the same across all pages
- **avoid-mixed-patterns** - Don't mix Tab + Sidebar + Bottom Nav at the same hierarchy level
- **modal-vs-navigation** - Modals must not be used for primary navigation flows
- **focus-on-route-change** - After page transition, move focus to main content region for screen readers
- **persistent-nav** - Core navigation must remain reachable from deep pages
- **destructive-nav-separation** - Dangerous actions (delete, logout) must be spatially separated from normal nav
- **empty-nav-state** - When a nav destination is unavailable, explain why instead of silently hiding

## 10. Charts & Data (LOW)

- **chart-type** - Match chart type to data type (trend = line, comparison = bar, proportion = pie/donut)
- **color-guidance** - Use accessible color palettes; avoid red/green only pairs for colorblind users
- **data-table** - Provide table alternative for accessibility; charts alone are not screen-reader friendly
- **pattern-texture** - Supplement color with patterns, textures, or shapes for colorblind users
- **legend-visible** - Always show legend; position near the chart, not below a scroll fold
- **tooltip-on-interact** - Provide tooltips/data labels on hover (Web) or tap (mobile) showing exact values
- **axis-labels** - Label axes with units and readable scale; avoid truncated/rotated labels on mobile
- **responsive-chart** - Charts must reflow or simplify on small screens
- **empty-data-state** - Show meaningful empty state when no data ("No data yet" + guidance)
- **loading-chart** - Use skeleton or shimmer placeholder while chart data loads
- **animation-optional** - Chart entrance animations must respect prefers-reduced-motion
- **large-dataset** - For 1000+ data points, aggregate or sample; provide drill-down for detail
- **number-formatting** - Use locale-aware formatting for numbers, dates, currencies
- **touch-target-chart** - Interactive chart elements must have >= 44pt tap area or expand on touch
- **no-pie-overuse** - Avoid pie/donut for >5 categories; switch to bar chart for clarity
- **contrast-data** - Data lines/bars vs background >= 3:1; data text labels >= 4.5:1
- **legend-interactive** - Legends should be clickable to toggle series visibility
- **direct-labeling** - For small datasets, label values directly on the chart
- **tooltip-keyboard** - Tooltip content must be keyboard-reachable and not rely on hover alone
- **sortable-table** - Data tables must support sorting with aria-sort indicating current sort state
- **axis-readability** - Axis ticks must not be cramped; maintain readable spacing
- **data-density** - Limit information density per chart to avoid cognitive overload
- **trend-emphasis** - Emphasize data trends over decoration; avoid heavy gradients/shadows
- **gridline-subtle** - Grid lines should be low-contrast (e.g. gray-200) so they don't compete with data
- **focusable-elements** - Interactive chart elements must be keyboard-navigable
- **screen-reader-summary** - Provide text summary or aria-label describing chart's key insight
- **error-state-chart** - Data load failure must show error message with retry action
- **export-option** - For data-heavy products, offer CSV/image export of chart data
- **drill-down-consistency** - Drill-down interactions must maintain clear back-path and hierarchy
- **time-scale-clarity** - Time series charts must clearly label time granularity and allow switching

---

## Common Professional Standards

Frequently overlooked issues that make UI look unprofessional:

### Icons & Visual Elements

| Rule | Standard | Avoid |
|------|----------|-------|
| No Emoji as Icons | Use vector-based icons (Lucide, Heroicons) | Emojis for navigation, settings, or system controls |
| Vector-Only Assets | SVG or platform vector icons that scale cleanly | Raster PNG icons that blur or pixelate |
| Consistent Icon Sizing | Define icon sizes as tokens (icon-sm, icon-md=24pt, icon-lg) | Mixing arbitrary values randomly |
| Stroke Consistency | Consistent stroke width within the same layer (1.5px or 2px) | Mixing thick and thin stroke styles |
| Filled vs Outline | One icon style per hierarchy level | Mixing filled and outline at same level |
| Icon Alignment | Align icons to text baseline with consistent padding | Misaligned icons or inconsistent spacing |
| Icon Contrast | WCAG: 4.5:1 for small elements, 3:1 for larger UI glyphs | Low-contrast icons blending into background |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|----|----- |
| Surface readability | Cards/surfaces clearly separated from background | Overly transparent surfaces |
| Text contrast (light) | Body text contrast >= 4.5:1 against light surfaces | Low-contrast gray body text |
| Text contrast (dark) | Primary text >= 4.5:1, secondary text >= 3:1 on dark surfaces | Text blending into background |
| Border visibility | Separators visible in both themes | Theme-specific borders disappearing |
| State contrast parity | Pressed/focused/disabled equally distinguishable in both themes | States defined for one theme only |
| Token-driven theming | Semantic color tokens mapped per theme | Hardcoded per-screen hex values |
| Scrim legibility | Modal scrim 40-60% black to isolate foreground | Weak scrim leaving background competing |

---

## Pre-Delivery Checklist

Before delivering UI code, verify:

### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon family and style
- [ ] Official brand assets used with correct proportions and clear space
- [ ] Pressed-state visuals do not shift layout bounds or cause jitter
- [ ] Semantic theme tokens used consistently (no ad-hoc hardcoded colors)

### Interaction
- [ ] All tappable elements provide clear pressed feedback
- [ ] Touch targets meet minimum size (>= 44x44pt iOS, >= 48x48dp Android)
- [ ] Micro-interaction timing stays in 150-300ms range
- [ ] Disabled states are visually clear and non-interactive
- [ ] Screen reader focus order matches visual order
- [ ] Gesture regions avoid nested/conflicting interactions

### Light/Dark Mode
- [ ] Primary text contrast >= 4.5:1 in both modes
- [ ] Secondary text contrast >= 3:1 in both modes
- [ ] Dividers/borders and interaction states distinguishable in both modes
- [ ] Modal/drawer scrim opacity strong enough for foreground legibility
- [ ] Both themes tested before delivery

### Layout
- [ ] Safe areas respected for headers, tab bars, and bottom CTAs
- [ ] Scroll content not hidden behind fixed/sticky bars
- [ ] Verified on small phone, large phone, and tablet (portrait + landscape)
- [ ] Horizontal insets/gutters adapt correctly by device size
- [ ] 4/8dp spacing rhythm maintained across all levels
- [ ] Long-form text measure remains readable on larger devices

### Accessibility
- [ ] All meaningful images/icons have accessibility labels
- [ ] Form fields have labels, hints, and clear error messages
- [ ] Color is not the only indicator
- [ ] Reduced motion and dynamic text size supported without layout breakage
- [ ] Accessibility traits/roles/states announced correctly
