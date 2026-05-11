# The Block Resume-Info Audit + Markdown Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit `vault/30_domains/product-management/the-block-resume-info/` for resume-grade material, convert the high-value `.docx` / `.pdf` artifacts to markdown so Claude Code agents can read them without `pandoc` overhead, frontmatter every `.md` so the nightly vault-indexer picks them up, flag CIIA §2.3-sensitive content, and produce a concrete "what to add to the resume" recommendation list cross-referenced against [`vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md`](../../vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md).

**Architecture:** The folder is a 578-file, 5-subdirectory archive (`SeanxEd-Q2-OKRs-Roadmap-2026/`, `The Block - PRD/`, `The Block - Bi-Weekly Update/`, `The Block-x402-Research/`, `The Block Job Description Breakdowns - ChatGPT/`, plus 4 top-level files). The audit follows a single producer pipeline: (1) inventory → (2) convert blob formats to markdown using local CLI tools (no pandoc dependency) → (3) frontmatter every `.md` for the indexer → (4) CIIA scrub-flag pass → (5) targeted deep-read audit of resume-relevant artifacts → (6) emit three deliverables (inventory CSV, CIIA scrub list, resume strengthening recommendations). The recommendations doc is the human payoff: each row says "current resume bullet X → strengthen with metric Y from artifact Z" or "new bullet candidate from artifact Z."

**Tech Stack:** macOS native `textutil` for `.docx → .html → .md`, `pdftotext` (poppler, already installed) for `.pdf → .txt`, Python 3 for frontmatter injection, `grep`/`rg` for CIIA pattern matching, hand-read for the audit pass. No new dependencies installed unless pandoc fidelity proves required (deferred decision in Task 2).

**Plan parent:** This implements the deferred follow-up flagged in [`vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md`](../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md) Task 2.2 ("Recommended follow-up — deep audit + markdown conversion (~90 min, not yet scheduled)").

**Source-of-truth files (re-read these at the start of each task to avoid drift):**

| Topic | Authoritative source |
|---|---|
| Current resume (master) | `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md` |
| Three tailored variants | `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume_AI_PM.md`, `_Tech_PM.md`, `_Creative_PM.md` |
| Sean's own bullet seed | `vault/30_domains/product-management/the-block-resume-info/the-block-resume-additions-2026.md` |
| The Block JD (for coverage check) | `vault/30_domains/product-management/the-block-resume-info/The-Block-Job-Description.md` |
| CIIA contract text (Section 2.3 + 5) | `vault/50_sources/finance/The Block Day 1 Information/The_Block_Offer_Letter.pdf` (pages 4–13) |
| Vault frontmatter convention | `vault/00_inbox/research-queue.md` (working example) |

---

## File Structure

Files to be created (all paths relative to repo root):

| File | Purpose |
|---|---|
| `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md` | Complete file inventory — one row per non-node, non-junk file: path, size, type, one-line description, proposed downstream artifact, CIIA-scrub status |
| `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md` | CIIA §2.3 scrub list — every flagged file, the pattern that flagged it, the redaction action needed before any public surfacing |
| `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md` | The user-facing payoff. Three sections: (A) bullets to strengthen with new metric/specifics, (B) net-new bullets to add, (C) story-bank entries unlocked. Each row cites source file + line range. |
| `vault/30_domains/product-management/the-block-resume-info/_AUDIT-INDEX.md` | Folder-local README pointing to the three deliverables above + the conversion log |
| `vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md` | Append-only log of every conversion: source path, output path, tool used, fidelity flag (clean / lossy / failed) |

Files to be modified:

| File | Modification |
|---|---|
| Every `.md` under `vault/30_domains/product-management/the-block-resume-info/` that lacks frontmatter | Prepend YAML frontmatter so the nightly indexer picks them up |
| `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md` line 220 | Mark the "deep audit + markdown conversion" follow-up done; link to the three new deliverables |

Files to be created alongside source artifacts (one `.md` per converted blob — placed in the same folder as the source so wikilinks work):

- `The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md` (from `.docx`)
- `The Block - PRD/Campus_Sponsored_MicroCourses_PRD_v3.md` (from `.docx`)
- `The Block - PRD/Campus Sponsored Micro-courses — Mvp Integration (matt-aligned Prd).md` (from `.docx`)
- `The Block - PRD/Sponsored_Courses_Sales_OnePager.md` (from `.docx`)
- `The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.md` (from `.docx`)
- `The Block - PRD/Sponsored_Courses_PRD_Confluence.md` (from `.docx`)
- `The Block - PRD/Campus_Sponsored_Courses_PRD_v2.md` (from `.docx`)
- `AdOps-Automation-Walkthrough.md` (from `.docx`)
- `The Block-x402-Research/x402 Strategy The Block.md` (from `.pdf`)
- `The Block-x402-Research/x402 Implementation Guide.md` (from `.pdf`)
- `The Block-x402-Research/x402 Competitive Landscape.md` (from `.pdf`)
- `The Block-x402-Research/Agentic Economy x402.md` (from `.pdf`)
- `The Block - PRD/PRD-Campus Sponsored Micro-Courses - MVP Integration-12-16.md` (from `.pdf`)
- `The Block - PRD/Ed Notes On PRD - 12-10.md` (from `.pdf`)
- `The Block - PRD/The Block Redesign — Stakeholder Interview Guide.md` (from `.pdf` — already has a `.md` twin, dedupe)

Files to be modified by adding frontmatter (sample — full list generated in Task 4):

- `the-block-resume-additions-2026.md`
- `The-Block-Job-Description.md`
- `TheBlock-And-Campus-Overviews.md`
- All 13 files in `The Block Job Description Breakdowns - ChatGPT/`
- All 9 files in `The Block - Bi-Weekly Update/` and its `Previous B-Weekly Updates/` subfolder
- All `.md` files in `SeanxEd-Q2-OKRs-Roadmap-2026/` excluding `node_modules/`

Files explicitly out of scope:

- All `node_modules/` (8,144 files in `Roadmap-2026/Pro-revamp-3-25-26-updated/data-explorer-server/node_modules/`)
- All `.DS_Store` (14 files)
- `.png`, `.jpeg`, `.jpg` (56 + 44 + 3 = 103 image files — they're indexed by parent doc; only describe in inventory)
- `.m4a` audio (3 files in `x402-Extra-Docs 2/`)
- `.xlsx`, `.pptx`, `.pages`, `.zip`, `.pen` (8 files — note in inventory, do not convert; flag for manual review if Sean wants any specific one)
- `.jsx`, `.js`, `.css`, `.html` (14 files — these are the data-explorer prototype; describe in inventory under "engineering artifacts" but do not convert)

---

## Task 1: Scaffold output files and read the source-of-truth set

**Files:**
- Create: `vault/30_domains/product-management/the-block-resume-info/_AUDIT-INDEX.md`
- Create: `vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md`
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md`
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md`
- Create: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md`

- [ ] **Step 1: Read the current resume and the bullet seed file.** This is the calibration set for everything downstream — every audit decision compares against these.

  Read all three with the Read tool:
  - `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md`
  - `vault/30_domains/product-management/the-block-resume-info/the-block-resume-additions-2026.md`
  - `vault/30_domains/product-management/the-block-resume-info/The-Block-Job-Description.md`

  Extract and write to a scratch note in your reasoning: (a) every Block bullet currently on the resume, verbatim, and (b) every claim from the bullet seed that is *not yet* on the resume. The audit will hunt for evidence to either upgrade (a) or back (b).

- [ ] **Step 2: Read the operating model + plan source paragraph that triggered this work.**

  Read lines 186–220 of `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md` (the Task 2.2 callout block). The plan already lists the high-value file set — confirm the file paths exist and capture any constraints stated there (CIIA §2.3 trigger words, conversion priority order).

- [ ] **Step 3: Create `_CONVERSION-LOG-2026-05-09.md`.**

  Write this file:

  ```markdown
  ---
  name: the-block-resume-info conversion log 2026-05-09
  description: Append-only log of every blob → markdown conversion run during the resume-info audit. One row per file. Used to verify nothing got dropped and to spot lossy conversions.
  type: archive-the-block
  domain: product-management
  ---

  # Conversion Log — 2026-05-09

  Format: `| source | output | tool | fidelity | notes |`

  Fidelity values: `clean` (no manual cleanup needed), `lossy` (tables / images / formatting dropped — usable but check), `failed` (do not trust).

  | source | output | tool | fidelity | notes |
  | --- | --- | --- | --- | --- |
  ```

  Leave the table empty — Tasks 3 and 5 will append rows.

- [ ] **Step 4: Create `the-block-resume-info-inventory-2026-05-09.md`.**

  Write this file with empty section bodies:

  ```markdown
  ---
  name: the-block-resume-info folder inventory 2026-05-09
  description: One-row-per-file inventory of vault/30_domains/product-management/the-block-resume-info/. Captures file type, byte size, one-line description, downstream artifact it can feed, and CIIA-scrub status. Generated by the audit pass executed 2026-05-09.
  type: archive-the-block
  domain: product-management
  status: draft
  ---

  # The Block resume-info folder inventory — 2026-05-09

  > Source folder: [`vault/30_domains/product-management/the-block-resume-info/`](../../../30_domains/product-management/the-block-resume-info/)
  >
  > Total non-node files inventoried: TBD-Task-2 (excluding node_modules/, .DS_Store, image files which are described inline under their parent doc).

  ## Legend

  - **Downstream artifact:** which job-hunt deliverable this file can feed. Values: `resume-bullet`, `portfolio-piece`, `story-bank`, `interview-prep`, `talk-track`, `cover-letter-input`, `reference-only`, `skip`.
  - **CIIA flag:** values: `clean` (no Block-protected IP), `redact` (contains §2.3-sensitive content; sanitize before public surfacing), `unreviewed` (Tier-3 file not deep-read this pass).

  ## Top-level files

  TBD-Task-2

  ## SeanxEd-Q2-OKRs-Roadmap-2026/

  TBD-Task-2

  ## The Block - PRD/

  TBD-Task-2

  ## The Block - Bi-Weekly Update/

  TBD-Task-2

  ## The Block-x402-Research/

  TBD-Task-2

  ## The Block Job Description Breakdowns - ChatGPT/

  TBD-Task-2

  ## Out of scope (noted, not described)

  TBD-Task-2
  ```

  The `TBD-Task-2` markers are filled in during Task 2 — they are NOT permanent placeholders.

- [ ] **Step 5: Create `the-block-resume-info-ciia-scrub-2026-05-09.md`.**

  ```markdown
  ---
  name: the-block-resume-info CIIA scrub list 2026-05-09
  description: Files in vault/30_domains/product-management/the-block-resume-info/ flagged for Block-protected content per CIIA §2.3. Each row lists the file, the trigger pattern, and the redaction action required before any public surfacing (portfolio site, public GitHub, LinkedIn).
  type: archive-the-block
  domain: product-management
  status: draft
  ---

  # CIIA §2.3 scrub list — the-block-resume-info — 2026-05-09

  > **Scrub criteria (from CIIA Section 2.3 read 2026-05-05):** proprietary client lists, internal Pro revenue figures, unannounced partnership names (specifically pre-launch Polymarket integration details), and any financial projections from the Pro 2.0 deck. Sean's own self-developed-IP carve-out (Section 2.4) covers the Superuser Pack, the agent fleet, and animation pipeline work — those do NOT need scrubbing.
  >
  > **Trigger patterns** searched in Task 6: `revenue|ARR|MRR|GMV|churn`, named clients (`Polymarket|Coinbase|Binance|Upbit` in pre-launch context), specific dollar amounts in proximity to product names, and the phrases "internal", "confidential", "do not share".

  | file | trigger pattern hit | redaction action | status |
  | --- | --- | --- | --- |

  ## Notes

  TBD-Task-6
  ```

- [ ] **Step 6: Create `resume-strengthening-recommendations-2026-05-09.md`.**

  ```markdown
  ---
  name: Resume strengthening recommendations 2026-05-09
  description: Concrete edit list for vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md and the three tailored variants. Each row cites the source artifact (file + line range) the recommendation is grounded in. Scope: bullets to strengthen with new metrics/specifics, net-new bullets to add, story-bank entries unlocked. Output of the the-block-resume-info audit pass executed 2026-05-09.
  type: career-asset
  domain: product-management
  status: draft
  ---

  # Resume strengthening recommendations — 2026-05-09

  > **What this is:** the user-facing payoff of the the-block-resume-info audit. It cross-references every resume-grade artifact discovered in `vault/30_domains/product-management/the-block-resume-info/` against the current master resume at `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md` and tells you exactly what to add or sharpen.
  >
  > **Decision rule:** every recommendation must cite (a) which current resume bullet it touches (or "NEW") and (b) the source artifact path + line range that grounds the claim. No claim without evidence.

  ## A. Bullets to strengthen (existing resume bullet → upgrade)

  TBD-Task-7

  ## B. Net-new bullets to add (under which section)

  TBD-Task-7

  ## C. Story-bank entries unlocked (Phase 6 interview prep — master plan Task 2.5)

  TBD-Task-7

  ## D. Portfolio-piece candidates (Phase 4 / unified roadmap Tasks 4–5)

  TBD-Task-7

  ## E. Considered and rejected

  TBD-Task-7
  ```

- [ ] **Step 7: Create `_AUDIT-INDEX.md` in the source folder.**

  Write to `vault/30_domains/product-management/the-block-resume-info/_AUDIT-INDEX.md`:

  ```markdown
  ---
  name: the-block-resume-info audit index
  description: Pointer file for the 2026-05-09 audit pass. Shows where the inventory, CIIA scrub list, conversion log, and resume recommendations live. Read this first when orienting to this folder.
  type: archive-the-block
  domain: product-management
  ---

  # The Block resume-info — audit index

  This folder is a 2026-05 archive of artifacts from Sean's tenure at The Block (Nov 2025 – May 2026). Used as raw material for the 2026 job-hunt sprint.

  **2026-05-09 audit pass produced:**

  - [Inventory](../../../20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md) — every file, what it is, what it can feed
  - [CIIA scrub list](../../../20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md) — files needing redaction before public surfacing
  - [Resume strengthening recommendations](../../../20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md) — concrete resume edits grounded in this folder
  - [Conversion log](_CONVERSION-LOG-2026-05-09.md) — every blob → markdown conversion, with fidelity notes

  **Folder shape:**

  - `SeanxEd-Q2-OKRs-Roadmap-2026/` — Q2 2026 OKR planning, Pro 2.0 revamp, Project CTO, P&E Confluence overhaul, iOS training
  - `The Block - PRD/` — Polymarket × Campus Sponsored Courses PRD evolution (v1 → v3 + Matt-aligned variant)
  - `The Block - Bi-Weekly Update/` — biweekly stakeholder updates, Jan–May 2026
  - `The Block-x402-Research/` — x402 / agentic-wallet research (4 strategy PDFs + extras)
  - `The Block Job Description Breakdowns - ChatGPT/` — JD competency breakdowns, one per JD line
  - Top-level: bullet seed (`the-block-resume-additions-2026.md`), JD copy, Block + Campus overview

  **Sister archive — Granola transcripts:** `vault/30_domains/product-management/the-block-meetings-granola-notes/` (84 meeting transcripts, indexed in the audit inventory under "Out of scope" with cross-references for the highest-value ones).
  ```

- [ ] **Step 8: Verify the five new files exist.**

  Run: `ls -la vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/*2026-05-09* vault/30_domains/product-management/the-block-resume-info/_AUDIT-INDEX.md vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md`
  Expected: all five files present, sizes between 400 bytes and 4 KB.

- [ ] **Step 9: Commit.**

  ```bash
  git add docs/superpowers/plans/2026-05-09-the-block-resume-info-audit-and-conversion.md vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md vault/30_domains/product-management/the-block-resume-info/_AUDIT-INDEX.md vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md
  git commit -m "docs(job-hunt): scaffold the-block-resume-info audit deliverables (2026-05-09)"
  ```

---

## Task 2: Generate the file inventory (auto, scripted)

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md`

- [ ] **Step 1: Generate the raw file list, sized, typed, sorted by folder.**

  Run:
  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  find . -type f \
    -not -path "*/node_modules/*" \
    -not -name ".DS_Store" \
    -exec stat -f "%z|%N" {} \; | sort -t'|' -k2
  ```
  Expected: ~432 lines (578 non-node total minus 14 .DS_Store, minus ~103 image files which are described inline under parent doc, minus 30 small junk). Pipe to a temp file: `> /tmp/the-block-resume-info-files.txt`.

- [ ] **Step 2: For each top-level group, write a one-line description per file into the inventory file.**

  Edit `the-block-resume-info-inventory-2026-05-09.md`. Replace each `TBD-Task-2` section with a markdown table:

  | path (relative to folder root) | size | type | one-line description | downstream artifact | CIIA flag |
  | --- | --- | --- | --- | --- | --- |

  For files where the description is non-obvious from the filename, open it via `head -30` (text files) or skip to Task 3/5 (blob files — leave description as `(content TBD post-conversion)`). Examples of obvious descriptions you can write without opening:

  - `the-block-resume-additions-2026.md` → `Sean's 14-bullet self-dump of Block workstreams, used as V1 resume seed`. Downstream: `resume-bullet`. CIIA: `clean`.
  - `The-Block-Job-Description.md` → `Block PM JD — competency list used for resume coverage cross-check`. Downstream: `cover-letter-input`. CIIA: `clean`.
  - `The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.docx` → `Final Confluence-format PRD for Polymarket × Campus Sponsored Courses, v3`. Downstream: `portfolio-piece`. CIIA: `redact` (Polymarket pre-launch detail).
  - `The Block-x402-Research/x402 Strategy The Block.pdf` → `Block-specific x402 / A2A / agentic-wallet integration strategy doc — anchor for resume Leadership-Experience bullet 4`. Downstream: `resume-bullet`. CIIA: `redact` (financial projections likely).

- [ ] **Step 3: Mark image files inline under their parent doc, not as separate rows.**

  Example, under the PRD section:
  ```
  | Sponsored_Courses_PRD_Confluence_v3.docx | … | docx | Final v3 PRD. Inline images: Sponsored_Courses_PRD.png, Sponsored-Course-User-Flow-Diagram-12-16.jpeg, USER-FLOW-12-17-PRD.jpg, Block-PRD-visual.png | portfolio-piece | redact |
  ```

- [ ] **Step 4: Fill in the "Out of scope" section.**

  List the 8 non-convertible blobs (`.xlsx`, `.pptx`, `.pages`, `.zip`, `.pen`) and the 14 engineering artifacts (`.jsx`, `.js`, `.css`, `.html`) and the 3 audio files. One row each, with a one-line note like "skip — manually open if a portfolio piece needs it" or "skip — engineering prototype only meaningful as compiled".

- [ ] **Step 5: Replace the `TBD-Task-2` count token at the top of the file with the real number.**

  Run: `wc -l /tmp/the-block-resume-info-files.txt` to confirm. Update the "Total non-node files inventoried" line.

- [ ] **Step 6: Verify the inventory has zero remaining `TBD-Task-2` markers.**

  Run: `grep -c "TBD-Task-2" vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md`
  Expected: `0`.

- [ ] **Step 7: Commit.**

  ```bash
  git add vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-inventory-2026-05-09.md
  git commit -m "docs(job-hunt): inventory the-block-resume-info folder (2026-05-09)"
  ```

---

## Task 3: Convert high-value `.docx` files to markdown

> **Tooling note:** macOS `textutil` (`/usr/bin/textutil`) is installed. It reads `.docx` and writes `.html` or `.txt`. Pandoc is NOT installed; we don't install it because (a) `textutil → html → manual cleanup` produces fine markdown for our purposes, (b) any pure-text fidelity loss is on tables/images which we'll inline-document anyway, (c) Sean's existing constraint is "Claude Code agents can read them directly without `pandoc` overhead" — installing pandoc just for one batch would contradict that. If `textutil`'s HTML output proves unreadable on a specific file, the fallback at Step 6 covers it.

**Files (created):**
- `vault/30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_PRD_Confluence.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Campus_Sponsored_MicroCourses_PRD_v3.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Campus_Sponsored_Courses_PRD_v2.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Campus Sponsored Micro-courses — Mvp Integration (matt-aligned Prd).md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Sponsored_Courses_Sales_OnePager.md`

**Files (modified):**
- `vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md` — append one row per converted file

- [ ] **Step 1: Convert each .docx to HTML, then strip to readable markdown.**

  Define the conversion command once and run it for each file. The pattern uses `textutil -convert html` then a sed pipeline that strips Apple-specific HTML wrappers and converts `<p>`, `<h1-6>`, `<ul>/<ol>/<li>`, `<strong>`, `<em>` to markdown equivalents. For the 8 files in this task, one shell loop:

  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  for f in \
    "AdOps-Automation-Walkthrough.docx" \
    "The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.docx" \
    "The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.docx" \
    "The Block - PRD/Sponsored_Courses_PRD_Confluence.docx" \
    "The Block - PRD/Campus_Sponsored_MicroCourses_PRD_v3.docx" \
    "The Block - PRD/Campus_Sponsored_Courses_PRD_v2.docx" \
    "The Block - PRD/Campus Sponsored Micro-courses — Mvp Integration (matt-aligned Prd).docx" \
    "The Block - PRD/Sponsored_Courses_Sales_OnePager.docx" \
  ; do
    out="${f%.docx}.md"
    /usr/bin/textutil -convert html -output "/tmp/textutil-out.html" "$f" && \
    python3 - <<'PY' > "$out"
  import re, html, sys
  with open("/tmp/textutil-out.html") as fp: s = fp.read()
  s = re.sub(r"<style[^>]*>.*?</style>", "", s, flags=re.S)
  s = re.sub(r"<head[^>]*>.*?</head>", "", s, flags=re.S)
  s = re.sub(r"<meta[^>]*>", "", s)
  s = re.sub(r"</?(html|body)[^>]*>", "", s)
  for tag, md in [("h1","# "),("h2","## "),("h3","### "),("h4","#### "),("h5","##### "),("h6","###### ")]:
      s = re.sub(rf"<{tag}[^>]*>", f"\n{md}", s, flags=re.I)
      s = re.sub(rf"</{tag}>", "\n", s, flags=re.I)
  s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", r"**\2**", s, flags=re.S|re.I)
  s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", r"*\2*", s, flags=re.S|re.I)
  s = re.sub(r"<li[^>]*>", "- ", s, flags=re.I)
  s = re.sub(r"</li>", "\n", s, flags=re.I)
  s = re.sub(r"</?(ul|ol)[^>]*>", "\n", s, flags=re.I)
  s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
  s = re.sub(r"<p[^>]*>", "\n", s, flags=re.I)
  s = re.sub(r"</p>", "\n", s, flags=re.I)
  s = re.sub(r"<a[^>]*href=\"([^\"]*)\"[^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S|re.I)
  s = re.sub(r"<[^>]+>", "", s)
  s = html.unescape(s)
  s = re.sub(r"\n{3,}", "\n\n", s)
  print(s.strip())
  PY
    echo "converted: $f → $out"
  done
  ```

  Expected: 8 new `.md` files, each between 2 KB and 50 KB. The script is one-shot; it does not need to be saved.

- [ ] **Step 2: Spot-check three converted files.**

  Read these three with the Read tool, capping at 80 lines each:
  - `AdOps-Automation-Walkthrough.md`
  - `The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md`
  - `The Block - PRD/Sponsored_Courses_Sales_OnePager.md`

  Look for: garbled HTML residue, missing headings, broken bullet structure, readable English prose. Headings should appear as `## ...`, bullets as `- ...`. If any file is unreadable, mark it `failed` in the conversion log and move it to the Step 6 fallback.

- [ ] **Step 3: Prepend frontmatter to each converted file.**

  For each newly-created `.md`, prepend a frontmatter block. The conversion script above output raw markdown — now add the YAML header. One-shot loop:

  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  for f in \
    "AdOps-Automation-Walkthrough.md" \
    "The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md" \
    "The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.md" \
    "The Block - PRD/Sponsored_Courses_PRD_Confluence.md" \
    "The Block - PRD/Campus_Sponsored_MicroCourses_PRD_v3.md" \
    "The Block - PRD/Campus_Sponsored_Courses_PRD_v2.md" \
    "The Block - PRD/Campus Sponsored Micro-courses — Mvp Integration (matt-aligned Prd).md" \
    "The Block - PRD/Sponsored_Courses_Sales_OnePager.md" \
  ; do
    base="$(basename "$f" .md)"
    # description placeholder — refined per-file in Step 4 below
    {
      echo "---"
      echo "name: ${base}"
      echo "description: (auto-converted from .docx 2026-05-09 — refine description in Task 7 deep-read)"
      echo "type: archive-the-block"
      echo "domain: product-management"
      echo "source: ${base}.docx"
      echo "converted: 2026-05-09"
      echo "ciia_status: unreviewed"
      echo "---"
      echo ""
      cat "$f"
    } > "$f.tmp" && mv "$f.tmp" "$f"
  done
  ```

- [ ] **Step 4: Hand-edit the `description:` field for each of the 8 files.**

  Replace the placeholder `description:` line with a one-line description grounded in the actual content. After running Step 3, read the first 50 lines of each file and write a single-sentence description capturing the doc's purpose. Use the Edit tool, replacing just the `description:` line. Examples:

  - `AdOps-Automation-Walkthrough.md` → `description: Walkthrough of the Zapier RevOps automation Sean built for the Block AdOps department — full step-by-step integration spec.`
  - `Sponsored_Courses_PRD_Confluence_v3.md` → `description: Final Confluence-format PRD for The Block × Polymarket Campus Sponsored Courses integration (v3) — covers user flow, X/Twitter auth, sponsor onboarding playbook hooks. Anchor doc for the Polymarket B2B revenue resume bullet.`

- [ ] **Step 5: Append a row to the conversion log for each of the 8 files.**

  Edit `_CONVERSION-LOG-2026-05-09.md`. Append rows like:

  ```
  | AdOps-Automation-Walkthrough.docx | AdOps-Automation-Walkthrough.md | textutil + py-strip | clean | tables flattened to bullets, no images |
  | The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.docx | The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md | textutil + py-strip | clean | (or "lossy" if Step 2 spot-check found issues) |
  ```

- [ ] **Step 6: Fallback path for any `failed` file.**

  If Step 2 marked any file as `failed`: open the source `.docx` in macOS Preview (or `open -a TextEdit "$f"`), copy its visible text, paste into the target `.md` file as-is. Add `extraction_method: manual-copy` to the frontmatter. This is rare but the path needs to exist; do not let one bad file block the rest.

- [ ] **Step 7: Verify all 8 .md files exist and have frontmatter.**

  Run:
  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  for f in "AdOps-Automation-Walkthrough.md" "The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md" "The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.md" "The Block - PRD/Sponsored_Courses_PRD_Confluence.md" "The Block - PRD/Campus_Sponsored_MicroCourses_PRD_v3.md" "The Block - PRD/Campus_Sponsored_Courses_PRD_v2.md" "The Block - PRD/Campus Sponsored Micro-courses — Mvp Integration (matt-aligned Prd).md" "The Block - PRD/Sponsored_Courses_Sales_OnePager.md"; do
    [ -f "$f" ] && head -1 "$f" | grep -q '^---$' && echo "ok: $f" || echo "MISSING_OR_NO_FRONTMATTER: $f"
  done
  ```
  Expected: 8 lines, all `ok:`.

- [ ] **Step 8: Commit.**

  ```bash
  git add vault/30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md "vault/30_domains/product-management/the-block-resume-info/The Block - PRD/"*.md vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md
  git commit -m "feat(job-hunt): convert 8 high-value .docx artifacts to markdown (resume-info audit)"
  ```

---

## Task 4: Frontmatter every existing `.md` for the vault indexer

> **Why:** the nightly `vault_indexer` agent only embeds files with YAML frontmatter. The 200+ existing `.md` files in this folder are currently invisible to it, which is why semantic search misses them.

**Files (modified):** every `.md` under `vault/30_domains/product-management/the-block-resume-info/` that does not start with `---`.

- [ ] **Step 1: Find every .md file lacking frontmatter.**

  Run:
  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  find . -type f -name "*.md" -not -path "*/node_modules/*" | while read f; do
    if ! head -1 "$f" | grep -q '^---$'; then
      echo "$f"
    fi
  done > /tmp/no-frontmatter.txt && wc -l /tmp/no-frontmatter.txt
  ```
  Expected: somewhere between 180–230 files (roughly 433 total .md minus the 8 just converted in Task 3 minus any with existing frontmatter).

- [ ] **Step 2: Generate per-file descriptions in batch.**

  For each file in `/tmp/no-frontmatter.txt`, derive a one-line description from the filename. Filename convention is descriptive (e.g., `Bi-Weekly-Update-May-1-2026.md` → "Bi-weekly stakeholder update for week of May 1, 2026"). Write a small python helper that does the filename → description mapping for the common cases, but spot-check 5 random files manually before running on all.

  Bulk-prepend script:
  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  while IFS= read -r f; do
    base="$(basename "$f" .md)"
    parent="$(dirname "$f" | sed 's|^\./||')"
    # naive description from filename: replace dashes/underscores with spaces, strip dates
    desc="$(echo "$base" | sed -E 's/[-_]+/ /g' | sed -E 's/[0-9]{1,2}-[0-9]{1,2}-[0-9]{2,4}//g' | sed -E 's/  +/ /g' | sed 's/^ //')"
    {
      echo "---"
      echo "name: ${base}"
      echo "description: ${desc} (Block archive — auto-frontmattered 2026-05-09)"
      echo "type: archive-the-block"
      echo "domain: product-management"
      echo "subfolder: ${parent}"
      echo "ciia_status: unreviewed"
      echo "---"
      echo ""
      cat "$f"
    } > "$f.tmp" && mv "$f.tmp" "$f"
  done < /tmp/no-frontmatter.txt
  ```

  This is intentionally a "good enough" first pass — Task 7 (deep-read audit) refines descriptions on the high-value subset. The other ~180 files are reference-only and the auto-description is fine.

- [ ] **Step 3: Verify zero .md files remain without frontmatter.**

  Run the same find from Step 1 again. Expected: empty output (or only the 8 files from Task 3 if the regex misses them, in which case those should already have frontmatter — verify with `head -3`).

- [ ] **Step 4: Sanity check — read 3 random files.**

  Pick 3 files from `/tmp/no-frontmatter.txt` at random. Read them. Confirm: (a) the file starts with a valid YAML block, (b) the body content is unchanged, (c) the description line is human-readable.

- [ ] **Step 5: Commit.**

  ```bash
  git add vault/30_domains/product-management/the-block-resume-info/
  git commit -m "feat(job-hunt): frontmatter all the-block-resume-info .md files for vault-indexer"
  ```

  Note: this is a 200+ file commit. That's fine — it's a single mechanical pass with no judgment calls per file, and the diff is small per file (8 lines added at top of each).

---

## Task 5: Convert the high-value `.pdf` files to markdown

> **Why:** the four x402 PDFs and the two PRD-related PDFs (`PRD-Campus Sponsored Micro-Courses - MVP Integration-12-16.pdf` and `Ed Notes On PRD - 12-10.pdf`) are central to two resume bullets that don't yet exist on the resume in detailed form. Conversion lets Task 7 grep for specific quantitative claims without re-running pdftotext interactively.

**Files (created):**
- `vault/30_domains/product-management/the-block-resume-info/The Block-x402-Research/x402 Strategy The Block.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block-x402-Research/x402 Implementation Guide.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block-x402-Research/x402 Competitive Landscape.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block-x402-Research/Agentic Economy x402.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/PRD-Campus Sponsored Micro-Courses - MVP Integration-12-16.md`
- `vault/30_domains/product-management/the-block-resume-info/The Block - PRD/Ed Notes On PRD - 12-10.md`

**Files (modified):**
- `vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md`

- [ ] **Step 1: Convert each .pdf using pdftotext (poppler).**

  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  for f in \
    "The Block-x402-Research/x402 Strategy The Block.pdf" \
    "The Block-x402-Research/x402 Implementation Guide.pdf" \
    "The Block-x402-Research/x402 Competitive Landscape.pdf" \
    "The Block-x402-Research/Agentic Economy x402.pdf" \
    "The Block - PRD/PRD-Campus Sponsored Micro-Courses - MVP Integration-12-16.pdf" \
    "The Block - PRD/Ed Notes On PRD - 12-10.pdf" \
  ; do
    out="${f%.pdf}.md"
    base="$(basename "${out}" .md)"
    pdftotext -layout "$f" "/tmp/pdf-text.txt"
    {
      echo "---"
      echo "name: ${base}"
      echo "description: (auto-converted from .pdf 2026-05-09 — refine description in Task 7 deep-read)"
      echo "type: archive-the-block"
      echo "domain: product-management"
      echo "source: ${base}.pdf"
      echo "converted: 2026-05-09"
      echo "extraction_method: pdftotext-layout"
      echo "ciia_status: unreviewed"
      echo "---"
      echo ""
      cat "/tmp/pdf-text.txt"
    } > "$out"
    echo "converted: $f → $out"
  done
  ```

- [ ] **Step 2: Spot-check two converted PDFs.**

  Read with the Read tool, capping at 100 lines each:
  - `The Block-x402-Research/x402 Strategy The Block.md`
  - `The Block - PRD/PRD-Campus Sponsored Micro-Courses - MVP Integration-12-16.md`

  pdftotext output is plain text with preserved layout — not markdown. Headings will not have `#` prefixes; tables come through as fixed-width columns. That's fine for grep + AI reading; it's NOT meant to be a polished doc. If a file is genuinely unreadable (rare with `-layout` flag), use the fallback at Step 4.

- [ ] **Step 3: Hand-edit the `description:` field for each of the 6 files.**

  Same approach as Task 3 Step 4. Examples:

  - `x402 Strategy The Block.md` → `description: Block-specific x402 protocol integration strategy — covers agentic-wallet flow, monetization model, integration with Pro MCP. Anchor for Leadership-Experience resume bullet 4 (X402 / A2A / Pro MCP mapping).`
  - `Ed Notes On PRD - 12-10.md` → `description: Ed Rupkus's annotated review notes on the v1 Campus Sponsored Courses PRD (12-10-2025) — captures cross-functional review feedback Sean incorporated into v3.`

- [ ] **Step 4: Fallback path for unreadable PDFs.**

  If a PDF is image-based (no extractable text), `pdftotext` will produce empty or garbage output. In that case, mark the conversion `failed` in the log and skip — note in the inventory that the file is "image-only PDF, content not searchable." Do not OCR; that's beyond audit scope.

- [ ] **Step 5: Append rows to the conversion log.**

  Same pattern as Task 3 Step 5. Six new rows.

- [ ] **Step 6: Commit.**

  ```bash
  git add "vault/30_domains/product-management/the-block-resume-info/The Block-x402-Research/"*.md "vault/30_domains/product-management/the-block-resume-info/The Block - PRD/"PRD-Campus*.md "vault/30_domains/product-management/the-block-resume-info/The Block - PRD/"Ed*Notes*.md vault/30_domains/product-management/the-block-resume-info/_CONVERSION-LOG-2026-05-09.md
  git commit -m "feat(job-hunt): convert 6 high-value .pdf artifacts to markdown (resume-info audit)"
  ```

---

## Task 6: CIIA §2.3 scrub flag pass

> **Why this is its own task:** before any of these files inform a public-facing resume, portfolio piece, or LinkedIn post, anything containing Block-protected IP needs an explicit redact-or-keep decision. Doing this once produces a reusable scrub list for every downstream surfacing.

**Files (modified):**
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md`
- Every `.md` file flagged: update its frontmatter `ciia_status:` from `unreviewed` to `clean` or `redact`

- [ ] **Step 1: Run the trigger-pattern grep across every converted + native .md.**

  ```bash
  cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/30_domains/product-management/the-block-resume-info && \
  rg -i --no-heading -n -e '\$[0-9]+(?:[,.]?[0-9])*(?:[KMB])?' \
                       -e '\b(?:ARR|MRR|GMV|churn rate|conversion rate)\b' \
                       -e '\b(?:Polymarket|Coinbase|Binance|Upbit|OKX|Kraken)\b' \
                       -e '\b(?:internal|confidential|do not share|do not distribute)\b' \
                       -e '\bPro 2\.0\b' \
                       *.md "*/"*.md "*/*/"*.md 2>/dev/null > /tmp/ciia-grep-hits.txt && wc -l /tmp/ciia-grep-hits.txt
  ```
  Expected: 50–500 hits across 30–80 files. Most will be benign (e.g., "Polymarket" appears in the Sponsored Courses PRD because that IS the partnership — but it was launched, so post-launch mentions are clean; pre-launch detail is the redact-flag).

- [ ] **Step 2: Review hits and classify each flagged file.**

  Read `/tmp/ciia-grep-hits.txt`. For each unique file, decide:
  - **clean:** all hits are post-launch public information or Sean's own work covered by the Section 2.4 self-developed-IP carve-out. Example: `the-block-resume-additions-2026.md` — Polymarket mention is a launched, publicly-announced integration.
  - **redact:** at least one hit is genuinely Block-protected. Example: any internal Pro revenue figure, any unannounced partnership name, financial projections from the Pro 2.0 deck. Decision: this file should NOT be surfaced publicly without sanitization.
  - **redact-but-keep-internal:** the file is fine to keep in the vault for Sean's own reference but must never be referenced from a public artifact. Example: the Pro 2.0 CEO briefing xlsx (out of scope but flag the parent folder).

- [ ] **Step 3: Update the CIIA scrub list with one row per flagged file.**

  Edit `the-block-resume-info-ciia-scrub-2026-05-09.md`. Replace the empty table body with rows like:

  ```
  | The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md | "Polymarket" + revenue projections in §3.2 | redact section §3.2 before any public surfacing; sponsor onboarding playbook hooks are clean | redact |
  | SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/CEO-Pitch-Slide-Foundation.md | financial projections; "Pro 2.0" pre-launch detail | keep internal-only — never reference from public resume / portfolio / LinkedIn | redact-but-keep-internal |
  | the-block-resume-additions-2026.md | "Polymarket" mentioned post-launch | no action — public info | clean |
  ```

  Be specific. Each row has to actually inform a redaction action a future agent could execute.

- [ ] **Step 4: Update each flagged file's frontmatter.**

  For each file marked `redact` or `redact-but-keep-internal`, edit its YAML frontmatter and change the `ciia_status: unreviewed` line to `ciia_status: redact` or `ciia_status: redact-internal-only`. For files reviewed and confirmed clean, change to `ciia_status: clean`. (Files not touched in this pass remain `unreviewed` — that's the default and is fine.)

- [ ] **Step 5: Add a "Notes" subsection to the scrub list summarizing scope.**

  Replace the `TBD-Task-6` line with one paragraph: how many files reviewed, how many flagged redact, how many redact-but-keep-internal, and which folders had the most concentration of flags.

- [ ] **Step 6: Verify the scrub list has zero `TBD-Task-6` markers and at least one row per flagged file.**

  ```bash
  grep -c "TBD-Task-6" vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md
  ```
  Expected: `0`.

- [ ] **Step 7: Commit.**

  ```bash
  git add vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/the-block-resume-info-ciia-scrub-2026-05-09.md vault/30_domains/product-management/the-block-resume-info/
  git commit -m "feat(job-hunt): CIIA scrub pass on the-block-resume-info — flagged files + per-file ciia_status"
  ```

---

## Task 7: Deep-read audit — match artifacts to resume bullets

> **This is the actual user payoff.** Tasks 1–6 prepared the ground; this task produces the recommendation list. Estimated 60–90 minutes of focused reading. Subagent-friendly: dispatch one subagent per artifact-cluster for the read pass, but the synthesis (cross-referencing back to the resume) must happen in the main session.

**Files (modified):**
- `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md`

- [ ] **Step 1: Re-read the current master resume.**

  Open `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md` and write down (in your reasoning, not in a file) the exact text of all five bullets in the Work Experience → The Block section, plus all four bullets in the Leadership Experience → The Block section. Also note the three Selected Projects and the Skills section. This is the comparison anchor.

- [ ] **Step 2: Cluster A — read the AdOps automation artifact.**

  Read `vault/30_domains/product-management/the-block-resume-info/AdOps-Automation-Walkthrough.md` end to end (post-conversion from Task 3).

  Hunt for: specific tool integrations named (Zapier + WordPress + Jira + ?), specific time saved (any hours/week or % automation), specific output count (how many tickets created automatically, how many ETF pages generated), the actual scope of automation (is it just ETFs, or broader?). Compare against current resume bullet: *"Built and shipped 3 production Claude Skills (etf-page-creator, stakeholder-update, jira-automation) and a Zapier RevOps automation pipeline for the AdOps department — automating WordPress ETF page generation, Jira ticket creation, and biweekly stakeholder updates."*

  Decide: **strengthen** (with a metric like "X hours/week reclaimed" or "Y tickets/month auto-routed"), **keep as-is** (current bullet already captures the substance), or **add net-new bullet** (if there's a separate workstream uncovered).

- [ ] **Step 3: Cluster B — read the Polymarket × Sponsored Courses PRD set.**

  Read these four converted files in order:
  1. `The Block - PRD/Sponsored_Courses_PRD_Confluence.md` (v1)
  2. `The Block - PRD/Sponsored_Courses_PRD_Confluence_v2.md`
  3. `The Block - PRD/Sponsored_Courses_PRD_Confluence_v3.md` (final)
  4. `The Block - PRD/Sponsored_Courses_Sales_OnePager.md` (sales-facing)

  Hunt for: scope of the partnership, scope of the integration (just Sponsored Courses, or broader Polymarket × Block?), measurable launch outcome if any, the number of sponsor onboarding steps, the X/Twitter auth scope ("first sponsor of the year" / "first B2B revenue vertical of the year" — is there evidence that's literally true or is it Sean's self-framing?). Compare against current resume bullet: *"Drafted the PRD and shipped the Polymarket × Campus Sponsored Courses integration end-to-end — The Block's first sponsored-microcourse B2B revenue vertical, including X/Twitter auth flow and full user-flow QA."*

  Decide: same options as Step 2.

- [ ] **Step 4: Cluster C — read the x402 strategy set.**

  Read these four converted files:
  1. `The Block-x402-Research/x402 Strategy The Block.md`
  2. `The Block-x402-Research/x402 Implementation Guide.md`
  3. `The Block-x402-Research/Agentic Economy x402.md`
  4. `The Block-x402-Research/x402 Competitive Landscape.md`

  Hunt for: how Sean specifically positioned the x402 + A2A + Pro MCP integration story (what was the deliverable — a memo, a proposal, a slide deck?), who consumed it (incoming CEO, Ed, Block leadership?), what decision did it drive. Compare against current resume bullet (Leadership Experience): *"Mapped the integration of the X402 protocol, A2A (agent-to-agent), and The Block Pro MCP into a unified agentic-wallet transaction strategy, positioning Block Pro for the agent economy under the incoming CEO."*

  Decide: same options.

- [ ] **Step 5: Cluster D — read the Q2 OKRs + bi-weekly updates + Project CTO set.**

  Read these (most are existing native .md, post-Task-4 frontmatter pass):
  1. `SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Q2-OKRs.md` (the OKR backbone)
  2. `SeanxEd-Q2-OKRs-Roadmap-2026/P&E-Department-2.0-Execution-Plan.md` (10-week Confluence overhaul)
  3. `SeanxEd-Q2-OKRs-Roadmap-2026/TASKS.md`
  4. `The Block - Bi-Weekly Update/Bi-Weekly-Update-May-1-2026.md`
  5. `The Block - Bi-Weekly Update/Bi-Weekly-Update-April-17-2026.md`
  6. `SeanxEd-Q2-OKRs-Roadmap-2026/Project-CTO/Project-CTO-Visual-Audit-List.md`

  Hunt for: which OKRs Sean *owned* (Objectives 4 and 5 per the CLAUDE.md in that subfolder — confirm), what the actual KR completion state was as of the last bi-weekly, the breadth of the Confluence consolidation (mentioned: "7 competing team-doc hubs", "25+ orphaned meeting-note pages" — verify those numbers from source). Compare against current resume bullets — particularly the Confluence consolidation bullet ("Authored the 10-week P&E Department 2.0 execution plan...").

- [ ] **Step 6: Cluster E — read the Pro 2.0 / Pro Revamp set selectively.**

  This subfolder is huge (~50 files). Don't read all of it. Read these targeted files:
  1. `SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/CEO-Pitch-Narrative-Synthesis.md`
  2. `SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Block-Pro-Audit-and-Gap-Analysis.md`
  3. `SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Pro-Search-Pre-Mortem.md`
  4. `SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Pro-Search-Value-Proposition.md`

  Hunt for: scope of Sean's contribution (was he lead? co-lead? a contributor?), the prototype that was built (data-explorer-server is in that folder — is it real, demoable, or sketch?), the user-research methodology (A/B sessions: how many, what came of them?). Compare against current resume bullet: *"Performed competitive research, stakeholder interviews, A/B-session analysis, and built the demo-ready prototype for the Pro 2.0 platform proposal delivered to the incoming CEO."*

  **Heavy CIIA caution here.** This cluster is the most likely to have `redact` flags. Lean toward conservative phrasing in any new bullet — avoid revenue projections, avoid specific institutional client names, frame in capability terms ("competitive intelligence on N institutional crypto data products" rather than naming them).

- [ ] **Step 7: Cluster F — Granola transcripts cross-reference.**

  This is a sister folder, NOT inside the-block-resume-info, but the master plan flagged it explicitly: `vault/30_domains/product-management/the-block-meetings-granola-notes/` (84 files).

  Don't read all 84. Read these high-signal three:
  1. `Larry_Cermak_Final_Meeting.md` (the layoff meeting — story-bank material for the layoff line)
  2. `MattxEdxSean Meeting.md` (Matt is the incoming CEO context — verify how Sean framed the Pro 2.0 work)
  3. `Sean × Ed Pro Workshop` (search for the file with that name pattern — it exists per the master plan)

  Hunt for: direct-quote phrasing Sean used to describe his own work, framings that worked well (and might work in interviews), specific story beats (the moment Matt accepted the proposal, etc.). These feed the **C. Story-bank entries** section, not the resume bullets directly.

- [ ] **Step 8: Synthesize Cluster A–F findings into the recommendations file.**

  Edit `resume-strengthening-recommendations-2026-05-09.md`. Replace each `TBD-Task-7` section with concrete rows.

  Section A format (bullets to strengthen):
  ```
  ### Resume bullet: "Built and shipped 3 production Claude Skills..."
  - **Source:** AdOps-Automation-Walkthrough.md, lines 42–58
  - **Current:** "...automating WordPress ETF page generation, Jira ticket creation, and biweekly stakeholder updates."
  - **Strengthen to:** "...automating WordPress ETF page generation (X pages/week), Jira ticket creation (Y tickets/month auto-routed), and biweekly stakeholder updates (Z hours/week reclaimed)."
  - **Caveat:** verify the X/Y/Z numbers are real before shipping; if Sean can't defend them in an interview, drop the metric and keep the qualitative version.
  ```

  Section B format (net-new bullets):
  ```
  ### NEW bullet (Work Experience → The Block, suggested position: bullet 6)
  - **Source:** SeanxEd-Q2-OKRs-Roadmap-2026/Roadmap-2026/Pro-revamp-3-25-26-updated/Block-Pro-Audit-and-Gap-Analysis.md
  - **Proposed text:** "Authored the Block Pro audit & gap analysis surfacing N feature gaps vs. competitive set (Blockworks, Dune, Messari) — used as the cornerstone artifact for the Pro 2.0 strategic deck delivered to the incoming CEO."
  - **CIIA risk:** medium — verify no internal revenue figures leaked into bullet phrasing; competitive set is public info.
  ```

  Section C format (story-bank entries):
  ```
  ### Story: "The MattxEdxSean Pro 2.0 alignment moment"
  - **Source:** the-block-meetings-granola-notes/MattxEdxSean Meeting.md
  - **Beats:** S=Block CEO transition; T=Sean tasked with Pro 2.0 proposal alignment; A=structured the meeting around three strategic pillars; R=Matt approved direction, became foundation for the deck.
  - **Use for:** Phase 6 interview prep, master plan Task 2.5 story 1 ("Block Pro revamp — your flagship").
  ```

  Section D format (portfolio-piece candidates):
  ```
  ### Portfolio piece: "Polymarket × Campus Sponsored Courses — full PRD evolution"
  - **Source:** The Block - PRD/Sponsored_Courses_PRD_Confluence_v1/v2/v3.md (post-Task-3 conversion)
  - **Why it works:** v1→v3 evolution shows real PM craft; v3 was final, shipped artifact.
  - **CIIA gating:** must redact any pre-launch revenue projections before public surfacing — flagged in CIIA scrub list.
  - **Best fit:** unified roadmap Task 4 (sanitized portfolio piece) or Phase 4 EXPLANATION.md.
  ```

  Section E format (considered and rejected):
  ```
  ### Rejected: iOS Training docs
  - **Source:** SeanxEd-Q2-OKRs-Roadmap-2026/iOS-Training-2026/*.md
  - **Why considered:** complete training docs Sean produced for fellow PMs.
  - **Why rejected:** internal training, not externally legible value; covered already in current Leadership-Experience bullet 2.
  ```

- [ ] **Step 9: Write a 5-line executive summary at the top of the recommendations file.**

  Right under the H1, before Section A:

  ```markdown
  ## TL;DR

  - Audit reviewed N source artifacts across 6 thematic clusters (AdOps, Polymarket PRD, x402, OKRs/biweeklies, Pro 2.0, Granola transcripts).
  - **K bullets to strengthen** (with metrics from the source artifacts) — Section A.
  - **M net-new bullet candidates** for the master resume — Section B.
  - **P story-bank entries** unlocked for Phase 6 interview prep — Section C.
  - **Q portfolio-piece candidates** that need CIIA redaction before public surfacing — Section D + cross-ref `the-block-resume-info-ciia-scrub-2026-05-09.md`.
  - Conservative recommendation: pick top 3 from B, top 5 from A, ship the resume update in one ~45-min session this week.
  ```

  Replace N, K, M, P, Q with the real counts.

- [ ] **Step 10: Verify the recommendations file has zero `TBD-Task-7` markers.**

  ```bash
  grep -c "TBD-Task-7" vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md
  ```
  Expected: `0`.

- [ ] **Step 11: Commit.**

  ```bash
  git add vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/resume-strengthening-recommendations-2026-05-09.md
  git commit -m "feat(job-hunt): resume strengthening recommendations from the-block-resume-info audit"
  ```

---

## Task 8: Update the master plan and close the loop

**Files:**
- Modify: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md` (the Task 2.2 follow-up callout, lines ~209–220)

- [ ] **Step 1: Read the current Task 2.2 follow-up paragraph.**

  Re-read lines 209–220 of the master plan. The paragraph currently ends with `Best run before the Phase 5 Week-3 application surge or before any portfolio piece starts referencing these artifacts. Daily-note breadcrumb for this V1 session: ...`

- [ ] **Step 2: Edit the paragraph to mark the follow-up complete.**

  Use the Edit tool. Replace the paragraph header `> **Recommended follow-up — deep audit + markdown conversion (~90 min, not yet scheduled):**` with `> **Recommended follow-up — deep audit + markdown conversion ✅ COMPLETED 2026-05-09:**`.

  Append after the existing paragraph body (before the next `>` line if any):

  ```
  >
  > **Audit deliverables (2026-05-09):**
  > - [Inventory](the-block-resume-info-inventory-2026-05-09.md) — N files described
  > - [CIIA scrub list](the-block-resume-info-ciia-scrub-2026-05-09.md) — K files flagged for redaction
  > - [Resume strengthening recommendations](resume-strengthening-recommendations-2026-05-09.md) — M bullets to strengthen, P new candidates, Q portfolio pieces
  > - 14 high-value `.docx` + `.pdf` files converted to markdown alongside their sources
  > - 200+ existing `.md` files frontmatter-stamped for the nightly vault-indexer
  ```

  Replace N, K, M, P, Q with the real counts pulled from the recommendations file TL;DR.

- [ ] **Step 3: Update the Task 2.2 STATUS callout (line ~190).**

  The current STATUS line reads `**Pending on Sean's side:** read each aloud (Step 7), cut what sounds robotic, decide whether NYL bullets need modernization for 2026-target recruiters, decide whether the HelloPM cert listing is still active.`

  Append: ` **Resume strengthening recommendations from the-block-resume-info deep-audit are now in [`resume-strengthening-recommendations-2026-05-09.md`](resume-strengthening-recommendations-2026-05-09.md) — review before next resume revision.`

- [ ] **Step 4: Verify the master plan still parses and the link works.**

  Read the modified region of the master plan with the Read tool. Confirm: (a) markdown is valid (no broken `>` blockquotes), (b) the three new links resolve to real files in the same directory, (c) no double-checkmark or duplicated content.

- [ ] **Step 5: Commit.**

  ```bash
  git add vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md
  git commit -m "docs(job-hunt): close the-block-resume-info deep-audit follow-up in master plan"
  ```

- [ ] **Step 6: Final verification — read the three deliverables top-to-bottom.**

  Read the three new files end to end (post-Task-7) one last time as a hiring-manager-style review. Specifically check:
  - Inventory: every cluster has at least one row marked `resume-bullet` or `portfolio-piece` (otherwise the audit failed to find resume-grade material)
  - CIIA scrub list: every flagged file has an actionable redaction step (not just "review")
  - Recommendations: every Section A/B row cites a specific source path + line range; no row says "consider adding" or "potentially useful" — those are placeholder failures

  If any of those checks fails, fix the relevant file inline and append a follow-up commit.

- [ ] **Step 7: Report back.**

  Write a 5-bullet summary message to Sean: how many source artifacts read, top 3 strongest recommendations from Section A/B, top 1 portfolio piece from Section D, the count of CIIA-flagged files, and a one-line "what to do next" (recommended: review recommendations, pick 3-5 to apply to the resume tonight or this weekend, ship updated resume).

---

## Self-Review

**Spec coverage check against the user's ask:**

The user asked for: (1) a plan to do the deep audit + markdown conversion of `vault/30_domains/product-management/the-block-resume-info/`, (2) identify items that would strengthen the existing resume at `vault/20_projects/prj-job-hunt-2026/assets/Sean_Winslow_Resume.md`, (3) decide what should be converted to markdown for future agents.

- (1) Audit + conversion → Tasks 2 (inventory), 3 (.docx → .md), 4 (frontmatter for indexer), 5 (.pdf → .md). ✅
- (2) Resume strengthening → Task 7 produces a structured recommendations file with explicit "strengthen this bullet / add this bullet" rows grounded in source artifacts. ✅
- (3) Markdown conversion decision → Tasks 3 + 5 cover the 14 high-value blob files (8 .docx + 6 .pdf). The reason for converting *just these 14* and not all 29 .docx + 94 .pdf is captured in the File Structure scope statement: only the resume-grade and audit-relevant artifacts. The other 87 PDFs are mostly research deep-dives, deck PDFs, and archived references that the inventory describes inline; they're not load-bearing for a resume. If Sean wants a wider pass, that's a follow-up, not v1 scope. ✅
- (4) CIIA scrub (a constraint the master plan imposed) → Task 6. ✅
- (5) Master-plan loop closure → Task 8. ✅

**Placeholder scan:**

- All `TBD-Task-N` tokens in the deliverable file scaffolds are explicitly filled by the named task. They are not unresolved placeholders.
- No "TBD", "implement later", "fill in details", "as appropriate" in any task step.
- Every Edit-style step says exactly which line/section to change and what the new content is.
- Every grep/find command has expected output described.
- The "Decide same options as Step 2" pattern in Task 7 Steps 3–6 is acceptable because Step 2 explicitly enumerates the three decision options ("strengthen / keep / add new"); the engineer doesn't have to invent the criteria.

**Type consistency:**

- File paths are consistent: `vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/` for deliverables that belong to the job-hunt project, `vault/30_domains/product-management/the-block-resume-info/` for files that live with the source archive.
- Frontmatter schema is consistent across all generated files: `name`, `description`, `type` (always `archive-the-block` for source-folder files, `career-asset` for the recommendations file), `domain: product-management`, plus per-file extras (`source`, `converted`, `extraction_method`, `ciia_status`).
- The `ciia_status` field uses three values consistently: `unreviewed` (default), `clean`, `redact`, `redact-internal-only`. Task 6 Step 4 + the scrub list both use this exact vocabulary.
- The "downstream artifact" enum is defined once in the inventory legend and used identically in Task 2 Step 2 row examples and Task 7 Section D.

**Judgment calls flagged:**

- **Pandoc deferred.** I chose `textutil + py-strip` over installing pandoc. Reason: Sean's master plan explicitly framed the goal as "no pandoc overhead," textutil is native, and the conversion fidelity for these specific PRD/walkthrough/strategy docs (which are mostly prose + bullets, not heavy on tables/equations) is good enough. If a converted file is unreadable, Task 3 Step 6 has a manual-copy fallback. If multiple files prove lossy, that's a signal to install pandoc as a one-shot follow-up — not a v1 blocker.
- **Granola transcripts treated as sister folder, not in scope.** The master plan flagged them but they live at `vault/30_domains/product-management/the-block-meetings-granola-notes/`, not in `the-block-resume-info/`. I included them in Task 7 Cluster F because story-bank material is in scope for the user's question, but I did NOT inventory all 84 transcripts (would balloon the audit). If Sean wants a full Granola sweep, separate plan.
- **The Pro-revamp `data-explorer-server/` engineering prototype is out of scope.** It's a working JSX + Node prototype Sean built for the Pro 2.0 demo. It's resume-grade (it's THE prototype the current resume references) but the value is in its existence, not its source code. Inventoried as a single row, not file-by-file.
- **All ~200 .md frontmatter pass uses naive filename → description.** Task 4 prioritizes coverage over per-file polish. Task 7's deep-read pass refines descriptions on the high-value subset. The remaining ~180 reference-only files get a "good enough" description that the indexer can use for embedding-based retrieval. Refining all 200 manually is out of scope.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-05-09-the-block-resume-info-audit-and-conversion.md`.**

This is a research + audit plan, not a TDD code plan. The bulk of the work is reading and synthesizing — Task 7 is the time sink (60–90 min of focused reading). Tasks 1–6 are mechanical and scriptable; Task 7 is human/Claude judgment; Task 8 is housekeeping.

**Two execution options:**

**1. Subagent-Driven (recommended for Tasks 2, 3, 4, 5, 6)** — I dispatch a fresh subagent per task, you review between tasks. Tasks 7 and 8 are kept in the main session because they require synthesis against the resume that benefits from continuous context.

**2. Inline Execution (recommended if you want to ship the audit in one sitting)** — Execute all tasks in this session using `superpowers:executing-plans`, with checkpoints after Tasks 2, 6, and 7 for you to review.

Which approach?
