---
title: "Two Audiences"
type: concept
sources:
  - 20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-06-11-readmes-voice-final.md
tags: [auto-generated, phase-6]
created: 2026-06-16
updated: 2026-06-16
---

## Definition

This mechanism describes the structural bifurcation of a single artifact into two distinct rhetorical registers based on the reader's cognitive load and intent. The first register, 'voice,' operates at high abstraction to signal strategic judgment and narrative coherence to recruiters who skim for pattern recognition. The second register, 'neutral body,' operates at low abstraction to provide verifiable technical depth for engineers who audit for implementation fidelity. The tension arises because optimizing one register often degrades the other; successful artifacts maintain a strict boundary where voice never contaminates technical precision, and technical detail never dilutes narrative clarity.

## Context

Sean is navigating a job hunt where he must simultaneously prove high-level product thinking (via README framing) and low-level engineering rigor (via code/infra). This concept explains why his '35% split dial' strategy works: it allocates cognitive bandwidth to the recruiter's first ten seconds without sacrificing the engineer's need for auditability.

## Evidence

> voice carries the one-liner / Problem / What-I-Learned (the recruiter's first ten seconds and the judgment signal); the technical body (install, API, config, tables) stays clean and neutral.

> Most agent failures aren't reasoning failures. They're intent failures. The spec is vague, the stop rules are missing, the outcome is an activity disguised as a state.

## Examples

- The README opener uses inversion ('Most agent failures...') to create narrative tension for the recruiter, while the subsequent technical sections use dry, imperative commands for the engineer.
- Em dashes are scrubbed from both registers to prevent 'dry wit' from bleeding into command syntax, ensuring the neutral body remains machine-readable and unambiguous.

## Related Concepts

[[Two Audiences]] [[Craft in Product Design]] [[Workbench Narrative]]
