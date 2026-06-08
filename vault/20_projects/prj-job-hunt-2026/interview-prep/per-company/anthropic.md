---
type: interview-prep
artifact: per-company-packet
company: anthropic
role: Forward Deployed Engineer, Applied AI (Boston / NYC)
project: prj-job-hunt-2026
status: draft
created: 2026-06-08
related:
  - ../tmay-script.md
  - ../tmay-per-company-variations.md
  - ../story-bank.md
  - ../../../../40_knowledge/references/ref-anthropic-pm-interview-guide.md
  - ../../onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md  # Task 32
ai-context: "Self-contained Anthropic interview prep packet (Task 32, target #1). Anchored on the Forward Deployed Engineer / Applied AI role (Sean's tracker target), built on the universal core of the Insider Loops Anthropic interview guide + Sean's TMAY + 7-story bank. Designed so Sean can run a full mock from THIS file + story-bank.md alone and self-grade against the Task 19 8-dimension rubric. Source JD verified live 2026-06-08 (greenhouse 4985877008)."
---

# Anthropic — Interview Prep Packet

> **Target role:** Forward Deployed Engineer, Applied AI — Boston / NYC (Greenhouse `4985877008`). This is the "crown jewel / would-relocate" target in [[../../target-companies|target-companies]] and the override-condition company in your operating model.
>
> **How to use this packet.** It's built to be self-sufficient: you should be able to run a full mock interview from this file plus [[../story-bank|story-bank.md]] alone, then grade yourself on the 8 dimensions (§8). Read §0 first — it's the strategic frame the rest hangs on. Drill §2 (mission/values) and §3 (Why Anthropic over OpenAI) until they're reflex; those are table stakes and the #1 documented rejection reason. The rounds in §4 are where you actually win or lose.

---

## §0 — Role reality check (read this first)

**The honest fit map.** FDE / Applied AI is the one Anthropic role where your portfolio maps *1:1 to the job description*. The JD names your deliverables verbatim:

> *"Deliver technical artifacts for customers like **MCP servers, sub-agents, and agent skills** that will be used in production workflows."* — Anthropic FDE JD, verified 2026-06-08

You have shipped **two** public MCP servers (`intent-engineering`, `vault-knowledge`), a fleet of sub-agents, and a skills library. No other candidate's "what I built on weekends" overlaps the JD this cleanly. **That is your single biggest edge here — lead with it.**

**But be honest about what this role is.** FDE is an *engineering-leaning, customer-facing* role, not a classic PM role. The bar the JD sets:

| JD requirement | Your evidence | The honest gap to preempt |
|---|---|---|
| Ship **MCP servers / sub-agents / agent skills** to customer production | Two published MCPs + 17-agent fleet | None — this is your strength. Lead here. |
| **4+ yrs technical, customer-facing** (FDE / SWE-with-consulting) | ~10 yr NYL AI-evangelist/operations, APM at The Block | You haven't held the "embedded-at-a-customer" title. Bridge: your evangelist arc *is* forward-deployment inside non-AI orgs. |
| Production LLMs: **prompt eng, agent dev, eval frameworks, deployment at scale** | Eval suites grounded in real logs, judge layer, HybridRouter | "At scale / in enterprise customer environments" is the stretch. Don't overclaim — say "solo at fleet scale," then ask how they scope scale. |
| **Strong Python**, shipping production apps | Agent SDK fleet in Python; MCP servers in TS | Real, but you self-describe as "coding fundamentals." Be precise about what you write vs. what you orchestrate — don't bluff depth. |
| Operate **autonomously, under ambiguity**, ~25% travel | The entire 8-week solo sprint is the proof | None — your build-in-public sprint is the literal evidence. |

**The positioning line for the whole loop:** *"I've shipped the exact artifacts your JD names — MCP servers, sub-agents, skills — solo and in public. I'm not coming in to learn the stack; I'm coming in to do at customer-scale what I've been doing on my own fleet."* Then let them probe the scale/tenure gap honestly — don't paper over it.

**FDE-vs-PM note (decide consciously).** The guide you're prepping from is Anthropic's *PM* interview guide. The FDE loop will differ — it'll be **more engineering** (expect a coding / technical build component) and **less product-strategy take-home**. But three things are identical across *every* Anthropic role and are the highest-risk filters regardless: the **Culture Interview** (§4b), **mission alignment / Why-Anthropic** (§2–§3), and **live Claude fluency** (§4c — which for an FDE is literally the job, not a side test). So this packet leans on the universal core and flags PM-only rounds where they appear. **First action when a recruiter engages: ask them to walk you through the exact loop shape for FDE** — the guide says good recruiters customize, and it changes what you drill.

---

## §1 — The loop at a glance

Anthropic runs **6 stages**, and unlike a FAANG loop there's no single gate — there are *multiple independent elimination points*. Passing five rounds and failing one ends it.

| # | Stage | Format | Applies to FDE? |
|---|---|---|---|
| 1 | Recruiter Screen | 20–30 min call | Yes — mission ignorance = auto-reject |
| 2 | Hiring Manager Screen | 20–60 min, the Applied-AI HM | Yes — last gate before the exercise |
| 3 | Take-home / exercise + defense | take-home + live defense | **Likely a technical/build exercise for FDE**, not the PM product-proposal take-home. Confirm with recruiter. |
| 4 | Onsite Loop | 5–6 interviews, ~7 hrs over 1–2 days | Yes |
| 5 | Team Matching | profile circulated to team leads | Maybe — FDE may be specific-team (faster) rather than talent-pool |
| 6 | Offer | — | — |

**The three highest-risk eliminators (memorize these):**

1. **Mission ignorance at the recruiter screen** — a technically brilliant candidate was rejected for a generic "I want to transition into AI" answer. *Documented.* (§2, §3)
2. **The Culture Interview** — rehearsed STAR stories are Anthropic's stated **#1 failure mode**. The instincts that win at other companies actively lose here. (§4b)
3. **Live Claude fluency** — if you can't write a prompt and iterate on bad output live in front of someone, no amount of product-sense prep saves you. For FDE this is the *core job sample*. (§4c)

---

## §2 — Mission & values (table stakes — tested at every stage)

This is not just Culture-Interview material. Mission alignment is scored **independently at every stage**, and falling short at any one can end the candidacy. You need to *operationalize* these, not recite them.

### The 7 core values (know all 7 — #7 is the one candidates miss)

1. **Act for the global good** — zoom out to societal/second-order consequences, not just user-level.
2. **Hold light and shade** — *the most distinctive value.* Pure optimists AND pure doomers both fail. You must hold a specific risk AND a specific benefit at the same time.
3. **Be good to our users** — expand "user" past the button-clicker: policymakers, employees, affected communities.
4. **Do the simple thing that works** — over-engineering is penalized. *"We don't invent a spaceship if all we need is a bicycle."* (This is *your* "intercept, don't rebuild" instinct — Story 5.)
5. **Be helpful, honest, and harmless** — applies to the *org*, not just the model. *"High-trust, low-ego."* Be honest about failures without spin.
6. **Put the mission first** — the screening question: *"Would you accept your equity going to zero if Anthropic withholds a model for safety?"* They declined a **$200M Pentagon contract** on principle.
7. **Ignite a race to the top on safety** — the game-theory one. *Why* publish safety research that helps competitors? *Why* advocate standards that constrain your own products? Have a view.

### Core Views on AI Safety — the WHEN / WHY / WHAT / HOW spine

- **WHEN:** transformative AI / AGI possible this decade.
- **WHY:** technical alignment **AND** societal disruption (most candidates only name technical risk — naming both is the tell of someone who actually read it).
- **WHAT:** a *portfolio* approach across optimistic / intermediate / pessimistic scenarios.
- **HOW:** empiricism — *"we do not know how to train systems to robustly behave well."* **Mirror that "we do not know" honesty in your own reasoning.** It's the intellectual-honesty signal they screen for.

### RSP v3.0 — the live controversy you WILL be asked about (don't dodge)

The Responsible Scaling Policy is Anthropic's self-imposed ruleset tied to **AI Safety Levels (ASLs)**. **v3.0 (Feb 2026)** removed some hard limits earlier versions treated as absolute → public controversy. ASL-3 safeguards activated May 2025; CSO **Jan Leike** called prior limits *"naive"*; a Safeguards lead resigned.

> **The move:** do **not** defend or condemn it. Engage with the genuine difficulty — *maintaining safety commitments while competing against companies with none.* That tension **is "Hold light and shade" in action.** Candidates who dismiss either side fail.

### Constitutional AI — know it without the jargon

Two-phase training (self-critique + RLAIF) producing a priority ordering: **safe > ethical > compliant > helpful.** If you can't explain CAI *without saying "Constitutional AI,"* you don't understand it yet. Plain version: *"You write the principles down explicitly and train the model to critique itself against them, instead of hoping good behavior is implicit in human feedback."*

### Product leadership (reference the model, not the names, in answers)

Ami Vora (Head of Product), Scott White (Head of Product, Claude), Cat Wu (Head of Product, Claude Code). Team model is **four-legged: PM + Designer + Engineer + AI Researcher.** Cat Wu: *"PMs build prototypes and evals"* — which is *exactly* your story (you build evals).

### The "stock-to-zero" question — how to answer honestly

Don't perform conviction. The honest frame: *"That's hard to answer truthfully before it's real. But the reason I'm drawn here over a competitor is that the mission is **structural** — PBC status, the founders' wealth pledge, walking away from a $200M Pentagon contract. Structure is what makes me believe the commitment survives the moment it's expensive."*

---

## §3 — "Why Anthropic over OpenAI" (must survive 3 rounds of "but OpenAI does that too")

This question goes 3+ follow-ups deep in the Culture Interview and recruiter screen. Expect *"OpenAI also does that"* and *"OpenAI does free models to democratize access — how is Anthropic different for you?"* Build a position with layers so each pushback has an answer.

**Your layered answer (drilled in your own voice, not memorized):**

- **Layer 1 (structural, not vibes):** *"It's not that Anthropic talks about safety more — it's that they operationalized it. The RSP is a self-binding commitment with thresholds. The PBC charter and the Pentagon-contract refusal are structural, not marketing."*
- **Layer 2 (when they say 'OpenAI has a safety team too'):** *"They do. The difference I weight is the **race-to-the-top** value — publishing interpretability and safety research that helps competitors. That's costly and only makes sense if safety is the actual mission, not a feature."*
- **Layer 3 (when they say 'OpenAI democratizes access with free models'):** *"Access and meaning are different problems — I actually wrote an essay on this. Free access to a system nobody can govern isn't obviously good. I'd rather ship the boring control layer that makes a powerful model safe to deploy than maximize raw reach."* ← ties to your **Access-over-Meaning manifesto** + the **judge layer**.
- **Layer 4 (the personal hook — why YOU, now):** *"Reading 'Machines of Loving Grace' reframed how I think about the 5–10-year horizon. I spent a decade as the only person pushing AI inside orgs that wouldn't build it. This is the one place where the thing I care about — agents that act with intent, inside a control architecture — is the actual mission, not a side quest."*

**Do not say:** "AI is the future," "I'm passionate about AI," anything that would fit on any AI company's application.

---

## §4 — The 5 rounds that decide it

### §4a — Recruiter Screen (filter: low, but mission-ignorance is auto-reject)

The recruiter is screening four things. Have a <2-min answer for each:

1. **Credibility** — one or two projects, specific. *"I built and published `intent-engineering`, an MCP server on npm and the public registry that audits and scaffolds agent specs — I dogfooded it on my own 100+ skills and published the score."* (NOT "I've been a PM for X years and I'm excited about AI.")
2. **Timing** — why now. Your layoff → inflection arc, one factual sentence on the layoff, then the pivot. (See the contained layoff answer in [[../tmay-per-company-variations|tmay-per-company-variations]].)
3. **Mission understanding** — §2/§3. *This is the auto-reject dimension.*
4. **Contribution** — what you'd *create/own*, not manage. *"I'd want to own the repeatable-deployment-pattern problem — turning customer engagements into reusable MCP/sub-agent scaffolds, which is literally what the JD's last bullet asks for."*

**After the call, ask the recruiter:** the exact FDE loop shape, whether it's a talent-pool or specific-team hire, and what to prep. Good recruiters customize.

### §4b — Culture Interview (THE #1 eliminator — universal across every role)

45 min, interviewer is often **not** a PM/engineer on your team (it's calibration-universal). **Pre-rehearsed behavioral stories are the stated #1 failure mode.** They want to **watch you think in real time and change your mind mid-answer**, not watch you perform a polished narrative.

**What they score:** complexity tolerance · intellectual honesty · second-order reasoning · authenticity.

**The anti-patterns that eliminate prepared candidates:**

| Anti-pattern | Do instead |
|---|---|
| Shoehorning a STAR story into a safety question | Engage the actual question; reason from scratch |
| Skill-selling (listing accomplishments) | Share the reasoning process, not the resume — they already assume you're competent |
| Parroting (*"the RSP is a breakthrough"*) | *"The portfolio approach is rare — but where I have questions is the v3.0 changes…"* |
| Over-polishing (perfect, no hesitation) | Think out loud: *"Wait — I framed that as binary, but it's actually a spectrum…"* |

**How to practice (the only way that works):** debate AI-safety tradeoffs *out loud* with Claude, having it argue the opposite side, until you find where your own reasoning breaks. Those breakpoints are exactly where the interviewer will push.

**The disagreement-story drill (insider note — this gets the deepest probing).** If you tell a story about disagreeing with a senior leader and changing your mind, expect **4–6 follow-ups**: *Was this disagree-and-commit or a genuine update? · Looking back, was one path clearly right, or is it still unclear? · Did it carry emotional weight? · If it hadn't been your founder/CEO, would you have landed differently? · Is there someone you disagree with but deeply respect?* **Pick a story where you can answer all five honestly without contradicting yourself.** Calibrated uncertainty (*"I still hold it as unsettled"*) beats a clean resolution.

**Verified Culture questions to rehearse reasoning for (not answers):**
- "What are your thoughts on AI safety and the risks of advanced AI?"
- "Walk me through a project you're most proud of." *(NOT a competence question — what you pick reveals what you optimize for. Picking the **eval suite you shipped red** signals you optimize for honesty over polish.)*
- "Would you lose your equity if Anthropic withheld a model for safety?"
- "What's a belief about AI development most of the industry would disagree with?"
- "How do you reconcile caring about access with Anthropic's best models being expensive?" *(your Access-over-Meaning essay is the spine here)*
- "Is there something Dario has said publicly that resonates and makes Anthropic feel right?"

**Your stand-out moves:** have a *genuine disagreement* with Anthropic ready (RSP v3.0 is fair game); demonstrate "Hold light and shade" by stating an optimistic AND a pessimistic scenario before your position; admit a *specific* thing you don't know (*"I don't have a good model for the transition period between AI doing 80% vs 100% of a deployment engineer's job"*).

### §4c — Customer Scenarios / Live Claude Fluency (FOR FDE: this is the job, not a test)

Live roleplay: the interviewer plays a customer; you run **discovery → demo → iterate → close**, driving Claude live. **No other company runs this.** For an FDE this round is the single most predictive of on-the-job success — treat it as a *work sample*, not an interview.

**The 3-phase structure (≈55 min):**
- **Phase 1 — Discovery (0–15):** open with questions, *not* a demo. *"Before I show you anything — walk me through your current workflow. Where's the biggest bottleneck? Who'd use this and how technical are they?"* Anchor on one concrete use case by min 15.
- **Phase 2 — Live demo (15–35):** write prompts in real time (not pre-written). System prompt to set context → single/multi-turn → evaluate output *with* the customer → refine, re-run, compare.
- **Phase 3 — Challenges & close (35–55):** address **accuracy** (*"we'd stand up an eval — run Claude on a labeled sample, measure precision/recall"* ← your literal expertise), **cost** (*"for your volume, Batch API + prompt caching is ~50% cheaper"*), then **close with a concrete pilot**: scope + metric.

**When Claude produces bad output (it will):** acknowledge flatly (*"Interesting — it went a different direction than I expected"*) → diagnose (*"my prompt was too vague about X"*) → fix and re-run → frame as the normal workflow (*"this IS prompt engineering — the first prompt is rarely right"*). **Never** apologize profusely, blame the tool, or pretend it didn't happen. Recovering smoothly *is* the thing being scored.

**Build your demo kit (drill these until mechanical):** 3–5 ready use cases with sample data — **classification, extraction, summarization, analysis, generation.** This maps directly to your real work (you built a classification/synthesis fleet). Practice 10–15 hrs of *hands-on live driving*, not reading docs. Know the pricing cold (below).

### §4d — Technical Problem Solving (production diagnosis + system design)

Two-part, ~55 min, PM-level technical thinking (NOT deep ML).

- **Part 1 — Production issue diagnosis (~25 min):** a launched product is misbehaving. Framework: clarify scope/severity → segment users into cohorts → hypothesize **MECE** (system / product / external / data) → mitigate in **three horizons** (immediate / 2–4 wks / systemic). **Name the org stakeholders** in your mitigation (customer comms, Trust & Safety, on-call eng, leadership) — PMs who only give the technical fix miss the point.
- **Part 2 — System design (~25 min):** *"design a system that prevents this class of problem."* Best candidates make Part 2 directly address Part 1's failure class. **Safety is a first-class architectural requirement** — name the tradeoff (more safety checks = higher latency; where do you draw the line?).

**The AI-specific failure modes to have ready** (at least one will appear): hallucination → factuality checks / citation / confidence signals; **prompt injection** → input sanitization / system-prompt isolation / output filtering *(you literally shipped this — the `/etc/passwd` file-read hardening on `intent-engineering`)*; model drift → regression eval suites / canary deploys *(your eval suite)*; safety-filter false positives → tiered filtering + appeals; context overflow → RAG / summarization.

**Stay PM-level:** *"100K concurrent requests, sub-200ms, filter harmful outputs"* = good. *"transformer attention with KV-cache optimization"* = bad. Pick **one** whiteboard tool (Excalidraw) and draw 2–3 diagrams before the day.

### §4e — Leadership & Influence / behavioral (lead with the dilemma, not the outcome)

~80% scenario-based, ~20% real-experience probes — **not pure STAR.** Three buckets: conviction-vs-consensus · failure ownership · vision under uncertainty.

**The approach:** lead with **the tension** (competing values) → **your reasoning** → **how you brought people along** (influence, not authority) → **what you'd change** (intellectual honesty). "I convinced them" with no *how* is a red flag.

**Verified questions:**
- "Convince a cross-functional team to change direction." → **Story 6** (kept delivery legible through the Block turnover).
- "Walk me through a product failure you owned." → **Story 1** (the 9-day silent regression — you own it in one sentence, then the eval-suite flip).
- "Pitch a new Claude capability to a skeptical enterprise customer." *(then: re-pitch to an excited non-technical user, then to a safety researcher — same capability, 3 registers.)* → this is your **cross-functional-translation PRD** skill made live (5 personas, 5 vocabularies).
- "Set a 6-month vision when the tech changes every quarter."
- "Five ideas to solve one problem — how do you get to a decision?"

---

## §5 — Story → round mapping (and the Anthropic-specific warning)

Your 7-story bank ([[../story-bank|story-bank.md]]) maps cleanly to FDE rounds:

| Story | M-line anchor | Best round(s) at Anthropic |
|---|---|---|
| **2 — intent-engineering MCP** | 3 tools · npm+registry · 23/25 dogfood · 13 days early | Recruiter credibility · HM ("what have you built") · the JD-match centerpiece |
| **5 — Judge Layer** | 8-field ActionProposal · 4 rules · $0/decision · fail-open | HM strategy · Culture (control-architecture) · the FDE "production agent deployment" hook |
| **1 — Eval suite shipped red** | 10 cases · 6 modes · 1/10→7/10 · 17 days of logs | **Culture "proudest project"** (signals honesty>polish) · L&I failure-ownership |
| **4 — LDR fabrication catch** | 0 fabricated briefs post-fix · specimen kept | Safety questions · Tech Problem Solving (hallucination/grounding) |
| **3 — Cluster-bias retrieval** | HDBSCAN cluster-and-sample · audited depth-gate | Tech depth probe ("do you actually understand the ML") |
| **6 — Block cross-functional** | 35 ETF pages on a repeatable workflow | L&I "influence a team" · the one real-org story |
| **7 — Substack-Drafter cost** | ~$0–0.10/run · local-first · 0 autonomous publishes | "Tell me about a cost/latency tradeoff" · pricing fluency |

> **⚠ The Anthropic-specific warning that overrides normal interview advice:** in the **Culture Interview specifically, do NOT deliver these as polished STAR stories.** The stories are your *raw material* — the facts you reason *from* — not scripts you recite. When asked "what are you proudest of," start reasoning ("honestly, the one I keep coming back to is the eval suite, and the reason is uncomfortable — I shipped it failing on purpose, because…") rather than running the rehearsed S-T-A-R. In the **L&I and HM rounds**, more structure is fine; in **Culture**, structure is the tell that gets you cut.

---

## §6 — TMAY + the layoff answer (already built — pointers)

Your filled Anthropic Why-Here and the contained layoff answer live in [[../tmay-per-company-variations|tmay-per-company-variations.md]]. The FDE-tuned Why-Here (verbatim-ready):

> *"Your FDE role literally lists MCP servers, sub-agents, and skills as deliverables — that's the exact stack I've been shipping solo. And the JD line about codifying repeatable deployment patterns is the work I've been doing on my own fleet: turning one-off agent builds into reusable scaffolds. This is the one role where my evangelism arc doesn't just graduate into accountability — it lands at the source."*

The full 2-min TMAY is in [[../tmay-script|tmay-script.md]] — Proof Points 1/2/3 (MCP / eval-shipped-red / judge layer) are already FDE-perfect; the only swap is the §4 Why-Here above. **Layoff handling:** one factual sentence (cost-cutting, not performance, president is a reference), then the pivot. Never volunteer org drama.

---

## §7 — Pre-interview homework (the non-negotiables)

**Must-read (in priority order), with what to extract:**

1. **"Machines of Loving Grace"** (Dario) — articulate **one risk AND one benefit** for each of the 5 areas. This is the single most-referenced doc in Culture Interviews.
2. **Core Views on AI Safety** — explain the *portfolio approach* in 60 sec without notes; internalize the "we do not know" admission.
3. **RSP v3.0** — a *nuanced* position on the v3.0 changes (neither defend nor condemn). §2 above is your starting draft.
4. **Constitutional AI paper** — explain why explicit principles beat implicit ones, in plain language.
5. **Cat Wu — "PM on the AI Exponential"** — "PMs build prototypes and evals" (= your literal practice).
6. **Anthropic company page — the 7 values** — memorize all 7, especially #7.

**Must-do hands-on (this is FDE table stakes, not optional):**
- **Drive Claude live daily** — write/run/iterate prompts until it's mechanical. Build the 5-use-case demo kit (§4c).
- **Use the Claude API** — you have; be able to say *"I built X with the Messages API; prompt caching cut cost ~40%; the Batch API's 24-hr latency didn't fit use case Y."* That one sentence proves pricing + infra + real-limitation fluency.
- **Keep a friction log** — 5–10 observations (bugs/delights/limits) from daily use. Most credible answers come from here.
- **Know pricing cold** (verified 2026-06-08, per-M-tokens): **Haiku 4.5 $1 / $5 · Sonnet 4.6 $3 / $15 · Opus 4.8 $5 / $25.** Levers: prompt caching, batch processing, extended thinking.
- **Have a nuanced MCP take** — it's Anthropic's biggest platform bet *and* gets criticized for consuming 40–50% of the context window before agents work. You've shipped two MCP servers — you've *lived* this tradeoff. Say so.

---

## §8 — Self-contained mock runsheet (run this from this file + story bank)

> Satisfies the Task 32 verification gate: you can run a mock from this packet + [[../story-bank|story-bank.md]] alone. Use [[../../onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap|Task 19]]'s `mock_interview_loop.py` to record + grade. Target: **8+/10 on all 8 dimensions, 3 consecutive.**

**The 3 mock questions (one per type — behavioral / culture+safety / live-fluency-proxy):**

1. **(Behavioral / Why-now)** *"Walk me through what happened with The Block and how it reset your search."*
   - Hit: one factual layoff sentence (cost-cutting, reference intact) → the inflection → the 4 shipped artifacts → close on "stopped evangelizing, started shipping." Target 45–60s, calm. (Full model answer in tmay-per-company file.)

2. **(Culture + safety — the eliminator)** *"What's a belief about AI development that most of the industry would disagree with, and how do you hold the risk and the benefit at once?"*
   - This is a **reason-out-loud** answer, NOT a story. Demonstrate "Hold light and shade": state a real optimistic case AND a real pessimistic case before landing a *tentative* position. Reference your Access-over-Meaning thesis if it fits, but don't force it. Admit one specific thing you don't know. **You're graded on how you think, not the conclusion.** If you find yourself reciting a story, you're failing this one.

3. **(Live-fluency proxy / FDE core)** *"A 50-person content team wants to use Claude to draft articles but is worried about accuracy. Run me through how you'd take them from skeptical to a pilot."*
   - Run the 3-phase shape (§4c): discovery questions first → anchor one use case → describe the live demo you'd build → close on accuracy-via-eval + cost-via-caching + a scoped pilot with a metric. This is your Discovery-PRD skill spoken aloud. (If you have Claude open, actually drive a live extraction/summarization demo here.)

**The 8 grading dimensions (from the Task 19 rubric):** timing · structure · impact specificity · confidence · filler (<3/min) · weakness-flipping · information control · memorability. **Anthropic overlay:** add a 9th informal check on Q2 — *did I reason out loud and change my mind, or did I perform a rehearsed answer?* On Anthropic Culture questions, rehearsed = fail even at 8/10 on the standard rubric.

---

## Verification gate (Task 32)

- [x] Company-specific JD language pulled from the **live** JD (verified 2026-06-08, greenhouse 4985877008).
- [x] Stage-by-stage loop mapped, FDE-vs-PM differences flagged.
- [x] 6+ verified-recent questions per high-risk round (§4).
- [x] Company-specific TMAY/Why-Here + layoff answer wired (§6).
- [x] Live-Claude demo-kit drill specified (§4c, §7).
- [x] Safety angle woven through (§2, §4b, §4c, §4d) — not bolted on.
- [x] Self-contained mock runsheet (§8) — packet + story bank alone is mock-runnable.
- [ ] **Sean runs a mock from this packet scoring 8+/10** (gated on Task 19 rig — the real close).
- [ ] Confirm exact FDE loop shape with the recruiter when engaged (changes §4 emphasis).

## Open items

- 🔲 **Confirm role intent** — this packet anchors on FDE per [[../../target-companies|target-companies]]. If you re-aim at an Anthropic *PM* posting, the Case Presentation take-home (§ guide 5) comes back into scope; flag and I'll add it.
- 🔲 **Re-verify before the loop (search-first):** the current RSP version + any post-v3.0 news, current Claude model lineup/pricing, and the live JD (roles get edited). Facts here are accurate as of 2026-06-08.
- 🔲 **Build the friction log** (§7) — 2 weeks of daily Claude use, 5–10 observations. Start now; it's the slowest-to-fake prep item.
- 🔲 **Drill the live demo kit** (§4c) — 10–15 hrs hands-on. The FDE-defining round.

## Sources

- Anthropic FDE / Applied AI JD — [Greenhouse 4985877008](https://job-boards.greenhouse.io/anthropic/jobs/4985877008) (verified 2026-06-08)
- Insider Loops — Anthropic PM Interview Guide — [[../../../../40_knowledge/references/ref-anthropic-pm-interview-guide|local clip]] · [insiderloops.com/guides/anthropic](https://www.insiderloops.com/guides/anthropic)
- Sean's [[../story-bank|story bank]] · [[../tmay-script|TMAY]] · [[../tmay-per-company-variations|per-company variations]]
