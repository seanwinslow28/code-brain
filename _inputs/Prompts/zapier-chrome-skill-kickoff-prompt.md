# Claude Code Kickoff Prompt — Zapier MCP + Chrome Automation Skill

Paste everything below the line into Claude Code:

---

I want you to create a new Skill using the skill-system-mastery framework located at:
`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/skill-system-mastery`

Read that skill's SKILL.md first so you understand the structure and conventions for building skills in this system.

## What this Skill does

This Skill combines **two tools you already have access to** into one coordinated workflow for building, editing, and maintaining Zapier Zap workflows end-to-end:

1. **Zapier MCP** — for API-level actions (storage read/write, find/create/delete events, trigger Zaps, etc.)
2. **Claude in Chrome** — for browser-based UI automation of the Zapier Zap Editor (swapping steps, changing action configurations, updating dropdown selections, adding/removing steps)

The problem this solves: The Zapier MCP can only perform API actions — it cannot edit Zap step configurations, change which apps/accounts a step uses, or rearrange workflow logic. Those changes require interacting with Zapier's web-based editor UI. This Skill bridges that gap by using Claude in Chrome to handle all editor-level changes.

**Read the official Anthropic documentation on Claude in Chrome integration before building this Skill:**
https://code.claude.com/docs/en/chrome

This confirms you have access to Chrome browser automation via the `/chrome` command. You can navigate pages, click buttons, fill forms, read the DOM/accessibility tree, and interact with any site the user is logged into — including Zapier.

## Skill Name

`zapier-chrome-automation`

## Skill Location

Create it at:
`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/skills/zapier-chrome-automation/`

## Account Requirement — CRITICAL

All Zapier browser automation MUST target my work Google account: **swinslow@theblock**

This is where all of my Zaps are built and where I'm logged into Zapier. Build the following safeguard into the Skill:

### Pre-flight Account Verification (required before ANY browser automation)
1. Before performing any Zapier editor interaction, navigate to `zapier.com/app/zaps`
2. Read the page to confirm the logged-in account is **swinslow@theblock**
3. If the account does NOT match, **STOP immediately** and alert me with:
   - "Wrong Zapier account detected. Please close other Chrome profiles and ensure only your swinslow@theblock profile is open, then re-run /chrome."
4. Only proceed with editor automation after account verification passes

If Chrome is not yet connected, prompt me to run `/chrome` or launch with `claude --chrome` and ensure my work profile is the active Chrome window.

## Core Capabilities the Skill Should Cover

### Category 1: API Actions (via Zapier MCP)
- Read/write Zapier Storage values
- Search for and retrieve events across connected apps
- Backfill storage with existing ID mappings between source and destination apps
- Test Zap trigger/action logic programmatically
- Clean up test data

### Category 2: Zap Editor UI Actions (via Claude in Chrome)
- Navigate to a specific Zap by name or URL
- Open a specific step in the Zap editor
- Change a step's app, action/trigger type, or account
- Update field values within a step (e.g., change which calendar, which spreadsheet, which channel)
- Add new steps to a Zap
- Remove steps from a Zap
- Reorder steps in a Zap
- Turn a Zap on/off
- Test individual steps within the editor
- Save/publish changes

### Category 3: Coordinated Workflows (combining both)
- Full Zap creation: build new Zaps from scratch by combining MCP data lookups with editor UI construction
- Zap migration: move a Zap's configuration from one app/account to another (e.g., swap calendar targets)
- Zap debugging: use MCP to test data flow, then use Chrome to fix editor configuration issues
- Storage-backed workflows: set up Storage by Zapier steps via the editor, then backfill values via MCP

## Handling Zapier Editor UI Patterns

The Zapier editor is a React-based web app. Include guidance for handling:
- **Loading states**: Zapier's editor has async loading — wait for elements to be interactive before clicking
- **Dropdowns and search fields**: Many step configurations use searchable dropdowns — type to filter, then select
- **Modal dialogs**: Step configuration often opens in modals/panels — identify and interact within these contexts
- **Save/publish states**: After editing, the Zap may need to be explicitly saved or published
- **CAPTCHAs and auth prompts**: If encountered, STOP and ask me to handle manually, then resume

## Error Handling

- If a Zapier MCP action fails, report the error and suggest whether it's a permissions issue, a wrong ID, or an API limitation
- If a Chrome automation step fails (element not found, page didn't load), take a screenshot, report what happened, and ask me how to proceed
- Never silently skip a failed step — always surface errors

## Skill Structure

Follow the conventions from skill-system-mastery. The Skill should include at minimum:
- `SKILL.md` — the main skill file with all instructions, patterns, and workflows
- Any supporting reference files if needed for complex editor interaction patterns

## Test Cases to Consider

After building the Skill, we should test with:
1. **Account verification**: Run the pre-flight check against my live Zapier session
2. **Navigation**: Navigate to an existing Zap and read its step configuration
3. **Simple edit**: Change a single field value in a Zap step (like swapping a calendar target)
4. **MCP + Chrome combo**: Use MCP to look up storage values, then use Chrome to update a Zap step that references those values

Go ahead and read the skill-system-mastery SKILL.md, read the Chrome integration docs at the URL above, review what Zapier MCP tools you have available, and then build this Skill. Start with the SKILL.md draft and show it to me before running any tests.
