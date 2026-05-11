---
type: build-prompt
project: prj-job-hunt-2026
artifact: sw-mcp-intent-engineering
created: 2026-05-07
purpose: Paste this into a fresh Claude Code session at the start of the 19-day build. Replaces the two earlier draft prompts in v0-scope-prompt.md.
ai-context: "Single-prompt operating contract for Claude Code. Phase 0 = read + plan (gated). Phase 1 = scaffold (gated). Phase 2-4 unlock per scope-lock §9. All identity values locked 2026-05-07."
---

# Claude Code Build Prompt — `sw-mcp-intent-engineering`

> **How to use this file.** Open Claude Code in the new repo directory after running `mkdir -p ~/Code/sw-mcp-intent-engineering && cd ~/Code/sw-mcp-intent-engineering`. Paste everything below the horizontal rule into the first message. Do NOT shorten it — the discipline gates are what keep the build on rails for 19 days.

---

You are implementing an MCP (Model Context Protocol) server called `sw-mcp-intent-engineering` for me (Sean). Target ship: **2026-05-25** (19 days from today). This is a recruiter-facing portfolio piece tied to an active job hunt. Quality matters more than speed. Scope is locked. Schedule changes require my explicit written approval.

## Phase 0 — Required Reading (Do This First, No Code)

Read all six files in this order. Use the `Read` tool with absolute paths. Do not skim. These files are the contract.

1. **The binding scope lock (READ FIRST):**
   `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/v0-scope-intent-engineering-mcp.md`
   This is the implementation contract. §2 is the pinned tech stack. §4–§6 are the three tool contracts. §7 is what's out of scope. §8 is the ship gate. §9 is your operating discipline. §10 is the locked identity (do not relitigate).

2. **The strategic context (read for the why):**
   `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`
   Task 3 maps to this build. Decision 1 closes when the scope-lock is committed to this repo. Tier-A truths in the Self-Review section are inviolate.

3. **Technical grounding — measured + citation-heavy:**
   `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/research/2026-05-07-chatgpt-mcp-server-production-patterns.md`
   The conservative read on SDK choice, transport, registry process, and antipatterns. Cite this when the two research docs disagree (which is rare).

4. **Technical grounding — prescriptive + paste-ready boilerplate:**
   `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/research/2026-05-07-mcp-server-production-patterns.md`
   Lean on this for skeleton speed. §1 has the McpServer + StdioServerTransport pattern. §7 is the 19-day calendar.

5. **Source of truth for tool logic:**
   `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/intent-engineering/SKILL.md`
   The validation checklist (40 items), the 5 fatal anti-patterns, the 4 retrofit levels, the 4 autonomy levels, and the 9-section template all live here. Tool implementations import these as constants. They do not paraphrase, summarize, or reinvent the skill's logic. If something in this skill conflicts with the scope-lock, ask me — do not silently choose.

6. **Source of truth for the YAML scaffold:**
   `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/intent-engineering/references/intent-spec-template.md`
   The blank template scaffold for `generate_intent_spec_scaffold` (Tool 2). The Level-1 MVR variant comes from the SKILL.md "Minimum Viable Retrofit (MVR) Guide" section.

## Phase 0 Output — One-Page Implementation Plan (NO CODE)

After reading, output an implementation plan covering each item below, citing the specific section of the specific file you're relying on for each decision. Where the two research docs disagree, prefer the stable v1 stance the ChatGPT doc takes (per scope-lock §2). Aim for one printed page — terse beats verbose.

1. **SDK + runtime:** `@modelcontextprotocol/sdk` version, Node version, module type, build command. Cite scope-lock §2.
2. **Transport choice + isolation:** Why Stdio for v0; how the transport layer is isolated in `src/index.ts` so a future Streamable HTTP swap touches only one file. Cite ChatGPT §3 and Gemini DR Max §3.
3. **Project layout:** Confirm the `src/intent/*` module structure from scope-lock §2. Note where each tool's logic lives, where the validation checklist constant lives, where the anti-pattern detectors live, where the templates live (TS string constants, not files).
4. **Tool 1 — `audit_intent_spec`:** Strategy for parsing both YAML-frontmatter form and Markdown-headed form (scope-lock §10.7). Strategy for the pagination implementation (start_index + max_length per scope-lock §4). How the 5 anti-pattern detectors are structured.
5. **Tool 2 — `generate_intent_spec_scaffold`:** Where the three template variants live (`blank`, `level-1-mvr`, `full-9-section`). How `objective_hint` is interpolated. How `autonomy_level` selects the matching Decision Authority block from the four patterns in SKILL.md "Autonomy Levels."
6. **Tool 3 — `assess_retrofit_level`:** The heuristic for choosing L1/L2/L3 grounded in the SKILL.md "Prioritization for 107 Skills" criteria (blast radius, failure frequency, autonomy level, complexity). What signals in the input text raise blast radius and complexity.
7. **Schema validation:** Zod usage pattern. The XOR refinement for `spec_text` vs `file_path`. Cite Gemini DR Max §2 and ChatGPT §2.
8. **Error handling model:** When errors are protocol-level (let the SDK reject) vs `isError: true` tool results. Why `console.log` is forbidden everywhere. Cite Gemini DR Max §2 and §6.
9. **Registry path:** Confirm the domain-verified namespace `com.seanwinslow/intent-engineering` via DNS TXT — NOT `io.github.seanwinslow28/intent-engineering`. The `mcp-publisher` flow per scope-lock §10.3 and ChatGPT §5.
10. **Days 1–3 task breakdown:** Concrete commits planned for Phase 1 per Gemini DR Max §7 Phase 1.

After the plan, **STOP** and wait for my approval. Do not write any code. Do not initialize the repo beyond what's already there. Do not run any commands.

When I review, I'll either approve, request changes, or ask clarifying questions. Only after I respond with explicit "approved — proceed with Phase 1" will you begin scaffolding.

## Phase 1 — Skeleton (only after I approve the plan)

Execute Gemini DR Max §7 Phase 1 (Days 1–3) at the locked identity values. Specifically:

- `npm init -y`, then edit `package.json`:
  - `"name": "@swinslow/intent-engineering-mcp"` (try this scope first; if `npm publish --dry-run` later shows it's taken, fall back to `@swins/intent-engineering-mcp` — but DO NOT publish in Phase 1)
  - `"version": "0.1.0"`
  - `"type": "module"`
  - `"engines": { "node": ">=20" }`
  - `"bin": { "intent-engineering-mcp": "./build/index.js" }`
  - `"scripts": { "build": "tsc && chmod 755 build/index.js", "start": "node build/index.js" }`
  - `"files": ["build"]`
  - `"license": "MIT"`
- Install pinned dependencies: `@modelcontextprotocol/sdk@1.29.0`, `zod@^3.25.0`, devDeps `typescript@^5.0.0`, `@types/node@^22.0.0`.
- Write `tsconfig.json` per scope-lock §2 (target ES2022, module Node16, strict, outDir `./build`, rootDir `./src`).
- Write `LICENSE` file (MIT, copyright Sean Winslow, year 2026).
- Write `.gitignore` (node_modules, build, *.log, .DS_Store).
- Create `src/index.ts` with: `McpServer` instantiation, ONE dummy `ping` tool registered via `registerTool`, `StdioServerTransport` connected. The dummy tool returns a static text response. Use `console.error` for any logging, never `console.log`.
- Verify `npm run build` succeeds and produces `build/index.js`.
- Output the absolute path to `build/index.js` and the `claude_desktop_config.json` snippet I should paste, along with macOS-specific instructions for restarting Claude Desktop.
- Commit with message `chore: scaffold project per docs/v0-scope.md §2 (Phase 1)`.

After Phase 1, **STOP**. I will paste the config into Claude Desktop, restart, and confirm the server appears with the `ping` tool. Once I confirm "Phase 1 verified," you may begin Phase 2.

## Phase 2 — Tool Implementation (only after I confirm Phase 1)

Execute Gemini DR Max §7 Phase 2 (Days 4–9). Implement all three tools:

- `src/intent/checklist.ts` — the 40-item validation checklist as a typed constant array, sourced verbatim from SKILL.md "Validation Checklist."
- `src/intent/anti-patterns.ts` — the 5 fatal anti-patterns as detector functions, sourced from SKILL.md "The 5 Fatal Anti-Patterns."
- `src/intent/templates/` — three TS string-constant templates (`blank.ts`, `level-1-mvr.ts`, `full-9-section.ts`) sourced from `references/intent-spec-template.md` and the SKILL.md MVR section.
- `src/intent/parser.ts` — the permissive parser that accepts both YAML-frontmatter and `## Heading` Markdown forms.
- `src/intent/audit.ts` — Tool 1 logic, calling `parser` then `checklist` + `anti-patterns`. Implement `start_index` + `max_length` pagination from day one.
- `src/intent/scaffold.ts` — Tool 2 logic. Interpolate `objective_hint`. Map `autonomy_level` to the matching Decision Authority block.
- `src/intent/retrofit.ts` — Tool 3 logic with the blast-radius / complexity / autonomy-level heuristic.
- `src/index.ts` — register all three tools using the locked input/output schemas from scope-lock §4–§6. `index.ts` does NOT contain tool logic — it is a thin protocol adapter.
- Each tool wraps execution in `try/catch` and returns `{ isError: true, content: [{ type: "text", text: "<short message>" }] }` on runtime failure (file not found, parse error, etc.). Schema-shape errors propagate as protocol errors.
- Commit each tool as a separate commit (`feat(audit): implement audit_intent_spec`, `feat(scaffold): implement generate_intent_spec_scaffold`, `feat(retrofit): implement assess_retrofit_level`).

After Phase 2, **STOP**. I will test each tool from Claude Desktop using the example inputs in scope-lock §4–§6. I'll either confirm "Phase 2 verified" or report bugs.

## Phase 3 — Hardening + README + Loom (only after I confirm Phase 2)

Execute Gemini DR Max §7 Phases 3 + 4 (Days 10–17). Specifically:

- MCP Inspector pass: `npx @modelcontextprotocol/inspector node ./build/index.js` — verify all three tools list with correct schemas. Fix any discrepancies.
- Stress-test pagination on `audit_intent_spec` with a 30k-character spec. Verify `next_chunk_token` round-trips correctly.
- Run `audit_intent_spec` against 5 real SKILL.md files from `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/`. Verify findings are non-trivial.
- Run `assess_retrofit_level` against 3 real SKILL.md files. Verify reasoning differentiates per file.
- Write `README.md` per scope-lock §8 done-criteria item 9. Open with the single-sentence pitch from scope-lock §1.
- Write `docs/EXPLANATION.md` (4Q comprehension artifact) — paste in the pre-drafted text from unified-roadmap §Task 3 Step 11, swap any `analyze_intent_spec` references to the actual locked tool names from scope-lock §4–§6.
- Add a CI grep check to `package.json` `scripts.prepublishOnly`: fail if any `console.log` exists in `src/`.
- Pause for me to record the 90-second Loom — you will not record it. After I record, I'll send you the Loom URL to embed in the README.

After Phase 3, **STOP**. I'll review the README and EXPLANATION.md, record the Loom, and confirm "Phase 3 verified."

## Phase 4 — 117-Skill Audit + Publish + Registry (only after I confirm Phase 3)

Execute the final ship sequence (Days 14–19 of Gemini DR Max §7 with the side-artifact addition):

- Generate `examples/superuser-pack-retrofit-assessment.csv` by running `assess_retrofit_level` against every SKILL.md under `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/`. Time-box this to 90 minutes of execution; if longer, note the bottleneck and ask me. Before commit, scan the CSV for any rows referencing residual Block IP and exclude them. Reference scope-lock §10.6.
- Write `server.json` registry manifest. Use namespace `com.seanwinslow/intent-engineering` (NOT `io.github.*`). Reference ChatGPT §5 and Gemini DR Max §5.
- I will add the DNS TXT record on seanwinslow.com — you will output the exact record content from `mcp-publisher init`'s output and pause for me to confirm the DNS propagation before continuing.
- `npm publish --access public` (I will execute the actual publish; you will prepare the package and run `npm publish --dry-run` first).
- `mcp-publisher publish` after I confirm DNS propagation.
- Run the 19-item ship-gate checklist from scope-lock §8. Output pass/fail for each.
- One LinkedIn post + one Substack post — DRAFT only. I send.

## Hard Rules (immovable for the entire 19 days)

- **Pinned versions:** `@modelcontextprotocol/sdk@1.29.0` exact, NOT `main`-branch v2 pre-alpha. Node `>=20`. Zod `^3.25.0`.
- **Transport:** `StdioServerTransport` only. No SSE. No Streamable HTTP.
- **Logging:** `console.error` for everything. `console.log` is a build failure (CI will catch it in Phase 3).
- **Architecture:** `src/index.ts` registers tools and connects transport. Tool LOGIC lives in `src/intent/*`. Do not put logic in `index.ts`. The MCP server is a thin protocol adapter over the skill's logic (MarkItDown pattern, Gemini DR Max §4).
- **Tools:** Three tools only — `audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`. No prompts. No resources. No annotations in v0.
- **Schema discipline:** Input/output schemas in scope-lock §4–§6 are exact. Any change requires my written approval in `CHANGELOG.md` BEFORE code is touched.
- **Source-of-truth discipline:** Validation checklist content, anti-pattern definitions, template strings, retrofit-level criteria all come from `.claude/skills/intent-engineering/`. Do not paraphrase or reinvent.
- **Phase gates:** Stop and wait for my confirmation between phases. Do not auto-advance.
- **Identity (locked, do not relitigate):**
  - Repo: `~/Code-Brain/sw-mcp-intent-engineering/`
  - GitHub: `github.com/seanwinslow28/sw-mcp-intent-engineering`
  - npm package: `@swinslow/intent-engineering-mcp` (fallback `@swins`)
  - Registry namespace: `com.seanwinslow/intent-engineering` (DNS TXT verified — NOT `io.github.*`)
  - License: MIT
  - Personal site: seanwinslow.com (deep-dive page at `/transactions/intent-engineering-mcp`)

## What to Do When You're Unsure

- If the scope-lock conflicts with one of the research docs: scope-lock wins. Note the conflict.
- If the two research docs conflict: ChatGPT's stable-v1 stance wins (per scope-lock §2 footnote).
- If the SKILL.md content suggests a different tool surface than the scope-lock: scope-lock wins. Note the conflict, ask me.
- If something is genuinely undefined: ask me. Do not invent.

## Begin Phase 0 Now

Read the six files. Output the implementation plan. Then stop and wait for me.
