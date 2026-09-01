---
title: "The Extraction Fidelity Trap in Knowledge Infrastructure"
type: concept
sources:
  - knowledge/connections/the-extraction-fidelity-trap-in-knowledge-infrastructure.md
tags: [auto-generated, phase-6]
created: 2026-09-01
updated: 2026-09-01
---

## Definition

This mechanism describes a systemic risk where automated ingestion pipelines prioritize operational reliability and semantic completeness over structural fidelity, resulting in the silent loss of non-textual intellectual assets. The system creates an illusion of health by successfully parsing text-based structures while discarding figures, diagrams, or scanned content that contain core expertise. This leads to a knowledge base that is technically accurate but semantically hollowed out, undermining the depth required for high-stakes creative or professional work because the infrastructure cannot distinguish between surface-level summary and deep structural insight.

## Context

Sean's vault synthesizer relies on tools like book-to-skill which hard-abort on scanned PDFs and ignore figures in EPUBs. This creates a blind spot where his knowledge base appears robust but lacks the visual or structural data that distinguishes deep expertise from surface-level summary, directly impacting the quality of his creative output and professional positioning.

## Evidence

> One caveat either way: figures/diagrams are never extracted (text baked into images is lost, by design), and scanned PDFs hard-abort with an "OCR first" message.

> The output is not a summary; the spec explicitly extracts *structure*: named frameworks ("preserve the author's exact naming"), decision rules, techniques, anti-patterns, glossary terms

## Examples

- EPUB reflowable HTML inside a zip: no page headers/footers to strip, no scanned-page risk, and chapter boundaries survive extraction (their Moby-Dick EPUB test auto-detected all 133 chapters via its ToC).

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Tacit Knowledge Erosion vs. Automation Scale]]
