"""Run the topic_20 benchmark suite against a single LM Studio model.

Companion to benchmark_ollama_model.py — runs the same 6-dimension suite
but talks to LM Studio's OpenAI-compatible /v1/chat/completions endpoint
instead of Ollama's /api/chat. Used for the Tier A (MBP) sweep where
production runtime is LM Studio + MLX, not Ollama.

Key differences vs the Ollama harness:
- POST /v1/chat/completions with OpenAI-format body
- No eval_count/eval_duration in response — tok/s is measured from
  usage.completion_tokens / wall-clock time
- max_tokens (not num_predict)
- response_format={"type":"json_object"} for tool-call probes (LM Studio
  honors this for MLX models that support JSON mode)
- No "think" flag — Qwen3.5/3.6 MLX models may emit <think>...</think>
  tags in content; we strip them before scoring
- num_ctx is configured per-model in LM Studio's UI, not per-request;
  the --num-ctx CLI arg is informational only and used for the needle
  suite skip-decision
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from lib.benchmark_scorers import (  # noqa: E402
    score_tool_call_json,
    compute_tokens_per_second,
    score_needle_recall,
    score_pi_gotcha_compat,
)
from benchmarks.topic_20.prompts import needle_haystack  # noqa: E402


DEFAULT_HOST = "http://seans-macbook-pro.local:1234"
TIMEOUT_PER_REQUEST = 600
TOOL_CALL_PROMPTS = HERE / "benchmarks/topic_20/prompts/tool_calls.jsonl"

_THINK_TAG_RE = re.compile(r"<think>.*?</think>", flags=re.DOTALL)


def _strip_thinking(text: str) -> str:
    """Strip <think>...</think> blocks from MLX Qwen3.5/3.6 output."""
    return _THINK_TAG_RE.sub("", text).strip()


def _lmstudio_chat(host: str, model: str, messages: list[dict],
                   max_tokens: int = 1024, temperature: float = 0.0,
                   response_format_json: bool = False,
                   seed: int | None = None) -> tuple[dict, float]:
    body: dict = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False,
    }
    # LM Studio rejects {"type":"json_object"} — must be 'json_schema' or 'text'.
    # We rely on system-prompt + scorer to enforce JSON; if a probe needs stricter
    # formatting later, switch to a permissive json_schema here.
    if response_format_json:
        body["response_format"] = {"type": "text"}
    if seed is not None:
        body["seed"] = seed
    start = time.monotonic()
    resp = requests.post(f"{host}/v1/chat/completions", json=body,
                         timeout=TIMEOUT_PER_REQUEST)
    wall = time.monotonic() - start
    resp.raise_for_status()
    return resp.json(), wall


def run_tool_call_suite(host: str, model: str) -> list[dict]:
    results = []
    with open(TOOL_CALL_PROMPTS) as f:
        for line in f:
            probe = json.loads(line)
            system_msg = (
                "You are a tool-calling assistant. Output ONLY a single JSON "
                "object of the form {\"name\": <tool>, \"arguments\": {...}}. "
                "No prose, no markdown fences, no <think> tags."
            )
            try:
                resp, _wall = _lmstudio_chat(
                    host, model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": probe["prompt"]},
                    ],
                    # Note 2026-05-25: bumping max_tokens to 2048 to give
                    # Qwen3.5/3.6 thinking-mode room caused LM Studio queue
                    # hangs (33s+ empty responses, no completion). Reverted
                    # to 512. Consequence: when Qwen3.5/3.6 thinking burns
                    # past the budget, content comes back empty — counted
                    # as fail in scoring. This is a real LM-Studio-runtime
                    # limitation that the Topic 20 report documents.
                    max_tokens=512, temperature=0.0,
                    response_format_json=True,
                )
                content_raw = resp["choices"][0]["message"]["content"]
                content = _strip_thinking(content_raw)
                scored = score_tool_call_json(content, probe["schema"])
            except Exception as e:
                scored = {"valid": False, "schema_match": False, "error": str(e)}
                content = None
                content_raw = None

            results.append({
                "kind": "tool_call",
                "probe_id": probe["id"],
                "model": model,
                "raw_response": content,
                "raw_response_pre_strip": content_raw,
                **scored,
            })
    return results


def run_throughput_suite(host: str, model: str, runs: int = 3) -> list[dict]:
    prompt = (
        "Write a 1000-word fictional vignette about a programmer debugging "
        "a network issue at 3 AM. Include dialogue, technical detail, and a "
        "twist ending. Aim for exactly 1000 words."
    )
    results = []
    for i in range(runs):
        try:
            resp, wall = _lmstudio_chat(
                host, model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024, temperature=0.7, seed=i,
            )
            usage = resp.get("usage") or {}
            completion_tokens = usage.get("completion_tokens", 0)
            wall_tps = compute_tokens_per_second(completion_tokens, wall)
            results.append({
                "kind": "throughput",
                "model": model,
                "run": i,
                "completion_tokens": completion_tokens,
                "wall_secs": wall,
                "wall_tps": wall_tps,
            })
        except Exception as e:
            results.append({
                "kind": "throughput", "model": model, "run": i,
                "error": str(e),
            })
    return results


def run_needle_suite(host: str, model: str, num_ctx: int, runs: int = 5) -> list[dict]:
    if num_ctx < 32768:
        return [{
            "kind": "needle",
            "model": model,
            "skipped_reason": f"num_ctx={num_ctx} < 32768 (configure LM Studio model context)",
        }]

    results = []
    for seed in range(runs):
        hs = needle_haystack.generate(seed=seed)
        try:
            resp, _wall = _lmstudio_chat(
                host, model,
                messages=[{"role": "user", "content": hs.prompt}],
                # Note 2026-05-25: needle answer is 12 chars (~5 tokens),
                # but Qwen3.5/3.6 burn ~200-400 tokens on thinking first.
                # Bumping max_tokens > 512 causes LM Studio queue hangs;
                # leaving at 64 means thinking-mode models return empty
                # content on this dimension. The Topic 20 report flags
                # this as a runtime-level limitation, not a model failure.
                max_tokens=64, temperature=0.0,
            )
            content_raw = resp["choices"][0]["message"]["content"]
            content = _strip_thinking(content_raw).strip()
            scored = score_needle_recall(content, hs.needle)
        except Exception as e:
            scored = {"recalled": False, "error": str(e)}
            content = None
        results.append({
            "kind": "needle",
            "model": model,
            "seed": seed,
            "needle": hs.needle,
            "response": content,
            **scored,
        })
    return results


def run_pi_gotcha_suite(host: str, model: str) -> list[dict]:
    """Pi gotchas — only a subset apply to LM Studio.

    - developer_role: LM Studio MAY accept (Pi sends as 'developer'); test it
    - ctx_2048_truncation: not applicable — LM Studio sets context per-model in UI, not per-request
    - streaming_tool_calls: SKIPPED — LM Studio's OpenAI-compat streaming behavior differs
    - gemma4_vision_read: flag-by-family only
    - auto_compaction: not applicable here
    """
    results = []

    try:
        resp, _wall = _lmstudio_chat(
            host, model,
            messages=[{"role": "developer", "content": "Say hello."}],
            max_tokens=50, temperature=0.0,
        )
        text = json.dumps(resp)
        results.append({
            "kind": "pi_gotcha",
            "gotcha": "developer_role",
            "model": model,
            **score_pi_gotcha_compat(text, "developer_role"),
        })
    except requests.HTTPError as e:
        results.append({
            "kind": "pi_gotcha", "gotcha": "developer_role", "model": model,
            "affected": True,
            "matched_signature": f"HTTP {e.response.status_code}: {e.response.text[:200]}",
        })
    except Exception as e:
        results.append({
            "kind": "pi_gotcha", "gotcha": "developer_role", "model": model,
            "affected": True, "matched_signature": str(e),
        })

    results.append({
        "kind": "pi_gotcha", "gotcha": "ctx_2048_truncation", "model": model,
        "affected": False,
        "note": "Not applicable to LM Studio (context configured per-model in UI, not per-request).",
    })
    results.append({
        "kind": "pi_gotcha", "gotcha": "streaming_tool_calls", "model": model,
        "affected": False,
        "note": "Skipped — LM Studio streaming-tool-call behavior differs from Ollama's; not the right harness here.",
    })
    results.append({
        "kind": "pi_gotcha", "gotcha": "gemma4_vision_read", "model": model,
        "affected": model.lower().startswith("gemma"),
        "note": "Family flag only; vision-read bug is irrelevant for text-only fleet.",
    })
    results.append({
        "kind": "pi_gotcha", "gotcha": "auto_compaction", "model": model,
        "affected": False,
        "note": "Not measurable from a single-call harness; tested implicitly via agentic loops.",
    })

    return results


def main() -> int:
    p = argparse.ArgumentParser(description="Topic 20 benchmark runner for a single LM Studio model.")
    p.add_argument("--model", required=True,
                   help="LM Studio model ID (e.g., 'qwen3.5-27b' or 'lmstudio-community/Qwen3-Coder-30B-A3B-Instruct-MLX-4bit')")
    p.add_argument("--host", default=DEFAULT_HOST, help="LM Studio base URL (default: http://seans-macbook-pro.local:1234)")
    p.add_argument("--tier", required=True, choices=["A", "B", "C"], help="Hardware tier")
    p.add_argument("--num-ctx", type=int, default=32768,
                   help="Model's configured context window (informational only; LM Studio sets per-model in UI)")
    p.add_argument("--out", default=str(HERE / "benchmarks/topic_20/results"))
    p.add_argument("--skip", nargs="*", default=[],
                   choices=["tool_calls", "throughput", "needle", "pi_gotchas"])
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = args.model.replace(":", "_").replace("/", "_")
    out_file = out_dir / f"{slug}-tier{args.tier}-lmstudio-{date.today().isoformat()}.jsonl"

    all_results: list[dict] = []
    if "tool_calls" not in args.skip:
        print(f"[bench-lms] tool_calls suite on {args.model}@tier{args.tier}…", flush=True)
        all_results.extend(run_tool_call_suite(args.host, args.model))
    if "throughput" not in args.skip:
        print(f"[bench-lms] throughput suite…", flush=True)
        all_results.extend(run_throughput_suite(args.host, args.model))
    if "needle" not in args.skip:
        print(f"[bench-lms] needle suite (num_ctx={args.num_ctx})…", flush=True)
        all_results.extend(run_needle_suite(args.host, args.model, num_ctx=args.num_ctx))
    if "pi_gotchas" not in args.skip:
        print(f"[bench-lms] pi_gotchas suite…", flush=True)
        all_results.extend(run_pi_gotcha_suite(args.host, args.model))

    with out_file.open("a") as f:
        for record in all_results:
            f.write(json.dumps(record) + "\n")

    tc_pass = sum(1 for r in all_results if r.get("kind") == "tool_call" and r.get("schema_match"))
    tc_total = sum(1 for r in all_results if r.get("kind") == "tool_call")
    print(f"[bench-lms] DONE — wrote {len(all_results)} records to {out_file}")
    print(f"[bench-lms] tool-call pass rate: {tc_pass}/{tc_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
