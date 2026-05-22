from datetime import datetime
from pathlib import Path

import pytest

from lib.fleet_summary import build_fleet_overnight_digest, AGENT_ORDER, AGENT_DISPLAY


def test_agent_order_includes_vault_critic_after_deep_researcher():
    """vault_critic runs after deep_researcher (03:30 vs 02:45) and the
    display order should reflect the schedule sequence."""
    assert "vault-critic" in AGENT_ORDER
    dr_idx = AGENT_ORDER.index("deep-researcher")
    vc_idx = AGENT_ORDER.index("vault-critic")
    assert vc_idx > dr_idx


def test_agent_display_has_vault_critic_label():
    assert AGENT_DISPLAY["vault-critic"] == "Vault Critic"


def test_fleet_digest_renders_vault_critic_line(tmp_path):
    """When a vault-critic run is present in agent-run-history.csv, the
    digest names it explicitly."""
    repo_root = tmp_path
    csv = repo_root / "vault" / "90_system" / "agent-logs" / "agent-run-history.csv"
    csv.parent.mkdir(parents=True)
    csv.write_text(
        "date,time,agent,mode,status,cost_usd,duration_ms,turns,notes\n"
        "2026-05-22,03:30:01,vault-critic,,success,0.0000,180000,,"
        "status=ok articles=2 codex_fail=0 ag_fail=0\n"
    )
    vault_root = repo_root / "vault"
    digest = build_fleet_overnight_digest(
        repo_root=repo_root,
        vault_root=vault_root,
        now=datetime.fromisoformat("2026-05-22T08:30:00"),
    )
    assert "Vault Critic" in digest
