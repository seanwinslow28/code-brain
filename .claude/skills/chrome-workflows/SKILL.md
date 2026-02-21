---
name: chrome-workflows
description: Chrome integration and browser-in-the-loop development for Claude Code. Enables visual build-verify loops with screenshots, native Chrome browser automation via --chrome flag, Playwright MCP comparison, and UI testing patterns for frontend development.
---

# Chrome Integration and Browser Workflows

## Purpose

Use Claude Code's browser integration to create visual feedback loops for frontend development. Implement the Write-Screenshot-Iterate pattern to self-correct based on rendered output rather than just code syntax. Choose between native Chrome integration and Playwright MCP based on the task requirements. Enable visual verification, Figma comparison, and authenticated session debugging.

## When to Use

- Building or refining frontend components that need visual verification
- Comparing rendered output against a design mock or Figma export
- Debugging UI issues that only appear in the browser (console errors, layout bugs)
- Testing pages behind authentication (SSO, internal tools)
- Any time you mention "browser testing", "screenshot", "visual verification", "Chrome", or "UI testing"

## Examples

**Example 1: Visual build-verify loop**
```
User: "Build this card component to match this design [paste image]"
Claude: [Uses chrome-workflows]
Implements the card component. Opens localhost:3000 in Chrome. Takes a
screenshot. Compares against the provided design. Lists visual discrepancies
(padding, color, alignment). Fixes CSS. Repeats until match.
```

**Example 2: Authenticated debugging**
```
User: "Debug this admin panel page — I'm already logged in"
Claude: [Uses chrome-workflows]
Uses native Chrome integration (/chrome) to access the user's authenticated
browser session. Navigates the admin panel without needing credential injection.
Captures console errors and inspects the DOM.
```

## Setup and Activation

**CLI flag:** Start Claude with browser support:
```bash
claude --chrome
```

**Slash command:** Toggle during an active session:
```
/chrome
```

**Quick alias:** Set up a short alias for frequent use:
```bash
alias ch='claude --chrome'
```

**Requirements:** Requires an active Claude Pro, Team, or Enterprise plan. Uses the "Claude in Chrome" extension as a bridge between the terminal agent and your browser.

## The Write-Screenshot-Iterate Pattern

The core visual verification loop for frontend work:

1. **Provide the target:** Supply a visual mock (Figma export, screenshot) or detailed description
2. **Implement:** Claude writes the initial code (HTML/CSS/React)
3. **Verify:** Claude opens the dev server in Chrome, takes a screenshot, and analyzes the rendered output
4. **Iterate:** Claude compares its screenshot against your original mock, lists specific visual discrepancies, and applies fixes automatically

**Prompt template:**
```
[Paste image of design] Implement this card component.
Take a screenshot of the result, compare it to the original image I provided,
list the differences (padding, colors, alignment), and fix them until they match.
```

## Native Chrome vs Playwright MCP

Choose the right browser tool for the task:

| Feature | Native Chrome (/chrome) | Playwright MCP |
| :--- | :--- | :--- |
| Mechanism | Uses your local Chrome profile via extension | Runs a headless/controlled browser via MCP |
| Interaction | Visual: clicks using coordinates, takes screenshots | Structural: uses accessibility tree and DOM |
| Authentication | Uses your existing logged-in sessions | Requires fresh login or credential injection |
| Best for | Visual verification, pixel CSS work, authenticated tools | Functional testing, scraping, console log capture |
| Limitation | Slower, occasional coordinate precision issues | Cannot access user-authenticated states easily |

**Default recommendation:** Use Playwright MCP for speed and stability. Use native Chrome (/chrome) specifically when you need your existing logged-in browser state or strict visual verification.

## UI Testing Patterns

### Screenshot Evaluation

Instead of relying solely on unit tests (which pass even if the UI looks broken), use screenshots as the source of truth:

```
Take a screenshot of the homepage and verify the navbar is sticky when scrolling.
```

### Console Log Debugging

For runtime errors that do not show up in terminal logs, capture the browser console:

```
Open the page in the browser and capture any console errors. Feed them back
for debugging.
```

### Figma Comparison

Export Figma frames as images and use the visual loop:

```
Here is the Figma export [image]. Render the code, snapshot it,
and calculate the visual delta. List specific differences.
```

## Hybrid Verification Pattern

Combine the Builder-Validator approach with browser tools:

1. **Builder agent:** Writes the frontend code
2. **Validator agent (with browser tools):** Takes a screenshot, compares to specs, and rejects if the visual output does not match
3. **Builder agent:** Receives the rejection list and fixes the issues

This prevents the builder from marking work as "done" when the UI is visually broken.

## Logged-In Workflow

When debugging a page behind complex SSO (Single Sign-On):

1. Log in manually to the site in your Chrome browser
2. Start Claude with `/chrome`
3. Claude navigates the authenticated session to debug specific user-facing issues
4. No need to pass credentials to Claude or set up headless auth flows

This is the primary advantage of native Chrome over Playwright — leveraging existing authentication state.

## Success Criteria

- [ ] Visual verification loop catches CSS/layout issues before manual review
- [ ] Correct browser tool is chosen (native for auth/visual, Playwright for functional)
- [ ] Screenshots are compared against design mocks with specific discrepancy lists
- [ ] Console errors are captured for runtime debugging
- [ ] Authenticated pages are accessible via native Chrome integration

## Copy/Paste Ready

```
"Use Chrome to verify this component matches the design"
"Take a screenshot and compare it to the Figma mock"
"Debug this page using my logged-in browser session"
"Set up visual verification for this frontend build"
"Capture browser console errors for this page"
```
