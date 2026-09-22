"""Registry numbers (#286): the runtime × seat table, counts only, and the meter-source drift test."""
import re
import subprocess
import sys
from pathlib import Path

import pytest

from synth import build
from tracekit.engagement import METER_SOURCES, load_engagement
from tracekit.registry import numbers_for, render_markdown

TRACE = Path(__file__).resolve().parents[1]
REGISTRY = TRACE.parent / "templates" / "runtime-registry.md"


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    assert old in text, f"{old!r} not in {path.name}"
    path.write_text(text.replace(old, new, 1))


def by_runtime(eng_dir):
    per_runtime, per_pair = numbers_for([load_engagement(eng_dir)])
    return {c.runtime: c for c in per_runtime}, {(c.runtime, c.seat): c for c in per_pair}


# --------------------------------------------------------------------------- #
# the vocabulary lives in one place
# --------------------------------------------------------------------------- #


def test_registry_meter_source_vocabulary_matches_the_kit():
    text = REGISTRY.read_text()
    section = text[text.index("## Meter-source vocabulary"):]
    values = [m.group(1) for m in re.finditer(r"^\| `([^`]+)` \|", section, re.MULTILINE)]
    assert values, "the registry's vocabulary table has no rows"
    assert set(values) == set(METER_SOURCES), (
        f"registry {sorted(values)} vs kit {sorted(METER_SOURCES)} — add the value to both in one change"
    )
    assert "UNMEASURED" in values


def test_every_registry_row_names_a_vocabulary_value():
    text = REGISTRY.read_text()
    rows = text[text.index("## The rows"):text.index("## Standing")]
    for line in rows.splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        named = [v for v in METER_SOURCES if f"`{v}`" in line or (v != "UNMEASURED" and "as row 3" in line)]
        assert named, f"row without a meter_source value: {line[:60]}"


# --------------------------------------------------------------------------- #
# numbers on the synthetic train
# --------------------------------------------------------------------------- #


def test_counts_per_runtime_add_up(eng_dir):
    rt, _ = by_runtime(eng_dir)
    assert sum(c.passes for c in rt.values()) == 25
    codex = rt["codex gpt-5.6-sol high"]
    assert (codex.passes, codex.labeled, codex.passed, codex.trials) == (5, 4, 3, 1)
    sonnet = rt["claude-sonnet-5"]
    assert (sonnet.passes, sonnet.labeled, sonnet.passed) == (6, 5, 5)
    fable = rt["claude-fable-5-1"]
    assert (fable.passes, fable.measured, fable.median_tokens) == (1, 0, None)


def test_measured_medians_exclude_unmeasured_passes(eng_dir):
    rt, _ = by_runtime(eng_dir)
    opus = rt["claude-opus-5"]
    assert opus.measured == opus.passes == 13
    assert opus.median_tokens and opus.median_wall_clock_s
    assert len(opus.tokens) == 13


def test_rung0_clean_drops_a_pass_a_finding_names(eng_dir):
    before, _ = by_runtime(eng_dir)
    edit(eng_dir / "trace" / "pass-05-discovery-lead-draft.md", "meter_source: Agent-tool usage", "meter_source: estimated")
    after, _ = by_runtime(eng_dir)
    assert after["claude-opus-5"].clean == before["claude-opus-5"].clean - 1
    assert after["claude-opus-5"].measured == before["claude-opus-5"].measured - 1


def test_per_seat_cells_carry_a_family(eng_dir):
    _, cells = by_runtime(eng_dir)
    assert cells[("codex gpt-5.6-sol high", "red-team-gate")].family == "gate"
    assert cells[("claude-opus-5", "product-strategist")].family == "framing"
    assert cells[("claude-sonnet-5", "delivery-execution")].trials == 0
    assert cells[("codex gpt-5.6-sol high", "delivery-execution")].trials == 1


def test_promotion_is_read_from_the_trial_notes_line_only(eng_dir):
    rt, _ = by_runtime(eng_dir)
    assert (rt["codex gpt-5.6-sol high"].promotable, rt["codex gpt-5.6-sol high"].promoted) == (0, 0)
    labels = eng_dir / "trace" / "labels.md"
    edit(labels, "| pass-18 |  |  |  |  |", "| pass-18 | pass |  | The trial's roadmap keeps KR-3 measurable. |  |")
    edit(labels, "| pass-16 | pass |  |", "| pass-16 | fail | 6 |")
    rt, _ = by_runtime(eng_dir)
    assert (rt["codex gpt-5.6-sol high"].promotable, rt["codex gpt-5.6-sol high"].promoted) == (1, 0)
    edit(eng_dir / "trace" / "pass-18-delivery-execution-trial.md",
         "Shadow pass on identical inputs. Label blind.",
         "Shadow pass on identical inputs. Label blind.\npromoted: 2026-10-07 — dated substitution under rule 7, noted on pass-16 too.")
    rt, _ = by_runtime(eng_dir)
    assert rt["codex gpt-5.6-sol high"].promoted == 1


def test_markdown_prints_counts_and_never_a_percentage(eng_dir):
    per_runtime, per_pair = numbers_for([load_engagement(eng_dir)])
    md = render_markdown(per_runtime, per_pair)
    assert "%" not in md
    assert "| `codex gpt-5.6-sol high` | 5 | 3 of 4 |" in md
    assert "Engagements read: pc-eng-000." in md
    assert md.count("\n|") >= 4 + len(per_pair)


def test_two_engagements_aggregate(eng_dir, tmp_path):
    other = build(tmp_path / "pc-eng-009-callboard")
    per_runtime, _ = numbers_for([load_engagement(eng_dir), load_engagement(other)])
    rt = {c.runtime: c for c in per_runtime}
    assert rt["claude-opus-5"].passes == 26
    assert rt["claude-opus-5"].engagements == {"pc-eng-000"}  # the synthetic brief carries the same id twice


# --------------------------------------------------------------------------- #
# the script
# --------------------------------------------------------------------------- #


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=TRACE)


def test_registry_script_prints_the_tables(eng_dir):
    r = run("registry.py", str(eng_dir))
    assert r.returncode == 0, r.stderr
    assert "| Runtime | Passes | Labeled pass |" in r.stdout
    assert "| `claude-opus-5` | product-strategist | framing |" in r.stdout
    assert "%" not in r.stdout


def test_registry_script_json(eng_dir):
    import json
    r = run("registry.py", str(eng_dir), "--json")
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert {c["runtime"] for c in data["runtimes"]} == {"claude-opus-5", "claude-sonnet-5", "codex gpt-5.6-sol high", "claude-fable-5-1"}
    assert all("median_tokens" in c for c in data["cells"])


def test_registry_script_rejects_a_non_engagement(tmp_path):
    r = run("registry.py", str(tmp_path / "nowhere"))
    assert r.returncode == 2
    r = run("registry.py")
    assert r.returncode == 2
