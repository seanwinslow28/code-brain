"""The two Close-ritual commands: check.py and render.py, run as scripts on the system python."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from synth import build

TRACE = Path(__file__).resolve().parents[1]


@pytest.fixture
def eng_dir(tmp_path) -> Path:
    return build(tmp_path / "pc-eng-000-callboard")


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, cwd=TRACE)


def test_check_exits_zero_and_prints_every_check(eng_dir):
    r = run("check.py", str(eng_dir))
    assert r.returncode == 0, r.stderr
    assert "PASS  Every pass has a record  25 of 25" in r.stdout
    assert r.stdout.count("\nPASS") + r.stdout.startswith("PASS") == 9


def test_check_exits_one_on_a_failing_check(eng_dir):
    (eng_dir / "trace" / "pass-10-discovery-lead-audit.md").unlink()
    r = run("check.py", str(eng_dir))
    assert r.returncode == 1
    assert "FAIL  Every pass has a record" in r.stdout
    assert "pass-10 has no record" in r.stdout


def test_check_json(eng_dir):
    r = run("check.py", str(eng_dir), "--json")
    data = json.loads(r.stdout)
    assert [c["name"] for c in data][:2] == ["Records parse and carry every required field", "Every pass has a record"]
    assert all(set(c) >= {"name", "ok", "n_ok", "n_total", "findings", "notes"} for c in data)


def test_check_refuses_a_folder_that_is_not_an_engagement(tmp_path):
    r = run("check.py", str(tmp_path / "nowhere"))
    assert r.returncode == 2
    assert "no engagement" in (r.stderr + r.stdout).lower()


def test_render_writes_eval_html(eng_dir):
    r = run("render.py", str(eng_dir))
    assert r.returncode == 0, r.stderr
    assert (eng_dir / "trace" / "eval.html").is_file()
    assert "eval.html" in r.stdout


def test_render_out_flag(eng_dir, tmp_path):
    out = tmp_path / "custom.html"
    r = run("render.py", str(eng_dir), "--out", str(out))
    assert r.returncode == 0 and out.is_file()


def test_render_still_renders_when_checks_fail(eng_dir):
    (eng_dir / "trace" / "pass-10-discovery-lead-audit.md").unlink()
    r = run("render.py", str(eng_dir))
    assert r.returncode == 0
    assert "checks failing" in r.stdout


def test_the_kit_runs_on_a_bare_interpreter(eng_dir):
    """No third-party import anywhere: the Close ritual must not need a venv."""
    r = run("-I", "-c",
            "import sys; sys.path.insert(0, %r); import tracekit.checker, tracekit.viewer; print('ok')" % str(TRACE))
    assert r.returncode == 0 and r.stdout.strip() == "ok", r.stderr


# --------------------------------------------------------------------------- #
# #297 · the id helper
# --------------------------------------------------------------------------- #


def test_nextid_prints_the_next_id_with_its_accounting(eng_dir):
    r = run("nextid.py", str(eng_dir))
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("pc-eng-000.d11\n")
    assert "10 entries on disk" in r.stdout


def test_nextid_bare_is_one_line_for_a_shell_variable(eng_dir):
    r = run("nextid.py", str(eng_dir), "--bare")
    assert r.returncode == 0, r.stderr
    assert r.stdout == "pc-eng-000.d11\n"


def test_nextid_refuses_a_folder_that_is_not_an_engagement(tmp_path):
    (tmp_path / "empty").mkdir()
    r = run("nextid.py", str(tmp_path / "empty"))
    assert r.returncode == 2
    assert "not an engagement" in r.stderr
