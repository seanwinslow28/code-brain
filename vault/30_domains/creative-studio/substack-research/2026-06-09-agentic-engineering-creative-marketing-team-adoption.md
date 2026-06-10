---
title: "Agentic Engineering — The Creative/Marketing-Team Adoption View (Intent / Eval / Governance)"
type: research
status: complete
domain: [creative-studio]
tags: [agentic-engineering, ai-agents, intent, evals, governance, human-in-the-loop, marketing-teams, creative-teams, market-gaps, intent-engineering-mcp, vault-knowledge-mcp, voiceprint, last30days, research, opportunity]
created: 2026-06-09
last-updated: 2026-06-09
date-range: 2026-05-10 to 2026-06-09
sources: [reddit, x, youtube, web]
tool: "/last30days v3.0 — team-adoption anchor pass + WebSearch supplement"
coverage: "Reddit with comments (14 threads, ~1,690 upvotes / ~600 comments), X (4 posts), YouTube (17 videos / 5 transcripts, ~2.0M views), Web (12+ pages). HN, Polymarket, TikTok, Instagram returned nothing on-topic."
companion-to: 2026-06-09-agentic-engineering-intent-eval-governance-gaps
ai-context: "COMPANION report. The sibling 2026-06-09-agentic-engineering-intent-eval-governance-gaps.md was built from the engineering-frustrations --deep pass (r/AI_Agents, r/AI_Governance, coding-agent YouTube) and explicitly flagged that it lacked a directly-observed creative/marketing-team source and re-aimed engineer-voiced gaps. THIS report supplies exactly that missing half: a last30days anchor pass on 'how creative and marketing teams are adopting AI agents' (r/DigitalMarketing, r/AIMarketingPros, WPP/Bloomberg, AI Marketers Guild), mined along the same INTENT -> EVAL -> GOVERNANCE axes. Same conclusion reached from the buyer's side rather than the builder's. Part 3 anchored to Sean's two shipped MCPs (intent-engineering: the audit IS the eval; vault-knowledge: typed reasoning edges). Confidence: medium-low (single anchor pass; marketing-adoption-skewed; agentic-engineering gaps refracted through team pain, not tooling vocabulary). Read alongside the sibling — together they triangulate the niche from both builder and buyer."
related: [2026-06-09-agentic-engineering-intent-eval-governance-gaps, 2026-06-09-claude-code-skills-mcp-gaps-and-opportunities, 2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days, 2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days, tool-shipping-playbook, voiceprint-plugin-build-spec]
---

# Agentic Engineering — The Creative/Marketing-Team Adoption View

> Research across **14 Reddit threads (~1,690 upvotes / ~600 comments), 4 X posts, 17 YouTube videos (~2.0M views, 5 full transcripts), and 12+ web pages**, 2026-05-10 → 2026-06-09. One `/last30days` anchor pass ("how creative and marketing teams are adopting AI agents") + WebSearch supplement. Query type: GENERAL, mined along the intent → eval → governance axes. Raw corpus saved at `~/Documents/Last30Days/how-creative-and-marketing-teams-are-adopting-ai-agents-raw.md`.
>
> **Companion to [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]].** That report mapped the same three gaps from the *builder's* side (engineer-skewed corpus: r/AI_Agents, r/AI_Governance, coding-agent YouTube) and explicitly noted it lacked a directly-observed creative/marketing source. This one is that missing half — the *buyer's* side. The two reach the same conclusion from opposite ends of the table; read them together.

## Read-this-first caveat (it shapes everything below)

**This corpus is a *marketing-adoption* conversation, not an *AI-engineering* one.** Nobody in it says "spec," "eval harness," or "governance gate." They say "brand voice," "is it actually working," and "wild west." So the intent/eval/governance gaps here are **real but refracted through team pain, not tooling vocabulary** — which is itself the finding: the buyers in Sean's niche don't yet have words for this layer. Reddit titles/comments and YouTube transcript highlights are **verbatim and low-agenda** (trust most); web percentages are **report-derived and vendor-biased** (treat as directional, flagged `[web]`). Single anchor pass, so confidence is **medium-low**.

---

## Quick verdict

Where the sibling report heard engineers say *"correct behavior was never defined,"* this corpus hears marketing teams live the consequence: agent adoption is **near-universal in intent but narrow, contested, and unproven in practice**, and the loudest practitioner voices are *pushing back* on agents rather than cheering them. The biggest thread of the month is literally titled ["Stop building AI agents"](https://www.reddit.com/r/AI_Agents/comments/1taei9m/stop_building_ai_agents/) (1,556 upvotes). The three things teams can't get — *make it do what I meant* (intent), *prove it worked* (eval), *let me stay in control* (governance) — are exactly the layer nobody sells to people who aren't backend engineers. The enterprise has it (WPP's proprietary "brand brains" + "performance brain"); the five-person creative shop has a blank chat box. That asymmetry is the opening, and it confirms the judgment-layer thesis from the buyer's side.

---

# Part 1 — What teams ask for / struggle with (the findings)

## The dominant signal: "automations, not agents" (INTENT, from the buyer's mouth)

The most-upvoted item in the pull is a backlash. ["Stop building AI agents"](https://www.reddit.com/r/AI_Agents/comments/1taei9m/stop_building_ai_agents/) (1,556 upvotes, 342 comments), top comment (156 upvotes):
> *"This is the first post in this sub I actually agree with, and I build exactly the same — automations with LLM nodes. The maintenance burden is what actually kills these projects."*

The constraint pattern people trust instead of open-ended autonomy:
> *"the agent would have hallucinated. This is why I sell customers on closed world prinicple agents that rely on reasoning chains."*

The most-cited insight across r/AI_Agents, from ["After using AI agents for a few months…"](https://www.reddit.com/r/AI_Agents/comments/1tegjgx/after_using_ai_agents_for_a_few_months_these_are/) (94 upvotes, 77 comments):
> *"'The agent is only as good as the environment around it' is probably the most underrated point here."*

**Read:** the buyer's version of the sibling report's *"correct behavior was never defined"* is "constrain it to what I actually meant, or the maintenance burden kills it." Same root cause, said in plain marketing-team language.

## The proof problem is everywhere (EVAL)

The ROI doubt is stated openly as thread titles:
- ["Are AI agents just hype, or are they actually delivering measurable business value?"](https://www.reddit.com/r/AI_Agents/comments/1tpylty/are_ai_agents_just_hype_or_are_they_actually/) (18 comments)
- ["Is AI Agent adoption low?"](https://www.reddit.com/r/AI_Agents/comments/1tg0hqy/is_ai_agent_adoption_low/) (15 comments)
- ["6 ai management tools teams are actually using for agent oversight in 2026"](https://www.reddit.com/r/AIToolsAndTips/comments/1tcqtkr/6_ai_management_tools_teams_are_actually_using/)

The marketing-ops version, verbatim from [r/AIMarketingPros](https://www.reddit.com/r/AIMarketingPros/comments/1tzswjp/ai_adoption_in_marketing_ops_is_nearuniversal_in/):
> *"AI adoption in marketing ops is near-universal in intent. Most teams still can't tell you where their campaigns are losing time."*

The most concrete failure measurement in the pull, [r/DigitalMarketing](https://www.reddit.com/r/DigitalMarketing/comments/1tq9azh/the_marketing_teams_content_volume_tripled/):
> *"the marketing team's content volume tripled. engagement dropped 40%. the ai content generator arms race is real and its losing."*

The enterprise answer exists but is locked inside a platform — WPP, in Bloomberg's ["Quantum Marketing"](https://www.youtube.com/watch?v=a40YkQDSIrk) (199K views):
> *"a custom-trained AI model can predict whether an ad will work, why it will work or not work, and what you need to do to improve it"* — the "performance brain" scores each of 13,000 variants before spend, because *"you are sometimes wasting… tens of thousands… of media spend against something that's not going to resonate."*

**Read:** teams bought agents before instrumenting the problem. This is the buyer-side mirror of the sibling's *"passes clean but produces wrong output"* — except for creative output there's no pass/fail test at all, only taste.

## Governance lags adoption badly (CONTROL)

The loudest control signal is chaos, not capability — from the [AI Marketers Guild webinar](https://www.youtube.com/watch?v=DUf72tbU8kk) (Amanda Jeffs):
> *"93% of organizations has already dealt with at least one shadow AI incident of someone at work using AI without approval."*
> *"there's no guidelines. There's no guardrails. IT is behind."* … *"It's literally the wild west."*

The failure-when-uncontrolled story:
> *"We know businesses that have implemented agents that told them to give everything up and they had to rewind them all. It's inconsistent."*

The human-in-the-loop consensus is unanimous among the technical voices — IBM Technology, ["5 Types of AI Agents"](https://www.youtube.com/watch?v=fXizBc03D7E) (394K views):
> *"AI agents typically work best with a good old human in the loop. At least for the time being."*

IBM, ["Generative vs Agentic AI"](https://www.youtube.com/watch?v=EDb37y_MhRw) (1.2M views):
> *"The AI generates possibilities but the human curates them."* … *"at each step, there is a human… reviewing it… refining it… directing this whole process."*

The creative-specific fear, [r/DigitalMarketing](https://www.reddit.com/r/DigitalMarketing/comments/1td5oo3/are_marketing_teams_actually_ready_for_ai_agents/):
> *"Are marketing teams actually ready for AI agents to touch live ad campaigns?"*

Regulation is now forcing review steps — [@researchUSAI](https://x.com/researchUSAI/status/2062338301424697591):
> *"New York state officials require commercial advertisers to disclose when people depicted in ads are AI-generated, pushing brands and ad agencies to add review steps."*

This is the buyer-side echo of the sibling's Singapore-framework / *"moved from PDFs to enforced policies"* finding — same hardening, felt as shadow-AI chaos rather than as architecture.

## The structural backdrop (web — directional)

- **91% of marketers report using AI**, up from 63% a year ago [web — Jasper "State of AI Marketing 2026"]; the webinar's number is *"almost 90%… use AI in their daily work."*
- **The pilot-to-production gap is real:** ~23% of orgs are *piloting* agents, ~14% have partial/full deployment; Gartner projects 40% of enterprise apps embed task-specific agents by end-2026 [web].
- **Where agents actually ship**, per a [250-agency survey](https://www.digitalapplied.com/blog/agentic-ai-adoption-survey-2026-250-agencies): **brief/outline generation 64% in production** (forgiving quality bar), **SEO-audit agents 51% — highest reported ROI** [web].
- **The judgment layer is the consensus moat:** [McKinsey](https://www.mckinsey.com/capabilities/growth-marketing-and-sales/our-insights/reinventing-marketing-workflows-with-agentic-ai) and [EY](https://www.ey.com/en_us/insights/cmo/how-ai-is-reshaping-the-future-of-marketing) both frame brand stewardship and creative direction as *more* valuable as agent output floods the web.

---

# Part 2 — The gaps nobody is filling

> Ranked by **frequency in the corpus × how unserved it is.** Quotes verbatim unless tagged `[web]`. Each gap is tagged **Sean-niche** (intent/eval/governance judgment, creative-team-facing — taste required, infra-light) or **NOT-Sean** (orchestration/security/observability infra — capital + eng play), per the [[tool-shipping-playbook]] guardrail. Gap numbering is aligned to the sibling report where they map.

### Gap 1 — "Did it actually work?" — proof-of-value for agent output (EVAL) · **Sean-niche**
Highest-frequency doubt in this corpus, lowest served for non-enterprise. *"Are AI agents just hype, or are they actually delivering measurable business value?"* and *"Most teams still can't tell you where their campaigns are losing time."* WPP's "performance brain" is the only answer on display, and it's a proprietary enterprise platform.
**Hard to build because:** predicting *business* outcomes needs data scale a solo builder doesn't have. The touchable slice is narrower — judging whether the *output itself* is good/on-brand (Gap 3). Honest scope: "score the artifact," not "predict the revenue." (= sibling Gap 2, buyer-side.)

### Gap 2 — Encoding intent/brand/voice so the agent does what was meant (INTENT) · **Sean-niche**
Loud, unserved for everyone who isn't WPP. The enterprise pattern: *"brand brains… custom AI models trained on data, brand assets, and details like tone of voice."* The bottom-up version: *"training the AI in your brand clarity… your brand voice… your customer personas… your ethics guidelines, your policies, your templates."* Failure when absent: agents *"told them to give everything up and they had to rewind them all."*
**Hard to build because:** taste/voice is subjective and resists a config file — encoding "what I meant" as a checkable artifact is the unsolved part, and the reason it's defensible. (= sibling Gap 1, the buyer's restatement of *"correct behavior was never defined."*)

### Gap 3 — Quality gate on creative output: anti-slop, on-brand (EVAL) · **Sean-niche**
The most visceral failure quote: *"content volume tripled. engagement dropped 40%… the ai content generator arms race is real and its losing,"* plus *"AI is making a lot of marketing teams worse,"* and the raw version, *"Fucking AI slop man."* Volume is solved; *good* is not. Nobody sells small teams an "on-brand and not slop?" gate before ship.
**Hard to build because:** it requires *subjective* judgment, which is exactly why generic eval frameworks and the "6 agent-oversight tools" category can't touch it — they score structured pass/fail, not taste. The single best wedge; it's what `writing-critique` already does for prose.

### Gap 4 — Human review *before* agents touch live work (GOVERNANCE) · **Sean-niche (team slice)**
Stated as fear (*"ready for AI agents to touch live ad campaigns?"*), consensus (*"the human curates them,"* *"a good old human in the loop"*), and regulation (*"add review steps"*). The approve-before-publish surface, with the agent showing its reasoning, barely exists for creative work below enterprise.
**Hard to build because:** the value prop self-destructs if review is slow — people disable the gate to get their "automation" back. You're building *fast, legible review*, not a checkpoint. (= sibling Gap 3 team-slice.)

### Gap 5 — "When do I NOT need an agent?" — reliability/maintenance (INTENT/architecture) · **mixed, lean NOT-Sean**
The 1,556-upvote consensus: *"automations with LLM nodes… the maintenance burden is what actually kills these projects,"* *"closed world principle agents."* There's a real *advisory* gap (tell a team they need a workflow, not an agent) — but the runtime that runs the workflow is orchestration infra.
**Hard to build because:** the *advice* is a lens (Sean-buildable); the *engine* (n8n/LangGraph/Zapier) is a capital/eng play. Build the lens, not the engine.

### Gap 6 — Guardrails / shadow-AI / policy enforcement (GOVERNANCE) · **NOT-Sean**
Highest raw frequency of any control signal — *"93%… shadow AI incident,"* *"no guardrails, IT is behind,"* *"wild west."* But the fix is enterprise IT/security: DLP, SSO, audit, compliance, sold to CISOs. [@BessemerVP's](https://x.com/BessemerVP/status/2056441982298513503) *"AI pricing and monetization playbook"* surfacing here signals VCs already fund this lane.
**Hard to build because:** it's a security product, not a creative tool. Solo builders get crushed here. **Stay out** — flag it for the buyer, don't build it. (= sibling Gap 3 enterprise-slice + the regulatory hardening it noted.)

### Gap 7 — Agent observability / oversight ops (GOVERNANCE) · **NOT-Sean**
*"6 ai management tools teams are actually using for agent oversight in 2026."* The tracing/monitoring category is filling fast and VC-funded. (= sibling Gap 5.) **Skip.**

### Gap 8 — "The environment around the agent" / context plumbing (INTENT) · **NOT-Sean**
*"The agent is only as good as the environment around it."* Real, but it's retrieval/context/tool-wiring — infra-heavy. Skip the runtime; the *spec* that defines the intended environment is the Sean-niche slice (Gap 2).

### Overlap flag (read with the siblings, don't repeat them)
This report and [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]] are the **same three gaps from opposite sides of the table** — engineers naming the root cause (*"correct behavior was never defined,"* *"ghost debugging"*) vs. marketing teams living the consequence (*"is it actually delivering value,"* *"engagement dropped 40%,"* *"wild west"*). The **new** material this companion adds: directly-observed creative/marketing-team voice (which the sibling inferred), the WPP enterprise-only "brand brain/performance brain" benchmark, the shadow-AI governance reality, and the live-campaign-readiness fear. Gaps 2–4 are also the agentic root of the creative-facing gaps in [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]] (voice vacuum, brand-lock, approval-gate) and the judgment-bottleneck thesis in [[2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days]] / [[2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days]].

---

# Part 3 — How Sean is positioned

> Anchored to the two shipped MCPs, leading with **intent-engineering** for the spec/eval gaps (1–3) and **vault-knowledge** for the memory/provenance gaps. No invented capabilities.

## Priority 1 — [[intent-engineering]] MCP IS the answer to Gaps 1+2 (the flagship fit)
`@swins/intent-engineering-mcp` (tools `audit_intent_spec`, `generate_intent_spec_scaffold`, `assess_retrofit_level`) is built on **"the audit IS the eval"** — it scores a spec against the framework *before* that spec ships to an agent. That is, almost exactly, the two loudest gaps in this corpus:
- **Gap 2 (encode intent):** `generate_intent_spec_scaffold` produces the "what I meant" artifact teams lack — the non-enterprise equivalent of WPP's "brand brain," as a spec rather than a trained model.
- **Gap 1 (prove it):** `audit_intent_spec` operationalizes *"evals are the new PRDs"* — it answers *"are they actually delivering measurable value?"* at the point of intent, before spend, the cheapest place to catch a doomed run (WPP's "predict whether it will work before wasting media spend," generalized).
- **The 0–5 maturity ladder** the webinar describes (*"confusion → foundation → workflows → professionalization → team-wide literacy → fully-automated engine"*) is what `assess_retrofit_level` already scores — a ready-made, research-validated framing.
- **Honest risk (the big one):** the MCP today is **dev-facing** — a spec that ships to a *coding* agent. The niche this report serves is **creative/marketing teams who don't write specs.** The gap between "audit a dev spec" and "audit a campaign brief / brand intent" is a *translation and packaging* problem, not a capability one — but it's the difference between adoption and a 16-install fate. The MVP must speak brief/brand, not PRD/agent. (The sibling report reaches the identical risk from the builder's side.)

## Priority 2 — the writing chain already proves the pattern for Gap 3
`writing-voice-modes` (intent) → `writing-critique` (eval/red-team) → `writing-humanity-pass` (the gate) is the **elicit → score → gate** loop this corpus is begging for, shipped and working for prose. Gap 3 (anti-slop, on-brand gate) is this chain pointed at *any* creative artifact. The Cheese Gauntlet / stylometry baseline is the "prove it held" eval the *"slop"* threads say nothing else delivers.
- **Honest risk:** subjective eval only earns trust if the score is legible. Lead with the eval as proof, not vibes.

## Priority 3 — [[vault-knowledge]] MCP for the provenance/review gaps (Gap 4 + the instrumentation gap)
vault-knowledge's **typed reasoning edges** (`supports / contradicts / evolved_into / supersedes / depends_on / related_to`) are a decision-trail substrate that makes *why* an output exists auditable:
- **Gap 4 (review gate):** a reviewer sees what a decision `depends_on` or `contradicts` before approving — review that's fast *because* it's legible (what keeps people from disabling the gate).
- **The *"can't tell you where campaigns are losing time"* instrumentation gap:** typed edges over a body of work surface contradictions and supersessions a flat log can't.
- **Honest risk:** least-proven mapping in the pull — the corpus doesn't ask for "typed reasoning edges" in any words. Hypothesis to validate, not a confirmed fit. (Sibling frames the same as "decision/provenance memory, not another memory server.")

## Priority 4 — design-team agents = the design sibling of the gate (Gap 4, brand-lock)
**Design System Enforcer** + **Visual Polish Auditor** already do token-compliance and drift-catching — the same elicit-then-enforce pattern, for visual identity. The honest-automation Substack angle (*"the review step is the product"*) writes itself from this corpus's *"human curates"* / *"add review steps"* quotes. [[voiceprint-plugin-build-spec|VoicePrint]] is the productized version of the whole loop.

## The throughline
Every Sean-niche gap is the **same loop Sean already shipped**: elicit intent → score it → gate the output. intent-engineering does it at the spec layer; the writing chain for prose; the design-team agents for UI; vault-knowledge makes the *why* auditable. The opportunity is **not a new capability** — it's pointing that loop at the creative/marketing teams the agent-infra builders ignore, and translating it out of dev-spec language into brief/brand language. Both halves of this research — builder and buyer — converge on that one move.

---

# Part 4 — What to build (clean-sheet ideas)

> Grounded only in the gaps above. **Bias: gates and lenses, not generators.** Each names the gap and the genuinely hard part. (Overlaps the sibling report's idea list by design — same conclusion, same build slate; flagged where identical.)

### 1. Intent Card — a campaign brief that audits itself
**Gap 2 + Gap 1.** A non-engineer fills a guided brief (audience, brand voice, must/never-do, success signal); the tool scores it for completeness/ambiguity *before* any agent runs — the `audit_intent_spec` move re-skinned from PRD to brief. Output: a portable intent artifact + a "will this spec survive contact with an agent?" score. (= sibling's "Intent Interview → Spec Compiler.")
**Hardest part:** the score must be right often enough to trust on Day 1, and read like marketing, not engineering. Translation is the whole game.

### 2. Did-It-Land — proof-of-value card for creative output
**Gap 1 + Gap 3.** Paste output + original intent; get a structured verdict (on-brief? on-brand? slop-risk? the one thing to fix) with a similarity/stylometry score so it's provable. The honest, infra-light slice of WPP's "performance brain." (= sibling's "Spec-Bound Eval Card.")
**Hardest part:** scope to "judge the artifact" (achievable), resist "predict the KPI" (needs data scale you don't have).

### 3. On-Brand Gate — anti-slop checkpoint before publish
**Gap 3.** A pass/fail gate blocking output until it clears brand-voice + slop + fact checks, with the three failing spans highlighted so you fix, not rewrite. The `writing-critique` loop generalized past prose.
**Hardest part:** encoding "off-brand" as a checkable rule — the unsolved 80%. Scope to *enforce an existing brand*, not *invent taste*.

### 4. Approval-Gate Publisher — the review is the product
**Gap 4.** Agent output can't go live until a human clears a fast, legible checkpoint showing the agent's reasoning + what it depends on (vault-knowledge edges). Sells the *review*, the literal answer to *"ready for AI agents to touch live ad campaigns?"* (= sibling's "Lightweight Approval Gate.")
**Hardest part:** review fast enough that nobody disables it. If it's slower than the work it gates, it's dead.

### 5. Decision Trail — show me why the agent did this
**vault-knowledge MCP + Gap 4.** A lens over a run surfacing what each decision `supports` / `contradicts` / `supersedes`, so a reviewer follows the "why" instead of a flat log. Provenance as a creative-team feature, not a compliance one. (= sibling's "Provenance Trace.")
**Hardest part:** capturing intent edges cleanly from a messy run without making the human annotate everything.

### 6. Agent-or-Automation Advisor — talks you OUT of building an agent
**Gap 5 (the lens, not the engine).** Describe the task; the tool says whether you need an agent at all or just *"automations with LLM nodes,"* and where the maintenance burden will bite. Contrarian, cheap, aligned with the 1,556-upvote consensus. (Net-new vs. the sibling's slate — this corpus's distinctive contribution.)
**Hardest part:** being right enough to be trusted, and resisting scope-creep into building the workflow (the NOT-Sean engine).

**Pattern across all six:** verify, score, enforce, gate, trace, advise — every buildable win is a **gate or a lens**, never another generator. The intent → eval → governance layer, which infra players structurally can't serve because it needs taste, not throughput.

---

## Methodology & sources

- **Tool:** `/last30days v3.0`, one GENERAL anchor pass ("how creative and marketing teams are adopting AI agents") + WebSearch supplement. 2026-05-10 → 2026-06-09. Raw dump: `~/Documents/Last30Days/how-creative-and-marketing-teams-are-adopting-ai-agents-raw.md`.
- **Sources:** Reddit with comments (14 threads, ~1,690 upvotes / ~600 comments), X (4 posts), YouTube (17 videos, 5 transcripts, ~2.0M views), Web (12+ pages: McKinsey, Jasper, EY, DigitalApplied 250-agency survey, Bloomreach, MindStudio, Coupler.io, Braze case studies). HN, Polymarket, TikTok, Instagram returned nothing on-topic — a Reddit/YouTube/web conversation.
- **Top voices:** r/AI_Agents, r/DigitalMarketing, r/AIMarketingPros; IBM Technology + Bloomberg + AI Marketers Guild (YouTube transcripts); [@researchUSAI](https://x.com/researchUSAI/status/2062338301424697591), [@BessemerVP](https://x.com/BessemerVP/status/2056441982298513503).
- **Confidence: medium-low.** Single anchor pass; corpus is marketing-adoption-skewed and uses no agentic-engineering vocabulary natively, so intent/eval/governance gaps are inferred from team pain rather than stated in tooling terms. Strength relative to the sibling: this is the directly-observed creative/marketing source the sibling *lacked* — so the pair together is materially more confident than either alone. To harden further: run the kit's remaining passes (*"AI agent frameworks people wish existed"*, *"spec-driven development and evals for AI agents"*) and fold them into both reports.
- **Related:** [[2026-06-09-agentic-engineering-intent-eval-governance-gaps]] (sibling — builder-side), [[2026-06-09-claude-code-skills-mcp-gaps-and-opportunities]], [[2026-06-09-ai-creative-tools-frustrations-and-gaps-last30days]], [[2026-06-09-ai-tools-creatives-marketers-wish-existed-last30days]], [[tool-shipping-playbook]], [[voiceprint-plugin-build-spec]], [[intent-engineering]], [[vault-knowledge]].
