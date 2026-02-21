---
name: changelog-navigator
description: Evaluates new Claude Code features (2025-2026) for adoption. Checks version history, identifies breaking changes, and provides a "Green Light/Red Light" framework for upgrading.
---

# What's New & Changelog Navigator

## Purpose

This skill helps you stay current with the rapid evolution of Claude Code (v2.x series). It provides a decision framework for adopting new features, lists breaking changes/deprecations, and identifies authoritative sources for announcements to separate signal from noise.

## When to Use

- You see a notification about a new Claude Code version and wonder "broken or better?"
- You encounter a feature that used to work but is now deprecated
- You want to know if a new "hype" feature (like Subagents) is worth the token cost
- You need to find the official release notes or migration guide

## Examples

**Example 1: Feature Evaluation**
```
User: "Should I start using the new Subagents feature?"
Claude: [Uses changelog-navigator]
### 🚦 Feature Analysis: Subagents
**Verdict:** 🟡 **Caution (Red Light for simple tasks)**
*   **Cost:** High token usage (separate context window).
*   **Complexity:** "Black box" decision making.
*   **Recommendation:** Use only for separated concerns (e.g., Security Audit) where isolation is critical. For simple tasks, stick to CLI commands.
```

**Example 2: Breaking Change Check**
```
User: "Why isn't my 'Output Style' working anymore?"
Claude: [Uses changelog-navigator]
### ⚠️ Deprecation Alert
Output Styles were deprecated in **v2.0.30** but **un-deprecated** later due to demand.
**Action:** Run `claude update` to ensure you are on v2.1.0+ which restores support.
```

## Adoption Framework

Use this "Green Light / Red Light" framework to evaluate any new feature:

| Criteria | 🟢 **Green Light (Adopt)** | 🔴 **Red Light (Wait/Avoid)** |
| :--- | :--- | :--- |
| **Tokens** | Uses **Lazy Loading** (loads only when invoked) | Loads >2k tokens into *every* session start |
| **Security** | Respects permissions / requires approval | Requires `--dangerously-skip-permissions` |
| **Stability** | Deterministic (e.g., Hooks, Checklists) | Relies on "Vibe Coding" / vague prompts |
| **Value** | Automates a manual task (e.g., specific linter) | Adds "Black Box" complexity (e.g., auto-commit) |

## Major Changes & Timeline (2025-2026)

### v2.1.x Series
*   **v2.1.9 (Hooks):** Introduced event listeners (`PreToolUse`, `PostToolUse`). Essential for deterministic security.
*   **v2.1.7 (Lazy Loading):** Critical performance fix. MCP tools now load only when needed, solving "context start" latency.
*   **v2.0.x (Output Styles):** Experimental styling features. Valid for persona control but volatile support history.

### V3 Series (Late 2025)
*   **LSP Support:** Language Server Protocol integration.
*   **Native MCP:** 25+ integrated servers (GitHub, PostgreSQL, etc.).
*   **Opus 4 / Sonnet 4:** 1M token context window support.

## Official Announcement Channels

| Channel | Best For | URL / Command |
| :--- | :--- | :--- |
| **CLI Check** | Real-time version check | `claude update` / `claude doctor` |
| **Discord** | Staff interaction & outage reports | `anthropic.com/discord` |
| **DeepLearning.AI** | Official Courseware & Architecture | "Claude Code: Agentic Assistant" |
| **Reddit** | "Alpha" leaks & reverse engineering | `r/ClaudeAI` |

## Success Criteria

- [ ] New features are evaluated against the Token/Security cost framework
- [ ] Breaking changes (like v2.0.30 deprecations) are correctly identified
- [ ] Users are directed to `claude doctor` for version health checks
- [ ] "Hype" features are flagged with appropriate caution

## Copy/Paste Ready

```
"What changed in the latest version?"
"Should I use the new Subagents feature?"
"List recent breaking changes"
"Is this feature deprecated?"
"Evaluate the safety of this new update"
```
