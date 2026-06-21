# fusion-discovery-council — Phase 4 (Extended Collectors + Fetch Hardening) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Widen Stage-1 GATHER beyond Sonar + Brave web + last30 with three free, fabrication-gate-compatible collectors (review-sites + competitor-weakness mining, GitHub Issues, Stack Exchange Q&A), harden the fetch surface those collectors share (SSRF/redirect allow-list), strengthen Sonar evidence to verbatim quotes, and fold the two deferred §7b code nits.

**Architecture:** Pure additive hardening of the existing `tools/llm-council/council/discovery/` subpackage — no new stages, no new lens, no Fusion change. Three new `gather/<source>.py` collectors follow the existing `gather/web.py` injection-seam pattern (an injectable `search=`/`fetch=` provider, default-wired to a free API/Brave) and slot into `gather_evidence()` gated by new `TierConfig` flags per the spec §6 matrix. Every new record carries a real URL + a verbatim quote so the Stage-3 fabrication gate stays the sole arbiter. All new collectors are **free** (GitHub Search API, Stack Exchange API, Brave free-tier site-targeted search), so no new billable call is introduced — the cost-integrity invariant is enforced by a regression guard + a documented threading recipe for the day a paid collector lands.

**Tech Stack:** Python ≥3.10, `httpx` (async), `click`, `rich`, `pytest` + `pytest-asyncio` + `pytest-httpx`. OpenRouter Fusion + Sonar; Brave Search API (`site:` operators); GitHub Search API (`/search/issues`); Stack Exchange API (`/2.3/search/advanced`); stdlib `ipaddress`/`socket`/`html`/`datetime`. Source-of-truth docs: the [spec](2026-06-20-fusion-discovery-council-design.md) (§6 coverage matrix, §3 non-goals), the [Phase 3 field report](../../../tools/llm-council/council/docs/2026-06-20-fusion-discovery-council-phase3-field-report.md) §7c, and [FUSION_SCHEMA.md](../../../tools/llm-council/council/discovery/FUSION_SCHEMA.md).

## Global Constraints

- Python floor stays `>=3.10`. Co-located subpackage; **reuse the council spine (`client.py`, `budget.py`)** — do **not** add a second HTTP client or a second spend file.
- **Run all commands from `tools/llm-council/`.** The test command is **`uv run --extra dev python -m pytest -v`** — plain `uv run pytest` does NOT work (pytest lives in the `dev` extra). Baseline after the Phase-1–3 merge: **93 passed, 1 skipped**; every task must keep the full suite green (no regressions) on top of its new tests.
- **The fabrication gate (`verify.py`) is SACRED — never weaken it.** Every ledger pain point must trace to a quote whose URL is in the evidence bundle (`needle in hay` containment only — do not loosen). Every new collector must emit records with a real, fetched URL and a verbatim quote, or its evidence will (correctly) be dropped by Stage 3.
- The skill **never** `git add`s the `vault/` directory (CLAUDE.md rule 8 — Obsidian-Git owns vault commits).
- Verified OpenRouter model IDs (live 2026-06-20): `~google/gemini-pro-latest` (tilde = floating alias; bare form 400s), `mistralai/mistral-medium-3-5` (hyphen; dotted form 400s), plus `anthropic/claude-opus-4.7`, `openai/gpt-5.5`, `x-ai/grok-4.3`, `deepseek/deepseek-v4-pro`, all Sonar variants. Do not reintroduce the invalid forms.
- Caps unchanged: per-run quick **$0.50** / standard **$1.50** / deep **$4.00**; discovery daily **$10** / monthly **$50** (tagged `tool="discovery"`), isolated from council's $7/$40 (tagged `tool="council"`). Phase 4 keeps these and adds a **mandatory live standard+deep cost re-check** (Task 9) — bump only if a real run exceeds the cap.
- **Cost-integrity theme: never bill a provider and record $0.** All Phase-4 collectors are free, so no gather-stage billing is introduced. The invariant is preserved by a regression guard + a documented threading recipe (Task 9); if a future collector bills, thread its incurred cost into a typed failure exactly as `FusionError.cost → DiscoveryFailed.cost_usd → record_spend` already does.
- Env keys in the repo-root `.env` (gitignored, loaded via dotenv): `OPENROUTER_API_KEY`, `BRAVE_API_KEY`, `GITHUB_TOKEN` (optional — raises the GitHub API rate limit; the collector degrades to unauthenticated without it), `SCRAPECREATORS_API_KEY`, optional `EXA_API_KEY`. Stack Exchange needs **no** key.
- last30 live yield is still blocked by the upstream `INCLUDE_SOURCES=null` crash (external config; the collector degrades safely to `[]`). Note it; don't re-litigate. GATHER today = Sonar + Brave web live; Phase 4 adds reviews/github/qa on standard/deep.
- No new skill/agent/script file is created (collectors are modules inside the existing CLI), so **no CLAUDE.md/README count-table change is required** — only a CHANGELOG entry + a SKILL.md surface update (Task 9).

---

## Design decisions locked for this phase (Sean, 2026-06-20)

- **Collector scope:** ship **3 gate-fit free collectors** — review-sites + competitor-weakness mining, GitHub Issues, Stack Exchange Q&A. **Defer** demand-intent (Google autocomplete/PAA produces queries, not URL-anchored quotes → would be dropped by VERIFY; better modeled later as query-expansion feeding web/reviews), trend-velocity (no clean free API), and Quora (heavy anti-scraping).
- **Fetch path:** **free** — Brave site-targeted search + the SSRF-hardened `_simple_fetch`. No Firecrawl/Apify (spec §3). Because nothing bills at gather time, the cost-integrity work stays a documented invariant + a $0-spend regression guard (not a `GatherFailed.cost_usd` plumbing task).
- **Tier gating (spec §6 matrix):** `quick` stays lean (sonar + web + last30). `standard` adds **reviews + github**. `deep` adds **reviews + github + qa**.
- **Caps:** keep $0.50 / $1.50 / $4.00; add a mandatory live standard+deep cost re-check (Task 9); bump only if a real run exceeds a cap.

---

## File Structure (touched in this plan)

```
tools/llm-council/council/discovery/gather/web.py       # MODIFY: SSRF/redirect allow-list in _simple_fetch (Task 1)
tools/llm-council/council/discovery/tiers.py            # MODIFY: add reviews/github/qa flags + matrix (Task 2)
tools/llm-council/council/discovery/gather/reviews.py   # CREATE: review-sites + competitor-weakness collector (Task 3)
tools/llm-council/council/discovery/gather/github.py    # CREATE: GitHub Issues collector (Task 4)
tools/llm-council/council/discovery/gather/qa.py        # CREATE: Stack Exchange Q&A collector (Task 5)
tools/llm-council/council/discovery/gather/sonar.py     # MODIFY: verbatim-quote-per-URL hardening (Task 6)
tools/llm-council/council/discovery/gather/__init__.py  # MODIFY: slot new collectors + sonar fetch opt-in, tier-gated (Task 7)
tools/llm-council/council/discovery/fusion.py           # MODIFY: _first_json_object scan-forward robustness (Task 8)
tools/llm-council/council/discovery/gather/last30.py    # MODIFY: timeout → module constant (Task 8)
.claude/skills/fusion-discovery-council/SKILL.md        # MODIFY: collectors now live (Task 9)
CHANGELOG.md                                            # MODIFY: Phase 4 entry (Task 9)
tools/llm-council/tests/discovery/*                     # new + updated tests per task
```

**Sequencing note (file overlap):** `gather/__init__.py` is touched by Task 7 only; `web.py` by Task 1 only (its public helpers `_default_brave_search`/`_simple_fetch`/`extract_quotes` are imported, not re-edited, by Tasks 3 and 6); `gather/sonar.py` by Task 6 only. Run tasks **sequentially** in the order below. Task 1 must precede Tasks 3/6/7 because they widen the fetch surface `_simple_fetch` guards.

---

## Task 1: SSRF / redirect allow-list in `_simple_fetch`

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/web.py`
- Modify: `tools/llm-council/tests/discovery/test_gather_web.py` (one existing test → literal IP; add SSRF tests)

**Interfaces:**
- Produces (new): `_is_safe_fetch_url(url: str, *, resolve=_resolve_ips) -> bool` and `_resolve_ips(host: str) -> list[str]`. `_simple_fetch` keeps its signature `(url: str, timeout: float = 20.0) -> str` but now validates scheme + resolved IP of the initial URL **and every redirect hop** before connecting (manual redirect following).

**Context:** Today `_simple_fetch` (web.py:60) does `follow_redirects=True` with no scheme/host allow-list — a recorded Phase-2/3 deferral, fine while fetch targets came only from Brave. Phase 4's review-sites collector fans `_simple_fetch` out across a wider, less-trusted URL surface, so this hardening must land first (Phase-3 §7c: "do this in the same phase that adds the new collectors").

- [ ] **Step 1: Write the failing tests**

Replace the existing `test_simple_fetch_strips_html` (it uses a hostname, which would now hit real DNS) with a literal-IP version, and add the SSRF tests. In `tests/discovery/test_gather_web.py`, change the import line and the one test, then append the new tests:

```python
# update the existing import block at the top of the file to include the new helpers:
from council.discovery.gather.web import (
    collect_web,
    extract_quotes,
    _default_brave_search,
    _simple_fetch,
    _is_safe_fetch_url,
)
```

Replace `test_simple_fetch_strips_html` with (literal public IP → no DNS in the test):

```python
@pytest.mark.asyncio
async def test_simple_fetch_strips_html(httpx_mock):
    httpx_mock.add_response(url="http://93.184.216.34/p",
                            text="<html><body><p>Exports fail silently every time.</p><script>x()</script></body></html>")
    text = await _simple_fetch("http://93.184.216.34/p")
    assert "Exports fail silently" in text
    assert "x()" not in text
```

Append:

```python
def test_is_safe_fetch_url_blocks_non_http_schemes():
    assert _is_safe_fetch_url("file:///etc/passwd") is False
    assert _is_safe_fetch_url("gopher://169.254.169.254/") is False
    assert _is_safe_fetch_url("ftp://example.com/x") is False


def test_is_safe_fetch_url_blocks_private_and_metadata_ips():
    assert _is_safe_fetch_url("http://169.254.169.254/latest/meta-data/") is False  # cloud metadata
    assert _is_safe_fetch_url("http://127.0.0.1/") is False
    assert _is_safe_fetch_url("http://10.0.0.5/") is False
    assert _is_safe_fetch_url("http://192.168.1.10/") is False


def test_is_safe_fetch_url_resolves_hostname_via_injected_resolver():
    assert _is_safe_fetch_url("https://g2.com/x", resolve=lambda h: ["93.184.216.34"]) is True
    # any resolved private IP rejects the whole host (DNS-rebinding-conservative)
    assert _is_safe_fetch_url("https://evil.test/x", resolve=lambda h: ["10.1.2.3"]) is False
    # unresolvable host is rejected
    assert _is_safe_fetch_url("https://nope.test/x", resolve=lambda h: []) is False


@pytest.mark.asyncio
async def test_simple_fetch_blocks_redirect_to_metadata(httpx_mock):
    # public literal-IP first hop 302s toward the cloud-metadata IP → must be blocked, returns ""
    httpx_mock.add_response(url="http://93.184.216.34/start", status_code=302,
                            headers={"location": "http://169.254.169.254/latest"})
    text = await _simple_fetch("http://93.184.216.34/start")
    assert text == ""
    assert len(httpx_mock.get_requests()) == 1   # metadata hop never fetched
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_web.py -v`
Expected: FAIL — `ImportError: cannot import name '_is_safe_fetch_url'`.

- [ ] **Step 3: Implement the hardening**

In `council/discovery/gather/web.py`, add the stdlib imports at the top (next to `import os`, `import re`):

```python
import ipaddress
import socket
from urllib.parse import urlparse
```

Add the helpers and a redirect cap above `_simple_fetch`:

```python
_FETCH_MAX_REDIRECTS = 3


def _resolve_ips(host: str) -> list[str]:
    """Resolve a hostname to its IP strings (IPv4 + IPv6). Real DNS; injectable in tests.

    Note: a brief blocking getaddrinfo is acceptable for this personal tool. There is a
    residual TOCTOU gap between resolve and connect (DNS rebinding) we accept rather than
    pin the connection IP — fetch targets come from Brave results, not an attacker.
    """
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return []
    return [info[4][0] for info in infos]


def _is_safe_fetch_url(url: str, *, resolve=_resolve_ips) -> bool:
    """True only for http(s) URLs whose host resolves entirely to globally-routable IPs.

    Blocks non-http(s) schemes (file://, gopher://, ftp://, …) and SSRF targets: loopback,
    private, link-local (incl. 169.254.169.254 cloud metadata), and reserved ranges. A host
    that resolves to ANY non-global IP is rejected (no partial trust).
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = parsed.hostname
    if not host:
        return False
    try:                                  # literal IP host → check directly, no DNS
        return ipaddress.ip_address(host).is_global
    except ValueError:
        pass
    ips = resolve(host)
    if not ips:
        return False
    for raw in ips:
        try:
            if not ipaddress.ip_address(raw).is_global:
                return False
        except ValueError:
            return False
    return True
```

Replace the body of `_simple_fetch` (keep the signature and the trailing tag-strip) with a manual, per-hop-validated redirect loop:

```python
async def _simple_fetch(url: str, timeout: float = 20.0) -> str:
    """Best-effort full-page text for quote density (crude tag-strip).

    SSRF-hardened: validates scheme + resolved IPs of the initial URL AND every redirect hop
    against a public-IP allow-list before connecting. Redirects are followed manually
    (follow_redirects=False) so a public URL can't 302 into a private/metadata address.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as c:
            current = url
            html = ""
            for _ in range(_FETCH_MAX_REDIRECTS + 1):
                if not _is_safe_fetch_url(current):
                    return ""
                r = await c.get(current, headers={"User-Agent": "Mozilla/5.0 (discovery-bot)"})
                if r.is_redirect:
                    loc = r.headers.get("location")
                    if not loc:
                        return ""
                    current = str(httpx.URL(current).join(loc))
                    continue
                r.raise_for_status()
                ctype = r.headers.get("content-type", "")
                # Skip non-HTML bodies (PDF/binary); missing content-type is allowed.
                if ctype and not (ctype.startswith("text/") or ctype.startswith("application/xhtml")):
                    return ""
                html = r.text[:2_000_000]
                break
            else:
                return ""  # exceeded the redirect cap
    except httpx.HTTPError:
        return ""
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()
```

Delete the now-stale `# Phase 3: add scheme/private-IP allow-list ...` comment that preceded the old body.

- [ ] **Step 4: Run the web tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_web.py -v`
Expected: PASS (existing collect_web/brave tests untouched + the updated strip test + 4 new SSRF tests).
Then: `cd tools/llm-council && uv run --extra dev python -m pytest -v` → full suite green (94+ passed, 1 skipped).

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/web.py tests/discovery/test_gather_web.py
git commit -m "harden(discovery): SSRF/redirect allow-list in _simple_fetch (per-hop public-IP check)"
```

---

## Task 2: TierConfig collector flags (the §6 matrix)

**Files:**
- Modify: `tools/llm-council/council/discovery/tiers.py`
- Modify: `tools/llm-council/tests/discovery/test_tiers.py` (add matrix test)

**Interfaces:**
- Changed: `TierConfig` gains three boolean fields with defaults — `reviews: bool = False`, `github: bool = False`, `qa: bool = False`. `quick` leaves all False; `standard` sets `reviews=True, github=True`; `deep` sets `reviews=True, github=True, qa=True`. The gather orchestrator (Task 7) reads these flags exactly like the existing `social`/`web` flags.

**Context:** `TierConfig` is a frozen dataclass whose current fields all lack defaults; new fields **must** be appended with defaults so the existing keyword instantiations stay valid.

- [ ] **Step 1: Write the failing test**

Add to `tests/discovery/test_tiers.py`:

```python
def test_collector_tier_gating_matches_matrix():
    q, s, d = get_tier("quick"), get_tier("standard"), get_tier("deep")
    assert (q.reviews, q.github, q.qa) == (False, False, False)   # quick stays lean
    assert (s.reviews, s.github, s.qa) == (True, True, False)     # standard: + reviews + github
    assert (d.reviews, d.github, d.qa) == (True, True, True)      # deep: + reviews + github + qa
    assert all(t.social and t.web for t in (q, s, d))             # social + web stay on everywhere
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_tiers.py::test_collector_tier_gating_matches_matrix -v`
Expected: FAIL — `AttributeError: 'TierConfig' object has no attribute 'reviews'`.

- [ ] **Step 3: Implement**

In `council/discovery/tiers.py`, append the three fields to `TierConfig` (after `web: bool`):

```python
@dataclass(frozen=True)
class TierConfig:
    name: str
    panel: tuple[str, ...]      # Fusion analysis_models (tool-capable only)
    judge: str                  # Fusion judge / outer model
    max_tool_calls: int         # per-panel-model web tool-call budget
    max_cost_per_run: float
    sonar_model: str            # Stage 1b article harvester
    social: bool                # run last30days backbone
    web: bool                   # run exa/brave web collector
    reviews: bool = False       # review-sites + competitor-weakness mining (standard+)
    github: bool = False        # GitHub Issues unmet-need mining (standard+)
    qa: bool = False            # Stack Exchange Q&A pain mining (deep)
```

Set the flags on `standard` and `deep` in the `TIERS` dict (add the lines; leave `quick` as-is so the three default to `False`):

```python
    "standard": TierConfig(
        name="standard",
        panel=_STANDARD_PANEL,
        judge="anthropic/claude-opus-4.7",
        max_tool_calls=5,
        max_cost_per_run=1.50,
        sonar_model="perplexity/sonar-reasoning-pro",
        social=True,
        web=True,
        reviews=True,
        github=True,
    ),
    "deep": TierConfig(
        name="deep",
        panel=_STANDARD_PANEL + ("deepseek/deepseek-v4-pro", "mistralai/mistral-medium-3-5"),
        judge="anthropic/claude-opus-4.7",
        max_tool_calls=8,
        max_cost_per_run=4.00,
        sonar_model="perplexity/sonar-deep-research",
        social=True,
        web=True,
        reviews=True,
        github=True,
        qa=True,
    ),
```

- [ ] **Step 4: Run the tier tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_tiers.py -v`
Expected: PASS (existing 5 + the new matrix test). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/tiers.py tests/discovery/test_tiers.py
git commit -m "feat(discovery): tier flags for reviews/github/qa collectors (spec §6 matrix)"
```

---

## Task 3: Review-sites collector + competitor-weakness mining

**Files:**
- Create: `tools/llm-council/council/discovery/gather/reviews.py`
- Test: `tools/llm-council/tests/discovery/test_gather_reviews.py` (new)

**Interfaces:**
- Produces: `async collect_reviews(*, topic, search=..., fetch=..., max_results=8) -> list[EvidenceRecord]`, plus `_review_query(topic) -> str` and module constants `REVIEW_DOMAINS`, `_WEAKNESS`. Reuses `_default_brave_search`, `_simple_fetch`, `extract_quotes` from `gather/web.py` (DRY — no second Brave client). Records carry `source_type="review"`, `source_name=<domain>`.

**Context:** Spec §6/§1c — review sites (G2/Capterra/Trustpilot/Product Hunt/App Store/Play) with competitor-weakness mining ("harvest 1★/2★ reviews = where competitors fail"). Realized via a Brave **site-targeted** query biased toward low-star/negative language, then complaint-sentence extraction. No paid scraper (spec §3). Every record is a real review-page URL + a verbatim complaint sentence → fabrication-gate-compatible.

- [ ] **Step 1: Write the failing tests**

Create `tests/discovery/test_gather_reviews.py`:

```python
import pytest
from council.discovery.gather.reviews import collect_reviews, _review_query, REVIEW_DOMAINS


def test_review_query_targets_sites_and_weakness():
    q = _review_query("acme crm")
    assert "acme crm" in q
    assert "site:g2.com" in q and "site:trustpilot.com" in q
    assert "worst" in q  # competitor-weakness bias term


@pytest.mark.asyncio
async def test_collect_reviews_builds_records_with_domain_name():
    async def search(query):
        return [{"title": "Acme on G2", "url": "https://www.g2.com/products/acme/reviews",
                 "published": "2026-06-12",
                 "_text": "Reviewers complain Acme crashes during export and support is slow."}]
    recs = await collect_reviews(topic="acme", search=search, fetch=None)
    assert len(recs) >= 1
    r = recs[0]
    assert r.source_type == "review"
    assert r.source_name == "g2.com"
    assert r.url == "https://www.g2.com/products/acme/reviews"
    assert "crashes during export" in r.quote


@pytest.mark.asyncio
async def test_collect_reviews_fetch_fallback_when_snippet_thin():
    async def search(query):
        return [{"title": "T", "url": "https://www.capterra.com/p/x", "published": "2026-06-01",
                 "_text": "neutral marketing copy"}]
    async def fetch(url):
        return "One reviewer wrote that the tool is painfully slow and they will cancel."
    recs = await collect_reviews(topic="x", search=search, fetch=fetch)
    assert any("painfully slow" in r.quote for r in recs)


@pytest.mark.asyncio
async def test_collect_reviews_no_key_returns_empty(monkeypatch):
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    recs = await collect_reviews(topic="x")
    assert recs == []
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_reviews.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.gather.reviews'`.

- [ ] **Step 3: Implement the collector**

Create `council/discovery/gather/reviews.py`:

```python
# council/discovery/gather/reviews.py
"""Collector: review-site complaint mining with competitor-weakness bias.

Brave site-targeted search across review domains → fetch each result page → extract
complaint quotes biased toward low-star / negative language ("where competitors fail =
your wedge"). Every record is a real review-page URL + a verbatim complaint sentence, so
it is fabrication-gate-compatible. No paid scraper (spec §3) — reuses the free Brave
provider + the SSRF-hardened _simple_fetch from web.py.
"""

import os

from council.discovery.evidence import EvidenceRecord
from council.discovery.gather.web import _default_brave_search, _simple_fetch, extract_quotes

REVIEW_DOMAINS = (
    "g2.com", "capterra.com", "trustpilot.com",
    "producthunt.com", "apps.apple.com", "play.google.com",
)
_WEAKNESS = (
    '"1 star"', '"2 star"', "worst", "terrible", "disappointing", "avoid", "cancel",
)


def _review_query(topic: str) -> str:
    sites = " OR ".join(f"site:{d}" for d in REVIEW_DOMAINS)
    weak = " OR ".join(_WEAKNESS)
    return f"{topic} review ({weak}) ({sites})"


async def collect_reviews(*, topic: str, search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        key = os.environ.get("BRAVE_API_KEY")
        search = _default_brave_search(key) if key else None
    if fetch is ...:
        fetch = _simple_fetch
    if search is None:
        return []
    results = await search(_review_query(topic))
    recs: list[EvidenceRecord] = []
    for it in results[:max_results]:
        url = it.get("url", "")
        if not url:
            continue
        text = it.get("_text") or ""
        quotes = extract_quotes(text)
        if not quotes and fetch is not None:
            quotes = extract_quotes(await fetch(url))
        domain = next((d for d in REVIEW_DOMAINS if d in url), "review")
        for q in quotes:
            recs.append(EvidenceRecord(
                source_type="review", source_name=domain, url=url,
                date=it.get("published", ""), quote=q, engagement=0,
            ))
    return recs
```

- [ ] **Step 4: Run the reviews tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_reviews.py -v`
Expected: PASS (4 tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/reviews.py tests/discovery/test_gather_reviews.py
git commit -m "feat(discovery): review-sites collector with competitor-weakness mining (Brave site-targeted)"
```

---

## Task 4: GitHub Issues collector

**Files:**
- Create: `tools/llm-council/council/discovery/gather/github.py`
- Test: `tools/llm-council/tests/discovery/test_gather_github.py` (new)

**Interfaces:**
- Produces: `async collect_github(*, topic, search=..., max_results=8) -> list[EvidenceRecord]`, plus `_default_github_search(token) -> callable` and `_repo_from_html_url(html_url) -> str`. Records carry `source_type="github"`, `source_name=<owner/repo>`, `url=<issue html_url>`, `quote=<issue title>`, `engagement=<reactions.total_count>`.

**Context:** Spec §6/§1c — GitHub Issues = explicit, upvoted unmet needs (strongest `pm`-lens signal). Uses the free GitHub Search API (`GET /search/issues`); reads an optional `GITHUB_TOKEN` from the env for a higher rate limit and degrades to unauthenticated without it. The issue **title** is the verbatim quote (reliably a true substring → gate-safe).

- [ ] **Step 1: Write the failing tests**

Create `tests/discovery/test_gather_github.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_github.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.gather.github'`.

- [ ] **Step 3: Implement the collector**

Create `council/discovery/gather/github.py`:

```python
# council/discovery/gather/github.py
"""Collector: GitHub Issues — explicit, upvoted unmet needs (strongest pm-lens signal).

Free GitHub Search API (https://docs.github.com/rest/search/search#search-issues-and-pull-requests).
Works unauthenticated (low rate limit); reads an optional GITHUB_TOKEN from the env for a higher
limit. Each issue is a real html_url + a verbatim title quote → fabrication-gate-compatible.
"""

import os

import httpx

from council.discovery.evidence import EvidenceRecord

GITHUB_SEARCH_URL = "https://api.github.com/search/issues"


def _repo_from_html_url(html_url: str) -> str:
    # https://github.com/owner/repo/issues/123 → "owner/repo"
    parts = html_url.split("/")
    if "github.com" in html_url and len(parts) >= 5:
        return f"{parts[3]}/{parts[4]}"
    return "github"


def _default_github_search(token: str | None):
    async def search(query: str) -> list[dict]:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(GITHUB_SEARCH_URL, headers=headers,
                            params={"q": query, "sort": "reactions", "order": "desc", "per_page": 12})
            r.raise_for_status()
            return r.json().get("items", [])
    return search


async def collect_github(*, topic: str, search=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        search = _default_github_search(os.environ.get("GITHUB_TOKEN"))
    if search is None:
        return []
    items = await search(f"{topic} in:title,body is:issue")
    recs: list[EvidenceRecord] = []
    for it in items[:max_results]:
        url = it.get("html_url", "")
        title = it.get("title", "")
        if not (url and title):
            continue
        reactions = (it.get("reactions") or {}).get("total_count", 0) or 0
        recs.append(EvidenceRecord(
            source_type="github", source_name=_repo_from_html_url(url), url=url,
            date=(it.get("created_at") or "")[:10], quote=title, engagement=int(reactions),
        ))
    return recs
```

- [ ] **Step 4: Run the github tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_github.py -v`
Expected: PASS (3 tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/github.py tests/discovery/test_gather_github.py
git commit -m "feat(discovery): GitHub Issues collector (free Search API, optional GITHUB_TOKEN)"
```

---

## Task 5: Stack Exchange Q&A collector

**Files:**
- Create: `tools/llm-council/council/discovery/gather/qa.py`
- Test: `tools/llm-council/tests/discovery/test_gather_qa.py` (new)

**Interfaces:**
- Produces: `async collect_qa(*, topic, search=..., max_results=8) -> list[EvidenceRecord]`, plus `_default_se_search(site="stackoverflow") -> callable` and `_epoch_to_date(epoch) -> str`. Records carry `source_type="qa"`, `source_name="stackoverflow"`, `url=<question link>`, `quote=<HTML-unescaped title>`, `engagement=<score>`.

**Context:** Spec §6/§1c — Q&A pain (Stack Overflow/Quora) is `deep`-only. Uses the free Stack Exchange API (`/2.3/search/advanced`, no key needed, 300 req/day unauthenticated). Question titles are the verbatim quotes; Stack Exchange HTML-entity-encodes titles, so `html.unescape` is applied for a clean verbatim string. Multi-site (beyond `stackoverflow`) and Quora are deferred.

- [ ] **Step 1: Write the failing tests**

Create `tests/discovery/test_gather_qa.py`:

```python
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
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_qa.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'council.discovery.gather.qa'`.

- [ ] **Step 3: Implement the collector**

Create `council/discovery/gather/qa.py`:

```python
# council/discovery/gather/qa.py
"""Collector: Stack Exchange Q&A pain mining (deep tier).

Free Stack Exchange API (https://api.stackexchange.com/docs/advanced-search) — no key needed
(300 req/day unauthenticated). Each question is a real link + a verbatim (HTML-unescaped) title
quote → fabrication-gate-compatible. Defaults to the stackoverflow site; multi-site is deferred.
"""

import html
from datetime import datetime, timezone

import httpx

from council.discovery.evidence import EvidenceRecord

STACKEXCHANGE_URL = "https://api.stackexchange.com/2.3/search/advanced"


def _epoch_to_date(epoch) -> str:
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return ""


def _default_se_search(site: str = "stackoverflow"):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(STACKEXCHANGE_URL, params={
                "order": "desc", "sort": "relevance", "q": query, "site": site, "pagesize": 15,
            })
            r.raise_for_status()
            return r.json().get("items", [])
    return search


async def collect_qa(*, topic: str, search=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        search = _default_se_search()
    if search is None:
        return []
    items = await search(topic)
    recs: list[EvidenceRecord] = []
    for it in items[:max_results]:
        url = it.get("link", "")
        title = html.unescape(it.get("title", ""))
        if not (url and title):
            continue
        recs.append(EvidenceRecord(
            source_type="qa", source_name="stackoverflow", url=url,
            date=_epoch_to_date(it.get("creation_date")), quote=title,
            engagement=int(it.get("score", 0) or 0),
        ))
    return recs
```

- [ ] **Step 4: Run the qa tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_qa.py -v`
Expected: PASS (3 tests). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/qa.py tests/discovery/test_gather_qa.py
git commit -m "feat(discovery): Stack Exchange Q&A collector (free API, deep tier)"
```

---

## Task 6: Sonar verbatim-quote hardening

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/sonar.py`
- Modify: `tools/llm-council/tests/discovery/test_gather_sonar.py` (add 2 tests; existing 3 stay green)

**Interfaces:**
- Changed: `collect_sonar(*, api_key, topic, model, timeout=120.0, fetch=None) -> list[EvidenceRecord]`. New `fetch` param defaults `None` (positional-sentence behavior unchanged — existing tests stay green). When a `fetch` callable is supplied (the orchestrator wires `fetch=_simple_fetch` in Task 7), each of the top `_VERBATIM_FETCH_LIMIT` citations is fetched and a **verbatim** complaint quote actually present at that URL replaces the synthesized sentence; the synthesized sentence is kept only when the fetch yields nothing.

**Context:** Phase-1 minor 6 / Phase-3 §7c — today the cited quote is Sonar's *synthesized* sentence positionally paired with citation `i`; it is anchored to a real URL but not guaranteed to be the verbatim text there. Fetching the citation and extracting a true substring strengthens the Stage-3 gate. Bounded to the top citations to cap latency.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_gather_sonar.py`:

```python
@pytest.mark.asyncio
async def test_collect_sonar_anchors_verbatim_quote_via_fetch(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Synthesized paraphrase sentence about onboarding."}}],
        "citations": ["https://news.com/a"], "usage": {},
    })
    async def fetch(url):
        return "Real reviewers complain the onboarding flow is broken and confusing."
    recs = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar", fetch=fetch)
    assert len(recs) == 1
    assert "onboarding flow is broken" in recs[0].quote   # verbatim from the page, not the paraphrase


@pytest.mark.asyncio
async def test_collect_sonar_falls_back_to_synthesized_when_fetch_empty(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Teams report onboarding is slow and painful."}}],
        "citations": ["https://news.com/a"], "usage": {},
    })
    async def fetch(url):
        return ""    # page yielded no complaint sentence
    recs = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar", fetch=fetch)
    assert recs[0].quote == "Teams report onboarding is slow and painful."
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_sonar.py::test_collect_sonar_anchors_verbatim_quote_via_fetch -v`
Expected: FAIL — `TypeError: collect_sonar() got an unexpected keyword argument 'fetch'`.

- [ ] **Step 3: Implement**

In `council/discovery/gather/sonar.py`, add the import + a fetch-limit constant near the top (below the existing `_SENT` line):

```python
from council.discovery.gather.web import _simple_fetch, extract_quotes

_VERBATIM_FETCH_LIMIT = 6   # fetch the top-N citations to anchor a true verbatim quote
```

> Note: `_simple_fetch` is imported for symmetry/availability but the **default** stays `fetch=None`; the orchestrator (Task 7) passes `fetch=_simple_fetch` explicitly. Importing it here does not create a cycle — `web.py` does not import `sonar.py`.

Replace the `collect_sonar` signature and the record-building loop:

```python
async def collect_sonar(*, api_key: str, topic: str, model: str, timeout: float = 120.0, fetch=None) -> list[EvidenceRecord]:
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": f"What are the most recent, specific user complaints and unmet needs about {topic}? "
                       f"Quote real users where possible. Cite sources.",
        }],
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            resp.raise_for_status()
            payload = resp.json()
    except (httpx.HTTPError,):
        return []
    citations = _extract_citations(payload)
    if not citations:
        return []
    content = (payload.get("choices") or [{}])[0].get("message", {}).get("content", "")
    sentences = [s.strip() for s in _SENT.findall(content)][: len(citations)] or [content[:200]]
    recs = []
    for i, url in enumerate(citations):
        synthesized = sentences[i] if i < len(sentences) else sentences[-1]
        quote = synthesized
        if fetch is not None and i < _VERBATIM_FETCH_LIMIT:
            verbatim = extract_quotes(await fetch(url))
            if verbatim:
                quote = verbatim[0]      # a true substring of the fetched page → strengthens VERIFY
        recs.append(EvidenceRecord(
            source_type="sonar", source_name="Perplexity Sonar", url=url,
            date="", quote=quote, engagement=0,
        ))
    return recs
```

- [ ] **Step 4: Run the sonar tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_sonar.py -v`
Expected: PASS (existing 3 — they pass no `fetch`, so default `None` keeps the synthesized-sentence behavior — plus the 2 new tests).
Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/sonar.py tests/discovery/test_gather_sonar.py
git commit -m "feat(discovery): Sonar verbatim-quote hardening (WebFetch citations, gate-strengthening)"
```

---

## Task 7: Wire new collectors + Sonar fetch opt-in into the gather orchestrator

**Files:**
- Modify: `tools/llm-council/council/discovery/gather/__init__.py`
- Modify: `tools/llm-council/tests/discovery/test_gather_orchestrator.py` (add a tier-gating test; existing test untouched)

**Interfaces:** `gather_evidence` signature unchanged (`-> tuple[EvidenceBundle, dict]`). Its default `collectors` dict now includes `reviews`/`github`/`qa` gated by the matching `TierConfig` flags, and the `sonar` entry opts into `fetch=_simple_fetch`. The concurrency / per-collector status / dedup machinery is unchanged.

**Context:** This is the single edit that activates the three new collectors and the Sonar verbatim path in production. The existing `test_gather_returns_bundle_and_status` passes an explicit `collectors=` dict, so it is unaffected by the new defaults.

- [ ] **Step 1: Write the failing test**

Add to `tests/discovery/test_gather_orchestrator.py`:

```python
@pytest.mark.asyncio
async def test_default_collectors_respect_tier_flags(monkeypatch):
    seen = []

    def stub(name):
        async def fn(*a, **k):
            seen.append(name)
            return []
        return fn

    import council.discovery.gather as gmod
    monkeypatch.setattr(gmod, "collect_last30", stub("last30"))
    monkeypatch.setattr(gmod, "collect_sonar", stub("sonar"))
    monkeypatch.setattr(gmod, "collect_web", stub("web"))
    monkeypatch.setattr(gmod, "collect_reviews", stub("reviews"))
    monkeypatch.setattr(gmod, "collect_github", stub("github"))
    monkeypatch.setattr(gmod, "collect_qa", stub("qa"))

    await gmod.gather_evidence(topic="x", tier=get_tier("quick"), api_key="k")
    assert "reviews" not in seen and "github" not in seen and "qa" not in seen

    seen.clear()
    await gmod.gather_evidence(topic="x", tier=get_tier("standard"), api_key="k")
    assert "reviews" in seen and "github" in seen and "qa" not in seen

    seen.clear()
    await gmod.gather_evidence(topic="x", tier=get_tier("deep"), api_key="k")
    assert {"reviews", "github", "qa"} <= set(seen)
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_orchestrator.py::test_default_collectors_respect_tier_flags -v`
Expected: FAIL — `AttributeError: <module 'council.discovery.gather'> does not have the attribute 'collect_reviews'` (the names aren't imported yet).

- [ ] **Step 3: Implement the wiring**

Replace `council/discovery/gather/__init__.py` import block + the default `collectors` dict:

```python
# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → (deduped bundle, per-collector status).

COST-INTEGRITY INVARIANT: every collector below is FREE (no billable provider call). The CLI's
generic pre-fuse `except` therefore records $0 correctly. If you add a paid collector (e.g. Firecrawl
/ Apify), you MUST thread its incurred cost into a typed gather failure and record_spend it in that
`except` — mirror FusionError.cost → DiscoveryFailed.cost_usd — or a gather-stage failure will
silently record $0 (cost-integrity leak). See test_gather_cost_integrity.py.
"""

import asyncio
import sys

from council.discovery.evidence import EvidenceBundle
from council.discovery.gather.github import collect_github
from council.discovery.gather.last30 import collect_last30
from council.discovery.gather.qa import collect_qa
from council.discovery.gather.reviews import collect_reviews
from council.discovery.gather.sonar import collect_sonar
from council.discovery.gather.web import collect_web, _simple_fetch
from council.discovery.tiers import TierConfig


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str,
                          collectors: dict | None = None) -> tuple[EvidenceBundle, dict]:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model, fetch=_simple_fetch)),
            "web": (lambda t: collect_web(topic=t)) if tier.web else None,
            "reviews": (lambda t: collect_reviews(topic=t)) if tier.reviews else None,
            "github": (lambda t: collect_github(topic=t)) if tier.github else None,
            "qa": (lambda t: collect_qa(topic=t)) if tier.qa else None,
        }
    active = {name: fn for name, fn in collectors.items() if fn is not None}
    results = await asyncio.gather(*(fn(topic) for fn in active.values()), return_exceptions=True)
    bundle = EvidenceBundle()
    status: dict[str, str] = {}
    for name, r in zip(active.keys(), results):
        if isinstance(r, Exception):
            status[name] = f"error: {type(r).__name__}: {r!r}"
            print(f"[gather] collector {name!r} failed: {type(r).__name__}: {r}", file=sys.stderr)
        else:
            added = sum(1 for rec in r if bundle.add(rec))
            status[name] = f"ok: {added} records ({len(r)} found)"
    return bundle, status
```

- [ ] **Step 4: Run the orchestrator tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_orchestrator.py -v`
Expected: PASS (existing tuple test + new tier-gating test). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/gather/__init__.py tests/discovery/test_gather_orchestrator.py
git commit -m "feat(discovery): wire reviews/github/qa collectors + Sonar fetch opt-in, tier-gated"
```

---

## Task 8: Fold the deferred §7b code nits (`_first_json_object` scan-forward + last30 timeout constant)

**Files:**
- Modify: `tools/llm-council/council/discovery/fusion.py` (`_first_json_object`)
- Modify: `tools/llm-council/council/discovery/gather/last30.py` (timeout constant)
- Modify: `tools/llm-council/tests/discovery/test_fusion.py` (add 2 tests)

**Interfaces:** signatures unchanged. `_first_json_object(text) -> dict | None` now scans forward to the next `{` when a balanced object fails to parse, instead of returning `None` at the first failure. `last30.py` hoists the hard-coded `300` to `_LAST30_TIMEOUT_S = 300`.

**Context:** Phase-3 §7b — `_first_json_object` stops at the first balanced `{…}` even if it fails to parse (fine for the documented prose-wrapped-single-object case, but brittle as the last-resort decoder). last30's `300` timeout is a magic number. Both are safe-today nits to fold while Phase 4 is in these files.

- [ ] **Step 1: Write the failing tests**

Add to `tests/discovery/test_fusion.py`:

```python
def test_first_json_object_skips_malformed_leading_object():
    # leading {...} is balanced but not valid JSON (unquoted key); the second is valid
    text = 'noise {not: valid} more {"pain_points": []} trailing'
    assert _first_json_object(text) == {"pain_points": []}


def test_first_json_object_none_when_no_valid_object():
    assert _first_json_object("{nope} {still bad}") is None
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py::test_first_json_object_skips_malformed_leading_object -v`
Expected: FAIL — the current implementation returns `None` at the first unparseable balanced object instead of scanning forward.

- [ ] **Step 3: Implement the scan-forward decoder**

In `council/discovery/fusion.py`, replace the whole `_first_json_object` function with:

```python
def _first_json_object(text: str) -> dict | None:
    """Return the first balanced {...} object that parses as JSON (string-aware), or None.

    Scans from each "{" in turn — if a balanced span fails to parse, it continues to the
    NEXT "{" rather than giving up, so a malformed leading object followed by a valid one
    still decodes. Digs past leading arrays/prose to find the object.
    """
    search_from = 0
    while True:
        start = text.find("{", search_from)
        if start < 0:
            return None
        depth = 0
        in_str = False
        esc = False
        end = -1
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            return None                       # unbalanced from here to the end
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            search_from = start + 1           # scan forward to the next "{"
```

In `council/discovery/gather/last30.py`, add the constant near the top (below the imports) and use it in `_subprocess_runner`:

```python
_LAST30_TIMEOUT_S = 300   # last30days can be slow; hard cap so a hung child can't stall gather
```

and change the `asyncio.wait_for(... timeout=300)` line to:

```python
        out, err = await asyncio.wait_for(proc.communicate(), timeout=_LAST30_TIMEOUT_S)
```

- [ ] **Step 4: Run the fusion + last30 tests + full suite**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_fusion.py tests/discovery/test_gather_last30.py -v`
Expected: PASS (existing fusion tests — incl. the prose-wrapped + braces-in-strings tests — plus the 2 new scan-forward tests; last30 tests unchanged and green). Then full suite green.

- [ ] **Step 5: Commit**

```bash
git add council/discovery/fusion.py council/discovery/gather/last30.py tests/discovery/test_fusion.py
git commit -m "harden(discovery): _first_json_object scan-forward + last30 timeout constant (§7b nits)"
```

---

## Task 9: Cost-integrity guard + docs reconciliation + verification + live cost re-check

**Files:**
- Create: `tools/llm-council/tests/discovery/test_gather_cost_integrity.py` (new)
- Modify: `.claude/skills/fusion-discovery-council/SKILL.md`
- Modify: `CHANGELOG.md`

**Interfaces:** none (test + docs + final gate).

**Context:** Closes the cost-integrity theme for the free-collector path (regression guard + the documented threading recipe lives in `gather/__init__.py` from Task 7), updates the skill surface to stop calling the extended collectors "deferred," and re-checks the per-run caps live now that GATHER is wider (Phase-3 §7f).

- [ ] **Step 1: Write the cost-integrity guard test**

Create `tests/discovery/test_gather_cost_integrity.py`:

```python
import pytest
from datetime import date
from council import budget
from council.discovery.tiers import get_tier
from council.discovery.gather import gather_evidence
from council.discovery.evidence import EvidenceRecord


@pytest.mark.asyncio
async def test_gather_collectors_record_no_spend(tmp_spend_dir):
    """Cost-integrity invariant: Stage-1 collectors are all FREE today, so a full gather run
    records ZERO discovery spend. If a future collector bills (Firecrawl/Apify), this stays
    green ONLY by threading the incurred cost into a typed gather failure + record_spend
    (see the gather/__init__.py invariant note) — never by a silent billable call."""
    async def fake(t):
        return [EvidenceRecord("review", "g2.com", "https://g2.com/1", "", "it crashes daily")]
    bundle, status = await gather_evidence(
        topic="x", tier=get_tier("deep"), api_key="k",
        collectors={"reviews": fake, "github": fake, "qa": fake},
    )
    assert len(bundle.records) >= 1
    assert budget.tool_total_for_day(date.today(), "discovery") == 0.0
```

- [ ] **Step 2: Run to verify it passes (it is a guard, not red-then-green)**

Run: `cd tools/llm-council && uv run --extra dev python -m pytest tests/discovery/test_gather_cost_integrity.py -v`
Expected: PASS. (This guard documents and locks an already-true invariant; it would go RED only if a collector started billing without threading the cost. To confirm it is load-bearing, temporarily add `budget.record_spend(amount=0.01, profile="deep", tag="x", on_date=date.today(), tool="discovery")` inside `fake`, re-run → it FAILS; then remove the line and re-confirm green.)

- [ ] **Step 3: Update SKILL.md §2 — the extended collectors are now live (tier-gated)**

In `.claude/skills/fusion-discovery-council/SKILL.md`, update the §2 GATHER list to add the new collectors, and replace the "deferred" blockquote. Change the GATHER bullet list (after the existing web-collector bullet) to add:

```
   - **Extended collectors (tier-gated):** review sites + competitor-weakness mining, GitHub Issues, and Stack Exchange Q&A. `standard` adds review sites + GitHub Issues; `deep` adds those plus Stack Exchange Q&A. Each emits a real URL + a verbatim quote, so the Stage-3 gate still governs everything.
```

Replace the blockquote:

```
> Phase 1 ships the GATHER backbone (last30days + Sonar + web). Extended collectors (review sites, GitHub issues, trend feeds) are deferred to Phase 2/3 and do **not** run yet — do not claim them.
```

with:

```
> As of Phase 4 the extended collectors are LIVE and tier-gated: review sites + competitor-weakness mining and GitHub Issues on `standard`/`deep`, Stack Exchange Q&A on `deep`. Still deferred (do **not** claim them): demand-intent (autocomplete/PAA), trend-velocity feeds, and Quora. `quick` stays lean (last30days + Sonar + web).
```

Also update the §3 `--tier` table's "Panel"/breadth note is fine as-is; no cap change.

- [ ] **Step 4: Add a CHANGELOG entry**

Add a dated entry under the latest `CHANGELOG.md` heading:

```markdown
### fusion-discovery-council Phase 4 — extended collectors + fetch hardening (2026-06-20)
- Three new free, fabrication-gate-compatible Stage-1 collectors, tier-gated per spec §6: review sites + competitor-weakness mining (Brave site-targeted) and GitHub Issues on `standard`/`deep`; Stack Exchange Q&A on `deep`. `quick` stays lean.
- `_simple_fetch` SSRF/redirect allow-list: per-hop scheme + public-IP validation (blocks file://, private/loopback/link-local + cloud-metadata IPs, and redirects into them).
- Sonar evidence hardened to verbatim quotes (WebFetch each citation, extract a true substring; falls back to the synthesized sentence) — strengthens the Stage-3 gate.
- Folded §7b nits: `_first_json_object` scans forward past a malformed leading object; last30 timeout hoisted to a module constant.
- Cost integrity: all new collectors are free; a regression guard + a documented threading recipe (gather/__init__.py) keep "never bill and record $0" true if a paid collector is ever added. Caps unchanged ($0.50/$1.50/$4.00); validated live (Step 6).
- Plan: docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase4.md. Deferred to Phase 5: the `substack` lens + `--segment` qualifier. Deferred further: demand-intent, trend-velocity, Quora.
```

- [ ] **Step 5: Full verification gate**

Run the whole suite and the repo validator:

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run --extra dev python -m pytest -v
cd /Users/seanwinslow/Code-Brain/code-brain && python3 scripts/validate.py
```

Expected: pytest fully green (93 baseline + all new Phase-4 tests passed, 1 skipped); `validate.py` passes (pre-existing secret-pattern warnings only, none in changed files).

- [ ] **Step 6: MANDATORY live cost re-check (ask Sean before spending) — standard + deep**

The new collectors widen the evidence bundle → larger Fusion prompt → higher per-run cost. The live `quick` run was $0.36; standard/deep have never been live-tested. Run one `standard` and one `deep` e2e and confirm each lands under its cap:

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
  "obsidian plugins" --lens pm --tier standard --output /tmp/p4-standard-ledger.md
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council.discovery \
  "obsidian plugins" --lens pm --tier deep --yes --output /tmp/p4-deep-ledger.md
```

Expected: each writes a ledger; the printed `$X.XX` is **under the cap** ($1.50 standard / $4.00 deep) and the session JSON's `gather_status` shows the new collectors firing (`reviews: ok …`, `github: ok …`, and `qa: ok …` on deep). **If a run exceeds its cap**, raise that tier's `max_cost_per_run` in `tiers.py` (e.g. standard → $2.00, deep → $5.00), update `test_tiers.py` + the SKILL.md §3 table + this CHANGELOG entry, re-run to confirm, and record the new figure. **If under cap** (expected), leave caps unchanged and record the live cost in the field report.

- [ ] **Step 7: Commit**

```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git add tools/llm-council/tests/discovery/test_gather_cost_integrity.py .claude/skills/fusion-discovery-council/SKILL.md CHANGELOG.md
git commit -m "docs(discovery): Phase 4 cost-integrity guard + SKILL.md/CHANGELOG reconciliation"
```

> The vault is intentionally **not** staged (CLAUDE.md rule 8 — Obsidian-Git owns vault commits). The live-run ledgers go to `/tmp`; any spend-ledger row written to `vault/health/` is left for Obsidian-Git, never `git add`-ed here.

---

## Self-Review (completed during plan authoring)

**Spec coverage (§6 extended-collectors menu + Phase-3 §7c):**
- Review sites + competitor-weakness mining → Task 3 ✅ (Brave site-targeted, 1★/2★-biased query, complaint extraction).
- GitHub Issues → Task 4 ✅. *(Canny / public roadmaps from §6 are NOT shipped — they have no free API and overlap the review-style site-targeted path; explicitly deferred, see below.)*
- Q&A (Stack Overflow) → Task 5 ✅. *(Quora deferred — anti-scraping.)*
- Demand/intent (PAA/autocomplete) → **deferred with rationale** (produces queries, not URL-anchored quotes → would be dropped by VERIFY; better as query-expansion later). Documented in "Design decisions locked" + the SKILL.md update.
- Trend velocity (Trends/Exploding Topics) → **deferred with rationale** (no clean free API; not URL-quote evidence). Documented.
- `_simple_fetch` SSRF/redirect allow-list → Task 1 ✅ (landed first, before the fetch surface widens).
- Quote-verbatim hardening (WebFetch Sonar citations) → Task 6 ✅.
- §7b nits (`_first_json_object` scan-forward, last30 timeout constant) → Task 8 ✅.
- Cost-integrity rule (§7a) → Task 9 ✅ — all collectors free, so the invariant is a regression guard + documented threading recipe (the conditional "if a paid call" branch is not triggered; recipe is in place for the day it is).
- Tier gating per §6 matrix → Task 2 ✅ (standard: reviews+github; deep: +qa).
- Caps re-check (§7f) → Task 9 Step 6 ✅ (mandatory live standard+deep validation).

**Placeholder scan:** every code/test step carries complete code grounded in the real current files (re-read 2026-06-20) and real public-API shapes (GitHub `/search/issues`, Stack Exchange `/2.3/search/advanced`, Brave `site:` operators). No TBD/TODO. The only live step (Task 9 Step 6) is a gated, Sean-approved cost validation with the deterministic unit tests as the real gate.

**Type consistency:** new collectors all return `list[EvidenceRecord]` (the existing collector contract consumed by `gather_evidence`); `TierConfig.reviews/github/qa` (Task 2) are added before they're read in `gather_evidence` (Task 7); `collect_sonar`'s new `fetch` param defaults `None` (existing tests unaffected) and is wired to `_simple_fetch` only in the orchestrator (Task 7); `_is_safe_fetch_url`/`_resolve_ips` (Task 1) are consumed only inside `_simple_fetch`; `_first_json_object` (Task 8) keeps its `dict | None` return. No signature referenced before it is defined.

---

## Phasing reminder

This plan is **Phase 4 (extended collectors + fetch hardening)** only. After it lands and the live standard+deep cost re-check confirms caps:
- **Phase 5:** the `substack` lens (`frame_substack` + handoff brief into `substack-value-engine`) + the `--segment` qualifier. See `docs/superpowers/plans/2026-06-20-fusion-discovery-council-phase5.md`. Phase 5 can ship independently of Phase 4 (it grounds against today's collectors); recommended order is Phase 4 first.
- **Deferred further (documented, not lost):** demand-intent (autocomplete/PAA as query-expansion), trend-velocity, Quora, Canny/public-roadmaps, App-Store/Play RSS, multi-site Stack Exchange.
