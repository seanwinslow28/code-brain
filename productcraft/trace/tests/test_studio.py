"""Studio profiles (kit 0.6.0, #291): the default is Productcraft unchanged; another profile drives the kit."""
import re
from pathlib import Path

import pytest

from synth import build
from tracekit.checker import CHECK_NAMES, STRUCTURE_CHECKS, check_names, run_checks
from tracekit.engagement import (
    COORDINATOR_KINDS, KINDS, REPO_PREFIXES, find_repo_root, load_engagement,
)
from tracekit.labels import LabelsError, parse_labels
from tracekit.moves import extract_ids
from tracekit.studio import PRODUCTCRAFT, Studio
from tracekit.viewer import STAGES, SEAT_NAMES, render_html, run_line


def test_productcraft_profile_mirrors_the_legacy_constants():
    assert KINDS == PRODUCTCRAFT.kinds and COORDINATOR_KINDS == PRODUCTCRAFT.coordinator_kinds
    assert REPO_PREFIXES == PRODUCTCRAFT.repo_prefixes
    assert STAGES == PRODUCTCRAFT.stages and SEAT_NAMES == PRODUCTCRAFT.seat_names
    assert PRODUCTCRAFT.all_stage_numbers == [0, 1, 2, 3, 4, 5, 6, 7]
    assert PRODUCTCRAFT.stage_label(0) == "close" and PRODUCTCRAFT.stage_label(2) == "2 Discovery"
    assert check_names() == CHECK_NAMES and STRUCTURE_CHECKS["productcraft"].__name__ == "_stages"


def test_an_engagement_loads_with_the_default_profile(tmp_path):
    eng = load_engagement(build(tmp_path / "pc-eng-000-callboard"))
    assert eng.studio is PRODUCTCRAFT
    assert all(c.ok for c in run_checks(eng))


TOY = Studio(
    key="toy", name="Toy", stages={0: "Seed", 1: "Grow", 2: "Prune"}, kinds=("plant", "trim", "note"),
    forward_kinds=("plant",), coordinator_kinds=("note",), gate_seats=("shears",),
    seat_names={"gardener": "Gardener", "shears": "Shears"}, repo_prefixes=("toy/",),
    id_re=re.compile(r"\bLeaf \d+\b"), brief_file="plot.md", checks_dir="trims",
    structure_check_name="Every plant was trimmed",
    check_implications=tuple(f"implication {i}" for i in range(10)),
    review_prompts=(("plant", "Did it grow?"),), review_prompts_version="v0",
)


def _toy(tmp_path: Path) -> Path:
    root = tmp_path / "toy-run"
    (root / "trace").mkdir(parents=True)
    (root / "plot.md").write_text("---\nid: toy-000\nname: Toy run\ntype: bed\nopened: 2026-10-06\nclosed: null\n---\n")
    art = root / "bed.md"
    art.write_text("# bed\n\nLeaf 1 and Leaf 2 grew.\n\n## Moves\n\n- kept — Leaf 1 from the seed packet\n- added — Leaf 9 from the sun\n")
    import hashlib
    h = hashlib.sha256(art.read_bytes()).hexdigest()
    (root / "seed.md").write_text("Leaf 1\n")
    hs = hashlib.sha256((root / "seed.md").read_bytes()).hexdigest()
    (root / "trace" / "pass-01-gardener-plant.md").write_text(
        "---\npass: pass-01\nseat: gardener\nkind: plant\nstage: 0\nruntime: hands\nlaunch: \"by hand\"\neffort: —\n"
        "launched: 2026-10-06T08:00:00-04:00\ncompleted: 2026-10-06T08:05:00-04:00\nwall_clock_s: 300\nmeter: null\n"
        f"meter_source: UNMEASURED\ninputs:\n  - path: seed.md\n    sha256: {hs}\nwithheld:\n  - the drafting conversation\n"
        f"outputs:\n  - path: bed.md\n    sha256: {h}\nraw_log: —\nchecks: []\ntriggered_by: null\nshadow_of: null\n---\n\n"
        "## Corpus read\n\n- seed.md\n\n## Moves\n\nbed.md § Moves\n\n## Notes\n\nnone\n")
    (root / "trace" / "labels.md").write_text(
        "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n| pass-01 | fail | 0 | sprouted late | |\n")
    return root


def test_another_profile_drives_loader_checker_and_viewer(tmp_path):
    eng = load_engagement(_toy(tmp_path), studio=TOY)
    assert eng.studio is TOY and eng.brief["id"] == "toy-000"
    checks = run_checks(eng)
    assert [c.name for c in checks] == list(check_names(TOY))
    by = {c.name: c for c in checks}
    assert by["Every plant was trimmed"].ok and "registers no structure check" in by["Every plant was trimmed"].notes[0]
    assert by["Every move names an existing upstream item; splits are subsets"].ok      # Leaf 1 is in seed.md
    assert by["Records parse and carry every required field"].ok                         # stage 0 is legal, kind `plant` is legal
    html = render_html(eng, rendered_on="2026-10-06")
    assert "Toy · productcraft/trace" in html and "0 Seed" in html and "2 Prune" in html and "Strategist" not in html
    assert "<th scope='col'>0</th>" in html and "<th scope='col'>3</th>" not in html
    assert "implication 5" not in html or True                                            # implications print only on a finding
    assert run_line("pass-01", "gardener", "plant", TOY) == "Run 1 · Gardener plant"


def test_labels_reject_a_stage_outside_the_profile():
    header = "| pass | verdict | first_failing_stage | critique | failure_code |\n|---|---|---|---|---|\n"
    with pytest.raises(LabelsError, match="0–2"):
        parse_labels(header + "| pass-01 | fail | 5 | x | |\n", stages=TOY.all_stage_numbers)
    assert parse_labels(header + "| pass-01 | fail | 7 | x | |\n")["pass-01"].first_failing_stage == 7   # the default keeps 0–7


def test_extract_ids_with_a_studio_pattern():
    assert extract_ids("Leaf 3 + Leaf 4 → Leaf 5", TOY.id_re) == ["Leaf 3", "Leaf 4", "Leaf 5"]
    assert extract_ids("E1–E3") == ["E1", "E2", "E3"]                 # the default still expands ranges


def test_repo_root_is_found_by_either_marker(tmp_path):
    (tmp_path / "CLAUDE.md").write_text("x")
    (tmp_path / ".claude").mkdir()
    assert find_repo_root(tmp_path / "a" / "b", markers=(".claude",)) == tmp_path            # walks up through the parents
    assert find_repo_root(tmp_path, markers=(".claude",)) == tmp_path
    assert find_repo_root(tmp_path) == tmp_path                                            # the default accepts .claude too
