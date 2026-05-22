---
type: continuation-prompt
project: prj-job-hunt-2026
created: 2026-05-21
for_session_on: 2026-05-22
ai-context: |
  Kickoff prompt for the fresh Claude Code session Sean opens on 2026-05-22. Self-contained —
  fresh Claude has no context from prior sessions. Orients on: (a) the operating-model Tier-A
  truths, (b) what shipped 2026-05-21 (Task 20 closed, Task 13 Steps 2 + 3 done), (c) what's
  left for the Sat 5/23 EOD draft-lock (Task 13 Steps 4-7), (d) the 6 load-bearing files to
  read first, (e) the work pattern (agents draft / Sean sends), (f) tone preferences.
  Paste this entire body into the fresh Claude Code session as the opening message.
---

# Kickoff prompt for 2026-05-22 — paste this into the fresh Claude Code session

---

I'm picking up the job-hunt sprint from yesterday's Cowork session. Read the load-bearing files below in this order, then walk me through next steps. I want you to explain everything so I can speak to it in interviews — be brief and to the point, but tell me the WHY behind every choice.

CONTEXT (don't ask me to re-explain):

I'm Sean. I was laid off from The Block on 2026-05-05 and am running an 8-week job-hunt sprint with these Tier-A truths from my operating model (do not violate any of these):
- Target: AI PM > Tech PM > Creative PM. Walk-away comp is $100k+.
- 8:30 AM - 5:30 PM work container. 1-2 PM mandatory break. 5:30 PM hard stop.
- Agents draft / Sean sends — every word that reaches another human's inbox is mine.
- Track-C (intent-engineering MCP) is protected even in offer weeks. It's shipped (npm + Anthropic MCP registry, 2026-05-12, 13 days early).
- Boston-metro + remote roles, no SF on-site unless wildcards (Sierra/Decagon).

YESTERDAY'S SHIP (2026-05-21):

- **Task 20 GitHub Profile Audit CLOSED.** Bio rewritten (Variant A, 132 chars, "AI PM building MCP servers + an agent fleet"), 6 repos pinned in recruiter-impact order (sw-mcp-intent-engineering first), 4-section READMEs added to each, 3 strategic forks live, cross-links live across GitHub / LinkedIn / Substack. Shipped 1 day ahead of the 5/22 target. Gate A precondition satisfied.
- **Task 13 Step 2 — Manifesto Draft SHIPPED.** Premium-profile LLM council run (Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20, chairman = Opus 4.7, $0.5285 actual cost) drafted the canonical "Access Over Meaning" manifesto. Unanimous A-first cross-rank. 4-edit voice pass applied (§1 P2 polysyndeton push, §1 P3 hedge removal, §1 P4 Nate citation tightening, §5 P2 dial push from 50% sober to 85% Sean Mode). Final at `docs/MEANING_OVER_ACCESS.md` — 1,622 words, voice dial average ~90% Sean Mode across §1 + §5, concept_edges schema corrected (`supports, contradicts, evolved_into, supersedes, depends_on, related_to`) to match Task 15 Vault Scorecard shipping 6/3.
- **Task 13 Step 3 — Mermaid Render SHIPPED.** `docs/diagrams/access-meaning-spectrum.{mmd,svg,png}` with brand palette config locking teal #0A3E42. SVG (7.6KB) for portfolio /essays/ embed, PNG (95KB, 1000×1000) for Substack image embed. `mmdc 11.15.0` installed globally at `/opt/homebrew/bin/mmdc` for all future essay renders.

I read the manifesto out loud last night. If anything still feels off when YOU re-read it, flag specific sentences — but do NOT rewrite anything until I ask.

WHAT'S LEFT FOR TASK 13 (Sat 5/23 EOD draft-lock):

- **Step 4 — V3-bridge `/essays/` IA.** Extend `~/Code-Brain/sw-portfolio/` (the already-shipped V3 bridge with `/transactions/` infrastructure) to add a `/essays/` route that renders `docs/MEANING_OVER_ACCESS.md`. Per Task 13 Step 1 prep doc §7, this is option (a) — `sw-ai-pm-portfolio/` is Phase 0/1 and can't host the route by 5/23. Approx 3-4h. Mirror the `/transactions/` pattern, don't invent a new structure.
- **Step 5 — Substack cross-post.** Draft at `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/2026-06-19-meaning-over-access-substack-cross.md`. Substack-formatted (PNG embed of the spectrum chart, no Mermaid block — Substack doesn't render it). Approx 1-2h.
- **Step 6 — 4Q EXPLANATION.md + final voice review.** `docs/MEANING_OVER_ACCESS_EXPLANATION.md` in 4Q format (What is this? / Why this approach? / What would break? / What did I learn?). Then one last writing-voice-modes pass on the manifesto if anything still bothers me from the out-loud read. Approx 1.5h.
- **Step 7 — Commit + tag `gap-fill-2-draft-locked`.** Across code-brain + sw-portfolio repos. Approx 30 min.

ENVIRONMENT (read these files first, in this order):

1. `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md` — canonical roadmap. Status pointer at Task 13 (~line 904) reflects Steps 2 + 3 shipped. Task 20 is a closed 2-line stub linking to the completion log.
2. `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md` — ship history. Read the 2026-05-21 amendment entry narrating Task 13 Steps 2 + 3 ship, AND the Task 20 entry under `## Completed Tasks`.
3. `/Users/seanwinslow/Code-Brain/code-brain/vault/05_atlas/operating-models/job-hunt-2026/operating-model.md` — Tier-A truths and HEARTBEAT rituals.
4. `/Users/seanwinslow/Code-Brain/code-brain/docs/MEANING_OVER_ACCESS.md` — the current voice-pass-applied manifesto draft. Read end-to-end.
5. `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-20-task-13-step-1-manifesto-outline.md` — Step 1 outline. §6 lists the supporting artifacts Steps 4-7 produce. §7 has locked decisions including the V3-bridge IA path.
6. `/Users/seanwinslow/Code-Brain/code-brain/CLAUDE.md` (main repo) + `/Users/seanwinslow/Code-Brain/sw-portfolio/CLAUDE.md` (V3 bridge where Step 4 lands).

WHAT YOU NEED TO DO AFTER READING:

1. Tell me which Task 13 step is highest-leverage to push on RIGHT NOW given today's date is 2026-05-22 (Friday) and the Sat 5/23 EOD draft-lock deadline. Step 4 is the riskiest (cross-repo Astro work in the V3 bridge); Steps 5-7 are mechanical.
2. For Step 4 specifically: examine the existing `/transactions/` infrastructure at `~/Code-Brain/sw-portfolio/src/pages/transactions/` and `~/Code-Brain/sw-portfolio/src/content/` to understand the IA shape I'm extending. Do NOT create a new collection from scratch — mirror the `/transactions/` pattern. Decide whether the manifesto goes at `/essays/` (index page) + `/essays/meaning-over-access` (detail page) or a flat single page.
3. Confirm imminent state: Task 19 build window (5/21-5/26) is also technically open — Step 1+1b (interview_grader profile + rubric template) could be done in ~1.5h. Do NOT push me into Task 19 unless I ask — keep me focused on Task 13.
4. Use the AskUserQuestion tool to ask me which Step of Task 13 I want to drive into first; offer the highest-leverage recommendation as the first option labeled "(Recommended)".
5. Maintain a TodoWrite task list as you go (Cowork mode renders it as a widget). Include a final verification step.
6. When you do real work, write outputs into:
   - Step 4 portfolio Astro files: `~/Code-Brain/sw-portfolio/src/pages/essays/` + `~/Code-Brain/sw-portfolio/src/content/essays/` (mirror the `/transactions/` structure)
   - Step 5 Substack cross-post: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/substack-drafts/2026-06-19-meaning-over-access-substack-cross.md`
   - Step 6 EXPLANATION.md: `docs/MEANING_OVER_ACCESS_EXPLANATION.md`

REFERENCES YOU MIGHT NEED:

- `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-21-task-13-step-2-council-draft.md` — full council transcript (4 panelist drafts + cross-ranks + chairman synthesis) if I want to revisit voice decisions
- `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/writing-voice-modes/SKILL.md` — voice calibration reference for a final §1/§5 pass during Step 6
- `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/target-companies.md` — strategic 30 with JD URLs (validated 2026-05-13). The 5 buyers in the manifesto's §3 role map came from here.
- `/Users/seanwinslow/Code-Brain/code-brain/docs/diagrams/.mermaid-config.json` — brand palette config; reuse for any new diagram renders this session via `mmdc -i <file>.mmd -o <file>.svg -c docs/diagrams/.mermaid-config.json`.
- `/Users/seanwinslow/Code-Brain/sw-portfolio/src/pages/transactions/` — the IA pattern Step 4 mirrors.

TONE: I'm a PM digging deep on the "why" and "how." Brief, kind, no fluff, no trailing summaries that just restate what you said. Push back when you think I'm wrong. Cross-pollinate from animation / game design / PM / AI-PM where it sharpens a recommendation. Use the AskUserQuestion tool before doing real work unless the path is obviously the right one.

Start by reading the 6 files in the ENVIRONMENT block + the manifesto draft end-to-end. Then summarize in 5-7 lines what state Task 13 is in. Then use AskUserQuestion to pick the next Step to drive into.
