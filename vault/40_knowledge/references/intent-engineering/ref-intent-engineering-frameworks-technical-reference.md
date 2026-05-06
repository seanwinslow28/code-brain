---
title: "Intent Engineering Frameworks for AI Agents — A Technical Reference"
type: reference
status: processed
domain: claude-mastery
created: 2026-02-28
ai-context: "Side-by-side reference for the six leading intent engineering frameworks — Huryn's 7-part structure, Pathmode's IntentSpec, Action Schemas, the UW 5-level Autonomy framework, the Autonomous Preamble pattern, and the WhatIsAFramework 7-component mapping; includes a cross-framework comparison matrix and notes which dimensions each addresses (health metrics, stop conditions, validation, scope)."
tags:
  - reference
  - intent-engineering
  - source/pdf
  - frameworks
  - huryn
  - pathmode
related:
  - "[[intent-engineering]]"
source-pdf: "Intent-Engineering-Frameworks.pdf"
---

# Intent Engineering Frameworks for AI Agents — Technical Reference

Intent engineering is the emerging discipline of structuring objectives, constraints, and decision boundaries that govern AI agent behavior — going beyond prompt engineering to design the full information architecture an agent needs to operate reliably. **Core premise across all frameworks:** agents fail not because of capability gaps but because intent is underspecified.

This reference covers six frameworks and methodologies practitioners use to codify intent for autonomous systems.

## 1. Huryn's 7-Part Intent Structure

**Origin:** Paweł Huryn, "The Intent Engineering Framework for AI Agents," *The Product Compass* (Substack), January 12, 2026. Draws on OKR methodology (Christina Wodtke) and empowered team objectives (Marty Cagan).

**Core thesis:** Intent is "what determines how an agent acts when instructions run out." Context without intent is noise — an agent can have rich contextual information but still optimize the wrong thing if objectives, outcomes, and constraints are underspecified.

### The Seven Components

The first four apply to any delegation, human or AI:

1. **Objective (The Problem + Why)** — Aspirational and qualitative. Defines the problem and why it matters. Weak: "Handle customer support tickets." Strong: "Help customers resolve issues quickly so they can get back to work, without creating more frustration than they started with."
2. **Desired Outcomes (Observable States)** — Not activities. Observable state changes from the user/stakeholder perspective. Measurable or verifiable without relying on agent self-report; leading rather than lagging. 2–4 outcomes per objective.
3. **Health Metrics (Goodhart Prevention)** — Non-regression metrics that define what must not degrade. Without them, "resolve issues faster" leads the agent to rush and reduce quality. Steer the prompt layer — they inform how conservative the agent should be when making trade-offs. Distinct from hard guardrails which block actions entirely.
4. **Strategic Context (System Boundaries)** — The system the agent operates within. arXiv:2401.04729 demonstrated that supplying strategic context beyond raw task specifications significantly improves AI autonomy.

The next three extend the structure for agents specifically:

5. **Constraints (Steering vs. Hard Enforcement)** — Steering constraints live in the prompt layer ("prefer brevity"). Hard constraints are enforced architecturally in orchestration ("never access production database directly"). The distinction matters: prompt-layer constraints can be circumvented; architecture-enforced constraints cannot.
6. **Decision Types & Autonomy Boundaries** — Explicitly define which decisions the agent may take autonomously vs. which require escalation.
7. **Stop Rules (Halt, Escalate, Complete)** — When the agent should stop, escalate to a human, and how it knows it's done. Without explicit stop rules, agents loop indefinitely on unsolvable problems or declare completion prematurely.

## 2. The Pathmode IntentSpec Format

**Origin:** Pathmode (pathmode.io), with Lewis Hall identified as a key figure. Open standard published at intentspec.org with formal JSON Schema, GitHub Action for CI/CD validation, and integrations with major AI coding agents.

### The Five-Part Structure

A structured document committed alongside code as an `intent.md` file:

1. **Objective** — What is being built and why. States the problem, user segment, and rationale.
2. **User Goal** — What the user is trying to accomplish (job-to-be-done from the user's perspective). Anchors every decision to a user outcome and prevents scope creep.
3. **Outcomes** — Measurable success criteria verifiable programmatically or through testing.
4. **Edge Cases** — Boundary conditions, error states, scenarios the implementation must handle. Prevents naive happy-path-only assumptions.
5. **Verification** — Test cases, acceptance criteria, automated checks closing the feedback loop.

### Spec-Driven Development Model

IntentSpec positions itself as the antidote to "vibe coding" — prompting an AI conversationally and hoping the output is correct. Core argument: prompts are ephemeral and don't survive context switching, while an IntentSpec is a structured contract that lives in the repo and tells any agent what "Done" looks like before it writes code.

Workflow: write `intent.md` → point AI agent to it (via CLAUDE.md, .cursorrules, or MCP context) → validate in CI using a GitHub Action enforcing schema compliance on every PR.

```yaml
---
id: "INT-EXPORT-JSON-001"
objective: "Allow users to export filtered data to JSON"
outcomes:
  - "User clicks Export → JSON file downloads to device"
  - "Export contains only the currently filtered dataset"
  - "No PII fields are included in the output"
constraints:
  - "Must run client-side only (no server round-trip)"
  - "File size must not exceed 10MB"
edgeCases:
  - scenario: "Empty dataset"
    expected: "Show toast: 'Nothing to export' — no file created"
  - scenario: "10k+ rows"
    expected: "Stream to file, show progress indicator"
healthMetrics:
  - "Page load time must not increase"
  - "Existing CSV export must continue to work"
---
```

### IntentSpec vs. AGENTS.md

| Feature | AGENTS.md | IntentSpec |
|---------|-----------|------------|
| **Format** | Unstructured text | Markdown + YAML + JSON Schema |
| **Validation** | None (vibe check) | Automated (CI/CD enforceable) |
| **Goal** | Context injection | Application logic standard |
| **Testability** | Low | High (deterministic) |

## 3. Action Schemas

**What they are:** A formal specification describing the actions an intelligent agent can perform within a system. Establishes structured parameters for agent behavior including input requirements, execution processes, expected outcomes, and error handling.

### Five Core Components

- **Action Identity** — Unique identifiers, names, versions, taxonomical classifications
- **Input Parameters** — Defined data types, validation rules, required vs. optional fields
- **Execution Logic** — Step-by-step procedures for processing inputs and generating outputs
- **Output Specifications** — Expected return formats, data structures, success indicators
- **Error Handling** — Predefined responses to failure scenarios, retry mechanisms, fallback procedures

Most modern implementations use JSON-LD formatting for semantic understanding and interoperability, often integrating with OpenAPI specifications.

### Action Schemas vs. Tool Whitelists

A tool whitelist is binary access control — determines whether an agent *can* call a tool. An action schema goes further by defining *how* the tool should be called, *what inputs are valid*, *what outputs to expect*, and *what to do when things fail*. Security practitioners recommend allowlists for tools an AI agent can access (anything not on the list is off-limits by default), but the schema provides the semantic meaning and execution context that a simple list cannot.

### Claude Code's Permission System

| Tool Type | Example | Approval Required |
|-----------|---------|-------------------|
| Read-only | File reads, grep | No |
| Bash commands | Shell execution | Yes |
| File modification | Edit/write files | Yes |

Permissions can be set via `/permissions`, CLI flags (`--allowedTools`, `--disallowedTools`), or `settings.json`. Deny rules take precedence, then ask, then allow. Permission modes range from `default` (prompts on first use) to `bypassPermissions` (skips all prompts), with `dontAsk` mode auto-denying tools unless pre-approved — a pattern that enforces action schemas at the configuration level rather than the prompt level.

The `--disallowedTools` flag removes specific tools from the model's context entirely, which is functionally stronger than a deny rule — the agent doesn't even know the tool exists. Maps to the action schema concept of constraining the agent's action space at the architecture layer rather than relying on prompt-level instructions.

## 4. Autonomy Level Framework

**Origin:** Feng, McDonald, Zhang at the University of Washington (arXiv:2506.12469), June 2025. Published in the Knight First Amendment Institute's "AI and Democratic Freedoms" essay series.

**Core thesis:** Autonomy should be a deliberate design decision separate from an agent's capability and operational environment.

### The Five Levels

User-centered — each level is defined by the role the user takes:

| Level | User Role | Must-Have Controls | Agent Behavior | Example Systems |
|-------|-----------|-------------------|----------------|-----------------|
| **L1** | Operator | User-managed planning; invocation before actions | Requires explicit invocation; avoids preference-based decisions | ChatGPT Canvas, Microsoft Copilot |
| **L2** | Collaborator | Control transfer; shared progress representation | User and agent plan/delegate/execute together; user can take over anytime | OpenAI Operator |
| **L3** | Consultant | Rich feedback elicitation interfaces | Agent plans and executes most tasks; consults user for expertise and preferences | Gemini Deep Research, GitHub Copilot Agent |
| **L4** | Approver | Approval elicitation for consequential actions | Agent operates independently; seeks user only at failure states or high-risk moments | Devin, Manus |
| **L5** | Observer | Emergency off switch | Fully autonomous; user can only monitor via activity logs | Voyager |

### Key Design Implications

A *capable* agent (one that performs well on benchmarks) can still be designed to operate at low autonomy. Conversely, a *less capable* agent can operate at higher autonomy when tasks are well-scoped. This decoupling means autonomy is a design choice about user experience and risk tolerance, not just a reflection of model quality.

The authors propose **autonomy certificates** — third-party-issued digital documents prescribing the maximum autonomy level an agent can operate at, given its technical specifications and operational environment.

### Mapping to Huryn's Framework

The autonomy levels map directly to Huryn's "Decision Types & Autonomy Boundaries" component. An L1 agent has nearly all decisions requiring escalation; an L5 agent has nearly all decisions marked as autonomous. The stop rules in Huryn's framework correspond to the "must-have controls" at each autonomy level — particularly the emergency off-switch at L5 and the approval gates at L4.

## 5. The Autonomous Preamble Pattern

**What it is:** Practitioner pattern for framing system prompts when agents operate without human presence — in headless, background, or fully unattended execution modes. Not a single published framework but an emerging set of conventions across Claude Code's SDK, Augment Code's prompting guides, and the broader agentic AI community.

### The Interactive → Autonomous Shift

| Dimension | Interactive Mode | Autonomous Mode |
|-----------|-----------------|-----------------|
| Permission model | Ask before acting | Act, then verify |
| Planning | User-guided or collaborative | Self-directed with constraints |
| Error handling | Pause and ask user | Retry, adapt, or escalate to logs |
| Scope boundaries | Implicit (user corrects drift) | Explicit (must be codified) |
| Stop conditions | User says "done" | Programmatic completion criteria |
| Context refresh | User provides missing info | Agent must gather its own context |

### Key Components of an Autonomous Preamble

- **Identity and scope** — "You are an [AGENT ROLE] whose goal is to [HIGH-LEVEL OBJECTIVE]"
- **Available tools and resources** — Explicit enumeration of files, APIs, execution environments
- **Decision-making strategy** — How to handle ambiguity, which decisions to make autonomously, when to log rather than ask
- **Constraints and prohibitions** — What the agent must never do (especially important when no human is watching)
- **Completion criteria** — How the agent knows it's done — verification checks, test suites, output validation
- **Failure modes** — What to do when stuck — retry limits, alternative approaches, graceful degradation
- **Escalation protocol** — Even in autonomous mode, defining when to halt and signal for human review

### Claude Code's Implementation

Claude Code enables autonomous execution through `--dangerously-skip-permissions` (equivalent to `--permission-mode bypassPermissions`), which auto-approves all tool calls. The Claude Agent SDK supports custom system prompts via the `systemPrompt` parameter — either appending to Claude Code's built-in prompt or replacing it entirely.

Background execution is supported through the Task tool, which spawns subagent instances that work autonomously and return results to the main session. Importantly, subagents inherit permission modes — when bypass mode is enabled, all subagents also get full autonomous access.

The recommended pattern for safe autonomous execution is **containerized environments** where the agent cannot access host-level credentials, SSH keys, or browser cookies. This architectural constraint is more reliable than any prompt-level instruction.

## 6. The 7-Component Framework Mapping

**Origin:** WhatIsAFramework.com, February 2026. Connects intent engineering vocabulary to an existing "framework methodology" that uses seven structural components to define agent behavior. Argues intent engineering is the same underlying architecture that framework methodology has used since 2024, with different vocabulary.

### The Seven Components

1. **Role** and operating identity
2. **Objective hierarchy** — What the agent is optimizing for
3. **Constraints** that apply in the current context
4. **Decision-making logic** at ambiguous branch points
5. **Output standards** — Quality and format expectations
6. **State and context** the agent should maintain
7. **Edge case handling** — What happens at system boundaries

The mapping to Huryn's framework is direct: every component Huryn describes has a structural equivalent in this methodology. The implementation language differs but the underlying architecture does not.

**Practical significance:** Both approaches share the key insight that agents don't fail on capability — they fail on context. When an AI agent makes a mistake, it's rarely because it lacks ability; it's because structured context about objectives, constraints, and decision boundaries was missing.

## Cross-Framework Comparison

| Dimension | Huryn (7-Part) | IntentSpec (Pathmode) | Action Schemas | Autonomy Levels | Autonomous Preamble |
|-----------|---------------|----------------------|----------------|-----------------|--------------------|
| **Primary focus** | Agent behavior design | Code implementation specs | Tool/action control | User-agent interaction | Headless execution |
| **Audience** | Product managers, AI architects | Software engineers | Platform engineers | Agent designers, researchers | Practitioners deploying agents |
| **Format** | Structured documentation | YAML/Markdown in repo | JSON-LD / OpenAPI | Conceptual framework | System prompt patterns |
| **Validation** | Checklist-based | CI/CD enforceable | Schema validation | Autonomy certificates | Runtime behavior |
| **Scope** | End-to-end agent intent | Feature-level specs | Individual actions | System-level autonomy | Execution mode config |
| **Constraints** | Steering + hard enforcement | Constraints field in spec | Input validation + ACL | Controls per level | Prompt + architecture |
| **Health metrics** | Explicit component | healthMetrics field | Not addressed | Not addressed | Not addressed |
| **Stop conditions** | Explicit stop rules | Verification section | Error handling | Emergency off-switch (L5) | Completion criteria |

## How They Complement Each Other

These frameworks operate at different levels of abstraction and address different moments in the agent design lifecycle:

- **Huryn's 7-part** defines *what* the agent should pursue and *how it should reason about trade-offs* — the **strategic layer**.
- **IntentSpec** translates that intent into *feature-level implementation contracts* AI coding agents can execute against — the **tactical layer**.
- **Action schemas** define *what the agent is allowed to do* at the tool level — the **enforcement layer**.
- **Autonomy levels** determine *how much human involvement* the agent design should require — the **governance layer**.
- **Autonomous preamble** configures *how the agent behaves when no human is present* — the **runtime layer**.

A well-architected agent system uses all five: Huryn's structure to define strategic intent, IntentSpec to translate that into implementable specs, action schemas to constrain the agent's tool access, an autonomy level to calibrate human involvement, and autonomous preamble patterns when the agent runs headless.

## Important Caveat: The I-5 Framework

The "I-5 Framework" described as a 5-stage methodology (Intent → Interpretation → Information → Instruction → Implementation) does **not** appear as a widely published, attributable framework in the intent engineering literature. While AWS has published a "5-I Framework" for AI-powered software development (Investigate, Integrate, Interact, Iterate, Impact), this addresses AI integration into the SDLC rather than intent engineering for autonomous agents. Several 5-stage frameworks exist for AI maturity and implementation, but none match the specific "I-5" nomenclature and stage sequence described — may be an emerging or informally circulated framework not yet formally published.
