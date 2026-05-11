"""Tests for config module."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from lib.config import load_config


class TestLoadConfig:
    def test_loads_config(self, tmp_config: Path):
        config = load_config(config_path=tmp_config)
        assert config.safety.max_turns_default == 10
        assert config.safety.max_budget_default == 0.25
        assert config.safety.permission_mode == "acceptEdits"
        assert config.log_level == "DEBUG"
        assert config.anthropic_api_key == "sk-ant-test-key-for-unit-tests"

    def test_agent_config(self, tmp_config: Path):
        config = load_config(config_path=tmp_config)
        daily = config.agent_config("daily_driver")
        assert daily.enabled is True
        assert daily.skills == ["test-skill", "another-skill"]

    def test_disabled_agent(self, tmp_config: Path):
        config = load_config(config_path=tmp_config)
        spending = config.agent_config("spending_analysis")
        assert spending.enabled is False

    def test_unknown_agent(self, tmp_config: Path):
        config = load_config(config_path=tmp_config)
        unknown = config.agent_config("nonexistent")
        assert unknown.enabled is False
        assert unknown.skills == []

    def test_missing_api_key_is_none(self, tmp_config: Path):
        # API key is optional — falls back to CLI auth
        old_key = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            config = load_config(config_path=tmp_config)
            assert config.anthropic_api_key is None
        finally:
            if old_key:
                os.environ["ANTHROPIC_API_KEY"] = old_key

    def test_missing_config_raises(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            load_config(config_path=tmp_path / "nonexistent.toml")


class TestLoadLogging:
    def test_log_dir_from_config(self, tmp_config: Path, tmp_vault: Path):
        config = load_config(config_path=tmp_config)
        assert config.log_dir == tmp_vault / "90_system" / "agent-logs"


class TestJobFeedConfig:
    def test_job_feed_config_loads(self):
        cfg = load_config()
        jf = cfg.agents.get("job_feed", {})
        assert jf.get("enabled") is True
        assert jf.get("max_cost_usd") == 0.10
        assert jf.get("fallback_disabled") is True
        assert jf.get("fetch_skip_if_within_hours") == 4
        assert jf.get("mbp_probe_url", "").startswith("http://")
        paths = jf.get("paths", {})
        assert paths.get("db") == "vault/.job-feed.db"
        assert paths.get("watchlist", "").endswith("watchlist.yaml")
        assert paths.get("roll_up_dir", "").endswith("job-feed")
        assert paths.get("manifest_dir") == "vault/health"
