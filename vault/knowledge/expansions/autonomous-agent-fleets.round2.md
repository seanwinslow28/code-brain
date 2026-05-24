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

1. **Add “Saga / Compensation Mode” for agent-fleet failure recovery**

   Anchor it on Hector Garcia-Molina and Kenneth Salem’s paper **“Sagas” (1987)**.

   Your current concept treats failure as stale context propagation. What’s missing is the distributed-systems pattern for *long-running workflows where rollback is impossible*. A nightly agent fleet is not a transaction; it is a saga. Each agent step needs a forward action, a compensating action, and a declared point of no return.

   Sentence pattern to add:

   > “Every autonomous agent action should declare its compensating action, its idempotency key, and the context boundary after which repair becomes a new forward action rather than rollback.”

   This unlocks a **fleet recovery runbook** or **agent spec template**: `step`, `side effect`, `observable receipt`, `compensation`, `retry policy`, `staleness budget`. Right now the article can say “silent failure is bad.” Saga mode lets Sean specify what the system should *do after partial success*.

2. **Add “Common Knowledge Failure” as the missing coordination problem**

   Anchor it on C. A. R. Hoare’s **“Communicating Sequential Processes” (1978)** and Leslie Lamport’s **“Time, Clocks, and the Ordering of Events in a Distributed System” (1978)**.

   The current article assumes shared state solves coordination if agents read/write it correctly. The harder problem is that agents may not know what other agents know, what they have seen, or whether a prior write is causally fresh. Daily notes are not just storage; they are a weak coordination substrate.

   Sentence pattern to add:

   > “A context write is not coordination until downstream agents can distinguish fresh, stale, absent, superseded, and disputed state.”

   This unlocks an **Agent Fleet Observability Dashboard** design that tracks causal freshness rather than just health: last-seen context version, upstream dependency version, write receipt, read receipt, and “acting on stale context” warnings. It also gives Sean a sharper Substack essay: not “my agents need memory,” but “my agents need common knowledge.”

3. **Add “Control Plane vs. Data Plane” to separate agent behavior from agent governance**

   Anchor it on Brendan Burns, Brian Grant, David Oppenheimer, Eric Brewer, and John Wilkes’ paper **“Borg, Omega, and Kubernetes” (2016)**.

   The concept currently blends agent work, shared context, scheduling, health, and repair into one blob called a fleet. Kubernetes’ useful lesson is not “use Kubernetes”; it is the split between desired state, controllers, reconciliation loops, and workload execution. Sean’s launchd agents are the data plane. The missing artifact is a control plane.

   Sentence pattern to add:

   > “An autonomous fleet needs a reconciler that compares desired knowledge state against observed vault state, then emits repairs, quarantines, or re-runs.”

   This unlocks an **executable demo** or **portfolio one-pager**: “Personal Agent Control Plane for a Knowledge Vault.” It could show desired state specs, agent status, drift detection, reconciliation actions, and audit logs. The current concept reaches “agents can fail silently.” Control-plane framing reaches “here is the architecture that notices drift and converges the system.”

## From Anti-Gravity (Gemini 3)

### 1. Supervisor Trees and the "Let It Crash" Philosophy
**WHAT to add:** Shift the failure paradigm from passive "health monitoring" of a shared blackboard to active "Supervisor Trees" where agents are strongly isolated actors with defined restart strategies. 
**WHO/WHAT exemplifies it:** Joe Armstrong’s PhD thesis, *Making reliable distributed systems in the presence of software errors* (2003), which formalized Erlang's OTP architecture.
**WHAT this would unlock for Sean:** An architectural RFC artifact for your `intent-engineering` MCP server. You currently treat read/write agent failures as state-corruption anomalies; Armstrong treats them as inevitable lifecycle events. Writing this RFC lets you produce a senior AI-PM portfolio piece demonstrating how to migrate Code-Brain from a fragile filesystem-polling architecture into a self-healing actor hierarchy, proving you can bridge classic distributed systems theory with modern LLM orchestration.

### 2. The Saga Pattern for Agentic Transactions
**WHAT to add:** Distributed transactions via Sagas. Your concept stops at "silent failure leaves stale data." Sagas acknowledge that distributed systems lack global locks, requiring every forward action to have a paired, programmatic rollback (a compensating transaction) if downstream steps fail.
**WHO/WHAT exemplifies it:** Hector Garcia-Molina and Kenneth Salem’s 1987 database paper, *Sagas*.
**WHAT this would unlock for Sean:** An executable Python feature in your Agents SDK. By forcing a `compensating_action()` callback into your base agent class, you unlock a highly technical Substack tutorial (in the Sean-default IC voice) demonstrating how to build an agent pipeline that cleanly rolls back a half-written daily note when an LLM context-window fails, rather than abandoning the workspace in a corrupted state.

### 3. Justification-Based Truth Maintenance Systems (JTMS)
**WHAT to add:** Epistemic dependency tracking. Your agents acting on "stale data" is an epistemic failure. A JTMS tracks *why* an agent generated an output by mapping it strictly to the upstream context state at the exact time of inference.
**WHO/WHAT exemplifies it:** Jon Doyle’s foundational AI paper, *A Truth Maintenance System* (1979).
**WHAT this would unlock for Sean:** A new SQLite-backed metadata graph for Code-Brain. Instead of just logging outputs, you tag agent decisions with their context dependencies. If an upstream note is altered, the JTMS automatically invalidates downstream outputs based on those now-false premises. This unlocks a Gonzo/Thompson-mode Substack piece attacking the "schizophrenic hallucinations of stateless multi-agent cartels," followed by a link to your working code that makes agentic reasoning causally traceable.
