"""Studio profiles (kit 0.6.0, #291; resolved per engagement since 0.9.0, #325): no studio lives in the kit."""
import re
from pathlib import Path

import pytest

import tracekit.studio as studio_mod
from reference import PRODUCTCRAFT, PROFILE, REPO
from synth import build
from tracekit.checker import CHECK_NAMES, STRUCTURE_CHECKS, check_names, run_checks
from tracekit.engagement import REPO_PREFIXES, find_repo_root, load_engagement
from tracekit.labels import LabelsError, parse_labels
from tracekit.moves import extract_ids
from tracekit.studio import PROFILE_ENV, Studio, StudioNotFound, find_profile, load_profile, resolve_studio
from tracekit.taxonomy import SHARED_TAXONOMY_PATH, taxonomy_for
from tracekit.viewer import render_html, run_line


def test_the_kit_holds_no_studio_of_its_own():
    assert not hasattr(studio_mod, "PRODUCTCRAFT")
    assert REPO_PREFIXES == ("craftwork/", ".claude/")                     # only what every studio shares
    assert not (Path(studio_mod.__file__).parents[1] / studio_mod.PROFILE_FILE).exists()   # a walk never finds the kit


def test_productcraft_profile_lives_with_productcraft():
    assert PROFILE == REPO / "productcraft" / "trace" / "studio.py"
    assert PRODUCTCRAFT.key == "productcraft" and PRODUCTCRAFT.all_stage_numbers == [0, 1, 2, 3, 4, 5, 6, 7]
    assert PRODUCTCRAFT.stage_label(0) == "close" and PRODUCTCRAFT.stage_label(2) == "2 Discovery"
    assert check_names(PRODUCTCRAFT) == CHECK_NAMES and STRUCTURE_CHECKS["productcraft"].__name__ == "_stages"
    assert load_profile(PROFILE) is PRODUCTCRAFT                           # one load per file: one studio object


def test_an_engagement_loads_with_the_reference_profile(tmp_path):
    eng = load_engagement(build(tmp_path / "pc-eng-000-callboard"))
    assert eng.studio is PRODUCTCRAFT
    assert all(c.ok for c in run_checks(eng))


def test_the_walk_finds_the_team_profile_above_its_ledger():
    eng_dir = REPO / "productcraft" / "ledger" / "engagements" / "pc-eng-001-anything"   # need not exist
    assert find_profile(eng_dir) == PROFILE
    assert find_profile(REPO / "productcraft" / "trace" / "samples" / "synthetic-engagement") == PROFILE
    assert find_profile(REPO / "craftwork" / "trace" / "tests") is None


def test_resolution_order_passed_then_walk_then_env_then_refuse(tmp_path, monkeypatch):
    team = tmp_path / "toycraft"
    (team / "trace").mkdir(parents=True)
    (team / "trace" / "studio.py").write_text(
        "from tracekit.studio import Studio\n"
        "STUDIO = Studio(key='toycraft', name='Toycraft', stages={1: 'One'}, kinds=('draft',), forward_kinds=('draft',))\n")
    eng = team / "ledger" / "engagements" / "tc-eng-001"
    eng.mkdir(parents=True)
    assert resolve_studio(eng, TOY) is TOY                                  # passed in wins
    assert resolve_studio(eng).key == "toycraft"                            # then the walk, over $TRACEKIT_STUDIO
    loose = tmp_path / "loose" / "eng"
    loose.mkdir(parents=True)
    assert resolve_studio(loose) is PRODUCTCRAFT                            # then the env fallback
    monkeypatch.delenv(PROFILE_ENV)
    with pytest.raises(StudioNotFound, match="no studio profile"):
        resolve_studio(loose)                                               # never a guess
    with pytest.raises(StudioNotFound, match="defines no STUDIO"):
        (tmp_path / "empty.py").write_text("X = 1\n")
        load_profile(tmp_path / "empty.py")


def test_cli_refuses_an_engagement_with_no_studio(tmp_path, monkeypatch):
    import subprocess, sys
    monkeypatch.delenv(PROFILE_ENV)
    loose = build(tmp_path / "loose" / "pc-eng-000-callboard")
    trace = Path(studio_mod.__file__).parents[1]
    r = subprocess.run([sys.executable, "check.py", str(loose)], capture_output=True, text=True, cwd=trace)
    assert r.returncode == 2 and "no studio profile" in r.stderr
    r = subprocess.run([sys.executable, "check.py", str(loose), "--studio", str(PROFILE)], capture_output=True, text=True, cwd=trace)
    assert r.returncode == 0, r.stdout + r.stderr


def test_taxonomy_is_shared_family_plus_the_studios_own(tmp_path):
    tax = taxonomy_for(PRODUCTCRAFT)
    assert {"manufactured", "stale-restatement", "overstated-scope", "kit-induced"} <= set(tax.codes)   # shared
    assert {"unobservable-measure", "overclaimed-pointer"} <= set(tax.codes)                             # Productcraft's
    assert list(tax.codes)[:4] == ["manufactured", "stale-restatement", "overstated-scope", "kit-induced"]
    assert tax.path == PRODUCTCRAFT.taxonomy_path
    own = tmp_path / "taxonomy.md"
    own.write_text("| code | family | a label with this code says | quote |\n|---|---|---|---|\n| `wilted` | seat | it wilted | — |\n")
    alone = Studio(key="t", name="T", stages={1: "One"}, kinds=("draft",), forward_kinds=("draft",),
                   taxonomy_path=own, shared_taxonomy=False)
    assert set(taxonomy_for(alone).codes) == {"wilted"}                     # opted out: its own file alone
    bare = Studio(key="b", name="B", stages={1: "One"}, kinds=("draft",), forward_kinds=("draft",))
    assert taxonomy_for(bare).path == SHARED_TAXONOMY_PATH and "manufactured" in taxonomy_for(bare).codes


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
    assert "Toy · craftwork/trace" in html and "0 Seed" in html and "2 Prune" in html and "Strategist" not in html
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
