---
title: "OpenRouter Quickstart Guide"
source: "https://openrouter.ai/docs/quickstart"
author:
  - "OpenRouter"
published:
created: 2026-05-11
description: "Get started with OpenRouter"
tags:
  - "source/web-clip"
  - "openrouter"
  - "llm-api"
type: reference
status: processed
domain: [claude-mastery]
ai-context: "OpenRouter Quickstart — three integration approaches (raw API / Client SDKs / Agent SDK), Python + JS examples, and app-attribution headers for the unified 300+ model endpoint."
---
OpenRouter provides a unified API that gives you access to hundreds of AI models through a single endpoint, while automatically handling fallbacks and selecting the most cost-effective options.

There are three ways to integrate with OpenRouter, depending on how much control you want:

| Approach | Best for |
| --- | --- |
| **[API](https://openrouter.ai/docs/quickstart#using-the-openrouter-api)** | Full control, any language, no dependencies |
| **[Client SDKs](https://openrouter.ai/docs/quickstart#using-the-client-sdks)** | Type-safe model calls with minimal overhead |
| **[Agent SDK](https://openrouter.ai/docs/quickstart#using-the-agent-sdk)** | Building agents with tool use, loops, and state |

```
Read https://openrouter.ai/skills/create-agent/SKILL.md and follow the instructions to build an agent using OpenRouter.
```

Looking for information about free models and rate limits? Please see the [FAQ](https://openrouter.ai/docs/faq#how-are-rate-limits-calculated)

In the examples below, the OpenRouter-specific headers are optional. Setting them allows your app to appear on the OpenRouter leaderboards. For detailed information about app attribution, see our [App Attribution guide](https://openrouter.ai/docs/app-attribution).

---

## Using the OpenRouter API

The most direct way to use OpenRouter. Send standard HTTP requests to the `/api/v1/chat/completions` endpoint — compatible with any language or framework.

You can use the interactive [Request Builder](https://openrouter.ai/request-builder) to generate OpenRouter API requests in the language of your choice.

```
1import requests
2import json
3
4response = requests.post(
5  url="https://openrouter.ai/api/v1/chat/completions",
6  headers={
7    "Authorization": "Bearer <OPENROUTER_API_KEY>",
8    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
9    "X-OpenRouter-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
10  },
11  data=json.dumps({
12    "model": "openai/gpt-5.2",
13    "messages": [
14      {
15        "role": "user",
16        "content": "What is the meaning of life?"
17      }
18    ]
19  })
20)
```

The API also supports [streaming](https://openrouter.ai/docs/api/reference/streaming). You can also use the [OpenAI SDK](https://openrouter.ai/docs/quickstart#using-the-openai-sdk) pointed at OpenRouter as a drop-in replacement.

---

## Using the Client SDKs

The [Client SDKs](https://openrouter.ai/docs/client-sdks/overview) wrap the OpenRouter API with full type safety, auto-generated types from the OpenAPI spec, and zero boilerplate. It is intentionally lean — a thin layer over the REST API.

First, install the SDK:

```
$npm install @openrouter/sdk
```

Then use it in your code:

```
1import OpenRouter from '@openrouter/sdk';
2
3const client = new OpenRouter({
4  apiKey: '<OPENROUTER_API_KEY>',
5  defaultHeaders: {
6    'HTTP-Referer': '<YOUR_SITE_URL>', // Optional. Site URL for rankings on openrouter.ai.
7    'X-OpenRouter-Title': '<YOUR_SITE_NAME>', // Optional. Site title for rankings on openrouter.ai.
8  },
9});
10
11const completion = await client.chat.send({
12  model: 'openai/gpt-5.2',
13  messages: [
14    {
15      role: 'user',
16      content: 'What is the meaning of life?',
17    },
18  ],
19});
20
21console.log(completion.choices[0].message.content);
```

See the full [Client SDKs documentation](https://openrouter.ai/docs/client-sdks/overview) for streaming, embeddings, and the complete API reference.

---

## Using the Agent SDK

The [Agent SDK](https://openrouter.ai/docs/agent-sdk/overview) (`@openrouter/agent`) provides higher-level primitives for building AI agents. It handles multi-turn conversation loops, tool execution, and state management automatically via the `callModel` function.

Install the package:

```
$npm install @openrouter/agent
```

Build an agent with tools:

```typescript
1import { callModel, tool } from '@openrouter/agent';
2import { z } from 'zod';
3
4const weatherTool = tool({
5  name: 'get_weather',
6  description: 'Get the current weather for a location',
7  inputSchema: z.object({
8    location: z.string().describe('City name'),
9  }),
10  execute: async ({ location }) => {
11    return { temperature: 72, condition: 'sunny', location };
12  },
13});
14
15const result = await callModel({
16  model: 'anthropic/claude-sonnet-4',
17  messages: [
18    { role: 'user', content: 'What is the weather in San Francisco?' },
19  ],
20  tools: [weatherTool],
21});
22
23const text = await result.getText();
24console.log(text);
```

The SDK sends the prompt, receives a tool call from the model, executes `get_weather`, feeds the result back, and returns the final response — all in one `callModel` invocation.

See the full [Agent SDK documentation](https://openrouter.ai/docs/agent-sdk/overview) for stop conditions, streaming, dynamic parameters, and more.

---

## Using the OpenAI SDK

You can also use the OpenAI SDK pointed at OpenRouter as a drop-in replacement. This is useful if you have existing code built on the OpenAI SDK and want to access OpenRouter’s model catalog without changing your code structure.

```
1import OpenAI from 'openai';
2
3const openai = new OpenAI({
4  baseURL: 'https://openrouter.ai/api/v1',
5  apiKey: '<OPENROUTER_API_KEY>',
6  defaultHeaders: {
7    'HTTP-Referer': '<YOUR_SITE_URL>', // Optional. Site URL for rankings on openrouter.ai.
8    'X-OpenRouter-Title': '<YOUR_SITE_NAME>', // Optional. Site title for rankings on openrouter.ai.
9  },
10});
11
12async function main() {
13  const completion = await openai.chat.completions.create({
14    model: 'openai/gpt-5.2',
15    messages: [
16      {
17        role: 'user',
18        content: 'What is the meaning of life?',
19      },
20    ],
21  });
22
23  console.log(completion.choices[0].message);
24}
25
26main();
```

## Using third-party SDKs

For information about using third-party SDKs and frameworks with OpenRouter, please [see our frameworks documentation.](https://openrouter.ai/docs/guides/community/frameworks-and-integrations-overview)

---
*Clipped from [openrouter.ai](https://openrouter.ai/docs/quickstart) on 2026-05-11T14:16:47-04:00*
