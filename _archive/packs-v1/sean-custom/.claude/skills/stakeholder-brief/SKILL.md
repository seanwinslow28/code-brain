---
name: stakeholder-brief
description: Creates one-page stakeholder updates optimized for busy executives. TL;DR first, details on demand.
---

# Stakeholder Brief Skill

## Purpose

Create status updates that get read. Optimized for:
- Executives who skim
- Slack/email consumption
- Async communication
- Building trust through transparency

## Clarifying Interview

```
Stakeholder Brief Setup:

1. **Audience:** Leadership | Cross-functional | Investors | All-hands
2. **Frequency:** Weekly | Bi-weekly | Monthly | Ad-hoc
3. **Project/Initiative:**
4. **Tone:** Formal | Casual | Urgent
5. **Include metrics?** Y/N
```

## Output Format

```markdown
# [Project] Status Update - [Date]

## TL;DR (30 seconds)
🟢/🟡/🔴 **Overall:** [One-line status]
- [Key win this period]
- [Key blocker/risk if any]
- [What's needed from stakeholders]

---

## Progress This Period
✅ **Completed:**
- [Accomplishment 1]
- [Accomplishment 2]

🔄 **In Progress:**
- [Work item 1] - [% or status]
- [Work item 2] - [% or status]

## Metrics (if applicable)
| Metric | Target | Actual | Trend |
|--------|--------|--------|-------|
| ...    | ...    | ...    | ↑/↓/→ |

## Risks & Blockers
| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| ...  | H/M/L  | ...        | ...   |

## Next Period
- [ ] Priority 1
- [ ] Priority 2
- [ ] Priority 3

## Asks
- **From [Person/Team]:** [Specific ask]

---
*Questions? Reply to this thread or ping @[owner]*
```

## Success Criteria

- [ ] TL;DR is readable in <30 seconds
- [ ] Status color (🟢/🟡/🔴) is defensible with evidence
- [ ] No surprises - risks were flagged before they became problems
- [ ] Asks are specific and actionable (not "support needed")
- [ ] Update builds narrative continuity from previous updates

## Verification Steps

1. **Skim Test:** Read only headers and TL;DR. Do you know the status?
2. **Action Test:** Is every "ask" specific enough to act on today?
3. **Surprise Test:** Would any stakeholder be surprised by this content?
4. **Evidence Test:** Can every claim be backed by a ticket/metric/artifact?

## Tone Templates

**Formal (Investors/Board):**
> "The authentication initiative remains on track for Q2 delivery. Key milestone achieved: SSO integration completed. Primary risk: third-party API rate limits may require architecture adjustment."

**Casual (Internal Slack):**
> "Auth project update! 🎉 SSO is DONE. Next up: password reset flow. One hiccup - the external API is rate-limited so we might need to cache more aggressively. Will know more by Friday."

**Urgent (Escalation):**
> "🔴 BLOCKED: Auth project at risk. Payment provider API has been down for 48 hours. Need executive escalation to their enterprise support. Impact: 2-week delay if not resolved by EOD Wednesday."

## Anti-Patterns

- Burying bad news at the bottom
- Status colors that don't match content
- Vague blockers ("waiting on dependencies")
- No asks when stakeholder action is needed
- Updates that could apply to any project (too generic)

## Copy/Paste Ready

```
/stakeholder-brief weekly for Auth Project
/stakeholder-brief urgent - API outage impacting launch
/stakeholder-brief monthly investor update
```
