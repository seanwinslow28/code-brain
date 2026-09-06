# Kickoff: package `writing-voice-modes` for Claude Cowork

*Written 2026-09-03. Paste the block below into a fresh session at the repo root.*

---

I want to upload the current `writing-voice-modes` skill into Claude Cowork, replacing an older
version of it that still has all the author modes (Sedaris / Thompson / Kerouac / Vonnegut) in it.
The upload is failing because there is more than one `SKILL.md` in the folder. Before you touch
anything, I want the whole picture: what this skill has become, how it wires into the content
machine, why there are two `SKILL.md` files, and what a Cowork-uploadable version of it should
actually contain.

**Read first, in this order.** `.claude/skills/writing-voice-modes/SKILL.md` (~8,400 words — read
all of it, it is the artifact in question), then `.claude/skills/content-machine/SKILL.md`
(especially "The law", "The shaping context", and "Runtime-impact rulings"), then
`.claude/skills/content-machine/contracts/build_licensing.py` and `contracts/move-licensing.md`,
then CLAUDE.md rule 9 and the `PRIVATE LAYER` block in `.gitignore`, then
`.claude/skills/content-machine/runtime-retirements.toml`. Ground every claim in a file you have
actually opened; this skill has been rewritten repeatedly and the stale descriptions of it outnumber
the accurate ones.

**Four questions, in this order. Answer them before proposing a fix.**

1. **What does this skill do now, after the 2026-08-31 rules-off re-scope?** It has three standing
   jobs and none of them is drafting inside the content machine. Say what each job is, name the file
   or script that consumes it, and say what breaks if the skill were deleted tomorrow.

2. **How does it connect to `content-machine`?** Two connections matter and they pull in opposite
   directions: it is the **roster of record** that `contracts/build_licensing.py` reads (an unrated
   move fails the build), and it is **explicitly banned from the shaping context** — the drafting
   subagent must never load it, because voice is induced from samples rather than complied into from
   a rulebook. Explain both, and check whether the version I would upload to Cowork lands on the
   right side of that ban.

3. **Why are there two `SKILL.md` files?** I have found these already — verify them rather than
   trusting me:
   - `.claude/skills/writing-voice-modes/SKILL.md` — the real one, ~54 KB, last touched 2026-09-03.
   - `.claude/skills/writing-voice-modes/references/corpus-sources/voiceprint/my-voice/SKILL.md` —
     ~10 KB, dated 2026-07-29, frontmatter `name: sean-voice`. This looks like the output of a
     VoicePrint run that got parked inside the references tree as corpus source material, which
     would make it a *different skill* sitting inside this one's folder. Confirm what it is, where
     it came from, and whether anything still reads it. Then say whether it should move, be
     archived, or be deleted — and note that it is git-ignored, so git will not bring it back.

4. **What can actually be uploaded?** This is the part I care most about and the part I have not
   thought through. Only three files in this folder are tracked by git: `SKILL.md`, `evals.yaml`,
   `evals.sealed.yaml`. **Everything else — `references/` and `drafts/`, about 700 KB — is
   git-ignored under the privacy layer**, and `references/voice-samples.md` (92 KB), the cheese
   bank, the backups and the corpus-sources tree are in there. Uploading the folder wholesale would
   push private material into Cowork. Tell me plainly: what does the skill actually need at runtime
   to work in Cowork, what is local-only reference that must not travel, and what does `SKILL.md`
   promise that would break if its references are absent (it points at `voice-samples.md` as the
   calibration authority — does the uploaded version still function, or does it need that section
   rewritten)?

**Then propose the fix, and stop.** I want a plan, not edits: what the Cowork bundle contains, what
gets moved or removed from the working folder and where to, whether `SKILL.md` needs any edit to
stand alone, and what I do about the old author-modes version already sitting in Cowork. Flag
anything that would be a runtime-impact ruling under the content machine's protocol — this skill is
inside that operating surface, and the author modes are a live retirement entry
(`author-mode-machinery`), so a copy of the old version escaping into Cowork is exactly the
orphaning bug that registry exists to catch.

**Constraints.** Do not weaken any `.gitignore` rule, do not write private material into a tracked
file, and do not quote `voice-samples.md`, the corpus, the cheese bank or the Do-Not-Promote list
into your answer. I am a PM, not a dev — plain language, and give me a recommendation with every
question you ask.
