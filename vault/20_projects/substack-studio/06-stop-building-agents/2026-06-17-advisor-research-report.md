---
type: research-report
project: substack-studio
series: raising-claude
post: 6
for: Agent-or-Automation Advisor build spec
created: 2026-06-17
method: deep-research (5 parallel angles, web-sourced + cited)
scope: external landscape only — moat (Sean's fleet rubric) deliberately NOT researched
---

# Advisor — Research Report (what "good" looks like)

Three buckets, as scoped 2026-06-17: **A** credible framing, **B** competitive scan, **C**
reliability math. Moat excluded by design (the rubric is Sean's lived doctrine; researching
it would only dilute it). Bottom line up front:

- **The wedge is OPEN.** The content is saturated; the *tool* does not exist — and nothing
  exists as a local, deterministic, no-API-key MCP server.
- **Sean's rubric ALIGNS with the expert consensus** — which is the goal: build with the grain
  of what credible voices already say, then point it at the audience they ignore.
- **The reliability math is defensible but must be reframed** from a loose "pass^k" to the
  proper *pass@k vs pass^k* distinction with a real empirical anchor (τ-bench), and the caveats
  must ship *inside* the tool's output.

---

## A — Credible framing (the rubric aligns with consensus)

**The canonical anchor:** Anthropic, *Building Effective Agents* (Schluntz & Zhang, 19 Dec
2024). The load-bearing distinction, almost verbatim:
> "**Workflows** are systems where LLMs and tools are orchestrated through predefined code
> paths. **Agents** are systems where LLMs dynamically direct their own processes and tool
> usage." (https://www.anthropic.com/engineering/building-effective-agents)

Their prescription is Sean's thesis in Anthropic's words: *"find the simplest solution
possible, and only increas[e] complexity when needed. This might mean not building agentic
systems at all,"* and add complexity *"only when it demonstrably improves outcomes."* Agents
specifically *"trade latency and cost for better task performance"* and carry *"the potential
for compounding errors."* The five workflow patterns (prompt chaining, routing, parallelization,
orchestrator-workers, evaluator-optimizer) are the named vocabulary a technical reader expects.

**The single sharpest operational test** comes from LangGraph's docs, and it's cleaner than
anything in my own spec language:
> *"Can you draw the flowchart of the task before the LLM runs? If yes → workflow. If the
> flowchart depends on what the LLM discovers at runtime → agent."*
> (https://docs.langchain.com/oss/python/langgraph/workflows-agents)

**Agency is a spectrum, not a binary** (Hugging Face smolagents): four levels from "no agency"
(output doesn't affect flow) to "high" (controls iteration / spawns agents); their explicit
guidance is to *"regularize towards not using any agentic behaviour."*
(https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents)

**The production-engineering rallying cry:** *12-Factor Agents* (Dexter Horthy / HumanLayer,
2025) — successful production agents are *"mostly well-engineered traditional software, with LLM
capabilities carefully sprinkled in,"* shaped as *"a mostly deterministic DAG"* with *"small
agent loops"* (3–10 steps), because pure agent loops hit a reliability wall around 70–80%.
(https://github.com/humanlayer/12-factor-agents) This maps onto Sean's actual fleet exactly.

**The definition that won:** Simon Willison (Sept 2025), after years calling the term hopeless —
*"An LLM agent runs tools in a loop to achieve a goal."*

**Counter-views (carry these so the post is even-handed):**
- Cognition, *Don't Build Multi-Agents* (Walden Yan, Jun 2025) vs Anthropic's *multi-agent
  research system* (Jun 2025) — the "agent architecture wars," dropped days apart.
- *The Bitter Lesson* (Sutton): general methods that scale with compute beat hand-engineered
  scaffolding, so as models improve, *more* autonomy may win and elaborate workflows are
  "coping, not scaling." (Caveat: strongest where training data is abundant; workflows still
  win in novel/data-scarce domains.)

**Implication for the rubric:** keep it — it's consensus-aligned. Three sharpenings (§spec edits):
adopt the LangGraph flowchart test as the headline one-liner; frame the verdict as a spectrum
(smolagents) under a binary headline; cite 12-Factor's "deterministic DAG + small loops" as the
backbone. One credibility nuance: "workflow vs agent" is partly a definitional artifact — the
precise claim is *"most things need LOW agency,"* and the post should land that so an expert
reader can't dismiss the title as a false binary.

---

## B — Competitive scan (verdict: OPEN, first-of-kind)

No tool takes a task description and returns an agent-vs-automation verdict + reliability math.
None exists as a local, no-API-key MCP server. The MCP-registry sweep (Smithery ~7k, Glama ~21k,
mcp.so ~19.7k) surfaced only reasoning/process servers (Sequential Thinking, Structured Workflow
MCP) — not an advisor that classifies your task.

**Closest adjacents and how the Advisor differs:**

| Closest thing | What it is | How the Advisor differs |
|---|---|---|
| Anthropic *Building Effective Agents* | The canonical essay/heuristic | Authority to cite, not a tool. Advisor *operationalizes* it. |
| LangGraph "Workflows and agents" | A construction kit (build either) | LangGraph lets you build either; it never says "this task shouldn't be an agent." |
| Reliability-math articles (MindStudio, TDS) | Publish the `p^n` formula as prose | Nobody wrapped it in `task → step-count → success-probability` as a verdict. **The biggest unclaimed asset.** |
| Agent.ai "What should your first agent be?" quiz | Lead-gen quiz | *Assumes* you want an agent; no "just use automation" exit, no math. |
| Agent-readiness checklists (Galileo, Cloudflare, 100-pt audits) | Assess *org/infra* readiness | Assess readiness to *deploy*, not whether a *task* warrants an agent. |

**Why it's defensible:** the two ingredients a tool needs — a decision heuristic (Anthropic's)
and reliability math (`p^n`) — both exist *as published artifacts* but have never been fused
into a deterministic input→verdict tool, and certainly not a local $0 one. Being deterministic
and local is the differentiation, not a footnote — the opposite of the LLM-wrapper quizzes.

**Couldn't confirm:** the exact viral Reddit thread (Reddit is poorly indexed by the search
engine). The discourse is real (HN, Cognition, the "agentic ROI" panic, Gartner's "40% of
agentic projects cancelled by 2027"), but **Sean should pull the specific 1,556-upvote thread
directly** (r/AI_Agents, r/LocalLLaMA, r/n8n) to cite it in the post.

---

## C — Reliability math (defensible, but reframe it)

**Provenance.** The loose version (0.95^10 ≈ 59%, 0.85^k) is everywhere; the underlying math is
**Lusser's Law** (a series system's reliability is the product of its components'). The most-cited
popular figure is **Chip Huyen** (95%/step → ~60% over 10 steps;
https://huyenchip.com/2025/01/07/agents.html). **Andrew Ng** teaches per-step compounding +
majority-vote mitigation. *12-Factor Agents* popularized "3–10, maybe 20 steps max" (qualitative,
not the explicit arithmetic).

**The rigorous, citable version — use this.** Anthropic + the **τ-bench** paper formalize
**pass@k (capability) vs pass^k (reliability):** pass^k is the probability that *all* k trials
succeed, and it falls fast — **GPT-4o: 61% pass@1 → 25% pass@8** on real retail-agent tasks.
(https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents · Phil Schmid:
https://www.philschmid.de/agents-pass-at-k-pass-power-k · τ-bench: https://arxiv.org/pdf/2406.12045)
METR's "time horizons" is the same story by task length (at 80% reliability a 5-hr horizon
shrinks to ~29 min). This is stronger than the illustrative 0.85^8 because it's *measured*.

**The honest caveats (r^k is a naive floor, not a law):**
1. Steps aren't independent — errors correlate, so reliability decays *super-linearly* (often
   **worse** than r^k).
2. Retries aren't free or independent (a prompt that yields malformed JSON tends to do it again).
3. Many steps are deterministic (r = 1) — only the LLM decision points carry probabilistic risk.
4. Errors can be caught/recovered (verification, circuit breakers, human escalation) — often
   **better** than r^k.
5. Per-step r varies; a hard task isn't cleanly decomposable into uniform "steps."
6. 0.85 is illustrative, not measured — defensible as a "strong-but-not-perfect step" placeholder
   to show *shape*, never to predict a number.

**The skeptic-proof framing (lift this into the tool's output card):**
> Under a naive independence assumption, chaining k steps that each succeed ~85% of the time
> gives roughly 0.85^k end-to-end — about 27% over 8 steps. That's an illustrative floor, not a
> law: real steps aren't independent (errors correlate, so it's often worse), but many are
> deterministic or recoverable (so a well-engineered pipeline does better). The point isn't the
> exact number — reliability multiplies, so shortening the chain and catching errors beats
> optimizing any single step.

**Implication:** rename the engine's backbone to *pass@k vs pass^k*, anchor it with τ-bench's
61%→25%, and **ship the caveats inside the verdict card.** A tool that models its own uncertainty
is the exact move the "good twin" (Gemini Deep Research) made in the LDR story — thematic gold.

---

## Canonical references (cite these in the post)

1. Anthropic, *Building Effective Agents* (Schluntz & Zhang, Dec 2024) — https://www.anthropic.com/engineering/building-effective-agents
2. OpenAI, *A Practical Guide to Building Agents* (PDF) — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
3. LangChain/LangGraph, *Workflows and agents* (the flowchart test) — https://docs.langchain.com/oss/python/langgraph/workflows-agents
4. Hugging Face smolagents, *Introduction to Agents* (agency spectrum) — https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents
5. Dexter Horthy / HumanLayer, *12-Factor Agents* — https://github.com/humanlayer/12-factor-agents
6. Chip Huyen, *Agents* (Jan 2025) — https://huyenchip.com/2025/01/07/agents.html
7. Simon Willison, *Agents* / "tools in a loop" — https://simonwillison.net/2025/Jan/11/agents/
8. Anthropic, *Demystifying evals* (pass@k vs pass^k) + τ-bench (https://arxiv.org/pdf/2406.12045); Phil Schmid, *pass@k vs pass^k* — https://www.philschmid.de/agents-pass-at-k-pass-power-k
9. Cognition, *Don't Build Multi-Agents* (counter-view) — https://cognition.ai/blog/dont-build-multi-agents

## Verification notes (claims to treat as soft)
- The compounding figures are **illustrative, not empirical** — cite as directional, not a measured rate.
- The "$7.2M sunk-cost / $16.5M-per-enterprise" abandonment figures appear only in vendor blogs — **do not cite** until traced to the S&P Global primary.
- The exact 1,556-upvote Reddit thread is unconfirmed via search — **verify directly before quoting the number.**
