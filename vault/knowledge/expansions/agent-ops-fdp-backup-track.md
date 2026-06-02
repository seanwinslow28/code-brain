---
title: "How to make `Agent Ops / FDP Backup Track` better"
type: expansion
parent: "[[agent-ops-fdp-backup-track]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-02
updated: 2026-06-02
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agent-ops-fdp-backup-track]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Incident Command as Agent-Ops Career Track”**
   - **What to add:** A concrete ops-mode distinction: *fleet operator as incident commander*, not “backup support.” Define severity levels, escalation paths, rollback authority, comms cadence, and post-incident learning loops for agent fleets.
   - **Anchor:** John Allspaw, **“Blameless PostMortems and a Just Culture”**; plus Google SRE book, **Chapter 14: “Managing Incidents.”**
   - **Unlocks:** This turns the concept into a **portfolio runbook**: “Agent Fleet Incident Command for Personal AI Systems.” Sean can show how his daily-driver/meta-agent/critic stack handles failed schedules, partial outputs, rate caps, vault corruption risk, and human escalation. Current article sounds like a vague job track; this would make it a credible operational discipline.

2. **Add “Control Plane / Data Plane Split for Agent Fleets”**
   - **What to add:** A systems architecture facet: distinguish the *control plane* that schedules, routes, authorizes, observes, and halts agents from the *data plane* where agents actually read/write vault artifacts, run research, generate summaries, or mutate files.
   - **Anchor:** Brendan Burns, **“Designing Distributed Systems”**, especially the reusable patterns around sidecars, adapters, ambassadors, and control loops; optionally Kubernetes’ own controller pattern via **“Kubernetes: Up and Running”** by Burns, Beda, and Hightower.
   - **Unlocks:** This gives Sean language for an **agent-ops architecture diagram** and an **IC interview whiteboard artifact**. Instead of saying “I run scheduled agents,” he can say: “I built a local agent control plane over launchd, file manifests, cost caps, health checks, and Obsidian-Git boundaries.” That is much stronger for AI-PM and agentic-engineering roles.

3. **Add “Resilience Engineering: Work-as-Imagined vs Work-as-Done”**
   - **What to add:** A contradicting framework to the current “fleet management” phrasing: agent ops is not just keeping agents green; it is detecting when the designed workflow and the real workflow diverge. Add a section on drift, hidden coupling, brittle handoffs, and how operators learn from near-misses.
   - **Anchor:** Erik Hollnagel, **“Safety-I and Safety-II”**; also Sidney Dekker, **“The Field Guide to Understanding Human Error.”**
   - **Unlocks:** This enables a **Substack essay** or **decision record** titled something like “My Agents Don’t Fail Like Software, They Fail Like Organizations.” Sean can use real incidents: Obsidian-Git ownership, launchd PATH failures, daily-note race conditions, local LDR citation collapse. Current concept cannot reach that level; it is descriptive, while this frame produces generative critique and sharper career signal.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
