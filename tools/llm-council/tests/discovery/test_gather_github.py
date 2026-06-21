import pytest
from council.discovery.gather.github import collect_github, _repo_from_html_url


def test_repo_from_html_url():
    assert _repo_from_html_url("https://github.com/anthropics/claude-code/issues/35357") == "anthropics/claude-code"
    assert _repo_from_html_url("not-a-github-url") == "github"


@pytest.mark.asyncio
async def test_collect_github_builds_records_from_issues():
    async def search(query):
        return [
            {"html_url": "https://github.com/owner/repo/issues/1", "title": "Export silently drops rows",
             "body": "details here", "created_at": "2026-06-18T10:00:00Z", "reactions": {"total_count": 42}},
            {"html_url": "", "title": "missing url → skipped", "created_at": "2026-06-01T00:00:00Z"},
        ]
    recs = await collect_github(topic="data export", search=search)
    assert len(recs) == 1
    r = recs[0]
    assert r.source_type == "github" and r.source_name == "owner/repo"
    assert r.url == "https://github.com/owner/repo/issues/1"
    assert r.date == "2026-06-18" and r.engagement == 42
    assert r.quote == "Export silently drops rows"


@pytest.mark.asyncio
async def test_collect_github_empty_when_no_provider():
    assert await collect_github(topic="x", search=None) == []
