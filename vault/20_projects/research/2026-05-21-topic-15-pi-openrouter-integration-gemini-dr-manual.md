---
type: research-report
date: 2026-05-21
question: "Topic 15 — Pi + OpenRouter integration pattern in 2026. How to configure Pi to use OpenRouter as a model provider: auth, per-task routing, cost caps, automatic fallback, mixed-provider projects."
topic: 15
source: gemini-deep-research-manual
tier: dr
tags: [research, deep-research, pi.dev, openrouter, gemini-dr-manual]
---

# **OpenRouter Integration and Cost-Capped Agentic Workflow Configuration for Pi.dev**

## **1\. Integration Mode**

The integration of OpenRouter into the Pi coding platform (pi.dev) represents an intersection of client-side modularity and server-side model aggregation. Pi operates as a highly specialized, minimal terminal coding harness, explicitly eschewing bloated, predefined sub-agent architectures in favor of a deeply configurable, text-based extension ecosystem.1 Because Pi is designed to remain small at its core 2, it does not rely on a monolithic, proprietary software development kit (SDK) to connect to OpenRouter. Instead, Pi provides comprehensive, first-class support for OpenRouter natively, supplementing it with a generic OpenAI-compatible base URL override mechanism that is officially documented and integrated through the configuration layer.3  
The official documentation provides unambiguous confirmation of this integration. The configuration literature explicitly states: "OpenRouter, OPENROUTER\_API\_KEY, openrouter" when listing the built-in API key providers that the platform natively recognizes.4 Furthermore, the documentation detailing custom model additions quotes: "Via models.json: Add Ollama, LM Studio, vLLM, or any provider that speaks a supported API (OpenAI Completions, OpenAI Responses, Anthropic Messages, Google Generative AI)".4 By utilizing the openai-completions API type within the configuration, Pi normalizes all outbound requests to adhere to the standard OpenAI chat completions schema. This allows OpenRouter to intercept the payload and handle the downstream translation to disparate endpoints, such as Anthropic or Google, dynamically.3  
While Pi supports manual configuration via JSON files, the developer ecosystem also features community extensions engineered to automate the synchronization of upstream models. The extension @vtstech/pi-openrouter-sync is explicitly designed for this purpose, allowing platform-integration engineers to "Add models from OpenRouter URLs or bare model IDs directly into Pi's models.json configuration".6 However, in an architecture involving a strict budgetary environment with approximately fourteen concurrent agent processes running on a macOS system, relying on automated synchronization extensions introduces substantial financial risk. Automated fetching might inadvertently expose the local routing tables to high-cost frontier models. Consequently, the manual definition of the OpenRouter provider block utilizing the openai-completions override in the models.json file is the mathematically and architecturally superior integration mode. This manual approach guarantees that the routing layer only acknowledges explicitly whitelisted, cost-analyzed models, isolating the multi-agent workflow from unexpected pricing fluctuations in the upstream aggregator.

## **2\. Auth Pattern**

Authentication within the Pi platform is orchestrated through a highly secure, hierarchical credential resolution system designed to protect sensitive API keys while preserving maximum flexibility for automated, multi-agent workflows.2 For an architecture relying on a fleet of fourteen concurrent agents operating within a macOS environment, securing the OpenRouter API key is critical to preventing unauthorized token expenditure and maintaining the strict financial limits of the operation.  
Pi resolves API credentials utilizing a strict priority order: command-line interface (CLI) flags (--api-key), local authorization files (auth.json), environment variables, and finally, custom provider keys embedded directly within the models.json file.2 The simplest authentication pattern involves injecting the credential via environment variables. Pi natively maps the standard OPENROUTER\_API\_KEY environment variable to its internal openrouter authentication identifier.4 A developer can export this variable within the macOS terminal session, or define it globally within a .zshrc or .bash\_profile configuration, instantly authenticating all spawned agents within that shell session.2  
Despite the convenience of environment variables, a significantly more robust and secure pattern involves utilizing Pi's dedicated global authorization file, located at \~/.pi/agent/auth.json.2 This global file is automatically provisioned by Pi with strict 0600 POSIX file permissions, ensuring that only the owning user account can read or modify the stored credentials. This permission structure intrinsically protects the API keys from unauthorized access by other processes or users on the shared macOS system.2 The auth.json architecture supports three distinct value resolution formats for injecting the OpenRouter API key: literal strings, referenced environment variables, and dynamically executed shell commands.2  
The literal value injection format requires hardcoding the key directly into the JSON data structure. While functional for isolated testing, this approach unnecessarily exposes the plaintext key to file system backups or accidental source control commits. The environment variable format allows the JSON configuration to reference a named variable, deferring the actual credential injection to the shell's environment.2 However, the most advanced, enterprise-grade authentication pattern for macOS developers leverages the shell command resolution mechanism. By prefixing the key value with an exclamation mark (\!), Pi executes the subsequent string as a subshell command at the exact moment of the API request, capturing the standard output (stdout) as the authenticated key.3  
This dynamic execution feature facilitates seamless integration with the macOS Keychain or third-party secret managers directly into the agentic workflow. A developer can store the OpenRouter API key securely within the macOS Keychain and configure the auth.json file to retrieve it dynamically using the native macOS security command-line utility.2 The exact configuration syntax required for this secret manager integration is structured as follows:

JSON  
{  
  "openrouter": {  
    "type": "api\_key",  
    "key": "\!security find-generic-password \-w \-s 'openrouter-api-key'"  
  }  
}

When an agent initializes a network connection, Pi triggers the security command, retrieves the password securely from the encrypted macOS Keychain, and caches it in memory for the lifetime of that specific process.2 The official documentation explicitly notes that Pi does not apply arbitrary time-to-live (TTL) limits, stale reuse logic, or automatic recovery mechanisms to these arbitrary shell commands.3 Consequently, if the executed shell command introduces significant system latency, it will directly delay the initial model request. For a high-throughput environment simultaneously managing fourteen agents, utilizing the macOS Keychain via the security CLI is highly optimal. Local Keychain retrieval is computationally inexpensive and nearly instantaneous, completely eliminating the risk of persisting plaintext credentials on disk while maintaining low-latency initialization for the agent swarm.

## **3\. Per-Task Model Routing Inside Pi**

The orchestration of a fourteen-agent workflow on a highly constrained budget necessitates uncompromising control over the specific models utilized for distinct computational tasks. Frontier models excel at complex code generation and abstract architectural planning, but they are prohibitively expensive and computationally wasteful when applied to routine operations such as context summarization, logging, or simple textual analysis. Pi accommodates granular, per-task model routing through a combination of its sophisticated extension ecosystem and localized configuration overrides, allowing discrete tasks to be explicitly mapped to designated OpenRouter endpoints.3  
At the foundational level, Pi skips monolithic features like hardcoded sub-agents and strict planning modes, opting instead to ship with powerful defaults that developers adapt via packages.1 To route different tasks to different models within a single project, developers must utilize specialized community extensions that implement multi-phase state machines. For planning and code execution tasks, extensions such as @dreki-gg/pi-plan-mode implement a distinct two-phase workflow.8 This extension forces the agent into a read-only planning phase utilizing a highly capable reasoning model, generates a deterministic PLAN.md artifact, and subsequently hands execution over to a cheaper, faster model for implementation.8 Similarly, the @plannotator/pi-extension manages task states—categorized as idle, planning, and executing—and provides dedicated configuration blocks for each phase. By configuring a local .pi/plannotator.json file, an engineer can explicitly bind the execution phase to a specific model identifier, overriding the default project parameters.9  
For core system maintenance tasks, particularly context compaction and branch summarization, Pi provides native configuration blocks that do not require third-party extensions. When an active session exceeds its predefined context window, Pi initiates an auto-compaction process to summarize older messages and preserve token overhead.10 Extensions such as @howaboua/pi-subagent-review document the exact syntax required to route these summarization tasks to specific, cost-effective models.11 To configure summarization routing natively, the global or project-level .pi/settings.json file must include a specific summary block detailing the exact model identifier and the required thinking level for the task.11  
If a specialized task-routing extension is not deployed, the standard workaround for per-task routing involves utilizing Pi's native model-switching commands either interactively or programmatically. Within an active terminal session, the /model \<provider/model-id\> command immediately shifts the conversational context to a new endpoint.2 Programmatically, via Pi's Remote Procedure Call (RPC) mode or the native Software Development Kit (SDK), an external orchestrating script can issue a set\_model command over standard input (stdin) prior to transmitting a specific prompt.12 This mechanism enables a master controller script managing the fourteen agents to dynamically switch an individual agent to anthropic/claude-opus-4-7 for an intensive code generation pass, and immediately revert it to openai/gpt-5.4-mini for the subsequent code review or commit message generation, relentlessly optimizing the financial expenditure of the workflow.  
The configuration syntax for routing the native summarization task to a specific OpenRouter model, as officially documented by extension schemas and system parameters, must be defined verbatim within .pi/settings.json as follows:

JSON  
{  
  "summary": {  
    "enabled": true,  
    "model": "openrouter/openai/gpt-5.4-mini",  
    "thinking": "low"  
  }  
}

This configuration ensures that whenever the agent's context window reaches its threshold, or when navigating the session tree via /tree triggers a branch summary to preserve abandoned path data 7, the summarization payload is routed exclusively to the designated, lower-cost OpenRouter model. This strict routing parameter isolates the high-cost frontier model, reserving its capabilities strictly for the primary generative engineering tasks.

## **4\. Cost Tracking and Per-Day Caps**

Managing an aggregate budget of $5 per day across approximately fourteen autonomous agents demands uncompromising mathematical visibility into token consumption and the strict enforcement of absolute financial ceilings. The integration of Pi and OpenRouter provides a dual-layered approach to cost administration: Pi handles granular, real-time tracking and localized task caps within the terminal user interface, while OpenRouter enforces the absolute, cryptographic daily budgetary caps at the network edge.  
To grasp the complexity of this deployment, it is necessary to analyze the economics of the $5 daily limit. Distributed evenly across fourteen independent agents, the maximum allowable expenditure is approximately $0.35 per agent per day. The financial viability of this workflow depends entirely on the pricing structures of the targeted models.

| Provider | Model Identifier | Input Cost (Per 1M) | Output Cost (Per 1M) | Cache Read (Per 1M) |
| :---- | :---- | :---- | :---- | :---- |
| OpenRouter | anthropic/claude-opus-4-7 | $15.00 | $75.00 | $1.50 |
| OpenRouter | openai/gpt-5.4-mini | $0.15 | $0.60 | $0.00 |
| OpenRouter | meta/llama-4-405b-free | $0.00 | $0.00 | $0.00 |

If an agent relies exclusively on a frontier model such as Claude Opus, the $0.35 daily allocation purchases roughly 23,000 input tokens or a mere 4,600 output tokens.13 However, by routing routine tasks to lower-cost models and utilizing aggressive prompt caching protocols—where cached inputs cost only $1.50 per million tokens 13—the agent's operational lifespan is extended exponentially.  
To surface this OpenRouter expenditure accurately in real time within Pi, the engineer must explicitly define the token pricing economics within the models.json configuration file.3 Because OpenRouter functions as an aggregator with fluctuating, pass-through pricing schemas 5, Pi cannot automatically deduce the cost of a dynamically fetched OpenRouter model. The cost object must be manually mapped for each custom model, defining the expenditure per million tokens across four specific dimensions: input, output, cacheRead, and cacheWrite.3 When this object is populated, Pi's internal SessionManager algorithms calculate the precise financial impact of every API request based on the returned token usage metadata, accumulating the data into the internal AgentMessage usage object.2 This mechanism allows the developer to monitor the micro-expenditures of all fourteen agents in real time by inspecting the interactive TUI footer or by tailing the JSON event stream utilizing the pi \--mode json command.2  
While Pi excels at local cost tracking, it fundamentally lacks a centralized, cross-process financial firewall. Pi does not possess a native, global setting to enforce a strict monetary daily cap across independent agent processes running concurrently.7 Within Pi, budget caps are exclusively scoped to individual tasks or logical goals using extensions. The community extension pi-goal allows developers to set a strict token budget for an active objective.15 If an active goal reaches its configured token budget, the agent's internal state machine forcibly transitions to a budget\_limited state.15 At this juncture, the language model is restricted from initiating new substantive code generation, forced to summarize its progress, identify blockers, and await human intervention.15 This mechanism prevents infinite loops and runaway code generation within a single agent context, but it operates on token volume, not a fiat currency daily limit.  
To guarantee that the $5/day budget is never breached across the entire fourteen-agent fleet, the financial cap must be configured exclusively on the OpenRouter dashboard.17 OpenRouter provides definitive, server-side enforcement of credit limits per API key.17 Client-side cost enforcement is inherently vulnerable to race conditions; fourteen agents querying models simultaneously could drastically overshoot a local budget limit before the individual processes synchronize their ledger states. By enforcing the limit at the network gateway, OpenRouter prevents this entirely.  
The flow for setting this daily cap is executed outside of the Pi terminal: The developer must navigate to the OpenRouter dashboard (openrouter.ai/keys), generate a dedicated API key specifically for the Pi agent fleet, and utilize the "Credit limit" field to establish a hard monetary ceiling of $5.17 When the cumulative token expenditure across all agents hits this designated cap, OpenRouter immediately halts processing and returns a 402 Payment Required or a terminal rate-limit HTTP error code.17 Pi's native retry handlers will intercept this error, exhaust their maximum retry attempts, and emit an auto\_retry\_end event indicating failure, allowing the workflow to shut down gracefully without incurring further debt.2

## **5\. Automatic Fallback**

In a decentralized API environment routing through a global aggregator, transient errors such as 429 Too Many Requests or 503 Service Unavailable are statistical inevitabilities. Operating a fleet of fourteen agents significantly exacerbates the likelihood of encountering strict concurrency limits. A robust agentic workflow must possess resilient automatic failover capabilities. When utilizing Pi with OpenRouter, automatic fallbacks exist across two distinct but intersecting layers: the Pi client-side retry loop and the OpenRouter server-side fallback arrays.  
Pi possesses an internal, client-side resilience mechanism designed to intercept HTTP errors and implement exponential backoff.7 Configured within the global \~/.pi/agent/settings.json file, the retry block governs how the Pi core responds to timeouts and server rejections.7 The syntax for configuring Pi's internal retry logic requires enabling the feature, setting the maximum number of retries, defining the base delay for the exponential backoff algorithm, and setting the maximum server-requested delay.7  
The verbatim configuration for the Pi-side retry mechanism is defined as follows:

JSON  
{  
  "retry": {  
    "enabled": true,  
    "maxRetries": 3,  
    "baseDelayMs": 2000,  
    "provider": {  
      "timeoutMs": 3600000,  
      "maxRetryDelayMs": 60000  
    }  
  }  
}

If a request fails, Pi will pause for the designated base delay and attempt to resend the payload. However, Pi's native retry loop only requests the exact same model again; it does not possess the native capability to transition a failed request to a cheaper or alternative model upon encountering a 429 error.  
To achieve actual model fallbacks—for instance, shifting a request from an Anthropic model to a Meta Llama model when rate-limited—the configuration must leverage OpenRouter's advanced downstream routing parameters. OpenRouter allows developers to define a structured array of fallback models in priority order.19 If the primary model's endpoints are down, rate-limited, or refuse to reply due to content moderation filters, OpenRouter automatically attempts the next model in the fallback list before returning a failure to the client.19  
Pi officially supports injecting these advanced routing preferences into the OpenRouter API payload. Through the models.json file, engineers can define the openRouterRouting object within a specific model's compat block.3 This object is serialized and transmitted verbatim in the provider field of the OpenRouter request body.3 Within this block, setting allow\_fallbacks to true and defining the order array with desired provider slugs instructs OpenRouter to fall back to alternative hosts (e.g., from Anthropic's direct API to AWS Bedrock) for the *same* model.3  
However, to fall back to an entirely different model architecture (from Claude to Llama), the request must utilize the OpenRouter models array API parameter.19 Because Pi maps its internal representation to the OpenAI SDK schema, this parameter can be passed directly. When configured correctly, if the primary model throws a 429 error, OpenRouter intercepts the failure internally, reroutes the exact same context window to the secondary model specified in the array, and returns the successful response to Pi.19 This server-side failover occurs within a single Pi network request, completely bypassing Pi's client-side exponential backoff loop and drastically reducing the time-to-recovery for the stalled agent. If the OpenRouter fallback list is ultimately exhausted and it returns a hard error to Pi, Pi's retry.maxRetries configuration will trigger, pausing the agent before restarting the entire OpenRouter fallback chain.

## **6\. Mixed-Provider Projects**

A highly optimized, cost-capped local workflow frequently requires leveraging multiple upstream Large Language Model APIs simultaneously. A solo developer might possess a direct, prepaid Anthropic billing account for intensive codebase analyses, while utilizing OpenRouter strictly to access specialized or open-weights models that Anthropic does not host. The Pi architecture inherently supports maintaining an Anthropic key, an OpenRouter key, and an OpenAI key simultaneously within a single project, facilitating seamless task routing across disparate APIs without requiring environment variable manipulation during runtime.2  
To achieve this mixed-provider architecture, the authentication and model configurations must be strictly segregated. The global auth.json file is explicitly designed to hold multiple distinct credentials simultaneously, indexed by their unique provider identifiers.2  
The configuration required to hold all three keys simultaneously is structured as follows:

JSON  
{  
  "anthropic": {  
    "type": "api\_key",  
    "key": "sk-ant-..."  
  },  
  "openai": {  
    "type": "api\_key",  
    "key": "sk-proj-..."  
  },  
  "openrouter": {  
    "type": "api\_key",  
    "key": "sk-or-v1-..."  
  }  
}

Subsequently, the models.json file must explicitly define the distinct provider endpoints. Pi allows the definition of an infinite number of provider blocks within the root providers object.3 When an agent triggers an inference request, the Pi runtime matches the requested provider/model-id string (e.g., anthropic/claude-3-5-sonnet versus openrouter/meta-llama-3-70b-instruct) and routes the network payload to the appropriate Base URL, utilizing the specific API schema and authentication header assigned to that designated provider block.3  
This mixed-provider configuration is exceptionally powerful for mitigating vendor lock-in and optimizing latency. By utilizing the modelOverrides object within models.json, a developer can selectively map built-in models to specific routing proxies.3 For example, the default Anthropic requests can be handled directly by Anthropic's low-latency API infrastructure, but specific, high-throughput tasks can be mapped to OpenRouter to take advantage of specific enterprise routing features or inverse-square price selection algorithms.18 The ability to route different tasks to different providers is achieved by instructing the active agent phase or script to invoke the fully qualified provider and model ID.12 This structural design guarantees that a single Pi session tree 2 can seamlessly contain a conversation history generated consecutively by OpenAI, Anthropic, and OpenRouter, synthesizing their outputs into a unified, mathematically bounded agentic context.

## **7\. Working Config Example**

The following is a comprehensive, copy-paste-ready configuration implementation utilizing Pi's standard JSON file structures. This configuration establishes a sophisticated environment that fulfills all specific architectural requirements for a solo developer running a cost-capped multi-agent fleet.  
This configuration achieves the following objectives:  
(a) Securely sets the OpenRouter API key utilizing the macOS Keychain integration.  
(b) Routes core codegen tasks to anthropic/claude-opus-4-7 via the OpenRouter proxy endpoint.  
(c) Routes context summarization tasks to the highly economical openai/gpt-5.4-mini via OpenRouter.  
(d) Establishes the parameters for the $5/day limit (noting that the hard cap must be activated on the OpenRouter dashboard, while local tracking is enabled here).  
(e) Defines a fallback mechanism to meta/llama-4-405b-free in the event of rate limits.  
**File: \~/.pi/agent/auth.json**

JSON  
{  
  "openrouter": {  
    "type": "api\_key",  
    "key": "\!security find-generic-password \-w \-s 'openrouter-api-key'"  
  }  
}

**File: \~/.pi/agent/models.json**

JSON  
{  
  "providers": {  
    "openrouter": {  
      "baseUrl": "https://openrouter.ai/api/v1",  
      "api": "openai-completions",  
      "apiKey": "openrouter",  
      "authHeader": true,  
      "models":  
            }  
          }  
        },  
        {  
          "id": "openai/gpt-5.4-mini",  
          "name": "GPT 5.4 Mini (Summary Router)",  
          "reasoning": false,  
          "contextWindow": 128000,  
          "maxTokens": 16384,  
          "cost": {  
            "input": 0.15,  
            "output": 0.60,  
            "cacheRead": 0,  
            "cacheWrite": 0  
          }  
        },  
        {  
          "id": "meta/llama-4-405b-free",  
          "name": "Llama 4 405B (Rate Limit Fallback)",  
          "reasoning": false,  
          "contextWindow": 128000,  
          "maxTokens": 8192  
        }  
      \]  
    }  
  }  
}

**File: .pi/settings.json (Project-Level Settings)**

JSON  
{  
  "defaultProvider": "openrouter",  
  "defaultModel": "anthropic/claude-opus-4-7",  
  "defaultThinkingLevel": "medium",  
  "summary": {  
    "enabled": true,  
    "model": "openrouter/openai/gpt-5.4-mini",  
    "thinking": "low"  
  },  
  "compaction": {  
    "enabled": true,  
    "reserveTokens": 16384,  
    "keepRecentTokens": 20000  
  },  
  "retry": {  
    "enabled": true,  
    "maxRetries": 3,  
    "baseDelayMs": 3000,  
    "provider": {  
      "timeoutMs": 3600000,  
      "maxRetryDelayMs": 60000  
    }  
  }  
}

The integration of the compat.openRouterRouting parameter within the anthropic/claude-opus-4-7 model block dictates that OpenRouter will attempt to serve the primary inference request utilizing Anthropic's direct infrastructure first.3 If a 429 Rate Limit occurs, the allow\_fallbacks: true directive authorizes OpenRouter to instantaneously reroute the request to Amazon Bedrock or Google Vertex instances hosting the identical Claude Opus weights.18 By offloading the recurring summary tasks exclusively to openai/gpt-5.4-mini via the summary block in settings.json, the agent fleet avoids burning high-cost Opus tokens on routine context compaction.11 This strategy, combined with the hard API limit set externally, is fundamentally necessary to maintain operations within the strict $5/day mathematical boundary dictated by the environment.

## **8\. Sources**

The architectural assertions, API mapping logic, and configuration syntax detailed throughout this report rely upon the official documentation for both the Pi Coding Agent platform and the OpenRouter gateway.

1. 1 Pi.dev Platform Homepage. Accessed May 21, 2026\. https://pi.dev/  
2. 2 Pi.dev Official Documentation: Overview and Settings. Accessed May 21, 2026\. https://pi.dev/docs/latest  
3. 7 Pi.dev Official Documentation: Settings and Caps. Accessed May 21, 2026\. https://pi.dev/docs/latest/settings  
4. 3 Pi.dev Official Documentation: Custom Models and Provider Overrides. Accessed May 21, 2026\. https://pi.dev/docs/latest/models  
5. 2 Pi.dev Official Documentation: General Contents, Sessions, and TUI. Accessed May 21, 2026\. https://pi.dev/docs/latest/quickstart  
6. 18 OpenRouter Official Documentation: Provider Selection and Routing. Accessed May 21, 2026\. https://openrouter.ai/docs/guides/routing/provider-selection  
7. 4 Pi.dev Official Documentation: Providers and API Keys. Accessed May 21, 2026\. https://pi.dev/docs/latest/providers  
8. 15 Pi Packages: @baggiiiie/pi-goal. Accessed May 21, 2026\. https://pi.dev/packages/@baggiiiie/pi-goal  
9. \[16\] Pi Packages: @capyup/pi-goal. Accessed May 21, 2026\. https://pi.dev/packages/@capyup/pi-goal  
10. 10 Pi.dev Official Documentation: Compaction. Accessed May 21, 2026\. https://pi.dev/docs/latest/compaction  
11. 13 Pi.dev OpenRouter Model Mapping (Claude Opus 4.7). Accessed May 21, 2026\. https://pi.dev/models/openrouter/anthropic-claude-opus-4  
12. 6 Pi Packages: @vtstech/pi-openrouter-sync. Accessed May 21, 2026\. https://pi.dev/packages/@vtstech/pi-openrouter-sync  
13. 3 Pi.dev Official Documentation: Models and Routing (openRouterRouting). Accessed May 21, 2026\. https://pi.dev/docs/latest/models  
14. 11 Pi Packages: @howaboua/pi-subagent-review (Summarization Config). Accessed May 21, 2026\. https://pi.dev/packages/@howaboua/pi-subagent-review  
15. 9 Pi Packages: @plannotator/pi-extension (Plan Mode). Accessed May 21, 2026\. https://pi.dev/packages/@plannotator/pi-extension  
16. 8 Pi Packages: @dreki-gg/pi-plan-mode. Accessed May 21, 2026\. https://pi.dev/packages/@dreki-gg/pi-plan-mode  
17. 12 Pi.dev Official Documentation: RPC Mode and Turn Logging. Accessed May 21, 2026\. https://pi.dev/docs/latest/rpc  
18. 19 OpenRouter Official Documentation: Model Fallbacks. Accessed May 21, 2026\. https://openrouter.ai/docs/guides/routing/model-fallbacks  
19. \[5\] OpenRouter Official Documentation: Pricing and Limits. Accessed May 21, 2026\. https://openrouter.ai/pricing  
20. \[14\] OpenRouter Official Documentation: Support and FAQ. Accessed May 21, 2026\. https://openrouter.ai/support  
21. 19 OpenRouter API Reference: Model Fallbacks Array. Accessed May 21, 2026\. https://openrouter.ai/docs/guides/routing/model-fallbacks  
22. \[20\] OpenRouter API Reference: Call Model. Accessed May 21, 2026\. https://openrouter.ai/docs/agent-sdk/call-model/api-reference  
23. 18 OpenRouter Official Documentation: Provider Selection (allow\_fallbacks). Accessed May 21, 2026\. https://openrouter.ai/docs/guides/routing/provider-selection  
24. 17 OpenRouter Community Forum: Setting API Limits and Caps. Accessed May 21, 2026\. https://www.reddit.com/r/openrouter/comments/1sxaxd8/how\_do\_i\_set\_a\_max\_token\_cost\_limit\_on\_openrouter/

#### **Works cited**

1. Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/](https://pi.dev/)  
2. Pi Documentation · Docs · Pi \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/docs/latest](https://pi.dev/docs/latest)  
3. Custom Models · Docs \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/docs/latest/models](https://pi.dev/docs/latest/models)  
4. Providers · Docs \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/docs/latest/providers](https://pi.dev/docs/latest/providers)  
5. Pricing \- OpenRouter, accessed May 21, 2026, [https://openrouter.ai/pricing](https://openrouter.ai/pricing)  
6. vtstech/pi-openrouter-sync \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/packages/@vtstech/pi-openrouter-sync](https://pi.dev/packages/@vtstech/pi-openrouter-sync)  
7. Settings · Docs \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/docs/latest/settings](https://pi.dev/docs/latest/settings)  
8. dreki-gg/pi-plan-mode \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/packages/@dreki-gg/pi-plan-mode](https://pi.dev/packages/@dreki-gg/pi-plan-mode)  
9. plannotator/pi-extension · Packages \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/packages/@plannotator/pi-extension](https://pi.dev/packages/@plannotator/pi-extension)  
10. Compaction & Branch Summarization \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/docs/latest/compaction](https://pi.dev/docs/latest/compaction)  
11. howaboua/pi-subagent-review \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/packages/@howaboua/pi-subagent-review](https://pi.dev/packages/@howaboua/pi-subagent-review)  
12. RPC Mode · Docs \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/docs/latest/rpc](https://pi.dev/docs/latest/rpc)  
13. Anthropic: Claude Opus 4 \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/models/openrouter/anthropic-claude-opus-4](https://pi.dev/models/openrouter/anthropic-claude-opus-4)  
14. Support | OpenRouter, accessed May 21, 2026, [https://openrouter.ai/support](https://openrouter.ai/support)  
15. baggiiiie/pi-goal \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/packages/@baggiiiie/pi-goal](https://pi.dev/packages/@baggiiiie/pi-goal)  
16. capyup/pi-goal \- Pi Coding Agent, accessed May 21, 2026, [https://pi.dev/packages/@capyup/pi-goal](https://pi.dev/packages/@capyup/pi-goal)  
17. How do I set a max token / cost limit on OpenRouter API key? \- Reddit, accessed May 21, 2026, [https://www.reddit.com/r/openrouter/comments/1sxaxd8/how\_do\_i\_set\_a\_max\_token\_cost\_limit\_on\_openrouter/](https://www.reddit.com/r/openrouter/comments/1sxaxd8/how_do_i_set_a_max_token_cost_limit_on_openrouter/)  
18. Provider Routing | Intelligent Multi-Provider Request Routing ..., accessed May 21, 2026, [https://openrouter.ai/docs/guides/routing/provider-selection](https://openrouter.ai/docs/guides/routing/provider-selection)  
19. Model Fallbacks | Reliable AI with Automatic Failover | OpenRouter ..., accessed May 21, 2026, [https://openrouter.ai/docs/guides/routing/model-fallbacks](https://openrouter.ai/docs/guides/routing/model-fallbacks)  
20. API Reference | OpenRouter SDK, accessed May 21, 2026, [https://openrouter.ai/docs/agent-sdk/call-model/api-reference](https://openrouter.ai/docs/agent-sdk/call-model/api-reference)