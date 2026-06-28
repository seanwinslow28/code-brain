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
