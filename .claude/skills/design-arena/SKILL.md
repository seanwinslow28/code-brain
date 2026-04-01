---
name: design-arena
description: Orchestrate competitive UI/UX design exploration using Claude Code Agent Teams and Pencil.dev. Multiple agents create competing layout interpretations from the same design brief, you pick the best elements, then build out the final design. Use when exploring designs for a new project, comparing layout approaches, iterating on UI direction, or when you say "design arena", "explore designs", or "competing layouts".
---

# Design Arena

## Purpose

Deploy Claude Code Agent Teams to generate competing UI/UX design interpretations for any project. Watch agents design in real-time on Pencil.dev's canvas, evaluate the results, synthesize the best elements into a locked design direction, then build out the full UI. This is a fully interactive, human-in-the-loop workflow — you are present and steering throughout.

## When to Use

- Starting a new project and want to explore layout directions before committing
- Existing project feels stale and needs a fresh perspective on composition
- You have a locked design system (colors, type, spacing) but need to explore page layouts
- You want to see how the same brief produces different information hierarchies
- You want to visually compare 3-4 layout approaches side by side before writing production code

## Examples

**Example 1: New project with no design spec**
```
User: "I want to explore designs for my personal finance tracker. Use the design arena."
Claude: [Uses design-arena] Runs condensed design interview (5-8 questions),
generates constraint brief, proposes 4 agent creative briefs, deploys Agent Team
into Pencil.dev. User watches, steers, evaluates, synthesizes.
```

**Example 2: Existing project with design system**
```
User: "Run the design arena for my Agent Control Center — I have a design spec already."
Claude: [Uses design-arena] Scans project for design-system-spec.md and
tailwind.config.js, summarizes what it found, proposes agent briefs that
explore layout variations within the existing constraints.
```

**Example 3: Targeted exploration**
```
User: "Use the design arena but just for the homepage hero section."
Claude: [Uses design-arena] Scopes agents to a single component/section
rather than full pages. Faster cycle, tighter comparison.
```

## Prerequisites

Before running this workflow, verify these are available:

| Requirement | How to Check | Why |
|---|---|---|
| Agent Teams enabled | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json or env | Core execution mechanism |
| Pencil.dev installed | Pencil MCP appears in `/mcp` output | Visual design target |
| Project directory | `cd` into the project root | Agents need project context |

If Pencil MCP is not available, the skill falls back to **code-first mode** (Option B) where agents generate React + Tailwind pages directly instead of designing on the Pencil canvas.

## The Three-Act Pipeline

The workflow has three distinct phases with hard gates between them. Each phase has a different goal. Never skip ahead.

```
ACT 1: CREATIVE ARENA          ACT 2: SYNTHESIS WALL          ACT 3: BUILD-OUT
─────────────────────          ──────────────────────          ────────────────
Agent Teams compete            You evaluate + synthesize       Locked direction → code
on Pencil canvas               best elements into one          Agent Teams implement
                               design direction                full page set
Divergent → Options            Convergent → Decisions          Execution → Ship
```

### Act 1: Creative Arena

**Goal:** Generate 3-4 distinct layout interpretations of the same project brief.

**Step 1 — Context Assessment**
Scan the project directory for existing design context:
- `design-system-spec.md` or `design-system.md` → locked design tokens
- `tailwind.config.js` → existing color/font/spacing config
- `CLAUDE.md` → project-specific design rules
- `*.pen` files → existing Pencil designs
- Component files → existing UI patterns

If a design spec exists, summarize it and confirm with the user: *"I found your design system spec. Blue/orange palette, Inter + Sora typography, Linear-inspired dark mode. I'll use this as the constraint document for all agents. Confirm?"*

If no design spec exists, run the **Condensed Design Interview** (see below).

**Step 1.5 — Aesthetic DNA Assignment**

Each agent needs a unique visual identity — not just a different layout. Assign an **Aesthetic DNA profile** from `references/aesthetic-dna-library.md` to each agent. DNA profiles define 7 dimensions of visual identity:

| Dimension | What It Controls |
|-----------|-----------------|
| Design Movement | Overall visual philosophy (Editorial Swiss, Neobrutalist, etc.) |
| Typography | Specific fonts with weights — NON-NEGOTIABLE, agents must use their assigned fonts |
| Color Application | How shared palette tokens get applied (monochromatic vs gradient-heavy vs functional-only) |
| Texture & Materiality | Surface treatment (grain, glass, scanlines, dot-grid, or intentionally flat) |
| Motion Language | Easing, physics, entrance choreography, timing |
| Signature Interaction | One mandatory bespoke moment that makes someone screenshot the design |

**DNA selection rules:**
- No two agents in the same session share a DNA profile
- Pick profiles that are maximally different from each other (different font families, different texture approaches, different motion languages)
- Default to 2 natural pairings + 1-2 unexpected pairings for creative range
- If the user named reference sites in the interview, bias one profile toward that aesthetic and make the others deliberately different

Quick reference (full profiles in `references/aesthetic-dna-library.md`):

| DNA Profile | Feels Like | Key Differentiator |
|-------------|-----------|-------------------|
| Editorial Swiss | Magazine spread | Typography IS the design; extreme restraint |
| Neobrutalist | Zine / poster | Thick borders, offset shadows, raw energy |
| Glassmorphism Aurora | Premium fintech at 2am | Frosted glass, luminous borders, aurora orbs |
| Terminal Operator | Beautiful Bloomberg | All-monospace, CRT scanlines, ticker data |
| Minimal Luxury | Aesop product page | Extreme whitespace, whisper-quiet animation |
| Data Brutalism | Bloomberg meets FT | Numbers are oversized art, functional color |
| Kinetic Scroll | Apple product launch | Scroll IS the interaction, pinned sections |
| Bento Garden | Apple comparison page | Mixed-size card grid, 3D tilt hover |
| Retro Digital | Modern Game Boy | Pixel grid, stepped animation, limited palette |
| Dark Cinematic | Nolan title sequence | Film grain, clip-path reveals, spotlight hover |

**Step 2 — Creative Brief Configuration**
Propose 3-4 agent assignments, each combining a **layout brief** (from `references/creative-brief-library.md`) with an **Aesthetic DNA profile** (from `references/aesthetic-dna-library.md`). Present both together, e.g.:

> - **Agent A:** Dense Operator layout + Terminal Operator DNA
> - **Agent B:** Narrative Flow layout + Editorial Swiss DNA
> - **Agent C:** Split Cockpit layout + Dark Cinematic DNA
> - **Agent D:** Command Center layout + Glassmorphism Aurora DNA

Present assignments to the user for approval. The user may:
- Approve all assignments as-is
- Swap a DNA profile for a different one
- Swap a layout brief for a different one
- Request an unexpected pairing for creative tension
- Modify a brief or DNA's creative direction
- Add or remove agents (3-4 is the sweet spot)

**Step 3 — Agent Team Deployment**
Create the Agent Team. The lead agent (you) coordinates. Each creative agent receives a structured prompt built from their layout brief + Aesthetic DNA profile.

**Agent Prompt Template** (fill in per agent from their assignments):

~~~markdown
# Agent [X]: [Layout Brief Name] — [DNA Profile Name]

## Your Design Identity
You are designing with the **[DNA Profile Name]** aesthetic. This is your
visual worldview. Everything you create must feel like it belongs to this
movement. Read your full DNA profile in `references/aesthetic-dna-library.md`.

### Design Movement
[Movement description from DNA profile]

### Typography (NON-NEGOTIABLE — use these exact fonts)
- Headings: [Font] [Weight]
- Body: [Font] [Weight]
- Data/Mono: [Font] [Weight]

### Color Application (same palette, YOUR interpretation)
[Color application strategy from DNA profile — ratios, where primary
appears, neutral tinting approach]

### Texture & Materiality
[Texture approach from DNA profile — technique, opacity, blend mode]

### Motion Language
[Motion approach from DNA profile — easing, duration, stagger, physics]

### Signature Interaction (REQUIRED — this is your showpiece)
[Signature interaction from DNA profile — MUST be implemented, not just
described. This is the thing that makes someone screenshot your design.]

## Layout Brief
[Layout philosophy from creative-brief-library.md — structure, density,
information hierarchy approach]

## Banned Patterns (violating these = failed design)
- Inter/Roboto/Arial as your only font
- Purple/indigo gradients
- Cards nested inside cards with uniform padding
- Pure gray text (#666, #888) — use tinted neutrals
- Pure black (#000000) backgrounds — use near-black with tint
- shadow-lg on everything without elevation hierarchy
- "transition: all 0.3s ease" as the only animation
- Symmetric hero sections with even accent distribution
- Everything looking equally important (no hierarchy)
- Looking like the other agents' designs

## Anti-Convergence Self-Check
Before finalizing, verify:
1. Could someone tell your design apart from the others in under 2 seconds?
2. Is your signature interaction implemented and functional?
3. Are you using YOUR assigned fonts, not system defaults?
4. Is your texture/materiality approach visible in the output?
If any answer is "no," revise until all are "yes."

## Shared Constraints
- Project design tokens: [from spec or interview — palette, spacing scale]
- Tech stack: [React/Tailwind/etc.]
- Accessibility: WCAG AA, 44px touch targets, prefers-reduced-motion
- Performance: only animate transform and opacity, 60fps target
- Reference: `prompting-beautiful-ui` skill for techniques, `micro-interaction-patterns` for motion code
~~~

Each agent also receives:
- A unique design frame name in the `.pen` file (e.g., `arena-agent-a-terminal-operator`, `arena-agent-b-editorial-swiss`)
- The project's design constraint document (existing spec or interview output)

**Output target:**
- **Pencil mode (default):** Each agent designs on a separate frame in the Pencil canvas using the Pencil MCP tools. Designs are visible to you in real-time.
- **Code mode (fallback):** Each agent generates a standalone React + Tailwind page in a `/design-arena/` subdirectory. Run `npm run dev` to view.

**Step 4 — Live Steering**
While agents work, you can:
- Use `Shift+Down` to cycle between agents and watch their progress
- Message any agent directly: *"Agent B, try a sidebar instead of a top nav"*
- Let them communicate with each other to ensure differentiation
- Intervene if an agent is going off-track

Agents should be instructed to design the **highest-impact page first** (usually the main dashboard or homepage), not the entire app. One excellent page per agent is more useful than four mediocre pages.

### Act 2: Synthesis Wall

**Goal:** Evaluate all designs and synthesize the best elements into a single locked direction.

**Step 5 — Guided Evaluation**
Walk through each agent's design one by one. For each, ask:

- **What works?** Specific elements to keep (e.g., "Agent A's transaction table density")
- **What doesn't?** Specific elements to reject (e.g., "Agent C's header is too heavy")
- **What surprised you?** Unexpected approaches worth exploring further

Reference `creative-director` skill for structured critique and `visual-polish-checklist` for detail review.

For detailed evaluation criteria, see `references/evaluation-rubric.md`.

**Step 6 — Synthesis Document**
Compile the user's selections into a **Design Direction Document**:

```markdown
# [Project Name] — Design Direction
## Date: YYYY-MM-DD
## Locked Decisions
- Layout: [Selected approach, e.g., "Split cockpit from Agent D"]
- Navigation: [Selected pattern, e.g., "Collapsible sidebar from Agent A"]
- Card treatment: [Selected style]
- Information density: [Selected level]
- Key interaction patterns: [What needs to feel interactive]

## Elements Adopted (by source)
- From Agent A: [specific elements]
- From Agent B: [specific elements]
- From Agent C: [specific elements]

## Rejected Approaches
- [What was rejected and why — prevents revisiting dead ends]

## Open Questions
- [Anything still unresolved that needs Option B prototyping]
```

Save this document to the project directory as `design-direction.md`.

**Step 7 — Option B Gate**
Ask: *"Do you need to feel the interactions before locking this direction? Any animations, scroll behaviors, or state transitions that need a working prototype?"*

If yes → generate a React + Vite + Tailwind interactive prototype of the synthesized design. The user tests hover states, responsive behavior, motion patterns, and data rendering before finalizing.

If no → proceed to Act 3.

### Act 3: Build-Out

**Goal:** Implement the locked design direction across all pages/views.

**Step 8 — Build Plan**
Break the project into independent build units (pages, component groups, features). Each unit should be assignable to one agent without file conflicts.

**Step 9 — Build Team Deployment**
Deploy a new Agent Team (or repurpose the existing one). Build agents receive:
- The locked `design-direction.md`
- The design constraint document (spec or interview output)
- Instruction to reference `react-vite-tailwind` and `tailwind-advanced-patterns` for implementation
- Instruction to reference `animation-library-mastery` for motion (if GSAP/Lenis are in the stack)
- Their assigned build unit (specific pages/components)

Build agents produce **real, shippable code** — not prototypes.

**Step 10 — Design Review**
Run the 4 design team agents as read-only reviewers on the final output:
- **UI Reviewer** — layout, spacing, color, typography consistency
- **Accessibility Checker** — WCAG AA, contrast, keyboard nav
- **Design System Enforcer** — token compliance, naming conventions
- **Visual Polish Auditor** — animation quality, loading/error/empty states

Fix any issues flagged by reviewers before shipping.

## Condensed Design Interview

For projects without an existing design spec, run this 5-8 question interview to establish non-negotiable constraints before agents explore. This is NOT a full design system spec — it's the minimum needed to prevent creative chaos.

| # | Question | What It Locks |
|---|----------|---------------|
| 1 | What's the core purpose of this project? (one sentence) | Design priorities |
| 2 | Who's the audience? (you only, public, team) | Polish level and tone |
| 3 | Dark mode, light mode, or both? | Surface palette |
| 4 | Name 2-3 sites/apps whose visual feel you admire for this project | Aesthetic direction |
| 5 | Dense data or spacious editorial? | Information density |
| 6 | What tech stack? (React, Astro, vanilla, etc.) | Implementation constraints |
| 7 | Any colors, fonts, or visual elements that are non-negotiable? | Hard constraints |
| 8 | What should this absolutely NOT look like? | Anti-patterns |

Compile answers into a constraint brief. This becomes the shared context for all agents.

## Skill Cross-References

This skill orchestrates other skills — it does not duplicate their content.

| Phase | Skills Referenced | Role |
|---|---|---|
| Act 1 (DNA Assignment) | `prompting-beautiful-ui` | **Core dependency** — DNA profiles draw from its design movements, font pairings, texture techniques, and banned patterns list |
| Act 1 (Creative) | `prompting-beautiful-ui`, `micro-interaction-patterns` | Creative agents reference for implementation techniques |
| Act 2 (Evaluate) | `creative-director`, `visual-polish-checklist` | Lead agent (you + Claude) |
| Act 3 (Build) | `react-vite-tailwind`, `tailwind-advanced-patterns`, `animation-library-mastery` | Build agents |
| Act 3 (Review) | Design team agents (UI Reviewer, Accessibility, Enforcer, Polish) | Read-only reviewers |

If a referenced skill is not installed in the project, the workflow continues without it — the reference is a quality enhancement, not a hard dependency.

For the creative brief library (reusable agent personas by project type), see `references/creative-brief-library.md`.
For evaluation criteria and scoring, see `references/evaluation-rubric.md`.

## Success Criteria

- [ ] Context assessment completed before any agent deployment
- [ ] User approved all layout brief + Aesthetic DNA assignments before agents started
- [ ] Each agent used its assigned typography (not Inter/system defaults)
- [ ] Each agent's signature interaction is implemented and functional
- [ ] No two agents share the same Aesthetic DNA profile
- [ ] Banned patterns list was enforced (no AI slop indicators)
- [ ] Each agent produced a meaningfully different visual interpretation (not just layout variation)
- [ ] User evaluated every agent's output with specific keep/reject decisions
- [ ] A `design-direction.md` document was saved to the project directory
- [ ] Option B prototype was offered for interaction-heavy projects
- [ ] Build-out agents referenced the locked design direction, not their own creativity
- [ ] Design team reviewers ran on the final output before shipping

## Copy/Paste Ready

```
"Use the design arena for this project"
"Run design arena — I want to explore layouts"
"Explore designs for [project name]"
"I want to see competing layouts for my dashboard"
"Design arena — just the homepage hero section"
"Run the design arena in code mode (no Pencil)"
```
