---
title: "Strategic Analysis — Nate's 7 Skills + Sean's 8-Week Hunt"
created: 2026-05-06
type: career-analysis
status: working-doc
related:
  - 20_projects/prj-job-hunt-2026/README
  - 50_sources/clippings/Nate-B-Jones-AI-Credentials-Artifacts-Network
ai-context: "Strategic analysis of Nate B Jones (2026-03-25) seven-skills framework loaded against Sean's post-Block context. Output of Claude.ai session 2026-05-06."
---

# Strategic Analysis: Nate's 7 Skills, Sean's 8 Weeks

*Generated 2026-05-06 — Day 2 of the 8-week hunt. Today is verification day for the hunt's structural assumptions; Friday's retro is when the plan locks.*

---

## 1. Executive Summary — Nate's Thesis in 3 Bullets + Verdict

- **The labor market is K-shaped, not contracting.** Nate: "there are essentially infinite AI jobs right now." His 3.2-to-1 demand-to-supply ratio and the 142-day time-to-fill claim are corroborated by ManpowerGroup's 2026 Talent Shortage Survey of 39,063 employers in 41 countries, which placed AI Model & Application Development (20%) and AI Literacy (19%) as the two hardest-to-find skills globally for the first time in survey history [ManpowerGroup, 2026-02-26]. Q1 2026 saw 81,747 tech layoffs alongside ~275,000 open AI roles in the US with a 56% wage premium [Invezz/Bloomberg, 2026-05-04]. The split is real.
- **Credentials are noise; artifacts are signal.** Nate's strongest claim is that the credentialing layer ("AI for Everyone" at the top, ML PhD at the bottom) has nothing in the middle, and that hiring managers have learned to discount badges. He recommends "artifacts over badges" — a published agent product spec, a failure post-mortem, an open-sourced MCP integration. This is the most actionable claim in the piece.
- **The 7 skills are a real progression, not a checklist.** Specification Precision → Evaluation → Decomposition → Failure Patterns → Trust Boundaries → Context Architecture → Cost Economics. "The market-two premium comes from depth in at least three and working knowledge of five or more."

**Verdict in one sentence:** The 7-skills framework is the most useful artifact-driven hiring map currently in public circulation, and Sean already has working knowledge of 5 of the 7 — the leverage point is **publishing** what he's already built, not learning more.

---

## 2. Dissection — The 7 Skills, Decomposed for Sean

Honest assessment from the v2.0 context file. No manufactured gaps.

| Skill | Sean's Depth | Evidence | Highest-Leverage Gap | 8-Week Artifact to Close It |
|---|---|---|---|---|
| **Specification Precision** | **Strong** | 117 skills + 13 subagents + 14 SDK agents in the Code-Brain; PM by trade; writes specs that agents execute. The Block PM templates retained. | None at the skill level. Gap is **public evidence** that someone else can read. | Publish 2 of the existing skill files as case studies — `writing-voice-modes` and one agent — with before/after output examples. Half-day each. |
| **Evaluation & Quality Judgment** | **Working** | Phase 6 vault knowledge loop has nightly synthesizer + weekly lint — that *is* an eval pipeline. But Sean has not framed it that way externally. | No domain-specific eval framework published. The Hamel Husain / Shreya Shankar canon (3,000+ students from 500+ companies including Anthropic) is now the lingua franca recruiters expect. [hamel.dev] | Publish a domain eval framework: "Evals for the Crypto News PM" — error taxonomy from The Block work, LLM-as-judge prompts, sample test cases. The Block context is a *moat*, not a liability. |
| **Decomposition for Delegation** | **Strong** | 14 SDK agents with 7 active, multi-agent system already in production for personal use. Hybrid router exists. | Same as #1 — built it, hasn't shown it. | A 5-minute Loom walking through the agent fleet — narrated, real session, not polished. Nate explicitly calls this "underused and almost unfakeable." |
| **Failure Pattern Recognition** | **Working** | The 16BitFit sprite consistency problem was a months-long failure-mode investigation; the Alienware ICMP-blocked workaround is failure-mode thinking. | Nate's 6-pattern taxonomy (context degradation, spec drift, sycophantic confirmation, tool selection, cascade, silent) hasn't been applied as a labeling system to past failures. | One published post-mortem on a real Code-Brain incident, labeled with Nate's six patterns. Title it for SEO: "Six Failure Patterns I Hit Building 14 Production Claude Code Agents." |
| **Trust Boundary & Security Design** | **Working-leaning-Strong** | The Hard Nevers list (Block GitHub, Block WordPress, final spend, medical, relationship, career calls), the local-only finance constraint, the gemma4/phi4-mini local inference for personal data, the gitignored finance folder — this is a published trust-boundary architecture in everything but name. | Has not been written up externally. | A short post: "How I Architected Trust Boundaries for a Personal Multi-Agent Fleet" — the four-variable framework (cost of error / reversibility / frequency / verifiability) applied to Sean's actual setup. |
| **Context Architecture** | **Strong** | The vault, the operating-models per domain, HTML comment anchors for programmatic injection, persistent vs per-session context split via SOUL/HEARTBEAT/USER files — this is *exactly* what Anthropic now calls "context engineering" and what the CCA-F weights at 15%. Sean is ahead of most candidates here. | Naming. Sean calls it "the vault" and "operating models." Recruiters search for "context engineering" and "RAG architecture." | A README in the public Code-Brain repo titled "Context Architecture for a Personal Claude Code Stack" using Anthropic's vocabulary. |
| **Cost & Token Economics** | **Beginner** | This is the weakest of the seven. The context file does not mention cost models, token budgeting, or model routing economics. Local Ollama use is *price-driven* in spirit, but no published spreadsheet exists. | The full skill — input/output tokens, caching, model routing decisions, batch vs real-time tradeoffs. | An interactive cost calculator (HTML artifact + GitHub repo) for choosing between Haiku/Sonnet/Opus on a workflow. Two days. Doubles as a sellable product. |

**Strong: 3. Working: 3. Beginner: 1.** Per Nate's own framework, depth in 3 + working in 5 = market-two qualified. Sean is already there. The 8 weeks are about *demonstrating* the position, not arriving at it.

---

## 3. The Agentic Landscape — Where Q2→Q4 2026 Is Actually Heading

Nate's K-shaped framing is correct but stops short. Pushing past it:

**MCP adoption has crossed the chasm.** Smithery hosts 7,000+ servers; MCPMarket lists 10,000+ across 23 categories [TrueFoundry, 2026]. The Anthropic Forward Deployed Engineer role (Boston/NYC/Chicago) literally lists deliverables as "MCP servers, sub-agents, and agent skills that will be used in production workflows" [Anthropic Greenhouse]. Sean's Track C strategy is now the *expected* artifact for FDE-adjacent roles, not differentiation. The differentiation has moved to: *which* MCP server, *for what domain*, with *what eval framework*.

**The Claude Certified Architect launched March 12, 2026.** Free for Partner Network employees, $99 otherwise. 60 questions, 120 minutes, five domains: Agentic Architecture & Orchestration (27%), Claude Code Configuration & Workflows (20%), Prompt Engineering & Structured Output (20%), Tool Design & MCP Integration (18%), Context Management & Reliability (15%) [LinkedIn/AIM, 2026-03-16]. Nate's claim that "Accenture is rolling this out to hundreds of thousands" is plausible — Anthropic committed $100M to the Partner Network in 2026 with Accenture and Cognizant as flagship partners [Anthropic, 2026-03-12]. But the credential is six weeks old. It's not yet AWS-Cert-equivalent; it's signal that Sean is *ahead of the wave*, not that he needs it to compete today.

**The eval layer is where money is moving.** Hamel Husain and Shreya Shankar's "AI Evals for Engineers & PMs" course has trained 3,000+ engineers and PMs across 500+ companies including OpenAI, Anthropic, and Google [hamel.dev]. The September 2026 cohort is positioned around the slogan "evals are the new PRDs" (Brendan Foody) [Lenny's Newsletter]. This is Sean's lane as a PM. Hamel teaches: "Start with error analysis, not infrastructure. Spend 30 minutes manually reviewing 20-50 LLM outputs whenever you make significant changes." This is Sean's PM superpower repackaged.

**Where the puck is going that Nate doesn't see:** Three things.

1. **Agent-eval-as-a-service** is forming as a category. Braintrust, Langfuse, and Arize Phoenix are competing for the dev-tool layer; the *PM-friendly layer above them* (eval design + domain rubrics + judge-prompt versioning) is essentially empty. A small MCP server that integrates with Braintrust/Langfuse and ships pre-built judge templates for vertical domains (crypto, fintech, animation pipeline QA) is a real wedge.

2. **The "AI-washing" pattern in layoffs is creating a candidate-pool repricing.** Bloomberg data: roughly half of AI-attributed layoffs will result in the same roles rehired offshore or at lower salaries [Invezz, 2026-05-04]. Translation: the senior US AI PM seat is *more* valuable in absolute terms because companies are concentrating headcount at the top. Generalist PM seats are the ones being commoditized, which validates Sean's targeting.

3. **The animation industry is running 12-18 months behind on AI tooling adoption** — and that's the long-game opening. The studios (Pixar, Cartoon Network, Aardman) are quietly hiring AI specialists for pipeline integration, but they're hiring engineers, not PMs. By Q4 2026 the role of "Animation Pipeline PM with AI fluency" will exist. Sean's positioning into Q3 2026 (the AI PM role) is the bridge to where he actually wants to be by Q3 2027.

---

## 4. Career Strategy — 8-Week Plan Anchored to Sean's Situation

**Primary track: AI Product Manager.** Reasons: the salary band ($133K–$437K+) overlaps Sean's target; "research on 12,000+ AI PM hires found 60% don't come from CS backgrounds" — Sean's freelance-multimedia-to-PM path is now an asset, not a defect; specification, evaluation, decomposition, and trust-boundary skills are exactly what he's strongest in.

**Backup track: AI-Augmented Domain Specialist.** Specifically: *Crypto/Fintech Domain Specialist* (The Block experience + Larry Cermak as reference is unique signal) OR *Creative Pipeline Specialist* (animation + AI). Salary premium: 23-35% over equivalent roles. This catches him if Q3-Q4 hiring slows or if a creative-industry door opens unexpectedly.

**Not chosen: AI Systems Architect/Engineer.** Reason: Sean's coding fluency is beginner-to-intermediate; the depth gap can't be closed in 8 weeks; CCA-F path is a distraction relative to PM positioning. Worth pursuing in Q4 *if* he lands a PM role and wants to broaden.

**Not chosen: Agent Operations.** Reason: closer fit on paper, but the role market is still nascent ("least defined track with the most open running room" per Nate). Translation: harder to find postings, less likely to result in offers in 8 weeks.

### Week-by-Week (anchors: 5:30 wake, 9–14 deep work, 14–15 decompress, 15–17:15 comms, evening with Mary, Friday retro)

**Week 1 (May 5–11) — Foundation week. Already underway.**
- Mon-Tue (done): Severance + COBRA + outplacement Track A.
- Wed (today): Lock the artifact list. *Pick the 5 portfolio items in §5 below; commit one to ship by Friday.*
- Thu-Fri: Ship artifact #1 — the Loom agent fleet walkthrough (4 hours of deep-work time including re-shoots). Publish to a fresh GitHub README + LinkedIn post + Substack.
- Friday retro: lock the apply target (15 quality apps/week, not 50).

**Week 2 (May 12–18) — Specification artifact + first 15 apps.**
- Deep work: write the Agent Product Spec for the financial-research fleet (using Nate's "Agent Product Spec Builder" prompt as the template, then iterate). Publish.
- Comms block: 15 targeted applications. Anthropic FDE in Boston is the wildcard application — Sean is undercredentialed by years but artifact-overcredentialed. Apply.
- Outreach: 5 networking coffees with crypto/fintech PMs (use Larry as the warm-up).

**Week 3 (May 19–25) — Evaluation framework artifact.**
- Deep work: publish "Evals for the Crypto News PM" — error taxonomy from Block work, LLM-as-judge prompts, sample test cases. This is *the* differentiator artifact. Hamel's blog is the technical reference.
- Animation pipeline: lock the storyboard for the June 11 short. Pencil-test artifact.
- Apps: 15 more.

**Week 4 (May 26–Jun 1) — Failure post-mortem + cost calculator.**
- Deep work: publish the "Six Failure Patterns I Hit" post-mortem AND ship the token-cost calculator (interactive HTML artifact, GitHub repo, public Vercel deploy). Two artifacts in one week is aggressive but doable because the failure post-mortem is already lived experience.
- Apps: 15 more. Include 3 stretch apps (Anthropic Applied AI, Sierra, Decagon).
- Friday retro: midpoint check. If pipeline is dry, pivot tactics, not strategy.

**Week 5 (Jun 2–8) — Animation short crunch + Track C MCP server v0.**
- Deep work: animation short final week. The June 11 deadline holds.
- Background: ship Track C MCP server v0 (the eval-templates-for-agents idea from §5). Doesn't have to be perfect — has to be live.
- Apps: 10 (reduced for animation crunch).

**Week 6 (Jun 9–15) — Animation ships; first interviews land.**
- June 11: ship the portfolio short. Publish to YouTube + Substack + LinkedIn. The cross-pollination matters: animation is the long-game brand, not a distraction.
- Interview prep: assume 2-3 first-round interviews land this week.
- Apps: 10.

**Week 7 (Jun 16–22) — Interview cycle peak.**
- Deep work shifts from artifact-building to interview prep + take-home assignments. The artifacts are the take-homes.
- Continue the eval-framework substack with 1 more post per week (compound publishing).
- Apps: 10.

**Week 8 (Jun 23–29) — Close mode.**
- Final-round interviews + offer negotiations.
- Backup activation: if no offers by EOW, extend the runway 4 weeks and pivot apps toward backup track (domain-specialist roles) AND explore consulting (Track A from severance, Track B as bridge income).

---

## 5. Portfolio Products to Build (Job-Search Signal)

Five artifacts. Each demonstrates ≥3 of the 7 skills. All linkable. All double as Track C material.

**1. The Agent Fleet Loom (Day 1 ship — this Friday)**
- *What:* 5–7 minute unedited screen recording walking through the 14 SDK agents, showing one running live, narrating the decomposition logic and one failure mode.
- *Skills proven:* Decomposition, Failure Patterns, Specification.
- *Scope:* 4 hours. Includes re-shoots.
- *Publish:* GitHub README of `claude-code-brain` (make repo public if not already), Substack post linking to it, LinkedIn post with the Loom embedded, X thread.
- *Recruiter-eye headline:* "Built a 14-agent personal Claude Code fleet that runs my life on launchd. Here's the 5-minute tour."
- *Hard-to-fake:* Yes. Live system, real failure, narration. Cannot be cargo-culted.

**2. The Agent Product Spec — "Financial Research Fleet"**
- *What:* A 1,500-word PRD-style spec for the financial-research fleet from §8. Problem definition, escalation logic, evaluation criteria, trust boundaries, cost model. Uses Nate's "Agent Product Spec Builder" prompt as scaffolding then strips out the prompt-output flavor.
- *Skills proven:* Specification, Trust Boundaries, Cost Economics, Decomposition.
- *Scope:* 1.5 days.
- *Publish:* Substack with markdown source on GitHub.
- *Recruiter-eye headline:* "An AI PM spec for a multi-agent financial research system, including the cost model that almost killed it."

**3. "Evals for the Crypto News PM" — Domain Evaluation Framework**
- *What:* A real eval framework for the kind of work Sean did at The Block. LLM-as-judge prompts, code-based assertions, error taxonomy with examples (anonymized as needed), sampling strategy, monitoring metrics. The Hamel/Shreya school's approach applied to a vertical.
- *Skills proven:* Evaluation, Domain Specialization, Specification.
- *Scope:* 3 days.
- *Publish:* GitHub repo + Substack longform.
- *Recruiter-eye headline:* "I shipped this eval framework for crypto-news AI products. The error taxonomy alone took 14 production failures to assemble."
- *Why this is the wedge:* Almost no public eval frameworks exist for crypto/fintech AI. This single artifact defines a category.

**4. "Six Failure Patterns I Hit Building 14 Production Claude Code Agents" — Post-Mortem**
- *What:* A real post-mortem labeled with Nate's six patterns + Sean's own additions if any emerged. One pattern per section, one screenshot or log per pattern, one fix per pattern.
- *Skills proven:* Failure Patterns, Evaluation, Trust Boundaries.
- *Scope:* 2 days.
- *Publish:* Substack, link from GitHub repo READMEs.
- *Recruiter-eye headline:* "Production agent systems fail in six predictable ways. I hit all six."

**5. The Token Cost Calculator (HTML artifact + GitHub)**
- *What:* Interactive calculator: input expected workflow steps, model choice per step, expected token volume, frequency. Output: monthly cost across Haiku/Sonnet/Opus mix, with sensitivity analysis. Published as a single-file HTML artifact.
- *Skills proven:* Cost Economics (the #1 Sean gap), Specification, Decomposition.
- *Scope:* 2 days. Use Anthropic's API in Artifacts capability — the calculator can actually call Sonnet to demo a real run.
- *Publish:* Public Vercel deploy + GitHub repo + Substack write-up.
- *Recruiter-eye headline:* "Closed my biggest knowledge gap by building the tool I wished existed. Try it: [link]."
- *Cross-purpose:* Doubles as a sellable product (see §6).

---

## 6. Sellable Products (Cushion-Building Income Streams)

Anchored to "every win counts" + "build don't buy." Each $50–$2000/month range. Distribution biased toward lowest-effort channels.

**1. `claude-eval-templates` MCP Server — $99 one-time + $19/mo for updates**
- *Who buys:* Indie devs and small AI teams shipping LLM features who need eval scaffolding fast. Hamel's course has 3,000+ alumni; many would pay to skip the setup.
- *What it costs to build:* ~3 days. A node MCP server exposing pre-built LLM-as-judge templates per domain (crypto, fintech, customer support, content moderation), plus a versioning layer.
- *Run cost:* ~$10/mo (Vercel + minimal storage).
- *Distribution:* List on MCPize (85% revenue share, Stripe payouts, the only marketplace currently paying creators) [mcpize.com]. Cross-list on Smithery for free discovery. Substack launch post.
- *Realistic:* $100–500/mo within 90 days if positioned correctly.

**2. The Token Cost Calculator (Pro version) — $29 one-time**
- *Who buys:* Solo PMs, technical founders, agency owners scoping AI engagements. The free version is the lead magnet (portfolio artifact #5); the Pro version adds: multi-workflow comparison, CSV export, batch vs real-time modeling, custom model pricing import.
- *Build:* +2 days on top of the free version.
- *Run cost:* near-zero.
- *Distribution:* Gumroad (10% fee, instant payout). Stripe link from the free-version page.
- *Realistic:* $50–300/mo. Compounds with every Substack post that links to the free version.

**3. "The Animation Pipeline Eval Pack" — $49 (digital pack)**
- *Who buys:* Small animation studios and indie animators experimenting with AI assist. Nano Banana Pro / Kling / Veo users who are losing hours to bad outputs.
- *What it is:* A pack of 30 eval prompts + 10 character-consistency test cases + a Notion template for tracking style drift across frames. Sean's existing 16BitFit sprite-consistency work is the moat.
- *Build:* 2 days, mostly packaging.
- *Distribution:* Gumroad. Animation industry Discord communities.
- *Realistic:* slow start, but unique positioning. Long-game brand-builder for the animation-PM north star.

**4. `crypto-news-eval` GitHub repo (open source, GitHub Sponsors)**
- *Who buys:* No direct buyers. This is a brand asset. The GitHub Sponsors button is there if anyone wants to throw $5/mo, but the real value is interview signal.
- *Cost:* same as artifact #3 in §5 — already being built.
- *Distribution:* Reddit r/CryptoCurrency dev threads, HackerNews launch post, X thread tagging Larry and key crypto-AI accounts.
- *Realistic income:* $0–50/mo. Real value: warm intro currency.

**5. "Failure Patterns Field Guide" — $19 (Gumroad PDF)**
- *Who buys:* Mid-level PMs and ops people moving into AI. Companion to the post-mortem artifact (#4 in §5). Includes a printable diagnostic flowchart, the six patterns with detection signals, mitigation playbooks per pattern.
- *Build:* 1 day if the post-mortem is done first.
- *Distribution:* Gumroad. Linked from every post-mortem read.
- *Realistic:* $50–200/mo. The flowchart is the thing people share.

**Honest expectation:** $300–1,000/mo combined within 90 days *if* distribution gets attention. The sellable side is secondary to the job-hunt signal. Treat income as bonus.

---

## 7. Where Nate Is Probably Wrong / What He's Underselling

**Steel-man first.** Nate has been kicking around tech for decades; the seven skills are extracted from real postings, not invented; the K-shaped split is corroborated by independent data; the failure-pattern taxonomy is genuinely useful even if the bundling is his own construction (he admits this); the artifact-over-credential argument is empirically true for the current moment.

**Where he overreaches:**

1. **"Essentially infinite AI jobs."** Hyperbole. Q1 2026 had ~275,000 AI postings open in the US against ~518,000 qualified candidates globally per Second Talent — that's a real 3.2:1 ratio, but "infinite" is rhetorical. For Sean's specific Boston-metro AI PM bucket, the actual count is ~60-80 active postings on any given week per a Built In Boston scan [Built In, 2026-05]. Plenty, not infinite. The targeting matters more than the volume.

2. **The 142-day time-to-fill cuts both ways.** Nate frames it as employer pain. From Sean's side, it means *Sean's interview cycles will be slow*. Median Bay Area senior tech time-to-hire is at 2022-wave levels [Invezz]. The 8-week plan should assume that final offers may not land until week 10-12. Plan severance accordingly.

3. **The Nate's Network and AiCred plugs are commercial.** Both are Nate's own products. He's selling vetted-network access and a $1-credit assessment. The advice is real; the business model behind the advice is also real. Sean has zero obligation to sign up for either, and the AiCred assessment can be replicated for free with an honest hour of self-scoring against the 7 skills (see §2).

4. **"Taste is not a skill" is half-right.** Nate is correct that "develop taste" is unactionable. But the seven skills he names *are* taste, decomposed. He's not refuting Graham/Altman — he's operationalizing them. Sean should not internalize this as "taste doesn't matter" but as "here are the parts of taste you can practice."

5. **The CCA-F is six weeks old.** Treating it as an AWS-equivalent credential is forward-looking, not present-tense. Nate's framing implies the certification is necessary now; in fact, *artifacts* are necessary now and the credential is a nice-to-have for 2027. Sean's $99 is better spent on a Loom Pro subscription and Substack Pro.

**What Nate is underselling that Sean should over-index on:**

1. **Context architecture as a librarian skill.** Nate makes the librarian/technical-writer translation in passing — "context architecture is like building the Dewey Decimal System for agents." For Sean, whose vault is a working production-grade context architecture, this is the easiest skill to weaponize on a resume. It deserves headline placement.

2. **The "publish a real working session" advice in §"How to prove it"** is buried but is the single highest-leverage tactic in the entire piece. "Record yourself working with an AI system and narrate your decisions in real time. Not a polished tutorial. A real working session... The transparency is the credential." Sean's Friday Loom should hold this directly.

3. **Cost economics as a *PM* skill, not just an engineer skill.** Nate puts cost economics at #7 and frames it as senior-engineer territory. For an AI PM, the ability to model unit economics on an agent workflow is a differentiator that almost nobody applying for PM roles brings. Sean's gap is also his biggest single-week opportunity.

---

## 8. The 5 Decisions This Week

**Decision 1: Primary track lock.**
Default: AI PM. Switch only if: Sean lands a Boston-metro Anthropic FDE first-round, in which case the FDE-track conversation overrides — the "PM vs engineer" question gets reopened by the actual interview.

**Decision 2: Apply volume.**
Default: 15 high-quality applications per week, each with a custom artifact link. Switch only if: by end of Week 3, response rate is below 5% — then increase volume to 25/week and reduce per-app customization to title/intro only.

**Decision 3: Ship cadence.**
Default: One major published artifact per week, Friday by 5 PM, no exceptions. Switch only if: an interview take-home assignment in a given week consumes the artifact-building block — in which case the take-home *is* the artifact (publish it after the cycle ends).

**Decision 4: Substack vs. dev.to vs. LinkedIn-only.**
Default: Substack as the primary publishing home, LinkedIn for distribution, GitHub for code. Reasons: Sean already reads Substack daily, Nate's mentor-influence is on Substack, and the long-form format suits artifact write-ups. Switch only if: by Week 4, Substack subscriber count is < 25 — then add dev.to mirroring for SEO.

**Decision 5: Animation short cushion.**
Default: June 11 deadline holds; the short ships even if it's at 80% of vision. Switch only if: a final-round interview lands the week of June 8 — in which case slip the short to June 18 *and only by one week*. This is the long-game brand and slipping past one week starts to compound.

---

## 9. Open Research Questions

**1. What's the actual current state of AI PM hiring at the named companies (Sierra, Decagon, Pair Team, Glean, Robinhood, Scale AI) for Sean's seniority band?** Nate cites them as a class; a candidate-side scan would tell whether the realistic apply list is 6 companies or 60. *Sean to scan or follow-up Claude session to research.*

**2. Is there a Boston-metro AI/agentic-AI meetup or in-person community worth one evening per week of attendance?** The context file notes "Communities: None currently. Open to free communities for learning + networking." Boston has the MIT/Harvard ecosystem; whether anything specific to MCP/Claude Code exists locally is worth 30 minutes to verify.

**3. What does Larry Cermak's reference letter actually say or look like, and can it be pre-positioned as a quotable LinkedIn endorsement vs. a back-channel call?** A written, public endorsement from the President of a known crypto media company is a credential Nate undersells (he focuses on artifacts, not references). The asymmetry of having the *layoff-deliverer* as the *primary reference* is a story worth telling carefully.

**4. Does the financial-research-fleet idea (Perplexity API + Gemini Deep Research MCP + NotebookLM MCP + Block crypto API + GitHub/Reddit/YouTube scraping) survive a public-publishing test?** Some of the data sources may have ToS issues if positioned as a product. A 30-minute review would clarify whether artifact #2 in §5 needs to genericize away from the actual data sources.

---

*Cross-pollination note for §10 of Sean's brain that doesn't exist in this output: the eval framework artifact (§5 #3) and the financial-research fleet (§8 active focus) are the same project told two different ways. Building one ships both.*
