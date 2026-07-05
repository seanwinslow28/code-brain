# Continuation — intent-engineering MCP strengthening (2026-06-17)

Paste this whole file into a **fresh Cowork session with the `code-brain` folder open** (the
`sw-mcp-intent-engineering` repo is also mounted and readable from Cowork). This thread is the
**strategist / explainer / decision partner** for strengthening the intent-engineering MCP. It
helps Sean understand where the build stands, decide the open questions, and prepare clean
handoffs — explaining *what to do and why* at each step.

> **Companion thread:** the Substack posts live in a *separate* Cowork continuation
> (`CONTINUATION-2026-06-17-substack-posts.md`). Keep post work there. The one link between
> them: Post 3 ("Correct Was Never Defined," publishing Thu 6/18) is built around this MCP — but
> **none of this MCP work blocks Post 3.** Post 3 ships on the MCP as-is.

## The role split (important — read this first)

* **This Cowork thread = think, decide, explain, prepare.** Read the repo and the context
  files, explain the field report and the diff in plain terms, help Sean make the open
  decisions, brainstorm Workstream B, and **draft the precise handoff prompts/instructions for
  Claude Code.** Walk Sean through each step and the reasoning.
* **Claude Code (opened inside the `sw-mcp-intent-engineering` repo) = execute.** It writes the
  code, runs `npm run build` / `npm test`, and edits repo files.
* **Sean commits.** `sw-mcp-intent-engineering` is a normal public repo Sean commits himself.
* So: **do not make code commits to the MCP repo from this thread.** You may read everything in
  it, and you may write/iterate planning + brainstorm docs (in the repo's `docs/` or in
  code-brain) to hand to Claude Code. Code changes go through Claude Code.

Be a thinking partner, not an executor: honest, challenge the plan, brief and direct, no
trailing summaries. Use AskUserQuestion at real decision points.

## The whole idea (what we're doing and why)

This MCP is Sean's published proof of a thesis the whole "Raising Claude" series is built on:
**"define correct before you build" / "the audit is the eval."** The market sells generators
and bigger models; the missing layer is **structured intent**. The server makes that gap
auditable from inside the harness the agent already runs in. Positioning (from the opportunity
report): *"I build the judgment layer for AI agents — intent, proof, and control — for the
people who aren't backend engineers."*

There are **two workstreams**, both defined in the original brief
(`sw-mcp-intent-engineering/docs/2026-06-16-strengthening-brief.md` — read it first):

* **Workstream A — technical hardening** (the v0.2 "what would break" list). Small, concrete.
* **Workstream B — the Intent Card / brief-mode tools.** The real product growth move: re-skin
  the same three-tool shape from "dev PRD → coding agent" to "creative brief → any agent," so
  the MCP speaks to the creative/marketing audience the series targets. Ranked #1 "BUILD NEXT"
  in the opportunity report, but it's the **second** build in the series order (Advisor for
  Post 6 → **Intent Card** → On-Brand Gate), so there's no rush to implement.

## Where things stand (from the 2026-06-17 field report)

Claude Code ran the first pass against the brief. The uploaded field report is the record;
here's the state:

**Shipped (staged in the working tree, NOT yet committed):**
* **A1 — heading-vocabulary mapper.** Done, and cleaner than the brief's "~1-day" estimate: the
  parser already matched headings via case-insensitive regex and everything downstream operates
  on an abstract sections object, so A1 was a **conservative 14-row alias table in
  `src/intent/parser.ts`** (e.g. `## Purpose` / `## When to Use` → Objective; `## Success
  Criteria` → Desired Outcomes; `## Completion` → Stop Rules), appended **after** the canonical
  patterns so canonical spellings always win. Adds an **internal-only `sourceHeading` field** so
  the audit notes say *"(recognized from heading '## When to Use')"* — legibility, no
  output-schema change. **Deliberately leaves procedural headings unmapped** (`## How to Apply`,
  `## Instructions`, `## Usage`) — they're not intent equivalents, so they stay honest rather
  than crediting the wrong section.
* **A3 — pagination boundary test** (test-only): confirms the documented behavior when a section
  heading straddles a chunk boundary (shows `missing` in that chunk; pagination continues to
  aggregate).
* **Verification:** `npm test` → **28/28 green**; no `console.log` in `src/`; **dogfood
  re-confirmed at 23/25, zero anti-patterns** against the canonical SKILL.md; **README
  Limitations rewritten**; **CHANGELOG approval entry written.**

**Scoped, not built:**
* **A2 — schema-drift contract test.** Written up as a cheap `node:test` asserting the checklist
  count + IDs, but **deferred pending a source-of-truth decision** (generate-from-skill vs.
  snapshot). Sean's call.
* **Workstream B.** Fully scoped at `sw-mcp-intent-engineering/docs/2026-06-16-intent-card-scope.md`
  — no code.

**Housekeeping notes from the report:** nothing is committed (working tree staged for Sean's
review); `npm install` ran (the only `package-lock.json` change is npm correcting a stale
version field `0.1.0 → 0.1.1` to match `package.json`); the untracked
`docs/2026-06-16-strengthening-brief.md` was left as-is.

## The decisions Claude Code is waiting on (and what this thread should help Sean do)

Tackle these in order. For each, explain the tradeoff, get Sean's call, then (where code is
involved) draft the Claude Code handoff.

### 1. Review + commit Workstream A (the immediate, low-risk step)

* **Glance at the alias table** in `src/intent/parser.ts` (it's a 14-row data table, "yours to
  tune"). Help Sean sanity-check the equivalences against his actual skill library — e.g. is
  `## Requirements → Constraints` right? Is anything mapped that shouldn't be, or missing? This
  is a taste call on his own heading vocabulary; read a few of his real SKILL.md headings if
  useful.
* **Read the README "Limitations" rewrite and the CHANGELOG entry** with him; confirm they're
  honest and that the dogfood claim (23/25) still reads true.
* **Confirm the version bump** for the release that carries A1+A3. A1 changes audit *scores*
  (behavior), not tool schemas — decide patch vs. minor and that the CHANGELOG framing calls it
  an intended behavior change, not a stealth one. (The v0-scope §9 approval gate is satisfied by
  the written CHANGELOG entry, but Sean should explicitly approve.)
* Then Sean commits (and optionally publishes the new version to npm). This thread can draft the
  commit message + the npm-publish checklist; Sean runs them.

### 2. Decide A2 (schema-drift contract test) — cheap, do-or-defer

The open question is the **source of truth**: should the checklist/anti-pattern constants be
**generated from the canonical skill** at build time, or should a **snapshot test** assert the
count + IDs and fail CI on drift? Help Sean pick. If he wants it, draft the one-paragraph Claude
Code instruction (it's a small `node:test`). If not, leave it ticketed.

### 3. Brainstorm Workstream B — the Intent Card (the big one)

This is what Sean wanted to "brainstorm separately." Use this thread to think it through, then
hand a refined build brief to Claude Code. The scope doc
(`docs/2026-06-16-intent-card-scope.md`) already lays out the terrain — **read it in full** —
and frames the decisions:

* **Headline decision — tool count.** Brief-mode is the first thing that pushes on the published
  "more-than-4-tools-is-a-smell" stance. Three options:
  (a) add 3 tools (3→6); (b) a `mode: "spec" | "brief"` param on the existing 3; (c) a separate
  `creative-eval` server. **Claude Code recommends (b)** for storefront coherence — **with an
  honest caveat:** (b) is *partly cosmetic*, because a brief mode needs a **parallel
  brief-native checklist, anti-patterns, and templates regardless of how the tools are
  surfaced.** So the tool-count call is about public-surface UX, not internal reuse. Don't let
  the brainstorm mistake the plumbing decision for the hard part.
* **The actual hard part — the brief-native rubric.** The current rubric speaks agent-safety
  (Goodhart, blast-radius, autonomy tiers, infinite-loop stop rules). A marketer's brief has
  different failure modes (off-brand voice, vague audience, unmeasurable "success," no approval
  chain, no channel/format constraints). The scope doc has a first-sketch 9-section reskin table
  **to react to, not commit to.** **This rubric is the real deliverable** — the thing that
  decides whether it lands at "1,000 installs" or "16." Spend the brainstorm here.
* **The 5 open questions for Sean** (bottom of the scope doc) — these are the brainstorm inputs:
  1. **One product or two?** Would a creative who writes briefs ever also spec an agent? (This
     answer picks (b) vs (a)/(c) more than any technical factor.)
  2. **What's the canonical reference brief** we dogfood against, and who's the stand-in brand
     (Sean's own Substack brand? a sample studio)?
  3. **Does "correct" for a brief need brand assets** (a voice guide, a do/don't list) as input,
     or is it self-contained like the spec rubric? (If it needs brand context, that's a new
     input shape + possibly a new file-load path through `safe-fs.ts`.)
  4. **Anti-pattern translation:** which of the five current anti-patterns have brief analogues,
     and what net-new brand failure modes belong in the list?
  5. **Naming/positioning:** "Intent Card" (product name) vs. the `audit_brief` tool names — how
     do they relate in the post and the README?

The output of the brainstorm should be a **decided, sharpened build brief** (update the scope
doc or write a build plan), which then becomes Claude Code's spec when Sean is ready to build —
**after** the Advisor (Post 6's tool).

## Governance guardrails (these are real; honor them)

* **`docs/v0-scope.md` is binding.** §9: changes to schemas, tool count, or technical foundation
  require Sean's written approval in `CHANGELOG.md` **before** code is touched. So the workflow
  is always: propose → Sean approves in CHANGELOG → Claude Code builds.
* **The 3-tool ceiling is deliberate** (`docs/EXPLANATION.md`, "Why exactly three tools"). The B
  decision is exactly this ceiling — treat it as a real product decision, not a default.
* **Thin protocol adapter.** Logic lives in `src/intent/*` (or a sibling `src/brief/*`);
  `src/index.ts` stays plumbing.
* **The dogfood invariant is the credibility move.** The server must keep auditing its own
  canonical SKILL.md at ~23/25, zero anti-patterns, and the README claim must stay literally
  true. Brief-mode will need its **own** dogfood (a canonical reference brief that scores high).
* **Security posture (from 0.1.1) holds:** every disk read goes through `safe-fs.ts`
  (`loadFileSafely`); Zod input schemas stay `.strict()`; no `console.log` in `src/`. A `mode`
  enum or new tools = an input-schema/tool-count change = the CHANGELOG approval gate.
* **Identity (don't drift):** npm `@swins/intent-engineering-mcp`; registry
  `com.seanwinslow/intent-engineering` (DNS-verified); MIT.

## Context files to read

**In the MCP repo** (`sw-mcp-intent-engineering/`, mounted + readable from Cowork):
* `docs/2026-06-16-strengthening-brief.md` — the original brief (the whole idea + both
  workstreams + the embedded opportunity-report excerpts).
* `docs/2026-06-16-intent-card-scope.md` — Claude Code's Workstream B scope (read in full for
  the brainstorm).
* `docs/EXPLANATION.md` — the design rationale ("why three tools") + the "what would break" v0.2
  list (the source of A1/A2/A3) + the intent-over-instructions thesis.
* `docs/v0-scope.md` — the **binding** scope-lock (§2 pinned foundation, §9 approval gate).
* `README.md` — the public contract, the rewritten Limitations, the dogfood claim.
* `CHANGELOG.md` — the 0.1.1 baseline + the new A1/A3 approval entry.
* `src/intent/parser.ts` — the alias table (decision #1) + the heading-map mechanism.
* `src/intent/{checklist,anti-patterns,scaffold,retrofit}.ts` + `templates/*` — the rubric logic
  Workstream B re-skins.
* The uploaded field report: `intent-engineering-mcp-update-report-2026-06-17.md` (the record of
  what Claude Code just did).

**In code-brain** (the "why" + the series context):
* `vault/30_domains/creative-studio/substack-research/2026-06-09-opportunity-report-creative-agentic.md`
  — Part 1 (#1 Intent Card), Part 2A (the brief-mode extension), Part 3 (positioning).
* `vault/20_projects/substack-studio/README.md` +
  `03-correct-was-never-defined/post.md` — why the MCP is being strengthened now (Post 3).
* `vault/00_inbox/tickets.md` — the "build the 3 missing ships-with tools" item (Advisor →
  Intent Card → On-Brand Gate) is the standing record of the build order.

## Definition of done for a working session

* Sean understands the field-report state and has reviewed the staged A1/A3 changes.
* Each open decision either made (with the reasoning captured) or explicitly deferred with a
  ticket in `vault/00_inbox/tickets.md`.
* Where code is the next step, a precise Claude-Code handoff prompt drafted for Sean to paste
  into the repo session.
* The Workstream B brainstorm advances the scope doc toward a decided build brief (it does not
  need to finish in one session).
* A crisp recap: what's committed/shipped, what's decided, what's still open, and the single
  next action.

## What's NOT in scope here

* Post copy / the voice chain (that's the Substack thread).
* Making code commits to the MCP repo (Claude Code edits, Sean commits).
* Building Workstream B now — it's the second build, after the Advisor. This thread shapes the
  brief; it doesn't ship the Intent Card.

Open by orienting Sean on the field-report state, then ask which of the three decisions he wants
to take first (review+commit A / decide A2 / brainstorm B).
