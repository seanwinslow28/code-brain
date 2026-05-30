# Continuation Prompt — Build `vault-knowledge-mcp` (second MCP)

> Paste everything below the line into a fresh Claude Cowork session. Connect these folders first: **`code-brain`** (the vault + spec + fixture live here) and **`sw-mcp-intent-engineering`** (the skeleton + publish flow you're reusing). You'll create a new sibling repo for the MCP itself.

---

You are my build partner for shipping **`vault-knowledge-mcp`** — my **second** MCP server. (My first, `intent-engineering`, is already published; this one reuses its skeleton and publish flow but is a different shape: it wraps my vault's typed knowledge graph, not a skill.) Do **not** confuse the two — `sw-mcp-intent-engineering` is reference/skeleton only; the new code goes in a new repo.

## Working mindset

I'm a PM who digs for the "why" and the "how." Be a thinking partner, not an executor — challenge while we explore, amplify once we commit, keep it brief and factual, no trailing summaries. Before any multi-step work, set up a task list and ask clarifying questions via the question tool. When we're designing, put us in the multi-perspective (PM / Designer / Engineer) headspace — invoke `pm-product-discovery:brainstorm` if it helps. All user-facing prose (README, the 4Q EXPLANATION, the Loom script, the LinkedIn post) is calibrated through the `writing-voice-modes` skill — read it before writing copy. Dial: ~40% for the README/technical surfaces, higher for the LinkedIn post.

## Read these first, in order

1. `code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-knowledge-mcp-spec.md` — the full build spec (status: research-complete). This is the authority.
2. `code-brain/vault/20_projects/research/2026-05-18-vault-knowledge-mcp-research.md` — the deep-research pass that resolved the 10 open questions (see its Executive Summary for the verdicts). Two companion passes (`-chatgpt`, `-gemini`) sit alongside it.
3. `code-brain/examples/public_vault_fixture/` — the synthetic espresso fixture that becomes the public demo vault (README + `edges.json` + 10 concept notes).
4. `code-brain/vault/SCORECARD.md` and `code-brain/docs/VAULT_AS_AGENT_INFRASTRUCTURE.md` — the just-shipped scorecard/essay. This MCP is the *live, queryable* surface of the same `concept_edges` graph those docs score. Keep the narrative coherent with them (esp. the "find contradictions" demo story).
5. `code-brain/agents-sdk/lib/concept_edges.py` + `code-brain/vault/.vault-index.db` — the data the MCP reads (632 typed edges, six SQL-enforced relations, 15,582 chunks).
6. `code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md` § "Publish + registry flow — frozen reference" — the exact npm + MCP-registry publish mechanics to reuse.
7. `sw-mcp-intent-engineering/` — the TypeScript skeleton to scaffold from (same SDK pin, same publish flow, DNS-verified namespace + Ed25519 key already provisioned).
8. `code-brain/.claude/skills/writing-voice-modes/SKILL.md` — voice authority for all copy.

## Locked decisions (do NOT re-litigate — research already settled these)

- **Name:** `vault-knowledge-mcp`.
- **3 tools, hard cap:** `search_concepts(query, limit=5)`, `find_contradictions(scope='all'|'recent_30d')`, `get_article(slug)`. Do not add tools mid-build; defer extras to v0.2.
- **Stack:** TypeScript, Node 22, `@modelcontextprotocol/sdk` 1.29.0, **stdio transport, launched via `npx`**. No HTTP/SSE, no auth, no SaaS.
- **Embeddings:** **JS-native** (Transformers.js / ONNX Runtime) — *not* a Python sidecar. Zero-friction `npm install` for a recruiter is the entire reason.
- **State:** **read-only** against the existing `vault/.vault-index.db`. No second index, no write surface, no watch-loop.
- **Privacy boundary:** allowlist by **env-var + explicit absolute pathing** (prevents LLM directory traversal). Readable: only `vault/knowledge/{concepts,connections,qa}/`. Never `00_inbox/`, `health/`, `90_system/`, `prj-job-hunt-2026/`, `the-block/`, `operating-models/`, `60_archive/`. Scope is config-only — never a request parameter.
- **Demo vault:** ship a sanitized, public SQLite built from `examples/public_vault_fixture/` so a recruiter gets a zero-config test environment.
- **Empty-state honesty:** if the vault/db is empty, return clean status objects (`{results:[], status:'vault-empty', message:...}`). Never hallucinate or invent data.
- **License / publish:** MIT · npm `@swins/vault-knowledge-mcp` · MCP registry `com.seanwinslow/vault-knowledge` (reuse the frozen publish flow + existing key).
- **v0.2 (not v0):** a `VAULT_ROOT` env var so anyone can point it at their own vault.

## The one open decision — make this call at kickoff before scaffolding

The research's "outsized-impact" recommendation is renaming `find_contradictions` → `analyze_reasoning_edges` to signal a graph-traversal engine to enterprise eyes. **Counter-weight:** the scorecard, essay, and fixture README I just shipped all narrate the demo as *"find contradictions."* So it's enterprise-signal vs. cross-artifact narrative coherence. Present both, with a recommendation, and let me pick. (My current lean: keep `find_contradictions` — it's the story my published artifacts already set up and the sharper Loom moment.)

## Build sequence (4 phases — this maps to my queued tasks 11–14)

1. **Confirm naming + scaffold.** Make the tool-name call above. Create a new repo (sibling to `sw-mcp-intent-engineering`, e.g. `sw-mcp-vault-knowledge`) from the intent-engineering skeleton. Pin the SDK, set up stdio entry, `package.json` for `npx`.
2. **Implement the 3 tools, read-only over `.vault-index.db`.** `search_concepts` (JS-native embeddings), `find_contradictions` (SQL: `relation='contradicts' AND valid_until IS NULL`, scope filter on `created_at`), `get_article` (file read + wikilink resolution). Empty-state honesty on every path. Tests + MCP Inspector pass.
3. **Ship the public demo vault + wire the privacy boundary.** Build the sanitized SQLite from the espresso fixture; env-var/absolute-path allowlist; verify a malicious client can't escalate scope.
4. **README + 4Q EXPLANATION + Loom + publish.** README < 200 words with a copy-paste `claude_desktop_config.json` block; `EXPLANATION.md` that passes a < 90-second recruiter cold-read; 90-second Loom exercising all 3 tools; publish to npm + registry via the frozen flow; draft the LinkedIn post (I send it, you draft).

## Hard constraints

- **Read-only.** Zero write surface against the vault. Ever.
- **Rule #8 (vault git ownership):** the Obsidian-Git plugin is the sole committer of anything under `code-brain/vault/`. Never `git add/commit` a vault path directly. The new MCP repo is its *own* repo — commit there freely; only vault-side changes (e.g., flipping the spec's `status` frontmatter) are Obsidian-Git's job.
- **Don't touch the portfolio build mechanics** (`sw-ai-pm-portfolio`) — out of scope here.
- **Lock the 3-tool spec.** No new tools mid-build.
- **$0 cloud.** Local-first; my machine + existing Ollama. npm + registry are free; domain auth already paid/verified.
- Keep it inside a normal workday container; nothing here needs evening overflow.

## Success criteria (binary — from spec §8)

`@swins/vault-knowledge-mcp@0.1.0` on npm · `com.seanwinslow/vault-knowledge@0.1.0` on the MCP registry · `docs/EXPLANATION.md` passes the < 90-sec cold-read · README < 200 words with config block · all 3 tools return non-error against my live vault (MCP Inspector) · empty-state path returns clean status (tested against a blank db) · 90-sec Loom plays end-to-end · LinkedIn syndication post drafted · publish-flow parity with `intent-engineering` (no surprises).

Start by reading the spec + research Executive Summary, then walk me through the kickoff: confirm the tool-naming decision, then scaffold.
