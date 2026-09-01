---
title: "Content machine research pause — Lieberman re-read, field survey, and the rules-off experiment design"
date: 2026-08-31
project: code-brain
skill: content-machine
status: findings-awaiting-sean
tags: [research, content-machine, writing-voice-modes, substack-chain, style-transfer, prompt-constraints]
cost: $0 (web research + local file reads; no paid research invoked)
---

# Content machine research pause: findings

Executes the research brief in [docs/prompts/2026-08-31-content-machine-reset-research.md](../../../docs/prompts/2026-08-31-content-machine-reset-research.md). Three legs were run: (1) a re-read of both Lieberman transcripts against our L2 constitution, (2) a field survey of shipped AI writing systems plus the constraint-count research, (3) craft research on the brain-dump-to-prose gap — the craft leg's full findings live in the companion note [[2026-08-31-brain-dump-to-prose-operations]], which extends [[2026-08-28-story-hooks-and-narrative-through-line]].

**Nothing was built or amended.** The machine is exactly as it was when run #3 was drafted. Sean's rulings on the ledger's run-#3 entries (L3-01 through L3-07) remain pending and unrouted.

## The verdict in one paragraph

The hypothesis (L3-02: the prohibition layer is the cause) is **supported on every axis that could be checked, with one precise correction**: the problem is not that we misread Lieberman's origin lock — his machine is words-locked too — it's that his lock has three licensed escape hatches ours bans, and more importantly, the whole field puts rules in a different *place* than we do. Every shipped system surveyed keeps the drafting context clean (samples + a small positive voice guide) and runs its rules as **post-draft verification passes**; none carries a generation-time law layer at our scale, and the one commercial system whose creator tried it (Spiral) abandoned it. The instruction-following research supplies the mechanism: compliance with N simultaneous instructions decays roughly exponentially in N. And the craft leg names the operations the origin law structurally forbids: the two passes that turn a transcript into writing (Flower's writer-based→reader-based restructure, and the speech-to-prose register repack) both require adding and re-saying material — the exact operations the law bans. The rules-off experiment is worth running, and there is also a middle design (claims-locked, texture-free) that the evidence points at even more directly.

---

## Leg 1 — Lieberman, re-read at the source

Both transcripts at `vault/20_projects/prj-job-hunt-2026-REVAMP/docs/alex-lieberman/`.

### 1a. The add-vs-forbid question: answered, and it's a split decision

**Sean did not misread the core.** Lieberman, verbatim (voice-chain-workflow transcript): *"I have basically trained it to only use my words… the transcript really should be the only words that are used other than maybe the hook and the conclusion. And the job of the writer is really to almost be… shaping the clay of the content, not inventing net new things."* That is our origin law, near enough.

**But his lock ships with three licensed exceptions ours bans:**

| Lieberman licenses | Our machine's rule |
|---|---|
| An editor layer that **adds**: *"an editor who's checking what you've said, to add in places where you need to provide more context because you didn't share it with your initial thoughts"* (founders-AI-workflow transcript) | Additions become ASK-LIST questions back to the author; the machine may never add |
| **Hook and conclusion exempt** from the transcript lock (*"other than maybe the hook and the conclusion"*) | "A closing line assembled from nothing" is explicitly forbidden (SKILL.md, The law) |
| A **writer's-council revision loop** — six editor personas score 1–10, revise until ≥9/10 | "No autonomous revision loops… no score-until-good cycle, no persona panel, no numeric quality mean" |

So the machine we built is *stricter than its source on exactly the three axes where a writer does writer-work*: openings, closings, and revision.

### 1b. The confounds in copying him at all

- **Medium distance.** His outputs are LinkedIn posts and X threads — forms whose distance from a spoken riff is tiny. Ours is the narrative Substack essay, where the transcript-to-piece distance is a genuine rewrite. His pattern working for him is weak evidence it transfers to our form.
- **Input quality.** He's a 10-year content professional with 350 podcast episodes and ~10,000 posts behind him; his interview answers arrive nearly publishable. His own slop diagnosis blames input, not rules: slop is *"an indictment of the person not sharing good enough ideas during the interview step."*
- **Even his machine underdelivers.** In the live demo he flagged his own machine's line as *"kind of AI cringey… the newest em dash,"* and his honest fallback when output disappoints: *"I'll just write the thing by hand."*
- **His voice files are exemplar-derived and positive.** The voice guide is built by studying his top-performing posts — hook formulas, structures, characteristic language, one rule ("write like you're texting a friend"). No prohibition tables, no licensing matrix. His content-lessons file is our ledger (ours is the more rigorous implementation).
- **His interview panel is push-back-first**: six personas that refuse to advance without 2–3 specific stories with real details. Our dictation upgrade (#197) moved us in this direction and measurably worked.

## Leg 2 — Field survey: where voice lives in systems people actually ship

Full per-source detail preserved in §Appendix below. The pattern across every surveyed system (GitHub skills: angelarose210/ghostwriter, ericporres/voice-as-a-skill, artemnovitckii/content-skills, itallstartedwithaidea/writing-agent, anthropics/skills; practitioners: Lieberman's machine, the aimaker solo rebuild, Every's Spiral, ghostwriting agencies):

1. **Voice lives in samples, not rules.** Every serious system requires the author's writing (typically 5–20 pieces) as the primary voice source; several refuse to run without it.
2. **Prohibition lists exist but are small, target generic AI tells, and run as a separate post-draft pass** — never as generation-time law the drafting model holds in its head. (Our own `writing-humanity-pass` is already the field-standard shape; the origin law + anti-pattern table + licensing matrix loaded at composition time is the deviation.)
3. **Models are allowed to add.** Transitions, structure, framing, and context are the AI's job in every shipped pipeline. What's restricted is *facts and stories*, enforced by post-hoc traceability ("could every sentence be traced to something I said?") that routes missing material **back to the interview**, not into polished gap-fill. (The aimaker rebuild's "invention check" is our origin gate moved downstream and made advisory.)
4. **The direct precedent:** Spiral's creator ran exactly our experiment: *"when we first started this, I was going down this very much rules-based approach… none of that worked… let's allow it to be fluid… let's not constrain it with these really hard rules."* Voice via examples + interview; interviewer and writer split into separate contexts so the writer's context stays small.

**The mechanism, measured.** The instruction-following literature: "Curse of Instructions" (ManyIFEval, OpenReview R6q67CDBCH) — the probability of following *all* instructions ≈ per-instruction rate raised to the power of instruction count; GPT-4o followed all 10 of 10 instructions ~15% of the time, Claude 3.5 Sonnet ~44%. Replicated across 10 LLMs (arXiv 2509.21051). The remedy in both papers is post-hoc refinement loops — i.e., the architecture the shipped systems converged on independently. A composition context carrying the origin law + 36-move roster + 17-row anti-pattern table + G1–G5 + licensing matrix + medium contract sits far past the measured collapse regime, and the symptom matches: structurally compliant, stylistically dead.

**The honest counterweight.** Exemplars aren't magic: the best-controlled study ("Catch Me If You Can? Not Yet", arXiv 2509.14543 — ~400 authors, 6 frontier models) finds few-shot style imitation works for formal registers but still fails at informal, idiosyncratic voice, with limited gains past ~5 examples. The systems that work compensate with richer *input* (harder interviews) and staged pipelines, not more rules. So rules-off is not a guaranteed win; it removes a measured cost, and the residual gap is closed by material and iteration, not by either rules or samples alone.

## Leg 3 — The craft layer (summary; full note: [[2026-08-31-brain-dump-to-prose-operations]])

What a writer does between brain dump and finished piece is ~10 named operations in three tiers: **reorganize for the reader** (Bereiter & Scardamalia's knowledge-transforming; Flower's writer-based→reader-based restructure), **register conversion** (speech→writing repacking — measured: Chafe, Halliday, Biber), and **sentence work** (cohesion, compression, rhythm, syntax variety). The current pipeline does tier 3 lightly and tiers 1–2 not at all — a transcript reorganized by topic is, in Flower's exact vocabulary, *writer-based prose shipped to a reader*.

The register science also explains the analyzer conflict flagged in the continuation prompt: dictated speech is lexically narrower than prose **by register** (his own MATTR: 0.733 dictated vs 0.843 written). A words-locked draft of a transcript inherits speech's lexical profile no matter how well it's arranged, so the `writing-critique` MATTR gate at 0.807 demands what the origin law forbids. That conflict is not a calibration bug; it's the register gap itself.

And the professional order matters: transcript editors restructure first and re-apply the speaker's fingerprint diction *afterward*. Our runs #2–3 did the inverse — preserved clause-grain wording (where speech lives) and lost the fingerprint work (where voice lives).

## What our own three runs show, re-examined

- **The origin law defunds the move roster.** The licensing matrix licenses 34/36 moves for Substack, but most moves require invention: Jewel Center ("generate it from this piece's subject"), Hyper-Specific Anecdote, Borrowed Canon Line, Tool-as-Character dialogue, Pop Culture Anchoring. Under the law, a move can fire only if the transcript happens to contain its raw material. The run-#3 transcript (dictated, honest, image-free — his own words in it: "I was just rambling… clean everything up and make it coherent") contained almost none. The machine had a rich positive vocabulary and no legal material to spend it on.
- **His rewrites are additive, and what he adds is texture, not claims.** Across all three finals, the best moments are invented dramatization (the Claude dialogue in ep. 1 and run #3, the blank-markdown-files image, the GOD DAMMIT beat, the tailcoat line in run #2) — none of them false claims about events. Ledger L3-05 states it: some material only arrives at the writing.
- **What the gates actually caught was the other category.** The real saves in runs #2–3 were fabricated *claims*: an invented assertion that his writing "needed fixing," a contradicted three-months-wasted claim, a nightly schedule he never stated. The law's value concentrated entirely in the claims tier; its cost concentrated in the texture tier.
- **Even the best run leaned on invention.** Ep. 1 (64% survival, thinnest rule layer) shipped with dramatized dialogue in the final, and its ASK-LIST case ("Cool. Thanks.") was a right beat with wrong provenance — the beat survived, reworded by Sean.

**[analysis] The claims/texture split is where every line of evidence converges.** Lieberman locks substance and licenses hook/closer/context-additions. The field locks facts-and-stories via post-hoc traceability and frees everything else. The craft literature's "adding" operations (frame, context, image, syntax) are texture; its "never add" items are propositions. Sean's rewrites add texture and never false claims; the gates' real catches were all claims. Our law bans both categories uniformly, which is the design error the evidence points at.

## The experiment (to be designed with Sean, not run unilaterally)

Sean's ask stands as the primary arm; the evidence suggests testing the middle design alongside it.

**Arm A — rules-off (his hypothesis, verbatim).** A session gets: the corpus, `voice-samples.md`, the reference universe, and a transcript. It does NOT get: the origin law, the 36-move roster, the anti-pattern table, the licensing matrix, the medium contract, the gate chain, or the analyzer gates. Instruction is only: write the piece in his voice, from this material. (`do-not-promote.md` and the privacy law stay — they are not style rules.)

**Arm B — claims-locked, texture-free (the Lieberman/field configuration).** Same clean context as Arm A plus one rule stated positively: every fact, number, name, and event must come from the transcript; images, jokes, framing, hook, and closer are the writer's job. Origin check runs *after* drafting, claims-tier only, advisory, and anything untraced routes to an ask, not a silent cut.

**Measurement, same instrument as always** (`lessons/diff_pieces.py` survival on his hand-rewrite): above 64% beats the machine's best; below 38% and the hypothesis is in trouble. Plus a fabrication count per draft (claims-tier origin check + hand-check), because Arm A's known failure mode is the thing the law used to catch. Both failure modes from the continuation prompt stay live: Arm A may fabricate (law was load-bearing), or may still be flat (cause is elsewhere — most likely the missing Flower/register passes, which neither arm adds).

**Topic choice trades off two confounds** (Sean's call): re-draft the run-#3 transcript (controls topic; but his existing final contaminates a fresh hand-rewrite — though a $0 pre-test exists: diff each arm's draft against his *existing* run-#3 final before he touches anything), or a fresh piece (clean rewrite, topic confound). Cheapest honest sequence: run both arms on the run-#3 transcript, diff against his existing final as a pre-read, then run the surviving arm on a fresh piece for the real survival number.

**Regardless of the winner**, the field survey's strongest transferable pattern applies: keep the origin *guarantee* by moving it from generation-time law to a post-draft traceability gate that routes missing material back to the interview. That preserves what the law was actually protecting at the moment its cost is gone from the drafting context.

---

## Appendix — field survey sources

- angelarose210/ghostwriter — https://github.com/angelarose210/ghostwriter (voice from sample-derived profile; 200+ banned generic AI tells applied as post-draft elimination pass)
- ericporres/voice-as-a-skill — https://github.com/ericporres/voice-as-a-skill (refuses to run without 5+ samples; 8-week harvest cycles; scoped personal-cliché list)
- artemnovitckii/content-skills — https://github.com/artemnovitckii/content-skills (~20 own posts → extracted patterns; anti-AI pass targets patterns, not word lists)
- itallstartedwithaidea/writing-agent — https://github.com/itallstartedwithaidea/writing-agent (stylometric fingerprint from samples; 40-point QA downstream)
- anthropics/skills — https://github.com/anthropics/skills (instructions + examples; no prohibition-matrix architecture anywhere)
- Lieberman workflow write-ups — https://www.chatprd.ai/how-i-ai/alex-liebermans-6-step-workflow-to-beat-ai-slop ; https://www.lennysnewsletter.com/p/how-i-ai-how-the-founder-of-morning
- aimaker solo rebuild (the post-hoc "invention check") — https://aimaker.substack.com/p/ai-writing-workflow-creators
- Spiral creator on abandoning rules — https://every.to/podcast/transcript-spiral-s-creator-on-why-better-writing-means-better-thinking
- Every on style-as-data beating style-as-description — https://every.to/chain-of-thought/how-to-make-ai-write-like-your-favorite-author
- Ghostwriters on transcript work — https://www.thewritersforhire.com/can-ai-help-a-ghostwriter-make-sense-of-messy-interview-transcripts/
- Curse of Instructions (ManyIFEval) — https://openreview.net/forum?id=R6q67CDBCH
- When Instructions Multiply — https://arxiv.org/abs/2509.21051
- DeCRIM (decompose-critique-refine) — https://arxiv.org/pdf/2410.06458
- Negative-instruction analysis (anecdote + theory tier, flagged) — https://eval.16x.engineer/blog/the-pink-elephant-negative-instructions-llms-effectiveness-analysis
- Catch Me If You Can? Not Yet (few-shot style limits) — https://arxiv.org/html/2509.14543v1
- StyleAdaptedLM (sample-overload caveat) — https://arxiv.org/html/2507.18294v1
- Register descriptions can beat examples on style strength — https://arxiv.org/pdf/2505.00679

**Evidence gaps, stated:** no controlled study directly compares big-prohibition-list vs exemplars-only on generation *quality* (as opposed to compliance); the negative-framing claims are anecdote + theory + vendor guidance; "everyone who tried it quit" rests on one strong first-hand account (Spiral) plus universal revealed preference across shipped systems.
