# Roadmap `sw-portfolio` → `sw-ai-pm-portfolio` Rename — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update every reference to the old portfolio repo (`sw-portfolio`) in the unified job-hunt roadmap to point at the new portfolio repo (`sw-ai-pm-portfolio`) — without mangling the unrelated `sw-portfolio-animation-pipeline` repo name on line 155.

**Architecture:** One mechanical text substitution against a single file. The naive `sw-portfolio` → `sw-ai-pm-portfolio` global replace collides with `sw-portfolio-animation-pipeline` (line 155 — a separate planned private repo for the June 11 animation short). Solution: a Python one-liner using a negative lookahead `sw-portfolio(?!-animation-pipeline)` so the animation-pipeline repo is left untouched. Verify before, verify after.

**Tech Stack:** Python regex (stdlib only), grep, the roadmap markdown file.

**Scope notes:**
- New website repo is `github.com/seanwinslow28/sw-ai-pm-portfolio`. Local path: `~/Code-Brain/sw-ai-pm-portfolio/` (confirmed via `git remote -v` on 2026-05-19).
- The new repo currently has **no** `src/` directory (still in design/spec phase). The roadmap's `~/Code-Brain/sw-portfolio/src/content/transactions/foo.md` style paths assume an Astro structure. We're not adjusting those paths in this plan — Sean said the website "isn't linked to either yet, so there's no issue there." If the new build picks a non-Astro stack, those paths get reconciled when the build starts, not now.
- The `sw-portfolio-animation-pipeline` line-155 repo is intentionally **out of scope**. It's a distinct planned private repo for the 2D animation short shipping June 11. Sean can rename that separately if he wants; not part of this plan.

**File touched:** `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md` (only)

---

### Task 1: Snapshot the current state

**Files:**
- Read: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`

- [ ] **Step 1: Confirm working tree is clean for the roadmap file**

Run:
```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git status vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
```
Expected: file appears unmodified relative to last commit (no `modified:` line for this path), OR if dirty, snapshot the diff first via `git diff <path> > /tmp/roadmap-pre-rename.diff` so it can be re-applied after the rename.

- [ ] **Step 2: Capture pre-rename hit count and line numbers**

Run:
```bash
grep -nc "sw-portfolio" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
grep -n "sw-portfolio" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md | wc -l
```
Expected: both report **35** (35 lines, 36 occurrences — one line contains the string twice).

- [ ] **Step 3: Confirm the animation-pipeline guard line exists at the expected location**

Run:
```bash
grep -n "sw-portfolio-animation-pipeline" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
```
Expected: exactly one line — `155:| 5 | 2D animation pipeline (\`sw-portfolio-animation-pipeline\`) | ...`

This is the **only** line that should survive the rename unchanged. If grep returns 0 or >1 results, stop and re-scope before continuing.

---

### Task 2: Run the guarded rename

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`

- [ ] **Step 1: Execute the regex substitution**

Run (single Python one-liner — stdlib only, no venv needed):
```bash
python3 -c '
import re, pathlib
p = pathlib.Path("/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md")
src = p.read_text()
new, n = re.subn(r"sw-portfolio(?!-animation-pipeline)", "sw-ai-pm-portfolio", src)
p.write_text(new)
print(f"replacements={n}")
'
```
Expected stdout: `replacements=36`

The negative lookahead `(?!-animation-pipeline)` is what keeps line 155 untouched. Every other occurrence — bare `sw-portfolio`, `sw-portfolio/`, `sw-portfolio/src/...`, `seanwinslow28/sw-portfolio`, `sw-portfolio.git` — gets renamed.

---

### Task 3: Verify the rename landed correctly

**Files:**
- Read-only: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`

- [ ] **Step 1: Confirm only the animation-pipeline reference remains**

Run:
```bash
grep -n "sw-portfolio" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
```
Expected: exactly **one** line returned — line 155, the `sw-portfolio-animation-pipeline` reference, unchanged.

If anything else surfaces, the regex missed a case. Stop and diagnose before continuing — common culprits would be unicode look-alikes (en-dash instead of hyphen) or a stray instance in a code fence.

- [ ] **Step 2: Spot-check the new path style by sampling three high-leverage lines**

Run:
```bash
sed -n '203p;245p;1275p' /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
```
Expected: all three lines contain `sw-ai-pm-portfolio` in place of `sw-portfolio` (line 203 includes a GitHub URL → should now show `seanwinslow28/sw-ai-pm-portfolio`; line 245 is the schema-modify path → should now show `~/Code-Brain/sw-ai-pm-portfolio/src/content/config.ts`; line 1275 is the pinned-repos list → should now show `(5) sw-ai-pm-portfolio`).

- [ ] **Step 3: Confirm hit count of new name matches expected**

Run:
```bash
grep -c "sw-ai-pm-portfolio" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
```
Expected: **36**.

- [ ] **Step 4: Diff review — eyeball the changes for sanity**

Run:
```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git diff --stat vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
git diff vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md | head -120
```
Expected: stat shows roughly `35 +- / 35 +-` (or similar — one line per substituted line). The diff head should show old `sw-portfolio` lines marked `-` and new `sw-ai-pm-portfolio` lines marked `+`. No structural changes (no line reorderings, no whitespace changes, no encoding shifts).

---

### Task 4: Commit (only if Sean says ship it)

**Files:**
- Commit: the roadmap file.

- [ ] **Step 1: Pause and ask Sean to confirm**

This repo runs an auto-commit hook on the vault — but the unified roadmap lives inside that vault, so the change is likely to get auto-committed within a few minutes regardless. Either way, do **not** explicitly `git commit` from this session unless Sean asks. If he does:

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git add vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
git commit -m "$(cat <<'EOF'
roadmap: rename sw-portfolio → sw-ai-pm-portfolio (36 refs)

New portfolio build (attempt 3) at github.com/seanwinslow28/sw-ai-pm-portfolio.
sw-portfolio-animation-pipeline reference on line 155 deliberately preserved
(separate planned private repo for the June 11 animation short).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Self-Review Checklist

**1. Spec coverage:** The user asked for every `sw-portfolio` reference in the unified roadmap to be replaced with `sw-ai-pm-portfolio`. Task 2 does the replace; Task 3 verifies all 36 occurrences landed. The only retained `sw-portfolio` reference (line 155, `sw-portfolio-animation-pipeline`) is intentional and documented in scope notes.

**2. Placeholder scan:** No TBDs, no "fill in later," no "similar to" references. Every step has the exact command and expected output.

**3. Type consistency:** No types or method signatures involved — this is text substitution on a markdown file.

**4. Risks & rollback:** If anything goes wrong, rollback is `git checkout -- vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md`. The auto-commit hook is the only concern — if it fires between Task 2 and the Task 3 verify, the rollback target is the previous auto-commit (`git log --oneline -5 -- <path>` → `git checkout <sha>~1 -- <path>`).

**5. Out-of-scope side effects:** The Astro-shaped paths (`src/content/transactions/foo.md`, `src/pages/essays/[slug].astro`, etc.) get their *repo name* updated but their *internal structure* stays Astro-style. If the new build picks a different framework, those paths will need a second pass — but Sean explicitly said that's a problem for build time, not now.

---

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-19-roadmap-sw-portfolio-rename.md`. Two execution options:

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints.

Given this is one Python one-liner with three verification greps, **inline execution is probably overkill on the ceremony**. The fastest path is: I just run Tasks 1-3 right now in this session, show you the diff, and you tell me whether to commit. Want me to proceed inline?
