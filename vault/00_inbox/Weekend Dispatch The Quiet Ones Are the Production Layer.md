---
title: "Weekend Dispatch: The Quiet Ones Are the Production Layer"
source: "https://claudecodefornoncoders.substack.com/p/weekend-dispatch-the-quiet-ones-are"
author:
  - "[[Daniel Williams]]"
published: 2026-05-23
created: 2026-06-02
description: "Everyone’s reading this week’s AI stories wrong: AI didn’t replace the careful thinkers. It exposed how long the org has been ignoring them. /goal just shipped in Claude Code to close the gap."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
**👋 Welcome! I’m Daniel Williams.** I write Claude Code for Non-Coders for senior technical professionals who built their careers on technical judgment, stopped writing code years ago, and are now figuring out how AI and coding agents will change their work.

The goal is to keep you as the operator, not the AI’s assistant (“ [reverse-centaur](https://claudecodefornoncoders.substack.com/p/accenture-is-building-reverse-centaurs) ”), by helping you decide which tasks to automate and which require the judgment that made you valuable in the first place.

I advise clients on AI tools, strategy, and human resilience at [dewilliams.co](https://dewilliams.co/). This newsletter is where I document the patterns, commands, and operator habits that help you grow from babysitting prompts to building reliable systems.

**Join 33,000+ senior technical professionals** learning the operating discipline that keeps your judgment valuable.

## The careful professional in the meeting wasn’t failing at communication. The org was structurally rewarding confidence theater over judgment. AI is now making the cost legible.

Mats Alvesson coined the term "functional stupidity" in 2016, and it is finally getting the attention it deserved a decade ago. Orgs systematically tax reflexive thinking and reward fluent performance, because frictionless execution looks good in quarterly numbers. The colleague who delivered three confident sentences about alignment got the nod. The careful point, the one with the actual data, and the inconvenient caveat got “parked for later consideration,” which everyone in the room understood to mean never.

Sven Brodmerkel’s [piece this week](https://svenbrodmerkel.substack.com/p/why-competent-people-disappear-functional) extends the diagnosis to the very people most likely to be reading this newsletter. Senior technical professionals built careers on careful pattern recognition. Many learned to mask it to survive. The ones who couldn’t perform confidence theater on demand became the “difficult” ones, the ones meetings get scheduled without, the ones whose pattern recognition was too sharp for the room to absorb. I’ve watched this play out in client engagements more than once. The person with the careful read on the rollout gets sidelined for the person with the confident roadmap, and six months later, the rollout stalls in exactly the way the careful person predicted, after the budget has already been spent.

The CC4NC thesis names what the system has been hiding. Your judgment is the layer the org de-funded for thirty years, and the AI rollout is about to make the cost show up on the line item. When McKinsey reports that less than 20% of AI adopters see bottom-line impact, somebody has to figure out why. When the 18,000-process automation at the apparel group stops compounding, somebody has to redesign the operating model. The careful thinkers are the only people in the building who can do that work. The org that taxed your judgment will now need it back, and the question is whether you’re still in the room when they ask.

*“The social penalty for thinking carefully, in a functionally stupid organisation, is real and cumulative. And it operates below the level at which you can easily name it and fight it.”  
\- Sven Brodmerkel (PhD)*

---

## McKinsey just admitted in print that less than 20% of AI adopters see bottom-line impact, and the reason isn’t the models.

Andrei Savine’s [analysis](https://andreisavine.substack.com/p/last-mile-enterprise-ai-dies) pairs [McKinsey’s State of Organizations 2026](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/the-state-of-organizations) with [HBR’s “Last Mile” diagnosis](https://hbr.org/2026/03/the-last-mile-problem-slowing-ai-transformation). One story repeats across both. 88% of organizations deploy AI in some capacity. 86% of leaders say they aren’t ready to embed it in day-to-day operations. The productivity gains that show up locally (250 LLM apps in production at one global bank, 18,000 automated processes at an apparel group, 99% Copilot adoption at a payments network) get reabsorbed into low-value work because nobody redesigned the roles and budgets to harvest the freed time.

McKinsey put a number on it: for every $1 spent on AI technology, $5 should be spent on people. Current spend is the opposite. We funded models, integration, and dashboards. We did not fund the production layer: verification, agent orchestration, role redesign, and the governance that determines whether an AI output touches a customer or a ledger. Savine calls it System 2. Almost no enterprise has built it.

I keep running into a version of this in advisory discussions. The exec team announces an AI program. The engineering team builds the integrations. Six months later, the CFO asks why the line item hasn’t moved, and the answer is always the same: nobody owned the operating-model redesign. The reabsorption pattern in McKinsey’s data matters because CFOs who can’t see a production layer balance the spreadsheet by cutting headcount and calling it an AI transformation. Atlassian cut 10% of staff in March. WiseTech is cutting 29% of its 7,000-person workforce over 18 months. The first companies to cut aren’t the ones with the most AI value to capture. They’re the ones with the least serious operating-model design.

If your judgment is what System 2 looks like in practice, your value just doubled. The question is whether you’re positioned to be the one the CFO calls when the spreadsheet stops working, or whether you’re already on the layoff slate the spreadsheet generated instead.

*“Everywhere I look, companies are rolling out copilots and agents, building hundreds of pilots and process automations. Yet when you ask for firm‑level impact, you get silence, hand‑waving or a headcount plan. The “last mile” is where enterprise AI quietly dies.”  
\- Andrei Savine*

---

## The $700B consulting industry isn’t being disrupted by AI. Its positioning to capture the production-layer margin that enterprises never funded, and whether it can actually deliver the work it’s now charging for, are open questions.

Pradeep’s [analysis](https://cioinsights.substack.com/p/the-great-consulting-reinvention) of CB Insights’ professional services report reveals what the headline numbers are hiding. McKinsey has deployed 12,000 internal AI agents. Accenture merged five business units into a single “reinvention services” line. KPMG, EY, Deloitte, and PwC have all launched agentic platforms in the past year. AI agent solutions generated over $10B in private market revenue in 2024 and are on pace to more than double in 2025. The orchestration layer (Workbench at KPMG, Refinery at Accenture, EY.ai’s agentic platform) is the product the firms now sell, and the advisor tier is being subsidized to feed it. KPMG’s Global AI Head said it plainly: “We built Workbench as our global architecture to standardize how agents are built, deployed, and monitored.” That is the language of a platform company, not a service firm.

The caveat the announcements skip past is that management consulting has lived in the advisory-recommendation lane for fifty years. The deck got delivered, the partner moved on, and accountability for whether the recommendation actually worked was structurally somebody else’s problem. Owning the orchestration tier is the opposite business model. You stay through implementation, you’re on the hook when the agent breaks the audit, and you eat the margin when the productivity number doesn’t hit. Whether these firms can actually staff to deliver that work, or whether they’re charging platform prices for a service offering they’ve never proven they can ship, is the question every CIO should be asking in the next procurement cycle.

The second question is even sharper. If AI compresses delivery costs by 60-80%, where does the surplus land go? The optimistic read says competition forces firms to pass savings through to clients, and outcome-based pricing makes the lower cost legible on the invoice. The realistic read says firms sell their platforms as proprietary infrastructure, lock clients into multi-year arrangements that look like SaaS and feel like SOW retainers, and keep as much of the new margin as they can for as long as they can. The history of this industry suggests the realistic read wins, which means the orchestration platform pivot is partly a value-capture play wearing platform-economics clothing.

If you’re a senior technical professional inside one of these firms, the question is whether you’re being moved into the orchestration tier or the advisory tier. The traditional pyramid is inverting fast. Lovable hit $100M ARR with 45 people. Anysphere generates over $2M revenue per employee. When clients eventually run at that efficiency, the billable-hour justification collapses, and the firms that survive will be the ones who can actually deliver outcomes they charge for. Internal builders who can own a production layer are about to be the most valuable people in the industry. Everyone else is in the headcount review the spreadsheet is already writing.

![](https://substackcdn.com/image/fetch/$s_!Eu9B!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc3aeb54a-a8dc-4f86-a437-2cdf76d9b5aa_751x794.png)

---

## The credentials American universities have been selling for fifty years just got reevaluated in real time, and the institution can’t hedge between “formation” and “ticket” anymore.

Amarda Shehu’s [piece](https://amardashehu.substack.com/p/what-the-university-is-now-for) names what every higher-ed piece this year has been hedging. She’s a computer scientist running AI deployment at a 40,000-student public research university, most of whose students are first-generation. She names what the institution has been doing for two generations: telling the public a story about citizenship and formation while collecting tuition for a credential the labor market reads as a hiring filter. AI is making both stories impossible to hold at once.

The data she pulls together is hard to dismiss. Forrester’s 2026 Future of Work report finds 55% of employers regret AI-related layoffs and projects roughly half will be reversed. The Burning Glass Institute reports the value of a bachelor’s degree has dropped to a thirty-year low. Companies that fired junior analysts last year are quietly rehiring them offshore. Tuition keeps rising. The bachelor’s wage premium is approaching parity with non-graduates, because the entry-level cognitive work the degree was supposed to qualify you for has been absorbed by language models.

Shehu’s answer isn’t a list of safe disciplines. There is no list. The answer is formation: judgment, slow understanding, tolerance for ambiguity, relational capacity under uncertainty. The things that resist automation aren’t subjects. They emerge from sustained encounters with hard problems and the people working on them. The contrarian move isn’t a new AI-literacy curriculum or another interdisciplinary degree. It’s an honest audit of which existing programs actually deliver formation and which deliver only the ticket, and a refusal to keep charging the same tuition for both. The public research university (where a first-generation student can access formation without being born to wealth) has the most to lose if it doesn’t choose, in public, what it actually sells.

If you’re hiring senior people in the next five years, the formation pipeline that produces them is narrowing under you. The same question hits parents with high schoolers at the dinner table. This is the Loop 3 reabsorption question from last week’s dispatch at the institutional level: the careful thinkers orgs will need to build production layers that come from somewhere, and the places that take formation seriously aren’t the ones selling tickets. If the public university spends the next five years studying the question, the formation slot in American life closes, and the only people who get it are those who can pay private-college prices. That’s a much narrower industrial base for the AI economy than anyone in policy circles is acknowledging.

*Anyone who gives you a list is selling you something, and the institution that has been gesturing at one has been complicit in a pretense that is no longer sustainable. The truth is simpler and harder. If a job is a task that can be fully digitized, it is done. The tempo at which it is done is not in our hands.  
\-* Dr. Amarda Shehu

---

## Anthropic just shipped /goal in Claude Code, and it isn’t a chatbot feature. It’s the outcome-specification interface this newsletter has been pointing at since Domain 1.

`/goal` lets you tell Claude Code what “done” looks like, then walk away while it works across sessions until it either succeeds or escalates. I ran it this week, paired with the feature contract workflow I use on AutomationResilience.com. Wednesday evening, I specified the goal, handed Claude the contract that defined “done,” and went to make dinner for the kids with my wife. By the time we sat down to eat, Claude had shipped the update, and the test suite was green.

This is the operator move at the personal-practice level. Most Claude Code usage is still in task mode: prompt, watch, prompt again, watch again. /goal is outcome-mode: name the contract, let the agent figure out the steps, return when the work is verifiable. The discipline isn’t typing. It’s specifying outcomes precisely enough that an agent can’t drift away from them. That is the production layer in personal practice, the same layer that the McKinsey 5:1 ratio names as missing at the enterprise level. The reason most enterprises can’t see ROI on AI is the same reason most individuals can’t get more than a chat session out of Claude Code: they’re still operating in task-mode when the tool is built for outcome-mode.

If you’re using Claude Code, this is the skillset to build. Most users will treat /goal like a fancier prompt and keep getting fancier-prompt value out of it. The operators will treat it like a contract: a specification of what “done” means, written before they start, that the agent has to satisfy or escalate. The skill that gets harder to charge for over time is task execution. Anthropic just made the second one cheaper to practice, and the gap between people who do it deliberately and those who don’t is widening fast.

![](https://substackcdn.com/image/fetch/$s_!8g_S!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67a07bdd-9723-4e45-a80a-e488c5ee6e46_1512x166.png)

---

*Claude Code for Non-Coders publishes Tuesdays and Thursdays. Weekend Dispatch covers AI developments that I find interesting and typically share with friends and family.*

---

*Daniel Williams advises clients about AI tools, strategy, and human resilience at [dewilliams.co](https://dewilliams.co/).*

---
*Clipped from [substack.com](https://claudecodefornoncoders.substack.com/p/weekend-dispatch-the-quiet-ones-are) on 2026-06-02T11:08:46-04:00*
