---
type: spec
project: prj-job-hunt-2026
created: 2026-05-13
status: research-pending
artifact_target: 8th flagship portfolio artifact
ships: TBD pending deep research
linked_artifacts:
  - "[[2026-05-06-unified-roadmap]]"
  - "[[intent-engineering MCP server]]"
  - "[[concept_edges]]"
  - "[[knowledge_loop]]"
linked_research:
  - "[[2026-05-07-target-role-specs]]"
ai-context: "Build spec + deep-research prompt scaffolding for `vault-knowledge-mcp` — Sean's second MCP server. Designed to be ingested by Gemini DR-Max or a Claude deep-research run to validate the architecture, reference-implementation choices, and recruiter-resonance hypothesis before any code is written. Status remains `research-pending` until DR results land at `vault/20_projects/research/2026-05-XX-vault-knowledge-mcp-research.md`."
---

# `vault-knowledge-mcp` — Build Spec + Research Prompt

> **Status: research-pending.** No code is written until deep research returns with architecture + reference-implementation validation. This document IS the research input.

---

## 1. Executive Summary

`vault-knowledge-mcp` is a proposed second MCP server exposing Sean's existing vault knowledge graph (the [[concept_edges]] typed-reasoning-edge SQLite table + the [[knowledge_loop]] producer/consumer pipeline) as queryable tools any MCP-aware client (Claude Desktop, Cursor, Anti-Gravity) can call.

The first MCP — `intent-engineering` — wraps a *skill*. This second MCP wraps a *knowledge graph with typed edges over a 17-day production-grounded vault*. Different shapes of the same primitive. Shipping it is the highest-leverage proof that the MCP-server pattern is repeatable in Sean's hands, not a one-off.

Three tools (stdio transport, TypeScript SDK 1.29.0, Node 22), published to npm + MCP registry under the existing DNS-verified `com.seanwinslow/*` namespace. Reuses the publish flow frozen in the unified roadmap's "Publish + registry flow — frozen reference" subsection. Expected build time: 5–7 working days. Expected ship: 2026-06-04 (target — 10 days after the existing Track-C ship date), gated on this research returning a clean architecture.

The recruiter-resonance hypothesis: this artifact converts "Sean has knowledge graph experiments" from a static GitHub repo finding into a live, queryable demo that the recruiter / hiring manager can invoke from their own Claude Desktop in under 60 seconds.

---

## 2. Why This Is Necessary

Five reasons, each grounded against a specific source. The strength rating reflects the load-bearing weight of the source.

**Reason A — Pattern repeatability is the durable career signal. (STRONG)**
One MCP = could be a one-off. Two MCPs of meaningfully different shapes = "this candidate understands MCP as a primitive, not as a project." Karpathy's Sequoia talk explicitly names "stop building skills and start building MCP servers" as the single top recommendation for the 2026 hiring market ([[Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow]]). The Anthropic FDE Boston listing names "MCP servers, sub-agents, and agent skills" as deliverables ([[2026-05-07-target-role-specs]] §3 Anthropic FDE Applied AI). Two shipped MCPs of different shapes (skill-wrapper + knowledge-graph-wrapper) is the obvious differentiator over candidates with one or zero.

**Reason B — Phase D + Phase 6 currently have no customer-facing surface. (STRONG)**
The [[concept_edges]] SQLite table and the nightly synthesizer pipeline are real production infrastructure, but they only exist as: (i) CHANGELOG entries, (ii) the new [[concept_edges#EXPLANATION]] file (shipped 2026-05-12 evening), and (iii) the [[knowledge_loop#EXPLANATION]] file. Recruiters who want to *see* the work have to read code. An MCP makes it interactive — they can ask `find_contradictions()` and watch typed reasoning edges return as JSON. That's a 10x stronger signal than "read this 90-second 4Q artifact."

**Reason C — Knowledge-graph-as-product is an under-built thesis recruiters notice. (MEDIUM-STRONG)**
The dominant 2026 frame still treats LLMs as either (a) chat interfaces or (b) function-calling agents. The Karpathy synthesis Claim C ("specs and comprehension are the durable PM skill in the agent era") implies a third axis: LLM-curated structured knowledge as the bridge artifact between unstructured corpus and agent action. Sean's vault DOES this — typed edges, supersedence detection, contradiction surfacing — and the synthesizer's relations taxonomy mirrors OB1's published schema. An MCP makes this thesis live for any recruiter who has Claude Desktop open.

**Reason D — The Anthropic FDE Boston ask is literally this. (STRONG)**
The Anthropic FDE listing reads: "delivering technical artifacts for customers like MCP servers, sub-agents, and agent skills" ([[2026-05-07-target-role-specs]] §3). The portfolio-to-role mapping in §5 already maps `intent-engineering` MCP to this role; a *second* MCP of a different shape proves the candidate can adapt the pattern to customer-specific knowledge bases, which is the actual FDE day-to-day. Hiring manager talking point on this role family ([[2026-05-07-target-role-specs]] §4) is "can you design MCP architectures, sub-agent routing, and evaluation frameworks on a whiteboard." A second shipped MCP is the durable answer.

**Reason E — Recursive self-application: the MCP exposes the work that produced it. (MEDIUM)**
The vault contains the concept articles that explain the vault. The MCP querying that vault is a closed loop the recruiter can observe in real time. Aside from the demo elegance, this is functionally the same shape a Forward Deployed Engineer ships at customer sites: a server that exposes a customer's structured knowledge to their own agent workforce. Sean *being* the customer in his own demo is the cleanest possible proof of "I have done this at production grade for myself; I can do it for you."

---

## 3. How It Would Work (v0 Best-Guess Architecture)

### 3a. Tool Surface (3 tools, mirroring `intent-engineering`'s contract)

| Tool | Signature | Backed by | Returns |
|---|---|---|---|
| `search_concepts` | `(query: string, limit?: int = 5)` | Semantic search over `vault/knowledge/concepts/` + `connections/` + `qa/` | Array of `{slug, title, similarity_score, excerpt, last_modified}` |
| `find_contradictions` | `(scope?: 'all' \| 'recent_30d' = 'all')` | SQL: `SELECT * FROM concept_edges WHERE relation='contradicts' AND valid_until IS NULL` | Array of `{from_slug, to_slug, surfaced_at, source_run_id}` |
| `get_article` | `(slug: string)` | File read of `vault/knowledge/{concepts,connections,qa}/{slug}.md` | `{slug, frontmatter, body, wikilinks_out, wikilinks_in}` |

### 3b. Privacy / Allowlist Boundary

**Default config (locked):** only `vault/knowledge/concepts/`, `vault/knowledge/connections/`, `vault/knowledge/qa/` are readable. **Never** `00_inbox/`, `90_system/`, `health/`, `60_archive/`, `operating-models/`, `prj-job-hunt-2026/`, `the-block/`. Configurable via a JSON allowlist in the server config; not by request parameter (so a malicious client can't escalate scope).

### 3c. Tech Stack (v0 default — open for research challenge)

- **Language:** TypeScript (mirrors `intent-engineering`; preserves the muscle memory + publish flow)
- **SDK:** `@modelcontextprotocol/sdk` 1.29.0 (same pin as `intent-engineering`)
- **Transport:** Stdio (v0 — no HTTP/SSE; no auth surface)
- **Runtime:** Node 22
- **SQLite client:** `better-sqlite3` (synchronous, fast, no native build hassles on macOS)
- **Embedding strategy:** **Open question for research** — see §6 Q1
- **Index strategy:** **Open question for research** — see §6 Q2
- **License:** MIT
- **npm scope:** `@swins/vault-knowledge-mcp` (matches existing pattern)
- **MCP registry namespace:** `com.seanwinslow/vault-knowledge` (reuses Ed25519 key + TXT record already set up for Track-C)

### 3d. Data Flow (the demo path)

```
Claude Desktop (or any MCP client)
  → calls find_contradictions()
  → vault-knowledge-mcp Node process
    → reads vault/.vault-index.db (read-only, no write surface)
    → SELECT from concept_edges where relation='contradicts'
    → returns 0-N pairs as JSON
  → Claude Desktop renders the pairs in chat
  → user can call get_article(from_slug) on any pair to read the source
```

Zero network, zero auth, zero state mutation. Read-only, local-first, demo-able in 60 seconds at any conference table.

### 3e. Empty-State Behavior

If the vault is empty or the synthesizer hasn't run, every tool returns cleanly with explicit metadata: `{results: [], status: 'vault-empty', message: 'No concept articles found in vault/knowledge/concepts/. The synthesizer may not have run yet.'}`. **Never invent data.** Never hallucinate. Matches the vs-014 honest-deferral pattern from the eval suite.

---

## 4. How This Complements the Existing 7 Flagships

| Existing flagship | Today's surface | What `vault-knowledge-mcp` adds |
|---|---|---|
| `intent-engineering` MCP | Three tools, dogfooded 23/25 | Pattern proof: 2 MCPs, different shapes, same publish flow |
| Phase D typed reasoning edges | EXPLANATION.md + SQLite table | Interactive query surface — recruiters can call `find_contradictions` |
| Phase 6 knowledge loop | EXPLANATION.md + producer/consumer code | Interactive read surface — recruiters can call `search_concepts` |
| Sanitized financial-research fleet | (Pending Friday Week 4) | Independent — different vertical, no overlap |
| Animation pipeline | (Pending 6/11) | Independent — different vertical, no overlap |
| Vault Synthesizer Eval Suite | 7/10 binary pass/fail | Becomes downstream test target — eval the MCP's responses |
| Substack-Drafter Agent | Voice rotation, kill-switch layers | Demonstrates the producer side; MCP demonstrates the read side. Closed loop. |

Net portfolio count after this ships: **8 flagship + 2 supporting + 1 post-employment**. The eighth artifact is also the one that ties #2 + #3 + #6 + #7 into a single demo surface — that's the integration story.

---

## 5. Recruiter / Hiring-Manager Resonance Hypothesis

**The 60-second demo we believe lands hardest:**

> "Open Claude Desktop. Click the MCP server icon. You'll see `vault-knowledge` already connected. Type: *'find contradictions in my engineering decisions over the past month and explain the strongest one.'* Watch Claude call `find_contradictions(scope: 'recent_30d')`, get back two slugs, call `get_article` on each, and render a side-by-side. Total time: 40 seconds. The contradictions are real, surfaced by a typed-edges schema I built, queried by an MCP I published, rendered by your Claude Desktop. Zero infrastructure on my end. Zero auth. Zero magic."

**Why we believe this lands at each tier:**

- **Tier 1 (Anthropic FDE, Glean FDP):** Direct match to the JD ask. The demo IS the deliverable shape.
- **Tier 2 (Klaviyo, HubSpot, Liberate):** Demonstrates the candidate can take an organization's structured knowledge (Klaviyo's segmentation rules, HubSpot's CRM relationships, Liberate's insurance underwriting rules) and surface contradictions / search semantically — the exact pattern these companies are trying to build internally.
- **Tier 3 (Sierra, Decagon):** Shows the candidate can architect an agent's read surface, which is a sub-skill of designing prompt logic + agent behaviors.

**The pattern the demo refutes:** "Junior PM with portfolio demos." This isn't a portfolio demo — it's infrastructure the recruiter can install on their own machine in 30 seconds.

---

## 6. Open Questions for Deep Research

These are the questions a 60–90 minute Gemini DR-Max run should answer before code is written. Order by leverage.

**Q1 — Embedding strategy: JS-native vs. Python sidecar?**
Two options. (a) JS-native via Transformers.js or ONNX Runtime Web — runs entirely in Node, no Python dependency. (b) Python sidecar — the MCP shells out to a small Python service that wraps the existing `vault_indexer.py` embedding pipeline (nomic-embed-text on Mac Mini Ollama). Tradeoffs to evaluate: install complexity (recruiter clones repo + `npm install` — must just work), embedding quality (nomic-embed-text is proven on Sean's vault; JS alternatives may not match), latency (local Ollama vs in-process), maintenance burden. Research target: what have other "knowledge graph MCPs" or "RAG MCPs" published in the past 9 months done? Verify with at least 3 reference implementations (GitHub repo + last-commit-date + star count + npm-install + dry-run if possible).

**Q2 — State management: own the index or read Sean's existing `.vault-index.db`?**
The simpler path: the MCP reads `vault/.vault-index.db` directly, in read-only mode, with no write surface. The richer path: the MCP owns its own embedding index, regenerated on a watch-loop. Tradeoffs: shared-DB sees Sean's nightly synthesizer updates for free but couples publish state to vault layout; owned-DB is portable but doubles the indexing cost. Research target: which pattern is more common in published MCP servers, and is there a published "MCP best practices" doc (from Anthropic, MCP working group, or community) that takes a position?

**Q3 — Privacy boundary: allowlist vs. blocklist?**
v0 spec says allowlist by directory. But what's the failure mode if Sean later adds `vault/knowledge/private/`? Research target: what privacy boundary patterns ship in production MCP servers handling user data? Look at the Anthropic-published reference MCPs + the top 10 starred community ones. Is there a `MCP_ALLOWED_PATHS` env var convention emerging?

**Q4 — Naming: is `vault-knowledge-mcp` the right name?**
Candidates: `vault-knowledge-mcp` (descriptive), `vault-graph-mcp` (more accurate — it IS a graph), `comprehension-mcp` (Claude-Nate-2's pre-coined name), `knowledge-edges-mcp` (technical accuracy on the unique-feature side). Research target: name pattern analysis on the top 50 published MCP servers — what works for SEO + GitHub discovery + Loom-script readability? Is the `-mcp` suffix mandatory by convention or noise?

**Q5 — Tool surface count: 3 tools or 6?**
v0 spec says 3 tools. But the typed-reasoning-edge schema has 6 relations (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`). Should `find_contradictions` instead be `query_edges(relation: string)`? Tradeoffs: 3 tools = cleaner Loom script, 6 tools = more surface area for the recruiter to poke at. Research target: what tool-count distribution is currently optimal for "feels learnable in 60 seconds" vs "feels rich enough to be real"? Look at the top 20 MCP servers by GitHub stars and report tool-counts + descriptions.

**Q6 — Reference implementations to study (5–10 published MCPs to disassemble).**
Find 5–10 published MCP servers in the "knowledge graph", "vault", "RAG", or "personal-knowledge-base" categories, accessed in May 2026. For each, report: GitHub URL, npm package, last-commit-date, star count, tool count + names, transport type, language, license, README pitch quality (0–5), Loom availability. Identify the 1–2 strongest patterns to copy and the 1–2 weakest to avoid.

**Q7 — Recruiter-resonance pattern study.**
Are there published examples of "MCP server got me an interview at $COMPANY"? LinkedIn posts, Substack threads, HN comments. What was the artifact, what was the pitch, what landed? Look for at least 3 attributable cases dated April or May 2026.

**Q8 — FDE-loop-applicable demo shape.**
The 60-sec demo in §5 is one hypothesis. Are there better demo shapes? Specifically: what would an Anthropic FDE *want* to see vs a Glean FDP want to see vs a Decagon Senior Agent PM want to see? Surface 3 demo variants tuned to those audiences and evaluate against (a) demo length, (b) "wow" moment specificity, (c) follow-up question potential.

**Q9 — License + IP boundary.**
MIT for the code is obvious. But the vault knowledge embedded in the published demo: should Sean publish a generic "demo vault" repo alongside the MCP so the recruiter has something to point it at (since they don't have Sean's actual vault)? Or is "bring your own vault" the right v0 stance? Research target: what's the pattern for MCP servers that need user data — do they ship a demo dataset?

**Q10 — Productization ladder.**
Per Claude-Nate-2's recommendation, this could become `comprehension-mcp` as a paid product later ($10–15/seat/mo). Per ChatGPT-Nate-2's recommendation, the service-first ladder is the better cushion play. Research target: what published paid MCPs exist? What pricing? What conversion paths? Is the productization realistic, or is the right end-state "free + open source, used in interviews, never monetized"?

---

## 7. Anti-Patterns (Things NOT to Build)

- **Hosted SaaS / cloud-API mode.** v0 is stdio + local-vault. Period.
- **Auth surface.** MCP at this layer doesn't need it. Adding auth doubles complexity and zeros the demo elegance.
- **Real-time WebSocket updates.** Daily-refreshed read is fine. The synthesizer fires once nightly.
- **Hallucinating empty states.** If the vault is empty, return empty arrays with explicit status, never invent data.
- **Over-fitting to Claude Desktop.** The tool surface must work in Cursor, Anti-Gravity, and any compliant MCP client. Stdio + JSON Schema = portable.
- **Naming as a feature.** "vault-knowledge-magic-AI-graph-engine-pro" is anti-signal. Plain technical naming.
- **Coupling to Sean's vault layout permanently.** v0 reads Sean's paths; v0.2 should accept `VAULT_ROOT` env var so anyone can run it against their own Obsidian/Logseq/etc. vault.
- **Inventing new tools mid-build.** Lock the 3-tool spec at scope-lock, do not add tools during build, defer to v0.2.

---

## 8. Success Criteria (Binary, Measurable)

| # | Criterion | How verified |
|---|---|---|
| 1 | `@swins/vault-knowledge-mcp@0.1.0` published to npm | `npm view @swins/vault-knowledge-mcp version` returns `0.1.0` |
| 2 | `com.seanwinslow/vault-knowledge@0.1.0` published to MCP registry | `curl -s https://registry.modelcontextprotocol.io/v0/servers/com.seanwinslow/vault-knowledge` returns 200 |
| 3 | 4Q `EXPLANATION.md` lands at `docs/EXPLANATION.md` in the repo | File exists, passes <90-sec recruiter readability cold-read test |
| 4 | README pitch under 200 words with copy-paste `claude_desktop_config.json` block | Word count + screenshot of connected-server status |
| 5 | All 3 tools return non-error responses against Sean's live vault | Manual MCP Inspector pass |
| 6 | Empty-state path returns clean status (not hallucination) | Test against a blank `vault/.vault-index.db` |
| 7 | 90-sec Loom demonstrating all 3 tools | Loom URL exists, plays end-to-end |
| 8 | LinkedIn syndication post tagging Anthropic + MCP team | Post URL exists |
| 9 | At least 1 recruiter / hiring-manager engagement attributable to this artifact | Recorded in [[target-companies]] notes column |
| 10 | Pattern proof: same publish flow as `intent-engineering`, no surprises | CHANGELOG of the new repo references the frozen reference in the unified roadmap |

---

## 9. Time + Cost Estimate

**Time:** 5–7 working days. Day 1: scaffolding (reuse `intent-engineering` skeleton). Day 2–3: tool implementations + tests. Day 4: hardening + MCP Inspector pass. Day 5: README + EXPLANATION + Loom. Day 6: publish + registry. Day 7: announce + cleanup. If research surfaces a Python-sidecar requirement (Q1), add 1 day.

**Cost:** $0 cloud. Sean's machine + existing Ollama. npm + MCP registry are free. Domain auth already paid + verified.

**Schedule placement:** earliest start Mon 2026-05-19 (after Target-30 list + agent fleet audit close), ship target Wed 2026-05-28 to Fri 2026-06-04 depending on research depth. Slips do not affect Track-C, animation pipeline (6/11), or eval suite Loom (5/22). Tier-A protected.

---

## 10. Tier-A Check (Operating Model Compliance)

- **Walk-away $100k base:** N/A — this is portfolio, not employment.
- **5-days-in-office no:** N/A — local work.
- **AI > Tech > Creative PM ordering:** ✅ — this is the canonical AI-PM artifact.
- **Agents draft / Sean sends:** ✅ — Sean sends the LinkedIn announcement personally; agents may draft.
- **Track-C protected:** ✅ — `intent-engineering` is shipped; this is a follow-on, not a replacement.
- **Friday 4:30 retro:** ✅ — build fits inside the 8:30–5:30 deep-work container.
- **5:30 PM hard stop:** ✅ — 5–7 day build does not require evening overflow.

---

## 11. References to Study (Pre-Research Reading List)

Sean and the deep-research run should both ingest these:

- [[2026-05-06-unified-roadmap]] §"Publish + registry flow — frozen reference" — the existing publish mechanics
- [[Claude-Karpathys-Sequoia-Ascent-2026-Strategic-Synthesis-for-Sean-Winslow]] §"MCP servers are the portable career artifact"
- [[2026-05-07-target-role-specs]] §3 Anthropic FDE + §5 Portfolio-to-Role Mapping
- [[concept_edges#EXPLANATION]] — the data the MCP exposes
- [[knowledge_loop#EXPLANATION]] — the pipeline that produces the data
- Anthropic's published MCP examples: https://github.com/modelcontextprotocol/servers
- The OB1 reference schema for typed reasoning edges (referenced in the v3.20.0 Phase D CHANGELOG entry)
- The npm registry MCP listing: https://www.npmjs.com/search?q=mcp-server

---

## 12. Research Instructions (Paste-Ready Prompt Scaffold)

The following is a paste-ready prompt for Gemini DR-Max (or a Claude deep-research run). Copy from the line below to the end of this document.

---

```
<role>
You are an MCP-ecosystem analyst with deep coverage of published MCP servers as of May 2026. You read source repos, npm package READMEs, MCP-registry listings, and community discussion on the MCP working group's GitHub Discussions + Anthropic's developer Discord. You speak with the precision of someone whose architectural recommendations have shipped to production at frontier AI shops.

Your job is to produce a grounded architecture-validation document for a personal MCP server (`vault-knowledge-mcp`) that a 33-year-old AI PM is preparing to ship as the 8th flagship artifact in his job-hunt portfolio. The document feeds (a) the architectural decisions before code is written, (b) the README + Loom-script positioning, and (c) the recruiter-resonance hypothesis evaluation.
</role>

<context>
**Candidate profile:**
- 2 years titled PM experience, 4–6 years of agentic-engineering portfolio signal
- One MCP server already published: `intent-engineering` (3 tools, stdio, TypeScript, npm + MCP registry under `com.seanwinslow/intent-engineering@0.1.0`)
- Existing vault infrastructure: Obsidian vault with ~120 concept articles, ~40 connection articles, ~10 qa articles, a SQLite `concept_edges` table with 6 relation types (`supports`, `contradicts`, `evolved_into`, `supersedes`, `depends_on`, `related_to`), nightly synthesizer that emits typed edges
- Target roles: AI PM at frontier labs (Anthropic FDE, Glean FDP), Agent PM at AI-native startups (Sierra, Decagon), Forward Deployed Product at infra (Cohere, Liberate)

**The artifact being designed:**
- Name (working): `vault-knowledge-mcp`
- 3 tools: `search_concepts(query, limit)`, `find_contradictions(scope)`, `get_article(slug)`
- Stack: TypeScript, MCP SDK 1.29.0, stdio transport, Node 22
- Publish target: npm `@swins/vault-knowledge-mcp` + MCP registry `com.seanwinslow/vault-knowledge`
- Build time budget: 5–7 working days
- Cost target: $0 (local-first, no cloud)

**Why this artifact matters:**
- Pattern repeatability — 2 MCPs of different shapes proves the candidate gets MCP as a primitive
- Anthropic FDE JD literally asks for "MCP servers, sub-agents, and agent skills"
- Phase D typed-reasoning-edges work currently has no customer-facing surface — this MCP makes it queryable
- The 60-second demo: open Claude Desktop, call find_contradictions, watch the candidate's vault surface real contradictions in their engineering decisions

**Non-negotiables:**
- Local-first, stdio transport only, no auth, no SaaS
- Read-only against the vault — zero write surface
- Empty-state honesty: if vault is empty, return cleanly, never hallucinate
- Reuse the publish flow from `intent-engineering` (DNS-verified namespace, Ed25519 key already provisioned)
- Build fits inside a 5:30 PM hard-stop daily container
</context>

<task>
Produce a 10-section architecture-validation document covering the questions in <output_format>. Multi-source triangulation: every architectural recommendation must cite at least 2 independent reference implementations (published MCP server + README/source + last-commit-date verifiable on GitHub).

The goal is NOT to summarize the MCP spec — the candidate has read it. The goal is to surface:
- What architectural decisions in the proposed v0 spec are wrong or suboptimal
- What reference implementations are doing better, and what specifically to copy
- What the recruiter-resonance hypothesis (60-second demo, 3-tool surface, naming) should be tuned to based on observable signal from MCP-related interview reports
- The 1–2 things in the v0 spec that, if changed before code is written, would have outsized impact on outcome
</task>

<anti_hallucination_guards>
Non-negotiable. Prior research has fabricated MCP server names, GitHub URLs, npm packages, and "industry conventions."

1. Every cited MCP server must link to a current, reachable GitHub URL AND a reachable npm package (if applicable). If a server is mentioned in a blog post but not findable on GitHub or npm, mark as "claimed but unverifiable — recommend skip."
2. Star counts, last-commit-dates, and tool counts must be from a verifiable source (GitHub repo page, accessed on YYYY-MM-DD). Do not interpolate.
3. "Industry convention" claims (e.g., "most MCPs use stdio") must cite at least 3 specific MCP server examples that follow the convention. If you can't find 3, mark as "preliminary pattern."
4. "Anthropic recommends X" — only include if attributable to an Anthropic-published source (docs.anthropic.com, github.com/modelcontextprotocol, an Anthropic engineering blog post). Paraphrased rumor is forbidden.
5. If a reference implementation's last commit is more than 6 months old, flag it as "possibly abandoned."
</anti_hallucination_guards>

<output_format>
Markdown with frontmatter, then ten sections.

## 1. Reference Implementation Survey (8–12 MCPs)
For each: name, GitHub URL, npm package, last-commit-date, star count, tool count + names, transport, language, license, README pitch quality (0–5), Loom/demo URL availability, "what they got right," "what they got wrong." Order by relevance to `vault-knowledge-mcp`.

## 2. Embedding Strategy Verdict (answers Q1)
JS-native vs. Python sidecar. Pick one. Cite reference implementations supporting the pick. Estimate install complexity for a recruiter cloning the repo.

## 3. State-Management Verdict (answers Q2)
Read-only against existing `.vault-index.db` vs. own embedding index. Pick one. Cite published "MCP best practices" if any exist; otherwise cite 3 reference implementations and their patterns.

## 4. Privacy-Boundary Pattern (answers Q3)
Allowlist vs. blocklist vs. env-var-based. Pick the pattern that ships in the most reference implementations.

## 5. Naming Verdict (answers Q4)
`vault-knowledge-mcp` vs. `vault-graph-mcp` vs. `comprehension-mcp` vs. `knowledge-edges-mcp` vs. other. Pick one. Cite SEO + GitHub-discovery signal and at least 3 example MCPs whose naming worked.

## 6. Tool-Count Verdict (answers Q5)
3 tools vs. 6 tools vs. other. Pick a count. Cite distribution from §1 survey.

## 7. Recruiter-Resonance Cases (answers Q7)
List 3+ attributable cases of MCP-server-led job-hunt wins from April–May 2026. For each: source URL, candidate name (or anonymized), company, what the artifact was, what the pitch was.

## 8. Demo-Shape Variants (answers Q8)
3 demo shapes tuned to different role families (Anthropic FDE, Glean FDP, Decagon Senior Agent PM). Evaluate each on demo length, wow-moment specificity, follow-up-question potential.

## 9. License / Demo-Vault Boundary (answers Q9)
Should the repo ship a public demo vault? Cite at least 2 MCPs that need user data and how they handled this.

## 10. The Outsized-Impact Recommendation
One specific architectural or positioning change to the v0 spec that, if made before code is written, would meaningfully shift the recruiter-resonance outcome. Justify with reference to §1 and §7 findings.

## Sources Index
Every GitHub URL, npm URL, blog post, podcast, post, and reference cited above. Organized by section. Accessed-on date for each.
</output_format>

<validation>
Before delivering:
1. Link health: every GitHub + npm URL gets opened to verify it loads.
2. Star/commit verification: report each star count and last-commit-date as of the accessed-on date.
3. Tool-count discipline: re-read §6 — if your verdict differs from the distribution in §1, explain the divergence.
4. Recruiter-case verification: every case in §7 must have a public-source URL OR be marked anonymized + how-anonymized.
5. The outsized-impact recommendation must trace to specific findings in §§1, 7, or 8.
6. Word count target: 3,500–5,500 words.
</validation>
```

---

**Status when this research returns:** flip this spec's frontmatter `status` from `research-pending` to `research-complete`. Append the research file path as a new `linked_research` entry. Then update Task 10 in the unified roadmap to reflect the locked architecture + ship date.
