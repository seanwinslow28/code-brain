---
name: community-navigation
description: Guides you to the best Claude Code community resources. Compares Reddit vs Discord vs GitHub, lists notable power users, and provides etiquette tips for getting high-quality answers.
---

# Community Navigation Guide

## Purpose

Navigate the diverse Claude Code ecosystem to find the right help fast. This skill helps you distinguish between "Vibe Coding" noise and engineering-grade advice, identifies the best channels for specific needs (bug reports vs. inspiration), and highlights who to follow.

## When to Use

- You need technical support for a bug or outage
- You want to find "Awesome Lists" of plugins, prompts, or MCP servers
- You are looking for inspiration or "show and tell" examples
- You need to know the proper etiquette for asking questions in Discord/Reddit

## Examples

**Example 1: Finding High-Quality Tools**
```
User: "Where can I find good MCP servers for Claude?"
Claude: [Uses community-navigation]
### 🛠️ Resource: GitHub Repos
**Best Source:** `awesome-claude-code` (GitHub)
**Why:** GitHub repos are curated and technical. Avoid Reddit for tool discovery as it contains more noise/promotional content.
**Search Query:** `site:github.com "awesome-claude-code" mcp`
```

**Example 2: Reporting a Bug**
```
User: "I think I found a bug in the latest update."
Claude: [Uses community-navigation]
### 🚨 Channel: Anthropic Discord
**Best Source:** Official Discord Server -> `#bug-reports`
**Etiquette:**
1. Search first (duplicate reports are ignored).
2. Post logs from `~/.claude/mcp.log`.
3. Be respectful (staff are present but busy).
```

## Community Ecosystem Map

| Platform | Best For | Noise Level | Vibe |
| :--- | :--- | :--- | :--- |
| **Discord (Official)** | Real-time troubleshooting, Outage reports, Staff interaction | Low (Moderated) | Professional, urgency-based |
| **r/ClaudeCode** | Deep technical discussion, Engineering workflows, CLI tips | Medium | "Engineering Rigor" |
| **r/ClaudeAI** | General news, Pricing complaints, Broad discovery | High | "Vibe Coding", casual |
| **GitHub** | Downloading tools, `CLAUDE.md` templates, "Awesome" lists | Very Low | Utilitarian, resource-heavy |
| **Twitter/X** | "Alpha" tips, thought leader announcements | Variable | Hype-driven, fast-moving |

## Notable Members & Projects

**Who to Follow (High Signal)**
*   **yksugi:** Workflow optimization (Voice/System Prompts).
*   **TheDecipherist:** Advanced configuration (`CLAUDE.md`, Hooks).
*   **IndyDevDan:** Practical, engineering-focused video tutorials.
*   **karanb192:** Deep dives on Hooks and Security automation.

**Key Projects**
*   `awesome-claude-code`: The definitive directory of plugins/agents.
*   `claude-code-templates`: CLI tool for initializing agents.
*   `claude-hooks`: Python-based safety enforcement.

## Community Etiquette & Best Practices

1.  **Engineering vs. Vibe Coding**
    *   **Rule:** In technical channels (r/ClaudeCode, Discord), avoid "It just feels wrong" feedback. Provide logs, reproduction steps, and `git status`. Acknowledge TDD and rigorous methods.

2.  **"Context Engineering" is King**
    *   **Tip:** When sharing success, don't just post the result. Post the *System Prompt*, `CLAUDE.md`, or "Context Engineering" setup that achieved it.

3.  **No Grift**
    *   **Rule:** Be transparent about self-promotion. If you built a plugin, say so. The community is skeptical of hidden ads.

## Success Criteria

- [ ] User is directed to Discord (not Reddit) for urgent bugs
- [ ] User checks GitHub (not Twitter) for tool downloads
- [ ] Questions include logs/reproduction steps (following etiquette)
- [ ] User can identify "Vibe Coding" advice vs. Engineering advice

## Copy/Paste Ready

```
"Where is the best place to report a bug?"
"Find me a list of reliable MCP servers"
"Who should I follow for advanced tips?"
"What is the etiquette for the Discord server?"
"Search for Claude Code templates on GitHub"
```
