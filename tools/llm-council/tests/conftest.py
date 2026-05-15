"""Shared pytest fixtures."""

import os
import json
from pathlib import Path

import pytest


@pytest.fixture
def fake_api_key(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-fake-for-tests")
    yield "sk-or-v1-fake-for-tests"


@pytest.fixture
def tmp_spend_dir(tmp_path, monkeypatch):
    spend_dir = tmp_path / "vault" / "health"
    spend_dir.mkdir(parents=True)
    monkeypatch.setenv("COUNCIL_SPEND_DIR", str(spend_dir))
    yield spend_dir
