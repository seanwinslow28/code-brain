---
type: interview-prep-portfolio-roadmap
project: prj-job-hunt-2026
phase: interview-prep-phase-3
created: 2026-05-10
inherits_from:
  - 2026-05-10-vibe-coding-research-synthesis.md
  - 2026-05-10-vibe-coding-playbook.md
  - 2026-05-06-unified-roadmap.md
ai-context: "Portfolio projects sized specifically for interview-prep signal between 2026-05-10 and 2026-06-30. Composes with the unified roadmap rather than replacing it. Lives in <6 hrs/wk side-time budget; protects Track-C deep-work hours absolutely."
---

# Portfolio Projects for Interview Prep — Sean × 2026-05

> **What's different from the unified roadmap.** The roadmap names 5 flagship artifacts + 2 supporting artifacts as build targets through July 4. This document filters and reorders them through one lens: **what produces interview-rep signal between now and 2026-06-30**. Two of the roadmap's projects survive unchanged. Three new projects are added that the roadmap doesn't cover. Two roadmap items are explicitly deprioritized for the interview-prep window (they still ship; they just don't gate prep). The total bandwidth fits inside <6 hrs/week of evening/weekend side-time and never touches Track-C deep-work hours.

---

## Frame: the 4 prep goals these projects must hit

Each project below earns its place by lifting ≥3 of these:

1. **AI fluency** — visible working vocabulary with current agentic tooling (Bolt, v0, Cursor, Replit Agent, MCP, evals).
2. **Agentic engineering signal** — something an FDE evaluator notices in a 5-minute repo skim.
3. **Hiring-manager appeal** — a non-engineer recruiter understands the value in 90 seconds.
4. **Vibe-coding rep familiarity** — when a Bolt/v0/Cursor rep lands in a live loop, it's not alien.

The unified roadmap's existing artifacts skew heavy on (1), (2), (3). The named gap is (4) — Sean has zero public reps of "I sat in front of a vibe-coding tool with a clock running." The new projects below specifically fill (4).

---

## The 5 projects, ranked by leverage

### Project 1 — Vibe-Coding Rep Loom #1: MCP Server Visualizer in Bolt or v0 ⭐ **highest leverage**

**Why it's #1:** This is the only project that directly addresses the (4) gap — vibe-coding rep familiarity. It also produces public, recruiter-readable evidence ("yes, I can vibe-code") that hits all four prep goals at once. The decision-narration is recorded *in public*, which means it doubles as a §6 verbal-lifeline drill against the most realistic stakes available without a live evaluator.

**The deliverable:** A single-page React/TS app, built in Bolt (or v0 if Bolt struggles with the MCP stdio reference), that visualizes the 3 tools in the `intent-engineering` MCP server. User pastes an intent spec, sees which tool would run, sees a mocked tool-response payload. **Built unedited in one 45-minute session, recorded as a Loom.** No retakes; the Loom is the artifact.

**Ship deadline:** Friday 2026-05-22 (Week 3, end of solo-rep phase). Or earlier if the MCP server v0 ships ahead of 2026-05-25.

**Time budget:** 90 minutes total. 45 min build + 30 min Loom edit-and-publish + 15 min EXPLANATION.md.

**4Q `EXPLANATION.md` plan:**
- **What is this?** A 45-min unedited vibe-coding rep — a small visualizer for the intent-engineering MCP server's 3 tools, built in [Bolt | v0] with concurrent narration. The Loom is the artifact; the code is the byproduct.
- **Why this approach?** Vibe-coding is a current-table-stakes AI-PM signal. Publishing a real rep beats claiming the skill in a resume bullet. Chose Bolt over Cursor because Bolt's deploy-by-default lets the artifact be a live link, not a screenshot.
- **What would break?** (1) Bolt occasionally hallucinates Anthropic SDK shape; the rep includes the live correction. (2) The Loom is unedited — a polished version would not be the artifact. (3) The mocked tool responses are intentional; integrating live MCP stdio is v2.
- **What did I learn?** That 45 minutes is enough to ship a defensible thin slice if the scope discipline is set in the first 5 minutes. Also: that the act of recording the rep changed my prompting behavior in a useful direction — the "narrate before you prompt" habit only sticks under public-witnessing pressure.

**Portfolio-fit hook:** Unlocks the Tier-1 AI APM / PM I-II target list (Sierra, Decagon, Cursor, Replit, Glean, Scale AI, smaller AI-natives). Without this, "can you vibe-code?" is an open question; with this, the answer is a Loom link.

**Public-copy tone:** Substack post in comedic Sean Mode — title direction: "I let Bolt build my MCP visualizer in 45 minutes. It tried to install a package called `@anthropic-ai/dignity`." Sober tone on the GitHub README + EXPLANATION.md.

---

### Project 2 — Eval Harness + Golden Set for the `intent-engineering` MCP server

**Why it's #2:** Closes the F1-score landmine for the **single most-walked-through artifact** (the MCP server). Hits the "evals are the new PRDs" canon (Hamel / Shreya). Hits the "Extra Hour" north star (Agent Evals is one of the three named vectors). Lets Sean stop saying "I'd have to check" and start saying "precision on `audit_existing_spec` is 0.87 on a 15-case golden set; the false-positive mode is X."

**The deliverable:** A small `evals/` directory in `sw-mcp-intent-engineering`. Three files: `golden_set.json` (10-15 hand-graded specs with expected outputs), `run_evals.py` (or `.ts`, matching server stack), `EVAL_REPORT.md` (current scores + failure-mode analysis). Pattern lifted from Hamel's canon.

**Ship deadline:** Friday 2026-06-05 (one week after Track-C MCP v0 ships; intentionally placed after so it can grade the actual shipped server, not a draft).

**Time budget:** ~5 hours total. 2 hrs for the 15-case golden set (the hardest part — writing diverse-but-defensible specs). 1.5 hrs for the runner. 1 hr for the eval report. 30 min for the EXPLANATION.md.

**4Q `EXPLANATION.md` plan:**
- **What is this?** An eval harness for the 3 tools in `intent-engineering`. 15 hand-graded specs, deterministic scoring, per-tool precision/recall/F1.
- **Why this approach?** Because "I shipped an MCP server" without "and here's how I know it works" is the most-failed interview moment in 2026 AI PM loops. Cited Aakash Gupta failure mode directly.
- **What would break?** (1) The golden set is small and reflects my prompt distribution, not the world's. (2) F1 hides the asymmetric cost of false positives (more harmful for `audit_existing_spec` than for `generate_template`). The report flags this rather than hiding it. (3) Re-grading on every model swap is manual.
- **What did I learn?** That eval design forces the product question. The interesting work was not the runner; it was the 15 specs — deciding what counts as a "good" output is the actual PM craft.

**Portfolio-fit hook:** Unlocks the Tier-3 wildcards (Anthropic FDE, Glean FDP, Senior PM at small AI-natives where eval-design is the differentiator). Also the strongest single defense against the F1-score landmine — every portfolio walkthrough about the MCP server now has a number to cite.

**Public-copy tone:** Substack post in comedic Sean Mode — "I asked my MCP server 15 different ways if it was good at its job. Here's the score." Sober tone on the EVAL_REPORT.md and the EXPLANATION.md.

---

### Project 3 — Token Cost Calculator (ratifies roadmap Task 5)

**Why it's #3:** Closes the **only beginner skill gap** Nate-1 flagged (cost economics). Already in the unified roadmap; ratified here without modification. Hits D7-economics of the playbook rubric directly. Single HTML file means recruiter-pokeable with zero install friction.

**The deliverable:** Single HTML file at `~/Code/sw-token-cost-calculator/index.html`, deployed via Vercel. Inputs: workflow steps × model per step × token volume × frequency. Outputs: monthly cost across Haiku/Sonnet/Opus/local-model mixes + sensitivity analysis. Optional: a "demo run" button that calls Sonnet to show a live trace.

**Ship deadline:** Friday 2026-05-29 (Week 4, per roadmap Task 5 Step 3 timing).

**Time budget:** ~4 hours total per the roadmap's existing estimate. Single-file artifact; no infra.

**4Q `EXPLANATION.md` plan:** Already fully drafted inline in unified roadmap Task 5 Step 5 (lines 380-393). Paste-and-commit.

**Portfolio-fit hook:** Cross-cutting — every interview that asks "what's the cost of running this in production?" now has a live demo, not a hand-wave. Especially strong for AI-native startups where economics is real (every cycle is paid for).

**Public-copy tone:** Per roadmap — comedic Sean Mode on the Substack post; sober on the calculator UI itself (which needs to be readable as a tool).

---

### Project 4 — Personal Site `/transactions/` live with 3 artifacts loaded

**Why it's #4:** The distribution layer. Without it, recruiters who Google Sean land on LinkedIn + a stale Substack and miss the deep work. With it, the GitHub READMEs and the Substack posts both link to a canonical home that surfaces the full portfolio in one scrollable page.

**The deliverable:** Astro 5 + React islands site live at the existing personal-site domain, with `/transactions/` route loading three artifact deep-dive pages: (a) `intent-engineering` MCP server, (b) Phase D typed reasoning edges, (c) 14-agent fleet tour. Each page = embedded Loom + 4Q text + link to repo. Search and RSS deferred to v2.

**Ship deadline:** Friday 2026-06-12 (Week 6, after MCP v0 + Eval Harness + Loom #1 all exist as content to surface).

**Time budget:** ~6 hours total spread across two weeks. Astro 5 scaffolding 2 hrs, three deep-dive pages 1 hr each, copy editing + deploy 1 hr.

**4Q `EXPLANATION.md` plan:**
- **What is this?** The canonical home for the explanation artifacts. One `/transactions/` route, currently 3 deep-dive pages, growing.
- **Why this approach?** Owned distribution beats rented distribution (Substack, Medium, LinkedIn) for canon. Substack syndicates; the site canonicalizes.
- **What would break?** (1) No search yet — discovery is link-driven. (2) No RSS yet — readers can't subscribe. (3) Site-only changes don't trigger Substack syndication automatically; that's a manual paste for now.
- **What did I learn?** That the act of writing 3 deep-dive pages forced me to compare the artifacts side-by-side — and that surfaced one editorial decision (the MCP server is the *load-bearing* artifact; everything else is supporting evidence).

**Portfolio-fit hook:** Cross-cutting. Every interview-prep email, every recruiter cold reply, every "where can I see your work?" answer now has one URL.

**Public-copy tone:** Sober + minimal on the site itself. The artifacts speak; the chrome shuts up.

---

### Project 5 — Sierra-Style 2-Hour Solo Build: a new agent for the SDK fleet

**Why it's #5:** Specifically the **stamina rep** for the Sierra wildcard. The Sierra Build phase is 2 hours solo with the interviewer out of the room. Sean has never sat for a 2-hour solo build with the clock visibly running on portfolio output. This project simulates that *exact* shape with a real deliverable.

**The deliverable:** One new agent in the SDK fleet (e.g., a `weekly_portfolio_audit` agent that scans the personal site + GitHub for new commits and writes a Friday-retro-shaped report). Built start-to-finish in a single 2-hour timed window. Loom + 4Q + commit.

**Ship deadline:** Saturday or Sunday 2026-06-20 (Week 7, after all prior projects exist so the agent has artifacts to audit).

**Time budget:** 2.5 hours total. 2 hr timed build + 30 min Loom upload + EXPLANATION.md.

**4Q `EXPLANATION.md` plan:**
- **What is this?** A `weekly_portfolio_audit` agent for the SDK fleet, built in a single 2-hour timed solo session to drill the Sierra interview shape.
- **Why this approach?** Stamina is a separate muscle from the 45-min sprint. The Sierra Build phase requires sustained scope + verification discipline for 4x as long.
- **What would break?** (1) The agent currently scans only 3 surfaces (site / GitHub / Substack). (2) The audit output is markdown only; no Slack / email delivery. (3) The 2-hour scope deliberately left out failure-mode telemetry.
- **What did I learn?** That the Sierra rep tests a different skill than the 45-min rep — what's hard is *not* over-building during the long quiet middle. The discipline of "ship a smaller thing well" is harder when there's no clock pressure forcing it.

**Portfolio-fit hook:** Unlocks the Sierra (Tier-3 wildcard) specifically. Also a credible signal for any role that mentions "operational reliability" or "long-horizon agent ownership."

**Public-copy tone:** Comedic Sean Mode on the Substack — "I sat in a chair for 2 hours and built an agent that judges all my other agents." Sober EXPLANATION.md.

---

## Ranking summary

| Rank | Project | Ship date | Time | Closes which gap | Role tier hook |
|---|---|---|---|---|---|
| 1 | Vibe-Coding Rep Loom #1 (Bolt MCP visualizer) | 2026-05-22 | 90 min | Vibe-coding rep familiarity | Tier-1 AI APM / PM I-II |
| 2 | Eval Harness + Golden Set for `intent-engineering` | 2026-06-05 | 5 hrs | F1-score landmine + Agent Evals fluency | Tier-3 wildcards (FDE, FDP) |
| 3 | Token Cost Calculator | 2026-05-29 | 4 hrs | Cost economics (Nate-1 beginner gap) | Cross-cutting |
| 4 | Personal site `/transactions/` live | 2026-06-12 | 6 hrs | Distribution canon | Cross-cutting |
| 5 | Sierra-style 2hr solo build | 2026-06-20 | 2.5 hrs | Stamina-rep familiarity | Sierra wildcard |

**Total bandwidth: ~18 hours across 7 weeks = 2.6 hrs/week average.** Well under the 6 hrs/week ceiling. Loads peak around Project 4 (the site, ~3 hrs/week for 2 weeks). Track-C deep-work hours untouched.

**The single most important project — Project 1.** Every other project in this list either (a) is already in the unified roadmap unchanged or (b) layers on top of Project 1's vibe-coding-rep credibility. Without Project 1 in the bank, the playbook's portfolio walkthrough leans entirely on artifacts Sean built outside the vibe-coding context. With Project 1, the §5 walkthroughs gain a "and yes, here's me doing it cold in 45 minutes" trump card.

---

## What changes the priority

If any of these surface before 2026-06-30, re-rank:

- **A live FDE Boston interview lands in Week 2-3.** Project 2 (eval harness) jumps to #1; the eval question lands cold otherwise.
- **A Sierra recruiter reply with onsite scheduled.** Project 5 jumps to #1; the stamina rep is no longer optional.
- **The MCP server slips past 2026-05-25.** Projects 1 + 2 + 4 all wait — they depend on it. Project 3 (Token Cost Calculator) is the only project that can run regardless.
- **A Substack post hits >250 organic subscribers from a single share.** Project 4 (personal site) jumps to #1 — distribution becomes the bottleneck instead of artifact density.

---

## 10 alternatives I rejected, and why

The five projects above won by leverage. The following ten alternatives lost — each with the specific reason, anchored to either the unified roadmap or the Tier-A constraints.

1. **Build a second MCP server from scratch on a different domain** (Nate-2 Claude's `vault-knowledge-mcp`). **Rejected:** would compete with Track-C for deep-work attention. The differentiator is *one* shipped MCP server, per Karpathy's single-top-rec. A second MCP dilutes the signal and signals scope indiscipline.

2. **A new Claude Code skill or plugin.** **Rejected:** roadmap STOP-DOING list explicitly bans new skills until 2026-06-11. 117 skills is already past Sean's working-memory ceiling.

3. **Hamel's evals course (paid, 3,000-student cohort).** **Rejected:** roadmap §I scopes Week 5 to *reading* the Hamel canon, not paying for the course. Tier-A spend cap of $100 by 2026-06-11. Project 2 (eval harness) captures the value at $0.

4. **Resurrect 16BitFit Battle Mode as a portfolio piece.** **Rejected:** roadmap STOP-DOING list explicitly says hold 16BitFit paused until Nano Banana 3 ships or LoRA work resolves. Sprite-consistency hacking soaks time without producing portfolio signal.

5. **A Substack-only essay series** ("AI PM in 2026" thesis pieces). **Rejected:** writing alone doesn't drill vibe-coding muscle. Substack is a *syndication* surface for other artifacts, not a replacement. The roadmap already commits to one Substack post per Friday syndicating each artifact; an essay series is duplicative.

6. **A second sanitized portfolio artifact from Block work** (additional templates). **Rejected:** the CIIA scrub closed 2026-05-07 with a clean grep. Reopening to extract more templates is unjustified CIIA risk for marginal portfolio gain.

7. **A YouTube channel with multiple Looms.** **Rejected:** roadmap Task 6 §G defers YouTube to Week 5+ explicitly with a switch condition (at least 3 Looms must exist first). The Looms from Projects 1 + 4 + 5 can be uploaded retroactively at zero cost if the channel decision flips.

8. **Build the `comprehension-mcp` paid linter** (Nate-2 Claude's product play). **Rejected:** roadmap Decision 3 (Comprehension-as-product vs. comprehension-as-practice) defaults to practice-first, productize-only-if-demand-surfaces. No demand has surfaced. Productization is post-employment scope.

9. **An open-source contribution to a high-profile AI repo** (e.g., a PR to the Anthropic SDK or the MCP TypeScript SDK). **Rejected:** unpredictable review-cycle timing means it can't ship in ≤2 weeks reliably. The signal is real but the ship-date risk fails the constraint.

10. **Refactor the existing fleet to "production-grade."** **Rejected:** roadmap STOP-DOING list says "stop refining the 14-agent fleet structurally." Audit + Mac Mini migration (Task 6 §B) is the *only* sanctioned scope for the fleet. Production-grade refactoring eats deep-work and lifts no rubric dimension that the existing fleet doesn't already lift.

Three honorable mentions that nearly made the top 5 but didn't:

- **An adversarial prompt-injection test suite for the MCP server.** Would lift artifact-defense (D6) for the Anthropic FDE walkthrough. Cut for time — the eval harness covers most of the same ground at higher leverage.
- **A short technical post on the OPTIONAL relations pattern from Phase D.** Would syndicate well to AI-engineering audiences. Cut because the existing Phase D `EXPLANATION.md` (already drafted in unified roadmap Task 2) covers the technical content; a separate post duplicates without lifting.
- **A `prompt-rubric.md` artifact** showing how Sean writes prompts vs. how the average dev does. Karpathy-flavored. Cut because the Bolt/v0 Loom (Project 1) demonstrates this *in motion*, which beats a written rubric.

---

## How this composes with the unified roadmap

**Two roadmap items survive unchanged** as Projects 3 and 4 (Token Cost Calculator + personal site).

**Two roadmap items deprioritize for interview-prep but still ship on roadmap dates:**
- *Phase D + Phase 6 `EXPLANATION.md` commits* (roadmap Task 2). These are paste-and-commit artifacts; they ship Friday Week 1 per the roadmap. They're foundational, but they don't drill new prep signal beyond what's already there. The Loom in Project 1 and the eval harness in Project 2 carry more interview-prep leverage per hour.
- *Sanitized financial-research fleet artifact* (roadmap Task 4). Ships Friday Week 4 per the roadmap. Strong story-bank material (covered in playbook §8 Story 4) but not gating any specific role tier.

**Two roadmap items reach further than 2026-06-30 (out of scope for this document):**
- The animation pipeline + production diary (June 11 ship). Stays in the roadmap; not pulled into interview-prep because it's a creative-PM artifact, lower priority per the AI > Tech > Creative ordering.
- The Week 7 published-eval-framework artifact (conditional on Project 2 going well). Stays in the roadmap; revisited end of Week 6.

**The three new projects this document adds** (Projects 1, 2, 5) compose on top of Track-C without competing for deep-work hours. All three are evening/weekend artifacts that *use* the Track-C output (MCP server) rather than re-doing Track-C work.

---

## Self-review

**Spec coverage:** 5 projects ranked by leverage ✓. Each has deliverable + ship date + 4Q plan + portfolio-fit hook ✓. 10 alternatives rejected with reasons ✓. Total bandwidth fits inside <6 hrs/wk ✓. None touch Track-C deep-work ✓. Honors comedic-Sean-Mode public copy + sober README distinction ✓.

**Tier-A respect:**
- $100k floor: no spend recommendations ✓
- ≤3-day RTO: not implicated ✓
- AI > Tech > Creative: 4 of 5 projects are AI-native; 1 (animation pipeline) is the existing Creative anchor and is intentionally not pulled into this prep set ✓
- Track-C protected: all projects sized to evening/weekend; none pull deep-work hours ✓
- Agents draft / Sean sends: every project's public-copy step (Substack, LinkedIn, README) is explicitly Sean's review-and-publish ✓
- Friday 4:30 retro: untouched ✓
- 8:30-9:30 sacred learning, 1-2 PM break, 5:30 PM stop: untouched ✓

**Honest flags:**
- Project 5 (Sierra 2hr build) is the most likely project to slip. It requires a 2-hour uninterrupted weekend block that's harder to defend than a 90-min slot. If Week 7 looks busy, slip to Week 8 or convert to a 75-min mini-rep instead. Don't kill it — the stamina rep is the only one in this set that drills the Sierra-specific shape.
- Project 2 (eval harness) depends on the MCP server v0 being stable enough to grade. If 2026-05-25 ships but v0 has bugs, slip Project 2 by one week to let the bugs land first.

End of Phase 3.
