---
type: interview-prep-playbook
project: prj-job-hunt-2026
phase: interview-prep-phase-2
created: 2026-05-10
inherits_from: 2026-05-10-vibe-coding-research-synthesis.md
ai-context: "Executable vibe-coding interview playbook. Phase 2 of 4. Sober tactical register — comedic Sean Mode reserved for public-facing copy in Phase 3. Provenance is consolidated from the synthesis; reread that doc for tag-level attribution."
---

# Vibe-Coding Playbook — Sean × 2026-05

> **How to read this.** This is the executable layer on top of the synthesis. Every section is built to be glanced at the morning of an interview without needing to re-orient. Sections 4-6 are the load-bearing tactical moves; sections 5 and 8 are the highest-leverage prep before any specific loop.

---

## §1 — The format you'll face

The defensible shape of a vibe-coding interview varies by company. Use this table to set prep load before any specific loop. Where a row says "not publicly verifiable," do warm-network outreach to a recent hire before treating the format as known.

| Company / role tier | Format | Length | Tooling | Take-home variant | Portfolio walkthrough |
|---|---|---|---|---|---|
| **Sierra** (Agent PM / Eng) — Tier-3 wildcard | Plan-Build-Review structure | **2-hour solo Build** + ~30-45 min Plan + 45-60 min Review | Open choice; Sierra explicitly tolerates pivots | Pilot-debugging round on a medium codebase with coding agents | Review phase asks "how you used AI along the way" |
| **Anthropic FDE** Boston/NYC/Chicago — Tier-3 wildcard | **No live vibe-coding rep for PM/FDE roles.** Recruiter screen → hiring manager (45 min, Mission/Values/Safety/Product Sense/Tech Fluency) → 4-5 rounds incl. project deep dive | 45 min HM round; ~20 min project deep dive presentation | Take-home permits Claude only when explicitly stated | Yes — primary signal channel |
| **Google AI PM** (India + select US) — Tier-1 realistic if listed | 45-min live build | 45 min | Open choice (Replit, Bolt, Lovable, v0) | Not standard | Not standard |
| **Stripe, Netflix** — Tier-2 stretch | Take-home with deployed prototype | Multi-day | Open choice; deployed link required | Yes — this *is* the format | 1-pager + prototype link |
| **Glean** (Outcome / FDP) — Tier-2/3 | Multiple technical rounds; vibe-coding **format unverified** | Likely 45 min if present | Open choice | 2-hour assessment likely | Substituted for AI drudgery / automation roles |
| **Scale AI** — Tier-2 | 4-7 rounds (Glassdoor reports vary); behavioral + case heavy; vibe-coding **not publicly confirmed** | Variable | Open choice if rep occurs | Take-home case study likely | 45-min live presentation of assignment |
| **Cursor (Anysphere)** — Tier-1/2 | 3-4 rounds with prototyping component | 45 min build + 30-60 min product design case | Cursor | Homework case requesting prototype link | Yes |
| **Replit** — Tier-1/2 | 3-4 rounds | 45 min | Replit Agent | Variant available | Collaborative review of built artifact |
| **Microsoft AI PM** — Tier-2 | 3-4 rounds | 60 min build | Open choice (Lovable, vibe-coding tools) | Not publicly documented | Deep dive on resume project |
| **Decagon** — Tier-2 | Not publicly verifiable | — | — | — | — |

**Prep-load implication.** Sean is not prepping for one format; he's prepping for three: (a) 45-min live build for the Tier-1 set, (b) 2-hour Sierra-style stamina rep, (c) portfolio walkthrough + project deep dive for the Tier-3 wildcards. Phase 4 practice cadence rotates these.

**One discipline that holds across all formats:** whatever the rep shape, the load-bearing skill is **verification depth + decision narration**. Generation is cheap; explaining why the generated code is the right code is what's being scored.

---

## §2 — The rubric: 7 dimensions evaluators actually score

The dimensions below are the consensus rubric from the synthesis, with the seventh slot fused per the [P/G] disagreement. For each: HIGH signal, LOW signal, blow-up signal, and where Sean is most exposed.

### D1 — Spec interpretation & scope contract

- **HIGH:** Restates the brief in own words within 2 minutes. Asks 2-3 scoped clarifying questions. Names target user + core JTBD. States an explicit "will build / won't build" list before touching the tool.
- **LOW:** Starts prompting immediately. Scope expands mid-build as new ideas emerge.
- **Blow-up:** Builds for the wrong user (e.g., spec says "small business owner," candidate ships a CLI tool).
- **Sean exposure:** Low risk *if* he holds the 5-minute opening discipline. Higher risk under interview anxiety where the urge to "just start building" lands hard.

### D2 — Prompting / tool fluency (steerage)

- **HIGH:** Prompts in layers (layout → data → interactions → edge cases). Reads what the tool produced before issuing the next prompt. When AI output is 80% right, explains what's wrong before re-prompting.
- **LOW:** Dumps the spec into one prompt. Accepts output without reading. Fights a broken component for 10+ minutes.
- **Blow-up:** Cannot explain any of the generated code when asked.
- **Sean exposure:** **High.** This is the dimension his weak spots map onto. Beginner-to-intermediate TypeScript means reading Bolt/v0-generated React + TS, which he hasn't drilled. Inoculation is Phase 4 daily TS-vocab + the 15-second-audit-rule drill.

### D3 — Decision narration

- **HIGH:** Concurrent narration throughout. Names every significant decision aloud as it happens. Checks in with evaluator at min 15 and min 25.
- **LOW:** Silent stretches >60 sec. Evaluator cannot score what they cannot hear.
- **Blow-up:** Total silence >3 min during the build phase.
- **Sean exposure:** **Highest single-dimension risk.** Sean's named weak spot is *over-narration when nervous*. The fail mode for him is the inverse of the LOW signal — he talks too much, not too little. The drill is the 30-sec-per-build-step verbal cap, practiced relentlessly in Weeks 3-4.

### D4 — Failure recovery

- **HIGH:** Diagnoses before re-prompting ("I see X happened; I think it's because Y; let me try Z"). Pivots cleanly when the tool can't produce a component ("3-prompt rule" triggers a verbal pivot, not silent fighting).
- **LOW:** Panic-deletes working code. Accumulates technical debt silently.
- **Blow-up:** Destroys the only working state with a workspace-wide delete or "rewrite this from scratch" at minute 35.
- **Sean exposure:** Medium-low. Strong intuition from agent-fleet work; but no rep-against-stranger reps exposes how the recovery instinct holds under live pressure.

### D5 — Speed to working state

- **HIGH:** Shippable core by min 30-32 in a 45-min rep (leaves a 13-15 min buffer). Cuts scope deliberately, not reactively.
- **LOW:** Still mid-build at min 40 with no demoable state.
- **Blow-up:** No working artifact at time's end.
- **Sean exposure:** Medium. Linked to D3 — over-narration eats clock. The minute-35 freeze is the protective rule.

### D6 — Artifact quality (architectural awareness)

- **HIGH:** The final artifact has a coherent data model + readable structure + defensible abstractions, even if AI-generated. Candidate can explain why the structure looks the way it does.
- **LOW:** Different parts of the code feel inconsistent. Cannot explain any generated section.
- **Blow-up (adversarial follow-up variant):** When asked "now make this resilient to X" — candidate has no response or suggests starting over.
- **Sean exposure:** Medium-high. Architectural fluency is real (14-agent fleet, Phase D edges, MCP server), but defending AI-generated code he didn't write personally is a different muscle than defending code he authored. Inoculation: practice the explicit "I read this and chose to keep it because" sentence.

### D7 — User & system economics (fused)

This dimension fuses [P] user-centered decision-making and [G] economic/capital awareness. They land in the same evaluator moment — rejecting an expensive vector DB for a 50-row CSV is both economically aware and user-centered.

- **HIGH:** Design choices justified in user-goal language. Compute / latency / token costs verbalized as constraints. Can name a specific success metric (one primary, one engagement, one efficiency).
- **LOW:** Builds the technically interesting thing instead of the user-need thing. Selects the heaviest tool for a trivial task.
- **Blow-up:** Architects nested LLM calls per interaction (guaranteed latency timeout). Freezes when asked "how would you measure if this was successful?"
- **Sean exposure:** Low on the user-centered half (this is core PM craft). **Higher on the economic half** — Nate-1 explicitly named cost economics as Sean's one beginner skill. Inoculation: Token Cost Calculator artifact (already in the unified roadmap as Task 5) doubles as a drillable vocabulary anchor.

**Dimension rank order for Sean (where exposure is highest first):** D3 narration > D7 economics-half > D2 prompting > D6 artifact defense > D5 speed > D4 recovery > D1 spec. Phase 4 drills weight accordingly.

---

## §3 — Failure modes Sean should specifically inoculate against

The synthesis catalogued 11 failure modes (10 from Gemini + 1 from Perplexity + 1 [Coach] addition). Filtered to the modes that match Sean's named weak spots, the inoculation list is six:

**FM1 — Over-narration killing the clock.** [Sean weak spot match: direct.] Detection signal during practice: the timer hits min 20 and the working state is still scaffolding. Drill: the **30-second verbal cap per build step**. Every prompt gets ≤30 sec of narration before Sean's hands return to the keyboard. Practice with a kitchen timer in Week 3 solo reps. Phase 4 calls this the "narration governor."

**FM2 — The F1-score landmine.** [Sean weak spot match: directly addresses the "2-year titled / 4-6 year portfolio" reframe gap.] Detection signal: during portfolio walkthrough, a metric-defining question lands and Sean says "I'd have to check." Inoculation: memorize precision / recall / F1 / accuracy / ROC-AUC / mean reciprocal rank / groundedness / latency p50-p95-p99 / token cost per call — with one **concrete artifact-specific example** per term. Phase 4 daily warm-keep includes the rolling vocab review.

**FM3 — Backend over-indexing (the Google PM trap).** [Match: medium — Sean's instinct is to build the orchestration layer first because that's where his comfort sits.] Detection signal: min 25 and the UI is still a `<div>`. Drill: open every rep with the question "what's the user-visible artifact, and is it on screen yet?" If not, stop building backend and ship the UI shell with mocked data.

**FM4 — Hallucinated dependency acceptance.** [Match: medium — security-conscious flag for FDE/FDP wildcards.] Detection signal: AI suggests an obscure third-party library; candidate runs `npm install` without checking. Drill: any non-standard library suggestion triggers the verbal "I don't recognize this — let me check it's real" pause. Phase 4 lists a 10-package "I trust these on sight" allowlist for React/TS reps.

**FM5 — Fighting the tool instead of pivoting.** [Match: medium — no rep-against-stranger means Sean hasn't felt the panic-clock pull.] Detection signal: same broken component after 3 targeted prompts. Drill: the **3-prompt rule** — fail twice with targeted retries, third attempt either ships a simpler alternative or pivots, narrated aloud. Tape this rule to the laptop bezel for the live loops.

**FM6 — The freeze (no script for "I'm blanked").** [Coach addition; Sean weak spot match: direct because the no-rep-against-stranger condition means he's never been forced to recover from a real freeze on someone else's clock.] Detection signal: 5+ seconds of silence with the cursor not moving. Drill: the verbal lifeline (full move in §6).

**Why these 6 and not the other 5.** The unselected modes (Surface Correctness Trap, Under-Narration, Panic-Deleting Working Code, Ignoring Spec Edge Cases, Scope Creep, Context Window Exhaustion, No Success Metric, "One More Feature" Crash) are real but lower-likelihood for Sean specifically. He has too much agent-fleet engineering instinct to panic-delete or context-window-blow. The narration risk is over-, not under-. The "one more feature" crash is mitigated by the working-state freeze rule. He'll still cover them in solo reps via the §2 rubric self-scoring; they don't need top-of-mind inoculation.

---

## §4 — The first-five / last-five tactical playbook

Compressed phased execution. Every move has a one-line attribution: [P] / [G] / [P+G] / [Coach]. Don't memorize verbatim phrases (reads rehearsed); memorize the moves and improvise the language.

### Phase A — Minutes 0-5 (Orientation)

**Move 1: Read the brief twice in silence (30-45 sec)** [P]. Evaluators expect this pause; they read it as composure. Don't start talking immediately.

**Move 2: Restate the brief in your own words** [P+G]. Use natural language, not a rehearsed scaffold. "So the goal is [user] doing [JTBD], and the core pain is [X]. Want me to confirm before scoping?"

**Move 3: Ask 2-3 scoped clarifying questions; stop at 3** [P]. Target: (a) target user's technical sophistication, (b) device / platform, (c) any hard constraints on stack or data. Asking >3 reads as stalling.

**Move 4: State the will-build / won't-build contract** [P]. "Will build: A, B, C. Won't build: D, E. If time allows: F." Then physically write it on a notepad visible during the rep. This is the scope discipline anchor.

**Move 5: Prime the tool with a system-rules nudge** [G]. Specifically for Bolt/v0: "Use strict TypeScript types. Prefer standard React hooks over third-party libraries. Modular components over monolithic files." Narrate this as you type it.

### Phase B — Minutes 5-35 (Build cadence)

**Move 1: Prompt in layers, layer-aware narration** [P+G]. Layer 1: layout / data model. Layer 2: core interaction flow. Layer 3: one edge case or error state. Layer 4: polish if time. Don't jump to Layer 4 before Layer 2 ships.

**Move 2: The 15-second audit rule** [G]. After every AI response, hands off the keyboard for at least 15 seconds. Read the diff. Narrate one observation about the generated code (one good thing or one concern). Then continue.

**Move 3: Two check-ins — min 15 and min 25** [P]. "I have the core input flow working. Given the time remaining, should I add [X] or polish [Y]?" Lets the evaluator steer scope; demonstrates product judgment in real time.

**Move 4: Verbalize tradeoffs as they happen** [P]. "I'm using localStorage instead of a real DB because we have 30 minutes." One sentence per tradeoff. Don't justify; just narrate.

**Move 5: The 3-prompt rule** [Coach, derived from P]. If the same component fails after 3 targeted prompts, pivot verbally and ship a simpler alternative. "I'm going to swap this for a [alternative] to protect my time — in production this would be [original]."

**Move 6: Working-state declaration** [G]. Out loud, when a feature works: "I have a working state on the input flow — committing this mentally." This is the recovery anchor; if a later prompt breaks things, this declaration is where you mentally roll back to.

### Phase C — Minutes 35-45 (Freeze + frame + demo)

**Move 1: Hard stop on new features at minute 35** [P, with G calling minute 40 — see synthesis Disagreement 5; we're holding minute 35 for Sean]. After min 35, no new prompts. Anything not built goes into verbal roadmap, not the codebase.

**Move 2: Self-test the user flow (60 sec)** [P]. Walk through the prototype as the end user would. Catches obvious breaks before the evaluator sees them.

**Move 3: Lead the review with trade-offs, not apologies** [P]. Open the demo with: "I scoped to A and B, deliberately left out C because [reason]. The two biggest risks if this shipped as-is are X and Y; here's how I'd address them in the next sprint."

**Move 4: Deliver a success metric before being asked** [P]. "If I were measuring whether this is successful, the primary metric is [X]; engagement signal would be [Y]; efficiency would be [Z]." Pre-empts the "how would you measure success?" freeze.

**Move 5: Preemptive defense narration** [G]. Critique your own code before they do. "If I had two more hours, I'd rip out this [thing] and replace it with [better thing]. The technical debt I knowingly took on is [list]." Demonstrates self-awareness; signals you're not blind to your shortcuts.

**Move 6 (if adversarial follow-up lands):** Treat it as scope clarification, not a crisis [P]. "Great — the highest-risk surface there is [Y]. The move I'd make immediately is [Z]. I'd want to test [W] before shipping." You don't need to build it. Demonstrate reasoning.

---

## §5 — Portfolio walkthrough variant: per-artifact scripts

For each of Sean's 7 artifacts: a 5-minute walkthrough skeleton (Sean fills the prose), the 3-5 evaluator questions to expect, HIGH vs LOW answer signals, and the role tiers each artifact maps to. The 4Q `EXPLANATION.md` files already in the roadmap are the source content; the walkthrough is reading from the 4Q out loud in Sean's voice.

### Artifact 1 — `intent-engineering` MCP server

- **Target roles:** Anthropic FDE Boston/NYC/Chicago (Tier-3), Glean FDP (Tier-3), Cursor / Replit AI PM (Tier-1/2). The single highest-leverage walkthrough opener for the FDE wildcards.
- **5-min skeleton:**
  1. **Open with the Karpathy thesis frame (30 sec):** "If you ask Andrej Karpathy what one artifact a 2026 AI PM should ship, the answer is one MCP server. You're looking at mine."
  2. **What problem MCP solves vs. function-calling / API chaining (60 sec):** Context management + tool orchestration as a *protocol*, not a wrapper.
  3. **Codebase walkthrough — the 3 tools (90 sec):** `analyze_intent_spec`, `generate_template`, `audit_existing_spec`. Stdio transport. TypeScript SDK. Show the actual code briefly.
  4. **The eval question — how you measure it works (60 sec):** Specific metric (e.g., "the audit tool catches missing-acceptance-criteria with X% precision on N hand-graded specs"). This is where the F1-score landmine fires; have the number ready.
  5. **Scope discipline as a feature (30 sec):** "I shipped 3 tools, stdio only, no remote transport. The scope is deliberate — defensible small beats over-engineered. v1 would add remote SSE transport, schema versioning, and rate limiting."
- **Expected questions:**
  1. "Why MCP specifically over standard function-calling?"
  2. "What's the security surface? How are you thinking about auth?"
  3. "How do you eval that intent-engineering improves agent behavior vs. noise?"
  4. "What's the deployment target and how does this scale to enterprise?"
  5. "Why TypeScript? Why not Python?"
- **HIGH answer signals:** Names specific evals; references Anthropic's published MCP spec; can articulate the precise gap MCP fills vs. function-calling (statelessness, client portability, capability negotiation); honest about beginner-TS friction without apologizing for it.
- **LOW answer signals:** "It's an MCP server, it connects things." "It depends." "I'd have to check the eval metrics."

### Artifact 2 — 14-agent SDK fleet (7 active on launchd)

- **Target roles:** AI APM / PM I-II at AI-native (Tier-1), Senior PM at small AI startup (Tier-2). Also a credible secondary walkthrough for FDE wildcards.
- **5-min skeleton:**
  1. **Problem framing (30 sec):** "I run my morning, my vault, and my research from a fleet of agents. Here's how."
  2. **Architectural map — decomposition by responsibility, not by tool (90 sec):** Daily-driver, vault-indexer, vault-synthesizer, deep-researcher, meta-agent, knowledge-lint, flush, gemini-researcher. Show `config.toml`.
  3. **Live or pre-recorded Loom — one agent running (90 sec):** Recommended: `daily_driver.py --mode morning --dry-run`. Show the actual output, not a slide.
  4. **The eval / failure modes (60 sec):** MBP-asleep degrades the synthesizer; cost governors cap per-task / per-day / per-month spend; local-model-first routing with cloud fallback.
  5. **Cost-economics close (30 sec):** "Total daily cost across the fleet: ~$0.40 per morning run. The local-model routing means most agents are $0/run."
- **Expected questions:**
  1. "How do you handle state management between agents?"
  2. "What's the failure mode you worry about most?"
  3. "If you shipped this to 10 external customers, what breaks first?"
  4. "What evals run on the agents' outputs?"
  5. "Why launchd? Why not a queue / cron / Airflow?"
- **HIGH answer signals:** Specific cost numbers; named failure modes with detection signals; opinionated on routing decisions; can articulate why launchd (low-overhead, native, no cloud egress) beats heavier alternatives for a single-user fleet.
- **LOW answer signals:** "The agents mostly just work." Hand-waves on cost or eval.

### Artifact 3 — Phase D typed reasoning edges

- **Target roles:** Senior PM at small AI startup (Tier-2), Anthropic FDE (Tier-3) — anywhere "deterministic outputs from probabilistic models" is a real conversation.
- **5-min skeleton:**
  1. **Thesis frame (45 sec):** "LLMs are probabilistic; enterprise workflows demand deterministic outcomes. Typed reasoning edges are how I close that gap."
  2. **The `concept_edges` SQLite table — what it is, what it stores (90 sec):** 6 allowed relation types (supports, contradicts, evolved_into, supersedes, depends_on, related_to). Mirrors OB1's schema.
  3. **The synthesizer emitting relations (60 sec):** Show the prompt change — relations array is OPTIONAL, so the LLM degrades gracefully if it can't produce them.
  4. **The fast-path query (60 sec):** Knowledge-lint Tier 2 used to LLM-detect contradictions; now it SQL-queries `concept_edges` first, falls back to LLM only for novel pairs. Speed + cost win.
  5. **What would break (15 sec):** Bad relation values are logged + dropped; LLM still writes the article. Failure mode is graceful.
- **Expected questions:**
  1. "Why custom logic vs. standard Langchain output parsers?"
  2. "What's the system's behavior when the LLM persistently fails the type check?"
  3. "How do you validate the typed edges improve output quality?"
  4. "How would you explain this to a non-technical PM?"
- **HIGH answer signals:** Names the "spaghetti agent" failure mode; explains the OPTIONAL pattern as a graceful-degradation choice; cites the OB1 schema influence without overstating dependency.
- **LOW answer signals:** Dismisses Langchain without a real reason; can't explain the schema in plain language.

### Artifact 4 — Phase 6 knowledge loop (producer + consumer)

- **Target roles:** Senior PM stretch (Tier-2), Glean FDP (Tier-3).
- **5-min skeleton:**
  1. **The loop, not the pieces (45 sec):** SessionEnd flush → nightly synthesizer → weekly lint → SessionStart re-injection. The producer side is automated; the consumer side closes when a new session loads the index.
  2. **The PreCompact safety net (Phase A) (60 sec):** Before Claude Code auto-compacts a long session, flush.py fires so pre-compact knowledge isn't lost.
  3. **The Q&A endpoint (Phase C) (60 sec):** Three-tier article structure: concepts, connections, Q&A. Q&A articles cite specific chunk_ids back to the vault index.
  4. **The "is the synthesizer running?" question (60 sec):** It only runs when MBP is awake (Qwen3-14B on the laptop). On dry days, the producer is silent. The morning brief surfaces this status.
  5. **What would break (45 sec):** MBP-asleep ⇒ no synthesis ⇒ stale index. Mitigation in flight: migrate to Mac Mini (always-on).
- **Expected questions:**
  1. "How does the system know what changed?"
  2. "What's the cost of running this nightly?"
  3. "How do you avoid the synthesizer producing garbage that pollutes the index?"
  4. "What's the user-facing signal that this is working?"
- **HIGH answer signals:** Names the chunk_id + SHA-256 detail for change detection; honest about the MBP-flakiness; clear on what "working" looks like to the user (faster sessions, fewer rediscoveries).

### Artifact 5 — Sanitized agentic financial-research fleet

- **Target roles:** AI APM / PM I-II at fintech-adjacent AI co; Crypto/Fintech AI PM via Larry's network (Tier-2 Domain Specialist fallback).
- **5-min skeleton:**
  1. **Problem framing (30 sec):** "I built a multi-agent retrieval + synthesis fleet for personal financial research. The pattern transfers to any vertical research workflow."
  2. **The topology (90 sec):** Queue file → router → 3 retrieval agents → synthesis → daily note. Karpathy's "sensors + actuators" frame.
  3. **The eval question (60 sec):** Sanitized "did the synthesis cover the user's question?" with golden-set test cases.
  4. **Why this matters in an enterprise context (60 sec):** Same pattern works for legal research, medical literature, due-diligence workflows. The architecture, not the data, is the portable IP.
  5. **What's left out (30 sec):** No personal financial numbers. No advice. The sanitization itself is a feature, not a limitation.
- **Expected questions:**
  1. "Why three retrieval agents and not one?"
  2. "How do you handle disagreement between agents?"
  3. "What would change if you ran this on noisy enterprise data?"
- **HIGH answer signals:** Decomposition rationale (different sources need different retrieval logic); clear on the disagreement-resolution layer; transfers cleanly to a non-finance vertical when asked.

### Artifact 6 — Animation pipeline (June 11 short-film ship)

- **Target roles:** Creative PM (Tier-1 backup); secondary signal for any role where "candidate can ship a non-trivial creative artifact under deadline" matters.
- **5-min skeleton:**
  1. **The deadline as feature (30 sec):** "Ships June 11. Single-deadline pipelines force scope discipline."
  2. **The stack (60 sec):** ComfyUI for character generation, Remotion for composition, LoRA for character consistency. Show the directory.
  3. **The handoff problem solved (90 sec):** Frame interpolation (RIFE/FILM) closes the gap between AI-generated keyframes and broadcast frame rates. This is the non-obvious technical win.
  4. **The production diary (60 sec):** 4Q artifact ships with the film. The artifact is the explanation; the film is the demo.
  5. **Why this matters for a PM role (30 sec):** It's a shipped artifact under a real deadline with a complex multi-tool stack. Demonstrates execution + creative judgment.
- **Expected questions:**
  1. "What did you cut to hit the ship date?"
  2. "How did you decide when AI output was good enough vs. when to regenerate?"
  3. "What broke that surprised you?"
- **HIGH answer signals:** Specific cuts named; opinionated "good enough" threshold; honest about LoRA consistency hacks.

### Artifact 7 — Personal site `/transactions/` route (in flight, Astro 5)

- **Target roles:** Cross-cutting — this is the artifact that *hosts* the other artifacts publicly. Mentioning it shows that distribution + explanation is part of the discipline, not an afterthought.
- **5-min skeleton:**
  1. **The thesis (30 sec):** "Every artifact gets a co-located `EXPLANATION.md` in its repo + a deep-dive page on the personal site. The site is the canonical home."
  2. **The 4Q template (60 sec):** What is this / Why this approach / What would break / What did I learn. Shown briefly.
  3. **Karpathy / Nate framing — comprehension as 2026 currency (60 sec):** "When generation is cheap, explanation is the durable PM skill."
  4. **Why Astro 5 + React islands (30 sec):** Static-first, JS only where interactive. Fast cold load matters for recruiters who skim.
  5. **What's missing (60 sec):** Honest list — search, RSS, full design polish.
- **Expected questions:**
  1. "Why a personal site vs. Substack vs. Medium?"
  2. "How do you decide what gets a deep-dive page vs. just the GitHub EXPLANATION?"
- **HIGH answer signals:** Owns the distribution-as-craft framing without sounding precious about it.

---

## §6 — Recovery: when the rep goes sideways

Five most-likely failure inflections and the clean move for each.

**R1 — Spec misread (15 minutes in, evaluator says "actually I meant X").** Move: don't apologize. Restate the new spec. Cut existing scope ruthlessly. "Okay — that's a meaningful change. The work I've done on Y is throwaway. Let me re-state: I'm now building X with constraints A and B. The will-build / won't-build is updated to [new list]." 60 seconds of recalibration > 5 minutes of trying to salvage the old direction.

**R2 — Agent produces garbage (broken component after 3 prompts).** Move: the 3-prompt rule fires. Pivot verbally and ship a simpler alternative. "I'm going to swap this for [alternative]. In a real prod environment I'd circle back to [original]. The reason for the swap is that I'd rather ship a defensible smaller thing than burn 10 more minutes on this." This converts a stuck moment into a judgment-display moment.

**R3 — Deploy target broken / build won't compile.** Move: don't panic-debug. Open a new file / new component / new prompt. "I'm going to leave the broken build in place for a second and ship the next feature in isolation; we can integrate in the last 10 minutes." Compartmentalization. Sometimes the deploy target unblocks itself on the next save; sometimes it doesn't and you ship a partial demo with a verbal walk-through of what would have been integrated.

**R4 — Sean freezes (the no-rep-against-stranger weak spot lands).** Move: the **verbal lifeline**. Out loud: "Let me restate where I am — I have [X] working, [Y] is in progress, the next prompt I want to try is [Z]. Does that match how you're seeing it?" This converts silence-blow-up into decision-narration in one move. **Drill this script in every solo rep until it's automatic.** It's the single most important move in this section.

**R5 — Evaluator throws an adversarial follow-up ("now handle case X").** Move: treat as scope clarification, not crisis. "Great — the highest-risk surface is [Y]. The move I'd make is [Z]. I'd want to test [W] before shipping." You don't need to build it. Reasoning is enough. If they say "build it" — narrate the trade-off ("I'm going to do this by deleting [thing] from scope; is that the right call?") and proceed.

**The meta-move:** in every recovery, the play is *to narrate the recovery itself*. Evaluators score the recovery, not just the build. Silent recovery is worse than a clumsy but narrated recovery.

---

## §7 — Question-asking: 4 to always ask, 3 to avoid

End-of-loop questions are not just polite — they're signal. Each "always-ask" tied to the signal it sends.

### Always ask

**Q1 — "What does the first 90 days look like for whoever takes this role?"** Signals: thinking about ramp + execution, not titles. Forces a specific answer; pulls out real expectations.

**Q2 — "What's the eval / measurement loop on the work this role owns? How does the team know what's working?"** Signals: AI-PM-fluent (the Hamel/Shreya "evals are the new PRDs" frame). Directly counters the F1-score landmine *from your side* — you're the one asking the eval question.

**Q3 — "Where does the team's deepest disagreement live right now? What's the open architectural debate?"** Signals: senior-curious; wants to understand the actual decisions, not the marketing version. Often pulls out the most interesting answer of the loop.

**Q4 — "What's the single biggest gap on the team that this role is meant to close?"** Signals: outcome-oriented; wants to understand why this hire, not just what the JD says. The answer tells you whether the role is well-scoped or a wishlist.

**Optional 5th (if rapport allows):** "What's something I should be worried about that's not in the JD?" Signals: comfortable with uncertainty; not allergic to friction. Use only when the loop is warm — feels intrusive otherwise.

### Avoid

**A1 — Compensation questions.** Save for recruiter. Asking the panel reads as either underprepared or pushing the wrong lever at the wrong time.

**A2 — Generic culture questions** ("what's the culture like?"). Useless. Everyone says "collaborative + high-bar." Replace with Q3 or Q4 above, which gets a real answer.

**A3 — Questions whose answers are on the company's blog / website.** Asking "what does Anthropic care about?" at Anthropic reads as having not read the homepage. The fix: read the most recent 3 engineering / product posts before the loop; ask questions that reference them specifically.

---

## §8 — Story bank: 5 STAR stories framed around demonstrated work

Each story is framed around an artifact or moment, **never** around tenure milestones. The "what this signals" tag is the dimension the story is meant to lift.

### Story 1 — Track-C scope discipline (the MCP server v0)

- **Signals:** Judgment under uncertainty; scope as a feature; bias to ship.
- **S** (Situation): Post-Block severance, 8-week sprint, Karpathy thesis says "ship one MCP server."
- **T** (Task): Build the differentiator artifact without burning the 80% deep-work budget across other tracks.
- **A** (Action): Scoped to 3 tools, stdio transport, Claude Desktop demo. Wrote the 4Q `EXPLANATION.md` first to force the scope. Locked the 2026-05-25 ship date and refused to renegotiate it even when a tempting feature surfaced in Week 2.
- **R** (Result): Shipped on date. The artifact got an evaluator's-eye 4Q explanation alongside the code. The discipline of locking scope before locking code is the transferable habit.

### Story 2 — Phase D typed reasoning edges (the contradiction that surfaced via SQL, not LLM)

- **Signals:** Technical depth; ability to read other people's architectures and pick what fits; eval-design instinct.
- **S** (Situation): The weekly knowledge-lint job was using an LLM to detect contradictions in vault articles. Expensive, slow, and the model was hallucinating contradictions that weren't there.
- **T** (Task): Make contradiction detection cheap, fast, and grounded.
- **A** (Action): Read OB1's typed-reasoning-edges schema, ported it to SQLite as `concept_edges`, taught the synthesizer to emit relations as an OPTIONAL field in its existing JSON output, and gave knowledge-lint a SQL fast path with LLM fallback for novel pairs.
- **R** (Result): Contradiction queries went from "LLM call per check" to "SQL row lookup." LLM still writes the article regardless of whether it produces relations — graceful degradation by design. The OPTIONAL pattern is now the default for any new schema work.

### Story 3 — The agent-fleet audit (saying no to building more)

- **Signals:** Maturity; cost economics; ability to retire work, not just add work.
- **S** (Situation): The 14-agent fleet had drifted. 6 agents were disabled but still in the repo. The Vault Synthesizer was MBP-dependent and silently failing on travel days.
- **T** (Task): Decide what stays, what moves to Mac Mini, what retires.
- **A** (Action): Spent one Saturday evening on a structured audit. Migration list scoped to one week. The audit verdict was "keep daily-driver + deep-researcher always-on, move synthesizer + lint to Mac Mini, retire 4 of the 6 disabled agents, hold 2 for explicit re-enable review."
- **R** (Result): The fleet went from "drift + maintenance debt" to "decisions logged + scope defended." The single most important decision was the *retire* list, not the keep list. PM craft is saying no.

### Story 4 — The financial-research fleet sanitization (privacy + portability as a product decision)

- **Signals:** Customer obsession (where the customer is Sean himself); ability to think about portability of a pattern.
- **S** (Situation): A private agentic research fleet built for personal financial research. Useful internally; un-publishable externally without leaking financial position.
- **T** (Task): Make the pattern public without making the data public.
- **A** (Action): Stripped every personal number. Genericized every data source ("a crypto market data API," "a deep-research agent"). Kept the topology + the architecture diagram + the eval logic. Wrote the 4Q explanation as if the audience were a recruiter who'd never seen the underlying data.
- **R** (Result): The architectural pattern is public + portable to legal research, medical literature, due-diligence workflows. The sanitization itself surfaced as a feature ("you can take this pattern to any vertical") rather than a limitation. The privacy decision became the headline.

### Story 5 — The Block PM templates' second life (turning a layoff artifact into an asset)

- **Signals:** Resilience; ability to convert constraint into asset; CIIA-discipline (you didn't take what wasn't yours).
- **S** (Situation): Two years of PM templates at The Block — Jira ticket writing, ETF page generation, biweekly stakeholder updates. Owned by Block per CIIA Section 2.3.
- **T** (Task): Preserve the *pattern* without the *IP*. Specifically: extract the transferable PM craft from the Block-specific implementations.
- **A** (Action): Audited all skills line-by-line (11 KB audit doc). Rewrote three skills to remove Block-specific names, vocabulary, and templates while keeping the structural patterns. Committed the sanitization with explicit reference to the CIIA clause. Validated with grep + `validate.py`. Kept the protected physical archive path in one file as a deliberate deviation, documented in the commit message.
- **R** (Result): Public Code-Brain is now CIIA-compliant. The patterns transfer cleanly to non-Block teams. The discipline of "what's the pattern vs. what's the IP" is a reusable PM skill.

### Story 6 — The Phase 6 knowledge loop (closing a producer-consumer gap)

- **Signals:** Systems thinking; willingness to leave 50% scope on the table to ship the 50% that matters; eval mindset.
- **S** (Situation): The Code-Brain had a producer side (SessionEnd flush, nightly synthesizer) that wrote knowledge articles, but no consumer side — the articles existed but new sessions didn't know about them.
- **T** (Task): Close the loop without over-engineering it.
- **A** (Action): One hook — `session-start-inject-index.sh` — reads `vault/knowledge/index.md` and injects it as `additionalContext` on every new session. 5-second timeout. 15,000-char cap. File-read-only. No new infrastructure.
- **R** (Result): The consumer side shipped in a day. The Phase 6 loop is closed. The autoresearch feedback layer (which would have been the heavier version) was descoped explicitly and parked for a future autoresearch harness. The discipline was: ship the cheap loop that closes the gap; defer the expensive loop until the cheap one proves the value.

### Story 7 — The severance navigation (the meta-story)

- **Signals:** Composure under personal pressure; ability to execute a multi-track plan when motivated; partnership with critical-path collaborators.
- **S** (Situation): May 5, 2026. Layoff from The Block delivered by Larry Cermak and Vicky Lu.
- **T** (Task): Build an 8-week job-hunt sprint that produces shippable portfolio artifacts, doesn't burn through the runway, and doesn't break the household.
- **A** (Action): Wrote the master plan day 1. Brought Mary in as a critical-path collaborator from day 1. Locked Track-C MCP server as the differentiator and protected it even against application volume. Set the 5:30 PM hard stop and the Friday retro as non-negotiable rituals. Treated the sprint as a project with a `prj-job-hunt-2026/` directory, a README pipeline tracker, a unified roadmap, and an operating-model bundle.
- **R** (Result): One week in: severance signed, UI claim filed (slipped from target), Block IP scrub closed, Track-C scope locked, unified roadmap shipped. The most important meta-result: treating the hunt itself as a PM project — with a SOUL doc, a HEARTBEAT, and a Friday retro — is the same craft that the new role will pay for.

---

## §9 — How to use this playbook the morning of a loop

1. **Re-read §2 (rubric) and §3 (failure modes).** 5 minutes.
2. **Re-read §6 (recovery) once.** Especially R4 (the verbal lifeline). 2 minutes.
3. **Pull up the specific artifact's §5 script and read it once aloud.** 5 minutes.
4. **Pick one §7 always-ask question per panelist on the schedule.** 3 minutes.
5. **Don't re-read §8 (stories) the morning of.** Cramming behavioral stories degrades them. Trust that the prep is in your head.
6. **Stop reading this 60 min before the loop.** The pre-loop ritual (Phase 4) takes over.

End of playbook.
