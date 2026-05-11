---
title: "intent-engineering"
type: concept
status: active
domain: [agents-sdk, claude-mastery, life-systems]
tags: [intent-engineering, prompt-engineering, agent-design, ai-pm]
created: 2026-05-11
last-updated: 2026-05-11
source-skill: ".claude/skills/intent-engineering/SKILL.md"
ai-context: "Vault hub for the intent-engineering concept. Sits between prompt-engineering (what you write) and context-engineering (what's available) — intent is the structured specification of WHAT the agent should accomplish and under WHAT constraints. Sean's job-hunt 2026 sprint targets AI PM roles where intent-engineering is a core competency."
---

# intent-engineering

**Intent-engineering** is the discipline of writing structured intent specifications for AI agents and skills — capturing not just the prompt but the *boundaries, success criteria, and decision rules* the agent must operate inside. It sits one layer above prompt engineering and one layer above context engineering: prompt is *what you write*, context is *what's available*, intent is *what should happen and under what constraints*.

## Why this hub exists

Multiple research notes and one Sean-authored framework note in the vault reference `[[intent-engineering]]` as a concept. This file is the canonical wiki target so those links resolve and the synthesizer can cluster all intent-engineering material together during the nightly run.

## Source skill

The Claude Code skill that operationalizes this concept lives at [`.claude/skills/intent-engineering/SKILL.md`](../../.claude/skills/intent-engineering/SKILL.md). The skill covers:
- Designing intent specs for new agents and skills
- Reviewing existing agents/skills against intent-engineering standards
- Retrofitting legacy prompts into proper intent specs
- Converting unstructured behavior descriptions into testable success criteria

## Related references

All notes in [`vault/40_knowledge/references/intent-engineering/`](../references/intent-engineering/) inbound-link to this hub. Notable entries:

- `ref-intent-engineering-overview.md` — high-level definition + scope
- `ref-intent-engineering-origin-and-lineage.md` — where the term came from
- `ref-intent-engineering-landscape-survey-2026.md` — practitioner survey
- `ref-intent-engineering-claude-code-implementation.md` — how it maps to Claude Code skills + agents
- `ref-intent-engineering-skill-design-guide.md` — applied to skill authoring
- `ref-intent-engineering-frameworks-technical-reference.md` — formal frameworks
- `ref-intent-engineering-autonomous-agent-research.md` — agent-specific applications
- `ref-ai-agent-engineering-stack-prompt-context-intent.md` — the prompt/context/intent stack
- `ref-personal-agentic-intent-engineering.md` — Sean's personal framework
- `ref-nate-klarna-intent-engineering.md` — Nate Jones's writeup on Klarna's use of intent-engineering

## Related concepts

- **Prompt engineering** — the surface layer (what you type into the model).
- **Context engineering** — what the model has access to during the call (RAG, memory, tools).
- **Agent design** — the broader practice that intent-engineering serves.

## Open threads

- Does Sean's MCP scaffolding project (Track-C in the job-hunt plan) need a formal intent spec before code? — yes, per [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md`](../../20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md).
- How does the intent-engineering skill compose with the verification-before-completion and brainstorming skills? — open question.
