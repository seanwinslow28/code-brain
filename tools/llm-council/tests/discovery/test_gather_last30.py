import json
import pytest
from council.discovery.gather.last30 import parse_last30_json, collect_last30, _last30_env


def test_last30_env_forces_include_sources(monkeypatch):
    # Upstream last30days defaults INCLUDE_SOURCES=None then calls .split(',') on it → crash.
    # We force a non-null value (reddit,hackernews work keyless) via the subprocess env.
    monkeypatch.setenv("SOME_INHERITED_VAR", "keepme")
    env = _last30_env()
    assert env["INCLUDE_SOURCES"] == "reddit,hackernews"
    assert env["SOME_INHERITED_VAR"] == "keepme"   # preserves inherited env (API keys, PATH, etc.)

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


@pytest.mark.asyncio
async def test_collect_breadcrumb_on_non_json(capsys):
    async def runner(topic):
        return "AttributeError: 'NoneType' object has no attribute 'split'"
    recs = await collect_last30("x", runner=runner)
    assert recs == []
    assert "[last30]" in capsys.readouterr().err


@pytest.mark.asyncio
async def test_collect_empty_output_returns_empty(capsys):
    async def runner(topic):
        return "   \n"
    recs = await collect_last30("x", runner=runner)
    assert recs == []


@pytest.mark.asyncio
async def test_subprocess_runner_kills_and_reaps_on_timeout(monkeypatch):
    import asyncio as _asyncio
    from council.discovery.gather import last30

    flags = {"kill": False, "wait": False}

    class _FakeProc:
        returncode = -9
        async def communicate(self):
            await _asyncio.sleep(999)  # hang → forces the timeout branch
        def kill(self):
            flags["kill"] = True
        async def wait(self):
            flags["wait"] = True

    async def fake_exec(*a, **k):
        return _FakeProc()

    real_wait_for = _asyncio.wait_for
    async def fast_wait_for(aw, timeout):
        # use the REAL wait_for semantics (genuine cancellation of communicate()) but fast
        return await real_wait_for(aw, timeout=0.05)

    monkeypatch.setattr(last30.asyncio, "create_subprocess_exec", fake_exec)
    monkeypatch.setattr(last30.asyncio, "wait_for", fast_wait_for)
    monkeypatch.setattr(last30, "_find_last30_script", lambda: "/tmp/fake-last30.py")

    with pytest.raises(_asyncio.TimeoutError):
        await last30._subprocess_runner("x")
    assert flags["kill"] is True and flags["wait"] is True  # child reaped, not orphaned


@pytest.mark.asyncio
async def test_collect_last30_composes_segment_into_subject():
    seen = {}
    async def runner(subject):
        seen["s"] = subject
        return "{}"
    await collect_last30("pm tools", runner=runner, segment="enterprise")
    assert seen["s"] == "pm tools enterprise"


@pytest.mark.asyncio
async def test_subprocess_runner_breadcrumb_on_empty_stdout(monkeypatch, capsys):
    from council.discovery.gather import last30

    class _FakeProc:
        returncode = 1
        async def communicate(self):
            return (b"", b"Traceback (most recent call last):\nAttributeError: 'NoneType' object has no attribute 'split'")
        def kill(self):
            pass
        async def wait(self):
            pass

    async def fake_exec(*a, **k):
        return _FakeProc()

    monkeypatch.setattr(last30.asyncio, "create_subprocess_exec", fake_exec)
    monkeypatch.setattr(last30, "_find_last30_script", lambda: "/tmp/fake-last30.py")

    out = await last30._subprocess_runner("x")
    assert out == ""
    err = capsys.readouterr().err
    assert "[last30]" in err and "empty stdout" in err   # stderr tail breadcrumb fired
