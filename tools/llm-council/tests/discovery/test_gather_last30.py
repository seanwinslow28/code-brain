# tests/discovery/test_gather_last30.py
import pytest
from council.discovery.gather.last30 import parse_last30_output, collect_last30


SAMPLE = """\
🟠 Reddit
r/ProductManagement (score:120) https://reddit.com/r/pm/abc [120pts, 30cmt]
title: Roadmap tools all suck
💬 Top comment (88 upvotes): "Every roadmap tool forces a process my team hates"

🔵 X
@pmhandle (score:50) https://x.com/pmhandle/status/9 [50likes, 5rt]
"Linear is great until you need cross-team OKRs, then it falls apart"
"""


def test_parse_extracts_reddit_and_x_records():
    recs = parse_last30_output(SAMPLE)
    by_type = {r.source_type for r in recs}
    assert "reddit" in by_type and "x" in by_type
    reddit = next(r for r in recs if r.source_type == "reddit")
    assert reddit.url == "https://reddit.com/r/pm/abc"
    assert "roadmap tool forces a process" in reddit.quote
    assert reddit.engagement == 120


@pytest.mark.asyncio
async def test_collect_uses_injected_runner():
    async def fake_runner(topic):
        return SAMPLE
    recs = await collect_last30("roadmap tools", runner=fake_runner)
    assert len(recs) >= 2
