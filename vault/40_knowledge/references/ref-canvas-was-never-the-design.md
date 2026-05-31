---
title: "The Canvas Was Never The Design"
source: "https://substack.com/inbox/post/194401692"
author:
  - "[[MC Dean]]"
published: 2026-04-22
created: 2026-05-31
description: "What Claude Design reveals, what the Eames always knew, and two tools I built this week"
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain:
  - "design-team"
ai-context: "MC Dean uses Claude Design's launch (and Figma's 7% stock drop) plus Ray Eames's philosophy to argue the canvas was never the design — the value is in the thinking/decisions, not the artifact tooling; includes two tools he built that week."
---
![Eames Office – Official Website & Online Store](https://substackcdn.com/image/fetch/$s_!5jXB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a51fbad-d571-4f9b-a6bb-ef19d90ba6d3_2000x1500.jpeg)

Eames Office

[Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) launched two days ago. You talk to it and it designs. Complex pages that used to take twenty prompts now happen in two. Figma’s stock [dropped 7%](https://www.marketbeat.com/instant-alerts/figma-nysefig-shares-down-7-should-you-sell-2026-04-17/) by close of trading on Friday. The headlines are all about AI versus designers, tools versus jobs, who wins, who loses.

I want to talk about something else.

If you know where to look, there is something extraordinary happening here.

---

## The thing that is visible

[Ray Eames](https://www.eamesoffice.com/) had a line that design schools quote so often it has almost lost its meaning.

“Design is a plan for arranging elements in such a way as best to accomplish a particular purpose.”

Let’s note that it does not mention a rendering, a deliverable, a beautifully crafted file.

It underscores a plan: an act of thinking about purpose, and what it demands.

When Claude Design (or any agent assisted design tool) generates a working prototype from a two-sentence prompt, it is not replacing the design. It is rendering what the design already was. The thinking happened in the conversation. The intent happened in the language. The judgment about purpose and person and constraint happened before anything appeared on a screen.

The canvas was where we went to externalise the thinking. Now there is a faster way to externalise it and that means the canvas, which we spent decades treating as the design, has been revealed as something different. It was always the artifact that design thinking left behind.

This is a clarification that has been a long time coming.

---

## What we're trading away

We do owe it to ourselves to be honest about what changes.

The canvas had friction. You would be making something and it would not quite work, and the wrestling with the material, the three pixels that were wrong, the component that refused to behave, would reveal something you had not understood about the problem yet. Constraints imposed by the tool forced clarity about what was essential. Eames worked within the constraints of plywood and fibreglass not despite them but through them. The resistance was the method.

There is something in the making, in the physical negotiation with a medium, that conversation does not fully replicate. I know a designer who says she does her best thinking with her hands and not at a keyboard, she likes moving things around and drawing. I understand that.

---

## Where the friction went

When execution was the hardest part, you could hide weak thinking behind technical skill. A designer who could not articulate why something should be a particular way could still make it beautiful, and beauty was a kind of argument. It often passed the bar with clients and in product teams.

Now the argument has to come first. The intent has to be precise enough, specific enough, purposeful enough to produce the output you actually need. Claude Design will render your clarity faithfully. It will also render your confusion faithfully.

The constraint has shifted from “can I execute this?” to “can I think this clearly enough?”

That is more design, not less. That is design moving up to where it was always supposed to live.

---

## The piece that is still missing

You can brief Claude Design on purpose. You can give it your brand files, your design system, your target user. You can bring genuine clarity to the conversation. It will generate something technically correct, on brand, well structured.

It will still feel oddly wrong.

Here is why: We have given agents procedural knowledge (how to do things) but we have no way of telling them what something should feel like, and for designers (also musicians, architects, artists…), that feeling is the a huge part of job.

Think about how you actually work. Before you open any tool, before a single decision gets made, you have already have an image or a sensation of something in your mind. You have collected images, pinned references, grouped things spatially, written “YES, this energy” on a sticky note next to a photograph. That moodboard is the highest-bandwidth communication tool in your entire workflow. It carries colour temperature, spatial rhythm, typographic character, emotional register, material quality, and a dozen other signals that would take thousands of words to describe, and even then you would lose the texture.

Now look at what we have built for agents. SKILL.md tells them how to write good CSS. System prompts tell them how to behave. Brand guides tell them which colours and fonts to apply.

There is no protocol for how things should feel.

---

## mood.md - the counterpart to SKILL.md

Designers already have the answer. You already curate visual direction. You already know how to communicate aesthetic intent through images. The problem is that this communication happens on a canvas, in a spatial medium, and it has no way to cross the bridge into the text-based world where agents live.

That is what I have been noodling on this past week. It is called mood-protocol, and the idea is really very simple.

Where SKILL.md says “here is how to do things,” [mood.md](https://github.com/Owl-Listener/mood-protocol) says “here is what it should feel like.”

You take your moodboard, the one you have already made, the one with the sticky notes and the annotations and the spatial groupings and all your scrawls and export it as an image. Upload it to the AI you already use. Paste one prompt. The vision model reads everything: the images, the annotations, the relationships, the things you labelled as references and the things you labelled as anti-references. Then it generates a structured [mood.md](https://github.com/Owl-Listener/mood-protocol) that any agent can read.

The output is a creative direction brief: colour palette with hex values and semantic names, typographic character, spatial rhythm, emotional register, and an Agent Instructions section that tells any AI exactly how to apply this direction when making design decisions.

One section matters more than I expected: the anti-reference. In design, knowing what to avoid is as valuable as knowing what to pursue. “NOT corporate dashboard” carries as much information as “warm editorial layout.” Maybe more, because it closes off an entire territory of bad decisions before anyone wastes time making them. Eames chose constraints deliberately, because constraints are the method. The anti-reference is a constraint with a name.

The [mood.md file](https://github.com/Owl-Listener/mood-protocol) lives in your repo. It versions with your code. It is there when you open Claude Design or nay other agent tool and when you come back to a project three months later and need to remember what it was supposed to feel like. It is the felt brief made portable and persistent.

A brand guide tells Claude Design what to apply. [mood.md](https://github.com/Owl-Listener/mood-protocol) tells it how the result should feel when everything is applied correctly. Those are not the same instruction. One is specification. The other is more about your judgment.

---

## What this means together

The Eames-inspired Test is five questions you answer before you open any design tool. Purpose, person, constraints, the one thing, how you will know it worked. The thinking that should precede the canvas. The field guide I released this week, **[46 ways to work with Design Agents effectively](https://github.com/Owl-Listener/ai-design-field-guide)**, is built around that discipline. The brief before the tool, intent before execution.

**[mood.md](https://github.com/Owl-Listener/mood-protocol)** is the companion to that in some ways. The Eames-inspired Test captures the rational brief. mood.md captures the felt brief. Together they are the full picture of what a designer brings to a project, the thinking and the feeling, externalised from the designer’s head and made usable by any agent, any tool, any collaborator.

This is what is actually happening this week, underneath the Figma stock price and the job-displacement headlines.

We are building the infrastructure for design intent. The protocols, the formats, the structured ways of carrying what designers know and feel into a world where the execution layer is increasingly automated. That work is urgent and it is fundamentally design work, even though it looks like it is being done with terminals and markdown files rather than Figma and sticky notes.

The Eames would recognise it immediately. They spent their careers finding new ways to communicate complex ideas to people who did not share their vocabulary. They used films, exhibitions, multi-screen installations, whatever the medium demanded. The medium is different now. The work is the same.

“There is no Eames style, only a legacy of problems beautifully and intelligently solved.” - Bill Lacey

---

## What you can do this week

Run the Eames Test before you open you favourite agent design tool. Answer the five questions for yourself properly. Take ten minutes and let yourself percolate. Let the thinking precede the canvas.

Generate a [mood.md](https://github.com/Owl-Listener/mood-protocol) for a project you are working on now. Drop your reference images in a folder. See what it surfaces about what you already know but have never written down.

When you are in Claude Design, brief it on feeling, not just function. “Confident but not aggressive. Dense with information but never overwhelming. The kind of interface a person trusts immediately, the way you trust a good doctor.” That is a design brief. That right there is the friction that has moved.

The canvas was never the design. We always knew that.

Now the question is what you build with the time you just got back.

---

*The field guide “ [46 ways to work with Claude Design](https://github.com/Owl-Listener/ai-design-field-guide) ” is on GitHub now. [mood-protocol](https://github.com/Owl-Listener/mood-protocol) is also on Github and both are open source, MIT licensed, free to use.*

---
*Clipped from [substack.com](https://substack.com/inbox/post/194401692) on 2026-05-31T16:05:57-04:00*
