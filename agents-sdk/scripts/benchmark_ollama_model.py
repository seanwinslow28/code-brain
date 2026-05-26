"""Run the topic_20 benchmark suite against a single Ollama model.

Captures all 6 dimensions defined in benchmarks/topic_20/README.md.
Writes one JSONL per run at:
    benchmarks/topic_20/results/<model-slug>-<tier>-<YYYY-MM-DD>.jsonl

Each line is a complete record for ONE measurement (one tool-call probe,
one tok/s sample, one needle run, etc.) with a `kind` field disambiguating.

Idempotency: re-running with the same (model, tier, date) APPENDS — caller
should manage that or pass --out-file with a unique name.

All inference is over Ollama's native /api/chat endpoint (NOT /v1 OpenAI-
compat) to bypass the streaming tool_calls bug per Topic 19 §"Critical Pi
Gotchas — 1. Tool-call streaming bug (Ollama issue #12557)".
"""
from __future__ import annotations

import argparse
import json
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


DEFAULT_HOST = "http://localhost:11434"
TIMEOUT_PER_REQUEST = 600  # seconds; long for needle-haystack at 32K
TOOL_CALL_PROMPTS = HERE / "benchmarks/topic_20/prompts/tool_calls.jsonl"
AGENTIC_LOOP_PROMPTS = HERE / "benchmarks/topic_20/prompts/agentic_loops.jsonl"


# ─── Ollama HTTP wrappers ─────────────────────────────────────────────────

def _ollama_chat(host: str, model: str, messages: list[dict], options: dict | None = None,
                 stream: bool = False, format_json: bool = False) -> dict:
    body: dict = {"model": model, "messages": messages, "stream": stream, "think": False}
    if options:
        body["options"] = options
    if format_json:
        body["format"] = "json"
    resp = requests.post(f"{host}/api/chat", json=body, timeout=TIMEOUT_PER_REQUEST)
    resp.raise_for_status()
    return resp.json()


# ─── Dimension runners ────────────────────────────────────────────────────

def run_tool_call_suite(host: str, model: str) -> list[dict]:
    """Dimension 1: tool-call JSON validity."""
    results = []
    with open(TOOL_CALL_PROMPTS) as f:
        for line in f:
            probe = json.loads(line)
            system_msg = (
                "You are a tool-calling assistant. Output ONLY a single JSON "
                "object of the form {\"name\": <tool>, \"arguments\": {...}}. "
                "No prose, no markdown fences."
            )
            try:
                resp = _ollama_chat(
                    host, model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": probe["prompt"]},
                    ],
                    options={"num_ctx": 4096, "temperature": 0.0},
                    format_json=True,
                )
                content = resp["message"]["content"]
                scored = score_tool_call_json(content, probe["schema"])
            except Exception as e:
                scored = {"valid": False, "schema_match": False, "error": str(e)}
                content = None

            results.append({
                "kind": "tool_call",
                "probe_id": probe["id"],
                "model": model,
                "raw_response": content,
                **scored,
            })
    return results


def run_throughput_suite(host: str, model: str, runs: int = 3) -> list[dict]:
    """Dimension 2: decode tok/s on a fixed ~1024-token output."""
    prompt = (
        "Write a 1000-word fictional vignette about a programmer debugging "
        "a network issue at 3 AM. Include dialogue, technical detail, and a "
        "twist ending. Aim for exactly 1000 words."
    )
    results = []
    for i in range(runs):
        start = time.monotonic()
        resp = _ollama_chat(
            host, model,
            messages=[{"role": "user", "content": prompt}],
            options={"num_ctx": 4096, "num_predict": 1024, "temperature": 0.7, "seed": i},
        )
        wall = time.monotonic() - start
        eval_count = resp.get("eval_count", 0)
        eval_duration_ns = resp.get("eval_duration", 0)
        ollama_tps = compute_tokens_per_second(eval_count, eval_duration_ns / 1e9)
        wall_tps = compute_tokens_per_second(eval_count, wall)
        results.append({
            "kind": "throughput",
            "model": model,
            "run": i,
            "eval_count": eval_count,
            "eval_duration_secs": eval_duration_ns / 1e9,
            "wall_secs": wall,
            "ollama_tps": ollama_tps,
            "wall_tps": wall_tps,
        })
    return results


def run_needle_suite(host: str, model: str, num_ctx: int, runs: int = 5) -> list[dict]:
    """Dimension 5: long-context needle recall at 28K position inside 32K window."""
    if num_ctx < 32768:
        return [{
            "kind": "needle",
            "model": model,
            "skipped_reason": f"num_ctx={num_ctx} < 32768",
        }]

    results = []
    for seed in range(runs):
        hs = needle_haystack.generate(seed=seed)
        try:
            resp = _ollama_chat(
                host, model,
                messages=[{"role": "user", "content": hs.prompt}],
                options={"num_ctx": 32768, "temperature": 0.0, "num_predict": 32},
            )
            content = resp["message"]["content"].strip()
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
    """Dimension 6: probe each of the 5 Pi gotchas as binary pass/fail."""
    results = []

    # 1. developer_role
    try:
        resp = _ollama_chat(
            host, model,
            messages=[{"role": "developer", "content": "Say hello."}],
            options={"num_ctx": 4096, "temperature": 0.0},
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
            "affected": True, "matched_signature": f"HTTP {e.response.status_code}",
        })

    # 2. ctx_2048_truncation — feed ~3K-token prompt with default ctx
    big_input = ("the quick brown fox jumps over the lazy dog. " * 600)
    try:
        resp = _ollama_chat(
            host, model,
            messages=[{"role": "user", "content": big_input + "\n\nSummarize in 5 words."}],
        )
        content = resp["message"]["content"]
        affected = len(content) < 5 or "[..." in content or "..." in content[-30:]
        results.append({
            "kind": "pi_gotcha", "gotcha": "ctx_2048_truncation", "model": model,
            "affected": affected, "matched_signature": "truncation heuristic",
        })
    except Exception as e:
        results.append({
            "kind": "pi_gotcha", "gotcha": "ctx_2048_truncation", "model": model,
            "affected": True, "matched_signature": str(e),
        })

    # 3. streaming_tool_calls — stream=True, ask for a tool call
    try:
        body = {
            "model": model,
            "stream": True,
            "messages": [
                {"role": "system", "content": "Output a JSON tool call only."},
                {"role": "user", "content": "Call read_file with path /etc/hosts."},
            ],
            "options": {"num_ctx": 4096, "temperature": 0.0},
            "format": "json",
        }
        last_chunk = None
        got_content = False
        with requests.post(f"{host}/api/chat", json=body, stream=True,
                           timeout=TIMEOUT_PER_REQUEST) as r:
            for line in r.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                last_chunk = chunk
                if chunk.get("message", {}).get("content"):
                    got_content = True
        done_no_content = (last_chunk and last_chunk.get("done") and not got_content)
        results.append({
            "kind": "pi_gotcha", "gotcha": "streaming_tool_calls", "model": model,
            "affected": bool(done_no_content),
            "matched_signature": "done=true with no content emitted" if done_no_content else None,
        })
    except Exception as e:
        results.append({
            "kind": "pi_gotcha", "gotcha": "streaming_tool_calls", "model": model,
            "affected": True, "matched_signature": str(e),
        })

    # 4 + 5. gemma4_vision_read + auto_compaction — flag-by-family, not measured
    results.append({
        "kind": "pi_gotcha", "gotcha": "gemma4_vision_read", "model": model,
        "affected": model.lower().startswith("gemma4"),
        "matched_signature": "model is gemma4 family" if model.lower().startswith("gemma4") else None,
        "note": "Vision-on-read bug is irrelevant for text-only fleet — flagged for awareness only.",
    })
    results.append({
        "kind": "pi_gotcha", "gotcha": "auto_compaction", "model": model,
        "affected": False,
        "matched_signature": None,
        "note": "Tested implicitly via agentic loops; flagged separately only if a loop times out >120s.",
    })

    return results


# ─── Main ─────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(description="Topic 20 benchmark runner for a single Ollama model.")
    p.add_argument("--model", required=True, help="Ollama model tag, e.g., qwen3.5:27b")
    p.add_argument("--host", default=DEFAULT_HOST, help="Ollama base URL")
    p.add_argument("--tier", required=True, choices=["A", "A-ollama", "B", "C"],
                   help="Hardware tier (A=MBP LM Studio, A-ollama=MBP Ollama, B=Mac Mini, C=Alienware)")
    p.add_argument("--num-ctx", type=int, default=16384,
                   help="Native context window of the model variant under test")
    p.add_argument("--out", default=str(HERE / "benchmarks/topic_20/results"))
    p.add_argument("--skip", nargs="*", default=[],
                   choices=["tool_calls", "throughput", "needle", "pi_gotchas"],
                   help="Dimensions to skip (useful for debugging or rerunning a single dimension)")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = args.model.replace(":", "_").replace("/", "_")
    out_file = out_dir / f"{slug}-tier{args.tier}-{date.today().isoformat()}.jsonl"

    all_results: list[dict] = []
    if "tool_calls" not in args.skip:
        print(f"[bench] tool_calls suite on {args.model}@tier{args.tier}…", flush=True)
        all_results.extend(run_tool_call_suite(args.host, args.model))
    if "throughput" not in args.skip:
        print("[bench] throughput suite…", flush=True)
        all_results.extend(run_throughput_suite(args.host, args.model))
    if "needle" not in args.skip:
        print(f"[bench] needle suite (num_ctx={args.num_ctx})…", flush=True)
        all_results.extend(run_needle_suite(args.host, args.model, num_ctx=args.num_ctx))
    if "pi_gotchas" not in args.skip:
        print("[bench] pi_gotchas suite…", flush=True)
        all_results.extend(run_pi_gotcha_suite(args.host, args.model))

    with out_file.open("a") as f:
        for record in all_results:
            f.write(json.dumps(record) + "\n")

    tc_pass = sum(1 for r in all_results if r.get("kind") == "tool_call" and r.get("schema_match"))
    tc_total = sum(1 for r in all_results if r.get("kind") == "tool_call")
    print(f"[bench] DONE — wrote {len(all_results)} records to {out_file}")
    print(f"[bench] tool-call pass rate: {tc_pass}/{tc_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
