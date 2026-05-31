---
artifact: judge-layer
created: 2026-05-31
surface: control-plane
shipped: 2026-06-04
repoUrl: https://github.com/seanwinslow28/code-brain/tree/main/agents-sdk/lib/judge
ai-context: "Comprehension artifact for the judge layer (Council Gap-Fill 1 / Task 12). 4-question template per Nate B Jones / ADR convention. Related: agents-sdk/agents/substack_drafter.py (wrap target), agents-sdk/policies/substack_drafter.yaml (policy), agents-sdk/lib/judge/{schema,policy,judge,ledger,action}.py."
---

# Judge Layer — Explanation

## What is this?

A control-plane interceptor that sits between a production agent's *intent* and its *action*. The agent emits a typed `ActionProposal` (what it wants to do, where it lands, what would undo it, plus the draft itself); the judge evaluates that proposal against a declarative YAML policy and returns one of five outcomes — `ALLOW`, `REVISE`, `BLOCK`, `ESCALATE`, or `JUDGE_UNAVAILABLE`. It runs on a local model (`gemma4:e4b` on a Mac Mini) at $0 per decision, and writes every verdict to an append-only JSONL ledger the fleet dashboard reads. The first wrapped agent is the Substack-Drafter: drafts that fabricate a quote get quarantined, drafts that lean on uncited employer facts get sent back for a citation, and drafts that try to publish themselves get blocked — while a healthy draft passes straight through to my manual review.

## Why this approach?

Three options for adding control to the fleet. **(1)** Retrofit all eight agents at once — rejected; too much surface for a v0, and most agents don't take risky actions. **(2)** Put the rules in Python inside each agent — rejected; the rules become invisible to anyone who doesn't read code, and a CISO or recruiter can't audit them. **(3)** Intercept one agent, with the rules in a YAML policy a non-engineer can read — chosen. The actor-judge separation is the architecture; the policy file is the contract. The accepted trade-off is **fail-open**: if the judge model is unavailable, the wrapped agent falls back to my manual review rather than blocking. I chose that deliberately — my "agents draft / I send" gate is the canonical control, so the judge is defense-in-depth, and cadence preservation beats a theoretical bypass that my own review already catches.

## What would break?

- **The judge can't see what it's judging.** The original schema carried only metadata — eight fields *about* the action, none holding the draft text the rules actually read. Caught on the Day-6 wire-up: every policy rule says "the draft…," but the draft never reached the prompt, so the judge would silently fall through to `ALLOW`. Detection signal: a judge that *never* fires a rule on adversarial input is broken, not clean. Fix: a `content_preview` field carries the (truncated) draft into the proposal — and the ledger row now records exactly what produced each verdict.
- **Policy drift from the actual code paths.** If the YAML names a rule the agent can no longer trigger, the control is theater. Detection: an integration test loads the real policy and asserts the rule count and outcome distribution, so a silent rule deletion fails CI.
- **The judge becomes the bottleneck.** A `REVISE` loop with no ceiling could spin forever or burn cost. Detection: a bounded retry (default 2) that escalates to a quarantine folder instead of looping, plus a per-decision latency field on every ledger row so a slow judge shows up as a trend, not a surprise.

## What did I learn?

The distance between "an agent that writes" and "an actor inside a control architecture" is almost entirely *legibility*, not capability — one Pydantic schema plus one YAML policy turns existing behavior into something auditable. The non-obvious part: the most valuable field in the whole system was the one that didn't exist yet. Wiring the judge into a real agent exposed that the schema had no channel for the artifact under review — a gap the unit tests had hidden by mocking the model's response. Integration is where you find out whether your abstraction can actually see the thing it claims to govern.
