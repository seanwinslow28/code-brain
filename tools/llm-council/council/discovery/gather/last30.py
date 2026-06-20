"""Collector: shell out to last30days --agent and parse its compact output into evidence."""

import asyncio
import re
import shutil
from pathlib import Path

from council.discovery.evidence import EvidenceRecord

_URL = re.compile(r"https?://\S+")
_ENGAGE = re.compile(r"\[(\d+)\s*(?:pts|likes)")
_QUOTE = re.compile(r'"([^"]{12,})"')
_SECTION = {"reddit": "reddit", "x": "x", "youtube": "youtube", "hn": "hn"}


def parse_last30_output(text: str) -> list[EvidenceRecord]:
    records: list[EvidenceRecord] = []
    section = "web"
    cur_url = cur_name = ""
    cur_engage = 0
    for raw in text.splitlines():
        line = raw.strip()
        low = line.lower()
        for key, st in _SECTION.items():
            if low.startswith(("🟠", "🔵", "🔴", "🟡")) and key in low:
                section = st
        m = _URL.search(line)
        if m:
            cur_url = m.group(0).rstrip(").,")
            cur_name = line.split()[0] if line.split() else section
            e = _ENGAGE.search(line)
            cur_engage = int(e.group(1)) if e else 0
        q = _QUOTE.search(line)
        if q and cur_url:
            records.append(EvidenceRecord(
                source_type=section, source_name=cur_name, url=cur_url,
                date="", quote=q.group(1), engagement=cur_engage,
            ))
    return records


def _find_last30_script() -> Path:
    for cand in (
        Path.home() / ".claude/skills/last30days/scripts/last30days.py",
        Path.home() / ".agents/skills/last30days/scripts/last30days.py",
    ):
        if cand.exists():
            return cand
    raise FileNotFoundError("last30days script not found in ~/.claude or ~/.agents skills.")


async def _subprocess_runner(topic: str) -> str:
    script = _find_last30_script()
    py = shutil.which("python3") or "python3"
    proc = await asyncio.create_subprocess_exec(
        py, str(script), topic, "--agent", "--emit=compact", "--no-native-web",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    out, _ = await asyncio.wait_for(proc.communicate(), timeout=300)
    return out.decode("utf-8", "replace")


async def collect_last30(topic: str, runner=_subprocess_runner) -> list[EvidenceRecord]:
    try:
        text = await runner(topic)
    except (FileNotFoundError, asyncio.TimeoutError):
        return []
    return parse_last30_output(text)
