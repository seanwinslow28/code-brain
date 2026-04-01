#!/usr/bin/env python3
"""
PostToolUse hook: Detect stuck agents in tool-call loops.

Maintains a sliding window of recent tool call hashes. If the same
hash appears N times in the window, the agent is stuck — exit code 2
to kill the loop.

Hook type: PostToolUse
Exit codes: 0 = allow, 2 = deny (loop detected)
"""

import hashlib
import json
import os
import sys
import tempfile

# Sliding window size
WINDOW_SIZE = 10
# How many duplicates trigger a loop detection
LOOP_THRESHOLD = 3
# State file per session
STATE_DIR = os.path.join(tempfile.gettempdir(), "claude-hooks")


def _state_file(session_id: str) -> str:
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, f"loop-detector-{session_id}.json")


def _hash_call(tool: str, input_data: str) -> str:
    """Hash tool name + input for dedup comparison."""
    content = f"{tool}:{input_data}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def main() -> None:
    try:
        hook_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool = hook_data.get("tool", "")
    tool_input = json.dumps(hook_data.get("tool_input", {}), sort_keys=True)
    session_id = hook_data.get("session_id", os.environ.get("CLAUDE_SESSION_ID", "default"))

    call_hash = _hash_call(tool, tool_input)

    # Load existing window
    sf = _state_file(session_id)
    try:
        with open(sf) as f:
            window: list[str] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        window = []

    # Append and trim
    window.append(call_hash)
    window = window[-WINDOW_SIZE:]

    # Write back
    with open(sf, "w") as f:
        json.dump(window, f)

    # Check for loops
    if window.count(call_hash) >= LOOP_THRESHOLD:
        print(
            f"LOOP DETECTED: Tool '{tool}' called {window.count(call_hash)} times "
            f"with identical input in last {WINDOW_SIZE} calls.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
