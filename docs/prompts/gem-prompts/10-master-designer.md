# Master Designer - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Master Designer"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals. I want Claude Code to produce beautiful, polished, **alive-feeling** interfaces on the first try — minimal iteration. My stack is React (Vite + Tailwind), React Native (Expo + Reanimated), and I care about motion, micro-interactions, and premium visual quality. I'm not a designer, but I want design-quality output.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers making Claude Code a **design-excellence partner** that produces polished, animated, premium UI across web and mobile.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Master Designer") contains deep research on creating beautiful interfaces with Claude Code: animation libraries (Motion/Framer Motion, React Spring, GSAP, CSS animations), micro-interaction patterns, design tool MCP integrations (Figma, icon libraries), Tailwind CSS advanced patterns, React Native animations (Reanimated, Gesture Handler), desktop app design (Electron/Tauri), prompting strategies for visual code, design system management, and visual polish techniques. Sources include animation library documentation, design system guides, UI/UX research, and AI-assisted design workflow articles.

## Your Task

Analyze all sources in this notebook and generate **6-8 Claude Skills** that make Claude Code produce design-quality interfaces. The goal: describe what I want, and Claude generates polished, animated, accessible code on the first or second try.

## Target Skills to Extract

### 1. Animation Library Mastery
**Priority**: High
**What to extract**: A decision framework for choosing between Motion (Framer Motion), React Spring, GSAP, and CSS animations. For each library: when to use it, copy-paste patterns for common effects (fade in, slide, scale, spring bounce), integration with React/Next.js, and performance characteristics. Default recommendation: Motion for most use cases (best AI generation quality). Include specific spring parameters for common motion styles:
- Bouncy: `{ stiffness: 300, damping: 10 }`
- Smooth: `{ stiffness: 100, damping: 30 }`
- Snappy: `{ stiffness: 500, damping: 30 }`
**Trigger phrases**: "animate", "animation", "Motion", "Framer Motion", "React Spring", "GSAP", "spring animation", "transition"

### 2. Micro-Interaction Pattern Library
**Priority**: High
**What to extract**: Copy-paste micro-interaction patterns for the most impactful UI elements: button feedback (hover scale, click shrink, loading state), form field interactions (focus glow, validation feedback, floating labels), navigation transitions (indicator slide, menu reveal, hamburger morph), state change animations (loading → loaded, empty → populated, expand/collapse), scroll reveals (fade on scroll, stagger reveals, parallax), and attention direction (pulse, bounce, badge animations). Include timing recommendations for each.
**Trigger phrases**: "micro-interaction", "hover effect", "button animation", "form animation", "loading state", "scroll animation", "feedback"

### 3. Design System for CLAUDE.md
**Priority**: High
**What to extract**: How to encode a design system in CLAUDE.md so Claude generates on-brand code consistently: color token definitions, typography scale, spacing scale (4px base), shadow depth system, border radius conventions, animation defaults (library, spring parameters, durations), interaction patterns (whileTap, whileHover values), and dark mode rules. Include a complete, ready-to-use CLAUDE.md design system template.
**Trigger phrases**: "design system", "design tokens", "CLAUDE.md design", "brand consistency", "style guide", "colors", "typography scale"

### 4. Prompting for Beautiful UI
**Priority**: High
**What to extract**: The research-first approach (brainstorm → specify → generate), visual description vocabulary for AI (premium, minimal, warm, alive, spatial), component prompt template structure (visual requirements → interaction states → animations → technical constraints), what details to specify upfront to avoid iteration (states, responsive behavior, animations, edge cases), and common prompting mistakes that produce generic or broken UI.
**Trigger phrases**: "create a component", "build a page", "make it beautiful", "design this", "UI for", "make it look like"

### 5. Tailwind CSS Advanced Patterns
**Priority**: Medium
**What to extract**: Tailwind patterns for premium aesthetics: gradient techniques (mesh, animated, text gradients), glassmorphism (backdrop-blur, transparency), shadow depth systems (layered shadows, colored shadows), animation utilities and plugins (tailwindcss-motion, tailwindcss-animate), dark mode implementation patterns, and responsive animation (breakpoint-specific motion). Focus on utility patterns that achieve high-end visual design without custom CSS.
**Trigger phrases**: "Tailwind", "gradient", "glassmorphism", "shadow", "dark mode", "responsive", "premium look"

### 6. React Native Animations (Reanimated + Gesture Handler)
**Priority**: Medium
**What to extract**: React Native Reanimated 3 patterns: useAnimatedStyle, withSpring/withTiming/withDecay, worklets, shared values. Gesture Handler patterns: GestureDetector, Pan/Tap/Pinch recognition, combining gestures with Reanimated. Mobile-specific interactions: pull-to-refresh customization, bottom sheet animations, shared element transitions, staggered list entries, haptic feedback integration. Performance: running on UI thread, avoiding JS thread bottlenecks.
**Trigger phrases**: "React Native animation", "Reanimated", "Gesture Handler", "mobile animation", "native feel", "bottom sheet", "gesture"

### 7. Figma-to-Code Workflow
**Priority**: Medium
**What to extract**: Setting up Figma MCP server for Claude Code access, extracting design tokens from Figma files, design-to-code conversion workflow (inspect → specify → generate → compare), maintaining design fidelity, icon library MCP servers (Icons8, Lucide, Iconify — which to install), and creating a feedback loop between design files and code output.
**Trigger phrases**: "Figma", "design to code", "extract from Figma", "match the design", "icon library", "design tokens from Figma"

### 8. Visual Polish Checklist
**Priority**: Lower
**What to extract**: A systematic checklist for visual quality: shadow and depth (layered shadows, elevation scale), gradient quality (mesh gradients, animated gradients), typography refinements (line height, letter spacing, font rendering), spacing rhythm (consistent scale, component padding), border treatments (subtle separators, corner consistency), dark mode correctness (contrast, hierarchy preservation), and loading states (skeleton screens, shimmer effects, optimistic UI). The skill should help Claude self-review its generated UI for polish gaps.
**Trigger phrases**: "polish this", "make it premium", "review the design", "visual quality", "refine the UI", "it looks generic"

## Extraction Guidance

- **Motion is the default**: When sources discuss multiple animation libraries, default to Motion (Framer Motion) for React web and Reanimated for React Native. Only recommend alternatives when they genuinely excel.
- **Copy-paste priority**: Every pattern should include actual code. A micro-interaction pattern without code is useless.
- **First-try quality**: The entire point is reducing iteration. Skills should front-load the details Claude needs to get it right the first time.
- **Accessibility built-in**: Every animation skill should include `prefers-reduced-motion` handling. Every component should include semantic HTML and ARIA labels. Don't make accessibility optional.
- **Performance awareness**: Flag which CSS properties are GPU-accelerated (transform, opacity) vs layout-triggering (width, height, top, left). Include performance budgets for animations.
- **Not just web**: Include React Native patterns alongside web patterns. My projects span both platforms.
- **Concrete over abstract**: "Spring with stiffness 300, damping 10" is useful. "Choose appropriate spring parameters" is not.

## Cross-Domain Notes

- **Animation Library** connects to Remotion Mastery (spring animations in video), Creative Projects (game UI), and Technical Stack (React patterns)
- **Micro-Interactions** connect to Creative Projects (game UI feedback) and Life Optimization (app interfaces)
- **Design System** connects to Core Features (CLAUDE.md patterns) and Advanced Techniques (configuration management)
- **Prompting for UI** connects to PM Workflows (stakeholder presentation design), Remotion Mastery (describing video visuals), and all domains that generate visual output
- **Tailwind Patterns** connect to Technical Stack (frontend development) and Creative Projects (game UI wrapper)
- **React Native Animations** connect to Creative Projects (16BitFit mobile app) and Technical Stack (React Native development)
- **Figma Workflow** connects to Core Features (MCP setup) and PM Workflows (design handoff)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include working code patterns with all imports, not pseudocode
- Cover both web (React) and mobile (React Native) where applicable
- Include specific numeric values (spring parameters, timing, spacing) — not vague descriptions
- Handle accessibility (reduced motion, ARIA, keyboard navigation) by default
- Be organized as a pattern library Claude can reference quickly, not a tutorial to read through

---

## PROMPT END
