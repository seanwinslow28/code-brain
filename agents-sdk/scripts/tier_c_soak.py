"""Tier C pilot soak — manual-trigger summarization against gemma4_26b-32k @ Alienware.

Topic 20 §Soak validation: 7-day passive observation of gemma4:26b before the
fleet's first Tier C production adoption. Direct httpx probe + chat against
Alienware Ollama (no HybridRouter, no task_map, no launchd schedule).

Pattern E (manual wake): Alienware is reachable 7am–5pm when Sean wakes it
physically. Outside that window the firmware blocks all non-Microsoft-signed
wake events (project_alienware_wake_impossible.md). The script fails fast on
unreachable — there is no WoL retry, no fallback target. The script's exit
status IS the operating contract.

Usage:
    PYTHONPATH=. .venv/bin/python3 scripts/tier_c_soak.py --workload summarize
    PYTHONPATH=. .venv/bin/python3 scripts/tier_c_soak.py --workload summarize --dry-run
    PYTHONPATH=. .venv/bin/python3 scripts/tier_c_soak.py --workload summarize \
        --article 20_projects/research/2026-05-21-topic-20-fleet-model-refresh-benchmarks.md

Output:
    vault/health/tier-c-soak-{YYYY-MM-DD}.jsonl   — one record appended per run
    vault/health/tier-c-soak/{YYYY-MM-DD}/{slug}.md — full LLM response per run

Decision record + soak protocol: /Users/seanwinslow/.claude/plans/we-re-continuing-topic-20-generic-kitten.md
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.config import load_config  # noqa: E402


ALIENWARE_HOST = "http://192.168.68.201:11434"
MODEL_TAG = "gemma4_26b-32k:latest"
PROBE_TIMEOUT = 3.0
CHAT_TIMEOUT = 300.0

RESEARCH_SUBDIR = "20_projects/research"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str, max_len: int = 80) -> str:
    s = _SLUG_RE.sub("-", text.lower()).strip("-")
    return (s or "untitled")[:max_len]


def probe_alienware() -> bool:
    try:
        r = httpx.get(f"{ALIENWARE_HOST}/api/tags", timeout=PROBE_TIMEOUT)
        return r.status_code == 200
    except (httpx.ConnectError, httpx.ReadTimeout, httpx.ConnectTimeout, httpx.RequestError):
        return False


def pick_source_article(vault_root: Path, override_rel: str | None) -> Path:
    if override_rel:
        p = (vault_root / override_rel).resolve()
        if not p.exists():
            sys.exit(f"override article not found: {p}")
        return p
    candidates = sorted((vault_root / RESEARCH_SUBDIR).glob("*.md"))
    if not candidates:
        sys.exit(f"no research articles under {vault_root / RESEARCH_SUBDIR}")
    return random.choice(candidates)


def size_num_ctx(article_chars: int) -> int:
    # ~3 chars/token estimate, round up to 4K boundary, clamp [8192, 32768].
    raw_tokens = article_chars // 3
    rounded = ((raw_tokens + 4095) // 4096) * 4096
    return max(8192, min(32768, rounded))


def build_prompt(article_body: str) -> str:
    return (
        "You are summarizing a long-form research article for a personal "
        "knowledge base. Write a faithful 3-paragraph summary: paragraph 1 "
        "states the thesis; paragraph 2 lists the key supporting points with "
        "specific examples preserved; paragraph 3 captures the open questions "
        "or recommendations. Do not invent facts not present in the source.\n\n"
        f"=== ARTICLE ===\n{article_body}\n=== END ARTICLE ==="
    )


def run_chat(prompt: str, num_ctx: int) -> dict:
    body = {
        "model": MODEL_TAG,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "options": {"num_ctx": num_ctx, "temperature": 0.0},
    }
    r = httpx.post(f"{ALIENWARE_HOST}/api/chat", json=body, timeout=CHAT_TIMEOUT)
    r.raise_for_status()
    return r.json()


def next_unused_path(out_dir: Path, base_slug: str) -> Path:
    p = out_dir / f"{base_slug}.md"
    n = 2
    while p.exists():
        p = out_dir / f"{base_slug}-{n}.md"
        n += 1
    return p


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tier C pilot soak — gemma4_26b-32k @ Alienware Pattern E.",
    )
    parser.add_argument("--workload", choices=("summarize",), default="summarize",
                        help="Pilot workload (only 'summarize' supported today).")
    parser.add_argument("--article", default=None,
                        help="Vault-relative article path override (skip random pick).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Probe + pick + size num_ctx + print plan; no chat call.")
    args = parser.parse_args()

    cfg = load_config()

    if not probe_alienware():
        sys.stderr.write(
            f"Alienware unreachable at {ALIENWARE_HOST} within {PROBE_TIMEOUT:.0f}s.\n"
            "Pattern E says wake it manually (mouse jiggle, ~7am).\n"
            "Try again 7am–5pm Eastern. NOT firing WoL (non-functional on this hardware).\n"
        )
        return 2

    src = pick_source_article(cfg.vault_root, args.article)
    body = src.read_text(encoding="utf-8", errors="replace")
    num_ctx = size_num_ctx(len(body))
    prompt = build_prompt(body)

    src_rel = src.relative_to(cfg.vault_root).as_posix()

    if args.dry_run:
        print(
            f"[soak][dry-run] would summarize {src_rel} "
            f"({len(body)} chars, num_ctx={num_ctx}, model={MODEL_TAG})"
        )
        return 0

    start = time.monotonic()
    resp = run_chat(prompt, num_ctx)
    wall = time.monotonic() - start

    content = resp.get("message", {}).get("content", "") or ""
    today = date.today().isoformat()
    out_dir = cfg.vault_root / "health" / "tier-c-soak" / today
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = next_unused_path(out_dir, slugify(src.stem))
    out_path.write_text(content, encoding="utf-8")

    eval_count = int(resp.get("eval_count", 0) or 0)
    eval_duration_ns = int(resp.get("eval_duration", 0) or 0)
    eval_duration_s = eval_duration_ns / 1e9
    tps = round(eval_count / max(eval_duration_s, 0.001), 1) if eval_count else 0.0

    record = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "model": MODEL_TAG,
        "host": ALIENWARE_HOST,
        "workload": args.workload,
        "source_path": src_rel,
        "source_chars": len(body),
        "num_ctx": num_ctx,
        "response_path": out_path.relative_to(cfg.vault_root).as_posix(),
        "response_chars": len(content),
        "wall_secs": round(wall, 2),
        "eval_count": eval_count,
        "eval_duration_secs": round(eval_duration_s, 2),
        "tokens_per_sec": tps,
        "ok": bool(content.strip()),
    }
    manifest = cfg.vault_root / "health" / f"tier-c-soak-{today}.jsonl"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    print(
        f"[soak] {src.name} → {out_path.name} | "
        f"{len(content)}c in {wall:.1f}s | {tps} tok/s | "
        f"manifest={manifest.relative_to(cfg.vault_root).as_posix()}"
    )
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
