\# BUILD\_BRIEF.md — Claude Code Superuser Pack (Repo Implementation)

\#\# Purpose  
Ship a \*\*versioned, installable “Superuser Pack” repo\*\* for Claude Code that upgrades day-to-day productivity across three domains in my Research Profile: \*\*PM work, creative projects (React Native \+ Phaser), and life automation\*\*. The pack must be \*\*docs-first\*\*, beginner-friendly, and automation-oriented (hooks \+ templates \+ skills), while keeping safety deterministic where possible.  

\#\# Non-negotiables (Must-Follow Truth Rules)  
These are “ground truth” and must not be contradicted anywhere in this repo (docs, templates, skills, scripts):

1\. \*\*Plan Mode vs Extended Thinking are different\*\*  
   \- \*\*Plan Mode\*\* requires an explicit trigger: \*\*double \`Shift+Tab\`\*\* or \`/plan\`.  
   \- \*\*Extended Thinking\*\* is toggled by \*\*single \`Tab\`\*\*.  
   \- Never document \`Tab\` as entering Plan Mode. \*(Contradiction Resolver: “Plan vs. ‘Think’ Mode Shortcut”)\*

2\. \*\*Use deny-list for subagent tools (recommended in v2.0.31+)\*\*  
   \- Subagents can use \`disallowedTools\` to block only unsafe tools rather than allow-listing everything.  
   \- Prefer deny-list model for maintainability. \*(Contradiction Resolver: “Subagent Tool Restrictions”)\*

3\. \*\*Hooks enforce; subagents judge\*\*  
   \- Use \*\*PreToolUse hooks\*\* for strict, deterministic enforcement (binary allow/deny).  
   \- Use \*\*subagents\*\* for subjective checks (quality, review, audits). \*(Contradiction Resolver: “Hooks vs. Subagents for Policy”)\*

4\. \*\*Hook blocking rule\*\*  
   \- A \*\*PreToolUse\*\* hook can deny an operation by exiting with \*\*code \`2\`\*\*.  
   \- Exit \`0\` \= allow; exit \`1\` \= error. \*(Contradiction Resolver: “Hooks” section \+ hook example)\*    
   \- \*\*TODO:\*\* If we ever rely on a structured JSON “permissionDecision” response, verify exact schema first. \*(Contradiction Resolver: “Hook Permission Schema” unknown)\*

5\. \*\*Chrome automation constraint\*\*  
   \- \`/chrome\` requires \*\*Claude Pro/Max \+ Chrome extension\*\*, and works on \*\*native Windows/macOS\*\*, \*\*not WSL\*\*.  
   \- Treat as an optional capability; do not depend on it for core pack value. \*(Contradiction Resolver: “Chrome Integration Availability”)\*

6\. \*\*Plugin distribution is marketplace-based (GitHub repos), not NPM\*\*  
   \- Install via \`/plugin marketplace add \<user\>/\<repo\>\` with a repo manifest at \*\*\`.claude-plugin/marketplace.json\`\*\*.  
   \- Official curated registry exists (\`claude-plugins-official\`). \*(Contradiction Resolver: “Plugin Installation Mechanism” \+ “Plugin Installation & Marketplace”)\*    
   \- \*\*TODO:\*\* Manifest filename sometimes mentioned as \`plugin.json\`; confirm what Claude Code version accepts. \*(Contradiction Resolver: “Marketplace Manifest” note)\*

7\. \*\*MCP config scoping\*\*  
   \- By default, MCP servers are \*\*project-scoped\*\* and stored in \*\*\`\<project\>/.mcp.json\`\*\*.  
   \- Global MCP configs live in \*\*\`\~/.claude/claude.json\`\*\* when added with \`--scope user\`.  
   \- Use scoping to avoid tool leakage across projects. \*(Contradiction Resolver: “MCP Configuration Scope”)\*

8\. \*\*Settings precedence (highest wins)\*\*  
   \- Enterprise managed settings \> project local overrides \> project settings \> user settings.  
   \- Document this explicitly. \*(Contradiction Resolver: “Config File Locations & Precedence”)\*

9\. \*\*Permission evaluation order\*\*  
   \- Deny → Ask → Allow, first match wins. \*(Contradiction Resolver: “Permission Hierarchy”)\*

10\. \*\*Known plugin limitation\*\*  
   \- Plugin distribution may not auto-install \`.claude/rules/\*\`. Avoid depending on rules auto-import.  
   \- \*\*TODO:\*\* If we include rules, document manual copy step. \*(Contradiction Resolver: “Plugin Rule Auto-Import” limitation)\*

\---

\#\# Repo Deliverable  
A single repo containing:  
1\) \*\*Pack templates\*\* to copy into any project (\`starter\`, \`power\`, \`enterprise\`)    
2\) An \*\*optional Claude plugin\*\* (safe, universal pieces only)    
3\) Scripts \+ validation so the pack is reproducible and hard to break

\#\#\# Exact Repo Folder Structure (create exactly)  
claude-code-superuser-pack/  
├── BUILD\_BRIEF.md  
├── README.md  
├── CHANGELOG.md  
├── LICENSE  
├── scripts/  
│ ├── install-pack.sh  
│ ├── install-pack.ps1  
│ └── validate-pack.py  
├── packs/  
│ ├── starter/  
│ │ ├── CLAUDE.md  
│ │ ├── .gitignore  
│ │ └── .claude/  
│ │ ├── settings.json  
│ │ ├── settings.local.json.example  
│ │ ├── skills/  
│ │ │ ├── team-styleguide/SKILL.md  
│ │ │ ├── commit-checklist/SKILL.md  
│ │ │ └── safe-ops/SKILL.md  
│ │ └── hooks/  
│ │ ├── block-secrets.py  
│ │ └── log-tool-use.sh  
│ ├── power/  
│ │ ├── CLAUDE.md  
│ │ ├── .gitignore  
│ │ └── .claude/  
│ │ ├── settings.json  
│ │ ├── settings.local.json.example  
│ │ ├── skills/  
│ │ │ ├── pm-prd/SKILL.md  
│ │ │ ├── pm-jira/SKILL.md  
│ │ │ ├── pm-stakeholder-update/SKILL.md  
│ │ │ ├── react-native-phaser/SKILL.md  
│ │ │ ├── supabase-python/SKILL.md  
│ │ │ └── life-budget/SKILL.md  
│ │ ├── agents/  
│ │ │ ├── pm-tech-writer.md  
│ │ │ ├── security-reviewer.md  
│ │ │ ├── game-design-advisor.md  
│ │ │ └── data-analyst.md  
│ │ ├── hooks/  
│ │ │ ├── block-secrets.py  
│ │ │ ├── format-on-edit.sh  
│ │ │ ├── run-tests-on-stop.sh  
│ │ │ └── log-tool-use.sh  
│ │ └── templates/  
│ │ ├── prd.md  
│ │ ├── jira\_ticket.md  
│ │ ├── stakeholder\_update.md  
│ │ ├── game\_feature\_spec.md  
│ │ └── finance\_report.md  
│ └── enterprise/  
│ ├── CLAUDE.md  
│ ├── .gitignore  
│ └── .claude/  
│ ├── settings.json  
│ ├── settings.local.json.example  
│ ├── skills/  
│ │ ├── org-security/SKILL.md  
│ │ ├── org-definition-of-done/SKILL.md  
│ │ └── pm-prd/SKILL.md  
│ ├── agents/  
│ │ ├── security-reviewer.md  
│ │ └── compliance-summarizer.md  
│ └── hooks/  
│ ├── block-secrets.py  
│ ├── require-confirm-highrisk.sh  
│ ├── run-tests-on-stop.sh  
│ └── log-tool-use.sh  
├── plugin/  
│ ├── skills/  
│ │ ├── team-styleguide/SKILL.md  
│ │ ├── commit-checklist/SKILL.md  
│ │ └── safe-ops/SKILL.md  
│ ├── agents/  
│ │ └── security-reviewer.md  
│ └── hooks/  
│ ├── block-secrets.py  
│ └── log-tool-use.sh  
└── .claude-plugin/  
└── marketplace.json

\---

\#\# File Creation Notes (what each must accomplish)  
\- \`packs/\*/CLAUDE.md\`: \*\*Pointer Pattern\*\* (index \+ rules) \+ quick “How to use Plan Mode vs Thinking” note.  
\- \`packs/\*/.claude/settings.json\`: baseline permissions \+ hooks registration.  
\- \`settings.local.json.example\`: placeholders for local-only tweaks (never committed).  
\- Skills (\`SKILL.md\`): include YAML frontmatter with \`name\` \+ \`description\`. Keep descriptions tight so Claude auto-loads correctly. Include examples and “when to use”.  
\- Agents (\`\*.md\`): include YAML frontmatter with \`name\`, \`description\`, and \*\*deny-list\*\* \`disallowedTools\` where appropriate (esp. read-only reviewers).  
\- Hooks:  
  \- \`block-secrets.py\`: deny edits/writes to \`.env\`, \`\*\*/secrets/\*\*\`, and other sensitive paths; return exit \*\*2\*\* when blocking.  
  \- \`log-tool-use.sh\`: append tool name \+ target path/command to a local log file (audit trail).  
  \- \`format-on-edit.sh\`: run formatter after edits (prettier/black). Must be non-blocking.  
  \- \`run-tests-on-stop.sh\`: run project tests on Stop; non-blocking in starter, optionally blocking in enterprise (decision documented).  
  \- \`require-confirm-highrisk.sh\` (enterprise): intercept risky Bash patterns and force deny (exit 2\) unless explicit allow is configured.

\*\*TODO (paths/schemas to confirm against Contradiction Resolver unknowns):\*\*  
\- Plugin manifest format: confirm required keys in \`.claude-plugin/marketplace.json\`. \*(Contradiction Resolver: “Marketplace Manifest” note)\*  
\- If any hook relies on undocumented env vars (e.g., \`$CLAUDE\_FILE\_PATH\`), verify in local Claude Code version. \*(Contradiction Resolver: version sensitivity warnings)\*

\---

\#\# Definition of Done (Checklist)  
\- \[ \] Repo tree matches \*\*exactly\*\* the structure above.  
\- \[ \] All \`settings.json\` files are valid JSON and load in Claude Code without warnings.  
\- \[ \] Starter pack works in default-safe mode: Claude prompts for risky ops; hooks block secrets deterministically.  
\- \[ \] \`block-secrets.py\` demonstrably blocks \`.env\` writes/edits (PreToolUse exit code \*\*2\*\*).  
\- \[ \] Permissions logic documented: \*\*Deny → Ask → Allow\*\* and settings precedence (enterprise \> local \> project \> user).  
\- \[ \] Subagents use \*\*deny-list (\`disallowedTools\`)\*\* where applicable; read-only reviewers cannot Write/Edit/Bash.  
\- \[ \] Power pack includes at least 1 workflow skill each for: \*\*PM\*\*, \*\*Creative\*\*, \*\*Life\*\* (aligned to profile).  
\- \[ \] Enterprise pack removes “speed” defaults and adds logging \+ stricter guardrails.  
\- \[ \] \`scripts/install-pack.\*\` copies a chosen pack into a target project root, resulting in \`\<project\>/.claude/...\` \+ \`\<project\>/CLAUDE.md\`.  
\- \[ \] \`scripts/validate-pack.py\` verifies: JSON validity, required files present, and no secrets committed.  
\- \[ \] Plugin directory installs via marketplace (or documented TODO if manifest schema differs).  
\- \[ \] README explains: choose pack, install, what to edit first, and how to extend safely.

\---

\#\# Inputs this brief is based on  
\- Claude-Code-Research-Profile.md :contentReference\[oaicite:0\]{index=0}    
\- contradiction-resolver-chatgpt-dr.pdf :contentReference\[oaicite:1\]{index=1}    
\- roadmap-syllabus-chatgpt-dr.pdf :contentReference\[oaicite:2\]{index=2}    
