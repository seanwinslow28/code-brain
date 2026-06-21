import pytest
from datetime import datetime, timezone
from council.discovery.gather.qa import collect_qa, _epoch_to_date


def test_epoch_to_date_roundtrips():
    epoch = int(datetime(2026, 6, 18, tzinfo=timezone.utc).timestamp())
    assert _epoch_to_date(epoch) == "2026-06-18"
    assert _epoch_to_date(None) == ""


@pytest.mark.asyncio
async def test_collect_qa_builds_records_and_unescapes_titles():
    async def search(query):
        return [{"link": "https://stackoverflow.com/q/1",
                 "title": "Why does &quot;export&quot; hang forever?",
                 "score": 17, "creation_date": int(datetime(2026, 6, 10, tzinfo=timezone.utc).timestamp())}]
    recs = await collect_qa(topic="export hang", search=search)
    assert len(recs) == 1
    r = recs[0]
    assert r.source_type == "qa"
    assert r.url == "https://stackoverflow.com/q/1"
    assert r.engagement == 17
    assert r.date == "2026-06-10"
    assert '"export"' in r.quote   # HTML entities unescaped


@pytest.mark.asyncio
async def test_collect_qa_empty_without_provider():
    assert await collect_qa(topic="x", search=None) == []
