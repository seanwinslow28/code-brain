---
title: "I spent the last week building you a Team OS in Claude Code"
source: "https://substack.com/inbox/post/196814801"
author:
  - "[[Aakash Gupta]]"
published: 2026-05-07
created: 2026-05-11
description: "This is the unlock most product teams need to get the most out of Claude Code"
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [claude-mastery, product-management]
ai-context: "Aakash Gupta's week-long build of a Claude Code Team OS — the harness-engineering pattern he argues product teams need to extract real value from Claude Code at the team rather than individual level."
---
OpenAI published a line in their [harness engineering post](https://openai.com/index/harness-engineering/) in February that I haven’t stopped thinking about:

> *“That Slack discussion that aligned the team on an architectural pattern? If it isn’t discoverable to the agent, it’s illegible in the same way it would be unknown to a new hire joining three months later.”*

![](https://substackcdn.com/image/fetch/$s_!gk_2!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2b32824-e89d-4b83-ba15-6c192cee16eb_1402x576.png)

OpenAI released a great post on Harness Engineering. The author is on the podcast in a few weeks.

They were talking about AI coding agents. But read it again. **It applies to your entire product team.**

That pricing decision your team made in February? If it’s buried in reply #31 of a Slack thread, it doesn’t exist. Not for the AI. And not for the PM who started last month. That customer call where the VP of Engineering said the integration was a dealbreaker? If the summary lives in one PM’s personal notes, it might as well not have happened. The churn query your analyst wrote last quarter? If the engineer paged at 2 AM can’t find it, she’s stuck until morning.

The knowledge exists. It’s just trapped: in someone’s head, in a personal setup, in a tool nobody else can search.

---

## The Solution: A Team OS

[Hannah Stulberg](https://hannahstulberg.substack.com/), a PM at DoorDash, showed the solution on my [podcast](https://www.news.aakashg.com/p/how-to-build-a-team-os-in-claude) a few weeks back.

![](https://www.youtube.com/watch?v=0UArKLQ6bXA)

She built a shared repo where every team function checks in their context and anyone on the team can query it in natural language. She demoed a query that found the answer using **3% of the context window.**

The part that stuck with me was what happened the following week, when a new engineer needed context about a customer decision from three months ago.

Instead of pinging Hannah in Slack and waiting, the engineer opened the repo, asked the question, and got the full reasoning in **15 seconds.**

Hannah wasn’t involved. She wasn’t even online.

She had made herself unnecessary for context questions. The team treated her as more valuable for it. Every PM book tells you to make yourself indispensable. Hannah's bet was the opposite. She freed herself from being the bottleneck so she could do the work that actually requires judgment.

I’ve spent months building personal AI setups. [My PM OS](https://www.news.aakashg.com/p/i-spent-100s-of-hours-building-a) has 41 skills and a context library and sub-agents. I’m proud of it. And I’ve slowly realized it solves the *first* problem. It makes *me* faster. The harder problem is making the *team* faster. When I’m asleep at 2 AM and an engineer needs the churn query, my personal OS can’t help them.

I’ve spent the past week studying four implementations of what I’m calling a Team OS. Hannah at DoorDash. [Dave Killeen](https://www.news.aakashg.com/p/this-cpo-uses-claude-code-to-run) at Pendo. [Gabor Meyer](https://www.news.aakashg.com/p/how-to-build-a-full-ai-dev-team-in) at Google. [Carl Vellotti](https://www.news.aakashg.com/p/how-to-turn-claude-code-into-an-operating) building solo. Four people, four companies, four different levels of complexity. They all converged on the same architecture.

**That convergence is what convinced me to write this.**

---

## Today’s Post

*I’ve partnered up with [Hannah Stulberg](https://open.substack.com/users/4630983-hannah-stulberg?utm_source=mentions) to make sure this followup to her podcast is the highest quality possible guide to building a Team OS in Claude Code out there.*

![](https://substackcdn.com/image/fetch/$s_!tkq_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a8303b7-1a1a-42cb-9ad7-0c309b8ee6c6_1200x800.png)

*She is the author of [In the Weeds](https://hannahstulberg.substack.com/) (including her viral [Claude Code for Everything](https://hannahstulberg.substack.com/s/claude-code-for-everything) series) and is running a [Maven workshop](https://maven.com/hannah-stulberg/how-to-build-your-teamos) on the topic this weekend.*

---

## Why We Built This

- New hires take [6 to 7 months](https://www.insightglobal.com/blog/onboarding-statistics/) to feel settled.
- [Only 12%](https://www.gallup.com/workplace/235121/why-onboarding-experience-key-retention.aspx) of employees say their company does onboarding well.
- [47% of companies](https://enboarder.com/blog/employee-engagement-onboarding-stats/) call institutional knowledge loss their top offboarding challenge.

Most of that time, most of that loss: context that already exists somewhere, trapped in someone’s head or buried in a tool nobody else can search.

A context question is rarely just the lookup time. It's the lookup, the Slack ping, the wait, the context-switch back. At 10 of those a day at 10 minutes of total productive time lost each, you're at over 8 hours a week. Most teams I've talked to are higher.

*And the pattern isn’t Claude Code specific. Codex, Cursor, GitHub Copilot. This architecture can be moved wherever you are, because it’s just Markdown files. The examples here just use Claude Code because that’s what is most popular with AI-native PMs right now.*

---

## The Deep Dive

🔒 *For paid subscribers, we’ve put together everything you need:*

1. How to Upgrade your Personal OS to a Team OS with 1 command
2. The Architecture That Works (The 3 Layers)
3. Three Ways Teams Actually Use It
4. How to Build One in 4 Weeks
5. The Real Problems You’ll Encounter
6. What the First Month Actually Looks Like

*Plus **6 downloadable resources**, including: a skill to convert your personal OS to a team OS,a starter repo, and an adoption playbook.*

---

*Everything in this deep-dive is also built-into this easy to fork GitHub repo:*

---

## 1\. How to Upgrade your Personal OS to a Team OS with 1 command

I built [a personal PM OS](https://www.news.aakashg.com/p/pm-os) earlier this year. Skills, context library, sub-agents. It’s the best personal productivity system I’ve ever used. You probably have one, too.

Here’s the problem. The moment a second person needs what’s inside it, you realize you’ve built a really good silo:

- Designer can’t see customer call summaries.
- Eng lead can’t query the competitive research.
- The PM who started last month can’t access the context.

The compounding intelligence compounds for a *single person*. A Team OS compounds **for the whole team**.

So we’ve shipped a simple command you can implement:

**Downloadable #1: Upgrade to Team OS Skill.** This takes any Personal Claude Code OS and sanitizes it and surfaces what’s ready for the team.

This will launch the upgrade to team OS skill:

```markup
/upgrade-to-team-os
```

Personal context (working preferences, voice, sub-agent reviewers, half-formed drafts) stays personal. Only what genuinely benefits the team earns its way into the shared repo. The starter kit’s upgrade flow scans your existing personal OS, classifies every file, and produces a sanitized fork - never modifying your originals.

*Now let’s walk through what you’ve built for yourself.*

---

## 2\. The Architecture That Works

After studying four implementations, here’s what we’ve found: every working Team OS has three layers. Strip away the differences in tools, folder names, and complexity, and this is the skeleton that holds.

![](https://substackcdn.com/image/fetch/$s_!nJes!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cb5a4b3-2532-447d-b384-b04c3daa491e_2160x2260.png)

### Layer 1: Shared Context

The repo everyone writes to. This is where 80% of the value lives. 5 components matter:

#### Component 1 - The root file is a routing table, not an encyclopedia

The root CLAUDE.md has three things: a doc index mapping every folder to its purpose, a team roster with Slack and GitHub handles, and a channel map.

![](https://substackcdn.com/image/fetch/$s_!rn5O!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7008ab58-9cb1-46dd-b91c-458f656a3b00_1560x1332.png)

The root Claude.MD file.

Under 500 tokens. Loaded every session. [OpenAI’s harness engineering](https://openai.com/index/harness-engineering/) describes the identical pattern: their AGENTS.md is roughly 100 lines and serves as a map, with the actual knowledge base living in structured docs/ underneath.

I learned this the hard way. My first PM OS draft had my company context, writing style, competitive intel, and personal preferences all crammed into the root CLAUDE.md. By the third query of a session I was hitting limits. Claude was loading 40K+ tokens of mostly irrelevant material on every turn before it even looked at the question. The fix was structural. Treat the root file as a routing table and let everything else live where it belongs.

#### Component 2 - Every folder gets a nested CLAUDE.md

These are navigation files.

![](https://substackcdn.com/image/fetch/$s_!kJnF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffff05ecf-87cf-440c-8f92-41319802bc2b_1136x958.png)

A nested CLAUDE.md file.

Two lines per document: what it is and when Claude should read it. Without these, Claude runs expensive explore agents across the entire repo, burning thousands of tokens just *looking* for information before it can start *thinking* about your question. With them, Hannah demoed a query that resolved using about 3% of the context window. That gap is the difference between a useful system and one that hits usage limits in 30 minutes.

#### Component 3 - Summaries first, raw data on demand

A one-hour customer call is 10,000+ tokens. A structured summary is 500.

![](https://substackcdn.com/image/fetch/$s_!p5QP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1aadce9a-248d-4495-9cb1-55cdd5f4a7b1_1250x1172.png)

Example customer account summary.

The repo always points Claude to summaries. Raw transcripts live one folder deeper, loaded only when the summary can’t answer the question. Every level of nesting saves context. This principle applies across every content type: meeting summaries over full transcripts, metric definitions over full table schemas, decision rationale over full meeting notes.

#### Component 4 - The analytics structure that pays for the whole system

This is the part of Hannah's setup that landed first when I rebuilt my own folders. Under analytics/, she organizes by product area, then splits the content into three files: metrics (definitions only, low token cost), queries (the actual SQL, medium cost), and schemas (table structures, loaded only on demand). When someone asks *“what are our billing metrics?”* Claude reads one file and stops. When someone needs the full picture, it reads all three. Right-sized context for every question.

![](https://substackcdn.com/image/fetch/$s_!q4Xl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe83de740-2230-4d45-8207-d0b9a0d3a92f_812x922.png)

Every level of nesting is a context-saving decision.

#### Component 5 - Two YAML registries do routing work

`feature-index.yaml` maps every feature to its PRD, RFC, plan, schema, dashboard, experiments, and tickets.

![](https://substackcdn.com/image/fetch/$s_!aG1Z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98c7fd1f-26ab-4430-b4a2-6203407f885d_1140x1060.png)

feature-index.yaml

It’s one place to look up anything. `analytics/data-catalog.yaml` registers every warehouse table with grain, partition key, refresh cadence, PII flag, and a `used_by` list pointing to the dashboards and queries that depend on it.

![](https://substackcdn.com/image/fetch/$s_!8iFL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F713b7fa6-540f-4cc3-aee1-04a521c7d325_1722x1522.png)

data-catalog.yaml

The launch gate enforces both. The result: the analytics folder operates as a dependency graph the team compiles every release**.** A new analyst onboards in one read of `data-catalog.yaml`. Schema drift becomes a diff that engineering catches in review. The cost of the Nth analytics question drops because the (N-1)th already wrote down where the data lives.

### Layer 2: Shared Queries

Layer 1 is what goes into the system. Layer 2 is how people get value out. Three practitioners showed me three approaches on the podcast. Each fits a different team. More on the comparison in Section 3.

The range goes from everyone on the team querying directly (Hannah’s approach, most powerful, requires everyone to use a coding agent) to one power user running queries and sharing outputs (Dave’s approach, lowest barrier) to specialized agents handling different query types automatically (Gabor’s approach, most scalable). The right one for your team depends on how many people on your team already use AI tools.

### Layer 3: Shared Discipline

I almost called this “Shared Memory.” But that would be misleading.

Claude doesn’t learn across sessions. It doesn’t remember your team’s preferences. It doesn’t accumulate wisdom. **Every session starts from zero.** The files persist. And files only get better when humans update them.

The third layer is team discipline, not AI memory. Two kinds:

1. **Explicit discipline:** humans check in new context after decisions, calls, and launches. Hannah enforces this with a rule I think every team should steal: *“The feature is not rolled out until the repository is updated.”* Metrics definitions, SQL queries, table schemas, dashboards. All checked in before the feature ships. That’s the enforcement mechanism that prevents the repo from going stale.
2. **Encoded learnings:** the [CLAUDE.md](http://claude.md/) files themselves get refined over time as the team discovers what works. [Pawel Huryn described](https://www.theproductcompass.com/) adding self-improvement blocks to his [CLAUDE.md](http://claude.md/): by week three, Claude was applying 24 rules the system had accumulated. Dave Killeen goes further with session start hooks that inject a *“mistakes file”* into every new conversation so the same errors don’t recur.

But here’s what I want to be precise about: *the files compound*. **The AI doesn’t**. A team that adds context for three months has a repo that answers questions a new hire would need weeks of Slack archaeology to figure out on their own. That’s valuable. But it’s valuable because humans did the work of encoding their knowledge into structured files.

---

## 3\. Three Ways Teams Actually Use It

![](https://substackcdn.com/image/fetch/$s_!TrjG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc8ff0aff-e2e1-455b-b0c9-2d9bc46d995e_2160x2260.png)

### Model 1 - Full Adoption

Hannah’s model at DoorDash. Everyone in the repo. Everyone querying. Everyone contributing.

Her entire team works in Claude Code: designers, engineers, data scientist, operations partners. Even her strategy partner, who had never opened GitHub two months earlier, now checks in customer call summaries daily through pull requests.

Hannah was direct about what makes this possible: *“I see a lot of chatter online that this way of working is only for PMs, or only for engineers, or only for technical people. I think that’s very incorrect. Anyone can learn how to do this.”*

The requirement: remove friction from learning. Most people want to learn. The blocker is infrastructure: a teacher, clear docs, team rituals. Forcing people into a terminal without that support stalls adoption. It has to pull rather than push.

### Model 2 - Hub and Spoke

[Dave Killeen’s](https://www.news.aakashg.com/p/this-cpo-uses-claude-code-to-run) approach at Pendo. One power user, everyone else gets the outputs.

Dave connects his calendar, CRM, meeting transcripts from [Granola](https://www.granola.so/), analytics, LinkedIn, and 120+ newsletters. He runs a morning command that synthesizes everything into priorities, account health scores, and drafted Slack messages. His team benefits without touching Claude Code.

> *“I run one command in the morning, and five minutes later, I know what deals need attention,”* Dave said on the pod. *“Who I’m meeting, what I owe them, and what they owe me. The system does it all for me.”*

**What Dave’s morning command actually looks like.** The starter kit ships a `/portfolio-pulse` skill and a `cpo-morning-ritual` workflow that codify this pattern. The input is a single `accounts/portfolio.yaml` registry with one row per managed account - status (healthy / at-risk / expanding / churning), health score, renewal stage, champion status, last executive touch, expansion signals, risks, ARR band. The output is a five-section daily brief: Top 3 Priorities, Calendar Today, Accounts Needing Touch, Open Loops Aging > 7 Days, and Slack Drafts (review-only, never auto-sent).

Sample output (against a populated portfolio):

```markup
## Portfolio Pulse - 2026-05-07 (Daily)

### Today's Top 3 Priorities
1. Acme Corp: pilot procurement demo passed Friday. Confirm outcome before tier-switch commitment slips.
2. Tier-switch modal UX (flagged by 3 accounts): verify Q2 ship status with eng.
3. Credit-usage-dashboard: Acme staked the expansion proposal on it.

### Accounts Needing Touch
- Bravo Inc: last executive touch 18 days ago; renewal in 45 days
```

Five sections, under 800 tokens, runs in < 30 seconds. That’s “I run one command in the morning” turned into a copy-paste pattern.

**Downloadable #2: [Populated Portfolio.yaml + Sample Portfolio-Pulse Output](https://github.com/aakashg/product-growth-team-os/tree/main/product-development/product/customers/accounts).** Nine accounts spanning every status (healthy / at-risk / expanding / churning / new) with health scores, renewal stages, champion status, ARR bands, and risks - plus a fully-rendered sample daily brief produced by /portfolio-pulse against this seed data. Drops Dave’s “I run one command in the morning” claim into a copy-paste artifact your team can replicate Monday morning.

This is the starting model for most teams. The PM becomes the team’s AI interface. And something happens naturally: once teammates see synthesized intelligence appearing in their Slack channel every morning, they get curious about the source. Adoption spreads from there.

### Model 3 - Agent Delegation

[Gabor Meyer’s](https://www.news.aakashg.com/p/how-to-build-a-full-ai-dev-team-in) approach at Google. [21 specialized agents](https://github.com/gabormayer/pm), each with a defined role.

System analyst breaks down specs. Spaghetti-code agent audits maintainability. Product counsel checks compliance. Test architect designs coverage. When Gabor creates development tickets, the agent team reviews them, each contributing from their role’s perspective.

On the podcast, he went from idea to a working app in TestFlight with agents handling ticket creation, Figma design, parallel development, and QA. The key quote: *“I set up these agents in a way how I would imagine in a real world I would work with a group of software engineering team members.”*

This is the scale-up path. Reach for it once Hub and Spoke or Full Adoption is already running.

**The decision is quick.** Less than half your team uses AI tools? Hub and Spoke. More than half? Full Adoption. Ten or more people with eng resources? Layer on Agent Delegation. You can always graduate upward.

### What Each Role Actually Uses It For

The same scaffolding that makes a PM faster makes every adjacent role faster, but they read the repo differently.

- **The CSM** runs a Monday renewal-review workflow that scans the portfolio by renewal window and flags any account where health is below 3, last touch is over 21 days, or the champion has departed. Dave's team reports that what used to be a multi-hour weekly prep ritual now runs as a few minutes of structured triage. When a teammate hands off an account, the new CSM inherits the recurring UX findings, the open loops, and the strategic context. A Salesforce row labeled "champion: John" doesn't carry any of that.
- **The AE** opens the battlecard for the competitor named in the deal, the pricing-objection talk track, and a permissioned customer quote - three tabs, five minutes before the call. When the deal is lost, the win-loss entry feeds back into the battlecard automatically. Most sales orgs leak this loop; the repo closes it.
- **The designer** doesn’t get faster at *making* designs in Claude Code. They get faster at **knowing what to design.** Before opening Figma, they ask the repo for every customer mention of the surface - five quoted moments with dates, severity, and source files, in 15 seconds. Cross-customer UX patterns synthesize themselves.
- **The analyst** ships a metric file, a SQL query, a schema doc, and a `data-catalog.yaml` entry - and the launch gate refuses to merge the feature without all four. Analytics ownership becomes structural, enforced at the launch gate.
- **The on-call engineer** at 2 AM runs `ls bug-investigations/billing/`, finds the prior occurrence of “Stripe webhooks duplicating,” and reads the previous engineer’s root cause + fix + prevention monitor in 90 seconds. The March engineer’s 2-hour debugging session becomes the May engineer’s 90-second read.

The kit ships role-specific onboarding guides and skills for each. The pitch is " *every role gets a 2x lift on the slowest part of their job*.”

---

## 4\. Build One in 4 Weeks

### Week 1: Seed It

You don't need permission or a team initiative. You need one hour.

**Create a repo**. GitHub, Azure DevOps, Bitbucket, GitLab, whatever your org uses. Set up the folder structure from Section 2. Then check in **10 documents** your team asks about most often. The decision log for last quarter, reconstructed from memory if you have to. Current goals. Last 3 sprint retro takeaways. Your 5 most referenced customer call summaries. Current metric baselines.

**Don’t polish anything**. A repo with 10 rough documents is better than a perfectly designed repo that doesn’t exist. Ship the first version.

**Write the root [CLAUDE.md](http://claude.md/)** (template in Downloadable #2): team roster, doc index, channels. One page max. Write a two-line nested [CLAUDE.md](http://claude.md/) for every folder with files: what’s in it, when to read it.

**Push to GitHub so you have version control**. I’ve had to revert my own [CLAUDE.md](http://claude.md/) multiple times after changes degraded performance. You’ll want that safety net.

**If you have [my PM OS](https://www.news.aakashg.com/p/i-spent-100s-of-hours-building-a):** you’re already halfway there. The command from section 1 upgrades it:

```markup
/upgrade-to-team-os
```

It scans your existing personal OS, classifies every file as private or shareable (a file must earn its way into the shared repo), and produces a sanitized fork of the skills and docs that should land in the team space - voice neutralized, working preferences stripped, sub-agents kept private.

After it runs, fill in the team roster in the root [CLAUDE.md](http://claude.md/) (names, Slack IDs, GitHub handles) and push to GitHub. You now have a Team OS that your teammates can clone.

### Week 2: Add One Person

Pick someone curious. Show them one query. *“Why did we choose vendor X over vendor Y?”* If the decision log answers it in 15 seconds, the demo sells itself.

If the repo doesn’t have the answer, that’s your first PR together. Write the decision log entry right there. Now you have two people contributing and the concept has proof.

### Week 3: Set Two Habits

The Team OS lives or dies here.

**After every meeting where a decision is made,** one person writes a short entry:

```markup
# Chose Pricing Model B
**Date:** 2026-05-04 | **Decided by:** Hannah, Alex, Casey

**Options:** (A) Per-seat, simpler. (B) Tiered with guardrails, maps to cost structure.
**Decision:** Model B. P90/P50 cost ratio is 22x. Flat pricing breaks at that ratio.
**Tradeoff:** More complex billing UX.
```

Two minutes. Saves 25 minutes every time someone asks later. That’s 12x return on the effort. And you’re not adding new work. You already write meeting notes somewhere. You already answer *“why did we decide that?”* in Slack. This just redirects the same effort into a place where it persists instead of scrolling away.

**After every customer call,** run the shared customer-call-summary skill. Same format every time. Same fields. Same location. Ten people summarizing calls in identical structure means Claude synthesizes across all of them instantly.

Hannah’s enforcement mechanism for keeping the system current:

*“The feature is not rolled out until the repository is updated.”*

Bake it into your launch checklist. It takes 5 minutes at the end of a launch and prevents months of context rot.

The Team OS doesn’t replace standups or retros. It feeds them. Query before standup. Check in the retro summary after retro. **The repo is the persistent layer. Meetings are the synchronization layer.** Both coexist.

### Week 4: Open It Up

Share the repo with the full team. Run a **15-minute demo.** Show three queries, in this order:

1. *“Why did we choose \[recent decision\]?”* Decision log. 15 seconds. This gets attention.
2. *“What have customers said about \[feature\] this month?”* Summaries synthesize across calls. This shows cross-cutting power.
3. *“How do we calculate \[key metric\]? Show me the query.”* Analytics folder returns definition, SQL, and schema. This gets the engineer who was paged at 2 AM last month to say *“where was this six weeks ago?”*

Those three queries tell the story.

If you have non-PMs in the room, run one query per role:

- **CSM:** *“Which of my accounts have a renewal in the next 90 days and a health score under 3?”* - `portfolio.yaml` + the renewal-review workflow surfaces the punch list in 30 seconds.
- **AE:** *“What did the last 5 deals we lost to Competitor X have in common?”* - `customers/win-loss/` + battlecard. The pattern shows up before the 6th deal.
- **Designer:** *“What have customers said about the pricing page in the last 90 days?”* - call summaries’ UX Findings subsections synthesize across accounts.

Multi-role demos convert multi-role audiences. PMs are an easy audience for this argument; the lift comes when the eng lead, designer, and CSM all see their version of the value.

**Downloadable #3: [Product Growth Team OS Starter Kit](https://github.com/aakashg/product-growth-team-os).** Full repo with the folder architecture. 6 shared skills: customer-call-summary, decision-log-entry, feature-launch-gate, freshness-check, weekly-synthesis, portfolio-pulse. Analytics templates with pre-filled examples you can swap for your data. Session start hook. The `/upgrade-to-team-os` command for PM OS owners.

**Downloadable #4: Team [CLAUDE.md Template](https://github.com/aakashg/product-growth-team-os/blob/main/CLAUDE.md).** Copy-paste Notion page. Team identity, product context, doc index, decision-making norms, preferred formats.

---

## 5\. The Real Problems and How to Survive Them

### Half Your Team Doesn’t Use AI Tools

Start with Hub and Spoke. One power user queries the repo and shares outputs. The team benefits from shared context without anyone touching a terminal. Dave Killeen does this at Pendo. Hannah’s strategy partner started here before learning GitHub.

And this works at any size. **A 3-person startup benefits more per person** than a 50-person org because the context bottleneck is worse when you’re the only PM.

### “This Is Extra Work”

The most common objection and the easiest to counter.

You already write meeting notes. You already summarize calls for your manager. You already answer *“why did we decide X?”* in Slack three times a month. Right now that effort vanishes: the note gets buried, the summary sits in your personal files, the Slack answer helps one person and scrolls away.

A Team OS doesn’t add work. It redirects work you already do into a place where it compounds. The two minutes on a decision log entry save 25 minutes the next time the question comes up. Run that math across a team and the ROI is so obvious your VP won’t need a slide deck.

### Sensitive Data - Classify, Consent, Enforce

The Team OS works in regulated industries (healthcare, finance, EU data subjects) when you treat sensitive-data handling as a three-layer control model - and the kit ships scaffolding for each layer.

**1\. Classify.** The `customer-call-summary` skill applies role-only attribution by default. *“Their VP of Engineering”*, never *“Sam Lee”*. Internal summaries are PII-safe by construction. The skill also explicitly strips GDPR Article 9 special categories (health, racial / ethnic, religious, biometric, sexual orientation) from both summary and transcript files. The default is safety; you have to opt out, not opt in.

**2\. Consent.** When sales or marketing need named external quotes, they don’t get them by relaxing the PII rule. They get them through `case-studies/permissions.yaml`: a registry where each named customer has a signed permission form, an expiration date, an `approved_uses` allow-list, and a `do_not_use` deny-list. Quotes get re-confirmed annually. This is the bridge most B2B companies handle by lawyers panicking and marketing winging it; the repo turns it into a structured artifact.

**3\. Enforce.** Branch protection on `main` (required reviewers, signed commits, no force-push). CODEOWNERS for `customers/` and `analytics/data-catalog.yaml`. A pre-commit + CI Gitleaks scanner blocking PII patterns before they land. A documented `git filter-repo` runbook for GDPR Article 17 erasure requests, including the sub-processor deletion ticket to your LLM vendor. A DPIA template in `team/compliance/` with retention schedule, risk register, and DPO sign-off.

The repo on its own isn’t SOC2 / GDPR / HIPAA compliant. Compliance comes from operating the repo with these three layers in place. The kit gives you the artifacts an auditor can put in a binder; you wire up the enforcement that fits your industry.

**Downloadable #5: [Three-Layer Sensitive-Data Control Checklist (PDF)](https://github.com/aakashg/product-growth-team-os/raw/main/team/compliance/sensitive-data-checklist.pdf).** For your CISO / DPO / compliance reviewer: classify → consent → enforce → sub-processor controls mapped row-by-row to the named artifacts in the repo (PII rule sections of the customer-call skill, permissions.yaml, branch protection, CODEOWNERS, Gitleaks pre-commit hook, GDPR Article 17 erasure runbook, DPIA template). Hand it across the table during your adoption review.

### Role Transitions (the 47% Problem)

The post’s opening cites *47% of companies call institutional knowledge loss their top offboarding challenge.* The kit’s answer is two structural artifacts that catch what evaporates from a PM’s head when they leave:

1. **Append-only hindsight notes on decisions.** When a PM leaves the team, their last week includes one task: append a `## Hindsight` block to every decision they authored in the last 12 months. One sentence each, dated, signed. *“2026-08-01 (6 months in, outgoing PM): P90/P50 cost ratio settled at 18x not 22x. Tier B is leaving money on the table; revisit before Q3.”* The original decision stays untouched. The successor inherits the call AND the calibration of watching it play out.
2. **A** `pm-handoff` **workflow** that runs in five steps: portfolio sweep (transition every account ownership cleanly with named successors), decision revisit (the hindsight notes above), unshipped drafts and bets (surface what was on the shelf), warm intros (synchronous three-way calls scheduled in the final two weeks while the outgoing PM is still in the room), final handoff doc (manager sign-off contingent on completion).

Most handoff templates capture documents. This one captures *calibration*: the part that’s actually load-bearing and is exactly what the 47% stat is measuring.

### Context Rot

The metric snapshot from three months ago is wrong. The decision log references a killed feature. If nobody maintains the repo, Claude gives answers based on stale context and trust erodes fast.

Three fixes, layered. The **feature launch gate** prevents rot on new features. A **weekly freshness check** (skill included in the downloadable) scans for files untouched in 90 days. [OpenAI’s harness engineering team](https://openai.com/index/harness-engineering/) runs what they call garbage collection: automated background tasks that scan for deviations and open targeted cleanup PRs. For teams without automation, quarterly manual pruning works: one hour, rotate the responsibility.

### “We Already Have Notion”

Notion stores documents. A Team OS stores context that an AI can query with structured navigation and progressive disclosure. You don’t replace Notion. You add a query layer on top.

[Gabor Meyer](https://www.news.aakashg.com/p/how-to-build-a-full-ai-dev-team-in) uses Confluence and Jira, both connected via Atlassian MCP. Docs live in Confluence. Claude queries them through the MCP. The repo holds navigation files, skills, and agent definitions that tell Claude *how* to work with everything else.

**For your VP who will ask:** the Team OS replaces ad-hoc Slack Q&A, manual onboarding walkthroughs, and repeated *“why did we decide X?”* meetings. It complements your wiki, your ticketing system, and your meeting cadence. It doesn’t touch sprint planning, design review, or release management.

---

## 6\. What the First Month Actually Looks Like

I asked Hannah to walk me through the actual progression at DoorDash. Not hypothetical. The real sequence.

![](https://substackcdn.com/image/fetch/$s_!xREl!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fca26c20e-156c-48e2-a355-3e9926d42017_2160x2260.png)

### Phase 1: Lay the Foundation

Hannah started by moving all PRDs into markdown files in the repo. The goal was specific: make it easier to work on PRDs with Claude, and for engineering to use the PRD with Claude to write the TDD and hand off for agentic development. Then she organized all customer calls into the repo to make it easier to write PRDs from customer context and to synthesize across calls.

This was intentional from day one. Hannah had done extensive research on how models work, context engineering, and context management before designing the repo structure. The nested [CLAUDE.md](http://claude.md/) files, the summary-first architecture, the tiered context loading: all of it was planned based on how LLMs actually consume information. She also checked in shared skills for the team to use right away.

The core team (engineering, analyst, PM) was in the repo from the start. Other functions joined as the system became useful to them.

### Phase 2: The Team Starts Building Together

Phase two was about the whole team contributing shared skills and agents. Other people started checking in their own work alongside what Hannah had set up. Her analyst started checking in skills that made it easy to run common analyses. Engineers contributed investigation templates. The team was riffing and partnering to build the system together.

This is the shift that matters. Phase 1 is one PM setting up infrastructure. Phase 2 is the team owning it collectively. Each person makes the system better for everyone else. The analyst’s skills help the PM run queries. The PM’s customer summaries help the designer prioritize. The engineer’s bug investigations help the next person who encounters the same issue.

Hannah’s strategy partner started contributing around this time. First PR took 20 minutes with Hannah’s help. Second PR took 5 minutes. By the end of the week, daily.

### Phase 3: The System Compounds

The feature launch gate kicked in: no feature ships until the repo is updated. Decision log entries after key meetings. Customer call summaries as a team-wide habit.

Full team access. The 15-minute demo. Three queries. The engineer who'd been paged at 2 AM the previous month saw the analytics structure in the demo and immediately started checking in his team's query files.

### The Lesson

The common advice is to start small and iterate. Hannah’s approach was different: **design the architecture deliberately, then fill it in.** She didn’t start with a flat folder of random docs and gradually organize them. She researched how models handle context, designed the repo structure to match, and then filled in the content. The architecture was right from day one. The content grew into it over weeks.

Hannah on the biggest mistake PMs make with this kind of system: *“People try it for a day, don’t get good results, and decide it’s not for them. I’ve spent 1,500 hours in Claude and I’m still iterating on my setup and improving it literally every single day.”*

A Team OS is infrastructure. The infrastructure doesn't need to be perfect to start being useful. The system gets better every week because humans make it better, and the improvement compounds.

*If you want a structured approach to building this, Hannah and Carl are teaching a [Team OS course on Maven](https://maven.com/hannah-stulberg/how-to-build-your-teamos) this Sunday at 10AM PT / 1 PM ET / 7PM CET that walks through the full setup.*

---

## This Weekend

Create the repo. Write the [CLAUDE.md](http://claude.md/). Check in the 10 documents your team asks about most. Push to GitHub. Show one teammate on Monday.

The compounding starts with the first commit.

**Downloadable #6: Adoption Playbook.** The Slack message to pitch your team. The 15-minute demo script: which 3 queries, in what order, what to say about each. Weekly ritual template. Feature launch gate checklist. Meeting integration guide (how Team OS feeds standups and retros).

---

### Go Deeper

- [I Spent 100s of Hours Building a PM OS for You](https://www.news.aakashg.com/p/i-spent-100s-of-hours-building-a): the personal foundation
- [The Ultimate Guide to Context Engineering for PMs](https://www.news.aakashg.com/p/the-ultimate-guide-to-context-engineering): the theory underneath
- [How to Build a Full AI Dev Team in Claude Code](https://www.news.aakashg.com/p/how-to-build-a-full-ai-dev-team-in): Gabor’s 21-agent workflow
- [How to Build a Team OS in Claude Code](https://www.news.aakashg.com/p/how-to-build-a-team-os-in-claude): Hannah’s full podcast walkthrough
- [This CPO Uses Claude Code to Run His Entire Work Life](https://www.news.aakashg.com/p/this-cpo-uses-claude-code-to-run): Dave’s living files
- [How to Turn Claude Code into an Operating System](https://www.news.aakashg.com/p/how-to-turn-claude-code-into-an-operating): Carl’s context management
- [Taste at Speed](https://www.news.aakashg.com/p/theres-a-new-pm-skill-its-called): Boris Cherny’s prototype-first workflow

See you next week 🫶,

Aakash

---

### Downloadables for Paid Subscribers

1. **[Upgrade to Team OS skill](https://github.com/aakashg/product-growth-team-os/blob/main/.claude/skills/upgrade-to-team-os/SKILL.md).** Converts your Personal OS to a workable Team OS in minutes, keeping personal context private.
2. **[Populated Portfolio.yaml](https://github.com/aakashg/product-growth-team-os/blob/main/product-development/product/customers/accounts/portfolio.yaml) + [Sample Portfolio-Pulse Output](https://github.com/aakashg/product-growth-team-os/blob/main/product-development/product/workflows/cpo-morning-ritual/reference/2026-05-07.md).** Nine synthetic accounts spanning every status (new / healthy / at-risk / expanding / churning), with a sample daily brief produced by `/portfolio-pulse`. Drops Dave’s *“I run one command in the morning”* claim into a copy-paste artifact.
3. **[Product Growth Team OS Starter Kit](https://github.com/aakashg/product-growth-team-os).** Full repo: folder architecture, 6 shared skills (customer-call-summary, decision-log-entry, feature-launch-gate, freshness-check, weekly-synthesis, portfolio-pulse), analytics templates, session start hook, `/upgrade-to-team-os` command for PM OS owners.
4. **Team [CLAUDE.md](http://claude.md/) Template.** Copy-paste Notion page. Team identity, product context, doc index, decision-making norms, preferred formats.
5. **[Three-Layer Sensitive-Data Control Checklist (PDF)](https://raw.githubusercontent.com/aakashg/product-growth-team-os/main/team/compl%20%20%20iance/sensitive-data-checklist.pdf).** For compliance reviewers: classify / consent / enforce mapped to artifacts in the repo (PII rule sections, `permissions.yaml`, branch protection, CODEOWNERS, Gitleaks config, GDPR Art. 17 runbook). DPIA template included.
6. **[Adoption Playbook](https://pgnewsletter.notion.site/Team-OS-Adoption-Playbook-35980214aa4a808bb5a2e1e563c3bb73?source=copy_link).** Slack pitch, demo script, weekly ritual, launch gate checklist, meeting integration guide.

---
*Clipped from [substack.com](https://substack.com/inbox/post/196814801) on 2026-05-11T19:03:06-04:00*
