"""audit_dr_citations: both source-list shapes, tiers, and the no-network audit path."""
from __future__ import annotations

import json

from scripts.audit_dr_citations import (
    audit_urls,
    is_citable,
    main,
    parse_gemini_sources,
    parse_plain_sources,
    parse_sources,
    tier,
)

GEMINI = """Body.

**Sources:**
1. [openai.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AAA)
2. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/BBB)
"""

PLAIN = """## Sources

```text
1. OpenAI announcement — https://openai.com/index/something
1. https://news.ycombinator.com/item?id=1
2. https://www.youtube.com/watch?v=abc.
- https://arxiv.org/abs/2609.00001
```
"""


def test_gemini_shape_still_parses():
    srcs = parse_gemini_sources(GEMINI)
    assert [s[0] for s in srcs] == [1, 2]
    assert srcs[0][1] == "openai.com"
    assert srcs[0][2].startswith("https://vertexaisearch")


def test_plain_shape_keys_by_written_number_and_runs_bullets():
    srcs = parse_plain_sources(PLAIN)
    assert [(i, u) for i, _, u in srcs] == [
        (1, "https://openai.com/index/something"),
        (1, "https://news.ycombinator.com/item?id=1"),
        (2, "https://www.youtube.com/watch?v=abc"),   # trailing period dropped
        (1, "https://arxiv.org/abs/2609.00001"),      # bullet: running index
    ]
    assert srcs[0][1] == "OpenAI announcement"


def test_plain_parser_skips_gemini_redirects():
    assert parse_plain_sources(GEMINI) == []


def test_parse_sources_autodetects(tmp_path):
    g = tmp_path / "g.md"
    g.write_text(GEMINI)
    p = tmp_path / "p.md"
    p.write_text(PLAIN)
    assert parse_sources(g)[0][2].startswith("https://vertexaisearch")
    assert parse_sources(p)[0][2].startswith("https://openai.com")


def test_tiers_for_news_lane_domains():
    assert tier("https://openai.com/index/x") == "B primary"
    assert tier("https://blog.google/technology/ai/x") == "B primary"
    assert tier("https://gemini.google/overview/video-generation/") == "B primary"
    assert tier("https://metr.org/blog/2026-08-26-x/") == "B primary"
    assert tier("https://news.ycombinator.com/item?id=1") == "D forum/UGC"
    assert tier("https://www.youtube.com/watch?v=1") == "D forum/UGC"
    assert tier("https://arxiv.org/abs/1") == "A academic"
    assert tier("https://www.zdnet.com/article/x") == "C other/trade"
    assert is_citable("B primary") and is_citable("A academic")
    assert not is_citable("C other/trade") and not is_citable("D forum/UGC")


def test_audit_urls_without_network():
    rows = audit_urls([(1, "", "https://openai.com/x"), (2, "", "https://reddit.com/r/x")],
                      resolve_urls=False)
    assert [r["tier"] for r in rows] == ["B primary", "D forum/UGC"]
    assert all(r["status"] is None for r in rows)


def test_main_json_no_resolve(tmp_path, capsys):
    p = tmp_path / "p.md"
    p.write_text(PLAIN)
    assert main(["--json", "--no-resolve", str(p)]) == 0
    out = json.loads(capsys.readouterr().out.strip())
    assert out["totals"] == {"A academic": 1, "B primary": 1, "D forum/UGC": 2}
    assert len(out["citations"]) == 4
