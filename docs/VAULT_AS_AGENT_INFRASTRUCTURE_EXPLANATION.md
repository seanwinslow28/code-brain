# EXPLANATION — Vault as Agent Infrastructure

> 4Q artifact for the [`SCORECARD.md`](../vault/SCORECARD.md) + [long-form essay](VAULT_AS_AGENT_INFRASTRUCTURE.md). Companion to the architecture-writeup genre: the four questions a reviewer should be able to answer after reading the artifact.

## What is this?

A five-test architectural argument that scores four knowledge systems — Notion, default Obsidian, Linear, and my own vault — against Nate Jones's structural tests for agent infrastructure: persistent state, defined verbs, ownership, permissions, and queryable audit history. The verdict is three passes and two honest losses: the vault scores above Linear on persistent state, defined verbs, and audit history, and loses to Linear on ownership and permissions. Every cell is backed by live telemetry from `vault/.vault-index.db` (632 typed edges across ~110 nodes, 15,582 indexed chunks, six SQL-enforced relations), regenerable with [`scripts/generate_schema.py`](../scripts/generate_schema.py).

## Why this approach?

Nate's five-test framing is the load-bearing recruiter vocabulary for agent-infrastructure work in 2026. Scoring against an external standard is faster and more credible than inventing my own rubric — it's citing a yardstick instead of grading my own homework. Building the comparison first also earns the right to ship `vault-knowledge-mcp` as "the MCP wrapping the only public PM vault that passes the agent-infrastructure tests," with the scorecard as the prior-art document, so the MCP launch isn't stuck answering "why does this exist?" The two honest losses are deliberate: Linear genuinely beats POSIX file permissions on ownership and RBAC, and naming that calibrates the whole artifact's credibility upward.

## What would break?

Two failure modes. First, **fixture / telemetry drift**: the numbers in the scorecard are a snapshot, so they go stale as the synthesizer runs nightly (they already moved from 478 edges to 632 in nine days). Mitigation: the numbers are regenerable on demand from the live schema via `generate_schema.py --self-test` plus a live run, so the artifact is refreshable rather than hand-maintained. Second, **reading my own architectural arguments as truth when they're really claims** — a scorecard I author about my own system is structurally self-serving. Mitigation: the explicit Linear-wins-here callouts are the check; an argument that names where it loses is harder to dismiss than one that wins every cell.

## What did I learn?

Most "agent infrastructure" claims fail the persistent-state test on day one — the moment you ask "does the structured state survive a crash without a recovery procedure," most setups turn out to be tool integrations with a session-scoped memory, not infrastructure. The test discriminates, which is exactly why it's worth scoring against. The second lesson came from the permissions axis: the closer for that gap — the Judge Layer, a control-plane interceptor with typed action proposals, declarative policy, and an append-only decision ledger — was already built and tested, which reframed that "loss" from a someday into a rollout. The losses that are most useful are the ones whose fix is already on disk.
