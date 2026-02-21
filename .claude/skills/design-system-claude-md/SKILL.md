---
name: design-system-claude-md
description: Design system encoding for CLAUDE.md to ensure on-brand, consistent UI generation. Create and maintain design tokens, typography scales, spacing systems, shadow depths, animation defaults, and dark mode rules in CLAUDE.md. Use when setting up a new project design system, enforcing brand consistency, defining color tokens, typography scale, or component interaction patterns.
---

# Design System for CLAUDE.md

## Purpose

Encode a complete design system in CLAUDE.md so Claude generates on-brand, polished code on every attempt. Use semantic token names, explicit constraint rules, and progressive disclosure to keep the file under 300 lines while governing all visual decisions.

## When to Use

- Setting up a new project and defining visual standards
- Claude is generating inconsistent colors, spacing, or typography
- Encoding brand identity into a machine-readable format
- Defining dark mode rules, animation defaults, or interaction patterns
- Creating a shared design language across multiple components

## Examples

**Example 1: New project setup**
```
User: "Set up a design system for my Next.js dashboard"
Claude: [Uses design-system-claude-md] Creates CLAUDE.md with semantic color
tokens, 4px spacing scale, typography scale, shadow depth system, animation
defaults, and interaction patterns. Adds CSS variable definitions in globals.css.
```

**Example 2: Fixing inconsistent output**
```
User: "Claude keeps using random colors and spacing"
Claude: [Uses design-system-claude-md] Adds strict token rules to CLAUDE.md:
"NEVER hardcode hex values. Use semantic tokens only." Defines complete
color, spacing, and radius token sets with usage context.
```

## CLAUDE.md Design System Template

Place this in your project root. Customize tokens to your brand.

```markdown
# CLAUDE.md - Design System Governance

## Visual Language and Tokens
IMPORTANT: Do not use hardcoded values (e.g., 16px, #000). Always use the
semantic variables defined below.

### Color System (Semantic)
- Primary: --color-primary (Brand action) | --color-primary-hover
- Surface: --bg-surface (Card/Panel) | --bg-canvas (Page background)
- Text: --text-primary (High contrast) | --text-secondary (Medium contrast)
- Border: --border-default | --border-subtle
- Feedback: --color-success | --color-error | --color-warning
- Dark Mode: Use CSS variables rooted in body[data-theme='dark'].
  Do not use separate classes for dark mode.

### Typography Scale
- Font Family: --font-sans (Inter/System) | --font-mono (JetBrains Mono)
- h1 / .text-4xl: 36px Desktop / 30px Mobile - Bold
- h2 / .text-3xl: 30px Desktop / 24px Mobile - SemiBold
- h3 / .text-2xl: 24px - Medium
- .text-base: 16px / 1.5 lineHeight - Regular
- .text-sm: 14px / 1.4 lineHeight - Regular
- .text-xs: 12px / 1.2 lineHeight - Medium (Caps/Labels)

### Spacing Scale (4px Base)
- 2 (8px): Micro-spacing (icon to text)
- 4 (16px): Standard component padding
- 6 (24px): Container padding / card gap
- 8 (32px): Section gap
- 16 (64px): Layout gap

### Shape and Depth
Border Radius:
- --radius-sm: 4px (Checkboxes, tags)
- --radius-md: 8px (Buttons, inputs, cards)
- --radius-lg: 16px (Modals, large containers)
- --radius-full: 9999px (Pills, avatars)

Shadow Depth:
- --shadow-sm: 0 1px 2px rgba(0,0,0,0.05) (Interactive hints)
- --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1) (Cards, dropdowns)
- --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1) (Modals, floats)

### Animation and Motion
Default Curve: cubic-bezier(0.4, 0, 0.2, 1)
- --duration-fast: 150ms (Hover, micro-interactions)
- --duration-normal: 300ms (Modals, drawer slides)
- --duration-slow: 500ms (Page transitions)

Pattern Rules:
- Entrances: ease-out + opacity-0 to opacity-100 + small translate-y
- Exits: ease-in + duration-fast
- Hover: Only animate transform, opacity, or colors. Never layout properties.

## Interaction Patterns
- Buttons: hover (brightness-110%), active (scale-95), focus-visible (ring-2)
- Inputs: Default border --border-default. Focus: border --color-primary + ring
- All interactive elements: minimum 44px touch target
- Never remove focus outlines without replacing them
- Text contrast: WCAG AA (4.5:1) via token pairing

## Code Rules
1. Styling: Use Tailwind utility classes matching tokens above
2. Components: Prefer composition. Use cva (class-variance-authority) for variants
3. Naming: PascalCase for components, camelCase for props

## Design System Rules
1. Token Usage: ALWAYS use semantic tokens, never primitive colors or hex codes
2. Spacing: Strictly follow 4px grid. Round 15px to 16px (unit-4)
3. Dark Mode: DO NOT hardcode dark classes. Use semantic variable system
4. Consistency: Check src/components/ui first. Composition over new implementation
5. Motion: Limit to user-triggered micro-interactions (hover, click)
```

## CSS Variable Implementation

```css
@layer base {
  :root {
    --bg-canvas: 0 0% 100%;
    --bg-surface: 210 40% 98%;
    --text-primary: 222 47% 11%;
    --color-primary: 217 91% 60%;
    --shadow-color: 220 3% 15%;
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 16px;
  }

  [data-theme="dark"] {
    --bg-canvas: 222 47% 11%;
    --bg-surface: 217 33% 17%;
    --text-primary: 210 40% 98%;
    --shadow-color: 0 0% 0%;
  }
}
```

## Tailwind Configuration

```typescript
// tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  theme: {
    spacing: {
      0: "0px",
      1: "4px",
      2: "8px",
      3: "12px",
      4: "16px",
      6: "24px",
      8: "32px",
      12: "48px",
      16: "64px",
    },
    fontSize: {
      xs: ["12px", { lineHeight: "16px" }],
      sm: ["14px", { lineHeight: "20px" }],
      base: ["16px", { lineHeight: "24px" }],
      lg: ["18px", { lineHeight: "28px" }],
      xl: ["20px", { lineHeight: "28px" }],
      "2xl": ["24px", { lineHeight: "32px" }],
      "3xl": ["30px", { lineHeight: "36px" }],
      "4xl": ["36px", { lineHeight: "40px" }],
    },
    extend: {
      borderRadius: {
        sm: "var(--radius-sm)",
        md: "var(--radius-md)",
        lg: "var(--radius-lg)",
      },
    },
  },
};

export default config;
```

## Governance Best Practices

1. **Semantic naming**: Use `Action-Primary` (intent), not `Blue-500` (appearance)
2. **Explain relationships**: "Use text-secondary for metadata and timestamps"
3. **Progressive disclosure**: Keep CLAUDE.md under 300 lines. Point to external docs
4. **Guardrails over manuals**: Focus on constraints ("NEVER introduce new z-indices")
5. **Component matrix**: Validate all states (Default, Hover, Active, Focus, Disabled)

## Success Criteria

- [ ] CLAUDE.md defines semantic tokens for color, spacing, typography, shadows
- [ ] All tokens have named intent, not just values
- [ ] Dark mode uses variable remapping, not separate classes
- [ ] Animation defaults include duration and easing values
- [ ] File stays under 300 lines with pointers to external references

## Copy/Paste Ready

```
"Set up a design system in CLAUDE.md for this project"
"Define design tokens for my brand colors and typography"
"Claude keeps using random spacing, enforce the 4px grid"
"Add dark mode rules to my design system"
"Create a CLAUDE.md style guide for consistent UI generation"
```
