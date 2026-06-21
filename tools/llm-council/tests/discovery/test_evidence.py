from council.discovery.evidence import EvidenceRecord, EvidenceBundle


def _rec(url="https://r.com/1", quote="it crashes daily", **kw):
    base = dict(source_type="reddit", source_name="r/x", url=url, date="2026-06-19", quote=quote, engagement=12)
    base.update(kw)
    return EvidenceRecord(**base)


def test_add_returns_true_then_false_on_dup():
    b = EvidenceBundle()
    assert b.add(_rec()) is True
    assert b.add(_rec()) is False           # same url+quote → deduped
    assert len(b.records) == 1


def test_has_url_and_urls():
    b = EvidenceBundle()
    b.add(_rec(url="https://a.com/x"))
    b.add(_rec(url="https://b.com/y", quote="other pain"))
    assert b.has_url("https://a.com/x") is True
    assert b.has_url("https://nope.com") is False
    assert b.urls == {"https://a.com/x", "https://b.com/y"}


def test_dedup_is_case_insensitive_on_quote():
    b = EvidenceBundle()
    b.add(_rec(quote="It Crashes Daily"))
    assert b.add(_rec(quote="it crashes daily")) is False
