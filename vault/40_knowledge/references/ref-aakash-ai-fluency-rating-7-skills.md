---
title: "Zapier, Shopify, and Meta Now Rate Employees on AI Fluency. Most PMs Would Score \"Unacceptable.\""
source: "https://aakashgupta.medium.com/zapier-shopify-and-meta-now-rate-employees-on-ai-fluency-most-pms-would-score-unacceptable-4d4fe23c2fd8"
author:
  - "[[Aakash Gupta]]"
published: 2026-03-19
created: 2026-05-29
description: "Your company is about to start grading you on how well you use AI. And right now, most PMs would fail."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [product-management]
ai-context: "Aakash Gupta breaks down the 7 skill areas companies now formally grade PMs on — prompting, copilots, agents, prototyping, AI-powered discovery, discovery for AI features, and AI-powered analysis — with the priority order to build them."
---
![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0NK3iZPARQkEeir8gPTFLA.png)

Your company is about to start grading you on how well you use AI. And right now, most PMs would fail.

Zapier, Shopify, and Meta have all started rating employees on AI fluency, from "Unacceptable" to "Transformative." These aren’t internal experiments. They’re formal performance evaluation criteria that affect promotions, compensation, and whether you keep your role. The companies that aren’t doing this yet are watching the ones that are.

I’ve spent hundreds of hours breaking down the 7 skill areas that separate each level. Not 7 tools. Not 7 apps. Seven skill categories that determine whether your AI usage looks like a party trick or a professional operating system.

You don’t need to try 1,000 AI tools. You need to get genuinely good at these 7 things.

## 1\. Prompting

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*foTOphS_4LQdT8Hyb3Yihw.png)

Most PMs type lazy one-liners into ChatGPT and wonder why the output reads like a Wikipedia article with bullet points.

The best PMs write structured prompts with XML tags, defined roles, chain-of-thought reasoning, and few-shot examples. Their prompts are on version 12. They’ve iterated on the same prompt a dozen times because each iteration produced noticeably better output than the last.

The gap between a one-liner prompt and a structured prompt isn’t 10% better output. It’s a completely different category of output. One gives you generic filler. The other gives you something you’d actually put in front of your VP.

I built a complete [PM prompt library](https://www.news.aakashg.com/p/pm-prompt-library) with frameworks for every major PM workflow. Start there, then iterate every prompt until the output matches what you’d actually ship.

## 2\. AI copilots

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*0jCwVT8xTawUtOCY-yIrjQ.png)

Notion AI drafts your PRD. GitHub Copilot writes your SQL. Figma AI iterates your mocks. These are copilots, tools that assist you while you’re actively working.

The PMs who’ve woven copilots into their daily workflow are saving 5–10 hours a week. Not on a good week. Every week. Because the time savings compound across dozens of small tasks that each save 10–20 minutes.

The PMs who haven’t integrated copilots are falling behind without realizing it. They’re still manually formatting docs, hand-writing queries, and rebuilding wireframes from scratch. They feel productive because they’re busy. But busy and productive diverged the moment copilots became reliable enough to trust with execution work.

I covered the full [copilot integration strategy](https://www.news.aakashg.com/p/ai-stack-pm) in a keynote breaking down which copilots matter for which PM tasks.

## 3\. AI agents

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*2IXGXgYLVaI7RPlcLidBsw.png)

Copilots wait for you to ask. Agents go do the work without you.

A research agent synthesizes 200 competitor pages overnight and has a summary waiting for you in the morning. A code agent builds your prototype from a spec while you’re in a meeting. A feedback agent processes 500 support tickets and clusters them by theme, severity, and recommended action.

The skill with agents isn’t prompting. It’s setting the right guardrails. Because agents will confidently do the wrong thing if you let them. They’ll hallucinate competitor features that don’t exist. They’ll build prototypes that look great but solve the wrong problem. They’ll analyze data with flawed assumptions and present the results with perfect confidence.

The PMs who get value from agents are the ones who define clear boundaries, validate outputs, and treat agent work as a first draft that needs human judgment applied on top.

## Get Aakash Gupta’s stories in your inbox

Join Medium for free to get updates from this writer.

I wrote the practical [agent setup guide](https://www.news.aakashg.com/p/practical-ai-agents-pms) and the complete [AI agents guide for PMs](https://www.news.aakashg.com/p/ai-agents-pms) covering everything from configuration to the mistakes that kill agent reliability.

## 4\. AI prototyping

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*zBYSwIY_QFbHec6O356EIQ.png)

I went from idea to working app in under an hour last week. No designer. No engineer. Just a prompt and [Cursor](https://www.news.aakashg.com/p/how-cursor-grows).

When you can show stakeholders a working prototype instead of a slide deck, everything changes. The conversation shifts from “do we understand the spec?” to “does this actually solve the problem?” You skip three weeks of interpretation, misalignment, and revision cycles because everyone is reacting to the same working software.

This is the single highest-leverage PM skill right now. Nadav Abrahami, who co-founded Wix ($5.5B) and now runs Dazl, said it directly on [the podcast](https://www.news.aakashg.com/p/nadav-abrahami-podcast). His team used to assign three developers for weeks to build functional prototypes. Now every feature goes through AI prototyping before a single line of production code gets written.

I published the complete [AI prototyping tutorial](https://www.news.aakashg.com/p/ai-prototyping-tutorial) covering the workflow from idea to working prototype to stakeholder demo.

## 5\. AI-powered discovery

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*olv0eGFzOOvJYZQgJwg0Fg.png)

You used to interview 5–10 users and hope you caught the right patterns. Now you upload 100+ transcripts and get themes, direct quotes, and sentiment analysis in hours instead of weeks.

The bottleneck isn’t research bandwidth anymore. It’s knowing what questions to ask the AI. If you feed it transcripts with no framework for what patterns to look for, you get generic summaries that tell you nothing. If you define the specific signals you’re tracking and the hypotheses you’re testing, you get insights that would have taken a full-time researcher two weeks to surface.

Teresa Torres talked about this evolution on [the podcast](https://www.news.aakashg.com/p/teresa-torres-podcast) and her framing changed how I think about what AI-powered discovery should look like.

## 6\. Discovery specifically for AI features

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*fmlXAYRNrSUlrO8ui99iqg.png)

Here’s the problem that makes AI product discovery fundamentally different from traditional discovery. Users can’t tell you what AI features they want because they don’t know what’s possible.

You can’t survey your way to an AI roadmap. Nobody would have asked for predictive text, auto-generated summaries, or Smart Compose before they experienced them. The only way to discover what AI features your users actually want is to prototype them, put working versions in front of real users, and watch what they actually do.

This is why AI prototyping and AI discovery are so tightly connected. The [discovery guide for AI features](https://www.news.aakashg.com/p/how-to-build-ai-products) walks through the full process from hypothesis to prototype to user signal to roadmap decision.

## 7\. AI-powered analysis

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*qO1oss5H0VsdnkJj9-i6Pg.png)

I used to wait 3 days for the data team to run a query. Now I describe what I need in plain English, get the SQL back, and validate it myself.

Dashboards. Cohort analysis. A/B test interpretation. Funnel breakdowns. The PMs who can self-serve on data make faster decisions because they’re not waiting in a queue behind 15 other requests. They have the answer before the next standup instead of after the next sprint.

This doesn’t mean you don’t need a data team. It means the data team focuses on complex statistical analysis and infrastructure while you handle the exploratory questions that used to take three days and a Jira ticket.

The complete [AI analysis guide for PMs](https://www.news.aakashg.com/p/ai-foundations-for-pms) covers the workflow from plain-English question to validated SQL to decision.

## The priority order that matters

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*rzSA7uufqw1MWN26T2P6Rw.png)

If you’re starting from zero, this is the sequence that builds on itself most efficiently.

Prompting first, because every other skill depends on it. Copilots second, because the daily time savings are immediate. Analysis is third, because self-serve data accelerates every decision you make. Discovery the fourth. Prototyping fifth. Agent's sixth. AI feature discovery last, because it requires all the other skills working together.

Master the skills, not the tools. The tools will change every six months. The skills compound forever. I cover each of these skill areas with practical guides and frameworks in [Product Growth](https://www.news.aakashg.com/), where 200K+ product leaders are building the AI fluency that companies are now formally evaluating.

The rating scale exists whether you’re ready for it or not.

---
*Clipped from [medium.com](https://aakashgupta.medium.com/zapier-shopify-and-meta-now-rate-employees-on-ai-fluency-most-pms-would-score-unacceptable-4d4fe23c2fd8) on 2026-05-29T15:10:00-04:00*
