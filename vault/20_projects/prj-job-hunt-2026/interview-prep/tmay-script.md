---
type: interview-prep
artifact: tmay-script
project: prj-job-hunt-2026
status: draft
created: 2026-05-30
related:
  - story-bank.md
  - tmay-per-company-variations.md
  - ../onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md  # Task 17
ai-context: "TMAY (Tell Me About Yourself) 2-minute script, Aakash Gupta 4-part structure: Hook (15s) -> AI Inflection Point (30s) -> Proof Points (45s) -> Why Here (30s). Sets the frame for every interview through the gate. Proof points pull from story-bank.md. Per-company Why-Here swaps + the layoff-question handling live in tmay-per-company-variations.md. Verification: 2:00-2:30 spoken, Council grader 8+/10 on all 8 dims x3."
---

# TMAY — "Tell Me About Yourself" (2-Minute Script)

> **Why this is the single most-rehearsed artifact in the prep.** TMAY is the first question in ~90% of interviews and it sets the frame for everything after. A good TMAY makes the interviewer ask the follow-ups *you* want. The structure below is Aakash Gupta's 4-part AI-PM frame: **Hook → AI Inflection Point → Proof Points → Why Here**. Total target: **2:00–2:30 spoken** (~300–340 words).
>
> **The spine.** This script is the **AI-evangelist → AI-native-operator arc** made into 2 minutes: *I was the person pushing AI inside orgs that wouldn't build it; the Block layoff was the inflection; so I went and built the proof myself.* Every proof point is something an interviewer can install or visit.
>
> **One factual flag before you say this in a room:** the Hook references your pre-Block history. Confirm the NYL title/years (see `story-bank-source-material.md` ground-truth table) so the timeline is bulletproof under follow-up. Bracketed `[CONFIRM]` spots are where you must verify, not improvise.

---

## The script (delivery version)

> Read the **bold** at full voice; the rest is connective tissue. Slashes `/` mark breath/beat points. Bracketed timings are cumulative targets.

### 1 — Hook (0:00–0:15)

> **"I'm a product manager who came up through a decade of creative and multimedia work, / then pivoted hard into AI. / Most recently I was an Associate PM on the technical side at The Block, a crypto-media company — / and across that role and the years before it, I was almost always the only person in the room actively pushing AI into the work."**

*Beat. Let "only person in the room" land — it sets up the inflection.*

### 2 — AI Inflection Point (0:15–0:45)

> **"The thing I kept running into was a gap between how fast AI was moving and how slowly the orgs around me would adopt it. / I was evangelizing — and getting nowhere fast. / Then in early May I was laid off in a cost-cutting round. / And instead of treating that as a hole in my timeline, I treated it as the inflection: / if the orgs wouldn't build it, I'd go build it myself, in public, with real artifacts — / and pivot from 'AI evangelist' to 'AI-native operator who can prove it.'"**

*This is the weakness-flip. One factual sentence on the layoff, then immediately the pivot. Do not dwell.*

### 3 — Proof Points (0:45–1:30)

> **"So over an eight-week sprint I shipped three things I can hand you right now. / One — an MCP server called intent-engineering, live on npm and the public registry, that audits and scaffolds agent specs; / I dogfooded it on my own hundred-plus skills and published the score. / Two — an eval suite for one of my own agents that I shipped intentionally red, at one out of ten, / grounded in seventeen days of real failure logs, and drove up from there — because a green scorecard on day one is a lie. / Three — a control architecture: a judge layer that sits between my autonomous agents and any action they take, / so I can say I don't just have agents, I run actors inside a control architecture."**

*These three map to Story-Bank Stories 2, 1, and 5. Each is install-able or visit-able — that's the non-fakeable part.*

### 4 — Why Here (1:30–2:00)

> **"And that's exactly why I'm talking to you. / The work your team is doing on [SPECIFIC PRODUCT SURFACE] is the kind of [agent-platform / context-engineering / vendor-eval / forward-deployed] work / I've been trying to ship from the outside for months. / This role is where my evangelism arc graduates into named accountability — / I'd rather build this inside your team than keep proving it solo."**

*The `[SPECIFIC PRODUCT SURFACE]` and the bracketed archetype swap per company — full table in `tmay-per-company-variations.md`. Never deliver the default placeholder; if you don't have the swap ready, you're not ready for that interview.*

---

## Why each section is built this way

| Section | Job it does | Rubric dimension it targets |
|---|---|---|
| **Hook** | Locates you fast (creative → PM → AI) and plants "only one in the room" — the seed of the whole arc. | Structure, memorability |
| **Inflection** | Handles the layoff *on your terms* before they ask, and converts it to momentum. | Weakness-flipping, information control |
| **Proof Points** | Three install-able/visit-able artifacts with hard numbers — the non-fakeable core. | Impact specificity, memorability |
| **Why Here** | Makes it about them; turns the arc into a reason to hire, not a story about you. | Structure, confidence |

---

## Delivery notes (the 8-dimension targets)

- **Timing:** 2:00–2:30. Off by >20% (under 1:36 or over 2:24 on the 2:00 read) loses points. Time every rep.
- **Filler:** under 3 "um/uh/like/you know" per minute. The slashes are your breath points — use them instead of fillers.
- **Confidence:** no hedging on the numbers. "One out of ten" and "thirteen days early" are said flat and certain.
- **Information control:** the layoff is **one sentence, factual, cost-cutting**. You never volunteer more. If they probe, the per-company file has the contained answer.
- **Weakness-flipping:** the entire inflection section *is* the flip — practice the pivot from "laid off" to "so I went and built it" as a single breath.
- **Memorability:** the quotable line is **"I don't just have agents, I run actors inside a control architecture."** That's the sentence they repeat to the next interviewer. Land it clean.

---

## Verification gate (Task 17)

- [ ] Script runs **2:00–2:30** spoken (time 3 reps).
- [ ] Council `interview_grader` hits **8+/10 on all 8 dimensions, 3 consecutive attempts** — *gated on the Task 19 rig being live.*
- [ ] Hook timeline facts confirmed (NYL title/years).
- [ ] At least the top-5 target companies have a filled `Why Here` swap in the per-company file.

## Open items

- ⚠️ **NYL specifics** — confirm before delivery; the Hook leans on the pre-Block history.
- 🔲 **Council grading** — run once the Task 19 mock-interview rig ships (it's overdue; that's the next code task in this cluster).
- 🔲 **Proof-point swap** — if a given interview is heavy on a 4th artifact (e.g. the live Fleet Dashboard at fleet.seanwinslow.com), you can sub it into Proof Point 3; keep the count at three.
