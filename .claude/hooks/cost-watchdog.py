#!/usr/bin/env python3
"""
PostToolUse hook: Track cumulative cost per session and block if over budget.

Reads estimated cost from hook_data (if provided by the SDK) or estimates
based on tool type. Maintains a running total per session. Blocks when
the session exceeds the configured budget.

Hook type: PostToolUse
Exit codes: 0 = allow, 2 = deny (budget exceeded)

Budget default: $0.50 (matches config.toml safety.max_budget_default)
"""

import json
import os
import sys
import tempfile

# Default budget per session (USD)
DEFAULT_BUDGET = 0.50
STATE_DIR = os.path.join(tempfile.gettempdir(), "claude-hooks")

# Rough cost estimates per tool call type (USD)
# These are conservative estimates for API-backed operations
TOOL_COST_ESTIMATES = {
    "claude_api": 0.02,   # ~1K tokens at Sonnet rates
    "read": 0.0,
    "write": 0.0,
    "edit": 0.0,
    "bash": 0.0,
    "glob": 0.0,
    "grep": 0.0,
    "default": 0.001,     # Minimal cost for unknown tools
}


def _state_file(session_id: str) -> str:
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, f"cost-watchdog-{session_id}.json")


def main() -> None:
    try:
        hook_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    session_id = hook_data.get("session_id", os.environ.get("CLAUDE_SESSION_ID", "default"))
    tool = hook_data.get("tool", "").lower()
    budget = float(os.environ.get("AGENT_BUDGET_USD", DEFAULT_BUDGET))

    # Use explicit cost if provided, otherwise estimate
    cost = hook_data.get("cost_usd")
    if cost is None:
        cost = TOOL_COST_ESTIMATES.get(tool, TOOL_COST_ESTIMATES["default"])

    # Load running total
    sf = _state_file(session_id)
    try:
        with open(sf) as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        state = {"total_usd": 0.0, "call_count": 0}

    state["total_usd"] += cost
    state["call_count"] += 1

    # Write back
    with open(sf, "w") as f:
        json.dump(state, f)

    # Check budget
    if state["total_usd"] >= budget:
        print(
            f"BUDGET EXCEEDED: Session cost ${state['total_usd']:.4f} "
            f">= budget ${budget:.2f} after {state['call_count']} calls.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
