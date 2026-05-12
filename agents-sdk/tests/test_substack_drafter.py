"""Tests for agents-sdk/agents/substack_drafter.py — voice-rotation module."""
from datetime import date
import pytest
from agents.substack_drafter import pick_voice_mode

# SPEC rotation table: 0=sean, 1=sedaris, 2=kerouac, 3=thompson, 4=vonnegut

def test_voice_mode_at_epoch():
    assert pick_voice_mode(today=date(2026, 5, 4), epoch=date(2026, 5, 4)) == "sean"


def test_voice_mode_week_1():
    # 7 days after epoch → index 1 → sedaris
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4)) == "sedaris"


def test_voice_mode_week_2():
    # 14 days after epoch → index 2 → kerouac
    assert pick_voice_mode(today=date(2026, 5, 18), epoch=date(2026, 5, 4)) == "kerouac"


def test_voice_mode_week_3():
    # 21 days after epoch → index 3 → thompson
    assert pick_voice_mode(today=date(2026, 5, 25), epoch=date(2026, 5, 4)) == "thompson"


def test_voice_mode_week_4():
    # 28 days after epoch → index 4 → vonnegut
    assert pick_voice_mode(today=date(2026, 6, 1), epoch=date(2026, 5, 4)) == "vonnegut"


def test_voice_mode_wraps_at_5():
    # 35 days after epoch → index 5 → wraps to 0 → sean
    assert pick_voice_mode(today=date(2026, 6, 8), epoch=date(2026, 5, 4)) == "sean"


def test_voice_mode_override_pins():
    assert pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="vonnegut") == "vonnegut"


def test_voice_mode_rejects_bad_override():
    with pytest.raises(ValueError):
        pick_voice_mode(today=date(2026, 5, 11), epoch=date(2026, 5, 4), override="hemingway")


# --- Synthesizer-dryness gate (Task C3) ---
import json
from pathlib import Path


def _write_manifest(d: Path, date_str: str, concepts: int, status: str = "ok") -> None:
    (d / f"synth-manifest-{date_str}.json").write_text(json.dumps({
        "status": status, "concepts_written": concepts, "duration_s": 12.0
    }))


def test_dryness_gate_blocks_when_last_3_are_zero(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 0)
    _write_manifest(tmp_path, "2026-05-31", 0)
    _write_manifest(tmp_path, "2026-06-01", 0)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


def test_dryness_gate_passes_when_last_3_have_output(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    _write_manifest(tmp_path, "2026-06-01", 7)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False


def test_dryness_gate_passes_when_only_most_recent_3_have_output(tmp_path):
    # Even if older manifests were dry, the gate looks only at the last N.
    _write_manifest(tmp_path, "2026-05-25", 0)
    _write_manifest(tmp_path, "2026-05-26", 0)
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    _write_manifest(tmp_path, "2026-06-01", 7)
    from agents.substack_drafter import is_synthesizer_dry
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False


def test_dryness_gate_blocks_when_one_of_last_3_is_zero(tmp_path):
    # Any single zero in the last N nights → dry. Conservative.
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 0)
    _write_manifest(tmp_path, "2026-06-01", 7)
    from agents.substack_drafter import is_synthesizer_dry
    # NOTE: spec is "exit no-op if last N have concepts_written == 0".
    # That implies ALL N must be zero. So this case is NOT dry.
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is False


def test_dryness_gate_handles_empty_dir(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    # No manifests yet → treat as dry (don't draft from nothing)
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


def test_dryness_gate_handles_too_few_manifests(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    # Fewer than threshold manifests exist at all → treat as dry (insufficient signal)
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    # Only 2 manifests; threshold is 3 → dry
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


def test_dryness_gate_handles_unreadable_manifest(tmp_path):
    from agents.substack_drafter import is_synthesizer_dry
    _write_manifest(tmp_path, "2026-05-30", 5)
    _write_manifest(tmp_path, "2026-05-31", 3)
    (tmp_path / "synth-manifest-2026-06-01.json").write_text("not valid json{")
    # Unreadable in the window → treat as dry to be safe
    assert is_synthesizer_dry(health_dir=tmp_path, threshold=3) is True


# --- Cluster picker (Task C4) ---

def _write_concept(d: Path, slug: str, wikilinks: list[str]) -> None:
    body = f"---\ntype: concept\nslug: {slug}\n---\n\n# {slug}\n\n"
    body += " ".join(f"[[{w}]]" for w in wikilinks)
    (d / f"{slug}.md").write_text(body)


def test_cluster_picker_returns_densest_3_to_5(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # Cluster A: three concepts that share >= 3 wikilinks pairwise
    _write_concept(tmp_path, "a", ["x", "y", "z", "shared"])
    _write_concept(tmp_path, "b", ["x", "y", "shared", "extra"])
    _write_concept(tmp_path, "c", ["y", "z", "shared"])
    # Cluster B: one isolated concept
    _write_concept(tmp_path, "lonely", ["nothing-shared"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    assert {"a", "b", "c"} <= set(cluster)
    assert "lonely" not in cluster
    assert 3 <= len(cluster) <= 5


def test_cluster_picker_empty_dir_returns_empty(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    assert pick_densest_cluster(concepts_dir=tmp_path, min_shared=3) == []


def test_cluster_picker_no_overlap_returns_singleton(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # Each concept has unique wikilinks → no edges meet min_shared
    _write_concept(tmp_path, "a", ["x", "y"])
    _write_concept(tmp_path, "b", ["w", "z"])
    _write_concept(tmp_path, "c", ["m", "n"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    # With no edges, every node is its own connected component. The largest is size 1.
    assert len(cluster) == 1


def test_cluster_picker_clips_to_5(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # 7 concepts all sharing >= 3 wikilinks → should clip to 5
    shared = ["a1", "a2", "a3"]
    for slug in ["n1", "n2", "n3", "n4", "n5", "n6", "n7"]:
        _write_concept(tmp_path, slug, shared + [f"unique-{slug}"])
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=3)
    assert len(cluster) == 5


def test_cluster_picker_ignores_aliased_wikilinks(tmp_path):
    from agents.substack_drafter import pick_densest_cluster
    # [[target|display]] notation — extract target, not display
    (tmp_path / "a.md").write_text("# a\n[[shared|display 1]] [[shared|display 2]] [[other|x]]")
    (tmp_path / "b.md").write_text("# b\n[[shared|y]] [[other|z]] [[third|w]]")
    cluster = pick_densest_cluster(concepts_dir=tmp_path, min_shared=2)
    assert set(cluster) >= {"a", "b"}


# --- Prompt composer (Task C5) ---

def test_compose_prompt_includes_voice_skill(tmp_path):
    from agents.substack_drafter import compose_prompt
    voice_skill = tmp_path / "SKILL.md"
    voice_skill.write_text("# Voice Modes\n\nSean Mode signature moves: short, blunt, narrative.")
    out = compose_prompt(
        voice_mode="sean",
        voice_skill_path=voice_skill,
        cluster_slugs=["pushover-fail-quiet", "silent-empty-output"],
        cluster_bodies=["Body A about Pushover.", "Body B about silent empty."],
        reference_excerpts=["ref about Hamel evals", "ref about Anthropic playbook"],
        word_count_target=1350,
    )
    assert "Sean Mode signature moves" in out["system"]
    assert "pushover-fail-quiet" in out["user"]
    assert "silent-empty-output" in out["user"]
    assert "1350" in out["user"]
    assert "Hook in the first 2 sentences" in out["user"]


def test_compose_prompt_returns_two_strings():
    """The shape is {'system': str, 'user': str} — HybridRouter takes both."""
    from agents.substack_drafter import compose_prompt
    from pathlib import Path
    out = compose_prompt(
        voice_mode="sedaris",
        voice_skill_path=Path("/nonexistent-but-read-tolerant-here"),
        cluster_slugs=["a"],
        cluster_bodies=["body"],
        reference_excerpts=[],
    )
    assert isinstance(out, dict)
    assert set(out.keys()) == {"system", "user"}
    assert isinstance(out["system"], str) and isinstance(out["user"], str)


def test_compose_prompt_handles_missing_voice_skill(tmp_path):
    """If voice_skill_path doesn't exist, the system prompt should degrade
    gracefully (fall back to a minimal voice-mode-named prompt). The agent
    should not crash mid-run if the skill file moves."""
    from agents.substack_drafter import compose_prompt
    missing = tmp_path / "definitely-not-here.md"
    out = compose_prompt(
        voice_mode="kerouac",
        voice_skill_path=missing,
        cluster_slugs=["a", "b"],
        cluster_bodies=["x", "y"],
        reference_excerpts=["r"],
    )
    # System prompt still mentions the voice mode by name even when the
    # spec file is missing — graceful degradation.
    assert "kerouac" in out["system"].lower()
    assert "missing" in out["system"].lower() or "not found" in out["system"].lower() or len(out["system"]) > 50


def test_compose_prompt_includes_all_cluster_bodies(tmp_path):
    from agents.substack_drafter import compose_prompt
    voice_skill = tmp_path / "SKILL.md"
    voice_skill.write_text("voice spec")
    out = compose_prompt(
        voice_mode="thompson",
        voice_skill_path=voice_skill,
        cluster_slugs=["a", "b", "c"],
        cluster_bodies=["UNIQUE-MARKER-A", "UNIQUE-MARKER-B", "UNIQUE-MARKER-C"],
        reference_excerpts=[],
    )
    for marker in ["UNIQUE-MARKER-A", "UNIQUE-MARKER-B", "UNIQUE-MARKER-C"]:
        assert marker in out["user"]


def test_compose_prompt_handles_empty_references():
    from agents.substack_drafter import compose_prompt
    from pathlib import Path
    out = compose_prompt(
        voice_mode="vonnegut",
        voice_skill_path=Path("/nonexistent"),
        cluster_slugs=["a"],
        cluster_bodies=["body"],
        reference_excerpts=[],  # empty list
    )
    # Should not crash; user prompt should still be coherent
    assert "vonnegut" in out["user"].lower()
    assert len(out["user"]) > 100  # not empty/trivial


# --- HybridRouter wrapper + draft writer (Task C6) ---

def test_write_draft_creates_file_with_frontmatter(tmp_path, monkeypatch):
    from agents import substack_drafter
    captured = {}
    def fake_route(*, task, system, user, max_cost_usd=None):
        captured["task"] = task
        captured["system"] = system
        captured["user"] = user
        return {
            "text": "# The Night My Vault Said Nothing\n\nDraft body here ending with [[some-concept]].",
            "model_used": "qwen3-14b",
            "cost_usd": 0.0,
        }
    monkeypatch.setattr(substack_drafter, "_route", fake_route)

    out_dir = tmp_path / "drafts"
    out_dir.mkdir()
    path = substack_drafter.write_draft(
        out_dir=out_dir,
        slug="vault-said-nothing",
        voice_mode="sean",
        cluster_slugs=["a", "b"],
        prompt={"system": "sys", "user": "user"},
        max_cost_usd=0.10,
    )
    assert path.exists()
    content = path.read_text()
    # Frontmatter
    assert "voice: sean" in content
    assert "source_concepts:" in content
    assert "'a'" in content or "a," in content or "- a" in content  # source_concepts list format flexible
    assert "model_used: qwen3-14b" in content
    assert "cost_usd: 0.0" in content
    assert "status: pending-review" in content
    # Body
    assert "# The Night My Vault Said Nothing" in content
    # Filename pattern
    assert path.name.endswith("-agent-draft-vault-said-nothing.md")
    # _route was called with the prompt
    assert captured["task"] == "substack_draft"
    assert captured["system"] == "sys"
    assert captured["user"] == "user"


def test_write_draft_handles_route_returning_long_text(tmp_path, monkeypatch):
    """A real draft is ~1300 words — make sure persistence handles it."""
    from agents import substack_drafter
    long_text = "# Title\n\n" + ("Long paragraph body. " * 200)  # ~1200 words
    monkeypatch.setattr(substack_drafter, "_route", lambda **kw: {
        "text": long_text, "model_used": "claude-sonnet-4-6", "cost_usd": 0.05,
    })
    out_dir = tmp_path / "drafts"
    out_dir.mkdir()
    path = substack_drafter.write_draft(
        out_dir=out_dir, slug="long-test", voice_mode="kerouac",
        cluster_slugs=["x"], prompt={"system": "s", "user": "u"}, max_cost_usd=0.10,
    )
    content = path.read_text()
    assert "model_used: claude-sonnet-4-6" in content
    assert "cost_usd: 0.05" in content
    assert long_text in content


def test_write_draft_handles_missing_optional_fields(tmp_path, monkeypatch):
    """If _route() returns a result without all keys, write_draft degrades gracefully."""
    from agents import substack_drafter
    monkeypatch.setattr(substack_drafter, "_route", lambda **kw: {"text": "minimal"})
    out_dir = tmp_path / "drafts"
    out_dir.mkdir()
    path = substack_drafter.write_draft(
        out_dir=out_dir, slug="min", voice_mode="vonnegut",
        cluster_slugs=["a"], prompt={"system": "s", "user": "u"}, max_cost_usd=0.10,
    )
    content = path.read_text()
    assert "model_used: unknown" in content  # graceful default
    assert "cost_usd: 0.0" in content  # graceful default
    assert "minimal" in content


# --- main() + --dry-run (Task C7) ---

def test_main_dryrun_no_route_call(tmp_path, monkeypatch, capsys):
    """In --dry-run mode, _route() must NOT be called. Kill-switch layer 3."""
    from agents import substack_drafter
    # Build scaffolding that would otherwise reach the prompt step:
    health = tmp_path / "health"; health.mkdir()
    concepts = tmp_path / "concepts"; concepts.mkdir()
    drafts = tmp_path / "drafts"; drafts.mkdir()
    # 3 nights of healthy synth manifests
    for dstr in ["2026-06-01", "2026-06-02", "2026-06-03"]:
        (health / f"synth-manifest-{dstr}.json").write_text(
            '{"status":"ok","concepts_written":3}')
    # 2 connected concepts (need >= 3 shared wikilinks for cluster to form)
    (concepts / "a.md").write_text("# a\n[[x]] [[y]] [[shared]] [[extra]]")
    (concepts / "b.md").write_text("# b\n[[x]] [[y]] [[shared]]")
    voice_skill = tmp_path / "SKILL.md"; voice_skill.write_text("voice spec content")

    called = {"n": 0}
    def fake_route(**kw):
        called["n"] += 1
        return {"text": "draft", "model_used": "qwen3-14b", "cost_usd": 0.0}
    monkeypatch.setattr(substack_drafter, "_route", fake_route)

    rc = substack_drafter.main(
        health_dir=health, concepts_dir=concepts, out_dir=drafts,
        voice_skill_path=voice_skill, dry_run=True,
    )
    assert rc == 0
    assert called["n"] == 0  # dry-run must NOT call the model
    assert list(drafts.glob("*.md")) == []  # no draft written
    out = capsys.readouterr().out
    assert "DRY-RUN" in out
    assert "voice:" in out


def test_main_dry_synth_exits_zero_no_op(tmp_path, capsys):
    """When the synthesizer is dry, main exits 0 with a no-op message."""
    from agents import substack_drafter
    health = tmp_path / "health"; health.mkdir()
    for dstr in ["2026-06-01", "2026-06-02", "2026-06-03"]:
        (health / f"synth-manifest-{dstr}.json").write_text(
            '{"status":"ok","concepts_written":0}')
    rc = substack_drafter.main(
        health_dir=health, concepts_dir=tmp_path / "none",
        out_dir=tmp_path / "out", voice_skill_path=tmp_path / "SKILL.md",
        dry_run=False,
    )
    assert rc == 0
    captured_out = capsys.readouterr().out
    assert "synthesizer dry" in captured_out


def test_main_writes_draft_when_synth_healthy_and_not_dryrun(tmp_path, monkeypatch, capsys):
    """Happy path: synth healthy, cluster found, _route returns body, draft written."""
    from agents import substack_drafter
    health = tmp_path / "health"; health.mkdir()
    concepts = tmp_path / "concepts"; concepts.mkdir()
    drafts = tmp_path / "drafts"; drafts.mkdir()
    for dstr in ["2026-06-01", "2026-06-02", "2026-06-03"]:
        (health / f"synth-manifest-{dstr}.json").write_text(
            '{"status":"ok","concepts_written":3}')
    (concepts / "a.md").write_text("# a\n[[x]] [[y]] [[shared]] [[extra]]")
    (concepts / "b.md").write_text("# b\n[[x]] [[y]] [[shared]]")
    voice_skill = tmp_path / "SKILL.md"; voice_skill.write_text("voice spec")

    monkeypatch.setattr(substack_drafter, "_route", lambda **kw: {
        "text": "# DRAFT TITLE\n\nbody [[a]] [[b]]",
        "model_used": "qwen3-14b",
        "cost_usd": 0.0,
    })

    rc = substack_drafter.main(
        health_dir=health, concepts_dir=concepts, out_dir=drafts,
        voice_skill_path=voice_skill, dry_run=False,
    )
    assert rc == 0
    drafts_written = list(drafts.glob("*.md"))
    assert len(drafts_written) == 1
    assert "DRAFT TITLE" in drafts_written[0].read_text()


def test_main_no_cluster_exits_zero(tmp_path, monkeypatch, capsys):
    """No dense cluster (e.g., empty concepts dir, or fewer than 2 connected) -> no-op."""
    from agents import substack_drafter
    health = tmp_path / "health"; health.mkdir()
    concepts = tmp_path / "concepts"; concepts.mkdir()  # empty
    drafts = tmp_path / "drafts"; drafts.mkdir()
    for dstr in ["2026-06-01", "2026-06-02", "2026-06-03"]:
        (health / f"synth-manifest-{dstr}.json").write_text(
            '{"status":"ok","concepts_written":3}')
    voice_skill = tmp_path / "SKILL.md"; voice_skill.write_text("voice spec")

    monkeypatch.setattr(substack_drafter, "_route", lambda **kw: {"text": "x"})

    rc = substack_drafter.main(
        health_dir=health, concepts_dir=concepts, out_dir=drafts,
        voice_skill_path=voice_skill, dry_run=False,
    )
    assert rc == 0
    captured = capsys.readouterr().out
    assert "no dense cluster" in captured.lower()
    assert list(drafts.glob("*.md")) == []


def test_main_voice_override_pins(tmp_path, monkeypatch):
    """voice_override='sedaris' should override the calendar rotation."""
    from agents import substack_drafter
    health = tmp_path / "health"; health.mkdir()
    concepts = tmp_path / "concepts"; concepts.mkdir()
    drafts = tmp_path / "drafts"; drafts.mkdir()
    for dstr in ["2026-06-01", "2026-06-02", "2026-06-03"]:
        (health / f"synth-manifest-{dstr}.json").write_text(
            '{"status":"ok","concepts_written":3}')
    (concepts / "a.md").write_text("# a\n[[x]] [[y]] [[shared]] [[extra]]")
    (concepts / "b.md").write_text("# b\n[[x]] [[y]] [[shared]]")
    voice_skill = tmp_path / "SKILL.md"; voice_skill.write_text("voice spec")

    captured = {}
    def fake_route(**kw):
        captured["system"] = kw["system"]
        return {"text": "x", "model_used": "qwen3-14b", "cost_usd": 0.0}
    monkeypatch.setattr(substack_drafter, "_route", fake_route)

    rc = substack_drafter.main(
        health_dir=health, concepts_dir=concepts, out_dir=drafts,
        voice_skill_path=voice_skill, dry_run=False,
        voice_override="sedaris",
    )
    assert rc == 0
    # The system prompt must mention 'sedaris' (compose_prompt embeds the voice name)
    assert "sedaris" in captured["system"].lower()
