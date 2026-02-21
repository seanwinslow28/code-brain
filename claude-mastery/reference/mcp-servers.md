# Common MCP Server Setup Reference

## Setup Commands

### GitHub (Remote - Official)
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```
**Capabilities**: Manage PRs, search code, read issues, create branches
**Usage**: "Find the PR that introduced the bug in auth.ts"

### PostgreSQL (Local - stdio)
```bash
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost:5432/db"
```
**Capabilities**: Query schemas, read/write data, explore tables
**Usage**: "Show me the schema for the orders table"

### Filesystem (Local - Restricted Paths)
```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/dir1 /path/to/allowed/dir2
```
**Capabilities**: Read/write files in specified directories only
**Usage**: "Search my notes for meeting minutes and summarize them"

### Slack (Local - stdio)
```bash
claude mcp add slack --env SLACK_BOT_TOKEN=xoxb-... --env SLACK_TEAM_ID=T12345 -- npx -y @modelcontextprotocol/server-slack
```
**Capabilities**: Search threads, summarize channels, post updates
**Usage**: "Summarize the last 20 messages in #engineering"

### Figma (Remote)
```bash
# Cloud version
claude mcp add --transport http figma https://mcp.figma.com/mcp

# Desktop version (requires Figma app running)
claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
```
**Capabilities**: Inspect layouts, extract design tokens, generate code from frames
**Usage**: "Convert the Login frame in this Figma URL to React code"

### Jira (Local - Python)
```bash
claude mcp add jira --env JIRA_API_TOKEN=... --env JIRA_URL=https://yourco.atlassian.net -- python main.py
```
**Capabilities**: Create tickets, transition issues, search via JQL
**Usage**: "Create a bug ticket for the login crash"

### MongoDB (Local - stdio)
```bash
claude mcp add mongodb -- npx -y @modelcontextprotocol/server-mongodb "mongodb://localhost:27017/mydb"
```
**Capabilities**: Query collections, inspect schemas, aggregate data
**Usage**: "Show me the most recent 10 orders"

### Brave Search (Local - stdio)
```bash
claude mcp add brave-search --env BRAVE_API_KEY=YOUR_KEY -- npx -y @modelcontextprotocol/server-brave-search
```
**Capabilities**: Web search with AI-friendly results
**Usage**: "Search for the latest React 19 release notes"

### Google Drive (Remote)
```bash
claude mcp add --transport http gdrive https://mcp.google.com/drive
```
**Capabilities**: Read/search Google Drive files
**Usage**: "Find my Q4 planning doc"

### Memory (Local - sqlite)
```bash
claude mcp add memory -- npx -y @modelcontextprotocol/server-memory
```
**Capabilities**: Persistent key-value memory across sessions
**Usage**: "Remember that the API key format changed in v3"

## .mcp.json Templates

### Minimal Project Setup (Database + GitHub)
```json
{
  "mcpServers": {
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### Full PM Stack (Jira + Slack + Figma + GitHub)
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "figma": {
      "type": "http",
      "url": "https://mcp.figma.com/mcp"
    },
    "slack": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "${SLACK_TEAM_ID}"
      }
    },
    "jira": {
      "type": "stdio",
      "command": "python",
      "args": ["main.py"],
      "env": {
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}",
        "JIRA_URL": "${JIRA_URL}"
      }
    }
  }
}
```

## Windows-Specific Notes

On Windows, npx cannot be executed directly by stdio transport. Wrap in cmd:

```json
{
  "mcpServers": {
    "postgres": {
      "type": "stdio",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/db"]
    }
  }
}
```
