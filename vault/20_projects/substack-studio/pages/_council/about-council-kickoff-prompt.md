# PROMPT TO PASTE INTO CLAUDE CODE (run from the `code-brain` repo root)

Everything below the line is the prompt. Copy it as-is.

---

You are orchestrating the **LLM Council** to WRITE (not critique) the "About" page for Sean's Substack, **Pencil & Prompt**, then running the chairman's synthesis through the full writing-voice chain. The council's native flow is what we want: each model writes its own version, they cross-rank, and the chairman synthesizes the best parts.

**Hard rule:** Do NOT read, reference, or feed the council Sean's existing draft at `vault/20_projects/substack-studio/pages/about.md` (or any prior Claude draft). The council writes BLIND from the context you assemble below. Sean compares against his own draft himself. Leave `about.md` untouched.

## Step 1 — Read context
- `vault/20_projects/substack-studio/POSITIONING-AND-EDITORIAL-SPEC.md` (positioning source of truth)
- `vault/20_projects/substack-studio/pages/start-here.md` (the sibling page, for register only, do not copy it)
- `.claude/skills/writing-voice-modes/SKILL.md` (Sean Mode, the House Style grit register, the signature-moves table)
- `.claude/skills/writing-voice-modes/references/voice-samples.md` (READ the newest section: "Pencil & Prompt — Start Here page, Sean's full rewrite (2026-06-23) — PRIME ANCHOR." This is the strongest single voice calibration.)
- `/Users/seanwinslow/Code-Brain/anima/CLAUDE.md` (anima facts; the fact-sheet below is already distilled, read only if you need more)

## Step 2 — Build the council prompt file
Write a SELF-CONTAINED prompt to `/tmp/llm-council/about-page-<timestamp>.md`. The council models have NO file access, so paste everything in. Include, in order:

**(a) Who the publication is** (paste verbatim):
> Pencil & Prompt is a Substack for the blocked, skeptical artist: a non-coding creative (illustrator, writer, animator, musician, designer) who tried AI, got soulless output from a prompt or two, and walked away sure it can't make anything with taste. Sean is the guide and the character, not the audience. The thesis: AI isn't here to replace the artist, it's a wildly talented intern with no taste yet, and your job is to teach it yours until it makes work that's recognizably you, on demand. The demonstration is the moat: show, never preach. The white space Sean owns: maker's soul (real craft demos) + skeptic's-eye empathy + a teachable taste-transfer method + a tool that kills the grind + dive-bar anti-hype voice.

**(b) The task** (paste verbatim):
> Write the COMPLETE About page, SHORT and to the point: about 250-350 words plus a one-line footer. This is the Substack-standard About length and shape (cf. Hannah Stulberg's "In the Weeds" and Matt Ferguson's "Life in the Machine": roughly five short first-person paragraphs, credibility shown sideways, a point of view stated as a belief, a tight "what you'll get," a warm sign-off, and NO pricing/monetization section). Write blind from this brief; do not reference any existing draft. First person, Sean's voice (spec below). It has to make a skeptical maker trust THIS guide, fast.

**(c) The short skeleton** (follow it; you may bend it, but keep the length and the genre):
> (1) Hook + who he is, 2-3 sentences, credibility sideways and fast: self-taught animator and filmmaker (his first comedy short is "Break Time"), wrote eleven screenplays in his twenties that nobody asked for, and now runs a small fleet of AI agents that handle a chunk of the work. (2) The threat + the turn, 2-3 sentences: AI showed up and everyone lost it (half the feed turned into Miyazaki characters, the other half wrote art's obituary); he didn't buy either; the machine isn't here to replace you, it's a wildly talented intern with no taste yet, and your job is to teach it yours. anima gets ONE sideways clause, not its life story. (3) The belief stated plainly: he won't preach "taste matters," he'll SHOW it, one real creative job at a time, the soulless first draft dragged move by move into something with a pulse, recipe handed over. (4) "What you'll find here" as three one-line bullets, the formats: Take Two (a real piece taken soulless-to-yours + the method); Tim The Tool Man Taylor (the occasional no-code tool that kills a grind); Fronkenschteen (send your worst AI output, he fixes it in public). (5) A warm sign-off that echoes the ethos (the "if the machine hands you slop, don't close the tab, that's just the intern asking to be taught" energy). (6) A one-line footer: YouTube (youtube.com/@seanpwinslow, where "Break Time" lives), github.com/seanwinslow28, seanwinslow.com, and "start with Take Two #1." His channel tagline is real and usable: "I like getting creative with AI and making silly cartoons." Name "Break Time" but do NOT invent its plot; invent no other biography; leave only [Take Two #1] as a placeholder.

**(d) anima fact-sheet** (paste verbatim; use accurately and SIDEWAYS, never as a resume or pitch; in this SHORT About, anima gets only a clause or one sentence, not the saga):
> anima is a pipeline for 2D animation made by a human and a fleet of agents. The name is Latin for breath, for soul. Its single rule: the human owns the timing, the casting, and the taste; the agents own everything that can be made cheap, parallel, and structured, and they propose, they never decide. Its core primitive is the Character Bible: a character is a folder of references (an anchor, turnarounds, expressions) that teaches the model the character's identity until it stops drifting. The lesson made concrete: stop describing your character and start handing the model evidence. A critic stack of agents proposes fixes; the human decides. The one law over the whole system (its "Engine Truth"): if the loop plays smoothly and the character is recognizably itself in its intended medium, it ships. anima was born from shipping a real animated piece called the Pencil Test.

**(e) Voice** — paste from `SKILL.md`: the **Sean Mode** section, the **House Style grit register**, and the **signature-moves table**. Then paste the **PRIME ANCHOR voice sample** (the 2026-06-23 Start Here rewrite) from `voice-samples.md` verbatim. Then these rules verbatim:
> No em dashes, ever. Dive-bar grit (bodily, profane when it earns it, blue-collar over literary). Anti-hype: never sound like an AI hype-bro. Credibility is shown, never claimed (strip every self-describing adjective; if the reasoning still proves competence it works). Keep strictly to the creative journey and the work, no sympathy backstory, no job-hunt ask. References woven as diction are good and Sean's natural density runs hotter than a hard 1-2 cap; avoid only the "that reminds me of the time... cut to [bit]" gorging cadence. The closer must be the strongest line and must not ask the reader for anything.

**Do NOT paste** `calibration-notes.md` or any Do-Not-Promote material into the council prompt.

## Step 3 — Run the council
```bash
mkdir -p /tmp/llm-council /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/pages/_council
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council \
  --profile premium \
  --prompt-file /tmp/llm-council/about-page-<timestamp>.md \
  --output /Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/substack-studio/pages/_council/about-council-short-$(date +%Y-%m-%d).md \
  --tag about-page
```
If the CLI refuses on a budget cap, surface the error verbatim and ask Sean before doing anything with `--force`.

## Step 4 — Run the synthesis through the full voice chain
Take the **chairman synthesis** from the transcript and run it, in order, through:
`substack-value-engine` → `storytelling-architecture` → `writing-voice-modes` (Sean Mode) → `writing-critique` → `writing-humanity-pass`.
Use the voice-modes reference files (`voice-samples.md`, `reference-universe.md`, `cheese-bank.md`) during the voice and humanity passes. Enforce zero em dashes, the grit register, anti-hype, and credibility-sideways. The YouTube channel (youtube.com/@seanpwinslow) and the film "Break Time" are real, use them; do NOT invent Break Time's plot. Keep only the [Take Two #1] placeholder. Invent no other biography. **Keep the final piece SHORT (~250-350 words); do not let the voice chain re-expand it into a long essay.**

## Step 5 — Deliver
Write the final, chain-scrubbed page to `vault/20_projects/substack-studio/pages/about-council-version-short.md` with page frontmatter (`publication: pencil-and-prompt`, `type: page`, `title: About`, `status: draft`, a `source:` note = "LLM Council premium + full voice chain," and a link to the transcript in `_council/`). Then append a `## Divergence note`: where the four versions differed most (structure, which beat each leaned hardest on, grit/voice level), and what the chairman kept from each. Report the run cost from the transcript's cost summary.

Keep `about.md` untouched. Sean will compare the two himself.
