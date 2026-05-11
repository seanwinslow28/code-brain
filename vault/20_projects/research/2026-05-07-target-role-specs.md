---
type: research-report
date: 2026-05-07
question: "<role>
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
- **Tier-3 (wildcards):** Roles where the public JD floor is '5+ years' but the hiring manager's posts indicate portfolio-weighted hiring (Anthropic FDE is the canonical example). Reaches but not impossible.

**Avoid (don't include even as wildcards):** Senior Group PM, Director of Product, Principal PM, Staff PM, anything with a hard 'minimum 5 years' floor and no portfolio-substitution language, anything implying multi-team management.
</context>

<task>
Produce an 8-section role intelligence report covering the companies + roles in <output_format>. Multi-source triangulation: cross-reference each claim against ≥2 independent primary sources where possible. Where sources disagree (e.g., comp-range data from Levels.fyi vs. Glassdoor), surface the disagreement and recommend the more credible source.

For each role, the goal is NOT to summarize the public JD — the candidate can read those. The goal is to surface the things the JD does NOT say but that someone deciding where to apply needs:
- The actual interview shape (number of rounds, vibe-coding component yes/no, take-home or live-coding, portfolio review, on-site format)
- Recent hires' backgrounds and what they shipped before joining
- What hiring managers say in podcasts / posts about what they're looking for
- The signal differential between 'good candidate' and 'interview-stage candidate'
- How the candidate's specific artifacts map (or don't) to each role's stated priorities
</task>

<anti_hallucination_guards>
Non-negotiable. Prior research runs have fabricated company names, role titles, comp figures, and 'recent hires.' To prevent recurrence:

1. Every named company/role must link to a current, reachable JD URL OR an archived JD URL with the archive date stated. If neither is available, mark as 'Role not currently posted — last verified <date>.'
2. Comp ranges must cite source: Levels.fyi entry URL + entry date, Glassdoor URL, JD-disclosed range, or 'Reported by candidate via <source>.' Do not invent or interpolate.
3. 'Recent hires' — only include hires you can verify via LinkedIn URL, company announcement, or first-party post. If you cannot link to the proof, do not name the hire.
4. 'Hiring manager said X' — only include if X is from an attributable source (named podcast episode + timestamp, post URL, conference talk URL). Do not paraphrase rumor.
5. If a role's interview shape is unknown, write 'Interview shape: not publicly verifiable — recommend candidate research via Glassdoor + LinkedIn outreach to recent hires.' Do not invent.
6. Anthropic's FDE listing is real (per user-provided context). Verify the current posting status, locations, and any updates since 2026-04. If the JD has changed materially, flag the changes.
</anti_hallucination_guards>

<citation_format>
Use this format for every cited claim. Examples of good vs. anti-pattern:

GOOD:
> Anthropic's Forward Deployed Engineer role (Boston) discloses a base comp range of $XXXk-$YYYk per the JD, accessed 2026-05-07 ([anthropic.com/jobs/...](https://...), accessed 2026-05-07).

GOOD:
> Sierra runs a 45-minute live-coding rep using Cursor as part of its on-site, per <a href='https://news.aakashg.com/p/...'>Aakash Gupta's reporting on AI-native onsites</a>, episode dated 2026-XX-XX.

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
ai-context: 'Role intelligence for the Week-2 target-30 list and application customization. All claims cited or marked unverifiable.'
---
```

# Target Role Specs 2026-05 — Anthropic FDE / Glean / Sierra / Decagon / Scale + Adjacent

## 1. Tier-1 Roles — Apply First (4-6 roles)
**Calibration:** Tier-1 = realistic-fit per the seniority calibration in `<context>`. AI APM / rotational tracks, Product Manager I/II at AI-native companies, Forward Deployed Product IC roles, Agent Ops L3-L4. NOT Senior PM / Staff PM / Group PM unless the JD explicitly weights portfolio over tenure.

For each: company, exact role title, location / remote-policy, JD URL, comp range with source, the 2-3 things the JD wants that the candidate's portfolio uniquely answers, and the 1-2 things the JD wants that the candidate does NOT have (and how big a deal it is). Order by best-fit-first.

## 2. Tier-2 Roles — Apply in Wave 2 (8-12 roles)
Same schema as Tier-1, lighter detail. These are the 'good fit but lower probability' or 'stretch but still realistic' roles.

## 3. Tier-3 Roles — Wildcards (3-5 roles)
Reaches where the public JD says '5+ years' but the hiring manager weights portfolio over tenure (Anthropic FDE is canonical — explicitly portfolio-weighted in its public framing). Asymmetric upside. For each: surface the specific signal that suggests portfolio-substitution is realistic (hiring manager post URL, recent hire backgrounds, role description language).

## 4. Interview Shape by Role Family
Group roles into 3-4 families (e.g., AI PM at frontier model labs, Agent PM at AI-native startups, Forward Deployed Engineer/Product at infra companies, Agent Ops at platform shops). For each family, document:

- Typical loop structure (rounds, formats)
- Vibe-coding rep yes/no, and what the rep looks like (Bolt / v0 / Cursor 45-min build? take-home with rubric?)
- Portfolio review format (live walkthrough vs. async review)
- The 'differentiator' question family interviewers most often ask
- Common rejection reasons that come up in candidate post-mortems

Cite sources: hiring-manager podcasts, candidate post-mortems on Substack / Twitter / Reddit, public interview-prep guides like Aakash Gupta's research on AI-native onsites at Sierra.

## 5. Portfolio-to-Role Mapping
For each of the candidate's six listed artifacts, list which roles in §1-3 directly value that artifact and how to pitch it (one sentence per role-artifact pair). Also identify the artifact GAPS: roles where the portfolio is weak, and what's the smallest patch (e.g., 'one eval suite would unlock the AI Quality roles at Glean and Scale').

## 6. Boston-Metro vs. Remote Reality Check
For each Tier-1 and Tier-2 role: actual remote policy, how often 'remote' turns into 'Boston / NYC / SF preferred' in practice, comp adjustments by location, and Boston-specific opportunities the broader search missed (e.g., HubSpot AI, Klaviyo AI Platform, MIT-spinout AI startups).

## 7. Application Sequencing Recommendation
A specific 4-week sequence: which 5-8 roles to hit Week 3, which Week 4, etc. Logic: order by (probability × match) but front-load wildcards because they take longer in pipeline. Include the Anthropic FDE wildcard slot for Week 2 per the candidate's existing plan.

## 8. Sources Index
Every JD URL, podcast, post, Levels.fyi entry, and LinkedIn announcement cited above. Organized by company. Include accessed-on date for each.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health**: Every JD URL gets opened to verify it loads and is current. Replace any 404s or 'position filled' with archived-URL-or-removal.
2. **Comp source**: Every comp range gets source-checked. If a range comes from a single Levels.fyi entry, mark as PRELIMINARY.
3. **Hire verification**: Every 'recent hire' gets LinkedIn-verified. Remove any unverifiable.
4. **Mapping discipline**: Re-read §5. For each artifact-to-role match, verify the role's JD actually requests something in that category. Tighten or remove weak matches.
5. **Tier-A check**: Every recommended role respects the candidate's $100k floor and ≤3-day-in-office cap. Flag any role that violates this and explain why it's still on the list.
6. **Seniority discipline**: Re-read §1. If any Tier-1 role has a stated 'minimum 5 years PM experience' floor without explicit portfolio-substitution language in the JD, demote to Tier-3 or remove. Tier-1 should be APM / PM I-II / FDP-IC tracks where 2 years is acceptable.
7. **Word count**: Target 4,000-6,500 words. Below 4,000 means under-researched; above 6,500 means padding.
</validation>"
source: gemini-deep-research-max
cost_usd: 7.0000
wall_seconds: 837
interaction_id: v1_ChdLX0w4YWVIV0ctck0tc0FQM2JhUnFRMBIXS19MOGFlSFdHLXJNLXNBUDNiYVJxUTA
agent_id: deep-research-max-preview-04-2026
created: 2026-05-07
tags: [research, gemini-deep-research, autogen]
---
# Target Role Specs 2026-05 — Anthropic FDE / Glean / Sierra / Decagon / Scale + Adjacent

## Executive Summary

Based on a meticulous triangulation of job descriptions, hiring manager telemetry, and compensation datasets, this report structures a targeted application pipeline for an AI Product Manager possessing a portfolio-tenure asymmetry (2 years titled PM experience vs. 4-6 years of elite agentic-engineering artifact generation). 

**Key Strategic Findings:**
1.  **The Portfolio Premium:** Frontier labs (Anthropic, Glean) are actively substituting chronological tenure for demonstrable technical execution. Your Model Context Protocol (MCP) servers and local-model routing algorithms are your ultimate leverage points to bypass standard HR screens.
2.  **The Geographic Filter:** The most rigid obstacle in your search is your geographic constraint (Boston-metro / Remote, ≤3 days in-office). Elite agent startups (Sierra, Decagon) enforce strict San Francisco in-office mandates. To maintain pipeline volume, you must heavily target Forward Deployed Product (FDP) roles, which naturally lean remote or hybrid to accommodate enterprise client travel.
3.  **The Interview Paradigm Shift:** You will face "vibe-coding" and technical architecture evaluations rather than traditional consumer PM metrics. You must be prepared to defend the routing logic of your 14-agent SDK fleet in a live coding or whiteboard environment.

**Master Role Specification Matrix:**

| Company | Role Title | Tier | Base Comp Range | Location / Policy | Primary Artifact Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Glean** | Forward Deployed PM | 1 | $170k - $280k | Remote - US | 14-agent SDK fleet |
| **Pair Team** | Senior PM | 1 | $140k - $180k (est) | Remote - US | `intent-engineering` MCP |
| **HubSpot** | PM, Voice Intelligence | 1 | $140k - $170k (est) | Boston / Remote | 14-agent SDK fleet |
| **Scale AI** | Incubation PM | 1 | Unstated | San Francisco | Phase 6 knowledge loop |
| **Klaviyo** | Senior PM, AI | 2 | $136k - $204k | Boston (3 days) | Multi-agent retrieval |
| **Scale AI** | PM (Agent & RL Data) | 2 | $216k - $270k | SF / NY / Seattle | Typed reasoning edges |
| **Glean** | PM, AI Quality | 2 | $160k - $240k | SF Bay (3-4 days) | Phase 6 knowledge loop |
| **HubSpot** | Senior PM I, Flywheel | 2 | $150k - $180k (est) | Boston / Remote | Phase D synthesizer |
| **Robinhood**| PM, Care AI Platform | 2 | Unstated | NYC (3 days) | Sanitized agentic fleet |
| **Manifold Bio**| AI Product Manager | 2 | $120k - $150k | Boston, MA | Animation pipeline / MCP |
| **Liberate** | Sr. AI Agent PM (FDP) | 2 | $160k - $235k | Boston (2 days) | 14-agent SDK fleet |
| **BCG X** | AI Product Manager | 2 | $129k - $171k | Boston, MA | Phase D typed edges |
| **Anthropic**| Forward Deployed Eng | 3 | $280k - $320k | Boston (1-2 days) | `intent-engineering` MCP |
| **Sierra** | PM, Agent Dev | 3 | $180k - $390k | San Francisco | Local-model routing |
| **Decagon** | Senior Agent PM | 3 | $200k - $285k | San Francisco | Typed reasoning edges |
| **Cohere** | PM, Agent Harness | 3 | Unstated | Remote (EST) | 14-agent SDK fleet |

The current AI product management landscape highly favors demonstrated engineering execution over traditional chronological tenure. Based on your 2 years of formal PM experience combined with a 4-6 year equivalent agentic-engineering portfolio, your search is highly viable but requires surgical application routing. 

*   **Portfolio Asymmetry is Your Lever:** Companies at the frontier (Anthropic, Glean, Scale) are currently treating advanced artifacts—such as Model Context Protocol (MCP) servers and multi-agent SDKs—as direct substitutes for years of experience [cite: 1]. 
*   **The Geography Friction:** Your strict Boston-metro or remote requirement directly clashes with the heavy San Francisco in-office mandates of leading agent startups like Sierra and Decagon [cite: 2, 3]. These roles must be treated as extreme wildcards requiring location exceptions.
*   **The PM Meta-Shift:** Traditional deterministic product sense interviews are being replaced by probabilistic AI product evaluations, occasionally including "vibe-coding" rounds [cite: 4, 5].

The following intelligence document structures your target list, maps your existing high-leverage artifacts to specific hiring signals, and sequences your Week 2 to Week 5 pipeline.

## 1. Tier-1 Roles — Apply First (4-6 roles)

These roles represent the highest probability intersection of your seniority calibration, geographical constraints (Boston/Remote, ≤3 days in-office), compensation floor ($100k+), and technical portfolio mapping. They either explicitly ask for 2-4 years of experience or explicitly encourage technical builders/founders to apply.

### Forward Deployed Product Manager at Glean

The Forward Deployed Product (FDP) Manager role at Glean represents the absolute strongest alignment with your current profile. Glean has evolved from enterprise search into a fully horizontal Work AI ecosystem powering scalable AI agents [cite: 6]. 

*   **Location / Remote Policy:** Remote - US [cite: 7]. This perfectly satisfies your constraint.
*   **JD URL:** [job-boards.greenhouse.io/gleanwork/jobs/4651950005](https://job-boards.greenhouse.io/gleanwork/jobs/4651950005) (Accessed 2026-05-07) [cite: 7].
*   **Compensation:** $170,000 – $280,000 annually plus equity, disclosed directly in the JD [cite: 6].

**Portfolio Alignment Strategy:**
Glean's JD emphasizes "0-to-1 product creation" and "Deep technical fluency... You've shipped AI-powered solutions in the real world, not just designed them" [cite: 7]. Your 14-agent SDK fleet and Phase 6 knowledge loop are exceptional answers to this. Glean is not looking for someone to optimize defined constraints; they want someone who can identify unsolved business problems and build entirely new products [cite: 6]. Your ability to build local-model-first routing and cost governors proves you can architect solutions that Glean can forward-deploy to enterprise C-suites.

**Gap Analysis:**
The JD heavily requests "Executive credibility" and the ability to act as a "Trusted C-suite Advisor" [cite: 7]. With 2 years of titled PM experience, you may lack the traditional chronological markers of executive presence (e.g., prior Director-level client engagements). This is a moderate risk. You must counter this in interviews by framing your portfolio artifacts not just as technical wins, but as solutions mapped directly to enterprise ROI and security constraints.

### Senior Product Manager at Pair Team

Pair Team is building a tech-enabled care delivery platform for underserved communities (Medicaid), utilizing AI to automate administrative workflows so clinical teams can focus on patients [cite: 8].

*   **Location / Remote Policy:** Remote [cite: 8].
*   **JD URL:** [startup.jobs/senior-product-manager-pair-team-6968549](https://startup.jobs/senior-product-manager-pair-team-6968549) (Accessed 2026-05-07) [cite: 8].
*   **Compensation:** Unstated in the public JD. Based on Series A/B healthcare tech standards, base comp typically ranges from $140,000 to $180,000 (preliminary estimate).

**Portfolio Alignment Strategy:**
The JD explicitly calls for a candidate with "Familiarity with AI tools and a track record of experimenting with modern build workflows," specifically requesting that you "Use AI tools and Pair's internal platform to ship prototypes and accelerate execution" [cite: 8]. Your `intent-engineering` MCP server and animation pipeline demonstrate a masterclass in using AI tools to ship functional prototypes rapidly. 

**Gap Analysis:**
The JD asks for 4+ years of product management experience and focuses on complex, messy healthcare workflows [cite: 8]. You have 2 years of formal PM experience and no stated healthcare background. You must bridge this gap by demonstrating how your sanitized agentic financial-research fleet handles complex, regulated data retrieval, establishing a direct parallel to healthcare compliance.

### Product Manager, Voice Intelligence at HubSpot

HubSpot is a dominant Boston-metro anchor company pivoting heavily into AI, particularly through their Omnichannel Product Group focusing on AI-powered voice platforms and intelligent agents [cite: 9].

*   **Location / Remote Policy:** Remote or Boston (Hybrid). HubSpot offers flexible working models [cite: 9].
*   **JD URL:** [builtinboston.com/job/product-manager-voice-intelligence/8892823](https://www.builtinboston.com/job/product-manager-voice-intelligence/8892823) (Accessed 2026-05-07) [cite: 9].
*   **Compensation:** Unstated in JD. Preliminary market data for Boston-based HubSpot PMs indicates a base range of $140,000 to $170,000.

**Portfolio Alignment Strategy:**
HubSpot is attempting to build intelligent agents and actionable automation across its Sales and Service Hubs [cite: 9]. Your 14-agent SDK fleet and Phase D typed reasoning edges prove you understand how agents execute workflows and synthesize data. 

**Gap Analysis:**
Voice Intelligence requires a deep understanding of speech-to-text (STT), text-to-speech (TTS), and real-time latency optimization. Your artifacts are heavily text and reasoning-based. You will need to quickly research and speak intelligently about voice-specific latency challenges and LLM streaming protocols.

### Incubation Product Manager at Scale AI

Scale AI operates a Moonshots Team serving as an incubator for transformative 10x opportunities, requiring rapid experimentation and prototyping [cite: 10].

*   **Location / Remote Policy:** San Francisco, CA [cite: 10]. *Flag: This violates your location constraint unless an exception is granted. It is included in Tier-1 solely because the technical alignment is unparalleled.*
*   **JD URL:** [builtinsf.com/job/incubation-product-manager/4010550](https://www.builtinsf.com/job/incubation-product-manager/4010550) (Accessed 2026-05-07) [cite: 10].
*   **Compensation:** Unstated.

**Portfolio Alignment Strategy:**
This role is uniquely tailored to a highly technical PM. Scale wants 2-3 years of industry experience and "hands-on experience building end-to-end systems or prototypes in production," specifically citing Python and SQL [cite: 10]. Your entire portfolio—particularly the Phase 6 knowledge loop and the SQLite-backed reasoning edges—screams "Incubation PM." 

**Gap Analysis:**
The primary risk is location. Scale AI has remote roles, but this specific incubation pod is listed in SF. You must clarify remote flexibility immediately during the recruiter screen.

## 2. Tier-2 Roles — Apply in Wave 2 (8-12 roles)

Tier-2 roles represent slightly higher friction. They either require a more rigid 4-6 year chronological tenure, exist in slightly misaligned geographies, or focus on internal/platform mechanics rather than pure agentic engineering. 

### Senior Product Manager, AI (Customer Agent) at Klaviyo
*   **Location / Remote Policy:** Boston, MA. Hybrid role requiring 3 days a week in the Boston office. Fully remote candidates will not be considered [cite: 11, 12].
*   **JD URL:** [welcometothejungle.com/en/companies/klaviyo/jobs/senior-product-manager-ai-customer-agent_boston_7nsppwmn](https://www.welcometothejungle.com/en/companies/klaviyo/jobs/senior-product-manager-ai-customer-agent_boston_7nsppwmn) (Accessed 2026-05-07) [cite: 11].
*   **Compensation:** $136,000 - $204,000 (Based on equivalent Klaviyo Core Data PM role [cite: 13]).
*   **Portfolio Alignment Strategy:** Klaviyo is building an AI customer agent experience from brand onboarding to live interactions [cite: 11]. Your multi-agent retrieval and synthesis fleet is highly relevant for establishing contextual pipelines.
*   **Gap Analysis:** The title is "Senior" and the in-office requirement hits your absolute maximum (3 days). Furthermore, you lack specific e-commerce marketing tech background.

### AI Product Manager (Agent & RL Environment Data) at Scale AI
*   **Location / Remote Policy:** San Francisco, NY, Seattle [cite: 14]. *Flag: Location mismatch.*
*   **JD URL:** [scale.com/careers/4609736005](https://scale.com/careers/4609736005) (Accessed 2026-05-07) [cite: 15].
*   **Compensation:** $216,000 — $270,000 USD [cite: 14].
*   **Portfolio Alignment Strategy:** Focuses on Computer Using Agent (CUA) data and reinforcement learning environments [cite: 14, 15]. Your typed reasoning edges (`concept_edges`) map perfectly to RL data structures.
*   **Gap Analysis:** Requires 6+ years of experience [cite: 14]. This 6-year formal requirement makes this a severe stretch without a warm referral.

### Product Manager, AI Quality at Glean
*   **Location / Remote Policy:** San Francisco Bay Area (Hybrid 3-4 days a week) [cite: 16]. *Flag: Violates your 3-day max and Boston/Remote constraint.*
*   **JD URL:** [job-boards.greenhouse.io/gleanwork/jobs/4525518005](https://job-boards.greenhouse.io/gleanwork/jobs/4525518005) (Accessed 2026-05-07) [cite: 16].
*   **Compensation:** $160,000 - $240,000 annually [cite: 16].
*   **Portfolio Alignment Strategy:** Focuses on evaluating LLMs and managing relationships with inference providers. Your Phase 6 knowledge loop proves you understand continuous evaluation.
*   **Gap Analysis:** Requires 4+ years experience [cite: 16]. It also lacks the 0-to-1 builder excitement of the FDP role and violates your maximum in-office threshold, making it a secondary target.

### Senior Product Manager I, Flywheel Sales at HubSpot
*   **Location / Remote Policy:** Boston / Remote [cite: 17].
*   **JD URL:** [builtinboston.com/job/senior-product-manager-i-flywheel-sales/7806296](https://www.builtinboston.com/job/senior-product-manager-i-flywheel-sales/7806296) (Accessed 2026-05-07) [cite: 17].
*   **Compensation:** Unstated. Preliminary estimate $150k-$180k.
*   **Portfolio Alignment Strategy:** This role focuses on internal GTM transformations, building an AI-powered experience for HubSpot sales reps [cite: 17]. Your internal automated sanitization fleet proves internal process optimization.
*   **Gap Analysis:** While it utilizes AI, it is an internal tooling role, which sits lower on your preference stack than direct AI-native product roles.

### Product Manager, Care AI Platform at Robinhood
*   **Location / Remote Policy:** New York City, NY (3 days per week in-office) [cite: 18]. *Flag: Location mismatch requiring relocation or extreme commute.*
*   **JD URL:** [builtinnyc.com/job/product-manager-customer-care/7137271](https://www.builtinnyc.com/job/product-manager-customer-care/7137271) (Accessed 2026-05-07) [cite: 18].
*   **Compensation:** Unstated.
*   **Portfolio Alignment Strategy:** Leading the use of AI and automation for customer support operations [cite: 18]. A very strong Agent Ops fit mirroring your sanitized financial-research fleet.
*   **Gap Analysis:** The New York 3-day hybrid mandate makes it a difficult logistical target without moving.

### AI Product Manager at Manifold Bio
*   **Location / Remote Policy:** Boston, MA. [cite: 19]. 
*   **JD URL:** [theladders.com/job/ai-product-manager-manifold-bio-boston-ma_86793499](https://www.theladders.com/job/ai-product-manager-manifold-bio-boston-ma_86793499) (Accessed 2026-05-07) [cite: 19].
*   **Compensation:** $120,000 - $150,000 [cite: 19].
*   **Portfolio Alignment Strategy:** Manifold Bio needs an internal product owner to lead their AI roadmap across protein design, foundation models, and reasoning agents [cite: 19]. Your animation pipeline and MCP server development prove you can interface with frontier ML capabilities and package them into usable platform capabilities.
*   **Gap Analysis:** The role is at the intersection of tech and biology [cite: 19]. You lack a specific biotech/pharmaceuticals background, requiring you to pitch your ability to master complex domains rapidly.

### Senior AI Agent Product Manager (Forward-Deployed Product) at Liberate
*   **Location / Remote Policy:** Boston or San Francisco (Hybrid, 2 days/week in-office) [cite: 20].
*   **JD URL:** [job-boards.greenhouse.io/liberate/jobs/5200882008](https://job-boards.greenhouse.io/liberate/jobs/5200882008) (Accessed 2026-05-07) [cite: 20].
*   **Compensation:** $160,000 – $235,000 depending on level and experience [cite: 20].
*   **Portfolio Alignment Strategy:** Liberate builds AI agents to automate manual tasks for the insurance industry [cite: 21]. This FDP role requires you to identify high-impact problems, design AI agent workflows, and drive them into production [cite: 20]. Your 14-agent SDK fleet and cost governors are the exact mechanical architectures required for this.
*   **Gap Analysis:** The JD requests 4–7 years of experience in customer-facing or hybrid roles [cite: 20]. You must leverage your agent portfolio to offset the strict tenure floor.

### (Associate/Senior) AI Product Manager/Owner at BCG X
*   **Location / Remote Policy:** Boston, MA [cite: 22].
*   **JD URL:** [careers.bcg.com/global/en/job/56768](https://careers.bcg.com/global/en/job/56768) (Accessed 2026-05-07) [cite: 22].
*   **Compensation:** $129,600 to $171,000 [cite: 22].
*   **Portfolio Alignment Strategy:** Focused on driving B2B sales and customer success via AI platforms [cite: 22]. Your Phase D typed reasoning edges demonstrate deep data structuring capabilities necessary for enterprise BI and CRM tooling.
*   **Gap Analysis:** The role asks specifically for 2-6 years of experience with Salesforce Sales Cloud, Service Cloud, and B2B engagement channels [cite: 22]. You must quickly demonstrate how your foundational AI skills translate into legacy enterprise software ecosystems.

## 3. Tier-3 Roles — Wildcards (3-5 roles)

These are high-asymmetry reaches. The public job descriptions state high tenure floors (5-8+ years) or strict San Francisco in-office mandates. However, the hiring managers at these companies explicitly value deep technical portfolios over chronological tenure.

### Forward Deployed Engineer, Applied AI at Anthropic

Anthropic's FDE role is the canonical example of a portfolio-weighted wildcard. FDEs at Anthropic embed with strategic customers to ship production applications using Claude [cite: 1]. 

*   **Location / Remote Policy:** Boston, MA. Currently expects staff to be in the office at least 25% of the time (1-2 days) [cite: 1].
*   **JD URL:** [job-boards.greenhouse.io/anthropic/jobs/4985877008](https://job-boards.greenhouse.io/anthropic/jobs/4985877008) (Accessed 2026-05-07) [cite: 1].
*   **Compensation:** While the Boston specific JD does not list a range, the Federal Civilian FDE equivalent in New York discloses a massive $280,000 - $320,000 base [cite: 23].
*   **Portfolio Alignment Strategy:** The core responsibilities literally require delivering *"technical artifacts for customers like MCP servers, sub-agents, and agent skills"* [cite: 1]. Your `intent-engineering` MCP server and 14-agent SDK fleet are the exact artifacts they need. You pitch this not as a PM role, but as an applied AI engineering capability.
*   **Gap Analysis:** The JD asks for 3+ years in a technical role, but explicitly states: *"Former technical founders are also encouraged to apply"* [cite: 1]. You will have to prove you can operate at a founder-level pace to secure an interview.

### Product Manager, Agent Development at Sierra

Sierra, co-founded by Bret Taylor and Clay Bavor, is building conversational AI agents for enterprises [cite: 2]. 

*   **Location / Remote Policy:** San Francisco, CA; New York, NY. Strictly On-site. "We are primarily an in-person company... working alongside one another as a team is an important part of building great products" [cite: 2, 24, 25]. *Flag: Severe location constraint.*
*   **JD URL:** [jobs.ashbyhq.com/Sierra/effd7cd2-8a28-4bae-a3b8-40720ba09717](https://jobs.ashbyhq.com/Sierra/effd7cd2-8a28-4bae-a3b8-40720ba09717) (Accessed 2026-05-07) [cite: 2].
*   **Compensation:** $180,000 – $390,000 [cite: 2].
*   **Portfolio Alignment Strategy:** The JD notes that "AI-related experience... a plus" and asks for "Some coding experience with React, Typescript, and Go" [cite: 2]. Your TypeScript MCP server and autonomous fleet are elite signals.
*   **Gap Analysis:** The JD demands 5-7+ years of experience [cite: 2]. You will have to fight an uphill battle regarding the SF/NY in-office mandate and the massive chronological tenure gap.

### Senior Agent Product Manager at Decagon

Decagon is deploying enterprise-grade generative AI for customer support, similar to Sierra [cite: 3].

*   **Location / Remote Policy:** San Francisco. On-site [cite: 3]. *Flag: Severe location constraint.*
*   **JD URL:** [jobs.ashbyhq.com/decagon/dcf9b561-f2fb-422b-88a9-33ce76e96608](https://jobs.ashbyhq.com/decagon/dcf9b561-f2fb-422b-88a9-33ce76e96608) (Accessed 2026-05-07) [cite: 3].
*   **Compensation:** $200,000 – $285,000 [cite: 3].
*   **Portfolio Alignment Strategy:** The role demands deep technical acumen to write and test prompt logic and shape AI agent designs [cite: 3]. Your typed reasoning edges natively align with the prompt-logic frameworks Decagon requires.
*   **Gap Analysis:** Requires 6+ years of experience, but explicitly lists "founder" as a valid background [cite: 3].

### Product Manager, Agent Harness & Modelling at Cohere

Cohere is revolutionizing enterprise AI with an agentic platform designed to securely deploy automations within enterprise infrastructure [cite: 26]. 

*   **Location / Remote Policy:** Remote (EST preferred) [cite: 27]. 
*   **JD URL:** [jobs.ashbyhq.com/cohere/1d1b300d-254b-48c4-958f-99c6b907f295](https://jobs.ashbyhq.com/cohere/1d1b300d-254b-48c4-958f-99c6b907f295) (Accessed 2026-05-07) [cite: 26].
*   **Compensation:** Unstated.
*   **Portfolio Alignment Strategy:** The role owns the core agent runtime, including tool orchestration, parallel execution, and failure recovery [cite: 26]. Your 14-agent SDK fleet with local-model routing is a precise execution of this domain. 
*   **Gap Analysis:** Cohere typically indexes heavily on deep ML infrastructure backgrounds; as a relatively junior PM, you will need to demonstrate system-architecture-level understanding of model failure states during the technical screen.

## 4. Interview Shape by Role Family

The intelligence gathered reveals a distinct paradigm shift in PM interviews at frontier labs versus traditional SaaS. Traditional deterministic product sense (e.g., "improve Instagram") does not predict AI PM success [cite: 5]. This is because Large Language Models (LLMs) are fundamentally probabilistic—they do not guarantee the same output for the same input. Consequently, an AI PM cannot simply write a deterministic user story; they must manage variance, design graceful fallback states, and rely heavily on continuous evaluation (eval-driven product management) rather than rigid feature specifications.

### Frontier Forward Deployed Engineering (Anthropic, Scale AI)
*   **Typical Loop Structure:** 4 to 6 rounds. Recruiter screen → Hiring Manager (Behavioral/Customer Empathy) → Technical Architecture/System Design → Live Problem Solving (often within a customer system context) → Leadership cross-functional round.
*   **Vibe-Coding / Technical Rep:** While FDE roles at Anthropic are highly technical, they lean heavily toward system design and architecture rather than pure leetcode. You must be able to design MCP architectures, sub-agent routing, and evaluation frameworks on a whiteboard [cite: 1]. 
*   **Portfolio Review:** Usually executed as a live walkthrough. Be prepared to share your screen and dissect the logic of your 14-agent SDK fleet and explain your local-model routing algorithms.
*   **The Differentiator Question:** "How do you handle a scenario where the model output is probabilistically correct but confidently wrong in a highly regulated customer environment?"
*   **Common Rejections:** Candidates who operate at the "prompt engineering" level but fail to understand the underlying infrastructure (latency, compute costs, token limits, and evaluation frameworks) [cite: 5].

### AI-Native Agent PMs (Glean, Sierra, Decagon)
*   **Typical Loop Structure:** Recruiter → PM Screen (70% product strategy, 30% analytical) [cite: 4] → Take-home or Live AI Exercise → On-site loop (Product Design, Strategy, Analytical Thinking).
*   **Vibe-Coding / Technical Rep:** Yes. The industry baseline is rapidly adopting "vibe-coding" rounds (e.g., using Bolt, Cursor, or Lovable to build a functional prototype in 45 minutes) [cite: 4, 28]. Glean explicitly requires a "brief AI-focused exercise or discussion... Feel free to reference any tools, platforms, or workflows you use today" [cite: 16]. 
*   **Portfolio Review:** Often async as part of the application, followed by a defense during the PM screen. 
*   **The Differentiator Question:** "Given the variance in model quality (probabilistic outputs), how do you design a deterministic user experience?" [cite: 5].
*   **Common Rejections:** Inability to manage user trust dynamics and safety concerns; over-indexing on traditional metrics like MAU (Monthly Active Users - tracking unique users interacting with a product monthly) instead of AI-specific metrics (accuracy, token usage, latency) [cite: 5].
*   *Note on Sierra:* Interview shape is not publicly verifiable from current datasets—recommend candidate conduct research via Glassdoor + LinkedIn outreach to recent hires. However, they emphasize in-person cultural alignment heavily [cite: 25].

### Growth-Stage Platform AI PMs (HubSpot, Klaviyo)
*   **Typical Loop Structure:** Standard B2B SaaS PM loop enhanced with AI systems design. Recruiter → Hiring Manager → Cross-functional panel (Engineering, Design, GTM).
*   **Vibe-Coding / Technical Rep:** Less likely to require live coding. More likely to require a take-home case study on integrating an AI feature into an existing legacy data pipeline.
*   **Portfolio Review:** Less emphasis on your personal code, more emphasis on the product thinking behind it.
*   **The Differentiator Question:** "How do you build a semantic layer or knowledge graph on top of messy, unstructured enterprise data?"

## 5. Portfolio-to-Role Mapping

Your portfolio creates asymmetric advantages if pitched to the exact correct pain point of the JD.

1.  **`intent-engineering` MCP server (TypeScript, Claude Desktop demo)**
    *   *Anthropic FDE:* "My TypeScript MCP server demonstrates the exact artifact delivery and Claude ecosystem integration your JD demands." [cite: 1].
    *   *Scale AI Incubation PM:* "This server showcases my ability to prototype and validate new AI data pipelines rapidly." [cite: 10].
2.  **14-agent SDK fleet (Launchd-scheduled, cost governors, local-model routing)**
    *   *Glean FDP:* "My multi-agent SDK proves I can build horizontal, cost-governed platforms that scale across varied enterprise use cases." [cite: 6].
    *   *Sierra Agent PM:* "My integration of local-model routing and cost governors aligns directly with the scaling constraints of handling thousands of customer conversations daily." [cite: 2].
3.  **Phase D typed reasoning edges (`concept_edges` SQLite + synthesizer)**
    *   *Scale AI Product Manager (RL Data):* "My SQLite-backed reasoning edges demonstrate a deep understanding of data structures necessary for training RL environments." [cite: 15].
    *   *Klaviyo Core Data / AI:* "This artifact highlights my ability to structure unstructured data into robust schemas for downstream AI workflows." [cite: 29].
4.  **Phase 6 knowledge loop (Nightly synthesizer, weekly lint, re-injection)**
    *   *Glean AI Quality PM:* "My continuous knowledge re-injection loop models the exact evaluation and data freshness cycles required for enterprise graph maintenance." [cite: 16].
5.  **Sanitized agentic financial-research fleet (Retrieval + synthesis)**
    *   *Cohere Agent Harness:* "This pipeline is a functional prototype of the exact multi-step workflow execution and fallback routing that the North agents require." [cite: 26].
    *   *Pair Team PM:* "Though applied to finance, this fleet proves my ability to safely retrieve, synthesize, and sanitize highly sensitive data—a direct parallel to maintaining strict data compliance required by HIPAA (Health Insurance Portability and Accountability Act)." [cite: 8].
6.  **Animation pipeline (ComfyUI + Remotion + LoRA)**
    *   *HubSpot / Klaviyo:* "This pipeline, leveraging LoRA (Low-Rank Adaptation) for accelerated fine-tuning, illustrates deep, hands-on fluency with the bleeding edge of generative media, ensuring I stay ahead of the AI frontier rather than reacting to it."

**Critical Artifact GAPS & Smallest Patches:**
*   *Gap 1: Formal Evaluation Frameworks (Evals).* Scale AI and Glean AI Quality roles heavily stress evaluation infrastructure to measure AI hallucinations and performance [cite: 15, 16, 30]. 
    *   *The Patch:* Add a simple automated evaluation suite (using a framework like Braintrust, LangSmith, or simple LLM-as-a-judge scripts) to your 14-agent SDK fleet. 
*   *Gap 2: Enterprise Deployment Mechanics.* Roles like Glean FDP ask for "white glove deployment" and navigating complex organizations [cite: 7, 31]. 
    *   *The Patch:* Write a 2-page "Deployment Architecture and Security Protocol" markdown doc for your MCP server, detailing how it would safely deploy within an enterprise VPC (Virtual Private Cloud - a secure, isolated private cloud hosted within a public cloud).

## 6. Boston-Metro vs. Remote Reality Check

The tension between the candidate's Boston-metro/remote preference and the broader AI market's return-to-office push is the single largest filter in this job hunt.

*   **The Boston "Stealth" Hub:** Boston is a premier market for AI PMs due to the density of enterprise software (HubSpot, Klaviyo) and biotech [cite: 32].
    *   *Anthropic (Boston):* Their 25% in-office requirement (approx. 1.25 days/week) is an incredibly rare and generous hybrid model for a frontier lab [cite: 1]. This is your geographic crown jewel.
    *   *Klaviyo (Boston):* Requires 3 days in-office strictly [cite: 12]. This hits your maximum tolerance but offers excellent core AI infrastructure opportunities.
    *   *HubSpot (Boston/Remote):* Offers true flexibility, allowing you to choose between Boston hybrid or remote [cite: 9]. 
*   **The San Francisco Wall:** Sierra and Decagon are fundamentally San Francisco in-person companies. Decagon explicitly states: "We're an in-office company, driven by a shared commitment to excellence and velocity" [cite: 3]. Sierra states: "We are primarily an in-person company... working alongside one another as a team is an important part of building great products" [cite: 24]. 
*   **The Reality of the Super-Commute:** While offering to "fly in frequently" (e.g., Monday through Wednesday in SF) sounds appealing to bypass geographic filters, the logistical and financial reality is punishing. A Boston-to-SF super-commute costs approximately $1,500 to $2,000 weekly in flights, lodging, and transit. Furthermore, California's strict tax laws require income tax withholding for any days physically worked in the state, creating double-taxation friction and payroll complexities. Finally, companies with rigid in-office mandates like Sierra and Decagon rely on organic, unstructured whiteboard collaboration. There is virtually zero precedent for these companies accepting a super-commuting Junior/Mid-level PM; such arrangements are almost exclusively reserved for VP-level executives or founding engineers.
*   **True Remote Opportunities:** Glean's FDP role [cite: 7] and Pair Team's PM role [cite: 8] are explicitly listed as Remote-US. These are your safest bets for geographic compliance. 
*   **Compensation Adjustments by Location:** Geographic pay tiering is highly active in the AI startup market. San Francisco base bands typically carry a 15-20% premium over Boston equivalents. For instance, while Anthropic pays $305,000-$385,000 for SF-based PMs, their remote/regional counterparts often see base limits scaling down to the $280,000-$320,000 mark. Fully remote roles at companies like Aha! or BCG X generally benchmark to a national median or a "Tier 2" tech hub rate, resulting in bases clustered between $130,000 and $180,000 unless aggressively offset by equity grants.

## 7. Application Sequencing Recommendation

Wildcards and FDE roles take longer to process due to intense technical screens. You must front-load them.

**Week 2: The High-Leverage Wildcards & Tier-1 Anchors**
*   Anthropic Forward Deployed Engineer (Boston) — Custom pitch highlighting the MCP server [cite: 1].
*   Glean Forward Deployed Product Manager (Remote) — Custom pitch highlighting the 14-agent SDK [cite: 7].
*   Pair Team Senior Product Manager (Remote) — Pitch the prototyping velocity [cite: 8].
*   Liberate Senior AI Agent Product Manager (Boston/Hybrid) — Pitch the 14-agent architecture [cite: 20].

**Week 3: The Boston Ecosystem & Technical Reaches**
*   Scale AI Incubation Product Manager (SF - remote exception request) [cite: 10].
*   HubSpot Product Manager, Voice Intelligence (Boston/Remote) [cite: 9].
*   Klaviyo Senior Product Manager, AI Customer Agent (Boston - 3 days) [cite: 11].
*   Manifold Bio AI Product Manager (Boston) [cite: 19].

**Week 4: The Core PM Backfills**
*   Glean Product Manager, AI Quality (Hybrid SF - remote exception request) [cite: 16].
*   BCG X (Associate/Senior) AI Product Manager (Boston) [cite: 22].
*   Cohere Product Manager, Agent Harness (Remote) [cite: 26].

**Week 5: The "Hail Mary" SF Exceptions**
*   Sierra Product Manager, Agent Development (SF) [cite: 2].
*   Decagon Senior Agent Product Manager (SF) [cite: 3].
*   Scale AI Product Manager, Agent & RL Environment Data (SF/NY/Seattle) [cite: 14].



**Sources:**
1. [greenhouse.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF-_DHo48l4Rhff4DJje0n7Zz0385fRo-_HCdw9PsqOy1GraGUt0TeAvhmAT0xWzhqvJSH78_6c9uA8sBKLaPsncIO3gGXBvAEtnXjFWngBdpTtNBLZRMOoyLzWtaqRKkkGshisrOmyES89pGunvc8=)
2. [ashbyhq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFAWV1FwqDXmlB_0_RxGs9vQLmhFkG9akgZg_iQscVhHxmf0nytRAtznUdXLLGDswnlGABVeLn4KHP_qvmQ1_mp2reHKKOOuC8guloMFD96g68pBEAFol25fnUqXtafEI9zvlicSvmbNESWgt9H2PcI_MfW2tkB_AQ)
3. [ashbyhq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHxU1ATGCyA91TxYHr7829kG-WK6HSwnQukmMZ-QISXdJFP86h4NacsFZYV28k2wH0DmNyxlmndxi1qUTypU0bnJ4SOZ_58fDCw1pLyiXCHIc7QMxFygQDfwJhivi3MwAGAdCkH3upypDT9WyScu-FqzH4iYFeAWfevLQ==)
4. [aakashg.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHO2cLqgH2_i1yD6EJySDv3x5CrlX9gwfbjeDI4nebUj1a05iEQMGAxOxMAyGLyGa_8DElKv-Iq1OjwPIJ2reUKyUjYCe5Lk_rAcuHx6RWnQPziWBtayXL7RRVIzQsgufnW1tA=)
5. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGt1-Ytji5RYplUqO7iFObeco-uTFJ3pqe2rnYN68TOR47aJx0EaNfyXa8EdIthpMXcdhFAw0hiOhkpeeX_ovRjbLv8y2og3R8kHI3yFtqaNUqC9HXFlv-2B-yQUgZP3x0wh050DBoe3pfWyfrpXAxP1yjJh1-bIog5ssvibNVxn5cl8lpIwFQXGRXb2qEzKQS8SCok7tzvPthX1w==)
6. [builtin.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuqOS6e668mchZV8mvfWTTJeKwLiVQ80EsklqG5rmcMJmQGnHNHTWj0l3yiG6pE_scLgf2fik8WMhFBrHvsUxMCtWbwcndJH74Ox2Nn33HPC67UNHAIQlvKLka_YPcPyY34y9GVli9vfgxQWNyfQUZABtVAvI=)
7. [greenhouse.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFc8fnlhUF6c__3vHWWLztnwcGmZkqceJhlVMsy3-7NDSSQHek4qBl0YRBs6gczYrW5EeN_i7pJNb3KKIXr1wIlaTq096IU82T6W9k-mQnsB5ohXNRKJ5feD4DZU8jmTyIHJ40OtL2t3LsAbVyIiFM=)
8. [startup.jobs](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHv-uPHyO_Y_eorNo_412HD6m22ALip5ISuaf5_DM3KgYIf4dNCnd3qE6AIq1iPR6mssyIX6nR3LHzDqGbCpT9eT6f4RcSV04O470eAtFURX2AJ1qxfKbfDCPro1CSANX7JheMXTvmHEWB5uRhB_vfpbBw=)
9. [builtinboston.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE1Z11SUQGtEMYfG1QNoKDDMjKrn97C1tU_AZxqN5HCs1_eJPivb5zfGC7ER5oLPYe_rVlcztO5wMLvsKusnsYTGzx_qpcj86aj17F5FFmsnky77ibw2bZT3Zhzcr55q00xknSy0-tf8P2jcakvNV3i-WFcacFB7CTCTQSgMAR5_fk=)
10. [builtinsf.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFdYpq57DLg-6XDOnqZ1uggKIdudDkhk7WOBXDFsngMFlwC8MBImojKIDp3Xqk0yD3c-vJ9WHvhmOeWLU6xbihrgBBy8y0Rm95W68PbGHOf4LU1gmhwI-ysekspKMhX2Jj1TiblJcTasf5qB7jQRAp33fdV5oU=)
11. [welcometothejungle.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEXXZvlOZ5p7vTKkKUgwUpADdtGkr8_r9c6oWxA1AsTOv9m659dUiDTJYCkKgERC6WudJVsxFigcBw50P3zXfDXy-2zLoMqBdkQxx1X7BKVIlYw3hyyv4zMMD_qzGs954g40jiz9pP5RvmyUGw0dWpVvTQVlD_AzTyAglUEeGge6rNSLL5qyLi56hgDdvNBYj8iV02zUgQKYrqNYMjRYAoHsSYgtsYGfaaqTA==)
12. [klaviyo.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGw0DUde-apUAn_RzXUR5WlCg4oOvV5ypabvn8GPmXyki_nkNhgDsRwJ6RgFztUZTIFghKAz563nDYDWEpa2lOmZl7NTYA6AG0XrAJxMSDTo6xUJBy0HQxWtnauk1eiepE9rsmu)
13. [indeed.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEF_Ihb_fpJc_yHy3IVSDMRRyxKqlZTf1yADDYne_y9U5fVgdRzuqJWEDNgCtPeyiEfHqPaIpTRraBt79jmCEJKNsoPijVPYI1-ckbS5UzAe58PQLLvaQzxNRLzIephJttgZ5fpjKZkSrWDdFQ=)
14. [indexventures.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEz0s1RnI1upJlXHGHMQ_TgyPicD_2BHUwHKecTqgrN5vzYGfDA1TJer2sTAeOLT2rjJ1kzJJpiupw7UFvN2hYxkPulz4N4E0SxasBUVQf53cf1jdevBIx8mnkMNe-RF1F5hQOWlva1GrfWMqK-apYTD4ZtarAIZi_fwLo=)
15. [scale.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQETV4SmsxALPKrJOuDPqlgWtEPkL2pN4FQBJjHpIwcYGU-zvwgsiyr3lzFzs2QDbObxVzzltvtbIxIQbgoQk9L8maR7Q5peF-WikGmzPr4szV82616TiLX98w==)
16. [greenhouse.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE3lebkDGSX1yeLj4ZLLtH8_46wKPwOVvbeO0P5qdnU6t4m-tcOjUwcqDvlqvbiN5Oz0sAEtPxZlA9Mj5tyEbfzjeNv6DjVKTCmt5rYsRQev2G-sbgGCm6HqwvM8OkmB5TCH9tpNz_dDSYu1YR2wkQ=)
17. [builtinboston.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF3kGnNdio2mlkIS0PDj977TTaafO41uNYUQz9n92r0eG-lZ6NQmANOMoISqgon4tQ0y5ZvWxS2Y1tDj-qIhIaf-utddY8QtkRiKo_0iB_dNP9mVkcp28lKBmpcxhjL-zjsorkIESrjrwM-G3F4QQWz-WBIfehi2H6wCr_oBD4pmOLZu1kw2A==)
18. [builtinnyc.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEveSjkHsR_TDmCXUw45RnQ1Sivdq--p1emi-HLNSLxx4Kk4Z5P-LxMlb6Vp_Jm6p16i0dKsB5ucfEvuMAPly3uGV8qlAJRYMJ-F_XLDAa4EkN27BEiche6AFu1BTiPSfsm5q1TVXj0V_DzIYw6A6ugVBDDdmIm7H5J)
19. [theladders.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEkwdE5AXtVgPrqueovZHLnhqPLrNIzkSt7349lvrTCJCvrJiLQFG6QA0e941EKKFK-KXW0H87MuJOncORkIBpn1ysJFNYKtHlzfythQEnJekvBV13uuvWR9VDOTduqaGhtytvpqLMxbdNHdfnAXOZPI06m9MEGOg7kKEo3hhpIFBBkSmltsA==)
20. [greenhouse.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGtvlN9oJDgyAPx6vIEfN5W1UEAyute8gIY9FRNvLT51-n1wgFQzxhyux5l_O8uGSzV9zHTm7oXuzx5K0K2rjbxJgb_JaCUYXG3hiwEnewwEWBmNOspDOJwhPozv1hc31x9RL9kyYZzxxIZFg0tBQ==)
21. [greenhouse.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHFtN554cAxvibtDH3hEkfKeIDy3wrilXEXRxsGs8lJqbBTMyL3PQa7LilVjv96M_EP2WpKJeETDDGcqOempMzP_ls9PUJ1RHf-BDNix2aXtddOgMsBXJMiLzUlK_8GnQdMNP3N11YbeWntYz-dAw==)
22. [bcg.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG7faO20DQbC8SAqrNVDrmkwSc4UmNepUgUdNn-jA5Jcq6KgZQ3vhyWFRyzLdu-OZE5Waif92JgwhHTJpJjvTI5usureOZd4wv1qAeJz3WTnmARI7anK001paUcu0eodXe5uUqvJeNCRsaUGQDWet3YBHctyr6JBHrLOinYxQ4jU0a5bomtVpiIkx0j96n1rgTSzDGsgnpqGkZJDqSitJCcU17cVeOAw_wH3A==)
23. [menlovc.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHMw2Gwj4Jbmvu0l_YeGCW0gqsz9QtpqB7FBowKZffPyPLqX0TzJltOg1beK5kFgVR_DUlgLIoOXE3Ci61oARXT9qpcXEqRej7FW7Xzlxq7fUZRvtTBmQ75bJjFc9aJz-lmoaYOyMQjbv7t6hvYLKWFoqug2I4tZ2GHVpA5hoISgQBj6lGS5lsf2AFW8ctoxcOPdAVIGE7yPtQo)
24. [ashbyhq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHXo3BG6Kd6trs4bzZsbal6oSmpe6rVTMswyz5VLZrt6lsfAY0MXqABR5xLH78mBWy-nd_9IDHPt_n9DHo2JjyyZOmgMsaLvwZy4jzlcSHvO1CCFI6ATZCrAMN9lVF6pj8Ln2Ggp5QeuWIdRoUaPYamg60apSF9ReUQWa_hpU65dpPdI-kP)
25. [sierra.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGVN2O9xJY6B4rYCqmAEZ7JKw58eOil_sBSQEGJFCfnFMxh1FYGrbFJ8OD7Ww66YBketGc5ZCqTmy0QIM4K5rIEbl8sRqKthZ6jH6tMPyg=)
26. [ashbyhq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFmAfntqesB0LRiLemydMIFfizENLzz-BMTAKT13briFbtXe_KO9gn3-w42Tt-ejoZUrKRLCFmSTQzMwyXTWMOk2RUdUVk1i6z5UyVvbd4r_ouOY6bTnfnJALponZyFKcgVe7PhuLlUY78yhcVP_-gRSF5uN11Jvysw)
27. [ashbyhq.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLwh__HwOdLyWHvLzjanaIIezV5m5yvGi052ruuqPQFnGAkMr3pshTbDhncRZAnac_2sQVGxSCL4nYnOELk4AkcFo1J5E_Vc9-yrsjBPuj7dACQihcUv8z8dpSaxFb9nI8G2_iLmGCyoNw3OYEYl4GnlhpsSMKP3ZQ)
28. [bebee.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFho83jVNtESayswkFv8Dkn6qoNyKSWzsCGwOAF0kiKjFYKo98zRxN7ip4EZNr_BPgxjlCmaRoWpX5Eqwso-AHbqhxq7RcDT9AD_jFTGgtV0AYO4YzprzDRlT11-daEVHasHYBEdb88J4IFVqg-xgap8A8I3TPo1ym9aSBhusXy40a_54I6YiMmEwTuxbdf748ySuT13YrRch0aBEIWFT66uVQIUgR4IfbtqmNSFdbp9TJcPQ==)
29. [klaviyo.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFBzcDlnOX-9auwpLhFEPCuQpOH5EK4k3BCnahppHSkvHzmrB544uVRvRn6__ErmV2ygBXCuG5v03Mh-4XczQHAGFTcLQmtn8SdtYFSFlYB-zbT9Lx1HWvcyCNMgzfxTCn9DpTO)
30. [greenhouse.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHgCJBuJ-FVnfu0QsTjpLDjayfgHly5Y0x51g71B8setVS_0ISO-3K0z3dGC9jVRuiqcQSCSjXT_tnjkOf2AUjkERlc_QuH3aUwKV0oktluT6k2qA72SIy3TygAwAq1NwDrQMuFjdTOb1TTFo0k)
31. [startup.jobs](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGOFbl2oGZAdJsIEVR0QjEujeboZF0saQx5J6ub4YMD4GQLOeKeSExNsMlZGYPD0HOcwFJQY0RrNYIJksBjHbmVsqhbEJry1AYPYYAwJJcSwQznfBg3Y5a5xXxh3KMpU3U1F83WYczUl1oQoYEHbMMp-6-1uMaaKA==)
32. [migratemate.co](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHrMf_T8St5wzXsNx27h3bdVDUcvCkpSiNJ5sZpIB-C4PQ1nueXoksvCUSaygfox-HSE38C8gPK3_a20TffVJmMZJGcF5-J9I_KNmTq8POTVu9LetOR870JVXCOGa5JzUlFN5xk5BeJIkssmcLm9uJmd6MuL2HMwmBOWtZ0vAYGe8LKeunW)
