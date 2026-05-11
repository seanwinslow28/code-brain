#!/usr/bin/env python3
"""Validation experiment for Hermes-style system_and_3 prompt-caching pattern.

Candidate 1 from the 2026-04-26 Hermes Agent investigation SPIKE.
Proves or disproves whether injecting cache_control: {"type": "ephemeral"}
on the skills_prompt system block gives a cache hit on the second call.

Usage (from agents-sdk/ with .venv activated):
    PYTHONPATH=. .venv/bin/python3 scripts/validate_prompt_caching.py

Requirements:
    - ANTHROPIC_API_KEY set in environment (or in .env)
    - anthropic SDK >= 0.39 (pulled in by claude-agent-sdk 0.1.63)
    - agents-sdk .venv installed

Cost estimate (claude-haiku-4-5 @ $0.80/$4/$0.08 per MTok in/cache-write/cache-read):
    - Call 1 (cache write):  ~7,700 tokens x $4.00/MTok  ~= $0.031
    - Call 2 (cache read):   ~7,700 tokens x $0.08/MTok  ~= $0.0006
    - Outputs: ~100 tokens x $4.00/MTok per call          ~= $0.0008
    Total: ~$0.033 -- well under the $0.10 hard cap.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Allow running from repo root or agents-sdk/
_REPO_ROOT = Path(__file__).parent.parent.parent
_AGENTS_SDK = Path(__file__).parent.parent
sys.path.insert(0, str(_AGENTS_SDK))

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic SDK not installed. Run: pip install anthropic", file=sys.stderr)
    sys.exit(1)

from lib.skill_loader import load_skills

# Hard cost cap -- abort if estimated spend would exceed this.
COST_CAP_USD = 0.10

# Use Haiku for cost efficiency; this test probes the cache mechanism, not model quality.
# If you want to verify production parity, swap to claude-sonnet-4-6.
MODEL = "claude-haiku-4-5-20251001"

# Same skills used by daily_driver morning mode (config.toml [agents.daily_driver].skills)
SKILLS = ["daily-driver", "vault-read-write"]

# Skills dir relative to repo root
SKILLS_DIR = _REPO_ROOT / ".claude" / "skills"

USER_MSG = "Hello. What is the current date? Reply in one sentence."


def run_experiment() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment.", file=sys.stderr)
        print("  On Sean's Mac: export ANTHROPIC_API_KEY=$(security find-generic-password "
              "-s com.sean.agents.anthropic_api_key -w)", file=sys.stderr)
        sys.exit(1)

    print(f"Loading skills from: {SKILLS_DIR}")
    if not SKILLS_DIR.exists():
        print(f"ERROR: skills dir not found: {SKILLS_DIR}", file=sys.stderr)
        sys.exit(1)

    skills_prompt = load_skills(SKILLS, SKILLS_DIR)
    token_estimate = len(skills_prompt) // 4
    print(f"Skills prompt: {len(skills_prompt):,} chars (~{token_estimate:,} tokens)")

    # Per Hermes system_and_3 pattern: inject cache_control on the system block.
    # The anthropic SDK represents this as a list of content blocks.
    system_with_cache = [
        {
            "type": "text",
            "text": skills_prompt,
            "cache_control": {"type": "ephemeral"},
        }
    ]

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\nModel: {MODEL}")
    print(f"Cost cap: ${COST_CAP_USD:.2f}")
    print("\n--- Call 1 (expect cache_creation_input_tokens > 0) ---")

    t0 = time.monotonic()
    resp1 = client.messages.create(
        model=MODEL,
        max_tokens=64,
        system=system_with_cache,
        messages=[{"role": "user", "content": USER_MSG}],
    )
    t1 = time.monotonic()

    u1 = resp1.usage
    print(f"  input_tokens:                {u1.input_tokens}")
    print(f"  cache_creation_input_tokens: {getattr(u1, 'cache_creation_input_tokens', 'N/A')}")
    print(f"  cache_read_input_tokens:     {getattr(u1, 'cache_read_input_tokens', 'N/A')}")
    print(f"  output_tokens:               {u1.output_tokens}")
    print(f"  wall_ms:                     {(t1 - t0) * 1000:.0f}")
    print(f"  response:                    {resp1.content[0].text[:120]!r}")

    # Estimate cost of call 1; abort if the two-call total would breach $0.10.
    cache_write_tokens = getattr(u1, "cache_creation_input_tokens", 0) or 0
    cost1_est = (
        (u1.input_tokens * 0.80 / 1_000_000)
        + (cache_write_tokens * 4.00 / 1_000_000)
        + (u1.output_tokens * 4.00 / 1_000_000)
    )
    print(f"  estimated cost:              ${cost1_est:.4f}")

    if cost1_est * 2 > COST_CAP_USD:
        print(f"\nABORTED: two-call cost estimate ${cost1_est * 2:.4f} > cap ${COST_CAP_USD:.2f}")
        sys.exit(2)

    print("\n--- Call 2 (expect cache_read_input_tokens > 0) ---")

    t2 = time.monotonic()
    resp2 = client.messages.create(
        model=MODEL,
        max_tokens=64,
        system=system_with_cache,
        messages=[{"role": "user", "content": USER_MSG}],
    )
    t3 = time.monotonic()

    u2 = resp2.usage
    cache_read_tokens = getattr(u2, "cache_read_input_tokens", 0) or 0
    print(f"  input_tokens:                {u2.input_tokens}")
    print(f"  cache_creation_input_tokens: {getattr(u2, 'cache_creation_input_tokens', 'N/A')}")
    print(f"  cache_read_input_tokens:     {cache_read_tokens}")
    print(f"  output_tokens:               {u2.output_tokens}")
    print(f"  wall_ms:                     {(t3 - t2) * 1000:.0f}")
    print(f"  response:                    {resp2.content[0].text[:120]!r}")

    cost2_est = (
        (u2.input_tokens * 0.80 / 1_000_000)
        + (cache_read_tokens * 0.08 / 1_000_000)
        + (u2.output_tokens * 4.00 / 1_000_000)
    )
    print(f"  estimated cost:              ${cost2_est:.4f}")

    print(f"\n--- Verdict ---")
    total_cost = cost1_est + cost2_est
    print(f"Total estimated spend: ${total_cost:.4f}")

    if cache_read_tokens > 0:
        cache_hit_pct = cache_read_tokens / max(u1.input_tokens + cache_write_tokens, 1) * 100
        print(f"CACHE HIT: {cache_read_tokens} tokens read from cache ({cache_hit_pct:.0f}% of call-1 input).")
        print("Verdict: SHIP -- explicit cache_control markers work. Port system_and_3 to daily_driver.py.")
        print()
        print("Proposed change: bypass ClaudeAgentOptions.system_prompt for morning mode.")
        print("  Instead, call anthropic.messages.create() directly with:")
        print("  system=[{\"type\": \"text\", \"text\": skills_prompt,")
        print("           \"cache_control\": {\"type\": \"ephemeral\"}}]")
        print("  + cache_control on the last 3 non-system messages (full system_and_3 pattern).")
    else:
        print("NO CACHE HIT on call 2 (cache_read_input_tokens == 0).")
        # Check if call 1 created a cache entry at all
        if cache_write_tokens == 0:
            print("Also no cache_creation on call 1.")
            print("Verdict: SKIP-DOESNT-WORK -- the model/SDK is not accepting cache_control markers.")
        else:
            print(f"Call 1 wrote {cache_write_tokens} cache tokens but call 2 didn't hit.")
            print("Possible causes: cache TTL < inter-call latency (unlikely -- calls were back-to-back),")
            print("or the system block content changed between calls (content drift).")
            print("Verdict: DEFER-AGAIN -- investigate cache TTL or content-identity issue.")


if __name__ == "__main__":
    run_experiment()
