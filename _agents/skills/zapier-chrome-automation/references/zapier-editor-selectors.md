# Zapier Editor UI Reference

Read this file when performing browser automation on the Zapier Zap editor for guidance on common UI patterns, navigation paths, and interaction strategies.

## Key URLs

| Destination | URL Pattern |
|-------------|-------------|
| All Zaps | `https://zapier.com/app/zaps` |
| Specific Zap editor | `https://zapier.com/editor/{zap_id}` |
| New Zap | `https://zapier.com/app/editor` |
| Zap history | `https://zapier.com/app/history?zap={zap_id}` |
| MCP config | Use `get_configuration_url` tool |

## Page Structure

The Zapier editor is a React SPA with these main regions:

1. **Top bar**: Zap name, on/off toggle, publish button
2. **Step list** (left/center): Vertical list of steps (trigger, actions, filters)
3. **Step config panel** (right): Opens when a step is selected — contains app selector, account picker, field mappings, test button
4. **Step test output**: Appears at the bottom of the config panel after testing

## Writing browser_subagent Tasks for Zapier

When delegating Zapier editor work to `browser_subagent`, structure your tasks around these UI regions. Always reference elements by their **visible label text**, not by CSS selectors or internal IDs.

**Template for a Zapier editor task:**
```
Task: "Navigate to [URL]. Wait for the editor to load fully (step list visible).
[Specific action: click step, change dropdown, toggle option, etc.]
After making the change, verify by reading back the field value.
Return: [what information to report back]."

RecordingName: "[descriptive_name]"
```

## Common Interaction Patterns

### Opening a Step for Editing

1. Click on the step card in the step list
2. Wait for the config panel to slide open on the right
3. The panel has tabs: "App & Event", "Account", "Configure", "Test"

### Changing a Step's App or Action

1. Open the step
2. Click the "App & Event" tab
3. Click the app name to change it — opens a searchable app picker
4. Type to filter, click the desired app
5. Select the trigger/action event from the dropdown
6. Confirm or re-select the account

### Changing the Connected Account

1. Open the step
2. Click the "Account" tab (or look for the account dropdown within "Configure")
3. Click the current account name
4. Select a different account from the dropdown
5. If the account you need isn't listed, click "Connect a new account" and follow OAuth flow (may require manual intervention — use `notify_user` to alert)

### Updating Field Values (e.g., Calendar, Search Term)

1. Open the step, go to the "Configure" tab
2. Find the field by its label (e.g., "Calendar", "Search Term", "Key")
3. If it's a dropdown: click to open, type to filter, click the matching option
4. If it's a text input: click, clear existing value (Cmd+A, Delete), type the new value
5. For mapped/dynamic values: click the field, then click the "+" or mapping icon to insert a reference to a previous step's output

### Mapping a Value from a Previous Step

When a field needs to reference output from an earlier step (e.g., Step 2's Event ID):
1. Click into the target field
2. Look for a "+" icon, "Insert data" button, or mapping panel
3. A panel shows available fields from previous steps, organized by step number
4. Click the field you want to map (e.g., "Step 1 > ID" or "Step 2 > Event ID")
5. The field populates with a mapping token like `{{step2.event_id}}`

### Toggling Boolean Options

Options like "Successful if no search results found" or "Notify attendees":
1. Find the toggle/checkbox by its label
2. Read its current state (on/off, true/false, yes/no)
3. Click to toggle
4. Verify the new state visually

### Adding a New Step

1. Click the "+" button between existing steps (or at the end of the step list)
2. A step type picker appears: Action, Filter, Delay, etc.
3. Select the step type
4. Search for and select the app
5. Configure as above

### Removing a Step

1. Hover over the step card
2. Click the "..." menu (three dots) on the step
3. Select "Delete" or "Remove step"
4. Confirm the deletion in the dialog

### Testing a Step

1. Open the step, scroll to bottom
2. Click "Test step" or "Test & Review"
3. Wait for the spinner to complete (can take 5-30 seconds)
4. Read the output fields
5. Green = success, Red = error

### Publishing/Saving

After making changes:
1. Look for "Publish" button in the top-right area
2. If the Zap was already ON, you may see "Publish changes" or "Update Zap"
3. Click through any confirmation dialogs
4. Verify the Zap status shows "ON" or "Published"

## Turning a Zap On/Off

1. Navigate to the Zap editor or the Zaps list page
2. Find the on/off toggle (usually in the top bar of the editor, or in the Zaps list row)
3. Click to toggle
4. Confirm in any dialog that appears

## Checking Zap Run History

1. Navigate to `https://zapier.com/app/history?zap={zap_id}`
2. Or from the editor, click "Zap Runs" or "History" in the top bar
3. Each run shows: timestamp, status (success/error/filtered), and per-step details
4. Click a run to expand and see input/output for each step

## Tips for Reliable Browser Automation

- **Always wait after clicks**: The editor has many async loading states. Include explicit wait instructions in every `browser_subagent` task.
- **Use text search in dropdowns**: Don't scroll through long lists. Type characters to filter.
- **Request verification**: Always instruct the subagent to read back values after making changes.
- **Read before you write**: Always read the current field value before changing it, to confirm you're editing the right thing.
- **One change at a time**: Make one field change, verify it, then move to the next. Don't batch changes without verification.
- **Set clear return conditions**: Tell the subagent exactly when to return and what to report.
