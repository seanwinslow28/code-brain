<!-- RT1 preserve-session fix-spec · OPUS baseline · 2026-07-05 · model=opus · harness=intent-engineering · agentId a51ff176b6785b2fb · 17 tool-uses / 257s -->

# Restated grounding (my understanding, confirmed against the repo)

**(a) What it's FOR.** Sean runs `preserve-session` at the end of a work session to hand off state to a future session with **zero loss**. It is the **WRITE** half of a two-skill pair; `resume-session` is the **READ** half. The pair only works if what preserve *writes* is exactly what resume *reads*, in the shape resume expects.

**(b) What FEEDS it / what it feeds.** Consumers: (1) `resume-session`, which reads back three destinations; (2) a human reading the project `CLAUDE.md`. The three write destinations are:
1. **Project `CLAUDE.md`** → a `## Session Log` section (decisions / blockers / next steps / files modified).
2. **The vault project note** under `vault/20_projects/` → four sub-targets: the `<!-- status-update -->` anchor (current state), the `ai-context` frontmatter field, the `## Key Decisions` table, and the `## Blockers` list.
3. **Today's daily note** at `vault/10_timeline/daily/YYYY-MM-DD.md` → the `<!-- claude-sessions -->` anchor, as one Dataview inline-field line.

It operates in a neighborhood of hooks that fire around it (confirmed in `.claude/settings.json`): `SessionStart` runs two inject hooks (`session-start-inject-index.sh`, `session-start-inject-tickets.sh`); `SessionEnd` runs `session-end-flush.sh` (spawns `flush.py`, which mines the transcript into `vault/knowledge/` **and** appends a separate `## Sessions` block to the daily note) and `session-end-auto-stub.sh`. **`preserve-session` is NOT itself wired to any hook — it is a manual/interactive skill** the user invokes by name.

**(c) What DISAPPOINTS today.** (i) `resume-session` misses items preserve claimed to capture — because they were never durably written (corroborated: `## Session Log` appears in **zero** real files across the tree; the skill's primary artifact has apparently never landed). (ii) You can't tell whether the vault / daily writes actually landed — Step 5 reports "saved" from the fact that steps *ran*, not from a read-back. (iii) It **always** reports "saved" even when the hand-off is lossy — a silent no-op and a real write print identical confirmations.

**(d) The WOW / desired end state.** Zero-loss reconstruction **in the reader's shape** (everything `resume-session` looks for is present where it looks for it), with **per-destination confirmation** that each write either **verifiably landed** (confirmed by re-reading the bytes) or was **skipped with a stated reason** — never a blanket "saved."

**Two genuine owner-forks** the findings flag, which I resolve below (never as a bare menu, never silently): **missing vault note** handling, and **flush-hook coexistence**.

---

# INTENT-CARRYING FIX SPEC — `preserve-session`

**Profile:** 4-element floor (Objective · Desired Outcome · The change per finding with reasoning · What NOT to change), per the intent-engineering Right-Sizing Decision Rule row 0. **One escalation beyond the floor is warranted and taken:** this is an existing skill whose failures include a **silent-confidence data-loss class** (findings #1, #2, #5, #7, #9) and a **downstream-contract shape** (the `<!-- claude-sessions -->` inline-field format that `daily_driver.py` parses, finding #6). Because the fix touches a downstream contract and adds a verification discipline, I pull in three named extras from the full template: a **Strategic Context** note (to pin the reader's shape and the flush-hook seam), **Edge Cases** (findings #4, #7, #9 are edge conditions with silent-failure blast radius), and a **Stop Rules / done** section. Everything else stays at floor ceremony. This skill is **interactive-only**, so the Zero-Interaction Mandate does **not** apply (its trigger is "runs unattended"; preserve-session is invoked by a present human).

---

## 1. Objective

`preserve-session` exists so a future session can be reconstructed with **zero loss** — it is the write half of the preserve/resume pair, and `resume-session` is the only automated reader of what it writes. Today it fails at its one job in the most dangerous way available: it **reports success from intent rather than from a verified write**, so a silent no-op and a real write are indistinguishable, and its primary artifact (`## Session Log`) has apparently never landed in a real file. The result is a hand-off that looks complete and is lossy — the exact failure a preservation tool is supposed to prevent.

**When facing any trade-off in this fix, prefer a visibly incomplete hand-off over a silently lossy one.** A destination that is honestly reported "skipped — anchor absent" is a success of this skill; a destination reported "saved" that a re-read cannot confirm is a failure, even if the write happened to work. Confidence without a read-back is the bug; **verification is the feature.** Every design choice below flows from that ordering — when the spec doesn't enumerate an edge case, resolve it by asking "which branch makes a loss *visible* to the next session?" and take that branch.

---

## 2. Desired Outcome (owner-observable, before → after)

| | Before (today) | After (this fix) |
|---|---|---|
| **Reader-shape fidelity** | `## Session Log` lands nowhere; resume reads an empty/absent section | Everything `resume-session` reads for — `## Session Log` in CLAUDE.md, `<!-- status-update -->` + `ai-context` + decisions table + blockers in the vault note, the `<!-- claude-sessions -->` inline-field line in the daily note — is present, in the exact shape resume expects. |
| **Landing proof** | "updated / appended" printed because the step ran | Each destination line reads **`landed (verified)`** — emitted only after re-reading the file and finding the written bytes — **or** **`skipped: <reason>`**. No third state. |
| **Honest skips** | silent no-op indistinguishable from a write | A missing anchor, a missing vault note, an absent daily note each produce a named skip with the reason and (where applicable) the fallback taken. |
| **Nothing captured is dropped** | "Open Questions" gathered, shown as done, written nowhere | Every category Step 1 gathers has a durable destination; Open Questions reaches the note and resume can resurface it. |
| **No stale state surfaced as current** | `<!-- status-update -->` appended → resume shows last week as "now" | `<!-- status-update -->` is **replaced** (current-state semantics); `<!-- claude-sessions -->` is **appended** (log semantics). |

**The single observable that proves the fix:** run preserve-session, then run `resume-session` in a fresh session — the briefing reconstructs the prior session with no gaps, and preserve's Step 5 output for that run contained only `landed (verified)` / `skipped: <reason>` lines, at least one of which (the CLAUDE.md `## Session Log`) is `landed (verified)`.

---

## 3. Strategic Context (the reader's shape + the flush-hook seam)

- **Downstream consumer #1 — `resume-session` (automated).** It reads, in order: the current-directory `CLAUDE.md` `## Session Log` (latest entry: decisions / blockers / next steps / files modified); the matching vault note's `ai-context` frontmatter + `<!-- status-update -->` content + blockers + key decisions; today's `<!-- claude-sessions -->` daily-note entries (else yesterday's). **preserve must write to exactly these locations in exactly these shapes** — this is the pair's whole contract.
- **Downstream consumer #2 — `daily_driver.py` (the fleet console).** It parses the `<!-- claude-sessions -->` anchor's inline-field line — `- [time:: HH:MM] | [domain:: …] | [context:: …] | **Outcomes:** … Link: [[prj-…]]` — for a Dataview roll-up. Field-name or pipe-structure drift makes that session **invisible to the fleet**. This line's format is a **hard contract**, not free text.
- **Adjacent writer — `flush.py` (SessionEnd hook).** On every session close, `flush.py` appends a **separate** `## Sessions` block to the same daily note (`\n---\n\n## Sessions\n- <tool>: <duration>, <messages> messages, tag: <tag> (<time>)`), delimited by `---`, and does **not** touch `<!-- claude-sessions -->`. It mines the transcript into `vault/knowledge/`. See §6 (What NOT to change) and Edge Case E5 for the coexistence resolution.
- **Vault auto-commit ownership (Rule #8, code-brain CLAUDE.md).** The Obsidian-Git plugin is the **sole** owner of vault auto-commit. preserve-session writes files; it must **never** invoke `git add`/`commit` against the vault. This is why the flush-hook fork below resolves to "stay two structures" rather than "have preserve reconcile them" — reconciliation would tempt a second write/commit path.

---

## 4. The change, per finding

Findings are grouped by severity. For each dangerously-wrong and structural finding I give **the specific change** and **the reasoning a weaker implementing model needs** to make the same call on an edge the spec didn't enumerate. Minor findings are brief.

### Dangerously-wrong

**#1 — Step 5 confirms from intent, not a verified read-back. + #2 — no write transport is named.** (Fixed together; they are the same root cause — an unnamed mechanism can silently no-op, and an unverified confirmation can't catch it.)

- **Change — name the transport.** Every write in Steps 2–4 uses the **`Edit` tool** (or `Write` when creating a file that does not yet exist), operating on the vault-as-codebase per the `vault-read-write` skill. Do **not** leave the mechanism to improvisation, and do **not** treat "the anchor already looks current" as license to skip. (mcp-obsidian is a *search* path only; it is not the write mechanism here.)
- **Change — verify every write by read-back.** After each destination write, **re-read the file** and confirm the specific bytes just written are present (the new `## Session Log` timestamp header for CLAUDE.md; the new `<!-- status-update -->` body; the new `[time:: …]` line for the daily note). Step 5 emits `landed (verified)` **only** on a positive read-back; if the read-back does not find the bytes, emit `✗ write failed — <what was attempted, where>` and do not claim success.
- **Reasoning for the weaker model:** the entire failure class is *silent confidence*. The remedy is not "try harder to write" and not retry logic — it is **making the outcome observable**. Treat "did the bytes land?" as a question you must answer by looking, never by assuming your own action worked. If you are ever tempted to print a status you have not just re-read, that temptation *is* the bug — resolve it by reading the file. A no-op you can see is a success of this skill; a write you can't confirm is a failure.

**#3 — vault-note match key #2 targets a nonexistent field.** The skill says "match by the `context` field in CLAUDE.md frontmatter," but **CLAUDE.md files carry no frontmatter**; `context:` lives on the **vault project note** (confirmed: `tpl-project.md` line 5, and real notes like `prj-16bitfit.md` line 6).

- **Change — invert the match.** The matching pipeline is: **(1) directory-name map** (see #4); **(2) if that is ambiguous or empty, scan `vault/20_projects/*/` for a note whose `context:` frontmatter value equals the working directory's basename** (e.g. cwd basename `16bitfit` → the note whose `context: 16bitfit`). Never look for `context:` in CLAUDE.md.
- **Reasoning for the weaker model:** the fallback key must live where the field actually is. `context:` is a property of the vault note, so you *read the vault notes* to find the match, not the CLAUDE.md. If both keys fail, that is the **missing-vault-note** case — go to Edge Case E1, do not guess a note.

**#4 — directory-name match has no target for the most-used repo (code-brain).** The worked example (`16bitfit/ → prj-16bitfit/prj-16bitfit.md`) assumes a single `prj-<name>.md`, but **`vault/20_projects/prj-code-brain/` is a folder of many sub-notes with no `prj-code-brain.md`** (confirmed: the file does not exist; the folder holds `prj-agent-wiring-rollout.md`, `prj-knowledge-loop-consumer.md`, etc.). Run at the end of a code-brain session — the common case — Step 3 today either silently skips or an improviser writes into an arbitrary wrong sub-note.

- **Change — resolve the folder-of-notes case explicitly.** The directory-name resolver returns a **single note file** only when `vault/20_projects/prj-<name>/prj-<name>.md` exists. If the folder exists but that canonical file does **not**, the resolver returns **"no single project note"** (an honest non-match), which routes to Edge Case E1 (missing-vault-note fork). It must **never** pick an arbitrary sub-note.
- **Reasoning for the weaker model:** "a folder named `prj-code-brain` exists" is **not** "a project note to write to exists." A directory full of sub-notes has no single canonical status surface; writing session state into a random sub-note corrupts an unrelated note and is worse than skipping. When the canonical `prj-<name>.md` is absent, treat the vault-note destination as *not resolvable* and fall to E1 — never salvage it by choosing one of the siblings.

### Structural

**#5 — the two vault anchors have opposite write disciplines; one blanket rule is half-wrong.** `<!-- status-update -->` holds **current state** and `resume-session` reads it as "where you left off" — so it must be **REPLACED** each session (appending stacks stale status and resume surfaces last week as current). `<!-- claude-sessions -->` is a **log** and must be **APPENDED** (replacing wipes the day's earlier lines = data loss). The single "PATCH not PUT" instruction is right for one and wrong for the other.

- **Change — split the discipline explicitly, per destination:**
  - `<!-- status-update -->`: **replace** the anchor's body (write the new current-state block between the anchor and the next `##` heading, discarding the prior body). Current-state semantics.
  - `<!-- claude-sessions -->`: **append** one new line directly below the anchor, leaving all prior lines intact. Log semantics.
  - `## Key Decisions` table: **append** new rows (never rewrite existing rows). Log semantics.
  - `## Blockers` list: **replace** the list with the current open blockers (resolved blockers drop off; this is a current-state surface resume reads for "open blockers"). If uncertain whether a blocker is still open, keep it and mark it — bias toward not dropping.
  - `## Session Log` (CLAUDE.md): **append** a new timestamped entry. Log semantics.
- **Reasoning for the weaker model — the rule that generalizes:** decide replace-vs-append by asking **"is this surface a *log* (a history readers scroll) or a *current-state snapshot* (a single 'now' readers trust)?"** Logs append (replacing = data loss). Snapshots replace (appending = stale state surfaced as current). "PATCH not PUT" only ever meant "don't rewrite the *whole file*" — it never dictated the within-anchor discipline. Apply this test to any anchor the spec didn't name.

**#6 — the daily-note anchor is a multi-owner, format-load-bearing surface.** `daily_driver.py` parses the exact inline-field line for a Dataview roll-up; field drift makes a session invisible to the fleet console.

- **Change — treat the inline-field line as a hard contract.** The daily-note append MUST be exactly:
  `- [time:: HH:MM] | [domain:: <domain>] | [context:: <project>] | **Outcomes:** <one sentence>. Link: [[prj-<project>]]`
  Field names (`time`, `domain`, `context`), pipe delimiters, and the `Link: [[prj-…]]` tail are fixed. `HH:MM` is 24-hour local (see #11). Do not invent fields, reorder, or reword the labels.
- **Reasoning for the weaker model:** this line is read by machine, not just by a human. It is a schema. Improving the wording breaks the parser and silently removes the session from the fleet roll-up. Fidelity beats polish here — copy the format, fill only the bracketed values.

**#7 — daily-note write silently no-ops on any day the Daily Driver hasn't run.** Step 4 is guarded "if today's daily note exists," but the note (with its `<!-- claude-sessions -->` anchor) only exists once the Daily Driver creates it at 08:45. Evening / weekend / out-of-band sessions skip the daily write with no create-or-locate. → Resolved in **Edge Case E2** (create-from-template).

**#8 — "Open Questions" is gathered but routed nowhere.** Step 1 extracts five categories; the Session Log template carries four. Open Questions — the one class Sean flags for his own next-session decision — is gathered, shown as work-done, written nowhere; resume has no source to resurface it.

- **Change — give Open Questions a durable home in both readable surfaces:**
  - Add an **`**Open Questions:**`** field to the CLAUDE.md `## Session Log` entry template (fifth field, after Files Modified).
  - Also write open questions into the vault note's **`## Open Questions`** section when that section exists (real notes like `prj-16bitfit.md` have one — append items; create the section under `## Blockers` if absent and a vault note was resolved).
- **Reasoning for the weaker model:** a category you gather and display but never persist is a lie told to the next session — it was "captured" only in the transcript that is about to be discarded. Anything Step 1 extracts must land in a surface `resume-session` reads. Open Questions is the highest-value such class (it's Sean's own next-decision queue), so it gets a field, not a footnote.

**#9 — no adapter for a missing/renamed anchor.** "PATCH into `<!-- status-update -->`" has no defined behavior when the anchor is absent (hand-edited note, note predating the template). → Resolved in **Edge Case E3**.

**#10 — no stated relationship to the SessionEnd flush hook.** `session-end-flush.sh` fires on every close and mines the transcript into `vault/knowledge/`; preserve-session is the interactive structured write. Overlap / ordering / dedup undefined. → Resolved in **Edge Case E5** and §6.

### Minor

- **#11 — timestamp has no timezone/source.** Stamp all times as **`HH:MM` 24-hour, machine local time** (the timezone the daily-note filename `YYYY-MM-DD.md` is derived in). Use one consistent clock for the `## Session Log` header and the daily-note `[time::]` field so resume can order correctly.
- **#12 — "ai-context under 200 chars" has no summarize-don't-truncate rule** (real values run ~380 chars). **Change:** "Keep `ai-context` a **summary** of ≤200 characters — *rewrite* to fit, never hard-truncate mid-sentence. If the current state genuinely needs more than 200 chars, write the fullest coherent sentence that fits and put the remainder in `<!-- status-update -->` (which has no cap)."
- **#13 — `## Session Log` has no cap/rotation.** **Change:** cap the CLAUDE.md `## Session Log` at the **most recent 10 entries**; when appending an 11th, drop the oldest. (CLAUDE.md is read first every session; unbounded growth taxes every read. 10 is enough for resume, which only reads the latest.) Keep it lightweight — this is a nicety, not a gate.

---

## 5. Edge Cases (the two owner-forks + the silent-skip conditions)

**E1 — Missing / unresolvable vault project note (OWNER-FORK #1 — resolved here, not left as a menu).**
The current skill says "report it but don't auto-create." The findings offer three options: (i) report-and-skip; (ii) auto-scaffold from `tpl-project.md` then write; (iii) redirect the structured block into CLAUDE.md as a fallback.

- **RESOLUTION — I recommend option (iii): redirect-to-CLAUDE.md fallback, with a report.** This is a *recommendation with its contingency*, because the record does not pre-decide it (the current skill's "don't auto-create" is a stated preference, so I do **not** silently override it toward auto-scaffolding).
  - **Why (iii):** The Objective is **zero loss**. Option (i) loses the session's status/decisions/blockers entirely when the common code-brain case hits (finding #4) — unacceptable against the Objective. Option (ii) auto-creating a `prj-<name>.md` writes a **new tracked vault file** on a bare session-save, which collides with Rule #7 (new active-domain content is a deliberate act) and Rule #8 (Obsidian-Git will auto-commit a note the user never chose to create) — it makes a filing decision the human should make. Option (iii) loses nothing and creates no unwanted vault file: the vault-bound block (status, decisions, blockers, open questions) is written into a **`## Vault Handoff (no project note found)`** subsection of the CLAUDE.md `## Session Log` entry instead, and Step 5 reports **`vault note — skipped: no note resolved for '<dir>'; captured in CLAUDE.md instead`**. `resume-session` still finds it because it reads CLAUDE.md first.
  - **Contingency / when to revisit:** if Sean later wants a real vault note for that project, the CLAUDE.md handoff block is the material to seed it from — this fallback is a holding pen, not a permanent home. If the owner **prefers** report-and-skip (i) or auto-scaffold (ii), that is a one-line change to this branch; flag it at spec-review. Do **not** implement all three behind a flag — pick one default (iii) and state it.
- **Reasoning for the weaker model:** the ranking is driven by the Objective (never lose the content) *and* the two repo rules (don't create tracked vault files the user didn't ask for; never stand up a second commit path). When you hit an unresolvable note, the safe move is **capture-in-CLAUDE.md + honest skip line**, never invent a vault note and never drop the content.

**E2 — Today's daily note does not exist (finding #7).** The daily note only exists after the Daily Driver runs (08:45); evening/weekend/out-of-band sessions have none.

- **RESOLUTION:** **Create it from `vault/90_system/templates/tpl-project.md`'s sibling `tpl-daily.md`** at `vault/10_timeline/daily/YYYY-MM-DD.md` (resolving the Templater `<% %>` tokens: `date` and title = today's date), then append the session line to its `<!-- claude-sessions -->` anchor. Report `daily note — created + appended` vs `daily note — appended`. Creating today's daily note is squarely inside the vault's normal timeline structure (unlike creating a *project* note, E1), so auto-create is correct here.
- **Reasoning for the weaker model:** the asymmetry with E1 is deliberate — a **daily note is a dated timeline slot** the system expects to exist for every active day (auto-create = filling a known slot); a **project note is a filing decision** (auto-create = making a choice for the human). Create the former, never silently create the latter. If the daily template file is itself missing, fall back to writing a minimal note containing the `## Claude Code Sessions\n<!-- claude-sessions -->` anchor, then append — losing the line is not an option.

**E3 — Target anchor absent in an existing file (finding #9).** A vault note or daily note exists but lacks the expected `<!-- status-update -->` / `<!-- claude-sessions -->` anchor (hand-edited, predates template).

- **RESOLUTION:** Do not write blindly. In priority order: (a) if the matching `##` heading exists (`## Current Status`, `## Claude Code Sessions`) but the anchor comment is gone, **re-insert the anchor comment under that heading**, then write. (b) If neither heading nor anchor exists, **append the whole section** (heading + anchor + content) at end of file. (c) Either way, report the repair in Step 5: `<destination> — anchor restored + written`. Never report plain success for a write whose anchor you had to improvise.
- **Reasoning for the weaker model:** a missing anchor is a *repairable* condition, not a reason to abandon the write or a license to dump text at a guessed location. Restore the structural landmark, then write to it — and surface that you did so, so the human knows the note drifted from template.

**E4 — Empty session (nothing to preserve).** No decisions, no files modified, no blockers.

- **RESOLUTION:** Write nothing to any destination; emit `nothing to preserve — no durable changes this session` as the entire Step 5 output. Do not write an empty `## Session Log` stub (it pollutes the file resume reads first).
- **Reasoning for the weaker model:** the honest report *is* the deliverable. An empty entry is noise that makes resume's job harder; a clear "nothing to preserve" is a correct, complete run.

**E5 — Flush-hook coexistence (OWNER-FORK #2 — resolved here).** `session-end-flush.sh` also writes the same day's session record — as a plain-append `## Sessions` block, **not** into `<!-- claude-sessions -->` — and mines the transcript into `vault/knowledge/`. The findings ask: stay two separate structures, or reconcile into one? (This bears on Rule #8 — no second auto-commit mechanism.)

- **RESOLUTION — stay two separate structures; preserve owns only `<!-- claude-sessions -->`; do not touch `## Sessions`.**
  - **Why:** They serve different readers and different write disciplines. `<!-- claude-sessions -->` is the **human-authored, Dataview-parsed** roll-up (`daily_driver.py` reads it) — that is preserve-session's lane. `## Sessions` is **flush.py's machine-generated telemetry** (tool, duration, message count) delimited by `---` — that is the hook's lane, written by an autonomous process on every close. Reconciling them would require preserve-session to **read and rewrite flush's block**, i.e. stand up a second writer over a surface an autonomous hook owns — which invites exactly the "two auto-commit systems" class of merge conflict Rule #8 exists to prevent. Keep the lanes separate; each anchor/block has exactly one owner.
  - **De-dup / ordering:** preserve-session makes **no attempt** to dedup against `## Sessions` and does not order relative to the flush hook. The two coexist; a human scanning the daily note sees one rich human line (`<!-- claude-sessions -->`) and one thin telemetry line (`## Sessions`), which is the intended, honest picture (one is "what I did," the other is "how long the session ran").
  - **Contingency / when to revisit:** if the duplication ever becomes noise Sean wants gone, the correct move is to change **flush.py** (the autonomous writer) to skip `## Sessions` when a `<!-- claude-sessions -->` line already exists for that session — **not** to have the interactive skill reach into the hook's block. Flag that as a follow-up ticket if it comes up; do not build it into this fix.
- **Reasoning for the weaker model:** "two records of the same session" is not automatically a bug to merge. Ownership is the deciding principle: **one surface, one writer.** preserve-session writes the human anchor; the hook writes the telemetry block; neither edits the other's. When two systems touch the same file, separate anchors with single owners is the safe topology — shared-rewrite is where data-loss and commit-conflicts come from.

---

## 6. What NOT to change (Preservation Constraints — confirmed-correct, with why)

- **The `<!-- claude-sessions -->` inline-field line format** — `- [time:: HH:MM] | [domain:: …] | [context:: …] | **Outcomes:** … Link: [[prj-…]]`. **Protected because** `daily_driver.py` parses it verbatim for a Dataview roll-up; any field/pipe drift makes the session invisible to the fleet console (finding #6). Fill the bracketed values; touch nothing else.
- **flush.py's `## Sessions` block and everything under `vault/knowledge/`.** **Protected because** it is owned by the SessionEnd flush hook, an autonomous writer; preserve-session must not read, rewrite, or dedup against it (E5, Rule #8).
- **The append-only discipline for `## Session Log`, `<!-- claude-sessions -->`, and the `## Key Decisions` table.** **Protected because** these are logs/history — the existing "never overwrite existing content — append only" instruction is *correct for these three surfaces* (finding #5 only overturns it for the current-state surfaces `<!-- status-update -->` and `## Blockers`). Do not "simplify" the split back into one blanket rule.
- **The `<!-- anchor -->` PATCH pattern itself** and the anchor vocabulary in `vault-read-write` (`tpl-project` → `<!-- status-update -->`, `<!-- git-commits -->`; `tpl-daily` → `<!-- jira-log -->`, `<!-- claude-sessions -->`, `<!-- side-projects -->`). **Protected because** it is the shared read/write contract across preserve, resume, daily_driver, and flush; anchors are load-bearing landmarks — never rename or remove one (only restore a missing one, per E3).
- **Never invoke `git add`/`git commit` against the vault.** **Protected because** Obsidian-Git is the sole vault auto-commit owner (Rule #8); preserve-session writes files and stops. This is why E1 resolves to CLAUDE.md-capture, not auto-scaffolding, and E5 resolves to separate-owners, not reconcile.
- **`resume-session` is read-only and unchanged by this fix.** **Protected because** it is the reader; the fix makes preserve *write the shape resume already expects*. Do not "co-fix" resume — if the shapes match after this change, the pair works. (If a future change alters the shape, that is a **paired** preserve+resume change, flagged as such.)
- **The skill stays interactive/manual — do NOT wire it to a hook.** **Protected because** its trigger is a present human ("save my progress"); a present human means **no** Zero-Interaction Mandate, and hooking it onto SessionEnd would collide with the flush hook already there (finding #10 / E5). Its aspiration to be SessionEnd-hooked is explicitly **not** adopted.

---

## 7. Done looks like (checkable statements)

1. **Transport named:** the SKILL.md Protocol names `Edit` (and `Write` for file creation) as the write mechanism for all three destinations, and every write step is followed by a re-read verification step.
2. **Read-back gate:** Step 5's output vocabulary is exactly `landed (verified)`, `skipped: <reason>`, `✗ write failed — <detail>`, or (empty session) `nothing to preserve …`. No bare "updated / appended / saved" strings remain.
3. **First-run proof:** on a real save, a fresh `resume-session` reconstructs the session with no gaps, AND the project `CLAUDE.md` now contains a `## Session Log` section with the run's timestamped entry.
4. **Match key inverted:** the Protocol's vault-note matching reads `context:` from the **vault note**, never from CLAUDE.md; the directory resolver returns a note only when `prj-<name>/prj-<name>.md` exists, else routes to the missing-note branch.
5. **Anchor disciplines split:** `<!-- status-update -->` and `## Blockers` are documented **replace**; `<!-- claude-sessions -->`, `## Key Decisions`, `## Session Log` are documented **append**.
6. **Open Questions durable:** the `## Session Log` entry template carries an `**Open Questions:**` field, and the Protocol writes open questions to the vault note's `## Open Questions` section when present.
7. **Daily-note create path:** Step 4 creates today's daily note from `tpl-daily.md` when absent, then appends; the "if today's daily note exists" silent-skip guard is gone.
8. **Anchor-repair path:** a missing target anchor is restored under its `##` heading (or the section appended) and the repair is reported, rather than a blind write reported as success.
9. **Both owner-forks decided in text:** E1 states redirect-to-CLAUDE.md as the default with its contingency; E5 states stay-two-structures with its contingency. Neither appears as a bare menu; neither is silently picked.
10. **Preservation respected:** the inline-field line format is byte-unchanged; no `git` invocation against the vault appears anywhere in the skill; the skill remains unhooked.
11. **Caps:** `ai-context` write is summarize-to-≤200 (no mid-sentence truncation) and `## Session Log` caps at 10 entries.

*(No unit-test harness ships for `.claude/skills/*.md` in this repo — these are prose-checkable greps + the two behavioral proofs in #3/#4. The single highest-value manual test is #3: save a real session, resume it clean, confirm `## Session Log` exists.)*

---

## VALIDATION VERDICT — Profile: 4-element floor + 3 named escalations (Strategic Context, Edge Cases, Stop/Done) — hand-run (intent-engineering MCP tools not mounted; SKILL.md prose method is the declared fallback)

- **Objective Quality:** pass — states the problem, why it matters, and a trade-off line that decides ambiguous cases (*prefer a visibly incomplete hand-off over a silently lossy one; verification is the feature*).
- **Outcome Quality:** pass — 5 outcomes stated as owner-observable before→after states, each verifiable without agent self-report; the single load-bearing observable is named.
- **Edge Case Quality (in scope — voluntarily included):** pass — 5 edge cases (E1–E5) with explicit fallback behavior; empty-session (E4) and both owner-forks (E1, E5) handled with a recommendation + contingency, never a bare menu.
- **Constraint / Preservation Quality (in scope — fix spec, mandatory):** pass — §6 names each protected thing *and* its reason.
- **Zero-Interaction Mandate:** correctly **omitted** — trigger is "runs unattended"; this skill is invoked by a present human and §6 forbids hooking it.
- **Handoff rehearsal (pre-emit, one fresh case not enumerated):** *"preserve-session is run inside a git worktree of code-brain whose cwd basename is `code-brain-wt3`, which maps to no `prj-<name>` folder at all."* → the directory resolver finds no `prj-code-brain-wt3/`, the `context:` scan finds no note with `context: code-brain-wt3`, so the vault-note destination is unresolvable → E1 fires → captured in CLAUDE.md, honest skip line, nothing lost, no stray vault note invented. One rehearsal, no Objective rewrite needed.

**VALIDATION: PASS** — the spec is emit-ready.

---

*Final note to the caller:* Two owner-forks resolved as **defaults + contingencies**, not silent picks: **E1** → redirect-to-CLAUDE.md; **E5** → stay-two-structures. Both one-line reversible at spec-review. Key repo-verified facts: `## Session Log` in zero real files; `prj-code-brain.md` does not exist; the write transport is filesystem `Edit`/`Write` per `vault-read-write`; `daily_driver.py` parses the `<!-- claude-sessions -->` line; `flush.py` appends a separate `## Sessions` block; `preserve-session` is not wired to any hook.
