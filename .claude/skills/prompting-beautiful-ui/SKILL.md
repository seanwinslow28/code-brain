---
name: prompting-beautiful-ui
description: Prompting strategies for generating beautiful, polished UI with Claude Code. Covers the spec-driven development workflow, visual description vocabulary, component prompt templates, and common mistakes that produce generic AI output. Use when creating components, building pages, designing interfaces, or when UI output looks generic or broken.
---

# Prompting for Beautiful UI

## Purpose

Transform vague UI requests into specification-driven prompts that produce polished, distinctive interfaces on the first try. Use the research-first workflow (brainstorm, specify, generate) and precise visual vocabulary to avoid generic "AI slop" output.

## When to Use

- Creating any new UI component or page layout
- UI output looks generic, corporate, or "AI-generated"
- Building a component that needs specific states (loading, error, empty)
- Wanting to match a specific design aesthetic
- Setting up system prompts for consistent visual quality

## Examples

**Example 1: Breaking out of generic output**
```
User: "Create a pricing page for my SaaS app"
Claude: [Uses prompting-beautiful-ui] Before generating code, asks:
1. What aesthetic? (brutalist, glassmorphism, minimal editorial)
2. What font pairing? (suggest: Space Grotesk + JetBrains Mono)
3. What color strategy? (monochromatic with accent, or gradient)
Then generates spec, then implements with all states.
```

**Example 2: Component with full states**
```
User: "Build me a user profile card"
Claude: [Uses prompting-beautiful-ui] Generates card with:
- Default, hover, loading (skeleton), error, and empty states
- Specific font weights and spacing from design tokens
- Hover elevation using transform + shadow transition
- Focus-visible ring for keyboard navigation
```

## The Spec-Driven Workflow

Never jump straight to code. Use three phases:

### Phase 1: Brainstorm
Ask Claude to act as a Product Designer first. Generate a high-level plan.

Prompt pattern:
```
Draft a detailed specification for [feature]. Cover objectives, user stories,
and acceptance criteria. Do not write code yet.
```

### Phase 2: Specify
Refine the plan into a formal spec. Decompose into data models, edge logic, and UI components in that order.

### Phase 3: Generate
Only after the spec is approved, ask for implementation.

Prompt pattern:
```
Implement the 'UserCard' component following the specifications in SPEC.md
and the design tokens in CLAUDE.md.
```

## Visual Description Vocabulary

Vague adjectives produce generic output. Use specific terms:

| Dimension | Avoid (Generic) | Use (Specific) |
|---|---|---|
| Typography | "Nice fonts", "Clean text" | "Editorial aesthetic", "Space Grotesk + JetBrains Mono", "High contrast serif/sans pairing" |
| Spacing | "Good spacing" | "Powers of 2 scale (4, 8, 16, 32px)", "Dense data grid", "Airy whitespace" |
| Color | "Bright colors" | "Dominant monochromatic with Electric Lime accents", "Low-saturation pastel", "OLED black dark mode" |
| Motion | "Smooth animations" | "Staggered entrance reveals", "CSS-only micro-interactions", "Spring physics for layout" |
| Layout | "Responsive" | "Bento-grid layout", "Sidebar with collapsible groups", "Asymmetric split-screen" |

## Component Prompt Template

Structure prompts with Role-Task-Context-Format:

```markdown
# ROLE
You are a Senior Design Systems Engineer. You value accessibility (WCAG AA),
semantic HTML, and distinctive aesthetics over generic "AI slop."

# TASK
Build a [Component Name] using [Tech Stack: React, Tailwind, Lucide Icons].

# VISUAL CONTEXT
- Typography: [Specific font pairing or utility class]
- Spacing: [Density level, e.g., "Comfortable, 16px padding"]
- Shape: [Border radius strategy, e.g., "Fully rounded pill shapes"]
- Vibe: [Specific aesthetic, e.g., "Brutalist", "Glassmorphism", "Swiss Style"]

# FUNCTIONAL REQUIREMENTS
- [Requirement 1: e.g., "Must handle loading and error states"]
- [Requirement 2: e.g., "Support keyboard navigation"]

# REFERENCE
[Attach screenshot of desired layout if available]
```

## Anti-Generic System Prompt

Add this to your system instructions to break Claude out of default patterns:

```typescript
const AESTHETICS_PROMPT = `
<frontend_aesthetics>
You tend to converge toward generic outputs. In frontend design, this creates
"AI slop." Avoid this: make creative, distinctive frontends.

Focus on:
1. Typography: Avoid Arial/Roboto/Inter defaults. Use Space Grotesk, Fraunces,
   or JetBrains Mono.
2. Color: Commit to a cohesive aesthetic. Dominant colors with sharp accents
   over timid palettes.
3. Motion: Use staggered reveals (animation-delay) for page loads.
4. Depth: Layer CSS gradients or subtle noise textures over flat colors.

Avoid:
- Purple gradients on white backgrounds
- Cookie-cutter component patterns
- Default spacing and border radius

Interpret creatively. Think outside the box.
</frontend_aesthetics>
`;
```

## Details to Specify Upfront

Pre-load Claude with your "Design Truth" to avoid iteration:

1. **Design tokens**: Semantic intent, not just values. `color-action-primary` not `blue-500`
2. **Component library**: "Use shadcn/ui; do not invent new primitives"
3. **Tech stack**: React, Vue, Tailwind, CSS Modules, etc.
4. **Accessibility**: "44x44px minimum touch targets"
5. **States**: Always request loading, error, and empty states explicitly
6. **Screenshots**: Paste current state alongside code for visual context

**Scope boundaries:**
- For **post-generation polish** (reviewing shadows, spacing, dark mode), use `visual-polish-checklist` instead.
- For **animation/video critique** without generating code, use `creative-director` instead.
- This skill focuses on **crafting prompts** that produce beautiful UI on the first try.

## Common Mistakes

| Mistake | Fix |
|---|---|
| One giant prompt for entire app | Break into component-by-component requests |
| "Fix the layout" without screenshot | Always paste screenshot of current state |
| Asking for "modern UI" | Use specific aesthetic (brutalist, editorial, glassmorphism) |
| Forgetting data states | Explicitly request skeleton loaders and error boundaries |
| No design tokens defined | Create CLAUDE.md with semantic token definitions first |

## Success Criteria

- [ ] Every component request follows the spec-driven workflow (brainstorm, specify, generate)
- [ ] Visual vocabulary uses specific terms, not vague adjectives
- [ ] Component prompts include all interaction states (hover, focus, loading, error, empty)
- [ ] CLAUDE.md or system prompt includes design token governance
- [ ] Output is visually distinctive, not generic corporate SaaS

## Copy/Paste Ready

```
"Create a component for [feature] - brainstorm the design first, don't code yet"
"Build a page layout that feels premium and editorial, not generic"
"Make this look distinctive - avoid default AI aesthetics"
"Design this component with all states: loading, error, empty, populated"
"Review this UI for 'AI slop' and suggest distinctive alternatives"
```
