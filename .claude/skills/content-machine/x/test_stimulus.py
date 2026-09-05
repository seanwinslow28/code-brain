#!/usr/bin/env python3
"""Offline fixture for X's route 1 (#250, #251).

No network, no watchlist on disk, no private brain — so it runs on a fresh
clone and on the Mac Mini, unlike the origin gate's older half. Every payload
below is either synthetic or a real public post captured verbatim from
publish.x.com/oembed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stimulus import (  # noqa: E402
    _post_text_from_html, canonical_status_url, check_block, is_stimulus,
    parse_block, parse_watchlist, Post, render_block,
)

# Captured from publish.x.com/oembed 2026-09-05 for a real public post.
OEMBED_HTML = (
    '<blockquote class="twitter-tweet" data-dnt="true"><p lang="en" dir="ltr">'
    'Explosion at the cheese factory<br><br>Da brie is everywhere</p>'
    '&mdash; Bob Golen (@BobGolen) <a href="https://x.com/BobGolen/status/'
    '2087727910509556132?ref_src=twsrc%5Etfw">August 13, 2026</a></blockquote>'
)

# Synthetic, exercising the three #247 conventions at once: an @mention restored
# from the anchor X expands it into, an INLINE t.co that becomes [link], a
# TRAILING t.co that is dropped (X auto-appends one for media and quote cards),
# and the ellipsis X leaves when it cuts a post at the embed limit.
OEMBED_MESSY = (
    '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">'
    'hey <a href="https://x.com/simonw">@simonw</a> see '
    '<a href="https://t.co/abc">https://t.co/abc</a> for the numbers &amp; the rest…'
    '<a href="https://t.co/zzz">https://t.co/zzz</a></p>'
    '&mdash; X (@x) <a href="https://x.com/x/status/1?ref_src=t">March 1, 2026</a></blockquote>'
)

# The trap this file exists for. Every `- @handle` line below the Rejected
# heading is an account we decided NOT to sweep. A parser that reads `- @` lines
# without lane scoping arms the watchlist with its own rejections — which is the
# coined-lines ledger bug (#250) in a second costume, where the file's worked
# example parsed as a live entry.
WATCHLIST = """# X watchlist

## How to read and edit this file

- @notanaccount — this bullet lives under a prose heading and must not parse.

## Lane A — Experimenters

- @simonw — Co-creator of Django.
- @karpathy — Founding member of OpenAI. [reach] [caveat: biggest account in the file]

## Lane B — News and watchers

- @testingcatalog — Finds unreleased features.

## Lane C — Reach

- @lennysan — Biggest PM newsletter there is.

## Rejected, with reasons

- @hsvsphere — top reach score, antisemitic account.
- @openclaw — posts its own product releases.

## Pick record

No runs yet.
"""


def test_watchlist_is_lane_scoped():
    accts = parse_watchlist(WATCHLIST)
    handles = [a.handle for a in accts]
    assert handles == ["simonw", "karpathy", "testingcatalog", "lennysan"], handles
    for banned in ("hsvsphere", "openclaw", "notanaccount"):
        assert banned not in handles, f"{banned} parsed as a live account"
    lanes = {a.handle: a.lane for a in accts}
    assert lanes == {"simonw": "A", "karpathy": "A",
                     "testingcatalog": "B", "lennysan": "C"}, lanes
    k = next(a for a in accts if a.handle == "karpathy")
    assert k.reach is True
    assert k.caveat == "biggest account in the file", k.caveat
    assert next(a for a in accts if a.handle == "simonw").caveat is None
    print("  watchlist: lane-scoped, 4 accounts, 3 traps refused")


def test_oembed_extraction():
    text, trunc, dropped, inline = _post_text_from_html(OEMBED_HTML)
    assert text == "Explosion at the cheese factory\n\nDa brie is everywhere", repr(text)
    assert (trunc, dropped, inline) == (False, 0, 0)

    text, trunc, dropped, inline = _post_text_from_html(OEMBED_MESSY)
    assert "@simonw" in text, text
    assert "[link] for the numbers & the rest…" in text, text
    assert not text.endswith("[link]"), "trailing shortener was not dropped"
    assert trunc is True, "X's embed-limit ellipsis must be reported, not read as his own"
    assert (dropped, inline) == (1, 1), (dropped, inline)
    print("  oembed: mention restored, inline [link] kept, trailing dropped, truncation flagged")


def test_url_validation():
    canon, handle, sid = canonical_status_url("https://twitter.com/BobGolen/status/2087727910509556132?s=20")
    assert canon == "https://x.com/BobGolen/status/2087727910509556132", canon
    assert (handle, sid) == ("BobGolen", "2087727910509556132")
    for bad in ("https://x.com/BobGolen", "https://x.com/search?q=cheese", "not a url"):
        try:
            canonical_status_url(bad)
        except ValueError:
            continue
        raise AssertionError(f"accepted a non-permalink: {bad}")
    print("  urls: permalinks canonicalised, profiles and searches refused")


def test_block_roundtrip():
    post = Post(url="https://x.com/BobGolen/status/2087727910509556132",
                handle="BobGolen", author_name="Bob Golen",
                text="Explosion at the cheese factory\n\nDa brie is everywhere",
                posted="August 13, 2026", truncated=False,
                links_dropped=0, links_inline=0)
    rendered = render_block(post, "fixture-cheese", "quote-post", None)
    assert is_stimulus(rendered), "the sentinel is how the origin gate refuses this file"
    data = parse_block(rendered)
    assert data["post"] == post.text, repr(data["post"])
    assert data["author"] == "@BobGolen"
    assert data["surface"] == "quote-post"
    assert data["media"] == "none", "an unset Media must read 'none', never blank"
    assert not check_block(data), check_block(data)

    # A truncated fetch must survive the round trip as a Fetch: note rather than
    # a bare ellipsis a later reader takes for the author's own.
    post.truncated = True
    assert "embed limit" in render_block(post, "s", "reply", None)

    for bad_surface in ("retweet", "", "Reply"):
        try:
            render_block(post, "s", bad_surface, None)
        except ValueError:
            continue
        raise AssertionError(f"accepted surface {bad_surface!r}")

    broken = parse_block(rendered.replace("Surface: quote-post", "Surface: retweet"))
    assert check_block(broken), "check_block missed an invalid surface"
    print("  block: round-trips, sentinel set, bad surfaces refused")


def main():
    print("X route-1 fixture (offline)")
    test_watchlist_is_lane_scoped()
    test_oembed_extraction()
    test_url_validation()
    test_block_roundtrip()
    print("\nOK")


if __name__ == "__main__":
    main()
