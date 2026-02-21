---
name: mcp-integration
description: MCP (Model Context Protocol) server setup and debugging guide for Claude Code. Configures stdio and HTTP transports, manages user/project/managed scopes, sets up common servers (GitHub, PostgreSQL, Slack, Figma, Jira, Obsidian, filesystem), handles OAuth 2.1 authentication, and troubleshoots connection failures. Use when connecting Claude Code to external tools, setting up MCP, debugging MCP errors, or adding a new MCP server.
---

# MCP Server Integration Guide

## Purpose

Set up, configure, and debug MCP (Model Context Protocol) server connections that extend Claude Code with external tools and data sources. MCP standardizes how Claude connects to databases, APIs, design tools, and project management systems through a universal client-server protocol.

## When to Use

- Connecting Claude Code to an external service (Jira, Slack, Figma, databases)
- Setting up a new MCP server (choosing transport, scope, authentication)
- Debugging MCP connection failures or tool errors
- Choosing between user, project, and managed scope for a server
- Understanding why MCP tools are not appearing or loading slowly
- Configuring OAuth 2.1 for remote MCP servers

## Examples

**Example 1: Setting up a database connection**
```
User: "Connect Claude Code to my PostgreSQL database"
Claude: [Uses mcp-integration] Runs:
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost/mydb"

Verifies with /mcp to check connection status. Tests with: "Show me the schema for the users table."
```

**Example 2: Debugging a connection failure**
```
User: "My GitHub MCP server isn't connecting"
Claude: [Uses mcp-integration] Troubleshooting steps:
1. Run /mcp to check server status
2. Run claude --debug to see initialization errors
3. Check if GITHUB_TOKEN env var is set
4. Test server in isolation: npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-github
5. On Windows: wrap command in cmd /c
```

**Example 3: Project vs user scope decision**
```
User: "Should I put the Jira MCP config in .mcp.json or my personal config?"
Claude: [Uses mcp-integration]
- .mcp.json (project scope): If the whole team needs Jira access -- committed to git, requires one-time user approval
- ~/.claude.json (user scope): If only you need it, or it requires your personal API token
- .claude/settings.local.json: If project-specific but contains your personal credentials (git-ignored)
Recommends: .mcp.json for the server definition, personal API token in an env var.
```

## MCP Architecture

MCP provides three primitives:
- **Tools**: Executable functions (create_issue, query_database, send_message)
- **Resources**: Read-only data (file contents, API responses, log streams)
- **Prompts**: Reusable templates for common operations

## Transport Types

| Transport | Protocol | Best For |
|-----------|----------|----------|
| **stdio** | Subprocess stdin/stdout | Local tools (databases, filesystem, CLI wrappers) |
| **http** | HTTP POST + SSE | Remote/cloud services (GitHub, Figma, SaaS APIs) |

**stdio** runs the server as a child process of Claude Code. Low latency, no network config needed.
**http** connects to a remote endpoint. Supports OAuth, load balancers, multi-client access.

## Configuration Scopes

| Scope | File | Shared? | Precedence | Use Case |
|-------|------|---------|-----------|----------|
| Local | `~/.claude.json` (project key) | No | Highest | Personal API keys, experimental servers |
| Project | `.mcp.json` (repo root) | Yes (git) | 2nd | Team tools (database, Jira, GitHub) |
| User | `~/.claude.json` (global key) | No | 3rd | Personal tools across all projects |
| Managed | System path | Enforced | Override | Enterprise IT-mandated servers |

If the same server name exists in multiple scopes, Local wins over Project wins over User.

## The .mcp.json Format

```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "remote-service": {
      "type": "http",
      "url": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

**Key fields:**
- `type`: `"stdio"` or `"http"`
- `command` / `args`: executable and arguments (stdio only)
- `url`: endpoint URL (http only)
- `env`: environment variables passed to the process (supports `${VAR}` expansion)
- `headers`: HTTP headers for authentication (http only)

## Common Server Setup Commands

For the complete setup reference with all servers, see `references/mcp-servers.md`.

### GitHub (Remote)
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

### PostgreSQL (Local)
```bash
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost/db"
```

### Filesystem (Local - Restricted Paths)
```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /Users/me/Projects /Users/me/Docs
```

### Slack (Local)
```bash
claude mcp add slack --env SLACK_BOT_TOKEN=xoxb-... --env SLACK_TEAM_ID=T12345 -- npx -y @modelcontextprotocol/server-slack
```

### Figma (Remote)
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

## Tool Search (Lazy Loading)

When many MCP servers are configured, tool definitions can consume 50k+ tokens. Claude Code uses Tool Search to load tools on demand.

- **How it works**: Instead of loading all tool schemas, Claude loads a lightweight search index. When it needs a capability, it searches for relevant tools and loads only those schemas.
- **Activation**: Automatic when tools exceed 10% of the context window
- **Override**: Set `ENABLE_TOOL_SEARCH=false` to load all tools upfront, or `ENABLE_TOOL_SEARCH=auto:5` to change the threshold to 5%

## OAuth 2.1 for Remote Servers

Remote HTTP servers must use OAuth 2.1 with PKCE for authentication:
- Never share tokens between servers
- Use Resource Indicators to bind tokens to specific servers
- Validate redirect_uri strictly (localhost or HTTPS only)
- Claude Code handles the OAuth flow automatically for supported servers

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Server not appearing in /mcp | Config syntax error | Check JSON validity in .mcp.json |
| "Connection refused" | Server not running or wrong port | Check command path; on Windows use `cmd /c npx` |
| Tools not loading | Context limit or tool search active | Run `/mcp` to check; set ENABLE_TOOL_SEARCH=false to test |
| "Environment variable not found" | ${VAR} not set in shell | Export the variable or use ${VAR:-default} syntax |
| Large responses truncated | Output token limit | Set MAX_MCP_OUTPUT_TOKENS=50000 |
| Auth errors on remote server | OAuth token expired or missing | Re-authenticate; check token scopes |

**Debug commands:**
- `/mcp` -- interactive server status
- `claude mcp list` -- all configured servers across scopes
- `claude --debug` or `claude --mcp-debug` -- raw JSON-RPC messages
- `npx @modelcontextprotocol/inspector <command> <args>` -- test server independently

## Security Best Practices

1. Never commit API tokens to .mcp.json -- use `${ENV_VAR}` expansion
2. Run untrusted servers in Docker containers or sandboxed environments
3. Use project scope (.mcp.json) for team tools; user scope for personal tokens
4. Audit MCP server tool definitions before granting access
5. Combine MCP tools with Skills: MCP provides the tools, Skills provide the procedures ("When querying users table, always exclude password_hash column")

## Success Criteria

- [ ] Server appears in /mcp with connected status
- [ ] Tools are discoverable and callable from Claude Code
- [ ] Credentials are stored in environment variables, not hardcoded
- [ ] Correct scope is chosen (project for team, local for personal secrets)
- [ ] Connection failures are diagnosed with debug mode

## Copy/Paste Ready

```
"Connect Claude Code to my PostgreSQL database"
"Set up the GitHub MCP server"
"Why isn't my MCP server connecting?"
"Add Jira integration to this project"
"Set up Slack MCP for team notifications"
```
