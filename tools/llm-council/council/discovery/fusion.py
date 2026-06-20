# council/discovery/fusion.py
"""Stage 2 — one OpenRouter Fusion call: panel reasons over the evidence bundle, judge clusters pain points."""

import json
from dataclasses import dataclass, field

import httpx

from council.discovery.evidence import EvidenceBundle
from council.discovery.tiers import TierConfig

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class FusionError(Exception):
    pass


@dataclass
class CandidatePainPoint:
    title: str
    summary: str
    quotes: list[str]
    urls: list[str]
    consensus: str = ""
    intensity: int = 0
    recency: str = ""
    segment: str = ""


@dataclass
class FusionResult:
    pain_points: list[CandidatePainPoint] = field(default_factory=list)
    blind_spots: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    web_calls: int = 0
    cost: float = 0.0


def _evidence_block(bundle: EvidenceBundle) -> str:
    lines = []
    for r in bundle.records:
        lines.append(f"[{r.source_type}/{r.source_name} | {r.date} | {r.url}] {r.quote}")
    return "\n".join(lines)


_JUDGE_INSTRUCTION = (
    "You are the judge of a multi-model discovery panel. Cluster the panel's findings into "
    "user PAIN POINTS grounded ONLY in the evidence provided. Return ONLY a JSON object: "
    '{"pain_points":[{"title","summary","quotes":[verbatim strings from evidence],'
    '"urls":[urls from evidence that contain those quotes],"consensus","intensity":1-5,'
    '"recency","segment"}],"blind_spots":[strings],"contradictions":[strings]}. '
    "Every quote MUST be copied verbatim from the evidence and every url MUST appear in the evidence. "
    "Do not invent sources."
)


def _build_body(bundle: EvidenceBundle, tier: TierConfig, topic: str) -> dict:
    user = (
        f"TOPIC: {topic}\n\nEVIDENCE (real, fetched):\n{_evidence_block(bundle)}\n\n"
        "Find the highest-signal user pain points. Use web_search only to fill gaps."
    )
    # Shape confirmed correct against a live 200 response (see FUSION_SCHEMA.md).
    return {
        "model": tier.judge,
        "messages": [
            {"role": "system", "content": _JUDGE_INSTRUCTION},
            {"role": "user", "content": user},
        ],
        "tools": [{"type": "openrouter:fusion"}],
        "tool_choice": "required",
        "fusion": {
            "analysis_models": list(tier.panel),
            "max_tool_calls": tier.max_tool_calls,
        },
    }


def _parse(content: str) -> dict | None:
    text = (content or "").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return None
    return data if "pain_points" in data else None


def _web_calls(usage: dict) -> int:
    # Real captured path (FUSION_SCHEMA.md): usage.server_tool_use_details.tool_calls_executed
    details = usage.get("server_tool_use_details") or {}
    return int(details.get("tool_calls_executed", 0) or 0)


def _to_result(data: dict, usage: dict) -> FusionResult:
    pts = [
        CandidatePainPoint(
            title=p.get("title", ""), summary=p.get("summary", ""),
            quotes=list(p.get("quotes", [])), urls=list(p.get("urls", [])),
            consensus=p.get("consensus", ""), intensity=int(p.get("intensity", 0) or 0),
            recency=p.get("recency", ""), segment=p.get("segment", ""),
        )
        for p in data.get("pain_points", [])
    ]
    return FusionResult(
        pain_points=pts,
        blind_spots=list(data.get("blind_spots", [])),
        contradictions=list(data.get("contradictions", [])),
        tokens_in=usage.get("prompt_tokens", 0),
        tokens_out=usage.get("completion_tokens", 0),
        web_calls=_web_calls(usage),
        cost=float(usage.get("cost", 0.0) or 0.0),
    )


async def fuse(*, api_key: str, bundle: EvidenceBundle, tier: TierConfig, topic: str, timeout: float = 180.0) -> FusionResult:
    body = _build_body(bundle, tier, topic)
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(2):
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            if resp.status_code >= 400:
                try:
                    msg = resp.json().get("error", {}).get("message") or resp.text
                except Exception:
                    msg = resp.text
                raise FusionError(f"OpenRouter {resp.status_code} on Fusion call (judge={tier.judge}): {msg}")
            payload = resp.json()
            choice = (payload.get("choices") or [{}])[0]
            content = choice.get("message", {}).get("content", "")
            data = _parse(content)
            if data is not None:
                return _to_result(data, payload.get("usage", {}))
            body["messages"][0]["content"] = _JUDGE_INSTRUCTION + "\n\nReturn ONLY the JSON object."
        raise FusionError("Fusion judge did not return parseable pain-point JSON after retry.")
