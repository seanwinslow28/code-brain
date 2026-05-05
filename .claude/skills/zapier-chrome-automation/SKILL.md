---
name: zapier-chrome-automation
description: Zapier workflow automation combining MCP API actions with Chrome browser UI editing. Use when building, editing, debugging, or maintaining Zapier Zaps — especially when you need to change step configurations, swap apps/accounts, update field mappings, add/remove steps, or do anything in the Zapier web editor that MCP cannot do alone.
---

# Zapier Chrome Automation

## Purpose

Coordinate two tools into one workflow for building, editing, and maintaining Zapier Zaps end-to-end: Zapier MCP for API-level data actions, and Chrome browser integration for UI-level Zap editor manipulation. This bridges the gap where MCP can query data and execute actions but cannot edit Zap step configurations.

## When to Use

- Building a new Zap from scratch (combining MCP data lookups with Chrome editor construction)
- Editing an existing Zap's step configuration (changing app, account, fields, calendar targets, etc.)
- Debugging a failing Zap (MCP to test data flow, Chrome to inspect/fix editor settings)
- Swapping a Zap's connected accounts or app targets (migration)
- Setting up Storage by Zapier steps via the editor, then backfilling values via MCP
- Turning Zaps on/off, testing individual steps, or rearranging step order
- Any task that says "edit this Zap", "fix this Zap", "change the Zap step", or "update Zapier workflow"

## Examples

**Example 1: Fix a misconfigured Zap step**
```
User: "My Zap is searching the wrong calendar. Change Step 2 to use NL-Pod-Research Sponsorships instead."
Claude: [Uses zapier-chrome-automation]
1. Runs pre-flight account verification via Chrome
2. Navigates to the Zap in Zapier editor
3. Opens Step 2 configuration
4. Changes the calendar dropdown to "NL-Pod-Research Sponsorships"
5. Saves and tests the step
```

**Example 2: Build a new Zap with Storage backfill**
```
User: "Create a Zap that syncs calendar events and stores ID mappings in Storage by Zapier."
Claude: [Uses zapier-chrome-automation]
1. Uses MCP to query source calendar events and identify IDs
2. Uses Chrome to create a new Zap in the editor, adding trigger + action steps
3. Configures each step via the editor UI (dropdowns, field mappings)
4. Uses MCP to backfill Storage with existing ID mappings
5. Tests end-to-end via Chrome + MCP
```

**Example 3: Debug a Zap that stopped working**
```
User: "My delete-on-cancel Zap isn't firing. Help me figure out why."
Claude: [Uses zapier-chrome-automation]
1. Uses MCP (find_zap) to check Zap status (on/off, last run)
2. Uses MCP (find_events, get_value) to verify data flow and storage state
3. Uses Chrome to open the Zap editor and inspect step configurations
4. Identifies misconfigured fields and fixes them via Chrome
5. Tests the corrected Zap
```

## Tool Inventory

### Category 1: API Actions (Zapier MCP)

These run without a browser. Use for data queries, storage CRUD, and programmatic actions.

| Tool | Purpose |
|------|---------|
| `google_calendar_find_events` | Search events by calendar, term, date range |
| `google_calendar_retrieve_event_by_id` | Get specific event by ID |
| `google_calendar_create_detailed_event` | Create events with full field control |
| `google_calendar_delete_event` | Delete events by ID |
| `google_calendar_update_event` | Modify existing events |
| `storage_by_zapier_get_value` | Read a key from Storage |
| `storage_by_zapier_set_value` | Write a key-value pair to Storage |
| `storage_by_zapier_get_all_values` | Dump all stored key-value pairs |
| `storage_by_zapier_remove_value` | Delete a key from Storage |
| `storage_by_zapier_set_multiple_values` | Batch write multiple key-value pairs |
| `zapier_manager_find_zap` | Look up Zap by name (status, ID, last run) |
| `zapier_manager_find_app` | Look up app availability on Zapier |
| `get_configuration_url` | Get MCP server config URL |
| `code_by_zapier_run_javascript` | Execute JS code in Zapier's runtime |
| `code_by_zapier_run_python` | Execute Python code in Zapier's runtime |
| `webhooks_by_zapier_custom_request` | Raw HTTP requests |

### Category 2: Zap Editor UI Actions (Chrome)

These require Chrome integration (`claude --chrome` or `/chrome`). Use for anything that touches the Zapier web editor.

- Navigate to a specific Zap by name or URL
- Open a specific step in the Zap editor
- Change a step's app, trigger/action type, or connected account
- Update field values within a step (calendar target, search term, etc.)
- Add, remove, or reorder steps
- Toggle "Successful if no search results found" and similar options
- Turn a Zap on/off
- Test individual steps within the editor
- Save/publish changes

### Category 3: Coordinated Workflows (MCP + Chrome)

- **Full Zap creation**: MCP for data lookups, Chrome for editor construction
- **Zap migration**: Chrome to swap accounts/targets, MCP to verify data integrity
- **Zap debugging**: MCP to test data flow, Chrome to fix editor config
- **Storage-backed workflows**: Chrome to add Storage steps, MCP to backfill values

## Pre-flight Account Verification

<HARD-GATE>
Before ANY Chrome-based Zapier editor interaction, you MUST verify the logged-in account.
This is non-negotiable. Never skip this step even if "we just checked" or "it's quick."
</HARD-GATE>

### Steps

1. Ensure Chrome is connected (if not, prompt: "Please run `/chrome` or launch with `claude --chrome` and ensure your **your-zapier-account** Chrome profile is the active window.")
2. Navigate to `https://zapier.com/app/zaps`
3. Read the page to identify the logged-in account
4. Verify the account is **your-zapier-account**
5. If the account does NOT match, **STOP immediately** and alert:
   > "Wrong Zapier account detected. Please close other Chrome profiles and ensure only your your-zapier-account profile is open, then re-run `/chrome`."
6. Only proceed after verification passes

### Re-verification Triggers

Re-run account verification if:
- Chrome was reconnected during the session (`/chrome` was run again)
- You navigated away from Zapier and came back
- More than 15 minutes have elapsed since last verification

## Zapier Editor UI Patterns

The Zapier editor is a React-based SPA. Follow these patterns for reliable automation.

### Loading States

Zapier's editor loads asynchronously. After any click or navigation:
- Wait for loading spinners to disappear before interacting
- Look for the step configuration panel to be fully rendered
- If a dropdown says "Loading..." wait for options to populate

### Dropdowns and Search Fields

Most step configurations use searchable dropdowns:
1. Click the dropdown field to open it
2. Type a few characters to filter options (e.g., type "NL-Pod" to find "NL-Pod-Research Sponsorships")
3. Wait for filtered results to appear
4. Click the matching option
5. Verify the selection stuck by reading the field value after clicking

### Toggles and Checkboxes

For boolean options like "Successful if no search results found":
1. Locate the toggle/checkbox by its label text
2. Read its current state before clicking
3. Click to toggle
4. Verify the new state

### Save and Publish

After editing steps:
1. Look for a "Save" or "Publish" button (usually top-right or bottom of panel)
2. If the Zap was previously ON, Zapier may prompt "Do you want to publish changes?"
3. Click through the publish flow
4. Verify the Zap status after saving

### Testing Steps

To test an individual step in the editor:
1. Open the step you want to test
2. Scroll to the bottom of the step configuration panel
3. Click "Test step" or "Test & Review"
4. Wait for the test to complete (may take several seconds)
5. Read the test output to verify correct behavior
6. Take a screenshot of the result for verification

### Modal Dialogs and Panels

Step configuration often opens in slide-out panels:
- Interact within the panel context, not the background
- If a confirmation modal appears, read it before clicking through
- For account selection modals, verify you're picking the correct account

## Error Handling

### MCP Action Failures

If a Zapier MCP tool returns an error:
1. Report the exact error message
2. Diagnose: Is it a permissions issue? Wrong ID? API rate limit? Connection mismatch?
3. Suggest specific remediation steps
4. Never silently skip a failed action

### Chrome Automation Failures

If a browser interaction fails (element not found, page didn't load, unexpected state):
1. Take a screenshot immediately
2. Report what happened: what was expected vs. what was observed
3. Check if the page is in a loading state and retry once after waiting
4. If retry fails, ask the user how to proceed
5. Never silently skip a failed step

### CAPTCHAs and Auth Prompts

If a CAPTCHA, re-authentication prompt, or 2FA challenge appears:
1. **STOP immediately** — do not attempt to solve it
2. Take a screenshot
3. Alert: "A CAPTCHA/auth prompt appeared. Please handle it manually in your browser, then tell me to continue."
4. Resume only after the user confirms

### Connection/Namespace Mismatches

Storage by Zapier connections are scoped to namespaces. If data written via MCP is not visible in a Zap:
1. Verify the MCP Storage connection matches the Zap's Storage connection
2. Use `get_configuration_url` to find the MCP connection details
3. In Chrome, check what Storage account the Zap step is using
4. If mismatched, either change the Zap's account or re-backfill to the correct namespace

## Workflow: Fix a Misconfigured Zap

1. **Identify** the Zap via MCP: `find_zap` to get name, status, ID, URL
2. **Pre-flight**: Run account verification via Chrome
3. **Navigate**: Open the Zap URL in Chrome
4. **Inspect**: Open each step, take screenshots, read field values
5. **Diagnose**: Compare actual configuration against intended specification
6. **Fix**: Update misconfigured fields via Chrome (dropdowns, toggles, field mappings)
7. **Test**: Run step tests in the editor
8. **Verify**: Use MCP to run a data-level test (e.g., query events, check storage)
9. **Publish**: Save changes and turn the Zap back on if it was disabled

## Workflow: Build a New Zap

1. **Plan**: Identify trigger app, action apps, and data flow
2. **Pre-flight**: Run account verification
3. **Navigate**: Go to `https://zapier.com/app/editor` to start a new Zap
4. **Configure trigger**: Select app, trigger event, account, and test
5. **Add action steps**: For each step — select app, action, account, map fields
6. **Add filters**: If needed, add Filter by Zapier steps between actions
7. **Add storage**: If the workflow needs ID mapping, add Storage by Zapier steps
8. **Test**: Test each step individually in the editor
9. **Backfill**: Use MCP to pre-populate Storage with existing data
10. **Publish**: Turn the Zap on

## Success Criteria

- [ ] Pre-flight account verification runs before every Chrome interaction
- [ ] MCP is used for data queries and storage operations (not Chrome)
- [ ] Chrome is used for editor UI manipulation (not MCP)
- [ ] Errors from either tool surface immediately with screenshots/details
- [ ] CAPTCHAs and auth prompts trigger an immediate stop-and-ask
- [ ] Storage connection namespaces are verified before read/write operations
- [ ] Each editor change is verified after making it (read-back confirmation)

## Copy/Paste Ready

```
"Edit my Zap to use a different calendar"
"Fix the Zapier workflow that's not triggering"
"Build a new Zap that syncs events between calendars"
"Change the Storage account in my Zap to match MCP"
"Debug why my Zap's delete step isn't working"
```
