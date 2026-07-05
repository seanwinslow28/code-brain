# WWF5D Eye-Check — skill-audit(`preserve-session`), Opus with vs. without

- **Date:** 2026-07-05
- **Step:** Campaign Step 1 (the cheap gut-check before spending Fable on Round 2).
- **Question:** Does loading WWF5D visibly lift Opus on a real audit — does the with-WWF5D arm show the premium moves (verify-the-world, breadth past named seams, existence-check "enforced via X", spec-decidedness) the without arm lacks?
- **This is a gut-check, not the formal validation.** N=1 per arm, in-domain, no council. Step 4 is the real thing.

## Setup (single-variable design)

- **Harness:** `skill-audit` (inlined into both prompts, identical). Chosen over `zoom-out-and-think` deliberately: the run's own finding is the plain zoom-out/diagnosis loop is *cheap-on-Opus* (matched in BT2 + BT5), so a zoom-out eye-check would structurally under-show WWF5D's lift. `skill-audit` hits the premium head-on (BT1 is where the premium was starkest).
- **Target:** `.claude/skills/preserve-session/SKILL.md`, audited with `.claude/skills/resume-session/SKILL.md` named as its consumer (a real write→read handoff pair).
- **Two Opus subagents**, identical prompt + identical pinned grounding + identical repo access. **The only variable:** one had the full WWF5D SKILL.md pasted in as standing context; the other did not.
- Grounding (a)–(d) pinned identically (see Appendix C).

## ⚠️ Methodological caveat (disclosed up front)

My pinned grounding answer (b) **named the three destinations, the exact anchors, and "SessionStart inject hooks and SessionEnd flush hooks operating in the same area."** That handed *both* arms a map pointing at the world to verify. Consequently **both arms verified the world heavily** — so the *verify-the-world axis did not cleanly separate the arms* in this run.

This confound **levels** the arms (it makes a WWF5D lift *harder* to see, not easier). The fact that a sharp delta still emerged is therefore a **conservative** read — a cleaner grounding that didn't pre-name the targets would likely widen the gap. Worth fixing if we want a crisper signal, but it doesn't threaten the direction of the result.

## Verdict: WWF5D visibly helped — concentrated in the *sharper* premium moves

Both audits are genuinely strong (Opus 4.8 is a strong auditor, and the confound above lifted the baseline). The separation showed up exactly where the campaign says Fable's premium lives — **contract-contradiction, point-of-effect tracing, and spec-decidedness** — not in generic "did it read files."

### The single cleanest, eyeball-able signal

- **Baseline (no WWF5D)** put "keep the `PATCH not PUT` / append-only anchor discipline" in its **What NOT to change** — it *protected* the blanket anchor rule.
- **WWF5D arm** caught that the two anchors have **opposite** write disciplines: `<!-- status-update -->` is *current-state* → must be **replaced** (resume-session reads it for "where you left off"; appending stacks stale status so resume shows last week as current), while `<!-- claude-sessions -->` is a *log* → must be **appended** (replacing wipes the day's earlier lines = data loss). The blanket "PATCH not PUT" is right for one and **wrong** for the other.

So the baseline would hand a weaker implementer a spec that *protects a half-wrong instruction*; the WWF5D spec catches the contradiction and splits the disciplines with a distinguishing test ("if the region holds current-state it's replaced; if it holds a log it's appended"). That is a legible, decision-relevant safety delta — the kind of thing this eye-check was looking for.

### Premium-move comparison

| Move (run's yardstick) | Baseline (no WWF5D) | WWF5D arm |
|---|---|---|
| **Verify-the-world** | Strong — *but confounded* (grounding named the targets; both arms verified) | Strong — same |
| **Existence-check "enforced via X"** | Caught it: Step 5 "Confirm" reports from **intent**, not a verified read-back (its keystone DW) | Caught it + went deeper: **no write transport is named** → the silent no-op lives there; proof = `## Session Log` appears in **zero** real CLAUDE.md files (the pair has apparently never successfully written its primary artifact) |
| **Contract-contradiction / point-of-effect** | **Missed** — treated anchor discipline as uniform; *protected* "PATCH not PUT" | **Caught** the opposite-disciplines contradiction (stale-status vs. data-loss) |
| **Breadth past named seams** | Solid (flush-hook `## Sessions` collision; today's daily note absent) | Solid + extra: `claude-sessions` is **Dataview-parsed by `daily_driver.py`** (line format = a contract, drift → invisible to the fleet console); Session Log unbounded growth |
| **Spec-decidedness (§6)** | Strong reasoning-to-carry + scaffold/redirect fallbacks — but leaves the write **mechanism** unnamed | More decided: names the transport + fallback ladder (`patch_content`/`append_content` → Edit → SKIP), splits per-anchor discipline with a test, pins the Dataview line shape with a `[domain:: unknown]` placeholder-not-omit edge rule |

**Both** independently found: the Open-Questions dropped-input seam, the code-brain vault-match failure, the reports-from-intent gap, the daily-note create-or-locate need, and the non-existent `context:`-in-CLAUDE.md match field. Convergence on those = they're the cheap-on-Opus headline; the WWF5D premium is in the tail + the mechanics, consistent with BT3.

### Gate

**Visibly helps → proceed to Step 2 (scope Round 2).** Not a placebo. Sean's eye is the call.

---

## Appendix A — Baseline audit (Opus, NO WWF5D), verbatim

> (agent aaed0ba0e553817d5; 11 tool uses; ~165s)

### Artifact 1 — Seam Report

**Seam Scan**
- `[structural]` — **Step 1 → Steps 2/3/4 · "Open questions" is gathered but has no destination.** Step 1 extracts five categories; only four map to any template in Steps 2–4. "Open questions" is collected then referenced by nothing → the most hand-off-critical class (what a future session must ask before proceeding) is silently discarded; `resume-session`'s "Suggested First Action" is built without it.
- `[structural]` — **Step 1 → Step 4 · "files modified" and "decisions" never reach the daily note.** Step 4's line carries only time/domain/context/Outcomes/link. Opening today's daily note directly (a stated read path) shows a one-line outcome with no trace of what changed/was decided.
- `[dangerously-wrong]` — **Step 3 → Step 5 · vault-match failure silently absorbed as a "skip."** In code-brain, `prj-code-brain/` has no `prj-code-brain.md` and `code-brain/CLAUDE.md` has no frontmatter/`context` → both match strategies fail → the vault half is a permanent no-op for the primary repo, while Step 5 prints "skipped."

**Adapter Scan**
- `[dangerously-wrong]` — **Step 3 · CLAUDE.md-`context`-frontmatter match targets a field that doesn't exist.** Real `context:` lives on the vault project note; CLAUDE.md carries no frontmatter → fallback match can never succeed → collapses to directory-name-only.
- `[dangerously-wrong]` — **Step 4 · daily-note anchor collides with the SessionEnd flush hook's `## Sessions` block; no reconciliation.** `flush.py` plain-appends `## Sessions`, NOT into `<!-- claude-sessions -->` → same day's activity split across two structures, neither cross-references.
- `[structural]` — **Step 4 · no create-or-locate adapter; guard silently no-ops.** Daily note only exists once the Daily Driver creates it (08:45); latest is 2026-06-10 → out-of-band sessions skip silently.
- `[structural]` — **Steps 2/3/4 · PATCH-into-anchor described but no adapter for a missing/renamed anchor.**

**Wow-Gap Scan**
- `[dangerously-wrong]` — **Step 5 · "Confirm" reports from intent, not verified writes — the core wow-gap.** No read-back that the anchor existed / bytes landed. Missing move: re-read each destination, assert the marker is present, report `landed (verified)` / `skipped:<reason>` / `FAILED:<reason>` per destination.
- `[structural]` — **Step 3/Constraint · silent non-creation of a missing vault note is a dead-end.** Missing move: scaffold a minimal note, or redirect the structured block into CLAUDE.md — and say which fired.
- `[minor]` — Step 2 timestamp/timezone unspecified.
- `[minor]` — "ai-context under 200 chars" has no summarize-don't-truncate rule (real value is ~380).

### Artifact 2 — Intent-Carrying Improvement Spec
**Objective:** preserve is the WRITE half of a zero-loss handoff; today it fails (c) in two ways — vault/daily writes frequently do nothing (worst in code-brain), and it always reports "saved" from intent. **Desired outcome:** each destination reports `landed (verified)`/`skipped:<reason>`/`FAILED`; nothing silently dropped. **Fixes:** (1) Step 5 verify not narrate (keystone); (2) robust vault match + scaffold/redirect fallback; (3) daily create-or-locate + coexist with flush; (4) route every Step-1 input (add Open Questions to the Session Log); (5) minors. **What NOT to change:** append-only/PATCH-into-anchor discipline; resume-session's read-only contract; the five Step-1 categories; do not stand up a second daily auto-commit or reconcile the flush block (Rule #8).

---

## Appendix B — WWF5D-loaded audit (Opus, WITH WWF5D), verbatim

> (agent a4c7fdfaf0576d04f; 12 tool uses; ~193s)

### Artifact 1 — Seam Report
- `[dangerously-wrong]` — **Step 5 · confirmation derived from intent, never a read-back.** A silent no-op and a real write print identical confirmations → disappointment (c) verbatim.
- `[dangerously-wrong]` — **Steps 2/3/4 · no write transport named, so the mechanism is improvised and can silently no-op.** Proof: `## Session Log` exists in **zero** real CLAUDE.md files across the whole tree — this pair has apparently never successfully written its primary artifact.
- `[dangerously-wrong]` — **Step 3 · match key #2 ("`context` field in CLAUDE.md frontmatter") targets a field that doesn't exist.** Degrades to directory-name-only.
- `[dangerously-wrong]` — **Step 3 · directory-name matching has no defined target for the owner's most-used repo.** `prj-code-brain/` is a folder of many sub-notes with no single `prj-code-brain.md` → silent skip, or an improviser writes the summary into the wrong project's note.
- `[structural]` — **Step 3 vs Step 4 · "PATCH not PUT" is stated once but the two vault anchors have opposite write disciplines.** `status-update` = replace-the-block (region-PUT); `claude-sessions` = append-a-line. One rule everywhere → either stale status stacked (resume shows last week as current) or the day's earlier lines wiped (data loss).
- `[structural]` — **Step 4 · `claude-sessions` is a multi-owner, Dataview-parsed surface** (`daily_driver.py` reads it) with an exact inline-field line format; the skill treats it as private free-text → any drift makes the session invisible to the console, indistinguishable from a dropped one.
- `[structural]` — **Step 1 → later · "Files Modified" and "Open Questions" only partially routed.** Open Questions is written to no durable destination → resume never resurfaces it.
- `[structural]` — **whole skill · no defined relationship to the SessionEnd flush hook** operating in the same territory; a future decision to hook preserve to SessionEnd would collide with flush.
- `[minor]` — Step 2 · `## Session Log` has no cap/rotation; grows unbounded in the first-read file.

### Artifact 2 — Intent-Carrying Improvement Spec
**Objective:** root cause is one shape — the skill promises writes it has no verified mechanism for, to targets that don't reliably resolve, then confirms success from intent. Repo confirms it (`## Session Log` in no CLAUDE.md; `context:` match field absent; code-brain has no single project note). **Desired outcome:** per-destination "written and verified" or "SKIPPED — <reason>", never a silent/mislabeled "saved". **Fixes:** (1) confirm from read-back; (2) name the write transport (mcp-obsidian `patch_content`/`append_content` → Edit fallback → else SKIP), insertion point pre-decided; (3) fix match keys to real fields + define the miss path (don't guess a sub-note); (4) handle the directory-is-a-folder case (code-brain) explicitly; (5) split the two anchor write-disciplines with a distinguishing test; (6) mark `claude-sessions` a shared, format-load-bearing surface + pin the line shape (`[domain:: unknown]` placeholder rather than omit); (7) route Open Questions to a durable home; (8) state the relationship to the flush hook; (9) minor: cap/rotate Session Log. **What NOT to change:** resume-session read-only; "report but don't auto-create a missing note"; "append-only" for the CLAUDE.md log (but NOT over-generalized to `status-update`, which is *supposed* to be replaced); the anchor PATCH pattern itself; the 200-char ai-context cap + one-line daily Outcome; the five-item gather list.

---

## Appendix C — Pinned grounding (identical in both arms)

- **(a) For** — Sean runs it himself at end of a work session, most often in code-brain but any project with a CLAUDE.md. WRITE half of a pair (resume-session is READ). Not hook-wired (interactive today); its reason to exist is zero-loss handoff to a future session (maybe a cheaper model).
- **(b) Feeds** — Consumer: resume-session. Also a human reading CLAUDE.md. Three destinations: (1) project CLAUDE.md `## Session Log`; (2) vault project note under `vault/20_projects/` (`ai-context`, `<!-- status-update -->`, decisions table, blockers); (3) today's daily note `<!-- claude-sessions -->`. *[This clause named the verify-the-world targets — see the caveat.]*
- **(c) Disappoints** — resume next session misses things Sean knows he captured; he can't tell whether vault/daily writes landed or silently did nothing. Reports "saved" but the handoff is lossy.
- **(d) Wow** — a future session / resume reconstructs exactly where he was with zero loss, in the shape the reader reads; confirmation makes it obvious per destination whether each write landed or was skipped-with-a-reason.
