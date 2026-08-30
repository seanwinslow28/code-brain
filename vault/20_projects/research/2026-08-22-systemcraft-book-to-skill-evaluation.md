---
title: "Systemcraft corpus — book-to-skill evaluation (#149)"
date: 2026-08-22
project: systemcraft
status: draft
tags: [research, systemcraft, corpus, tooling, book-to-skill]
cost: $0 (source-and-docs evaluation; no code executed, no LLM spend)
---

# book-to-skill evaluation — findings brief

Evaluation of [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (v1.4.0, MIT, last commit 2026-08-19) as the ingestion tool for the Systemcraft reference corpus. Method: cloned to a scratch directory and read the source, SKILL.md spec, and docs. **No code was executed, no dependencies installed, no book content touched.**

## 1. What it actually does

Two halves, cleanly separated:

1. **A deterministic Python extractor** (`scripts/extract.py` → `book_to_skill/` package): converts a document (or folder/glob of documents) into one clean `full_text.txt` plus a `metadata.json` (pages, words, token estimate, per-source stats). Pure local text extraction — **the extractor makes no network or LLM calls**.
2. **A generator spec** (`SKILL.md`, ~700 lines): a step-by-step procedure that the *host agent* (Claude Code, Copilot CLI, or Amp) follows to distill the extracted text into a structured "book skill". The LLM doing the distillation is your own Claude Code session — the tool ships no model, no API key, no cloud service.

The output is not a summary; the spec explicitly extracts *structure*: named frameworks ("preserve the author's exact naming"), decision rules, techniques, anti-patterns, glossary terms — with hard per-file token budgets and a "never copy raw book text" quality rule (Quality Rule #7).

## 2. Input formats → purchase-format verdict (unblocks #151)

Supported: **PDF, EPUB, DOCX, TXT, Markdown, reStructuredText, AsciiDoc, HTML, RTF, MOBI/AZW/AZW3** (last three require the external Calibre app).

**Verdict: buy the six O'Reilly books as EPUB; DRM-free PDF is the acceptable fallback; avoid MOBI/AZW.**

Why EPUB wins:

- The EPUB path (`ebooklib` + `beautifulsoup4`, with a zero-dependency stdlib-zipfile fallback) is the repo's own top-rated extraction tier ("⭐⭐⭐ Best"), and it is instant.
- EPUB is reflowable HTML inside a zip: no page headers/footers to strip, no scanned-page risk, and chapter boundaries survive extraction (their Moby-Dick EPUB test auto-detected all 133 chapters via its ToC).
- Technical *PDFs* need the heavyweight `docling` extractor (~1.5 s/page, big dependency) to preserve code blocks and tables; the fast `pdftotext` path flattens them. EPUB sidesteps that trade-off entirely.
- MOBI/AZW requires Calibre and is usually DRM-locked — a dead end.

One caveat either way: figures/diagrams are never extracted (text baked into images is lost, by design), and scanned PDFs hard-abort with an "OCR first" message.

## 3. Output shape and fit with the five-lane layout

Per book, the generator writes one folder:

| File | Purpose | Budget |
|---|---|---|
| `SKILL.md` | Core frameworks + chapter/topic index | ~4,000 tokens |
| `chapters/chNN-slug.md` (one per chapter) | On-demand chapter distillations | ~1,000–3,000 tokens each (depth × book-type matrix) |
| `glossary.md` | All key terms, alphabetized, chapter refs | ~1,500 tokens |
| `patterns.md` | Techniques/patterns with when/how/trade-offs | ~2,000 tokens |
| `cheatsheet.md` | Decision rules, thresholds, trade-off matrices | ~1,200 tokens |

Realistic size per technical book: roughly **20–60K tokens ≈ 100–250 KB of plain Markdown**. Chapter files load on demand, so a session only pays for the slice it reads.

**Fit verdict: yes, cleanly.** The output is just a self-contained Markdown folder per book. The five-lane Systemcraft layout is an organizational wrapper on top — e.g. `references/framing/<book-slug>/`, `references/architecture/<book-slug>/`, etc., inside a gitignored path (mirroring the existing `.claude/skills/*/references/` private-layer pattern). Nothing in the output hardcodes its location; the spec asks where to write and a custom destination works. The tool's own copyright policy also matches ours: **skills generated from purchased books must stay private/gitignored — never committed to the public repo.** Its Step 11 "publish to GitHub" offer must always be declined for these.

## 4. End-to-end workflow for one purchased book

1. **One-time setup:** `git clone https://github.com/virgiliojr94/book-to-skill.git ~/.claude/skills/book-to-skill` (clone the **official repo only** — see §5), then `pip3 install ebooklib beautifulsoup4` (the only deps the EPUB path wants), and sanity-check with `python3 scripts/extract.py --check`.
2. In a Claude Code session: `/book-to-skill ~/books/the-book.epub <lane-slug>-<book-slug>`.
3. Answer two questions: content type (**technical** vs text-heavy — for EPUBs either is fast) and purpose (reference vs study — sets chapter depth).
4. Confirm the pre-flight token/cost estimate it prints from `metadata.json`.
5. The agent extracts locally, then greps/seds its way through `full_text.txt` chapter by chapter (REPL-style, not one giant read) and writes the skill folder.
6. It runs its own advisory security scan (`tools/scan_generated_skill.py`) on the generated files, cleans up the temp workdir, and reports.
7. **Decline the publish-to-GitHub offer.** Move/point the folder to the correct gitignored lane directory.

Time: minutes per book. Repeat six times; the Update/Fold-in mode (Mode 4) can later merge errata or companion papers into an existing book skill.

## 5. Licensing, dependencies, cost, gotchas

- **License:** MIT (converter only; explicitly not the processed content).
- **Python:** ≥ 3.9. Zero *required* dependencies — every format has a stdlib fallback; optional extras per format (`ebooklib`/`bs4` for EPUB best-tier).
- **API keys / LLM:** none of its own. Distillation runs inside your Claude Code session; the repo's measured benchmark is **~$1/book at Sonnet API rates** (~150–400K input tokens per book) — on a Claude subscription this is session token budget, not new dollars. Extraction itself is $0 and offline.
- **SECURITY (the big one):** the repo carries a 2026-08-17 `SECURITY-NOTICE.md`: a **malicious re-upload at `Leutenegger/book-to-skill`** circulated with wallet-enumeration and data-exfiltration code added. Install only from `virgiliojr94/book-to-skill` (or `npx skills add virgiliojr94/book-to-skill`); never from search results.
- **Chapter auto-detection** needs explicit `Chapter N`-style headings; books using bare section titles (their Pro Git example) still convert but need manual chapter pointing.
- **Session-context cost:** converting a 300-page book consumes a large chunk of one session's context; run conversions as dedicated sessions, one book each.
- Scanned PDFs abort by design (run `ocrmypdf` first); irrelevant if we buy EPUBs.

## 6. Adopt vs in-house — recommendation

**Adopt.** The hypothetical in-house alternative ("plain chapter-splitting + Claude distillation") is essentially what this tool *is* — except it has already paid for the unglamorous 80%: seven format parsers with graceful fallbacks, boilerplate/header stripping, chapter detection (incl. non-English and Roman-numeral ToCs), Unicode/bidi sanitization, batch resilience, a ~50-test pytest suite, and a distillation spec with token-budget discipline and a "never copy raw text" copyright posture that matches our public-repo privacy law. Rebuilding that for six books would cost more than the six conversions themselves and would be worse at the edges.

Adaptation needed is trivial and organizational, not code: (a) pin the install to the official repo, (b) decline the publish step, (c) place each generated folder under its Systemcraft lane in a gitignored path, (d) optionally trim the generated `SKILL.md` frontmatter if lanes are consumed as reference folders rather than auto-loaded skills. No fork, no wrapper script required to start.

**Decision chain unblocked:** #151 → purchase the six books in **EPUB (DRM-free)**, PDF fallback.
