"""Collector: shell out to last30days --emit=json and parse its report into evidence.

Real script: ~/.claude/plugins/marketplaces/last30days-skill/scripts/last30days.py
JSON shape: report.to_dict() from that skill's lib/schema.py.
"""

import asyncio
import json
import shutil
from pathlib import Path

from council.discovery.evidence import EvidenceRecord


def _eng(item: dict, *keys: str) -> int:
    e = item.get("engagement") or {}
    for k in keys:
        v = e.get(k)
        if v:
            return int(v)
    return 0


def parse_last30_json(data: dict) -> list[EvidenceRecord]:
    recs: list[EvidenceRecord] = []

    for it in data.get("reddit", []):
        sub = it.get("subreddit", "")
        name = f"r/{sub}" if sub else "reddit"
        url, date = it.get("url", ""), it.get("date") or ""
        if url and it.get("title"):
            recs.append(EvidenceRecord("reddit", name, url, date, it["title"], _eng(it, "score", "num_comments")))
        for c in it.get("top_comments", []):
            cu, ex = c.get("url") or url, c.get("excerpt", "")
            if cu and ex:
                recs.append(EvidenceRecord("reddit", name, cu, c.get("date") or date, ex, int(c.get("score") or 0)))

    for it in data.get("x", []):
        url, txt = it.get("url", ""), it.get("text", "")
        if url and txt:
            recs.append(EvidenceRecord("x", it.get("author_handle", "") or "x", url, it.get("date") or "", txt, _eng(it, "likes")))

    for it in data.get("web", []):
        url, sn = it.get("url", ""), it.get("snippet", "")
        if url and sn:
            recs.append(EvidenceRecord("web", it.get("source_domain", "") or "web", url, it.get("date") or "", sn, 0))

    for it in data.get("youtube", []):
        url = it.get("url", "")
        for hl in it.get("transcript_highlights", []) or []:
            if url and hl:
                recs.append(EvidenceRecord("youtube", it.get("channel_name", "") or "youtube", url, it.get("date") or "", hl, _eng(it, "views")))

    for it in data.get("hackernews", []):
        url = it.get("url", "") or it.get("hn_url", "")
        name = it.get("author", "") or "hn"
        if url and it.get("title"):
            recs.append(EvidenceRecord("hn", name, url, it.get("date") or "", it["title"], _eng(it, "score", "num_comments")))
        for c in it.get("top_comments", []):
            cu, ex = c.get("url") or url, c.get("excerpt", "")
            if cu and ex:
                recs.append(EvidenceRecord("hn", name, cu, c.get("date") or "", ex, int(c.get("score") or 0)))

    return recs


def _find_last30_script() -> Path:
    candidates = [
        Path.home() / ".claude/plugins/marketplaces/last30days-skill/scripts/last30days.py",
        Path.home() / ".claude/skills/last30days/scripts/last30days.py",
        Path.home() / ".agents/skills/last30days/scripts/last30days.py",
    ]
    for cand in candidates:
        if cand.exists():
            return cand
    raise FileNotFoundError("last30days script not found in plugin marketplace or skills dirs.")


async def _subprocess_runner(topic: str) -> str:
    script = _find_last30_script()
    py = shutil.which("python3") or "python3"
    proc = await asyncio.create_subprocess_exec(
        py, str(script), topic, "--emit=json", "--quick", "--no-native-web",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    out, _ = await asyncio.wait_for(proc.communicate(), timeout=300)
    return out.decode("utf-8", "replace")


async def collect_last30(topic: str, runner=_subprocess_runner) -> list[EvidenceRecord]:
    try:
        text = await runner(topic)
    except (FileNotFoundError, asyncio.TimeoutError):
        return []
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return []
    return parse_last30_json(data)
