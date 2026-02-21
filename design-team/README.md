# Design Team

Design system enforcement, visual review, and a team of 4 read-only review agents that audit UI code before shipping.

## The Agent Team

| Agent | Role | What It Checks |
|-------|------|----------------|
| **UI Reviewer** | Visual quality | Layout, spacing, color, typography, hierarchy |
| **Accessibility Checker** | WCAG 2.1 AA | Contrast, keyboard nav, ARIA, semantic HTML |
| **Design System Enforcer** | Token compliance | Hardcoded values, naming, component patterns |
| **Visual Polish Auditor** | Production readiness | Animations, loading/empty/error states, micro-interactions |

All agents are read-only (disallowedTools: Edit, Write, Bash). They identify issues, they don't fix them.

## What Lives Here

### design-system/
Design tokens, component specs, variant documentation. The source of truth for your design system.

### brand/
Brand guidelines, color palettes, typography specs, logo usage rules.

### checklists/
Visual polish checklists, accessibility audit templates, pre-ship review guides.

### reference/
Spring animation parameters, Tailwind advanced patterns, Figma-to-code workflows.

## Related Skills (8)
From export group: 10-master-designer

design-system-claude-md, tailwind-advanced-patterns, animation-library-mastery, prompting-beautiful-ui, micro-interaction-patterns, react-native-animations, visual-polish-checklist, figma-to-code-workflow
