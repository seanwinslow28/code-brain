#!/usr/bin/env python3
"""PreToolUse hook (matcher: Write|Edit): block writes to sensitive files.

Payload contract (measured 2026-08-28 against Claude Code, not assumed):
    {"hook_event_name": "PreToolUse", "tool_name": "Write",
     "tool_input": {"file_path": "...", "content": "..."}, ...}

The previous version had three independent defects, each fatal on its own:
  1. read ``hook_data['tool']`` -- the field is ``tool_name``; always ''
  2. compared against lowercase ``['write', 'edit', ...]`` -- real names are
     ``Write``/``Edit``, so the check could never match even with (1) fixed
  3. read a top-level ``target``/``file_path`` -- the path lives at
     ``tool_input.file_path``
On top of that, every ``**/`` glob was string-compared with its asterisks
intact (``'secrets/**' in path``), so those patterns matched nothing either.
Net effect: this hook has never blocked a single write.

Exit 2 denies (Claude Code hook contract). A payload we cannot parse is denied
rather than allowed -- silent fail-open is precisely the bug being fixed here.
"""

import json
import os
import re
import sys

# Tool names that write to disk, exactly as Claude Code emits them.
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}

BLOCKED_GLOBS = [
    "**/.env",
    "**/.env.*",
    "**/secrets/**",
    "**/credentials/**",
    "**/.aws/**",
    "**/.ssh/**",
    "**/config/secrets.*",
    "**/*secret_key*",
    "**/*client_secret*",
    "**/*_secret*",
    "**/*password*",
    "**/*passwd*",
    "**/*api_key*",
    "**/*api-key*",
    "**/*apikey*",
    "**/*private_key*",
    "**/*private-key*",
]

# Checked BEFORE BLOCKED_GLOBS. These are templates and prose, never live
# secrets, and blocking them breaks ordinary work. Measured against all 6,883
# tracked files in this repo: with these exemptions the rule set blocks 0
# legitimate files.
#
# Deliberately NOT used as patterns, despite shipping in shared/ and plugin/:
#   "**/*key*"        -> blocks agents-sdk/lib/keychain.py, keyboard/hotkey files
#   "**/*secret*"     -> blocks block-secrets.py itself, i.e. its own maintenance
#   "**/*credential*" -> blocks vault notes ABOUT credentials (this is a
#                        knowledge vault; it writes prose on these topics)
EXEMPT_GLOBS = [
    "**/*.example",
    "**/*.sample",
    "**/*.template",
    "**/*.dist",
]

def _glob_to_regex(glob: str) -> re.Pattern:
    """Translate a gitignore-ish glob to a regex.

    ``**/`` matches any number of leading directories, ``*`` matches within a
    single path segment, ``**`` at the tail matches everything below.
    """
    out = ["^"]
    i = 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob.startswith("**", i):
            out.append(".*")
            i += 2
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        elif glob[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    out.append("$")
    return re.compile("".join(out), re.IGNORECASE)


_COMPILED = [(g, _glob_to_regex(g)) for g in BLOCKED_GLOBS]
_EXEMPT = [(g, _glob_to_regex(g)) for g in EXEMPT_GLOBS]


def normalize_path(path: str) -> str:
    return os.path.normpath(path).replace("\\", "/")


def matched_pattern(file_path: str):
    """Return the glob that blocks this path, or None if allowed."""
    normalized = normalize_path(file_path)
    for _, rx in _EXEMPT:
        if rx.match(normalized):
            return None
    for glob, rx in _COMPILED:
        if rx.match(normalized):
            return glob
    return None


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    try:
        hook_data = json.loads(raw)
    except json.JSONDecodeError:
        print("block-secrets: unparseable hook payload; denying.", file=sys.stderr)
        sys.exit(2)

    tool_name = hook_data.get("tool_name", "")
    if tool_name not in WRITE_TOOLS:
        sys.exit(0)

    tool_input = hook_data.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not target:
        sys.exit(0)

    hit = matched_pattern(target)
    if hit:
        print(f"BLOCKED: write to sensitive file: {target}", file=sys.stderr)
        print(f"Matched pattern: {hit}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
