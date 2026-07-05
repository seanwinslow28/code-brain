# Council Session — wwf5d-val-rt1-AB

- **Session ID:** `20260705-135214-284a5a`
- **Profile:** `variance`
- **Duration:** 271.1s
- **Tokens:** 115108 in, 14510 out
- **Cost:** $0.7932

## Original prompt

```
Two independent authors produced these two artifacts for the identical task from the identical inputs. Judge which is the stronger artifact.

## Task context

Both artifacts are an intent-carrying fix spec for a session-preservation skill (a "preserve-session" tool that hands off state from one work session to a future one), written from the same findings about the same skill.

## Judging rubric — score ONLY these; ignore length and prose polish

1. **Decidedness** — pre-made decisions (field names, error shapes, done-criteria), edge guidance a weaker implementer could act on; not options/hedging.
2. **Self-consistency** — does any rule the artifact states contradict its own stated objective? (e.g. a "cap-and-delete" inside a zero-loss spec; a step that writes a value nothing downstream reads.)
3. **Breadth / evidence-discipline** — did it verify claims against the real system (real files, live docs, the actual tool) vs reason from text; did it audit seams the brief didn't name.
4. **Task-specific** — does the artifact catch these two self-contradictions in the source material, if present: (i) an "Open Questions" section that gets written but never read downstream by anything; (ii) a cap or limit that silently drops gathered data inside a spec whose stated objective is zero data loss?

## Bias controls

One artifact is substantially longer than the other — do NOT reward length. A shorter artifact that is more decided and more self-consistent wins over a longer one that merely says more. Judge A and B strictly on merit regardless of which order they appear in below.

## ARTIFACT A

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

## ARTIFACT B

# Fix Spec — `preserve-session` skill

**Profile: 4-element floor (fix spec)** — Objective, Desired Outcome, The change per finding (with reasoning-to-carry), What NOT to Change. Sized per the intent-engineering Right-Sizing Decision Rule Row 0. The skill is **interactive-only** (`[agents.preserve_session] enabled = false` in `config.toml`, no launchd schedule), so this is not a scheduled/autonomous change and the full 9-section template is not warranted. Two findings (#6 daily-note format contract, #8 Open-Questions routing) reach into a *downstream contract* — resume-session's read shape and the fleet console's Dataview parse — so those two carry the paired-change protocol and edge up to per-fix reasoning, but the spec as a whole stays at the floor. No autonomy level, hard constraint, or execution limit changes.

---

## Grounding — restated, then used

The task pre-supplies four grounding facts. Restated in my own words, each then does work below (§1.1 — consume, don't just restate):

- **(a) For.** Sean runs preserve-session at session end to hand off state with **zero loss** to a future session. It is the **WRITE** half; resume-session is the **READ** half. → This makes *zero-loss* the spec's Objective invariant (§6.9): every fix is re-checked against it, and any rule that drops a gathered item (a cap that deletes, a fail-open skip) is a self-contradiction the objective overrides. It also means the reader's *shape* is the target the writer must hit — findings #5, #6, #8 are all "wrote it, but not where/how the reader can use it."
- **(b) Feeds.** Consumers: resume-session + a human reading CLAUDE.md. Three destinations: (1) project CLAUDE.md `## Session Log`; (2) the vault project note's `ai-context` / `<!-- status-update -->` / decisions table / blockers; (3) today's daily note `<!-- claude-sessions -->`. SessionStart inject hooks + a SessionEnd flush hook operate nearby. → This is the seam inventory. I traced each destination to its *point of effect* (§2.3): resume-session's exact extract list (its lines 26/30/33), the daily anchor's Dataview parser, and the flush hook's *actual* write target. Two of those traces broke the skill's stated assumptions (see #6 and #8).
- **(c) Disappoints.** Resume misses captured items; you can't tell if vault/daily writes landed; the skill **always reports "saved"** though the hand-off is lossy. → This is the `dangerously-wrong` core: silent × trusted × propagating (§4). The confirmation is believed, and it's wrong on the failure path — which is *most* paths, since `## Session Log` has landed in **zero** CLAUDE.md files across the tree (verified).
- **(d) Wow.** Zero-loss reconstruction **in the reader's shape**, with **per-destination confirmation** that each write landed or was **skipped-with-a-reason**. → This is the Desired Outcome, verbatim in intent. "Skipped-with-a-reason" (never a silent skip, never a false "saved") is the load-bearing phrase every fix serves.

**Live-system checks I ran before writing** (§1.3 — expand to first-degree references, inspect measured state):
- `grep -rl "## Session Log" --include=CLAUDE.md` → **0 files**. The skill's primary artifact has never landed. (Confirms #2.)
- CLAUDE.md files (root, anima, creative-studio, life-systems) carry **no YAML frontmatter**; `context:` lives on the vault note (`context: 16bitfit`, line 5 of `prj-16bitfit.md`). (Confirms #3.)
- `vault/20_projects/prj-code-brain/` is a **folder of sub-notes** (`prj-automode.md`, `prj-knowledge-loop-consumer.md`, `prj-agent-wiring-rollout.md`, …) with **no `prj-code-brain.md`**. (Confirms #4.)
- Real daily notes live at **`vault/10_timeline/daily/`** (e.g. `2026-06-10.md`), anchor `<!-- claude-sessions -->` present at line 161. **`vault/daily/` does not exist.**
- **flush.py resolves `vault_daily_dir = cfg.vault_root / "daily"` → `vault/daily/`** (config.toml `vault_root` line 3). It **appends a raw `## Sessions` block** via `format_daily_log_body` (line 172), **creates the file if missing** (lines 210–212), and **never touches `<!-- claude-sessions -->`**. So preserve-session and flush.py target **different directories** and **different sections** — a sharper form of #6/#7 than the finding states. (See #6 change note.)
- SessionEnd hook chain (`.claude/settings.json`): `session-end-flush.sh` then `session-end-auto-stub.sh`. Obsidian-Git is the **sole vault auto-commit owner** (root CLAUDE.md Rule #8).
- `mcp-obsidian` (with `patch_content`/`append_content`) is documented only as an **optional Claude-Desktop** setup (`obsidian-mcp-setup` skill); it is **not guaranteed mounted** in a Claude Code CLI session. → the write transport must floor on always-available built-ins.

---

## 1. Objective

**The problem.** `preserve-session` promises three structured writes but has no verified mechanism for any of them, aims two of them at targets that do not reliably resolve, and then reports success from the fact that its *steps ran* rather than from a re-read confirming bytes landed. The observable result: a session-end hand-off that says "saved" while losing state — proven by `## Session Log` existing in **zero** CLAUDE.md files. This matters because preserve-session is the WRITE half of the only zero-loss continuity path Sean has; when it lies about landing, resume-session silently reconstructs from missing or stale data, and the loss is invisible until a future session is already working from a wrong premise.

**Trade-off priority for unspecified cases.** Prefer a **visibly incomplete, honestly-reported** hand-off over a **silently lossy, confidently-"saved"** one. When any fix decision is ambiguous, choose the branch that (a) preserves the gathered item somewhere durable and (b) tells the truth about where it landed or why it didn't. Zero loss beats vault-tidiness; an honest SKIP beats a fabricated success. This line is the designed fallback when the spec doesn't enumerate a case (§6.2).

---

## 2. Desired Outcome (owner-observable, before → after)

| | Before (today) | After (this fix) |
|---|---|---|
| **Confirmation** | Step 5 prints "CLAUDE.md updated / Vault note updated / Daily note appended" because the steps executed. A silent no-op and a real write print **identically**. | Every destination line reports one of exactly three states, each derived from a **read-back**: `WRITTEN & VERIFIED — <what, where>`, or `SKIPPED — <reason>`, or `FAILED — <reason + the exact payload, so nothing is lost>`. No fourth state; no unqualified "saved". |
| **CLAUDE.md** | `## Session Log` claimed, never lands (0 files). | The `## Session Log` entry is present in the file after the run, confirmed by re-reading the file and finding the new timestamped block. |
| **Vault note match** | Falls back to a `context:`-in-CLAUDE.md key that never exists; directory-name match has no target for `prj-code-brain`. | Match resolves against fields that actually exist; the code-brain "folder-not-note" case is handled explicitly; an unresolved match is a reported SKIP, never a guessed wrong sub-note. |
| **Two vault anchors** | One blanket "PATCH not PUT" rule stacks stale status under `<!-- status-update -->`. | `<!-- status-update -->` is **replaced**; `<!-- claude-sessions -->` is **appended**. resume-session surfaces *current* status, not last week's. |
| **Daily note** | Silent no-op on any day the Daily Driver hasn't created the note. | The note is located or created at the correct path; the session line lands in the anchor in the exact format the fleet console parses. |
| **Open Questions** | Gathered, shown as work-done, written nowhere; resume-session can't resurface it. | Written to a durable destination **and** resume-session is taught to read it back — the one class Sean flags for his own next decision survives the hand-off. |

---

## 3. The change, per finding

Notation: **DW** = dangerously-wrong, **S** = structural, **m** = minor (from the findings file). Each DW/S fix carries the reasoning a weaker implementing model needs to make the same call on an edge the spec didn't enumerate (§6.2).

### 3.1 [DW] #1 — Confirm from a verified read-back, not from "the step ran"

**Change.** Replace Step 5 "Confirm" with a **read-back verification** per destination. After each write, **re-read the target region** and assert the just-written content is present; the Step-5 report line is *emitted from that assertion*, not from the fact that a write was attempted. Report vocabulary is fixed to three states only:

- `WRITTEN & VERIFIED — <destination>: <one-line what landed>` — the re-read found the new content.
- `SKIPPED — <destination>: <reason>` — the write was deliberately not performed (e.g. no vault note found; daily anchor absent and create declined). A skip is a *decision with a reason*, never silence.
- `FAILED — <destination>: <reason>. Unsaved payload: <the exact text that did not land>` — a write was attempted and the re-read did **not** confirm it. Dumping the payload is mandatory so the item is recoverable by hand.

**Reasoning to carry.** The root cause of the whole skill is *reporting from intent instead of from state* (§5.4 — state lives on the artifact, not in promised behavior). The fix is not "add a retry loop" (an interactive human is present and can act on a FAILED line; a retry masks the signal). The fix is **make the report a function of a fresh read**. Edge rule the spec can't enumerate exhaustively: if you ever cannot re-read a destination to verify (permission, transport error), that destination is `FAILED` with its payload dumped — **never** `WRITTEN & VERIFIED`, and **never** silently downgraded to a bare `SKIPPED`. Verified means *you looked and saw it*; anything short of that is Failed-or-Skipped, and the difference is whether you *tried*.

### 3.2 [DW] #2 — Name the write transport, with a fallback ladder and an anti-skip rule

**Change.** Add a **Write Mechanism** subsection consumed by Steps 2–4. The transport is a fixed ladder, floored on always-available built-ins:

1. **`Edit`** (built-in) for modifying an existing file/region — anchor replacement, appending a Session Log entry to an existing CLAUDE.md, replacing `<!-- status-update -->` content, inserting into `<!-- claude-sessions -->`. **`Write`** (built-in) only when creating a file that does not yet exist (a missing daily note; a scaffolded vault note if that fork is taken — see §6).
2. **Optional upgrade:** if the `mcp-obsidian` MCP is **mounted in this session** and exposes `patch_content` / `append_content`, its anchor-aware write MAY substitute for the vault-note writes — but the §3.1 read-back still runs afterward regardless of which transport wrote. mcp-obsidian is **not** assumed present (it is an optional Claude-Desktop setup, not part of this repo); when absent, the built-in `Edit`/`Write` path is the mechanism, not a stall.

**Anti-skip rule (the load-bearing half).** The common improvisation — *"the anchor already looks current, so I'll skip the write"* — is **forbidden**. preserve-session's whole job is to capture *this* session; "looks current" is never grounds to skip, because the current-looking content is from a *prior* session. Perform the write, then verify. The only legitimate non-write is a `SKIPPED — <reason>` where the reason is a real blocker (no target resolves), not "it looked done."

**Reasoning to carry.** §2.4 / §5.4: an unnamed mechanism is a false sense of safety worse than an admitted gap — the executor improvises, and the cheapest improvisation is the silent no-op that produced the zero-landed-files evidence. Naming `Edit`/`Write` as the floor guarantees the mechanism exists in every Claude Code session. Edge rule: if a write genuinely cannot be performed by any available transport, that is `FAILED` with payload dump (§3.1), not an invented success. Never retry a transport in a loop — one attempt, then verify, then report.

### 3.3 [DW] #3 — Fix the vault-note match keys to fields that exist

**Change.** Rewrite Step 3's match logic. The current match key #2 — "the `context` field in CLAUDE.md frontmatter" — is **deleted**: verified, CLAUDE.md files carry no frontmatter, so this key can never fire. Replace the match procedure with, in order:

1. **Directory-name → note-name convention**, but handled per §3.4 (the folder-vs-note case is real).
2. **`context:` field on the *vault note*** (not CLAUDE.md): scan `vault/20_projects/**/*.md` frontmatter for a `context:` value matching the working directory's basename (e.g. working in `16bitfit/` → note with `context: 16bitfit`). This is where `context:` actually lives.
3. If neither resolves to a single note → **SKIP with reason** (§3.5), never a guess.

**Reasoning to carry.** §2.4 (existence-check every claim about the world): the skill asserted a field location without checking it. The correcting principle is *match on fields that are observed to exist in the store you're reading*. Edge rule: if step 1 and step 2 resolve to **different** notes, prefer the explicit `context:` match (step 2) — a frontmatter field authored by a human is a stronger signal of intent than a directory-name coincidence.

### 3.4 [DW] #4 — Define the target for the folder-that-is-not-a-note case (the code-brain common case)

**Change.** Add explicit handling for the case where the directory-name match points at a **folder of sub-notes with no single top-level note** — verified true for `vault/20_projects/prj-code-brain/`, which is the most common session-end repo. When the derived note path (`vault/20_projects/prj-<name>/prj-<name>.md`) **does not exist as a file**:

1. Try the `context:`-on-vault-note match (§3.3 step 2) first — it may resolve to a real sub-note the human tagged.
2. If that also fails to resolve to a single note → **do not** write the structured block into an arbitrary sub-note. Instead, **redirect the vault block into the project CLAUDE.md** as a fallback destination (append it under the `## Session Log` entry as a `**Vault note:** not resolved — captured here instead` sub-block), and report `SKIPPED — vault note: no single note for <dir>; block preserved in CLAUDE.md`.

**Reasoning to carry.** §2.3 (trace to point-of-effect) + the Objective's zero-loss priority: the failure here is *silent loss or wrong-destination write*. Guessing a sub-note pollutes an unrelated note and is unrecoverable; the CLAUDE.md redirect preserves the content in a destination that *definitely* exists and that resume-session *definitely* reads, at the cost of it not being in the vault. Zero-loss beats vault-placement (Objective trade-off line). Edge rule: never invent a `prj-code-brain.md` — creating the canonical note for a multi-note folder is a vault-structure decision that is not preserve-session's to make.

### 3.5 [S] #5 — Split the two vault anchors' write disciplines, with a distinguishing test

**Change.** Replace the single "PATCH not PUT" instruction with **two rules keyed to the anchor's semantics**:

- `<!-- status-update -->` holds **current state** → **REPLACE** the anchor's body each session. (resume-session reads it for "where you left off"; appending stacks stale status and resume surfaces last week as current.)
- `<!-- claude-sessions -->` (and the CLAUDE.md `## Session Log`) is a **log** → **APPEND** a new timestamped entry, never replace. (Replacing wipes the day's earlier lines = data loss.)

Add a one-line **discipline test** the implementer can run: *does resume-session read this region as "the current state" or as "a history"? Current-state → replace; history → append.*

**Reasoning to carry.** §2.5 (degraded/asymmetric paths) + §6.9 (hold the objective): one blanket rule is *half-wrong by construction* — correct for the append region, data-losing for the replace region, and the reverse mislabeling (append-to-status) is the subtler bug because it doesn't lose data, it *poisons freshness*. The generalizable rule is **write-discipline follows read-semantics**: match the reader's expectation of the region, not a global preference. This is the discriminating rule for any *future* anchor the skill learns to write.

### 3.6 [S] #6 — Mark `<!-- claude-sessions -->` a shared, format-load-bearing surface; pin the line shape; state the flush relationship; fix the path

**Change (three coupled parts):**

**(a) Pin the exact line format** the fleet console parses. The daily session line MUST be emitted as the inline-field Dataview shape:
```
- [time:: HH:MM] | [domain:: <domain>] | [context:: <project>] | **Outcomes:** <1-sentence summary>. Link: [[prj-<project>]]
```
Every field is required. If a field's value is unknown at write time, emit a **placeholder, never omit the field** — `[domain:: unknown]`, `[context:: unknown]`, `Link: [[prj-unknown]]`. A dropped field (not just a wrong value) makes the whole session **invisible** to the Dataview roll-up on the daily-note fleet console.

**(b) Fix the path.** The correct daily-note directory is **`vault/10_timeline/daily/YYYY-MM-DD.md`** (verified; this is also what resume-session Step 1 reads). The skill's current text is already correct on this; the fix is to keep it pinned and add the note below.

**(c) State the flush relationship explicitly** (this also resolves finding #10 and Fork 2). Add a note: *"`session-end-flush.sh` → `flush.py` is a separate SessionEnd hook that mines the transcript into `vault/knowledge/` and appends a raw `## Sessions` block to `vault/daily/YYYY-MM-DD.md` (a different directory and a different section from this skill's `<!-- claude-sessions -->` anchor in `vault/10_timeline/daily/`). The two do not collide and must not be merged: flush is unattended knowledge-extraction; preserve-session is the interactive, structured, human-triggered hand-off for resume-session. preserve-session does not write to `vault/knowledge/` and does not touch the `## Sessions` block. Do not add a second vault auto-commit step — Obsidian-Git is the sole auto-commit owner (root CLAUDE.md Rule #8)."*

**Reasoning to carry.** §2.3 (arrives-but-unreadable) + §5.1 (name WHO and the exact SHAPE): the anchor is a **cross-owner contract**, not private free-text. `daily_driver.py` parses this exact line for a Dataview roll-up; drift makes a session vanish from the console silently. **This is a paired-change awareness:** the line shape is *consumed by* the fleet console — if a future edit changes the fields, it must change the console's parser too, or file a ticket (§2.7). Edge rule: when in doubt about a field value, a visible `unknown` placeholder is always safe; an omitted field is never safe.

### 3.7 [S] #8 — Route "Open Questions" to a durable home AND teach resume-session to read it (paired change)

**Change (two files — this is the point-of-effect pairing).**

**In preserve-session:** add an **Open Questions** field to the `## Session Log` template (Step 2), so all five gathered categories (Step 1) have a destination:
```
**Open Questions (for next session's decision):**
- <question 1>
- <question 2>
```
Also insert the same list into the vault note under `<!-- status-update -->` if a note resolved (it is current-state: these are open *now*).

**In resume-session (`.claude/skills/resume-session/SKILL.md`) — the paired change:** add `Open Questions` to the Step-1 extract list (currently line 26 extracts "decisions, blockers, next steps, files modified" with **no line for open questions**) and add a **`### Open Questions`** section to the Step-2 briefing template, so the reader surfaces them.

**Reasoning to carry.** §2.3 corollary (the RT1 lesson, verbatim): *a value written to a surface its consumer doesn't read is inert; if surfacing it requires editing the reader too, that is a paired change — make it, never protect the reader into inertness.* Writing Open Questions to CLAUDE.md while resume-session's extract list ignores them would *look* fixed and change nothing. The Objective (zero loss) is only satisfied when the item is written **and** read. Edge rule: Open Questions are the one class the grounding says Sean flags for *his own next-session decision* — if forced to pick a single durable home, CLAUDE.md `## Session Log` wins (it always exists and resume-session always reads it), with the vault-note copy as a bonus when a note resolves.

> **Self-application note (§6.7 / intent-engineering §6.5):** resume-session is named in "What NOT to Change" as *read-only* (§5). This fix edits it — the edit is **additive read behavior only** (a new extract line + a new briefing section), which does not violate read-only-ness (it reads *more*, writes nothing). The pairing is called out here so the implementer makes both edits in one change and does not treat the resume-session edit as scope creep.

### 3.8 [S] #7 — Locate-or-create the daily note (no silent no-op)

**Change.** Replace Step 4's guard "if today's daily note exists" with **locate-or-create**:
1. Look for `vault/10_timeline/daily/YYYY-MM-DD.md`.
2. If absent, **create it from the template** at `vault/90_system/templates/tpl-daily.md` (which carries the `<!-- claude-sessions -->` anchor), then write the session line into the anchor.
3. Only if creation itself fails → `SKIPPED — daily note: could not locate or create; session line preserved in CLAUDE.md Session Log`.

**Reasoning to carry.** §2.5 (fail-open intake): "if X exists, write X" silently drops every evening/weekend/out-of-band session — precisely the sessions a hand-off matters most for, because no morning Daily Driver ran to create the note. The distinguishing question — *legitimately-absent vs not-yet-created* — resolves to "always create," because the anchor's absence here is never intentional. Edge rule: create from the template (so the anchor and the Dataview blocks exist for the fleet console), not as a bare file — a bare file with no anchor re-creates finding #9 one level down. Do **not** add a git commit after creating (Rule #8 — Obsidian-Git owns that).

### 3.9 [S] #9 — Define the missing/renamed-anchor adapter

**Change.** Add a rule for every anchor write (`<!-- status-update -->`, `<!-- claude-sessions -->`): **if the anchor is absent** from the target file (a hand-edited note, a note predating the template):
1. **Append** a new section with the anchor and the content, at the end of the file (e.g. `\n## Current Status\n<!-- status-update -->\n<content>` or `\n## Claude Code Sessions\n<!-- claude-sessions -->\n<content>`). Appending a missing anchor is safe; guessing an insertion point in unfamiliar structure is not.
2. Report `WRITTEN & VERIFIED — <dest>: anchor was absent, appended new section` (verified by re-read per §3.1) — the "anchor absent" fact is surfaced, not hidden.

**Reasoning to carry.** §2.5 + §3.1: the current skill writes "nowhere or in the wrong place" and still reports success. The fix makes anchor-absence a **visible, self-healing** event (append + note it), never a silent land-nowhere. Edge rule: for a `status-update` (replace-discipline) anchor that is absent, appending a fresh section is correct — there is no prior state to replace. Never fabricate the whole template structure around a missing anchor; append the one section you need.

### 3.10 [m] #11 — Timestamp gets a timezone/source

**Change.** Step 2's timestamp is emitted as **local time with an explicit offset or tz abbreviation** (e.g. `2026-07-05 14:30 ET`). Source is the machine clock. Brief: resume-session mis-orders across a tz boundary without it.

### 3.11 [m] #12 — `ai-context` is summarized, not truncated

**Change.** The "keep ai-context under 200 characters" rule gains: **summarize to fit, never hard-cut.** If the natural summary exceeds 200 chars, compress the *meaning* to fit; do not slice mid-sentence. Brief: real values run ~380 chars; a mid-sentence cut is worse than a shorter true summary.

### 3.12 [m] #13 — `## Session Log` gets a cap that ARCHIVES, never deletes

**Change.** Add a rotation rule: when `## Session Log` exceeds **N = 10** entries, move the **oldest** entries to a `## Session Log (archive)` section at the bottom of the same file (or a sibling `CLAUDE-session-log-archive.md`), keeping the 10 most recent under `## Session Log`. **Archive, never delete.**

**Reasoning to carry (§6.9 — hold the objective as an invariant).** A cap that *drops* the oldest entry is **data loss inside a zero-loss spec** — locally reasonable (keep the file small), globally a betrayal of the Objective. The objective wins: rotation must relocate, never delete. This is the one minor finding that carries reasoning, because the obvious implementation (drop oldest) directly contradicts the spec's purpose.

---

## 4. Owner-forks — surfaced with a recommendation + contingency (not silently decided)

Per §6.8 / intent-engineering: pre-make what the record decides; **surface** genuine owner-taste calls with a recommendation and its contingency — never a bare menu, never a silent pick. Both named forks are genuine taste calls (the record does not decide them), so both are surfaced.

### Fork A — Missing vault note: report-and-skip vs auto-scaffold vs CLAUDE.md-redirect

**What the record says.** Current skill (line 88): *"report it but don't create one automatically."* That is the standing decision, but it predates the zero-loss framing and the code-brain folder-not-note evidence.

**New tradeoff info the diagnosis surfaced.** Option (iii) — **redirect the structured block into CLAUDE.md** — was not in the original skill. It preserves **zero loss** (the item lands in a destination that always exists and that resume-session always reads) **without** touching the vault at all, so it sidesteps the vault-cleanliness objection to option (ii). Note on Rule #8: auto-scaffolding a note (option ii) would *not itself* violate the "no second auto-commit" rule — Obsidian-Git still does the commit — but it does add un-asked-for files to the vault, which is the cleanliness cost.

**Recommendation:** **(iii) CLAUDE.md-redirect** as the default when no vault note resolves, combined with **(i) report** — i.e. `SKIPPED — vault note: none resolved for <dir>; block preserved in CLAUDE.md Session Log`. This is what §3.4 and §3.8 already implement, because it is the only option that satisfies the Objective's zero-loss priority for the *most common* case (code-brain) without a vault-structure guess.

**Contingency (if Sean prefers vault-cleanliness over CLAUDE.md redirect):** fall back to **(i) pure report-and-skip** — emit `SKIPPED — vault note: none resolved; not captured to vault (Open Questions/next-steps still in CLAUDE.md)`. Do **not** adopt (ii) auto-scaffold unless Sean explicitly asks, because a scaffolded stub for every unmatched directory clutters `vault/20_projects/` and creates notes no human authored. The recommendation is a decision Sean can flip in one line; it is surfaced, not buried.

### Fork B — Flush-hook coexistence: stay two structures vs reconcile into one

**What the record says.** flush is a SessionEnd hook (knowledge-loop producer; root CLAUDE.md line 160) that mines the transcript into `vault/knowledge/` and appends a raw `## Sessions` block to `vault/daily/`. The record does **not** decide "reconcile"; Rule #8 forbids a second auto-commit mechanism.

**Recommendation:** **stay two separate structures.** They serve different purposes on different surfaces: flush = unattended, transcript-mined, knowledge/narrative, targeting `vault/knowledge/` + `vault/daily/## Sessions`; preserve-session = interactive, human-curated, structured hand-off, targeting `<!-- claude-sessions -->` in `vault/10_timeline/daily/` + CLAUDE.md + the vault note. §3.6(c) writes this coexistence into the skill. Reconciling into one writer would either make preserve-session unattended (it is not — `enabled = false`) or make flush structured (it can't curate decisions/blockers from a transcript as well as the interactive session can). Keeping them separate is the lower-risk, record-consistent choice.

**Contingency (if Sean later wants one console line per session, not two records):** the reconciliation is a *separate* piece of work — it must (a) pick one writer as the owner of the `<!-- claude-sessions -->` line, (b) route the other's output through it, and (c) **not** introduce a second auto-commit step (Rule #8). That is out of scope for this fix and would be its own spec; flag it as a deferral, do not attempt it here.

---

## 5. What NOT to change (Preservation Constraints — the thing + WHY)

Per intent-engineering Section 6 (mandatory on a fix spec) and §3.5 (confirmed-correct rows protect working design from the fix):

- **resume-session stays read-only** — *why:* it is the READ half; it must never write to the sources it reads or it corrupts the state it reports. The §3.7 edit is **additive read behavior only** (new extract line + new briefing section); it reads more, writes nothing. Do not add any write to resume-session.
- **"Report it but don't create one automatically" is the *default* for a missing vault note** (Fork A) — *why:* auto-creating vault notes is a vault-structure decision that belongs to Sean, not the skill. The recommended CLAUDE.md-redirect preserves zero loss *without* auto-creating a note, so the "don't auto-create" instinct is honored, not overridden.
- **`## Session Log` and `<!-- claude-sessions -->` stay APPEND-discipline** — *why:* they are logs; replacing them is data loss (#5). This is the half of "PATCH not PUT" that was **right** — preserve it. Do **not** over-generalize the append rule to `<!-- status-update -->`, which is *supposed* to be replaced (that over-generalization is finding #5 itself).
- **The `<!-- anchor -->` PATCH pattern itself** — *why:* anchored, region-scoped writes (vs whole-file PUT) are correct and are what let multiple writers share a file. The fix refines *which discipline per anchor*, not the anchor mechanism.
- **The 200-char `ai-context` cap and the one-line daily Outcome** — *why:* these are consumer-shape contracts (resume-session reads `ai-context`; the Dataview roll-up expects a one-line Outcome). The fix changes truncate→summarize (#12) but keeps the length targets — do not lengthen them.
- **The five-item Step-1 gather list** (decisions, blockers, files modified, next steps, open questions) — *why:* it is the correct capture set; the bug was that Open Questions had no *destination* (#8), not that it was gathered. Keep all five; the fix adds the missing destination + reader.
- **No Zero-Interaction Mandate** — *why:* preserve-session is interactive (`[agents.preserve_session] enabled = false`, no schedule). The mandate's trigger is "runs unattended," not "is a skill." Injecting it here would be wrong — it would tell an interactive skill that has a human present to never ask, which is the opposite of correct.
- **flush.py, `session-end-flush.sh`, and the `## Sessions` block are not touched** — *why:* they are a separate, working, unattended knowledge-extraction path (Fork B). preserve-session states the relationship (§3.6c) but writes none of flush's surfaces. Reconciliation is a deferral, not this fix.

---

## 6. Done looks like (checkable statements)

Each is a grep, a test, or an exact behavior an implementer can run (§6.6):

1. **Transport named:** `grep -n "Edit\|Write" .claude/skills/preserve-session/SKILL.md` shows the built-in write mechanism named in a Write Mechanism subsection; `grep -n "already.*current\|looks current" SKILL.md` shows the **anti-skip rule** forbidding "skip because it looks current."
2. **Confirmation is read-back-gated:** the skill's Step 5 text emits only `WRITTEN & VERIFIED` / `SKIPPED — <reason>` / `FAILED — <reason> + payload`; `grep -n "updated\b" SKILL.md` finds no unqualified "updated/saved" success line that isn't downstream of a re-read.
3. **Dead match key gone:** `grep -n "context.*field in CLAUDE.md\|CLAUDE.md frontmatter" SKILL.md` returns **nothing** (the never-firing key #2 is deleted); the `context:`-on-vault-note match is present instead.
4. **Folder-not-note handled:** the skill names the `prj-code-brain`-style "folder of sub-notes, no single note" case and its CLAUDE.md-redirect fallback; it never instructs creating `prj-<name>.md` for such a folder.
5. **Two anchor disciplines split:** the skill states `<!-- status-update -->` = REPLACE and `<!-- claude-sessions -->` = APPEND, with the current-state-vs-history test. A reviewer can confirm the two anchors carry *different* verbs.
6. **Daily line shape pinned:** the exact `- [time:: …] | [domain:: …] | [context:: …] | **Outcomes:** … Link: [[prj-…]]` format is in the skill, with the "placeholder-not-omit" rule for unknown fields; the daily path reads `vault/10_timeline/daily/`.
7. **Flush relationship stated:** `grep -n "flush\|## Sessions\|Obsidian-Git\|Rule #8\|sole" SKILL.md` shows the coexistence note (different dir, different section, do-not-merge, no second auto-commit).
8. **Open Questions has a destination AND a reader:** `grep -n "Open Questions" .claude/skills/preserve-session/SKILL.md` shows it in the Session Log template; `grep -n "Open Questions" .claude/skills/resume-session/SKILL.md` shows it in **both** resume-session's Step-1 extract list and Step-2 briefing template. (Both greps non-empty = the paired change landed; either empty = inert.)
9. **Locate-or-create daily:** the skill creates the daily note from `tpl-daily.md` when absent, and only SKIPs if creation fails; `grep -n "if today's daily note exists" SKILL.md` returns nothing (the fail-open guard is gone).
10. **Missing-anchor adapter defined:** the skill states the append-new-section behavior for an absent anchor and reports it, rather than landing nowhere.
11. **Cap archives, never deletes:** `grep -n "Session Log" SKILL.md` shows a rotation rule that **relocates** entries beyond N=10 to an archive section; `grep -n "delete\|drop.*oldest\|remove.*oldest" SKILL.md` shows no delete-oldest rule.
12. **Timestamp carries tz; ai-context summarizes:** the skill's timestamp format includes an offset/tz; the ai-context rule says summarize-to-fit not hard-cut.
13. **Live acceptance test (the outcome that matters):** run preserve-session at the end of a real code-brain session; then `grep -c "^### " <that CLAUDE.md's ## Session Log>` shows the new entry present (the zero-landed-files symptom is gone), and Step 5's report shows a `SKIPPED — vault note` line naming the folder-not-note reason (not a false "Vault note updated").

---

## 7. Band-aid tripwires (reject these in review)

- **"Report from a flag we set after writing"** instead of a fresh read-back — this is the original bug reworded. The report MUST derive from re-reading the destination, not from an in-memory "did_write=true".
- **A retry loop** on a failed write — an interactive human is present; a `FAILED — <payload>` line they can act on beats a silent retry that masks the failure. Reject added retry logic.
- **"Skip the write if the anchor looks current"** in any form — the anti-skip rule (§3.2) is explicit; a reviewer should reject any hedge that lets current-looking prior-session content justify not writing.
- **Writing Open Questions to CLAUDE.md but not editing resume-session** — inert by construction (§3.7). Both files change or neither claim is fixed.
- **A `## Session Log` cap that deletes** the oldest entry — data loss in a zero-loss spec (§3.12). Must archive.
- **Auto-scaffolding a vault note by default** for every unmatched directory (§Fork A) — clutters the vault with un-authored stubs; only on Sean's explicit ask.
- **Adding any git commit / auto-commit step** anywhere in the skill — Rule #8: Obsidian-Git is the sole vault auto-commit owner.

---

## 8. Deferrals (explicitly NOT in this fix; what gates them)

- **Reconciling preserve-session and flush into one `<!-- claude-sessions -->` writer** (Fork B) — gated on Sean choosing "one record per session, not two." It is its own spec: pick the line-owner, route the other through it, keep Rule #8. Not attempted here.
- **Fixing flush.py's `vault/daily/` vs `vault/10_timeline/daily/` path discrepancy** — surfaced during grounding (flush writes to a directory that doesn't exist), but flush.py is out of this skill's scope. Flagged for a follow-up ticket; not fixed in this SKILL.md.
- **Auto-creating a canonical `prj-code-brain.md`** for the code-brain multi-note folder — a vault-structure decision for Sean, not a skill behavior. The fix redirects to CLAUDE.md instead; a real canonical note is Sean's call.

---

## VALIDATION VERDICT — Profile: 4-element floor (Objective + Outcome in scope) — hand-run (intent-engineering MCP tools not confirmed mounted this session)

- **Objective Quality:** pass — states the problem (writes with no verified mechanism to targets that don't resolve, reported from intent), why it matters (zero-loss continuity path lies about landing → resume rebuilds from missing/stale data), and a trade-off line that guides unspecified cases (visibly-incomplete-honest > silently-lossy-confident).
- **Outcome Quality:** pass — outcomes are observable states from the owner's chair (per-destination WRITTEN/SKIPPED/FAILED report derived from read-back; `## Session Log` present after run; current-not-stale status; Open Questions survive), measurable without agent self-report (greps + a live acceptance test), and there are 3–6 of them, not 1, not 10.
- **Out of scope (floor):** Health Metric, Constraint (beyond Preservation), Autonomy, Edge-Case group as a standalone section — governed here by the consumer's contract (resume-session's read shape, the Dataview parser) rather than this checklist; recorded as out of scope, not as failures.
- **Preservation Constraints:** present and reasoned (§5) — mandatory on a fix spec, satisfied.
- **Paired-change protocol:** applied — §3.6 (daily line ↔ fleet-console parser) and §3.7 (Open Questions ↔ resume-session reader) both carry the "edit both or file a ticket" rule; the self-application note flags the resume-session edit as additive-read, in-scope.
- **Owner-forks:** both surfaced with recommendation + contingency (§4), neither silently decided nor left a bare menu.
- **Handoff rehearsal (§1.5 / intent-engineering pre-emit):** fresh un-enumerated case — *"preserve-session runs in a brand-new project directory with no CLAUDE.md and no vault note at all."* Would the Objective + trade-off line force the right call for a weaker model? **Yes:** zero-loss-over-tidiness → create the CLAUDE.md `## Session Log` (the always-available destination) via `Write`, capture everything including Open Questions there, report `SKIPPED — vault note: none for a new project` and `WRITTEN & VERIFIED — CLAUDE.md: created Session Log`. No silent loss, no fabricated success, no vault-structure guess. The Objective carried the case the spec didn't enumerate — no edge-case-list patch needed.

## Required output

Emit exactly this format, in this order:

```
VERDICT: A
```
(or `VERDICT: B`, or `VERDICT: TIE`)

Then exactly 3 bullets of reasoning, each tied explicitly to one of the four rubric criteria above.

Then one final line: a note on whether ARTIFACT A, ARTIFACT B, both, or neither contains a self-contradiction (a stated rule that contradicts the artifact's own stated objective).
```

## Council responses

### ~anthropic/claude-sonnet-latest

```
VERDICT: B
```

- **Self-consistency (rubric #2):** Artifact A's own fix for finding #13 states "cap the `## Session Log` at the most recent 10 entries; when appending an 11th, drop the oldest" — this is a cap-and-delete rule embedded inside a spec whose Objective is explicitly "zero loss," a direct self-contradiction of the kind the rubric names. Artifact B addresses the identical finding by mandating archive-not-delete rotation and explicitly calls out why "drop oldest" would betray the stated objective — B avoids the contradiction A commits.

- **Task-specific catch (rubric #4, both sub-items):** B explicitly diagnoses and fixes the "written but never read" failure mode for Open Questions — it traces resume-session's actual Step-1 extract list (citing line numbers) and finds Open Questions absent from it, then makes a paired edit to resume-session's read logic, naming this "the RT1 lesson: a value written to a surface its consumer doesn't read is inert." A only adds Open Questions to CLAUDE.md/vault-note write templates and explicitly declares resume-session "read-only and unchanged," never verifying that the reader actually consumes the new field — reproducing the exact contradiction the rubric flags rather than catching it.

- **Breadth/evidence-discipline (rubric #3):** B performed deeper live-system verification, citing flush.py's actual code paths (e.g., `format_daily_log_body` line 172, file-creation logic lines 210–212) and discovered that flush.py resolves to `vault/daily/` — a directory that doesn't exist — while preserve-session targets `vault/10_timeline/daily/`, a real seam the brief didn't name. A describes the flush relationship less precisely, missing this path mismatch, indicating shallower verification of the actual tool despite reaching a similar high-level resolution (keep the structures separate).

**Self-contradiction check:** Artifact A contains a stated rule (cap-and-delete on `## Session Log`) that contradicts its own stated zero-loss objective. Artifact B does not exhibit an equivalent contradiction — it identifies and explicitly resolves the same tension via archive-not-delete.

### openai/gpt-5.4-mini

VERDICT: B

- **Decidedness / self-consistency:** B is more actionably decided. It names a concrete write mechanism ladder, fixed report vocabulary, explicit replace-vs-append rules, and a precise daily-line schema. A is also decided, but it contains more internal tension, especially around proposing a 10-entry cap that drops the oldest entry inside a zero-loss spec.

- **Breadth / evidence-discipline:** B shows stronger live-system grounding: it reports actual checks on file paths, the absence of frontmatter in CLAUDE.md, the real `vault/10_timeline/daily/` path, and the flush hook’s actual behavior. A also claims repo confirmation, but B is more explicit about what was checked and where the seam boundaries are.

- **Task-specific:** Both catch the two target contradictions, but B handles them more cleanly. It identifies the unused Open Questions destination and fixes it by pairing writer and reader, and it explicitly rejects a destructive cap by changing it to archive-never-delete. A catches both issues too, but its own cap rule is self-contradictory against the zero-loss objective.

Both contain self-contradictions, but **ARTIFACT A** contains the clearer one.

### deepseek/deepseek-v4-pro

VERDICT: B

- **Decidedness:** Both artifacts supply concrete decisions, field names, error shapes, and edge‑case guidance, but B achieves the same level of actionable specificity without the extra framing and validation sections that length would otherwise reward; its anti‑skip rule, fixed report vocabulary, and explicit anchor‑repair procedure are equally implementable.
- **Self‑consistency:** B explicitly rejects a cap that deletes oldest session‑log entries (it archives instead) and flags such deletion as data loss incompatible with the zero‑loss objective. A’s “cap at 10, drop oldest” rule, while rationalized as a nicety, injects a data‑discard that risks contradicting the stated goal of zero‑loss hand‑off, making B more internally coherent.
- **Task‑specific:** Both artifacts catch the “Open Questions written but never read” contradiction and the silent‑loss potential in the ai‑context truncation. B additionally identifies the cap‑that‑drops‑data as a self‑contradiction and resolves it with archiving, while A’s deletion‑based cap fails to fully eliminate the data‑loss pattern the criterion expects the artifact to detect and fix.

Artifact A contains a self‑contradiction: its rule to drop the oldest `## Session Log` entries after collecting them is a form of data loss inside a spec whose core objective is zero loss of session‑state information. Artifact B avoids this by archiving and explicitly treats a delete‑based cap as a self‑contradiction to reject.

### mistralai/mistral-medium-3-5

VERDICT: A

- **Decidedness**: Artifact A pre-makes decisions on critical edge cases (e.g., missing vault note handling via CLAUDE.md redirect, explicit replace/append disciplines per anchor) with clear, actionable rules (e.g., "redirect-to-CLAUDE.md fallback" in E1, "read-back verification" in Objective 1). Artifact B’s edge-case handling is thorough but leans more on recommendations + contingencies (e.g., Fork A’s CLAUDE.md-redirect *recommendation*), which leaves slightly more room for interpretive ambiguity.
- **Self-consistency**: Artifact A explicitly calls out and resolves the two self-contradictions in the source material: (i) the "Open Questions" section is routed to durable destinations (CLAUDE.md + vault note), and (ii) the silent-drop risk (via caps or unverified writes) is eliminated through read-back verification and explicit "landed/skipped/failed" reporting. Artifact B also addresses these but frames them as part of broader reasoning rather than direct resolutions.
- **Breadth / evidence-discipline**: Artifact A demonstrates deeper system verification (e.g., confirming `## Session Log` in 0 files, the `prj-code-brain` folder structure, flush-hook coexistence via direct repo inspection) and ties these findings to specific, auditable changes (e.g.,_tabular done-criteria in §7). Artifact B’s live-system checks are similarly rigorous but less tightly coupled to enforceable done-criteria.

Neither artifact contains a self-contradiction.

## Cross-rankings

### Judge: ~anthropic/claude-sonnet-latest

- **Order:** B > A > C
- **Reasoning:** Response B most precisely nails the rubric's named self-contradiction test: Artifact A's finding #13 explicitly instructs 'drop the oldest' entry inside a zero-loss spec (a textbook cap-that-drops-data violation), while Artifact B explicitly rejects that exact pattern and archives instead — Response B states this cleanly and unambiguously. Response A reaches the same correct verdict and cites the same cap issue, but its closing line ('Both contain self-contradictions, but ARTIFACT A contains the clearer one') is muddled and undercuts its own clarity by implying B also has an unspecified contradiction without naming one. Response C is the weakest: it asserts 'Neither artifact contains a self-contradiction,' which is factually wrong given Artifact A's explicit drop-oldest cap directly contradicting its own zero-loss objective — a miss on the exact criterion (4-ii) the rubric calls out, undermining its overall credibility despite otherwise reasonable observations about A's decidedness.

### Judge: openai/gpt-5.4-mini

- **Order:** B > A > C
- **Reasoning:** B is strongest because it is the most self-consistent and task-specific: it explicitly rejects data-dropping caps, directly fixes the “Open Questions” write/read mismatch by editing resume-session too, and backs claims with concrete live-system checks. A is also detailed and decided, but it contains a direct self-contradiction by capping Session Log at 10 and dropping the oldest entries, which conflicts with the zero-loss objective, even though it handles many other seams well. C is weakest because it is less accurate about the comparison points and understates A’s contradiction, while also being less grounded in the actual system behavior than B.

### Judge: deepseek/deepseek-v4-pro

- **Order:** B > A > C
- **Reasoning:** Artifact B is the strongest because it maintains self-consistency by rejecting a destructive cap in favor of archive-never-delete, performs a more precise paired change to fix the 'Open Questions writes but never read' contradiction, and demonstrates richer live-system verification (e.g., flush.py's actual path discrepancy). Artifact A is next—it is highly decided with clear rules, but it commits a self-contradiction by proposing a 10-entry cap that drops the oldest entry inside a zero-loss objective. Artifact C ranks last because it incorrectly claims Artifact A contains no self-contradiction and its reasoning overstates A's direct resolution of source-material contradictions without noting A's internal flaw.

### Judge: mistralai/mistral-medium-3-5

- **Order:** B > A
- **Reasoning:** Response B is best because it correctly identifies Artifact B as superior on all key rubric criteria (self-consistency, task-specific catches, and evidence discipline) while noting A's self-contradictory cap-and-delete rule. Response A is second because it provides thorough analysis but frames the reasoning around contradiction detection rather than the broader quality of the artifacts. Both B and A highlight Artifact A's fatal flaw (cap-and-delete contradicting zero-loss), but B's reasoning is more precise and actionable.

## Chairman synthesis

_Chairman model: `~anthropic/claude-sonnet-latest`_

# Council Synthesis: Artifact A vs. Artifact B

## Convergence (high confidence, unanimous across models)

All four council members agree on the underlying architecture of the comparison, independent of their final verdict:

- **Both artifacts are genuinely decided** — field names, error-shape vocabularies, and edge-case defaults are pre-made, not left as menus. No judge flagged either artifact for hedging.
- **Both catch the brief's two named self-contradictions in principle** — the "Open Questions gathered but never read" gap (finding #8) and the "cap that silently drops data in a zero-loss spec" pattern (finding #13) are addressed by name in both artifacts.
- **Both verify against the real repo rather than reasoning from text alone** — grep results, real file paths, real note structures (`prj-code-brain` as a folder-of-notes, CLAUDE.md's lack of frontmatter) appear in both.
- **Both resolve the two owner-forks identically in substance** — missing vault note → redirect to CLAUDE.md as the default; flush-hook coexistence → keep separate structures, owned surfaces, no reconciliation. Neither artifact ducks these as a bare menu.

Given this baseline parity, the deciding weight falls on execution quality within two specific rubric items — and this is where the council's votes concentrate.

## Divergence and how it resolves

**~anthropic/claude-sonnet-latest, openai/gpt-5.4-mini, and deepseek/deepseek-v4-pro** converged on **B**, all citing the same two discriminating facts:

1. **Artifact A's own finding #13 fix** — "cap the `## Session Log` at the most recent 10 entries; when appending an 11th, **drop the oldest**" — is a textbook instance of the exact pattern the rubric names parenthetically ("a cap-and-delete inside a zero-loss spec"). A frames this as "a nicety, not a gate," but framing doesn't neutralize the contradiction: the Objective explicitly states zero loss is what makes silent confidence "the exact failure a preservation tool is supposed to prevent," and A's own rotation rule silently discards data past entry 10. Artifact B handles the identical finding by mandating **archive-never-delete**, and — notably — B is the only artifact that explicitly *names* the tension ("the obvious implementation (drop oldest) directly contradicts the spec's purpose") before resolving it, which is stronger self-consistency discipline than A shows anywhere.

2. **The Open Questions pairing.** Artifact B (openai/gpt-5.4-mini, deepseek/deepseek-v4-pro, and Sonnet all flag this) traces resume-session's *actual* Step-1 extract list (citing its concrete line reference) and finds Open Questions genuinely absent from what the reader consumes — then makes the paired edit to resume-session's read behavior. Artifact A adds Open Questions to CLAUDE.md and the vault note's write templates, but its own §6 explicitly declares resume-session "read-only and unchanged... it is already the shape resume expects" — an *asserted*, not *verified*, claim. That gap means A's fix for finding #8 risks reproducing the very failure mode the rubric is testing for (a value written to a surface nothing downstream reads), whereas B closes the loop on both ends.

**mistralai/mistral-medium-3-5** dissented for **A**, arguing A's edge-case resolutions (E1/E5) are more crisply pre-decided and that "neither artifact contains a self-contradiction." This dissent is the outlier, and it rests on a factual claim the other three judges directly contradict: A's finding-#13 cap-and-drop rule is a stated rule that contradicts A's own stated zero-loss objective — precisely the pattern the rubric calls out by name. Mistral's read undercounts this, and its praise for A's "firmer defaults" doesn't survive contact with the fact that B's owner-fork resolutions (Fork A, Fork B) are equally concrete recommendation-plus-contingency structures, just with additionally more granular live-system evidence behind them (e.g., B's discovery that `flush.py` actually resolves `vault_daily_dir` to a nonexistent `vault/daily/` directory — a seam neither the brief nor Artifact A surfaced with that precision).

## Direct answer

```
VERDICT: B
```

- **Self-consistency (criterion 2):** Artifact A's finding-#13 fix ("cap at 10 entries, drop the oldest") is a stated rule that contradicts A's own zero-loss objective — the exact contradiction pattern the rubric names as exemplary. Artifact B resolves the identical finding with archive-never-delete and explicitly reasons that "drop oldest" would betray its stated purpose, making B internally coherent where A is not.
- **Task-specific catch (criterion 4, part i):** Artifact B verifies resume-session's actual extract list, finds Open Questions absent from what downstream code reads, and makes the paired write-and-read fix. Artifact A writes Open Questions to new surfaces but declares resume-session "read-only and unchanged" without verifying it consumes the new field — leaving open the possibility that A's fix is itself an instance of "written but never read downstream," the very failure the rubric asks the artifact to catch.
- **Breadth / evidence-discipline (criterion 3):** Artifact B traces `flush.py`'s live behavior to specific code lines and surfaces a real, previously unnamed seam — `flush.py` resolves its daily-note target to `vault/daily/` (which does not exist) rather than the real `vault/10_timeline/daily/` preserve-session uses — a discrepancy Artifact A's otherwise-solid flush-hook account does not surface with comparable precision.

**Self-contradiction check:** ARTIFACT A contains a self-contradiction — its finding-#13 rule to drop the oldest `## Session Log` entries after 10 is data loss inside a spec whose stated objective is zero loss. ARTIFACT B does not; it identifies this exact tension in its own reasoning and resolves it via archive-never-delete rather than deletion.
