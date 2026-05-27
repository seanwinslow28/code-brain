---
title: "Topic 27 — Long-Term Memory Backends (Cross-Vendor Synthesis)"
date: 2026-05-27
type: research-synthesis
status: canonical
topic_id: 27
sources:
  - "[[2026-05-26-topic-27-long-term-memory-backends-gemini-dr-manual]]"
  - "[[2026-05-26-topic-27-long-term-memory-backends-perplexity-dr-manual]]"
decision: adopt-anthropic-memory-20250818
confidence: high
tags:
  - research/synthesis
  - agent-memory
  - self-improving-agents
---

# Topic 27 — Long-Term Memory Backends: Cross-Vendor Synthesis

Two independent research runs (Gemini Deep Research + Perplexity Deep Research, same prompt, 2026-05-26 to 2026-05-27) on the same five-option matrix (Mem0 / Letta / Zep / Anthropic native / do-nothing). Both arrived at the **same recommendation by independent reasoning paths**. That convergence is the highest-confidence signal this synthesis carries.

## The Decision

**Adopt Anthropic's native `memory_20250818` tool, mounted at a shared `/memories/fleet/` directory readable by all 27 agents.** Both vendors picked this independently. Both gave nearly identical migration paths. Treat this as a high-confidence call, not a hedged one.

## Where the Two Reports Converge (High Confidence)

The following findings appeared in both reports with consistent citations. Treat these as load-bearing facts for the decision:

1. **Anthropic `memory_20250818` is the right answer for this operator profile right now.** Zero infrastructure, native first-class Claude integration, full privacy, output is human-readable markdown that integrates cleanly with the existing Obsidian PARA structure. The computational cost of memory synthesis is offloaded to Anthropic's inference path — no local RAM tax beyond filesystem I/O.

2. **Mem0's implicit-extraction write-path has documented production failures.** Both reports cite mem0 GitHub issue #4573 (97.8% junk extraction rate over 32-day production audit, 808 duplicate entries from a self-amplifying hallucination loop) and issue #4956 (ADD-only pipeline in v3 means contradictory facts accumulate instead of superseding). Gemini emphasizes the audit numbers, Perplexity adds issue #5193 ("I like coffee" + "I no longer like coffee" both stored with near-equal scores). Both reach the same conclusion: don't trust background-LLM extraction without an explicit mutation pass.

3. **Zep Community Edition is frozen as of April 2025.** Graphiti is the active OSS path. Both reports agree that self-hosting Graphiti on Apple Silicon requires Neo4j or FalkorDB containers + an LLM extraction pipeline — operational overhead that doesn't pay off for a 27-agent fleet without genuine temporal-reasoning requirements.

4. **The current three-store baseline is rational scaffolding but architecturally insufficient.** Both reports identify the structural failure mode: lessons learned by one agent cannot propagate to the other 26. Perplexity cites Claude Code issue #4588 (Jul 2025) explicitly documenting that subagents are stateless and "domain expertise must be re-explained in every Task tool invocation." Gemini frames it as "state-fragmentation actively prevents cross-agent learning."

5. **The migration path is the same in both reports.** Subclass `BetaAbstractMemoryTool` (Anthropic Python SDK), point all SDK + Claude Code agents at a shared `/memories/fleet/` path, enforce sub-directory namespacing for multi-agent isolation, keep Obsidian vault RAG as a separate read-only knowledge tier (vault notes are too large for the memory-file pattern).

6. **Switch to Mem0 OSS only when the fleet grows past ~50 agents OR cross-entity relational queries become first-class needs.** Both reports name the same threshold and the same trigger. The operator's existing nomic-embed-text Ollama instance is already compatible with Mem0's local config — the integration lift later will be low.

7. **All published LoCoMo / LongMemEval numbers are vendor-self-reported and contested.** Both reports surface the same dispute (Zep-papers issue #5, May 2025) and the same correction (Zep 84% → 75.14%, Mem0 92.5% → ~66% under standardized harness). Perplexity also surfaces dev.to/vektor_memory's April 2026 audit finding "serious methodological issues" in the LoCoMo dataset itself. Treat all retention-quality benchmarks as directional signals, not ground truth.

## Where the Two Reports Diverge (Uncertainty Markers)

These deltas are worth resolving before betting big. Listed by importance:

### Letta LoCoMo score
- **Gemini:** Cites an independent eval at 74.0% on LoCoMo with pure filesystem operations (Letta blog post "Benchmarking AI Agent Memory: Is a Filesystem All You Need?", attributed source).
- **Perplexity:** Explicitly states no published LoCoMo benchmark exists for Letta's current architecture as of mid-2026.
- **Resolution:** Perplexity's claim is more defensible — the Letta blog post referenced is a vendor write-up, not a peer-reviewed eval. Treat 74% as a directional vendor claim, not an independent result.

### Mem0 escape hatch: the Differential Memory Engine (DME)
- **Gemini:** Surfaces mem0 issue #4978 as a community proposal for a "Zero-DB Overhead via Serverless WFA & JSON" local deployment mode — bypasses Qdrant/Neo4j entirely, uses NumPy + SciPy + flat JSON for state. Mathematical novelty threshold (0.85 cosine) prevents recursive bloat.
- **Perplexity:** Doesn't mention DME at all — only describes the standard Docker stack (Qdrant + Neo4j + Ollama).
- **Resolution:** This is a real Gemini value-add. If the operator ever reconsiders Mem0, DME is the right starting point for an Apple-Silicon-friendly local config, not the production Docker stack. Worth a follow-up read.

### Severity framing of Mem0's known failures
- **Gemini:** Cites the 97.8% junk rate as catastrophic; explicitly notes the rate did NOT decrease when upgrading the extraction model from a small local instance to Sonnet 4.6 ("the superior model simply followed the permissive extraction prompts more faithfully").
- **Perplexity:** Cites the same data but treats it as "biggest risk right now" rather than disqualifying — leaves room for Mem0 as the Phase 2 backend once issue #4956 is fixed.
- **Resolution:** Both framings are defensible. The Gemini framing implies "don't trust the architecture even with a frontier model"; Perplexity's implies "wait for the bugfix." For the immediate Phase 1 decision (adopt Anthropic native), this doesn't matter — both reports agree Mem0 is not the right Phase 1 choice. For Phase 2 trigger logic, lean Gemini: monitor whether the architectural extraction pattern improves, not just whether specific issues close.

### Security framing
- **Gemini:** Highlights Zep/Graphiti's prompt-injection vulnerability via external tool sources (issue #1466 — malicious `<system-reminder>` directives in fetched HTML get baked into the graph as persistent directives).
- **Perplexity:** Highlights Anthropic memory tool's path-traversal vulnerability (developer video documented an agent reading `.env` outside `/memories` without `realpath + prefix check`).
- **Resolution:** Both vulnerabilities are real and both belong in the threat model. The Anthropic-native one is more actionable because the operator owns the `handle_memory()` implementation; the Zep/Graphiti one is harder to mitigate because it's in the extraction pipeline. Add `realpath + prefix check` to the Phase 1 implementation as a non-negotiable.

## Vendor-Specific Value-Add

What each report uniquely surfaced (not in the other):

**Gemini contributed:**
- The implicit-vs-explicit memory philosophy frame (parallel-extraction systems amplify hallucinations because they lack the primary agent's contextual awareness)
- Specific Apple Silicon RAM math: 8–14 GB for the local 14B model + KV cache leaves limited headroom for JVM-based graph databases
- The DME (issue #4978) escape hatch for Mem0
- Concrete junk-source breakdown from the Mem0 audit (52.7% system-prompt re-extraction, 11.5% cron output, 8.2% config dumps)

**Perplexity contributed:**
- The "manifest-then-top-5" retrieval pattern for Anthropic native memory scaling past ~200 files (r/LocalLLaMA, April 2026)
- Letta funding context ($10M seed from Felicis, $70M post-money, 13 employees, $1.4M ARR — useful for evaluating maintenance-signal risk)
- Graphiti MCP Server 1.0 details (Nov 2025, 100k+ weekly users) — most natural fit for Claude Desktop / Code multi-client setups
- The Claude Code issue #4588 citation that names the cross-agent propagation problem explicitly
- Phased week-by-week migration plan with promotion logic from `~/.claude/projects/` auto-memory to shared fleet memory

## Concrete Next Steps for Code-Brain

The plan that survives both reports' scrutiny, tied to Sean's actual fleet topology:

### Phase 1 (this week — pilot)
1. Implement a shared `agents-sdk/lib/fleet_memory.py` helper that subclasses `BetaAbstractMemoryTool`. ~50–80 lines. Mount point: `vault/90_system/fleet-memory/` (inside the vault so it gets the shell-level auto-commit hook for free — issue #22 sync rule still applies).
2. Mandatory hardening: `realpath + prefix check` against the mount point root; reject any path that escapes via `..` or symlinks. This is the path-traversal mitigation both reports flag.
3. Sub-directory namespacing: each agent writes to `fleet-memory/{agent_id}/` for its own state; reads from `fleet-memory/shared/` for cross-fleet lessons. Promotion from agent-local to shared is explicit (a tool call), not automatic.
4. Pilot on two agents: `vault_synthesizer` and `daily_driver` (morning). Both already have failure modes worth remembering — synthesizer's stale-checkout incident (PR #52), daily-driver's MBP-not-awake fallback path.

### Phase 2 (within 30 days — fleet rollout)
5. Migrate per-domain CLAUDE.md "do not do X" sections into `fleet-memory/shared/feedback/`. Keep CLAUDE.md for durable architectural context; move corrections to the memory layer where they can be updated programmatically by the agents that learned them.
6. Add a `MEMORY_INDEX.md` manifest at the mount root that each agent updates with a one-line summary of new writes — enables the manifest-then-top-5 retrieval pattern Perplexity surfaced for scaling past ~200 files.
7. Decide whether to deprecate Claude Code's `~/.claude/projects/.../memory/` auto-memory or keep it running in parallel. Recommendation: keep in parallel for one month, then audit which store accumulated more useful entries and consolidate.

### Phase 3 (deferred until trigger)
8. Re-evaluate Mem0 OSS when: (a) fleet grows past ~50 agents, OR (b) mem0 issue #4956 (ADD-only extraction) is fixed AND independently verified, OR (c) cross-entity relational queries become a first-class need ("which agents have hit Tool X's rate limit?"). Use DME (issue #4978) as the local config starting point, not the production Docker stack.
9. Re-evaluate Graphiti when: (a) temporal queries become first-class ("what did vault_critic believe about file X last month?"), OR (b) Anthropic memory tool's lack of deduplication becomes a maintenance burden. Graphiti MCP Server is the most natural integration path.

## Risk Register

Carried forward from both reports for the Phase 1 implementation:

| Risk | Source | Mitigation |
|------|--------|------------|
| Path traversal (agent reads `.env`) | Perplexity (developer video, Apr 2026) | `realpath + prefix check` in `fleet_memory.py` — non-negotiable |
| Cross-agent data bleeding (Agent A corrupts Agent B's state) | Both reports | Per-agent sub-directory namespacing; promotion to shared is an explicit tool call |
| Beta header dependency (`context-management-2025-06-27`) | Perplexity | Pin SDK version; monitor Anthropic's GA timeline for the memory tool |
| Scale past ~200 memory files degrades retrieval | Perplexity (r/LocalLLaMA, Apr 2026) | Implement manifest-then-top-5 from day one, not as a later optimization |
| No built-in deduplication or contradiction resolution | Both reports | Document this as a known limitation; defer dedup to Phase 3 / Mem0 migration if it becomes a real problem |
| Mem0 v3 ADD-only bug (issue #4956) blocks Phase 3 trigger | Both reports | Monitor issue close; do not migrate to Mem0 until verified fixed |

## Source Attribution

- **Gemini DR (manual web UI run):** [[2026-05-26-topic-27-long-term-memory-backends-gemini-dr-manual]] — heavy on architectural philosophy framing + Mem0 audit detail + DME escape hatch
- **Perplexity DR (manual web UI run):** [[2026-05-26-topic-27-long-term-memory-backends-perplexity-dr-manual]] — heavy on citation traceability + funding/maintenance signals + scaling patterns + week-by-week migration plan

Both runs were  (manual via paid subscriptions, no API spend against the Gemini cap).

## Re-evaluation Triggers

Per the standing rule that this kind of decision is perishable, re-run this synthesis if any of the following land:

- Anthropic ships a breaking change to `memory_20250818` (e.g., GA replacement, schema change, or beta-header removal that changes behavior)
- mem0 issue #4956 closes with an independently verified fix
- Letta publishes a peer-reviewed LoCoMo result (the 74% claim becomes substantive rather than directional)
- Graphiti ships a managed-server analog of Zep CE that's self-hostable on Apple Silicon without Neo4j/FalkorDB
- The fleet crosses 50 agents
