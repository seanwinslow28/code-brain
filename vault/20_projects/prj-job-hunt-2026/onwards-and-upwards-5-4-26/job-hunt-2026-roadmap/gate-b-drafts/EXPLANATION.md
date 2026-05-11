# EXPLANATION.md

A 4Q comprehension artifact for the `intent-engineering` MCP server. The 4Q framework (Nate B. Jones) is the explanation artifact in the generative era — the equivalent of a commit message in traditional software, but optimized for "does this person understand what they shipped?" instead of "did the bytes change?".

---

## What is this?

An MCP server that exposes three tools — `audit_intent_spec`, `generate_intent_spec_scaffold`, and `assess_retrofit_level` — over the standard Model Context Protocol. Any MCP-aware client (Claude Desktop, Cursor, Anti-Gravity) can call them to review, scaffold, or triage agent intent specs against a 9-section unified template.

The template, the 25-item validation checklist, the 5 fatal anti-patterns, and the 4 autonomy levels all come from the `intent-engineering` skill in my personal Claude Code Superuser Pack. The MCP server doesn't reinvent any of that — it's a thin protocol adapter that lets the skill's logic reach any agent harness, not just the one that ships it.

---

## Why this approach?

**Why MCP, and not something else.** Three alternatives I considered and rejected:

- **A REST API.** Rejected because no agent harness reads OpenAPI specs natively at agent-call time. You'd write a per-harness client wrapper for Claude Desktop, another for Cursor, another for Anti-Gravity. MCP is the protocol every serious agent client now speaks; one server, every client.
- **A CLI.** Rejected because CLIs aren't tool-shaped from an agent's perspective. An agent can shell out, but it doesn't get structured input schemas, validation, or paginated output. The audit's `next_chunk_token` pattern would be ugly in a CLI; it's native in MCP.
- **A slash command inside one harness.** Rejected because it locks you to one client. Slash commands are great for personal workflows; they're a dead end for distribution.

**Why exactly three tools.** Each tool maps to one mode of the underlying skill — review, write, retrofit. Adding a fourth (`compare_approaches`, say) would either duplicate logic the model can already do in chat, or extend the surface before it's stable. The Gemini DR Max research report on MCP production patterns flagged "more than 4 tools" as a smell in v0 servers; three is intentional.

**Why Stdio transport.** Two reasons. First, v0 is a local-only Claude Desktop demo — there's no infrastructure to host. Second, Streamable HTTP and SSE both add deployment complexity (auth, transport-state lifecycle, network surface) that buys nothing for a personal-laptop use case. Stdio is the right primitive for "the agent client spawns my server as a subprocess." Both production-pattern research reports converged on Stdio for v0.

**Why TypeScript and `@modelcontextprotocol/sdk@1.29.0`.** TypeScript because the MCP TypeScript SDK has the deepest client coverage and the cleanest Zod schema integration. Version `1.29.0` because the v2 line is pre-alpha on the SDK's `main` branch — pinning to the stable v1.x line is the only defensible v0 choice. Treating SDK versioning as a live decision rather than a default is the kind of thing that bites people six months later.

**Why domain-verified registry namespace (`com.seanwinslow/intent-engineering`).** The MCP registry accepts two namespace forms: `io.github.<username>/<package>` or `<reversed-domain>/<package>` with DNS TXT verification. I went with the domain-verified form because (a) my GitHub handle ends in a number for legacy reasons, and the domain-verified namespace reads cleaner, and (b) DNS verification is a stronger trust signal than "this GitHub user controls this username." Worth doing once, even for a personal artifact.

---

## What would break?

Three real boundaries, observed during Phase 3 verification.

**1. Heading-vocabulary boundary.** The v0 audit expects `## Objective` and `## Desired Outcomes` as literal section headings to score per-section findings. When I tested the audit against five SKILL.md files from my personal library, four scored `1/25` — not because the skills are bad, but because they use different heading vocabularies (`## When to Use`, `## How to Apply`, etc.). This is a v0 design choice (the spec template is opinionated about structure) but a recruiter reading the README without context would clock it as a false negative. Named explicitly in the README "Limitations" section. The v0.2 fix is a heading-vocabulary mapper that recognizes equivalent sections under different labels — a 1-day add, but out of scope for the 19-day ship window.

**2. Schema drift between the skill and the tool descriptions.** The MCP tool descriptions and the validation checklist live in two places: as TS constants in `src/intent/*`, and as canonical markdown in the underlying skill. If the skill changes (a new anti-pattern lands, the checklist grows from 25 to 30), the TS constants don't auto-update. v0 has no versioning relationship between them. The right v0.2 fix is either a generated-from-skill build step or a contract test that fails CI when the skill and the constants diverge. For now, the discipline is: when the skill changes, update the constants in the same commit, log it in `CHANGELOG.md`. (We've already done this once — the validation count was corrected from 40 to 25 mid-build per the skill's actual contents.)

**3. Pagination boundary on `audit_intent_spec`.** The audit supports `start_index` + `max_length` pagination for long inputs, mirroring the official `fetch` MCP server's pattern. The 30k-character round-trip works cleanly (verified during Phase 3 Gate A). What I haven't stress-tested is what happens when a single section heading straddles a chunk boundary — the parser is forgiving enough that the worst case is a per-chunk section showing as `missing` and the LLM aggregating across calls — but it's a known edge case worth a test in v0.1.

A fourth boundary worth naming: clients that can't pass file paths (web-only chat surfaces, sandboxed environments) silently fall back to `spec_text`. That's by design — the XOR validation between `spec_text` and `file_path` makes the degradation explicit — but it means the same audit run in different harnesses can have different ergonomics. Tradeoff I'd take again.

---

## What did I learn?

Two things, in increasing order of how often they'll come up in interviews.

**The first is procedural.** MCP is essentially a contract for "I am a tool an agent harness can call without me writing a wrapper for each harness." Once that landed, the server became almost embarrassingly simple — `src/index.ts` registers three tools and connects an Stdio transport, and that's the entire protocol surface. The interesting code lives in `src/intent/*` (parser, checklist, anti-patterns, retrofit heuristics), which is just normal TypeScript with no protocol awareness. The OPTIONAL field pattern translated cleanly from the underlying skill: `file_path` and `spec_text` are both optional, with a XOR `.refine()` keeping them mutually exclusive. That kept the tools resilient to clients that can pass file paths and clients that can't.

**The second is conceptual.** I audited my own canonical `intent-engineering` SKILL.md with the very server it ships, and it scored `23/25` with zero anti-patterns detected. The two warnings were real — outcome measurability could be tighter, and one health-metric phrasing was activity-leaning where it should be state-leaning — but the dogfood result is the headline. The skill that defines what a good intent spec looks like is itself a (mostly) good intent spec.

The lesson isn't "I'm great at writing specs." The lesson is that **intent** is more durable than instructions. The skill was written months before the MCP server existed, against a template I refined while researching production-agent failures (Klarna's intent gap, the activity-vs-outcome confusion that surfaces across most of the SKILL.md files I've audited — 4 of the 5 skills I ran the audit against during Phase 3 hit `vibe-coded-edge-cases` and `missing-stop-rules`). When I built the server, I didn't need to retrofit the skill to make the tool work — the spec was already shaped right. That's the real argument for intent-engineering as a discipline: write the intent once, well, and the artifacts that consume it (tools, evaluators, runbooks) stay aligned without per-artifact rework.

The corollary, and the thing I'll be talking about most in interviews: when an agent fails in production, the post-mortem usually points at the model or the prompt. It almost never points at the intent — because nobody wrote the intent down. Klarna's high-profile support-agent rollback was a missing health-metric problem, not a missing-capability problem. Building a tool that surfaces those gaps before the agent ships is more useful than a smarter model. That's the bet.
