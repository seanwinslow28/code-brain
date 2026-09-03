#!/usr/bin/env python3
"""Stdlib-only tests for analyze.py. Run either way:
    python3 -m pytest .claude/skills/writing-critique/references/test_analyze.py -v
    python3 .claude/skills/writing-critique/references/test_analyze.py   # zero-dependency fallback
"""
import importlib.util
import json
import tempfile
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "analyze", str(Path(__file__).with_name("analyze.py")))
analyze = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(analyze)


def test_mattr_window_is_locked_50():
    assert analyze.MATTR_WINDOW == 50


def test_strip_frontmatter_and_fences():
    raw = "---\ntitle: x\n---\nHello world.\n```\ncode\n```\nReal prose here."
    out = analyze.strip_frontmatter_and_fences(raw)
    assert "title: x" not in out
    assert "code" not in out
    assert "Real prose here." in out


def test_words_tokenizes_lowercase():
    assert analyze.words("The Cat's hat.") == ["the", "cat's", "hat"]


def test_cv_high_for_varied_sentences():
    sents = ["Short.", "This one is a good deal longer than the first sentence here.",
             "Mid length sentence now.", "Tiny.",
             "Another fairly long winding clause that keeps going and going for a while."]
    stats = analyze.sentence_length_stats(sents)
    assert stats["cv"] is not None and stats["cv"] >= 0.45
    assert stats["monotony_flag"] is False


def test_cv_low_for_monotone_sentences():
    sents = ["The agent ran the nightly job again.",
             "The system logged the result to disk.",
             "The report listed the total for today.",
             "The metric stayed inside the normal band."]
    stats = analyze.sentence_length_stats(sents)
    assert stats["cv"] is not None and stats["cv"] < 0.45
    assert stats["monotony_flag"] is True


def test_cv_guards_single_sentence():
    stats = analyze.sentence_length_stats(["Only one sentence here."])
    assert stats["cv"] is None          # no div-by-zero
    assert stats["monotony_flag"] is False


def test_mattr_none_for_short_text():
    assert analyze.mattr(["a", "b", "c"]) is None


def test_mattr_value_for_long_text():
    toks = (["the", "cat", "sat", "on", "a", "mat"] * 20)
    val = analyze.mattr(toks)
    assert val is not None and 0.0 < val <= 1.0


def test_mtld_lower_for_repetitive_text():
    diverse = "alpha beta gamma delta epsilon zeta eta theta iota kappa".split() * 6
    repetitive = "the the the the cat the the the the the".split() * 6
    assert analyze.mtld(repetitive) < analyze.mtld(diverse)


def test_lexical_diversity_uses_mtld_under_60_tokens():
    toks = "the agent ran the job and then it failed and i fixed it fast".split()
    ld = analyze.lexical_diversity(toks)
    assert ld["primary_metric"] == "mtld"
    assert ld["low_confidence"] is True


def test_emit_baseline_has_mean_and_stdev_per_metric():
    corpus = (
        "## one\n" + "I ran the fleet at dawn and the agents sang back to me. "
        "Short. A longer winding line that keeps unspooling across the morning quiet.\n\n"
        + " ".join(f"word{i}" for i in range(80)) + "\n\n"
        "## two\n" + "We shipped it late. The ferry horn blew across the cold gray water again. "
        "Tiny. Another long meandering clause that refuses to end for quite a while now.\n\n"
        + " ".join(f"alt{i}" for i in range(80)) + "\n"
    )
    with tempfile.TemporaryDirectory() as d:
        cpath = Path(d) / "corpus.md"
        cpath.write_text(corpus, encoding="utf-8")
        out = Path(d) / "baseline.json"
        bl = analyze.emit_baseline(str(cpath), str(out))
        assert bl["segments"] == 2
        assert bl["mattr_window"] == 50
        assert "cv" in bl["metrics"]
        assert "mean" in bl["metrics"]["cv"] and "stdev" in bl["metrics"]["cv"]
        # Observed min/max, added by #219: the dashboard prints the range the
        # segments actually occupy, not a +/-sigma envelope around their mean.
        assert bl["metrics"]["cv"]["min"] <= bl["metrics"]["cv"]["max"]
        # The register pair the rules-off experiment kept computing by hand.
        for key in ("mean_len", "short_share", "long_share"):
            assert key in bl["metrics"], key
        assert json.loads(out.read_text(encoding="utf-8"))["schema_version"] == 2


def test_short_and_long_shares_are_percentages_of_sentences():
    # Five sentences: three <=6 words, one >=35, one in between.
    text = ("Short one. Short two. Short three. "
            + " ".join(f"word{i}" for i in range(40)) + ". "
            + " ".join(f"mid{i}" for i in range(15)) + ".")
    m = analyze.metrics_from_raw(text)["sentence_length"]
    assert m["n"] == 5
    assert m["short_share"] == 60.0
    assert m["long_share"] == 20.0


def test_empty_committed_gate_flags_nothing():
    """The #219 ruling, asserted against the committed baseline rather than a
    fixture: with flag_metrics empty, no draft can raise a flag however far it
    sits from the band. Re-arming a metric stays a data edit."""
    committed = json.loads(
        (Path(__file__).with_name("baseline.json")).read_text(encoding="utf-8"))
    assert committed["gate"]["flag_metrics"] == []
    flat = _metrics(cv=0.01, mattr=0.05, fp=0.0, opener=0.0)
    assert analyze.baseline_flags(flat, committed) == []


def test_rewrite_band_holds_no_prose():
    """Same discipline as baseline.json: aggregates and labels only. A verbatim
    line leaking into a tracked file is how the contaminated baseline happened."""
    path = Path(__file__).with_name("rewrite-band.json")
    if not path.is_file():
        return
    band = json.loads(path.read_text(encoding="utf-8"))
    for name, blk in band["series"].items():
        for piece in blk["pieces"]:
            assert set(piece) == {"label", "source", "metrics"}, (name, piece.keys())
            assert all(isinstance(v, (int, float, type(None)))
                       for v in piece["metrics"].values()), piece["label"]
        # Below the floor there is no band, only points.
        if blk["n"] < band["n_floor"]:
            assert blk["metrics"] is None, name
        else:
            assert blk["metrics"] is not None, name


def _metrics(cv=0.10, mattr=0.50, fp=0.1, opener=5.0):
    return {
        "sentence_length": {"cv": cv, "monotony_flag": True},
        "lexical_diversity": {"mattr": mattr},
        "pronouns": {"first_person_rate": fp},
        "openers": {"other_pct": opener},
    }


_BASELINE_METRICS = {
    "cv": {"mean": 0.70, "stdev": 0.10},
    "mattr": {"mean": 0.80, "stdev": 0.03},
    "first_person_rate": {"mean": 4.0, "stdev": 1.0},
    "opener_other_pct": {"mean": 40.0, "stdev": 8.0},
}


def test_baseline_flags_fire_below_range():
    flags = analyze.baseline_flags(_metrics(), {"metrics": _BASELINE_METRICS})
    assert any("monotonous" in f for f in flags)
    assert any("vocabulary" in f for f in flags)
    assert any("pronoun" in f for f in flags)
    # opener variety is REPORT-ONLY by default (#177): it was the last
    # false-positive source once the gate moved to 2 sigma.
    assert not any("open the same way" in f for f in flags)


def test_default_gate_is_two_sigma():
    """A value inside 2 sigma but outside 1 must NOT flag.

    This is the #177 regression: the old 1-sigma gate flagged 5 of 6 passages of
    Sean's own verbatim prose under leave-one-out.
    """
    between = 0.80 - 1.5 * 0.03  # 1.5 sigma below the mattr mean
    flags = analyze.baseline_flags(_metrics(mattr=between), {"metrics": _BASELINE_METRICS})
    assert not any("vocabulary" in f for f in flags)


def test_gate_sigma_is_read_from_the_baseline():
    """The gate shape travels in the baseline, so a rebuild can change it."""
    between = 0.80 - 1.5 * 0.03
    loose = analyze.baseline_flags(_metrics(mattr=between), {"metrics": _BASELINE_METRICS})
    tight = analyze.baseline_flags(
        _metrics(mattr=between),
        {"metrics": _BASELINE_METRICS, "gate": {"sigma": 1.0}},
    )
    assert not any("vocabulary" in f for f in loose)
    assert any("vocabulary" in f for f in tight)


def test_gate_can_re_enable_opener_variety():
    flags = analyze.baseline_flags(
        _metrics(),
        {"metrics": _BASELINE_METRICS,
         "gate": {"flag_metrics": ["cv", "mattr", "first_person_rate",
                                   "opener_other_pct"]}},
    )
    assert any("open the same way" in f for f in flags)


def test_compute_metrics_and_json(tmp_path=None):
    import os
    d = tempfile.mkdtemp()
    p = Path(d) / "draft.md"
    p.write_text("# Title\n\nThe agent ran. It failed. I fixed it. So it goes.\n", encoding="utf-8")
    m = analyze.compute_metrics(str(p))
    assert m["sentence_length"]["n"] >= 3
    assert "lexical_diversity" in m and "pronouns" in m and "openers" in m
    os.remove(p)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL {fn.__name__}: {exc}")
    raise SystemExit(1 if failed else 0)
