---
title: "Opportunity Report — Creative-AI × Agentic Engineering (the niche synthesis)"
type: opportunity-report
domain: [creative-studio]
created: 2026-06-09
synthesizes:
  - 2026-06-09-claude-code-skills-mcp-gaps-and-opportunities
  - 2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days
  - 2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days
  - 2026-06-09-agentic-engineering-intent-eval-governance-gaps
  - 2026-06-09-agentic-engineering-creative-marketing-team-adoption
  - 2026-06-09-agentic-engineering-spec-driven-eval-gaps
anchored_to: [intent-engineering MCP, vault-knowledge MCP, writing chain, VoicePrint, design-team agents]
related: [tool-shipping-playbook, voiceprint-plugin-build-spec]
---

# Opportunity Report — Creative-AI × Agentic Engineering

The decision-ready synthesis across all six research reports. Four parts, as scoped:
**(1) ranked idea backlog → (2) new-MCP shortlist → (3) positioning brief → (4)
Substack series plan.** Built on the niche guardrail from the playbook: **intent → eval
→ governance, for creative/SaaS/UX/marketing teams; gates and lenses, not generators;
the judgment layer, not the infrastructure.**

## The one bet (read this first)

Six reports, two angles (what creatives *want* + what makes the *agents under them*
fail), one conclusion: the market is **flooded with generation and starved of intent,
proof, and control** — and every tool that addresses that layer is *"designed for ML
engineers."* The creative/marketing slice has the same three needs (make it do what I
*meant*, prove it worked, keep me in control) and **nobody is selling to them.**

You already shipped the answer once: **elicit intent → score it → gate the output.**
The `intent-engineering` MCP does it at the spec layer ("the audit *is* the eval"); the
writing chain does it for prose; VoicePrint productizes the whole loop; the design-team
agents do it for UI; `vault-knowledge` makes the *why* auditable. **The opportunity is
translation, not invention:** take that engineer-framed loop and re-skin it in
brief/brand/voice language for the people the agent-infra builders ignore.

The single sharpest line the research handed you, to build and write around:
> *"The missing layer in AI agents is not autonomy. It is structured intent."*
And the wedge:
> *"eval tooling like Braintrust and LangSmith is designed for ML engineers… most teams
> don't need 'research-grade evals' first."*

---

## Part 1 — Ranked idea backlog

Merged + de-duped across all six reports (they propose largely the same slate from
different angles; duplicates collapsed). Scored on **Pain** (frequency × unservedness in
the corpus), **Fit** (closeness to a shipped asset), **Effort-to-first-proof**, and a
**Verdict**. Ordered by build priority.

| # | Idea | Pain | Fit | Effort | Verdict |
|---|------|------|-----|--------|---------|
| 1 | **Intent Card** — guided brief → self-auditing, checkable spec for non-coders (the creative front-end on intent-engineering MCP; `audit_brief`/`scaffold_brief`) | ★★★★★ | ★★★★★ (it's your MCP, re-skinned) | Med | **BUILD NEXT** |
| 2 | **On-Brand / Did-It-Land Gate** — score any output against the intent spec; pass/fail + violated clauses + slop-risk + the one fix (writing-critique generalized past prose) | ★★★★★ | ★★★★★ (writing chain) | Med-High (the eval *is* the product) | **BUILD NEXT** |
| 3 | **Agent-or-Automation Advisor** — describe the task; it tells you if you need an agent at all or just "automations with LLM nodes," and where maintenance will bite | ★★★★ | ★★★★ | **Low** | **BUILD NEXT (cheap + great content)** |
| 4 | **VoicePrint** — portable voice spec that *is* the intent artifact + eval target + thing the human approves | ★★★★★ | SHIPPED | done | **SHIP IT (dogfood → launch)** |
| 5 | **Fast Approval Gate for small teams** — review-before-publish, fast + legible enough nobody disables it; shows the agent's reasoning | ★★★★ | ★★★★ (the review IS the product) | Med | **NEXT** |
| 6 | **Drift Lens** — span-by-span highlight of where output left the voice/brand spec, so you fix 3 spans not the whole draft | ★★★ | ★★★★ | Med | **NEXT** |
| 7 | **Decision Trail** — vault-knowledge typed edges → "why did the agent do this," traceable for a reviewer (supports/contradicts/supersedes) | ★★★ | ★★★ (least-proven mapping) | Med-High | **VALIDATE FIRST** |
| 8 | **Reliability Card** — the pass^k math (85% × 8 steps ≈ 27%) made visible for *creative* output, with confidence bands | ★★★ | ★★★ | Med | **LATER** |
| 9 | **Anti-listicle creative registry** — tools organized by creative job, "works without a terminal?" flag, last-tested date | ★★★ | ★★ (no moat) | Low | **CONTENT-ONLY (VoicePrint funnel)** |
| 10 | Orchestration engine / memory store / gate-firewall / observability / shadow-AI security | ★★★★★ | ✗ | Very High (capital + eng) | **SKIP — NOT your lane** |

**The honest read of this table:** items 1, 2, and 4 are the *same loop* at three
zoom levels (spec, eval, productized). You are not building 10 things — you're building
**one judgment loop and pointing it at a non-engineer audience**, with the Advisor (#3)
as a cheap, contrarian wedge that doubles as your loudest post. Everything below #6 is
"later" or "content." Everything in #10 is a deliberate no.

**Build-order recommendation:** #3 Advisor (a weekend, ships a post) → #1 Intent Card
(the creative front-end your MCP is missing) → #2 On-Brand Gate (generalize
writing-critique). That sequence is cheapest-proof-first and each step is a post.

---

## Part 2 — New-MCP shortlist (adjacent to your two)

The research's strongest signal is that **your existing MCPs already sit on the gaps** —
so most "new MCP" ideas are really **new tools inside the MCPs you shipped**, plus one
genuinely new server. Distinguished honestly:

**A. Extend `intent-engineering` MCP with brief-mode tools (highest leverage, not a new server).**
Add `audit_brief` / `scaffold_brief` / `assess_brief_readiness` — the exact three-tool
shape you already shipped, re-skinned from "dev PRD → coding agent" to "creative brief →
any agent." This is the literal code answer to *"correct behavior was never defined"* for
non-coders. **Why it wins:** you're not proving a new thesis, you're widening the audience
of a published one. The risk the reports name twice: today it speaks PRD/agent; it must
speak brief/brand or it lands at 16 installs.

**B. A new `creative-eval` MCP — the calibrated subjective judge (the loudest unserved gap).**
Expose the writing-critique calibrated judge as a portable tool: `score_against_voice_spec`,
`slop_check`, `on_brand_check` → a pass/fail card with violated clauses + a stylometry/
similarity score so it's *provable*, not vibes. **This is the single most defensible new
build** — the corpus says eval tooling is "for ML engineers" and there is *no* pass/fail
test for subjective creative output. The hard part is the product: Goodhart's Law applies
to your own rubric, and non-determinism means single-run scores need confidence bands.

**C. Extend `vault-knowledge` MCP into a decision-trail tool (validate the fit first).**
A `why_this` / `trace_decision` tool over the typed edges (supports/contradicts/
supersedes) → the "show me why the agent did this" lens a reviewer needs. **Caveat the
reports flag:** the corpus never asks for "typed reasoning edges" in those words — this is
a hypothesis to test, not a confirmed pull. Frame as *decision/provenance memory*, never
"another memory server" (that's the funded infra race you avoid).

**Do NOT build a new MCP for:** memory/state, orchestration, observability/tracing,
gate-firewalls, or security/shadow-AI. Three funded products appeared in a *single*
30-day window for the gate layer alone. That's VC + platform territory; you lose by
entering.

---

## Part 3 — Positioning brief

**The position, one line:** *I build the judgment layer for AI agents — intent, proof,
and control — for the people who aren't backend engineers.* (Creatives, marketers,
designers, small studios.)

**The wedge, stated as counter-positioning:**
- The incumbents (Braintrust, LangSmith, the gate-firewall startups) are **built for ML
  engineers.** You build the same intent→eval→governance loop **for taste, not
  throughput** — in brief/brand/voice language.
- The market sells **generators** ("make content faster"). You sell **gates and lenses**
  (define what right means, prove it, keep the human deciding). Generation is solved;
  good is not. *"Content volume tripled. Engagement dropped 40%."*
- **Local, no API key, no account, nothing uploaded** — a trust feature in a market
  actively warned about plugins that touch accounts/cloud, and where 93% of orgs have had
  a shadow-AI incident.

**How each asset is positioned (lead with these, in this order):**
- **`intent-engineering` MCP** → *"define correct before you build."* The published proof
  that "evals are the new PRDs" / "the audit is the eval." Reframe from dev tool to the
  intent layer for non-coders. (Sits on the #1 + #2 gaps in the whole dataset.)
- **VoicePrint** → the productized loop: interview → a voice spec (intent) → that spec is
  the eval target (proof) → human approves (control). Your flagship, creative-first.
- **The writing chain** → the working proof that a *spec-bound eval for subjective output*
  exists and holds (the thing the "slop" threads say nobody delivers). Lead with the
  Cheese-Gauntlet eval as proof, not vibes.
- **`vault-knowledge` MCP** → *decision/provenance memory* — why an output exists,
  traceable. (Differentiator: typed edges, not vector similarity.)
- **design-team agents** → the same gate, for visual identity.

**What you explicitly do NOT claim:** infrastructure (orchestration, memory, tracing,
firewalls, compliance). Say it out loud in the materials — it's a credibility move that
proves you know where the line is. The prior reports' own words: those are "an
org-maturity problem," "a capital play," "not yours."

**The unfakeable proof you carry that competitors don't:** you've *shipped* this loop and
*measured* it (VoicePrint's burstiness proof; the writing-critique analyzer). In a market
of demos and "80% on the first pass," a measured before/after is the hiring signal and the
sales proof at once.

---

## Part 4 — Substack series plan

The throughline that makes the series a *position*, not a pile of posts: **"the judgment
layer for creatives adopting AI."** Every post = a pain point in the audience's own words
+ the gate/lens you ship alongside it. The ask lands sideways; the work is the pitch.

| # | Working title | Pain (their words) | Tool it ships with | Status |
|---|---------------|--------------------|--------------------|--------|
| 1 | You Can't Prompt Taste Into a Machine | "humanize prompts don't work" | the Cheese Gauntlet kit | **shipped** |
| 2 | I Built a Machine to Sound Like You (then made it sound like a stranger) | "it's obvious, we know" / "I'm becoming a fraud" | **VoicePrint** | **drafted** (run voice chain) |
| 3 | Correct Was Never Defined | *"the missing layer is not autonomy, it's structured intent"* | **Intent Card** (#1) / intent-engineering MCP | next |
| 4 | The Eval Tools Are Built for the Wrong People | *"designed for ML engineers… most teams don't need research-grade evals"* | **On-Brand Gate** (#2) | next |
| 5 | Your Content Tripled and Engagement Dropped 40% | *"the AI content arms race is real and it's losing"* / *"Fucking AI slop man"* | the gate, as anti-slop checkpoint | next |
| 6 | Stop Building Agents | *"automations with LLM nodes… the maintenance burden kills it"* (1,556 upvotes) | **Agent-or-Automation Advisor** (#3) | next (loudest hook) |
| 7 | The Judgment Layer | McKinsey/EY: brand stewardship is worth *more* as output floods | the whole stack; ties to "Access Over Meaning" | capstone |

**Sequencing note:** Post 6 ("Stop Building Agents") has the single highest-engagement
hook in the entire corpus and the cheapest tool to ship (#3) — consider pulling it
earlier as the re-introduction of the series after VoicePrint. Post 7 is the thesis post
that names the position explicitly and connects to your existing "Access Over Meaning"
manifesto.

---

## What to do next (the short list)

1. **Ship VoicePrint** — finish the real-human dogfood (runbook is written), then Post 2.
2. **Build the Agent-or-Automation Advisor (#3)** — a weekend, and it's Post 6's tool.
3. **Add brief-mode tools to intent-engineering MCP (#1 / shortlist A)** — the creative
   front-end your published MCP is missing; this is the highest-leverage single move.
4. **Generalize writing-critique into the On-Brand Gate / creative-eval MCP (#2 / B)** —
   the most defensible new build; the eval is the product.
5. Keep the loop turning: each build is a post; each post names the pain in their words
   and hands them the gate. That's the engine in the playbook, running.

**The meta-point:** none of this is a pivot. It's the same loop you already shipped,
aimed at the audience the whole agent-infra industry structurally can't serve — because
it needs taste, not throughput.
