---
title: "Interactions API: A unified foundation for models and agents"
source: "https://blog.google/innovation-and-ai/technology/developers-tools/interactions-api/"
author:
  - "[[Ali Çevik]]"
published: 2025-12-11
created: 2026-05-03
description: "Google’s Interactions API is a unified interface for interacting with Gemini models and agents."
tags:
  - "source/web-clip"
type: reference
status: active
domain: [claude-mastery]
ai-context: "Google's Interactions API — unified RESTful endpoint for models + built-in agents (Deep Research) with server-side state, background execution, and remote MCP tool support; relevant counterpart to Anthropic's Agent SDK."
---
Today, we’re introducing the [Interactions API](https://ai.google.dev/gemini-api/docs/interactions), a unified interface for interacting with our models, like [Gemini 3 Pro](https://deepmind.google/models/gemini/pro/), and agents like [Gemini Deep Research](https://blog.google/technology/developers/deep-research-agent-gemini-api). It’s available for developers in public beta through the [Gemini API](https://ai.google.dev/gemini-api/docs/interactions) in Google AI Studio.

The Interactions API introduces a native interface specifically designed to handle complex context management when building agentic applications with interleaved messages, thoughts, tool calls and their state.

Alongside our suite of Gemini models, the Interactions API provides access to our first built-in agent: [Gemini Deep Research](https://blog.google/technology/developers/deep-research-agent-gemini-api) (Preview), a state-of-the-art agent capable of executing long-horizon research tasks and synthesizing findings into comprehensive reports.

This is just the start. We will expand built-in agents and introduce the ability to build and bring your own agents. This will enable you to connect Gemini models, Google’s built-in agents, and your custom agents using one API.

### The Interactions API at a glance

Interactions API offers a single RESTful endpoint (/interactions) for interacting with models and specialized agents.

**Interact with models by specifying the "model" parameter.**

```
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3-pro-preview",
    input="Who won the last euro?",
    tools=[{"type": "google_search"}],
)
```

**Interact with agents by specifying the "agent" parameter.**

*Currently supports deep-research-pro-preview-12-2025.*

```
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    agent="deep-research-pro-preview-12-2025",
    input="Research the history of Google TPUs.",
    background=True
)
```

The Interactions API extends the core capabilities of [generateContent](https://ai.google.dev/api/generate-content#method:-models.generatecontent) with the features required for modern agentic applications, including:

- **Optional server-side state:** The ability to offload history management to the server. This simplifies your client code, minimizes context management errors and may result in reduced costs via increased chance of cache hits.
- **Interpretable and composable data model:** A clean schema designed for complex agentic histories. You can debug, manipulate, stream and reason over interleaved messages, thinking, tools and their results.
- **Background execution:** The ability to offload long-running inference loops to the server without maintaining client-side connections.
- **Remote MCP tool support:** Models can directly call Model Context Protocol (MCP) servers as tools.

### Our motivations for a new API

Models are becoming systems and over time, might even become agents themselves. When we designed generateContent, the primary use case was stateless request-response text generation. This works perfectly for chatbots and completion tasks.

Since then, the landscape has shifted. With the arrival of new model capabilities like “thinking” and advanced tool use, we heard lots of feedback around providing a native interface designed to support these complex interaction patterns. As we expand the Gemini ecosystem from models to fully managed agents like Gemini Deep Research, trying to force these capabilities into generateContent would have resulted in an overly complex and fragile API.

While the Interactions API supports most generateContent features and offers a more robust developer experience, it is currently in public beta and thus is still subject to breaking changes. For standard production workloads, generateContent remains the primary path and will continue to be developed and maintained.

### Getting started

You can start building with the Interactions API public beta today using your Gemini API key from Google AI Studio following the [API documentation](https://ai.google.dev/gemini-api/docs/interactions). You can also check out the OpenAPI spec [here](https://ai.google.dev/api/interactions.openapi.json).

We want to ensure this API solves the real friction points you face when moving agents to production, while still letting you seamlessly spin up new lightweight experiences, so we encourage you to test it and [share your feedback](https://discuss.ai.google.dev/).

We are committed to bringing these capabilities to the broader open source ecosystem so you can use them with your favorite tools. As a first step, the Agent Development Kit (ADK) and Agent2Agent (A2A) protocol [now support](https://developers.googleblog.com/building-agents-with-the-adk-and-the-new-interactions-api/) the Interactions API. You can expect broader support across other tools in the coming months. Interactions API and Gemini Deep Research will be coming soon to Vertex AI.

---
*Clipped from [blog.google](https://blog.google/innovation-and-ai/technology/developers-tools/interactions-api/) on 2026-05-03T11:10:47-04:00*
