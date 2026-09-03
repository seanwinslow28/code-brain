#!/usr/bin/env python3
"""Resolve + tier-classify citations, from either of two source-list shapes.

1. The numbered **Sources:** list at the foot of a gemini_dr report — Google
   grounding redirects, followed to their real URL before classification.
2. A plain-URL sources list (#239, the Oracle's listening report): numbered or
   bulleted lines carrying an https URL, inside or outside a code fence.

The shape is auto-detected per file: Gemini redirects first, plain URLs if there
are none. Read-only; no writes to the vault. Tiers: A academic, B primary
(the vendor, the code, the thing itself), C other/trade, D forum/UGC.

    audit_dr_citations.py <report.md> [...]
    audit_dr_citations.py --json <report.md>          # one JSON object per file
    audit_dr_citations.py --no-resolve <report.md>    # classify the written URL, no network
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

# Tier A: peer-reviewed / preprint / academic venue
TIER_A = (
    "arxiv.org", "neurips.cc", "aclanthology.org", "openreview.net", "acm.org",
    "ieee.org", "ieeexplore", "nature.com", "science.org", "sciencedirect.com",
    "springer.com", "link.springer", "pubmed", "ncbi.nlm.nih.gov", "doi.org",
    "cambridge.org", "tandfonline.com", "wiley.com", "mdpi.com", "plos.org",
    "semanticscholar.org", "researchgate.net", "biorxiv.org", "ssrn.com",
)
# Tier B: primary vendor / product / code — the thing itself. The second row is
# the first-party news surfaces the Oracle's news lane (#239) meets every week:
# a vendor announcing its own release is primary for what the release does.
TIER_B = (
    "github.com", "huggingface.co", "anthropic.com", "openai.com",
    "ai.google.dev", "cloud.google.com", "deepmind.google", "databricks.com",
    "mlflow.org", "langfuse.com", "braintrust.dev", "confident-ai.com",
    "docs.", "developer.", "pypi.org", "npmjs.com", "readthedocs",
    "blog.google", "ai.meta.com", "microsoft.com", "nvidia.com", "mistral.ai",
    "x.ai", "deepseek.com", "apple.com", "aws.amazon.com", "amazon.science",
    "qwen.ai", "perplexity.ai", "stability.ai", "runwayml.com", "midjourney.com",
    "elevenlabs.io", "cursor.com", "github.blog", "ollama.com",
    "modelcontextprotocol.io", "cohere.com", "together.ai", "z.ai", "gemini.google",
    "metr.org", "redwoodresearch.org",   # investigators publishing their own findings
)
# Tier D: forum / UGC / self-published — leads only, never citable alone.
# news.ycombinator.com is a forum: the story it links to may be primary, the
# thread is not.
TIER_D = (
    "reddit.com", "medium.com", "substack.com", "linkedin.com", "quora.com",
    "dev.to", "hashnode", "x.com", "twitter.com", "facebook.com", "youtube.com",
    "youtu.be", "tiktok.com", "blogspot", "wordpress.com", "wixsite", "pinterest",
    "news.ycombinator.com", "bsky.app",
)

_GEMINI_RE = re.compile(r"^(\d+)\.\s*\[([^\]]+)\]\((https://vertexaisearch[^)]+)\)", re.M)
# A numbered or bulleted line carrying a URL: `1. Title — https://…`, `- https://…`,
# `3) https://…`. The label is whatever precedes the URL.
_PLAIN_RE = re.compile(r"^\s*(?:(\d+)[.)]|[-*•])\s*(.*?)\s*(https?://[^\s)\]>]+)", re.M)


def tier(url: str) -> str:
    u = url.lower()
    host = urlparse(u).netloc
    if any(d in u for d in TIER_A):
        return "A academic"
    if any(d in host or u.startswith(f"https://{d}") for d in TIER_B):
        return "B primary"
    if any(d in host for d in TIER_D):
        return "D forum/UGC"
    return "C other/trade"


def is_citable(t: str) -> bool:
    """Tier A or B: a figure may be spoken with this source behind it."""
    return t.startswith(("A ", "B "))


def resolve(item):
    idx, label, url = item
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return idx, label, r.geturl(), r.status
    except urllib.error.HTTPError as e:
        # 403/401 still reveal the final URL after redirects
        return idx, label, getattr(e, "url", url), e.code
    except Exception as e:  # noqa: BLE001
        return idx, label, f"UNRESOLVED ({type(e).__name__})", 0


def parse_gemini_sources(text: str) -> list[tuple[int, str, str]]:
    return [(int(m.group(1)), m.group(2), m.group(3)) for m in _GEMINI_RE.finditer(text)]


def parse_plain_sources(text: str) -> list[tuple[int, str, str]]:
    """Numbered or bulleted lines with a plain URL. Fences are ordinary lines here.

    A numbered line keeps its number (so several lines may share one index —
    the listening report keys sources by item that way); a bulleted line takes
    the next running index.
    """
    out: list[tuple[int, str, str]] = []
    running = 0
    for m in _PLAIN_RE.finditer(text):
        url = m.group(3).rstrip(".,;")
        if "vertexaisearch" in url:
            continue
        if m.group(1):
            idx = int(m.group(1))
        else:
            running += 1
            idx = running
        label = m.group(2).strip().rstrip("—–-: ").strip()
        out.append((idx, label, url))
    return out


def parse_sources(path: Path) -> list[tuple[int, str, str]]:
    text = path.read_text(encoding="utf-8")
    return parse_gemini_sources(text) or parse_plain_sources(text)


def audit_urls(items: list[tuple[int, str, str]], resolve_urls: bool = True) -> list[dict]:
    """Classify each (idx, label, url). With resolve_urls the redirect chain is followed."""
    if resolve_urls:
        with ThreadPoolExecutor(max_workers=12) as ex:
            results = sorted(ex.map(resolve, items), key=lambda r: r[0])
    else:
        results = [(idx, label, url, None) for idx, label, url in items]
    out = []
    for idx, label, final, code in results:
        t = tier(final) if code != 0 else "X unresolved"
        out.append({"idx": idx, "label": label, "url": final, "status": code, "tier": t})
    return out


def _totals(rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["tier"]] = counts.get(r["tier"], 0) + 1
    return counts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true", help="emit one JSON object per file")
    ap.add_argument("--no-resolve", action="store_true", help="classify the written URL; no network")
    args = ap.parse_args(argv)

    for path in args.paths:
        srcs = parse_sources(path)
        rows = audit_urls(srcs, resolve_urls=not args.no_resolve)
        if args.json:
            print(json.dumps({"file": str(path), "citations": rows, "totals": _totals(rows)}))
            continue
        print(f"\n{'='*78}\n{path.name}\n{len(srcs)} citations\n{'='*78}")
        for r in rows:
            code = r["status"] if r["status"] is not None else "-"
            print(f"[{r['idx']:>3}] {r['tier']:<14} {code:<4} {r['url'][:112]}")
        print(f"\n--- {path.name} tier totals ---")
        total = len(rows) or 1
        counts = _totals(rows)
        for t in sorted(counts):
            print(f"  {t:<14} {counts[t]:>3}  ({counts[t]*100//total}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
