---
type: research-prompt
project: prj-job-hunt-2026
target_model: gemini-deep-research-max
estimated_cost: ~$5
created: 2026-05-07
expected_output: vault/20_projects/research/2026-05-07-target-role-specs.md
ai-context: "DR Max prompt for the Week-2 target-30 list + application customization. Engineered using the prompt-engineering skill — clarity + role + XML structure + anti-hallucination guards + portfolio-mapping requirement + validation."
---

# Gemini DR Max Prompt — Target Role Specs (Anthropic FDE / Glean / Sierra / Decagon / Scale)

> Copy everything below the `--- PROMPT START ---` line into Gemini Deep Research (Max tier) or pipe via `agents-sdk/scripts/gemini_dr.py --tier max`. Output report saves to `vault/20_projects/research/2026-05-07-target-role-specs.md`.

--- PROMPT START ---

<role>
You are a talent intelligence analyst with deep coverage of AI-native PM and Forward Deployed Engineer hiring at frontier and rising AI companies. You read JDs, hiring manager podcasts, and Levels.fyi; you track who recently joined where, what they shipped before, and what the actual interview shape is — not what marketing says it is. You speak with the precision of someone whose recommendations have been independently verified by candidates who got offers.

Your job is to produce a grounded role-intelligence document for a 33-year-old PM (2 years experience, currently in AI-native PM job-hunt mode, Boston-metro / remote-flexible) with a specific portfolio shape. The document feeds (a) the PM's Week-2 target-30 company list, (b) application customization, and (c) interview-prep priority sequencing.
</role>

<context>
**The candidate's primary track:** AI Product Manager.
**Backup track:** Agent Ops / Forward Deployed Product / Support Ops AI.

**Tier-A constraints (non-negotiable):**
- Walk-away salary: $100k base
- Will not take 5-day-in-office roles (3 days max, prefers 0-2)
- Boston-metro preferred, remote works
- AI > Tech > Creative PM ordering

**Companies named in current planning** (not exhaustive — the report should ADD to this list, not just process it):
- Anthropic (Forward Deployed Engineer, Boston / NYC / Chicago)
- Glean (Agent Security & Governance, AI Quality, Forward Deployed Product)
- Sierra (agent PM roles)
- Decagon (agent PM roles)
- Scale AI (GenAI Platform PM, Public Sector T&E PM)
- Robinhood, Pair (per the candidate's existing roadmap)
- Plus: any company hiring AI PMs / FDPs / Agent Ops where the candidate's specific portfolio shape (MCP server + agent fleet + comprehension artifacts) is a meaningful differentiator.

**Candidate's existing high-leverage artifacts** (each will be linked from applications):
1. `intent-engineering` MCP server — ships 2026-05-25, three tools, TypeScript, Claude Desktop demo.
2. 14-agent SDK fleet — launchd-scheduled, cost governors, local-model-first routing, 7 active agents.
3. Phase D typed reasoning edges — `concept_edges` SQLite + synthesizer-emitted relations (supports / contradicts / supersedes).
4. Phase 6 knowledge loop — SessionEnd flush → nightly synthesizer → weekly lint → SessionStart re-injection.
5. Sanitized agentic financial-research fleet — multi-agent retrieval + synthesis, daily-note pipeline.
6. Animation pipeline — June 11 short-film ship, ComfyUI + Remotion + LoRA workflow.

**Seniority calibration (critical for tier sorting):**
The candidate has 2 years of titled PM experience but a portfolio demonstrating 4-6 years of agentic-engineering signal. This portfolio-vs-tenure asymmetry drives role targeting:

- **Tier-1 (realistic-fit):** AI APM / rotational tracks, Product Manager I/II at AI-native companies, Forward Deployed Product IC, Agent Ops L3-L4. Roles where 2-3 years is the stated bar OR where the JD weights demonstrated work over tenure.
- **Tier-2 (stretch):** Senior PM at small AI startups (Series A-B) where portfolio can outweigh years-of-experience. PM at growth-stage AI shops with flexible tenure requirements.
- **Tier-3 (wildcards):** Roles where the public JD floor is "5+ years" but the hiring manager's posts indicate portfolio-weighted hiring (Anthropic FDE is the canonical example). Reaches but not impossible.

**Avoid (don't include even as wildcards):** Senior Group PM, Director of Product, Principal PM, Staff PM, anything with a hard "minimum 5 years" floor and no portfolio-substitution language, anything implying multi-team management.
</context>

<task>
Produce an 8-section role intelligence report covering the companies + roles in <output_format>. Multi-source triangulation: cross-reference each claim against ≥2 independent primary sources where possible. Where sources disagree (e.g., comp-range data from Levels.fyi vs. Glassdoor), surface the disagreement and recommend the more credible source.

For each role, the goal is NOT to summarize the public JD — the candidate can read those. The goal is to surface the things the JD does NOT say but that someone deciding where to apply needs:
- The actual interview shape (number of rounds, vibe-coding component yes/no, take-home or live-coding, portfolio review, on-site format)
- Recent hires' backgrounds and what they shipped before joining
- What hiring managers say in podcasts / posts about what they're looking for
- The signal differential between "good candidate" and "interview-stage candidate"
- How the candidate's specific artifacts map (or don't) to each role's stated priorities
</task>

<anti_hallucination_guards>
Non-negotiable. Prior research runs have fabricated company names, role titles, comp figures, and "recent hires." To prevent recurrence:

1. Every named company/role must link to a current, reachable JD URL OR an archived JD URL with the archive date stated. If neither is available, mark as "Role not currently posted — last verified <date>."
2. Comp ranges must cite source: Levels.fyi entry URL + entry date, Glassdoor URL, JD-disclosed range, or "Reported by candidate via <source>." Do not invent or interpolate.
3. "Recent hires" — only include hires you can verify via LinkedIn URL, company announcement, or first-party post. If you cannot link to the proof, do not name the hire.
4. "Hiring manager said X" — only include if X is from an attributable source (named podcast episode + timestamp, post URL, conference talk URL). Do not paraphrase rumor.
5. If a role's interview shape is unknown, write "Interview shape: not publicly verifiable — recommend candidate research via Glassdoor + LinkedIn outreach to recent hires." Do not invent.
6. Anthropic's FDE listing is real (per user-provided context). Verify the current posting status, locations, and any updates since 2026-04. If the JD has changed materially, flag the changes.
</anti_hallucination_guards>

<citation_format>
Use this format for every cited claim. Examples of good vs. anti-pattern:

GOOD:
> Anthropic's Forward Deployed Engineer role (Boston) discloses a base comp range of $XXXk-$YYYk per the JD, accessed 2026-05-07 ([anthropic.com/jobs/...](https://...), accessed 2026-05-07).

GOOD:
> Sierra runs a 45-minute live-coding rep using Cursor as part of its on-site, per <a href="https://news.aakashg.com/p/...">Aakash Gupta's reporting on AI-native onsites</a>, episode dated 2026-XX-XX.

ANTI-PATTERN (do not produce):
> Anthropic pays competitively for FDE roles. Sierra runs a vibe-coding interview as part of their loop.

The first two contain a verifiable fact + a verifiable URL + an accessed-on date. The third is rumor and is forbidden.
</citation_format>

<output_format>
Markdown document with this exact frontmatter, then the eight sections. Use the literal `<RESEARCH_DATE>` placeholder if needed.

```
---
type: research-report
project: prj-job-hunt-2026
research_topic: target-role-specs-2026-05
created: <RESEARCH_DATE>
model: gemini-deep-research-max
ai-context: "Role intelligence for the Week-2 target-30 list and application customization. All claims cited or marked unverifiable."
---
```

# Target Role Specs 2026-05 — Anthropic FDE / Glean / Sierra / Decagon / Scale + Adjacent

## 1. Tier-1 Roles — Apply First (4-6 roles)
**Calibration:** Tier-1 = realistic-fit per the seniority calibration in `<context>`. AI APM / rotational tracks, Product Manager I/II at AI-native companies, Forward Deployed Product IC roles, Agent Ops L3-L4. NOT Senior PM / Staff PM / Group PM unless the JD explicitly weights portfolio over tenure.

For each: company, exact role title, location / remote-policy, JD URL, comp range with source, the 2-3 things the JD wants that the candidate's portfolio uniquely answers, and the 1-2 things the JD wants that the candidate does NOT have (and how big a deal it is). Order by best-fit-first.

## 2. Tier-2 Roles — Apply in Wave 2 (8-12 roles)
Same schema as Tier-1, lighter detail. These are the "good fit but lower probability" or "stretch but still realistic" roles.

## 3. Tier-3 Roles — Wildcards (3-5 roles)
Reaches where the public JD says "5+ years" but the hiring manager weights portfolio over tenure (Anthropic FDE is canonical — explicitly portfolio-weighted in its public framing). Asymmetric upside. For each: surface the specific signal that suggests portfolio-substitution is realistic (hiring manager post URL, recent hire backgrounds, role description language).

## 4. Interview Shape by Role Family
Group roles into 3-4 families (e.g., AI PM at frontier model labs, Agent PM at AI-native startups, Forward Deployed Engineer/Product at infra companies, Agent Ops at platform shops). For each family, document:

- Typical loop structure (rounds, formats)
- Vibe-coding rep yes/no, and what the rep looks like (Bolt / v0 / Cursor 45-min build? take-home with rubric?)
- Portfolio review format (live walkthrough vs. async review)
- The "differentiator" question family interviewers most often ask
- Common rejection reasons that come up in candidate post-mortems

Cite sources: hiring-manager podcasts, candidate post-mortems on Substack / Twitter / Reddit, public interview-prep guides like Aakash Gupta's research on AI-native onsites at Sierra.

## 5. Portfolio-to-Role Mapping
For each of the candidate's six listed artifacts, list which roles in §1-3 directly value that artifact and how to pitch it (one sentence per role-artifact pair). Also identify the artifact GAPS: roles where the portfolio is weak, and what's the smallest patch (e.g., "one eval suite would unlock the AI Quality roles at Glean and Scale").

## 6. Boston-Metro vs. Remote Reality Check
For each Tier-1 and Tier-2 role: actual remote policy, how often "remote" turns into "Boston / NYC / SF preferred" in practice, comp adjustments by location, and Boston-specific opportunities the broader search missed (e.g., HubSpot AI, Klaviyo AI Platform, MIT-spinout AI startups).

## 7. Application Sequencing Recommendation
A specific 4-week sequence: which 5-8 roles to hit Week 3, which Week 4, etc. Logic: order by (probability × match) but front-load wildcards because they take longer in pipeline. Include the Anthropic FDE wildcard slot for Week 2 per the candidate's existing plan.

## 8. Sources Index
Every JD URL, podcast, post, Levels.fyi entry, and LinkedIn announcement cited above. Organized by company. Include accessed-on date for each.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health**: Every JD URL gets opened to verify it loads and is current. Replace any 404s or "position filled" with archived-URL-or-removal.
2. **Comp source**: Every comp range gets source-checked. If a range comes from a single Levels.fyi entry, mark as PRELIMINARY.
3. **Hire verification**: Every "recent hire" gets LinkedIn-verified. Remove any unverifiable.
4. **Mapping discipline**: Re-read §5. For each artifact-to-role match, verify the role's JD actually requests something in that category. Tighten or remove weak matches.
5. **Tier-A check**: Every recommended role respects the candidate's $100k floor and ≤3-day-in-office cap. Flag any role that violates this and explain why it's still on the list.
6. **Seniority discipline**: Re-read §1. If any Tier-1 role has a stated "minimum 5 years PM experience" floor without explicit portfolio-substitution language in the JD, demote to Tier-3 or remove. Tier-1 should be APM / PM I-II / FDP-IC tracks where 2 years is acceptable.
7. **Word count**: Target 4,000-6,500 words. Below 4,000 means under-researched; above 6,500 means padding.
</validation>

--- PROMPT END ---
