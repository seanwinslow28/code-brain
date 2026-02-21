---
name: safe-ops
description: Ensures safe operations by checking for destructive actions and prompting for confirmation
---

# Safe Operations Skill

## When to Use

Use this skill when:
- Performing potentially destructive operations (deletes, overwrites)
- Working with production data or critical files
- Making bulk changes across multiple files
- Executing commands that could affect system state

## Examples

**Example 1: Safe file deletion**
```
User: "Delete the old test files"
Claude: [Uses safe-ops skill] I found 15 test files matching that pattern. Before deleting, let me confirm:
- These are test files only (not production code)
- They're not referenced elsewhere
- You have a backup if needed

Should I proceed with deletion?
```

**Example 2: Bulk refactoring**
```
User: "Rename all instances of 'oldName' to 'newName'"
Claude: [Uses safe-ops skill] This will affect 47 files across the codebase. I'll:
1. Show you a preview of changes
2. Check for potential breaking changes
3. Ensure no critical files are modified
4. Ask for confirmation before proceeding
```

## Safety Checks

This skill performs:
- Confirmation prompts for destructive operations
- Impact analysis before bulk changes
- Backup recommendations for critical data
- Validation that operations won't break the system
- Checks for production vs development environments

## Copy/Paste Ready

To use this skill:
- "Use safe-ops when deleting these files"
- "Safely refactor this code"
- "Check if this operation is safe"
