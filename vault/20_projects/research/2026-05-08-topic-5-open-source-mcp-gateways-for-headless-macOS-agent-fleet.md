# Open-Source MCP Gateways for a Headless macOS Agent Fleet

## Executive summary

The 2025–2026 open-source field does **not** yet have a single obvious drop-in project that cleanly combines all four of your requirements in one local daemon: centralized upstream OAuth custody, automatic token refresh, downstream multi-tenant policy isolation, and a reusable local MCP surface for many agents. What exists today splits into a few distinct camps: **OAuth authorities** such as urlAthenZ/mcp-oauth-proxyhttps://github.com/AthenZ/mcp-oauth-proxy, **local multi-server hubs** such as urlsamanhappy/mcphubhttps://github.com/samanhappy/mcphub, **infra-oriented reverse proxies** such as urlmicrosoft/mcp-gatewayhttps://github.com/microsoft/mcp-gateway, **registry/federation platforms** such as urlagentic-community/mcp-gateway-registryhttps://github.com/agentic-community/mcp-gateway-registry, and **thin transport adapters** such as urlpunkpeye/mcp-proxyhttps://github.com/punkpeye/mcp-proxy. citeturn24view0turn16view0turn48view0turn48view2turn49view0

If I weight **centralized OAuth lifecycle** most heavily, the strongest project in the source set is **AthenZ/mcp-oauth-proxy**: it has explicit provider implementations for GitHub, Google Workspace, Slack, and Atlassian; DynamoDB-backed token persistence; distributed refresh coordination; and multi-tenant OIDC/authz concepts. Its downside is that it is plainly built with enterprise assumptions: Quarkus, EKS/Helm, DynamoDB/KMS, Kubernetes secrets, and HTTP/OIDC-first operation. citeturn24view0turn27view0turn35view0turn37view5turn41view0turn45view0turn45view1turn45view2

If I weight **“can I have this running on my Mac in under two hours?”** most heavily, the better starting point is **MCPHub**. It is actively maintained, has a real headless mode, routes multiple servers through one daemon, exposes group/server endpoints, supports bearer authentication and OAuth server primitives, and has a live release cadence. The caveat is important: from the sources I gathered, I can verify **gateway auth storage and refresh-token support**, but I cannot verify with the same confidence that MCPHub already gives you the exact “single browser-granted upstream SaaS token vault + automatic refresh across Slack/Google/GitHub” flow you want. citeturn16view0turn17search1turn17search0turn22view0turn13view0turn14search0turn14search4

The practical conclusion is: **do not write your own gateway from scratch yet**. There are enough credible projects in flight that greenfield code would mostly be re-implementing transport, authz, and lifecycle plumbing. But you should also not expect one perfect repo to exist today. For a personal fleet, the decision is really between **auth correctness first** and **local operability first**. citeturn24view0turn16view0turn48view0turn48view2turn49view0

## Project survey

### AthenZ mcp-oauth-proxy

**Project identity.** Repo: urlAthenZ/mcp-oauth-proxyhttps://github.com/AthenZ/mcp-oauth-proxy. The repo is Apache-2.0 licensed, shows 1 star and 0 open issues on the repo page, and its latest visible commits landed on **May 8, 2026**, including changes titled “Adjust upstream refresh token ttl/expiry by provider” and a merge for a refresh-token race-condition branch. In other words: publicly tiny, but freshly maintained. citeturn24view0turn25view0

**Architecture.** This is an **HTTP/OIDC authorization server and proxy**, not a stdio daemon. The README describes it as a unified proxy for multiple identity providers, and `CLAUDE.md` enumerates OAuth/OIDC endpoints such as `TokenResource`, `AuthorizeResource`, `RegisterResource`, `WellKnownResource`, plus provider callbacks for Google, GitHub, and Atlassian. The same file describes multi-tenant OIDC resolution, token-exchange services, token stores, and both memory and enterprise store selections. That makes it the strongest “single auth authority” architecture in this survey, but it is clearly not tuned for simple local stdio fanout. citeturn24view0turn27view0

**Token storage.** This is the clearest implementation in the set. The README says tokens are stored “with encryption support (DynamoDB + KMS),” and `CLAUDE.md` names `TokenStoreDynamodbImpl`, `TokenStoreAsyncDynamodbImpl`, and `UpstreamTokenStoreDynamoDbImpl` under the AWS-backed store layer. `RefreshLockStoreDynamodbImpl.java` documents a DynamoDB lock table used for refresh coordination, while `UpstreamTokenStoreDynamoDbImpl.java` shows persisted TTL fields and refresh-participation metadata for upstream token rows. One nuance: the refresh-lock table itself is explicitly documented as **not encrypted**, even though the main token store path is described as encrypted. citeturn24view0turn27view0turn35view0turn37view5turn37view0

**Token refresh.** Source-level evidence here is unusually strong. `RefreshCoordinationService.java` says it provides “Distributed refresh coordination via DynamoDB lease locks” and explicitly serializes centralized upstream refresh. `GoogleWorkspaceUpstreamRefreshClient.java` states that promoted providers route refreshes through `UpstreamRefreshService`, which “holds the L2 lock and writes back to L2.” Provider implementations then expose concrete refresh paths: `TokenExchangeServiceGithubImpl.java` has `refreshWithUpstreamToken(...)`; `TokenExchangeServiceAtlassianImpl.java` documents rotating refresh tokens and says the newly returned token is always persisted; `TokenExchangeServiceSlackImpl.java` also implements `refreshWithUpstreamToken(...)`. The May 2026 commit log further shows work on provider-specific refresh TTLs, per-client token caches, race-condition handling, and cross-region fallback. citeturn41view0turn41view1turn45view0turn45view1turn45view2turn41view9turn25view0

**Multi-tenant and scope isolation.** The repo claims multi-tenant OIDC provider support, dynamic client registration, Athenz-backed fine-grained authorization decisions, and subject/scope-based authorization. That is much closer to your desired “Agent A sees Calendar, Agent B sees Slack” model than the more hobby-oriented tools. I did not surface a source line showing exactly how downstream “agent identity” maps to provider scopes, but the architecture clearly supports client-level and tenant-level separation. citeturn24view0turn27view0turn25view0

**Service coverage.** This is the best-covered project in the sample for your target services. The README names Google, GitHub, Atlassian, and Okta as unified identity providers, and the service layer includes `TokenExchangeServiceGithubImpl.java`, `GoogleWorkspaceUpstreamRefreshClient.java`, `TokenExchangeServiceAtlassianImpl.java`, and `TokenExchangeServiceSlackImpl.java`. That is the closest match to your Slack + Google + GitHub + Atlassian requirement. citeturn24view0turn39view0turn45view0turn45view1turn45view2turn41view9

**Headless-friendliness and maturity.** Once configured, it is plainly meant to run headless; it is a Quarkus service with Helm deployment, health checks, metrics, and certificate reloaders. The public-adoption signal is mixed: **excellent architecture**, **weak public GitHub social proof**. I would call it **production-shaped but not yet community-validated**. citeturn27view0turn24view0turn25view0

### MCPHub

**Project identity.** Repo: urlsamanhappy/mcphubhttps://github.com/samanhappy/mcphub. The repo page shows roughly **2.1k stars**, the commit history shows active work through **April 23, 2026**, and the releases page shows version `v0.12.16` on **May 8, 2026**. Issue activity is brisk: the issues page showed 25–26 open issues while the search result for the issues page reported **259 closed**, which is roughly **10.4:1 closed/open**. The repo page says Apache-2.0, though `package.json` still says `ISC`; if licensing is sensitive for you, verify that discrepancy before vendoring. citeturn16view0turn13view0turn15search7turn14search0turn17search1

**Architecture.** MCPHub is a **single daemon** that centrally manages multiple MCP servers and APIs, exposes them via **HTTP/SSE**, and can run with or without the dashboard UI. The README explicitly lists centralized management, HTTP/SSE endpoints for all servers or groups, hot-swappable config, group visibility controls, compact bearer auth, and a headless mode via `DISABLE_WEB=true`. This is the cleanest “one local process, many downstream agents” design in the set. citeturn16view0

**Token storage.** For gateway auth, there is clear source evidence of persistent storage. `.env.example` says turning on `DB_URL` enables database-backed mode, and `src/betterAuth.ts` throws if `DB_URL` is absent, then wires Better Auth to a PostgreSQL dialect. `package.json` also includes both `better-auth` and `better-sqlite3`, though the file-level code I surfaced for auth uses Postgres. What I **could not verify** from the gathered source set is where **upstream provider OAuth tokens** for Slack / Google Workspace / GitHub are persisted, if MCPHub itself is acting as the OAuth client rather than simply proxying configured downstream servers. citeturn15search1turn22view0turn17search1

**Token refresh.** MCPHub’s sample `mcp_settings.json` clearly includes an internal OAuth server that supports the `refresh_token` grant and lifetimes for access tokens, refresh tokens, and authorization codes. That proves the gateway can issue and refresh **its own** tokens. It does **not** prove, from the sources I collected, that MCPHub already does centralized auto-refresh for upstream Slack/Google/GitHub tokens in the way you want. In other words: gateway-issued token refresh is sourced; upstream SaaS refresh remains **unverified** in the available material. citeturn17search0turn16view0

**Multi-tenant and scope isolation.** MCPHub has the best personal-fleet ergonomics here. The README says it supports granular group visibility for tools, prompts, and resources, and separate endpoints for all servers, specific groups, or individual servers. That is not the same thing as OAuth-scope partitioning, but for a 14-agent fleet it is a useful practical isolation boundary: one agent can hit `/mcp/calendar`, another `/mcp/slack`, another `/mcp/$smart/ops`, each with different bearer credentials. citeturn16view0

**Service coverage.** Coverage is configuration-driven rather than deeply built-in. The shipped sample config includes Slack via `@modelcontextprotocol/server-slack`; social login covers Google and GitHub; and the issue tracker shows real-world Jira/Atlassian usage. But I did **not** surface source proof that MCPHub ships a first-class unified OAuth bridge for Slack + Google Calendar/Gmail/Drive + GitHub the way AthenZ does. It is better described as an orchestrator that can host or route many MCP servers, some of which may themselves handle those services. citeturn17search0turn16view0turn14search3

**Headless-friendliness and maturity.** This is where MCPHub shines for your exact environment. It has a documented Docker path, a real headless mode, local endpoints, releases, and strong visible maintenance. It also has a couple of caution lights: an open security-report placeholder issue and real-world connection issues against some clients and Jira Cloud. That reads like “serious fast-moving project,” not “weekend toy.” citeturn16view0turn13view0turn14search0turn14search2turn14search3turn14search4

### Microsoft MCP Gateway

**Project identity.** Repo: urlmicrosoft/mcp-gatewayhttps://github.com/microsoft/mcp-gateway. The repo is MIT licensed, had about **625 stars** on the repo page, **7 open issues**, and the commit history shows visible commits through **March 16, 2026**. Freshness is good; maintenance is active; public signal is strong. citeturn48view0turn51view0turn47search3

**Architecture.** This is a classic **infrastructure reverse proxy plus control plane** for MCP servers. The README describes adapter routing, tool-gateway routing, session-aware stateful routing, bearer-token/RBAC on both data and control planes, and lifecycle management for MCP servers in Kubernetes. This is the most infra-native gateway in the sample. It is **not** trying to be a local OAuth token vault for consumer SaaS connections. citeturn48view0

**Token storage and refresh.** In the gathered sources, I found no concrete file-level evidence of upstream OAuth token persistence or refresh behavior. The gateway clearly has authn/authz layers, but nothing I collected shows local custody of Slack/Google/GitHub user refresh tokens. I would therefore treat it as a routing/control-plane project, not an OAuth-holder project, until proven otherwise. citeturn48view0turn51view0

**Isolation, coverage, and maturity.** Gateway-side isolation looks strong thanks to bearer auth and RBAC, but upstream-provider scope isolation was not surfaced. Service coverage is generic: it front-ends MCP servers rather than shipping first-class Slack/GitHub/Google provider logic. Maturity is high because the repo is official, recent, and infra-shaped. One interesting signal from the commit log is a **November 2025 “Add AuthZ support”** commit and a **“Remove SSE support”** commit, which implies the current direction is more streamable-HTTP-centric than transport-agnostic. citeturn48view0turn51view0

### Agentic MCP Gateway Registry

**Project identity.** Repo: urlagentic-community/mcp-gateway-registryhttps://github.com/agentic-community/mcp-gateway-registry. The repo is Apache-2.0 licensed, showed **637 stars**, **89 open issues**, and a latest visible release on **May 7, 2026**. The exact latest commit date did not surface in the retrieved lines, so I am not going to fabricate it; the release cadence at least says it is currently active. citeturn48view2turn50view0

**Architecture.** This is a **federated platform** rather than a simple local bridge: gateway, server registry, agent registry, A2A hub, external registry integration, and a unified control plane. The README explicitly pitches it as a way to replace scattered server connections with one gateway and governed access, and it references integration with external registries including Anthropic’s MCP Registry. This is the strongest “federated / governed platform” entry in the survey. citeturn48view2turn50view0

**Token handling and isolation.** The source set shows strong OAuth positioning — secure OAuth authentication, Keycloak/Entra integration, an `auth_server` directory, a `credentials-provider` directory, a `get_asor_token.py` utility, and a `start_token_refresher.sh` script in the root. That is good evidence that refresh and credential lifecycle are treated as first-class concerns. But I did **not** surface the underlying token store implementation or its exact refresh policy, so storage and refresh strategy remain **partially unknown**. On policy isolation, this project looks very strong: the README repeatedly frames governance, multi-tenant access, and curated tool catalogs as central value props. citeturn48view2turn50view0

**Service coverage and maturity.** Coverage is broadly about registered MCP servers and agents rather than hard-coded provider connectors, so I would not treat it as “Slack/Google/GitHub built-in” without checking live docs. Maturity looks significant — docs, demos, AWS workshop content, releases — but the open-issue load is also high enough that I would be cautious about calling it low-friction for a one-person macOS fleet. citeturn48view2turn50view0

### MCP Proxy

**Project identity.** Repo: urlpunkpeye/mcp-proxyhttps://github.com/punkpeye/mcp-proxy. The repo page shows **254 stars**, **6 open issues**, BSD-2-Clause licensing, and the commit history I pulled showed visible commits on **July 5, 2025**. A search result for the issues page showed **23 closed** issues, giving roughly **3.8:1 closed/open**. Because July 2025 is well over 90 days old relative to May 8, 2026, I would flag it as **stale for a fast-moving MCP edge component** unless you verify newer activity outside the lines I gathered. citeturn49view0turn4view0turn8search0

**Architecture.** MCP Proxy is a **thin transport adapter**: it runs a stdio MCP server as a child process and exposes it over **streamable HTTP and SSE**. It supports stateless mode, API-key auth, shell spawning, TLS knobs, and tunnels. This is a useful building block, but it is not a multi-tenant gateway and it is definitely not an OAuth holder. It is best thought of as plumbing, not policy. citeturn49view0

**Token storage, refresh, and isolation.** There is no upstream OAuth model here. The only auth visible in the README is an optional API key supplied via CLI or env var and required by clients in `X-API-Key`. There is no source evidence of persistent OAuth token storage, refresh scheduling, or per-agent scope partitioning. citeturn49view0

### Docker MCP Gateway

**Project identity.** Repo: urldocker/mcp-gatewayhttps://github.com/docker/mcp-gateway. The official repo search results showed roughly **1.4k stars** and **78 open issues**. I did not surface an exact last-commit date in the retrieved lines, but the activity page and open issues show substantial activity in April 2026, so it is clearly not abandoned. I also did not surface a license line in the sources I collected, so I am leaving that as unknown rather than guessing. citeturn46search0turn46search16turn46search7

**Architecture.** From the repo summary and supporting tutorial material, Docker MCP Gateway is a CLI/plugin-style **containerized gateway** that runs MCP servers through Docker, provides centralized management and secret handling, and can expose either **local stdio** or **network transports such as SSE**. That local-operator shape is highly relevant to your use case. citeturn46search0turn46search10turn46search18

**Token handling and maturity.** The product messaging says Docker handles setup, authentication, and security, and a tutorial emphasizes secret management. But the sources I gathered do **not** tell me where OAuth tokens are actually stored, whether refresh happens proactively or lazily, or how per-agent provider scopes are isolated. One open issue is especially relevant to your problem space: **“Docker MCP Gateway does not refresh updated env config for existing client sessions”** from April 6, 2026, which suggests active session/state invalidation is still a rough edge. So: excellent ergonomics signal, incomplete auth-lifecycle evidence. citeturn46search1turn46search7turn46search18

### Personal packaging pattern

A useful “published personal pattern” in the 2025–2026 corpus is urlhwdsl2/docker-mcp-gatewayhttps://github.com/hwdsl2/docker-mcp-gateway, which describes itself as a self-hosted multi-server hub “powered by MCPHub + Caddy,” fronted by bearer auth, configured by env file, and updated “5 days ago” in the search result. That is close to the pattern many solo operators actually want: one box, one endpoint, multiple upstream tools. What I could **not** verify from the gathered material is any first-class upstream OAuth custody or refresh logic, so I would treat it as a packaging convenience layer, not a definitive answer to your OAuth pain. Also, explicitly named “bridge” projects in the sources I saw — for example an OAuth-protected ChatGPT-focused bridge — were app-specific front doors rather than general-purpose local OAuth hubs, so I did not rank them with the main candidates. citeturn46search2turn0search2turn47search18

## Comparison matrix

The table below ranks projects by **fit for a personal 14-agent macOS fleet** that wants one shared access layer to Slack, Google, and GitHub, while heavily penalizing projects that do not show clear upstream OAuth refresh behavior.

| Rank | Project | Freshness and health | Transport and process model | Token storage | Token refresh | Isolation model | Service coverage | Headless | Bottom line |
|---|---|---|---|---|---|---|---|---|---|
| 1 | MCPHub | Last commit Apr 23 2026; ~2.1k stars; ~259 closed / 25 open; active releases | Single daemon; HTTP/SSE endpoints; dashboard optional; headless mode | PostgreSQL for Better Auth is sourced; upstream provider token store not surfaced | Gateway refresh-token grant is sourced; upstream SaaS refresh unverified | Group/server visibility and bearer-gated endpoints | Config-driven; Slack example, Google/GitHub social login, Atlassian seen in issues | Yes | Best **practical** fit on a Mac, but upstream OAuth centralization still needs verification |
| 2 | AthenZ mcp-oauth-proxy | Last commit May 8 2026; 1 star; 0 open issues | HTTP/OIDC auth server; enterprise daemon with provider-specific services | DynamoDB token stores with encryption support; refresh-lock table is unencrypted | Strongest sourced auto-refresh story in the set | Multi-tenant OIDC + fine-grained authz | Slack, Google, GitHub, Atlassian, Okta | Yes | Best **auth architecture** fit, but heavy and not local-first |
| 3 | Docker MCP Gateway | Active in Apr 2026; ~1.4k stars; 78 open issues; commit date not surfaced | Docker CLI/plugin; centralized containerized gateway; local stdio or network transports | Secret handling is claimed; precise token store unknown | No clear sourced upstream OAuth refresh details | Unknown from gathered sources | Broad server catalog; official positioning is strong | Yes | Strong operator UX, weak evidence on your core OAuth-refresh requirement |
| 4 | Agentic MCP Gateway Registry | Latest visible release May 7 2026; 637 stars; 89 open issues | Federated gateway + registry + A2A hub | Auth server and credential tooling present; storage implementation not surfaced | Token refresher exists, strategy not surfaced | Strong governance / FGAC positioning | Registry-based, not clearly built-in providers | Yes | Strong governed platform, probably too heavy for a personal fleet |
| 5 | Microsoft MCP Gateway | Last commit Mar 16 2026; ~625 stars; 7 open issues | Reverse proxy + control plane for K8s; streamable-HTTP-centric | No information found in available sources | No information found in available sources | Bearer auth + RBAC at gateway | Generic MCP servers, not SaaS-specific | Yes | Excellent infra proxy, weak fit for centralized personal OAuth custody |
| 6 | MCP Proxy | Last visible commit Jul 5 2025; 254 stars; ~23 closed / 6 open; stale | Thin stdio child-process wrapper exposed as HTTP/SSE | None | None | API key only | Service-agnostic | Yes | Useful plumbing, not a gateway answer |
| 7 | hwdsl2/docker-mcp-gateway | Search result says updated 5 days ago; stars/issues not gathered | Self-hosted packaged hub built on MCPHub + Caddy | Unknown | Unknown | Bearer auth | Multi-server hub | Yes | Interesting personal packaging pattern, but too little sourced detail for core recommendation |

The ranking above is the crux of the market right now: **AthenZ wins on auth mechanics, MCPHub wins on local operability**. Everything else is either more enterprise and less OAuth-specific, or more ergonomic and less explicit about centralized SaaS token lifecycle. citeturn24view0turn25view0turn16view0turn13view0turn14search0turn46search0turn46search7turn48view0turn51view0turn48view2turn49view0turn4view0turn46search2

## Recommended setup recipe

For a **competent engineer on macOS who wants a working local gateway in under two hours**, the most realistic recommendation from this source set is **MCPHub**. I am choosing it over AthenZ for this artifact because I can make the MCPHub path concrete and reproducible from the gathered sources. The important caveat stays the same: you should treat **upstream provider OAuth storage/refresh** as the thing to verify in a short pilot before migrating all 14 agents. citeturn16view0turn15search1turn22view0turn17search0

### Install and persistent layout

Use a dedicated local directory so the daemon, config, and mounted data survive restarts.

```bash
mkdir -p "$HOME/mcphub/data"
cat > "$HOME/mcphub/mcp_settings.json" <<'JSON'
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headless"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "replace-me",
        "SLACK_TEAM_ID": "replace-me"
      }
    }
  },
  "systemConfig": {
    "oauthServer": {
      "enabled": true,
      "accessTokenLifetime": 3600,
      "refreshTokenLifetime": 1209600,
      "authorizationCodeLifetime": 300,
      "requireClientSecret": false,
      "allowedScopes": ["read", "write"],
      "requireState": false,
      "dynamicRegistration": {
        "enabled": true,
        "allowedGrantTypes": ["authorization_code", "refresh_token"],
        "requiresAuthentication": false
      }
    }
  },
  "bearerKeys": [],
  "prompts": [],
  "resources": []
}
JSON
```

The `mcp_settings.json` shape above is directly aligned with the shipped sample file, including the internal OAuth server’s access-token and refresh-token settings, and the Slack example comes from the repo’s own sample config. citeturn17search0

### Run the gateway

```bash
docker run -d \
  --name mcphub \
  --restart unless-stopped \
  -p 3000:3000 \
  -e ADMIN_PASSWORD='change-this-now' \
  -e DB_URL='postgresql://mcphub:mcphub@host.docker.internal:5432/mcphub' \
  -e BETTER_AUTH_SECRET='replace-with-a-long-random-string' \
  -e BETTER_AUTH_URL='http://localhost:3000' \
  -e GOOGLE_CLIENT_ID='replace-me' \
  -e GOOGLE_CLIENT_SECRET='replace-me' \
  -e GITHUB_CLIENT_ID='replace-me' \
  -e GITHUB_CLIENT_SECRET='replace-me' \
  -v "$HOME/mcphub/mcp_settings.json:/app/mcp_settings.json" \
  -v "$HOME/mcphub/data:/app/data" \
  samanhappy/mcphub
```

That command is based on the project’s Docker quick start, its `.env.example`, and the fact that `src/betterAuth.ts` requires `DB_URL` for PostgreSQL-backed Better Auth storage. The Google and GitHub client variables also come straight from `.env.example` and `betterAuth.ts`. citeturn16view0turn15search1turn22view0

### Do the one-time interactive setup

Open `http://localhost:3000`, sign in as `admin`, and use the UI while the web bundle is still enabled. This is the practical place to do your **one-time human interaction**: register your servers, create groups, and set bearer keys per agent or per agent class. Once the initial config is stable, you can flip into headless mode by adding `DISABLE_WEB=true` and restarting the container. The README explicitly documents the admin login behavior, the headless flag, and the group/server endpoint patterns. citeturn16view0

The one thing I would **not** assume without a pilot is that MCPHub already stores and refreshes your upstream SaaS user tokens exactly the way AthenZ does. The sources I gathered prove gateway auth, OAuth server settings, and social login. They do **not** prove a centralized refresh vault for Slack/Google Workspace/GitHub user grants. So make that your first validation check before migrating all 14 agents. citeturn17search0turn22view0

### Connect the agents

Point agents at the gateway rather than at individual upstream MCP servers. MCPHub offers these endpoint forms:

- `http://localhost:3000/mcp` for everything
- `http://localhost:3000/mcp/{group}` for a service slice
- `http://localhost:3000/mcp/{server}` for a single server
- `http://localhost:3000/mcp/$smart` for routing across tools

The clean operational pattern for a 14-agent fleet is to make **one group per trust zone**, not one giant endpoint: for example `calendar`, `mail`, `github`, `slack`, `ops`, and `smart`. Then bind each agent to the narrowest group that matches its schedule and purpose, and give it a distinct bearer key. The README documents the endpoint forms and the fact that MCP endpoints require authentication by default. citeturn16view0

### How refresh works and what to monitor

For the gateway’s **own** OAuth server, refresh is clearly supported: the sample config includes `authorization_code` and `refresh_token` grants and sets refresh-token lifetime to 14 days. That means downstream agent-facing access can be made durable without hand-rotating tokens. What is still unresolved from the source set is upstream provider-token refresh, so you should monitor it explicitly with synthetic checks. citeturn17search0

The main failure modes I would watch are:

- **client/session compatibility problems** on streamable HTTP or SSE; MCPHub had a real “missing `sessionId`” compatibility issue that was fixed in February 2026, which tells you session semantics are an area to regression-test, especially with multiple agents using the same grouped endpoints. citeturn14search2
- **OAuth edge cases**; the Apr 21, 2026 commit stream includes “enhance OAuth redirect URI handling,” which is good news, but also a sign that auth flows were still moving recently. citeturn13view0
- **security and maintenance drift**; there is an open security-report placeholder in the issues list, so keep the image current rather than pinning a stale build forever. citeturn14search0
- **Atlassian/Jira instability**; there was a real Jira Cloud connection-closed issue in the tracker. If Jira matters, test it early. citeturn14search3

My practical rollout order would be: first prove the gateway itself with two or three agents and narrow groups, then verify whether your chosen upstream Slack / Google / GitHub MCP servers actually centralize tokens inside MCPHub the way you want. If they do, scale to all 14. If they do not, MCPHub is still a good fanout layer, and **AthenZ/mcp-oauth-proxy** becomes the auth-centric next step instead of a scratch-built replacement. citeturn16view0turn24view0turn45view0turn45view1turn45view2

## Open questions and limitations

The biggest gap in the current evidence is that I did **not** surface a single repo in the sample that simultaneously proved all of the following with source-level clarity: **local macOS-friendly deployment, shared upstream OAuth custody for Slack/Google/GitHub, automatic refresh, per-agent policy isolation, and reusable stdio transport**. That gap is why the field still feels fragmented. citeturn24view0turn16view0turn48view0turn48view2turn49view0

I also did not surface a convincing official open-source gateway from urlAnthropichttps://www.anthropic.com in the gathered 2025–2026 corpus; the “bridge” projects I did find were usually app-specific front doors rather than reusable local OAuth gateways. Treat that as a limitation of the collected source set, not as proof that no such project exists anywhere. citeturn0search2turn48view2

Finally, some projects had incomplete visibility for one or more axes from the retrieved lines — especially exact last-commit dates or closed-issue counts for Docker and Agentic. Where that happened, I marked the field as “unknown” or “not surfaced” rather than filling it in from guesswork.