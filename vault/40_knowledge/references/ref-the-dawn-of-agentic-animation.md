---
title: "The Dawn of Agentic Animation"
source: "https://lifeinthemachine.substack.com/p/the-dawn-of-agentic-animation"
author:
  - "[[Matt Ferguson]]"
published: 2026-03-02
created: 2026-05-30
description: "How AI agents are learning to use our tools and where that leaves artists"
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [creative-studio]
ai-context: "Matt Ferguson on agentic animation: AI agents (OpenClaw, 3D-Agent) operating Blender/Maya/Houdini semi-autonomously as crew members, the parallel to early CG and to Claude Code writing most of Anthropic's code, and the human 'dither' (Harold Speed) that remains irreplaceable."
---
As an animation-obsessed kid in the early 90s I was lucky enough to tour the late great animation studio **Nelvana** while they were working on the **Beetlejuice** animated series. When I look back at the photos I took at the time, the thing that strikes me now is the complete lack of computers. All I see is paper, paint, and artists at work.

![](https://substackcdn.com/image/fetch/$s_!Zi9X!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18e96d30-3896-4012-ab2a-b134d5fabc00_2048x761.png)

Nelvana Ltd. in 1991 / Lynn Chadwick (left) Rudolf Stussi (right)

As it would happen, a decade later I got one of my first animation jobs at Nelvana and by that time there was a workstation at every artist’s desk and an ever-dwindling supply of paper. Gone were the sounds of electric pencil sharpeners rumbling through the halls.

When I think about where we are with AI and animation today, I can’t help but feel we’re at the start of a similarly disruptive change. But this time it won’t be computers replacing light tables, it will be the introduction of AI agents as members of the crew.

## Now is the Time of Agents

If you follow the fast pace of AI news, you’ve likely heard that 2026 is being called the year of the AI agent. But what does that actually mean? You can think of agents as AI systems that are no longer confined to the chat box. They can browse the web, use software, and deliver results independently. What sets them apart from the **ChatGPT** or **Claude** experience you might be familiar with is their ability to use tools and pursue goals over longer stretches of time, more autonomously.

AI agents are having a bit of a moment right now, and a lot of that has to do with **OpenClaw** (formerly known as **ClawdBot** or **MoltBot**), an open-source project by Austrian developer **Peter Steinberger**. First published in November 2025, OpenClaw is an AI assistant built on top of existing large language models that, as its website says, *“actually does things.”* It is still early and this technology is definitely not without serious risk (there are stories of agents going rogue, [deleting inboxes](https://techcrunch.com/2026/02/23/a-meta-ai-security-researcher-said-an-openclaw-agent-ran-amok-on-her-inbox/), and [harassing people online](https://www.fastcompany.com/91492228/matplotlib-scott-shambaugh-opencla-ai-agent)), but this new project has caused quite a stir with Silicon Valley types and, more importantly for our industry, it is starting to use creative tools semi-autonomously.

![](https://substackcdn.com/image/fetch/$s_!QV99!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F63c31ede-0505-4c7b-ae6a-c9dfecd54342_1093x519.png)

OpenClaw from Peter Steinberger

## Agentic Animation

Whereas AI animation produced through video generation models like **Sora**, **Veo**, or **Seedance** can be hard to control and nearly impossible to iterate upon, AI agents that can manipulate animation software is a promise that could seriously disrupt current workflows. In the same way that a capable humanoid robot can easily fit into a factory floor designed for people, a digital system that operates the same software we use every day, has a better chance at sliding into existing animation and VFX pipelines.

**Enter OpenClaw for animation.**

**Riley Brown** is an AI **YouTuber** and the co-founder of **[Vibecode.dev](https://www.linkedin.com/company/vibecodeapp/)**. A couple of his recent videos show what might be possible when agents meet animation. Recently he used his OpenClaw assistant to operate **Blender** using only natural language commands. His first experiment involved modifying an existing model he bought online (you can watch that [here](https://youtu.be/dxlyCPGCvy8?si=9mtx1ZKjD42mOthK)). But what really blew my socks off was his next experiment. He instructed his OpenClaw to model a simple character in Blender based on a single image and then animate it (albeit in a super rudimentary way).

![](https://www.youtube.com/watch?v=uhVEIJXXvU4)

And now the agentically animated Billy Bob lives [here](https://billybob-eta.vercel.app/).

Riley Brown isn’t the only one. Every day there are people exploring the limits of these agents including their skills at modeling, animating, and even editing. Currently there are thousands of community-built skills for OpenClaw including ones dedicated to **Blender**, **Unreal**, and **Houdini** and they are growing every day. There are also animation-specific agents already emerging including a product called **[3D-Agent](https://3d-agent.com/)** that claims to be a simple way to connect natural language commands to Blender using **Claude**.

## The Early Days

Obviously, the results from Brown’s experiment are nothing that will upend the animation industry today. It seems more like a tutorial you might give to an elementary school class learning Blender for the first time. Most professionals would look at the video and rightly surmise that they could do the same thing faster and orders of magnitude better by just controlling the tools themselves. That is 100% true.

But I can’t help but think back to some of the early experiments with CG animation in the 70s and 80s. **Ed Catmull** ’s famous CGI hand project early in his career couldn’t hold a candle to the way **Milt Kahl** was animating hands with just paper and a pencil.

![](https://www.youtube.com/watch?v=wdedV81UQ5k)

![Milt Kahl Hands](https://substackcdn.com/image/fetch/$s_!R3NJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc86ef4a0-eb93-4771-a0c8-f2a939114b6a_1200x905.jpeg)

Merlin’s hands drawn by Milt Kahl for Disney ’s The Sword in the Stone (1963)

Not only was the simpler, more human pencil technology superior to the expensive and complicated computer animation at the time, it was nearly impossible to imagine the kind of artistic expression this technical exercise would allow for by the time Catmull co-founded **Pixar** 14 years later.

This is, of course, far from a perfect analogy. Both the pencil and CG programs are tools wielded by people, whereas we’re discussing a piece of software being used by another piece of software. But while OpenClaw is currently operating Blender in a fairly crude way, the important thing to note is that a semi-autonomous intelligent computer system is operating it at all. This feels like a tipping point.

## What’s Next

These experiments will only accelerate. As the underlying AI models improve, people like Riley Brown and others will push further, and at some point this kind of workflow will inevitably find its way into productions. Perhaps it will start with first-pass modeling on simple assets, layout blocking, or accessing motion libraries.

There’s already a parallel track to this AI agent workflow. Tools like **[Cascadeur](https://cascadeur.com/)**, **[Cartwheel](https://lifeinthemachine.substack.com/p/creating-an-ai-tool-with-animators)**, and **[Maya’s MotionMaker](https://lifeinthemachine.substack.com/p/inside-mayas-motionmaker)** synthesize motion data that can be imported into traditional CG tools for further refinement, and **[Animaj](https://lifeinthemachine.substack.com/p/pocoyos-ai-era)** (the studio behind current incarnations of **Pocoyo** and **Maya the Bee**) has a proprietary AI process for translating storyboard drawings into character poses in **Maya**. The approaches differ, but the end result is the same: AI working inside the software we already use.

![Animaj's Sketch-to-Pose AI Model](https://substackcdn.com/image/fetch/$s_!qofJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04088114-e8fa-402b-99a1-cc8c2770c0fd_1920x1080.webp)

Animaj ’s AI Sketch-to-Pose tool for Pocoyo

## Our Possible Future

Now that AI agents have demonstrated they can manipulate the tools of animation in autonomous ways, the question becomes how good will they get? It might be helpful to think about it this way: **How much of the work you do as a modeler, rigger, or animator is a learned skill, and how much of it is that special human sauce that is the combination of taste, lived experience, and individual performance?** I honestly don’t know the answer to that question, but my instinct is that a non-zero percent of the work of most animation artists can be taught to a sufficiently intelligent person (or system). That’s a hard pill to swallow, but my gut tells me it’s true.

We just need to look at what is happening with coding. Creating software can be a highly creative endeavor and yet with coding agents like **Claude Code**, much of the actual coding can now be done autonomously even as it continues to be directed by an engineer with real vision and taste. In January of this year, a principal engineer at **Google** said the tool [reproduced a year of her architectural work in one hour](https://ppc.land/google-engineers-claude-code-confession-rattles-engineering-teams/), and at **Anthropic** itself, it is estimated that [70%-90% of the code being written at the company is currently being written by](https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/) **[Claude](https://fortune.com/2026/01/29/100-percent-of-code-at-anthropic-and-openai-is-now-ai-written-boris-cherny-roon/)**.

What will happen when you have an AI system that can learn the fundamentals of modeling and rigging, internalize the principles of animation, and act on that knowledge? At the very least you would have a system that can get part of the way there and produce work that exists in software that allows for refinement, iteration, and human artistry.

There’s no denying that it’s scary for those of us working in the field. A world in which AI agents can do some of the work is a world in which crews might start to seriously shrink. AI optimists will tell you that it could lead to an explosion of content being created, but there is also reason to believe it will simply lead to many fewer jobs.

Which makes the question of what only humans can bring to this work more important than ever.

## The Importance of Dither

In 1913, **Harold Speed** wrote the fantastic book **[The Practice and Science of Drawing](https://www.goodreads.com/book/show/1514213.The_Practice_and_Science_of_Drawing)**. More than a century ago, Speed expressed the need for human imperfection in art, and it feels more relevant than ever today:

> *“There must be enough play between the vital parts to allow of some movement; “dither” is, I believe, the Scotch word for it. The piston must be allowed some play in the opening of the cylinder through which it passes, or it will not be able to move and show any life. And the axles of the wheels in their sockets, and, in fact, all parts of the machine where life and movement are to occur, must have this play, this “dither.” It has always seemed to me that the accurately fitting engine was like a good academic drawing, in a way a perfect piece of workmanship, but lifeless. Imperfectly perfect, because there was no room left for the play of life.”*

Looking back at those old **Nelvana** photos I see the dither everywhere. Yes, it’s in the pencils and paint, but more importantly it’s in the way the artists worked side by side, each one’s imperfections bouncing off each other to create something unique and human. If AI agents do, in fact, start joining the crew, it will be more important than ever to find room for the “play of life” as we create together.

*Seeya next time,*

**Matt Ferg.**

---
*Clipped from [substack.com](https://lifeinthemachine.substack.com/p/the-dawn-of-agentic-animation) on 2026-05-30T15:20:56-04:00*
