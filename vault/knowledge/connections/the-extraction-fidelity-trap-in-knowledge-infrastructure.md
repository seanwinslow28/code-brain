---
title: "The Extraction Fidelity Trap in Knowledge Infrastructure"
type: connection
connects:
  - The Illusion of Competence in Automated Systems
  - Tacit Knowledge Erosion vs. Automation Scale
  - Legibility Debt as a Supervision Failure Mode
created: 2026-08-31
updated: 2026-08-31
---

## Synthesis

There is a critical tension between the operational reliability of automated extraction tools and the semantic completeness of the resulting knowledge base. Tools like book-to-skill offer deterministic, fast extraction that feels robust, yet they silently discard non-textual data (figures, diagrams) that often contains the core intellectual value. This creates a 'fidelity trap' where Sean's infrastructure appears healthy and complete, but is actually missing the very elements that distinguish deep expertise from surface-level summary. The consequence is that his knowledge vault becomes a collection of accurate but hollowed-out artifacts, undermining the depth required for high-stakes creative or professional work.

## Threads

### [[The Illusion of Competence in Automated Systems]]

> One caveat either way: figures/diagrams are never extracted (text baked into images is lost, by design), and scanned PDFs hard-abort with an "OCR first" message.

### [[Tacit Knowledge Erosion vs. Automation Scale]]

> The output is not a summary; the spec explicitly extracts *structure*: named frameworks ("preserve the author's exact naming"), decision rules, techniques, anti-patterns, glossary terms

### [[Legibility Debt as a Supervision Failure Mode]]

> EPUB is reflowable HTML inside a zip: no page headers/footers to strip, no scanned-page risk, and chapter boundaries survive extraction (their Moby-Dick EPUB test auto-detected all 133 chapters via its ToC).

## Implications

- Sean must implement manual verification steps for any automated ingestion pipeline to detect missing visual or structural data.
- The choice of input format (EPUB vs PDF) becomes a strategic decision about what types of knowledge are preserved versus lost.
