---
type: research-report
date: 2026-05-04
question: "You are a senior research analyst specializing in AI developer tooling and the Anthropic API surface. Your output will guide a Product Manager who is building a personal autonomous agent fleet using the Claude Agent SDK (Python 0.1.63) running headlessly via macOS launchd.

<context>
The researcher's agents currently run headlessly and authenticate via `claude login` OAuth (refresh tokens stashed in macOS Keychain). They need MCP server access — specifically Slack, Google Calendar, Gmail, and Atlassian (Jira + Confluence) — but today the SDK agents cannot use MCP servers because MCP requires browser-based OAuth that's only available in interactive Claude Code sessions. The Anthropic API's 'MCP connector' mode (the `mcp_servers` parameter on the Messages API) might be the right path for headless contexts.
</context>

<your_task>
Research and synthesize, grounded in 2025-2026 sources:

1. Anthropic API MCP connector capabilities (current state). What does the `mcp_servers` parameter accept? Stdio MCP servers, HTTP MCP servers, or both? What auth mechanisms are supported (capability tokens, OAuth client credentials, scoped API keys)?

2. Headless agent compatibility. Can a headless agent (no browser, no interactive OAuth flow) authenticate to MCP servers via the API? If yes, how — what's the credential pattern? If no, what's the recommended workaround?

3. `claude login` OAuth inheritance. Does the Claude Agent SDK 0.1.x line inherit MCP access from the user's `claude login` session? What scopes flow through? Caveats for long-running headless processes (token rotation, refresh, expiration)?

4. Production patterns. 2-3 published patterns (blog posts, Anthropic docs, real-world examples) from 2025-2026 of headless Claude agents accessing external services via MCP. Include code snippets if available.

5. Gaps and roadmap signals. What MCP+headless capabilities are explicitly NOT supported as of the research date? Any roadmap signals from Anthropic about closing those gaps?

Prefer official Anthropic documentation, Anthropic team member posts, and production case studies. Cite versions and dates.
</your_task>

<output_structure>
Markdown report with sections matching the 5 numbered tasks. Length 1500-2500 words. Inline citations [1], [2] tied to numbered Sources at the end.
</output_structure>

<validation>
Before finalizing:
- The `mcp_servers` API parameter spec is cited from official Anthropic docs (not blog speculation)
- Any 'headless OAuth inheritance' claim is backed by SDK source code or docs, not assumptions
- It's explicit which MCP server types (stdio vs HTTP) work in API context vs only Claude Code
- API model versions tested are noted (e.g., claude-sonnet-4-6, claude-opus-4-7)
</validation>"
source: gemini-deep-research
cost_usd: 2.8000
wall_seconds: 384
interaction_id: v1_ChdwQXo1YWJTRERlV2RfdU1QcXMzZjJRZxIXcEF6NWFiU0REZVdkX3VNUHFzM2YyUWc
agent_id: deep-research-preview-04-2026
created: 2026-05-04
tags: [research, gemini-deep-research, autogen]
---

# You are a senior research analyst specializing in AI developer tooling and the Anthropic API surface. Your output will guide a Product Manager who is building a personal autonomous agent fleet using the Claude Agent SDK (Python 0.1.63) running headlessly via macOS launchd.

<context>
The researcher's agents currently run headlessly and authenticate via `claude login` OAuth (refresh tokens stashed in macOS Keychain). They need MCP server access — specifically Slack, Google Calendar, Gmail, and Atlassian (Jira + Confluence) — but today the SDK agents cannot use MCP servers because MCP requires browser-based OAuth that's only available in interactive Claude Code sessions. The Anthropic API's "MCP connector" mode (the `mcp_servers` parameter on the Messages API) might be the right path for headless contexts.
</context>

<your_task>
Research and synthesize, grounded in 2025-2026 sources:

1. Anthropic API MCP connector capabilities (current state). What does the `mcp_servers` parameter accept? Stdio MCP servers, HTTP MCP servers, or both? What auth mechanisms are supported (capability tokens, OAuth client credentials, scoped API keys)?

2. Headless agent compatibility. Can a headless agent (no browser, no interactive OAuth flow) authenticate to MCP servers via the API? If yes, how — what's the credential pattern? If no, what's the recommended workaround?

3. `claude login` OAuth inheritance. Does the Claude Agent SDK 0.1.x line inherit MCP access from the user's `claude login` session? What scopes flow through? Caveats for long-running headless processes (token rotation, refresh, expiration)?

4. Production patterns. 2-3 published patterns (blog posts, Anthropic docs, real-world examples) from 2025-2026 of headless Claude agents accessing external services via MCP. Include code snippets if available.

5. Gaps and roadmap signals. What MCP+headless capabilities are explicitly NOT supported as of the research date? Any roadmap signals from Anthropic about closing those gaps?

Prefer official Anthropic documentation, Anthropic team member posts, and production case studies. Cite versions and dates.
</your_task>

<output_structure>
Markdown report with sections matching the 5 numbered tasks. Length 1500-2500 words. Inline citations [1], [2] tied to numbered Sources at the end.
</output_structure>

<validation>
Before finalizing:
- The `mcp_servers` API parameter spec is cited from official Anthropic docs (not blog speculation)
- Any "headless OAuth inheritance" claim is backed by SDK source code or docs, not assumptions
- It's explicit which MCP server types (stdio vs HTTP) work in API context vs only Claude Code
- API model versions tested are noted (e.g., claude-sonnet-4-6, claude-opus-4-7)
</validation>

> Generated 2026-05-04 17:22 by `gemini-dr` (agent=deep-research-preview-04-2026 · tier=dr · wall=384s).

# Headless Fleet Architecture: MCP Integration and Authentication Analysis for the Claude Agent SDK

## 1. Anthropic API MCP Connector Capabilities

The Anthropic Messages API incorporates a native Model Context Protocol (MCP) connector, enabling direct integrations with external tools and data sources without necessitating a standalone MCP client implementation. As of early 2026, this capability is accessed via the `anthropic-beta: mcp-client-2025-11-20` header, which replaces the deprecated April 2025 iteration [cite: 1]. The connector operates by passing an `mcp_servers` array within the API request payload, alongside standard parameters such as the model designation. Production testing has verified compatibility across frontier models, including `claude-sonnet-4-6`, `claude-opus-4-7`, and legacy variants like `claude-3.5-sonnet-20240729` [cite: 1, 2, 3].

A critical architectural distinction exists between the raw Messages API and interactive client environments like Claude Desktop or Claude Code. While the broader MCP specification heavily emphasizes `stdio` (Standard Input/Output) as the preferred, zero-network-overhead transport for local processes [cite: 4, 5], the Messages API MCP connector explicitly prohibits direct `stdio` connections [cite: 1]. The API parameter strictly accepts remote servers exposed via HTTP, supporting both Streamable HTTP and the older Server-Sent Events (SSE) transport mechanisms [cite: 1]. Consequently, any local MCP server intended for direct API integration must be wrapped in an HTTP interface [cite: 1].

Regarding authentication, the `mcp_servers` parameter natively supports passing credentials to secure endpoints. The primary mechanism is the `authorization_token` field within the server definition object [cite: 1, 2]. When an `authorization_token` is provided, the Anthropic API automatically injects it as an OAuth Bearer token in the headers of its outbound JSON-RPC requests to the remote MCP server [cite: 1]. The API itself remains agnostic to the token's origin, transferring the burden of credential lifecycle management to the orchestration layer.

| Authentication Paradigm | Mechanism in MCP Connector | Primary Enterprise Use Case |
| :--- | :--- | :--- |
| **Static API Keys / PATs** | Passed directly via the `authorization_token` field or injected as custom headers. | Simple deployments lacking automated rotation infrastructure (e.g., legacy Atlassian server endpoints) [cite: 6, 7]. |
| **OAuth 2.1 Bearer Tokens** | Passed via the `authorization_token` field. | Standard enterprise integrations requiring machine-to-machine (M2M) Authorization Code or Client Credentials grants [cite: 8, 9]. |
| **Scoped API Keys** | Passed via custom HTTP headers in the server definition. | Enforcing the principle of least privilege by strictly limiting permissions to the endpoints defined in the MCP tool schema [cite: 10, 11]. |
| **Capability Tokens** | Injected via custom headers or emerging standard fields. | Delegating narrow, context-specific permissions (e.g., `recipient_domain: @company.com`) with a traceable audit trail directly linked to the agent's identity [cite: 12]. |

## 2. Headless Agent Compatibility

Deploying a headless agent—defined as an autonomous process operating without interactive terminal access or graphical browser capabilities—presents specific authentication challenges for MCP servers. Because headless agents cannot execute interactive OAuth 2.0 Authorization Code flows, standard user-delegated authentication is structurally incompatible.

Headless agents can successfully authenticate to MCP servers via the API, but the credential pattern must shift from user-interactive flows to Machine-to-Machine (M2M) paradigms. The recommended and fully supported workaround relies on the OAuth 2.0 Client Credentials grant or the use of pre-provisioned Service Accounts [cite: 8, 13]. In this pattern, the headless orchestration script (acting as the API consumer) independently authenticates with the target identity provider (such as Google Workspace or Slack) to retrieve a short-lived access token before initiating the Anthropic API call [cite: 1, 9]. 

Once the token is retrieved, the orchestration layer dynamically injects it into the `authorization_token` field of the `mcp_servers` array [cite: 1, 2]. If the target MCP server requires credentials in a non-standard format or necessitates custom HTTP headers, the API and corresponding Claude Agent SDK allow developers to bypass the `authorization_token` convenience field and define explicit HTTP headers directly in the connection options [cite: 14, 15]. For services that do not support the Client Credentials grant, or where infrastructure constraints prevent dynamic token fetching, the accepted fallback is the injection of static, scoped Personal Access Tokens (PATs) retrieved from a secure environment variable or secrets vault at runtime [cite: 2, 7].

## 3. Claude Login OAuth Inheritance in the Agent SDK

The Claude Agent SDK (version 0.1.x series) offers an abstraction layer for building agents in Python and TypeScript. Architecturally, the SDK operates as a wrapper around the Claude Code CLI's headless mode (`claude -p`). When an application invokes the SDK's `query()` function or instantiates the `ClaudeSDKClient`, it spawns the CLI binary as a subprocess, communicating via a JSON-lines stream over standard input and output [cite: 16, 17]. 

This architecture guarantees complete inheritance of the underlying CLI's configuration. The SDK automatically inherits the user's `~/.claude/` configuration directory, any local `CLAUDE.md` context files, and most importantly, the authentication state stored securely in the macOS Keychain [cite: 16, 17, 18]. Consequently, an agent built with the SDK automatically possesses the exact same API access, MCP server configurations, and scopes as the interactive user session [cite: 16, 17]. The scopes flow directly through from the initial interactive `claude login` execution. However, it should be noted that as of early 2026, a known bug in the Claude Code CLI prevents the transmission of the `scope` parameter during certain custom OAuth2 authorization flows, which can cause integrations with strict identity providers to fail entirely [cite: 13].

This inheritance model introduces a severe operational vulnerability for long-running headless fleets. Claude Code utilizes an OAuth flow for authentication, generating access tokens that expire approximately every eight hours [cite: 19]. In standard interactive use, the CLI detects an expired token, retrieves the long-lived refresh token from the macOS Keychain, and seamlessly rotates the credentials via Anthropic's OAuth endpoints [cite: 20]. 

In headless or subprocess execution modes, this token rotation mechanism fundamentally fails [cite: 19]. Documented telemetry from 2026 indicates that when the Claude CLI is invoked as a subprocess lacking a TTY interface, the auto-refresh logic is bypassed or silently fails to write back to the filesystem. The agent subsequently attempts to authenticate with the expired token, resulting in a `401 authentication_error` ("Invalid authentication credentials") [cite: 19, 21]. The process terminates, and because the failure occurs within the subprocess boundary, the orchestration layer receives no actionable error message. This leaves the headless agent permanently stalled until manual human intervention completes a new browser-based login flow [cite: 19, 22]. Furthermore, concurrent headless sessions attempting to refresh simultaneously can create race conditions that overwrite valid keychain entries with empty data, corrupting the authentication state entirely [cite: 22, 23].





## 4. Production Patterns

To deploy headless Claude agents connected to enterprise MCP servers without succumbing to the aforementioned token expiration failures, engineering teams in 2025 and 2026 have adopted several robust production patterns. 

The most direct solution for macOS-based fleets relying on the native Claude Agent SDK inheritance is the deployment of an out-of-band token refresher. Utilities such as `claude-oauth-refresher` operate as background daemons managed by macOS `launchd` [cite: 20, 24]. Operating on a scheduled cadence, the script independently reads the Claude authentication profile and queries the macOS Keychain [cite: 20]. If the access token is within a 30-minute expiration window, the daemon manually executes a `POST` request to the Anthropic `v1/oauth/token` endpoint using the stored refresh token, completely bypassing the SDK's broken subprocess logic [cite: 19]. It then writes the newly minted access and refresh tokens back into the Keychain [cite: 20, 24]. Because the Claude Agent SDK reads from the Keychain upon every invocation, the agent seamlessly inherits the fresh credentials without ever encountering an expiration event [cite: 16, 25].

When building agents that must connect to remote MCP servers over HTTP without relying on the CLI's native configuration, developers utilize the `ClaudeAgentOptions` class to manually inject credentials. By defining the `mcp_servers` dictionary directly within the Python script, orchestrators can pull tokens from secure environment files or cloud secret managers and map them directly to HTTP headers [cite: 14, 15].

```python
from claude_agent_sdk import ClaudeAgentOptions
import os

options = ClaudeAgentOptions(
    permission_mode="bypassPermissions",
    mcp_servers={
        "jira_remote": {
            "type": "http",
            "url": "https://mcp.internal.company.com/jira",
            "headers": {
                "Authorization": f"Bearer {os.getenv('JIRA_M2M_TOKEN')}"
            }
        }
    }
)
```
This pattern effectively bypasses the native `authorization_token` parameter, granting the orchestration layer absolute control over token rotation logic before the agent is instantiated [cite: 14, 15]. The orchestration layer can execute an OAuth Client Credentials flow, store the token in memory, and pass it cleanly to the SDK.

For enterprise fleets seeking to eliminate local credential storage entirely, Anthropic's Claude Managed Agents (introduced in public beta via the `managed-agents-2026-04-01` header) presents a paradigm shift [cite: 26, 27]. In this architecture, the agent runs in a managed cloud sandbox [cite: 27]. Credentials for external MCP servers are stored in an Anthropic-managed secure vault [cite: 28]. 

```bash
curl -sS --fail-with-body https://api.anthropic.com/v1/sessions \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: managed-agents-2026-04-01" \
  -H "content-type: application/json" \
  -d '{
    "agent_id": "agnt_01...",
    "vault_ids": ["vlt_01..."]
  }'
```
When the agent decides to utilize a tool, a credential proxy intercepts the request outside the sandbox, matches the MCP server URL to the vault, and injects the authorization token server-side [cite: 28, 29]. The token never enters the agent's execution environment or memory space, neutralizing the risk of credential theft via prompt injection [cite: 28, 30].

| Pattern | Execution Environment | Authentication Strategy | Primary Advantage |
| :--- | :--- | :--- | :--- |
| **`launchd` Sidecar** | Local macOS Fleet | Proactive Keychain polling and rotation. | Zero code changes to existing SDK scripts; ensures 24/7 uptime for legacy setups [cite: 20]. |
| **SDK Header Injection** | Local or Hosted | M2M tokens mapped via `ClaudeAgentOptions`. | Complete developer control over the M2M token lifecycle [cite: 14]. |
| **Vault Proxy** | Claude Managed Agents | Server-side injection via Anthropic Vault. | Tokens never enter the agent sandbox, maximizing security against prompt injection [cite: 30]. |

## 5. Gaps and Roadmap Signals

Despite rapid adoption across the developer ecosystem, several critical gaps remain in the headless MCP ecosystem as of mid-2026. The most prominent architectural limitation is the lack of direct `stdio` transport support for the Messages API MCP connector [cite: 1]. While interactive desktop clients excel at spinning up local subprocess servers with zero network overhead, API-driven architectures are forced to expose local tools over Streamable HTTP [cite: 1]. This introduces network latency and complex local networking requirements for systems that otherwise operate entirely on a single machine [cite: 5, 31]. Furthermore, the MCP connector is currently explicitly not supported on Amazon Bedrock and Google Vertex, forcing developers operating within those cloud ecosystems to build custom tool-calling wrappers [cite: 1].

The underlying OAuth implementation of the Claude Code CLI also suffers from incomplete standard compliance. The CLI fails to transmit the required `scope` parameter during OAuth2 Authorization Code flows, breaking integrations with strict identity providers that mandate explicit scope definitions [cite: 13]. Combined with the persistent inability to automatically refresh tokens in subprocess environments, the native SDK remains fragile for truly autonomous, long-horizon tasks unless augmented by external rotation scripts [cite: 19, 22]. Additionally, the SDK does not support in-client OAuth 2.0 flows, requiring external handlers [cite: 32].

Roadmap signals indicate an industry-wide pivot toward resolving these M2M authorization complexities. Following Anthropic's donation of the MCP standard to the Linux Foundation's Agentic AI Foundation in late 2025, subsequent specification revisions have mandated strict OAuth 2.1 compliance featuring PKCE S256 [cite: 33]. More importantly, the protocol is actively codifying "Capability Tokens" [cite: 12, 34]. These tokens will supersede generic API keys, allowing administrators to cryptographically issue narrow, time-bound execution constraints directly to an agent's identity. This ensures that headless fleets operate under zero-trust, verifiable parameters [cite: 12]. Finally, the continued expansion of the Claude Managed Agents infrastructure suggests Anthropic intends to centralize remote MCP execution and secret management within its proprietary cloud platform, standardizing the vault-proxy pattern as the default for enterprise deployments moving forward [cite: 3, 27].



**Sources:**
1. [claude.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH2vUSMD6phu4DqTfJIguh17msdrm3CdGsW8zmYuQ0RdU22Z0QOvqqMQQ_VdQFgvg7gNEm95XkD5fbL3fhIxcRFQy3EROuyXtUkMSbl2h-gEJQUCvSqoVPAfEVgPNswjG09VqobUwZ_F6ObV0J2WfaHd6W_95zQXIc=)
2. [bria.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFRVCQUhxwjTf64NAn1M7wXxRXUOwKaYkLe1X7S9EXSSs26inu9Txeoi9-3Ms4_D4JDWpyoD0LThI7FSrKVJG8bMj_Ga-RoUstPCvjV3nZ5UiExyM4OYyUVCG4I-RY=)
3. [gitconnected.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF4F3zBxKW-2XMoNhb3SSh4hdBae3jOyewMU7Tmt3rZPwXSwKED9YjoFOOi8GtQmI9dp8OuVyaazx0Z7Ls7FMGqEl0y-vF8_B4o2RnnACeJrG3x5OiZQZeVKTgIG9pfqzRM58GV17vSPI3lt4MMQTZQXB__I0xsBz2S9yT7aBs2oXNryX6GajZtMaKVKIkiT6jLl3iO34WAvF5r_5iT-xGpXs0dNh7iVrg_u-COEYdgSZFsXzFO)
4. [modelcontextprotocol.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQErXmIl62O3VSgGnzS7xneOWIjPs94UBd0Cy79og9vyGNpSxMBiZQq_MzZQ03eR2xE74chMtjlwg_9dGkkIUqQGRK22qiryNh5sVxWS-DaQXbEFfaDPTiER-L-pTXNx9c-q_vFK6fNppPDoHMeVnGe8PX_6IrZPCa5uVcVd71E=)
5. [kirkryan.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGk09ljA776gAjArXGG6sGEpNGNpxuD_51Ll72PJUgeSrhIOaVlaUHgMsR_mxJ7GuAeXknb-oemMh6QmDNeH5PS3qLby51cuj65RoSISOs0UIq3RkFRg-iIcqtef3cAfdjPN7yVp9wPOwaT6nG5spVUAFBHL1y1HKItTg_-Pn60RzDAzu7Ulw==)
6. [pypi.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHIjwUsZ5hYVi50JMD_G72D7hP6pl63P5qoWYxwJWVIud04rg18fZay7V8buC6Q68MEW5kuNsNhTc9OP5iOzLwUiUDXQihPhN5NSjkdhZY6C0i3OtmMJqgXf6L9kiw=)
7. [cdata.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFPgAxnHxwadGMcOQonYUhyH3-nWD3B-9rvpW4xWrbjPbDN7ka3LVAa9J9wptcD8bM5fZBKthEVFpun169frMDFh9MV_DMGX68SQAAS4rCkIvuFAiwf7emV_H_UHn17QtmES_inXGUKJebijUaTX8KGoqClsw==)
8. [deepsense.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEY88K1vx8VemF4F3HhE2LEGhroHuZV724z5CPbiqsBP2Tw2ixoHSVthi_E6-tNpdEEMbiLQ8GJpJuwbZzIbEajSq4GfUn5O9fuJI0s1idZ9A_59GuluKsWUz-cGE7Hp0VKLVbrv7X8pCRd0hD7P3bF4cJoNyrCOV5qfHf2YOe6om5bdwpSYkxJ1Y5deHhbXItYq_oh2BqUnFmjTi5cxNR_eodN5ODCgFbhhsp_aw0rYcmsOXE9sxD9O0wkNaENkSgy5n7vWpXn8hJmc__EI0D1zULI0KRMD_2ddSVtQ1eko9bL)
9. [transloadit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG10UwXGuh24FlUCBtVCrC89iiK6_OYPdCB7tV6p8aibaFI5oKpkAO026fha0HrLpX794BV9iSkZRNlcNsyNTh_pS_JQIiyYrd-dQQ2yBCRLOLNKyuoPyXP4FecbgrcqFj5CJukM6I=)
10. [protocolguard.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE9WDTa0LrmOUyofslPwE5FSM3fTDZ8Y0_jISocFm7dR993G8Y6DSM3fOw9SdtSIp1IB6WgGmnLuT3QSRKsp8R56ZJbdXmGIch7bbPuwr78SESHawozyWKelRDXggYUf9ebrudk1kRMqJ1UWT5gKe4=)
11. [coder.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHadWCjT-LySCs8H4OkcI5DCAE513epdEWMIDzZX37rvdpLQQf7MJN1wr78m7CuJ3aMy_UoC3SEElAIjS9tLJBrH69YMPNXznB1e2WYYqwtFYNErFqe-yRbaesJWoM=)
12. [scalekit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFRtPVPzaQUM-FWN4WIzixwKvMnqrd9MF_e7v_GzDbXnP3scJzFjbnIaCUb35Qln4a-2Jz9Hh_udXaf3j2MHZfVWNU94mFHgX7X5_Iqc0ZRN3559U92_ryag4vf0j5azFTdqE3-GQ=)
13. [getlarge.eu](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_bMV0QG2Twvnj6vAEMgIh4UsNZeXkGzklVohE6WOR7Qf_VTdFFCQf9xVyAbdzgDQCsxOQwMTa_bNhSUY-G9te5iTuc45rh-pNv6k7bSbClBo8Y_PIf2jzM8DjgqX0RktxWsUa9edVTSSieE-N8YkEuLgMZOJKalIhfzUWDzPhRy2QaJ5nE-s68twrvH0=)
14. [composio.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEK7ziESKqI1xjTjFzMnCPspkQxtyVixDrRo7FKdkDNOaYe5pCtvzEKdUaOWbGbCvxMvH6w9-WF1eODxhB3Hg8KN9RngKNZJXXZFW9wknQKxHBUCO-koUizgt92sKwi1eaQP3a7cO233nY2HCNGy9NwSAVN7Foz)
15. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwtb6PLdsAXZj6RmmowqyA0I9Ob9KtW17lyKZc30Vx_72JI8E67lbHbujoCUV5Tcg4AOGdqb25doVqopBiPodgFIYxBRWdIv7ojK-FkvV__ci9GEzsmTxrtaOav9smAWnL36bhmibBlRHfhOYcENRO-Mq_oLZ1RZIvYZ--e3B2LGF8O9GUW6ZBEHfSZYDiseLQyAQ=)
16. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEKiI_wQL9TsNhgTBhpUxeEkBXZKLiw_0TS-Ow_CI_ZIwC-aAexs5Llvvei_-VM4nzwleJM81LzAYqHiWjMrEBJ8n2OpzsU3GMyv-aRF0CTVrcXYqm-7YuO7phf2pQj0VKApjdSEwaOlHUegdAqvJhmXTHBDqfZo6aODPo=)
17. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG1tidR0-xS-U6GjPl6gV4Q1Iy8vDhmUH0RiebXmqw6-LyXPcMX4qPsBBtLR3AER9SIxXCexoBGmyPYov5ekpxdeU2p6IzH98jGGFPD-Z6xbUV7fvMUj88SAgLxE7YELURQzbiskU5Nz14dj4Uovr5glUiNyB_wM70SrR0nGJSO-oTKhoX5cEUDrJI=)
18. [claude.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0vtdmkIg5FS19JGPfnUNPKazzg29p4FVU4Em_T-us7oa4ikflZismb3sMDPprk0Kk01ebYYXe_A8gXzlbIN_edwGB7FvTo7S9CXfub5IUdlWulo6nymfozlP1WggdudRSbKs=)
19. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG3b5CyygVJtspSvgi-SsH3SZ1rr0z1z3jpnvw73emAm-4fdc8ttBmuiwmvLGhHeSkxEVb3SQPhgTXKP_f1H5ssdbrEk_UvKvNEMqbairrZ9iaTlc2IZBIwwCSYqr__HJe6jsECMgruDuwePFM=)
20. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH-mSDmOcHbHtIjlzIRImooGvGFbppSul5cbbgQ9Y9AJP7xXt4CjExyI9vqvN2yVAzoC3ws_ewxSXfwYd6hz8ebeUE2IcAChDfvig6NZE-ms5VDxiUPNofwfm_NdmADVlKQhNOYBenzc5nBa6uW8cf680dPAe7QGBHs-A==)
21. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEg31ZAMF8gLQzZwCvSeghLKSfY1vVOko8CpqUOQGjoD8zGjywEFIFdyqxkBQSKbE7-zmp8GW_7T-GbGduHN7CBA0Rv1qwN_8L4TfxmxdGJULGq_Elu8t9WzV7tMt2DFOS_DnO2gz_zNCTGdZg=)
22. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEr7ffls8VH0IpD3LiqxDX9FQmzQqumAKxiDExnGsadvugMMeldPjlm9sGbIV2sYarDizqQqXuWkH0CDt9DrEg1aRcn3JcGGvP6qUFJtOaaAlaxOM-S53lpKbrMcvVdHOpSBJFLQiv27D2O7cw=)
23. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH5-ybtlMyes9N8Da646P5OpWnK2cxRl8xEcPBA94H7KzFR6idgxJf7e1WACZkDok-QdmhrRVEm8Pfyp9lUL7wIqs32S1E8OMTXL0UHVkvZgWXOt5iJgQ-EDi3TFLq6dA9NBXpaMrC3GAoxyqQ=)
24. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEUYxtbid9oFBB0mSpZuSeijoDwjywYrbS2g75yPLJnO1ONbcpxYxIfePieJvNkAIfVuUnU_fQbIu9ZO0kX3KhXXbB5jAdn5Aux7vyiPMg8qFAQIDXtxh9wnNjDOhpMpCff2yPBHyFxRUMb_LnBil7FgPg1PVdCMw==)
25. [clawhub.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG21EnFI-hJLVat3aq7dTZPOJVsSMeTKr1mqAwMQE66zxNDvw3vvl3rIBAcGm1DBu06M6iiC-Z0X5WZZLH9UCTiqXkYYjggVjPr7NUBAp0V9tp4_CaZDZoEAdMHZEiKhBgrcrCx05E=)
26. [apiyi.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEUJWuSTDaioef279qg_nmMI9x9uHMYRshKrW1edZdpEK70nrvU7g9LckfpYJPl5oJ2Z9j9UKy_mI8g1-h243X63yrSiHgf5rtOaM40JVMhieB_Zqj-HpaXfAO_QhJeo8CbEReFd1xQWTi3BlM4sfSG03nyWT5_qKtTUfKuvodBnNil9zYGuQc86RU=)
27. [till-freitag.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE0zG5RZuPLrY7D1X43bVSnN2e5l4D-heTxPpkzZ4WuYCh_s0syuHV56-uwQqiGZC_cl-ZHzmKMqZU02IWhrvOehCFxZ-ALepNRxCYNmF0tQYFIfqP6p1Dcj1qiCf1dFJ2hOIaC4SuKGaDI748=)
28. [pluto.security](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGsGX--V_8iXuDt087WzGwNOCYse0ZB88ZCa2msQviXkw09EtAjs12jhwXaYyP-EbQGPI4h6C2AVew6T8TDpFKohx9vl4O4w3GY-TetZ_u-IU0FW9i-XOVtna7kqflGxVon9h5pB-_pOSV9Q9psJsU=)
29. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEADbXXiEENzPaxM-he-Dhs498qaCF5_aEx7eHy0tWZ3vcZ6Z0ErVKC7i9NsQN3qnFiAcBwr6hsYlST7c6aMVF6PwNghuE_WDkfQO-Ix-02eAY3OsbrmZUtoez09mJkSucZw2E1bhcwOEWSFDlbwT7cp_OLWCImNWHSeCvQ5ng_JbSnp8qnrH-tzUMXAyWL5Y58c58Buai82BULYr-2ZiU7UpytZQLREA==)
30. [n1n.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGk2-QhPZ_gfDPXQuwSBjvNE5d2D-KMjSJXpxIiGWRwbYelxW7UgF65SR4jhrohPAmqtsCjDIX7q6EGwIlp0lBFsCNUDJBw-9bMwerVLZyC7auUU7qkK1xlT93BUCZgDZwXsE1M63BwdFR38HnbjCHqgS0GNKCr5bMlpnYKn9AHLN8JNEznFFWftNjxIlaURC4yp5GIjiBB)
31. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEaH0XGPXNge2zMSko4bB-wUWOIVjFI4ggrYRvF7cbxXuhjxZTAK9kDIXvkYlT50m2PuzEW-Jz76JAds7Snik1vuxZyasErsN9fPBrhyM-fyhaYdIADjzBjaskdviM8VR6Onvq3SL25Aspkf1mPXtyD6w1mqnrK)
32. [neo4j.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG-LYVOZ7tjD_u62Hv0fgWpgkFpYBgKqfUT-cTxYK38pH-IU1QhkhlDzArJEJrbL0t14UCOVAhdToncUXYeTeU3SIO_1i30yAEC2bohyUxTB-ocZ6pMlMfxKfYQKhqJ_xceoAF9gKs3fPKBJyAZ1V1d_QTVM14M1S9kO30=)
33. [chatforest.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEm1WBIeiVaI2Y3DEn0c0b687SuZwbQ6WADNRgKCMp8082b-UclopcnmZxKPbkCp_ecI2VSj4LxskElUywLupjLFXDggptqqVCz12trAZFdBR1GLlpj1DFkv3jnli-zw7L2W7KkysixapQcSBu24349cqtwhpw=)
34. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGax9APaRgEQCclCw_nx-Cjhv0asIF1Il06cpng7yNZCUJMTllwFWkCF5en1tYmondrfO8Ntavh52vcq4OP-jCHtolWr2Ki9eyOrqx1KNPv-ATAyRd8d977IkbVIO8sPeBCb9fZVjB_rC4=)
