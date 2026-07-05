<!-- RT1 preserve-session fix-spec · FABLE blind run · 2026-07-05 · model=fable · harness=intent-engineering · agentId aa0a7c023dd3f43ca · 36 tool-uses / 969s -->

# Restated grounding (per the intent-engineering skill's step-1/2: answers were pre-supplied; restating and proceeding)

**(a) For.** Sean runs `preserve-session` at the end of a working session to hand off state to a future session with zero loss. It is the WRITE half of a pair; `resume-session` is the READ half. The payload is the session's living state: decisions, blockers, next steps, open questions, files modified — things that exist only in the about-to-die context window.

**(b) Feeds.** Two readers: `resume-session` (synthesizes the next session's briefing) and a human reading CLAUDE.md directly. Three write destinations: (1) the project CLAUDE.md's `## Session Log`; (2) the matching vault project note — frontmatter `ai-context`, the `<!-- status-update -->` region, the Key Decisions table, the Blockers list; (3) today's daily note's `<!-- claude-sessions -->` anchor. Machinery operates nearby: SessionStart inject hooks (index, tickets), and the SessionEnd flush hook (`session-end-flush.sh` → `flush.py`), which independently mines the transcript at close. Verified against the tree: `settings.json` registers flush + auto-stub on SessionEnd; `daily-note-appender.sh` exists but is **not registered** (dormant pattern file); the daily-note anchor line format is Dataview-parsed for the fleet roll-up; `vault/20_projects/prj-code-brain/` has no root `prj-code-brain.md`; `## Session Log` appears in zero CLAUDE.md files anywhere.

**(c) Disappoints.** Resume misses items that were captured in-session; the skill cannot tell whether the vault and daily writes actually landed; it always reports "saved" regardless; the net hand-off is lossy.

**(d) Wow.** Zero-loss reconstruction *in the reader's shape* — the next session's briefing carries everything the last session knew, including the open questions only Sean can answer — with per-destination confirmation that each write verifiably landed or was skipped for a named reason.

---

# Fix Spec — `preserve-session` (intent-carrying)

**Profile:** 4-element floor (fix spec for an existing skill; Right-Sizing rule row 0), voluntarily escalated with **Strategic Context**, **Edge Cases**, and a compact **Stop Rules** block — warranted because the fix pins two machine-parsed downstream shapes (resume-session's read contract; the Dataview inline-field line) and extends one additively (Open Questions). Full 9-section template not warranted: no autonomy change (the skill stays interactive), no new enforcement architecture beyond what the record already carries (block-secrets.py, Rule #8/#10).

## 1. Objective

A session-continuity skill exists so that closing a Claude Code session never costs Sean the state that session built. `preserve-session` is the WRITE half of that pair: at session end it must move the session's living state (decisions, blockers, next steps, open questions, files touched) out of the doomed context window onto the three surfaces the next reader reads — project CLAUDE.md, vault project note, today's daily note.

Today it fails in the worst way available to a persistence tool: **it reports success unconditionally while frequently writing nothing.** No write transport is named, the confirm step never re-reads, the vault match keys are broken for the most-used repo (code-brain has no `prj-code-brain.md`; the `context`-in-CLAUDE.md fallback targets a field that doesn't exist), and the daily write silently no-ops on any evening or weekend the Daily Driver didn't run. The corroborating evidence is total: zero `## Session Log` sections exist anywhere in the tree — the skill's primary artifact has never landed. Every lost hand-off is unrecoverable (the context is gone at close), and `resume-session` then reconstructs from stale or absent data *with confidence*.

**When facing trade-offs, prioritize in this order:**

1. **Truthful per-destination reporting over the appearance of completeness.** A verified `skipped (<reason>)` or `FAILED` is a *success* of this skill; an unverified "saved" is its worst failure, because it forecloses the human's last chance to recover the payload before close.
2. **Zero loss of captured state over destination correctness.** When a destination is unreachable, degrade to the destination of record (the CLAUDE.md entry always carries the full payload) and, at last resort, print the payload in chat. Never drop a category silently.
3. **Contract fidelity on shared surfaces over local convenience.** Anchors, the Dataview line, frontmatter keys, and section names are parsed by other systems; write in the pinned shape or don't write that surface — and say so.
4. **Vault cleanliness last.** Prefer skip-and-report over improvising a write into a "close enough" location.

These priorities run *inside* the record's hard constraints (privacy Rule #10 — enforced architecturally for literal secrets by `block-secrets.py` on Write|Edit; git Rule #8): zero-loss never licenses writing confidential specifics into a tracked file. Rule of thumb when instructions run out: **the skill's product is not the writes — it is the true report of what state now exists where.**

## 2. Desired Outcome (owner-observable, before → after)

1. **After any preserve run, Sean holds a three-line receipt** in which every destination reads `written+verified (…)`, `skipped (<named rule>)`, or `FAILED (<payload printed for manual paste>)` — produced from re-reads, so a receipt line and the bytes on disk cannot disagree. *(Before: one unconditional "saved," identical for a real write and a silent no-op.)*
2. **The next-session resume briefing reconstructs decisions, blockers, next steps, AND open questions**, with the vault status singular and current — resuming the next morning is materially equivalent to having kept the session open. *(Before: open questions vanish; stacked statuses surface last week as "current.")*
3. **An end-of-day code-brain session lands all three destinations or says exactly why not:** the daily note exists afterward even on days the Daily Driver never ran, and the vault miss is reported with the exact expected path plus a one-keystroke scaffold offer — never a silent skip. *(Before: evening daily writes no-op'd; the code-brain vault write could never succeed.)*
4. **Verifiable without self-report:** `## Session Log` sections exist and grow in real CLAUDE.md files; daily entries match the pinned line grammar by grep (§Done).

## 3. Strategic Context — consumers and pinned shapes

- **System role:** the interactive WRITE half of the preserve/resume pair. It runs in-session because the curated payload exists only in the live conversation — a hook firing at close can only mine the transcript, which is flush's job.
- **Consumers and the exact shapes they read:**
  1. `resume-session` reads: CLAUDE.md `## Session Log` → the **last** `### <YYYY-MM-DD HH:MM>` entry, bold field labels `**Decisions:** / **Blockers:** / **Next Steps:** / **Open Questions:** / **Files Modified:**`; vault frontmatter `ai-context`; the `<!-- status-update -->` region; `## Blockers`; the decisions table; daily anchor entries.
  2. Obsidian Dataview / fleet console parses the one-line grammar `- [time:: HH:MM] | [domain:: <d>] | [context:: <slug>] | **Outcomes:** <sentence>. Link: [[prj-<slug>]]`.
  3. `knowledge_lint` (Sunday) scans for broken wikilinks → the `Link:` field may exist only when its target note exists.
  4. Obsidian-Git commits all vault writes (sole owner — Rule #8).
  5. Humans read CLAUDE.md every session — hence a bounded Session Log.
- **Co-writers nearby:** `flush.py` (SessionEnd, detached, plain-append `## Sessions` block + knowledge extractions; lands *after* close); Daily Driver (08:30, creates the full daily note from `tpl-daily.md`); `daily-note-appender.sh` (**dormant** — not registered in `settings.json`; pattern source only).

## 4. The change, per finding

### F1 [dangerously-wrong] — Confirmation becomes a verified read-back
Replace Step 5 with **Verify & Report**: after all writes, `Read` each touched file and confirm the *specific new bytes* exist — the exact `### <timestamp>` heading in CLAUDE.md; the exact entry line under the daily anchor; the new dated status line inside the status region plus the new `ai-context` value. Emit exactly three destination lines, each one of: `written+verified (<path>, <what>)` / `skipped (<named rule + expected path>)` / `FAILED (<expected content absent>)`. On FAILED, print the un-landed payload verbatim in chat with paste instructions.

*Reasoning the implementing model needs:* verification means presence of the new content on re-read — never the write tool's return status, and never plausibility ("the file looks current"). The session is ending; a payload not on disk exists nowhere but this chat — that is why FAILED must dump the payload, and why an aggregate "Saved!" is forbidden even when all three verify: the per-destination structure is what makes a future silent regression visible. If a write reports success but the read-back can't find it, trust the read-back.

### F2 [dangerously-wrong] — Name the write transport
All writes use Claude Code's built-ins in a fixed loop: **Read (capture exact context) → Edit with exact `old_string`/`new_string` (the anchor line anchors the edit) → Read (verify, per F1)**. `Write` is legal only for file *creation* (new daily note, F7; consented scaffold, Fork A; archive, F13). When the project-scoped `obsidian-vault` MCP (`.mcp.json`) is mounted, its write tools may substitute for Edit — F1's Read-verify still runs. **Forbidden improvisations, named:** (a) skipping a destination because it "already looks current" — a skip is legal only via a named rule (Fork A miss; vault unreachable; user request), and every skip line names its rule; (b) writing the summary anywhere other than the three destinations (plus the sanctioned archive); (c) any `git add/commit/push` (Rule #8: Obsidian-Git owns vault commits; repo files are the human's).

*Reasoning:* zero `## Session Log` anywhere shows what "append or update" without a named tool degrades into — the model *narrates* the write instead of performing it, and the old Step 5 blesses the narration. A named tool plus mandatory read-back makes narration mechanically detectable (the verify step finds nothing). Any future destination added to this skill inherits the same loop by default.

### F3 [dangerously-wrong] — Fix the vault-note match (the direction was inverted)
Delete "the `context` field in CLAUDE.md frontmatter" — CLAUDE.md files carry no frontmatter; `context:` lives on the *vault note* (e.g., `prj-boston-move.md` has `context: boston-move`). New deterministic match, first hit wins:

1. `slug` := basename of the **project root** (nearest ancestor of cwd containing a CLAUDE.md), lowercased, spaces→hyphens.
2. **Direct:** `vault/20_projects/prj-<slug>/prj-<slug>.md` exists → target.
3. **Frontmatter scan (corrected direction):** for each `vault/20_projects/prj-*/` directory, read its **root note** (the `.md` whose basename equals its parent directory's name); the first whose frontmatter `context:` equals `slug` → target.
4. No hit → Fork A path. Never fuzzy-match; never select a non-root sub-note.

*Reasoning:* matching must stay human-checkable from the receipt — it prints which rule matched, or the exact path that missed. A fallback that can never succeed is worse than none: it manufactures confidence in a one-legged match. The corrected scan gives renamed projects a *declared*, greppable link instead of a guessed one.

### F4 [dangerously-wrong] — A defined target for the most-used repo
One explicit rule on top of F3: **a `prj-<slug>/` directory existing WITHOUT its eponymous root note is a MISS.** Code-brain today: `vault/20_projects/prj-code-brain/` holds `prj-automode.md`, `prj-agent-wiring-rollout.md`, `prj-knowledge-loop-consumer.md` — sub-projects with their own histories — and no `prj-code-brain.md`. Writing the session summary into any of them corrupts a different project's status surface *and* hides the entry where resume-session will never look.

*Reasoning:* when the obvious container exists but the contract file doesn't, the temptation is proximity ("this sub-note is about code-brain-ish stuff"). The rule to carry: **the target is defined by the contract (root-note naming), never by topical similarity.** A miss routes to Fork A, whose recovery is explicit, consented, and lossless.

### F5 [structural] — Per-surface write disciplines replace the blanket "PATCH, not PUT"

| Surface | Discipline | Definition |
|---|---|---|
| `<!-- status-update -->` (vault note) | **REPLACE-REGION** | Region = lines strictly between the anchor line and the next `## ` heading / next `<!-- ` anchor / EOF, whichever first. Write a fresh `**<YYYY-MM-DD>:**`-prefixed 1–3 line current state. |
| `<!-- claude-sessions -->` (daily note) | **APPEND** | Insert the new line directly below the anchor line, above prior entries (newest-first — `daily-note-appender.sh` + `inject_at_anchor` precedent). Never touch existing lines. |
| Key Decisions table (vault note) | **APPEND** | Add `\| YYYY-MM-DD \| <decision> \| <rationale> \|` rows below the header. |
| `## Blockers` (vault note) | **RECONCILE** | Rewrite to *currently-open* blockers: carry unresolved, drop resolved — resolutions are recorded as decisions in the CLAUDE.md entry, so removal loses nothing. |
| `ai-context` (frontmatter) | **REPLACE value** | Per F12. |
| CLAUDE.md `## Session Log` | **APPEND entry** | Chronological, newest last. Plus F13 rotation. |

*Reasoning — the discriminator to reuse on any surface this table doesn't list:* does the surface answer "what IS true now" (**state** → REPLACE/RECONCILE — a reader takes the whole surface as current, so stacking makes stale indistinguishable from current) or "what HAPPENED" (**log** → APPEND — replacement destroys history)? resume-session reads `status-update` as *the* current state — exactly why appending there is the lossy-handoff bug — and reads the sessions anchor as a log — exactly why replacing there is data loss.

### F6 [structural] — Pin the daily-note line grammar (a multi-owner, parsed contract)
The entry under `<!-- claude-sessions -->` is **exactly one line**:

```
- [time:: HH:MM] | [domain:: <domain>] | [context:: <slug>] | **Outcomes:** <one sentence>. Link: [[prj-<slug>]]
```

- Inline-field names (`time`, `domain`, `context`), the `[field:: value]` syntax, the ` | ` separators, and single-line-ness are load-bearing: the fleet console's Dataview roll-up parses them; a wrapped, re-ordered, or renamed-field line makes the session invisible to the fleet.
- `<domain>` from the CLAUDE.md routing vocabulary (`creative-studio`, `life-systems`, `the-block`, `job-hunt`, `claude-mastery`, `vault`) or the external repo's own name (e.g., `anima`); `<slug>` = F3's slug — the same value, so the console groups consistently.
- `Link: [[prj-<slug>]]` appears **only when F3 found a target**: a wikilink to a nonexistent note is a broken wikilink that Sunday's knowledge_lint flags (the vault holds at 0 — don't be the regression). On a miss, omit the whole field (the dormant appender's format shows it is optional).
- Overflow detail belongs in the CLAUDE.md entry, never in extra daily lines.

*Reasoning:* this surface has other writers (flush's block; the Daily Driver's template) and multiple readers (Dataview; resume-session). On a shared parsed surface, "improving the format" *is* the failure mode — so the grammar is pinned copy-pasteable, and no future session re-derives it.

### F7 [structural] — Daily note: create-or-locate (kill the silent skip)
Path = `vault/10_timeline/daily/<YYYY-MM-DD>.md` (system date, F11). If missing, **create it** with the reduced static skeleton proven in the dormant `daily-note-appender.sh`: frontmatter (`type: daily`, `date:`, nulls) + `# <date>` + Morning Focus + Tasks + `## Work Log` / `<!-- jira-log -->` + `## Claude Code Sessions` / `<!-- claude-sessions -->` + Side Project Notes / `<!-- side-projects -->` + Evening Reflection. Do **not** copy `tpl-daily.md` verbatim — it carries Templater placeholders (`<% tp.file.title %>`) and Dataview fleet sections that are the Daily Driver's morning job; faking them renders broken. Receipt says `created (reduced skeleton)`.

*Reasoning:* the note is keyed to *today*; tomorrow's 08:30 Daily Driver writes *tomorrow's* file, so creating today's cannot collide with it. The alternative — skip — deletes the session from the timeline, the surface both resume-session and the human read for what-happened-when. Precedent beats invention: the appender's skeleton is already shaped to survive the template's consumers.

### F8 [structural] — Route Open Questions to a durable destination (+ paired consumer edit)
Add `**Open Questions:**` to the Session Log entry template (field order: Decisions, Blockers, Next Steps, Open Questions, Files Modified). Empty categories omit their sub-heading — a thin entry should read as a thin session, not padded fields.

**Paired one-line consumer change, explicitly in scope:** `resume-session` Step 1.1 adds "open questions" to its extract list; its briefing gains `### Open Questions (yours to answer)` between Next Steps and Recent Decisions; "Suggested First Action" prefers an open question when one exists. **Scope guard:** those additions only — do not restructure the briefing.

*Reasoning:* open questions are the one category only Sean can advance — the highest-leverage item in the hand-off. Data written but never re-surfaced is not "preserved" in any sense the wow condition recognizes; that is why the consumer edit rides in this spec rather than a someday-ticket.

### F9 [structural] — Missing/renamed-anchor adapter: restore the surface, never relocate the write
When a target anchor is absent from an existing file:
- **Daily `<!-- claude-sessions -->` absent** (e.g., a bare `# Daily Log —` file created by flush, or a hand-made note): append at EOF a blank line + `## Claude Code Sessions` + the anchor line + the entry (the appender's exact fallback branch), then verify.
- **Vault `<!-- status-update -->` absent:** if `## Current Status` exists, insert the anchor line directly beneath it, then perform the F5 REPLACE-REGION write; if the heading is absent too, append `## Current Status` + anchor + status at EOF.
- Receipt on any adapter fire: `written+verified (anchor restored)` — never plain success.

*Reasoning:* hand-edited notes are normal in an Obsidian vault. The adapter's job is to *restore the contract surface in place* — purely additive to existing content, the same safety class as APPEND. Relocating the write instead would hide it from every reader that knows the contract (priority 3 beats priority 4).

### F10 [structural] — Declare the flush relationship in the skill
New SKILL.md section: preserve-session is the **interactive, curated** write — invoked in-session, before close, with live-context judgment. `session-end-flush.sh` → `flush.py` is the **automatic, transcript-mined** capture — fires detached at close, lands minutes later, writes its own plain-append `## Sessions` block plus knowledge extractions. Both may record the same session; the duplication is bounded and intentional (different shapes, different readers: Dataview/fleet reads the anchor line; the knowledge loop reads flush's output). Therefore preserve-session must **not**: wait for flush, attempt dedup against it, write `## Sessions` blocks (flush's namespace), or be registered as a SessionEnd hook.

*Reasoning:* the no-hook rule is physics, not turf. The curated payload exists only in the live conversation; a hooked preserve could only re-mine the transcript — a worse flush — while adding a second structured writer to a close path that must return in <100ms and never crash. The structure question is Fork B.

### F11 [minor] — Timestamp source and ordering authority
One system-clock read (`date +"%Y-%m-%d %H:%M"`) at gather time, reused across all three destinations so the heading, `[time:: ]`, and status dateline agree; never derived from conversation memory. Ordering authority = file position (Session Log newest-last; daily anchor newest-first); timestamps are display-only, so a tz oddity cannot re-order history. resume-session's "latest" = the last `###` entry.

### F12 [minor] — `ai-context`: compose-to-fit, never truncate
Compose a fresh ≤200-char value (shape: what the project is at + immediate next milestone). If a draft runs long — real values have hit ≈380 chars — **rewrite shorter**; a mid-sentence hard cut is forbidden (it ships garbage into every future resume read). Count before writing; verify after.

### F13 [minor] — Session Log rotation: bounded context tax, zero loss
Cap `## Session Log` at the **10 most recent entries**. On overflow, **MOVE** the oldest (cut + paste + verify both files) to `docs/session-log-archive.md` beside that CLAUDE.md (create dir/file with a one-line header if missing). This amends the append-only constraint: rotation is the sole sanctioned removal, and it is a relocation, not a deletion. *Why:* CLAUDE.md loads into every future session's context — unbounded growth taxes every session; deletion violates zero-loss; so relocate.

## 5. The two owner-forks (handled explicitly)

### Fork A — Missing vault note
**Status in the record:** the current skill's "report it but don't create one automatically" is the standing rule, but the findings name this a genuine owner-taste fork (vault-cleanliness vs zero-loss) — so it is surfaced with a recommendation, not silently kept or flipped.

**Recommendation: keep no-silent-create; add a consented scaffold offer.** On an F3 miss, report the exact expected path and — because this skill is interactive and the human is present — ask once: *"No vault note at `vault/20_projects/prj-code-brain/prj-code-brain.md`. Scaffold one from tpl-project.md and write the status there? [y/N]"*. **Yes** → create from `vault/90_system/templates/tpl-project.md` (title, `context: <slug>`, `created:` today; taste fields like `energy-level` left null), then run the normal vault writes. **No** → `skipped (no matching vault note; expected <path>)`.

**Why this side:** it preserves the value behind the current rule — project notes carry human-set metadata and MOC links a robo-scaffold would fake, and unconditional auto-create would mint junk notes when run from scratch dirs — while closing the loss: the CLAUDE.md entry carries the full payload on *every* branch, and the offer converts a permanent silent skip into a one-keystroke fix the first time it bites the common-case repo.

**Contingencies:** (i) Sean prefers strict report-and-skip → delete the offer sentence; nothing else in this spec changes (the CLAUDE.md-carries-everything invariant keeps both branches lossless). (ii) Sean prefers always-auto-scaffold → replace the ask with unconditional create, accepting robo-notes from one-off dirs (the reason it is not recommended). Option (iii) from the findings — redirect the structured block into CLAUDE.md — is subsumed: the entry is always full-payload.

### Fork B — Flush-hook coexistence
**Status in the record: partially decided.** Rule #8 fixes the commit half outright — whatever the structure answer, no second vault auto-commit mechanism may appear; this spec treats that as settled. The structure half (two records vs one) is genuinely open.

**Recommendation: stay two structures; F10's section is the ownership declaration.** Reasons: (1) different capture kinds — flush is $0, automatic, and fires even on crash-ends; preserve is judgment-bearing and exists only in-session. Merging means either `flush.py` learns the anchor grammar (a code change with blast radius on a latency-budgeted SessionEnd path) or preserve abandons the Dataview line (breaking the fleet-console contract). (2) Timing makes preserve-side dedup impossible — flush lands after close. (3) The duplication is one line + one block per session, read by different consumers.

**Contingency:** if Sean chooses reconcile-into-one, that is a **flush.py-side plan** (teach `format_daily_log_body` the anchor grammar or a shared section), ticketed separately per Rule #9 — and it must also resolve the path seam this grounding surfaced (`flush.py` targets `cfg.vault_root/daily/` while daily notes live at `10_timeline/daily/`). preserve-session's contract under this spec (the anchor line) is forward-compatible with that merge, so **this spec ships identically on either branch** — which is why the fork doesn't block it.

## 6. Edge cases (beyond the per-finding ones)

1. **Anchor appears twice in a file** → operate on the FIRST occurrence only (`inject_at_anchor`'s insert-after-every-occurrence is a lib quirk, not the contract).
2. **cwd is a subdirectory** → project root = nearest ancestor with a CLAUDE.md; slug from that basename (else `16bitfit-battle-mode/src` slugs as `src`).
3. **No CLAUDE.md up-tree (scratch dir)** → offer to create one at cwd; declined → `CLAUDE.md: skipped (no project root)` + payload printed in chat; daily note still written — the timeline is always reachable.
4. **Vault path absent** (skill exported to another machine/project) → vault + daily lines report `skipped (vault not accessible at /Users/seanwinslow/Code-Brain/code-brain/vault)`; the CLAUDE.md write proceeds. The vault root is that absolute path — name it in the skill.
5. **Frontmatter exists but lacks `ai-context`** → add the key (additive). **No frontmatter block at all** → skip ai-context with reason (creating a structural block in a hand-shaped note exceeds the sanctioned adapters); the status region is still written.
6. **Mid-run user redirection** ("skip the vault, just CLAUDE.md") → honor it; receipt reads `skipped (user request)`.
7. **Second invocation in the same session** → append a second Session Log entry + second daily line; status region and ai-context replaced again. The disciplines make re-runs shape-idempotent: logs grow, state surfaces never duplicate.
8. **Sensitive content in the payload** (employer-confidential, income, medical — Rule #10; literal secrets — `block-secrets.py` PreToolUse on Write|Edit): the tracked CLAUDE.md entry carries a redacted summary; specifics go only to the gitignored vault surfaces (`vault/10_timeline/`, the private project notes) or stay in chat. Zero-loss never licenses a privacy breach — the constraints bound the objective, not vice versa.
9. **MCP/tool-transport failure** (the `obsidian-vault` MCP is mounted but its write errors or times out) → fall back to the built-in Read→Edit→Read loop for that destination; if the built-in path also fails, that destination's line reads `FAILED` + payload dump. Never retry a transport in a loop (see Stop rules).

## 7. Stop rules (compact — this is an interactive skill; no Zero-Interaction Mandate, and F10 keeps it that way)

- **Halt per destination** after at most **one retry** (a failed Edit → one re-Read + re-Edit with fresh context — covers the file-changed-under-you case — then report `FAILED` honestly). Never loop on writes.
- **Escalate to the human** only via the two named interactive asks (Fork A scaffold offer; edge-case-3 CLAUDE.md offer) and on any FAILED line (the payload dump *is* the escalation).
- **Complete** when the three-line receipt has printed with zero unexplained lines — the receipt is the exit; nothing runs after it.

## 8. Done looks like (checkable)

**Text checks on the rewritten skill(s):**
- `grep -c "PATCH, not PUT" .claude/skills/preserve-session/SKILL.md` → 0; the F5 discipline table is present (`REPLACE-REGION` and `APPEND` appear beside the two anchor names).
- The broken CLAUDE.md-frontmatter match key is gone; the algorithm names `prj-<slug>/prj-<slug>.md` and the root-note rule verbatim.
- `grep -n "Open Questions" .claude/skills/preserve-session/SKILL.md` ≥ 1 (template field) **and** `grep -n "Open Questions" .claude/skills/resume-session/SKILL.md` ≥ 1 (extract list + briefing section).
- SKILL.md names: the Read→Edit→Read transport loop, the three receipt states, the flush-relationship section, create-or-locate, the anchor-restore adapter, the rotation rule, and the copy-pasteable daily line grammar.

**Behavioral checks (sandbox vault + throwaway repo):**
1. Code-brain run with no `prj-code-brain.md` → offer fires; declined → receipt reads `vault note — skipped (no matching vault note; expected vault/20_projects/prj-code-brain/prj-code-brain.md)`; the CLAUDE.md entry carries Decisions/Next Steps/Open Questions.
2. Today's daily note deleted → run → note exists after; entry matches `^- \[time:: \d\d:\d\d\] \| \[domain:: [a-z-]+\] \| \[context:: [a-z0-9-]+\] \| \*\*Outcomes:\*\* .+` and `Link:` is absent (no vault note).
3. Two runs same day → two anchor lines, newest first, the prior line byte-identical.
4. Two runs → the status region holds exactly ONE dated status (today's).
5. The receipt always has exactly three destination lines; a simulated edit failure yields `FAILED` + the payload block in chat.
6. An 11th Session Log entry → CLAUDE.md holds 10; `docs/session-log-archive.md` holds the oldest; concatenation preserves every byte of the moved entry.
7. `resume-session` on the fixture shows the Open Questions section and the single current status; "Last session" = the newest entry.
8. The only `git` mentions in the skill are inside the never-do-this constraint.

## 9. What NOT to change (Section 6 — Preservation Constraints)

- **resume-session's read-only nature and briefing shape** (beyond the named Open Questions rider) — it is the consumer; a reshaped briefing breaks the scan habit and re-opens the seam this spec closes. Don't "fix" the reader to compensate for writer bugs.
- **The daily-note inline-field grammar** — parsed by the fleet console's Dataview roll-up; prior entries already exist in this shape; "improving" it orphans them and blinds the console. This spec *pins* it.
- **The three-destination architecture** (CLAUDE.md + vault note + daily note) — each serves a different reader (repo-local resume; cross-project Obsidian status; timeline). Consolidation is a different product, not a fix.
- **`## Session Log` as the section name and `### <YYYY-MM-DD HH:MM>` as the entry heading** — resume-session greps for them (the consumer already speaks this vocabulary even though no instances exist on disk yet).
- **settings.json hook registrations and the SessionEnd path** (`session-end-flush.sh`, `flush.py`, `session-end-auto-stub.sh`) — load-bearing and latency-budgeted; this is a skill-text fix. **`daily-note-appender.sh` stays dormant/unregistered** — it is the pattern source; registering it would add a *third* writer to the anchor.
- **Rule #8 ownership** — the skill performs zero git operations; vault writes ride Obsidian-Git's commits, repo writes are the human's.
- **`vault/00_inbox/tickets.md` stays out of scope** — Rule #9's ticket lane has its own capture flow; routing Next Steps there too would double-capture.
- **`tpl-daily.md` / `tpl-project.md`** — writers conform to templates, never the reverse.
- **Anchor names and the `<!-- anchor -->` convention** — shared vocabulary across daily_driver, `vault_io.inject_at_anchor`, hooks, and this skill.
- **`agents-sdk/lib/vault_io.py` and `flush.py`** — precedent references only; no code edits ship with this spec.

---

## VALIDATION VERDICT — Profile: 4-element floor + voluntary Strategic Context / Edge Cases / Stop Rules — via audit_intent_spec (first 20,000 chars audited; the tail — the preservation-constraints list — hand-checked against Constraint Quality: each item names the thing AND why it's protected; no contradictions)
- Tool score: 11/25 unscoped; scoped interpretation below (floor runs Objective + Outcome; voluntarily included groups validated too; never below declared level).
- Objective Quality: warn → "new team member could understand": fixed — added the plain one-line opener ("A session-continuity skill exists so that closing a session never costs Sean the state it built").
- Outcome Quality: pass (4 outcomes, states not activities, measurable without self-report).
- Strategic Context: pass (consumers named WITH exact shapes).
- Edge Case Quality (voluntary): warn → network/API failure: fixed — added edge case 9 (MCP transport failure → built-in fallback → honest FAILED).
- Stop Rule Quality (voluntary): tool flagged missing-stop-rules anti-pattern → fixed — added §7 (per-destination one-retry halt, named escalations, receipt-as-completion). Zero-Interaction Mandate correctly NOT injected: the skill is interactive-only, and F10 architecturally keeps it un-hooked.
- Health Metrics: WAIVED (out of scope at floor) — the counter-metric role is carried by the Objective's priority order (truth ≥ zero-loss ≥ contract fidelity ≥ tidiness) and the preservation constraints; the Klarna-gap flag is answered by priority 1 being a quality guard on priority 2.
- User Goal: WAIVED (out of scope at floor) — carried verbatim by restated grounding (a)/(c)/(d).
- Decision Authority: WAIVED (out of scope at floor) — the two decisions that matter are explicitly human-owned (Fork A, Fork B) with recommendations + contingencies.
- Handoff rehearsal: case = "CLAUDE.md changed between Read and Edit (Daily Driver edited it mid-session) — old_string no longer matches." Objective + Stop rules force: re-Read, one retry, then honest FAILED + payload dump — yes, a weaker model reaches the right call. Strengthening pass = adding §7; re-test with fresh case ("vault folder renamed mid-week; direct match misses, context: scan misses") → Fork A offer + priority 1/4 force ask-and-report over guessing: yes.
