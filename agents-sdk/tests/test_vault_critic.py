import json
from pathlib import Path

import pytest

from agents.vault_critic import (
    AGENT_NAME,
    CritiqueResult,
    STATUS_ERROR,
    STATUS_OK,
    STATUS_PARTIAL,
    STATUS_SUCCESS_EMPTY,
    format_expansion_body,
    write_critic_manifest,
)


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
    import yaml
    head_end = body.find("---", 4)  # second --- (frontmatter close)
    frontmatter = body[3:head_end]   # between the two ---
    parsed = yaml.safe_load(frontmatter)
    assert parsed["title"] == 'How to make `My "Quoted" Title` better'
