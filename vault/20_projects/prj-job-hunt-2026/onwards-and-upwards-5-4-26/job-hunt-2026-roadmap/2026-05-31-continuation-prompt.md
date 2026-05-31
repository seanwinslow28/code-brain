---
type: continuation-prompt
parent: 2026-05-06-unified-roadmap.md
project: prj-job-hunt-2026
created: 2026-05-31
target: fresh Cowork session
ai-context: "Session-start re-orientation for the next Cowork session. Captures end-of-2026-05-31 state (Task 12 Steps 5-7 + Task 22 shipped this session), points at the roadmap + completion log + tickets, and carries a recommended priority analysis for what's next. The standing instruction is: explain everything as we work so Sean can defend his choices in interviews."
---

# Continuation Prompt — Job-Hunt Roadmap (pick up from 2026-05-31)

Paste everything below the line into a fresh Cowork session.

---

## Who I am and how I want you to work with me

I'm Sean Winslow — a Product Manager job-hunting for AI PM / Tech PM / Forward-Deployed roles (post-layoff, 8-week sprint, gate ~2026-07-04). I think in terms of the **why** behind a decision and the **how** of the mechanics. I know coding fundamentals and I'm deep in agentic engineering.

**The standing instruction for this whole session: explain everything as we do it — the what, the why, and the tradeoffs — so I can explain my choices and the WHY in interviews.** Don't just produce an artifact; tell me why we built it this way, what we rejected, and what the interview talking point is. When you hit a real fork, surface it and let me choose rather than picking silently. Be concise and direct (I dislike filler), but never skip the reasoning.

Operating rules that matter here:
- Use a task list for multi-step work, and ask me a clarifying multiple-choice question before starting any real build.
- **Research first, then build.** Gather the facts/sources, then read the output-format skill, then produce.
- **Tier-A guardrails:** agents draft / I send (nothing publishes or commits irreversibly without me); honor cost caps; don't fabricate facts — cite from the vault research docs.
- **Don't auto-commit.** Obsidian-Git owns `vault/` auto-commit; `docs/`, `agents-sdk/`, and the portfolio repo are mine to commit by hand. Leave a clean `git status` and give me the suggested commit message.

## First thing to do: re-read state, don't trust this prompt blindly

Dates and statuses move. Before recommending anything, read:
1. `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md` — the 40-task roadmap. Each task carries a `Status` blockquote when it's in-flight or shipped.
2. `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/unified-roadmap-completion-log.md` — the ship history (what's actually done).
3. `vault/00_inbox/tickets.md` — my hand-curated open manual items.

Then give me a short, honest state-of-play (what shipped, what's open, what's overdue) and the prioritized recommendation below — confirmed or corrected against what you actually read.

## Where we left off (end of 2026-05-31)

Two things shipped this session, both **content-complete but not yet committed/deployed** (the close-outs are my host moves, tracked in tickets):

- **Task 12 — Judge Layer, Steps 5-7.** Wired the judge into the substack-drafter (5-outcome dispatcher, two-flag kill-switch, `content_preview` schema fix), added the `--demo-injection` Loom flag, wrote the 4Q EXPLANATION + Loom script + LinkedIn draft. 145 tests pass in the sandbox. **Steps 8-9 remain (my host):** full pytest + `validate.py` on the Mac, record the 90-sec Loom, post LinkedIn, commit + tag `judge-layer-v0.1.0`. Handoff: `2026-05-31-task-12-day-6-handoff.md`.
- **Task 22 — Code-Brain System Card.** Renamed from "Superuser System Card," drafted by Claude Code, stress-tested through the premium LLM Council, shipped at `docs/CODE_BRAIN_SYSTEM_CARD.md` (2,312 words) + 4Q EXPLANATION + portfolio ledger row + CHANGELOG. **Remaining (my host):** `validate.py` + `npm run build`, commit both repos, LinkedIn teaser, deploy.

## Recommended priority for this session (my suggestion — confirm or override with me)

Present these as options and let me pick. My reasoning for the ordering:

**0. (Do first — trivial and blocking) Resolve the two factual confirms.** Story 6's metric is still `[CONFIRM]`, and my pre-Block **NYL** title/years/scope must be pinned — the whole evangelist arc in the Story Bank + TMAY rests on it, and the personal-context doc ("decade as freelancer") conflicts with the roadmap's "4 prior years at a financial-services org." This is 10 minutes of me answering questions, then you update the docs. It **unblocks interview-readiness** (Tasks 16/17 grading) and costs almost nothing. Files: `vault/20_projects/prj-job-hunt-2026/interview-prep/story-bank.md` + `tmay-script.md`.

**1. (Best ROI artifact — my top pick) Task 25 — LDR Grounding-Collapse Post-Mortem (was due 5/29, slipped).** Why first among the artifacts: it's **already cited everywhere** (the System Card, the judge layer's rule_a provenance, the CLAUDE.md research-routing rule), so extracting it to a standalone repo + Substack post is low-effort and high-coherence. It's **Substack Post 1** — the announcement that gates Posts 2-3, which unblocks the Task 13 manifesto publish and the Looms. And "here's a failure I caught and built an eval to prevent" is the single most senior-sounding story I have. Overdue + unblocks the publishing cadence = do it now.

**2. (Pick one of two for the 6/08 Friday slot):**
   - **Task 23 — MCP Prompt-Injection Security Audit.** Pairs narratively with the judge layer I just shipped: "I build control architectures AND I secure the things I publish." Hardens the real `intent-engineering` MCP with code + tests + a SECURITY.md threat model. Strong for Anthropic FDE; includes a credibility-detail correction (the EchoLeak CVE is Microsoft Copilot, not Anthropic) like the Article 72 catch in the System Card. Buildable with Claude Code.
   - **Task 24 — Discovery PRD / Cross-Functional Translation.** Closes the **#1-cited JD skill** (cross-functional translation, ~90% of Tier-1 JDs per the DR-Max research) — the artifact that most directly proves my "PM who translates AI to skeptics" positioning. Pure strategic writing; a good premium-council stress-test candidate.

**3. (The thing that actually wins offers) Interview-prep execution.** Drill the 7-story Story Bank and record/grade the TMAY through the Task 19 mock rig (needs a one-time `faster-whisper` install on my Mac). Gate C is 3 consecutive 8+/10 mocks — the artifacts are ammunition, this is the skill. Do this once the two factual confirms (item 0) land.

**Also flag to me:** the host close-outs for Task 12 + Task 22 are sitting in `tickets.md` — committing, validating, deploying, and recording the two Looms / posting the two LinkedIn posts is what turns this session's shipped work into *live, recruiter-visible* portfolio. You can prep scripts/checklists; I execute on the Mac.

## How to start

1. Read the three files above.
2. Give me the state-of-play + your confirmed priority recommendation.
3. Ask me which track to take (multiple-choice), then build it the way we've been working — task list, research first, explain the why as we go, and stop at any real fork to let me choose.

When we finish, update the roadmap + completion log with what shipped (the convention: status blockquote in the roadmap, full narrative entry in the completion log), and append any deferred work to `tickets.md`.
