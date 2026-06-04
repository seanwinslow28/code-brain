---
title: "Anthropic PM Interview Guide"
source: "https://www.insiderloops.com/guides/anthropic"
author:
  - "[[Insider Loops·Last updated Jun 2026]]"
published:
created: 2026-06-04
description: "Insider Loops' operational breakdown of Anthropic's PM interview loop — all 6 stages (Recruiter → HM → Case Presentation → Onsite Loop → Team Matching → Offer), with deep coverage of the universal Culture Interview and the live Customer Scenarios round no public resource documents."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [product-management]
ai-context: "Insider Loops' stage-by-stage Anthropic PM interview guide (L3–L7, all product areas) — covers the universal Culture Interview (rehearsed STAR stories = #1 failure mode) and the live Demo-Claude Customer Scenarios round; directly relevant to Sean's [[prj-job-hunt-2026]] Anthropic prep."
---
A comprehensive resource for product managers targeting roles at Anthropic. This guide synthesizes insights from insider candidates who completed the full interview loop, Anthropic's own published guidance, and extensive research. Unlike generic resources, this guide covers rounds that no public resource breaks down with the operational detail you need to actually prepare.

**Who it's for:** PM candidates targeting Anthropic across all seniority levels (L3–L7) and product areas — Platform/API, Claude Code, Consumer (claude.ai), Research, and Safeguards. The guide is especially valuable for candidates transitioning from traditional tech companies who need to understand why Anthropic's process differs fundamentally from FAANG loops.

**Why Anthropic's process is uniquely difficult:** Two factors set it apart from standard PM loops:

1. The Culture Interview is universal — every candidate, every role, every level. No other major tech company runs a dedicated 45-minute values interview for all hires. Pre-packaged STAR stories are the documented #1 failure mode.
2. The Customer Scenarios round has required candidates to demonstrate Claude live, in real time, with the interviewer playing a customer. This has been documented for some product areas — prepare for it regardless, but note the format may vary by team. No public resource covers this round.

*This guide is for personal use only. Sharing without consent is not allowed.*

*Created with ❤️ by [Ben Erez](https://www.linkedin.com/in/benerez/) and [Marc Baselga](https://www.linkedin.com/in/marcbaselga/) at [Insider Loops](https://www.insiderloops.com/)*

---

## 1\. Interview Process Overview

### 1.1 At a Glance

| Item | What to know |
| --- | --- |
| Typical timeline | Onsite to offer typically takes 4–8 weeks total, including 2–4+ weeks for team matching with no communication during that period |
| Total rounds | 6 stages: Recruiter Screen → HM Screen → Case Presentation → Onsite Loop → Team Matching + Offer. The Onsite Loop consists of 5–6 individual interviews |
| Highest-risk eliminators | The Culture Interview eliminates candidates who rely on rehearsed STAR stories. The Customer Scenarios round has zero public prep resources. The Case Presentation disqualifies AI-generated work automatically |
| Process variability | Referral candidates may skip the recruiter screen entirely. Onsite is typically scheduled across 1–2 days via video call |
| Core prep implication | This is a mission-driven product leadership role. Generic PM prep is necessary but not sufficient — every stage has Anthropic-specific dimensions that standard preparation alone won't address |

### 1.2 Stages of the Process

| Stage | Name | Format | Duration |
| --- | --- | --- | --- |
| 1 | Recruiter Screen | Phone or video call | 20–30 minutes |
| 2 | Hiring Manager Screen | Video call with product area HM | 20–60 minutes |
| 3 | Case Presentation | Take-home exercise + live panel defense | 3 hours writing + 45 minutes defense |
| 4 | Onsite Loop | 5–6 interviews over 1–2 days | ~7 hours total |
| 5 | Team Matching + Offer | Internal team circulation + offer | 2–4+ weeks |

### 1.3 What Each Stage Evaluates

| Stage | Primary Filter | What Kills You |
| --- | --- | --- |
| Recruiter Screen | Mission knowledge, communication, role fit | Not knowing Anthropic's mission — documented rejection for this. Inability to articulate a strong, specific answer for why Anthropic over OpenAI |
| HM Screen | Product depth, domain fluency, role-specific judgment | Generic PM pitch without AI depth; no product usage |
| Case Presentation | Product judgment, scoping, authentic reasoning | AI-generated output; boiling the ocean; proposing features instead of products |
| Culture Interview | Values alignment, intellectual honesty, safety reasoning | STAR stories, parroting safety talking points, pure optimism or pure doomerism |
| PM Rounds (L&I + AI P&E) | Cross-functional leadership, take-home defense, conviction | Rehearsed behavioral stories; inability to defend your own work |
| XFN Rounds (Tech + Customer) | System thinking, live product fluency, customer discovery | Jumping to solutions; not being fluent driving the product live; panic on bad model output |
| Team Matching | Team headcount, domain fit, mutual interest | Passing every round but no team has headcount |

*L&I = Leadership & Influence; AI P&E = AI Product & Execution*

### 1.4 How Elimination Works

Unlike traditional tech interviews where one round is the obvious gate, Anthropic's process has multiple independent elimination points. Understanding where candidates actually fail — and why — is the foundation of effective prep.

| Filter | What Separates Pass from Fail |
| --- | --- |
| **Culture Interview** | Authentic reasoning vs. rehearsed answers. The interviewer has seen hundreds of STAR stories — yours won't impress them. What impresses them is watching you think through a hard question in real time and change your mind mid-answer |
| **Customer Scenarios** | Live product fluency vs. slideware PM. If you can't write a prompt and iterate on bad output live in front of someone, no amount of product sense preparation will save you |
| **Case Presentation** | Your judgment vs. Claude's judgment. The take-home is designed to be *"sufficiently out of distribution"* for AI. Authentic, opinionated, imperfect work passes. Polished, comprehensive, generic work fails |
| **Team Matching** | Breadth vs. narrowness. Candidates who express interest in only one team have one shot at matching. Those who genuinely engage with 2–3 areas multiply their odds |

[Culture, Values & Mission](#culture-values-mission)

## 2\. Culture, Values & Mission

Anthropic evaluates mission alignment at every stage — not just in the Culture Interview. Understanding the values is table stakes. Understanding how they apply to product decisions at each interview stage is what separates candidates who pass from candidates who don't.

### 2.1 The 7 Core Values

INSIDER

**Insider:** The 7th value — **"Ignite a race to the top on safety"** — is the one most frequently missed by candidates. Don't skip it.

| # | Value | Interview Application |
| --- | --- | --- |
| 1 | **Act for the global good** | Do you zoom out to societal impact, or stop at user-level thinking? Interviewers probe for second-order consequences and long-term externalities |
| 2 | **Hold light and shade** | The most distinctive value. Pure optimists AND pure doomers fail. You must articulate specific risks AND specific benefits simultaneously |
| 3 | **Be good to our users** | Expand "user" beyond the person clicking buttons. Consider policymakers, employees, affected communities |
| 4 | **Do the simple thing that works** | In product and technical rounds, over-engineered solutions are penalized. *"We don't invent a spaceship if all we need is a bicycle"* |
| 5 | **Be helpful, honest, and harmless** | Applies to the organization, not just the model. *"High-trust, low-ego."* Can you be honest about failures without spin? |
| 6 | **Put the mission first** | Screening question: *"Would you accept your stock going to zero if Anthropic decides not to release models for safety reasons?"* They declined a $200M Pentagon contract on principle |
| 7 | **Ignite a race to the top on safety** | Understand the game theory: why publish safety research that helps competitors? Why advocate for standards that constrain your own products? |

### 2.2 AI Safety Positions to Know

**Core Views on AI Safety** — Anthropic's foundational document. The framework is WHEN / WHY / WHAT / HOW:

- **WHEN:** Transformative AI — including AGI (Artificial General Intelligence) — possible this decade
- **WHY:** Technical alignment AND societal disruption — most candidates only discuss technical risks, which is a gap interviewers notice. AGI risk is one of the key concerns: a system that surpasses human-level capabilities across domains with misaligned goals
- **WHAT:** Portfolio approach covering optimistic, intermediate, and pessimistic scenarios
- **HOW:** Empiricism — *"we do not know how to train systems to robustly behave well"*

PRO TIP

**Success:** That foundational admission — *"we do not know"* — is the intellectual honesty Anthropic screens for. Mirror it in your own reasoning. Don't pretend to have clean answers.

**RSP v3.0 controversy (February 2026):**

The Responsible Scaling Policy (RSP) is Anthropic's public self-commitment about how it will behave as its models become more powerful — essentially a set of rules Anthropic imposes on itself, tied to safety evaluation thresholds called AI Safety Levels (ASLs). Version 3.0, published February 2026, triggered public controversy because it appeared to loosen limits that earlier versions had treated as hard constraints. If you're interviewing at Anthropic, you will be asked to engage with this tension. Here's what you need to know:

- ASL-3 safeguards activated May 2025
- v3.0 removed hard limits on training without proven safety measures
- CSO [Jan Leike](https://jan.leike.name/) called prior limits *"naive"*; a Safeguards team head resigned
- Dual mitigation framework: unilateral commitments vs. industry-wide action

WARNING

**Warning:** Do not dodge the RSP controversy. Engage with the genuine difficulty of maintaining safety commitments while competing against companies with none. This tension IS **"Hold light and shade"** in action. Candidates who dismiss either side fail.

**Constitutional AI:** Two-phase training (self-critique + RLAIF) to produce a priority ordering: **safe > ethical > compliant > helpful**. This ordering explains product decisions you may be asked about — it's why Claude behaves the way it does when safety and helpfulness conflict.

### 2.3 Key Terminology

| Term | What You Must Know |
| --- | --- |
| [Constitutional AI (CAI)](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) | How it differs from RLHF; why explicit principles beat implicit ones |
| [Responsible Scaling Policy (RSP)](https://www.anthropic.com/news/responsible-scaling-policy-v3) | ASL levels, v3.0 controversy, dual mitigation framework |
| AI Safety Levels (ASLs) | ASL-3 activated; ASL-4/5 undefined |
| Mechanistic Interpretability | Reverse-engineering neural networks for transparency |
| *"Country of geniuses in a datacenter"* | [Dario Amodei](https://www.linkedin.com/in/daboramodeiai/) 's metaphor from [*"Machines of Loving Grace"*](https://www.darioamodei.com/essay/machines-of-loving-grace) |
| Helpful, Honest, Harmless (HHH) | Model property AND organizational value |
| Dario Vision Quest (DVQ) | Biweekly all-hands; radical transparency |

### 2.4 Product Leadership

Understanding who leads product decisions shapes how you answer questions about team dynamics and decision-making.

| Leader | Role | Background |
| --- | --- | --- |
| [**Ami Vora**](https://substack.com/@amivora) | Head of Product | Former VP Product at WhatsApp. Known for hiring playbook and product org scaling |
| [**Scott White**](https://www.linkedin.com/in/scottiewhite/) | Head of Product, Claude | Former product lead at Airtable and Instacart. *"Try to build stuff to develop your intuition"* |
| [**Cat Wu**](https://www.linkedin.com/in/cat-wu/) | Head of Product, Claude Code | Focus on developer tools and terminal-native workflows. *"PMs build prototypes and evals"* |

NOTE

**Note:** Anthropic uses a four-legged team model: PM + Designer + Engineer + AI Researcher. The researcher role varies by team. When discussing team structure in interviews, reference this model.

### 2.5 Mission Alignment

Most candidates prepare for mission questions only for the Culture Interview. This is a critical mistake. Mission alignment is evaluated independently at every stage — and falling short at any one can end your candidacy. Use this as a preview of what to expect:

- **Recruiter Screen:** *"Why Anthropic?"* must reference specific safety work, not generic AI enthusiasm. Candidates have been rejected here for not knowing the mission
- **HM Screen:** Mission + product-area-specific safety reasoning. *"How does safety intersect with the product you'd be working on?"*
- **Case Presentation:** Every product proposal must have a safety story woven in — not bolted on at the end
- **Culture Interview:** 45 minutes of live safety reasoning. The deepest probe
- **PM Rounds:** Safety-capability tradeoff questions surface repeatedly
- **XFN Rounds:** System design must include safety as a first-class requirement. *"A system that is fast but produces harmful outputs is considered broken"*

[Recruiter Screen](#recruiter-screen)

## 3\. Recruiter Screen

### 3.1 At a Glance

| Item | What to know |
| --- | --- |
| Duration | 20–30 minutes |
| Format | Phone or video, conversational |
| Primary filter? | Low — but automatic rejections happen for mission ignorance |
| Key focus | Credibility, timing, mission understanding, potential contribution |
| May be skipped | Yes — referral candidates sometimes go directly to HM |
| Interviewer | PM recruiter (varies) |

### 3.2 What Actually Happens

Most candidates treat this like a scheduling call. It's not. The recruiter is actively screening — and candidates have been cut here for giving generic answers about AI enthusiasm. Treat every minute as an evaluation.

The recruiter needs to walk away confident on four dimensions. If any one is weak, you don't advance.

**Dimension 1: Your credibility.** What have you actually built? Don't narrate your career history — pick one or two projects and go specific on what you did, what you shipped, and what the outcome was.

| Strong | Weak |
| --- | --- |
| *"I led the API platform redesign that reduced developer onboarding from 3 days to 4 hours. I wrote the evals that measured success."* | *"I've been a PM for 8 years and I'm excited about AI."* |

**Dimension 2: Your timing.** Why are you making a move now? The recruiter is gauging whether this is a deliberate career decision or an opportunistic AI gold rush.

| Strong | Weak |
| --- | --- |
| *"After reading 'Machines of Loving Grace,' I saw how Anthropic thinks about the next 5–10 years. That long-term vision matches how I think about product work."* | *"AI is the future and I want to be part of it."* |

**Dimension 3: Your mission understanding.**

CRITICAL

**Critical:** Not knowing Anthropic's mission is an automatic rejection. A technically brilliant candidate — senior developer, open-source contributor — was eliminated for giving a generic answer about wanting to transition into AI. This is documented.

Strong answers reference: (1) Why Anthropic exists as separate from OpenAI — the founding story, (2) What the RSP means in practice, (3) Why safety-first resonates with your product philosophy — with nuance, not platitudes.

| Strong | Weak |
| --- | --- |
| *"After reading the RSP, I saw how Anthropic operationalizes safety rather than just talking about it. The founding story — and the decision to walk away from OpenAI on principle — is what makes 'Why Anthropic' a real answer for me."* | *"I'm really passionate about AI and I want to work on something meaningful."* |

**Dimension 4: Your potential contribution.** At a ~25-person PM team, every PM has outsized ownership. The recruiter wants to hear what you'd create or discover — not what you'd manage or oversee.

| Strong | Weak |
| --- | --- |
| *"I've been building with the Claude API for three months. I see a gap in how enterprise developers onboard — I'd want to own that problem."* | *"I'd love to help manage products and collaborate with the team to drive impact."* |

**Before the call:** Read [*"Machines of Loving Grace,"*](https://www.darioamodei.com/essay/machines-of-loving-grace) [Core Views on AI Safety](https://www.anthropic.com/news/core-views-on-ai-safety), and the [RSP](https://www.anthropic.com/news/responsible-scaling-policy-v3). Use Claude for at least a week. Research the specific product area and role posting. Write out your answers to all four dimensions — not to memorize, but to ensure you can articulate each in under 2 minutes.

**During the call:** Your job is to be memorable for the right reasons. Lead with specificity — not *"I'm passionate about AI"* but *"I built a classification pipeline with the Claude API that processes 500 support tickets daily."* Name Anthropic-specific work that excites you.

**After the call:** Ask the recruiter for specific preparation guidance for subsequent rounds. Good recruiters customize — growth roles screen for experimentation experience, platform roles verify API knowledge, new product areas assess comfort with ambiguity. Also confirm whether you're being considered as a talent-pool hire or for a specific role on a specific team (common for Labs and Research). The answer shapes your team-matching expectations and how much product-area breadth to signal in later rounds.

### 3.3 Common Questions

- "Tell me about yourself, your experience, and how you ended up interested in Anthropic."
- "Why Anthropic? Why now?"
- "What specific problem or area would you want to own here?"

### 3.4 Common Pitfalls

| Pitfall | Preparation Strategy |
| --- | --- |
| Not knowing the mission | Read *"Machines of Loving Grace,"* Core Views, and the RSP before the call. Budget 30 minutes for reading, not 30 seconds |
| Generic *"AI is exciting"* enthusiasm | Name something specific: a product decision, a research paper, a policy choice |
| Revealing salary expectations | Deflect: *"I trust Anthropic's compensation philosophy."* They pay top of market by design |
| Overselling accomplishments | *"High-trust, low-ego"* culture. State facts without superlatives |

[Hiring Manager Screen](#hiring-manager-screen)

## 4\. Hiring Manager Screen

### 4.1 At a Glance

| Item | What to know |
| --- | --- |
| Duration | 20–60 minutes |
| Format | Video call with the hiring manager for your target product area |
| Primary filter? | **Yes — last gate before the take-home** |
| Key focus | Product depth, domain fluency, role-specific judgment |
| Interviewer | Product area HM (see table below) |

### 4.2 Product-Area Expectations

The HM screen is calibrated to the specific team. What impresses on Platform will fall flat on Consumer.

| Product Area | Expectations |
| --- | --- |
| **Platform / API** | API design principles, developer experience, model serving tradeoffs, evidence you've built something with an LLM API |
| **Claude Code** | Developer tools, IDE integrations, terminal-based agent workflows (not chatbot), eval frameworks, competitive landscape. Min 5 years PM + engineering background, at least 12 months as a practicing engineer |
| **Consumer (claude.ai)** | Consumer product intuition, growth mechanics, habit formation, Claude's personality differentiation. Former consumer founders preferred, 8+ years PM experience |
| **Research** | Research monetization, eval frameworks, working with PhD researchers, uncovering latent use cases for nascent technologies |
| **Safeguards** | Trust & safety systems, policy-to-product translation, risk frameworks, RSP v3.0 including the controversy |

### 4.3 How to Approach

**Before the call — three non-negotiables:**

1. **Use the product.** If API: build a prototype. If Claude Code: use it on a real project. If Consumer: use [claude.ai](https://claude.ai/) daily for a week and log friction points. Non-negotiable.
2. **Research the HM.** LinkedIn, published talks, blog posts. Platform HMs typically have deep technical backgrounds; Consumer HMs come from growth-oriented roles. Tailor your conversation to their domain.
3. **Prepare your flagship project narrative.** Lead with a 2-minute summary — clear ownership and measurable impact — then go 15 minutes deep if probed.

**During the call:** The HM is answering one question: *"Does this person have the judgment and domain fluency to ship products on my specific team?"* Every answer should connect to the product area. If you're interviewing for Platform, don't talk about consumer growth — talk about API ergonomics, developer experience, and infrastructure tradeoffs.

**The unspoken evaluation:** The HM is also calibrating your level. They won't tell you this. The depth of your strategic thinking and the scope of your examples determine whether you land L4, L5, or L6.

### 4.4 Common Questions

**Product & Strategy**

- "Tell me about a recent product you've helped lead. What KPIs did you use?"
- "Walk me through a product you shipped. What was the hardest trade-off?"
- "Describe your most impactful project. What was your contribution vs. the team's?"
- "How would you prioritize between a capability improvement and a safety improvement?"
- "What's your approach to prompt engineering?"
- "What features would you build to make Claude more useful, independent of model improvements?"
- "How would you improve Claude's context handling?"
- "What features would you add to Claude Code?"

**Behavioral & Culture Fit**

- "Why Anthropic? Why now? Why this specific team?"
- "What specific day-to-day activities give you energy? Describe your ideal day."
- "How have you structured teams in the past, and how has your view on AI team structure changed?"
- "Walk me through a product or project you're particularly proud of — end to end, from kickoff to outcome. What was one of the big challenges you faced, and what would you do differently?"
- "Tell me about a time you had to make a time-sensitive decision with limited data."
- "Tell me about a time you worked with someone who didn't think they needed your help — how did you earn their trust?"

**Strategic / Big Picture**

- "What do you believe about the current wave of AI that isn't a commonly held belief, and what are the implications for Anthropic?"
- "If you were building a new company today, how would you change your approach to product and company building?"

INSIDER

**Insider:** Anthropic interviewers ask extensive follow-up questions that require genuine understanding. One candidate told us: *"The interviewers' follow-ups were deeper than any interview I'd done before — they kept peeling back layers until they found the edge of what I actually knew."*

### 4.5 Pass/Fail Signals

| Dimension | Strong Signal | Red Flag | How to Prepare |
| --- | --- | --- | --- |
| **Product depth** | Has built with the relevant product; articulates specific limitations and opportunities | Has read about the product but not used it | Build a prototype (API) or use Claude Code on a real project — have a real answer to *"what have you built?"* |
| **Domain fluency** | Speaks naturally about API design, developer experience, or consumer growth depending on team | Generic PM language without AI or product-area specifics | Research your target team's competitive landscape and recent launches |
| **Ownership** | Uses *"I"* for decisions, *"we"* for team execution; attributes impact clearly | Claims team credit or hedges on personal contribution | Prepare your flagship narrative with a clear first-person account of your specific decisions |
| **Safety integration** | Naturally weaves safety into product discussion | Treats safety as separate from product thinking or doesn't mention it | Prepare a nuanced position on capability-safety tradeoffs specific to the product area |
| **Strategic scope** | Discusses product vision and competitive positioning | Focuses only on feature-level execution | Have a perspective on where the product area is heading in 12–18 months |

NOTE

**Note:** The HM is calibrating your seniority level throughout this call, even though they won't tell you that's happening. The depth and scope of your answers — not your current title — determine whether you land at L4, L5, or L6. Once Anthropic sets your level, it is non-negotiable: you will not be informed of it, and there is no appeal process.

### 4.6 How to Stand Out

- **Demonstrate product usage with specificity.** Don't say *"I've used Claude."* Say *"I built a classification pipeline with the API that processes 500 customer tickets daily. Prompt caching cut my costs by 40%, but I noticed the Batch API has a 24-hour latency that doesn't work for our use case."* That sentence tells the HM you understand pricing, infrastructure tradeoffs, and real product limitations.
- **Show you've thought about the product area.** If targeting Platform/API, have a perspective on MCP's context window overhead. If targeting Claude Code, know the competitive landscape — GitHub Copilot still dominates market share among paid AI coding tools, Cursor has scaled past $500M ARR with its IDE-native approach, and Claude Code is carving out a distinct category by operating in the terminal rather than the editor.
- **Ask questions that reveal strategic thinking.** *"How does the team think about the tradeoff between model capability improvements and product surface improvements?"* is better than *"What's the team working on?"*

[Case Presentation](#case-presentation)

## 5\. Case Presentation

### 5.1 At a Glance

| Item | What to know |
| --- | --- |
| Duration | 3 hours for the take-home + 45 minutes for the panel defense |
| Format | Written deliverable (<3 pages) followed by live presentation and Q&A |
| Primary filter? | **Yes — AI-generated work is grounds for disqualification** |
| Key focus | Product judgment, scoping discipline, authentic reasoning |
| Panel | Typically 2–5 reviewers: the hiring manager, at least one engineering or design leader, and often an additional cross-functional reviewer. Format may vary |
| Timing | The take-home is submitted in advance; the panel defense may happen during the Onsite Loop (as the AI Product & Execution round) rather than as a standalone round — confirm with your recruiter |

### 5.2 The Take-Home

Take-home prompts follow a consistent structure — propose a new product for your target team's domain, scoped to a small team and short timeframe — but the specifics vary by product area. Here are two real examples:

> **Q (API / Platform):** *"The [Anthropic API](https://docs.anthropic.com/en/api/messages) gives developers direct access to Anthropic's models — prompting, system instructions, and controls for sampling behavior. What new product would you build for API customers? Choose a direction that is meaningful to customer success and improves business outcomes. Address the customer journey — onboarding, adoption, and migration. Scope for one team (5–10 engineers) in a 6-month timeframe."*

> **Q (Claude Code):** *"Anthropic wants to grow the adoption of Claude Code among Fortune 2000 companies. Propose a feature that would increase the virality of the product within an organization. Choose a direction that is a compelling market (from a size, product-market fit, and competitive landscape perspective) and is achievable by a small team of 5 engineers in a 3-month timeframe."*

Notice the pattern: both ask you to propose a product, both constrain the team size and timeline, and both require you to justify the market. But the audience differs (developers vs. enterprise), the team size shifts (5–10 vs. 5), and the timeline tightens (6 months vs. 3). Your prompt will be tailored to the product area you're interviewing for.

The suggested amount of time is 3 hours. Output: fewer than 3 pages total.

| Constraint | What It Tests |
| --- | --- |
| *"New product" / "Propose a feature"* | Product-level thinking, not incremental improvements |
| *"Meaningful to customers AND business" / "Compelling market"* | Dual mandate — one-sided answers fail |
| *"Customer journey" / "Virality within an organization"* | Full-lifecycle thinking — how does this spread and stick? |
| *"5–10 engineers, 6 months" / "5 engineers, 3 months"* | Scoping judgment — tighter constraints demand sharper prioritization |
| *3 hours, <3 pages* | Prioritization under pressure |

### 5.3 Prompt Patterns by Area

Both prompts above share the same skeleton. Here's what we know about how the domain shifts by team:

| Product Area | Confirmed Prompt Direction | Scoping |
| --- | --- | --- |
| **API / Platform** | New product for API customers; customer journey focus | 5–10 engineers, 6 months |
| **Claude Code** | Enterprise adoption / virality within organizations | 5 engineers, 3 months |
| **Consumer (claude.ai)** | Feature or product for end-users (not yet confirmed) | TBD |
| **Research / Labs** | Three-part written deliverable — capability prediction, product proposal (2–3 pages), and working prototype — reviewed offline first; a 60-min onsite presentation follows only if the written work clears the bar. Panel is HM + a senior engineering leader; expect deep technical questions alongside product judgment. | ~15–20 hours total; no explicit team/timeline constraint |
| **Safeguards** | Product supporting safety infrastructure or eval tooling (not yet confirmed) | TBD |

INSIDER

**Insider:** One candidate reported their case prompt had no clear connection to their target role. The abstract framing may be by design — testing transferable product thinking. Do not panic if the prompt feels disconnected from your team.

### 5.4 Deliverable Structure

| Section | Length | Purpose |
| --- | --- | --- |
| Product concept + integration | ~0.5–1 page | What you're building, how it fits Anthropic's ecosystem, why it matters |
| Target audience + PMF testing | ~0.5–1 page | Who benefits, how you validate, what metric signals success |
| Strategy rationale | ~0.5–1 page | Why this over alternatives, business connection, competitive positioning |

> **Pro Tip:** Do not spend space describing Anthropic's current products back to them. They know what their API does. One sentence of context is enough. Use the rest of your pages for what is new and why.

### 5.5 The "Do Not Use AI" Rule

Anthropic's official guidance: *"Take-home assessments: Complete these without Claude unless we indicate otherwise."*

| Date | Policy |
| --- | --- |
| Pre-May 2025 | No explicit policy |
| May 2025 | AI banned entirely |
| July 2025 | Reversed: AI allowed for prep and applications, banned for take-homes and live interviews unless indicated |
| Current (2026) | *"Complete without Claude unless we indicate otherwise"* |

CRITICAL

**Critical:** Anthropic's evaluators are trained to detect AI-generated submissions — and they act on suspicion alone. Combined with the no-feedback policy, this means a candidate whose work reads like Claude output will simply never hear back. There is no appeal and no explanation.

**How evaluators detect AI-generated output:** structural uniformity (symmetrical sections, parallel sentences), generic customer empathy (*"developers who need reliable API access"*), breadth over depth, absence of personal judgment, excessive polish in a 3-hour document.

**How to ensure authentic work:**

1. Start with a handwritten outline (pen and paper, 15 minutes)
2. Write in your voice — short and punchy, or parenthetical asides, whatever is natural
3. Include a genuine point of view that is yours, not what you think they want to hear
4. Reference real experience (*"In my last role, I saw X pattern when we launched Y"*)
5. Leave breadcrumbs of your process (*"I considered X but chose Y because..."*)

### 5.6 Panel Defense

The panel has already read your document — expect 2–5 reviewers, typically including the HM and at least one engineering or design leader. You walk through your reasoning, not your content. Format: ~25 minutes presentation + ~15–20 minutes Q&A. **Research/Labs:** the panel is two people (HM + a senior engineering leader) for a 60-minute session. Plan for ~30 minutes of presenting, but expect questions to start after roughly 10 minutes — once the panel begins probing, the session rarely returns to your slides.

**Question types to expect:**

- **Assumption challenges:** *"You assumed X. What if that's wrong?"* — Tests intellectual flexibility
- **Scoping pressure:** *"This seems ambitious for 5–10 engineers. What would you cut first?"* — Tests prioritization
- **Strategic alternatives:** *"Why this and not \[alternative\]?"* — Tests conviction with reasoning
- **Safety:** *"What could go wrong if this is misused?"* — Not optional at Anthropic
- **Metrics:** *"How would you know if this is working? What would make you kill it?"* — Tests analytical rigor
- **Customer deep-dive:** *"Who exactly is the first customer? Walk me through their day"* — Tests specificity
- **Technical deep-dive (Research/Labs):** *"How would local deployment work here? What are the infrastructure trade-offs?"* — Panelists go beyond your written doc into adjacent implementation territory. Engineering trade-offs are an explicit evaluation criterion for Research/Labs.

### 5.7 How to Stand Out

- Include *"kill criteria"* for your own product: *"If after 3 months we see \[metric\] below \[threshold\], this should be sunset."* This is rare and signals intellectual honesty
- Name the tradeoff: *"I'm proposing X at the expense of Y because I believe Z"*
- Reference Anthropic's specific competitive position, RSP, and four-legged team model (PM + Designer + Engineer + AI Researcher)

INSIDER

**Insider:** Anthropic's culture values intellectual honesty. Admitting *"I'm less sure about this part of my analysis"* and explaining why is more impressive than defending a weak argument confidently. They are watching how you handle uncertainty.

### 5.8 Pass/Fail Signals

| Dimension | Strong Signal | Red Flag (Common Pitfall) |
| --- | --- | --- |
| **Authenticity** | Imperfect phrasing, personal voice, genuine opinions, evidence of process | Polished, symmetrical, reads like Claude wrote it — follow the 5-step authenticity protocol above |
| **Product thinking** | Proposes a product with clear user, business model, and success criteria | Proposing *"add batch processing to the API"* is a feature, not a product |
| **Scoping** | Fits within 5–10 engineers, 6 months with clear phasing | Either too ambitious or too trivial — the prompt constraints are also a scoping filter |
| **Safety awareness** | Safety implications woven into the product narrative | Safety mentioned as afterthought or not at all |
| **Defense quality** | Changes mind when presented with better arguments; explains tradeoffs | Defends every choice rigidly, or collapses — *"That's a fair challenge. If X is wrong, I'd pivot to Y because..."* |
| **Relevance** | Spends pages on new thinking | Describes Anthropic's current products back to them — one sentence of context is enough |

[Onsite Loop](#onsite-loop)

## 6\. Onsite Loop

### 6.1 At a Glance

| Item | What to know |
| --- | --- |
| Duration | ~7 hours total across 1–2 days (includes 15–30 minute breaks between rounds) |
| Format | 5–6 interviews: Culture (45 min), Leadership & Influence (45 min), AI Product & Execution (45 min), Technical Problem Solving (55 min), Customer Scenarios (55 min), plus HM conversation |
| Primary filter? | **Yes — multiple independent evaluations, any one can reject** |
| Key focus | Values alignment, cross-functional leadership, technical thinking, live product fluency, customer discovery |
| Scheduling | Typically scheduled across 1–2 days via video call |

### 6.2 Interview Day Structure

The onsite consists of 5–6 rounds across 1–2 days. The typical set of interviews:

- Culture Interview (45 min)
- Leadership & Influence (45 min)
- Technical Problem Solving (55 min)
- Customer Scenarios (55 min)
- AI Product & Execution (45 min)
- Hiring Manager Conversation (45 min)
- Working with Research Scientists (25 min) — research-adjacent roles only

Sequencing varies. Each round has a different interviewer — there is no panel. Virtual onsites may consolidate to a single day. Use breaks to reset, not to cram.

### 6.3 Culture Interview

Every candidate who interviews at Anthropic — PM, engineer, researcher, sales — goes through this round. The interviewer is not a PM; this is a universal interview conducted across all roles and functions. Same format, same duration, same bar. It is the single most common point of failure for experienced candidates, because the instincts that serve you well at other companies actively work against you here.

CRITICAL

**Critical:** Anthropic has explicitly flagged pre-rehearsed behavioral stories as the *"#1 failure mode"* for this round. The Culture Interview is a live conversation about how you reason through hard problems — not a behavioral assessment. Candidates who arrive with polished STAR narratives and try to map them onto whatever question comes up are rejected at a higher rate than candidates who simply think out loud and engage honestly.

INSIDER

**Insider:** The Culture Interview is the most misunderstood round. One candidate told us: *"I prepared like it was a behavioral interview. That was exactly wrong. They want to watch you think, not watch you perform thinking."*

**The four things interviewers are evaluating:**

| Dimension | What They're Looking For |
| --- | --- |
| **Complexity tolerance** | Can you sit with ambiguity and resist the urge to oversimplify? |
| **Intellectual honesty** | Will you name what you don't know rather than paper over gaps? |
| **Second-order reasoning** | Do you trace consequences past the first-order impact? |
| **Authenticity** | Does your reasoning sound like yours, or like someone performing preparation? |

**Pre-interview preparation materials:** Anthropic sends reading materials before this round — typically [Core Views on AI Safety](https://www.anthropic.com/news/core-views-on-ai-safety), the [RSP](https://www.anthropic.com/news/responsible-scaling-policy-v3), and sometimes recent research papers. Read everything they send. Then go further: use Claude to stress-test your understanding. Ask it to argue against your positions. Identify where your reasoning breaks down — those edges are exactly where the interviewer will probe.

**How to Prepare**

**1\. Build your knowledge base (table stakes):** Read [*"Machines of Loving Grace"*](https://www.darioamodei.com/essay/machines-of-loving-grace), Core Views on AI Safety, RSP v3.0, the [Constitutional AI paper](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback), and the [Claude System Card](https://www.anthropic.com/research/claude-4-system-card). Memorize all 7 values — they are defined and explained in Section 2 of this guide.

**2\. Practice reasoning out loud:** The quality of your reasoning matters more than your conclusions. Practice thinking through AI safety trade-offs aloud — not to polish your answers, but to find where your thinking breaks down before the interview does.

| Bad Reasoning | Good Reasoning |
| --- | --- |
| *"AI safety is critical. At my last company, I implemented safety guardrails, reducing harmful outputs by 40%."* | *"One tension I keep returning to is the deployment paradox — you need real-world usage to make models safer, but deployment itself creates risk. Anthropic's RSP tries to manage this with ASL levels, but the v3.0 changes suggest even they found the original framework too rigid for competitive reality. That tension doesn't resolve cleanly — and I think sitting with that discomfort honestly is more useful than pretending either extreme is right."* |

**3\. Know what gets well-prepared candidates eliminated:** Even candidates who've done the reading show up with habits that block genuine reasoning from coming through.

| Anti-Pattern | What It Looks Like | Do Instead |
| --- | --- | --- |
| **Shoehorning** | STAR story forced into a safety question | Engage with the actual question directly |
| **Skill-selling** | Listing accomplishments when asked how you think | Share your reasoning process, not your resume |
| **Parroting** | *"I really admire the RSP. Constitutional AI is a breakthrough."* | *"The portfolio approach is rare. Where I have questions is around the RSP v3.0 changes..."* |
| **Over-polishing** | Perfect structure, smooth transitions, no hesitation | Let yourself think out loud. *"Wait — I started by framing this as a binary, but it's actually more of a spectrum"* |

**What Anthropic Tells Candidates (and What They Actually Mean)**

| Anthropic's Instructions (Verbatim) | What This Means for Your Prep |
| --- | --- |
| *"Think out loud and share your authentic perspective"* | The interviewer is scoring how you arrive at positions, not the positions themselves. Showing a dead end you abandoned is more valuable than a clean answer |
| *"We aren't looking for any buzzwords"* | Safety jargon deployed without understanding is worse than saying nothing. If you can't explain Constitutional AI without the phrase *"Constitutional AI,"* you don't understand it yet |
| *"Avoid trying to sell your skills"* | Every minute you spend on accomplishments is a minute not spent on reasoning. The interviewer already assumes you're competent — that's why you got this far |
| *"We expect each question to take around 3–5 minutes"* | At that pace, expect 9–15 questions. This is a rapid-fire conversation, not a series of mini-presentations. Practice giving complete answers in under 4 minutes |
| *"If your interviewer interrupts you... don't worry! This is normal"* | Interruptions signal engagement, not dissatisfaction. The interviewer is steering you toward what they actually want to evaluate — follow their lead |
| *"Feel free to ask for alternative questions"* | They have backup questions ready. If a question isn't clicking, ask for a different angle — this shows self-awareness, not weakness |

**Common Questions**

- "What are your thoughts on AI safety and the risks of advanced AI systems?"
- "Walk me through a project you're most proud of." (This is NOT a competence question — what you choose to be proud of reveals what you optimize for)
- "Would you be willing to lose the value of your stock if Anthropic decides not to release models because it can't guarantee they're safe?"
- "What's a belief about AI development that most people in the industry would disagree with?"
- "How do you reconcile caring about accessibility with Anthropic's best models being expensive?"
- "How do you think about Anthropic's trade-off between revenue and safety?"
- "If Anthropic were holding back world-changing technology due to safety concerns, how would you personally feel about that?"
- "Why does AI safety feel more urgent to you now?"
- "Is there anything Dario has said publicly that especially resonates with you and makes Anthropic feel like the right place to work?"

The interviewer may work through an explicit checklist and move quickly between questions — this is by design, not an indication you're running out of time. "Why Anthropic" in particular often goes 3+ follow-up levels deep: expect pushback like *"OpenAI also does that"* or *"OpenAI is doing free models for democratizing access — so how is Anthropic different for you?"* Have a position that survives three rounds of "but OpenAI does that too." Interviewers have been observed looping back to your opening answers later in the interview to probe apparent tensions.

INSIDER

**Insider:** Disagreement stories get the deepest drill-down. When you share an example of disagreeing with someone (especially a senior leader) and changing your mind, expect the interviewer to spend 4–6 follow-ups testing what's underneath the story: *"Was this disagree-and-commit, or did you genuinely change your mind?"* / *"Looking back now, do you think one path was clearly right or wrong, or is it still unclear?"* / *"Did that disagreement carry emotional weight, or was it more of a routine workplace decision?"* / *"If this had not been your founder/CEO, do you think you would have landed on a different decision?"* / *"Is there someone you disagree with but still really respect?"* The probes are checking calibrated uncertainty (can you still hold the view as unsettled?), separating disagreement from respect, and stress-testing whether your update was authority-driven or evidence-driven. Pick a story where you can answer all five honestly without contradicting yourself.

NOTE

**Note:** You may have a shadow interviewer on the call — a second person who joins with video off and says little. This is for calibration purposes (Anthropic needs bench interviewers across all functions) and is not a signal about your performance. The interviewer may also be an engineer rather than a PM — this round is universal across disciplines.

WARNING

**Warning:** Anthropic declined a $200M Pentagon contract on principle. When asked the stock question, they expect you to mean it — not to perform conviction. A strong answer acknowledges the genuine difficulty: *"That's hard to answer honestly before it's real. But the reason I'm drawn to Anthropic over \[competitor\] is specifically because the mission is structural — PBC status, co-founder wealth pledge, the Pentagon decision."*

**How to Stand Out**

1. Have a genuine disagreement with Anthropic — RSP v3.0, open-sourcing safety research, or Constitutional AI limitations are fair territory
2. Reference *"limiting factors"* thinking from Dario's essay — demonstrate what AI can't accelerate alongside what it can
3. Demonstrate **"Hold light and shade"** in real time — present optimistic AND pessimistic scenarios before stating your position
4. Admit what you don't know specifically — not *"there's so much I don't know"* but *"I don't have a good model for how the transition period works between AI doing 80% vs. 100% of a PM's job"*
5. Ask a question that reveals genuine curiosity — *"How does the team navigate the RSP v3.0 tension internally?"*

### 6.4 Leadership & Influence

**Format:** Heavily scenario-based — roughly 80% simulated situations, 20% probes into real experience. Not pure STAR. Three question buckets: (1) Conviction vs. consensus — when do you push your view, when do you fold? (2) Failure analysis — what you learned, what you would change. (3) Vision-setting under uncertainty.

For Research/Labs candidates, this round diverges substantially from the three-bucket structure above. Expect an exploratory conversation that opens with your AI domain depth — contrarian views you hold about the technology, how those beliefs shape your product principles, and what excites you about emerging capability areas — then shifts to capability-development product scenarios (productizing nascent features, ship/no-ship calls on mixed signals, deciding when to keep investing) and closes with traditional leadership probes on major pivots and stakeholder alignment.

Standard L&I prep built around conviction/failure/vision scenarios will leave gaps. If targeting a Labs role, prepare for a judgment-focused conversation about AI capability development — not a structured team-dynamics session.

**Common Questions**

- "Tell me about a time you had to convince a cross-functional team to change direction."
- "How would you set a 6-month product vision when the technology changes every quarter?"
- "Walk me through a product failure you owned."
- "Imagine you're the PM for a new Claude feature. Research says it's safe but users are nervous. Engineering wants to ship. Design has concerns. How do you navigate?"
- "You need to pitch a new Claude capability to a skeptical enterprise customer. How do you position it?" *(Expect follow-ups: now pitch the same capability to an excited but non-technical user — then to an AI safety researcher with concerns. Same capability, three registers.)*
- "It's Monday standup. Your team just had a rough week. How do you open the meeting?"
- "The CEO asks you directly: 'Are we falling behind?' What do you say?"
- "Walk us through a user story that would make someone genuinely excited about a new Claude capability."
- "Your team has five different ideas about how to solve the same problem. How do you get to a decision?"

**Research / Labs Role Questions**

*AI domain depth:*

- "What's a view you hold about AI capabilities — from working with the technology — that isn't widely shared?"
- "How does that view shape your product principles and prioritization?"
- "Walk me through a product decision you made because of that view."
- "What's an emerging capability area you're excited about right now, and why should customers care?"
- "How would you measure the value of an emerging capability area for specific use cases?"

*Capability-development product scenarios:*

- "Imagine Labs is considering productizing a nascent capability. What's your approach — and what do you need to learn first?"
- "Research comes back and says: we're state-of-the-art on one dimension but below market on another. Do you ship?"
- "You launch and early feedback is mixed. Engineering wants to keep investing. How do you decide what's next?"
- "How do you decide when to keep iterating on an experience vs. pivot the approach?"

*Leadership alignment:*

- "Tell me about a large product decision where you had to execute a significant pivot. What was the situation and what did you do?"
- "How did you bring internal teams and customers along on that pivot?"
- "Anything else about how you lead as a product leader, or your product principles?"

INSIDER

**Insider:** If coming from FAANG, resist polished STAR stories. Anthropic's L&I round penalizes rehearsed answers. Prepare 6–8 stories but practice telling them conversationally, with honest reflection on what was hard and what you'd change.

**How to Approach: Lead with the Dilemma, Not the Outcome**

1. The tension — what made it hard, competing values
2. Your reasoning — why you chose the path you chose
3. How you brought people along — influence, not convincing
4. What you learned or would change — intellectual honesty

#### Pass/Fail Signals

| Dimension | Strong Signal | Red Flag |
| --- | --- | --- |
| **Conviction** | Takes a clear position and defends it with reasoning, then shows willingness to update | Either agrees with everything or refuses to budge |
| **Failure ownership** | Describes what they learned and what they'd change — not just what went wrong | Blames external factors or presents only successes |
| **Influence approach** | Shows how they brought people along through reasoning, not authority | *"I convinced them"* without explaining how |
| **Authenticity** | Pauses to think, revises mid-answer, acknowledges uncertainty | Delivers polished, rehearsed narratives with perfect transitions |

### 6.5 AI Product & Execution

NOTE

**Note:** Format varies by role. For most candidates, this round is the live defense of the Case Presentation take-home — the interviewer has already read your deliverable and will probe your reasoning, not re-hear your presentation. For Research/Labs candidates, this slot may be replaced by a **Product Judgment** interview: a scenario-based exercise where progressively revealing data points lead to a continue/kill decision, followed by a reflective discussion on a past judgment call that didn't hold up. Confirm which format applies before your onsite.

#### Product Judgment format (Research/Labs variant)

The scenario unfolds across roughly 10–12 turns anchored on a single hypothetical Anthropic product (e.g., a beta organizational-memory feature shipped six weeks earlier). The interviewer reveals data points sequentially and forces a call at each turn. A typical sequence:

1. Clarify the scenario.
2. Interpret early retention/engagement metrics.
3. Re-interpret given a benchmark comparison.
4. React to an unexpected use-case discovery (e.g., a different cohort using the product for an unintended purpose).
5. Decide whether to follow the emergent use case or push the original thesis.
6. Handle an external risk (e.g., an upcoming model snapshot that improves one dimension and degrades another).
7. Propose your first product response.
8. Call a week-N decision when retention still hasn't moved.
9. Decide what to do after a few iterations have failed.
10. Navigate an engineering disagreement on your call.
11. Behavioral closer: a past product or investment call you got wrong.

INSIDER

**Insider:** What's actually being scored is how you re-anchor when new data contradicts your prior call — do you update cleanly, or defend the previous turn? Keep the original thesis honest as the data changes, and name the safety/UX tradeoffs proactively rather than waiting to be probed.

**Format:** Take-home defense. The interviewer has already read your deliverable. Probes beyond the written submission into: why you made specific choices, alternatives you rejected, how you'd iterate, how your proposal connects to Anthropic's strategy, and whether you understand AI-specific product constraints.

**Products to know deeply:**

| Product | Key Detail |
| --- | --- |
| **Claude API** | Token-based pricing (Haiku $1/$5, Sonnet $3/$15, Opus $5/$25 per M tokens). Prompt caching, batch processing, extended thinking as cost levers |
| **claude.ai** | 18.9M professional users. Personality: *"curiosity, honesty, open-mindedness, self-awareness"* |
| **Claude Code** | Runs in the terminal with full file system access — operates autonomously on entire codebases, not line-by-line suggestions. 4% of public GitHub commits. $2.5B+ ARR |
| **MCP** | Open-source protocol for connecting AI to external tools. Fastest-growing standard in tech, but criticism: 40–50% of context windows consumed before agents work |

**Common Questions (Take-Home Defense)**

- "Walk me through your reasoning for choosing this product direction over alternatives."
- "You scoped this for 5–10 engineers. What would you cut if you only had 3?"
- "How would you measure success for this? What would make you kill it after 3 months?"
- "What's the safety story here? What could go wrong if this is misused?"
- "How does this connect to Anthropic's broader strategy — not just the API team?"
- "Who is the first customer? Walk me through their day before and after this product exists."

INSIDER

**Insider:** The gap between *"I've used Claude"* and *"I built a workflow with the API"* is the gap between rejection and onsite invitation. Cat Wu: *"Eating our dogfood grounds our model in solving practical problems that matter."*

#### How to Stand Out

- **Know the pricing model cold.** If Hamish asks *"How would you price this?"* and you don't know the token pricing tiers, you lose credibility immediately
- **Have opinions about MCP.** The Model Context Protocol is Anthropic's biggest platform bet. It's also getting criticism for context window overhead. Having a nuanced view signals product depth
- **Connect to the competitive landscape.** Reference what OpenAI, Google, and Cohere are doing (or not doing) in the space your product addresses. Show you understand Anthropic's positioning

INSIDER

**Insider:** On-site questions are tailored to your target team. One candidate reported being asked: *"The team has built a native audio Claude prototype — where do you start, what use cases do you explore, and what do you want to know from researchers before making a plan?"* Expect hypothetical product scenarios specific to the role you're interviewing for, not generic PM exercises.

### 6.6 Technical Problem Solving

**Format:** Two-part hybrid unique to Anthropic. No other major tech company runs this format for PMs.

**Part 1: Production Issue Diagnosis (~25 min).** You receive a scenario: a product launched, users came off a waitlist, something is going wrong. Your job:

1. Clarify scope and impact — who, how many, severity
2. Segment users into cohorts, look for patterns
3. Hypothesize using MECE — system issues, product issues, external issues, data issues
4. Propose mitigation with time horizons: **Immediate** (next hour), **Short-term** (2–4 weeks), **Long-term** (systemic prevention)

PRO TIP

**Success:** Explicitly name stakeholders in your mitigation plan: customer communication, Trust & Safety team, on-call engineering, leadership. PMs who think only about the technical fix miss the organizational dimension.

**Part 2: System Design (~25 min).** *"Now design a system that would prevent this class of problem."* The best candidates treat both halves as one narrative — the system design directly addresses the failure class diagnosed.

Key requirement: safety as a first-class architectural concern. Address the tradeoff: more safety checks = higher latency. Where do you draw the line?

WARNING

**Warning:** Do not try to impress with deep ML knowledge. This tests PM-level technical thinking. *"The system needs to handle 100K concurrent requests with sub-200ms latency while filtering harmful outputs"* will help. *"The inference pipeline uses transformer attention mechanisms with KV-cache optimization"* will not.

**AI-Specific Failure Modes to Study**

| Failure Mode | What It Is | System Design Implication |
| --- | --- | --- |
| **Hallucination** | Model generates confident but incorrect information | Factuality checks, citation requirements, user-facing confidence signals |
| **Prompt injection** | Malicious inputs override system instructions | Input sanitization, system prompt isolation, output filtering |
| **Model drift** | Performance changes between model versions | Regression testing, eval suites, canary deployments |
| **Safety filter false positives** | Legitimate requests blocked by overly aggressive filters | Tiered filtering, user appeal mechanisms, monitoring dashboards |
| **Context window overflow** | Too much context degrades output quality | Retrieval-augmented generation, summarization pipelines, context management |

**Must-do preparation:**

- Pick and master ONE whiteboard tool ([Excalidraw](https://excalidraw.com/) or [FigJam](https://www.figma.com/figjam/))
- Practice the production issue diagnosis framework with a timer — aim for 15 minutes diagnosis, 10 minutes mitigation plan
- Study the failure modes table above — at least one will appear in your scenario
- Test your screen-sharing setup before interview day — browser permission issues are common and can cost valuable interview time. Do a dry run with whichever video tool your recruiter specifies

NOTE

**Note:** ML Product Manager candidates may receive AI evaluation questions during on-site rounds, such as *"How would you detect and mitigate hallucinations in a generative AI product used by end-users?"* If you're interviewing for an ML PM role, prepare for technical AI evaluation scenarios alongside standard system design.

### 6.7 Customer Scenarios

INSIDER

**Insider:** This round has no equivalent at any other major tech company. No public resource covers it with the preparation detail you need. This section is based on documented candidate experience for specific product areas — format may vary by team.

This round mirrors the actual Anthropic PM job — especially on API, Claude Code, and enterprise-adjacent teams, where the day-to-day is running discovery → demo → iterate → close loops with design partners. What's being filtered is whether you can do that job solo, without a researcher or engineer standing next to you to demo the product. Prep it as work-sample prep, not as an interview round.

**Format:** Live roleplay. The interviewer takes on a customer role. You play the PM or solutions consultant. Candidates in some product areas have been required to demonstrate the product live during the interview — driving Claude in real time — so prepare for this regardless of your target team.

**What it tests:**

1. **Customer discovery** — Can you uncover real needs vs. stated wants?
2. **Product expertise** — Can you drive Claude competently and live?
3. **Technical communication** — Can you explain AI capabilities to a non-technical audience?
4. **Adaptability** — When Claude produces unexpected output (it will), can you recover?

**Live Product Fluency (Non-Negotiable)**

Drill the prompting fundamentals until they're second nature: clear and direct instructions, assigning roles, separating data from instructions, formatting output, chain-of-thought, using examples, and avoiding hallucinations. Anthropic publishes prompt-engineering guidance in their developer docs — work through it hands-on, writing and running real prompts rather than just reading.

**Master live prompting:** single-turn vs. multi-turn prompts, system prompts to set task context, and the parameters that shape output (model, max tokens, temperature). You should be able to write, run, and refine a prompt without thinking about the mechanics.

**Build a demo kit:** 3–5 prepared use cases (classification, extraction, summarization, analysis, generation), each with sample data, so you can switch between them based on what the customer needs.

**Recommended Approach: Three Phases**

We recommend structuring your 55 minutes in three phases to demonstrate the full range of skills being evaluated:

**Phase 1: Customer Discovery (Minutes 0–15).** Open with questions, not demos.

- *"Before I show you anything, I'd love to understand your current workflow."*
- *"What's the biggest bottleneck? Where do you spend the most time?"*
- *"Who would be using this tool? What's their technical comfort level?"*
- By minute 10–15, anchor on one concrete, demonstrable use case.

NOTE

**Note:** In some loops (confirmed for Labs), the discovery call is followed by a dedicated ~15-minute heads-down period where you build and refine your demo before a separate demo call. If you get this format, treat the 15 minutes as a sprint: choose your use case, write and test your prompts, prepare your framing. This is still a time crunch — arrive with a clear idea of which demo use case fits what you just learned in discovery, so you're not making the choice under pressure.

**Phase 2: Live Demonstration (Minutes 15–35).** Write prompts in real time — not pre-written.

- Start with a system prompt establishing task context
- Use a single-turn or multi-turn prompt depending on complexity
- Evaluate the output together with the *"customer"* — explicitly assess quality
- Iterate: refine, re-run, compare

**Phase 3: Challenges and Closing (Minutes 35–55).**

- Address accuracy: *"We'd set up an evaluation framework — run Claude on a labeled sample, measure precision and recall"*
- Address cost: *"For your volume, using the Batch API with prompt caching gives a 50% cost reduction"*
- Close with next steps: *"Based on what we explored, I'd recommend a pilot starting with \[scope\], measuring \[metric\]"*

**When Claude produces bad output (it will):**

DO: Acknowledge matter-of-factly — *"Interesting — Claude went in a different direction than expected."* Diagnose — *"This is likely because my prompt was too vague about X."* Fix — adjust and re-run. Frame as workflow — *"This IS the prompt engineering process. The first prompt is rarely perfect."*

DO NOT: Apologize profusely. Blame the tool. Pretend it didn't happen.

PRO TIP

**Success:** Treat the roleplay as real. The candidates who stand out forget they're in an interview and engage as if this is an actual customer meeting. Show genuine curiosity about the *"customer's"* problem.

**Estimated prep time:** 10–15 hours of hands-on practice driving Claude live. This is non-optional.

#### Pass/Fail Signals

| Dimension | Strong Signal | Red Flag |
| --- | --- | --- |
| **Customer discovery** | Asks open-ended questions before showing anything; uncovers the real problem behind the stated problem | Jumps to a demo immediately; assumes they know what the customer needs |
| **Live product fluency** | Writes and iterates prompts in real time, adjusts parameters naturally, recovers smoothly from bad output | Fumbles basic prompting; clearly hasn't practiced driving Claude live |
| **Handling bad output** | Diagnoses why the output was wrong, adjusts the prompt, frames iteration as normal workflow | Apologizes, blames Claude, or freezes |
| **Technical communication** | Explains AI capabilities in terms the customer understands without jargon | Either over-simplifies (*"AI just does it"*) or over-explains (*"The transformer architecture..."*) |
| **Closing** | Proposes a concrete next step with scope and success metric | Ends without a recommendation or trails off |

### 6.8 Working with Research

Not all candidates receive this round — it appears in loops for research-adjacent PM roles. Unlike other onsite rounds, the interviewer is a researcher rather than a PM.

INSIDER

**Insider:** Some onsite loops include a dedicated cross-functional round with a member of the research team. This evaluates how you collaborate with researchers: translating research capabilities into product direction, knowing when to push back on feasibility timelines, and understanding the research-to-product pipeline. If your recruiter confirms this round is in your loop, prepare examples of working at the boundary between research and product.

NOTE

**Note:** This round moves fast — expect a checklist-style interview with minimal follow-ups between questions. The researcher will proceed whether or not your answer fully lands. When hypothetical questions are underspecified (e.g., "build a roadmap for X"), ask explicitly whether they want an abstract framework or a domain-specific answer — don't assume.

**Confirmed questions (30 min):**

- "Tell me about past experience working with research teams on research-adjacent projects."
- "Tell me about a time you had to influence a researcher to change direction or take a decision."
- "How have you handled situations where technical feasibility was unclear?"
- "Suppose Anthropic was building a novel model capability. How would you build a roadmap for that? How would you think about what's feasible vs. not?"
- "How has product development changed pre-LLMs vs. post-LLMs?"
- "Give me one example of working with a research team that worked really well — and one that didn't."
- "What was your approach when a research-heavy project didn't go as planned? How did you iterate?"
- "Tell me about a case where it wasn't the user/product side that went badly — the researchers couldn't meet a goal that was desired. What did you do?"
- "If a requirement is something concrete like 'respond in under 50 milliseconds,' how would you figure out whether it's a goal worth trying to reach?"
- "If the researchers have different priorities — say, they're more interested in theory — how would you influence and work together?"
- "Working with PMs, where do you think PMs add the most value in the research process?"
- "Is there something you wish PMs could understand better about how research works or how to work with researchers?"

### 6.9 What Varies by Product Area

The Onsite rounds are consistent in format, but the content emphasis shifts by team:

| Round | Platform/API | Claude Code | Consumer | Research / Labs | Safeguards |
| --- | --- | --- | --- | --- | --- |
| **Culture Interview** | Universal — identical for all product areas | Universal | Universal | Universal | Universal |
| **L&I** | Cross-functional influence with engineering teams | Developer ecosystem influence | Consumer growth leadership | Research-to-product influence | Policy-to-product influence |
| **AI P&E** | API product strategy, developer adoption, pricing | SDK adoption, agent workflows | Growth loops, habit formation | Capability productization, prediction | Red-teaming, safety tooling |
| **Tech Problem Solving** | API architecture, rate limiting, developer experience | Terminal workflows, file system access | Product analytics, personalization | Evaluation tooling, benchmarking | Moderation systems, content filtering |
| **Customer Scenarios** | Enterprise developer scenario | Developer workflow automation | Consumer use case exploration | Research capability demo | Policy or safety scenario |

[Team Matching & Offer](#team-matching-offer)

## 7\. Team Matching & Offer

After passing the onsite, what happens next depends on how you interviewed. Specific-team candidates (e.g. Labs and Research openings) wait on the hire/no-hire decision for their role — typically faster and more like a standard PM loop. Talent-pool candidates (more common for generalist openings) enter Anthropic's team matching process.

### 7.1 How Team Matching Works

Anthropic uses two hiring patterns: talent-pool hiring and specific-team hiring. If you interviewed for a specific role on a specific team (more common for Labs and Research openings), team matching doesn't apply to you — you're waiting on the hire/no-hire decision for that role, not a headcount match, and the 2–4+ week silence patterns described below shouldn't be read the same way. The rest of this section describes the talent-pool path: after the onsite, your profile is circulated among 3–5 team leads, and internal headcount debates cause delays.

INSIDER

**Insider:** The 2–4+ week silence after the onsite is by design — not a sign of bad news. Anthropic circulates your profile among team leads and resolves internal headcount before making contact. Some candidates have not advanced at this stage because no team had headcount, even after passing every round. This is not a reflection of interview performance.

| Week | What to Do |
| --- | --- |
| 1–2 | Wait. This is normal |
| 3 | Send one professional follow-up email to your recruiter |
| 4+ | If you have a competing deadline, share it transparently. Otherwise, wait |
| 6+ | If no response to your follow-up, consider that team matching may not yield a result |

PRO TIP

**Success:** Express interest in multiple product areas during interviews to widen the matching pool. *"I'm most drawn to Platform, but I'd be excited about Claude Code or Research as well"* expands your options from 1 team to 3.

### 7.2 Managing Competing Offers

| Scenario | What to Do |
| --- | --- |
| You have a competing offer with a deadline | Share the deadline with your Anthropic recruiter. A real offer with a real deadline *"forces a decision"* |
| Another company is pushing during team matching | Tell Anthropic about the timeline pressure. Run parallel processes |
| Multiple AI companies simultaneously | Run parallel processes. Tell Anthropic you're finishing other processes — they expect it: *"We're happy to give you space to finish other interview processes"* |

INSIDER

**Insider:** Do not accept another offer during team matching silence without giving Anthropic a chance to respond first. Five weeks is completely normal. Nobody tells you this upfront.

### 7.3 Compensation & Leveling

For current compensation data, see [Levels.fyi](https://www.levels.fyi/companies/anthropic/salaries/product-manager). We don't publish salary or equity tables — these numbers change faster than a guide can stay accurate, and crowd-sourced data from Levels.fyi will be more reliable than anything we could provide.

#### Leveling

Anthropic uses internal levels (L3–L7) that map roughly to industry equivalents. Down-leveling happens — the committee evaluates scope of impact, not title history.

| Level | Title | Scope | Industry Equivalent |
| --- | --- | --- | --- |
| L3 | Associate PM | Single feature area | Google L4, Meta IC4 |
| L4 | Product Manager | Single product area, 5–10 engineers | Google L5, Meta IC5 |
| L5 | Senior PM | Multiple teams or business line, 15–30 engineers | Google L6, Meta IC6 |
| L6 | Principal PM | Cross-organizational scope, 30+ engineers | Google L7, Meta IC7 |
| L7 | Director of PM | Product org leadership | Google L8+, Meta Director |

INSIDER

**Insider:** Focus discussions on impact and systems built, not titles. Anthropic's committee has down-leveled candidates when experience doesn't match their scope expectations. If you led a team of 3 at a startup, that maps to L4 scope — even if your title was VP Product.

[Preparation Strategy](#preparation-strategy)

## 8\. Preparation Strategy

### 8.1 Preparation Priorities

Use the Must-Read and Must-Do checklists below as your foundation. Work through items in priority order — if you have less time, focus on higher-priority items first and add reps on the most important ones. The general sequence that works regardless of your timeline:

1. **Foundation** — Read all must-reads. Use Claude daily. Write a 1-page "Why Anthropic" memo in your own words
2. **Hands-on building** — Practice prompting Claude until you're fluent and fast. Build one project with the Claude API
3. **Case prep** — Do at least one timed take-home simulation (3 hours, <3 pages, no AI). Practice defending your reasoning out loud
4. **Culture prep** — Debate AI safety positions with Claude (argue both sides). Run a full mock culture interview conversationally — not with prepared answers
5. **Polish** — Review your "Why Anthropic" memo. Set up your whiteboard tool. Rest the day before

### 8.2 Must-Read Checklist

| Priority | Material | Time | Action |
| --- | --- | --- | --- |
| 1 | [*"Machines of Loving Grace"*](https://www.darioamodei.com/essay/machines-of-loving-grace) (Dario Amodei) | 45–60 min | Articulate one risk AND one benefit for each of five areas |
| 2 | [Core Views on AI Safety](https://www.anthropic.com/news/core-views-on-ai-safety) | 30–40 min | Explain the portfolio approach in 60 seconds without notes |
| 3 | [RSP v3.0](https://www.anthropic.com/news/responsible-scaling-policy-v3) | 40–50 min | Prepare a nuanced position on the v3.0 changes. Neither defend nor condemn |
| 4 | [Constitutional AI paper](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) | 45–60 min | Explain in plain language why explicit principles beat implicit ones |
| 5 | [Cat Wu's PM blog post](https://claude.com/blog/product-management-on-the-ai-exponential) | 15–20 min | Understand PM role definition, blurred boundaries, speed orientation |
| 6 | [Anthropic Company page](https://www.anthropic.com/company) (7 values) | 10–15 min | Memorize all 7 — especially the 7th |
| 7 | Dario on [Lex Fridman #452](https://www.youtube.com/watch?v=ugvHCXCOmm4) | 2–3 hrs | AGI timeline, strategic thinking. Models the reasoning style they want |

### 8.3 Product-Area Prep

Beyond the universal prep timeline, each product area has specific preparation requirements:

**Platform / API candidates:**

- Build a working application with the [Claude API](https://docs.anthropic.com/). Start with the Messages API, then explore tool use, prompt caching, and batch processing
- Understand the pricing model cold — token costs per model tier, cost optimization levers, how prompt caching affects billing
- Have a perspective on MCP: what it enables, where it falls short, how you'd improve it
- Study API design patterns: versioning, rate limiting, pagination, error handling. Platform hiring managers will expect you to speak naturally about these

**Claude Code candidates:**

- Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and use it daily for at least 2 weeks. Build a non-trivial project
- Know the competitive landscape in detail: GitHub Copilot dominates among paid AI coding assistants, Cursor has achieved rapid revenue growth with its IDE-first approach, and Claude Code differentiates by operating in the terminal with full file system access rather than inside an editor
- Understand the distinction between code completion (autocomplete your lines) and code delegation (tell it what to do, walk away, come back)
- Read [Boris Cherny](https://www.linkedin.com/in/bcherny/) 's interviews about Claude Code's development philosophy

**Consumer (claude.ai) candidates:**

- Use claude.ai daily across diverse tasks for at least 2 weeks. Keep a friction log
- Understand Claude's personality differentiation: *"curiosity, honesty, open-mindedness, self-awareness."* How does this translate to product decisions?
- Study consumer AI growth mechanics — habit formation, retention loops, the difference between *"tried it once"* and *"use it every day"*
- Have a perspective on Artifacts, Projects, and Cowork as product surface expansions

**Safeguards candidates:**

- Deeply understand RSP v3.0, including the controversy. You will be tested on whether you can reason about safety policy tradeoffs
- Know how Claude's Constitution works in practice — the priority ordering (safe > ethical > compliant > helpful) and when it creates product friction
- Study trust & safety systems at scale: content moderation, user appeals, policy enforcement
- Have examples of navigating policy-to-product translation from your own experience

### 8.4 Must-Do Hands-On Checklist

- Practice driving Claude live — write, run, and iterate prompts until you're fluent and fast. This is the core skill tested in the Customer Scenarios round
- Build something with the [Claude API](https://docs.anthropic.com/en/api/messages) — start with the Messages API, then add tool use or prompt caching. The goal is to have a real answer when asked "what have you built?"
- Use [claude.ai](https://claude.ai/) or the API daily for 2+ weeks; keep a running log of 5–10 observations — bugs, delights, limitations. These become your most credible answers
- Set up and practice with a whiteboard tool — [Excalidraw](https://excalidraw.com/) or [FigJam](https://www.figma.com/figjam/). Draw 2–3 system diagrams before interview day; don't learn the tool during the round
- For Claude Code PM: install and use [Claude Code](https://docs.anthropic.com/en/docs/claude-code) daily on a real project for at least 2 weeks. Know the competitive landscape — GitHub Copilot, Cursor — and how Claude Code's terminal-first approach differs
- For Consumer PM: use [claude.ai](https://claude.ai/) across diverse tasks daily; document friction points and growth opportunities with specific examples

### 8.5 Re-Interview Policy

Anthropic does not publicly document specific cooldown periods. Based on industry norms at frontier AI companies, expect to wait at least 6 months after a final-round rejection, and 3–6 months after earlier-stage rejections. These are industry estimates, not Anthropic-specific data — confirm with your recruiter before reapplying.

Use the cooldown productively: build visible AI work, publish writing on safety topics, contribute to open-source AI projects. When you reapply, reference specific growth since your last attempt — not just time elapsed.

[Additional Resources](#additional-resources)

## 9\. Additional Resources

| Resource | Why It's Relevant |
| --- | --- |
| [**Anthropic API Documentation**](https://docs.anthropic.com/) | Required reading for Platform/API candidates. Build something with it to demonstrate hands-on experience in the HM Screen |
| [**"Machines of Loving Grace"**](https://www.darioamodei.com/essay/machines-of-loving-grace) (Dario Amodei) | The single most referenced document in Culture Interviews. The *"limiting factors"* framework and five areas of impact are direct conversation starters |
| [**Core Views on AI Safety**](https://www.anthropic.com/news/core-views-on-ai-safety) (Anthropic) | Shared with candidates before the Culture Interview. The portfolio approach and *"we do not know"* admission are the foundation for safety reasoning |
| [**RSP v3.0**](https://www.anthropic.com/news/responsible-scaling-policy-v3) (Anthropic) | The most contentious topic in Culture Interviews. Understand ASL levels, the v3.0 changes, and the dual mitigation framework |
| [**Cat Wu: Product Management on the AI Exponential**](https://claude.com/blog/product-management-on-the-ai-exponential) | Defines the PM role at Anthropic: *"create clarity in ambiguity, push teams to think bigger, clear the path to shipping faster."* Required for understanding what Anthropic expects from PMs |
| [**Dario Amodei on Lex Fridman #452**](https://www.youtube.com/watch?v=ugvHCXCOmm4) | Models the reasoning style Anthropic screens for. AGI timelines, strategic thinking, intellectual honesty about uncertainty |
| [**ByteByteGo**](https://bytebytego.com/) (Alex Xu) | Best resource for AI system design prep. Covers distributed systems, ML infrastructure, and AI-native architectures at the level expected in the Technical Problem Solving round |
| [**Excalidraw**](https://excalidraw.com/) | Our recommended whiteboard tool for the Technical Problem Solving round. Clean, fast, no signup required |
| [**Levels.fyi**](https://www.levels.fyi/companies/anthropic/salaries/product-manager) | Most reliable public compensation data for Anthropic PM roles. Small sample but directionally accurate |

---
*Clipped from [insiderloops.com](https://www.insiderloops.com/guides/anthropic) on 2026-06-04T09:53:56-04:00*
