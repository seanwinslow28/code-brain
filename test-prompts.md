# Test Prompts for Superuser Pack Validation

Use these prompts to verify your skills, agents, and hooks are working correctly.

---

## Skill Trigger Tests

Copy-paste these into Claude Code to test each skill:

### PM Skills

```
# quick-prd
"Help me create a PRD for adding dark mode to our app"

# ticket-batch
"Create Jira tickets from these notes: 1) Fix login bug 2) Add password reset 3) Update user profile UI"

# stakeholder-brief
"Write a stakeholder update about our Q1 API improvements"

# tech-spec
"Create a technical spec for implementing webhook notifications"

# meeting-prep
"Help me prepare for tomorrow's sprint planning meeting"

# decision-doc
"Document the decision to use Supabase over Firebase"
```

### Game Dev Skills

```
# phaser-pattern
"What's the best pattern for a health bar component in Phaser 3?"

# sprite-pipeline
"Set up a sprite sheet workflow for my 16-bit character animations"

# rn-debug
"My React Native app crashes on startup with a red screen"
```

### Life/Personal Skills

```
# budget-entry
"Categorize these expenses: Uber $25, Starbucks $6, Amazon $89"

# learning-drill
"Create practice exercises for learning React hooks"
```

---

## Agent Delegation Tests

```
# security-reviewer
"Review this authentication code for vulnerabilities"

# data-analyst
"Analyze this CSV and identify the top performing products"

# game-design-advisor
"Is my stamina regeneration mechanic balanced? Currently 5 points per second"

# doc-reviewer
"Review this README for completeness and clarity"
```

---

## Hook Verification Tests

### Block Secrets Hook (Should BLOCK)

```
"Create a file called .env with my API key"
"Write OPENAI_API_KEY=sk-xxx to config/secrets.json"
"Edit the .env.local file to add a database password"
```

**Expected:** These should be blocked with message "BLOCKED: Attempt to modify sensitive file"

### Block Secrets Hook (Should ALLOW)

```
"Create a regular config.json file"
"Write a new component to src/Button.tsx"
```

**Expected:** These should proceed normally

### Format Hook Test

```
"Create a JavaScript file with messy formatting:
function test(){return{foo:'bar',baz:123}}"
```

**Expected:** File should be auto-formatted after creation

---

## Configuration Verification

### Check Active Skills
```
/skills
```

### Check Active Agents
```
/agents
```

### Check Hooks Status
```
/hooks
```

### Check MCP Servers
```
/mcp
```

---

## Multi-Instance Test (for 16BitFit)

Open 3 terminal windows and run:

**Terminal 1:**
```bash
export CLAUDE_CODE_TASK_LIST_ID=16bitfit-test
cd ~/16bitfit
claude
# Then: "Add a task: Implement health bar UI component"
```

**Terminal 2:**
```bash
export CLAUDE_CODE_TASK_LIST_ID=16bitfit-test
cd ~/16bitfit
claude
# Then: "Show all tasks" - should see task from Terminal 1
```

**Terminal 3:**
```bash
export CLAUDE_CODE_TASK_LIST_ID=16bitfit-test
cd ~/16bitfit
claude
# Then: "Mark the health bar task as in progress" - should update shared list
```

---

## Expected Behaviors Checklist

After running tests, verify:

- [ ] Skills trigger on relevant keywords (PRD, ticket, Phaser, etc.)
- [ ] Agents are delegated to for specialized tasks
- [ ] block-secrets hook blocks .env file writes
- [ ] format-on-edit hook auto-formats JS/TS files
- [ ] Permission prompts are reduced for git/npm commands (if allowedTools configured)
- [ ] Multi-instance task list is shared across terminals

---

## Troubleshooting

**Skill not triggering?**
- Check the `description` field in SKILL.md matches your prompt keywords
- Verify skill is in `.claude/skills/` directory
- Try explicit invoke: `/skill-name`

**Hook not running?**
- Check hook path in settings.json is correct
- Verify hook has execute permissions: `chmod +x hook.sh`
- Check hook exit codes (0=allow, 2=deny)

**Agent not delegating?**
- Check agent is listed in settings.json `agents.enabled`
- Verify agent file is in `.claude/agents/` directory
- Try explicit invoke: `@agent-name`
