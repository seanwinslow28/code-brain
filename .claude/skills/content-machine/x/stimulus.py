#!/usr/bin/env python3
"""X's route 1 — the autonomous sweep, and the stimulus block it produces.

Ruled on #249, built on #250. X is the one medium whose stage 2 is not an
interview: a reactive post's material is someone else's post, already on the
screen, and an interviewer knows no less about it than the author does. So
stage 2 here is a STIMULUS BLOCK, and this script is the only thing that
writes one.

    stimulus.py sweep  --query Q [--query Q ...] [--count N] [--json]
    stimulus.py auth
    stimulus.py fetch  <status-url> [--json]
    stimulus.py block  <status-url> --slug S --surface reply|quote-post
                       [--media "..."] [--out DIR] [--force] [--stdout]
    stimulus.py check  <block.md> [--json]

Two halves, deliberately apart.

**The sweep** is a stdlib wrapper over the X client `last30days` already
vendors (`scripts/lib/vendor/bird-search/`), which calls X's GraphQL
`SearchTimeline` with the `auth_token` / `ct0` session cookies. No password is
stored and nothing new is installed. Three standing caveats, all inherited:
the cookies rotate and a run re-reads them, the endpoint is internal and can
break without notice, and the session lives on whichever machine the author is
logged into (the MacBook Pro). **On demand only** — L7 blocks a launchd stanza
until probation is served, and there is no schedule anywhere in this file.

Where those cookies come from is a correction to the ruling, measured on the
MacBook Pro 2026-09-05: **all three browser-extraction paths fail.** Safari
returns EPERM on `Cookies.binarycookies` (no Full Disk Access), Chrome's
reader throws `Value is too large to be represented as a JavaScript number` on
a WebKit cookie timestamp — a node:sqlite integer bug, so it fails whether or
not he is signed in — and Firefox has no profile. What works is the credential
file `last30days`' own setup wizard writes. `credentials_env()` resolves in
that order and browser extraction stays on as the last resort, so a rotated
session is fixed in ONE place on this machine, not two.

**The block** takes verbatim post text from `publish.x.com/oembed`, the
sanctioned unauthenticated path established on #247. The sweep's own text is
a search payload and is treated as a candidate listing, never as the verbatim
record: every block re-fetches through oEmbed, which is the same two-stage
discover-then-verify method the research ran.

WHAT THIS SCRIPT DOES NOT DECIDE: what to search on, and how big a deck is.
That is #251. `sweep` takes queries and refuses to invent them.

The block carries nothing from the author. It is a **forbidden-strings**
source for the gates, never a permitted-vocabulary one, and it is written to
a git-ignored path or not at all.
"""

from __future__ import annotations

import argparse
import html as _html
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BLOCKS_DIR = REPO / "creative-studio" / "content-machine" / "stimulus"
BIRD = (Path.home() / ".claude" / "skills" / "last30days" / "scripts"
        / "lib" / "vendor" / "bird-search" / "bird-search.mjs")

OEMBED = "https://publish.x.com/oembed"
UA = "content-machine/stimulus (+https://github.com/seanwinslow28/code-brain)"
FETCH_TIMEOUT_S = 20
SWEEP_TIMEOUT_S = 60

SENTINEL = "STIMULUS BLOCK"
SURFACES = ("reply", "quote-post")

_STATUS_RE = re.compile(r"^https?://(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})/status/(\d+)")
_P_RE = re.compile(r"<p[^>]*>(.*?)</p>", re.DOTALL)
_A_RE = re.compile(r"<a\s+[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_TAIL_DATE_RE = re.compile(r"&mdash;.*?<a\s+[^>]*>([^<]+)</a>\s*</blockquote>", re.DOTALL)


# ---------------------------------------------------------------- data ----

@dataclass
class Post:
    """One post as oEmbed returned it. `text` is verbatim; the flags say what
    the channel could not give us, because a silent gap is how a paraphrase
    gets recorded as a quote."""
    url: str
    handle: str
    author_name: str
    text: str
    posted: str | None
    truncated: bool
    links_dropped: int
    links_inline: int

    def to_json(self) -> dict:
        return asdict(self)


# --------------------------------------------------------------- oembed ---

def canonical_status_url(url: str) -> tuple[str, str, str]:
    """(canonical url, handle, status id). Raises on anything that is not a
    status permalink — a profile or a search URL has no verbatim text to fetch
    and would silently produce an empty block."""
    m = _STATUS_RE.match(url.strip())
    if not m:
        raise ValueError(
            f"not an X status permalink: {url!r}\n"
            "  expected https://x.com/<handle>/status/<id>")
    handle, sid = m.group(1), m.group(2)
    return f"https://x.com/{handle}/status/{sid}", handle, sid


def _post_text_from_html(markup: str) -> tuple[str, bool, int, int]:
    """Pull the verbatim post text out of the oEmbed blockquote.

    Conventions are #247's, kept because the research corpus was read under
    them and a second convention would make the two records incomparable:
    `[link]` stands where an inline t.co shortener was, a trailing shortener
    (X's auto-appended media/quote card) is dropped, an @mention is restored
    from the anchor X expands it into, and a trailing ellipsis means X cut the
    post at the embed limit — the words shown are exact, there are more.
    """
    m = _P_RE.search(markup)
    if not m:
        return "", False, 0, 0
    body = m.group(1)

    inline = 0

    def sub_anchor(mm: re.Match) -> str:
        nonlocal inline
        href, label = mm.group(1), _TAG_RE.sub("", mm.group(2)).strip()
        if label.startswith("@") or label.startswith("#"):
            return label
        if "t.co/" in href or label.startswith("http"):
            inline += 1
            return "[link]"
        return label

    body = _A_RE.sub(sub_anchor, body)
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.IGNORECASE)
    body = _TAG_RE.sub("", body)
    text = _html.unescape(body).strip()

    dropped = 0
    while text.endswith("[link]"):
        text = text[: -len("[link]")].rstrip()
        dropped += 1
        inline -= 1

    truncated = text.endswith("…") or text.endswith("...")
    return text, truncated, dropped, max(inline, 0)


def fetch_post(url: str, timeout: int = FETCH_TIMEOUT_S) -> Post:
    canon, handle, _ = canonical_status_url(url)
    query = urllib.parse.urlencode({"url": canon, "omit_script": "1", "dnt": "1"})
    req = urllib.request.Request(f"{OEMBED}?{query}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    markup = payload.get("html", "") or ""
    text, truncated, dropped, inline = _post_text_from_html(markup)
    posted = None
    md = _TAIL_DATE_RE.search(markup)
    if md:
        posted = md.group(1).strip()

    author_url = payload.get("author_url") or ""
    real_handle = author_url.rstrip("/").rsplit("/", 1)[-1] or handle

    return Post(url=canon, handle=real_handle,
                author_name=(payload.get("author_name") or "").strip(),
                text=text, posted=posted, truncated=truncated,
                links_dropped=dropped, links_inline=inline)


# ---------------------------------------------------------------- sweep ---

def _read_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return out
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        v = v.strip().strip('"').strip("'")
        if v:
            out[k.strip()] = v
    return out


def credentials_env() -> tuple[dict[str, str], str | None]:
    """Subprocess env for the vendored client, plus where the cookies came from.

    Resolution order is `last30days`' own, deliberately, so there is one place
    on this machine to fix a rotated session rather than two: process env, then
    the per-project `.claude/last30days.env`, then the global
    `~/.config/last30days/.env`. Browser extraction stays enabled as the last
    resort — it is the path the ruling named, and on this machine it is the one
    that currently fails (see the #250 resolution).

    Values are never printed, logged, or returned to a caller that formats
    them; only the source label leaves this function.
    """
    env = os.environ.copy()
    if env.get("AUTH_TOKEN") and env.get("CT0"):
        return env, "process env"
    for path, label in ((REPO / ".claude" / "last30days.env", "project last30days.env"),
                        (Path.home() / ".config" / "last30days" / ".env", "global last30days .env")):
        got = _read_env_file(path)
        if got.get("AUTH_TOKEN") and got.get("CT0"):
            env["AUTH_TOKEN"] = got["AUTH_TOKEN"]
            env["CT0"] = got["CT0"]
            return env, label
    return env, None


def redact(text: str, env: dict[str, str] | None = None) -> str:
    """Never print a session cookie, even inside somebody else's error string.

    The client's stderr is passed straight through to the console and into
    whatever a GATE RECORD captures. A secret that reaches an error message is
    a secret in a log file, which is #221's derived-file lesson in miniature.
    """
    env = env or {}
    for key in ("AUTH_TOKEN", "CT0"):
        val = env.get(key) or os.environ.get(key)
        if val and len(val) > 8:
            text = text.replace(val, f"<{key} redacted>")
    return text


def bird_available() -> tuple[bool, str]:
    if not BIRD.exists():
        return False, f"vendored X client not found at {BIRD}"
    from shutil import which
    if which("node") is None:
        return False, "node is not on PATH (the vendored client needs Node 22+)"
    return True, str(BIRD)


def bird_authenticated(timeout: int = 20) -> tuple[bool, str]:
    ok, why = bird_available()
    if not ok:
        return False, why
    env, where = credentials_env()
    try:
        done = subprocess.run(["node", str(BIRD), "--check"], env=env,
                              capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"auth check failed: {exc}"
    try:
        info = json.loads(done.stdout or "{}")
    except json.JSONDecodeError:
        info = {}
    if info.get("authenticated"):
        return True, f"session cookies from {where or info.get('source') or 'browser'}"
    warn = info.get("warnings") or []
    detail = redact("; ".join(warn) if warn else (
        info.get("error") or "not signed in to X in a local browser"), env)
    if where:
        detail = (f"stored cookies found ({where}) but the client rejected them — "
                  f"a session this old has usually rotated. {detail}")
    return False, detail


def sweep(queries: list[str], count: int, timeout: int = SWEEP_TIMEOUT_S) -> list[dict]:
    """Run each query through the vendored client. Returns candidate listings.

    A candidate's `text` here is the search payload's text, kept only so the
    author can tell one candidate from another. It is NOT the verbatim record
    — `block` re-fetches every chosen post through oEmbed, which is #247's
    discover-then-verify method and the reason its 79 URLs came back clean.
    """
    ok, why = bird_available()
    if not ok:
        raise RuntimeError(why)

    env, _ = credentials_env()
    out: list[dict] = []
    seen: set[str] = set()
    for q in queries:
        try:
            done = subprocess.run(
                ["node", str(BIRD), q, "--count", str(count), "--json"],
                capture_output=True, text=True, timeout=timeout, env=env,
                preexec_fn=os.setsid if hasattr(os, "setsid") else None)
        except subprocess.TimeoutExpired:
            out.append({"query": q, "error": f"timed out after {timeout}s"})
            continue
        except (OSError, subprocess.SubprocessError) as exc:
            out.append({"query": q, "error": str(exc)})
            continue

        if done.returncode != 0:
            out.append({"query": q, "error": redact((done.stderr or "search failed").strip(), env)})
            continue
        try:
            tweets = json.loads(done.stdout or "[]")
        except json.JSONDecodeError as exc:
            out.append({"query": q, "error": f"invalid JSON from client: {exc}"})
            continue
        if isinstance(tweets, dict):
            if tweets.get("error"):
                out.append({"query": q, "error": tweets["error"]})
                continue
            tweets = tweets.get("tweets") or tweets.get("items") or []

        for t in tweets:
            if not isinstance(t, dict):
                continue
            author = t.get("author") or t.get("user") or {}
            handle = (author.get("username") or author.get("screen_name") or "").lstrip("@")
            sid = str(t.get("id") or t.get("id_str") or "")
            url = t.get("permanent_url") or t.get("url") or (
                f"https://x.com/{handle}/status/{sid}" if handle and sid else "")
            if not url or url in seen:
                continue
            seen.add(url)
            out.append({
                "query": q,
                "url": url,
                "handle": handle,
                "text": (t.get("text") or "").strip(),
                "posted": t.get("createdAt") or t.get("created_at"),
                "is_reply": bool(t.get("inReplyToStatusId")
                                 or t.get("in_reply_to_status_id_str")),
            })
    return out


# ---------------------------------------------------------------- block ---

def render_block(post: Post, slug: str, surface: str, media: str | None,
                 when: date | None = None) -> str:
    """The shape the X contract fixes. First line is the sentinel, and the
    gates refuse to index any file that starts with it — a block passed in a
    transcript's place would turn the origin gate from a leak-catcher into a
    leak-licenser."""
    if surface not in SURFACES:
        raise ValueError(f"surface must be one of {SURFACES}, got {surface!r}")
    when = when or date.today()
    media_line = media.strip() if media else "none"
    note = []
    if post.truncated:
        note.append("X truncated this post at the embed limit; the words above are exact "
                    "and there are more after them")
    if post.links_dropped:
        note.append(f"{post.links_dropped} trailing t.co shortener(s) dropped")
    if post.links_inline:
        note.append(f"{post.links_inline} inline link(s) shown as [link]")

    lines = [
        f"{SENTINEL} — {slug} — {when.isoformat()}",
        f"Source: {post.url}",
        f"Author: @{post.handle}",
        "Post: " + post.text.replace("\n", "\n      "),
        f"Media: {media_line}",
        f"Surface: {surface}",
    ]
    if note:
        lines.append("Fetch: " + "; ".join(note))
    lines += [
        "",
        "This block is someone else's words. It carries nothing from the author, it is",
        "never indexed as permitted vocabulary, and any fact about his own week that the",
        "draft turns out to need goes on the ASK LIST and comes back as a separate",
        "mini-transcript. Never merge the two files.",
        "",
    ]
    return "\n".join(lines)


def parse_block(text: str) -> dict:
    """Read a block back. Returns the typed fields plus `post`, the verbatim
    text the gates treat as forbidden strings."""
    lines = text.splitlines()
    if not lines or not lines[0].startswith(SENTINEL):
        raise ValueError(f"not a stimulus block: first line must start with {SENTINEL!r}")
    head = lines[0][len(SENTINEL):].strip(" —-")
    parts = [p.strip() for p in head.split("—")]
    out: dict = {"slug": parts[0] if parts else "",
                 "date": parts[1] if len(parts) > 1 else "",
                 "source": "", "author": "", "post": "", "media": "",
                 "surface": "", "fetch": ""}
    field = None
    body: list[str] = []
    for raw in lines[1:]:
        m = re.match(r"^(Source|Author|Post|Media|Surface|Fetch):\s?(.*)$", raw)
        if m:
            if field == "post":
                out["post"] = "\n".join(body).strip()
                body = []
            field = m.group(1).lower()
            if field == "post":
                body = [m.group(2)]
            else:
                out[field] = m.group(2).strip()
            continue
        if field == "post":
            if raw.startswith("      "):
                body.append(raw[6:])
            elif raw.strip() == "":
                out["post"] = "\n".join(body).strip()
                body, field = [], None
            else:
                body.append(raw)
    if field == "post":
        out["post"] = "\n".join(body).strip()
    return out


def load_block(path: Path) -> dict:
    return parse_block(path.read_text(encoding="utf-8"))


def is_stimulus(text: str) -> bool:
    for line in text.splitlines():
        if line.strip():
            return line.startswith(SENTINEL)
    return False


def check_block(data: dict) -> list[str]:
    problems = []
    if not data.get("slug"):
        problems.append("header has no slug")
    if not data.get("source", "").startswith("https://x.com/"):
        problems.append("Source is not an x.com permalink")
    if not data.get("author", "").startswith("@"):
        problems.append("Author is not an @handle")
    if not data.get("post"):
        problems.append("Post is empty — there is nothing to react to")
    if data.get("surface") not in SURFACES:
        problems.append(f"Surface must be one of {SURFACES}")
    if not data.get("media"):
        problems.append("Media is unset — write 'none' rather than leaving it blank")
    return problems


# ------------------------------------------------------------ watchlist ---
#
# Ruled on #251. Three lanes, each found by a different search: A experimenters
# (second ring, outbound only), B news/watchers (artifact search), C reach
# (accounts Lane A engages with, admitted BY EYE -- see the file for why).

WATCHLIST = REPO / "creative-studio" / "content-machine" / "watchlist.md"
_LANE_RE = re.compile(r"^##\s+Lane\s+([ABC])\b")
_ENTRY_RE = re.compile(r"^-\s+@([A-Za-z0-9_]{1,15})\s*—\s*(.*)$")
_CAVEAT_RE = re.compile(r"\[caveat:\s*(.*?)\]", re.DOTALL)


@dataclass
class Account:
    handle: str
    lane: str
    note: str
    reach: bool
    caveat: str | None


def parse_watchlist(text: str) -> list[Account]:
    """Accounts, lane-scoped.

    Only `- @handle — ...` lines **inside a `## Lane X` heading** count. Any
    other `## ` heading closes the lane, which is what keeps the file's own
    Rejected section from arming the sweep with the accounts it rejected --
    the same failure the coined-lines ledger hit when its worked example
    parsed as a live entry (#250).
    """
    out, lane = [], None
    for raw in text.splitlines():
        m_lane = _LANE_RE.match(raw)
        if m_lane:
            lane = m_lane.group(1)
            continue
        if raw.startswith("## "):
            lane = None
            continue
        if lane is None:
            continue
        m = _ENTRY_RE.match(raw)
        if not m:
            continue
        note = m.group(2).strip()
        cav = _CAVEAT_RE.search(note)
        out.append(Account(handle=m.group(1), lane=lane, note=note,
                           reach="[reach]" in note,
                           caveat=cav.group(1).strip() if cav else None))
    return out


def load_watchlist(path: Path | None = None) -> list[Account]:
    path = path or WATCHLIST
    if not path.exists():
        raise FileNotFoundError(
            f"no watchlist at {path}\n"
            "  It is git-ignored and therefore per-machine (#251/#252): a fresh clone has none,\n"
            "  and neither does the Mac Mini. Seed it from the 19 accounts in issue #247.\n"
            "  Refusing to sweep nothing and report clean.")
    return parse_watchlist(path.read_text(encoding="utf-8"))


def _or_chain(handles: list[str]) -> str:
    return "(" + " OR ".join(f"from:{h}" for h in handles) + ")"


def deck_candidates(accounts: list[Account], days: int, per_account: int,
                    want: int, timeout: int = SWEEP_TIMEOUT_S) -> tuple[list[dict], list[dict]]:
    """Retrieve wide, one query per lane; the deck is narrowed downstream.

    Per-lane queries rather than one big OR chain, because lanes are different
    populations and a single chain returns whoever posted most: a 14-handle
    chain measured 40 posts of which 17 were one account. `per_account` caps
    the same way for the same reason -- a deck of eight with three from one
    voice is not a deck.
    """
    since = (date.today() - timedelta(days=days)).isoformat()
    env, _ = credentials_env()
    by_lane: dict[str, list[Account]] = {}
    for a in accounts:
        by_lane.setdefault(a.lane, []).append(a)

    pool: list[dict] = []
    problems: list[dict] = []
    for lane, accts in sorted(by_lane.items()):
        handles = [a.handle for a in accts]
        meta = {a.handle.lower(): a for a in accts}
        # Batches of ten keep the query well under X's length limits and keep a
        # single unparseable handle from taking a whole lane down with it.
        for i in range(0, len(handles), 10):
            batch = handles[i:i + 10]
            q = f"{_or_chain(batch)} -filter:replies since:{since}"
            try:
                rows = sweep([q], count=max(want * 4, 40), timeout=timeout)
            except RuntimeError as exc:
                problems.append({"lane": lane, "error": str(exc)})
                continue
            for r in rows:
                if "error" in r:
                    problems.append({"lane": lane, "error": r["error"]})
                    continue
                acct = meta.get(r["handle"].lower())
                pool.append({**r, "lane": lane,
                             "reach": bool(acct and acct.reach),
                             "caveat": acct.caveat if acct else None})

    seen: set[str] = set()
    counts: dict[str, int] = {}
    kept: list[dict] = []
    for r in pool:
        if r["url"] in seen or not r["text"]:
            continue
        h = r["handle"].lower()
        if counts.get(h, 0) >= per_account:
            continue
        seen.add(r["url"])
        counts[h] = counts.get(h, 0) + 1
        kept.append(r)
    return kept, problems


def is_ignored(path: Path, repo: Path = REPO) -> bool:
    try:
        done = subprocess.run(["git", "check-ignore", "-q", str(path)],
                              cwd=repo, capture_output=True, timeout=10)
        return done.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# ------------------------------------------------------------------ cli ---

def _cmd_auth(args) -> int:
    ok, why = bird_authenticated()
    print(f"X session: {'available' if ok else 'UNAVAILABLE'} — {why}")
    if not ok:
        print("  Sign in to x.com in Safari, Chrome or Firefox on this machine, then re-run.")
    return 0 if ok else 1


def _cmd_sweep(args) -> int:
    if not args.query:
        print("sweep: no --query given. This script does not invent queries;\n"
              "       what X's sweep searches on is #251.", file=sys.stderr)
        return 2
    try:
        rows = sweep(args.query, args.count)
    except RuntimeError as exc:
        print(f"sweep: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    hits = [r for r in rows if "url" in r]
    errs = [r for r in rows if "error" in r]
    for r in errs:
        print(f"  ! {r['query']}: {r['error']}")
    print(f"X sweep — {len(hits)} candidate(s) across {len(args.query)} query/queries\n")
    for r in hits:
        flag = " [reply]" if r.get("is_reply") else ""
        print(f"  @{r['handle']}{flag}  {r['url']}")
        print(f"    {r['text'][:200]}")
        print()
    if hits:
        print("Text above is the search payload, not the record. `block` re-fetches the one")
        print("you pick through publish.x.com/oembed before writing anything down.")
    return 0


def _cmd_fetch(args) -> int:
    try:
        post = fetch_post(args.url)
    except Exception as exc:
        print(f"fetch: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(post.to_json(), indent=2))
        return 0
    print(f"@{post.handle} ({post.author_name}) — {post.posted or 'date unknown'}")
    print(post.text)
    if post.truncated:
        print("\n[truncated by X at the embed limit — the words above are exact, there are more]")
    return 0


def _cmd_block(args) -> int:
    try:
        post = fetch_post(args.url)
    except Exception as exc:
        print(f"block: {exc}", file=sys.stderr)
        return 1
    if not post.text:
        print("block: oEmbed returned no post text (a link-only post has nothing to react to).",
              file=sys.stderr)
        return 1
    rendered = render_block(post, args.slug, args.surface, args.media)
    if args.stdout:
        print(rendered)
        return 0

    out_dir = Path(args.out) if args.out else BLOCKS_DIR
    target = out_dir / f"{date.today().isoformat()}-{args.slug}.md"
    # Ask about the file, not the directory. A `dir/` rule in .gitignore matches
    # directories only, and `git check-ignore` cannot tell that a path which does
    # not exist yet is a directory — so the directory form reported "not ignored"
    # and refused a correctly-ignored destination on every machine where
    # `stimulus/` had not been created yet (#255, the route's first live run).
    if not is_ignored(target, REPO):
        print(f"block: refusing to write to {target} — it is not git-ignored.\n"
              "       A stimulus block is an unpublished editorial artifact in a public repo.",
              file=sys.stderr)
        return 2
    out_dir.mkdir(parents=True, exist_ok=True)
    if target.exists() and not args.force:
        print(f"block: {target} exists (use --force to overwrite)", file=sys.stderr)
        return 1
    target.write_text(rendered, encoding="utf-8")
    print(f"wrote {target}")
    if post.truncated:
        print("  note: X truncated the post at the embed limit — read the permalink before drafting")
    print("  Media: is a placeholder unless you passed --media; oEmbed returns no media.")
    return 0


def _cmd_watchlist(args) -> int:
    try:
        accts = load_watchlist(Path(args.path) if args.path else None)
    except FileNotFoundError as exc:
        print(f"watchlist: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps([asdict(a) for a in accts], indent=2))
        return 0
    if not accts:
        print("watchlist: parsed 0 accounts. A lane heading is `## Lane A|B|C`,")
        print("           and an entry is `- @handle — note`. Nothing else counts.")
        return 1
    names = {"A": "Experimenters", "B": "News / watchers", "C": "Reach"}
    for lane in ("A", "B", "C"):
        rows = [a for a in accts if a.lane == lane]
        print(f"Lane {lane} — {names[lane]} ({len(rows)})")
        for a in rows:
            tags = " [reach]" if a.reach else ""
            print(f"   @{a.handle}{tags}")
            if a.caveat:
                print(f"      caveat: {a.caveat[:100]}")
        print()
    print(f"{len(accts)} accounts. Lane C is admitted by eye, never by metric — the first")
    print("harvest ranked an antisemitic account top on every number available (#251).")
    return 0


def _cmd_deck(args) -> int:
    try:
        accts = load_watchlist(Path(args.path) if args.path else None)
    except FileNotFoundError as exc:
        print(f"deck: {exc}", file=sys.stderr)
        return 2
    if not accts:
        print("deck: watchlist parsed 0 accounts — refusing to sweep nothing.", file=sys.stderr)
        return 1

    pool, problems = deck_candidates(accts, args.days, args.per_account, args.size)
    if args.json:
        print(json.dumps({"pool": pool, "problems": problems,
                          "accounts": len(accts), "size": args.size}, indent=2))
        return 0

    for p in problems:
        print(f"  ! lane {p['lane']}: {p['error'][:160]}")
    print(f"X candidate pool — {len(pool)} posts from {len(accts)} watchlist accounts, "
          f"last {args.days} day(s)\n")
    for r in pool:
        tags = f"[{r['lane']}]" + (" [reach]" if r["reach"] else "")
        print(f"  {tags} @{r['handle']}  {r['url']}")
        print(f"      {r['text'][:200]}")
        if r["caveat"]:
            print(f"      caveat: {r['caveat'][:110]}")
        print()
    print("This is the POOL, not the deck. Retrieve wide, deck narrow (#251):")
    print(f"  1. rank the pool and take the top {args.size} — ranking candidates is not the")
    print("     scoring loop L8 bans (#169)")
    print("  2. `block <url>` each pick, which re-fetches verbatim text through oEmbed")
    print("  3. draft ONE candidate per stimulus in an isolated clean-context spawn — eight")
    print("     drafted in one context converge into variations of the first (#221)")
    print("  4. hand back 8 ranked pairs: each draft shown with the post it answers, because")
    print("     a reply is unreadable without its setup")
    return 0


def _cmd_check(args) -> int:
    path = Path(args.path)
    text = path.read_text(encoding="utf-8")
    if not is_stimulus(text):
        print(f"check: {path} does not start with {SENTINEL!r} — this is not a stimulus block.",
              file=sys.stderr)
        return 2
    data = load_block(path)
    problems = check_block(data)
    if args.json:
        print(json.dumps({"path": str(path), "fields": data, "problems": problems}, indent=2))
        return 1 if problems else 0
    print(f"stimulus block: {path}")
    print(f"  slug    : {data['slug']}")
    print(f"  source  : {data['source']}")
    print(f"  author  : {data['author']}")
    print(f"  surface : {data['surface']}")
    print(f"  post    : {len(data['post'].split())} words")
    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("\nShape is good. Remember its polarity: forbidden strings, never vocabulary.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="stimulus.py", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("auth", help="is there a usable X session on this machine")
    p.set_defaults(fn=_cmd_auth)

    p = sub.add_parser("sweep", help="search the author's own logged-in X")
    p.add_argument("--query", action="append", default=[],
                   help="a search query; repeatable. Required — this script invents none (#251)")
    p.add_argument("--count", type=int, default=20, help="results per query (default 20)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_cmd_sweep)

    p = sub.add_parser("fetch", help="verbatim post text via publish.x.com/oembed")
    p.add_argument("url")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_cmd_fetch)

    p = sub.add_parser("block", help="write the stimulus block for one post")
    p.add_argument("url")
    p.add_argument("--slug", required=True)
    p.add_argument("--surface", required=True, choices=list(SURFACES))
    p.add_argument("--media", default=None, help="what an attached image or video shows")
    p.add_argument("--out", default=None, help="directory (must be git-ignored)")
    p.add_argument("--force", action="store_true")
    p.add_argument("--stdout", action="store_true", help="print instead of writing")
    p.set_defaults(fn=_cmd_block)

    p = sub.add_parser("watchlist", help="parse and show the watchlist lanes")
    p.add_argument("--path", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_cmd_watchlist)

    p = sub.add_parser("deck", help="retrieve the candidate pool across the watchlist")
    p.add_argument("--size", type=int, default=8, help="deck size the pool is narrowed to (default 8)")
    p.add_argument("--days", type=int, default=3, help="window in days (default 3)")
    p.add_argument("--per-account", type=int, default=2, help="cap per account (default 2)")
    p.add_argument("--path", default=None)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_cmd_deck)

    p = sub.add_parser("check", help="validate a block's shape")
    p.add_argument("path")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=_cmd_check)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
