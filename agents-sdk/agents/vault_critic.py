#!/usr/bin/env python3
"""Vault Critic — nightly generative critique of synthesizer concept articles.

Runs on Mac Mini via launchd at 03:30 daily, after vault_synthesizer (02:30)
and deep_researcher (02:45). For each newly-written concept article from
today's synth-manifest (Mac-Mini-canonical, PR-contamination-filtered), fans
out two parallel subprocess critiques — Codex CLI (gpt-5.5) and Anti-Gravity
CLI (Gemini 3.1 Pro) — and writes a sibling expansion file at
vault/knowledge/expansions/{slug}.md plus a per-run manifest at
vault/health/critic-manifest-{date}.json.

Cost: $0 incremental on existing personal subscriptions. Sonnet fallback is
out of scope for v1; both-CLIs-rate-capped marks the run partial and exits
cleanly.

Schedule sequence:
    02:00  vault-indexer
    02:30  vault-synthesizer
    02:45  deep-researcher
    03:30  vault-critic        <- this agent
    08:30  daily-driver morning
    08:45  meta-agent
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

AGENT_NAME = "vault-critic"

STATUS_OK = "ok"
STATUS_PARTIAL = "partial"
STATUS_SUCCESS_EMPTY = "success-empty"
STATUS_ERROR = "error"
STATUS_VALUES = frozenset({STATUS_OK, STATUS_PARTIAL, STATUS_SUCCESS_EMPTY, STATUS_ERROR})

DEFAULT_MAX_TARGETS = 3
DEFAULT_WALL_BUDGET_S = 600
DEFAULT_PER_CLI_TIMEOUT_S = 120
RECENT_TITLES_CONTEXT_LIMIT = 30

EXPANSIONS_REL = "vault/knowledge/expansions"
HEALTH_REL = "vault/health"
KNOWLEDGE_INDEX_REL = "vault/knowledge/index.md"


@dataclass
class CritiqueResult:
    """Per-run summary written verbatim into critic-manifest-{date}.json."""
    status: str
    run_id: str
    articles_critiqued: int = 0
    codex_calls: int = 0
    codex_failures: int = 0
    codex_tokens_total: int = 0
    antigravity_calls: int = 0
    antigravity_failures: int = 0
    antigravity_tokens_total: int = 0
    duration_seconds: float = 0.0
    expansions_written: list[str] = field(default_factory=list)
    error: str = ""
    warnings: list[str] = field(default_factory=list)


def write_critic_manifest(
    *,
    repo_root: Path,
    result: CritiqueResult,
    today: str,
) -> Path:
    """Atomic write to vault/health/critic-manifest-{today}.json."""
    health = repo_root / HEALTH_REL
    health.mkdir(parents=True, exist_ok=True)
    path = health / f"critic-manifest-{today}.json"
    payload = {
        "run_id": result.run_id,
        "status": result.status,
        "articles_critiqued": result.articles_critiqued,
        "codex_calls": result.codex_calls,
        "codex_failures": result.codex_failures,
        "codex_tokens_total": result.codex_tokens_total,
        "antigravity_calls": result.antigravity_calls,
        "antigravity_failures": result.antigravity_failures,
        "antigravity_tokens_total": result.antigravity_tokens_total,
        "duration_seconds": round(result.duration_seconds, 2),
        "expansions_written": list(result.expansions_written),
        "warnings": list(result.warnings),
        "error": result.error,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
    return path
