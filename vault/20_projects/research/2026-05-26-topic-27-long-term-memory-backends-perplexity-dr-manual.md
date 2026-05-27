# Long-Term Memory Backend Decision for a Solo Claude Agent Fleet (2026)

> **Research date:** 2026-05-27. This landscape moves fast — any conclusion here is perishable. Re-evaluate if Anthropic ships a breaking memory-tool update, if Mem0 v3 stabilises its ADD-only pipeline bug (issue #4956), or if Letta releases a 2.0 milestone.

***

## Executive Summary

Five options are evaluated for a solo developer running ~27 Claude agents (14 SDK + 13 Code subagents) on local Apple Silicon hardware. The analysis finds that **Anthropic's native `memory_20250818` tool (Option D), extended with a thin cross-agent routing layer, is the correct choice now**: it has zero infra overhead, full privacy, a storage backend already running on every machine in the fleet, and native first-class integration with the Claude API. Mem0 OSS (Option A) is the correct answer the moment the fleet grows past ~50 agents or multi-hop relational queries become critical. The do-nothing baseline (Option E) is a rational fallback but accumulates coordination debt faster than any of the dedicated backends.

***

## Master Comparison Table

| Axis | A — Mem0 OSS | B — Letta | C — Zep / Graphiti | D — Anthropic `memory_20250818` | E — Do-Nothing (CLAUDE.md + CC auto-memory + Obsidian RAG) |
|------|-------------|-----------|-------------------|----------------------------------|-------------------------------------------------------------|
| **1. Architecture** | Hybrid: vector store (Qdrant or pgvector) + optional Neo4j/FalkorDB knowledge graph. Embedding-model dependency (nomic-embed-text, bge-m3, or OpenAI). History in SQLite. | Hybrid: PostgreSQL + pgvector for archival search; core memory as structured in-context blocks. Optional git-backed MemFS (Context Repositories) for versioned memory files.[^1][^2] No external graph DB required by default. | Temporal knowledge graph via Graphiti. Neo4j ≥5.26 (or FalkorDB 1.1.2+) required. Zep Community Edition is frozen/archived; active open-source effort is Graphiti alone.[^3][^4] Embedding dependency (OpenAI, Voyage, or local). | Flat-file, client-side. Memories stored as markdown files in a `/memories` directory you control. No vector store, no graph DB, no embedding model required.[^5][^6] | Three heterogeneous stores: markdown files (CLAUDE.md), model-managed flat files (~/.claude/projects/.../memory/), local Qdrant + nomic-embed-text Ollama index. No unified schema or routing layer. |
| **2. Write-path** | Automatic LLM-based extraction on every `add()` call. LLM reads the message, extracts discrete facts, embeds them, optionally resolves them against the graph. Hybrid; write triggered programmatically by the developer calling `m.add()`.[^7][^8] **Known bug (v3, open Apr 2026):** extraction pipeline is ADD-only — UPDATE/DELETE events were removed; contradictory facts now accumulate.[^9] | Agent-driven tool calls (`memory_insert`, `memory_append_to_block`, `memory_replace_in_block`, `archival_memory_insert`). The agent model itself decides what to save; no external LLM extraction pass. Hybrid; writes can also be triggered by the host application.[^1][^10] | Automatic ingestion via Graphiti's episode API. Graphiti uses an LLM call to extract entities/edges, then runs deterministic IR deduplication (MinHash+LSH) before writing to the graph.[^11] Write triggered on `add_episode()`. | Agent-issued tool calls (`view`, `create`, `str_replace`, `insert`, `delete`, `rename`) against a `/memories` directory on your filesystem. The agent model decides what to write — no separate extraction LLM needed.[^5][^6][^12] | Writes are manual (CLAUDE.md editing), model-initiated (CC auto-memory, opaque), or explicit note creation in Obsidian. No unified write trigger or cross-agent propagation. |
| **3. Read-path** | Similarity search: embed the query, cosine-search Qdrant/pgvector, optionally layer graph traversal. Results prepended to prompt by the calling application. Read is explicit; developer controls injection.[^7][^13] | Tiered: core memory blocks always in context (prepended); archival memory retrieved via similarity search on explicit tool call; conversation summary maintained. Context window engineering is Letta's core design.[^14][^15] | Graph RAG: hybrid search over nodes and edges (RRF + cross-encoder reranker), returns temporally-tagged relationship-aware context blocks. Sub-200ms claim from vendor (see §4).[^16][^17] | Agent reads `/memories` directory on every session start (Claude checks directory automatically when enabled). Reads relevant files into context via tool calls; no embedding pipeline; no similarity search.[^5][^6] | CLAUDE.md: always prepended (consumes context). CC auto-memory: opaque model decision. Obsidian RAG: explicit query against nomic-embed-text. No unified read API across all three. |
| **4. Retention quality** | **Vendor-self-reported:** LoCoMo 92.5, LongMemEval 94.4, BEAM-1M 64.1 (new algorithm, Apr 2026).[^18] **Independent controversy:** A May 2025 dispute (Zep-papers issue #5) showed both Mem0 and Zep used non-standard prompts and miscounted adversarial categories; corrected Zep score was ~75% vs Mem0's ~66% under standardised conditions.[^19] A separate Apr 2026 audit (dev.to/vektor_memory) found "serious methodological issues" in the LoCoMo dataset itself.[^20] **No independent peer-reviewed reproduction exists for Mem0's v3 numbers.** ADD-only write bug (issue #4956, open) means temporal accuracy degrades over long agent lifetimes.[^9] | No published LoCoMo score for Letta. The MemGPT paper introduced the DMR benchmark (94.8% MemGPT-claimed, now superseded by Zep's DMR result of 94.8% vs MemGPT 93.4%).[^21] No independent third-party benchmark results found for Letta's current Context Repositories architecture as of mid-2026. Context drift ("derailment") is a documented production concern.[^22] | **Vendor-self-reported (arxiv 2501.13956):** DMR 94.8% vs MemGPT 93.4%; LongMemEval +18.5% vs baseline; 90% latency reduction vs baseline.[^21][^23] **LoCoMo controversy:** Zep's original claim of 84% was challenged by Mem0 (issue #5, May 2025); Zep's corrected response is 75.14% ± 0.17 over 10 runs, still outperforming Mem0's 65.99% under standardised conditions.[^19] **No fully independent third-party reproduction of either score exists.** | No published benchmark. Storage is flat files; accuracy depends entirely on the Claude model's memory-writing discipline. Anecdotal: works well for coding/project-scoped agents; quality degrades with large memory directories.[^24][^25] The operator's Claude Code auto-memory already uses this pattern. | Obsidian RAG: no published retention benchmark. CLAUDE.md: full recall of whatever is in the file (bounded by file size). Auto-memory: opaque. LoCoMo performance unknown. System performance bounded by the weakest link (stale RAG index, bloated CLAUDE.md). |
| **5. Self-host on Apple Silicon** | **Yes — fully local.** Min config: `pip install mem0ai`, local Qdrant (Docker), Ollama nomic-embed-text. The operator already runs nomic-embed-text. Graph mode adds Neo4j or FalkorDB containers. A validated Reddit tutorial (Feb 2026) demonstrates full stack with Qdrant + bge-m3 + Ollama + optional Neo4j, all local.[^26][^7] Steps: (1) `docker run qdrant/qdrant`, (2) `ollama pull nomic-embed-text`, (3) configure `Memory.from_config()`, (4) optionally `docker run neo4j:5.26` or `docker run falkordb/falkordb`. No cloud calls in library mode with Ollama provider.[^7] | **Yes — self-hostable via Docker.** `docker run letta/letta` binds port 8283, stores pgdata at `~/.letta/.persist/pgdata`, supports Ollama and LM Studio for local models.[^1][^27] Embedding model must be configured explicitly (Ollama nomic-embed-text works). MemFS git-sync requires a sidecar; local mode is available. Letta Desktop app available for macOS. Setup friction: moderate — Docker required, embedding provider must be configured, ADE requires HTTPS for remote access.[^1] | **Graphiti only (Zep CE is frozen).** Graphiti + FalkorDB: `docker run falkordb/falkordb -p 6379:6379 -p 3000:3000`, then `pip install graphiti-core[falkordb]`.[^28][^29] Neo4j: requires `docker run neo4j:5.26-community` (~1–2 GB RAM). Both run on Apple Silicon via Docker. **Requires an OpenAI-compatible LLM for entity extraction** — local Ollama endpoint works but quality depends on model (Qwen3:14b tested with reasonable results).[^26] Setup friction: moderate-high — two services (graph DB + LLM), Graphiti is a library not a managed server, no dashboard. | **Yes — zero infra.** The tool works by issuing file-system commands against a local `/memories` directory. Nothing to install beyond `anthropic` Python SDK ≥ 0.74.1 and the `context-management-2025-06-27` beta header.[^12][^5] As of Apr 2026, Anthropic shipped memory for Claude Managed Agents in public beta, with filesystem mounts scoped at org or user level.[^30] For SDK agents, the operator implements `handle_memory()` in ~50 lines of Python. No Docker, no embedding model, no vector DB.[^25] | Already running — zero additional setup. Obsidian RAG requires maintaining the nomic-embed-text Ollama index and periodic re-indexing. CLAUDE.md files must be manually curated. No unified cross-agent memory layer. |
| **6. Latency overhead** | Vector search: Qdrant p95 ~10–30ms locally at 10k records; scales to 100k with minor degradation. Graph mode: each `add()` fires 1–3 LLM calls (entity extraction, relation resolution, deduplication) → 500ms–3s per write with Ollama local model; shorter with API.[^26][^8] Read (search) adds ~10–50ms for embedding + ANN search.[^18] At 100k+ records, Qdrant performance holds but Neo4j graph traversal slows — FalkorDB shows sub-10ms graph queries at scale.[^17] | Core memory operations (insert, replace) are in-context string edits — sub-millisecond. Archival memory writes: embedding + PostgreSQL insert, ~20–50ms. Archival search: pgvector cosine search, ~20–100ms at 10k records. Context Repositories (git-based) adds a git commit per write — tens of ms.[^1][^15] No public latency benchmarks for Apple Silicon. | Graphiti write: LLM extraction + graph write; vendor claims "sub-200ms" for retrieval.[^16] FalkorDB graph queries: sub-10ms to sub-millisecond at scale.[^17] Each `add_episode()` is significantly heavier than a vector write due to the LLM extraction pass. At 100k+ graph nodes, FalkorDB scales better than Neo4j Community Edition.[^17] No independent Apple Silicon latency data published. | Near-zero for read (directory listing + file reads = filesystem I/O, <5ms). Write: one LLM tool call + local file write, <100ms round-trip overhead. Scales well: at 100k+ memory files, Claude switches from scanning everything to a manifest+top-5 lightweight retrieval pattern.[^24] Performance bounded by context window injection size, not storage I/O. | CLAUDE.md read: always in context, zero latency but consumes tokens. Obsidian RAG search: ~50–200ms (Ollama embedding + HNSW search). Cross-agent propagation: non-existent — each agent reads its own store only. |
| **7. Integration friction (Claude Agent SDK + Claude Code)** | **SDK: Low.** `pip install mem0ai`. Call `m.add(messages, agent_id="vault-indexer")`. Inject `m.search(query, agent_id=...)` results into system prompt. No MCP required, pure Python. **Claude Code: Validated community MCP server exists (Feb 2026 Reddit tutorial) — Qdrant + Ollama + 11 tools exposed via MCP stdio transport.**[^26] Anthropic Agent SDK has no built-in memory; Mem0 fills the gap cleanly. | **SDK: Moderate.** Letta has its own agent loop — integrating with the Anthropic Agent SDK means running Letta as a sidecar REST service (port 8283) and calling it from within each SDK agent for memory reads/writes. Not a drop-in library. **Claude Code: No official adapter found as of mid-2026.** Letta Code is Letta's own coding agent, not a Claude Code plugin. Multi-agent groups API reported failing with backend errors (GitHub issue #3008, Sep 2025).[^31][^1] | **Graphiti SDK: Moderate.** `pip install graphiti-core`, call `graphiti.add_episode(...)` and `graphiti.search(...)` from Python. Works as a library. **MCP server: Available** — Graphiti MCP Server 1.0 (Nov 2025) supports Claude Desktop and MCP-capable agents, 100k+ weekly users.[^11] For Claude Code, add the Graphiti MCP server to `~/.claude.json`. Requires Neo4j or FalkorDB to be running. | **SDK: Minimal — first-class.** The `memory_20250818` tool type is declared in the Anthropic SDK like any other built-in tool.[^32][^5] Enable with `tools=[{"type": "memory_20250818"}]` and beta header `context-management-2025-06-27`. **Claude Code: Native — Claude Code already uses this exact flat-file pattern for its auto-memory.**[^24][^33] No MCP server needed; no additional libraries. The same `/memories` dir can be read/written by SDK agents and Code subagents if pointed at a shared path. | No integration work required — already in production. Cross-agent propagation requires manual copy-paste or a custom sync script. Claude Code subagents cannot read SDK agent CLAUDE.md files without explicit path configuration. The "three uncoordinated stores" problem is structural, not solvable without code changes. |
| **8. License + maintenance** | **Apache 2.0** (open-source core).[^34][^35] ~40k GitHub stars, active commits (May 2026).[^36] Open issues: 5000+ open (large active community); recent close rate high. Team: mem0ai (Series A funded, details not public). **Risk flag:** v3 ADD-only extraction bug (issue #4956) has been open since Apr 2026 without a fix.[^9] Vendor platform (cloud API) is separate; OSS is maintained independently. | **MIT** (letta-code and core).[^37] $10M seed round led by Felicis (Sep 2024, $70M post-money valuation).[^38][^39] Team: ~13 employees (2025).[^40] GitHub: 29 open issues (Oct 2025 snapshot); 1005+ closed — good close rate.[^31] Active development: Context Repositories shipped Dec 2025, Letta Code shipped Dec 2025.[^41][^2] No rewrite or sunset signals; research-oriented team with UC Berkeley pedigree. | **Graphiti: Apache 2.0.**[^11] Zep CE frozen (Apr 2025) — no further updates.[^3][^4] Graphiti: 24k+ stars (YC W24, as of mid-2026), weekly 25k PyPI downloads.[^42][^43] Zep AI team: 5 people, YC W24, seed stage, 50% MoM ARR growth claimed (YC jobs page).[^42] MCP Server 1.0 shipped Nov 2025.[^11] **Risk flag:** Zep cloud dependency for managed features; Graphiti OSS is the only self-host path and is still maturing. | **No separate license** — part of Anthropic's API. Client-side implementation is your own code. Beta status as of the `context-management-2025-06-27` header.[^5] GA designation: `memory_20250818` is listed as GA in the tool reference.[^32] Anthropic Managed Agents memory shipped public beta Apr 2026.[^30] **Risk flag:** Anthropic can modify or deprecate the tool; there is no independent open-source fork. The flat-file output format is portable, mitigating lock-in risk. | CLAUDE.md: no dependency, no license issue. Claude Code auto-memory: subject to Anthropic's opaque implementation decisions.[^44] Obsidian vault + nomic-embed-text: fully local, MIT-licensed tooling. **Risk flag:** three separate maintenance surfaces; no single upgrade path. |
| **9. Known production failure modes** | **Stale/contradictory facts accumulating (v3, documented):** GitHub issue #5193 (May 2026) — "I like coffee" + "I no longer like coffee" both stored; both return on query with near-equal scores.[^45] GitHub issue #4956 (Apr 2026) — ADD-only extraction pipeline means mutable-state facts never superseded.[^9] **Integration bug:** crewAI integration `mem0_storage.py` had a `TypeError` on search due to response format mismatch (GitHub crewAI #2589, Apr 2025).[^46] **Benchmark dispute:** Mem0's own LoCoMo numbers disputed by Zep (zep-papers issue #5, May 2025) and a separate independent audit found "serious methodological issues" in the benchmark itself.[^19][^20] | **Reliability with smaller LLMs:** GitHub issue #1776 (Sep 2024) — user reports MemGPT/Letta does not work reliably with any locally-hosted LLM; the tool-calling loop requires a capable model.[^22] **Groups API failures:** GitHub issue #3008 (Sep 2025) — Groups API (multi-agent supervisor, round-robin, dynamic) failing with backend errors.[^31] **Context derailment:** acknowledged in the MemGPT research community and by Letta CTO Sarah Wooders as a fundamental challenge ("pollution control, compaction, accurate referencing").[^10] **Ollama provider:** custom BYOK Ollama providers not discoverable via `/v1/models/` endpoint (issue #3037, Oct 2025).[^31] | **LoCoMo 84% claim retracted** to 75.14% (Zep-papers issue #5, May 2025) after Mem0 found a calculation error; Zep still claims superiority over Mem0 under corrected conditions.[^19] **Self-host analytics gap:** Reddit r/Rag (Apr 2026) — self-hosted Graphiti has no built-in analytics; "significant gap" vs. managed tier.[^47] **Zep CE frozen:** users relying on Zep Community Edition received no bug fixes after Apr 2025.[^3] **LLM extraction variance:** before Nov 2025 Graphiti update, entity deduplication was LLM-only, causing retry loops and token burn in high-throughput setups.[^11] | **Path traversal vulnerability:** A developer video (Apr 2026) documented that without `realpath + prefix check`, a Claude agent using `memory_20250818` can read arbitrary files (e.g., `.env`) outside `/memories`.[^25] **Must implement yourself:** no deduplication, no contradiction resolution, no recency ranking — the operator's application code must handle all of this. **Quality at scale:** r/LocalLLaMA (Apr 2026) notes that the model's manifest-then-top-5 approach works well up to ~200 files; no published data beyond that.[^24] **Beta status caveats:** as of mid-2026, requires the `context-management-2025-06-27` beta header; API behaviour could change.[^5] | **Zero cross-agent propagation:** GitHub issue #4588 (anthropics/claude-code, Jul 2025) explicitly documents that Claude Code subagents are stateless and "domain expertise must be re-explained in every Task tool invocation."[^48] **Auto-memory opacity:** Claude Code auto-memory writes are model-managed; the operator has no control over what gets written or overwritten. **RAG index staleness:** Obsidian vault changes require manual re-indexing; no event-driven update. **Scale cliff:** CLAUDE.md files grow unboundedly unless manually pruned; large files degrade context quality. |
| **10. Recommended use case** | Best when: cross-agent memory sharing is needed (shared `agent_id` or `user_id` namespace), the fleet is 10+ agents, or relational/entity queries ("what did agent X learn about tool Y?") matter. Also best when Obsidian vault data should be co-indexed with agent learnings. Switch to graph mode when multi-hop reasoning over concepts is required. | Best when: the primary use case is a single long-lived conversational agent that must maintain a rich, editable identity and preferences over months. Letta's white-box core memory blocks are uniquely good for this. Sub-optimal for fleet coordination of many short-lived task agents (launchd-scheduled batch runners). | Best when: temporal reasoning over evolving facts is critical (e.g., "what did this agent believe about X two weeks ago vs. now?"), or when the agent must reason over both conversation history and structured business data simultaneously. Graphiti's temporal graph is genuinely differentiated for this use case. | Best when: the fleet is primarily Claude-model agents, privacy is paramount, zero infra overhead is required, and the operator already manages the filesystem. Ideal for bootstrapping — get cross-session memory in an afternoon. Outclassed by Mem0/Graphiti once the fleet needs entity-level relational queries or cross-agent contradiction resolution. | Best when: the operator has insufficient time to evaluate alternatives, the fleet is small and agents are mostly independent (no shared knowledge needed), and vault RAG coverage is adequate. This is a rational holding pattern, not a permanent architecture. |

***

## Benchmark Quality Warning

All four active candidates have published LoCoMo or LongMemEval numbers, and **none of the four has an independent peer-reviewed reproduction as of mid-2026.**

- **Mem0** publishes LoCoMo 92.5 and LongMemEval 94.4 on its research page (Apr 2026) — vendor self-reported. The numbers are contested: Zep challenged the methodology in May 2025 (zep-papers issue #5) and a separate community audit found "serious methodological issues" in the LoCoMo dataset itself. Mem0's own v3 ADD-only pipeline bug (issue #4956) is a direct contradiction of its temporal-accuracy claims.[^19][^9][^18][^20]
- **Zep/Graphiti** self-reports DMR 94.8%, LongMemEval +18.5% (arxiv 2501.13956, Jan 2025). The LoCoMo claim was revised from 84% to 75.14% ± 0.17 (10-run average) after Mem0's critique. Both teams agree the corrected number shows Zep outperforming Mem0's 65.99% on LoCoMo; neither number has third-party verification.[^21][^23][^19]
- **Letta** has no published benchmark for its current 2025–2026 architecture.
- **Anthropic `memory_20250818`** has no published benchmark.

The LoCoMo dataset itself has documented quality issues (adversarial category miscounting, single-run variance). Treat all numbers as directional signals, not ground truth.[^20][^19]

***

## Architecture Diagram (Conceptual)

```
Current (three uncoordinated stores):
  SDK Agent A  →  CLAUDE.md (project-level)
  SDK Agent B  →  CLAUDE.md (project-level)
  CC Subagent  →  ~/.claude/projects/.../memory/ (auto-managed)
  All agents   ←  Obsidian vault RAG (ad-hoc pull only)
  [No cross-propagation; no shared namespace]

Proposed (Anthropic memory_20250818 + shared /memories):
  SDK Agent A  ↕  /memories/fleet/  (shared read-write)
  SDK Agent B  ↕  /memories/fleet/  (shared read-write)
  CC Subagent  ↕  /memories/fleet/  (shared via CLAUDE.md pointer)
  All agents   ←  Obsidian vault RAG (unchanged, kept separate)
  [Single human-readable directory; cross-agent propagation via shared path]
```

***

## Ranked Recommendation for This Operator

*As of 2026-05-27.*

**Pick Option D — Anthropic `memory_20250818` — as the unified memory layer, with a phased path to Mem0 OSS.**

### Why D wins now

The operator already pays the operational cost of three stores. The highest-value fix is not a better memory algorithm — it is **cross-agent propagation**: lessons from one agent's failed run should reach the other 26 agents. The `memory_20250818` tool solves this for free: point all SDK agents and Code subagents at the same `/memories/fleet/` directory, and every write is immediately readable by every reader. The storage is already on the machine (filesystem), the embedding model dependency is zero, the setup is ~50 lines of Python in a shared `handle_memory()` helper, and the output is human-readable markdown that integrates naturally with the existing Obsidian vault. Privacy is absolute — nothing leaves the machine.[^5][^25]

### Minimum-viable migration from the current three-store mess

1. **Week 1:** Implement a `handle_memory(tool_use_block)` helper (50 lines, validated example in cited YouTube walkthrough). Add `realpath + prefix check` for path traversal safety. Enable for two agents (vault-indexer + morning-briefing) as a pilot.[^25]
2. **Week 2:** Point all SDK agents at a shared `/memories/fleet/` path in their system prompts. Add a lightweight `MEMORY_INDEX.md` manifest file that each agent updates with a one-line summary of new writes (enables the manifest-then-top-5 retrieval pattern).[^24]
3. **Month 2:** Deprecate the three separate stores. Migrate CLAUDE.md summaries into the shared `/memories/fleet/` directory. Keep Obsidian vault RAG for document-scale retrieval (vault notes are too large for the memory-file pattern). The auto-memory at `~/.claude/projects/` can be left running in parallel; it does not conflict.
4. **Ongoing:** When a `~/.claude/projects/` auto-memory write occurs that is agent-specific knowledge (not just session state), manually promote it to `/memories/fleet/`.

### When to switch to Mem0 OSS (Option A)

- Fleet grows past ~50 agents, or agents begin needing cross-entity relational queries ("which agents have encountered Tool X's rate-limit pattern?").
- The Mem0 v3 ADD-only extraction bug (issue #4956) is fixed and verified.
- Integration: `pip install mem0ai`, configure `Memory.from_config()` with the already-running nomic-embed-text Ollama instance and local Qdrant. The operator's existing embedding infrastructure is already compatible.[^7]

### When to consider Graphiti/Zep (Option C)

- Agents need temporal reasoning ("what did the vault-critique agent believe about file X *last month* vs. *now*?").
- The Graphiti MCP Server is already the most natural fit for Claude Desktop/Code multi-client setups.[^11]

### When to reconsider Letta (Option B)

- The fleet shifts from scheduled batch runners to long-lived persistent conversational agents, or the operator joins a team and needs Letta's ADE for collaborative agent debugging.

### Conditions under which the do-nothing baseline (E) is correct

- Less than 30 days of runway for this decision; the cost of migration exceeds the cost of continued coordination overhead.
- Agents are fully independent (no shared domain knowledge needed) — the current Obsidian RAG is sufficient as a read-only knowledge base.

***

## Per-Option Quick-Reference

### A — Mem0 OSS
- **Strongest axis:** Cross-agent shared memory with entity deduplication; widest community MCP ecosystem.
- **Biggest risk right now:** ADD-only write pipeline (v3, issue #4956) means stale facts accumulate for time-sensitive attributes.[^9]
- **Self-host lift:** Low — operator already runs nomic-embed-text. Add Qdrant container (Docker), configure `Memory.from_config()`. Graph mode adds Neo4j or FalkorDB.

### B — Letta
- **Strongest axis:** White-box, editable core memory blocks; academic pedigree (UC Berkeley MemGPT); strong for single persistent conversational agents.
- **Biggest risk:** Tool-call reliability degrades with smaller/local LLMs; multi-agent Groups API had production failures as of Sep 2025.[^22][^31]
- **Self-host lift:** Moderate — Docker, PostgreSQL + pgvector, Ollama LM Studio integration available.[^1][^27]

### C — Zep / Graphiti
- **Strongest axis:** Temporal knowledge graph with deterministic deduplication (post-Nov 2025); uniquely good at "fact as of time T" reasoning; Graphiti MCP 1.0 is production-ready.[^11]
- **Biggest risk:** Zep CE frozen; Graphiti alone has no managed server equivalent; Neo4j Community adds ~1–2 GB RAM overhead; FalkorDB is lighter but less mature.[^3][^28]
- **Self-host lift:** Moderate-high — Neo4j or FalkorDB container + Ollama-compatible LLM for extraction (Qwen3:14b tested).[^26]

### D — Anthropic `memory_20250818`
- **Strongest axis:** Zero infra, first-class Claude integration, full privacy, native to the operator's existing stack.
- **Biggest risk:** No deduplication or contradiction resolution built in; scaling past ~200 memory files requires operator-built manifest logic; beta header dependency.[^5][^24]
- **Self-host lift:** Zero — implement `handle_memory()` once, share the `/memories/fleet/` path across all agents.

### E — Do-Nothing Baseline
- **Strongest axis:** Already running, zero additional setup, no new failure modes introduced.
- **Biggest risk:** Cross-agent propagation structurally absent (documented in claude-code issue #4588, Jul 2025); three-store coordination debt compounds as fleet grows.[^48]

---

## References

1. [Deploy a Letta server with Docker | Letta Docs](https://docs.letta.com/guides/docker/) - To install Docker, see Docker's installation guide. For issues with installing Docker, see Docker's ...

2. [Research blog - Letta](https://www.letta.com/blog-categories/research) - We're introducing Context Repositories, a rebuild of how memory works in Letta Code based on program...

3. [Announcing a New Direction for Zep's Open Source Strategy](https://blog.getzep.com/announcing-a-new-direction-for-zeps-open-source-strategy/) - We've decided to stop maintaining and releasing Zep Community Edition. The existing repository will ...

4. [Announcing a New Direction for Zep's Open Source Strategy | Zep AI (YC W24)](https://www.linkedin.com/posts/zep-ai_announcing-a-new-direction-for-zeps-open-activity-7313307679387488257-hDU0) - 👉️ We're announcing a New Direction for Zep's Open Source Strategy: The end of support for Zep Commu...

5. [Memory tool - Claude Docs](https://anthropic.mintlify.app/en/docs/agents-and-tools/tool-use/memory-tool)

6. [Agent makes tool calls to perform memory operations](https://x.com/helloiamleonie/status/1993356509930307627) - I've been exploring different dev tools for agent memory. Anthropic has a different approach than ot...

7. [Self-Hosted AI Companion - Mem0 Documentation](https://docs.mem0.ai/cookbooks/companions/local-companion-ollama) - By using Ollama, you can run Mem0 locally, which allows for greater control over your data and model...

8. [Self-Hosting Mem0: A Complete Docker Deployment Guide](https://mem0.ai/blog/self-host-mem0-docker) - Self-host Mem0’s AI memory stack in three Docker containers (API, Postgres + pgvector, Neo4j) to kee...

9. [ADD-only extraction in v3 may surface stale/contradictory facts for ...](https://github.com/mem0ai/mem0/issues/4956) - For facts representing a mutable state (e.g. current employer, current city, relationship status), t...

10. [Sarah Wooders, PhD's Post - LinkedIn](https://www.linkedin.com/posts/wooders_at-letta-we-treat-agent-memory-as-a-context-activity-7348065548393463809-pdUE) - At Letta we treat agent memory as a context engineer problem - see our latest blog post on agent mem...

11. [Graphiti Hits 20K Stars! + MCP Server 1.0 - Zep](https://blog.getzep.com/graphiti-hits-20k-stars-mcp-server-1-0/) - I used the Graphiti MCP server that runs 100% locally to cross-operate across AI apps like Claude De...

12. [Exploring Anthropic's Memory Tool - Leonie Monigatti](https://leoniemonigatti.com/blog/claude-memory-tool.html) - Learn how to build an example AI agent with persistent memory in Python using the Claude Developer P...

13. [Mem0: Building Production-Ready AI Agents with Scalable Long ...](https://arxiv.org/abs/2504.19413) - We introduce Mem0, a scalable memory-centric architecture that addresses this issue by dynamically e...

14. [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/pdf/2310.08560.pdf) - ...revolutionized AI, but are constrained by
limited context windows, hindering their utility in tas...

15. [Memory Blocks: The Key to Agentic Context Management - Letta](https://www.letta.com/blog/memory-blocks) - Memory blocks offer an elegant abstraction for context window management. By structuring the context...

16. [getzep/zep: Zep | Examples, Integrations, & More - GitHub](https://github.com/getzep/zep) - Zep is an end-to-end context engineering platform that delivers the right information at the right t...

17. [Graphiti + FalkorDB: Integration for Multi-Agent Systems](https://www.falkordb.com/blog/graphiti-falkordb-multi-agent-performance/) - Graphiti now supports FalkorDB as a graph database backend for multi-agent environments. This integr...

18. [Benchmarking Mem0's token-efficient memory algorithm](https://mem0.ai/research) - Benchmarked across LoCoMo, LongMemEval, and BEAM, achieves competitive accuracy while using under 7,...

19. [Revisiting Zep's 84% LoCoMo Claim: Corrected Evaluation & 58.44 ...](https://github.com/getzep/zep-papers/issues/5) - our analysis shows that Zep achieves 58.44 % accuracy—not the 84 % reported. This significant gap st...

20. [We Benchmarked Our AI Memory SDK. Is the Industry Standard Test Broken?](https://dev.to/vektor_memory_43f51a32376/we-benchmarked-our-ai-memory-sdk-is-the-industry-standard-test-broken-2b25) - A three-part story about retrieval engineering, grounding truth, and what 93% accuracy actually...

21. [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956) - We introduce Zep, a novel memory layer service for AI agents that outperforms the current state-of-t...

22. [MemGPT code is AAA+ unfortunately I cannot get it to work (no matter which LLM I try I cannot get it to work reliably) · Issue #1776 · letta-ai/letta](https://github.com/letta-ai/letta/issues/1776) - Hi MemGPT Team, Thank you for such a high quality codebase I'm pretty confident that, as LLMs will i...

23. [Zep: A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/pdf/2501.13956.pdf) - ...DMR that better reflect real-world enterprise use cases. While
existing retrieval-augmented gener...

24. [Claude code - file-based memory approach is actually kind of brilliant](https://www.reddit.com/r/LocalLLaMA/comments/1s9i9s4/claude_code_filebased_memory_approach_is_actually/) - Is it really better than full RAG pipelines though? I think for a simple tool it's pretty good but I...

25. [一招解决Claude API重启失忆问题，让你的Agent拥有灵魂。](https://www.youtube.com/watch?v=-O6SJEswdsg&list=PLQMuTJx7TfL0V9YVeueqq_cK2tIuVyG9Q) - 還在被 Claude「重啟就失憶」搞瘋？這支影片帶你用不到 100 行 Python 接上 ClaudeAPI 的 Memory Tool（memory_20250818），做出一個能記住你、能跨天接...

26. [Built a self-hosted mem0 MCP memory server for Claude Code ...](https://www.reddit.com/r/LocalLLaMA/comments/1r7gktw/built_a_selfhosted_mem0_mcp_memory_server_for/) - Built a self-hosted mem0 MCP memory server for Claude Code, Ollama handles embeddings locally, optio...

27. [LM Studio | Letta Docs](https://docs.letta.com/guides/server/providers/lmstudio/) - FYI Models labelled as MLX are only compatible on Apple Silicon Macs. The following models have been...

28. [FalkorDB Configuration - Zep Documentation](https://help.getzep.com/graphiti/configuration/falkor-db-configuration) - Configure FalkorDB as the graph provider for Graphiti. ... Docker Installation. The simplest way to ...

29. [falkordb/graphiti-knowledge-graph-mcp - Docker Image](https://hub.docker.com/r/falkordb/graphiti-knowledge-graph-mcp) - Graphiti is a framework for building and querying temporally-aware knowledge graphs, specifically ta...

30. [Anthropic adds persistent memory to Claude Managed Agents in ...](https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta) - Memories mount directly onto a filesystem, allowing Claude to use the same bash and code execution t...

31. [Issues 21](https://github.com/letta-ai/letta/issues) - Letta is the platform for building stateful agents: open AI with advanced memory that can learn and ...

32. [Tool reference - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference) - Directory of Anthropic-provided tools and reference for optional tool definition properties.

33. [What Is the Anthropic Claude Code Source Code Leak? Three ...](https://www.mindstudio.ai/blog/claude-code-source-leak-three-layer-memory-architecture/) - The three-layer approach (persistent files, active retrieval, background indexing) is a concrete arc...

34. [mem0/LICENSE at main · mem0ai/mem0](https://github.com/mem0ai/mem0/blob/main/LICENSE) - Universal memory layer for AI Agents. Contribute to mem0ai/mem0 development by creating an account o...

35. [GitHub - mem0ai/mem0: Universal memory layer for AI Agents](https://github.com/mem0ai/mem0) - Mem0 ("mem-zero") enhances AI assistants and agents with an intelligent memory layer, enabling perso...

36. [Trending AI Repositories on GitHub — Real-Time Rankings 2026](https://ossinsight.io/trending/ai) - Discover the top trending AI repositories on GitHub in 2026. Real-time rankings of AI agent framewor...

37. [letta-code/LICENSE at main - GitHub](https://github.com/letta-ai/letta-code/blob/main/LICENSE) - A permissive license whose main conditions require preservation of copyright and license notices. Co...

38. [Berkeley AI Research Lab Spinout Letta Raises $10M Seed Financing Led by Felicis to Build AI with Memory](https://www.prnewswire.com/news-releases/berkeley-ai-research-lab-spinout-letta-raises-10m-seed-financing-led-by-felicis-to-build-ai-with-memory-302257004.html) - /PRNewswire/ -- Letta, a new generative AI startup spun out of UC Berkeley's AI research lab, emerge...

39. [Letta Secures $10 Million Seed Funding Led By Felicis Ventures At ...](https://traded.co/vc/deal/letta-secures-10-million-seed-funding-led-by-felicis-ventures-at-70-million-valuation/) - Letta, an AI startup founded by Berkeley PhD students Sarah Wooders and Charles Packer, has emerged ...

40. [Letta Revenue 2025: $1.4M ARR, $4.3M Valuation](https://getlatka.com/companies/letta.com) - Letta 2025 revenue: $1.4M ARR. Valuation: $4.3M. Bootstrapped (no outside funding). 13 employees Upd...

41. [Letta Code: A Memory-First Coding Agent](https://www.letta.com/blog/letta-code) - Letta Code is built around long-lived agents that persist across sessions and improve with use. Rath...

42. [Jobs at Zep AI | Y Combinator](https://www.ycombinator.com/companies/zep-ai/jobs) - We're a seed-stage company (YC W24) with 50% month-over-month ARR growth, 240+ customers including F...

43. [Best Mem0 Alternatives in 2026: Benchmarks and Pricing - Atlan](https://atlan.com/know/mem0-alternatives/) - Graphiti has 20,000+ GitHub stars (milestone announced November 2025) and 25,000 weekly PyPI downloa...

44. [open-docs/docs/claude-agent-sdk/memory-and-context.md at main](https://github.com/bgauryy/open-docs/blob/main/docs/claude-agent-sdk/memory-and-context.md) - Important Clarifications: ❌ No Automatic Memory System - Claude Agent SDK does not have a built-in a...

45. [Automatically overwrite the out-of-date memory · Issue #5193 - GitHub](https://github.com/mem0ai/mem0/issues/5193) - Both of the two memories were added successfully, but I think the 1st one should be overwritten by t...

46. [[BUG] Mem0 memory search fails · Issue #2589 · crewAIInc/crewAI](https://github.com/crewAIInc/crewAI/issues/2589) - on Apr 11, 2025 · devin-ai-integration. added a commit that references this issue on Apr 11, 2025 · ...

47. [Anyone self-hosting Zep / Graphiti? Experiences & analytics setup?](https://www.reddit.com/r/Rag/comments/1s9pzd6/anyone_selfhosting_zep_graphiti_experiences/) - Hi all, I'm exploring building a fully self-hosted app using Zep / Graphiti as the memory and RAG la...

48. [Enable Persistent Memory and Learning for Specialized ...](https://github.com/anthropics/claude-code/issues/4588) - Title: Enable Persistent Memory and Learning for Specialized Agents Description: While Claude Code h...

