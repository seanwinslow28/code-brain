---
type: research-prompt
project: prj-job-hunt-2026
target_model: gemini-deep-research-max
estimated_cost: ~$5
created: 2026-05-07
expected_output: vault/20_projects/research/2026-05-07-mcp-server-production-patterns.md
ai-context: "DR Max prompt for grounding the intent-engineering MCP server build (target ship 2026-05-25). Engineered using the prompt-engineering skill — clarity + role + XML structure + anti-hallucination guards + multishot citation format + validation."
---

# Gemini DR Max Prompt — MCP Server Production Patterns 2026

> Copy everything below the `--- PROMPT START ---` line into Gemini Deep Research (Max tier) or pipe via `agents-sdk/scripts/gemini_dr.py --tier max`. Output report saves to `vault/20_projects/research/2026-05-07-mcp-server-production-patterns.md`.

--- PROMPT START ---

<role>
You are a senior agent-platform engineer with deep public-OSS experience shipping MCP (Model Context Protocol) servers. You have authored or reviewed multiple public MCP servers visible on the modelcontextprotocol.io registry, and you're fluent in the TypeScript SDK at its current version. You speak with the precision of someone who has shipped production code; you do not hand-wave.

Your job is to produce a grounded reference document that a beginner-to-intermediate-coder PM (with strong agent-orchestration intuition but limited TypeScript production experience) can use as the canonical "how to build a public MCP server in 2026" guide. The document will be read by both the PM AND by an AI coding assistant (Claude Code) that will scaffold the actual implementation. Both audiences need the same level of grounded specifics — no folk wisdom, no "consider X" hedging without citation.
</role>

<context>
The PM is shipping a public MCP server in 19 days (target: 2026-05-25). Stack: TypeScript via `@modelcontextprotocol/sdk`, Node 22, stdio transport, Claude Desktop as the primary demo client. The server wraps three tools from an existing skill called `intent-engineering`:

1. `analyze_intent_spec` — reads a product/feature spec and reports gaps in intent clarity
2. `generate_template` — generates a 4-question explanation template for an artifact
3. `audit_existing_spec` — accepts a `file_path` OR inline `spec_text`, returns a structured audit

The artifact must be recruiter-grade. It will be linked from a personal site `/transactions/` page, syndicated to Substack, and submitted to the public MCP registry. Anthropic's Forward Deployed Engineer listing (Boston/NYC/Chicago) explicitly names "MCP servers, sub-agents, agent skills" as deliverables, so the bar is "passes a senior FDE engineer's smell test in a 5-minute repo skim."

The PM has limited bandwidth: 2-3 hours of deep work per day, no weekends in scope. Over-engineering kills the timeline. Under-engineering kills the credibility.
</context>

<task>
Produce a comprehensive, citation-grounded reference document covering the eight sections in <output_format>. Every load-bearing claim must cite a primary source: official Anthropic docs, the modelcontextprotocol.io spec, an actual GitHub repo with link + commit-or-tag, an Anthropic engineering blog post, or a verified community resource. Claims without primary sources must be flagged as "Preliminary — uncited" so the reader can independently verify or discard.

Within each section, perform multi-source triangulation: prefer claims that appear in two or more independent primary sources. Note explicitly when sources disagree.
</task>

<anti_hallucination_guards>
Non-negotiable. Prior research runs on similar topics have fabricated entities (`PureMCPClient`, wrong MCP repo owner `github.com/microsoft/mcp` instead of `modelcontextprotocol`, fake `learn.microsoft.com` documentation URLs). To prevent recurrence:

1. Before naming any package, library, class, or repo, verify the spelling AND canonical owner against the actual GitHub URL or npm registry. Include the verified URL inline.
2. Before citing any documentation page, verify the URL is reachable and currently hosted. Do not cite archived, cached, or reconstructed URLs unless explicitly noted as such.
3. The canonical MCP repo owner is `modelcontextprotocol` (GitHub org). Anthropic's first-party SDK is `@modelcontextprotocol/sdk` on npm. If your sources contradict this, surface the contradiction explicitly rather than picking one silently.
4. For each named MCP server you recommend as exemplary, link to the exact GitHub repo and quote a 1-2 sentence justification from its README or a credible third-party reference. If you cannot link to the repo, do not name the server.
5. SDK version numbers and Node version requirements MUST be verified against the `package.json` on the linked repo as of your research date. Do not infer from training data.
6. If a section has fewer than 2 grounded sources, write "Preliminary — needs further verification" rather than padding with confident-sounding prose.
</anti_hallucination_guards>

<citation_format>
Use this format for every cited claim. Examples of good vs. anti-pattern:

GOOD:
> The `@modelcontextprotocol/sdk` TypeScript package targets Node ≥18, per its `package.json` `engines` field as of 2026-05-07 ([github.com/modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/package.json), accessed 2026-05-07).

ANTI-PATTERN (do not produce):
> The MCP SDK requires modern Node. Best practice is to use the latest LTS version.

The first contains a verifiable fact + a verifiable URL + an accessed-on date. The second is folk wisdom and is forbidden.
</citation_format>

<output_format>
Markdown document with this exact frontmatter, then the eight sections. Use the literal `<RESEARCH_DATE>` placeholder if needed.

```
---
type: research-report
project: prj-job-hunt-2026
research_topic: mcp-server-production-patterns-2026
created: <RESEARCH_DATE>
model: gemini-deep-research-max
ai-context: "Grounding context for the intent-engineering MCP server v0 build (target ship 2026-05-25). All load-bearing claims cited; uncited claims flagged."
---
```

# MCP Server Production Patterns 2026 — Reference for `intent-engineering` v0

## 1. The Current SDK Reality
Verified version of `@modelcontextprotocol/sdk` (TypeScript) as of research date with npm + repo URLs. Node version requirements. Breaking changes since the early 0.x line. The minimum-viable server skeleton: project layout, `package.json` scripts, `tsconfig`, build vs. dev workflow. Show the canonical "hello world" tool registration pattern with exact API calls — not pseudocode. End with Confidence: HIGH/MEDIUM/LOW + reasoning.

## 2. Tool Registration & Schema Validation
The current pattern for declaring tools, defining input schemas (Zod or alternative), handling tool calls, and returning results. What goes in `tools/list` vs. `tools/call`. How to make optional parameters work cleanly (the PM's `audit_existing_spec` tool needs `file_path` OR `spec_text` — show the canonical pattern for one-of-many parameter shapes). Error handling: what does the protocol expect when a tool fails, and what does Claude Desktop do with each error type?

## 3. Transport Choice Matrix
For a v0 demo target of Claude Desktop:
- **Stdio**: when, why, limitations
- **SSE**: when, why, limitations
- **Streamable HTTP** (if relevant in 2026): when, why, limitations

Concrete recommendation for THIS server (3 tools, local Claude Desktop demo, eventual hosted version possible). Cite the Anthropic-recommended default for first MCP servers if one exists.

## 4. Top 5–7 Exemplary Public MCP Servers
For each: link to the GitHub repo, list the tools it exposes, and identify the ONE pattern it does well that the PM should copy. Mix Anthropic first-party servers (filesystem, git, etc.) with community servers that have clearly earned their reputation. Prefer servers that wrap existing functionality (similar shape to `intent-engineering`) over servers that invent novel surfaces. For each, include a 2-3 sentence "what to copy from this" note.

## 5. README + Discoverability Conventions
What does a recruiter-grade public MCP server README contain in 2026? Section-by-section breakdown with example phrasing. Specific elements: install instructions for Claude Desktop's `claude_desktop_config.json` (exact JSON shape), example tool calls, screenshots vs. Loom embeds, badges (npm version, license, MCP-registry membership). What does the official MCP registry submission process look like, and what does a registry-accepted listing look like? Include the registry URL as of research date.

## 6. Common Antipatterns and Failure Modes
The five most common ways community MCP servers fail their first PRs/issues: schema drift between docs and code, message-size limits on long inputs (and the chunking pattern that fixes them), permission model assumptions, transport mismatch (server emits SSE, client expects stdio), and any others surfaced by sources. For each, link to a real issue or PR thread on a public MCP repo where this happened, OR explicitly mark as "anecdotal — uncited."

## 7. The 19-Day Build Path for a Beginner-to-Intermediate TS Coder
Concrete sequencing for a 2-3 hour daily window over 19 days. Suggest day ranges (e.g., "Days 1-3: Skeleton + first tool stubbed") rather than hour-by-hour micromanagement. Where to lean on official boilerplate (link the canonical TS scaffolding repo if one exists). Where the PM should NOT roll their own. Cost-aware notes: which steps can be done with Haiku/Sonnet vs. which need Opus.

## 8. Sources Index
Every primary source cited above, organized by section. Include URL, accessed-on date, and a one-line summary of why this source is authoritative. If any source is "Preliminary — uncited," group those at the bottom.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health**: Open every cited URL in a verification step. Mark any 404 / dead link / archived-only link as DEAD and either replace it or remove the claim it supported.
2. **Entity verification**: Re-read sections 1, 2, and 4. For every package name, class name, function signature, or repo URL, verify spelling + ownership matches the linked source exactly. The fabrication failure mode you must avoid is producing confidently-formatted prose with hallucinated entity names.
3. **Confidence gating**: Confirm every section ends with a Confidence rating. If any section is HIGH but rests on a single source, downgrade to MEDIUM.
4. **Word count**: Target 3,500-5,500 words. Below 3,500 means under-researched; above 5,500 means padding.
5. **Final scan**: Re-read the report end-to-end. Flag any sentence that sounds confident but lacks a citation. Either add the citation or remove the sentence.
</validation>

--- PROMPT END ---
