---
type: interview-prep-practice-plan
project: prj-job-hunt-2026
phase: interview-prep-phase-4
created: 2026-05-10
inherits_from:
  - 2026-05-10-vibe-coding-research-synthesis.md
  - 2026-05-10-vibe-coding-playbook.md
  - 2026-05-10-portfolio-projects-roadmap.md
  - HEARTBEAT.md
  - SOUL.md
  - schedule-recommendations.md
ai-context: "Phase 4 of 4. Daily + weekly + pre/post-loop practice routines, energy management, and the unshakeable-knowledge anchors. Composes with the operating-model rhythm; never violates Tier-A truths."
---

# Practice & Confidence Plan — Sean × 2026-05

> **The thesis of this plan.** Confidence isn't an affirmation; it's a pattern. The pattern is: a finite set of drills run on a finite schedule, against a finite set of known-weak-spot targets, with a debrief loop that converts each rep into the next rep's edge. The plan below is calibrated so that by the time Sean sits in front of a live evaluator in Week 5+, the only thing that's new about the situation is the evaluator. Everything else — the format, the recovery moves, the vocabulary, the artifact scripts — is already automatic.

---

## §1 — Daily warm-keep (inside the 8:30-9:30 sacred learning block)

The sacred learning hour is LEARNING ONLY (no email, no apps, no admin) per HEARTBEAT.md. The prep-specific warm-keep is a small, time-boxed slice inside that hour — typically the first 10-15 minutes — that keeps AI fluency current without crowding general learning.

**The rotation, Monday through Friday:**

| Day | Block (10-15 min) | What to consume | Time-box | Capture target |
|---|---|---|---|---|
| Mon | **Vocab rotation** | One pass through `vault/40_knowledge/eval-vocab.md` — 12 terms (precision, recall, F1, accuracy, ROC-AUC, MRR, groundedness, faithfulness, latency p50/p95/p99, token cost/call, context window, eval golden set). Read each term aloud with its one-line artifact-specific example. | 10 min | Flag any term where the example felt thin; rewrite that example tomorrow. |
| Tue | **Hamel Husain feed** ([hamel.dev](https://hamel.dev) + his Substack) | One post or one section. Lean toward the evals canon. | 12 min | 1-2 vocab terms → `vault/40_knowledge/eval-vocab.md`; 1 quote → `vault/40_knowledge/interview-vocab-quotes.md` (new file) |
| Wed | **Vocab rotation** | Repeat Monday's pass. Spaced repetition by design — second exposure within 48 hrs locks the vocabulary faster. | 10 min | Same as Monday. |
| Thu | **Aakash Gupta feed** ([news.aakashg.com](https://news.aakashg.com), LinkedIn) | One post. Lean toward AI PM interview content + 2026 format shifts. | 12 min | 1 vocab term or failure-mode pattern. |
| Fri | **Anthropic engineering blog + Latent Space** | Whatever's most recent. Skim, don't deep-read; this is the "what's the field actually publishing" pulse. | 15 min | 1 reference for §7 question-asking ("I saw your post on X — how does that land in this team's work?") |

**Once Project 2 (eval harness) ships on 2026-06-05:** swap Monday + Wednesday vocab rotation for live re-running the eval harness on the MCP server. The numbers stay fresh in Sean's head because he ran them this week. Vocab maintenance moves to passive review during Tuesday/Thursday feed-scan time.

**Hard rule:** the warm-keep ends at 8:45 AM. The rest of the sacred hour is general learning, podcasts, YouTube — whatever the day calls for. The warm-keep does not creep.

---

## §2 — Weekly reps (max 2/wk, 15:00-17:15 comms block, starting Week 3)

The cadence below maps onto Weeks 3-6 of the master plan (2026-05-18 → 2026-06-14). Track-C MCP server ships 2026-05-25, which lands inside Week 3 — so reps start with Track-C still active. The reps are deliberately scoped to be self-contained (Bolt runs in a browser tab, Cursor uses local files Sean already has) so the context-switch from Track-C is cheap.

**The 4-week schedule:**

| Week | Rep 1 (Tue 15:00-16:30) | Rep 2 (Thu 15:30-17:00) | Primary objective |
|---|---|---|---|
| **W3** (5/18-5/24) | **Bolt — Rep 1 from playbook §4 brief** (sentiment-triaging feedback widget) | **Cursor — Rep 2** (PII-redacting CSV uploader, Python/FastAPI) | First-five / last-five discipline. Narration governor. |
| **W4** (5/25-5/31) | **v0 — Rep 4** (agentic dashboard) | **Replit Agent — Rep 3** (mini-RAG over local Markdown) | Tool-mocking speed. 15-second audit rule. |
| **W5** (6/1-6/7) | **Live partner mock — Cursor backend** (45 min + 15 min debrief) | **Portfolio walkthrough self-record** (5-min Loom on the MCP server using §5 script) | External pressure. Verbal lifeline drill. |
| **W6** (6/8-6/14) | **Take-home simulation** — 2-hour Stripe/Netflix-style brief, deployed prototype | **Adversarial live partner mock** — partner mid-build curveball | Stamina + adversarial recovery. |

**Success criteria per rep:**

Use the playbook §2 rubric (7 dimensions). Score 1-5 on each within 10 minutes of the rep ending while memory is fresh. Target by Week 5: 4 or higher on every dimension. **Any 1 or 2 on a dimension is a re-rep trigger** before moving to the next tool.

**The drill that closes the over-narration weak spot — the "narration governor":**

Before every Week 3-4 solo rep, set a kitchen timer for 30 seconds. Every time Sean types a new prompt into the AI tool, the timer resets. If verbal narration exceeds 30 seconds for a single build step, the timer beeps and Sean's hands go back to the keyboard. The goal is the rhythm, not the rule. By Week 5, the rhythm is internalized and the timer goes away.

**The drill that closes the freeze weak spot — the "verbal lifeline":**

Three times per rep (at min 10, min 25, min 40 — or whenever silence stretches past 30 seconds), Sean says aloud:

> "Let me restate where I am — I have [X] working, [Y] is in progress, the next prompt I want to try is [Z]."

Even when not stuck. The point is to make the move automatic so it fires under pressure without thought. By Week 5, this should feel as natural as a swimmer breathing on the third stroke.

**The drill that closes the Python/TS weak spot — the "I read this and chose to keep it" sentence:**

For every block of AI-generated code accepted into the build, Sean says aloud: "I read this and chose to keep it because [one specific reason]." Forces the verification audit. Forces the vocabulary into use. Catches "I don't actually know what this does" before the build depends on it.

---

## §3 — Weekly mocks: how to ask Mary, Matt, Larry

Self-evaluation hits a ceiling around end of Week 4. The Week 5 graduation is bringing in a human evaluator. The three named critical-path collaborators each get a different ask, calibrated to their actual strengths — not a one-size-fits-all "interview me."

### Mary — domestic mock (Weeks 3-4, low-stakes)

**Why Mary first:** she lives with the prep load and is the lowest-cost external ear. Asking her to "interview" Sean introduces a partner-relationship dynamic that pollutes the signal. Asking her to *observe* avoids that.

**The ask, verbatim or adjusted to feel natural:**

> "I'm running practice reps for AI-PM interviews — 30-45 minutes me building something in front of a clock. Would you sit in the room for 20-30 min of one this week and tell me three things you couldn't follow? Not 'was it good' — specifically: where did I lose you? You don't need to know what the code is; you just need to be a person whose attention I'm trying to hold."

**What to give her:** nothing. No brief, no rubric. The whole point is "could a smart non-technical observer follow your reasoning?" — which is half the actual interview signal anyway.

**Cadence:** once in Week 3, once in Week 4. Don't ask in Week 5 — she's already absorbing the prep-week stress; preserve her bandwidth.

### Matt Vitebsky — adversarial mock (Week 5)

**Why Matt:** ex-Block CPO. Knows Sean's PM craft from inside. Technical-enough to ask real follow-ups. Already offered "anywhere" referrals — relationship is warm enough to ask for 60 min.

**The ask, paste-ready (Sean's review-and-send per Tier-A "agents draft, Sean sends"):**

> "Matt — I'm 4 weeks into interview prep and I need to drill against someone who'll actually push. Would you do a 60-min mock with me? Shape: I share a vibe-coding brief, I build for 45 minutes in Bolt or Cursor with concurrent narration, you ask 1-2 mid-build curveballs (changed spec, adversarial follow-up, your choice). Then 15 min of debrief — the rubric is in my prep doc, I'll share before we start. Aiming for [specific week, e.g., 'the week of June 1']. Best window for you?"

**What to give him in advance:** the playbook §2 rubric (7 dimensions, signals), one sentence on the failure modes he should look for ("I over-narrate when nervous; please tell me if you see it"), and one of the playbook §4 briefs as the rep brief.

**What to receive without spiraling:** the rubric scores + one specific observation per dimension. If Matt's feedback lands as "you did fine," that's a missed opportunity — push back gently with "the most useful thing is the lowest score. Where did I weakest?" Frame the ask so the honest answer is *easier* than the polite answer.

### Larry Cermak — referenced rep (Week 5-6, role-specific)

**Why Larry differently:** primary reference + warm-intro source. His leverage is *not* the same as Matt's. Larry is best positioned to introduce Sean to someone in his network who's recently run an AI-PM vibe-coding loop — and that person is a more credible adversarial mock-evaluator than Larry himself.

**Two options, sequenced:**

**Option A — Direct ask (lower leverage):** Behavioral mock, not vibe-coding. Larry's strength is executive-level conversation. The ask:

> "Larry — when I get a behavioral round in a Tier-2/3 loop, I'd love your read on the answers. Would you do a 30-min mock — you ask 4 standard senior-PM behavioral questions, I answer, you score? Aiming for [week]. I'll share the role / company beforehand."

**Option B — Gatekeeper ask (higher leverage):**

> "Larry — quick ask. Do you know anyone in your network who's run an AI-PM vibe-coding interview loop in 2025 or 2026? I'm running mock reps and the highest-signal evaluator is someone who's been on the receiving end recently. Even a 30-min Zoom would be enormous."

**The play:** ask Option B first. If it surfaces a name, take it. If Larry doesn't have an immediate name, fall back to Option A at a later date. Don't ask both at once — overloads the request and reads as needy.

---

## §4 — Pre-loop ritual stack

The ritual is calibrated against Sean's known patterns (works best in the morning, mandatory break, sleep matters, no novel inputs day-of). Specifics so Sean can execute without thinking.

### T-24 hours

- **Sleep target:** 7.5 hours minimum. In bed by 10:30 PM the night before. No exceptions for "one more prep pass."
- **Loop-prep brief written:** one markdown page in `vault/20_projects/prj-job-hunt-2026/interview-prep/loops/<YYYY-MM-DD>-<company>-<loop-#>.md`. Includes: company 90-sec summary, role 1-pager, panel names + LinkedIn skims (1 line per panelist), the 4-question §7 always-ask list with one customized per panelist, the §6 verbal-lifeline script copied verbatim.
- **Logistics test:** Zoom / Meet / whatever platform the loop is on — open it, screen-share test, mic test, camera angle. Test the actual link they sent, not a generic test.
- **Outfit decided.** Doesn't matter what; just decided. Decision-fatigue cleared.
- **Workspace tidy.** Visible space behind the laptop. One water glass on the desk. Phone in another room.
- **No new inputs after 8:00 PM.** No new podcast on AI, no new vocab term, no new framework. Day-before is consolidation, not acquisition.

### T-1 hour

- **Light meal 60-90 min before.** Whatever the staple is (oats, eggs, sandwich) — never something new. No heavy carbs that crash.
- **Water on the desk, room temperature.** Cold water spikes adrenaline.
- **20 minutes of calming music** (Sean knows what his pre-game playlist is — if there isn't one yet, pick it this week so it's ready).
- **5-minute quiet review of playbook §2 (rubric) and §6 (recovery).** Read the verbal lifeline script once aloud. Stop reading after 5 min — no more cramming.
- **Bathroom 20 min before.** Logistics matter.
- **Walk for 5 min if at home.** Get the heart rate up gently. Don't sit at the desk waiting.

### T-5 minutes

- Phone face-down, notifications off across Slack, Discord, iMessage.
- Water glass within reach.
- Camera angle confirmed.
- The grounding sentence — said aloud, alone, before joining the call:

> "I've shipped the work. The work is the proof. I'm here to be evaluated, not to perform."

This is not affirmation. It's a frame-setting sentence. The work *is* shipped. The evaluator is going to see the work either way. The next 45-60 minutes is a measurement, not a creation event.

---

## §5 — Post-loop debrief

The debrief is where reps compound. Without it, every loop is a one-shot. With it, every loop is a data point in a series.

### The 5-question template

1. **What was the strongest move in the rep — the moment the evaluator most likely scored high?** (Forces noticing what worked. Confidence compounds on noticed wins.)
2. **What was the lowest-confidence moment — the moment I felt the freeze, the doubt, or the over-narration coming?** (Surfaces the next drill target.)
3. **What did I learn about the company or role that I didn't know going in?** (Forces extraction of non-prep-related signal. Even a "no" interview produces useful intel.)
4. **What's one rubric dimension I scored below 3 on, and what's the specific drill that fixes it?** (Converts a felt sense into a Phase 2-aligned next step. Forces specificity.)
5. **What's the next decision — apply lessons after the 24-hour cool-down, or set aside?** (Cool-down rule below.)

### The 24-hour cool-down rule

**Do not apply lessons from a loop within 24 hours of the loop ending.** Adrenaline + recency bias produce overcorrection. The loop ends, the 5-question debrief gets written, the file is closed. Adjustments to the Phase 4 plan (vocabulary additions, new drill targets, schedule tweaks) happen the next morning during the 8:30-9:30 block, with cooler eyes.

The one exception: a logistical fix (the Zoom link was wrong, the camera was angled badly, the mic cut out) gets fixed immediately. Anything cognitive or skill-based waits.

### Journal home

`vault/20_projects/prj-job-hunt-2026/interview-prep/debriefs/<YYYY-MM-DD>-<company>-<loop-#>.md`

One file per loop. Frontmatter includes company, role, panelist names, format (45-min Bolt / portfolio walkthrough / 2-hour Sierra / etc.), and a `next_decision` field set in question 5. The Friday retro reads through any new debriefs filed during the week.

### What gets shared with Mary

Sean's choice. Tier-A says Mary gets honest signal, never a polished version — so whatever lands in the debrief, the *headline* gets surfaced (one-sentence summary + the lowest-confidence moment). The full debrief stays in the vault.

---

## §6 — Energy management

Interview-prep weeks are the most likely weeks for the over-prep / anxiety spiral. The spiral signal isn't intensity — it's *displacement*. Sean prepping hard is normal. Sean prepping *instead of* doing other Tier-A work (Track-C, Mary check-ins, the 5:30 PM hard stop) is the warning.

### The weekly check-in question

In every Friday 4:30 retro:

> **"Did this week's prep produce a concrete artifact, or did it produce a feeling of having prepped?"**

Artifacts in this context are: completed reps with scored debriefs, new vocabulary entries, a new drill identified, a logistics fix made. *Feelings of having prepped* are: re-read the playbook three times, re-watched the same Loom, mentally rehearsed the same story. The first set compounds; the second doesn't.

### The anxiety-spiral signals (any one is a flag)

- Reading the playbook more than twice in 24 hours.
- Practicing the verbal lifeline more than 5 times in 24 hours (memorization beyond 5 reps is diminishing returns + reads rehearsed in the actual loop).
- Postponing a Track-C build session "to prep more."
- Skipping the 1-2 PM break to prep.
- Eating dinner alone at the desk during interview weeks.
- Asking Mary a third time how the prep is going in the same evening.

### Recovery rituals beyond the Friday retro

- **The gym pre-8:30 AM** is already a sacred block. In interview weeks, do not skip it for "more prep time." The cortisol burn-off compounds.
- **The 1-2 PM break.** In interview weeks, take it *out of the workspace*. Walk outside, even for 10 minutes. The break is how Sean stays human under load.
- **The 5:30 PM hard stop.** Sacred under Tier-A. The exception is *not* "an interview is tomorrow." If the prep isn't done by 5:30, the prep isn't done.
- **Sunday evening Mary check-in.** Explicit verbal: "How's the load on you this week? Where am I leaning too hard on you that I shouldn't?" Once a week. Don't make it a daily question — that's a different kind of load.

### Family-context awareness

Mary is named as critical-path collaborator in SOUL.md. During interview weeks, Mary's load goes up — emotional surface, decision-support volume, partner-grade transparency. The plan respects this in two specific ways:

1. **The 5:30 PM hard stop does not move for an interview.** Mary deserves the evening regardless.
2. **Sunday evenings stay protected from prep work** unless an explicit loop lands Monday-Tuesday. If Sunday evening is needed for prep, Sean states it explicitly Friday: "Loop on Monday morning. Sunday evening I need 90 min for last-pass prep. Want to plan dinner around it?" Predictability reduces load more than capacity does.

---

## §7 — The "I'm prepared" mental model: 5 unshakeable anchors

These are the things Sean *knows* going into any loop such that, even if a curveball lands, he can respond from a grounded place rather than panic. Each anchor is hyper-specific to Sean's actual portfolio. None are generic.

### Anchor 1 — "I've shipped (or am about to ship) one MCP server. The Karpathy single-top-rec is in my hands."

The differentiator artifact exists. It's the named 2026 career artifact per Karpathy and per Sean's own operating-model. Sean has done the work the field is asking for. The next question is not "do I have the artifact" — it's "how do I describe it well." Phase 2 §5 has the script.

### Anchor 2 — "I have the verbal lifeline. I've drilled it. I can run it from a blank state."

Even if Sean freezes — even if the curveball is unfamiliar — the lifeline is automatic by Week 5: "Let me restate where I am — I have [X] working, [Y] is in progress, the next prompt I want to try is [Z]." This converts a silence-blow-up into a decision-narration moment in one move. The drill is in §2; the script is in playbook §6. The freeze isn't a failure if the recovery is automatic.

### Anchor 3 — "I have numbers. Precision on `audit_existing_spec` is [X] on [N] specs. The fleet costs ~$0.40/morning. The vault index serves ~15k chars in <5 sec."

The F1-score landmine doesn't fire on Sean. Every artifact in the portfolio has at least one *concrete number* attached to it. When an evaluator asks the metric-defining question, Sean doesn't say "I'd have to check" — he cites the number. This anchor compounds with Project 2 (eval harness) in Phase 3.

### Anchor 4 — "I'm not selling tenure. I'm selling demonstrated work."

The 2-year titled / 4-6 year portfolio gap is reframed into a strength: Sean is *less* asking the interviewer to imagine the work and *more* showing it. Every behavioral story in playbook §8 leads with an artifact, not a year. When a panelist asks "tell me about a time you led a project" — the answer is "let me show you the project," not "in my X years of PM experience." Anchor 4 inoculates against the tenure asymmetry that would otherwise read as junior.

### Anchor 5 — "The work has a canonical home. The interviewer can see it after the loop without my help."

Personal site `/transactions/` is shipped (Project 4). Every artifact has a 4Q `EXPLANATION.md` co-located in its repo. Substack syndicates. LinkedIn distributes. Whatever happens in the loop, the work is durable + linkable + recruiter-readable cold. The loop is a measurement event, not a sales event — because the sale is already made by the artifacts.

---

## §8 — Negotiation prep — note as Phase 5 future scope

Negotiation discipline matters but lands at offer time (Week 8+). It belongs in a Phase 5 plan, not Phase 4. The reason for the explicit note: tempting to want to "feel ready for everything" during prep weeks, which pulls energy away from the load-bearing skill (vibe-coding rep familiarity + portfolio walkthrough fluency). Hold the line.

**One Phase 4 carry-over for negotiation:** the walk-away ($100k base, with Tier-A override conditions of Anthropic-specifically or $250k+ anywhere) is already pre-decided in SOUL.md. Sean does not need to relitigate the walk-away during a loop. If asked "what are your salary expectations?", the answer is the pre-decided answer. No improvisation needed.

---

## §9 — How this plan composes with the master plan + unified roadmap

- **Daily warm-keep (§1)** lives inside the existing 8:30-9:30 sacred learning block. Doesn't add a new sacred block; refines what fills the existing one.
- **Weekly reps (§2)** live in the existing 15:00-17:15 comms block, 2/wk max, Weeks 3-6 per the unified roadmap practice cadence.
- **Weekly mocks (§3)** live inside the same comms block. Mary mocks are flexible-scheduled. Matt + Larry mocks are explicit calendar invites.
- **Pre-loop ritual (§4)** consumes a 2-hour window (T-1 hour ritual + the loop itself). Slot it into the day plan around the loop time.
- **Post-loop debrief (§5)** is a 15-30 min file write within 1 hour of the loop ending. Should not violate the 5:30 hard stop — if a loop runs late, debrief the next morning during the 8:30 block (and skip the warm-keep that day).
- **Energy management (§6)** integrates with the Friday 4:30 retro (existing sacred block) and the Sunday Mary check-in (new sacred touchpoint specifically for interview weeks).
- **"I'm prepared" anchors (§7)** are passive — they don't consume time. They exist so Sean can read them before a loop and the prep work feels like the foundation it is.

**Total new bandwidth introduced by Phase 4:** 0 hours. Everything fits inside existing sacred blocks (learning hour, comms block, Friday retro). The plan doesn't ask for new time; it asks for sharper use of the time that's already there.

---

## §10 — The first week of this plan (Week 3, 2026-05-18 to 2026-05-24)

Sean's actual Week 3 looks like this:

- **Mon 5/18:** Warm-keep — vocab pass. Track-C MCP work continues.
- **Tue 5/19:** Warm-keep — Hamel feed. **Rep 1 (Bolt, sentiment widget) 15:00-16:30.** Score self on rubric, file debrief if it counts as a practice debrief.
- **Wed 5/20:** Warm-keep — vocab pass. Track-C deep work.
- **Thu 5/21:** Warm-keep — Aakash feed. **Rep 2 (Cursor, PII redaction) 15:30-17:00.** Score + debrief.
- **Fri 5/22:** Warm-keep — Anthropic blog. **Ship Vibe-Coding Rep Loom #1 (Project 1 from Phase 3).** Friday 4:30 retro — first time using the "did this week produce an artifact or a feeling?" question.
- **Sat 5/23 / Sun 5/24:** Open per HEARTBEAT. Track-C if needed. Sunday Mary check-in.

Done correctly, Week 3 ends with: two rubric-scored reps in the bank, one shipped public Loom, eval vocabulary already harder to forget than it was Monday, and the verbal lifeline drilled six times in two real reps. That's the pattern. Repeat for Weeks 4, 5, 6.

End of Phase 4. End of the interview-prep prep cycle. The next move is the rep on Tuesday 5/19.
