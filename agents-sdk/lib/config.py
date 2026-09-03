"""Load configuration from config.toml and environment variables.

Local overrides (2026-09-03)
----------------------------
`config.toml` is TRACKED and public. Deploy-time state that must never enter
this repo — the claim-6 drill registration, whose `acknowledged_device` is a
personal device name — lives in a gitignored sibling `config.local.toml` that
is deep-merged OVER the tracked file by `load_raw_config()`.

This replaces three pieces of invisible local-only state that used to hold the
registration in a permanently dirty working tree: a `skip-worktree` mask on
`config.toml`, and the `.git/hooks/{pre-commit,post-merge}` guards that
existed to police it. The tracked config can now ship unarmed and committable
while the machine stays armed.

A malformed override raises rather than being skipped: an override silently
ignored is the exact failure mode this mechanism exists to end.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from dotenv import load_dotenv

CONFIG_PATH = Path(__file__).parent.parent / "config.toml"
ENV_PATH = Path(__file__).parent.parent.parent / ".env"


def local_config_path_for(config_path: Path) -> Path:
    """Return the `config.local.toml` sibling that overrides `config_path`.

    Derived from the given path rather than hardcoded so a test pointing at a
    tmp_path config never picks up the real machine's override.
    """
    return config_path.with_name(f"{config_path.stem}.local{config_path.suffix}")


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge `override` into `base`, returning a NEW dict.

    Nested tables merge key-by-key so an override may set a single key (e.g.
    `[agents.claim6_drill].schedule_enabled`) without restating its table.
    Non-table values — including lists — replace wholesale.
    """
    merged = dict(base)
    for key, value in override.items():
        existing = merged.get(key)
        if isinstance(value, dict) and isinstance(existing, dict):
            merged[key] = deep_merge(existing, value)
        else:
            merged[key] = value
    return merged


def load_raw_config(
    config_path: Path | None = None,
    *,
    local_path: Path | None = None,
) -> tuple[dict, Path | None]:
    """Load `config.toml` deep-merged under its `config.local.toml` sibling.

    Returns `(merged_mapping, applied_local_path_or_None)`. The second element
    is the provenance the callers surface so the override is never silent.

    Raises:
        FileNotFoundError: if `config_path` is missing.
        tomllib.TOMLDecodeError: if EITHER file is malformed. A broken override
            fails loud on purpose — see the module docstring.
    """
    config_path = config_path or CONFIG_PATH
    with open(config_path, "rb") as f:
        raw = tomllib.load(f)

    local_path = local_path or local_config_path_for(config_path)
    if not local_path.exists():
        return raw, None
    with open(local_path, "rb") as f:
        overrides = tomllib.load(f)
    return deep_merge(raw, overrides), local_path


@dataclass
class AgentConfig:
    """Configuration for a single agent."""

    enabled: bool = False
    skills: list[str] = field(default_factory=list)
    max_turns: int | None = None
    max_budget_usd: float | None = None


@dataclass
class SafetyConfig:
    """Global safety limits."""

    max_turns_default: int = 30
    max_budget_default: float = 0.50
    permission_mode: str = "acceptEdits"


@dataclass
class Config:
    """Top-level configuration."""

    repo_root: Path
    vault_root: Path
    skills_dir: Path
    life_systems_scripts: Path
    log_dir: Path
    log_level: str
    safety: SafetyConfig
    agents: dict[str, dict]
    anthropic_api_key: str | None
    artifacts: dict = field(default_factory=dict)
    fleet_memory: dict = field(default_factory=dict)
    portfolio: dict = field(default_factory=dict)
    # Provenance: the config.local.toml applied over config.toml, or None.
    # Surfaced by the meta-agent so a local override is never invisible.
    local_config_path: Path | None = None

    def agent_config(self, name: str) -> AgentConfig:
        """Get configuration for a named agent."""
        raw = self.agents.get(name, {})
        return AgentConfig(
            enabled=raw.get("enabled", False),
            skills=raw.get("skills", []),
            max_turns=raw.get("max_turns"),
            max_budget_usd=raw.get("max_budget_usd"),
        )

    def artifact_config(self, agent_name: str) -> dict:
        """Per-agent artifact config from [artifacts.per_agent.{agent_name}].

        Returns an empty dict when artifacts are globally disabled, missing,
        or when the agent has no per-agent entry.
        """
        if not self.artifacts.get("enabled", False):
            return {}
        return self.artifacts.get("per_agent", {}).get(agent_name, {})


def load_config(
    config_path: Path | None = None,
    env_path: Path | None = None,
) -> Config:
    """Load configuration from TOML file and environment.

    Args:
        config_path: Path to config.toml. Defaults to agents-sdk/config.toml.
        env_path: Path to .env file. Defaults to repo root .env.

    Returns:
        Populated Config dataclass, with `local_config_path` recording any
        `config.local.toml` override that was merged in.

    Raises:
        FileNotFoundError: If config.toml is missing.
    """
    config_path = config_path or CONFIG_PATH
    env_path = env_path or ENV_PATH

    # Load .env if it exists
    if env_path.exists():
        load_dotenv(env_path)

    # Load TOML, deep-merged under any gitignored config.local.toml sibling
    raw, applied_local = load_raw_config(config_path)

    paths = raw.get("paths", {})
    repo_root = Path(paths.get("repo_root", Path(__file__).parent.parent.parent))
    vault_root = Path(paths.get("vault_root", repo_root / "vault"))
    skills_dir = repo_root / paths.get("skills_dir", ".claude/skills")
    life_systems_scripts = repo_root / paths.get("life_systems_scripts", "life-systems/scripts")

    logging_cfg = raw.get("logging", {})
    log_dir = repo_root / logging_cfg.get("log_dir", "vault/90_system/agent-logs")
    log_level = logging_cfg.get("log_level", "INFO")

    safety_raw = raw.get("safety", {})
    safety = SafetyConfig(
        max_turns_default=safety_raw.get("max_turns_default", 30),
        max_budget_default=safety_raw.get("max_budget_default", 0.50),
        permission_mode=safety_raw.get("permission_mode", "acceptEdits"),
    )

    agents = raw.get("agents", {})
    artifacts = raw.get("artifacts", {})
    fleet_memory = raw.get("fleet_memory", {})
    portfolio = raw.get("portfolio", {})

    # API key is optional — if not set, the SDK falls back to
    # Claude Code CLI's existing auth (e.g., `claude login` OAuth)
    api_key = os.environ.get("ANTHROPIC_API_KEY") or None

    return Config(
        repo_root=repo_root,
        vault_root=vault_root,
        skills_dir=skills_dir,
        life_systems_scripts=life_systems_scripts,
        log_dir=log_dir,
        log_level=log_level,
        safety=safety,
        agents=agents,
        anthropic_api_key=api_key,
        artifacts=artifacts,
        fleet_memory=fleet_memory,
        portfolio=portfolio,
        local_config_path=applied_local,
    )
