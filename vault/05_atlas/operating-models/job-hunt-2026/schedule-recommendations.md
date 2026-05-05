---
type: operating-model
artifact: schedule-recommendations
domain: [job-hunt-2026]
status: confirmed
last_interviewed: 2026-05-05
created: 2026-05-04
ai-context: "Layer 5 friction findings + automation candidates expressed as 'when X, then Y' rules. Consumed by daily-driver and meta-agent for the Domain-Aware Insights summary. Drives Sean's Protect / Automate / Decline lists. North star: free up an hour/day for agentic-workflow + Agent-Evals + enterprise-build learning."
---

# Schedule Recommendations — Job Hunt 2026

## Protect

_(Calendar-level defenses. When X, then Y.)_

- **When the clock hits 8:30 AM, then the next 60 minutes are LEARNING ONLY** — no email, no LinkedIn, no apps. Daily-driver should refuse to surface any pipeline noise during this window.
- **When it's 9:30 AM Mon–Fri, then start with yesterday's open thread** (the kickoff prompt Claude wrote at end-of-day). Don't restart from scratch.
- **When it's 1:00–2:30 PM Mon–Fri, then the mid-day break is sacred.** No "quick recruiter screens" wedged in. The break is how Sean handles a long day mentally; compressing it costs the afternoon.
- **When it's Friday 4:30 PM, then the weekly retro runs (60 min, self + Claude).** Even in slow weeks. Even in hot interview weeks. Doesn't get skipped.
- **When it's 5:30 PM, then active job-hunt admin stops.** Informal learning bleed after is fine; pipeline / outreach / applications stop.
- **When Track-C MCP work is on the day's plan, then it gets the morning slot, not the afternoon scraps.** Building energy peaks before lunch.
- **When it's an offer week, then Track-C still gets at least one block on the calendar.** Differentiator does not get displaced by closing logistics.

## Automate

_(Manual work that should become agent-triggered. All of these are 20-min tasks today; targets are all 2-min or less.)_

**Application logging (highest priority):**
- One-shot: paste a JD URL → agent extracts company / role / link / resume variant → updates `prj-job-hunt-2026/README.md` pipeline table → logs to outreach log if a referral was used.

**Multi-board job aggregation:**
- Pull LinkedIn + Wellfound notification feeds (and any newly added boards) into a single ranked list filtered by USER.md prioritization criteria — geo, archetype, walk-away, brand bias.

**Resume keyword-tailoring per role:**
- Given a JD, pick the right master-resume variant (AI / Tech / Creative PM), surface 3–5 keyword-match suggestions, generate a tailored variant for review.

**"What should I build for company X" recommender:**
- Given a target company, scan their public surface (job ads, blog, GitHub, recent press) and propose 1–2 portfolio projects that would resonate. Pairs with Track-C planning.

**Cross-posting from a single source:**
- Substack post → auto-prepared Twitter thread + LinkedIn share. Sean reviews + publishes; doesn't rewrite.

**Gmail labeling pipeline (open action):**
- Set up labels (`recruiter`, `interview-loop`, `reference-request`, `network`); pipe labeled threads → markdown in `vault/30_domains/job-hunt-2026/email/` so Claude Code has fast file-system access without live MCP.

**Recruiter scheduling:**
- Standard "here are 3 windows in the next 5 days" reply template, generated from calendar free/busy. Sean reviews + sends.

**Interview-loop logistics:**
- One markdown-per-loop with prep checklist, company research summary, role 1-pager, talk-track variant, and a thank-you template pre-filled at loop kickoff.

**Follow-up reminder agent:**
- Weekly sweep: "X warm-network ping is at day 5 — draft a follow-up?" / "Y interview was 6 days ago — confirm thank-you went out."

**Cold-recruiter spam filtering:**
- Triage labeled `recruiter` mail against USER.md auto-no list (below walk-away, non-Boston/non-remote, bootcamp/consulting, 5-day-in-office). Surface only the survivors.

**Pipeline table updates:**
- README pipeline table should be agent-touchable so updates don't require manual table editing.

## Decline or Defer

- **Cold-recruiter spam below walk-away or outside geo filters** — ignore at the inbox-triage layer.
- **5-days-in-office roles** — auto-no, no exception.
- **Bootcamps / consulting roles** — auto-no.
- **LinkedIn one-click "Easy Apply"** — declined as a method; applications go through the company-direct path with a tailored resume.
- **Recruiter calls before research is done** — defer the call by 24–48h rather than take it cold.
- **"Just checking in" follow-ups** — declined; if there's no new value, don't send.

## 20-Minutes-to-2-Minutes Candidates

_(High-leverage automation targets from Q5.1 — the headline list.)_

1. **Logging an application** (find role / paste link / paste resume version / update README) → one-shot from URL.
2. **Researching a company before a recruiter call** → agent-generated 1-page brief.
3. **Tailoring a resume variant per role** → JD-in / variant-out.
4. **Drafting a Substack post from raw notes** → first-draft auto-generated in Sean Mode for review.
5. **Triaging the Gmail inbox** → labels + markdown pipeline + auto-no filter.
6. **Writing a thank-you follow-up after an interview** → template auto-filled with the loop's specifics.
7. **Updating the pipeline table in the README** → agent-touchable structured edit.

## Context-Switch Costs to Minimize

- **IDE ↔ LinkedIn / Wellfound.** Solution direction: the multi-board aggregation pipeline above means LinkedIn / Wellfound rarely need to be opened during deep-work hours — Sean reads a digest instead.
- **Cross-machine switches (Mac Mini ↔ MBP ↔ Alienware).** Solution direction: the Mac Mini is the build-primary; MBP is travel/couch; Alienware stays out of the daily hunt loop. Restructure the agent fleet so nothing critical-path requires MBP or Alienware to be awake (see "Claude Code / Agent-Fleet Friction Points" below).

## Claude Code / Agent-Fleet Friction Points

_(From Q5.7 — these are hooks/agents to fix or build.)_

- **Agent fleet audit required.** Keep daily-driver + deep_researcher (top-priority during the hunt). Audit every other active agent for relevance, reliability, and host dependency.
- **Migrate everything to Mac Mini as always-on host.** Anything that depends on the MacBook Pro or Alienware being awake to function should either be moved to the Mac Mini or retired. The MBP/Alienware-awake assumption is too flaky to be load-bearing during an active hunt.
- **Plan a restructure pass** — sequence the audit, the migration, and the deletions as an explicit work item, not background drift.

## The Extra Hour

_(If Sean had +1 hour every weekday in this domain, where it goes. North star — the agent fleet should optimize toward freeing this hour.)_

The extra hour is **learning, specifically along three vectors:**

1. **Agentic workflows + agent-harness fundamentals.** Not just "use the SDK" — *understand* where harness-level problems arise and how to fix them. Pattern-level, not symptom-level.
2. **Agent Evals.** The term Sean keeps hearing in AI PM circles — needs to be genuinely fluent, not surface-level.
3. **Enterprise-level building.** Sean currently builds locally; needs the bridge from "local prototype" to "company would trust me to ship and manage teams against this." Patterns, not just tools.

Every automation in this file should free time toward these three. If a proposed automation doesn't, deprioritize it.
