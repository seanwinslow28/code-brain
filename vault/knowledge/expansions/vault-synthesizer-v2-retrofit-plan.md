---
title: "How to make `Vault Synthesizer v2 retrofit plan` better"
type: expansion
parent: "[[vault-synthesizer-v2-retrofit-plan]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-03
updated: 2026-07-03
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[vault-synthesizer-v2-retrofit-plan]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “negative-control retrieval” as a required eval mode**
   - **What to add:** A synthesizer tier that deliberately injects plausible-but-wrong neighbors and measures whether the agent refuses bad bridges. Current plan optimizes for “cross-domain insight,” but not for *anti-insight*: resisting seductive false connections.
   - **Anchor work:** Nicholas Carlini et al., “Poisoning Web-Scale Training Datasets is Practical” and Anthropic’s “Sleeper Agents” paper. Use them as the adversarial frame: not “is retrieval relevant?” but “can irrelevant or malicious context bend synthesis?”
   - **Unlocks:** An executable eval artifact: `evals/vault-synthesizer/negative-controls/`. Sean could ship a portfolio one-pager showing agent-governance maturity: “My knowledge loop has adversarial controls, not just summarization metrics.” This is a stronger AI-PM signal than another RAG retrofit note.

2. **Add “progressive summarization with preserved source grain”**
   - **What to add:** A constraint that every synthesized concept must retain multiple compression layers: raw quote, local paraphrase, cross-domain claim, and reusable principle. Right now the concept jumps from evidence to definition too quickly, which risks making the vault sound confident but thin.
   - **Anchor work:** Tiago Forte, *Building a Second Brain*, specifically his “Progressive Summarization” method; pair it with Andy Matuschak’s evergreen note style from “Evergreen notes should be atomic.”
   - **Unlocks:** A stronger vault note template and Substack pipeline. Sean could produce essays where the argument visibly climbs from artifact to principle instead of reading like an auto-generated glossary. Artifact: `tpl-concept-progressive.md` plus a “source grain checklist” for the synthesizer.

3. **Add “productive contradiction” as a first-class output, not a lint issue**
   - **What to add:** A mode where the synthesizer must identify unresolved tensions and preserve them as named dialectics: “local-first cost discipline vs citation quality,” “autonomy vs auditability,” “cross-domain bridging vs false analogy.” Don’t just connect concepts; make the conflict durable.
   - **Anchor work:** Christopher Alexander, *Notes on the Synthesis of Form*, especially the idea that design advances by resolving misfits; also Donald Schön, *The Reflective Practitioner*, for reflection-in-action under uncertainty.
   - **Unlocks:** Better decision records and sharper agent specs. Instead of “Vault Synthesizer v2 improves cross-domain insight,” Sean can ship ADRs that say: “This system exists to manage these named tensions.” That is closer to senior IC architecture writing and less like a knowledge-base summary.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
