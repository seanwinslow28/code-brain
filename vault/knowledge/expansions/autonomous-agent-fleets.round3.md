---
title: "How to make `Autonomous Agent Fleets` better"
type: expansion
parent: "[[autonomous-agent-fleets]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[autonomous-agent-fleets]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Saga / Compensating Action” as the failure model**
   - **Anchor:** Hector Garcia-Molina and Kenneth Salem, “Sagas” (1987).
   - **What to add:** Treat an agent fleet as a long-lived transaction system where each agent action needs an explicit compensating action, not just a health check. Sentence pattern: “If Agent A writes state X and Agent B depends on it, then failure recovery is not retry; it is either compensate, quarantine, or roll forward.”
   - **Unlocks:** A concrete **agent runbook / architecture spec** for Sean’s launchd fleet: per-agent preconditions, committed outputs, downstream dependencies, and rollback/compensation behavior. The current concept says “silent failures propagate”; Saga thinking lets him specify what happens after propagation is detected.

2. **Add “Supervisory Control” as the coordination theory**
   - **Anchor:** P. J. Ramadge and W. M. Wonham, “Supervisory Control of a Class of Discrete Event Processes” (1987).
   - **What to add:** Model the fleet as a discrete-event system with forbidden states and a supervisor that disables unsafe transitions. This is sharper than “agents coordinate via shared state.” Sentence pattern: “The fleet is not a team; it is an event system whose unsafe transitions must be made unreachable.”
   - **Unlocks:** An **intent-engineering MCP demo** where Sean defines agent autonomy declaratively: allowed events, forbidden transitions, stop rules, and escalation states. This gives him a portfolio artifact beyond “I run scheduled agents” and connects directly to his “intent engineering” thesis.

3. **Add “Control Plane vs Data Plane” to separate orchestration from knowledge**
   - **Anchor:** Martin Kleppmann, *Designing Data-Intensive Applications*, especially the chapters on replication, distributed systems, and fault tolerance.
   - **What to add:** Split the concept into two layers: the **data plane** is vault content, notes, manifests, embeddings, daily notes; the **control plane** is schedules, leases, locks, health checks, budgets, and routing decisions. Sentence pattern: “A vault note is not a coordination primitive unless the control plane can prove freshness, ownership, and write completion.”
   - **Unlocks:** A strong **Substack essay / portfolio one-pager**: “My Obsidian vault is the data plane; launchd plus manifests are the control plane.” That framing makes the system legible to infra-minded hiring managers and prevents the concept from sounding like generic “multi-agent shared memory.”

## From Anti-Gravity (Gemini 3)

### 1. The Saga Pattern for Agentic Rollbacks
- **WHAT to add:** The Saga Pattern (compensating transactions) for handling distributed state failures. Your current concept identifies the problem ("failures in one agent's ability to read or write context can propagate silently") but relies on "Agent Health Monitoring" (passive observation). Sagas provide an active, programmatic rollback mechanism where every agent action (e.g., Vault Synthesizer creating a file) requires a paired, pre-written compensating action (e.g., deleting that file if the downstream Vault Critic fails).
- **WHO/WHAT exemplifies it:** Hector Garcia-Molina and Kenneth Salem’s 1987 paper *Sagas* (ACM SIGMOD), and its modern implementation in AWS Step Functions or the temporal.io architecture.
- **WHAT this unlocks:** This unlocks the ability to ship a **"Self-Healing Agent SDK" GitHub release**. Right now, your launchd fleet requires manual intervention when a pipeline breaks mid-stream. Implementing Sagas allows you to write an IC architectural blueprint (RFC) demonstrating how local agent fleets can safely mutate shared state (like an Obsidian vault) with guaranteed rollback consistency, moving your portfolio from "scheduled scripts" to "distributed systems engineering."

### 2. Supervisor Trees and the "Let It Crash" Philosophy
- **WHAT to add:** The Erlang OTP Supervisor Tree model. Instead of building complex inline error handling or relying on your 8:45 AM `Meta-Agent` to passively report fleet health, you structure the fleet hierarchically. A lightweight supervisor agent launches worker agents; if a worker (like the `Deep Researcher` timing out) crashes, the supervisor explicitly handles the failure policy (e.g., One-for-One restart, or One-for-All kill-and-restart of the entire research pipeline) rather than letting stale state propagate.
- **WHO/WHAT exemplifies it:** Joe Armstrong’s PhD thesis, *Making reliable distributed systems in the presence of software errors* (2003), specifically the chapters detailing the OTP framework and the "Let it crash" philosophy.
- **WHAT this unlocks:** This unlocks a **Substack technical essay ("Why Agent Fleets Need Erlang's 20-Year-Old Playbook")**. You currently sound like a PM describing fragile cron jobs. Applying supervisor trees lets you authoritatively critique modern AI orchestration frameworks (like LangChain/CrewAI) for lacking foundational distributed-systems resilience, positioning you as an IC who understands durable systems architecture, not just LLM API wrappers.

### 3. Tuple Spaces (The Blackboard Pattern) for Decoupled Context
- **WHAT to add:** Tuple Spaces for asynchronous, decoupled agent communication. Your fleet currently uses tightly coupled linear batons (Agent A writes `vault/knowledge/index.md` -> hook injects it -> Agent B reads it). A Tuple Space acts as a shared, concurrent blackboard (backed by your existing SQLite `.vault-index.db`) where agents asynchronously "produce" and "consume" structured tuples (e.g., `["research_task", "status:pending", payload]`) without knowing which agent will process them, entirely eliminating the "Daily note exists: No" race conditions.
- **WHO/WHAT exemplifies it:** David Gelernter and Nicholas Carriero's 1985 paper *Generative Communication in Linda* (ACM Transactions on Programming Languages and Systems).
- **WHAT this unlocks:** This unlocks a **live executable demo and accompanying PRD** for an asynchronous, event-driven agent architecture. Instead of waiting for a linear nightly batch run, your Mac Mini and MacBook Pro agents can pull tasks from the SQLite tuple space whenever they have idle compute. This allows you to ship an artifact proving you can design non-blocking, multi-node AI systems, a critical signal for senior AI-IC roles.
