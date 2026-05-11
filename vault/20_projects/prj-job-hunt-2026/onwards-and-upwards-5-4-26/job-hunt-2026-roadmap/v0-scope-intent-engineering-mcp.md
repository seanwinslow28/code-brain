---
type: scope-lock
project: prj-job-hunt-2026
artifact: sw-mcp-intent-engineering
target_ship_date: 2026-05-25
created: 2026-05-07
sean_approved: 2026-05-07
status: ready-for-commit-to-new-repo
synthesis_sources:
  - vault/20_projects/research/2026-05-07-chatgpt-mcp-server-production-patterns.md
  - vault/20_projects/research/2026-05-07-mcp-server-production-patterns.md
  - .claude/skills/intent-engineering/SKILL.md
  - .claude/skills/intent-engineering/references/intent-spec-template.md
identity_locked:
  repo_name: sw-mcp-intent-engineering
  github_username: seanwinslow28
  npm_scope: "@swins"  # @swinslow was taken on npm; @swins registered as primary 2026-05-08
  npm_package: "@swins/intent-engineering-mcp"
  registry_namespace: com.seanwinslow/intent-engineering  # domain-verified via DNS TXT, NOT io.github.* form
  license: MIT
  personal_site: seanwinslow.com
  personal_site_repo: /Users/seanwinslow/Code-Brain/sw-portfolio
  canonical_deep_dive_url: https://seanwinslow.com/transactions/intent-engineering-mcp
  canonical_fallback: GitHub docs/EXPLANATION.md (per roadmap Decision 2 if site delays past 2026-05-20)
ai-context: "Scope lock for the intent-engineering MCP server v0. This document is binding — Claude Code must implement against this exactly. All 10 open questions closed 2026-05-07. Decision 1 of the unified roadmap closes when this is committed to the new repo as docs/v0-scope.md."
---

# v0 Scope — `sw-mcp-intent-engineering`

> **Purpose.** This document locks the scope of the `intent-engineering` MCP server v0 build for the 19-day window 2026-05-07 → 2026-05-25. It is binding. Claude Code reads it once at the start of the build and treats it as the contract. Changes to schemas, tool count, or technical foundation require Sean's explicit written approval in the repo's `CHANGELOG.md` before code is touched.
>
> **Status.** Draft. To be moved to `~/Code-Brain/sw-mcp-intent-engineering/docs/v0-scope.md` on repo creation. Decision 1 of the [unified roadmap](2026-05-06-unified-roadmap.md) closes when this file is committed to the new repo.
>
> **Path note (2026-05-07):** Roadmap originally referenced `~/Code/sw-mcp-intent-engineering/`. Corrected to `~/Code-Brain/sw-mcp-intent-engineering/` to match Sean's existing convention (sibling to `claude-code-superuser-pack` and `sw-portfolio` inside `Code-Brain/`).

---

## 1. The One-Sentence Pitch

`intent-engineering` is an MCP server that exposes three tools — `audit_intent_spec`, `generate_intent_spec_scaffold`, and `assess_retrofit_level` — letting any MCP-aware client (Claude Desktop, Cursor, Anti-Gravity) review, scaffold, and triage agent intent specs against a 9-section unified template synthesized from production-agent research.

That sentence is the README opener. Don't write a different one.

---

## 2. Technical Foundation (pinned — do not change)

Both research docs converge on these. Treat them as immovable for v0.

| Decision | Locked value | Source |
|---|---|---|
| SDK | `@modelcontextprotocol/sdk@1.29.0` (stable v1.x line) | ChatGPT §1, Gemini DR Max §1. **Not** the v2 pre-alpha on `main`. |
| Node | `>=20` LTS | Gemini DR Max §1 (v2 alpha targets ≥20; future-proof). v1.x floor is 18 but use 20. |
| Schema lib | `zod` `^3.25.0` (compatible with v3.25+ and v4) | ChatGPT §1, Gemini DR Max §1 |
| Module type | ESM (`"type": "module"`) | ChatGPT §1, Gemini DR Max §1 |
| Server class | `McpServer` wrapper (NOT low-level JSON-RPC handlers) | Gemini DR Max §1 explicitly forbids low-level handlers |
| Transport | `StdioServerTransport` only | Both researchers emphatic. No SSE (deprecated). No Streamable HTTP for v0. |
| Demo target | Claude Desktop | ChatGPT §3, Gemini DR Max §3 |
| Build | `tsc` → `build/index.js`, `chmod 755` on the entry, `bin` field in `package.json` | ChatGPT §1 quickstart pattern |
| Logging | `console.error` only. NEVER `console.log`. | Both researchers flag stdout corruption as the #1 bug. |
| Distribution | npm publish first, then `mcp-publisher` to register | ChatGPT §5, Gemini DR Max §5 |
| Registry namespace | `com.seanwinslow/intent-engineering` (domain-verified via DNS TXT on seanwinslow.com — NOT the `io.github.*` form, because Sean's GitHub handle is `seanwinslow28` and the domain-verified form is cleaner) | ChatGPT §5, Gemini DR Max §5 |
| npm package | `@swins/intent-engineering-mcp` (`@swinslow` was already taken on npm; `@swins` registered as primary 2026-05-08) | Sean confirmed 2026-05-08 |
| GitHub repo | `github.com/seanwinslow28/sw-mcp-intent-engineering` | Sean confirmed 2026-05-07 — no rename, registry namespace via domain instead |

**Project layout (locked):**

```
sw-mcp-intent-engineering/
├── src/
│   ├── index.ts                    # MCP server boot + tool registration only
│   └── intent/
│       ├── audit.ts                # audit_intent_spec logic
│       ├── scaffold.ts             # generate_intent_spec_scaffold logic
│       ├── retrofit.ts             # assess_retrofit_level logic
│       ├── checklist.ts            # the 40-item validation checklist (constant)
│       ├── anti-patterns.ts        # the 5 fatal anti-patterns (constants + detectors)
│       └── templates/              # YAML scaffolds (blank / level-1-mvr / full-9-section)
├── docs/
│   ├── v0-scope.md                 # this file
│   └── EXPLANATION.md              # 4Q comprehension artifact (Task 3 Step 11)
├── package.json
├── tsconfig.json
├── server.json                     # registry metadata
├── README.md
└── LICENSE
```

**Claude Code discipline rule:** `src/index.ts` is allowed to import from `src/intent/*` but MUST NOT contain tool logic. Tool logic lives in the `intent/` modules. `index.ts` is a thin protocol adapter (MarkItDown pattern, Gemini DR Max §4).

---

## 3. Source of Truth

The skill at [`.claude/skills/intent-engineering/SKILL.md`](../../../../.claude/skills/intent-engineering/SKILL.md) is the canonical source for:

- The 40-item validation checklist (sections under "Validation Checklist")
- The 5 fatal anti-patterns (section "The 5 Fatal Anti-Patterns")
- The 4 retrofit-assessment criteria (section "Prioritization for 107 Skills")
- The 4 autonomy levels (section "Autonomy Levels")
- The 9-section unified template (section "The Unified 9-Section Intent Spec Template")
- The blank YAML scaffold ([`references/intent-spec-template.md`](../../../../.claude/skills/intent-engineering/references/intent-spec-template.md))

Tool implementations import these as constants. They do not paraphrase, summarize, or reinvent them. If the skill changes, the tools change.

---

## 4. Tool 1 — `audit_intent_spec`

**Job:** Take an existing intent spec (text or file path) and return structured findings against the validation checklist + anti-pattern detection.

**Maps to:** Skill's "review" mode.

### Input schema (Zod)

```ts
import { z } from "zod";

export const AuditIntentSpecInputSchema = z.object({
  spec_text: z.string().min(50).max(50_000)
    .describe("The raw intent spec text. Provide this OR file_path, not both.")
    .optional(),
  file_path: z.string().min(1)
    .describe("Absolute path to a markdown or YAML intent spec file. Provide this OR spec_text, not both.")
    .optional(),
  start_index: z.number().int().min(0).default(0)
    .describe("Zero-based character offset for paginated input. Default 0.")
    .optional(),
  max_length: z.number().int().min(500).max(20_000).default(10_000)
    .describe("Max characters of input to process this call. Default 10000.")
    .optional(),
}).refine(
  ({ spec_text, file_path }) => Boolean(spec_text) !== Boolean(file_path),
  { message: "Provide exactly one of spec_text OR file_path." },
);
```

### Output schema (tool result `content`)

The MCP tool result `content` array returns a single `text` block containing JSON-stringified output of the following shape:

```ts
type AuditIntentSpecOutput = {
  validation_score: string;                          // e.g. "23/40"
  section_findings: Array<{
    section: "objective" | "user_goal" | "desired_outcomes" | "health_metrics"
           | "strategic_context" | "constraints" | "decision_authority"
           | "edge_cases" | "stop_rules_verification";
    status: "pass" | "warn" | "missing";
    notes: string;                                   // 1–2 sentences
  }>;
  anti_patterns_detected: Array<
    "klarna-intent-gap"
    | "prompt-based-hard-constraints"
    | "activity-vs-outcome-confusion"
    | "vibe-coded-edge-cases"
    | "missing-stop-rules"
  >;
  top_3_recommendations: string[];                   // ordered by impact
  next_chunk_token: string | null;                   // null when input fully consumed
};
```

### Pagination behavior

If the input exceeds `max_length` characters from `start_index`, process the chunk, set `next_chunk_token` to the byte offset of the next chunk start, and include a partial result. Subsequent calls with the same `spec_text` (or `file_path`) and `start_index = <previous next_chunk_token>` continue the audit. The score and anti-patterns are reported per-chunk; the LLM aggregates across calls. (This mirrors the official `fetch` server's `start_index` + `max_length` pattern — Gemini DR Max §4.)

### Example call

```json
{
  "name": "audit_intent_spec",
  "arguments": {
    "spec_text": "## Objective\nMake support tickets resolve faster.\n\n## Outcomes\n- Tickets close in <2h\n- CSAT stays high\n\n## Stop Rules\n(none)\n"
  }
}
```

### Example output

```json
{
  "validation_score": "8/40",
  "section_findings": [
    {"section": "objective", "status": "warn", "notes": "States the activity ('resolve faster') but no problem framing or trade-off guidance. Cannot resolve ambiguity."},
    {"section": "user_goal", "status": "missing", "notes": "No user-perspective job-to-be-done."},
    {"section": "desired_outcomes", "status": "warn", "notes": "Outcome 1 is an activity disguised as a state. CSAT outcome lacks a measurable threshold."},
    {"section": "health_metrics", "status": "missing", "notes": "No counter-metric to prevent gaming the close-time outcome. Classic Klarna-style intent gap."},
    {"section": "strategic_context", "status": "missing", "notes": "Not specified."},
    {"section": "constraints", "status": "missing", "notes": "No steering or hard constraints listed."},
    {"section": "decision_authority", "status": "missing", "notes": "No autonomy-level mapping."},
    {"section": "edge_cases", "status": "missing", "notes": "No fallback behavior for ambiguous tickets, API failure, etc."},
    {"section": "stop_rules_verification", "status": "missing", "notes": "Stop rules section exists but is empty. Risk of infinite loops in autonomous mode."}
  ],
  "anti_patterns_detected": ["klarna-intent-gap", "activity-vs-outcome-confusion", "missing-stop-rules"],
  "top_3_recommendations": [
    "Add a health metric protecting CSAT below the close-time outcome (e.g., 'CSAT must stay >= 4.2 weekly average; if trending below, deprioritize speed').",
    "Rewrite outcome 1 as a state: 'No support ticket older than 2 hours sits unresolved during business hours.'",
    "Add a Stop Rule: 'Halt and escalate if confidence in resolution path < 0.7 OR after 3 failed agent attempts on a single ticket.'"
  ],
  "next_chunk_token": null
}
```

### Implementation notes

- The validation checklist constant lives in `src/intent/checklist.ts`. Each of the 40 items is a `{ id, section, predicate }` triple. The `predicate` is a small TS function that returns `pass | warn | missing` for a given parsed spec.
- The anti-pattern detectors live in `src/intent/anti-patterns.ts`. Each is a function that returns boolean given the parsed spec.
- Parsing: accept both YAML frontmatter form (per the template) AND markdown-headed form (per existing skill domain examples). Use a permissive parser — if the spec doesn't have a `## Objective` heading, look for the first paragraph as a fallback objective.
- File reads (`file_path`): use `path.resolve` and validate the resolved path is readable. If the file does not exist or is not readable, return a tool result with `isError: true` and a short message ("File not found at ${path}. Pass spec_text directly or check the path.").

---

## 5. Tool 2 — `generate_intent_spec_scaffold`

**Job:** Return the appropriate intent-spec template (blank, Level-1 MVR, or full 9-section) with optional pre-filled hints.

**Maps to:** Skill's "write" mode.

### Input schema (Zod)

```ts
export const GenerateIntentSpecScaffoldInputSchema = z.object({
  kind: z.enum(["blank", "level-1-mvr", "full-9-section"])
    .default("full-9-section")
    .describe("Which scaffold to return. 'blank' = empty 9-section template; 'level-1-mvr' = 3-section minimum-viable retrofit; 'full-9-section' = full template with prompts.")
    .optional(),
  objective_hint: z.string().min(10).max(500)
    .describe("Optional one-sentence hint about what the agent should do. Pre-fills the objective field with a starter draft.")
    .optional(),
  autonomy_level: z.enum(["full-autonomous", "guarded-autonomous", "proposal-first", "human-required"])
    .describe("Optional autonomy level. Pre-fills the Decision Authority section with the matching architecture pattern.")
    .optional(),
  agent_name: z.string().min(1).max(100)
    .describe("Optional agent/skill name. Used in the YAML header.")
    .optional(),
});
```

### Output schema (tool result `content`)

```ts
type GenerateIntentSpecScaffoldOutput = {
  template_yaml: string;            // the scaffold, ready to paste
  kind: "blank" | "level-1-mvr" | "full-9-section";
  next_steps: string[];             // 3–5 short actions ordered by importance
};
```

### Example call

```json
{
  "name": "generate_intent_spec_scaffold",
  "arguments": {
    "kind": "level-1-mvr",
    "objective_hint": "Categorize incoming support tickets by product area",
    "autonomy_level": "guarded-autonomous",
    "agent_name": "support-ticket-classifier"
  }
}
```

### Example output

```json
{
  "template_yaml": "# ==========================================\n# INTENT SPEC (Level 1 MVR): support-ticket-classifier\n# ==========================================\n# Date: 2026-05-12\n# Autonomy: guarded-autonomous\n\nobjective: >\n  Categorize incoming support tickets by product area, so [WHO] can [WHY IT MATTERS].\n  When facing trade-offs, prioritize [PRIMARY VALUE] over [SECONDARY VALUE].\n\ndesired_outcomes:\n  - \"[Observable state change 1 — what exists after the agent runs]\"\n  - \"[Observable state change 2]\"\n\nstop_rules:\n  halt_when:\n    - \"[Critical condition] → [halt | alert | rollback]\"\n  escalate_when:\n    - \"Confidence below [THRESHOLD]\"\n    - \"[N] consecutive failures\"\n  complete_when:\n    - \"[Completion criteria]\"\n\n# Note: Level 1 MVR captures 80% of intent value in 30 minutes.\n# Upgrade to Level 2 (add health_metrics, constraints, decision_authority, edge_cases)\n# when this skill begins running autonomously or its blast radius increases.\n",
  "kind": "level-1-mvr",
  "next_steps": [
    "Fill in the [WHO] and [WHY IT MATTERS] placeholders in the objective.",
    "Replace each desired_outcomes placeholder with a state (not an activity). Test: 'After the agent runs, [STATE] exists.'",
    "Add a halt_when condition specific to ticket-classifier failure modes (e.g., 'product-taxonomy file missing → halt and create error note').",
    "Once the skill ships, run audit_intent_spec on it to score the Level 1 against the full 40-item checklist. Promote to Level 2 if blast radius grows."
  ]
}
```

### Implementation notes

- Templates live in `src/intent/templates/` as TS string constants, not as separate files. Reason: shipping a single `build/index.js` is simpler than dealing with file-system reads in `bin`-published packages.
- `objective_hint` is interpolated into the objective field as the *start* of the sentence, not the whole thing — placeholders for trade-off guidance remain.
- `autonomy_level` selects which decision-authority block to include in `kind: full-9-section`. The mapping is:
  - `full-autonomous` → emphasizes `allowed_tools` whitelist, `acceptEdits` mode, autonomous loop guards
  - `guarded-autonomous` → adds `record_run()` logging, lower budget, rollback patterns
  - `proposal-first` → emphasizes interactive permission flow
  - `human-required` → emphasizes `disallowedTools: [Write, Edit, Bash]` deny-list
- `next_steps` is generated heuristically based on which placeholders remain. If `objective_hint` is provided, the first next-step shifts to "complete the trade-off clause" rather than "fill in the objective."

---

## 6. Tool 3 — `assess_retrofit_level`

**Job:** Look at an existing prompt or SKILL.md and recommend the right retrofit level (L1 / L2 / L3) with reasoning grounded in the skill's blast-radius / complexity / autonomy framework.

**Maps to:** Skill's "retrofit" mode.

### Input schema (Zod)

```ts
export const AssessRetrofitLevelInputSchema = z.object({
  skill_text: z.string().min(100).max(50_000)
    .describe("The existing prompt or SKILL.md text. Provide this OR file_path, not both.")
    .optional(),
  file_path: z.string().min(1)
    .describe("Absolute path to an existing SKILL.md or prompt file.")
    .optional(),
}).refine(
  ({ skill_text, file_path }) => Boolean(skill_text) !== Boolean(file_path),
  { message: "Provide exactly one of skill_text OR file_path." },
);
```

### Output schema (tool result `content`)

```ts
type AssessRetrofitLevelOutput = {
  current_state: string;                   // 1 sentence describing what's already there
  recommended_level: "L1-mvr" | "L2-structured" | "L3-full";
  reasoning: string;                       // 2–3 sentences citing blast radius + complexity
  estimated_time: string;                  // "30 min" | "2–4 hours" | "4–8 hours"
  blast_radius: "low" | "medium" | "high";
  complexity: "single-step" | "multi-step" | "autonomous-loop";
  autonomy_assumed: "full-autonomous" | "guarded-autonomous" | "proposal-first" | "human-required";
  next_steps: string[];                    // 3–5 ordered actions
};
```

### Example call

```json
{
  "name": "assess_retrofit_level",
  "arguments": {
    "file_path": "/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/format-on-edit/SKILL.md"
  }
}
```

### Example output

```json
{
  "current_state": "A single-purpose skill that runs prettier/eslint on edited files via a PostToolUse hook. Has clear instructions but no objective, outcomes, or stop rules.",
  "recommended_level": "L1-mvr",
  "reasoning": "Single-step skill, low blast radius (formatting changes are reversible via git), and the existing instructions are concise and correct. Level 1 adds objective + outcomes + stop rules in 30 minutes without disturbing the working hook logic. Level 2 would be over-engineering for a deterministic linter wrapper.",
  "estimated_time": "30 min",
  "blast_radius": "low",
  "complexity": "single-step",
  "autonomy_assumed": "full-autonomous",
  "next_steps": [
    "Add an Objective section: 'Keep the working tree consistently formatted, so diffs reflect logic changes only.'",
    "Add Desired Outcomes: 'Edited files pass prettier with no further changes; no formatting-only commits appear in git history.'",
    "Add Stop Rules: 'Halt if prettier/eslint binaries unavailable; halt if config file is missing.'",
    "After retrofit, run audit_intent_spec on the updated SKILL.md to confirm the L1 sections score pass.",
    "Defer L2 promotion until/unless this skill begins running autonomously across multiple repos."
  ]
}
```

### Implementation notes

- Heuristics live in `src/intent/retrofit.ts`. The function takes parsed skill content and emits an assessment based on:
  - Section count (which 9-section blocks are present?)
  - Presence of explicit "never X" / "halt if X" patterns (suggests existing safety thinking → may already be L1)
  - File-system / network / API invocation language (raises blast radius)
  - Loop / scheduled / autonomous keywords (raises complexity, suggests L3)
  - Word count and number of distinct directives (proxy for complexity)
- The `autonomy_assumed` field is the tool's best guess from the text; the LLM may override by passing `assume_autonomy_level` in a future v0.1. v0 does not accept that input.
- If the input contains the YAML frontmatter the skill template uses, parse it and use the present sections as direct evidence. If only markdown headings exist, use those.

---

## 7. Out of Scope for v0

Explicitly NOT in this build. If Claude Code suggests adding any of these, it has drifted.

| Item | Why not | When (maybe) |
|---|---|---|
| `compare_approaches` tool | Conversational, not tool-shaped | Never — belongs in chat |
| `apply_retrofit` (writes files) | High blast radius, violates v0's read-only posture | v0.2+, gated behind explicit user confirmation |
| MCP `prompts` primitive | Both researchers said skip for v0 | v0.2+, after tool surface stabilizes |
| MCP `resources` primitive | Same | v0.2+ |
| Streamable HTTP transport | v0 is local-only Claude Desktop demo | v0.3+, when hosting is needed |
| SSE transport | Deprecated per current MCP spec | Never |
| OAuth / authentication | Stdio is process-spawned; no network surface | v0.3+ with hosted transport |
| Tool annotations (`destructiveHint`, `idempotentHint`, etc.) | All v0 tools are read-only by design | v0.2+ if/when `apply_retrofit` lands |
| Custom transports | Not needed | Never |
| Test framework beyond a smoke script | Single-developer, 19-day window | v0.2+ |
| CI/CD beyond `tsc` build check | Same | v0.2+ |
| Multi-language support / i18n | English-only spec content | Never |
| Programmatic skill *generation* (LLM-call inside the tool) | Tools are deterministic; LLM calls happen client-side | Never inside this server — the calling LLM does that work |

---

## 8. Done Criteria for v0 (the 2026-05-25 ship gate)

The build is shippable when ALL of the following are true. Do not ship at 90%.

**Functional:**
1. `npm install && npm run build` succeeds on a clean clone with Node 20+.
2. Adding the server to `~/Library/Application Support/Claude/claude_desktop_config.json` with absolute path + restarting Claude Desktop shows the server connected and `intent-engineering` in the tool list.
3. Each of the three tools is callable from Claude Desktop and returns valid JSON in `tool_result.content[0].text` for at least one happy-path input.
4. `audit_intent_spec` correctly flags at least 3 of the 5 anti-patterns when given the worked support-ticket example from §4 above.
5. `generate_intent_spec_scaffold` returns the correct template variant for each of the 3 `kind` values.
6. `assess_retrofit_level` returns a non-default reasoning string for at least 3 distinct existing skill files from `.claude/skills/`.
7. XOR validation works: passing both `spec_text` and `file_path` to Tools 1 and 3 returns a clean error.
8. Pagination on `audit_intent_spec` works: a 30k-character input returns a partial result with `next_chunk_token != null`, and a follow-up call resumes correctly.

**Repository hygiene:**
9. README opens with the single-sentence pitch from §1, contains a literal copy-paste-able `claude_desktop_config.json` block with absolute-path placeholder, lists all three tools with one-line contracts, and includes one screenshot of the server connected in Claude Desktop.
10. `docs/EXPLANATION.md` exists with the 4Q template (per [unified roadmap Task 3 Step 11](2026-05-06-unified-roadmap.md)).
11. License is MIT and committed.
12. `.gitignore` excludes `node_modules/`, `build/`, `*.log`.
13. No `console.log` calls anywhere in `src/`. (CI grep check — fail the build if any are found.)
14. Tool-result error path returns `isError: true` for all expected runtime failures (file not found, invalid YAML, etc.).

**Distribution:**
15. Package published to npm as `@<sean-scope>/intent-engineering-mcp` (or unscoped — open question §10) with `mcpName` set in `package.json`.
16. `server.json` written, `mcp-publisher login github`, `mcp-publisher publish` executed; the listing appears at `registry.modelcontextprotocol.io`.

**Demo:**
17. A 90-second Loom exists at the path Sean designates, showing: setup (one breath), tool 1 audit on a real spec (one breath), tool 2 scaffold generation (one breath), tool 3 retrofit assessment (one breath), close.
18. The Loom plays end-to-end without a re-shoot or post-edit.

**Public:**
19. One LinkedIn post tagging Anthropic + the MCP team, one Substack post syndicating the Loom + EXPLANATION.md.

---

## 9. Build Discipline (rules for Claude Code)

This is the prompt scaffold to give Claude Code at the start of the build:

> Implement the three tools defined in `docs/v0-scope.md` exactly as specified. The spec is binding.
>
> Required reading before writing any code:
> 1. `docs/v0-scope.md` (this file) — the contract.
> 2. `vault/20_projects/research/2026-05-07-chatgpt-mcp-server-production-patterns.md` — SDK + transport + antipatterns grounding.
> 3. `vault/20_projects/research/2026-05-07-mcp-server-production-patterns.md` — boilerplate + Zod + isError patterns.
> 4. `.claude/skills/intent-engineering/SKILL.md` — source of truth for the validation checklist, anti-patterns, retrofit criteria, and template content.
> 5. `.claude/skills/intent-engineering/references/intent-spec-template.md` — source of truth for the YAML scaffold structure.
>
> Hard rules:
> - Pin `@modelcontextprotocol/sdk@1.29.0`. Do not use the `main`-branch v2 pre-alpha syntax.
> - Use `StdioServerTransport`. Do not implement Streamable HTTP or SSE.
> - Use `console.error` for all logs. `console.log` is a build failure.
> - `src/index.ts` registers tools and connects the transport. Tool logic lives in `src/intent/*`. Do not put logic in `index.ts`.
> - Do not add tools, prompts, or resources beyond the three specified.
> - Do not change any input or output schema without my explicit written approval in the repo's `CHANGELOG.md`.
> - Tool implementations import the validation checklist, anti-pattern definitions, and template strings from local TS modules that mirror the skill's content. They do not paraphrase, summarize, or reinvent the skill's logic.
> - For runtime errors (file not found, invalid YAML, etc.), return `{ isError: true, content: [{ type: "text", text: "<short message>" }] }`. Do not throw uncaught exceptions.
> - For schema validation errors (wrong shape, both `spec_text` and `file_path`, etc.), let the protocol layer handle it.
>
> Build sequence (per Gemini DR Max §7):
> - Days 1–3: project skeleton + dummy tool, verify Claude Desktop sees it.
> - Days 4–9: implement all three tools with deterministic happy paths.
> - Days 10–13: schema hardening + MCP Inspector validation + pagination.
> - Days 14–19: README + Loom + npm publish + registry submit.
>
> After reading the required docs, output a one-page implementation plan citing specific sections you're relying on for each major decision. I will review the plan before any code is written.

That prompt is the discipline lock. Save it to `docs/CLAUDE-CODE-BRIEF.md` in the new repo for re-use across sessions.

---

## 10. Identity Decisions (CLOSED 2026-05-07)

All seven open questions resolved. Listed here as a permanent record.

1. **Repo name:** `sw-mcp-intent-engineering` ✓ (parallel to existing `sw-portfolio-animation-pipeline`, `sw-token-cost-calculator` brand pattern).
2. **npm package name:** `@swins/intent-engineering-mcp`. `@swinslow` was already owned on npm — `@swins` registered as the primary scope on 2026-05-08. ✓
3. **Registry namespace:** `com.seanwinslow/intent-engineering` via DNS TXT verification on seanwinslow.com — NOT `io.github.seanwinslow28/intent-engineering`. Reason: domain-verified namespaces avoid the trailing-`28` brand inconsistency without requiring a GitHub username rename mid-build. The DNS TXT record is added during Days 13–15 of the build (registry-prep window) using the token `mcp-publisher` outputs. ✓
4. **License:** MIT ✓.
5. **Personal site:**
   - Production URL: `seanwinslow.com` (currently old, replacement in flight)
   - Replacement portfolio repo: `/Users/seanwinslow/Code-Brain/sw-portfolio`
   - Canonical deep-dive page (target): `https://seanwinslow.com/transactions/intent-engineering-mcp`
   - **Schedule note:** finishing the new portfolio is now a parallel critical-path deliverable for the 2026-05-25 ship. ~60% of deep-work time → MCP server, ~40% → portfolio site. If the site is behind by 2026-05-20, fall back to GitHub `docs/EXPLANATION.md` as canonical (per roadmap Decision 2) and ship the site post-announce. The MCP server ship date does not slip for site polish. ✓
6. **117-skill retrofit CSV side artifact:** YES. During Days 14–15 (polish phase), run `assess_retrofit_level` against every SKILL.md in `.claude/skills/`. Save raw output to `examples/superuser-pack-retrofit-assessment.csv` in the new repo. **Pruning of unused skills happens AFTER 5/25 as a separate post-employment cleanup project — do NOT add pruning to the 19-day window.** The CSV alone is the demo artifact. Before commit, scan for any skills containing residual Block IP that survived Task 0's scrub; exclude those rows. ✓
7. **Markdown + YAML parsing in `audit_intent_spec`:** YES, support both. YAML frontmatter takes precedence when present; markdown headings (`## Objective`, `## Desired Outcomes`, etc.) are the permissive fallback. Required for Q6 to work against existing markdown SKILL.md files. ✓

---

## 11. Verification Path

After the build completes, run this checklist before the 5/25 announcement:

1. **Cold install on a clean machine** (or a fresh Node 20 docker container): `git clone`, `npm install`, `npm run build`, paste config into Claude Desktop, restart, verify all three tools list.
2. **Tool-by-tool happy path**: invoke each from Claude Desktop with the example inputs from §4, §5, §6. Outputs match the example outputs structurally.
3. **Tool-by-tool error path**: pass invalid inputs (both `spec_text` and `file_path`; non-existent file path; oversize input) to each tool. Errors are clean, not stack traces.
4. **README install steps**: have a fresh reader (or Claude Code in a fresh session) follow the README from cold. They should reach a working tool call in <5 minutes.
5. **Inspector pass**: `npx @modelcontextprotocol/inspector node ./build/index.js` connects, lists three tools, shows correct input schemas (Gemini DR Max §7, Days 10–11).
6. **stdout cleanliness**: run the server in a terminal and verify nothing prints except MCP protocol JSON. All logs go to stderr.
7. **Senior-FDE skim**: ask one technical contact (or self-impersonate as one) to read the repo for 5 minutes and identify any smell. Address the top 1–2 findings before announce.

If any of 1–7 fails, do not announce. Slip the announce, not the quality.

---

## 12. What This Document Doesn't Do

For honesty: this scope-lock does not specify the *content* of the validation checklist, anti-pattern detectors, or template strings. Those live in the skill and are imported as constants. If the skill changes mid-build, the tools change accordingly. This is by design — the MCP server is a thin adapter, not a fork.

It also does not specify the LLM-prompt pattern for the *Loom narration*, the *Substack syndication post*, or the *LinkedIn announcement*. Those are roadmap deliverables (Task 3 Steps 12–14, Task 6 §C/§D), not scope-lock concerns.

---

**Decision 1 of the unified roadmap closes when this file is committed to `~/Code-Brain/sw-mcp-intent-engineering/docs/v0-scope.md`. All identity questions in §10 answered 2026-05-07 — file is ready for commit on repo creation.**

Onwards.
