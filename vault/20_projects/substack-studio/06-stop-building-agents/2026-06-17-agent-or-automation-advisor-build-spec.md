---
type: build-spec
project: substack-studio
series: raising-claude
post: 6
artifact: mcp-server
status: spec-for-review (do not build yet)
created: 2026-06-17
working_name: Agent-or-Automation Advisor
ships_with_post: 6 (Stop Building Agents)
related: [tool-shipping-playbook, opportunity-report-creative-agentic (idea #3), intent-engineering-mcp (sibling shape)]
---

# Agent-or-Automation Advisor — Build Spec

> **Status: SPEC ONLY.** This scopes the tool and estimates effort. Nothing gets built
> until Sean approves the shape. Decisions locked in the 2026-06-17 scoping session:
> **(1) MCP sibling** to intent-engineering, **(2) ships with a `audit_fleet` batch mode**
> that doubles as the post's proof, **(3) Post 6 releads with the fleet-audit dogfood.**
> Build it in a fresh Claude Code session over a weekend; carry this file into the repo as
> `docs/BUILD-PLAN.md`.
>
> **Research-validated 2026-06-17** (deep-research, 3 buckets — full report:
> [`2026-06-17-advisor-research-report.md`](2026-06-17-advisor-research-report.md)). Headlines
> folded into the sections below: the **wedge is OPEN** (no task→verdict+math tool exists, none
> as a local MCP); the **rubric aligns with the Anthropic/LangGraph/smolagents/12-Factor
> consensus** (sharpenings added to §3/§5); the **reliability math is reframed** to the proper
> *pass@k vs pass^k* with a τ-bench anchor + caveats-in-output (§5.2/§6). Canonical references to
> cite live in §12.

## 1. What it is

An MCP server that takes a plain-language description of a task you want to automate and
tells you, in one call, whether you actually need an **agent** or just an **automation with
an LLM node** — plus the reliability math, where the maintenance will bite, and what to build
instead if the answer is "not an agent."

It is the cheapest tool in the series and the loudest hook. The pain point is the single
highest-engagement signal in the whole research corpus: *"automations with LLM nodes... the
maintenance burden kills it"* (1,556 upvotes). People reach for an autonomous, multi-step,
tool-using, looping **agent** when what the task wants is a **deterministic pipeline that
calls a model at one or two bounded steps.** The agent is seductive; the maintenance burden —
non-determinism compounding across steps, debugging a thing that behaves differently every
run, the reliability collapse nobody does the arithmetic on — is what actually kills the
project three weeks later.

The Advisor makes that call before you spend the weekend. It is the same loop as the rest of
the series (elicit intent, score it, return a verdict) pointed at a build-vs-don't-build
decision instead of a spec or a draft.

## 2. The friction it kills (one sentence)

*Before you build an agent, the Advisor tells you in 60 seconds whether your task needs one
— or whether you're signing up for a maintenance burden a 20-line automation would avoid.*

If it can't be said in a sentence it's a feature dump (playbook §2). It can.

## 3. The moat — do NOT research this, it's earned

The defensibility is **Sean's fleet doctrine**, distilled. The agent-infra crowd writes
generic "agents vs workflows" listicles. Sean has *lived the maintenance burden and removed
agents because of it.* The Advisor's rubric is not crowd-sourced advice; it's the operating
discipline already encoded in a 14-agent fleet:

- **The fleet is mostly automations, by design.** Vault Indexer, Synthesizer, Critic, Knowledge
  Lint, Flush, Job Feed, Meta-Agent — scheduled launchd jobs with fixed control flow that call
  a model at one step. Those are *automations with LLM nodes*, not agents. The few genuine
  agents (daily-driver, skill_optimizer) are tightly fenced: 30-turn cap, hard dollar cap,
  `fallback="none"` so an off-hours miss raises rather than silently falling back to the paid path.
- **6 agents disabled 2026-04-09, "do not re-enable."** Direct evidence of the maintenance
  burden being paid and then refused. The Advisor would have flagged most of them up front.
- **Process Inbox paused** because the cloud-agent path cost $1.16/file vs $0/file local — an
  agent-vs-automation call made on cost, not vibes.
- **The LDR routing rule** ("compound / multi-target question → cloud agent that can ground;
  single-shape → local deterministic") is an agent-vs-automation decision written into the
  config the whole fleet reads. The default *was* the bug.
- **The pass^k math** (idea #8, the "Reliability Card"): 85% per-step reliability across 8
  steps ≈ **27%** end-to-end. This is the deterministic, no-API-key backbone of the verdict —
  the arithmetic the 1,556-upvote thread is implicitly screaming about and nobody shows.

Lead every artifact with the wedge: *"here's the doctrine my own fleet runs on, applied to
your task."* The unfakeable proof (§8) is that he ran it on his own fleet and it was right.

### 3.1 How the doctrine lines up with the public consensus (build with the grain)

Research confirms the rubric isn't a hot take — it's the expert consensus, which is exactly
where you want to be: align with what credible voices already say, then point it at the audience
they ignore. Fold these in (they sharpen the rubric, they don't replace it):

- **Adopt LangGraph's flowchart test as the headline one-liner.** *"Can you draw the flowchart
  of the task before the LLM runs? Yes → automation. If the flowchart depends on what the model
  discovers at runtime → agent."* It's the cleanest articulation of the "control-flow
  determinism + runtime tool-selection" dimensions and it's a citable authority.
- **Anthropic's own words back the thesis:** *"find the simplest solution possible... This might
  mean not building agentic systems at all,"* add complexity *"only when it demonstrably
  improves outcomes,"* agents *"trade latency and cost"* and risk *"compounding errors."*
- **Cite 12-Factor Agents as the backbone:** production agents are *"mostly well-engineered
  traditional software... a mostly deterministic DAG"* with *"small agent loops"* (3–10 steps),
  because pure loops wall out at ~70–80% reliability. This *is* the shape of Sean's fleet — name
  the parallel.
- **Frame the verdict as a SPECTRUM under a binary headline** (smolagents' four agency levels).
  The post title "Stop Building Agents" is the hook; the body must land the precise claim —
  *most things need LOW agency, not zero* — or an expert reader dismisses the title as a false
  binary. The four-rung ladder (§5.1) already does this; keep it.

## 4. Form factor + distribution (locked: MCP sibling)

- **A TypeScript MCP server**, same shape as `intent-engineering`: `@swins/agent-or-automation-advisor`
  on npm, `com.seanwinslow/agent-or-automation-advisor` in the official registry via the
  DNS-verified namespace. stdio transport, Node 20+, zod, MCP TS SDK. It lands in the registry
  *next to* intent-engineering, so the brand compounds and discovery is one listicle away from
  an install (playbook distribution notes).
- **The logic is a deterministic rubric — no LLM agent loop inside the server.** This is not an
  accident; it's the message embodied. The tool that tells you to stop building agents is
  itself an automation. Say so in the README; it's the same self-referential credibility move
  intent-engineering made by auditing its own spec.
- **Local, no API key, no account, nothing uploaded.** A trust feature in a market warned about
  plugins that touch accounts/cloud. The server scores a pasted task description against a fixed
  rubric and returns a card. It needs no network.
- **Ship as a GitHub marketplace repo** (`marketplace.json`), not only a `.plugin`. README
  carries the Problem / Solution / Tradeoffs / What I Learned block, the connect screenshot, and
  a one-screen before/after (a real task → its verdict card).

### 4.1 Competitive position (the wedge is OPEN — research-confirmed)

The content explaining agent-vs-workflow is saturated and the reliability math is published —
but **no tool fuses task-description → verdict + math, and none exists as a local, no-API-key
MCP server.** A registry sweep (Smithery ~7k / Glama ~21k / mcp.so ~19.7k) surfaced only
reasoning servers (Sequential Thinking, Structured Workflow MCP), not an advisor. The README and
the post should name the closest adjacents and pre-empt "isn't this just X":

| Closest thing | How the Advisor differs |
|---|---|
| Anthropic *Building Effective Agents* (essay) | The authority it *operationalizes*, not a tool |
| LangGraph "Workflows and agents" | A construction kit — lets you build either, never says "this shouldn't be an agent" |
| Reliability-math articles (`p^n` as prose) | Nobody wrapped it in an interactive `task → step-count → probability` verdict — **the biggest unclaimed asset** |
| Agent.ai "what should your first agent be?" quiz | *Assumes* you want an agent; no "just use automation" exit, no math |
| Agent-readiness checklists (Galileo, Cloudflare, 100-pt audits) | Score *org/infra* readiness to deploy, not whether a *task* warrants an agent |

The differentiation is that it's **deterministic and local** — the opposite of the LLM-wrapper
quizzes. That's the whole point and the trust feature.

## 5. The tool surface (two tools, deliberately small)

| Tool | Input | Output |
|---|---|---|
| `advise_task` | `task_description` (free text); optional `steps`, `runs_unattended` (bool), `frequency`, `human_in_loop` (bool) if the user wants to skip the inferred guesses | A verdict card: tier + reliability estimate + the 2-3 maintenance bites + the cheaper alternative + the one question that would flip the verdict |
| `audit_fleet` | A list of tasks/agents (`name` + `description` each), or a path to a manifest | A table: one verdict row per item + a fleet-level summary ("N of M are automations in a trench coat") |

That's it. `advise_task` is the product; `audit_fleet` is a thin batch wrapper that is *also*
the proof exercise and the post's lead. Resist a third tool in v0 — the whole point of this
post is "don't over-build."

### 5.1 The verdict taxonomy (the ladder)

Headline verdict is one of two — **AGENT** or **AUTOMATION** — because the post's title makes
a binary promise. The detail card places the task on a four-rung ladder so the advice is
actionable:

1. **Just a prompt** — one bounded transformation, human present, nothing scheduled. You don't
   need a pipeline at all.
2. **An automation** — fixed steps, predictable control flow, a model called at 1-2 bounded
   points, deterministic glue. *This is what most "agents" should be.*
3. **An automation with a routing gate** — like #2 plus a branch (the LDR rule: route by the
   question's shape). Control flow is still deterministic; the model doesn't choose the path at
   runtime, the rule does.
4. **A genuine agent** — *only* when the task needs dynamic runtime planning, tool selection it
   can't know in advance, and a loop toward a goal — and you can tolerate or contain the
   reliability collapse. The Advisor should make you **earn** rung 4, not default to it.

### 5.2 The scoring rubric (deterministic, drawn from the doctrine)

Each dimension pushes toward AUTOMATION or AGENT. The verdict is a weighted tally, not a vibe;
the reliability number is computed, not asserted.

| Dimension | Automation signal | Agent signal |
|---|---|---|
| **Step count** | 1-2 model calls | many chained steps (feeds the pass^k number) |
| **Control flow** | fixed, knowable in advance | changes per run / decided at runtime |
| **Tool selection** | a known fixed set of calls | the system must *choose* tools at runtime |
| **Stop condition** | "produce X" (bounded) | "keep going until goal" (open-ended loop) |
| **Unattended?** | runs with a human checking output | runs at 2am, filed unread (raises the bar — see the LDR story) |
| **Blast radius** | a wrong output is cheap to catch | confidently-wrong + unattended = the dread |
| **Frequency** | one-off / rare | nightly forever (maintenance burden compounds) |
| **Cost shape** | $0 local / cheap | per-token cloud justified only by genuine need |

**The reliability engine** is the load-bearing, demoable, no-key piece: given `steps` and a
per-step reliability assumption (default 0.85, overridable), compute `r^steps` and show it.
"Your 8-step agent at 85%/step lands at ~27% end-to-end." That single number is the
counter-positioning against "80% on the first pass" demos.

**Reframed per research (this is what survives Hacker News — see report §C):**
- The intellectual backbone is the **pass@k vs pass^k** distinction, not a loose "pass^k."
  pass@k = capability (does it ever succeed); **pass^k = reliability (do *all* k succeed)**, and
  it collapses fast. Anchor it with the **real** τ-bench number — **GPT-4o: 61% pass@1 → 25%
  pass@8** on retail-agent tasks — alongside the illustrative 0.85^8. The measured number is
  stronger than the toy one; show both. (Underlying math = Lusser's Law, series-system reliability.)
- **r^k is a naive *floor*, not a law — and the tool must say so in its own output.** Correlated
  errors make real chains *worse* than r^k; deterministic steps (r=1) and recovery/retry/human
  escalation make them *better*. 0.85 is illustrative, used to show *shape*, never to predict a number.
- A tool that states its own caveats is the exact move the "good twin" (Gemini Deep Research)
  made in the LDR story — it modeled its own uncertainty. Ship that humility *inside* the verdict
  card (§6); it's a credibility move, not a hedge.

## 6. What it outputs (the verdict card)

Mirror intent-engineering's "score + findings + top-3 recommendations" shape so the two tools
feel like a family:

```
VERDICT: AUTOMATION  (ladder rung 2 — automation with one LLM node)
RELIABILITY: an 8-step agent here lands at ~27% end-to-end (0.85^8, illustrative). An
             automation with one bounded model call lands at ~85%. (Real anchor: τ-bench
             GPT-4o 61% pass@1 -> 25% pass^8.)
             CAVEAT (printed, not hidden): this is a naive-independence floor — correlated
             errors make it worse, deterministic/recoverable steps make it better. The point
             is that reliability multiplies; shorten the chain.
WHERE MAINTENANCE BITES:
  1. Non-determinism compounds — you'll debug a different failure every run.
  2. It runs unattended; a confident wrong answer gets filed unread (see: the day my
     research agent invented Microsoft).
  3. Nightly forever = the burden never amortizes.
BUILD THIS INSTEAD: a deterministic pipeline that calls the model once at <step>, with a
  regression test on the output shape. ~20 lines, ~$0.
THE ONE QUESTION THAT FLIPS THIS: does the task genuinely need to choose its own tools at
  runtime? If yes, it's an agent and you contain it (turn cap + dollar cap + no silent fallback).
```

## 7. Build chunks (a weekend, checkpointed — playbook §4)

1. **Rubric + reliability engine** as a standalone, pure, tested module (no MCP yet). This is
   the moat and the proof; get it right first. Unit tests on the tally and on `r^steps`.
2. **`advise_task` MCP tool** — thin zod-typed adapter over the module. `npm run build` green.
3. **`audit_fleet` MCP tool** — batch wrapper + the fleet-level summary line.
4. **Self-dogfood** (§8) — run `audit_fleet` over Sean's real 14 agents; capture the table.
5. **Package** — README (Problem/Solution/Tradeoffs/Learned), `marketplace.json`, registry
   publish, connect screenshot, one-screen before/after.

Green between chunks, not just at the end (`tsc`, `node --test`).

## 8. The proof = the self-dogfood = the post's lead (locked)

Run `audit_fleet` on the actual fleet (the 14 SDK agents in code-brain CLAUDE.md). The honest,
on-message finding, predicted from the doctrine: **the overwhelming majority are automations
with LLM nodes**, the handful of genuine agents are fenced (30-turn / dollar cap / fallback=none),
and the 6 that were disabled were the ones whose agent framing never earned its maintenance
burden. Publish the results table in the post.

This is the playbook's "eat your own dogfood" gate and the post's opening gut-punch at once:
*"I ran a tool on my own fleet and it told me 9 of my 14 agents are automations in a trench
coat. It was right. I'd already disabled 6 of them, the hard way."* The pass^k number is the
deterministic before/after the technical crowd demands; the fleet table is the receipt.

## 9. Post 6 relead (Path B — direction only, NOT a draft)

Do **not** run the voice chain or rewrite the body in the build session — that happens at draft
time after the tool ships. Direction to carry forward:

- **Lead** with the fleet-audit gut-punch (also the proof). On-message with the title.
- **Mid** keep the existing PureMCPClient / LDR-collapse prose as the vivid "here's what the
  maintenance burden actually looks like" evidence beat — it's excellent and it stays.
- **Bridge** the LDR lesson explicitly into the thesis: *the failure wasn't a dumb model, it
  was an agent-shaped solution for an automation-shaped job; the fix was a deterministic route,
  not a smarter agent.*
- **Ships with** the Advisor; the ask lands sideways.
- **Dup-guard:** `event: ldr-grounding-collapse` stays Post 6's; the 9-night vault regression
  remains Post 7 / the bonus. Don't pull either in.

## 10. Open decisions (resolve before/at build, not blocking the spec)

1. **Name.** "Agent-or-Automation Advisor" is the working name and a good descriptor. Shorter
   registry-friendly options worth a beat: `agent-check`, `overkill` (the verdict it most often
   returns), `trench-coat` (off-brand but memorable). Lock at repo-init.
2. **Per-step reliability default.** 0.85 is the canonical figure; confirm it's the number Sean
   wants to defend in the post, and make it overridable so a reader can plug their own.
3. **`audit_fleet` input format.** A simple `[{name, description}]` list is enough for v0; a
   manifest-path reader is a nice-to-have, defer if it costs more than an hour.
4. **Verify the pain-point citation before the post.** The "1,556 upvotes / automations not
   agents" Reddit thread couldn't be confirmed via search (Reddit is poorly indexed). Pull the
   exact thread directly (r/AI_Agents, r/LocalLLaMA, r/n8n) and confirm the number, or soften
   the claim. Do NOT cite the "$7.2M sunk-cost / $16.5M-per-enterprise" abandonment figures —
   they trace only to vendor blogs.

## 11. Definition of done (for the build session)

- `advise_task` + `audit_fleet` callable from Claude Desktop; `npm run build` + `node --test` green.
- The reliability engine is unit-tested and the pass^k number is demoable with no API key.
- The fleet-audit table is captured (the post's proof).
- README + `marketplace.json` shipped; published to npm + the registry under `com.seanwinslow/*`.
- Tickets filed for anything deferred.

## 12. Canonical references (cite in the README + the post)

Full report + verification notes: [`2026-06-17-advisor-research-report.md`](2026-06-17-advisor-research-report.md).

1. Anthropic, *Building Effective Agents* (Schluntz & Zhang, Dec 2024) — https://www.anthropic.com/engineering/building-effective-agents
2. LangChain/LangGraph, *Workflows and agents* (the flowchart test) — https://docs.langchain.com/oss/python/langgraph/workflows-agents
3. Hugging Face smolagents, *Introduction to Agents* (agency spectrum) — https://huggingface.co/docs/smolagents/conceptual_guides/intro_agents
4. Dexter Horthy / HumanLayer, *12-Factor Agents* — https://github.com/humanlayer/12-factor-agents
5. Chip Huyen, *Agents* (Jan 2025, compounding-error figure) — https://huyenchip.com/2025/01/07/agents.html
6. Simon Willison, *Agents* / "tools in a loop" — https://simonwillison.net/2025/Jan/11/agents/
7. Anthropic, *Demystifying evals* + τ-bench (pass@k vs pass^k) — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents · https://arxiv.org/pdf/2406.12045 · Phil Schmid: https://www.philschmid.de/agents-pass-at-k-pass-power-k
8. OpenAI, *A Practical Guide to Building Agents* (PDF) — https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
9. Cognition, *Don't Build Multi-Agents* (counter-view) — https://cognition.ai/blog/dont-build-multi-agents
