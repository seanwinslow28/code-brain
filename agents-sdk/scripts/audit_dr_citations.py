#!/usr/bin/env python3
"""Resolve + tier-classify Gemini DR grounding-redirect citations.

Reads the numbered **Sources:** list at the foot of a gemini_dr report,
follows each Google grounding redirect to its real URL, and classifies the
destination by evidence tier. Read-only; no writes to the vault.
"""
from __future__ import annotations

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
# Tier B: primary vendor / product / code — the thing itself
TIER_B = (
    "github.com", "huggingface.co", "anthropic.com", "openai.com",
    "ai.google.dev", "cloud.google.com", "deepmind.google", "databricks.com",
    "mlflow.org", "langfuse.com", "braintrust.dev", "confident-ai.com",
    "docs.", "developer.", "pypi.org", "npmjs.com", "readthedocs",
)
# Tier D: forum / UGC / self-published — leads only, never citable alone
TIER_D = (
    "reddit.com", "medium.com", "substack.com", "linkedin.com", "quora.com",
    "dev.to", "hashnode", "x.com", "twitter.com", "facebook.com", "youtube.com",
    "tiktok.com", "blogspot", "wordpress.com", "wixsite", "pinterest",
)


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


def parse_sources(path: Path):
    text = path.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"^(\d+)\.\s*\[([^\]]+)\]\((https://vertexaisearch[^)]+)\)", text, re.M):
        out.append((int(m.group(1)), m.group(2), m.group(3)))
    return out


def main() -> int:
    for path_str in sys.argv[1:]:
        path = Path(path_str)
        srcs = parse_sources(path)
        print(f"\n{'='*78}\n{path.name}\n{len(srcs)} citations\n{'='*78}")
        with ThreadPoolExecutor(max_workers=12) as ex:
            results = sorted(ex.map(resolve, srcs))

        counts: dict[str, int] = {}
        for idx, label, final, code in results:
            t = tier(final) if code else "X unresolved"
            counts[t] = counts.get(t, 0) + 1
            print(f"[{idx:>3}] {t:<14} {code:<4} {final[:112]}")

        print(f"\n--- {path.name} tier totals ---")
        total = len(results) or 1
        for t in sorted(counts):
            print(f"  {t:<14} {counts[t]:>3}  ({counts[t]*100//total}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
