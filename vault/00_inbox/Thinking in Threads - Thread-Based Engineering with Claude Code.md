---
title: "Thinking in Threads - Thread-Based Engineering with Claude Code"
source: "https://agenticengineer.com/thinking-in-threads"
author:
  - "[[@IndyDevDan]]"
published:
created: 2026-05-28
description: "How do you know you're improving at agentic coding? Not luck. Threads. Learn the framework for measuring real progress with Claude Code."
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
## Thinking in Threads

## The mental framework for agentic coding with Claude Code

> "When you start thinking in threads, you stop being a bottleneck and become an orchestrator."

### Why Top Engineers Feel Behind (And Why You Might Too)

Every engineer using Claude Code is secretly asking the same question: How do I know I'm actually improving my Agentic Coding?

> "I've never felt this much behind as a programmer."  
> \- Andrej Karpathy

Karpathy's confession isn't weakness. It's recognition that agentic engineering is a fundamentally new skill. The old metrics don't apply. Lines of code per day? Irrelevant when agents write thousands in minutes. Pull requests merged? Meaningless when a single prompt can generate an entire feature.

So how do you know you're improving?

How do you measure progress in a world where your agents do the heavy lifting?

Improving at any skill is about knowing WHAT to measure. After you know the few variables you need to measure to improve, you can use mental frameworks to **consistently** improve.

I've been prompt engineering and context engineering since it was first possible (shout out to gpt-3.5 turbo and gpt-4). I've written tens of thousands of prompts and generated millions of lines of code with agents.

There's one mental framework that has been the most consistent predictor of success for me and thousands of other agentic engineers and once you see it, it's impossible to unsee.

The answer is Thread-Based Engineering.

By the end of this post, you'll have a concrete framework to measure your growth as an agentic engineer.

### The Base Thread: Every Prompt Starts Here

Watch this. This is the atomic unit of agentic coding - the base thread. Every prompt you'll ever run with Claude Code (or any agentic coding tool) follows this exact shape.

> PROMPT → TOOL CALLS → REVIEW
> 
> YouAgentYou

A thread is a unit of engineering work over time, driven by you and your agent. You show up at two nodes: the beginning (prompt or plan) and the end (review or validate). The middle is your agent executing tool calls - file reads, code writes, test runs, command executions.

- THEN (pre-2023): You opened files. You typed code. You ran commands. You were the tool calls.
- NOW: You prompt. Claude Code executes. You review. That's it. You show up in two places for maximum leverage: Prompt and Review. Beginning and End.

The key insight of Thread-Based Engineering: tool calls roughly equal impact. More tool calls means more work done. In the age of agents, your agents are the engine of your work and you are the driver.

Now once you understand a single base thread, guess what you can do next?

Yup, multiply it. Run more threads.

### P-Thread: Run 15 Threads Like the Creator of Claude Code

Five in the terminal. Five to ten in the browser. Zero apologies.

That's Boris Cherny, creator of Claude Code. 5 terminal Claude Codes for in-loop work where you're actively steering. 5-10 web Claude Codes for out-of-loop tasks that run autonomously.

The math is brutally simple: more agents equals more potential output. While one agent writes tests, another refactors, another explores a new approach.

- In-loop (terminal): Active collaboration where you guide and redirect
- Out-of-loop (web/cloud): Fire and forget tasks that complete while you focus elsewhere

P-threads unlock multi-agent workflows that single-agent work cannot: code review at scale, rapid exploration of solutions, and verification through redundancy. This is agentic coding at scale. The question isn't whether you can run multiple Claude Codes. The question is: why would you run just one?

### C-Thread: High-Stakes Work Needs Checkpoints

Checkpoints aren't because your agent messed up. That's not what a C-thread is. That's bad agentic coding.

A C-thread is intentional chunking - you choosing to chain work into phases because you want verification at critical junctures. You reach for this pattern for two reasons:

1. Context constraints - the work exceeds what fits in a single agent's context window
2. Production stakes - high-risk work where human verification at each phase prevents catastrophe

Intentional chunking is a feature, not a bug. If you break a task into steps because you want verification, that's a C-thread. If the agent crashes mid-task, that's just a bug.

Claude Code has built-in tools for this: AskUserQuestion for explicit approval, system notifications for passive awareness, and text-to-speech hooks for hands-free updates when your agent finishes a phase.

The trade-off here is your time and energy. Ask yourself before reaching for this pattern: "Do I really need to break this down?" If not, just run a base thread.

### F-Thread: Nine Agents, One Winner

This is by far my favorite type of thread. And it is my favorite because of simple math: the more agents you throw at a problem, the higher your chances of success. Take more shots at the problem.

Fusion threads start where P-threads end. You parallelize work across multiple agents, then you add the fusion: you aggregate, you merge, you choose the best. Best-of-N gives you confidence. Cherry-picking gives you quality. Combining the best ideas from multiple agents gives you results no single agent could produce alone.

Imagine this: 3 Claude Code instances + 3 Gemini instances + 3 Codex instances all tackling the same problem. Nine agents. Nine parallel futures. You evaluate them all and pick the winner.

If you ask one agent a question, it says something back. If you ask five, you get much higher confidence. Say four out of five give the same answer - now you can trust that answer. The probability math works in your favor.

"But what if they all mess up my codebase?" This is where agent sandboxes shine. Each agent runs in complete isolation. No shared state. No cross-contamination. You are looking into multiple branches of what a solution could look like - without committing to any of them. This is deferred trust. Zero risk until you choose to pull down a result.

> "The future of rapid prototyping will be done with fusion threads."

Fusion threads scale through consolidation. More compute deployed, more options generated, more confidence in the final result. This is the pattern for rapid prototyping, for experimentation at speed. Most engineers haven't started exploring this territory yet. You can mark my words: this is where serious agentic engineering is headed.

### B-Thread: When Agents Manage Agents

At some point along your agentic engineering journey, you stop working with a single agent, and start working with systems of agents.

> "You'll become an Orchestrator of Intelligence."

This is where agentic software engineering separates from basic prompting. You're not just using AI - you're architecting systems where AI manages AI.

The B-thread is how you scale vertically. While P-threads scale horizontally (more parallel agents), B-threads scale depth. The simplest B-thread is a sub-agent: one agent spawns another for a specific task. But the pattern scales to full orchestration - entire teams of specialized agents working under a single coordinator.

Your prompts are now firing off other prompts. This is meta-programming for the agentic age. These systems are known as "Meta-Agentics." In this case, we're talking about Meta-Prompts (prompts that generate prompts). By deploying more compute here, you create a thicker thread - more work executed per unit of your attention.

Picture an orchestrator agent managing a full team: plan agent, scout agent, build agent, review agents, deploy agent. From your perspective: one prompt in, one review out. Everything between is a black box you've engineered to just work, again and again.

The pattern gaining rapid traction in agentic engineering: deterministic code orchestrating non-deterministic intelligence. A loop over an agent. Simple in concept, powerful in practice. You may have seen it called the "Ralph Wiggum pattern" in the community - named for the meme-worthy simplicity of the idea.

We've been teaching this as AI Developer Workflows in [Tactical Agentic Coding](https://agenticengineer.com/tactical-agentic-coding?y=blgthit) since before the mainstream tooling caught up. The pattern works.

B-threads are where you stop being a coder and start being an architect of autonomous systems. The orchestration layer becomes your highest-leverage work. Combining code + agents gives you the best of both worlds and the B-thread is at the center of that.

### L-Thread: A Single Prompt That Ran 26 Hours

The L-thread comes full circle. Same shape as your base thread. Same prompt node. Same tool calls. Same review node. The only difference? Twenty-six hours instead of twenty-six minutes.

Top agentic engineers kick off a prompt and go to bed. They wake up, have coffee, work through the day, have dinner, go to bed again. Twenty-six hours later, they come back to review. It is still running. And it works. Once you teach your agents to build like you would, the length of time they can run without you grows exponentially.

Your base thread runs for minutes. A complex P-thread might run for an hour. But an L-thread? Days. 100x the duration means 100x the decisions your agent makes without you. Thousands of tool calls. Thousands of file reads, code writes, command executions - all autonomous.

The prerequisites are demanding. This is where the core four must all be exceptional:

- Context: Your agent needs the right information (no more, no less) to stay on track for hours
- Model: You must use a model that is capable of sustained reasoning and decision-making across large tasks
- Prompt: Crystal clear agentic prompt engineering and therefore planning become essential to success
- Tools: If your agents don't have the tools YOU would use to do the job, they won't be able to do the job

> "Great planning is great prompting."

That's the elegance of thread-based engineering: the patterns scale. What works for a five-minute thread works for a five-hour thread. Master the base thread, and the L-thread becomes your north star - the same shape, just stretched across time.

### Four Ways to Scale Your Agentic Output

How do you know you're improving at agentic coding? Here's the answer: you're improving when the same hour of your time produces exponentially more output. Four multipliers. Four levers.

Here are four ways to KNOW you're improving your agentic coding.

- Width (more threads): P-threads give you 5x the exploration per hour. Boris runs 15 Claude Codes. You started with one.
- Time (longer threads): L-threads turn 10 minutes of prompting into 8 hours of autonomous work.
- Depth (thicker threads): B-threads let one prompt fire off entire teams of specialized agents.
- Attention (fewer checkpoints): This one is different. It's not about adding compute. It's about earning trust.

Trust isn't blind faith. It's earned through evidence. When your context is bulletproof, when your tools self-verify, when your prompts eliminate ambiguity - you've earned the right to step back.

The common denominator: increase tool calls per unit of your attention. Stack these multipliers. Track them weekly. Watch them trend upward.

The foundation remains constant: context, model, prompt, tools. Invest in these, and your threads grow naturally.

*But there's a thread we haven't covered yet. One that erases the review node entirely.*

### Z-Thread: The Hidden Level Beyond Review

Every game has a secret level. The one that doesn't appear on the map. The one you only find after mastering everything else.

Thread-based engineering has one too.

Welcome to the Z-thread.

Zero-touch execution. No review node. You prompt. Your agent works. The work ships.

Let me be clear about something, because what I'm about to say makes a lot of engineers uncomfortable: This is NOT vibe coding.

Vibe coding is trusting blindly. Hoping the agent got it right. Shipping without understanding. Recklessness dressed as productivity.

Z-threads are the opposite. This is maximum earned trust. You've invested in context engineering. You've refined your prompts through hundreds of iterations. You've battle-tested your tools. Your agents can verify their own work. The system has proven itself.

> "It isn't that we don't look at the code. It's that we know we don't have to."

You don't unlock this level by accident. Every thread you've run - base, parallel, checkpoint, fusion, big, long - has been building your trust muscle. The Z-thread is where that investment pays off.

This is the north star of all agentic engineering. Not the starting point. The destination.

### Start Thinking In Threads

*"How do I know I'm actually improving my agentic coding?"*

We opened with that question. Now you have the answer.

It's not luck. It's measurable. You measure it in threads. More threads. Longer threads. Thicker threads. Fewer checkpoints. Each dimension you scale is proof you're improving.

At first, you'll run short threads with one agent in the terminal. Then you'll be running five agents like [Boris Cherny](https://x.com/bcherny). Then orchestrator agents managing teams. Then agents that work while you sleep running long threads of work.

The core four anchor everything: context, model, prompt, tools. Invest in these continuously. They're what make threads run longer, thicker, more autonomous.

> "Living software that works for us while we sleep."

That's the mission. It's been the mission for years. Thread-based engineering is how we get there.

Don't be afraid of it. Don't run away from it. Software engineering has changed again and again, and it will continue to. By thinking in threads, you know exactly how you're improving.

Now that you understand thread-based engineering, the next big question is: What are best practices for improving your context engineering and (agentic) prompt engineering to run more, thicker, and longer threads?

Stay focused and keep building.

\- Dan

Board

All Saves

---
*Clipped from [agenticengineer.com](https://agenticengineer.com/thinking-in-threads) on 2026-05-28T09:14:15-04:00*
