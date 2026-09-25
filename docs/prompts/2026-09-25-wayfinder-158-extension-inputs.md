---
title: "Wayfinder #158 extension — inputs for the Pencil & Prompt re-scope"
type: prompt
status: ready-to-paste (rulings filled 2026-09-25)
created: 2026-09-25
tags: [wayfinder, content-machine, pencil-and-prompt, re-scope]
ai-context: "Paste-ready inputs for Sean to run /wayfinder 158. Extends the Content Machine map with the 2026-09-24 re-scope: niche, Drop/Rig series, private pencil-and-prompt repo, and a writing-first curriculum. Decisions come from a creative-partner session whose sidecar is local-only; never quote it."
---

# Wayfinder #158 extension: inputs

**How to use:** in Code-Brain, run `/wayfinder 158` and paste everything below the line. This **extends** the existing map. It doesn't start a new one: it redraws the destination, amends the notes, applies the ticket sweep, and adds new tickets with their blocking edges.

Source of the decisions: a creative-partner session on 2026-09-24/25 with nine locks, backed by three research notes (links under Notes). The session sidecar is local-only at `~/.creative-harness/partner-sessions/2026-09-24-writing-brain-reset.md`. Read it for context, but never quote it into an issue.

---

## 1. Redraw the destination

Replace the current Destination with:

> Pencil & Prompt runs from its own private `pencil-and-prompt` repo and Obsidian vault as a **craft vs. the machine** publication. Sean writes regularly through coached workshops, and those sessions grow a voice library of stories, stances and signature lines. The Drop/Rig experiment series is in regular use. The content machine drafts from that library, not from rules, and Sean ships pieces through it.

Why it changes: the old destination ("the Content Machine is live and in weekly use") was reached in machinery but not in writing volume. The re-scope moves the bottleneck from mechanics to Sean's own samples.

## 2. Amend the Notes

Add these to `## Notes`, keeping everything else:

- **Re-scope 2026-09-24 (supersedes the Editorial law L11 line).**
  - **Niche:** craft vs. the machine. A hand-drawn-animation and screenwriting nerd tests what AI can and can't take from real craft: the reps, taste, style and learning. Experiments are the evidence, and PM judgment is the lens.
  - **Side topic:** Saturday-morning builder. Building the things a 90s kid grew up on (cartoons, 16-bit games, comedy) with today's AI, brought in now and again.
  - **Publication:** Pencil & Prompt keeps its name and is re-anchored to the niche. Nothing has been posted, so the rewrite costs nothing.
- **Experiment series: Drop + Rig.** One series with two episode types. **Drop** runs a new model on the same setup, on every model release. **Rig** runs the same model on a new setup (prompt size, tools, skills), between drops.
  - The **Drop battery** is five frozen briefs: a pencil-test walk cycle, a 16-bit fighter sprite (idle plus one punch), a one-page comedic cold open, a 30–45 second wordless micro-film, and the flour-sack test. Each is one self-contained HTML file or plain text, with the first attempt shown unedited.
  - The **Rig bench** holds three swap-in or add-on briefs: Seven Transfers (a chain reaction with one fail-then-succeed step), The Same Face Three Times (the Kuleshov effect in code), and Same Room, Three Lights.
- **Samples over rules (standing preference).** Do not add new prose rules, voice guides, gates or metrics to the machine. When output is wrong, the first remedy is more of Sean's writing, not a new mechanism. Anything else needs Sean's explicit ask.
- **Workshop method.** For voice samples, ask plain, open questions first ("tell me about a time…"). Offer options, opinions and examples only after Sean has spoken, so the coach's framing doesn't leak into the library. Treat the first obvious take as the warm-up.
- **Topic and experiment filter (one line).** Would the question make sense to a reader who has never heard of Sean's agent fleet? Fleet and incident-log topics fail it unless they're really about craft.
- **Home.** Once `pencil-and-prompt` exists (a private repo, sibling of `code-brain`), writing sessions run there. This map's issues stay on the public `code-brain` tracker, so the privacy law still holds: no corpus text, transcripts or sidecar quotes in issues.
- **Research on file** (all 2026-09-24, `vault/20_projects/research/`):
  - `nicolas-cole-curriculum-deconstruction`: what Cole's programs teach, what's reproducible for free, and a draft 8-week curriculum.
  - `voice-exercises-and-coaching-methods`: 15 live session formats; volume beats feedback; neutral questions before provocation.
  - `voice-transfer-stories-vs-stances`: stories alone probably aren't enough for new topics. Add argument pieces and stance notes, and diversity beats volume.

## 3. Apply the ticket sweep

Sean rules each open ticket on the sweep page: https://claude.ai/artifact/N3ULJLgq2TWRMqULKNyMsJ (collection `rulings`, readable with `ArtifactData`). Apply each ruling as follows:

- **Keep:** leave open, and reshape the body to the niche where the note says to.
- **Fold:** close with a pointer to the ticket that absorbs it.
- **Park:** leave open, move it to Not yet specified as "revisit after the library grows," and unassign it.
- **Cut** or **Move out:** close, with one line under Out of scope.

**Rulings (Sean, 2026-09-25; read back from the sweep page's db, all 16 ruled):**

**Keep (4)**
- **The big X writing session (#263):** keep, and reshape it into new ticket C, the first writing workshop. It *becomes* C: don't create C as a separate issue. Rewrite #263's body to C's question.
- **Run a Pencil & Prompt piece through the full chain (#303):** keep, and point it at the first **Rig** episode. The finding that 36 voice rules made drafts worse, while samples alone made them better, is the craft piece. Block it by D so it runs from the new repo.
- **One interview, several X posts (#233):** keep as is. It's the "squeeze every topic" experiment.
- **Rewrite the About page through the machine (#234):** keep, which **overrides the Park suggestion**. Sean's reason: the portfolio page isn't Pencil & Prompt, but it tests the voice library on writing *outside* social posts. Low priority, but on the list. No blocking edges.

**Fold (2)**
- **The X register is 1.5%… (#262):** fold into #263 (ticket C). Close it with a pointer.
- **Give the Oracle's news lane an X leg (#252):** fold into new ticket I (Oracle refocus). Close it with a pointer.

**Park (2)**
- **Frame-generated candidates for X (#228):** park. Unassign it, and add "revisit after the library grows" to Not yet specified.
- **Run the next deck through the trace (#302):** park, but Sean was explicit that it **comes back**. He wants traces and evals on the Oracle or the content machine, and learning evals matters to him. But the current trace kit is hard to read, with its labels and code names. Leave #302 open and **block it by new ticket K** (legible evals), so it re-enters the frontier as K's test bed.

**Cut (5):** close each, with one line under Out of scope.
- **Stage 3 still requires a Voice Decision Record the shaper cannot produce (#235):** cut. Sean's note turns into new ticket L: remove every mechanic instruction left in the machine, not just this one.
- **The retirement scan reports clean while retired vocabulary sits in scanned files (#236):** cut.
- **The hand-rewrite survival number is meaningless at tweet length (#257):** cut.
- **Register-gap watch: does the sentence-length undershoot persist (#220):** cut.
- **Console defect: the ranking stage has no way to re-read a draft (#225):** cut.

**Move out (3):** close each on this map, with one line under Out of scope. The Professional lane (cover letters) stays in Code-Brain as job-hunt work, and these tickets live on there.
- **Rewrite the cover-letter contract from evidence (#243).**
- **Story banks with provenance: retire the Professional-lane interview (#244).**
- **origin_check.py blocks every cover letter forever, on the signature line (#245).** A small, real bug, and worth fixing in a job-hunt session.

## 4. New tickets

The types are wayfinder's. "Blocked by" means native GitHub blocking, wired in a second pass. **Eleven new issues:** A, B, D, E, F, G, H, I, J, K and L. C is not new: it reshapes the big X writing session (#263). Section 7 shows which are on the frontier right away.

### A. Drop episode 1: Opus 5.5 · `task` (HITL) · frontier
**Question:** Freeze the exact wording of the five Drop briefs, run them on Opus 5.5 plus one earlier model as the side-by-side baseline, and decide what gets published. Timely: Opus 5.5 launched 2026-09-22, so this is worth doing within days. The wording is frozen by Sean's approval. Also rule on whether the brief text is published or kept private, with only outputs going public: a public gallery of frozen briefs and answers may become training data for later models. Runs from `code-brain` for now; outputs move to `pencil-and-prompt` once it exists.

### B. Migration audit: what moves into pencil-and-prompt · `research` (AFK) · frontier
**Question:** Which skills, docs, folders, scripts, hooks and private-layer files in `code-brain` **and in `~/Code-Brain/anima/`** should be moved, copied, adapted or left behind to set up `pencil-and-prompt`?
- **Deliverable:** a migration table. One row per item: its path, a move / copy / adapt / leave call, a one-line reason, dependencies that would break (hard-coded paths, hooks, tests, config readers, launchd stanzas, other skills that import it), its privacy class, and the adaptation needed.
- **Starting points, not a limit:**
  - skills: `content-machine`, `content-oracle`, `writing-voice-modes`, `writing-critique`, `writing-humanity-pass`, `storytelling-architecture`, `substack-value-engine`, `creative-partner`, `grilling`, `script-writing`, `screenwriting-modes`, `creative-writing`
  - Code-Brain folders: `creative-studio/content-machine/` (the corpus, ledger, cheese bank and reference universe, all git-ignored), `vault/20_projects/substack-studio/`, the three 2026-09-24 research notes, partner-session sidecars that concern Pencil & Prompt, and the Oracle's news lane and watchlist
  - `anima`: its skills, briefs, registers, characters, templates, prompts, docs and PHILOSOPHY/DESIGN material
- **Anima question to answer:** what would make pencil-and-prompt a better writing room, and what only works inside anima?
- **Rules:** read only. Change nothing. Flag anything whose move would break a running Code-Brain agent.

### C. First writing workshop: the topic list · `grilling` (HITL) · frontier
**Not a new issue:** this *is* the big X writing session (#263), reshaped per the sweep. Rewrite #263's body to this question, and have every edge below that names C point at #263.

**Question:** Run the first coached workshop on Sean's current X topic list, using the new method. Plain questions come first, then options, opinions and examples. Draw on Elbow's loop writing and the formats in the exercises note. The goal is volume: stance samples, story samples and short posts from each topic that lands, and skip anything he has nothing for. Samples go to the private corpus, never into an issue.
- **Keeps #263's original aim:** fill the short-form X gap (the corpus has almost no posts of Sean starting a conversation), which is also the answer to the folded 1.5% ticket (#262).

### D. Scaffold pencil-and-prompt and run the migration · `task` (AFK + HITL) · blocked by B, L
**Question:** Create the private `pencil-and-prompt` GitHub repo as a sibling of `code-brain`, make it an Obsidian vault, and carry out the migration table from B in small, verified batches.
- **Verification:** the corpus checksums match, every copied skill loads, and nothing in `code-brain` breaks. Re-run `python3 scripts/validate.py` and the agents-sdk tests after any move.
- **Pace:** Sean wants this slow and careful, not fast.

### E. Write pencil-and-prompt's CLAUDE.md and AGENTS.md · `prototype` (HITL) · blocked by D, C
**Question:** What do the new project's CLAUDE.md and AGENTS.md say? The roles are writing coach, creative partner and social-media expert.
- **Content:** these files describe how sessions work (the workshop method, where samples go, the topic filter, the Drop/Rig protocol), never rules for the prose.
- **Evidence:** written after the first workshop, so they describe what actually worked.

### F. Design the curriculum · `grilling` (HITL) · blocked by C
**Question:** What is Sean's own writing curriculum? Cover the weekly rhythm, which session formats from the exercises note, the shape of the stance bank and signature-line bank, the voice-memo path (record, rewrite by hand, keep both), and how Drop/Rig episodes fit in.
- **Inputs:** Cole's free frameworks (the 8-week draft in the Cole note), the exercises note, the library mix from the voice-transfer note, and what actually worked in workshop C.
- **Session style:** a creative-partner session.

### G. Ship 30 for 30 or our own curriculum? · `grilling` (HITL) · frontier · **decide before 2026-10-05**
**Question:** Should Sean join Cole's Ship 30 for 30 cohort (Oct 5 to Nov 9, 2026, $99/month) as the deadline, feedback and peer layer, or run the self-built curriculum alone?
- **What's known:** the research note says paying mainly buys a fixed deadline, live feedback and peer readers, and one 2025 participant found the cohort leaned toward business topics.
- **Why it's a ticket now:** the deadline makes it sharp before F resolves.

### H. Re-anchor Pencil & Prompt to craft vs. the machine · `grilling` (HITL) · blocked by D
**Question:** What are the new thesis sentence, the series names (does "Building the Ladder" survive as the name for Drop/Rig, and what is Raising Agents now that the fleet is out of scope?), and the rewritten About and Start Here pages?
- **Carries over:** the pencil-test visual identity and mascots from August.
- **Process:** the pages go through the machine with Sean's hand-rewrite.

### I. Refocus the Oracle on the niche · `grilling` (HITL) · blocked by D
**Question:** Keep the Oracle's sweep, news lane, frame stage and scoring. What replaces the incident-log supply?
- **Supply rule:** retire any source that fails the one-line filter. Rebuild the watchlist around creative-AI accounts (for example the two Opus 5.5 animation posters), model drops, and animation and craft news.
- **Experiment cards:** point the frame stage's cards at Drop/Rig.
- **Folds in** the Oracle-watchlist ticket (#252) if Sean rules it Fold.

### J. Stories vs. stances: the blind test · `task` (HITL) · blocked by C
**Question:** Is the voice library enough for a new topic? Sean writes 2–3 opinion pieces, which are held out.
- **Two machine versions** of each, drafted from a neutral brief: one from stories only, and one from stories plus argument pieces plus stance notes.
- **Sean reads blind** and answers two questions: "Which one did I write?" (tests style) and "Does any version say something I wouldn't?" (tests viewpoint).
- **Output:** the answer decides the library mix going forward.

### K. Legible evals: how to make a trace and eval readable · `research` (AFK) · frontier
**Question:** How do you make an eval of a writing machine easy for its owner to read and understand at a glance? Sean wants to learn evals and eventually run traces and evals on the Oracle or the content machine. But the current trace kit (#291) is hard to follow, because of its labels, code names and codes.
- **Research:** how practitioners present eval results to the person doing the labeling. Plain-language failure names instead of codes. Pass/fail with a one-line critique. Side-by-side views of the draft next to what went wrong. The smallest useful set of labels.
- **Anchor source:** Hamel Husain's published posts on evals (hand-read first, binary pass/fail with critiques, judges only after 30–50 labels per class, a local store and a rendered HTML viewer, no hosted eval tools). Cite his posts directly.
- **Deliverable:** a short recommendation for what a legible eval page for this machine shows and names.
- **Then:** the parked trace-deck ticket (#302) is re-scoped to test that recommendation on one real Oracle deck or content-machine run. Wire #302 as **blocked by K**.

### L. Strip the leftover mechanic instructions from the machine · `task` (AFK + HITL) · frontier
**Question:** Which instructions in the live content machine still demand mechanics that the samples-over-rules re-founding made obsolete, and what's left once they're removed? This is Sean's note on the Voice Decision Record ticket (#235): remove *all* such instructions, not just that one.
- **Audit:** `content-machine/SKILL.md`, the stage files, the medium contracts, and the gate chain (`writing-critique`, `writing-humanity-pass`, `writing-voice-modes`) for instructions that require move rosters, licensing checks, decision records, mode or dial settings, metric bands, or anything else a stage must comply with rather than induce from samples. Examples: the Voice Decision Record line, and move-licensing reads that have no runtime reader.
- **Protocol:** before changing live behavior, follow the **Runtime-impact rulings** protocol in `content-machine/SKILL.md`, including the human consumer inventory.
- **Sign-off:** Sean approves the removal list before anything is deleted.
- **Why it blocks D:** it runs before the migration, so what moves into `pencil-and-prompt` is already clean.

## 5. Not yet specified (add)

- **Where Drop and Rig outputs live publicly:** X video, a Substack post, a running gallery page, or a mix. This sharpens after episode 1.
- **A third episode type, "craft reps":** Sean learns one craft skill with AI as tutor and without it. Parked until Drop and Rig have run a few times.
- **Posting cadence and the timely vs. timeless mix** (Cole's value-horizon lens). This sharpens after the curriculum (F).
- **Frame-generated candidates for X (#228, parked):** revisit after the library grows.

## 6. Out of scope (add)

- **Fleet and incident-log content** that fails the one-line filter (e.g. "the nightly critic that has produced nothing in twenty days"). Ruled out on 2026-09-24 as off-niche.
- **New rule-based voice mechanics**: added guides, gates, metrics or checkers aimed at prose. They're superseded by the samples-over-rules preference, and they return only if Sean explicitly asks.
- **Measurement and plumbing tickets cut on 2026-09-25:**
  - the Voice Decision Record (#235), whose broader cleanup is ticket L
  - retirement-scan coverage (#236)
  - hand-rewrite survival at tweet length (#257)
  - the sentence-length register watch (#220)
  - the spread-run console ranking defect (#225)

  They're superseded by samples over rules, and none of them measures what the re-scope cares about.
- **The Professional lane (cover letters), moved out on 2026-09-25:** the cover-letter contract (#243), story banks with provenance (#244) and the origin-check signature bug (#245). This is job-hunt work that stays in Code-Brain outside this map.

## 7. Frontier and edge summary

- **Frontier on day one:**
  - A: Drop episode 1 on Opus 5.5 (time-sensitive)
  - B: the migration audit
  - C: the first workshop (#263 reshaped)
  - G: the Ship 30 decision (due before 2026-10-05)
  - K: legible evals
  - L: strip the leftover mechanics
  - #233
  - #234 (low priority)
- **Blocked:**
  - D by B and L
  - E by D and C
  - F by C
  - H by D
  - I by D
  - J by C
  - #303 by D
  - #302 by K
- **Suggested order** for the frontier: A (the clock is running), G (a deadline), C (writing starts), L and B (they unblock the migration), K, #233, then #234.
