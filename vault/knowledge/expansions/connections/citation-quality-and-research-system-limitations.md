---
title: "How to make `Citation Quality and Research System Limitations` better"
type: expansion
parent: "[[citation-quality-and-research-system-limitations]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-12
updated: 2026-06-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[citation-quality-and-research-system-limitations]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “AIS claim ledger,” anchored on Hannah Rashkin et al., _Measuring Attribution in Natural Language Generation Models_**
   
   Add the missing unit of analysis: not “does Gemini cite better than LDR?” but “is each generated claim attributable to an identified source?” Rashkin et al.’s AIS framework gives Sean a cleaner standard than vendor trust: every claim gets `supported / unsupported / ambiguous`, source ID, quoted evidence, and reviewer note.

   Sentence pattern: “For every research output, decompose the prose into atomic external-world claims; score each claim for attribution before accepting the synthesis.”

   This unlocks an **executable citation QA harness** for `vault_critic` or Gemini DR outputs: a SQLite-backed “claim ledger” that can produce a portfolio artifact called “How I Audit Agent Research.” Source: [AIS paper](https://arxiv.org/abs/2112.12870).

2. **Add “lateral-reading gate,” anchored on Sam Wineburg + Mike Caulfield, _Verified: How to Think Straight, Get Duped Less, and Make Better Decisions About What to Believe Online_**
   
   The concept currently treats citation quality as a source-linking problem. Missing: source *reputation* and network position. Wineburg/Caulfield’s SIFT/lateral-reading pattern says: leave the page, inspect the publisher/author elsewhere, find better coverage, then return.

   Sentence pattern: “A citation is not accepted until one independent source has validated the cited source’s authority, conflict position, or original-data proximity.”

   This unlocks a **research-routing runbook**: LDR can handle single-shape questions only if the lateral-reading gate passes; Gemini DR is required when source identity, incentives, or provenance are contested. It also gives Sean a stronger Substack essay: “Why Deep Research Needs Source Vetting, Not Just More Sources.” Source context: [Wineburg profile / _Verified_ reference](https://en.wikipedia.org/wiki/Sam_Wineburg).

3. **Add “RARR repair loop,” anchored on Luyu Gao et al., _RARR: Researching and Revising What Language Models Say_**
   
   The current concept jumps from “LDR fails” to “use Gemini DR.” Missing: a post-generation repair architecture. RARR separates generation from attribution and revision: take an existing answer, search for support, then minimally rewrite unsupported claims.

   Sentence pattern: “Do not regenerate the whole research note when citations fail; preserve the useful draft, attach evidence, and surgically revise only unsupported claims.”

   This unlocks an **agent spec** for `citation_repair_agent.py`: input any vault article, extract claims, retrieve sources, mark unsupported claims, patch the article, and emit a before/after manifest. That is more portfolio-grade than “we route hard research to Gemini.” Source: [RARR paper](https://arxiv.org/abs/2210.08726).

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
