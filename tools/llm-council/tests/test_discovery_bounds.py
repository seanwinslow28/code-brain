"""Point-of-effect bounds for paid discovery calls."""

import json

import pytest

from council.discovery import fusion
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.gather import sonar
from council.discovery.textbudget import clamp_utf8_bytes
from council.discovery.tiers import get_tier
from council.pricing import provider_price_policy


@pytest.mark.parametrize(
    ("text", "max_bytes", "expected"),
    [
        ("⚡", 1, ""),
        ("⚡", 2, ""),
        ("⚡", 3, "⚡"),
        ("a⚡b", 4, "a⚡"),
        ("a⚡b", 5, "a⚡b"),
        ("under cap", 100, "under cap"),
    ],
)
def test_clamp_utf8_bytes_never_exceeds_cap_or_splits_codepoint(
    text, max_bytes, expected
):
    out = clamp_utf8_bytes(text, max_bytes)

    assert out == expected
    assert len(out.encode("utf-8")) <= max_bytes
    assert len(out.encode("utf-8")) <= len(text.encode("utf-8"))


@pytest.mark.asyncio
async def test_sonar_request_enforces_completion_price_and_topic_bounds(httpx_mock):
    httpx_mock.add_response(
        json={
            "choices": [{"message": {"content": "No cited findings."}}],
            "citations": [],
            "usage": {},
        }
    )
    model = "perplexity/sonar"
    topic = "⚡" * 1_000

    await sonar.collect_sonar(api_key="k", topic=topic, model=model)

    body = json.loads(httpx_mock.get_requests()[0].content)
    expected_topic = "⚡" * 682  # 2,046 bytes: the longest whole prefix <= 2,048.
    assert sonar.SONAR_MAX_TOKENS == 2_048
    assert sonar.TOPIC_EMBED_MAX_BYTES == 2_048
    assert body["max_tokens"] == 2_048
    assert body["provider"] == {
        "max_price": {"prompt": 1.25, "completion": 1.25, "request": 0},
        "allow_fallbacks": False,
        "require_parameters": True,
    }
    assert body["provider"] == provider_price_policy(model)
    assert body["messages"][0]["content"] == (
        "What are the most recent, specific user complaints and unmet needs about "
        f"{expected_topic}? Quote real users where possible. Cite sources."
    )
    assert len(expected_topic.encode("utf-8")) <= sonar.TOPIC_EMBED_MAX_BYTES
    assert topic not in body["messages"][0]["content"]


@pytest.mark.asyncio
async def test_sonar_under_cap_topic_passes_through_unchanged(httpx_mock):
    httpx_mock.add_response(
        json={
            "choices": [{"message": {"content": "No cited findings."}}],
            "citations": [],
            "usage": {},
        }
    )
    topic = "under-cap ⚡ topic"

    await sonar.collect_sonar(
        api_key="k", topic=topic, model="perplexity/sonar", segment="developers"
    )

    body = json.loads(httpx_mock.get_requests()[0].content)
    assert body["messages"][0]["content"] == (
        "What are the most recent, specific user complaints and unmet needs about "
        f"{topic} specifically from the perspective of developers? "
        "Quote real users where possible. Cite sources."
    )


def _bundle(*records: EvidenceRecord) -> EvidenceBundle:
    bundle = EvidenceBundle()
    for record in records:
        bundle.add(record)
    return bundle


def _good_fusion_response() -> dict:
    return {
        "choices": [{"message": {"content": json.dumps({"pain_points": []})}}],
        "usage": {},
    }


@pytest.mark.asyncio
async def test_fusion_request_enforces_judge_bounds_and_preserves_tool_shape(
    httpx_mock,
):
    httpx_mock.add_response(json=_good_fusion_response())
    tier = get_tier("quick")
    topic = "⚡" * 1_000
    bundle = _bundle(
        EvidenceRecord(
            "reddit", "r/pm", "https://example.com/1", "2026-07-18", "slow sync"
        )
    )

    await fusion.fuse(api_key="k", bundle=bundle, tier=tier, topic=topic)

    body = json.loads(httpx_mock.get_requests()[0].content)
    expected_topic = "⚡" * 682  # 2,046 bytes: the longest whole prefix <= 2,048.
    assert fusion.FUSION_JUDGE_MAX_TOKENS == 8_192
    assert fusion.TOPIC_EMBED_MAX_BYTES == 2_048
    assert fusion.EVIDENCE_EMBED_MAX_BYTES == 131_072
    assert body["max_tokens"] == 8_192
    assert body["provider"] == {
        "max_price": {"prompt": 6.25, "completion": 37.5, "request": 0},
        "allow_fallbacks": False,
    }
    assert "require_parameters" not in body["provider"]
    expected_from_pricing = provider_price_policy(tier.judge)
    expected_from_pricing.pop("require_parameters")
    assert body["provider"] == expected_from_pricing
    assert {
        "tools": body["tools"],
        "tool_choice": body["tool_choice"],
        "fusion": body["fusion"],
    } == {
        "tools": [{"type": "openrouter:fusion"}],
        "tool_choice": "required",
        "fusion": {
            "analysis_models": list(tier.panel),
            "max_tool_calls": tier.max_tool_calls,
        },
    }
    assert body["messages"][1]["content"] == (
        f"TOPIC: {expected_topic}\n\nEVIDENCE (real, fetched):\n"
        "[reddit/r/pm | 2026-07-18 | https://example.com/1] slow sync\n\n"
        "Find the highest-signal user pain points. Use web_search only to fill gaps."
    )


@pytest.mark.asyncio
async def test_fusion_parse_retry_reuses_judge_bounds_on_both_attempts(httpx_mock):
    httpx_mock.add_response(
        json={"choices": [{"message": {"content": "not JSON"}}], "usage": {}}
    )
    httpx_mock.add_response(json=_good_fusion_response())
    tier = get_tier("quick")

    await fusion.fuse(
        api_key="k",
        bundle=_bundle(
            EvidenceRecord("web", "site", "https://example.com", "", "complaint")
        ),
        tier=tier,
        topic="topic",
    )

    bodies = [json.loads(request.content) for request in httpx_mock.get_requests()]
    assert len(bodies) == 2
    expected_provider = {
        "max_price": {"prompt": 6.25, "completion": 37.5, "request": 0},
        "allow_fallbacks": False,
    }
    assert [body["max_tokens"] for body in bodies] == [8_192, 8_192]
    assert [body["provider"] for body in bodies] == [
        expected_provider,
        expected_provider,
    ]


def _render_evidence_line(record: EvidenceRecord) -> str:
    return (
        f"[{record.source_type}/{record.source_name} | {record.date} | {record.url}] "
        f"{record.quote}"
    )


def _sent_evidence_block(user: str, topic: str) -> str:
    prefix = f"TOPIC: {topic}\n\nEVIDENCE (real, fetched):\n"
    suffix = (
        "\n\nFind the highest-signal user pain points. "
        "Use web_search only to fill gaps."
    )
    assert user.startswith(prefix)
    assert user.endswith(suffix)
    return user[len(prefix) : -len(suffix)]


@pytest.mark.asyncio
async def test_fusion_evidence_uses_whole_leading_records_and_marker_within_cap(
    httpx_mock,
):
    httpx_mock.add_response(json=_good_fusion_response())
    records = [
        EvidenceRecord(
            "web",
            f"source-{i}",
            f"https://example.com/{i}",
            "2026-07-18",
            f"record-{i}-" + ("x" * 1_000),
        )
        for i in range(150)
    ]
    bundle = _bundle(*records)
    topic = "bounded topic"

    await fusion.fuse(
        api_key="k", bundle=bundle, tier=get_tier("quick"), topic=topic
    )

    body = json.loads(httpx_mock.get_requests()[0].content)
    user = body["messages"][1]["content"]
    evidence = _sent_evidence_block(user, topic)
    lines = [_render_evidence_line(record) for record in records]
    assert len("\n".join(lines).encode("utf-8")) > 131_072

    def bounded_block(k):
        marker = f"[evidence truncated for bound: showing {k} of 150 records]"
        return "\n".join([*lines[:k], marker])

    expected_k = max(
        k for k in range(150) if len(bounded_block(k).encode("utf-8")) <= 131_072
    )
    assert evidence == bounded_block(expected_k)
    assert evidence.endswith(
        f"[evidence truncated for bound: showing {expected_k} of 150 records]"
    )
    assert len(evidence.encode("utf-8")) <= fusion.EVIDENCE_EMBED_MAX_BYTES

    fixed_framing = len(
        (
            "TOPIC: \n\nEVIDENCE (real, fetched):\n\n\n"
            "Find the highest-signal user pain points. "
            "Use web_search only to fill gaps."
        ).encode("utf-8")
    )
    assert len(user.encode("utf-8")) <= (
        len(topic.encode("utf-8"))
        + fusion.EVIDENCE_EMBED_MAX_BYTES
        + fixed_framing
    )


@pytest.mark.asyncio
async def test_fusion_small_evidence_bundle_is_embedded_in_full_without_marker(
    httpx_mock,
):
    httpx_mock.add_response(json=_good_fusion_response())
    records = [
        EvidenceRecord(
            "reddit", "r/pm", "https://example.com/1", "2026-07-18", "sync is slow"
        ),
        EvidenceRecord(
            "web", "review", "https://example.com/2", "", "pricing is opaque ⚡"
        ),
    ]
    topic = "small topic"

    await fusion.fuse(
        api_key="k",
        bundle=_bundle(*records),
        tier=get_tier("quick"),
        topic=topic,
    )

    body = json.loads(httpx_mock.get_requests()[0].content)
    evidence = _sent_evidence_block(body["messages"][1]["content"], topic)
    assert evidence == "\n".join(_render_evidence_line(record) for record in records)
    assert "[evidence truncated for bound:" not in evidence


def test_sonar_clamps_user_controlled_segment_bytes(monkeypatch):
    """Review finding (3a-2 round 2, dangerously-wrong): segment was appended raw after
    the topic clamp — a 200 KB --segment outran the priced input bound entirely."""
    import asyncio
    import httpx

    from council.discovery.gather import sonar as sonar_mod

    sent = {}

    async def fake_post(self, url, headers=None, json=None):
        sent["body"] = json
        request = httpx.Request("POST", url)
        return httpx.Response(200, json={"choices": [], "usage": {"cost": 0.0}}, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)
    huge_segment = "🧪" * 80_000  # 320,000 UTF-8 bytes of user-controlled input

    asyncio.run(
        sonar_mod.collect_sonar(
            api_key="k", topic="x", model="perplexity/sonar", segment=huge_segment
        )
    )

    content = sent["body"]["messages"][0]["content"]
    content_bytes = len(content.encode("utf-8"))
    assert content_bytes <= (
        sonar_mod.TOPIC_EMBED_MAX_BYTES + sonar_mod.SEGMENT_EMBED_MAX_BYTES + 256
    ), content_bytes
    assert content.encode("utf-8").decode("utf-8") == content  # codepoint-safe


def test_tier_registry_models_all_have_pricing_entries():
    """Review finding (3a-2 round 2, structural): a future tier edit must not outrun
    the pricing table and KeyError at fuse/sonar time — mirror the PROFILES guard."""
    from council.discovery.tiers import TIERS
    from council.pricing import MODEL_PRICING_PER_1K

    for tier in TIERS.values():
        for model in (*tier.panel, tier.judge, tier.sonar_model):
            assert model in MODEL_PRICING_PER_1K, (tier.name, model)


def test_clamp_utf8_bytes_full_boundary_matrix():
    """Review finding (3a-2 round 2, minor): prove cap-wins + codepoint safety across
    1/2/3/4-byte characters and zero/negative caps, not just ASCII + one 3-byte char."""
    from council.discovery.textbudget import clamp_utf8_bytes

    mixed = "A\u00a2\u20ac\U0001f600Z"  # 1+2+3+4+1 = 11 UTF-8 bytes
    for max_bytes in range(-3, 18):
        out = clamp_utf8_bytes(mixed, max_bytes)
        encoded = out.encode("utf-8")
        assert len(encoded) <= max(0, max_bytes), max_bytes
        assert encoded.decode("utf-8") == out
        assert mixed.startswith(out)
