---
type: research-report
project: prj-job-hunt-2026
research_topic: mcp-server-production-patterns-2026
created: 2026-05-07
model: gemini-deep-research-max
ai-context: "Grounding context for the intent-engineering MCP server v0 build (target ship 2026-05-25). All load-bearing claims cited; uncited claims flagged."
---

# MCP Server Production Patterns 2026 — Reference for `intent-engineering` v0

## The Current SDK Reality

The most important current-state fact is that the stable production line is still `@modelcontextprotocol/sdk` on the long-lived `v1.x` branch, while the `main` branch of urlmodelcontextprotocol/typescript-sdkturn12view0 is explicitly labeled “v2 … pre-alpha,” says v1.x “remains the recommended version for production use,” and shows split packages such as `@modelcontextprotocol/server` and `@modelcontextprotocol/client`. The stable `v1.x` `package.json` still names the package `@modelcontextprotocol/sdk`, shows version `1.29.0`, and declares `engines.node` as `>=18`; that means your planned stack of entity["software","Node.js","JavaScript runtime"] 22 is inside the supported floor. The official npm package page also surfaced `1.29.0` in search as of 2026-05-07. For a 19-day recruiter-facing build, the grounded recommendation is: use `@modelcontextprotocol/sdk@1.29.0`, not `main`-branch v2 imports. citeturn12view0turn15view0turn13search0

There is real source disagreement you should treat as operationally important, not as noise. The official “Build an MCP server” quickstart on modelcontextprotocol.io still says “Node.js version 16 or higher,” installs `@modelcontextprotocol/sdk zod@3`, and imports from `@modelcontextprotocol/sdk/server/mcp.js` and `@modelcontextprotocol/sdk/server/stdio.js`. By contrast, the SDK docs root page says the stable SDK has a peer dependency on `zod`, internally imports `zod/v4`, remains compatible with Zod `v3.25+` or `v4`, and the `main`-branch README shows the split-package v2 syntax with `@modelcontextprotocol/server`. That means the public docs currently span at least three eras at once: older quickstart prose, stable v1 docs, and pre-alpha v2 repo code. For your repo, do not mix those eras. Stick to stable v1 import paths everywhere until you deliberately choose a v2 migration. citeturn7view0turn7view1turn10view0turn12view0

The minimum viable project structure in the official TypeScript quickstart is intentionally small: `src/index.ts`, a `package.json` that sets `"type": "module"` and ships `build/`, and a `tsconfig.json` that compiles to ES2022 / Node-style modules into `./build`. The tutorial’s build script is just `tsc && chmod 755 build/index.js`, which is exactly the level of complexity you want for a time-boxed v0. For this project, the conservative public-server layout is: `src/index.ts`, `package.json`, `tsconfig.json`, `README.md`, and then optional extras like `LICENSE`, `server.json`, and `examples/` only after the three demo tools are working. citeturn7view1turn7view2

A safe `package.json`/`tsconfig.json` baseline, adapted directly from the first-party quickstart and stable-branch requirements, looks like this:

```json
{
  "name": "@your-scope/intent-engineering-mcp",
  "version": "0.1.0",
  "type": "module",
  "bin": {
    "intent-engineering-mcp": "./build/index.js"
  },
  "scripts": {
    "build": "tsc && chmod 755 build/index.js",
    "start": "node build/index.js"
  },
  "files": ["build"],
  "dependencies": {
    "@modelcontextprotocol/sdk": "1.29.0",
    "zod": "^3.25.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.0.0"
  }
}
```

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

That exact dependency pinning is a recommendation layered on top of first-party files; the underlying module shape, output directory, and build-first workflow are first-party. The addition of a `start` script and Node 22 devDependencies is a small integration convenience, not something the docs prescribe. Preliminary — uncited for the exact `devDependencies` versions; grounded for the project shape and build flow. citeturn7view1turn7view2turn15view0

The canonical stable hello-world pattern is still: create `McpServer`, register a tool, then connect a `StdioServerTransport`. A minimal version, using the stable import paths documented on the official quickstart page, is below:

```ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "intent-engineering",
  version: "0.1.0",
});

server.registerTool(
  "generate_template",
  {
    description: "Generate a 4-question explanation template for an artifact",
    inputSchema: {
      artifact_title: z.string().min(1).describe("Human-readable artifact title"),
    },
  },
  async ({ artifact_title }) => ({
    content: [
      {
        type: "text",
        text:
          `1. What is ${artifact_title}?\n` +
          `2. Who is it for?\n` +
          `3. What problem does it solve?\n` +
          `4. What should the reader do next?`,
      },
    ],
  }),
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

This snippet follows the officially documented stable import style and the documented `registerTool` / `StdioServerTransport` flow. The safest build-vs-dev workflow is: run compiled JS in entity["software","Claude Desktop","desktop AI assistant app by Anthropic"], and only use a watch runner during local iteration if you want faster turnarounds. The official tutorial gives you the build path; the official SDK repo examples use `tsx` during example execution, which is evidence that a watch/dev runner is reasonable, but not required. citeturn7view4turn7view3turn10view0

**Confidence: HIGH.** The stable-vs-pre-alpha split is documented in the SDK repo itself, the Node floor is in the stable `package.json`, and the build skeleton / import paths are documented in first-party quickstarts. The only material ambiguity is doc drift across v1, older quickstarts, and v2 pre-alpha, and that ambiguity itself is well evidenced. citeturn12view0turn15view0turn7view0turn10view0

## Tool Registration & Schema Validation

At the protocol level, the contract is clean even when SDK ergonomics vary. `tools/list` is where your server advertises each tool’s `name`, optional `title`, `description`, `inputSchema`, optional `outputSchema`, and optional `annotations`. `tools/call` is where the client sends a tool `name` plus `arguments`, and receives either a normal result object or a JSON-RPC error. In other words: `tools/list` is discovery and schema advertisement; `tools/call` is execution. That part is defined by the spec, not by SDK helper style. citeturn16view0turn16view2turn16view3

The current SDK docs on the v2/pre-alpha side describe `registerTool` as accepting an `inputSchema` in Standard Schema form and, optionally, an `outputSchema`; the TypeDoc says the SDK needs both JSON Schema export and runtime validation, and names `registerTool` / `registerPrompt` as the consumers of that combined contract. The stable quickstart page also uses `registerTool`, but its examples pass field maps rather than the full-object Zod forms shown in newer docs. That is another case where sources disagree on helper ergonomics while agreeing on the protocol truth: you must advertise JSON Schema, and you must validate incoming arguments before running business logic. citeturn6view2turn8search13turn7view3

For your three tools, the clean public contract is:

- `analyze_intent_spec(spec_text)`
- `generate_template(artifact_name | artifact_type | audience)` depending on how narrow you want the interface
- `audit_existing_spec(file_path XOR spec_text)`

The protocol-canonical answer for the XOR case is not “describe it in prose and hope the model figures it out.” The MCP spec says tool inputs are JSON Schema; the correct surface is a schema that enforces “exactly one of these fields.” In practice, that means either a JSON Schema `oneOf`, or a schema-library refinement that compiles to the same rule. A grounded implementation pattern is:

```ts
import { z } from "zod";

const AuditInput = z
  .object({
    file_path: z.string().min(1).optional(),
    spec_text: z.string().min(1).optional(),
  })
  .refine(
    ({ file_path, spec_text }) => Boolean(file_path) !== Boolean(spec_text),
    { message: "Provide exactly one of file_path or spec_text" },
  );
```

That is protocol-correct. What I could not fully verify from first-party stable v1 examples is whether the v1 `registerTool` helper accepts this full refined-object schema directly in the same way the v2/pre-alpha docs do. So the safe implementation rule is: keep the XOR validation as an explicit first step before any file I/O or audit logic, even if you have to layer it inside the handler in v1. The rule itself is grounded; the exact stable-v1 helper ergonomics are **Preliminary — needs further verification**. citeturn16view2turn8search13turn6view2

Error handling is where public MCP servers most often get squishy, and the spec is clearer than many repos. The tools spec defines two distinct channels: protocol errors for unknown tools, invalid arguments, and server errors; and tool execution errors reported as a normal tool result with `isError: true`. The spec’s example for an “unknown tool” uses a JSON-RPC error object with code `-32602`, while its example for an API-rate-limit-style failure uses a normal tool result with `content` plus `isError: true`. For your server, the production rule should be: schema/argument-shape failures stay at the protocol layer; domain/runtime failures stay inside a normal tool result. citeturn18view0turn18view1turn18view4

That recommendation matters because real servers in the ecosystem do not always follow it. In a Claude Desktop issue against the filesystem server, missing required arguments showed up as a normal `result` containing a text error and `isError: true`, even though the spec classifies invalid arguments as protocol errors. That is exactly the kind of subtle inconsistency that produces client-side weirdness and smell-test failures in a repo skim. Your server should be stricter than that: if the input shape is wrong, fail before entering the tool’s real execution path. citeturn20view0turn18view0

For entity["software","Claude Desktop","desktop AI assistant app by Anthropic"] specifically, the verified behavior breaks down into three buckets. First, malformed stdio traffic or extra stdout noise produces JSON parse errors and can break the connection entirely; that is shown both in the official debugging docs and in public bug reports where Claude Desktop logs `Unexpected end of JSON input` or parser failures. Second, tool-level failures can be surfaced to the user as natural-language tool failure text; in the public Google Maps issue, the user reports that Claude “responds with they are experiencing an issue” and includes the tool’s error message. Third, validation failures returned as `isError: true` also show up in logs and tool traces, as the filesystem issue demonstrates. So the practical guidance is: keep stdout pristine, keep protocol validation strict, and make `isError: true` messages short and user-readable. citeturn25view1turn22view1turn20view1turn22view0turn20view0

For this specific server, I would register exactly three tools and no prompts/resources in v0. `tools/list_changed` is not worth implementing unless you actually add or remove tools dynamically at runtime; the spec only expects it from servers that declare that capability. Over-exposing prompts or resources for a three-tool recruiter demo will dilute the repo rather than strengthen it. citeturn16view0turn16view2

**Confidence: MEDIUM.** The protocol semantics are strongly grounded in the spec, but the exact stable-v1 helper syntax for more advanced one-of-many Zod schemas is not fully verified in the public stable examples I accessed. The Desktop-client behavior portion is grounded partly in official docs and partly in issue evidence, so it is strong but not purely first-party. citeturn16view2turn18view0turn25view1turn20view0turn22view0

## Transport Choice Matrix

For a v0 demo whose primary client is entity["software","Claude Desktop","desktop AI assistant app by Anthropic"], `stdio` is the shortest path between “repo exists” and “someone can actually use it.” The current MCP transport spec still says clients “SHOULD support stdio whenever possible,” and the local-server docs for Claude Desktop are entirely built around the client launching a subprocess from `claude_desktop_config.json`. The same spec also says stderr is safe for logs while stdout must contain only valid MCP messages. That maps almost perfectly to your current situation: local demo, three tools, no hosted auth, and a PM who cannot afford transport work that does not improve the demo. citeturn26view2turn25view0turn25view1

`stdio`’s limitations are real, but they are acceptable for this project. It is process-spawned, local-machine oriented, restart-heavy, and not naturally shareable as a hosted URL. The official local-server docs say Claude Desktop must be fully restarted to pick up config or server-code changes, and the debugging guide explicitly says closing the window is not enough. Those are annoyances, not strategic blockers, for a 19-day local demo. citeturn25view0turn25view1

SSE should now be treated as legacy compatibility, not as a design target. The 2024-11-05 transport spec defined “HTTP with SSE” as one of the two standard transports, but the 2025 transport spec says Streamable HTTP replaces the old HTTP+SSE model, and the current SDK docs say “HTTP + SSE” is for backwards compatibility only. entity["software","Claude Code","agentic coding assistant by Anthropic"] docs go further and explicitly call remote SSE deprecated, telling users to prefer HTTP where available. In 2026, an SSE-first new server is swimming against both the spec and the current SDK/documentation direction. citeturn27view0turn26view2turn26view3turn43search0

Streamable HTTP is the right answer for your eventual hosted version, but not for your first ship. The spec defines it as one MCP endpoint supporting POST and optionally GET, with session IDs, Accept-header negotiation, optional SSE streaming for multi-message flows, and explicit security requirements like validating the `Origin` header and binding locally to `127.0.0.1` when run on a developer machine. The SDK docs say Streamable HTTP is “recommended” for remote servers, and the registry’s remote-server docs use `streamable-http` in examples and call it the recommended option over SSE. That is the reason to structure your tool logic so it does not care about transport: you will want to add Streamable HTTP later, but you should not pay that cost before the local demo works. citeturn26view2turn26view3turn26view0

The recommendation for **this** server is therefore very specific:

1. Ship `stdio` only in v0.
2. Keep transport code isolated in one file so you can later bolt on Streamable HTTP without rewriting tool logic.
3. Do not ship SSE-only.
4. If you host v1 later, make Streamable HTTP your primary remote transport and add SSE only if a concrete client still demands it. citeturn25view0turn26view2turn26view3turn43search0

If you want the one-sentence default to remember: the current first-party build docs and local Claude setup docs treat stdio as the default for local first servers, while the current SDK and transport docs treat Streamable HTTP as the default for remote servers. That split cleanly matches your roadmap. citeturn7view4turn25view0turn26view3turn26view2

**Confidence: HIGH.** The transport recommendation is triangulated across the current transport spec, the local Claude Desktop setup docs, the stable SDK docs, and the current Claude Code MCP docs, and those sources line up unusually well. citeturn26view2turn25view0turn26view3turn43search0

## Exemplary Public MCP Servers

The official example-servers page is the best starting filter because it distinguishes current reference implementations from archived ones and points directly at the currently maintained repos. For a small public v0 like `intent-engineering`, the best models are the servers that wrap existing, well-bounded functionality rather than trying to demonstrate the whole protocol at once. citeturn34view0

**urlmodelcontextprotocol/servers — Filesystem MCP Serverturn41view0.** The README documents a very explicit tool surface: `read_text_file`, `read_media_file`, `read_multiple_files`, `write_file`, `edit_file`, `create_directory`, `list_directory`, `list_directory_with_sizes`, `move_file`, `search_files`, `directory_tree`, `get_file_info`, and `list_allowed_directories`. The example-servers page summarizes it as “Secure file operations with configurable access controls.” What to copy from this server is not the file API itself, but the boundary design: it has a narrow permission model, it documents all tool arguments, and it uses tool annotations to mark read-only, idempotent, and destructive operations. Your server should copy that exact habit of making safety and side effects legible at the tool definition layer. citeturn41view0turn34view0

**urlmodelcontextprotocol/servers — Fetch MCP Serverturn41view4.** Its entire public tool surface is basically one tool, `fetch`, with `url`, `max_length`, `start_index`, and `raw`. The example-servers page describes it as “Web content fetching and conversion for efficient LLM usage.” What to copy is the output-discipline: the tool contract itself bakes in pagination and truncation controls. That is directly relevant to `analyze_intent_spec` and `audit_existing_spec`; long inputs and long outputs should be modeled as chunkable flows, not as one giant response blob. citeturn42view5turn34view0turn43search0

**urlmodelcontextprotocol/servers — Time MCP Serverturn41view5.** The README exposes just two tools, `get_current_time` and `convert_time`, and the example-servers page summarizes the server as providing “Time and timezone conversion capabilities.” This is a strong pattern for your `generate_template` tool: one or two deterministic tools with obvious required arguments are easier for clients to select and easier for humans to trust. When you can reduce ambiguity in the tool contract, do it. citeturn42view6turn34view0

**urlgithub/github-mcp-serverturn40view0.** The server is large, but it is worth studying because it solves a real production problem: how to expose a broad capability surface without drowning the client. Its README says it “connects AI tools directly to GitHub’s platform,” and documents both toolsets and fine-grained explicit-tool allowlists. Verified examples include default toolsets `context`, `repos`, `issues`, `pull_requests`, and `users`, optional toolsets like `actions` and `code_security`, and explicit tools such as `get_file_contents`, `issue_read`, and `create_pull_request`. What to copy is the scoping mechanism, not the size: if you ever expand `intent-engineering`, group tools by job-to-be-done and make it possible to expose only the subset needed in a given install. citeturn40view0

**urlgetsentry/sentry-mcp-stdioturn38search0.** This repo is especially useful because it is small, local, and explicitly positioned for IDE/agent use. The README says it “has been verified to work against Cursor, Codeium Windsurf, and Claude Desktop,” and its documented tools are `list_projects`, `resolve_short_id`, and `get_sentry_event`, each with `view` and/or `format` options where appropriate. What to copy is the interaction style: narrow tool count, human-in-the-loop debugging workflows, and explicit formatting/view switches so the tool can serve either terse or rich output without changing its identity. That is a strong analog for your audit tools, which should probably expose a stable schema plus a “brief vs full” mode before they expose more tools. citeturn38search0

**urlmodelcontextprotocol/servers — Everything MCP Serverturn33search10.** This is the one non-wrapper I would still study. Its README says it “is not intended to be a useful server, but rather a test server for builders of MCP clients,” and the example-servers page labels it a reference/test server. What to copy is not its product shape; it is the idea of having an internal “everything” or “conformance-ish” harness that exercises your own tool registration, error handling, and client compatibility before you publish. For a recruiter-grade repo, a tiny internal smoke-test script or inspector fixture that does this is a net positive. citeturn33search10turn34view0

If I had to pick just three patterns to steal for `intent-engineering`, they would be: Filesystem’s explicit safety boundary, Fetch’s built-in chunking/pagination knobs, and GitHub’s toolset-based surface control. Those three patterns map almost one-to-one to the risks in your server: reading external specs, returning potentially large audit payloads, and avoiding tool sprawl. citeturn41view0turn42view5turn40view0

**Confidence: MEDIUM.** The repos and their high-level patterns are well grounded, but some servers have broad surfaces whose full tool inventories were not completely enumerated in the publicly surfaced snippets I accessed. Where a tool list was partial or category-based, I stayed explicit about that. citeturn34view0turn41view0turn40view0turn38search0

## README + Discoverability Conventions

There is not, as of this research pass, an official “recruiter-grade MCP README template” from the MCP project. So the safest way to answer this section is to separate what the docs **do** require from what strong public repos **consistently** do. The official docs clearly support these README elements: a crisp description of what the server exposes, exact install/config steps for local clients, example prompts or tool calls, environment-variable requirements, and registry metadata that points to a public install method. Anything beyond that is best treated as public-repo convention rather than protocol law. citeturn25view0turn29view0turn29view2

For a public v0, the README should open with one sentence in the style of the better public repos: what the server does, for whom, and in what environment it is intended to run. Then add a short “Why this exists” paragraph, followed immediately by a **Tool inventory** section that names all three tools and gives each one a one-line contract. Do not make the reader infer the contract from a screenshot or a 90-second video. The GitHub, Filesystem, and Sentry READMEs all expose the contract close to the top rather than burying it. citeturn40view0turn41view0turn38search0

Your Claude Desktop install instructions should be exact, absolute-path based, and copy-pastable. The official local-server docs say the config file lives at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS and `%APPDATA%\Claude\claude_desktop_config.json` on Windows. The same docs show a `mcpServers` object with `command` and `args`, while Anthropic’s Claude Code docs show a Claude Desktop example that also includes `"type": "stdio"`. Because these two first-party sources disagree, the lowest-risk README pattern is to document the plain `command`/`args` shape first and note that some Anthropic examples also include `"type": "stdio"`. Test before documenting both. citeturn25view0turn43search0

A conservative config block for your README is:

```json
{
  "mcpServers": {
    "intent-engineering": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/intent-engineering-mcp/build/index.js"],
      "env": {}
    }
  }
}
```

That shape aligns with the modelcontextprotocol.io Claude Desktop docs for local servers. If you later confirm that Claude Desktop on your target version accepts `"type": "stdio"` and you want parity with Anthropic’s Claude Code docs, add a second verified example rather than silently replacing the first one. citeturn25view0turn43search0

The registry submission path is much more concrete because it is officially documented. The MCP Registry is in preview, is metadata-only, and expects the actual artifact to live somewhere public such as npm. For npm-based local servers, the quickstart says to add `mcpName` to `package.json`, publish the package first, install the official `mcp-publisher` CLI, create `server.json`, authenticate with the registry, and then publish the metadata. The auth docs say GitHub-based names must be of the form `io.github.username/*` or `io.github.orgname/*`, while domain-based names use reverse-DNS. citeturn29view0turn29view1turn29view2

A registry-accepted listing, as documented by the official registry pages, consists of standardized metadata rather than prose decoration. The registry “About” page says `server.json` includes the unique name, where to locate the server, execution instructions, and discovery metadata. The remote-server docs give a live example of a `server.json` that includes `$schema`, `name`, `title`, `description`, `version`, and `remotes` with `type: "streamable-http"` or `type: "sse"`. The public registry UI at registry.modelcontextprotocol.io visibly exists and is the official discovery surface, but I did not verify a single live server’s full API payload end-to-end in this pass, so any field-level guidance here should be read as “official documented shape,” not “reverse-engineered from a fetched live listing.” citeturn29view2turn26view0turn30view0

On screenshots, Loom embeds, and badges, the official docs are mostly silent. **Preliminary — uncited:** for a five-minute recruiter skim, a single still screenshot of Claude Desktop discovering and calling one tool is higher value than a Loom dependency; npm-version and license badges are useful immediately; and a registry badge or “Published on the MCP Registry” link only becomes useful after the listing is live. I did not find a first-party MCP style guide that mandates or ranks those elements. Preliminary — uncited.

**Confidence: MEDIUM.** The configuration paths, JSON shapes, and registry process are strongly grounded. The “recruiter-grade README” layer is partly synthesis from public repos because the MCP docs do not define a README rubric. citeturn25view0turn29view0turn29view2turn43search0

## Common Antipatterns and Failure Modes

The first repeated failure mode is **schema drift between docs and code**. The public filesystem server is the clearest example: issue threads record mismatches where the README referenced resources support that users could not find implemented, and where `edit_file` was documented or visible in code/README but missing or unavailable in clients. This is exactly the kind of thing that tanks trust in a repo skim, because the first question a reviewer asks is “does the README actually match the server I can install?” The fix is simple: generate your README tool inventory from the same source of truth you use for `tools/list`, or at minimum verify the README against a real client session before every release. citeturn33search7turn21search10turn33search13turn16view0

The second recurring failure mode is **corrupting stdio with logs or malformed output**. The official build guide explicitly says never use `console.log()` for stdio servers because it writes to stdout and breaks JSON-RPC; the debugging guide repeats that local stdio servers should not log to stdout. That warning is not theoretical: public issues show Claude Desktop logging JSON parse failures like `Unexpected end of JSON input`, and another bug report shows the client-side stdio parser choking on malformed MCP responses. The fix is equally explicit: stdout is protocol only, stderr is logs only, every build should be tested with Inspector or Claude Desktop before release. citeturn7view0turn25view1turn22view1turn20view1

The third failure mode is **permission-model assumptions that do not actually hold at runtime**. The official debugging docs say the working directory for client-launched stdio servers may be undefined and that only a limited subset of environment variables is inherited automatically. The filesystem README’s recommended design is therefore to use explicit allowed directories or client-provided Roots, and a Git-server issue in the official servers repo shows how stale root access can survive longer than intended if you do not revalidate on each call. For your server, the practical lesson is: avoid relative paths, do not assume the current working directory, and if a tool touches the filesystem, authorize the target path on every invocation, not just once at startup. citeturn25view1turn41view0turn33search18

The fourth failure mode is **transport mismatch and clinging to deprecated SSE expectations**. The transport spec changed: 2024-era MCP documented HTTP+SSE as a standard transport, while the modern spec says Streamable HTTP replaces it, the SDK docs say HTTP+SSE is for backwards compatibility only, and Anthropic’s Claude Code docs call remote SSE deprecated. There are also real transport-specific behavior bugs in the ecosystem, such as a report that sampling hung under Streamable HTTP or SSE while stdio worked. The fix for a new server is blunt: if your demo client is Claude Desktop and your server is local, use stdio; if you later host it, add Streamable HTTP; do not make SSE your primary transport in 2026. citeturn27view0turn26view2turn26view3turn43search0turn21search7

The fifth failure mode is **returning too much text at once and forcing the client to carry it all in context**. Anthropic’s current Claude Code MCP docs now document concrete thresholds: a warning above 10,000 tokens, a default max of 25,000 tokens, an environment override via `MAX_MCP_OUTPUT_TOKENS`, and a per-tool `_meta["anthropic/maxResultSizeChars"]` override up to a hard ceiling of 500,000 characters. The same docs explicitly suggest either asking the server author to add that annotation or paginating responses. That is a direct design input for your server: if an audit can be long, your tool contract should support slicing the input or paging the output instead of dumping a whole spec audit in one result. citeturn43search0

A related but narrower configuration failure mode is **local-command fragility on Windows / npm / nvm**, which shows up repeatedly in early issues around `npx` and local server startup. The official debugging and local-server docs already push you toward absolute paths and explicit `env`, and those are the right mitigations for this project too. I would treat this as part of your release checklist rather than as core architecture. citeturn21search12turn25view0turn25view1

**Confidence: MEDIUM.** The anti-patterns themselves are well grounded, but several are supported by issue threads rather than clean first-party design docs, which is appropriate for “what actually fails in public repos” but weaker than pure spec text. citeturn7view0turn25view1turn33search7turn21search10turn43search0

## The 19-Day Build Path for a Beginner-to-Intermediate TS Coder

The right strategy here is not “build a generalized MCP platform.” It is “ship one boring, correct local server that survives a five-minute senior skim.” The official quickstart and registry docs already give you the scaffolding you need: the build-server tutorial for local stdio structure, and the registry quickstart for publishable metadata. That means your schedule should bias toward getting one tool working end-to-end very early, then hardening the shape, not the scope. citeturn7view0turn29view0

**Days 1–3: freeze the stack and make Claude Desktop see one tool.** Use the stable `@modelcontextprotocol/sdk@1.29.0` line, create the minimal build-first TypeScript layout from the official quickstart, wire a single placeholder `generate_template` tool, compile to `build/index.js`, and get it loading from `claude_desktop_config.json` with an absolute path. If Claude Desktop does not see the server indicator or the tool list by the end of this phase, do not start implementing tool logic yet. This is also when you should add stderr logging and verify you can read `mcp.log` / server stderr logs. citeturn15view0turn7view1turn25view0turn25view1

**Days 4–6: implement all three tool contracts before polishing internals.** Write the public inputs and outputs for `analyze_intent_spec`, `generate_template`, and `audit_existing_spec`; get the schemas stable; and make the handlers return deterministic text or structured content. For `audit_existing_spec`, implement the `file_path XOR spec_text` rule immediately rather than leaving it for “later validation.” Do not add prompts, resources, remote transport, persistence, or auth in this phase. citeturn16view2turn18view0turn18view1

**Days 7–9: harden validation, error semantics, and output sizing.** Move every bad-input path into either schema rejection or a clearly labeled tool error; add short error messages; and make a deliberate decision about how you handle long specs and long audits. This is where you add pagination or chunking knobs if needed, because the Anthropic docs now document real output thresholds and per-tool size annotations. If a spec can blow past a few thousand words, solve that now instead of discovering it in demo week. citeturn43search0turn18view0

**Days 10–12: write the public README and installation path.** Add the exact Claude Desktop config block, example prompts, tool inventory, environment variables, and a one-sentence “why this server exists.” Then test the README from scratch on a clean machine or a clean user config. This phase should also include one screenshot of the tool showing up in Claude Desktop and one sample audit result. Preliminary — uncited for the screenshot choice itself; grounded for the need for exact config/tested install steps. citeturn25view0turn40view0turn41view0turn38search0

**Days 13–15: package and registry prep.** Publish the npm package, add `mcpName`, create `server.json`, install `mcp-publisher`, and verify the registry auth path you plan to use. If you are publishing under a personal GitHub namespace, decide the final server name now and make it stable across npm, README, and registry metadata. Do not leave naming until the last 48 hours. citeturn29view0turn29view1turn29view2

**Days 16–19: repo polish and smell-test pass.** This is where you run a final “senior FDE skim” checklist: does the README match the actual tool names; does installation work on the first try; do tool errors read cleanly; does stdout remain clean; is the repo free of abandoned HTTP/SSE experiments; and is the package/listing metadata consistent? If you have spare time, spend it on one or two small tests and one short demo transcript, not on adding a fourth tool. citeturn33search7turn22view1turn25view1

Where you should **not** roll your own is just as important. Do not invent a custom transport. Do not invent a metadata publishing flow instead of using `mcp-publisher`. Do not invent your own schema DSL when JSON Schema + Zod already cover the contract. Do not build a hosted transport before the local stdio demo is finished. And do not add a dynamic tool catalogue until your fixed three-tool surface is solid. Every one of those customizations spends schedule on plumbing rather than credibility. citeturn26view2turn29view0turn16view2

For official boilerplate, the best first-party starting points I found were the TypeScript server quickstart on modelcontextprotocol.io and the `weather-server-typescript` starter referenced in the registry quickstart from urlmodelcontextprotocol/quickstart-resourcesturn29view0. Those are the right places to lean on official scaffolding. citeturn7view0turn29view0

**Preliminary — uncited cost note:** use a cheaper model like Haiku or Sonnet for rote scaffolding, README churn, and fixture generation; reserve a stronger model like Opus for one or two high-stakes passes: final schema review, naming pass, and a “what would fail a senior repo skim?” audit. I did not find a primary source that turns that into a documented best practice, so treat it as tactical judgment, not as sourced doctrine.

**Confidence: MEDIUM.** The recommended sequence is synthesized from first-party quickstarts, registry docs, and real failure modes, but the calendar itself is my assembly of those facts into a workable plan rather than something stated in a source. citeturn7view0turn29view0turn25view0turn25view1

## Sources Index

**The Current SDK Reality**

- urlmodelcontextprotocol/typescript-sdk main READMEturn12view0 — accessed 2026-05-07. Authoritative because it is the official SDK repo README and explicitly states that `main` is v2 pre-alpha and that v1.x remains recommended for production. citeturn12view0
- urlmodelcontextprotocol/typescript-sdk v1.x package.jsonturn14view0 — accessed 2026-05-07. Authoritative because it is the stable-branch package manifest showing package name `@modelcontextprotocol/sdk`, version `1.29.0`, and Node engine requirements. citeturn15view0
- urlMCP TypeScript SDK docs rootturn10view0 — accessed 2026-05-07. Authoritative because it is the official generated SDK docs site and documents stable installation plus current transport guidance. citeturn10view0
- urlBuild an MCP serverturn1search2 — accessed 2026-05-07. Authoritative because it is the official modelcontextprotocol.io TypeScript quickstart used for project skeleton, imports, and local build wiring. citeturn7view0turn7view1turn7view3turn7view4
- url@modelcontextprotocol/sdk on npm search resultturn13search0 — accessed 2026-05-07. Supporting evidence that npm still surfaced `1.29.0` publicly on the stable package line. citeturn13search0

**Tool Registration & Schema Validation**

- urlMCP tools specificationturn1search3 — accessed 2026-05-07. Authoritative because it defines `tools/list`, `tools/call`, tool metadata fields, result structure, and error-handling semantics. citeturn16view0turn16view2turn18view0
- urlMCP base-protocol overviewturn17search4 — accessed 2026-05-07. Authoritative because it defines JSON-RPC response/error shape for MCP messages. citeturn18view4
- urlMCP TypeScript SDK docs rootturn10view0 — accessed 2026-05-07. Supporting evidence for Standard Schema expectations and current `registerTool` direction. citeturn10view0turn8search13
- urlClaude Desktop missing arguments issue on filesystem serverturn20view0 — accessed 2026-05-07. Useful real-world evidence for how validation failures are sometimes flattened into `isError: true` tool results in the ecosystem. citeturn20view0
- urlGoogle Maps MCP authorization issue in Claude Desktopturn22view0 — accessed 2026-05-07. Useful real-world evidence that tool-level failures surface to users as natural-language Claude errors. citeturn22view0
- urlMalformed MCP responses causing parser errorsturn20view1 — accessed 2026-05-07. Useful real-world evidence for bad JSON/stdout producing client-visible parser errors. citeturn20view1

**Transport Choice Matrix**

- urlMCP 2025-11-25 transport specificationturn17search7 — accessed 2026-05-07. Authoritative because it defines stdio and Streamable HTTP as the current standard transports and states that stdio should be supported whenever possible. citeturn26view2
- urlMCP 2024-11-05 transport specificationturn27view0 — accessed 2026-05-07. Authoritative historical source showing the earlier HTTP+SSE era and making the replacement visible. citeturn27view0
- urlMCP TypeScript SDK docs rootturn10view0 — accessed 2026-05-07. Supporting evidence that current SDK docs recommend Streamable HTTP for remote servers and treat HTTP+SSE as backwards compatibility only. citeturn26view3
- urlPublishing Remote Serversturn26view0 — accessed 2026-05-07. Authoritative because registry docs explicitly recommend `streamable-http` for remote registry entries and allow SSE as an alternative. citeturn26view0
- urlClaude Code MCP docsturn43search0 — accessed 2026-05-07. Supporting evidence that Anthropic now calls remote SSE deprecated and shows current client transport expectations. citeturn43search0

**Exemplary Public MCP Servers**

- urlExample Servers on modelcontextprotocol.ioturn34view0 — accessed 2026-05-07. Authoritative because it is the official maintained index of current reference servers versus archived examples. citeturn34view0
- urlFilesystem MCP Server READMEturn41view0 — accessed 2026-05-07. Authoritative because it documents the current tool list, directory-access model, and tool annotations for the official Filesystem reference server. citeturn41view0
- urlFetch MCP Server READMEturn41view4 — accessed 2026-05-07. Authoritative because it documents the exact `fetch` tool contract and built-in output slicing controls. citeturn42view5
- urlTime MCP Server READMEturn41view5 — accessed 2026-05-07. Authoritative because it documents a compact, deterministic two-tool surface. citeturn42view6
- urlGitHub MCP Server READMEturn40view0 — accessed 2026-05-07. Authoritative because it documents GitHub’s official server, local/remote install modes, and toolset/tool scoping model. citeturn40view0
- urlgetsentry/sentry-mcp-stdio READMEturn38search0 — accessed 2026-05-07. Authoritative because it documents a small, local, Claude-compatible vendor server with a clearly bounded tool surface. citeturn38search0
- urlEverything MCP Server READMEturn33search10 — accessed 2026-05-07. Authoritative as the official reference/test server for builders who need broad protocol coverage. citeturn33search10

**README + Discoverability Conventions**

- urlConnect to local MCP serversturn25view0 — accessed 2026-05-07. Authoritative because it documents Claude Desktop config-file locations, config shape, restart behavior, and local-server setup. citeturn25view0
- urlDebugging local MCP serversturn25view1 — accessed 2026-05-07. Authoritative because it documents Claude Desktop logs, stdio logging rules, and absolute-path / env pitfalls. citeturn25view1
- urlQuickstart: Publish an MCP Server to the MCP Registryturn29view0 — accessed 2026-05-07. Authoritative because it documents the official `mcp-publisher` flow, `mcpName`, and publish order. citeturn29view0
- urlHow to Authenticate When Publishing to the Official MCP Registryturn29view1 — accessed 2026-05-07. Authoritative because it defines GitHub-based and domain-based namespace rules. citeturn29view1
- urlThe MCP Registryturn29view2 — accessed 2026-05-07. Authoritative because it explains what metadata the registry stores and what kinds of servers it accepts. citeturn29view2
- urlOfficial MCP Registry UIturn30view0 — accessed 2026-05-07. Supporting evidence that the registry is live and visibly used for discovery. citeturn30view0

**Common Antipatterns and Failure Modes**

- urlFilesystem README/resources drift issueturn33search7 — accessed 2026-05-07. Strong ecosystem evidence for docs-code drift in an official example server. citeturn33search7
- urlFilesystem edit_file missing issueturn21search10 — accessed 2026-05-07. Strong ecosystem evidence that documented tools can still fail to appear in real clients. citeturn21search10
- urlBuild an MCP server logging guidanceturn1search2 — accessed 2026-05-07. First-party warning that stdout logging breaks stdio servers. citeturn7view0
- urlUnexpected end of JSON input in Claude Desktop logsturn22view1 — accessed 2026-05-07. Strong evidence of malformed output breaking client connections. citeturn22view1
- urlEnvironment and working-directory debugging guideturn25view1 — accessed 2026-05-07. First-party guidance on absolute paths, env inheritance, and capability mismatches. citeturn25view1
- urlGit roots-permission enforcement issueturn33search18 — accessed 2026-05-07. Strong evidence that permission boundaries must be re-checked during tool calls, not assumed from startup. citeturn33search18
- urlSampling hangs on Streamable HTTP or SSE issueturn21search7 — accessed 2026-05-07. Useful evidence that transport behavior can differ enough to matter for demos. citeturn21search7
- urlClaude Code MCP output limits and warningsturn43search0 — accessed 2026-05-07. First-party source for actual MCP output thresholds and the `anthropic/maxResultSizeChars` override. citeturn43search0

**The 19-Day Build Path for a Beginner-to-Intermediate TS Coder**

- urlBuild an MCP serverturn1search2 — accessed 2026-05-07. First-party source for the official minimal TypeScript scaffold and local stdio server flow. citeturn7view0turn7view1
- urlQuickstart: Publish an MCP Server to the MCP Registryturn29view0 — accessed 2026-05-07. First-party source for the publish sequence and the `weather-server-typescript` starter reference. citeturn29view0
- urlConnect to local MCP serversturn25view0 — accessed 2026-05-07. First-party source for Claude Desktop config and restart/test habits. citeturn25view0
- urlDebugging local MCP serversturn25view1 — accessed 2026-05-07. First-party source for log locations and debugging cycle expectations. citeturn25view1

**Preliminary — uncited**

- Screenshots vs. Loom embeds as a recruiter-screen optimization choice.
- Exact “best” badge set beyond a basic npm-version / license / registry-link convention.
- Cost-aware model routing advice about Haiku/Sonnet/Opus for different implementation phases.
- Exact stable-v1 `registerTool` ergonomics for advanced refined/union schemas beyond the public examples I verified.