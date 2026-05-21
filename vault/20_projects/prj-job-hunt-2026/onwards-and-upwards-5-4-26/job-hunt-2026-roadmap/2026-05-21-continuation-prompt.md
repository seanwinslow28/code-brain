---
type: continuation-prompt
created: 2026-05-21
target_audience: fresh Claude Cowork session (no prior context from this session)
ai-context: |
  Paste-ready prompt that re-orients a new Claude Cowork agent on where Sean's job-hunt
  roadmap stands after the 2026-05-20 → 2026-05-21 Cowork prep-doc sprint. Self-contained:
  the new agent reads the linked files and figures out next steps on its own rather than
  relying on session continuity.
---

# Continuation Prompt — for a fresh Claude Cowork session

> **How to use this file:** copy the contents of the code block below (everything between the triple backticks) and paste it as the first message in a brand-new Cowork session. The new agent will read the linked files itself and walk you through next steps based on the actual state of your roadmap.

---

## The prompt to paste

```
I'm picking up a job-hunt sprint from a prior Cowork session. Read the load-bearing files below in this order, then walk me through next steps. I want you to explain everything so I can speak to it in interviews — be brief and to the point, but tell me the WHY behind every choice.

CONTEXT (don't ask me to re-explain):

I'm Sean. I was laid off from The Block on 2026-05-05 and am running an 8-week job-hunt sprint with these Tier-A truths from my operating model (do not violate any of these):
- Target: AI PM > Tech PM > Creative PM. Walk-away comp is $100k+.
- 8:30 AM - 5:30 PM work container. 1-2 PM mandatory break. 5:30 PM hard stop.
- Agents draft / Sean sends — every word that reaches another human's inbox is mine.
- Track-C (intent-engineering MCP) is protected even in offer weeks. It's shipped (npm + Anthropic MCP registry, 2026-05-12, 13 days early).
- Boston-metro + remote roles, no SF on-site unless wildcards (Sierra/Decagon).

ENVIRONMENT (read these files first, in this order):

1. /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md — the canonical roadmap. Pay attention to the status pointers next to Tasks 13, 15, 19, 20 (added 2026-05-21).
2. /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md — the ship history. Read the 2026-05-20 amendment in particular — it summarizes the four queued tasks.
3. /Users/seanwinslow/Code-Brain/code-brain/vault/05_atlas/operating-models/job-hunt-2026/operating-model.md — Tier-A truths and the HEARTBEAT rituals.
4. /Users/seanwinslow/Code-Brain/code-brain/CLAUDE.md and /Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/CLAUDE.md — the two repos I work in.

FOUR PREP DOCS (the work queued for execution, with all decisions already locked):

- /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-20-task-20-github-profile-audit-deliverable.md — Task 20 (GitHub Profile Audit, ships Fri 5/22, ~60-90 min execution by me)
- /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-20-task-19-step-0-prebuild-prep.md — Task 19 (Mock Interview Infra, ships Tue 5/26, build window 5/21-5/26)
- /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-20-task-13-step-1-manifesto-outline.md — Task 13 (Access-vs-Meaning Manifesto, draft-lock Sat 5/23, publish ~6/19)
- /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-20-task-15-step-0-prebuild-prep.md — Task 15 (Vault Scorecard, build window 6/1-6/3)

WHAT YOU NEED TO DO AFTER READING:

1. Tell me which task is the highest-leverage to push on RIGHT NOW given today's date and the calendar — don't assume; check the prep docs' build windows and verification gates against the current date.
2. Confirm the imminent deadlines:
   - Task 20 ships Fri 5/22 (Sean executes ~60-90 min)
   - Task 13 Step 2 (full ~1,500-word draft pass) ships ideally same week as draft-lock 5/23
   - Task 19 build window is open NOW (5/21-5/26)
   - Task 15 build window opens 6/1
3. Surface any blockers or dependencies I should know about. Specifically:
   - Task 13 Step 4 needs a portfolio /essays/ IA — confirm whether to use the V3 bridge at ~/Code-Brain/sw-portfolio/ or wait for the redesign at ~/Code-Brain/sw-ai-pm-portfolio/ to hit Phase 3.
   - Task 15 Step 5 has the same /architecture/ IA dependency on the portfolio.
   - Task 19's test plan now uses a SWAPPED Q2 ("Walk me through what happened with The Block and how it reset your search") because I was laid off — confirm you see that in the prep doc.
4. Use the AskUserQuestion tool to ask me which task I want to drive into first; offer the highest-leverage recommendation as the first option labeled "(Recommended)".
5. Maintain a TaskCreate / TaskUpdate task list as you go (Cowork mode renders it as a widget). Include a final verification step in the list.
6. When you do real work, write outputs into the same vault path the existing prep docs live in: /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/ so they cluster with the rest.

REFERENCES YOU MIGHT NEED:

- vault/20_projects/prj-job-hunt-2026/target-companies.md — strategic 30 with JD URLs (validated 2026-05-13)
- vault/.vault-index.db — live SQLite of concept_edges (478 edges, 6 SQL-enforced relations, 13488 chunks, 8 superseded, 219 confidence-tagged). Useful for Task 15 telemetry checks.
- tools/llm-council/council/profiles.py — where the new interview_grader profile goes for Task 19
- The portfolio repo is in pre-build phase: 12 locked specs in docs/specs/, no Astro code yet. Phase 0/1 of its master plan.

TONE: I'm a PM digging deep on the "why" and "how." Brief, kind, no fluff, no trailing summaries that just restate what you said. Push back when you think I'm wrong. Cross-pollinate from animation / game design / PM / AI-PM where it sharpens a recommendation. Use the AskUserQuestion tool before doing real work unless the path is obviously the right one.

Start by reading the four files in the ENVIRONMENT block + the most recent amendment in the completion log. Then summarize in 5-7 lines what state the roadmap is in. Then use AskUserQuestion to pick the first task to drive into.
```

---

## What to expect from the new session

When you paste the prompt above into a fresh Cowork session, the new agent will:

1. Read the unified roadmap + completion log + the 4 prep docs (~5–10 min of file reads)
2. Surface the calendar-priority recommendation (which task is most time-urgent given today)
3. Use the AskUserQuestion tool to let you pick the entry point (with the recommended one first)
4. Spin up a task list and start driving

**Why this prompt structure works:** it tells the new agent (a) what the constraints are (Tier-A truths) so it doesn't propose violating them, (b) which files are load-bearing so it doesn't waste tokens grepping the vault, (c) what the decision state is (all 18 prep-doc decisions already locked — no need to ask them again), and (d) what tone to use (so it matches the existing voice). The "what you need to do after reading" block prevents the new agent from spending the first 10 minutes restating context back at you.

**If a fresh session feels lost or asks redundant questions:** paste this single follow-up: *"Did you read the unified-roadmap-completion-log.md 2026-05-20 amendment? All 18 open decisions across the four prep docs are already locked. Don't re-ask them."* That re-anchors the agent on the captured-decisions state.

**Where everything is, one more time, for muscle memory:**
- Roadmap: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`
- Completion log: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md`
- 4 prep docs: same dir, files starting with `2026-05-20-task-*`
- Operating model: `vault/05_atlas/operating-models/job-hunt-2026/operating-model.md`
