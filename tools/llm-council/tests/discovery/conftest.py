"""Discovery-suite fixtures."""

import pytest


@pytest.fixture(autouse=True)
def _no_web_keys(monkeypatch):
    """Hermetic by default: the Stage-5 BACKFILL / web collector must never hit a real
    Exa/Brave endpoint during tests. With no key set, backfill degrades to "skipped" and
    collect_web returns []. Tests that exercise a provider inject search=/fetch= explicitly
    (or set the key + httpx_mock), which overrides this deletion within that test."""
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    yield


@pytest.fixture(autouse=True)
def _hermetic_sessions_dir(tmp_path, monkeypatch):
    """Persist-by-default (D3 Slice A) must never write into the real vault during tests:
    any test that omits sessions_dir resolves to a per-test tmp dir via the env override."""
    monkeypatch.setenv("DISCOVERY_SESSIONS_DIR", str(tmp_path / "hermetic-sessions"))
    yield
