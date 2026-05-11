---
title: "How I built LennyRPG"
source: "https://www.lennysnewsletter.com/p/how-i-built-lennyrpg"
author:
  - "[[Lenny Rachitsky]]"
  - "Ben Shih"
published: 2026-03-17
created: 2026-05-11
description: "Turning 300+ episode transcripts into a fun, playable game with AI"
tags:
  - "source/web-clip"
  - "lennys-newsletter"
  - "ai-product-building"
  - "pixel-art"
type: reference
status: processed
domain: [product-management, creative-studio]
ai-context: "Ben Shih's guest post on Lenny's Newsletter walking through building LennyRPG (a Pokémon-style pixel-art game from 300+ podcast transcripts) with AI — PRD → POC → polish flow, useful as a non-technical AI build case study."
---
*👋 Each week, I answer reader questions about building product, driving growth, and accelerating your career. For more: [Lenny’s Podcast](https://www.lennysnewsletter.com/podcast) | [Lennybot](https://www.lennybot.com/) | [How I AI](https://www.youtube.com/@howiaipodcast) | My favorite [AI/PM courses](https://maven.com/lenny), [public speaking course](https://ultraspeaking.com/lennyslist?via=lenny), and [interview prep copilot](https://www.benerez.com/copilot/lenny)*

*P.S. Get a full free year of Lovable, Manus, Replit, Gamma, n8n, Canva, ElevenLabs, Amp, Factory, Devin, Bolt, Wispr Flow, Linear, PostHog, Framer, Railway, Granola, Warp, Perplexity, Magic Patterns, Mobbin, ChatPRD, and Stripe Atlas [by becoming an Insider subscriber](https://www.lennysnewsletter.com/subscribe?plan=founding). [Yes, this is for real](https://www.lennysnewsletter.com/p/productpass).*

---

A few months ago, I shared all of my podcast transcripts on socials on a whim, and holy sh\*t, y’all found such incredibly creative ways to use this data: [parenting wisdom rooted in PM advice](https://www.tinystakeholders.com/), [user research scripts](https://lenny-listens.vercel.app/), [antimemes](https://lenny.antimeme.co/), [an infographic for every episode](https://lennygallery.manus.space/), [a “Learn from Lenny” Twitter bot](https://x.com/learnfromlenny), and at least 50 other amazing projects.

But my favorite project of all was by [Ben Shih](https://www.benshih.design/), a non-technical product designer at Miro, who created [LennyRPG](https://www.lennyrpg.fun/). I asked Ben to share the step-by-step journey behind this wildly fun, video-game-inspired project—how he built it and what he learned.

**To let a thousand more flowers bloom, today I’m releasing my entire newsletter archive (and my podcast transcripts) in AI-friendly Markdown files.** **Also, an MCP server and a handy GitHub repo.** Paid subscribers get all of the data (some 350 posts and 300 transcripts); free subscribers can access a subset. Grab the data here: **[LennysData.com](https://www.lennysdata.com/)**.

I don’t think anyone’s ever done anything like this before, and I’m excited to give you this excuse to start playing with the latest and greatest AI tools.

**Here’s my challenge to you:** **build something, and let me know about it.** I’ll pick my favorite and give you a free 1-year subscription to the newsletter. Just post a link to your project in the comments below. If you’ve already built something, slurp in this new data and submit it, too. I’ll pick a winner on April 15th. **[Here’s the data](https://www.lennysdata.com/)**. Let’s go.

*Ben is a designer and product builder who enjoys creating small, fun, and thoughtful products that make the world a little better. He’s currently a growth designer at Miro. You can explore more of his work on his [website](http://benshih.design/) or [LinkedIn](https://www.linkedin.com/in/hbshih/).*

*Also, a big thank-you to [Tal Raviv](https://www.talraviv.co/), [Claire Vo](https://x.com/clairevo), and [Este Lopez](https://www.linkedin.com/in/estelopez/) for helping me beta-test and improve LennysData.com (which I proudly “agentically engineered” with Codex and Claude Code 👌).*

---

![](https://substackcdn.com/image/fetch/$s_!ZbLz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa9a5c1d4-371d-4bde-9429-25077e840ebc_1456x970.png)

A couple months back, Lenny dropped something special. He made transcripts from all his [more than 300 podcast episodes](https://www.linkedin.com/posts/lennyrachitsky_here-are-the-full-transcripts-from-all-320-activity-7417011928159629313-am-q?utm_source=share&utm_medium=member_desktop&rcm=ACoAABgR8zUBAFHabLdChWxyjRl3QjO7YIzQFF0) structured and publicly available. As someone who’s listened to the podcast for years, I couldn’t stop thinking about what I could actually build with this.

![](https://substackcdn.com/image/fetch/$s_!W4Mo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F272590a2-4b6a-41e2-b1f8-9a1831d38f8a_1456x970.png)

Lenny’s original LinkedIn post

[Brian Balfour](https://blog.brianbalfour.com/p/the-next-great-distribution-shift) talks a lot about building at the right moment: if you get the timing right, you’ll find a real window of opportunity. This felt like one of those windows.

The first idea that popped into my mind was to make a Lenny interview app where you can practice job interviews with Lenny’s Podcast guests. However, the more I thought about that idea, the less excited I felt. Interview practice tools by nature feel stressful, and that’s the last type of product I wanted to create. I wanted to make something fun.

What if I turned Lenny’s Podcast into a small role-playing game (RPG)? A game where you explore a pixel world, meet guests from Lenny’s Podcast, compete with them to test your product knowledge, and even capture them like Pokémon when you win. That’s how **LennyRPG** was born.

![Pixel-art game interface titled ‘LennyRPG: Catch ’Em All!’ showing a colorful town map with trees, grass, and buildings and a small character in the center, with a left panel displaying player stats (Level 1, 0/200 XP, 100/100 HP, captured 0/275), a ‘How to Play!’ box explaining movement, battling quests, and pressing C to view collection, right-side buttons for Collection, Leaderboard, Share Stats.](https://substackcdn.com/image/fetch/$s_!X5p7!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d7380ac-4cbf-4c7e-861f-e0b4d0209d58_1400x929.png)

Try it out at https://www.lennyrpg.fun/

## Here’s how I built it

When I build apps with AI, I usually follow a very simple flow:

![Workflow: Define the core idea → Create PRD (rough scope, idea, tech stack) → Create POC (proof of concept) → Add remaining features → Polish → Ship.](https://substackcdn.com/image/fetch/$s_!Tbe4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6a40f32-26ca-4244-9f7a-c0f3f34a188e_1024x296.png)

My workflow of using AI to create products

1. **Define the core idea:** I start by clarifying what the app is. For visually heavy products, I sketch it out so the AI can better understand the requirements.
2. **Create a product requirement document (PRD):** I turn the core idea into a proper PRD with the AI. This becomes the single source of truth for the build.
3. **Create a proof of concept:** I use the PRD to plan implementation and build the core functionalities first.
4. **Add remaining features:** I finish the end-to-end flow, such as connecting the database and building out settings, profile pages, and other non-core features.
5. **Polish:** I go through the app end-to-end, fix UX/UI details, and do final code reviews to make sure everything is stable.
6. **Ship it:** I deploy, get feedback, and get it out into the world.

The process isn’t that different from before the AI era. But now I really make sure that I spend enough time on the first two steps to ensure that the AI gets all the context of what I want. In my experience, nailing the core idea and PRD determines 80% of how smooth the rest of the build will be.

Here are the main tools and technologies I used throughout the build:

- **Ideation and planning:** Miro, ChatGPT
- **Coding:** Claude Code, Codex, Cursor
- **Image generation:** GPT Image Gen (gpt-image-1.5)
- **Quiz generation:** GPT-4o
- **Game engine:** Phaser 3
- **Database:** Supabase
- **Deployment:** Vercel

Now let’s walk through how I used this process to build my RPG game. I’ll share the exact prompts, tools, and decisions at each step so you can apply the same workflow to your own projects.

## 1\. Define the core idea

The core idea was simple: turn Lenny’s Podcast into a Pokémon-style RPG where players encounter podcast guests in the wild and battle them through product questions.

For many apps, text and a clear idea are enough to get started with. But for highly visual products like this game, spending some time on visualization can help you get a solid sense of how you want the game to look and feel. That makes a big difference later on when you ask the AI to build the UI and interactions.

For this game, I dropped a few Pokémon screenshots into a Miro board and put together a rough concept directly on the board. Nothing fancy, mostly text and boxes on top of screenshots. But it was enough to show how I imagined the map, the battle screen, and how the characters might look.

![](https://substackcdn.com/image/fetch/$s_!WjIr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa28b1c59-36e2-4afd-9334-f4c46e274bad_1153x528.png)

The initial visual concepts I sent to the AI

The goal was not to design the game exactly but to give the AI something concrete to read and reason about. Once the core idea was roughly visualized, the AI could read the visuals alongside the text, which led to a much stronger PRD in the next step.

### Creating a sample set of avatars

As part of the visualization, I also created a few test avatars with ChatGPT to validate the content generation workflow. This helped me understand the prompt engineering needed for consistent pixel art style avatars.

The process was very simple. I dragged in images of the RPG characters I wanted the style to match, then added Lenny’s photo into ChatGPT to create a similar one.

![A 2D pixel art RPG character sheet on a yellow background, showing a bearded man with short dark brown hair wearing a blue shirt, brown pants, and a brown belt, depicted from front, back, left, and right views with a sword sheathed at his side in the profile views. A small profile photo and the text ‘turn lenny into a RPG character. 2D version.’ appear above, with the caption ‘Image created — Pixel art RPG character views.’ below.](https://substackcdn.com/image/fetch/$s_!ZBni!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F15b1eb4a-ad8c-4685-9615-98b104e261ad_784x771.png)

How the main character gets created

Once I was happy with it, I asked ChatGPT to describe the tone, style, and design in detail so that I could reuse that as a prompt later.

Prompt I used:

> `Study and think through the styling, design, colors, proportions, and overall look in detail, then return only a polished image-generation prompt that will create a similar front-facing character based on the provided person’s photo, with a transparent background and no additional elements.`

![](https://substackcdn.com/image/fetch/$s_!7_eb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39e153f0-4b0e-4301-8a7f-088e70606492_1442x1426.png)

ChatGPT generated a reusable prompt template based on the avatar style I liked.

## 2\. Create a PRD (in a lazy way)

In my experience, the PRD is the most important document if you want the AI to execute your vision correctly. As a PRD does well with human teammates, it gives the AI the base understanding of your app’s goal, problem statement, and core idea. Whenever the AI hits a wall or the context window runs out, you can refer it back to the PRD to realign. No matter what stage you’re at, the PRD makes sure everything the AI generates stays true to what you’re actually trying to build. That’s why I always invest time here.

That said, writing PRDs can sometimes drive you crazy. **So instead of writing the PRD myself from scratch, I let the AI interview me.** I pasted my core idea along with the visuals into ChatGPT and then asked it to ask me questions so that I could answer them one by one.

Prompt I used:

> `Ask me questions to help you put together a brief PRD for the following web game: I want to create a mini game that takes all the podcast episodes from Lenny’s Podcast, generates questions from each episode, and make it like a Pokémon RPG game, with similar visuals. What I am expecting is, for example, you found Elena in the wild, and you can compete with Elena on product questions, you get 5 questions, and you lose HP [hit points] when you lose the answer etc. We can randomly pick 50 guests from the podcast and get challenged. The entire theme/design of the game needs to be very Pokémon RPG style in the old day.`

![](https://substackcdn.com/image/fetch/$s_!2GJ8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc4ebf208-ef1f-40e7-a6d5-39338c0d34be_1600x1344.png)

ChatGPT generated a set of clarifying questions grouped by category to help lock the scope and plan.

With the prompt, ChatGPT came back with 17 questions. I moved them into Miro to visualize them better and used [Wispr Flow](https://wisprflow.ai/) to quickly dictate my answers verbally.

Answering these questions also forced me to think through gaps and assumptions in my idea, while giving the AI much better context than a one-page description ever could.

Once I answered all of the questions the AI had for me, I chained the answers together with all the available artifacts in Miro and asked the AI to generate a comprehensive PRD.

![Digital workspace showing screenshots of a pixel-art game called Productmon on the left — a town scene and a battle UI with a character named ‘Elena Varro’ and a question prompt — and on the right a structured product requirements document with sections like Overview, Problem Statement, Goals & Objectives, Target Users, Core Features, and an Answers section about game scope, question design, and rewards.](https://substackcdn.com/image/fetch/$s_!MA0A!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f4da9e2-59cd-4a1b-ae39-8895775f46e2_1400x1206.png)

PRD generated with all connected artifacts

## 3\. Create a proof of concept

With the PRD in place, I moved it over to Cursor as a Markdown file so I could start working on the POC.

![](https://substackcdn.com/image/fetch/$s_!ZD3T!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5387094c-fa8c-4828-9312-e9324f086da0_1369x878.png)

Created the PRD as a Markdown file in Cursor to start development

For the actual development, my setup uses three tools: Claude Code, Codex, and Cursor’s Composer.

I treat Claude Code as my lead engineer. It helps draft the implementation plan, think through architecture, and reason about product and design constraints. I’ve also found it to be great at searching for solutions and open source libraries. Codex is mainly for executing tasks from the implementation plan. It’s very good at following instructions accurately, and comes with a more generous token limit. Composer is mostly for smaller tasks like formatting documents, JSON files, or writing simple scripts.

Using the PRD as input, I first asked Claude Code to search for any open source projects that could help me move faster. This is something I always do early on. Very often, people have already built something similar and made it open source on GitHub, which can help you set things up much faster.

![](https://substackcdn.com/image/fetch/$s_!RfC-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fc1059c-0a1f-4486-a8d4-025896ed24a4_1037x276.png)

Claude Code can help search for open source libraries

One of the first libraries I landed on was [RPG-JS](https://github.com/RSamaium/RPG-JS?tab=readme-ov-file). Thanks to the library, it took me around five minutes to get something running. I was able to quickly build out the essential game flow. The overworld map handled basic player movement, encounter zones, and simple UI elements.

![](https://substackcdn.com/image/fetch/$s_!wmSD!,w_1456,c_limit,f_webp,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5056817c-52b9-4fd2-bd36-00560365c164_1536x1080.gif)

POC with RPG-JS library

But very quickly, I started hitting challenges.

**Challenge #1: Hitting the limits of RPG-JS and pivoting**

After a few iterations, it became clear that RPG-JS was not the right foundation. The framework is heavily designed around inventory systems and weapon-based combat. That worked against me, since my battles were quiz-based and logic-driven. The more I tried to bend it, the harder it became for the AI to reason about the system cleanly.

After talking it through with Claude Code, I decided to stop forcing it and pivot. The new framework that I decided to use is [Phaser](https://phaser.io/), a 2D game framework used for making HTML5 games for desktop and mobile.

**Challenge #2: Getting the map running in Phaser**

After switching to Phaser, things became much more flexible in terms of scenes, maps, and game logic. However, because everything is more customizable, even setting up a basic map took a lot more work.

Fortunately, using Claude Code, I found a [Medium article](https://medium.com/p/1c34f601cc43/edit#:~:text=https%3A//medium.com/%40michaelwesthadley/modular%2Dgame%2Dworlds%2Din%2Dphaser%2D3%2Dtilemaps%2D1%2D958fc7e6bbd6) from a while ago that included an open source, reusable map template. That helped me speed things up significantly and get back to focusing on the game itself.

![](https://substackcdn.com/image/fetch/$s_!irKn!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F75f36efd-a589-4206-a5d2-cb94386a5329_1600x1073.png)

The first version of the map running in Phaser with the open source template

**Challenge #3: Polishing the details in Phaser**

Phaser is a powerful but complex library with a lot of different features. Claude Code took some time to actually understand how it works, and I had to go through many iterations to get the details right. Things like importing the right fonts, making sure UI elements were positioned correctly, and editing everything within Phaser’s open canvas all required a lot of back and forth.

One tip for complicated tasks like this is to ask Claude Code to create a simple Markdown file to log everything it tries, so it can keep referring back and updating what works and what doesn’t.

![](https://substackcdn.com/image/fetch/$s_!gkn0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43799691-cd17-470a-bb32-8c21ab171a6b_1194x798.png)

Claude Code’s Markdown log tracking each attempt at fixing fonts and UI rendering

This helps a lot for Claude Code and AI in general to understand the codebase and framework better. It’s especially useful as your codebase grows larger, where even small things like font changes can become difficult for an AI to handle.

![](https://substackcdn.com/image/fetch/$s_!QIHV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F56ddb5cf-3f51-40ce-b4b6-a5b8df0074d7_1520x514.png)

Before and after polishing the UI details in Phaser

After working through all these challenges, the game finally reached a playable state. The starting screen, map, and battle screen were all working end-to-end.

![](https://substackcdn.com/image/fetch/$s_!vnKi!,w_1456,c_limit,f_webp,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F09d48ec2-5656-43b8-900a-eab716e7e17a_1084x720.gif)

POC with everything from the start screen to the battle screen working end-to-end

Once the POC was ready, I shared it internally in the office to get a few people to try it out. At this stage, I wasn’t looking for polished feedback or detailed bug reports. I mostly wanted to see how people reacted when they opened the game for the first time. Did they immediately understand what to do? Did the core loop make sense? Most importantly—did it feel fun, or did it feel like work?

This kind of lightweight, informal testing gave me confidence that the core idea worked, and that it was worth investing more time to turn the POC into something more complete.

![A couple of people looking at the laptop with LennyRPG running.](https://substackcdn.com/image/fetch/$s_!UGBp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe3158678-d826-46a9-91d6-92baf8c280ea_1091x1082.png)

Testing the game in the office with Yuliya, our Head of Growth, and Mehdi, our engineer

## 4\. Add remaining features

Once I got the app running correctly with the basics and got great feedback from folks in the office, I started following the plan to scale my POC into a proper game.

But the process was less straightforward than expected, mainly because there were a lot of podcast episodes to process. Scaling from a working POC to a full game turned out to be mostly about figuring out how to handle things systematically instead of manually.

Here are the main tools and decisions that helped me get there:

### Processing 300+ transcripts systematically

The transcript file provided by Lenny contained only raw text. To make it usable in the game, I first had to enrich the data with things like episode title, episode URL, and podcast cover.

To do this, I pulled in the podcast [RSS feed](https://api.substack.com/feed/podcast/10845/private/732360bb-6d5c-458f-8552-38a5354d6f67.rss) with Cursor’s Composer and used it to attach the missing metadata to each transcript. This gave me a much more complete dataset that the game could actually use.

![](https://substackcdn.com/image/fetch/$s_!8qAh!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cc43380-46be-44b5-944e-a91947dc99fe_1600x968.png)

Using Cursor’s Composer to write a simple script that pulls in metadata from the Lenny’s Podcast RSS feed

Then, using Claude Code, **I asked it to create a simple CLI tool that could systematically generate quiz questions** for each episode using the OpenAI API. Instead of doing this episode by episode, the tool processed everything in one go.

This step was as simple as typing in a prompt: *“Create a CLI command tool that creates a simple way to read through all the transcripts in /transcript folder one by one, and for each, generate 5 questions following the requirements and JSON format: {Your requirements and JSON format}”*

It took around 20 minutes to finish, and the output was a structured JSON file that I could plug directly into the game.

![](https://substackcdn.com/image/fetch/$s_!qwFE!,w_1456,c_limit,f_webp,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2a7e774-d008-40d7-8c13-5379c2dbf63d_1728x1080.gif)

Claude Code wrote a CLI tool that automatically scans through the transcripts from each episode and extracts the questions

### The potential nightmare of creating 250+ RPG avatars

One of the hardest parts of building the game was creating over 250 RPG avatars in a consistent way. Each avatar needed a photo of the guest as input. Doing this manually by searching and downloading guest photos one by one would have taken forever.

Fortunately, every Lenny’s episode already includes an episode cover that contains the guest’s avatar. For this, I triggered Cursor’s Composer to pull RSS feed again to pull the image URLs, downloaded them locally, and used those as inputs for avatar generation.

![](https://substackcdn.com/image/fetch/$s_!7A8P!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e492fc8-b8dc-4787-bbb1-9c290accd3a4_1342x786.png)

Claude Code downloaded all these episode covers for me automatically.

That solved the sourcing problem but introduced another one: How do I make sure every avatar looks consistent in quality and style?

This is where I used OpenAI Playground to repeatedly test and refine my prompt, as well as testing which models work the best for the task. I kept adjusting it until every generated avatar followed the same style and looked like it belonged to the same game.

![Dark-themed OpenAI Playground ‘Images’ screen showing three small pixel art character sprites (two bearded men in white shirts and one younger character in blue shirt and brown pants) above a prompt box instructing the model to create a high-quality 2D pixel art RPG character sprite from a photo while ignoring text and logos, captioned ‘OpenAI Playground for testing prompts.](https://substackcdn.com/image/fetch/$s_!W0Rw!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d6dc033-7b48-43e8-9c27-018bc081fe65_1400x802.png)

OpenAI Playground for testing prompts

Once the prompt was stable, I used Claude Code again to write another CLI tool that could systematically generate all the RPG avatars from the episode covers. That turned a very painful manual task into a one-click process.

![](https://substackcdn.com/image/fetch/$s_!OXtN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde9e4c77-740c-40aa-90c6-1cc2a47bcc0c_1280x800.gif)

Claude Code wrote another CLI tool that generates avatars from episode covers

And of course, for each output, I had to check one by one to make sure the sizes and styling were similar and matched how the guests looked in the podcast cover. This was one of the most interesting steps because there were a few fun edge cases. For example, I didn’t know Adam Grenier really has rabbit ears on top of his profile image in the original podcast cover—I almost deleted them. Or there are episodes with two people in the cover image, like Jake Knapp and John Zeratsky’s episode, so I had to tell AI to generate a single separate image for each person.

![](https://substackcdn.com/image/fetch/$s_!dfS6!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F592f5dfc-fb8b-4f44-b73b-27b339a7e928_1100x1064.png)

Some fun edge cases: Adam Grenier’s rabbit ears carried over into his avatar, and episodes with two guests like Jake Knapp and John Zeratsky needed separate avatars.

![Dark blue background with the title ‘LennyRPG — Test your product knowledge with industry leaders’ above a large grid of colorful pixel art avatars in rows and columns, plus a larger bearded male avatar at top left, captioned ‘Results from creating all the avatars…](https://substackcdn.com/image/fetch/$s_!imUX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe18270be-879f-4d11-a1ec-9e492163f529_1191x1199.png)

Results from creating all the avatars

### Claude Code’s magic with background music

Audio is a huge part of any game. Many successful gamified apps, like Duolingo, invest a lot of effort in sound design because it makes everything feel more alive.

At the same time, searching for the right background music and wiring it into the game usually takes a lot of time. So I went to Claude Code and simply said: *“Search for me background music for each phase, with mute control.”*

To my surprise, it was able to find [OpenGameArt.org](http://opengameart.org/), an open source audio library for games, and wire it into the game correctly. When I wrote the prompt, I actually just wanted to add background music for when players are on the map, but it automatically added music for battle screens, victory screens, and defeat screens as well. I still had to adjust the timing and volume, but most of the heavy lifting was done automatically. That part genuinely felt like magic.

![Terminal-style interface showing commands that use web search and download tools to fetch an 8-bit JRPG soundtrack zip, list track names like ‘Opening,’ ‘Prelude,’ ‘Sanctuary,’ and copy selected Pokémon-style royalty-free music files into a game directory, with a note that ‘Claude Code automatically fetched, downloaded, and connected the music to the game.’](https://substackcdn.com/image/fetch/$s_!8dDB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffd7a8b2e-7753-492b-b276-e78344e88d2f_864x855.png)

Claude Code automatically fetched, downloaded, and connected the music to the game: crazy.

### Defining the gaming mechanics

Defining the gaming mechanics was the most interesting part of the process, as I wanted the game to be fun and low-stress but still competitive enough that people felt progression and stakes. I’ve studied game theory in the past, but for this project, most of it came down to common sense, play testing, and iteration.

I started with a very simple rule set: Each opponent has three questions. Every correct answer gives XP (experience points). If you answer all three correctly, that counts as a perfect kill.

**To keep things interesting, I added small variations.** Occasionally, one of the three questions becomes a bonus question, which gives extra XP and a small HP boost. This introduces a bit of randomness without breaking balance.

Stage progression is based on XP thresholds. Once you reach the required XP, a new map unlocks with a new batch of guests. Defeated opponents disappear and get added to your collection, so you can’t farm the same ones repeatedly.

I worked through most of this logic on my own first and then verified with the AI to make sure there were no obvious bugs or edge cases. The AI sanity-checked numbers and flows, but the final calls on balance, pacing, and stress level were all manual.

![Conversation in ChatGPT discussing with AI about the details of the game rules.](https://substackcdn.com/image/fetch/$s_!E7sL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71cb3e1f-d24c-40d9-94d2-7b4e3753207b_1400x817.png)

Me thinking about the game rules with ChatGPT

### Connecting Supabase using MCP (leaderboard)

The last step of the game is the leaderboard. It is the competition aspect of the game, where people can see their ranking and compete with each other.

I knew I had to set up a database for this, so I started by setting up Supabase MCP in Claude Code. That means instead of manually setting up tables, APIs, and connections, all I had to do was describe to Claude Code that I wanted a leaderboard synced with Supabase.

Once I did that, it triggered Supabase MCP, which called tools like create\_project and apply\_migration to set up the project and tables automatically, including the database structure and the connection between the game and Supabase. This made the whole process much faster and removed a lot of setup work that would normally take much longer.

The result was a working leaderboard that synced player progress in real time, without my having to touch much backend code at all.

![Dark code editor or terminal view showing a message about connecting to Supabase MCP and a TODO checklist to set up a global leaderboard safely, including steps like creating a leaderboard table with RLS, configuring Supabase client, and verifying .env safety, with commands such as ‘mcp__supabase__get_project_url’ and the caption ‘How Supabase MCP magically set up everything.’](https://substackcdn.com/image/fetch/$s_!_DYU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2ab6c763-fbe6-4f94-98fc-1c99e5958e0d_1128x889.png)

How Supabase MCP magically set up everything

![Pixel art ‘Hall of Fame’ leaderboard panel with yellow border listing player names like GRIBS, BAPTISTE, RK, and others alongside their levels and XP (for example GRIBS level 7 with 3540 XP), navigation buttons 1–5 and a Refresh button at the bottom, over a faint game background that says ‘Prove your worth, guests.’](https://substackcdn.com/image/fetch/$s_!bIG3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fa80d27-968e-4e2a-8ffe-5e26c84817cc_1400x850.png)

The leaderboard in the game

## 5\. Polish

Before shipping, I focused on final polish to make sure the app was stable, usable, and presentable enough for public launch. At this stage, the core gameplay was already working, so the goal was not to add new features but to reduce friction and obvious issues.

### QA check with Claude Skills

For this step, I downloaded the review skill from the Claude Code [Awesome Skills marketplace](https://github.com/ComposioHQ/awesome-claude-skills?tab=readme-ov-file) and used it to review the entire codebase comprehensively.

This was especially helpful for catching things I would normally miss, such as state issues between scenes, missing error handling, and small logic bugs that only show up after multiple rounds of gameplay. I did not blindly accept everything it suggested, but it gave me a solid checklist to go through before shipping.

![Dark-themed Claude Code interface showing a command palette with ‘/review’ for AI-powered code review and ‘/security-review’ to run a security review of pending changes, captioned ‘Review agent in Claude Code.’](https://substackcdn.com/image/fetch/$s_!l3Xo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F718e5cce-5a23-4620-b617-7b54d2e5fb60_1400x151.png)

Review skill in Claude Code

### UI polish

I went through the game end-to-end and logged all UI and UX inconsistencies in a Markdown file—things like spacing issues, text overflow, unclear labels, alignment problems, and visual hierarchy issues.

Once everything was written down, I let AI pick up the list one by one and fix them. This worked surprisingly well, especially when the issues were clearly described. It also made the process much more systematic compared with fixing things ad hoc while clicking around the app.

### SEO

For SEO, I used Claude Code to help figure out the basics: page title, meta description, social preview, and basic indexing setup.

Since this was a game and not a content-heavy site, I did not go deep into SEO optimization. The main goal was to make sure the site was indexable, shareable, and looked good when people posted it on social media.

![Code editor diff view for index.html in a LennyRPG project showing added HTML meta tags for title, description, keywords, canonical URL, and Open Graph/Twitter card fields promoting ‘LennyRPG — Test Your Product Knowledge | Lenny Rachitsky’s Podcast Game,’ with a note that all tags were added automatically by Claude Code.](https://substackcdn.com/image/fetch/$s_!7eoF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95070d48-4d77-4aa5-b518-7c82baa685e3_1400x998.png)

All these tags were added by Claude Code automatically.

## 6\. Ship it

Once the game was deployed smoothly on Vercel, I reached out to Lenny in the community Slack to get a quick sanity check. I honestly wasn’t even expecting a direct reply given how busy he is—but to my surprise, I got a very kind and encouraging response from him.

That was the nudge I needed to just ship it.

![](https://substackcdn.com/image/fetch/$s_!aYm1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9315cfa6-c525-4a29-92ef-c1d38be11c87_1600x609.png)

My initial conversation with Lenny

Seeing the game shared publicly, and then getting an extra boost of visibility when Lenny shared it on X, was surreal. The responses that followed—from people playing the game to sharing screenshots and reacting to the idea—were way beyond what I expected for a small side project built in a few hours.  
  
It was one of those moments that reminded me why I like building products. 💛

## A few lessons learned from building

I built LennyRPG originally because I wanted to make something fun to build and fun to play. But along the way, I also picked up some useful lessons for my future AI projects—and maybe yours too.

### 1\. Get creative with the tools you have

With AI, building is no longer the bottleneck. Almost anyone can spin up an app now. That’s where creativity starts to matter more than execution. Instead of asking, “What’s possible?” I’ve found it much more interesting to ask questions like “What would be fun?” “What feels a bit ridiculous?” or “What would I never attempt without AI?”

I’ve wanted to build a game for a long time, but the time and technical cost always felt too heavy. AI didn’t just speed things up; it lowered the threshold enough that this idea finally felt worth trying.

### 2\. When you’re in doubt, trust the AI

A pattern I keep coming back to is using AI when I’m stuck—not just when I need answers, but when I need clarity.

If you don’t know how to write a solid PRD, ask an AI to interview you.

If you’re unsure whether a tech stack makes sense, ask an AI to reason through the tradeoffs with you.

If something feels like boring manual work, pause and ask whether the AI can take the first pass—whether that’s searching for music, exploring open source libraries, or processing large datasets.

The biggest unlock for me was treating the AI less like a tool that executes and more like a collaborator that helps me structure my thinking. Once the thinking is clear, everything else tends to move much faster.

### 3\. Using AI isn’t an excuse for bad UX

Just because AI can generate something quickly doesn’t mean the result is automatically good.

A lot of AI-generated output works *technically* but feels awkward, confusing, or frustrating to use. If I had shipped the first version of everything AI produced, the game would function, but it wouldn’t be fun.

You still need to think about:

- How the core loop feels
- The details of the UI
- The emotional experience you want people to have

Good UX still requires intention, taste, and judgment. AI can help you move faster, but it doesn’t replace thinking deeply about how real people experience your product. That part is still on you.

![](https://substackcdn.com/image/fetch/$s_!IfsQ!,w_1456,c_limit,f_webp,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc945dc9f-44c6-492f-9fd1-ec4bbfe80715_1084x720.gif)

Every interaction was carefully crafted

—

Try it yourself! Play the game: **[www.lennyrpg.fun](https://www.lennyrpg.fun/)**

Huge thanks to Lenny for making the transcripts publicly available in the first place, and for the encouragement to share this once it was live.

Also, huge respect to the current top 3 on the leaderboard: Gribs, Baptiste, and RK—thanks for putting in the time to climb the ranks. 🏆

Whether you’re a product manager, designer, or developer, or just curious about building with AI, I hope this breakdown nudges you to try something slightly ambitious. The barrier to building polished, production-ready software has never been lower.

Now go test your product knowledge—and try to catch ’em all. 🎮

![](https://substackcdn.com/image/fetch/$s_!65vB!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa6bef6fa-53d4-45ed-944a-80429f4337f4_1200x630.png)

*Thanks, Ben! You can explore more of Ben’s work on his [website](http://benshih.design/) or [LinkedIn](https://www.linkedin.com/in/hbshih/).*

*Have a fulfilling and productive week 🙏*

---

**If you’re finding this newsletter valuable, share it with a friend, and consider subscribing if you haven’t already. There are [group discounts](https://www.lennysnewsletter.com/subscribe?group=true), [gift options](https://www.lennysnewsletter.com/subscribe?gift=true), and [referral bonuses](https://www.lennysnewsletter.com/leaderboard) available.**

Sincerely,

Lenny 👋

---
*Clipped from [lennysnewsletter.com](https://www.lennysnewsletter.com/p/how-i-built-lennyrpg) on 2026-05-11T13:21:40-04:00*
