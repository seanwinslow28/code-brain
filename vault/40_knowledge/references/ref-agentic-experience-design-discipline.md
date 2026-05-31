---
title: "Agentic Experience Design Is a New Discipline. Give it a whirl."
source: "https://substack.com/inbox/post/195451831"
author:
  - "[[MC Dean]]"
published: 2026-04-29
created: 2026-05-31
description: "Six layers, 42 skills, 18 commands. Free, MIT, installable in Claude Code or Gemini CLI this week."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain:
  - "design-team"
ai-context: "MC Dean frames Agentic Experience Design (AXD) as a new discipline with six layers (model-interaction, alignment-reasoning, system-behavior-shaping, evaluation, agent-orchestration, +1) shipped as a free MIT Claude Code/Gemini plugin — 42 skills, 18 commands — translating CHI/FAccT research into loadable design skills (error personality, handoff protocols, anti-patterns)."
---
![](https://substackcdn.com/image/fetch/$s_!Q3A3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff343766c-3845-4713-b496-eddc06af15bd_7680x4320.jpeg)

Photo by Google DeepMind: https://www.pexels.com/photo/a-diagram-of-a-model-25626448/

Agentic Experience Design (AXD) is a discipline now. For some it will still feel like an emerging discipline but I think for many it is shaping up in real-time. It has its own vocabulary, definitions, practices and is coming into its own. Some of the terms are *Mixed-initiative flow, Harm anticipation, Handoff protocol, Error personality.* If you have not heard those terms, this post is about introducing them and giving you the tools to have a go.

Six layers. 42 skills. 18 commands. Installable in your AI agent in one command, free, MIT-licensed, and ready to be used on real work this week. The repo is at [github.com/Owl-Listener/ai-design-skills](https://github.com/Owl-Listener/ai-design-skills).

The work in the underlying ideas was done by many other people: by alignment researchers and HCI scholars and the agent community over the last three years. What did not exist was the translation layer: the thing that takes a paper from CHI or FAccT and turns it into a skill your AI agent loads automatically when you ask it to design or audit anything. That is the contribution this week. Translating the science into a form designers can actually reach for when they’re mid-flow on a feature.

---

## Six layers mapping the discipline

Each plugin owns one part of the territory you have to cover to design Agentic products well. Seven skills and three commands inside each, the same shape across all six, because the discipline turns out to have a clear shape.

**model-interaction-design** is how humans and AI take turns. Conversation patterns, mixed-initiative flow (when the user drives, when the AI drives, when they share, when control transfers), progressive disclosure, generative UI, multimodal orchestration. This is the layer most designers feel comfortable in already. Most current Agentic design work has lived here.

**ai-alignment-reasoning** is the work designers should be involved in and that the technical alignment community specialises in: Harm anticipation, Guardrail design, Transparency patterns, Value specification, Escalation, Consent and agency. The technical alignment teams are working on the inside of the model. This plugin is for the alignment work that has to happen on the design side.

**system-behavior-shaping** is how the AI shows up in the experience. Persona architecture, tone calibration, behavioural consistency, cultural adaptation, domain voice, emotional design. The skill in this plugin I keep returning to: *error personality*. *“Every AI makes mistakes. Error personality is how it handles those moments. It is often the most revealing aspect of an AI persona, because it is where the mask of competence slips and the user sees the character underneath.”* That sentence is not on any design curriculum I have ever seen, and it is the kind of thing every designer making an Agentic product will eventually need to think about.

**evaluation** is the plugin most designers have not opened yet and most need to. Failure taxonomy, Output quality rubrics, Comparative evaluation, Longitudinal measurement, Task success metrics, User satisfaction signals, Heuristic evaluation for AI specifically, because the Nielsen heuristics from 1994 do not cover hallucination or overconfidence or sycophancy. If you cannot tell whether your Agent is getting better, you cannot ship it responsibly. This plugin is the bridge for that.

**design-agent-orchestration** is the plugin I expect to grow fastest, because the products being built right now are no longer single-agent: Agent role design, Handoff protocols, State management, Failure recovery, Human-in-the-loop, Observability… *The black hole, the echo chamber, the context cliff* are anti-patterns real multi-agent products can fall into and naming them helps you avoid them.

**prompt-architecture** is for the work that does not feel like design but it is. Chain-of-thought design, Constraint specification, Context engineering, Few-shot patterns, Prompt versioning, System prompt structure, Template design. Designers have been writing prompts for roughly two years now and most of us are still doing it as a craft we have not formally learned. This plugin should help with this.

---

## Wait, alignment? Yes, alignment.

A note on the second plugin, because this is the part of the discipline I want us to consider most.

The technical alignment community has been doing extraordinary work on the inside of the model: RLHF, Constitutional AI, Mechanistic interpretability. It has been a research conversation, and it has been research-shaped.

What is an opportunity for design, is the *outside-of-the-model* version of the same work. When you write a guardrail that escalates a conversation to a human at the right moment, that is alignment. When you architect a persona that does not collapse under pressure, that is alignment. When you anticipate the harms a feature could cause before you ship it, that is alignment. When you design the right escalation when the model is wrong, that is alignment.

We have been doing this thinking for years and not calling it that, because the only intelligence in the equation was human, and we had other words for it: usability, empathy, guardrails, taste, care. The skills in `ai-alignment-reasoning` are those words rewritten for the new world, the new audience, the new reader who is now reading our files and acting on them.

---

## How to use the skills, even if you are new to this

Install the skills in your favourite agent and take them for a spin.

Try this question with your agent, exactly as written:

> *“I am designing an AI assistant for customer support. Help me write the error states for when the assistant does not understand the user’s question. Walk me through the trade-offs.”*

Without the skills installed, the agent will give you five generic apologies and move on. With the skills installed, the agent reads `error-personality.md` and `tone-calibration.md`, and the response now actively avoids over-apologising, deflection, blaming the user, and the existential crisis pattern. It produces messages with character, opinionated about what good and bad look like for your specific persona. The output is the same words, structured by an entirely different muscle.

That is what the skills do. They give the agent a frame for thinking about your work. Your job is to be there in the loop, push back, redirect, and decide which output is the one to ship.

If you do not use a CLI (command line) agent like Gemini or Claude Code yet, this is the moment to learn one. The browser chat is not where any of this lives. Skills do not load there, instruction files are not read there, and the design surface this post argues for (the file the agent reads at the start of every session) does not exist in a tab. The CLI is where Agentic Experience Design really happens. The earlier you are there, the more you will shape this practice.

---

## What’s next for us

Take this. Install it. Use it on real work. Then tell me what is missing.

The skill files are plain markdown. Editing one is a sentence and a commit. The discipline gets better when more of us write it. If you fork the repo and add a skill *eval-design-for-multimodal*, *cultural-bias-stress-tests*, *the-thing-you-are-tired-of-explaining* please send it back. I want to read it.

Some of these skills will hold up. Some will need to be rewritten. Some are missing. There is nothing yet about the perceptual layer of design, the part that tells the agent what something should *feel* like, not just how it should behave. I am working on that one elsewhere and a start is mood.md: https://github.com/Owl-Listener/mood-protocol

Here is a great start for you though: Six layers, 42 skills, free, this morning. The repo is at [github.com/Owl-Listener/ai-design-skills](https://github.com/Owl-Listener/ai-design-skills).

There is a discipline forming, and we are the community of designers shaping it.

---
*Clipped from [substack.com](https://substack.com/inbox/post/195451831) on 2026-05-31T16:06:45-04:00*
