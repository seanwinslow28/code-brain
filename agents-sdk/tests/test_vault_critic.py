import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
import yaml

from lib.cli_runners import CLIResponse

from agents.vault_critic import (
    AGENT_NAME,
    critique_one_article,
    CritiqueResult,
    format_expansion_body,
    STATUS_ERROR,
    STATUS_OK,
    STATUS_PARTIAL,
    STATUS_SUCCESS_EMPTY,
    write_critic_manifest,
)
from agents.vault_critic import run as run_critic


@pytest.fixture
def tmp_repo(tmp_path):
    (tmp_path / "vault" / "health").mkdir(parents=True)
    return tmp_path


def test_agent_name_constant():
    # Must match the launchd plist label + record_run CSV value.
    assert AGENT_NAME == "vault-critic"


def test_critique_result_defaults():
    r = CritiqueResult(status=STATUS_OK, run_id="2026-05-22T03:30:00")
    assert r.articles_critiqued == 0
    assert r.codex_calls == 0
    assert r.codex_failures == 0
    assert r.expansions_written == []


def test_write_critic_manifest_round_trip(tmp_repo):
    r = CritiqueResult(
        status=STATUS_OK,
        run_id="2026-05-22T03:30:00",
        articles_critiqued=2,
        codex_calls=2, codex_failures=0, codex_tokens_total=34000,
        antigravity_calls=2, antigravity_failures=0, antigravity_tokens_total=31000,
        duration_seconds=180.5,
        expansions_written=[
            "vault/knowledge/expansions/foo.md",
            "vault/knowledge/expansions/bar.md",
        ],
    )
    path = write_critic_manifest(repo_root=tmp_repo, result=r, today="2026-05-22")
    assert path.name == "critic-manifest-2026-05-22.json"
    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == STATUS_OK
    assert payload["articles_critiqued"] == 2
    assert payload["expansions_written"] == [
        "vault/knowledge/expansions/foo.md",
        "vault/knowledge/expansions/bar.md",
    ]
    assert payload["duration_seconds"] == 180.5


def test_write_critic_manifest_atomic_via_tmp_rename(tmp_repo):
    r = CritiqueResult(status=STATUS_SUCCESS_EMPTY, run_id="x")
    path = write_critic_manifest(repo_root=tmp_repo, result=r, today="2026-05-22")
    # No leftover .tmp file
    assert not path.with_suffix(path.suffix + ".tmp").exists()


def test_write_critic_manifest_rejects_invalid_status(tmp_repo):
    r = CritiqueResult(status="sucess-empty", run_id="x")  # typo
    with pytest.raises(ValueError, match="Invalid status"):
        write_critic_manifest(repo_root=tmp_repo, result=r, today="2026-05-22")


def test_write_critic_manifest_rejects_empty_run_id(tmp_repo):
    r = CritiqueResult(status=STATUS_OK, run_id="")
    with pytest.raises(ValueError, match="run_id must be non-empty"):
        write_critic_manifest(repo_root=tmp_repo, result=r, today="2026-05-22")


def test_format_expansion_body_both_clis_succeeded():
    body = format_expansion_body(
        original_title="Writing Voice Modes",
        original_slug="writing-voice-modes",
        codex_text="1. Forensic Moral Essayist — Joan Didion ...",
        antigravity_text="### 1. Surgical Cultural Synthesis ...",
        today="2026-05-22",
        codex_failed=False,
        antigravity_failed=False,
    )
    assert body.startswith("---\n")
    assert 'title: "How to make `Writing Voice Modes` better"\n' in body
    assert 'type: expansion\n' in body
    assert 'parent: "[[writing-voice-modes]]"\n' in body
    assert '- codex (gpt-5.5)' in body
    assert '- anti-gravity (gemini-3.1-pro-preview)' in body
    assert "## From Codex (gpt-5.5)" in body
    assert "## From Anti-Gravity (Gemini 3)" in body
    assert "1. Forensic Moral Essayist" in body
    assert "Surgical Cultural Synthesis" in body


def test_format_expansion_body_one_cli_failed_renders_status_marker():
    body = format_expansion_body(
        original_title="X",
        original_slug="x",
        codex_text="codex response",
        antigravity_text="",
        today="2026-05-22",
        codex_failed=False,
        antigravity_failed=True,
    )
    assert "codex response" in body
    assert "_Anti-Gravity rate-capped or failed; no critique this run._" in body


def test_format_expansion_body_includes_required_wikilink():
    """Per validator pattern: every expansion file must contain >=1 wikilink
    so it isn't orphaned in vault/knowledge/index.md downstream."""
    body = format_expansion_body(
        original_title="X", original_slug="x",
        codex_text="text", antigravity_text="text",
        today="2026-05-22",
        codex_failed=False, antigravity_failed=False,
    )
    assert "[[x]]" in body


def test_format_expansion_body_escapes_double_quote_in_title():
    """If the synthesizer ever produces a concept title containing a literal
    double-quote, the YAML frontmatter must remain well-formed."""
    body = format_expansion_body(
        original_title='My "Quoted" Title',
        original_slug="my-quoted-title",
        codex_text="x", antigravity_text="x",
        today="2026-05-22",
        codex_failed=False, antigravity_failed=False,
    )
    # The escaped quotes must appear in the YAML title; verify the line is
    # parseable as YAML.
    head_end = body.find("---", 4)  # second --- (frontmatter close)
    frontmatter = body[3:head_end]   # between the two ---
    parsed = yaml.safe_load(frontmatter)
    assert parsed["title"] == 'How to make `My "Quoted" Title` better'


# ---------------------------------------------------------------------------
# D3: critique_one_article — parallel fan-out + isolation
# ---------------------------------------------------------------------------

CONCEPT_BODY = """\
---
title: "Writing Voice Modes"
type: concept
sources:
  - .claude/skills/writing-voice-modes/SKILL.md
---

## Definition

Five voice modes plus Sean Mode.

## Related Concepts

[[creative-writing]] [[blog-cadence]]
"""


@pytest.fixture
def tmp_concept(tmp_path):
    (tmp_path / "vault" / "knowledge" / "concepts").mkdir(parents=True)
    (tmp_path / "vault" / "knowledge" / "expansions").mkdir(parents=True)
    p = tmp_path / "vault" / "knowledge" / "concepts" / "writing-voice-modes.md"
    p.write_text(CONCEPT_BODY, encoding="utf-8")
    return tmp_path, p


def _ok(cli: str, text: str, tokens: int) -> CLIResponse:
    return CLIResponse(
        cli=cli, text=text, tokens=tokens,
        duration_s=10.0, exit_code=0, rate_capped=False, error=None,
    )


def _fail(cli: str, error: str) -> CLIResponse:
    return CLIResponse(
        cli=cli, text="", tokens=None,
        duration_s=0.5, exit_code=1, rate_capped=False, error=error,
    )


def _capped(cli: str) -> CLIResponse:
    return CLIResponse(
        cli=cli, text="", tokens=None,
        duration_s=0.5, exit_code=0, rate_capped=True, error=None,
    )


def test_critique_one_article_both_clis_succeed(tmp_concept):
    repo_root, concept_path = tmp_concept

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_ok("codex", "codex content", 17000))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_ok("antigravity", "gemini content", 15000))):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=["other-concept"],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path.name == "writing-voice-modes.md"
    assert expansion_path.parent.name == "expansions"
    assert expansion_path.exists()
    body = expansion_path.read_text(encoding="utf-8")
    assert "codex content" in body
    assert "gemini content" in body
    assert codex_resp.ok and ag_resp.ok


def test_critique_one_article_codex_capped_writes_antigravity_only(tmp_concept):
    repo_root, concept_path = tmp_concept

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_capped("codex"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_ok("antigravity", "gemini survived", 15000))):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=[],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path.exists()
    body = expansion_path.read_text(encoding="utf-8")
    assert "Codex rate-capped or failed" in body
    assert "gemini survived" in body
    assert codex_resp.rate_capped is True
    assert ag_resp.ok is True


def test_critique_one_article_both_fail_returns_none_path(tmp_concept):
    """If BOTH CLIs fail, do not write a useless expansion file — return None.
    The caller increments failure counts and marks the run partial."""
    repo_root, concept_path = tmp_concept

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_fail("codex", "boom"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_fail("antigravity", "boom"))):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=[],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path is None
    assert not codex_resp.ok and not ag_resp.ok


# ---------------------------------------------------------------------------
# D4: smoke-fixture replay — regression test against future CLI output drift
# ---------------------------------------------------------------------------

SMOKE_FIXTURES = Path(__file__).parent / "fixtures" / "critic"


def test_smoke_fixtures_replay_produces_expected_expansion_shape(tmp_concept):
    """Replay the persisted smoke-test outputs as subprocess stand-ins;
    assert the formatter produces an expansion file containing the verbatim
    headline recommendations from both CLIs. This is the regression test
    against future CLI output drift."""
    repo_root, concept_path = tmp_concept
    codex_stdout = (SMOKE_FIXTURES / "codex-out.txt").read_text(encoding="utf-8")
    gemini_payload = json.loads((SMOKE_FIXTURES / "gemini-out.json").read_text(encoding="utf-8"))
    gemini_response = gemini_payload["response"]

    async def go():
        codex_resp = _ok("codex", codex_stdout, 17182)
        ag_resp = _ok("antigravity", gemini_response, 15746)
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=codex_resp)), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=ag_resp)):
            return await critique_one_article(
                repo_root=repo_root,
                article_path=concept_path,
                recent_titles=[],
                today="2026-05-22",
                per_cli_timeout_s=60,
            )

    expansion_path, codex_resp, ag_resp = asyncio.run(go())
    assert expansion_path is not None
    body = expansion_path.read_text(encoding="utf-8")

    # Both Codex headline recommendations are present byte-for-byte.
    assert "Forensic Moral Essayist" in body
    assert "Architectural Systems Narrator" in body
    assert "Intimate Intellectual Pressure" in body

    # All three Anti-Gravity headline recommendations are present byte-for-byte.
    assert "Surgical Cultural Synthesis" in body
    assert "Escalating Moral Architecture" in body
    assert "Techno-Dialectical Aphorist" in body

    # The convergence signal (Didion in both) is preserved.
    assert body.count("Didion") >= 2


# ---------------------------------------------------------------------------
# D5: run() orchestrator + wall-clock budget
# ---------------------------------------------------------------------------


def _make_concept_at(vault_root: Path, slug: str) -> Path:
    p = vault_root / "vault" / "knowledge" / "concepts" / f"{slug}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'---\ntitle: "{slug}"\ntype: concept\n---\n\nbody [[wiki]]\n',
        encoding="utf-8",
    )
    return p


def _make_manifest(vault_root: Path, today_iso: str, **kwargs):
    (vault_root / "vault" / "health").mkdir(parents=True, exist_ok=True)
    (vault_root / "vault" / "health" / f"synth-manifest-{today_iso}.json").write_text(
        json.dumps({"status": "ok", "concepts_written": 2, **kwargs}),
        encoding="utf-8",
    )


def test_run_writes_manifest_when_no_synth_manifest_today(tmp_repo):
    """The 2026-05-15 MBP-offline canonical case: synthesizer didn't run.
    Agent exits cleanly with status=success-empty manifest. NOT status=error."""

    async def go():
        return await run_critic(
            repo_root=tmp_repo,
            date_iso="2026-05-22",
            max_targets=3,
            wall_budget_s=600,
        )

    result = asyncio.run(go())
    assert result.status == STATUS_SUCCESS_EMPTY
    assert result.articles_critiqued == 0

    manifest = tmp_repo / "vault" / "health" / "critic-manifest-2026-05-22.json"
    assert manifest.exists()


def test_run_codex_rate_capped_marks_partial_status(tmp_repo, monkeypatch):
    today = "2026-05-22"
    p = _make_concept_at(tmp_repo, "writing-voice-modes")
    _make_manifest(tmp_repo, today)

    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: [p])

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_capped("codex"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_ok("antigravity", "gem", 15000))):
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=600,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_PARTIAL
    assert result.articles_critiqued == 1   # the file WAS written (anti-gravity survived)
    assert result.codex_failures == 1
    assert result.antigravity_failures == 0
    expansion = tmp_repo / "vault" / "knowledge" / "expansions" / "writing-voice-modes.md"
    assert expansion.exists()


def test_run_both_clis_fail_for_every_article_marks_error(tmp_repo, monkeypatch):
    today = "2026-05-22"
    p = _make_concept_at(tmp_repo, "x")
    _make_manifest(tmp_repo, today)

    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: [p])

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(return_value=_fail("codex", "boom"))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(return_value=_fail("antigravity", "boom"))):
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=600,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_ERROR
    assert result.articles_critiqued == 0
    assert result.codex_failures == 1
    assert result.antigravity_failures == 1


def test_run_succeeds_with_three_articles(tmp_repo, monkeypatch):
    today = "2026-05-22"
    paths = [_make_concept_at(tmp_repo, slug) for slug in ("a", "b", "c")]
    _make_manifest(tmp_repo, today)
    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: paths)

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(side_effect=lambda *a, **k: _ok("codex", "ok", 100))), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(side_effect=lambda *a, **k: _ok("antigravity", "ok", 100))):
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=600,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_OK
    assert result.articles_critiqued == 3


def test_run_respects_wall_budget(tmp_repo, monkeypatch):
    """When wall_budget_s is exceeded mid-loop, mark partial and skip remaining."""
    today = "2026-05-22"
    paths = [_make_concept_at(tmp_repo, slug) for slug in ("a", "b", "c")]
    _make_manifest(tmp_repo, today)
    monkeypatch.setattr("agents.vault_critic.select_target_articles",
                        lambda root, date_iso, max_targets: paths)

    async def slow_cli(*args, **kwargs):
        await asyncio.sleep(0.2)
        return _ok("codex", "ok", 100)

    async def go():
        with patch("agents.vault_critic.run_codex", AsyncMock(side_effect=slow_cli)), \
             patch("agents.vault_critic.run_antigravity", AsyncMock(side_effect=slow_cli)):
            # 0.3s budget — first article should land; second/third should be skipped.
            return await run_critic(
                repo_root=tmp_repo,
                date_iso=today,
                max_targets=3,
                wall_budget_s=0.3,
            )

    result = asyncio.run(go())
    assert result.status == STATUS_PARTIAL
    assert result.articles_critiqued <= 2
    assert any("budget" in w.lower() for w in result.warnings)
