from council.discovery.evidence import EvidenceBundle, EvidenceRecord


def _sample_bundle() -> EvidenceBundle:
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="reddit", source_name="r/ProductManagement",
                         url="https://example.com/a", date="2026-06-01",
                         quote="Prompts never give the same result twice.", engagement=42))
    b.add(EvidenceRecord(source_type="sonar", source_name="Perplexity Sonar",
                         url="https://example.com/b", date="", quote="Creators want a repeatable system."))
    return b


def test_to_dict_lists_all_records():
    b = _sample_bundle()
    d = b.to_dict()
    assert [r["url"] for r in d["records"]] == ["https://example.com/a", "https://example.com/b"]
    assert d["records"][0]["engagement"] == 42


def test_round_trip_equals_original():
    b = _sample_bundle()
    restored = EvidenceBundle.from_dict(b.to_dict())
    assert restored == b                      # records + _keys + urls all match
    assert restored.has_url("https://example.com/a")


def test_from_dict_restores_dedup_guard():
    b = _sample_bundle()
    restored = EvidenceBundle.from_dict(b.to_dict())
    # adding a duplicate of an existing record must be rejected (dedup key rebuilt)
    dup = EvidenceRecord(source_type="reddit", source_name="r/ProductManagement",
                         url="https://example.com/a", date="2026-06-01",
                         quote="Prompts never give the same result twice.", engagement=42)
    assert restored.add(dup) is False
