# Evaluation Rubric

> Structured criteria for evaluating competing designs in the Design Arena. Use during Act 2 (Synthesis Wall) to guide the user through consistent evaluation of each agent's output.

---

## Evaluation Framework

Evaluate each agent's design across five dimensions. Not every dimension matters equally for every project — the lead should identify the 2-3 dimensions most critical for this specific project before starting evaluation.

### 1. Information Hierarchy

Does the layout guide the eye to the most important content first?

| Signal | Strong | Weak |
|---|---|---|
| Primary action | Immediately obvious, clear focal point | Buried or competing with other elements |
| Visual weight | Most important elements are largest/boldest | Everything is the same size and weight |
| Reading flow | Natural scan pattern (F-pattern, Z-pattern, or intentional break) | Eye bounces randomly without a path |
| Progressive disclosure | Summary → detail is clear | Everything shown at once, no layers |

**Ask the user:** *"When you first looked at this design, what did your eye land on? Is that the right thing?"*

### 2. Composition & Layout

Does the spatial arrangement feel intentional and balanced?

| Signal | Strong | Weak |
|---|---|---|
| Grid discipline | Elements align to a consistent grid | Misaligned elements, inconsistent gutters |
| Whitespace | Purposeful breathing room between groups | Either cramped or aimlessly empty |
| Grouping | Related elements are visually grouped | Related items scattered, unrelated items clustered |
| Responsive intent | Layout has a clear strategy for narrower viewports | Only designed for one breakpoint |

**Ask the user:** *"Does this feel like everything is where it belongs? Or does something feel out of place?"*

### 3. Design System Compliance

Does the design respect the project's established constraints?

| Signal | Strong | Weak |
|---|---|---|
| Color usage | Correct tokens, correct 80/20 ratio (if specified) | Off-palette colors, accent overuse |
| Typography | Correct font stack, correct weight hierarchy | Wrong fonts, inconsistent sizes |
| Spacing | Multiples of base unit, consistent internal padding | Random spacing values, inconsistent padding |
| Component patterns | Matches established card/button/input specs | Reinvents components that already have specs |

**Note:** This dimension only applies when a design system spec exists. For projects starting from scratch, skip this and evaluate whether the agent's internal consistency is strong.

### 4. Distinctiveness

Does this design avoid generic AI output?

| Signal | Strong | Weak |
|---|---|---|
| Memorable element | At least one thing you'd remember tomorrow | Could be any SaaS dashboard |
| Layout personality | Structure itself communicates something about the product | Default grid with default cards |
| Intentional choices | Every element feels deliberately placed | Elements feel auto-generated |
| Differentiation | Clearly distinct from the other agents' designs | Too similar to another agent's approach |

**Ask the user:** *"If I showed you this and the other agents' designs tomorrow, would you remember which was which?"*

### 5. Interaction Potential

How well does this static layout support dynamic behavior?

| Signal | Strong | Weak |
|---|---|---|
| State awareness | Design accounts for loading, empty, error, populated | Only shows the populated happy-path |
| Motion opportunities | Natural places for transitions and micro-interactions | Static layout with no obvious animation hooks |
| Touch/click targets | Interactive elements are clearly tappable/clickable | Ambiguous what's interactive vs decorative |
| Feedback loops | Clear where status changes, confirmations, and celebrations would appear | No space for dynamic feedback |

**Ask the user:** *"Can you imagine using this? Where would you click first? What would happen?"*

---

## Evaluation Walkthrough Script

Use this script during Act 2 to guide the user through evaluation. Adjust the language to be conversational, not robotic.

### Per-Agent Review (repeat for each agent)

1. **First impression** (5 seconds): Show the design. Ask: *"What's your gut reaction? Like, dislike, or mixed?"*

2. **Focal point test**: Ask: *"What did your eye land on first? Is that the right priority?"*

3. **Keep list**: Ask: *"What specific elements do you want to keep from this one?"* Record exact elements (e.g., "the transaction table layout", "the sidebar icon treatment", "the metric cards at the top").

4. **Reject list**: Ask: *"What doesn't work?"* Record with brief reasoning (e.g., "header is too heavy — takes too much vertical space").

5. **Surprise check**: Ask: *"Did this agent do anything unexpected that you like?"* This often surfaces the best innovations.

### Cross-Agent Comparison

After reviewing all agents individually:

1. **Side-by-side**: If in Pencil, zoom out to see all frames at once. Ask: *"Looking at all of them together, which one feels closest to what you want?"*

2. **Cherry-pick**: Ask: *"If you could Frankenstein the perfect version from pieces of each, which pieces would you grab?"*

3. **Conflict resolution**: If two agents did the same thing differently (e.g., different navigation patterns), force a choice: *"Agent A uses a sidebar, Agent C uses a top bar. Which feels right for how you'll use this app?"*

4. **Open questions**: Ask: *"Is there anything you want to see that none of the agents tried?"* This may trigger a quick follow-up round with a targeted brief.

---

## Synthesis Document Template

After evaluation, compile decisions into this format and save as `design-direction.md` in the project root.

```markdown
# [Project Name] — Design Direction

**Date:** YYYY-MM-DD
**Arena Session:** [number of agents] agents, [Pencil/Code] mode
**Design Spec:** [filename if exists, or "Generated from arena interview"]

## Locked Layout Decisions

### Overall Structure
- **Layout pattern:** [e.g., "Split cockpit — sidebar left, scrollable content right"]
- **Navigation:** [e.g., "Collapsible sidebar, 240px expanded, 64px collapsed"]
- **Primary page:** [e.g., "Dashboard home with status grid"]
- **Information density:** [e.g., "Comfortable — between Agent A's density and Agent B's spacing"]

### Component Decisions
- **Cards:** [which agent's treatment, with specifics]
- **Tables:** [which agent's treatment, with specifics]
- **Charts:** [which agent's treatment, with specifics]
- **Navigation items:** [which agent's treatment, with specifics]
- **Status indicators:** [which agent's treatment, with specifics]

### Motion & Interaction
- **Page transitions:** [approach]
- **Hover states:** [approach]
- **Loading states:** [approach]
- **Celebration/feedback:** [approach, if applicable]

## Elements Adopted by Source

| Agent | Elements Kept | Why |
|---|---|---|
| Agent A ([brief name]) | [specific elements] | [reasoning] |
| Agent B ([brief name]) | [specific elements] | [reasoning] |
| Agent C ([brief name]) | [specific elements] | [reasoning] |
| Agent D ([brief name]) | [specific elements] | [reasoning] |

## Rejected Approaches

| Rejected Element | Source | Why |
|---|---|---|
| [element] | Agent [X] | [reasoning — prevents revisiting dead ends] |

## Open Questions for Prototyping

- [ ] [Any interaction patterns that need Option B testing]
- [ ] [Any responsive behaviors that need live testing]
- [ ] [Any motion/animation that needs to be felt, not just seen]

## Build-Out Page List

| Page/View | Priority | Notes |
|---|---|---|
| [page name] | P1 | [any specific direction] |
| [page name] | P2 | [any specific direction] |
```

---

## Scoring (Optional)

If the user wants a more structured comparison, score each agent's design on a 1-5 scale per dimension. This is optional — many users prefer the qualitative keep/reject approach.

| Dimension | Agent A | Agent B | Agent C | Agent D |
|---|---|---|---|---|
| Information Hierarchy | /5 | /5 | /5 | /5 |
| Composition & Layout | /5 | /5 | /5 | /5 |
| Design System Compliance | /5 | /5 | /5 | /5 |
| Distinctiveness | /5 | /5 | /5 | /5 |
| Interaction Potential | /5 | /5 | /5 | /5 |
| **Total** | /25 | /25 | /25 | /25 |

Scores are a starting point for discussion, not a final verdict. The user's gut feeling always overrides the numbers.
