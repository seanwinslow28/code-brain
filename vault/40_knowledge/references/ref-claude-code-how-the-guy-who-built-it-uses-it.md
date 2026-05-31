---
title: "Claude Code for Everything: How the Guy Who Built It Actually Uses It"
source: "https://substack.com/@hannahstulberg/p-184381596"
author:
  - "[[Substack]]"
published: 2026-01-12
created: 2026-05-31
description: "Practical AI workflows to help you get things done - no coding required. Plus, my AI side projects and tips & tricks I discover along the way."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain:
  - "claude-mastery"
ai-context: "Hannah Stulberg's 'Claude Code for Everything' #2 — the core non-coding workflow: plan mode, parallel sessions, and session management; frames Anthropic's Cowork research preview as validation that Claude Code is going beyond code."
---
*This is the **second article** in my series on Claude Code for Everything - work and life.*

1. *[First article](https://hannahstulberg.substack.com/p/claude-code-for-everything-finally) covers setup and installation.*
2. ***[Second article](https://hannahstulberg.substack.com/p/claude-code-for-everything-how-the) (this article)** covers the core workflow: plan mode, parallel sessions, and session management.*
3. *[Third article](https://hannahstulberg.substack.com/p/claude-code-for-everything-why-ai) covers context management - the key to maintaining great output quality over long conversations with Claude.*
4. *[Fourth article](https://hannahstulberg.substack.com/p/claude-code-for-everything-draft-in-claude-code-collaborate-in-notion) covers drafting in Claude Code and collaborating in Notion.*
5. *[Fifth article](https://hannahstulberg.substack.com/p/claude-code-for-everything-the-best-personal-assistant-remembers-everything-about-you) covers CLAUDE.md files - so Claude already knows how you work before you say a word.*
6. *[Sixth article](http://\(this%20article\)%20covers%20the%20status%20line%20-%20your%20always-visible%20dashboard%20at%20the%20bottom%20of%20your%20terminal./)* covers the status line - your always-visible dashboard at the bottom of your terminal.

---

**If you’ve been following Claude news:** Anthropic just launched [Cowork](https://claude.com/blog/cowork-research-preview), a research preview that brings Claude Code’s agentic capabilities to non-coding work. (When I say “just,” I literally mean yesterday. Yes, this article got some last minute tweaks.) A research preview means it’s an early version Anthropic is testing publicly before a full release. Cowork’s release validates that “Claude Code for everything” isn’t just a workaround - it’s the direction the product is going.

![](https://substackcdn.com/image/fetch/$s_!h8AH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac4a6bb9-36ee-47af-94c8-1a359f34911d_1199x774.jpeg)

Cowork is an early product. Most of the features that make Claude Code powerful, such as context management, background agents, and custom commands, aren’t yet easily available in Cowork. (I fully expect this to change over the coming weeks.) I’ll be writing about Cowork as it develops, exploring where each tool shines and when to use which. I highly encourage you to play with both - try the same task in Claude Code and Cowork and see what you get. That’s what I’m doing!

What won’t change is my focus on teaching the fundamentals. Both tools are built on the same underlying system, which means the principles I teach in this series will apply whether you end up using Claude Code or Cowork. Learn the fundamentals now, and you’ll be better at both.

## The Claude Code Creator’s Workflow

Boris Cherny, the creator of Claude Code at Anthropic, recently shared his personal workflow for using Claude Code. His setup is surprisingly vanilla - proof that Claude Code works well out of the box. However, one tip stood out: *most of his sessions start in Plan mode.* He goes back and forth with Claude until he likes the plan, then switches to auto-accept edits and lets Claude execute.

Boris shared this as coding advice. But here’s the thing - the setup for coding is the setup for everything else too. Writing articles, planning trips, doing research, and building decks. The principle is the same: align on the plan first, then let Claude run.

That insight sent me down the rabbit hole of [his full thread](https://x.com/bcherny/status/2007179832300581177). After this little side quest, I realized that almost every tip Boris shared for developers applies directly to anyone using Claude Code - whether you’re writing code or not.

If you’ve been paying attention to Claude Code lately, you’ve probably seen the content explosion. Skills. Custom commands. Background agents. MCP integrations. Everyone’s sharing their fancy setups, and it can feel like you’re already behind.

Here’s the thing: we’re going to get there. This series will cover all of it. But you learn algebra before calculus for a reason - and none of those fancy features matter if you don’t have a solid working setup first. That’s what this article is about.

![](https://substackcdn.com/image/fetch/$s_!XWRj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f3288bc-2c95-417c-9a15-983589e1011a_1200x671.png)

## By the end of this article, you’ll have:

- **Workflow fundamentals:** A core workflow for tackling any task in Claude Code
- **Workspace setup:** The environment setup I use to make working with documents easier
- **Customization options:** A preview of the advanced features - slash commands, subagents, and MCP integrations - that we’ll explore together in future articles (and that Boris touches on in his thread)

These tips form the foundation of how I use Claude Code for everything. They’re adapted from Boris’s workflow, but you don’t need to be a software engineer to use them.

## Every In the Weeds guide comes with an AI tutor

Every In the Weeds article is available as an LLM-friendly markdown file in my [In the Weeds GitHub repository](https://github.com/in-the-weeds-hannah-stulberg/substack-articles). Clone the repo, start a new session in your AI coding agent, and you have an instructor that knows every article I’ve written - ask questions, get answers grounded in specific sections, or have your agent read through the guides and tell you what to improve about your current setup.

The goal of this repository is to be able to access these articles where you’re actually working - not in a browser tab you have to switch to, but right alongside you as you’re building with Claude, Codex, Cursor, Gemini, or your agent of choice.

**If you haven’t cloned the repo yet:**

1. Clone the [repo](https://github.com/in-the-weeds-hannah-stulberg/substack-articles). New to GitHub? Go from zero-to-confident with my [GitHub 101 guide](https://hannahstulberg.substack.com/p/tool-school-github-101).
2. Open the folder in Claude Code, Cursor, or your AI coding tool of choice.
3. Ask your first question.

**Already have the repo?** Open the repo folder in your terminal and run `git pull` to get this article.

Star the repo on GitHub if you learn something new!

## The Core Workflow

## Workflow Fundamentals

These four tips form the core of how I work in Claude Code:

1. **Plan mode:** Align on the approach before Claude starts making changes
2. **Parallel sessions:** Work on multiple tasks at once without mixing context
3. **Session management:** Name and resume sessions so you can pick up where you left off
4. **Background agents:** Hand off work and keep going

## 1\. The three modes (and when to use each)

This is Boris’s [tip #6](https://x.com/bcherny/status/2007179845336527000?s=20) - and it’s a game changer.

Claude Code has three modes that control how much autonomy Claude has.

![](https://substackcdn.com/image/fetch/$s_!Sa2k!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F964c84a0-3e46-4410-8ca1-6e15bed9221a_1376x768.png)

You cycle through them with `Shift+Tab` from the input line:

- **Plan mode:** Claude explores and plans but doesn’t execute anything. You align on the approach first.
	![](https://substackcdn.com/image/fetch/$s_!eUal!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90ea0553-5fc3-4159-85d4-4acdc4b54864_1812x262.png)
- **Default mode:** Claude asks permission before each edit. You review and approve every change.
	![](https://substackcdn.com/image/fetch/$s_!sj6a!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f620140-72b9-48e9-abea-7319943c63f9_1808x212.png)
- **Accept edits:** Claude executes without asking. Changes happen automatically.
	![](https://substackcdn.com/image/fetch/$s_!67qv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F611a7292-ec99-4493-9699-776791fb7e4c_1808x254.png)

Think of it like working with a junior employee. You’re constantly adjusting your oversight based on how much you trust what’s about to happen:

- **Big decision or new task?** Use *plan mode*. Like asking your junior employee to outline their approach before they start - Claude explores your files, asks clarifying questions, and proposes an approach. You go back and forth until you’re aligned. Boris mentions he’ll sometimes engage in significant back and forth on a single plan - I do the same.
	- Claude will often ask you questions before proposing a plan - clarifying your goals, surfacing assumptions, checking constraints. This is a feature, not a bug. The questions make the plan better.
		- *Pro tip:* [Dictating your feedback](https://hannahstulberg.substack.com/p/stop-typing-start-talking-how-dictation) is much faster than typing into the terminal (I personally use Wispr Flow.).
- **Executing the plan?** Use *default mode*. Like sitting side by side, reviewing each section as it’s drafted by your junior teammate - Claude proposes changes one at a time, and you accept or reject each one before it moves on.
- **Simple mechanical task you’re confident about?** Use *accept edits*. Like telling your junior report “just format the appendix, I trust you” - Claude executes without asking, and you check back when it’s done.

The key insight: match your level of oversight to your confidence in the output. I flip between modes constantly throughout a single task. Start in plan mode to align on the approach. Switch to default mode to execute with review. Flip to accept edits for trusted stretches where I know exactly what I want. Then back to plan mode when I hit a new decision point.

**The critical part: actually read the plan and give feedback.** Claude won’t always get it right on the first try - and that’s fine. Remember: you’re reviewing a proposal from your junior employee. You wouldn’t glance at a project plan, assume it’s right, and immediately say “looks great, go ahead.” You’d read it. Check that it covers everything you asked for. Spot what’s missing. Push back on approaches you don’t like. Ask questions about parts that seem off. That iteration process - the back and forth you’d have with a junior employee - is what makes the output good. A plan you didn’t read is worse than no plan at all - it gives you false confidence that you’re aligned when you’re not.

**A note on permissions:** By default, Claude asks for permission before running certain operations. Boris pre-allows the ones he knows are safe (his [tip #10](https://x.com/bcherny/status/2007179854077407667?s=20)) so he doesn’t get interrupted every time. Pre-allowing safe operations lets you and Claude work faster across both default and accept edits modes. I cover permission set-up in [the previous article](https://hannahstulberg.substack.com/i/184061644/pre-allow-safe-commands).

## 2\. Run parallel sessions

Back to our junior employee metaphor: imagine giving one new hire three completely unrelated tasks at the same time - draft this article, research those competitors, and analyze that spreadsheet. They’d be context-switching constantly, and the output would suffer.

Now imagine you have three junior employees, each focused on one task. Much better results.

![](https://substackcdn.com/image/fetch/$s_!_miV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb0572395-dc71-4f42-ad29-3e5e70218e5e_1376x768.png)

That’s exactly how Claude Code works. Each instance of Claude Code is like a separate junior employee - give it one task, and it can focus completely. The technical term for this is a *session*. Boris runs 5+ sessions at once (his tips #1 and #2), each dedicated to a different task.

Why does this matter? Each session has its own *context* - essentially, what Claude remembers and is paying attention to. If you try to draft an article and research competitors in the same session, Claude is juggling unrelated information and quality drops. Separate sessions mean each task gets Claude’s full attention. (The next few articles in this series will deep dive on effective context management.)

**How to run parallel sessions:**

Open separate terminal instances in your IDE, each running Claude Code. I covered this setup in my [Claude Code tips & tricks article](https://hannahstulberg.substack.com/i/183150134/5-run-tasks-in-parallel-to-move-faster) ([tip #5](https://hannahstulberg.substack.com/i/183150134/5-run-tasks-in-parallel-to-move-faster)).

## 3\. Pick up where you left off

Every time you start Claude Code (by typing `claude` in your terminal), you’re starting a fresh session with no memory of previous work. It’s like your junior employee going home and coming back the next morning with no memory of anything you discussed. That’s what happens if you don’t name and resume your sessions.

![](https://substackcdn.com/image/fetch/$s_!htPi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d92b751-a8bd-42ff-91c0-90ff88d5a268_1376x768.png)

- **Name your sessions:** Use `/rename Q1 Planning Meeting` in the command-line to give your session a name. I use the same name for both my terminal and my session - so I always know which session goes with which terminal. (I cover terminal naming in [tip #6](https://hannahstulberg.substack.com/i/183150134/6-split-your-terminals-so-you-know-when-tasks-finish) of my [Claude Code tips & tricks article](https://hannahstulberg.substack.com/p/skip-the-terminal-and-8-other-claude).)
- **Resume later:** Claude Code’s resume feature lets you pick up exactly where you left off within a session - all the context, all the decisions, and everything Claude learned about your task. Three ways to resume:
	1. `/resume` to browse your named sessions
		2. `/resume Q1 Planning Meeting` to go directly to a specific session by name
		3. `claude --resume Q1 Planning Meeting` to start Claude directly into a session from your terminal
	*(A note to the incredible Claude Code team, if you’re reading this: I’ve found the resume feature to be a bit buggy - it sometimes crashes Claude Code, and the session search doesn’t always work. It’s still worth using, but this feature could use a little love.)*
- **Save the session name in your file:** I’ve found session search to be buggy, so I literally type the session name into the markdown file I’m working on. That way, when I open the doc later, I know exactly which session to resume.

![](https://substackcdn.com/image/fetch/$s_!uj1I!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F71ed3f73-26aa-42b7-b791-fb2870ab89fb_1954x1010.png)

The set-up: Named terminal, named session and the session name with resume instructions saved to the relevant document.

## 4\. Hand off tasks to background agents

Here’s where the junior employee metaphor gets interesting. You’re working with your junior employee on a big task - say, drafting an article. Partway through, you realize there’s a related side task: “We need to pull together all the research sources we’ve referenced.”

Your junior employee could stop what they’re doing and handle it - but that breaks your flow. Instead, they hand it off to another junior employee they supervise. That second employee works on the research list while you and your main employee keep drafting the article. When it’s done, they tap you on the shoulder.

![](https://substackcdn.com/image/fetch/$s_!i9Gp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e9474b9-c4a8-4070-a306-d387eddc049e_1376x768.png)

That’s what background agents do. Claude (your main session) delegates a related task to another Claude instance that runs independently. You keep working with your main Claude on the main task, and when the background agent finishes, you get notified to review their work.

**How to use background agents:**

1. **Send a task to the background:** Tell Claude to run something in the background. For example:
	- “Compile all the sources we’ve referenced into a bibliography - do this in the background”
		- “Run this as a background agent: create a summary of the key points we’ve covered so far”
	Claude will confirm the task is running in the background, and you can keep working on your main task without waiting.
2. **Get notified when it’s done:** Claude will interrupt you when the background agent finishes. You’ll see a notification in your terminal that the task is complete.
3. **Check on running tasks:** Type `/tasks` to see all your background agents - what’s running, what’s finished, and what the output was.

**When to use background agents:**

The sweet spot is a task that needs the context from your current session but doesn’t need to block you. If the task is unrelated to what you’re working on, just open a separate terminal. But if the task requires context from the current discussion in order to be executed effectively - like making a series of edits after aligning on the edits to make - a background agent is the right solution.

I’ll cover background agents more deeply in a future article.

**A note on model choice:** Boris uses Opus 4.5 with thinking for everything (his [tip #3](https://x.com/bcherny/status/2007179838864666847?s=20)). His reasoning: even though it’s bigger and slower than Sonnet, you have to steer it less - so it’s almost always faster in the end. The same applies to everything you do in Claude Code. The extra quality from a better model compounds - less time correcting, less back-and-forth, and better first drafts. You’ll get the best results from this workflow if you’re using Opus 4.5.

## Setting Up Your Workspace

These next four tips help you work with files efficiently - essential when most of what you’re doing involves documents, notes, and research rather than code.

1. **Split editor:** Read in preview, edit in markdown - the best of both worlds
2. **Table of contents:** Navigate long markdown files with one click
3. **IDE over terminal:** Everything in one window - files, documents, and terminals
4. **PDF extension:** View PDFs directly in your editor without switching apps

## 1\. Split your editor: markdown on the left, preview on the right

Claude generates markdown files by default (I explained why in [the first article in this series](https://hannahstulberg.substack.com/i/184061644/why-does-claude-code-use-markdown), which also covers [preview mode](https://hannahstulberg.substack.com/i/184061644/how-to-read-and-edit-markdown-files)).

**The setup I recommend:** Markdown files on the left, preview on the right. They scroll in tandem, so you can read the nicely formatted preview while making quick edits in the raw markdown.

Why this works better than preview-only: Reading in preview mode is much easier than parsing raw markdown with all the `#` symbols and `**bold**` syntax. But if you need to make a quick edit, you don’t want to close preview, find the spot in the markdown, edit, then reopen preview. With this split view, you read in preview and edit in markdown - the best of both worlds.

![](https://substackcdn.com/image/fetch/$s_!4CL0!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd8d8580-914b-40da-8485-abc844bdda9a_1836x928.png)

**To set this up in Cursor:**

1. Open your markdown file
2. Click the “Open Preview to the Side” button in the top right of the editor
	![](https://substackcdn.com/image/fetch/$s_!b2wO!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff06f892c-1662-4d8c-8c04-939355b22017_1952x754.png)
3. The preview opens on the right, markdown stays on the left
4. Scroll either side - they stay synced

**Pro tip:** If the preview ever gets stuck showing stale content, force refresh it: Open the Command Palette (`Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows), search for “Markdown: Refresh Preview,” and hit enter.

*(To the good folks at Cursor - if you’re reading this, the ability to have multiple files open in preview at the same time would be fantastic!)*

## 2\. Add a clickable table of contents to long markdown files

When your markdown files get long, add a clickable table of contents at the top. It transforms a wall of text into a navigable document - click any section to jump straight there in Preview mode.

![](https://substackcdn.com/image/fetch/$s_!4MhD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2be341d0-3b2d-437c-943c-3c24641e30a7_1840x932.png)

**How to ask Claude to add or update one:**

> *Add a table of contents at the top of this file with links to each section header. If one already exists, update it to reflect the current sections.*

## 3\. Use an IDE, not the terminal

Even with Cowork on the horizon, this recommendation still stands strongly for Claude Code.

If you’re still using Claude Code in a standalone terminal, stop. This was my [first tip](https://hannahstulberg.substack.com/i/184061644/step-1-choose-and-install-your-ide) in [the setup article](https://hannahstulberg.substack.com/p/claude-code-for-everything-finally), and it’s even more important when you’re working with documents.

An IDE gives you everything in one window: your file structure, your documents, and your terminals. You can see what Claude is working on, preview your markdown, and manage multiple sessions - all without switching windows.

I use Cursor because it has built-in model switching (so I can test prompts in other models when needed), but VS Code or any other IDE works too. [The setup article](https://hannahstulberg.substack.com/p/claude-code-for-everything-finally) walks through installing an IDE and its core components.

**A note on third-party wrappers:** You may have seen recommendations for software layers that sit on top of Claude Code - tools that promise to make the terminal experience “friendlier” for non-technical users. I’d encourage you to be cautious here - especially now.

When you put a layer between yourself and Claude Code, you’re letting another company control your experience with the core product. You don’t know how they’re changing or limiting Claude Code’s features under the hood - and when Anthropic ships updates, you’re waiting for that third party to catch up. You’re giving up significant control and distancing yourself from the product you actually want to use.

With the launch of Cowork, Anthropic is building the more user-friendly layer themselves. An IDE isn’t a layer on top of Claude Code - it’s just the environment where you run it. Claude Code still works exactly as Anthropic designed it. You’re getting the full experience, straight from the source, with the added file management benefits that make document work easier. And using Claude Code directly now will help you learn Cowork if that’s where you ultimately decide to go.

## 4\. Install vscode-pdf for viewing PDFs

Cursor doesn’t support PDFs out of the box. If you try to open a PDF, you’ll just see gibberish. Install the vscode-pdf extension so you can view PDFs directly in Cursor - useful when you’re working with research papers, contracts, or reference documents and don’t want to switch to another app.

**To install in Cursor:**

1. Open the Extensions view (View → Extensions, or `Cmd+Shift+X` on Mac and `Ctrl+Shift+X` on Windows)
	![](https://substackcdn.com/image/fetch/$s_!VJeG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f752f90-504e-42a8-8a6b-2ed048d1baea_598x772.png)
2. Search for “vscode-pdf”
	![](https://substackcdn.com/image/fetch/$s_!xRmY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2d556b2-f9e6-42a0-85bb-b07dfbc82194_596x728.png)
3. Click Install
	![](https://substackcdn.com/image/fetch/$s_!cYgs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5397ea12-3e32-4acf-903e-4be3d0da01cc_1018x322.png)

## Preview: Customization

Boris’s thread covers more than just workflow fundamentals - he also shares how he customizes Claude Code to save even more time. Once you’ve nailed the fundamentals, these features let you automate your most common workflows and squeeze even more efficiency out of every session.

But you don’t want to jump to the fancy stuff before you understand the basics. The first few articles in this series will focus on fundamentals - once those are solid, we’ll dig into customization.

A quick preview of what’s coming:

- **Slash commands:** Save repeated workflows as commands you can run with a single `/` command (e.g., `/summarize-meeting`)
- **Subagents:** Automate review and polish steps that you’d run on most tasks, like a doc reviewer that checks every draft
- **MCP (Model Context Protocol):** A way to connect Claude to apps like Notion and Slack so Claude can pull from them directly - no copy-pasting required

I’ll cover the full setup for each of these in dedicated articles later in this series.

## What you should have now

If you’ve followed along, you now have:

- **A workflow for any task:** Start in plan mode, align on the approach with your junior employee, then switch to default or accept edits based on how much you trust the output. Adjust constantly.
- **Multi-tasking without the mess:** Parallel sessions let you work on multiple tasks at once. Named sessions let you pick up tomorrow where you left off today.
- **A workspace built for documents:** Markdown on the left, preview on the right. Clickable table of contents for long files. PDFs viewable without switching apps.

## The bottom line

The biggest unlock from Boris’s workflow is the realization that the setup for coding is the setup for everything else. Plan mode, parallel sessions, matching your oversight to your confidence - these are productivity fundamentals, not developer tricks.

Before we get to the customization features I previewed above, there’s one more foundational topic: context management. What Claude remembers, what you preserve, and how you structure information so Claude can use it effectively. That’s where we’re headed next.

## Want to go deeper?

If you want to see these concepts in action, check out Carl Vellotti’s Claude Code resources. His latest [YouTube](https://www.youtube.com/watch?v=59gy_24KIVE) episode covers plan mode and parallel agents with live demos and his [Claude Code for Everyone](https://fullstackpm.com/cc4e) course teaches Claude Code within Claude Code.

Carl’s a PM who’s been deep in Claude Code - watching him work through real examples is a great way to see how these workflows actually play out.

---
*Clipped from [substack.com](https://substack.com/@hannahstulberg/p-184381596) on 2026-05-31T16:05:13-04:00*
