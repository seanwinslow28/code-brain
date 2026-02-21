# Superuser Pack Improvement Plan for Sean Winslow
## Phase 2, Session 1: Profile-Based Recommendations

---

## Executive Summary

Based on your profile as an Associate PM (Technical) at The Block working on Campus, Simon AI, and RevOps/AdOps automation—plus your 16BitFit game project and life automation goals—here are the **5 highest-impact improvements**:

1. **Add a `crypto-context` skill** - You're at a crypto company but have no crypto-specific terminology or context helpers. This skill would help you write specs that don't require explaining blockchain basics to Claude every time.

2. **Add a `block-company-data` hook** - Your `block-secrets` hook catches API keys, but not company-specific sensitive patterns (internal project names, unreleased product codenames, confidential revenue data). Critical for PM work.

3. **Add a `weekly-review` skill** - You have budget-entry for transactions but no skill that helps you synthesize across your three domains (PM work, 16BitFit, life). A weekly review skill compounds over time.

4. **Add an `api-docs` skill** - You work on API products at The Block, but don't have a skill for generating API documentation. This is a weekly deliverable for many PMs.

5. **Add a `code-explainer` agent** - You're a beginner coder who wants to learn. A subagent that explains code decisions as it works would accelerate your learning without slowing down output.

---

## Quick Wins (< 30 min each)

### 1. Create `crypto-context` Skill

**What:** A skill that provides crypto/blockchain context to Claude so you don't have to explain fundamentals in every prompt.

**Why for Sean:** At The Block, you're writing specs for Campus (crypto education), Simon AI, and API products. Right now, every time you ask Claude for help, you probably re-explain what staking, DeFi, or on-chain means. This skill embeds that context.

**Where it goes:** `packs/sean-custom/.claude/skills/crypto-context/SKILL.md`

**Implementation:**

```markdown
# Crypto Context Skill

## Description
Provides blockchain and cryptocurrency context for PM work at The Block.

## When to Use
Invoke this skill when writing specs, PRDs, or documentation for crypto products.

## Context to Include

### The Block Context
- The Block is a crypto news, data, and research organization
- Products include: Campus (education platform), Simon AI, API products
- Audience: crypto-native professionals and institutions

### Key Crypto Concepts (for Claude)
When helping Sean, assume familiarity with:
- Blockchain fundamentals (consensus, blocks, transactions)
- DeFi (liquidity pools, AMMs, yield farming, staking)
- Token types (ERC-20, NFTs, governance tokens)
- Wallet types (custodial, non-custodial, hardware)
- L1 vs L2 chains (Ethereum, Solana, Arbitrum, etc.)
- CEX vs DEX (centralized vs decentralized exchanges)

### Vocabulary Shortcuts
| Term | Meaning |
|------|---------|
| TVL | Total Value Locked (DeFi metric) |
| APY | Annual Percentage Yield |
| Gas | Transaction fees on Ethereum |
| Mint | Create new tokens/NFTs |
| Bridge | Move assets between chains |
| Oracle | External data feed for smart contracts |

## Output Format
When invoked, acknowledge crypto context is loaded and proceed with the task.
```

**Priority:** High
**Effort:** Quick (15 min)
**Dependencies:** None

---

### 2. Add `block-company-data` Hook

**What:** A PreToolUse hook that catches The Block-specific sensitive patterns before they're written to files or commits.

**Why for Sean:** Your `block-secrets` hook catches API keys and passwords. But as a PM, you also handle confidential company data—unreleased product names, internal project codenames, revenue figures, partner names. This hook catches those patterns.

**Where it goes:** `packs/sean-custom/.claude/hooks/block-company-data.py`

**Implementation:**

```python
#!/usr/bin/env python3
"""
PreToolUse hook: Blocks company-specific sensitive data patterns.
Customize the SENSITIVE_PATTERNS list for The Block's specifics.
"""
import sys
import json
import re

# Add your company-specific patterns here
SENSITIVE_PATTERNS = [
    # Revenue/financial patterns
    r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:revenue|ARR|MRR)',
    r'(?:Q[1-4]|FY\d{2})\s*(?:revenue|earnings|profit)',

    # Internal project codenames (customize these!)
    r'\b(?:PROJECT_CODENAME_1|PROJECT_CODENAME_2)\b',

    # Employee data patterns
    r'(?:salary|compensation|equity).*\$\d+',

    # Partner/client names (add as needed)
    r'\b(?:CONFIDENTIAL_PARTNER_1|CONFIDENTIAL_PARTNER_2)\b',

    # Unreleased product names (customize!)
    r'\b(?:UNRELEASED_PRODUCT)\b',

    # Internal URLs/endpoints
    r'(?:internal\.|staging\.)[a-zA-Z0-9-]+\.theblock\.',
]

def check_for_sensitive_data(content: str) -> list:
    """Returns list of matched sensitive patterns."""
    matches = []
    for pattern in SENSITIVE_PATTERNS:
        found = re.findall(pattern, content, re.IGNORECASE)
        if found:
            matches.extend(found)
    return matches

def main():
    try:
        hook_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Can't parse, allow

    # Get content to check
    content = ""
    if "content" in hook_data:
        content = hook_data.get("content", "")
    elif "input" in hook_data:
        content = str(hook_data.get("input", ""))

    if not content:
        sys.exit(0)  # No content, allow

    matches = check_for_sensitive_data(content)

    if matches:
        # Block with explanation
        result = {
            "status": "blocked",
            "reason": f"Company-sensitive data detected: {', '.join(matches[:3])}... Update the hook patterns or remove sensitive data."
        }
        print(json.dumps(result))
        sys.exit(1)

    sys.exit(0)  # Allow

if __name__ == "__main__":
    main()
```

**Customization needed:** Replace the placeholder patterns (PROJECT_CODENAME_1, etc.) with actual internal terms you want to protect.

**Priority:** High
**Effort:** Quick (20 min to set up, then customize over time)
**Dependencies:** None

---

### 3. Add `release-notes` Template

**What:** A template for writing release notes for The Block's products.

**Why for Sean:** You work on Campus, Simon AI, and API products. Release notes are a recurring PM deliverable. Having a template means consistent formatting and nothing gets forgotten.

**Where it goes:** `packs/sean-custom/.claude/templates/release_notes.md`

**Implementation:**

```markdown
# Release Notes Template

## [Product Name] - v[X.Y.Z] Release Notes
**Release Date:** [YYYY-MM-DD]
**Environment:** [Production/Staging]

---

### What's New

#### Features
- **[Feature Name]**: [1-2 sentence description of what users can now do]
- **[Feature Name]**: [Description]

#### Improvements
- [Improvement description - focus on user benefit]
- [Improvement description]

### Bug Fixes
- Fixed: [Description of what was broken and now works]
- Fixed: [Description]

### Known Issues
- [Issue description and workaround if available]

### Breaking Changes
- [If any: what changed and what users need to do]

### Coming Soon
- [Preview of next release's key features]

---

### Technical Notes
*For internal use*

**Dependencies Updated:**
- [package@version → version]

**Database Migrations:**
- [Yes/No - if yes, describe]

**Configuration Changes:**
- [Any new env vars or settings required]

---

### Feedback
Questions? Contact [team/channel].
```

**Priority:** Medium
**Effort:** Quick (10 min)
**Dependencies:** None

---

### 4. Create `api-docs` Skill

**What:** A skill for generating API documentation from code or specs.

**Why for Sean:** You work on API products at The Block. API docs are a core PM deliverable for developer-facing products. This skill guides Claude to produce consistent, complete API documentation.

**Where it goes:** `packs/sean-custom/.claude/skills/api-docs/SKILL.md`

**Implementation:**

```markdown
# API Documentation Skill

## Description
Generates clear, consistent API documentation for The Block's API products.

## Trigger
`/api-docs [endpoint or spec]`

## Clarifying Interview
Before generating docs, ask:

1. **What endpoint(s) are we documenting?**
   - Single endpoint or full resource?

2. **Who's the audience?**
   - Internal developers
   - External API consumers
   - Both (need public + internal notes)

3. **What's the auth model?**
   - API key
   - OAuth
   - JWT
   - None (public)

4. **What format?**
   - OpenAPI/Swagger
   - Markdown
   - README-style
   - All of the above

5. **Any existing patterns to match?**
   - Link to existing docs to match style

## Output Format

### For Each Endpoint:

```markdown
## [METHOD] /path/to/endpoint

**Description:** [What this endpoint does in one sentence]

**Authentication:** [Required/Optional - type]

### Request

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | string | Resource ID |

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 20 | Results per page |

**Request Body:**
```json
{
  "field": "type - description"
}
```

### Response

**Success (200):**
```json
{
  "data": {},
  "meta": {}
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 400 | Invalid request body |
| 401 | Unauthorized |
| 404 | Resource not found |

### Example

```bash
curl -X GET \
  'https://api.theblock.co/v1/endpoint' \
  -H 'Authorization: Bearer YOUR_TOKEN'
```
```

## Success Criteria
- [ ] All parameters documented
- [ ] Request and response examples included
- [ ] Error codes listed
- [ ] Auth requirements clear
- [ ] Copy-paste ready curl example
```

**Priority:** High (you work on API products)
**Effort:** Quick (20 min)
**Dependencies:** None

---

### 5. Add `code-explainer` Agent

**What:** A subagent that explains its code decisions as it writes, teaching you along the way.

**Why for Sean:** You're a beginner coder learning fundamentals. When Claude writes code for you, you want to understand *why* it made certain choices. This agent includes explanations in comments and summaries.

**Where it goes:** `packs/sean-custom/.claude/agents/code-explainer.md`

**Implementation:**

```markdown
# Code Explainer Agent

## Description
A teaching-focused code agent for Sean's learning journey. Writes code AND explains the reasoning behind every significant decision.

## When to Use
- When you want to understand the code, not just get it working
- When learning new patterns or languages
- When reviewing code you'll need to maintain

## Behavior

### Always Include:
1. **Why This Approach**: Before writing code, briefly explain the approach and alternatives considered
2. **Inline Comments**: Comment on non-obvious lines explaining "why" not just "what"
3. **Pattern Explanation**: When using a design pattern, name it and explain when to use it
4. **Tradeoff Notes**: If there's a simpler way that doesn't scale, or a complex way that's overkill, mention it

### Example Output:

```python
# We're using a dictionary here instead of a list because we need
# O(1) lookups by user_id. A list would require O(n) scanning.
# Tradeoff: Uses more memory, but faster for our use case.
users_by_id = {}

# Using a generator (yield) instead of returning a list because
# we might have millions of records. Generators are memory-efficient
# since they produce one item at a time.
def get_transactions(user_id):
    for tx in database.query(user_id):  # This pattern is called "lazy evaluation"
        yield tx
```

### Summary Block:
After writing code, include a "What You Learned" summary:

```
## What You Learned
1. **Dictionaries for lookup**: When you need to find items by key, use a dict
2. **Generators for large data**: `yield` is memory-efficient for big datasets
3. **Type hints**: Adding types helps catch bugs and documents intent
```

## Constraints
- `disallowedTools`: [] (needs all tools for coding)
- Focus on teaching over speed
- Never say "this is too complex to explain" - break it down instead
```

**Priority:** High (directly supports your learning goal)
**Effort:** Quick (15 min)
**Dependencies:** None

---

## Strategic Improvements (1-2 hours each)

### 6. Create `weekly-review` Skill

**What:** A structured weekly review that synthesizes across your three domains.

**Why for Sean:** You have separate skills for PM work, game dev, and life admin. But nothing helps you step back and see the big picture. A weekly review compounds—you'll spot patterns, celebrate wins, and course-correct faster.

**Where it goes:** `packs/sean-custom/.claude/skills/weekly-review/SKILL.md`

**Implementation:**

```markdown
# Weekly Review Skill

## Description
Structured weekly synthesis across PM work, creative projects, and life admin.

## Trigger
`/weekly-review` (best used Sunday evening or Monday morning)

## Interview Questions

1. **PM Work (The Block)**
   - What shipped this week?
   - What's blocked?
   - What's the #1 priority for next week?

2. **Creative Projects (16BitFit)**
   - Hours invested this week?
   - What progress was made?
   - What's the next milestone?

3. **Life Admin**
   - Any budget surprises this week?
   - Habits maintained?
   - Upcoming deadlines or commitments?

4. **Energy & Learning**
   - What drained energy?
   - What gave energy?
   - What did you learn?

## Output Format

```markdown
# Week of [DATE] Review

## Wins
- [Celebration-worthy accomplishment]
- [Another win, even small ones count]

## Progress by Domain

### PM Work
- **Shipped:** [list]
- **In Progress:** [list]
- **Blocked:** [list with blockers]

### 16BitFit
- **Hours:** X
- **Progress:** [specific progress]
- **Next:** [next milestone]

### Life
- **Budget:** On track / Over by $X / Under by $X
- **Habits:** X/Y days
- **Upcoming:** [deadlines/events]

## Patterns Noticed
- [Pattern that's worth noting]

## Next Week's Focus
1. [Top priority]
2. [Second priority]
3. [Third priority]

## One Thing to Stop/Start/Continue
- **Stop:** [Something draining time/energy]
- **Start:** [Something to try]
- **Continue:** [Something working well]
```

## Success Criteria
- [ ] All three domains reviewed
- [ ] At least one win identified
- [ ] Clear next week priorities set
- [ ] Takes < 15 minutes to complete
```

**Priority:** High (compounding habit)
**Effort:** Moderate (45 min to set up well)
**Dependencies:** None

---

### 7. Add `campus-content` Skill

**What:** A skill for creating educational content for The Block's Campus platform.

**Why for Sean:** Campus is an education platform. You're probably creating course outlines, lesson plans, quiz questions, and educational content regularly. This skill structures that work.

**Where it goes:** `packs/sean-custom/.claude/skills/campus-content/SKILL.md`

**Implementation:**

```markdown
# Campus Content Skill

## Description
Creates structured educational content for The Block's Campus platform.

## Trigger
`/campus-content [topic]`

## Content Types

### 1. Lesson Plan
```markdown
# Lesson: [Topic]

**Duration:** [X minutes]
**Level:** [Beginner/Intermediate/Advanced]
**Prerequisites:** [What learners should know first]

## Learning Objectives
By the end of this lesson, learners will be able to:
1. [Observable, measurable outcome]
2. [Another outcome]

## Lesson Structure

### Hook (2 min)
[Engaging opening question or scenario]

### Core Content (X min)
#### Concept 1: [Name]
[Explanation with crypto-relevant example]

#### Concept 2: [Name]
[Explanation with crypto-relevant example]

### Practice (X min)
[Interactive exercise or scenario]

### Check for Understanding
- Quick question 1?
- Quick question 2?

### Summary
Key takeaways:
1. [Takeaway]
2. [Takeaway]

## Resources
- [Link to further reading]
- [Related Campus content]
```

### 2. Quiz Questions
```markdown
## Quiz: [Topic]

### Question 1
**Type:** Multiple Choice
**Difficulty:** [Easy/Medium/Hard]

[Question text]

A) [Option - explain why wrong if wrong]
B) [Option]
C) [Option]
D) [Option]

**Correct Answer:** [Letter]
**Explanation:** [Why this is correct]

---

[Repeat for each question]
```

### 3. Course Outline
```markdown
# Course: [Title]

**Duration:** [X hours total]
**Level:** [Beginner/Intermediate/Advanced]
**Description:** [2-3 sentences]

## Module 1: [Name]
- Lesson 1.1: [Topic] (X min)
- Lesson 1.2: [Topic] (X min)
- Quiz 1 (X min)

## Module 2: [Name]
[Same structure]

## Learning Path
[Visual or description of progression]

## Assessment Strategy
- Quizzes: X% of completion
- Final project: [Description]
```

## Success Criteria
- [ ] Learning objectives are measurable
- [ ] Content uses crypto-relevant examples
- [ ] Appropriate for stated difficulty level
- [ ] Includes knowledge checks
```

**Priority:** High (Campus is a core product)
**Effort:** Moderate (1 hour)
**Dependencies:** `crypto-context` skill helps here

---

### 8. Create `game-progression` Skill

**What:** A skill for designing game progression systems (XP, levels, unlocks, rewards).

**Why for Sean:** 16BitFit is a fitness RPG with retro Game Boy aesthetics. Progression systems (leveling, unlocks, rewards) are core to making a game feel satisfying. This skill helps you design balanced, motivating progression.

**Where it goes:** `packs/sean-custom/.claude/skills/game-progression/SKILL.md`

**Implementation:**

```markdown
# Game Progression Design Skill

## Description
Designs balanced progression systems for 16BitFit (or other games).

## Trigger
`/game-progression [system type]`

## System Types

### 1. XP & Leveling
Questions to answer:
- What actions give XP? (workouts, streaks, achievements)
- What's the XP curve? (linear, exponential, S-curve)
- What does leveling unlock?
- How long to max level?

Output: XP table, curve visualization, unlock schedule

### 2. Achievement System
Questions to answer:
- What categories? (fitness, social, exploration, meta)
- Difficulty tiers?
- Visible vs hidden achievements?
- Rewards for each?

Output: Achievement list with unlock conditions and rewards

### 3. Reward Loop
Questions to answer:
- What's the core loop? (workout → XP → level → unlock → motivation → workout)
- Immediate rewards?
- Short-term goals (daily/weekly)?
- Long-term goals (monthly/seasonal)?

Output: Loop diagram, reward timing analysis

### 4. Currency Economy
Questions to answer:
- What currencies? (coins, gems, energy)
- Earn rates?
- Spend sinks?
- Premium vs free?

Output: Economy spreadsheet template, balance recommendations

## Design Principles (for 16BitFit)

1. **Fitness-first**: Rewards should encourage healthy behavior, not gaming the system
2. **Sustainable**: Daily engagement shouldn't require 2-hour sessions
3. **Retro-authentic**: Rewards should feel like Game Boy era (badges, pixel unlocks)
4. **Failure-friendly**: Missing a day shouldn't destroy progress

## Output Format

```markdown
# [System Type] Design for 16BitFit

## Overview
[Summary of the system]

## Mechanics
[Detailed explanation]

## Balance Analysis
| Level | XP Required | Total XP | Est. Days | Unlock |
|-------|-------------|----------|-----------|--------|
| 1     | 0           | 0        | 0         | Tutorial badge |
| 2     | 100         | 100      | 1         | New sprite color |
...

## Implementation Notes
- Data structure recommendation
- Code patterns to use (from phaser-pattern skill)

## Potential Issues
- [Issue and mitigation]
```

## Success Criteria
- [ ] Mathematically balanced (no exploits)
- [ ] Motivating for target player
- [ ] Implementable in Phaser 3 + React Native
- [ ] Fits retro Game Boy aesthetic
```

**Priority:** High (core to 16BitFit's success)
**Effort:** Moderate (1-2 hours)
**Dependencies:** Works well with existing `phaser-pattern` skill

---

### 9. Add `revops-automation` Skill

**What:** A skill for designing and documenting RevOps/AdOps automation workflows.

**Why for Sean:** You work on RevOps/AdOps automation at The Block. This means designing workflows for revenue operations, ad operations, and related business processes. Having a skill helps you document and spec these consistently.

**Where it goes:** `packs/sean-custom/.claude/skills/revops-automation/SKILL.md`

**Implementation:**

```markdown
# RevOps/AdOps Automation Skill

## Description
Designs and documents automation workflows for revenue and advertising operations.

## Trigger
`/revops-automation [workflow name]`

## Interview Questions

1. **What process are we automating?**
   - Lead routing
   - Ad campaign reporting
   - Revenue recognition
   - Invoice generation
   - Other: [describe]

2. **What systems are involved?**
   - Salesforce
   - HubSpot
   - Google Ads
   - Custom APIs
   - Spreadsheets (to eliminate)
   - Other: [list]

3. **What's the trigger?**
   - Scheduled (daily/weekly)
   - Event-driven (new lead, campaign end)
   - Manual (on-demand)

4. **What are the steps?**
   - Walk me through manually first

5. **What could go wrong?**
   - Data quality issues
   - API failures
   - Edge cases

## Output Format

```markdown
# Automation: [Workflow Name]

## Overview
**Trigger:** [When this runs]
**Frequency:** [How often]
**Owner:** [Who maintains it]

## Process Flow
```
[Trigger]
    ↓
[Step 1: Action]
    ↓
[Decision Point?]
  Yes → [Step 2a]
  No  → [Step 2b]
    ↓
[Step 3: Output]
```

## Systems Integration

| System | Role | Connection |
|--------|------|------------|
| Salesforce | Source of leads | API |
| Zapier | Orchestration | Webhook |
| Slack | Notifications | API |

## Data Flow

**Input:**
- [Data field]: [Source] - [Format]

**Transformations:**
- [What changes between input and output]

**Output:**
- [Data field]: [Destination] - [Format]

## Error Handling

| Error Type | Detection | Response |
|------------|-----------|----------|
| API timeout | Retry 3x | Alert Slack |
| Missing data | Null check | Skip + log |

## Monitoring
- Success metric: [What indicates it worked]
- Alert channel: [Where failures notify]
- Dashboard: [Where to check status]

## Manual Fallback
If automation fails, here's how to do it manually:
1. [Step]
2. [Step]
```

## Success Criteria
- [ ] All systems and connections documented
- [ ] Error handling defined
- [ ] Monitoring in place
- [ ] Manual fallback documented
```

**Priority:** Medium-High (core to your role)
**Effort:** Moderate (1 hour)
**Dependencies:** None

---

## Advanced/Future Improvements

### 10. MCP Server Integrations

**What:** Connect Claude Code to your actual tools via MCP (Model Context Protocol).

**Why for Sean:** You use Jira, Figma, Notion, Slack, and GitHub. MCP servers let Claude Code read from and write to these tools directly. Instead of copy-pasting, Claude can create Jira tickets, read Figma designs, or update Notion docs.

**Implementation Path:**

1. **Jira MCP** - You already have Jira integration (I see it in the connected tools). Use it with your pm-jira skill.

2. **Figma MCP** - Also connected! Use with design specs and handoff docs.

3. **GitHub MCP** - For repository exploration and PR creation.

4. **Notion MCP** - Would need to check if available; great for knowledge base integration.

**Priority:** Medium (powerful but requires setup time)
**Effort:** Involved (2-4 hours per integration)
**Dependencies:** MCP server availability, API credentials

---

### 11. Headless Automation Pipeline

**What:** Run Claude Code skills automatically on schedules or triggers.

**Why for Sean:** Once you have skills like `weekly-review`, you could trigger them automatically (Sunday 6pm = weekly review prompt). Or auto-generate release notes when a GitHub tag is created.

**Implementation:** This requires headless mode setup and potentially cron/scheduler integration.

**Priority:** Low (learn the skills first, automate later)
**Effort:** Involved (half day+)
**Dependencies:** Comfort with command line, headless mode

---

### 12. Custom Slash Command Shortcuts

**What:** Create aliases for your most-used skill combinations.

**Why for Sean:** Instead of `/quick-prd` then `/ticket-batch` then doc-reviewer, you could have `/full-spec` that chains them.

**Priority:** Low (optimize after you have muscle memory)
**Effort:** Moderate
**Dependencies:** Understanding of how skills chain

---

## Implementation Roadmap

### Week 1: Foundation (Quick Wins)
- [ ] Day 1: Add `crypto-context` skill (15 min)
- [ ] Day 1: Add `code-explainer` agent (15 min)
- [ ] Day 2: Add `block-company-data` hook + customize patterns (30 min)
- [ ] Day 3: Add `api-docs` skill (20 min)
- [ ] Day 4: Add `release-notes` template (10 min)
- [ ] Day 5: Test all new components with real work

### Week 2: Strategic Skills
- [ ] Day 1-2: Build `weekly-review` skill (45 min)
- [ ] Day 2-3: Build `campus-content` skill (1 hr)
- [ ] Day 4-5: Build `game-progression` skill (1-2 hr)
- [ ] Day 5: First weekly review using the skill

### Week 3: Domain Deepening
- [ ] Build `revops-automation` skill (1 hr)
- [ ] Customize existing skills based on Week 1-2 usage
- [ ] Explore MCP integrations you already have connected

### Week 4+: Iteration
- [ ] Headless automation exploration
- [ ] Custom command shortcuts
- [ ] Phase 2 Session 2 (Research-Informed Improvements)

---

## Learning Path

As you implement these improvements, you'll learn:

| From This | You'll Learn |
|-----------|--------------|
| `crypto-context` skill | How to embed domain knowledge in skills |
| `block-company-data` hook | Python regex, how hooks intercept actions |
| `code-explainer` agent | How subagents modify Claude's behavior |
| `weekly-review` skill | Skill interview patterns, structured output |
| `campus-content` skill | Content templates, educational design |
| `game-progression` skill | Game design fundamentals, balance math |
| `revops-automation` skill | Workflow documentation, system design |
| MCP integrations | How Claude connects to external tools |

---

## Specific Answers to Your Questions

### Based on PM Work at The Block:

1. **Skills for Campus PRDs**: Use `quick-prd` + `crypto-context` + `campus-content` together
2. **Agents for crypto tech specs**: `pm-tech-writer` (already have) + `code-explainer` (new)
3. **Hooks for company info**: `block-company-data` (new) + `block-secrets` (existing)
4. **Templates for stakeholder comms**: `release-notes` (new), `stakeholder_update` (existing)
5. **RevOps automation patterns**: `revops-automation` skill (new)

### Based on 16BitFit:

1. **Game mechanic skills**: `game-progression` (new) + `phaser-pattern` (existing)
2. **Game design agents**: `game-design-advisor` (existing)
3. **Code quality hooks**: `format-on-edit` (existing) + `run-tests-on-stop` (existing)
4. **Game feature templates**: `game_feature_spec` (existing)
5. **Creative workflows**: `sprite-pipeline` (existing)

### Based on Life Automation:

1. **Budget tracking**: `budget-entry` (existing) + `life-budget` (existing)
2. **Financial decisions**: Build on `decision-doc` skill (existing)
3. **Personal data security**: `block-secrets` (existing) covers this
4. **Life admin templates**: `weekly-review` (new) synthesizes everything
5. **Productivity patterns**: `weekly-review` + existing skills cover this

---

## What's NOT Included (Waiting for Session 2)

These will come from your research files in Session 2:

- Community-discovered workflow patterns
- Plugin recommendations from other users
- Advanced hook strategies from documentation
- MCP server configurations and tips
- Superuser techniques we haven't covered

---

## Next Steps

1. **Start with Quick Wins** - Implement items 1-5 this week
2. **Test with real work** - Use new components on actual tasks
3. **Note what works** - Keep a simple log (as suggested in the Strategy Guide)
4. **Customize** - Adjust templates and patterns based on your experience
5. **Prep for Session 2** - Identify which research files are most relevant

Ready to implement? Start with `crypto-context` — it's 15 minutes and immediately useful for every Block-related task.
