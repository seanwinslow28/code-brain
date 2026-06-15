---
title: "How to make `MCP Server Pattern Repeatability` better"
type: expansion
parent: "[[mcp-server-pattern-repeatability]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-15
updated: 2026-06-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[mcp-server-pattern-repeatability]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “pattern language” mode, not just “repeatable pattern.”**  
   Anchor it on Christopher Alexander, Sara Ishikawa, and Murray Silverstein’s *A Pattern Language*.

   Current concept says Sean has built multiple MCPs, but it does not yet define the reusable grammar: context, forces, solution, resulting context. Add a sentence pattern like:

   > “An MCP server pattern is repeatable only when its domain primitive, tool boundary, client affordance, failure mode, and validation loop can be named independently of the first implementation.”

   This unlocks a **portfolio one-pager / MCP pattern catalog**: “Five MCP Server Shapes I Can Build,” with entries like skill-wrapper, graph-query, asset-pipeline controller, eval harness, and operating-model bridge. Right now the concept proves competence; Alexander-style pattern language would prove transferability.

2. **Add “boundary object” mode for why MCP matters organizationally.**  
   Anchor it on Susan Leigh Star and James R. Griesemer’s paper *Institutional Ecology, ‘Translations’ and Boundary Objects*.

   The missing facet is that MCP servers are not only technical wrappers. They are coordination artifacts between humans, agents, tools, and organizations. `intent-engineering` and `vault-knowledge-mcp` are boundary objects: rigid enough for machines to call, flexible enough for PMs, engineers, and recruiters to understand.

   Add this claim:

   > “A good MCP server turns private context into a boundary object: a shared interface where humans negotiate meaning and agents execute constrained action.”

   This unlocks a **Substack essay / interview narrative** where Sean stops sounding like “I built agent tools” and starts sounding like “I know how to make agent systems legible across teams.” That is stronger for AI-PM and senior-PM roles than a purely technical MCP demo.

3. **Add “anti-repeatability” via Brooks’s accidental vs essential complexity.**  
   Anchor it on Fred Brooks’s essay *No Silver Bullet: Essence and Accidents of Software Engineering*.

   The concept currently risks overclaiming: “I can make many MCP servers” can sound like every domain just needs a wrapper. Brooks gives Sean the contradiction he needs. Some repeatability is accidental: transport, schema, auth, tool registration, client setup. Some is essential: deciding what the domain primitive actually is.

   Add this distinction:

   > “The repeatable part of MCP is the serving shape; the non-repeatable part is discovering the irreducible domain object worth serving.”

   This unlocks an **agent spec / build runbook** with a preflight decision gate: “Is this MCP wrapping a real domain primitive, or just exposing files/functions because MCP is available?” That would keep `vault-knowledge-mcp` from becoming a generic vault search server and force it toward a sharper artifact: typed-edge reasoning as the primitive.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
