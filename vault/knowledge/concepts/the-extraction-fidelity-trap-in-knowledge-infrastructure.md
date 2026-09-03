---
title: "The Extraction Fidelity Trap in Knowledge Infrastructure"
type: concept
sources:
  - knowledge/connections/cross-domain-tension-automation-velocity-vs-semantic-integrity-in-knowledge-and-career-systems.md
tags: [auto-generated, phase-6]
created: 2026-09-03
updated: 2026-09-03
---

## Definition

This mechanism describes a structural asymmetry where automated ingestion pipelines prioritize text-based semantic extraction while systematically discarding non-textual data modalities such as visual diagrams, spatial layouts, and embedded image content. The system creates an illusion of completeness by processing the available text, but the resulting knowledge graph is fundamentally incomplete because the 'baked-in' visual context is lost by design during the OCR or parsing phase. This leads to a silent decay in semantic integrity where the agent fleet operates on a degraded representation of the source material without any operational visibility into what was omitted.

## Context

Sean's vault synthesizer relies on automated fleets to ingest books and articles; if these tools silently discard visual frameworks or diagrams, his 'taste memory' and strategic insights derived from those visuals are permanently lost to the graph, creating a hollowed-out knowledge base that supports operational tasks but fails high-level creative synthesis.

## Evidence

> figures/diagrams are never extracted (text baked into images is lost, by design), and scanned PDFs hard-abort with an 'OCR first' message.

> The output is not a summary; the spec explicitly extracts *structure*: named frameworks ('preserve the author's exact naming'), decision rules, techniques, anti-patterns, glossary terms

## Examples

- A book containing a critical architectural diagram where the text description is insufficient to reconstruct the logic, resulting in a concept entry that lacks the core visual insight.
- Scanned PDFs triggering hard-aborts that prevent ingestion entirely, forcing manual intervention or loss of the source material from the automated pipeline.

## Related Concepts

[[Tacit Knowledge Erosion vs. Automation Scale]] [[The Illusion of Competence in Automated Systems]]
