# preserve-session — consolidated audit findings (RT1 shared input)

> Two independent prior audits of `preserve-session` produced these findings. They are
> merged, de-duplicated, and severity-tagged below — this is the shared, neutral input for
> RT1. Your job is NOT to re-audit; it is to author the definitive intent-carrying **fix
> spec** from these findings. Treat every finding as given.

**Skill under fix:** `.claude/skills/preserve-session/SKILL.md` (writes session state to CLAUDE.md + a vault project note + today's daily note). **Consumer:** `.claude/skills/resume-session/SKILL.md` (reads them back into a "where you left off" briefing).

## Findings

1. **[dangerously-wrong] Step 5 "Confirm" reports from intent, not a verified read-back.** The confirmation ("CLAUDE.md updated / Vault note updated / Daily note appended") is emitted because the steps *ran*, not because a re-read confirmed the bytes landed. A silent no-op and a real write print identical confirmations.

2. **[dangerously-wrong] No write transport/mechanism is named.** The skill says "append or update," "PATCH not PUT," "insert into anchor" but names no tool (no mcp-obsidian `patch_content`/`append_content`, no Edit, no script). The mechanism is left to the executing model to improvise, and the common improvisation ("the anchor already looks current — skip") is a silent no-op. Corroborating evidence: `## Session Log` appears in **zero** real CLAUDE.md files across the tree — the skill's primary artifact has apparently never successfully landed.

3. **[dangerously-wrong] Vault-note match key #2 targets a field that does not exist.** Step 3 says match by "the `context` field in CLAUDE.md frontmatter." CLAUDE.md files carry no frontmatter; `context:` lives on the *vault project note*. So the fallback match can never succeed, collapsing matching to directory-name-only.

4. **[dangerously-wrong] Directory-name match has no defined target for the most-used repo.** The worked example is `16bitfit/ → prj-16bitfit/prj-16bitfit.md`, but `vault/20_projects/prj-code-brain/` is a folder of many sub-notes with **no single `prj-code-brain.md`**. Run at the end of a code-brain session (the common case), Step 3 finds nothing (silent skip) or an improviser writes the summary into an arbitrary wrong sub-note.

5. **[structural] The two vault anchors have opposite write disciplines; one blanket rule is half-wrong.** `<!-- status-update -->` holds *current state* and must be **replaced** each session (resume-session reads it for "where you left off," so appending stacks stale status and resume surfaces last week as current). `<!-- claude-sessions -->` is a *log* and must be **appended** (replacing wipes the day's earlier lines = data loss). The single "PATCH not PUT" instruction is correct for the append region and wrong for the replace region.

6. **[structural] The daily-note anchor is a multi-owner, format-load-bearing surface.** `session-end-flush.sh`/`flush.py` also writes the same day's session record — as a plain-append `## Sessions` block, NOT into `<!-- claude-sessions -->` — and `daily_driver.py` parses the anchor's exact inline-field line format (`- [time:: HH:MM] | [domain:: …] | [context:: …] | **Outcomes:** … Link: [[prj-…]]`) for a Dataview roll-up. The skill treats the anchor as private free-text: any field drift makes a session invisible to the fleet console, and nothing reconciles the two structures.

7. **[structural] Daily-note write silently no-ops on any day the Daily Driver hasn't run.** Step 4 is guarded "if today's daily note exists"; the note (with its `<!-- claude-sessions -->` anchor) only exists once the Daily Driver creates it. Evening/weekend/out-of-band sessions skip the daily write with no create-or-locate.

8. **[structural] "Open Questions" is gathered but routed nowhere.** Step 1 extracts five categories; the Session Log template (Step 2) carries four — Open Questions has no field. The one class Sean flags for his own next-session decision is gathered, shown as work-done in Step 5, then written to no durable destination; resume-session has no source to resurface it.

9. **[structural] No adapter for a missing/renamed anchor.** "PATCH into `<!-- status-update -->`" has no defined behavior when the anchor is absent (a hand-edited note, a note predating the template) — the write lands nowhere or in the wrong place, and Step 5 still reports success.

10. **[structural] No stated relationship to the SessionEnd flush hook.** `session-end-flush.sh` fires on every close and mines the transcript into `vault/knowledge/`; preserve-session is the interactive structured write. Overlap/ordering/dedup is undefined, and the skill's own aspiration to be SessionEnd-hooked would collide with the flush hook already there.

11. **[minor] Step-2 timestamp has no timezone/source;** resume-session can mis-order across a tz boundary.

12. **[minor] "Keep ai-context under 200 characters" has no summarize-don't-truncate rule** (real values run ~380 chars → risk of a mid-sentence hard cut).

13. **[minor] `## Session Log` has no cap/rotation** — it grows unbounded in the file every session reads first.

## Genuine owner-forks the fix spec must handle (not silently decide)

- **Missing vault note:** the current skill says "report it but don't auto-create." Options: (i) keep report-and-skip; (ii) auto-scaffold a minimal note from the template then write; (iii) redirect the structured block into CLAUDE.md as a fallback. These trade off vault-cleanliness vs zero-loss — an owner-taste call.
- **Flush-hook coexistence:** stay two separate structures (anchor vs `## Sessions`), or reconcile into one — affects Rule #8 (Obsidian-Git is the sole vault auto-commit owner; no second auto-commit mechanism).
