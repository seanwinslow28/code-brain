---
name: obsidian-mcp-setup
description: Obsidian MCP server installation and configuration assistant. Connect Claude Code to an Obsidian vault via Model Context Protocol. Diagnoses connection failures, configures transport protocols, and verifies vault access. Use when setting up Obsidian integration, troubleshooting MCP connections, or configuring vault access for AI workflows.
---

# Obsidian MCP Setup and Connection

## Purpose

Install, configure, and troubleshoot MCP server connections between Claude Code and an Obsidian vault. Cover the three main server implementations, transport protocol selection, authentication via the Local REST API plugin, and connection verification.

## When to Use

- Setting up Obsidian vault access for the first time
- Troubleshooting "connection refused" or "spawn ENOENT" errors
- Choosing between MCP server implementations
- Configuring transport protocols (stdio, HTTP/SSE, WebSocket)
- Verifying that Claude Code can read and write vault files

## Examples

**Example 1: First-time setup**
```
User: "Connect Claude Code to my Obsidian vault"
Claude: [Uses obsidian-mcp-setup] Walks through Phase 1 setup:
1. Install Local REST API plugin in Obsidian
2. Copy API key from plugin settings
3. Add mcp-obsidian config to claude_desktop_config.json
4. Restart Claude Desktop and verify with test prompt
```

**Example 2: Troubleshooting connection**
```
User: "Obsidian MCP not connecting, getting ECONNREFUSED"
Claude: [Uses obsidian-mcp-setup] Runs connection failure decision tree:
- Checks if Obsidian is running (required for Local REST API)
- Verifies port matches (27123 HTTP / 27124 HTTPS)
- Checks SSL verification setting for self-signed certs
- Tests with absolute path to executable
```

## Server Implementation Comparison

| Server | Transport | Best For | Key Feature |
| :--- | :--- | :--- | :--- |
| `mcp-obsidian` | stdio | Claude Desktop local | Full CRUD, patch updates |
| `obsidian-claude-code-mcp` | WebSocket + HTTP/SSE | Claude Code CLI | Auto-discovery, dual transport |
| `obsidian-rag-mcp` / `smart-connections-mcp` | stdio | Semantic search | Vector embeddings, meaning-based retrieval |

Recommend `mcp-obsidian` for beginners (simplest setup, most stable). Graduate to `obsidian-claude-code-mcp` for Claude Code CLI integration, or add `smart-connections-mcp` for semantic search.

## Phase 1: Basic Read/Write Setup (mcp-obsidian)

### Step 1: Install Local REST API Plugin

In Obsidian: Settings > Community Plugins > Browse > Search "Local REST API" (by Adam Coddington) > Install and Enable. Copy the API Key from the plugin settings page.

### Step 2: Configure Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "YOUR_KEY_FROM_REST_API_PLUGIN",
        "OBSIDIAN_HOST": "127.0.0.1",
        "OBSIDIAN_PORT": "27124",
        "OBSIDIAN_PROTOCOL": "https",
        "OBSIDIAN_VERIFY_SSL": "false"
      }
    }
  }
}
```

Set `OBSIDIAN_VERIFY_SSL` to `"false"` when using self-signed certificates (the default for the plugin).

### Step 3: Verify Connection

1. Restart Claude Desktop after changing config
2. Look for the plug/tool icon listing `obsidian_read_note` and similar tools
3. Test: "Can you list the files in the root of my Obsidian vault?"

## Phase 2: Claude Code CLI Setup (obsidian-claude-code-mcp)

This plugin runs inside Obsidian and uses WebSocket for Claude Code CLI with auto-discovery.

Install the `obsidian-claude-code-mcp` community plugin in Obsidian. For Claude Desktop access (which does not support HTTP transport natively), bridge via `mcp-remote`:

```json
{
  "mcpServers": {
    "obsidian-plugin": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:22360/sse"],
      "env": {}
    }
  }
}
```

For Claude Code CLI: navigate to the vault root before starting the session so the CLI treats the vault as the project root. The plugin auto-discovers the vault.

## Phase 3: Semantic Search Setup (smart-connections-mcp)

```json
{
  "mcpServers": {
    "obsidian-smart": {
      "command": "python",
      "args": ["/path/to/smart-connections-mcp/server.py"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/Users/username/Documents/MyVault"
      }
    }
  }
}
```

Requires the Smart Connections Obsidian plugin installed first. Reuses its existing embeddings to avoid double-indexing.

## Troubleshooting Decision Tree

```
Connection failing?
|
+-- "spawn uvx ENOENT" or "npx not found"
|   +-- Use absolute path: run `which uvx` or `which npx`
|   +-- Paste full path into "command" field
|
+-- ECONNREFUSED
|   +-- Is Obsidian running? (required for Local REST API)
|   +-- Port mismatch? Default: 27123 (HTTP) / 27124 (HTTPS)
|   +-- SSL issue? Set OBSIDIAN_VERIFY_SSL to "false"
|
+-- Path issues (Windows)
|   +-- Use forward slashes: C:/Users/Name/Vault
|   +-- Use absolute paths, not relative
|
+-- Tools not appearing
    +-- Restart Claude Desktop after config change
    +-- Check JSON syntax (trailing commas break parsing)
    +-- Verify plugin is enabled in Obsidian settings
```

## Security Best Practices

- Never commit config files containing API keys to Git
- Use environment variables or local overrides for sensitive values
- Start with read-only mode for critical vaults to prevent accidental modification
- The API key scope is limited to localhost by default

## The CLAUDE.md Pattern

Place a `CLAUDE.md` file in the vault root. Claude Code reads it automatically at session start.

```markdown
# Vault Context

## Structure
- `00_Inbox/`: New captures and raw notes
- `01_Projects/`: Active, time-bound initiatives
- `02_Areas/`: Ongoing responsibilities
- `03_Resources/`: Reference materials
- `04_Archive/`: Completed items

## Rules
- Use [[WikiLinks]] for internal connections
- Always search before creating to avoid duplicates
- Never delete files without explicit permission
```

## Success Criteria

- [ ] MCP server appears in Claude tool list after restart
- [ ] Claude can list files in vault root
- [ ] Claude can read a specific note by path
- [ ] Claude can create a new note in the vault
- [ ] Connection survives Obsidian restart (auto-reconnect)

## Copy/Paste Ready

```
"Connect Claude Code to my Obsidian vault"
"Set up Obsidian MCP server"
"Obsidian not connecting, getting ECONNREFUSED"
"Which MCP server should I use for Obsidian?"
"Troubleshoot my Obsidian vault integration"
```
