---
title: "Systemcraft bench composition — research findings (L7 gate)"
date: 2026-08-22
project: systemcraft
status: ratified-2026-08-22
tags: [research, systemcraft, multi-agent, bench-composition]
cost: $0 (last30days local lanes + web research; no paid research invoked)
---

# Systemcraft bench composition — findings brief

**Gate:** L7 — the five-seat bench is a baseline hypothesis; this pass ratifies, grows, or shrinks it before build.

**Method ($0):** three last30days passes (Reddit / X / YouTube / HN, last 30 days of field practice) + a web-research sweep of primary sources: Anthropic's multi-agent research system writeup, the MAST failure taxonomy (Berkeley, 1,600+ annotated traces), Google Research's agent-scaling study, Cognition's "Don't Build Multi-Agents," OpenAI's agent-building guide, the LLM self-correction literature, and CrewAI/Claude Code role-design guidance.

## Headline recommendation

**Keep the five seats. Do not add a standing sixth Red-Team seat. Amend the draft-and-audit rule: audits run in a fresh session that never sees the drafting context, and cross-seat audit is preferred where lanes touch.**

## Findings

### 1. Five is at the top of the sensible range — and the seats earn their chairs by being different
- Fresh field practice converges on the same number: "three to five teammates, don't go for massive agent swarms of 10+" (Nate Herk, YouTube, 290K views). Same range in Claude Code agent-teams practice generally.
- Empirically, adding agents helps only while each new agent brings a *different* kind of knowledge; redundant agents add coordination cost without capability (arXiv 2602.03794, "diversity delays saturation"). The five lifecycle lanes (framing / architecture / trust / evals / ops) are genuinely distinct knowledge domains — this is the good kind of five.
- Community warning worth keeping on the wall: "At what point does a multi-agent workflow become middle management?" (r/AI_Agents). Every seat added past five buys mostly coordination tax.

### 2. The bench must run as a pipeline, not a parallel panel
- Google Research's scaling study: multi-agent setups gain up to +81% on *parallelizable* work but **lose 39–70% on sequential-reasoning work**; independent agents amplify errors 17.2x vs 4.4x under central coordination.
- Systemcraft's lifecycle is sequential (frame → architect → trust-design → eval → ops), so the orchestrating session routes work seat-to-seat and passes **full artifact context** forward (Cognition: "share full agent traces, not just individual messages"). Parallelism is fine for read-only research inside a seat's turn — the Factory "Missions" production pattern (serial features, parallel read-only ops) and Cole Medin's "contract-first spawning" both confirm.
- Anthropic's orchestrator-worker system beat single-agent by 90.2% *on parallelizable research* at ~15x token cost — the pattern wins only where the work actually decomposes.

### 3. Where multi-agent systems actually fail (MAST, 1,600+ traces)
- Specification issues 41.8% (vague task specs, step repetition), inter-agent misalignment 36.9% (context not shared, no clarifying questions), verification failures 21.3%.
- "Disobey role specification" is nearly nonexistent (0.5%) — **lanes fail at the task-spec level, not the persona level**. The build effort should go into per-seat artifact contracts (what each seat receives, produces, and hands off), not elaborate personas. CrewAI's doctrine agrees: task design deserves ~4x the effort of agent design.
- The single highest-leverage fix MAST measured: multi-level verification that checks artifacts against original task objectives (+15.6%). That is the Evals & Evidence seat pointed inward at the bench itself — an argument for that seat, not a new one.
- Field echo: the top-voted failure in r/ClaudeCode's multi-agent guide (204 pts) is *output dispersion* — work scattering with no single record. "The thing that actually mattered was the message bus, not the agents" (r/AI_Agents, 8 months in production). The **decision ledger is load-bearing infrastructure**, not a nice-to-have.

### 4. Draft + audit needs one amendment (strongest single finding)
- LLMs auditing their own work *in the same context* is the empirically weakest configuration: intrinsic self-correction degrades or flatlines performance (Huang et al., arXiv 2310.01798; TACL survey 2406.01297). Generator and evaluator sharing context share error distributions.
- The direct test (Cross-Context Review, arXiv 2603.12123): same-model review **in a fresh session with no production history** beat same-session review, repeated self-review, and even different-model review (p≤0.008). The gain comes from *context separation*, not extra passes or a different model.
- Production echo: Factory's validators "have never seen the code before... validation is adversarial by design."
- **Amendment:** each seat keeps draft AND audit duties in its lane, but an audit is always a *fresh invocation* that never sees the drafting conversation. Where lanes touch, prefer cross-seat audit (e.g., Evals audits Architecture's ADR) for added error-distribution diversity. This is a one-line rule in each seat's definition — cheap to enforce in Claude Code, since subagent invocations are fresh-context by default.

### 5. Red-Team: a protocol, not a person
- Evidence favors adversarial *passes* in fresh context over a standing sixth seat. A persistent adversarial participant accumulates shared context and consensus pressure — sycophancy propagates between agents ("Too Polite to Disagree," arXiv 2604.02668), panels converge on wrong answers together, and extra debate rounds can entrench errors (arXiv 2509.05396). Structural insulation is what makes adversarial review work, and a standing conversational seat erodes exactly that.
- Recommended design: a **red-team protocol** — a reusable adversarial checklist/prompt any seat's auditor runs statelessly — plus a cross-cutting adversarial gate pass at major milestones (PRD sign-off, pre-launch) that attacks the whole design, invoked fresh each time. No sixth roster seat.
- Honestly flagged: no controlled study compares "standing red-team seat" vs "per-artifact adversarial pass" head-to-head; this recommendation triangulates from the self-correction and sycophancy literature plus production practice.

### 6. Judge design (feeds the Evals seat's own craft)
- Anthropic found a single LLM judge with a multi-criterion rubric more consistent than multi-judge panels; human spot-checks still catch what automation misses. Start eval suites at ~20 representative cases.

## Evidence strength

- **Strong** (multiple independent empirical sources): diminishing returns / task-structure dependence; MAST taxonomy; self-correction weakness + fresh-context fix; sycophancy in debate; pipeline-over-panel for sequential work.
- **Moderate**: Cross-Context Review specifics (single paper, small n, directionally consistent with the broader literature); single-judge-over-panel (one team's experience).
- **Weak** (opinion/uncited): CrewAI's "45% error reduction" vendor claim; the exact 80/20 task-vs-agent ratio; standing-adversary advocacy in practitioner blogs.

## Decision record (ratified by Sean, 2026-08-22)

1. **Ratified:** five-seat roster unchanged.
2. **Ratified:** audits are fresh-context invocations, cross-seat where lanes touch.
3. **Ratified:** Red-Team as a protocol + milestone gate pass, not a sixth seat — **with amendment: the red-team gate pass runs on Codex (GPT 5.6 Sol, High reasoning) via the codex plugin**, giving cross-vendor error-distribution diversity at $0 Claude-usage cost (ChatGPT subscription absorbs it), mirroring the fleet's vault_critic pattern.
4. **Added by Sean:** per-seat model delegation is a build requirement — the harness must not default every seat to the interactive session's model; charted as a Wayfinder decision ticket.

## Key sources

Anthropic multi-agent research system (anthropic.com/engineering/built-multi-agent-research-system) · MAST (arxiv.org/abs/2503.13657) · Google agent-scaling (research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work) · Diversity scaling (arxiv.org/html/2602.03794v1) · Cognition "Don't Build Multi-Agents" (cognition.com/blog/dont-build-multi-agents) · OpenAI "A Practical Guide to Building Agents" (cdn.openai.com PDF) · Cross-Context Review (arxiv.org/pdf/2603.12123) · Huang et al. self-correction (arxiv.org/pdf/2310.01798) · TACL survey (arxiv.org/html/2406.01297v3) · "Too Polite to Disagree" (arxiv.org/html/2604.02668v1) · "Talk Isn't Always Cheap" (arxiv.org/html/2509.05396) · Factory "Missions" talk (youtube.com/watch?v=ow1we5PzK-o) · r/ClaudeCode multi-agent guide (reddit.com/r/ClaudeCode/comments/1vphazv) · r/AI_Agents message-bus thread (reddit.com/r/AI_Agents/comments/1vt8088) · Nate Herk agent-teams (youtube.com/watch?v=vDVSGVpB2vc) · Cole Medin agent-teams (youtube.com/watch?v=-1K_ZWDKpU0)
