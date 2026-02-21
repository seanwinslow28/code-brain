# Claude Code Prompt: Configure Obsidian Plugins via JSON

## Context

My Obsidian vault is at `vault/` in this project. I have 6 community plugins already installed:
- obsidian-git
- templater-obsidian
- dataview
- obsidian-linter
- obsidian-local-rest-api
- remotely-save

Obsidian stores all plugin settings as JSON files in `vault/.obsidian/plugins/<plugin-name>/data.json` and core plugin settings in `vault/.obsidian/` root. I need you to configure everything by editing these JSON files directly — I don't want to navigate the Obsidian UI.

**Important:** After you make all changes, I will need to restart Obsidian once for it to pick up the new configs. Tell me when you're done so I can restart.

---

## Step 1: Read Current Configs

Before changing anything, read and show me the current contents of:
1. `vault/.obsidian/app.json`
2. `vault/.obsidian/core-plugins.json` (check if daily-notes is enabled)
3. `vault/.obsidian/daily-notes.json` (may not exist yet)
4. `vault/.obsidian/plugins/templater-obsidian/data.json`
5. `vault/.obsidian/plugins/dataview/data.json`
6. `vault/.obsidian/plugins/obsidian-linter/data.json`
7. `vault/.obsidian/plugins/obsidian-git/data.json`
8. `vault/.obsidian/community-plugins.json`

Show me what exists so we can see the baseline.

---

## Step 2: Configure Core Settings (`app.json`)

Update `vault/.obsidian/app.json` to set:
- `"newFileLocation": "folder"` (create new notes in a specific folder)
- `"newFileFolderPath": "00_inbox"` (default location for new notes)
- `"attachmentFolderPath": "50_sources/assets"` (where attachments go)
- `"strictLineBreaks": true`

Preserve any existing keys — only add/update these.

---

## Step 3: Enable & Configure Daily Notes Core Plugin

Check `vault/.obsidian/core-plugins.json` — ensure `"daily-notes"` is in the enabled array.

Create or update `vault/.obsidian/daily-notes.json`:
```json
{
  "folder": "10_timeline/daily",
  "format": "YYYY-MM-DD",
  "template": "90_system/templates/tpl-daily"
}
```

---

## Step 4: Configure Templater

Update `vault/.obsidian/plugins/templater-obsidian/data.json` to include:
- `"templates_folder": "90_system/templates"`
- `"trigger_on_file_creation": true`
- `"folder_templates"` array with these mappings:
  - folder `10_timeline/daily` → template `90_system/templates/tpl-daily.md`
  - folder `10_timeline/weekly` → template `90_system/templates/tpl-weekly.md`
  - folder `20_projects` → template `90_system/templates/tpl-project.md`

Preserve any other existing Templater settings.

---

## Step 5: Configure Dataview

Update `vault/.obsidian/plugins/dataview/data.json` to include:
- `"enableDataviewJs": true`
- `"enableInlineDataview": true`
- `"enableInlineDataviewJs": true`

Preserve any other existing settings.

---

## Step 6: Configure Linter

Update `vault/.obsidian/plugins/obsidian-linter/data.json` to include:
- Enable lint on save (look for the appropriate key — it may be `"lintOnSave": true` or nested under a different structure)
- Set YAML-related rules:
  - Enable the "YAML Title" rule
  - Enable the "YAML Timestamp" rule with `date modified: true`
- Set ignored folders to include: `70_apple-notes`, `60_archive`

**Note:** The Linter plugin's data.json structure can be complex. Read the current file first, understand the schema, then make targeted changes. If the structure is unfamiliar, show me what you see before editing.

---

## Step 7: Configure Obsidian Git

Update `vault/.obsidian/plugins/obsidian-git/data.json` to include:
- `"autoPullInterval": 5` (pull every 5 minutes)
- `"autoSaveInterval": 10` (auto commit every 10 minutes)
- `"commitMessage": "vault: auto-commit {{date}}"` 
- `"autoPullOnBoot": true`
- `"pushOnCommit": true` (auto push after each auto-commit)

Preserve any other existing settings.

---

## Step 8: Verify .gitignore

Check that `vault/.gitignore` includes at minimum:
```
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
.DS_Store
*.tmp
50_sources/finance/*.csv
```

If it doesn't exist or is missing entries, create/update it.

---

## Step 9: Summary Report

After all changes, give me:
1. A list of every file you modified and what changed
2. Any settings you couldn't configure (and why)
3. Confirmation that I just need to restart Obsidian to pick everything up
4. Any warnings about settings that might need manual verification after restart
