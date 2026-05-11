---
title: "writing-voice-modes"
type: concept
status: active
domain: [creative-studio, life-systems]
tags: [writing, voice, tone, creative-tools]
created: 2026-05-11
last-updated: 2026-05-11
source-skill: ".claude/skills/writing-voice-modes/SKILL.md"
ai-context: "Vault hub for the writing-voice-modes concept — five calibrated voice modes Sean uses across long-form writing, substack drafts, and creative work. Referenced from job-hunt operating-model artifacts as a Track-A capability."
---

# writing-voice-modes

**Writing voice modes** is Sean's five-mode tone-calibration system for long-form writing. Each mode is anchored to a known author's voice so the model has a concrete reference instead of vague instructions like "make it engaging." The modes:

1. **Domestic Observer** (David Sedaris) — small-scale, family-and-routine, dry first-person comic observation.
2. **Gonzo Technical** (Hunter S. Thompson) — first-person, opinionated, technically literate, conversational without being casual.
3. **Beat Flow** (Jack Kerouac) — momentum-driven, long sentences, breath-paced, sensory and rhythmic.
4. **Plain Direct** (George Orwell) — short sentences, concrete nouns, ruthless cuts, no metaphor unless it earns its keep.
5. **Critical-Theory Lyrical** (a hybrid of late-Sontag + Didion) — long-sentence reflective analysis, ideas grounded in specific scenes.

## Why this hub exists

The `vault/05_atlas/operating-models/job-hunt-2026/operating-model.md` artifact references `[[writing-voice-modes]]` as a Track-A capability (writing → substack drafts → portfolio artifacts → job-hunt evidence). This file is the canonical wiki target so the reference resolves and the synthesizer can cluster writing-related material together.

## Source skill

The Claude Code skill that operationalizes this concept lives at [`.claude/skills/writing-voice-modes/SKILL.md`](../../.claude/skills/writing-voice-modes/SKILL.md). The skill gives the model the full mode-by-mode rubric, prompts the user to pick a mode, and applies the corresponding rules to the draft.

## When to use which mode

- **Substack drafts about life or layoff** → Domestic Observer or Beat Flow
- **Technical deep-dives (e.g. the fleet architecture)** → Gonzo Technical
- **PM portfolio case studies** → Plain Direct
- **Reflective essays / culture writing** → Critical-Theory Lyrical

The skill itself contains the operational rules; this hub exists as a wiki anchor.
