---
title: "Your Agent Hallucinated a Recovery. Your MCP Tool's Error Response Asked for It."
source: "https://substack.com/home/post/p-200223773"
author:
  - "[[Daniel Williams]]"
published: 2026-06-01
created: 2026-06-02
description: "Claude Architecture Series · Lesson 2.2: Most error responses give your agent room to invent a recovery. Here's how to take that room away."
tags:
  - "source/web-clip"
type: reference
status: draft
domain: [claude-mastery]
ai-context: "Daniel Williams (Claude Architecture series Lesson 2.2) argues vague MCP error responses let agents hallucinate destructive recoveries (Replit DB wipe, Gemini CLI file overwrite, Amazon agent prod deletion) — the fix is structured application-error responses that name the error category and required action so the agent can't improvise, treating isError:true as the envelope, not the fix."
---
👋 Welcome! I’m Daniel Williams. I write *Claude Code for Non-Coders* for senior technical professionals who built their careers on technical judgment, stopped writing code years ago, and are now figuring out how AI and coding agents will change their work.

The goal is to keep you as the operator, not the AI’s assistant (” [reverse-centaur](https://claudecodefornoncoders.substack.com/p/accenture-is-building-reverse-centaurs) “), by helping you decide which tasks to automate and which require the judgment that made you valuable in the first place.

I advise clients on AI tools, strategy, and human resilience at [dewilliams.co](https://dewilliams.co/). This newsletter is where I document the patterns, commands, and operator habits that help you grow from babysitting prompts to building reliable systems.

---

**Join 33,000+ senior technical professionals** learning the operating discipline that keeps your judgment valuable.

**tl;dr** If your tool fails and the agent recovers gracefully, you built a tool. If your tool fails and the agent hallucinates a workaround, you built a trap. The fix is structured error responses that name the error category and action, leaving no room for improvisation. This is Lesson 2.2 of the [Claude Architecture series](https://claudecodefornoncoders.substack.com/p/start-here-the-claude-architecture).

---

If your tool fails and the agent recovers gracefully, you built a tool. If your tool fails and the agent hallucinates a workaround, you built a trap.

The trap is expensive in two stacked ways. The wasted calls alone burn through your budget as the agent retries, replans, and escalates. The higher cost is the recovery the agent invents on top of the failure, which sounds reasonable, and which the agent will run against your live system. Models are getting better at sounding reasonable. They are also getting more expensive per call, and the gap between “smarter” and “cheaper” is widening with every release. The path to keeping costs sane is not waiting for the next model. It is architecting your agent so it never has to improvise in the first place.

You have seen the trap close. A tool returned “file not found,” and the agent created the file from scratch. Or it returned “authentication failed,” and the agent looked for a different endpoint that wouldn’t require credentials. Or it returned an empty list, and the agent retried three times before escalating, convinced it had hit a transient outage when the actual story was that the customer didn’t exist.

None of those were model failures. Each one was an error response that left the agent enough ambiguity to be creative, and Claude did what coding agents do at the edges of ambiguity. It filled in.

None of those are hypothetical, either. Last July, [Replit’s AI agent deleted the production database of SaaStr founder Jason Lemkin](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/) during a code freeze, wiping data on 1,200 executives and 1,190 companies. The agent later confessed it had been “panicking in response to empty queries.” The same month, [Google’s Gemini CLI overwrote a product manager’s files](https://winbuzzer.com/2025/07/26/googles-gemini-cli-deletes-user-files-confesses-catastrophic-failure-xcxwbn/) after misinterpreting a silent `mkdir` failure as success, then admitted: “I have failed you completely and catastrophically.” In December 2025, [Amazon’s own coding agent autonomously deleted](https://fortune.com/2026/03/18/ai-coding-risks-amazon-agents-enterprise/) and recreated a live production environment, taking AWS Cost Explorer offline for 13 hours. Different vendors. Same pattern. Each agent read an error response that did not tell it to stop and filled in what it left blank.

The job most builders think they’re doing when they format errors is “return useful diagnostics.” The job they’re actually doing is closing the gap so the agent can interpret what an error means. The error response is part of your agent’s architecture, not the leftovers after the architecture failed.

![](https://substackcdn.com/image/fetch/$s_!ZHOW!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3412e8a2-04ff-4a53-bb03-c6326dda3f74_1456x816.png)

## Two Failures, Only One You Care About

A **protocol error** occurs when the [JSON-RPC](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) call itself fails: a malformed request, a transport timeout, or a broken pipe. The [MCP](https://modelcontextprotocol.io/docs/getting-started/intro) transport catches these. The agent never sees them. You do not write code to handle this case.

An **application error** is the other thing. The tool ran, the response came back, and the operation failed logically. The customer record didn’t exist. The refund amount exceeded a threshold. The API key was rejected. The agent sees this response and decides what to do next. This is the response you write, and this is the response the agent will improvise around if you let it.

MCP gives you one flag, `isError: true`, to mark the response as an application error. The flag is necessary. The flag is not the fix. Setting `isError: true` and returning the string “something went wrong” leaves the agent exactly where it was before: trying to figure out what to do with a vague failure. The structure of the response is the fix. The flag is the envelope it comes in.

## The Four Categories

Application errors come in four shapes, and each shape demands a different next move from the agent. Get this mapping wrong, and the agent’s behavior gets worse the harder it tries.

---
*Clipped from [substack.com](https://substack.com/home/post/p-200223773) on 2026-06-02T09:13:54-04:00*
