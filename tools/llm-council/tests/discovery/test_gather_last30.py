import json
import pytest
from council.discovery.gather.last30 import parse_last30_json, collect_last30

SAMPLE = {
    "topic": "roadmap tools",
    "reddit": [{
        "title": "Roadmap tools all suck", "url": "https://reddit.com/r/pm/abc",
        "subreddit": "ProductManagement", "date": "2026-06-18",
        "engagement": {"score": 120, "num_comments": 30},
        "top_comments": [
            {"score": 88, "date": "2026-06-18", "author": "u/x",
             "excerpt": "Every roadmap tool forces a process my team hates", "url": "https://reddit.com/r/pm/abc/c1"},
        ],
    }],
    "x": [{"text": "Linear falls apart for cross-team OKRs", "url": "https://x.com/h/9",
           "author_handle": "pmhandle", "date": "2026-06-17", "engagement": {"likes": 50}}],
    "web": [{"title": "Why PM tools fail", "url": "https://blog.com/z", "source_domain": "blog.com",
             "snippet": "Teams complain exports break weekly.", "date": "2026-06-15"}],
    "youtube": [{"title": "PM tool rant", "url": "https://youtu.be/v", "channel_name": "PMcast",
                 "date": "2026-06-12", "transcript_highlights": ["the sprint board never syncs"],
                 "engagement": {"views": 9000}}],
    "hackernews": [{"title": "Roadmapping is broken", "url": "https://news.site/a",
                    "hn_url": "https://news.ycombinator.com/item?id=1", "author": "hnuser",
                    "date": "2026-06-10", "engagement": {"score": 200},
                    "top_comments": [{"score": 40, "date": "2026-06-10", "author": "hn2",
                                      "excerpt": "Jira's roadmap view is unusable at scale", "url": "https://news.ycombinator.com/item?id=1#c"}]}],
}


def test_parse_extracts_all_source_types():
    recs = parse_last30_json(SAMPLE)
    types = {r.source_type for r in recs}
    assert {"reddit", "x", "web", "youtube", "hn"} <= types
    reddit_comment = next(r for r in recs if "forces a process" in r.quote)
    assert reddit_comment.url == "https://reddit.com/r/pm/abc/c1"   # comment's own url, not the thread
    assert reddit_comment.engagement == 88
    x_rec = next(r for r in recs if r.source_type == "x")
    assert x_rec.url == "https://x.com/h/9" and x_rec.engagement == 50


def test_parser_tolerates_missing_sections():
    assert parse_last30_json({"topic": "x"}) == []


@pytest.mark.asyncio
async def test_collect_uses_injected_runner_and_parses_json():
    async def fake_runner(topic):
        return json.dumps(SAMPLE)
    recs = await collect_last30("roadmap tools", runner=fake_runner)
    assert len(recs) >= 5


@pytest.mark.asyncio
async def test_collect_returns_empty_on_runner_failure():
    async def boom(topic):
        raise FileNotFoundError("no script")
    assert await collect_last30("x", runner=boom) == []
