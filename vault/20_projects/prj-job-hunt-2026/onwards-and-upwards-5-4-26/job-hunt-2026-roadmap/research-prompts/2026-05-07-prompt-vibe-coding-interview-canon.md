---
type: research-prompt
project: prj-job-hunt-2026
target_model: gemini-deep-research
estimated_cost: ~$2
created: 2026-05-07
fire_target_date: 2026-05-15  # Mid Week 2, after the 14-agent fleet Loom records, before any final-round invitation lands
expected_output: vault/20_projects/research/2026-05-15-vibe-coding-interview-canon.md
roadmap_link: Roadmap §3 Claim G + Master plan Phase 6 Task 6.1 (interview prep)
ai-context: "DR prompt (NOT Max) for interview-prep grounding on the 45-min Bolt/v0/Cursor rep + portfolio-walkthrough variant. Engineered using the prompt-engineering skill. Anti-hallucination guards are EXTRA strong here — interview details are notoriously unverifiable (NDAs, rumor cruft)."
---

# Gemini DR Prompt — Vibe-Coding Interview Canon 2026

> Copy everything below the `--- PROMPT START ---` line into Gemini Deep Research (standard tier — NOT Max; this is a single-shape topic with a coherent public-source set) or pipe via `agents-sdk/scripts/gemini_dr.py --tier dr`. Output report saves to `vault/20_projects/research/2026-05-15-vibe-coding-interview-canon.md`.

> **Fire timing:** Mid Week 2 (~2026-05-15), after the 14-agent fleet Loom is recorded but before any final-round invitation lands. Roadmap §3 Claim G (the live-demonstration claim) + Master plan Phase 6 Task 6.1 (interview prep).

> **Why this prompt is necessary even though §3 Claim G already named Aakash Gupta + Sierra:** the roadmap names the *existence* of the interview shape; this prompt produces the *playbook* — sample rep prompts, the failure-mode taxonomy, the rubric details, and the "first-five-minutes / last-five-minutes" tactical notes. Without that, Week 5+ interview prep is theoretical.

--- PROMPT START ---

<role>
You are a former AI-native company hiring manager who has personally run 50+ vibe-coding interview reps as the evaluator at companies like Sierra, Decagon, or comparable Series B-D AI-native shops. You also coach AI PM candidates pre-onsite. You have read every public post-mortem, podcast appearance, and Substack writeup on the AI-native onsite format from 2025-Q4 through 2026-Q2. You know which interviewer behaviors are real, which are myth, and which signals separate "advance to next round" from "polite no." You speak with the precision of someone whose pre-onsite coaching has produced verified offers.

Your job is to produce a vibe-coding interview playbook for a 35-year-old PM (8 years experience, beginner-to-intermediate coder, strong agent-orchestration intuition, AI-native PM job hunt mode). The candidate already has a 14-agent SDK fleet they can demo, an MCP server in build, and a Loom-recording habit. The playbook is not a "what is vibe-coding" explainer — the candidate already knows what it is. It's a *playbook* — concrete reps, rubrics, failure modes, and tactical notes for performing well under the actual format.
</role>

<context>
**Format the candidate is preparing for:** The 45-minute live build using Bolt, v0, Cursor, Replit Agent, or comparable AI coding tool, often with a take-home component or a portfolio-walkthrough variant. Spec: candidate is given a brief, an agent harness, a deploy target, and a deadline. Some loops add adversarial follow-up ("now make this resilient to <X> attack"). Per Karpathy's hiring framing.

**Where this format is documented in the roadmap's source set:**
- Aakash Gupta's research at news.aakashg.com on AI-native onsites (Sierra, Decagon, others)
- The "What was the F1 score?" → "I'd have to check" → interview-over failure mode (Aakash's coached candidate)
- Sierra's "AI-native onsite" public spec (corroborated by ChatGPT-Nate-2)
- 45-min Bolt/v0/Cursor live builds now standard at Google, Netflix, Stripe, Adobe per news.aakashg.com

**Candidate's existing assets that are reusable in interviews:**
1. 14-agent SDK fleet — recordable as a Loom, demo-able live, narratable as architecture
2. `intent-engineering` MCP server (in build, ships 2026-05-25)
3. Phase D typed reasoning edges + Phase 6 knowledge loop — both demoable in 5 min
4. Working knowledge of Anti-Gravity, Cursor (lightly), Bolt, v0, Claude Desktop, Claude Code

**Candidate's known weak spots:**
- Beginner-to-intermediate Python; weaker on TypeScript still
- Has not done a vibe-coding rep against a stranger evaluating in real-time
- Tendency to over-explain when nervous (the "narrate your decisions in real time" coaching from Claude-Nate-1 §7 cuts both ways — narration helps, over-narration kills clock)

**Tier-A constraint that affects interview prep:** the candidate must protect Track-C (MCP server build) even during interview weeks. Practice rep cadence cannot exceed 2 reps/week starting Week 3, and reps must fit inside the comms block (15:00-17:15), not deep-work.
</context>

<task>
Produce a 7-section vibe-coding interview playbook covering the items in <output_format>. Multi-source triangulation per claim: prefer claims that appear in two or more independent primary sources (Aakash Gupta + a candidate post-mortem + a hiring manager post; or a Sierra/Decagon/comparable's own published interview policy + a verified candidate report).

Calibrate to "this is the playbook the candidate uses to practice in Week 3 and to walk into a real loop in Week 5+." Not exhaustive coverage. Tactical concrete > academic comprehensive.
</task>

<anti_hallucination_guards>
EXTRA STRONG. Interview details are the worst-grounded topic in this prompt set:
- Most candidates sign NDAs and cannot confirm specifics
- Public reports come from blog posts, Substack post-mortems, and podcasts that mix verified facts with rumor
- Hiring-manager posts often describe what they wish their loop did, not what it actually does
- "Sierra runs a 45-min Cursor rep" is a specific claim that needs a specific source

Required discipline:
1. Every named company's interview format must cite (a) a candidate post-mortem with a name + URL OR (b) a hiring manager's verifiable post (LinkedIn, blog, podcast with timestamp) OR (c) the company's own engineering/hiring blog. Do not aggregate "I've heard from multiple sources" without naming sources.
2. Every "rubric" claim must cite where the rubric was published or described publicly. If a rubric is internal-only (which most are), write "Rubric: not publicly disclosed — pattern inferred from candidate post-mortems."
3. The "What was the F1 score?" failure mode is real (Aakash Gupta coached this candidate). Verify the original post URL + date and quote ≤15 words verbatim. Do not paraphrase as if it were Aakash's exact wording.
4. Tool-specific claims (Bolt does X, v0 does Y, Cursor does Z) must cite the tool's own docs or a verifiable demo. Do not attribute features to tools that don't have them.
5. If a tactical recommendation cannot be sourced (e.g., "always do X in the first 5 minutes"), present it as the playbook author's recommendation with reasoning, not as canon. Use phrasing: "My recommendation, based on <pattern>:" rather than "Industry consensus is:".
6. Sample rep prompts (§4) must be realistic and within tool capability. If you write a sample prompt that requires a feature Bolt doesn't have, the candidate will discover this in practice and lose trust in the playbook.
</anti_hallucination_guards>

<citation_format>
GOOD:
> The Sierra AI-native onsite includes a 45-minute live build using Cursor, per Sierra's own engineering blog post "How we hire engineers in the agent era" ([sierra.ai/blog/...](https://...), published 2026-XX-XX, accessed 2026-05-15).

GOOD:
> Aakash Gupta's coached candidate failed the loop on a follow-up question about training metrics — when asked the F1 score, the candidate said "I'd have to check," which Aakash describes as <quote ≤15 words> ([news.aakashg.com/p/...](https://...), accessed 2026-05-15).

ANTI-PATTERN (do not produce):
> Sierra is known for rigorous interview loops with vibe-coding components. Candidates often fail when they cannot answer detail questions about their work.

The first two contain verifiable source + URL + accessed-on date + (where applicable) a tightly-bounded quote. The third is unattributed pattern-matching and is forbidden.
</citation_format>

<output_format>
Markdown document with this exact frontmatter:

```
---
type: research-report
project: prj-job-hunt-2026
research_topic: vibe-coding-interview-canon-2026-05
created: <RESEARCH_DATE>
model: gemini-deep-research
ai-context: "Vibe-coding interview playbook for Week 3+ practice reps and Week 5+ live loops. Anti-hallucination discipline: every company-specific format claim cites a primary source."
---
```

# Vibe-Coding Interview Canon 2026 — Playbook

## 1. The Format Today — Verified, Per Company
For each of the following, report the verified interview format with a primary source: Sierra, Decagon, Anthropic, Glean, Scale AI, Cursor (Anysphere), Vercel, Replit, plus 3-4 others where the format is publicly documented. For each: total loop length, presence/absence of a vibe-coding rep, the rep tool (Bolt / v0 / Cursor / Claude Desktop / Replit Agent / language-only Python in browser), the rep duration, the take-home (if any), the portfolio-walkthrough variant (if any), the source URL.

If a company's format is not publicly documented, include them in §1 as "Format: not publicly verifiable — recommend Glassdoor + LinkedIn outreach to recent hires."

## 2. The Rubric — What Evaluators Actually Score On
The 5-7 evaluator dimensions that recur across published rubrics and hiring-manager posts:
- Speed of working solution
- Quality of agent-prompting (does the candidate know how to drive the AI tool?)
- Decision narration (the "narrate your decisions in real time" axis from Claude-Nate-1 §7)
- Failure recovery (when something breaks, what does the candidate do?)
- Code quality of the final artifact
- Spec interpretation (did the candidate solve the right problem?)
- Plus any others sources surface.

For each dimension: the canonical signal of HIGH score, the canonical signal of LOW score, and the "blow-up" signal that ends the loop early. Cite each.

## 3. Common Failure Modes (Catalogued)
The 7-10 most-cited failure modes from candidate post-mortems and hiring-manager posts. For each: a one-sentence description, a one-sentence "why it kills the loop," a one-sentence "how to inoculate against it before the rep." Lead with the F1-score failure (Aakash Gupta's coached candidate). Include at least: (a) over-narration killing clock, (b) under-narration making the evaluator unable to score, (c) prompting the agent without reading what it produced, (d) ignoring spec edge cases, (e) panic-deleting working code.

## 4. Sample Rep Prompts — 4-5 Realistic Briefs at the Right Difficulty
Each: a brief in the format the candidate would actually receive (1-2 paragraphs, with success criteria, with a clock). Use Bolt / v0 / Cursor / Replit Agent as the target tool variants. Tune difficulty to "intermediate AI PM with 8 years experience, beginner-to-intermediate coder" — not too easy (waste of practice time), not too hard (demoralizing).

Example tasks at the right level: build a feedback-collection form with sentiment analysis on submit; build a CSV uploader that runs LLM-based PII redaction; build a small RAG demo over uploaded markdown. Mark each with: target tool, target duration, success criteria, the 1-2 traps the candidate should expect.

## 5. The First-Five / Last-Five Tactical Playbook
Tactical-concrete advice on:
- The first 5 minutes: spec re-statement, scope clarification, agent priming, deploy target setup
- Minutes 5-35: build cadence, when to commit/deploy, when to pause and verify
- The last 5 minutes: working-state freeze, narration of trade-offs, demonstrable end state vs. partially-broken work

For each phase: 3-5 specific moves. Cite where each move comes from (Aakash, candidate post-mortem, hiring manager post, or "playbook author's recommendation based on pattern X").

## 6. The Portfolio-Walkthrough Variant
Some loops substitute a portfolio walkthrough for a vibe-coding rep. The candidate's 14-agent SDK fleet, MCP server, and Phase D edges are all walkthrough-able. For each artifact: a 5-minute walkthrough script outline (don't write the actual script — the candidate will), the 3-5 questions an evaluator typically asks, the 1-2 answers that signal HIGH score vs. LOW score. Anchor against Anthropic FDE / Glean FDP / Sierra agent PM expectations.

## 7. The Practice Cadence
A specific 4-6 week practice schedule starting Week 3:
- Reps per week (max 2 — must respect deep-work block)
- Time slot (within the 15:00-17:15 comms block)
- Tool rotation (Bolt week, v0 week, Cursor week, take-home week, portfolio-walkthrough week)
- Self-evaluation rubric (use §2 dimensions, score self 1-5 per rep)
- When to bring in a partner for live evaluation (recommend specific Boston-area AI-PM Slack/Discord communities or warm-network candidates)

## 8. Sources Index
Every URL cited above, organized by section. Include accessed-on date for each. Group "playbook author's recommendation" items separately at the bottom — these are the recommendations that are NOT canon, just defensible patterns.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health + quote accuracy**: Every URL gets opened. Every direct quote (especially Aakash's F1-score quote) gets verified ≤15 words and matches the source.
2. **Company-format discipline**: Re-read §1. For every company, either you have a primary source or you have written "Format: not publicly verifiable." No middle ground.
3. **Sample rep difficulty calibration**: Re-read §4. For each sample brief, ask: "Could a beginner-to-intermediate coder PM with 8 years experience and Cursor familiarity actually finish this in the stated duration?" If "no," recalibrate.
4. **Tool feature accuracy**: Re-read §4 and §5 for tool-specific claims. Verify each tool actually has the feature you're attributing to it.
5. **Practice cadence sustainability**: Re-read §7. Does the proposed cadence respect the candidate's "max 2 reps/week, inside 15:00-17:15 comms block, must protect Track-C deep-work" constraint? If not, recut.
6. **Word count**: Target 3,000-4,500 words. Below 3,000 means under-researched; above 4,500 means scope creep.
</validation>

--- PROMPT END ---
