---
type: research-prompt
project: prj-job-hunt-2026
target_model: gemini-deep-research
estimated_cost: ~$2
created: 2026-05-07
fire_target_date: 2026-05-13  # Week 2, before the target-30 list deadline of 2026-05-18
expected_output: vault/20_projects/research/2026-05-13-boston-remote-ai-pm-landscape.md
roadmap_link: Task 6 §E (Week 2 target-30 list deliverable)
ai-context: "DR prompt (NOT Max) for company-broad discovery to feed the Week-2 target-30 list. Complementary to the Tier-1 target-role-specs DR Max prompt — that one deep-profiles ~10 known companies, this one surfaces another 20+ candidates by casting a wider net. Engineered using the prompt-engineering skill."
---

# Gemini DR Prompt — Boston/Remote AI PM Company Landscape

> Copy everything below the `--- PROMPT START ---` line into Gemini Deep Research (standard tier — NOT Max; this is breadth-first discovery, not multi-target due diligence) or pipe via `agents-sdk/scripts/gemini_dr.py --tier dr`. Output report saves to `vault/20_projects/research/2026-05-13-boston-remote-ai-pm-landscape.md`.

> **Fire timing:** Early Week 2 (~2026-05-13) so the output feeds the target-30 list before the 2026-05-18 deadline. Roadmap Task 6 §E.

> **Sequencing note:** Run AFTER the Tier-1 target-role-specs prompt has produced output. That prompt deep-profiles ~10 known companies; this prompt surfaces another 20+ candidates that the next round of role research can deep-profile. Don't run them simultaneously — the first one's output narrows the second one's search space.

--- PROMPT START ---

<role>
You are a Boston-area tech recruiter and talent intelligence analyst with deep coverage of the New England + East-Coast-remote AI hiring market. You track which companies have actually posted AI PM, Forward Deployed Product, and Agent Ops roles in the last 60 days — not which companies have a generic "AI strategy" page. You read Built In Boston, Wellfound, AngelList, LinkedIn Jobs, company careers pages, and the Boston tech press (BostInno, BostonGlobe.com tech section). You speak with the precision of someone whose company-list recommendations have been independently verified by candidates who got onsite invitations.

Your job is to produce a Boston-metro + remote-East-Coast AI PM hiring landscape report for a 35-year-old PM (8 years experience, currently in AI-native PM job-hunt mode) whose existing company-list (Anthropic, Glean, Sierra, Decagon, Scale AI, Robinhood, Pair) is being deep-profiled separately. Your job is BREADTH — surface 25-35 additional companies the candidate hasn't already named where their portfolio shape (MCP server + 14-agent SDK fleet + comprehension artifacts + vault-RAG infrastructure) is a meaningful differentiator.
</role>

<context>
**The candidate's primary track:** AI Product Manager.
**Backup track:** Agent Ops / Forward Deployed Product / Support Ops AI.

**Tier-A constraints (non-negotiable):**
- Walk-away salary: $100k base
- Will not take 5-day-in-office roles (3 days max, prefers 0-2)
- Boston-metro preferred, remote-East-Coast-time-zone-friendly works
- AI > Tech > Creative PM ordering

**Already deep-profiled (do NOT re-cover):** Anthropic FDE, Glean (Agent Security & Governance / AI Quality / FDP), Sierra agent PM, Decagon agent PM, Scale AI (GenAI Platform / Public Sector T&E), Robinhood, Pair. The complementary prompt covers these.

**Target deliverable schema:** The candidate is building a `vault/20_projects/prj-job-hunt-2026/target-companies.md` file with 10 Tier-1 + 15 Tier-2 + 5 Tier-3 entries. Your output feeds the company candidates for that file — focus on Tier-2 and Tier-3 candidates. Tier-1 is mostly already filled by the deep-profile prompt.

**Candidate's portfolio shape (the differentiation hook):**
1. `intent-engineering` MCP server — TypeScript, ships 2026-05-25
2. 14-agent SDK fleet — launchd-scheduled, cost governors, local-model-first routing
3. Phase D typed reasoning edges — `concept_edges` SQLite + synthesizer relations
4. Phase 6 knowledge loop — SessionEnd flush → nightly synthesizer → weekly lint → SessionStart re-injection
5. Sanitized agentic financial-research fleet — multi-agent retrieval + synthesis
6. Animation pipeline — June 11 ship, ComfyUI + Remotion + LoRA workflow

The portfolio biases toward: AI infra companies, agent platforms, vertical-AI startups in finance/legal/healthcare/dev-tools, AI-native PM-tooling companies, AI-augmented productivity SaaS. It biases AGAINST: generic SaaS with a chatbot bolted on, big-co "AI transformation" roles, AI-marketing-flavored startups.
</context>

<task>
Produce a 7-section landscape report covering the items in <output_format>. Multi-source triangulation per company: prefer companies where you can verify (a) at least one open AI PM / FDP / Agent Ops role posted in the last 60 days, (b) the role respects the $100k floor and ≤3-day-RTO constraint, AND (c) a credible portfolio-fit signal (the company has technically substantial AI work, not just AI marketing).

Cast a wide net in §1 (Boston-metro) and §2 (Remote East Coast). Be ruthless in §3 (the do-not-apply list) — flag companies that LOOK like AI shops but have red flags the candidate should avoid.
</task>

<anti_hallucination_guards>
1. Every named company must link to (a) a current careers page URL OR (b) a Built In Boston / Wellfound / LinkedIn Jobs URL with the role posting date. If neither, do not include the company.
2. Every named role must include the role title as it appears on the JD, not a paraphrase. If the JD title is "Member of Technical Staff," do not call it "AI PM."
3. RTO policy claims must cite a primary source: the JD itself, the company's published policy page, a verified employee post, or a Built In Boston "Office Setup" field. Do not infer RTO from company size or category.
4. Comp range claims must cite Levels.fyi, Glassdoor, JD-disclosed range, or a credible candidate report. If unverifiable for a specific company, write "Comp range: not publicly disclosed — recommend Glassdoor + recruiter conversation."
5. Boston-area company list is NOT generic. The candidate already knows about HubSpot, Wayfair, Toast, Klaviyo, DraftKings — only include these if you can name a specific AI PM / FDP / Agent Ops role open at that company in the last 60 days. Otherwise skip.
6. Do not pad. If you can only verify 18 companies, deliver 18. Padding to 25 with hand-waved listings hurts the candidate.
</anti_hallucination_guards>

<citation_format>
GOOD:
> Tessera Therapeutics (Cambridge, MA) posted "Senior PM, AI Platform" on 2026-04-22, 3 days/week in-office, comp range disclosed at $185k-$220k base ([careers URL](https://...), accessed 2026-05-13). Differentiator hook: agent fleet for genomics workflows.

ANTI-PATTERN (do not produce):
> Tessera Therapeutics is a Boston biotech with AI initiatives. They likely hire for AI PM roles.

The first contains a verifiable role + posting date + RTO + comp + URL + accessed-on date. The second is unverified pattern-matching and is forbidden.
</citation_format>

<output_format>
Markdown document with this exact frontmatter, then the seven sections.

```
---
type: research-report
project: prj-job-hunt-2026
research_topic: boston-remote-ai-pm-landscape-2026-05
created: <RESEARCH_DATE>
model: gemini-deep-research
ai-context: "Company-broad discovery feeding the Week-2 target-30 list. Complements the Tier-1 deep-profile report. All companies cited or excluded."
---
```

# Boston/Remote AI PM Landscape 2026-05 — Companies Beyond the Deep-Profile Set

## 1. Boston-Metro Companies with Open AI PM / FDP / Agent Ops Roles (15-20 entries)
For each: company name, HQ + office locations, role title (verbatim), posting date, RTO policy, comp range with source, JD URL, the 1-2 portfolio-fit hooks the candidate would lead with in a cover note. Include enough variety: established (HubSpot AI Lab, Klaviyo AI Platform, Toast AI), growth-stage (e.g., Hugging Face Boston, Together AI, MosaicML/Databricks Boston), early-stage (MIT-spinout AI startups verifiable on Wellfound).

Specifically include if verifiable: HubSpot AI, Klaviyo, Wayfair AI, Toast AI, Salsify, Cogito, Pendo Boston, Salsify, Indigo Ag, Tessera, Ginkgo Bioworks, Iterable, DataRobot, Domo, FRG/Verily Boston, Klarna Boston, Atlassian Boston, Snyk, Cybereason, Rapid7. Skip any of these you cannot verify a current open role for.

## 2. Remote-East-Coast-Friendly Companies with Open AI PM / FDP / Agent Ops Roles (10-15 entries)
Same schema as §1 but for remote-first companies that hire East Coast time-zone candidates. Specifically check: Replit, Vercel, Linear, Notion AI, Cursor (Anysphere), Bolt (StackBlitz), v0/Vercel AI, Pinecone, Weaviate, Chroma, LlamaIndex, LangChain, Modal Labs, Modal, Hex, Hex AI, Outshift (Cisco), Cohere, Mistral US, Inflection, Character.AI, Perplexity, You.com, Adept (if still operating), Imbue, Magic.dev. Skip any you cannot verify.

## 3. The Do-Not-Apply Tier (5-10 entries)
Companies that appear AI-PM-shaped but have red flags: 5-day RTO mandate, sub-$100k base, recent layoffs in PM org, AI-washing without technical substance, glassdoor patterns indicating PM org dysfunction. For each: name, the disqualifying signal, the source.

## 4. Hidden Gems — Companies Not on Most Lists (5-8 entries)
Boston-area or remote AI shops that don't show up on Built In Boston or Wellfound's top results but where the candidate's portfolio is unusually well-matched. Sources: YC W25/S25/W26 batch, Anthropic Build with Claude features, recent AI-startup funding announcements ($5-50M Series A range), Boston-area AI meetup speakers in last 6 months.

## 5. Application Channel Per Company
For each company in §1, §2, §4: the recommended application channel. Options: career-page direct, recruiter network (name the Boston-area AI recruiters who cover the company if known), warm intro via the candidate's stated networks (Mary, Matt, Larry — the candidate's Tier-A collaborator list), or founder DM (if early-stage). Do NOT recommend channels you cannot defend with reasoning.

## 6. Tier Sorting Recommendation
For each verified company in §1, §2, §4: Tier-1 (immediate apply, top-fit) / Tier-2 (apply Wave 2) / Tier-3 (wildcard). Sort by (portfolio-fit × role-realism × Tier-A-compliance). Output as a single ranked table the candidate can paste directly into `target-companies.md`.

## 7. Sources Index
Every JD URL, careers page, Built In Boston entry, Wellfound profile, Levels.fyi entry, Glassdoor URL, employee post, and funding announcement cited above. Organized by company. Include accessed-on date for each.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health**: Every JD URL gets opened to verify it loads. Replace 404s or remove the entry.
2. **Tier-A discipline**: Every company in §1, §2, §4, §6 must respect the $100k floor and ≤3-day RTO. Flag any exceptions with explicit justification.
3. **De-duplication**: Cross-check against the deep-profile companies (Anthropic, Glean, Sierra, Decagon, Scale, Robinhood, Pair). Remove any duplicates.
4. **Padding check**: Re-read §1 and §2. If any entry is "this company probably has AI roles" without a verified open posting in the last 60 days, remove it.
5. **Channel discipline**: Re-read §5. If any recommended channel is "warm intro" without a verifiable connection in the candidate's stated networks, downgrade to "career-page direct."
6. **Word count**: Target 3,000-4,500 words. Below 3,000 means under-researched; above 4,500 means padding.
</validation>

--- PROMPT END ---
