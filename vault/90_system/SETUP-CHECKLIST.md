---
type: reference
domain:
  - vault
status: active
ai-context: Manual setup steps after Claude Code scaffolds the vault
created: 2026-02-20
---
# Vault Setup Checklist

Everything below must be done manually in the Obsidian app after the vault structure is scaffolded by Claude Code. Items marked with [x] were configured via JSON by Claude Code.

## 1. Open the Vault

- [x] Open Obsidian
- [x] Choose "Open folder as vault" and select `vault/` from this project
- [x] Obsidian will detect the existing `.obsidian/` config and load plugins

## 2. Configure Templater Plugin

The vault uses [Templater](https://github.com/SilentVoid13/Templater) for dynamic templates.

- [x] Set **Template folder location** to `90_system/templates` *(configured via JSON)*
- [x] Enable **Trigger Templater on new file creation** *(configured via JSON)*
- [x] Set folder templates *(configured via JSON)*:
  - `10_timeline/daily` -> `90_system/templates/tpl-daily.md`
  - `10_timeline/weekly` -> `90_system/templates/tpl-weekly.md`
  - `20_projects` -> `90_system/templates/tpl-project.md`

## 3. Configure Daily Notes Core Plugin

- [x] Daily Notes core plugin enabled *(already in core-plugins.json)*
- [x] Set **New file location** to `10_timeline/daily` *(configured via JSON)*
- [x] Set **Date format** to `YYYY-MM-DD` *(configured via JSON)*
- [x] Set **Template file location** to `90_system/templates/tpl-daily` *(configured via JSON)*

## 4. Configure Dataview Plugin

[Dataview](https://github.com/blacksmithgu/obsidian-dataview) powers the dashboard and MOC queries.

- [x] Enable **JavaScript queries** *(already enabled in JSON)*
- [x] Enable **Inline queries** *(already enabled in JSON)*
- [x] Enable **Inline JavaScript queries** *(already enabled in JSON)*
- [x] **VERIFY:** Open Home.md and confirm the Active Projects table renders

## 5. Set Home as Default Note

- [x] `openBehavior` set to `file:Home` in app.json *(configured via JSON)*
- [x] **VERIFY:** Restart Obsidian and confirm Home.md opens on launch

## 6. Configure Obsidian Git

[Obsidian Git](https://github.com/Vinzent03/obsidian-git) is already installed.

- [x] Set **Auto pull interval** to 5 min *(configured via JSON)*
- [x] Set **Auto commit interval** to 10 min *(configured via JSON)*
- [x] Set **Commit message** to `vault: auto-commit {{date}}` *(configured via JSON)*
- [x] Set **Auto pull on boot** to true *(configured via JSON)*
- [x] `.gitignore` excludes sensitive files *(already configured)*
- [ ] **NOTE:** Push-on-commit behavior uses shared interval (`differentIntervalCommitAndPush: false`). If you want separate push timing, adjust in Settings > Obsidian Git

## 7. Configure Linter Plugin

[Obsidian Linter](https://github.com/platers/obsidian-linter) is already installed.

- [x] Enable **Lint on save** *(configured via JSON)*
- [x] Enable **YAML Title** rule *(already enabled in JSON)*
- [x] Enable **YAML Timestamp** rule with `created`/`updated` keys, `YYYY-MM-DD` format *(configured via JSON)*
- [x] Set ignored folders: `70_apple-notes`, `60_archive` *(configured via JSON)*

## 8. MCP Server Setup

**Decision: Option A selected** (bitbonsai/mcp-obsidian)

- [x] Install the MCP server *(configured via `claude mcp add` to `.mcp.json`)*:
  ```bash
  claude mcp add obsidian-vault --scope project -- npx @mauricio.wolff/mcp-obsidian@latest /path/to/vault
  ```
- [x] Pointed at the `vault/` directory *(absolute path in .mcp.json)*
- [ ] Verify it connects by starting a new Claude Code session and running a test query
- **Link:** https://github.com/bitbonsai/mcp-obsidian
- **Package:** `@mauricio.wolff/mcp-obsidian` (not the outdated `@anthropic-ai/create-mcp`)

## 9. Optional: Remotely Save Plugin

[Remotely Save](https://github.com/remotely-save/remotely-save) is already installed for cross-device sync.

- [ ] Configure your sync provider (S3, Dropbox, OneDrive, WebDAV)
- [ ] Note: If using Obsidian Git for this repo, Remotely Save may conflict — choose one sync method

## 10. Triage Apple Notes

The `70_apple-notes/` folder contains 1,462 imported notes. Triage over time:

- [ ] Browse `70_apple-notes/iCloud/Notes/` to identify valuable notes
- [ ] Use the `process-inbox` skill to batch-classify notes (move batches to `00_inbox/` first)
- [ ] Move keepers to `40_knowledge/` or `20_projects/`
- [ ] Archive the rest in `60_archive/`

## 11. Verify Everything Works

- [ ] **Restart Obsidian** to pick up all JSON config changes
- [ ] Open Home.md — should show Active Projects table (6 projects)
- [ ] Click a domain MOC (e.g., [[moc-creative-studio]]) — Dataview queries should render
- [ ] Create a new daily note via hotkey — should use tpl-daily.md template
- [ ] Run Claude Code and say "Start my day" — should use daily-driver skill with new paths
- [ ] Stop Claude Code session — daily-note-appender hook should write to `10_timeline/daily/`
