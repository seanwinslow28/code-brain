---
title: "How to Design like OpenAI and Figma"
source: "https://www.news.aakashg.com/p/ed-bayes-gui-seiz-podcast"
author:
  - "[[Aakash Gupta]]"
published: 2026-04-10
created: 2026-05-23
description: "OpenAI design lead and Figma AI design director show the code-canvas loop, live demo, and 5-step adoption roadmap for any team."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [creative-studio]
ai-context: "Aakash Gupta podcast with Ed Bayes and Gui Seiz on the design language and process used at OpenAI and Figma — taste, system-driven UI, and how design teams operate inside AI-native product companies."
---
Ed Bayers leads design on Codex at OpenAI and Gui Seiz leads AI design at Figma. Today, they drop a masterclass on the new design workflow

![](https://www.youtube.com/watch?v=C_eXo6oCvRA)

*Check out the conversation on [Apple](https://podcasts.apple.com/in/podcast/how-to-design-like-openai-and-figma/id1763555775?i=1000760746398), [Spotify](https://open.spotify.com/episode/2q9Sk4a5htqzlJ4XSh8PL8?si=VWDjbQAoSAWiNSytMhm4ZA), and [YouTube](https://youtu.be/C_eXo6oCvRA).*

Brought to you by:

1. **[Bolt](https://bolt.new/solutions/product-manager?utm_source=Promoted&utm_medium=email&utm_campaign=aakash-product-growth)**: Ship AI-powered products 10x faster
2. **[Amplitude](https://amplitude.com/session-replay?utm_campaign=session-replay-launch-2025&utm_source=linkedin&utm_medium=organic-social&utm_content=productgrowthpodcast)**: The market-leader in product analytics
3. **[Pendo](http://www.pendo.io/aakash)**: The #1 software experience management platform
4. **[NayaOne](https://nayaone.com/aakash/)**: Airgapped cloud-agnostic sandbox
5. **[Product Faculty](https://maven.com/product-faculty/ai-product-management-certification?promoCode=AAKASH550C7)**: Get $550 off their #1 AI PM Certification with my link

---

## Today’s episode

Sometimes, I get access to the wildest guests on this podcast. Today, we get the awesome opportunity to look inside the design processes at **[OpenAI](https://www.news.aakashg.com/p/how-to-break-into-openai) and [Figma](https://www.news.aakashg.com/p/how-figma-grows)**:

- [Ed Bayes](https://www.linkedin.com/in/edbayes/) leads design on Codex at OpenAI
- And [Gui Seiz](https://www.linkedin.com/in/guiseiz/) leads all AI design at Figma

And they worked with me to put together a **masterclass on how to design in the AI era**.

*If you want to design like the leading AI companies, this episode is for you: complete with screen shares and everything else you need to adopt the new AI design workflow.*

---

***If you want access to my AI tool stack** - Dovetail, Arize, Linear, Descript, Reforge Build, DeepSky, Relay.app, Magic Patterns, Speechify, and Mobbin - **grab [Aakash’s bundle](https://bundle.aakashg.com/)**.*

***I’m accepting applications for my third LandPMJob cohort. [Join Me](https://www.landpmjob.com/).***

---

## Newsletter deep dive

*As a thank you for having me in your inbox, here is the complete guide to the new code-plus-canvas design workflow:*

1. **Why the linear design pipeline is dead**
2. **The code-canvas loop**
	- Codex to Figma
		- Figma to Codex
3. **When to use which tool**
4. **The 5-step adoption roadmap**
5. **Total football for product teams**

---

## 1\. Why the linear design pipeline is dead

You know the process. Everyone does. It was unchanged for 15 years:

Paper sketches. Wireframes. High-fidelity mockups. Developer handoff. Engineering builds it. Design files bug tickets because the spacing is off by 4 pixels.

Every single stage in that pipeline existed for one reason: **the next stage was too expensive to start with.**

![](https://substackcdn.com/image/fetch/$s_!yTep!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F482caea9-5d26-4f56-957f-364188e5ebef_2400x2706.png)

#### Constraint 1 - High fidelity required engineering

Building something interactive used to require an engineer. So designers front-loaded cheap artifacts. Wireframes exist because prototypes cost too much. Handoff specs exist because designers could not write code.

Codex changed this. A designer can now build a functional prototype in minutes. No engineer required. No sprint ticket. No two-week wait.

#### Constraint 2 - Design files and code were separate worlds

A designer worked in Figma. An engineer worked in VS Code. Getting them in sync required handoff documents. Redline specs. Manual transcription of padding values and border radii.

The Figma MCP changed this. Design files and codebases now read from each other directly. One click. Pixel-perfect. No translation layer.

#### Constraint 3 - Feedback required the finished product

You could not test interactions in a wireframe. You could not feel tap targets in a mockup. You had to wait until engineering built it. Then you filed bugs. Then engineering fixed them. Then you filed more bugs.

Now you test interactions in code from day one. Before a single engineer touches it. The feedback loop collapsed from weeks to minutes.

#### What this looks like in practice

1. **Inside OpenAI.** The Codex design team has been shipping this way since December. Something changed when the models hit a capability threshold. Content designers are submitting PRs. PMs bring working prototypes to design reviews.
2. **Inside Figma.** Designers are working directly in staging. Monetization designers who never wrote code before are building technically complex prototypes. The phrase I keep hearing is there are no more P2s. The cutoff between ship and backlog is arbitrary now.

I covered the foundations of this shift in my [AI prototyping for PMs](https://www.news.aakashg.com/p/ai-prototyping-for-pms) guide. The difference now is that the tools on both sides have converged.

*The old pipeline was not a design process. It was a workaround for expensive tools. The tools got cheap. The pipeline died.*

---

## 2\. The code-canvas loop

The new workflow is code + canvas in a loop.

![](https://substackcdn.com/image/fetch/$s_!7j2b!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd37ba055-c948-4735-8f49-d7f1305e7e0c_2400x2763.png)

The most common question about this workflow. Will it be lossy? Will things break when you translate between tools?

Short answer: it is already **remarkably high fidelity**. And it *only gets better* with every model improvement.

### Direction 1 - Codex to Figma

You have a React app running locally. You have been building a composer system in code. You need to feel how buttons morph. How permissions prompts expand. Where tap targets land. Static mockups cannot answer these questions.

Now you want to go deep on the visual layer. Get pixel-perfect on a component. Swap icons. Test type scales.

Open the Codex desktop app. Drag the pop-out window over your running app. Type this -

> *Import my homepage and composer permissions state into a new Figma file. @figma*

![](https://substackcdn.com/image/fetch/$s_!7kmB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5fe652be-506a-4399-995a-437516c2bcbe_5840x3140.png)

Three things happen -

1. **Reads your file system.** Codex understands the React structure, components, CSS
2. **Snapshots the running interface.** The Figma MCP captures your live app state
3. **Opens it in Figma.** Click Open in Figma. You get a real, editable design file

The result is not a screenshot. Everything is responsive.

1. Every padding value matches your CSS exactly
2. Every border radius is one-to-one
3. Every shadow transfers without manual transcription
4. You can select specific component nodes instead of full screens

The newest MCP improvement. The use Figma tool now references your actual design library. Components map to your design tokens and local styles. You are not working on a facsimile. You are working on a representation built from your real [design system](https://www.news.aakashg.com/p/the-ultimate-guide-design-systems).

*The snapshot is not a copy. It is a living bridge between your code and your canvas.*

### Direction 2 - Figma to Codex

The reverse direction is just as fluid.

You have been iterating in Figma. Changed the model name in the picker. Adjusted a color. Refined spacing on a card.

Copy a link to the modified component. Paste it into Codex -

> Update my code with the change I made here \[Figma component link\]

![](https://substackcdn.com/image/fetch/$s_!C8Kj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3078b106-d7e3-43f2-b563-9cdad069a3a4_2922x1510.png)

Ed demonstrating the workflow: Figma to Codex

Codex reads the link through the MCP. Diffs against your local codebase. Generates the code change.

For non-coding designers this is the unlock. You are no longer blocked. Make changes in Figma. Your engineer pastes the link into Codex. The change propagates automatically.

One engineer recently demonstrated aligning Storybook to GitHub to Figma with AI running the loop and finding diffs between them. The maintenance overhead of keeping design systems in sync, the thing every team complains about, can now be automated.

**Three foundations that make this work**

1. **Name components well.** Good naming is table stakes for humans. Essential for agents
2. **Align design tokens with CSS tokens.** Border radius, spacing scale, color palette. One-to-one mapping
3. **Use annotations.** Read annotations into the MCP so intent travels alongside the visual output

*The handoff is dead. The loop replaced it.*

### Where AI still falls short

AI isn’t still where it needs to be for lossless movement. These areas are limited:

1. **Shader effects** do not translate to a static canvas
2. **Complex CSS transitions** cannot be fully represented in Figma yet
3. **Edge case decisions** that only exist in code because an engineer solved something that never got recorded in the design file
4. **Web-specific effects** that Figma’s canvas does not yet support

Annotations help bridge some of these gaps. But the designer’s judgment is still critical for the last mile.

The good news. Every model improvement makes this better. OpenAI’s model 5.4 produced a material jump in quality. Internal designers say it is meaningfully better at working with the Figma MCP than anything before.

If you tried this six months ago and gave up, try again. The reliability has crossed into daily-use territory.

*The tools have limits. But those limits are shrinking every month instead of staying fixed.*

---

## 3\. When to use which tool

The biggest mistake teams make with this workflow. Trying to do everything in code. Or everything in canvas.

![](https://substackcdn.com/image/fetch/$s_!J7DO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3fc23c4-a8ba-44a4-8ebf-3b7b8dde63fc_2400x2628.png)

Match the tool to the question you are trying to answer.

#### Mode 1 - Go wide on ideas

**Use the canvas.**

You can see the whole flow in front of you. Rearrange screens. Explore lateral directions. Print it out and put it on a wall and tear it down.

The canvas is still the gold standard for divergent exploration. No code tool matches the spatial freedom of dragging artboards around and seeing twenty concepts at once.

When to pick this -

1. You are exploring completely new interaction paradigms
2. You need multiplayer collaboration with the whole team
3. You want to rally people around a hero image
4. You are doing deep design system work with tokens and color tests

#### Mode 2 - Test interactions in code

**Use Codex.**

How does the button morph? How does the composer resize? Where are the tap targets? What happens at different breakpoints?

Static mocks cannot answer these questions. You need something running.

When to pick this -

1. You are testing responsive behavior across mobile, tablet, desktop
2. You need to feel how transitions work in real time
3. You want to stress-test an engineering concept by forking a branch
4. You are building a prototype that needs real data

#### Mode 3 - Ship the last mile

**Use both.**

Build interactions in code. Pop them into Figma through the MCP. Go deep on pixel-perfect details. Push changes back to code. Ship.

This is where the loop becomes the most powerful. The round-trip that used to take a sprint now takes ten minutes.

When to pick this -

1. You are polishing a nearly finished feature
2. You need to fix button animations, loading states, string changes
3. Engineering is waiting and you want to unblock them without filing a ticket
4. You want to submit a PR yourself

I covered the decision frameworks in my [Codex PM guide](https://www.news.aakashg.com/p/codex-pm-guide). The underlying principle is simple.

*The question is never which tool. It is what are you trying to learn right now.*

---

## 4\. The 5-step adoption roadmap

If you are at a traditional company, and your design team follows the linear pipeline, and your company has not have procured these tools yet, here is the path:

![](https://substackcdn.com/image/fetch/$s_!uuGR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F595e6c0d-4b7e-41a0-9ea7-e9630efe2e35_2400x2867.png)

#### Step 1 - Just start

Download the [Codex](https://www.news.aakashg.com/p/codex-pm-guide) desktop app. You do not need your company’s permission. Build something for yourself.

Real examples from inside OpenAI -

1. **A GTM team member** built an entire iOS app with zero iOS experience
2. **A comms team member** designed an interactive drag-and-drop seating plan in HTML
3. **A design lead and his wife** are building a Japan trip planner for their honeymoon

None of these people are engineers. They downloaded the app and started.

If you do not know what to build, ask yourself one question. What would I build if I could build anything? Then build it.

#### Step 2 - Get the loop working once

Install the Figma [MCP](https://www.youtube.com/watch?v=a9wO6GSAoGk) plugin from the Codex app. Open a project you already have.

The checklist -

1. Import one screen from code to Figma
2. Make one change in Figma
3. Push that change back to code
4. Verify it worked

Get the loop working once end to end. This proves the pipeline before you scale it.

The foundation matters. Name your components well. Align design tokens with CSS tokens. Clean up your Figma file structure. If your files are messy it is harder for both colleagues and agents to get up to speed.

#### Step 3 - Start with polish not process

Do not replace your existing workflow on day one. Use code for the polish stage first.

1. The button animation that never feels right
2. The loading state engineering skipped
3. The string change stuck in the sprint backlog for three weeks
4. The spacing tweak that would take 30 seconds but requires a whole ticket

This is the lowest-risk entry point. You are not changing how the team designs. You are adding a new capability where the cost of iteration was always highest.

#### Step 4 - Shift the starting point

Once comfortable, change where design begins.

Instead of paper sketches or low-fi Figma frames, open Codex and describe what you want. Show the team something real in the first meeting.

What changes -

1. Edge cases surface in the first conversation instead of the third sprint
2. [Product strategy](https://www.news.aakashg.com/p/ai-product-strategy-2026) discussions start with working software instead of static decks
3. Your wireframe gives the team more dimensionality to the problem than any mockup
4. Feedback is immediate because the thing exists

#### Step 5 - Use AI as your tutor

You will hit walls. You will not understand why a React component renders the way it does.

Ask. The AI is an infinitely patient tutor that never clocks out.

**Questions that build facility -**

1. **Start simple.** Can you build this? If it does something, ask how does that work
2. **Go deeper.** I just inherited this system. Can you explain the data architecture
3. **Find gaps.** Are there redundant systems? Look through the entire codebase
4. **Learn structure.** What is the difference between a layout page and a normal page

The people who succeed in this era are not the ones who already know how to code. They are the ones curious enough to keep asking questions.

*The roadmap is not learn to code. It is learn to be curious in a world where every question gets answered.*

---

## 5\. Total football for product teams

The natural question from above is: *If designers can code and engineers can design and PMs can prototype, do we even need separate roles?*

**Yes**. And understanding *why* is the most important takeaway.

![](https://substackcdn.com/image/fetch/$s_!Bj3m!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F243d3a51-70c2-4ca4-842a-51958ec50a6d_2400x2656.png)

*The tools are converging. **The roles are not.***

#### The three questions that define each role

1. **Engineers** ask how do we build this well
2. **Designers** ask how should someone experience this
3. **PMs** ask why should we build this at all

A designer who ships code still self-identifies as a designer. They still care about being the voice of the user. They still think about craft and flow and emotional experience. The medium changed. The mandate did not.

#### The skill layer accelerates the blurring

Inside Figma, designers are writing skills that teach AI how to design well. PMs write skills for product decision-making. Anyone can use anyone else’s skill.

1. A designer uses a PM’s skill to work through a strategic decision
2. A PM uses a designer’s skill to prototype a flow
3. An engineer uses a design skill to ship polish to production

The skill layer means you are no longer limited to a third of the picture. You can lean into adjacent domains without switching careers.

#### Why roles survive despite tool convergence

The constraint was never the role. It was the amount of time it took to become proficient in tools outside your domain. If you wanted to learn code that gated you. If you wanted to learn design that gated you.

Now those gates are open. What remains is natural inclination. Judgment. Taste.

The mental model is total football. In 1970s Holland, every player could play every position. The goalkeeper could attack. The striker could defend. But each player still had a natural spike. The team was more dangerous because everyone could cover for each other.

The phrase inside OpenAI - **prototypes, not PRDs.** PMs bring working prototypes to design reviews. They ship PRs to stress-test ideas with engineers. The artifact that aligns teams is now running software, not static documents.

The bottleneck has moved. If developers have been accelerated 10x, designers have been accelerated maybe 1.5 to 2x. Design can become the bottleneck if you are not coding yourself.

*The tools are the same across roles. The questions are different. And the questions are what define the role.*

![](https://substackcdn.com/image/fetch/$s_!8ADM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92bfdc01-4a3c-4649-8f35-dd0d521f12fd_2400x2707.png)

---

### Where to find Ed Bayes

- [LinkedIn](https://www.linkedin.com/in/edbayes/)
- [OpenAI](https://openai.com/)
- [X](https://x.com/edbayes)

### Where to find Gui Seiz

- [LinkedIn](https://www.linkedin.com/in/guiseiz/)
- [Figma](https://figma.com/)
- [X](https://x.com/guiseiz)

---

POLL

### What did you think of today’s post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

---

## Related content

**Podcasts:**

1. [Xinran Ma - Design with AI](https://youtu.be/IUvi2YHayS0?si=2OV2HvIOvJxXU4jb)
2. [Crash Course in AI Product Design](https://open.spotify.com/episode/73xPP1ISsiaFvJPxlDYOnV)
3. [Codex PM Guide with Carl Vellotti](https://podcasts.apple.com/in/podcast/8-months-of-claude-code-lessons-in-80-minutes-with/id1763555775?i=1000745034725)

**Newsletters:**

1. [AI prototyping for PMs](https://www.news.aakashg.com/p/ai-prototyping-for-pms)
2. [The PM guide to Bolt](https://www.news.aakashg.com/p/pm-guide-bolt)
3. [Codex PM guide](https://www.news.aakashg.com/p/codex-pm-guide)

---

*PS. Please subscribe on [YouTube](https://youtu.be/LR_WOmcE9WI) and follow on [Apple](https://podcasts.apple.com/in/podcast/how-to-ai-prototype-well-masterclass-from-%245-5b-founder/id1763555775?i=1000752030510) & [Spotify](https://open.spotify.com/episode/4oHNke2KJNHh7xrbiynQEI?si=0V6avOAiQ-WxS9V-VuePYw). It helps!*

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/ed-bayes-gui-seiz-podcast) on 2026-05-23T14:50:43-04:00*
