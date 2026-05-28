"""Judge layer — control-plane interceptor for production agents.

Council Gap-Fill 1 (2026-05-16) ships this as a Pydantic-typed interceptor
that sits between an agent's intent and its action. Maps verbatim to the
Anthropic FDE Boston JD's "control architectures around production agent
deployments" line, and to Nate B Jones §3.5 "Judge Layer / Actor-Judge
separation / 4 outcomes" (one extra outcome — JUDGE_UNAVAILABLE — turns the
judge's own absence into a named, observable state instead of a silent
exception).

Architecture (council-locked 2026-05-16):
  - Pydantic ActionProposal schema (8 fields) — the demo phrase.
  - YAML policy files at agents-sdk/policies/<agent_name>.yaml — declarative
    rules a recruiter can read without reading Python.
  - Local-model evaluator (gemma4:e4b on Mac Mini Ollama via HybridRouter
    "judge_layer" profile) → $0 per decision.
  - JSONL ledger at vault/health/judge_log/<YYYY-MM-DD>.jsonl — append-only,
    consumed by the Fleet Observability Dashboard (Task 11).
  - Fail-open: any router failure / parse failure / timeout returns
    Outcome.JUDGE_UNAVAILABLE with a Pushover alert. Cadence preservation
    wins over theoretical bypass risk because Sean's manual publish gate
    remains the Tier-A canonical control — the judge is defense-in-depth,
    not the only review surface.

Wrap target (Phase 1): Substack-Drafter (agents-sdk/agents/substack_drafter.py).
Expansion candidates (Phase 2+): Daily Driver, Job Feed, Vault Synthesizer,
and a future "vault-to-build" agent — all additive policy YAML +
ActionProposal subclasses, no module rewrites.

Public surface (this module):
  - ActionProposal, JudgeDecision, Outcome  (from .schema)
"""

from __future__ import annotations

from lib.judge.schema import (
    ActionProposal,
    JudgeDecision,
    Outcome,
)

__all__ = [
    "ActionProposal",
    "JudgeDecision",
    "Outcome",
]
