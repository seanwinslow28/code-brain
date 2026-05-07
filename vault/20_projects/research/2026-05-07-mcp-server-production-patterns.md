---
type: research-report
project: prj-job-hunt-2026
research_topic: mcp-server-production-patterns-2026
created: 2026-05-07
model: gemini-deep-research-max
agent: deep-research-max-preview-04-2026
interaction_id: v1_ChdlTkQ4YWN2UkpkRFVfdU1QOElheDhROBIXZU5EOGFjdlJKZERVX3VNUDhJYXg4UTg
runner: gemini_dr_stream.py (stream=True) → gemini_dr_save.py recovery
input_tokens: 3090514
output_tokens: 94180
tool_use_tokens: 1554067
thought_tokens: 115244
cached_tokens: 731136
total_tokens: 4854005
ai-context: "Grounding context for the intent-engineering MCP server v0 build (target ship 2026-05-25). All load-bearing claims cited; uncited claims flagged. Recovered after first DR Max attempt wedged without billing; second attempt via stream mode succeeded."
---

---
type: research-report
project: prj-job-hunt-2026
research_topic: mcp-server-production-patterns-2026
created: 2026-05-06
model: gemini-deep-research-max
ai-context: "Grounding context for the intent-engineering MCP server v0 build (target ship 2026-05-25). All load-bearing claims cited; uncited claims flagged."
---

# MCP Server Production Patterns 2026 — Reference for `intent-engineering` v0

## Executive Summary
For the 19-day `intent-engineering` v0 build, the required architectural decisions are clear and unambiguous:
*   **Target Stack:** Use the canonical `@modelcontextprotocol/sdk` for TypeScript via Node.js LTS (v20 or higher) [cite: 1].
*   **Tool Registration Paradigm:** Utilize the `McpServer` wrapper class and Zod for automatic JSON-Schema generation and seamless tool routing, entirely avoiding low-level protocol event listeners [cite: 2, 3].
*   **Transport Choice:** **Stdio** is the mandatory, non-negotiable transport layer for the local Claude Desktop demonstration target, avoiding network configurations and CORS completely [cite: 4, 5]. 
*   **Build Timeline Focus:** Prioritize early transport validation (Stdio protocol connections) in Days 1-3, heavy AI logic implementation in Days 4-9, schema validation with the official MCP Inspector in Days 10-13, and registry publishing via the `mcp-publisher` CLI in the final week [cite: 6, 7, 8].

As you approach the 19-day build window for the `intent-engineering` MCP server v0, technical pragmatism is paramount. The Model Context Protocol (MCP) ecosystem has evolved rapidly, and the margin between a robust, recruiter-grade demonstration and a brittle, failing prototype often comes down to undocumented transport behaviors and schema validation edge cases. This document serves as the canonical reference for both you (the PM) and Claude Code to scaffold the implementation reliably. 

The following sections synthesize current specifications from Anthropic's official SDKs, the `modelcontextprotocol` GitHub organization, and verified community production patterns. Complex architectural decisions have been reduced to clear, binary recommendations suited for a 2-3 hour daily development bandwidth. 

## 1. The Current SDK Reality

To ensure maximum credibility during a 5-minute technical review by a senior engineer, the `intent-engineering` server must utilize the canonical tools without falling back on legacy wrappers or community forks. The core reality of the MCP TypeScript ecosystem revolves around the `@modelcontextprotocol/sdk` package, which abstracts the underlying JSON-RPC (a stateless, lightweight remote procedure call protocol encoded in JSON) protocol operations.

### Package and Version Requirements
The canonical repository owner is the `modelcontextprotocol` GitHub organization, and the first-party TypeScript implementation lives at `github.com/modelcontextprotocol/typescript-sdk` [cite: 9, 10]. On npm, this is published exclusively as `@modelcontextprotocol/sdk` [cite: 11]. 

Node version requirements present a slight contradiction depending on whether you adopt the stable v1.x line or the incoming v2.x line. The v1.x releases require Node `≥18` [cite: 12, 13]. However, the v2.0.0-alpha development branch explicitly targets Node `≥20` in its `package.json` `engines` field [cite: 1]. To future-proof the 19-day build and avoid phantom bugs during deployment, the project should target Node 20 LTS or higher. Furthermore, the SDK explicitly requires `zod` (a TypeScript-first schema declaration and validation library) as a peer dependency for schema validation, supporting both Zod v3 and the upcoming Zod v4 [cite: 11, 14].

### The Minimum-Viable Server Skeleton
The project layout must embrace modern ECMAScript modules (ESM) to align with Anthropic's first-party patterns. The `package.json` must include `"type": "module"` and utilize a dual development/build script strategy [cite: 1, 13, 15]. 

*   **Development:** Use `tsx` (TypeScript Execute) to run the server directly from source during local testing.
*   **Production Build:** Use `tsc` to compile to a `dist` directory for the final npm package.

The following illustrates the exact minimum-viable server skeleton required to register a tool using the `McpServer` class rather than the legacy, low-level JSON-RPC handler:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// 1. Initialize the MCP Server
const server = new McpServer({
  name: "intent-engineering-server",
  version: "1.0.0"
});

// 2. Register the 'analyze_intent_spec' Tool
server.registerTool(
  "analyze_intent_spec",
  {
    title: "Analyze Intent Spec",
    description: "Reads a product/feature spec and reports gaps in intent clarity",
    inputSchema: {
      spec_text: z.string().describe("The raw text of the product spec to analyze")
    }
  },
  async ({ spec_text }) => {
    // Implementation logic here
    const gaps = await analyzeSpec(spec_text);
    
    return {
      content: [
        { type: "text", text: `Found ${gaps.length} gaps: ${JSON.stringify(gaps)}` }
      ]
    };
  }
);

// 3. Connect via Stdio Transport
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Breaking Changes Since Early 0.x
Early MCP tutorials often referenced a low-level SDK approach requiring manual JSON-RPC request handling and manual schema validation. The current SDK abstracts this entirely via `McpServer.registerTool()` and `McpServer.registerResource()` [cite: 11, 14]. You should reject any generated code from Claude that attempts to manually parse `tools/call` JSON-RPC messages. Rely entirely on the `McpServer` wrapper, which handles protocol routing internally [cite: 14, 16].

**Confidence: HIGH.** The `@modelcontextprotocol/sdk` package, Node engine requirements, and `McpServer` instantiation patterns are consistently triangulated across Anthropic's SDK source code, npm registry data, and verified community tutorials.

## 2. Tool Registration & Schema Validation

Tools are the primary contract between an LLM and the `intent-engineering` server. They are designed to be model-controlled—meaning the AI dynamically decides which tool to invoke and constructs the arguments based on the schema you provide [cite: 11, 14, 17]. 

### Declaring Tools and Handling Optional Parameters
The `registerTool` method handles both the `tools/list` (discovery) and `tools/call` (invocation) phases of the protocol. When you define the `inputSchema` using Zod, the SDK automatically translates this into JSON Schema for the LLM during the `tools/list` phase [cite: 2, 3].

Your `audit_existing_spec` tool requires a specific input shape: it must accept either a `file_path` OR inline `spec_text`. The canonical way to represent optional parameters in Zod for MCP is using `.optional()`, accompanied by robust runtime validation inside the callback. 

```typescript
server.registerTool(
  "audit_existing_spec",
  {
    title: "Audit Existing Spec",
    description: "Accepts a file path or inline spec text and returns a structured audit",
    inputSchema: {
      file_path: z.string().optional().describe("Absolute path to the spec file on disk"),
      spec_text: z.string().optional().describe("Raw text of the spec to audit if no file is provided")
    }
  },
  async ({ file_path, spec_text }) => {
    if (!file_path && !spec_text) {
      return {
        isError: true,
        content: [{ type: "text", text: "You must provide either file_path or spec_text." }]
      };
    }
    
    // Process input...
    return { content: [{ type: "text", text: "Audit complete." }] };
  }
);
```

### Error Handling: `isError` vs Protocol Failures
Error handling is a critical failure point for novice MCP developers. The MCP protocol distinguishes strictly between two types of errors: **Protocol Errors** and **Tool Execution Errors** [cite: 2, 18].

1.  **Protocol Errors:** These occur when the JSON-RPC message is malformed, a tool name doesn't exist, or the server entirely crashes. The SDK handles these automatically, but when they occur, Claude Desktop typically aborts the tool call and the AI receives no contextual feedback [cite: 18, 19].
2.  **Tool Execution Errors:** These occur when the tool logic fails (e.g., a file is not found, or an API key is missing). If you throw a raw TypeScript exception, it becomes a Protocol Error and breaks the workflow [cite: 18].

**The Solution:** You must catch logical exceptions and return a successful JSON-RPC payload containing `isError: true`. By returning `isError: true` along with a descriptive text payload, the error is injected directly back into the LLM's context window [cite: 17, 19]. Claude can then read your error message ("File not found at path /temp/spec.md") and autonomously attempt to fix the problem by calling the tool again with a corrected argument [cite: 18, 19]. 

**Preventing the Infinite Retry Loop:** If Claude tries again and fails, it risks entering an infinite retry loop, burning through tokens and context limits. To prevent this, implement a local execution counter within the tool's runtime state to hard-fail the operation after a fixed number of retries (e.g., 3 attempts), or explicitly instruct the LLM in the error payload text: *"File not found. Do not retry this path more than once."*

**Confidence: HIGH.** The distinction between protocol-level JSON-RPC errors and the application-level `isError: true` flag is explicitly documented in the official MCP specifications and heavily corroborated by advanced implementer tutorials.

## 3. Transport Choice Matrix

The Model Context Protocol establishes communication through a defined transport layer. In protocol version 2024-11-05 and later, the matrix is strictly defined among three choices: Stdio, Server-Sent Events (SSE), and Streamable HTTP [cite: 4, 5]. Selecting the wrong transport will guarantee failure during the Claude Desktop demo.

| Transport Type | When to Use | Why it Works | Key Limitations |
| :--- | :--- | :--- | :--- |
| **Stdio** (Standard I/O) | Local integrations, desktop apps, CLI tools. | The MCP client launches the server as a local subprocess, bypassing CORS (Cross-Origin Resource Sharing, a mechanism that allows restricted resources on a web page to be requested from another domain) and network configurations entirely [cite: 4, 11]. | Ties the server to the local machine. Strictly reserves `stdout` for protocol messages; stray output causes silent crashes [cite: 5, 20]. |
| **Streamable HTTP** | Remote, hosted servers handling concurrent clients over the web. | Operates as an independent daemon exposing a single HTTP endpoint for POST and GET requests, serving as a unified gateway [cite: 5, 21]. | Exposes internet routing complexities. Requires OAuth/Token authentication and persistent session management [cite: 4, 22]. |
| **SSE** (Server-Sent Events) | Legacy remote web-based environments. | Allowed real-time, event-streamed communication [cite: 23]. | Officially marked as **deprecated** in recent MCP specs for backwards compatibility only. Avoid for v0 builds [cite: 11, 24]. |

### Concrete Recommendation for `intent-engineering`
**You must use the Stdio transport.** Anthropic explicitly advises that clients (like Claude Desktop) should support stdio whenever possible, and it is the default starting point for custom MCP development [cite: 4, 5, 11]. Because your 19-day v0 target assumes a local Claude Desktop demo, Stdio requires zero overhead for network security or hosting architecture. The server simply spawns, executes, and terminates alongside the Claude Desktop session. 

If a hosted version becomes necessary in the future, the `@modelcontextprotocol/sdk` allows you to swap `StdioServerTransport` for `StreamableHTTPServerTransport` with only two lines of code [cite: 11, 14, 25].

**Confidence: HIGH.** The deprecation of SSE, the definition of Streamable HTTP, and the recommendation of Stdio for local subprocess execution is sourced directly from the official MCP specification (versions 2024-11-05 to 2025-11-25) and Anthropic's introductory guides.

## 4. Top Exemplary Public MCP Servers

To pass a senior FDE engineer's "smell test," the `intent-engineering` server should mirror the structural patterns of the most heavily adopted open-source MCP implementations. The following servers demonstrate the gold standard for robust TS/JS execution.

### 1. The Everything Server (`modelcontextprotocol/server-everything`)
*   **Repo:** [github.com/modelcontextprotocol/servers/tree/main/src/everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything)
*   **Tools:** Exposes dummy tools like `echo`, resources, and prompts to exercise the entire protocol [cite: 26, 27, 28].
*   **What to copy:** Its transport initialization logic. As the official reference test server, it gracefully handles flags to switch between Stdio, SSE, and Streamable HTTP [cite: 26, 27]. Copy its clean separation of protocol initialization from business logic.

### 2. The Filesystem Server (`modelcontextprotocol/server-filesystem`)
*   **Repo:** [github.com/modelcontextprotocol/servers/tree/main/src/filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
*   **Tools:** `read_file`, `write_file`, `search_files`, `list_directory_with_sizes` [cite: 28, 29, 30].
*   **What to copy:** Security via path normalization. The server strictly prevents directory traversal attacks by validating all tool inputs against an `allowedDirectories` array passed via command-line arguments, actively resolving symlinks to prevent bypass [cite: 30, 31]. If your `audit_existing_spec` tool reads files, adopt this strict directory-scoping pattern.

### 3. Microsoft MarkItDown (`microsoft/markitdown`)
*   **Repo:** [github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
*   **Tools:** Converts PDFs, PPTs, and Word docs into clean Markdown for LLM consumption [cite: 32, 33, 34].
*   **What to copy:** The wrapper paradigm. MarkItDown does not build the conversion engine inside the MCP server; it treats the MCP server as a thin API wrapper around an existing, highly tested Python utility library [cite: 32, 34]. Your `intent-engineering` tools should follow this exactly: write the logic in isolated modules, and use the MCP server purely for I/O routing.

### 4. The Fetch Server (`modelcontextprotocol/server-fetch`)
*   **Repo:** [github.com/modelcontextprotocol/servers/tree/main/src/fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
*   **Tools:** A single tool to fetch and convert web content to markdown [cite: 28, 35, 36].
*   **What to copy:** Pagination and truncation for context windows. It utilizes `max_length` and `start_index` parameters to chunk massive payloads [cite: 37, 38]. Without pagination, large responses can cause memory exhaustion and LLM performance degradation. It manages this using cursor-based parsing [cite: 39]. If your `audit_existing_spec` target is a massive PRD, you must implement this parameter pattern.

### 5. Git Server (`modelcontextprotocol/server-git`)
*   **Repo:** [github.com/modelcontextprotocol/servers/tree/main/src/git](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
*   **Tools:** Reads, searches, and manipulates Git repositories [cite: 28].
*   **What to copy:** Segregation of read-only vs mutative actions. It cleanly separates state-altering tool schemas from non-destructive reads. This clarity in tool description is vital for model performance and safety when asking for user permission to execute actions.

**Confidence: HIGH.** All listed repositories belong to verified organizations (`modelcontextprotocol`, `microsoft`). The implementation details cited are drawn directly from their respective READMEs and source code files.

## 5. README + Discoverability Conventions

A recruiter-grade repository is evaluated heavily on developer experience (DX). In the MCP ecosystem, a stellar README provides frictionless onboarding for the primary test client: Claude Desktop. 

### Configuring Claude Desktop
Claude Desktop manages local Stdio MCP servers via a specific configuration file. On macOS, this is located at `~/Library/Application Support/Claude/claude_desktop_config.json`; on Windows, `%APPDATA%\Claude\claude_desktop_config.json` [cite: 29]. Your README must provide a literal, copy-pasteable JSON block for this file [cite: 40, 41].

Include this exact structure in your install instructions, customized for `intent-engineering`:

```json
{
  "mcpServers": {
    "intent-engineering": {
      "command": "node",
      "args": [
        "/absolute/path/to/intent-engineering/dist/index.js"
      ],
      "env": {
        "OPTIONAL_API_KEY": "..."
      }
    }
  }
}
```
*Note: Strongly emphasize to users that paths in this JSON file must be absolute; relative paths will cause silent failures [cite: 29, 42].*

### Registry Submission & The Server Manifest
The official MCP Registry is located at `registry.modelcontextprotocol.io` [cite: 43, 44]. It is crucial to understand that this is a *metaregistry*. It does not host your code (which remains on GitHub and npm); it hosts standardized metadata enabling discovery by clients and aggregators [cite: 43, 45].

To achieve a "registry-accepted" status, you must:
1.  **Create a `server.json` manifest:** This file defines your server's metadata, namespace, and package location.
2.  **Verify Namespace:** The registry enforces namespace ownership. If using GitHub authentication via OAuth, the name must map to `io.github.yourusername/server-name` [cite: 46, 47]. *Warning: The validator enforces strict remote URL matching for `io.github.*` namespaces, which can occasionally cause friction for non-standard deployments [cite: 46].* Alternatively, custom domains require `com.example/server-name` format verified via a DNS TXT record containing a registry token [cite: 46, 47].
3.  **Publish via CLI:** Use the official `mcp-publisher` CLI tool (`brew install mcp-publisher`). You initialize the project (`mcp-publisher init`), authenticate (`mcp-publisher login github`), and execute the upload (`mcp-publisher publish`) [cite: 7, 8, 48].

A recruiter-grade README should include badges for npm version, MIT License, and ideally an "MCP Registry" badge if applicable, followed by a Loom embed demonstrating Claude executing the `generate_template` tool, as visual proof is vastly superior to textual logs.

**Confidence: HIGH.** The configuration shape for Claude Desktop is universally documented. The registry submission mechanics are directly sourced from the `registry.modelcontextprotocol.io` API documentation, publishing guides, and `mcp-publisher` CLI references.

## 6. Common Antipatterns and Failure Modes

During a rapid 19-day build, debugging invisible protocol errors can destroy your timeline. The following are the most pervasive failure modes in the MCP community and how to sidestep them.

### 1. `console.log()` Corrupting the Stdio Stream (The #1 Bug)
When running over the Stdio transport, the server reads from `stdin` and writes JSON-RPC protocol messages strictly to `stdout` [cite: 4, 20]. **Any non-protocol text written to stdout will fatally corrupt the JSON-RPC stream.**
*   **The Failure:** Developers leave a stray `console.log("Tool called")` in their code. The client receives malformed JSON and throws a `-32700 Parse error` or simply disconnects silently. (*anecdotal — uncited*)
*   **The Fix:** You must route all diagnostic logging to `stderr`. Use `console.error()` for debugging, as the MCP specification explicitly allows `stderr` to be used for UTF-8 logging strings without interrupting the protocol [cite: 20, 24, 49].

### 2. Message Size Limits on Long Inputs
*   **The Failure:** When tools return massive payloads (like dumping a 30-page raw product spec), it can exceed the LLM's client-side text output limitations, resulting in an "Unexpected End JSON" crash. (*anecdotal — uncited*)
*   **The Fix:** Do not assume unlimited context. Implement chunking arguments in your tool schema (e.g., `start_index` and `max_length`), forcing the model to paginate through large specs iteratively, mirroring the pattern used in the official `fetch` server [cite: 35, 37].

### 3. Schema Drift Between Code and Prompts
*   **The Failure:** The tool's Zod `inputSchema` accepts `file_path`, but the internal tool logic expects `filePath` (camelCase). Because MCP relies on the LLM dynamically generating JSON based *exactly* on the Zod schema, the tool call fails runtime validation. (*anecdotal — uncited*)
*   **The Fix:** Rely entirely on TypeScript interface inference from your Zod objects (`type ToolInput = z.infer<typeof ToolSchema>`) rather than maintaining separate TS interfaces [cite: 13].

### 4. Permission Model Assumptions & Missing Annotations
*   **The Failure:** A server assumes that the LLM understands implicit bounds for read/write operations or external network calls, leading to potential data exfiltration or unintended state changes. For example, the official `@modelcontextprotocol/server-fetch` initially lacked tool annotations, creating a vector where an agent could chain a read from a local tool into an outbound fetch.
*   **The Fix:** Explicitly annotate your tools. Issue #3572 (`https://github.com/modelcontextprotocol/servers/issues/3572`) requested adding `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` directly into the tool schema to help clients enforce "allow reads, gate sends" policies accurately [cite: 50].

### 5. Swallowing Execution Errors
*   **The Failure:** An API call inside `analyze_intent_spec` times out. The server throws an uncaught exception, crashing the process, or returns an empty string. The LLM hallucinates a success state or the conversation abruptly ends. (*anecdotal — uncited*)
*   **The Fix:** As detailed in Section 2, wrap tool execution in a `try/catch` block. Catch the error, stringify it into human-readable instructions, and return it with `isError: true` so the LLM can auto-recover [cite: 17, 19].

### 6. Transport Mismatch
*   **The Failure:** A server is instantiated with `StreamableHTTPServerTransport`, but the user configures Claude Desktop to launch it directly via the `command`/`args` JSON config (which implicitly expects Stdio). The server hangs indefinitely waiting for HTTP POSTs that never arrive. (*anecdotal — uncited*)
*   **The Fix:** Hardcode `StdioServerTransport` for this v0 build.

**Confidence: HIGH.** The `stdout` corruption issue is widely documented as the most prevalent hurdle. The lack of permission annotations is directly sourced from GitHub issue discussions within the core `modelcontextprotocol` repository [cite: 50].

## 7. The 19-Day Build Path for a Beginner-to-Intermediate TS Coder

Given a constraint of 2-3 hours per day over 19 days (excluding weekends, leaving roughly 13-14 active workdays), micromanaging hours will fail. Instead, block the timeline into milestones that heavily leverage AI scaffolding.





### Phase 1: Skeleton and Infrastructure (Days 1–3)
*   **Day 1:** Initialize the Node project (`npm init -y`, `npm i @modelcontextprotocol/sdk zod`). Set `package.json` to `"type": "module"` and target Node 20 (`engines: { "node": ">=20" }`).
*   **Day 2:** Scaffold the `McpServer` class and `StdioServerTransport`. Do not roll your own routing. Lean on Claude Sonnet to generate the boilerplate `tsconfig.json` and build scripts.
*   **Day 3:** Register a dummy "ping" tool. Configure your local `claude_desktop_config.json` to point to the built `dist/index.js`. Verify connection in Claude Desktop. *If this fails, check for `console.log` statements.*

### Phase 2: Core Tool Implementation (Days 4–9)
*   **Days 4–5:** Implement `analyze_intent_spec`. Define the Zod schema. Since this involves parsing logic, use Claude Opus for the complex prompt/regex extraction logic underlying the tool. Wrap the execution in a `try/catch` returning `isError: true`.
*   **Days 6–7:** Implement `generate_template`. Ensure the returned content array is formatted cleanly.
*   **Days 8–9:** Implement `audit_existing_spec`. Define the Zod union for `file_path` (optional) and `spec_text` (optional). If reading from the filesystem, ensure you use `path.resolve` and normalize paths to prevent directory traversal, mimicking the official `filesystem` server. Implement the `start_index` and `max_length` pagination arguments to prevent memory exhaustion [cite: 37, 39].

### Phase 3: Testing and Hardening (Days 10–13)
*   **Days 10–11:** Use the official MCP Inspector (`npx @modelcontextprotocol/inspector`) to test tool schemas and trace JSON-RPC calls without launching the full Claude Desktop client [cite: 6, 14, 51]. The Inspector proxies JSON-RPC requests via a web UI, making it trivial to spot Zod schema mismatches before integration testing.
*   **Days 12–13:** E2E testing in Claude Desktop. Stress-test the 20k token limit by feeding `audit_existing_spec` a massive file. Implement basic error feedback loops to ensure Claude can recover from bad file paths automatically.

### Phase 4: Polish and Delivery (Days 14–19)
*   **Days 14–15:** Refactor all `console.log` statements to `console.error` [cite: 49]. Finalize the `package.json` metadata (author, license, keywords).
*   **Days 16–17:** Draft the recruiter-grade README. Include the mandatory `claude_desktop_config.json` setup block, clear architectural explanations, and a Loom demonstration.
*   **Days 18–19:** Prepare the `server.json` manifest. Publish the actual package to npm. Execute `brew install mcp-publisher`, authenticate via `mcp-publisher login github`, and run `mcp-publisher publish` to submit the metadata to `registry.modelcontextprotocol.io` [cite: 7, 8].

**Cost-Aware AI Usage:** Use Haiku or Sonnet for boilerplate scaffolding, repetitive Zod schema typing, and `package.json` generation. Reserve Opus strictly for debugging JSON-RPC failures, defining the core heuristic logic inside `analyze_intent_spec`, and writing the final README prose. 

**Confidence: MEDIUM.** While the timeline is a synthesized recommendation rather than a protocol spec, it is grounded in the operational realities of the SDK's learning curve, specifically prioritizing early transport validation (Day 3) to prevent late-stage protocol blocking.



**Sources:**
1. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGZTz31lJ5jrgU68fc_Jfth6utWAUIcHQZkDkXG_d55-wVhpeNZBZS-pnzaZ1gURWLxklqxsJNgnuQ2tH8euWtX1SDTTEJIngZMGJlo0ILWMav6yoNJeX27V9mFkEvH6IaEsxpOLrIajFDKT49krL9whdBttdzcLtkuVO51I6fOnqxw)
2. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGYeUVGL-OcCuMzrBRZt2mM_WkpVadi5rY3rpHpVhYgvFidt7518v8GjChZSSzFOStKKRtY8b8uI6QFTz1VPcLkFLl_R5g9Naa8tsYw4ZmNVojpQvxrDHiCWOz6FPYDsLNFwS-zWzIbqXluFGbF3A61CWgzzmpbWHsQ_g==)
3. [typia.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGgBszjoX8QK-YK28NGrqwgi0OoYoLP8HDm3-ImsDborIQ8LR5a5IbI1Nl50n5nz1X0hk2JlQvUtsksrl0lw1ZlZHGojYA7VhlwG2QnmuLkZzmGVFX3M9IbWofL)
4. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGzrWDUJMcA-Johjj_JUK6GWp5CddFPAXUEAVfgYXDF_6ZAss0SHtTH83zPfqCVRU_vqw2hUmQFKDZl15IMwO6e40YWKYyS1OpqWimsJ6nYidinVeSs2-VoXCIM3dYpcy2gLUL08tCFNlqmyk08AAA5KF-5u_I9885DKj2KtDQ=)
5. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLtS9318_x6UjnXmJg20FaRfo7USc2e6v2_Ui7qjQsBFc2EUjO-6MCmgkGrQYKyjBXiIMh_oBSk-GAL6ncZI-7j1TaSZSQ5eImtmr7TgZEfosjMomZpBEPJRvo2E2bi6bDcOwUavld68U3C3E-DouLEJUa5e7RJ67OzHwp7PQ=)
6. [augmentcode.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHM0Ylw7oSaPbpA0HjSh_utwdKOIfbX2fSv9gyAlmqZ6fpyN98MlLvPydOaMWGKqi42zt31ukt-k8LgmzWYI806Gp60VjbHNmshG31my1kgU9O7-pQt76ATZ2jhO6opyblU5A==)
7. [modelcontextprotocol.info](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5puBs9il9PNid5POkeF9o9D3dIZx49rNJhm-tLcvJxlptD-iRdvOr-3s_GHKtnxd6NImNSDuJFszN12QPsT8fW1FLYMNk2Ob_o-Aqh7VFDUswWAvIXmzuc5y7y7u2lCprigLzr33tBxGm)
8. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3iBkJiiHHI3pOvdw9FAIPp-APNZy1TbFOemv7VouaslhVU-bE2R9SWYqBitBw0dmfYKe05Uz9rrIVCMdJ0wfCo_e5Tndo4tLL5UGH1rpBpUB6wouX6VgfXj7-eGfacWST4ccrHlL9xg==)
9. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHggw9DDLTy7UUeIpMKmgv3JIzQGO51H8PT-Nz4-kpMp-X4mUmH8-bbUzmQLRJhAozHvNicvLdsqceXWDJh-luDtncCg10I3E-9Sak9jAhWT0JbhUebIsPBHAgQUQ==)
10. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEEuwAmRl4fk5kc_vM4VFQhSfAqr6EbGT0Aq4ZHpDxYysxaGOTFJX0fkTX3HEA1bGYIp29UzniCflh3vMhIoi96BWwWmZSaT7-YmO47gq2kZeVhRVNSjbrDVGx54F0oskwee6_44kk3y7cBLw==)
11. [npmjs.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGEYw-_tZ8juKvYl7ykS4TgH0zymLQLr_bkNOW29KcwNzbytgQjiXkrQDZNpopnLwzJxi-LwVN_FlJqsmxcPlMIKWNJI3Ah04HrOwrxDpblCscZeqqXEb-5Qnvu8cNyXXkewcZFDrFzyEkDZwg=)
12. [shinzo.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGQc9UIqBPgX6mZUPlr_dnv0ee_LaXM9pEyApFi3zDTlPaoE1c4Dg1C3gNMrYUWulWPTjZx4pZ5M1_zO0h0BjadxVFlcoFrC-IHZJB3dfisXLLn2NhSzjdIO1weDOmzNExVB3zLlliw84J8OVP0Bqbp86NufQ==)
13. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFs43OiYNjH-X2GDDLM9Dxs1wLhyDiCE3XWEdGhkEpSyqcM50vuO19BxKBvrCEEQ9IVwHM_EKBwbkvMrnJ13ZCMzCz4nos31i8msnSkrESgtgVd7W2m4Q-AkOrexUWrmEHAW3N_byXK7ypIGXkJzH8RSOsUK600SWsopNFReVeW4sHsdGBJmv0CLdD7aJqilQ97Ek4=)
14. [npmjs.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHN4m9WneRYj5BmdxvA7mSJnlIz8RuE12X_GRIUt7pDY-oQ-ENn6SlEY-a6WuegjKow8XcTlcT_0-RunG2fEgop-DQNP7NJWJhuNjmI7hj3bdx6kAefkUClHad_maYH8dERdbVnNVtjmEhdgKxGpRwWW7qncA==)
15. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLA6RX4rmv9ntpiy28QrdsQ4ZbVTZVZOFTQTEZ-lgNfkOP8ur12BtC9NiWFFVD2jFpUOhSy-H9Sb8aAarlbyEn66amPDE70pN2sQ5YOeUsTPafpxdCJlxzjXL-qrgKqnEXP_ZtK6z79r-5HXJWyg==)
16. [holt.courses](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbJ4i8pXd1iXCK-_f1U_DvplJu0DagvM8qvk6uf_6Jo5rFhTtWcggmpZjDIb2u-OmKeU2Fq4ZhYC4Bg3tN5ZY010Mjp4O6cgroz6goq23Whc_N5iEF86ZExoxDHTeExBm-X_wll9O04hHHPPqxi67HIh4NnfaDOqY=)
17. [modelcontextprotocol.info](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHoF2F7-cRSW98Tk1nmWl8TciM1STGw1y48PMDeC3MnO_NRFppYY6_mBkGNn8DTiS8ODLEOSAs_koYPDpBoyJeaLBUKjHmDp1430lKaLe3q0sOIMjtqTMEr_DSm_SMgUg_vCGwoxoK875bKIw==)
18. [apxml.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFYey9eXVA1FJULLjoaEpxGwd1CCUvpKK00ceKTp2_Tk5VrL9prRZdbIi2p2XHGl5IdL_TyfEB464t5DWhiwiTWcZ7emeKS2Euap0c2EMjET2oqcj3RGdJH8zGLgwLhlhwCnV2haLrbk3b0ZXA3NnbU2lx6prBTuQaTtJzdlXVbdugai5gGwiLbLILpmaW123vTxYpdtmsTNmsNx02b_ZUKaaHUOOdpoSVaiRhCwruQeftei1DrEQ==)
19. [alpic.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHZSHkw736AH2FNzidt5H_oe5nJONkngNNcRzOZT-a5JTwZWPlXBKxhuEDcJFJt3gnFNRPbYtm1R5B6fKpKS_DRYa3Mi4cBqmcC8hR7gUA6qrHmyMPRQ7Or0MwGwe9nFQCP9t4trYrsWnGb3-5DjkuPjeeuu4bK7Os-uhlwgmGtUjTZ6tia)
20. [rapidevelopers.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFoisNWRFIl1UMaXWkbYMV5CIy1AuJ21TFvwOH2qtedOeJ9N3iOnv-vVk7wVP5hRREdJmTmKw38YOkzR9VE42ulepoDhP2EMG_LKEK6eG3zJSITsEhAJrkBRYlRQH9Rpmq4umWExD6kXJ4-VasMs8OpmdYH8JQdfqhZFbb3H4oSrodD1Q_v)
21. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEcTglhZpE39noLGPkL-ID6VBD5kf90iscx4ew2PhNCCJaejAJarHm8113OizuQTk7scC8PoSeTmuAUwJsX3Evs9aAgLAvwElGk0GyJeXH80wxsNLxCsO041dyROxgsVB7WtJXU5SCA)
22. [cloudflare.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG7toxgJ0VvD0d4xYwtT93uTna6tz0VhILMRAwSpnPo2oqqf9_nvBIEeFBbnQETiaMOzY5mEdV1CdtN24folBWxi1NBWR7Mcavk-J-EVIhevD1DgiPUQo5wz-lWZVlY5zrO8sTdEi2HMje64FJyxpPIOfvwrvpz2uXMRAs=)
23. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQENvsmKvA67qmt3-WevTA62yeNe7N02FFQ74R8DsskfExEGREDLH00yx5V2ZpkUGnTfc2c4rjEZ8-Kw66QEu6iwcPd96VBCO2pBzQCSHpFOhyAMVh_Q4OK5NOAdNpQ05WZtxAseO2qoO_I8d58ULa-v1NO_onRoPxYQy-V6VOECGbhJ3zxpdH2q1cRWW5WFPLs4MiieT01L7iJZFht42RKObGoD-xC7_xvuW0v9WZgQYFfKZbt6EIE=)
24. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCgPtiqbXg661c8IzL8bt2KDtVQ92Z7unrEKDCPIDY7IbnqDWfoLVYXk8-iKjiuqcp-5MLZNhAW84E9lfYpo3enXko-Vxtnf9fJl8DynsKJ_R2GmRSwQkxBewLy8FiGj5dgPhtJrtqSiY2M9PTS_meFN7ArdhFSklgXp3ahHI=)
25. [mikeborozdin.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE1AVm_isgoMFSbLiBtYKnD5BF8qhmWSEtMiM27uBllHK6orMDlUPA15YXNeT3e9rx-pAyyzb3dY80eKNSMI8CYXo113FvcTeqJ2QUa-1S-wtw_hccNCegVJpgIsvLCZGeWbOUXecfylpkDBRD5pomckFZXrTeqhaI=)
26. [mintlify.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGv-G4iFqepZQzmz4LzJbVJj_WcTbYjZqwxS3R0D9p9aMJj7LSea6AlUSYL2XzGIc1OQw-X5Ri7Vf-pzjsDXagfT_LiMhUvtSmUdh7Cbrzt1sPdoRa-DqYLaXMRvawzuN3kev1RmJeJNGt38juj47nPKwQ=)
27. [mcpservers.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF2E5FCyz8supB9MZf_F1BXNxIgLaTicWnW-tzT6X4Q3KS_6PWN8ouMDBJoQHE6f6C0rQizDCiSopu22iRAJVhDXOwQJLY0bTxXFyPnCBcrRgMf6M00an7MtE4Vt6qlBPmJ4twYWcatSQ==)
28. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGvSfD6TlEeotDcV8RYumZPt5PA1mS9EbawAdBGALJcdl5cXZCmkSLnvNOApqWN8GwP8tr1mlWQy1tCgpJkM85hSNQaQ4XiT3WxHhoV4GI5pLTOLgXS7g-OqPY_lGBDjxznh-3R)
29. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrQ22Oti-C6tLZHKGKjzHhqVdDYIBCacqaj_HXRNP0gwQsUnvpoi1Sk0ZHDGKGg1n1pyDQqyeKM4f_Tu3mr0QRGZ-NBmPPw2oSlWetEtW3fMVa6eKbSnbK34T2F-SbD7NJ3uK-m8wLyknGj1zRMUZy4wbFRIJQqQ==)
30. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEAevYJwg3LvLnJWcJl25QuqWCZyx_Ky60lLYBbVh0GFL0OJEBHAgJnlnWWWIvQdSL8N4fcmPy7fPUW58tfEBrEtpugMs8mQ7SYOarHbO5V64O-reB5wBir12yMmxYp66Q35PcMR8OpoECLvGtN-9V6GbRecrtADCR8Z2qPpuH6ktIyA2aiTww=)
31. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFuSzhp3b6X5GEXIIkcbvWAGXNQ_wNJSP_-NFVcRQl5ARkFptSNJPiCKdFfpaXaATHd2B3axT4C9Ch7HADyBBtL9FB9zc5b3PwplTLI7iLzWW45LD1NrRXfESJib1A3MsVOGeTz1Zqzmvf1S5xrK7iEHqq2p12sMSODrFWMFWsrsECQ1RWyuQ==)
32. [nashtechglobal.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFdGHbMSVWMttQz40P1WPIZLTKYA6q7ELikPcBJlcX3lkTi6aGYZXTKS5iI5hWnsXqqAdXBHUxMY7jOPvHkEMoPdsYqetAImSB-8sIP37dKYNuI0Fz02kGnqcJw1pMULrYBmpxq_qrq22mtm6Gv9OErOH92xKlfXNTn8ZR9QKImEPo8PvwzdWdsUNaEs3WQbPr1TD00KmhB9vVDA6s__tjd)
33. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwePgwP_9kLUNqC2E80Y3QCQoCDS2eV5IiH_wehZ5HqGa23wTpLodE-t2vn6jY7D5m7KIADSnwAbCPKsDmjmRoJhB5ciU8VqgWceXVERZyZqzFQ9w2KR4sfsxldmx7hws=)
34. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFCxrhrgy6rmWRfu7gpGseBcWNDi0u0lidLnPILm1_d49cLbmbCaBgtdMnEeVnMf2f0Gcb2kVAOC8Cs2FAVRx79a0Hp9BJKgYWQO3lWOSY4J9O_orM8QaB3uPQgUQ==)
35. [lib.rs](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFiQ-1Al4dcW_yoAw8lKMcuetZRFVBlY5cNHCDCws4eyzzOfMHemdA604Jlhwdo41dYh9IGWzwDDCLOsEMjHKGfXQbnCxgoKYQrjdiR3GJhJxrLw4eHXN5U3rkg)
36. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3s7YMPN4CUiT7nPsxQI362xJvDLZU71i8acjIB1Rz4dFc-6F0oPcw4pXvfzn5g6lpEtaqaHOaBxnEqsNXsTC0v0Z4K9wUm_b4a6ddrXprluRAbDmV59K6ZPLiJXcpDqcU1r_igPDcrLZLsK_GaQru6iEddmZkBBqr75vit6IDSI6p)
37. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGxPani_omLO6nMtk15YMDqWBDRdyNBhKpc5QgsVf9_TUh8pnl4GZn9nJDwvt_OGM0KNdtkK_UXpmgKxEZWvBqR8jOPD-qQZDrNYYuHtJ1A0kDm9K1e5S1g)
38. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG0qPaMe3kmJyyO9AVlG007dIUNND3XZgiNWel0GHxSwwepvG9dGYiUnnXm_pv7tz5c6etlQeLgRgY2BfiZ3lptfaZdL4xYE7UHCg_aWXsnzurWfxgJabGQuqo=)
39. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH1uo3bX8AEfONnGhijJY55mhrwaRG2v09Djm_xdyX473avNyomEwyOvjSvObWnRafCB_YAFAn3WbXD32ImVFqCNH6ADZr-XZD8N35EjsCzYwlhS8woCA3pzwLX-bfKz_igvkM8CuSz6AoWa87AYKrMWzbt3kDEgGT1SH1TCEtCWH1ZsS1vwKtEtMkhnq0rRA_BJCQKux4CISfLaD6o)
40. [octavehq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFtFoZTEwUvQpdp0z5QoqRc_MpLqcp0WG09atF0o-9icXJ0uQHQPnapL9ITvBZUn6eLPzcDi6LLRjnOl7SJEHKzqtBEo4bl8hKbSHEyGEM6ee7uKsvkruaY8AXboPxfYVfh9wx1nml4ELMDPMH9StBjyE_6JDeZzQ==)
41. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGfUL9fVNK1aVGvYHU7y86DqXu1J1UEmPlnW2oDI4h8otVJQopfEyE_7JpMecoVwzKpUczNvUV3UvUoEJ1QSJjfwnINqZ86VDBMkaoxcr4_1Si43ihIugVd0vTZ40WHO98c10seuXwFlPLckzb1Vn0TOUoByWgcABLk_tM57UrE7lZvnEA9wks=)
42. [generect.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFsgM7sFabatxeAc_o7LfYF8yqgYBwPyH3HXWlKwrLv-5DfLY4gePdbLTzkEUS7XgWOhC3EjEKzv4Gu9YUmjkd_j2IrU_XoxJcU0NFBb3_d5hFYfgTXG_u5Ygk=)
43. [modelcontextprotocol.info](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHCTAE3kTQ8XVWv5KOq3QSbs_tLyhlOs3MY5xDsMsMZBkgefG3Egqw2VlDpfdastUwdxmei7sIQHj4tTJ_jqcNxvlwIDsfMp9XEp5EJPb1tnZ9T6IAK5xnmGlZ6xuwcoWfrfCe7JoM=)
44. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGJoQ_AgZ2WL0eEbAuQ_EuTqHmhnHZnEhkg6zxMK8kCEyIF2Q3TL77jBa1sUe8eOpSOApQGFep8iz7TEi05L34bw2MV4cOkPdVuxjqUcjXHX9C73KLNiQjYbY5sySiTG_sq6xJLxfVZeKnRK4MQ1hsYrMNLZ4TK5J6qfX0CDz6wWg==)
45. [truefoundry.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQELaseVbnT2OPod6utK3TjjEIoEnLujnYIIFao0SedIY2ncGZe9kWkkRQb5pzNJsqtmxutjhpLpT4h1Q6sq2L6pFz1ztZ1nifwug4NU7i20PkFJEnKU2aAE60DN8d4Fup6J37oAk9FFFLA=)
46. [augmentcode.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFoDNr2A8hgf1UbpbqAGyy1s-h6YeeT5lMzASAyhcJVo6ATsQUVizN9CcoXrAxdvLu7f8YtPaqF-l0OQTV9Ar6nmfDaR2Uf8oKoxhtX2Oyb2tWQIie_CoTTR28rPdaZkeSw)
47. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG4V40gzq208NC2APZ15uF7UJ7EbdSMWd-2sPd8DYFN4w80z_3sI7PNt54IrSqGghp1zmxXBaV5vQMPwLm86eQniD-bn2Q1XYAx5TiVzqJnsIALsvlDKqBx_2g6rggyW1WRUbFaKSdltYTC6rw=)
48. [github.blog](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFIm9hC-6CGToijRw2GQELrnKldG00zrtRB2R0Bb84GLbDoHSQkVpn_9GWpclL7VvtKWf_RiLLAAH6-fS1nR1REMUsMCWu6RAD7qXdEsrqjNlL6daNjeYAkmZmVNmCrkEpH4El3E3FpBKAUTIUHBLxtzrvJSPlPQn8FC7U0KvTyt_bjTzT2-uiytZ_Bb9mtM41g0dE19b67-wZQZvWbw_TTqt4XG_xThGoN)
49. [apigene.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG589Dns2996HqP7rjIzADhfTZaDRWtcF1V2q4LTNCGRopc7zBodfJ6FzRLwJ45Sh6dGRyloi8y5qeFk3mJjukxIcqbNws3AP_IdvxaXLRMpkgQgHkEiAS0latxCJXpQuFMnfI=)
50. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEK1YPry3y2fm2ny2rDHzJ-frU9tF_WWr6gqiZBafNrBlhBJfc-T9kKb6khVA3bZqLquaVUQZ1zSWPhJvJklyoB12WCjvjw6wts87ozuAyXrthRErUgCekP3Eb5VRALR5BJdWVEhrl57EvxlCDcGMpZ)
51. [dev.to](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGWvLh4Ml0rXMdwHiql6_HrJtGEF5a0NTOCC2Yy3aBdPxZRi063LLuB3VBh_JxuNhwigNY_I9RAG7sNiDqD6S1b9msITKp_Ee2WBc_6TmNziq1KrFqe3Rr4ZxiyVesOl2URj0htHaUrgwQSwyiNExk2mFBv-tsLu4qgc4PQcnbpfA8rTNuM1uUoHfwqt16eBGmvHXHyhFWh)

