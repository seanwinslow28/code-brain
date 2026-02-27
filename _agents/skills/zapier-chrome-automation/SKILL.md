---
name: zapier-chrome-automation
description: Zapier workflow automation combining MCP API actions with browser_subagent UI editing. Use when building, editing, debugging, or maintaining Zapier Zaps — especially when you need to change step configurations, swap apps/accounts, update field mappings, add/remove steps, or do anything in the Zapier web editor that MCP cannot do alone.
---

# Zapier Chrome Automation

## Purpose

Coordinate two tools into one workflow for building, editing, and maintaining Zapier Zaps end-to-end: Zapier MCP for API-level data actions, and the `browser_subagent` tool for UI-level Zap editor manipulation. This bridges the gap where MCP can query data and execute actions but cannot edit Zap step configurations.

## When to Use

- Building a new Zap from scratch (combining MCP data lookups with browser editor construction)
- Editing an existing Zap's step configuration (changing app, account, fields, calendar targets, etc.)
- Debugging a failing Zap (MCP to test data flow, browser to inspect/fix editor settings)
- Swapping a Zap's connected accounts or app targets (migration)
- Setting up Storage by Zapier steps via the editor, then backfilling values via MCP
- Turning Zaps on/off, testing individual steps, or rearranging step order
- Any task that says "edit this Zap", "fix this Zap", "change the Zap step", or "update Zapier workflow"

## Examples

**Example 1: Fix a misconfigured Zap step**
```
User: "My Zap is searching the wrong calendar. Change Step 2 to use NL-Pod-Research Sponsorships instead."
Agent: [Uses zapier-chrome-automation]
1. Runs pre-flight account verification via browser_subagent
2. Navigates to the Zap in Zapier editor
3. Opens Step 2 configuration
4. Changes the calendar dropdown to "NL-Pod-Research Sponsorships"
5. Saves and tests the step
```

**Example 2: Build a new Zap with Storage backfill**
```
User: "Create a Zap that syncs calendar events and stores ID mappings in Storage by Zapier."
Agent: [Uses zapier-chrome-automation]
1. Uses MCP to query source calendar events and identify IDs
2. Uses browser_subagent to create a new Zap in the editor, adding trigger + action steps
3. Configures each step via the editor UI (dropdowns, field mappings)
4. Uses MCP to backfill Storage with existing ID mappings
5. Tests end-to-end via browser + MCP
```

**Example 3: Debug a Zap that stopped working**
```
User: "My delete-on-cancel Zap isn't firing. Help me figure out why."
Agent: [Uses zapier-chrome-automation]
1. Uses MCP (find_zap) to check Zap status (on/off, last run)
2. Uses MCP (find_events, get_value) to verify data flow and storage state
3. Uses browser_subagent to open the Zap editor and inspect step configurations
4. Identifies misconfigured fields and fixes them via browser
5. Tests the corrected Zap
```

## Tool Inventory

### Category 1: API Actions (Zapier MCP)

These run without a browser. Use for data queries, storage CRUD, and programmatic actions.

> NOTE: Zapier MCP tools require an external MCP server configured in your environment. If Zapier MCP is not available, fall back to browser-only workflows using `browser_subagent`.

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

### Category 2: Zap Editor UI Actions (browser_subagent)

These use the `browser_subagent` tool to interact with the Zapier web editor. Each interaction should be structured as a clear task description.

**Key capabilities:**
- Navigate to a specific Zap by name or URL
- Open a specific step in the Zap editor
- Change a step's app, trigger/action type, or connected account
- Update field values within a step (calendar target, search term, etc.)
- Add, remove, or reorder steps
- Toggle "Successful if no search results found" and similar options
- Turn a Zap on/off
- Test individual steps within the editor
- Save/publish changes

**Writing effective browser_subagent tasks:**

When delegating Zapier editor work to `browser_subagent`, write highly specific task descriptions:

```
Task: "Navigate to https://zapier.com/editor/12345. Wait for the editor to load.
Click on Step 2 to open its configuration panel. In the 'Calendar' dropdown,
type 'NL-Pod' to filter, then select 'NL-Pod-Research Sponsorships'.
Verify the selection shows correctly, then return the field value you see."

RecordingName: "edit_zap_step"
```

Always include in your task descriptions:
1. The exact URL to navigate to
2. What to wait for before interacting
3. The specific UI elements to target (by label text, not CSS selectors)
4. Verification steps (read back a field value, check a toggle state)
5. What information to return

See `references/zapier-editor-selectors.md` for detailed UI patterns and navigation paths.

### Category 3: Coordinated Workflows (MCP + browser_subagent)

- **Full Zap creation**: MCP for data lookups, browser_subagent for editor construction
- **Zap migration**: browser_subagent to swap accounts/targets, MCP to verify data integrity
- **Zap debugging**: MCP to test data flow, browser_subagent to fix editor config
- **Storage-backed workflows**: browser_subagent to add Storage steps, MCP to backfill values

## Pre-flight Account Verification

<HARD-GATE>
Before ANY browser_subagent Zapier editor interaction, you MUST verify the logged-in account.
This is non-negotiable. Never skip this step even if "we just checked" or "it's quick."
</HARD-GATE>

### Steps

1. Call `browser_subagent` with the following task:
   ```
   Task: "Navigate to https://zapier.com/app/zaps. Wait for the page to load fully.
   Look for the logged-in account name or email in the navigation bar, header,
   or profile menu. Return the exact account email or name you see."
   RecordingName: "verify_zapier_account"
   ```
2. Check the returned account against the expected account (e.g., **swinslow@theblock**)
3. If the account does NOT match, **STOP immediately** and alert the user:
   > "Wrong Zapier account detected. Please ensure the correct browser profile is active and try again."
4. Only proceed after verification passes

### Re-verification Triggers

Re-run account verification if:
- A new `browser_subagent` session was started
- You navigated away from Zapier and came back
- More than 15 minutes have elapsed since last verification

## Zapier Editor UI Patterns

The Zapier editor is a React-based SPA. Follow these patterns for reliable browser automation.

### Loading States

Zapier's editor loads asynchronously. When writing `browser_subagent` tasks:
- Include "wait for the page to fully load" in every navigation task
- Instruct the subagent to wait for loading spinners to disappear
- If a dropdown says "Loading..." instruct the subagent to wait for options to populate

### Dropdowns and Search Fields

Most step configurations use searchable dropdowns. Instruct the subagent to:
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

After editing steps, instruct the subagent to:
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

### Modal Dialogs and Panels

Step configuration often opens in slide-out panels:
- Instruct the subagent to interact within the panel context, not the background
- If a confirmation modal appears, read it before clicking through
- For account selection modals, verify you're picking the correct account

## Error Handling

### MCP Action Failures

If a Zapier MCP tool returns an error:
1. Report the exact error message
2. Diagnose: Is it a permissions issue? Wrong ID? API rate limit? Connection mismatch?
3. Suggest specific remediation steps
4. Never silently skip a failed action

### Browser Automation Failures

If a `browser_subagent` interaction fails (element not found, page didn't load, unexpected state):
1. Read the subagent's returned report for details
2. Report what happened: what was expected vs. what was observed
3. Retry with a more specific task description (include wait conditions, alternative selectors)
4. If retry fails, use `notify_user` to ask the user how to proceed
5. Never silently skip a failed step

### CAPTCHAs and Auth Prompts

If a CAPTCHA, re-authentication prompt, or 2FA challenge appears:
1. **STOP immediately** — do not attempt to solve it
2. Use `notify_user` to alert: "A CAPTCHA/auth prompt appeared in the Zapier editor. Please handle it manually in your browser, then tell me to continue."
3. Resume only after the user confirms

### Connection/Namespace Mismatches

Storage by Zapier connections are scoped to namespaces. If data written via MCP is not visible in a Zap:
1. Verify the MCP Storage connection matches the Zap's Storage connection
2. Use `get_configuration_url` to find the MCP connection details
3. Via `browser_subagent`, check what Storage account the Zap step is using
4. If mismatched, either change the Zap's account or re-backfill to the correct namespace

## Workflow: Fix a Misconfigured Zap

1. **Identify** the Zap via MCP: `find_zap` to get name, status, ID, URL
2. **Pre-flight**: Run account verification via `browser_subagent`
3. **Navigate**: Use `browser_subagent` to open the Zap URL
4. **Inspect**: Use `browser_subagent` to open each step, read field values
5. **Diagnose**: Compare actual configuration against intended specification
6. **Fix**: Use `browser_subagent` to update misconfigured fields (dropdowns, toggles, field mappings)
7. **Test**: Use `browser_subagent` to run step tests in the editor
8. **Verify**: Use MCP to run a data-level test (e.g., query events, check storage)
9. **Publish**: Use `browser_subagent` to save changes and turn the Zap back on if it was disabled

## Workflow: Build a New Zap

1. **Plan**: Identify trigger app, action apps, and data flow
2. **Pre-flight**: Run account verification
3. **Navigate**: Use `browser_subagent` to go to `https://zapier.com/app/editor` to start a new Zap
4. **Configure trigger**: Select app, trigger event, account, and test
5. **Add action steps**: For each step — select app, action, account, map fields
6. **Add filters**: If needed, add Filter by Zapier steps between actions
7. **Add storage**: If the workflow needs ID mapping, add Storage by Zapier steps
8. **Test**: Test each step individually in the editor
9. **Backfill**: Use MCP to pre-populate Storage with existing data
10. **Publish**: Turn the Zap on

## Success Criteria

- [ ] Pre-flight account verification runs before every browser interaction
- [ ] MCP is used for data queries and storage operations (not browser)
- [ ] browser_subagent is used for editor UI manipulation (not MCP)
- [ ] Errors from either tool surface immediately with details
- [ ] CAPTCHAs and auth prompts trigger an immediate stop-and-ask via notify_user
- [ ] Storage connection namespaces are verified before read/write operations
- [ ] Each editor change is verified after making it (read-back confirmation)
- [ ] browser_subagent task descriptions are specific, include wait conditions, and request verification

## Copy/Paste Ready

```
"Edit my Zap to use a different calendar"
"Fix the Zapier workflow that's not triggering"
"Build a new Zap that syncs events between calendars"
"Change the Storage account in my Zap to match MCP"
"Debug why my Zap's delete step isn't working"
```
