# council/discovery/textbudget.py
"""Shared text clamps for provider query limits and paid prompt byte budgets.

A user-controlled topic (and/or --segment) gets composed into provider queries by several
collectors. Exceed Brave's q-param ceiling (~50 words / ~400 chars) or GitHub search's ~256-char
limit and the search returns HTTP 422 — which, before the clamp, propagated and crashed the
Stage-5 backfill (observed 2026-06-28). Paid discovery prompts also need codepoint-safe UTF-8
byte ceilings. This is the one place both classes of text budget live.
"""

# Provider q-param hard ceilings (exceed either → HTTP 422). Clamp under these, with margin.
BRAVE_Q_MAX_WORDS = 50
BRAVE_Q_MAX_CHARS = 400
GITHUB_Q_MAX_CHARS = 256


def clamp_utf8_bytes(text: str, max_bytes: int) -> str:
    """Return the longest codepoint-safe prefix no larger than ``max_bytes``."""
    if max_bytes <= 0:
        return ""
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    return encoded[:max_bytes].decode("utf-8", errors="ignore")


def clamp_words_chars(text: str, *, max_words: int, max_chars: int) -> str:
    """Trim `text` to stay under BOTH a word and a char ceiling, breaking on a word boundary.

    Word ceiling first (the usual 422 trigger), then a char backstop that backs off to the last
    whole word (a single overlong word with no space is hard-cut to max_chars).
    """
    words = text.split()
    if len(words) > max_words:
        text = " ".join(words[:max_words])
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] or text[:max_chars]
    return text
