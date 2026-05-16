---
name: MBP-awake scheduling for compute-heavy agents
description: Agents that depend on MBP-hosted Qwen3-14B (or any MBP-hosted compute) must NOT be scheduled overnight; schedule during waking hours when MBP is reliably awake
type: feedback
originSessionId: 1690f8b4-3f3b-48b0-8892-72839b84269d
---
Any agent that depends on MBP-hosted compute (Qwen3-14B for synthesis, scoring, or LLM tasks) must be scheduled during Sean's waking hours, not overnight.

**Why:** Overnight agents (2-3 AM) repeatedly fail because the MBP is asleep. The Vault Synthesizer (2:30 AM) is the canonical example — it succeeds only intermittently. Sean has explicitly hit this enough times to call it out as a pattern. He retired Wake-on-LAN in v3.14.3 rather than fight it.

**How to apply:** When scheduling a new SDK agent or launchd task that needs MBP compute, schedule it during Sean's waking hours (~7 AM – 10 PM ET, post-wake at 5:30 AM). Sean is willing to keep his MBP open and awake during the day, so anywhere in that window is fair game. If an agent's output needs to land in the 8:45 AM daily-driver morning brief, schedule it ~30-45 min before (e.g., 8:00 AM) — Sean's job-feed agent uses this exact pattern. Agents that run 100% on Mac Mini Ollama (e.g., gemma4:e4b, deep_researcher's Qwen3-14B GGUF on Mac Mini) are exempt — Mac Mini is always awake. The hard rule is just: **no overnight scheduling** for MBP-dependent agents.
