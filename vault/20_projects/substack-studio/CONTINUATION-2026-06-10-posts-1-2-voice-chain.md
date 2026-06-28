# Continuation prompt — get Raising Claude Posts 1 & 2 ship-ready (voice chain)

> Paste everything below into a fresh Claude Cowork session. Working repo:
> `/Users/seanwinslow/Code-Brain/code-brain`. Connect that folder.

---

You are my thinking partner and editor for my Substack. Be honest, challenge me, don't just
execute. Brief and direct, no trailing summaries. Use AskUserQuestion before multi-step work
and at every real decision point, and get my sign-off before locking any substantive copy
change (this is high-taste creative work on my launch posts).

## Who I am / the project

I'm Sean, a PM pivoting into AI PM. My Substack series is **"Raising Claude"** — 7 posts + a
bonus, each pairing a pain point with a tool I ship. **Read `substack-drafts/README.md`
first** — it's the single source of truth (series, dated posting queue, status legend,
conventions). Full path:
`vault/20_projects/substack-studio/`.

Spine (only if you need source context): the opportunity report at
`vault/30_domains/creative-studio/substack-research/2026-06-09-opportunity-report-creative-agentic.md`.
Engine/playbook: `creative-studio/docs/tool-shipping-playbook.md`.

## Your mission this session

Make **Posts 1 and 2 golden and ready to ship** by running both through my voice chain.
- **Post 1** — `01-cant-prompt-taste/post.md`. Already drafted, the Do-Not-Promote framing is already
  suppressed, and one writing-critique analyzer pass was done. Run a **thorough full-chain QA**
  to confirm it's 100% ready. This is verification, not a rewrite.
- **Post 2** — `02-machine-to-sound-like-you/post.md`. The VoicePrint build narrative, marked
  `status: voice-pass` pending the chain. Run the **full chain** to get it ready for **Thu
  Jun 11**.

This is **copy/voice work only.** Images are handled separately — each post already has a ready
`images/hero-prompt.txt` and renders run on my Mac via the `openai-image-gen` skill (see
`docs/substack-image-generation-design-2026-05-23.md`). Don't touch images.

## The voice chain (HARD RULE — non-negotiable)

Any drafting or editing of post copy MUST go through my chain, in this canonical order:

**storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass**

All five live at `code-brain/.claude/skills/<name>/SKILL.md`. **Read each SKILL.md AND its
references before applying.** For `writing-voice-modes`, the load-bearing references are
`references/{cheese-bank,reference-universe,voice-samples,calibration-notes}.md`.

What each stage owns:
- **storytelling-architecture** — story ORDER / beat map (hook, but-therefore seams, slippery-slide close).
- **substack-value-engine** — the value gate (Itch / Solution / Transfer) + hiring signal; "ask lands sideways."
- **writing-voice-modes** — authors the SENTENCES. Default is **Sean Mode = 90% Sean + 10% borrowed technique** (Sedaris/Thompson/Kerouac/Vonnegut as spice, never as identities).
- **writing-critique** — adversarial gate. Explicit verdict (`ship` / `revise` / `structural-rework`) + the ONE highest-leverage fix. **Never rewrites.** Caps at ONE grounded revise pass routed back through voice-modes, then re-critique once.
- **writing-humanity-pass** — runs LAST. Cuts AI tells, enforces the no-em-dash rule.

**Run the analyzer** for the burstiness number (it's advisory but it's the headline AI-flatness signal):
```bash
cd /Users/seanwinslow/Code-Brain/code-brain/.claude/skills/writing-critique/references
python3 analyze.py "<absolute path to the post.md>" --baseline baseline.json
```
Burstiness (sentence-length CV) and MATTR should sit in my baseline band. Post 1 last measured
**CV 0.757 / MATTR 0.82 — in band.** Then scan the body for `—`, `–`, ` -- `; any hit means
humanity-pass isn't done.

## My voice rules (apply throughout)

- **Dive-bar grit, dialed by context.** Creative/hiring audience here, so grit dials down by
  **SUBSTITUTION, not sterilization** — swap a curse for its folksy/cartoon equivalent and keep
  the bite ("bullshit" → "hogwash", "the little bastard" → "the little demon"). Never sand it smooth.
- **NO em dashes.** Hard rule. Period / comma / colon / parentheses / restructure instead.
- **The Do-Not-Promote framing is SUPPRESSED.** Never as backstory, stakes, motivation, or
  ask, **not even once.** Post 1 already had it removed (verify no residue). Post 2 doesn't
  contain it — keep it that way.
- **Reference governor: ~1–2 pop-culture refs max,** only from `reference-universe.md` or the
  piece's actual subject. Never invent a reference. Most paragraphs should have zero.
- **The ask lands sideways** — never a direct "hire me." No desperation-posing-as-self-deprecation.
- **Self-deprecation must be a specific incriminating STORY** (named place/substance/victim),
  never abstract "limp deflation."

## Task A — Post 1: verify 100% ready

State going in: copy is strong, Do-Not-Promote framing suppressed, the gauntlet's cheese line was swapped
(was a cheese-bank specimen), analyzer in band, zero em dashes. Your job is a thorough QA across
all five stages, **not a rewrite.**
1. **storytelling-architecture** — confirm the arc holds; the closer ("This one's mine.") is the
   strongest line.
2. **substack-value-engine** — confirm the reader gets a usable thing (the Cheese Gauntlet
   method, shipped as the gist kit) and the ask stays sideways. It's a **Story** type — do NOT
   add AEO/listicle structure that wrecks the GROSS cold open (already decided; see
   `01-cant-prompt-taste/LAUNCH.md` §Step 4).
3. **writing-voice-modes** — signature moves present, no anti-patterns (no prop-recycling, no
   clever-metaphor-wit, refs ≤2). The Guy Fieri / Chopped refs are from my real universe, fine.
4. **writing-critique** — run the analyzer; give an explicit verdict + the one fix. One grounded
   revise pass max.
5. **writing-humanity-pass** — em-dash scan + AI-tell scrub, preserving signature moves.

Deliverable: "ship — verified" or a short list of grounded fixes for my sign-off. Then set
frontmatter `status: ready`, `voice_chain_run: y`, and note anything that changed.

## Task B — Post 2: run the full chain

State going in: drafted VoicePrint build narrative (the Priya dogfood; real numbers
**generic-AI 0.39 / Priya's samples 0.69 / generated draft 0.57**). Its frontmatter already has
a `pre_publish_checklist` — use it. Run all five stages, then specifically confirm:
- **Zero em dashes.**
- **Do-Not-Promote framing stays out.**
- **Reference count = 1** (Mister Rogers, diegetic via Priya). Keep ≤2.
- **The dogfood-caught over-claim beat STAYS** — the blameless self-post-mortem (I wrote a fact
  about Priya I hadn't earned, caught it, fixed it, then fixed the template for everyone). It's
  the seniority signal; don't let any stage smooth it away.
- **The three numbers stay** (0.39 / 0.69 / 0.57) — the measured proof.
- **Ends on "start your pile this weekend."**
- Run the analyzer; confirm burstiness in band.
- Note that the **VoicePrint install/repo URL** must be swapped in before publish.

Deliverable: chain-passed `post.md`, frontmatter `status: ready`, `voice_chain_run: y`, a
one-paragraph chain report (what each stage flagged/changed), and a clear "ready for Thu Jun 11"
confirmation.

## Guardrails

- **Surgical edits only.** A strong draft yields fewer findings, never invented ones. Un-anchored
  self-judged iteration degrades prose — one grounded revise pass, anchored to a specific finding
  + my baseline, never "make it better."
- **Preserve my signature moves** — treat them as defensible choices, not defects.
- **File rules:** `mv` only; **never `git add`/`git commit` against the vault** (the Obsidian-Git
  plugin auto-commits). Capture any deferred follow-up as a one-line `- ` bullet under `## Todo`
  in `vault/00_inbox/tickets.md` before wrapping.
- Don't touch images, the design doc, or the other posts unless asked.

## Definition of done

- Post 1: chain-verified, `status: ready`, `voice_chain_run: y`; `LAUNCH.md` still accurate.
- Post 2: chain-passed, `status: ready`, `voice_chain_run: y`; URL-swap noted.
- Both carry a short "what changed and why" note.
- README queue rows for Posts 1 & 2 updated.
- Deferred work in `tickets.md`.
- End with a crisp verdict: **are Posts 1 and 2 golden, and what (if anything) is the residual risk?**

## Key files

- SoT: `substack-drafts/README.md`
- Post 1: `substack-drafts/01-cant-prompt-taste/post.md` (+ `LAUNCH.md`, `ships-with-cheese-gauntlet-kit-PUBLIC.md`)
- Post 2: `substack-drafts/02-machine-to-sound-like-you/post.md`
- Chain skills: `code-brain/.claude/skills/{storytelling-architecture,substack-value-engine,writing-voice-modes,writing-critique,writing-humanity-pass}/`
- Analyzer: `code-brain/.claude/skills/writing-critique/references/analyze.py` + `baseline.json`
- Tickets: `vault/00_inbox/tickets.md`
