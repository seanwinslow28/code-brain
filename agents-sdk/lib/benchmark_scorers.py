"""Pure scoring functions for the topic_20 benchmark harness.

Each scorer takes raw model output (or a derived measurement) and returns
a dict with at minimum a binary pass/fail field. No I/O. No state.
"""
from __future__ import annotations

import json
import re
from typing import Any


def score_tool_call_json(output: str, schema: dict[str, Any]) -> dict[str, Any]:
    """Score a single tool-call output against an expected schema.

    Returns:
        {"valid": bool, "schema_match": bool, "parsed": dict | None, "error": str | None}
    """
    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as e:
        return {"valid": False, "schema_match": False, "parsed": None, "error": str(e)}

    if not isinstance(parsed, dict):
        return {"valid": False, "schema_match": False, "parsed": parsed, "error": "not a JSON object"}

    name_match = parsed.get("name") == schema.get("name")
    args = parsed.get("arguments") or {}
    required = schema.get("required") or []
    args_present = all(key in args for key in required)

    return {
        "valid": True,
        "schema_match": bool(name_match and args_present),
        "parsed": parsed,
        "error": None,
    }


def compute_tokens_per_second(token_count: int, elapsed_seconds: float) -> float:
    """Return decode tok/s. Returns 0.0 if elapsed_seconds is 0 (no division by zero)."""
    if elapsed_seconds <= 0:
        return 0.0
    return float(token_count) / float(elapsed_seconds)


def score_needle_recall(response: str, needle: str) -> dict[str, Any]:
    """Binary recall check — is the needle string present in the response?"""
    return {"recalled": needle in response, "needle": needle}


_PI_GOTCHA_SIGNATURES: dict[str, list[str]] = {
    "developer_role": ["unknown role: developer", r"role.*developer"],
    "ctx_2048_truncation": ["context length exceeded", "truncated", "max tokens"],
    "streaming_tool_calls": [r'"finish_reason":"stop"', r'"content":""'],
    "gemma4_vision_read": ["image_url required", "binary data not accepted"],
    "auto_compaction": ["session truncated", "compaction overflow"],
}


def score_pi_gotcha_compat(response_text: str, gotcha: str) -> dict[str, Any]:
    """Binary affected-by-gotcha check.

    Returns {"affected": True} if the response text contains any failure
    signature for the named gotcha, False otherwise.
    """
    sigs = _PI_GOTCHA_SIGNATURES.get(gotcha, [])
    for sig in sigs:
        if re.search(sig, response_text, re.IGNORECASE):
            return {"affected": True, "matched_signature": sig}
    return {"affected": False, "matched_signature": None}
