# Sean's Custom Skill Pack

A curated set of 12 skills + 3 subagents designed for your PM + Creator + Coder workflow.

## Quick Reference

### PM Work Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| **quick-prd** | `/quick-prd [feature]` | Idea → PRD in <5 min with smart interview |
| **ticket-batch** | `/ticket-batch [source]` | Batch-create Jira/Linear tickets from PRDs or notes |
| **stakeholder-brief** | `/stakeholder-brief [project]` | TL;DR-first status updates that get read |
| **tech-spec** | `/tech-spec [feature]` | Implementation-ready specs for engineering |
| **meeting-prep** | `/meeting-prep [type] [duration]` | Agendas that respect everyone's time |

### Creative/Dev Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| **phaser-pattern** | `/phaser-pattern [topic]` | Phaser 3 patterns + React Native integration |
| **rn-debug** | `/rn-debug [error]` | Systematic RN debugging (iOS/Android/Expo) |
| **sprite-pipeline** | `/sprite-pipeline [task]` | Automate sprite sheets + asset optimization |
| **prototype-scaffold** | `/prototype-scaffold [stack]` | Zero-to-coding in <2 min |

### Life/Meta Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| **budget-entry** | `/budget-entry [transactions]` | Quick expense categorization |
| **decision-doc** | `/decision-doc [type]: [question]` | Document decisions so future-you understands |
| **learning-drill** | `/learning-drill [skill] [time]` | Deliberate practice for coding fluency |

## Subagents

| Agent | When to Use |
|-------|-------------|
| **context-gatherer** | Before writing PRDs/specs - gathers minimal relevant context |
| **checklist-validator** | Before marking done - validates against acceptance criteria |
| **doc-reviewer** | Before sharing - catches gaps stakeholders would ask about |

## Design Principles

Every skill follows these rules:

1. **Clarifying Interview First** - Asks 5-6 questions upfront to avoid back-and-forth
2. **Explicit Success Criteria** - You know exactly when it's "done"
3. **Verification Steps** - Checklist to validate output quality
4. **Minimal Context** - Never pulls entire repo; targeted searches only
5. **Copy/Paste Ready** - Outputs are ready to use, not require reformatting

## Workflow Examples

### "I need to spec a new feature"
```
1. /quick-prd Login with SSO
2. [Answer interview questions]
3. [Get PRD output]
4. Use doc-reviewer to check before sharing
5. /ticket-batch from PRD → Jira stories
```

### "I'm debugging a React Native crash"
```
1. /rn-debug [paste error message]
2. [Follow decision tree]
3. [Get fix or diagnostic commands]
```

### "I need to give a stakeholder update"
```
1. /stakeholder-brief weekly for Auth Project
2. [Answer tone/format questions]
3. Use doc-reviewer before sending
```

### "I want to practice React hooks"
```
1. /learning-drill React hooks 15 minutes
2. [Complete exercises without docs]
3. [Check solutions, log progress]
```

## Installation

This pack is located at: `packs/sean-custom/.claude/`

To use with Claude Code:
1. Copy `.claude/` folder to your project root
2. Skills auto-discover from the skills directory
3. Agents available when you reference them

## Customization

Each skill has:
- `SKILL.md` - Main skill definition
- Clarifying interview (customize questions for your workflow)
- Output format (adjust templates to match your tools)
- Success criteria (modify based on your quality bar)

Feel free to fork and adapt!
