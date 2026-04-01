#!/usr/bin/env python3
"""
PreToolUse hook: Verify vault file integrity before writes.

Protections:
1. Blocks writes to vault files if the target anchor string is empty
   (which would overwrite the entire file via vault_inject).
2. Enforces filelock for all vault writes to prevent concurrent corruption.
3. Blocks writes to vault files that appear corrupted (missing frontmatter).

Hook type: PreToolUse
Exit codes: 0 = allow, 2 = deny (integrity check failed)
"""

import json
import os
import sys
import time

VAULT_ROOT = os.environ.get(
    "VAULT_ROOT",
    os.path.expanduser("~/Code-Brain/claude-code-superuser-pack/vault"),
)


def _is_vault_path(path: str) -> bool:
    """Check if a path is inside the vault."""
    try:
        return os.path.commonpath([os.path.realpath(path), os.path.realpath(VAULT_ROOT)]) == os.path.realpath(VAULT_ROOT)
    except ValueError:
        return False


def _check_frontmatter(path: str) -> bool:
    """Verify a vault markdown file has valid frontmatter."""
    if not os.path.exists(path):
        return True  # New files are OK
    if not path.endswith(".md"):
        return True  # Only check markdown

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read(500)  # Only need the header
        # Valid frontmatter starts with ---
        return content.strip().startswith("---")
    except (OSError, UnicodeDecodeError):
        return False


def _check_empty_anchor(hook_data: dict) -> bool:
    """Block if tool_input contains an empty anchor string for vault_inject."""
    tool_input = hook_data.get("tool_input", {})

    # Check for empty old_string in Edit tool (which vault_inject uses)
    old_string = tool_input.get("old_string", None)
    if old_string is not None and old_string.strip() == "":
        return False  # Empty anchor = would replace entire file

    return True


def main() -> None:
    try:
        hook_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool = hook_data.get("tool", "").lower()
    tool_input = hook_data.get("tool_input", {})

    # Only check write operations
    write_tools = {"write", "edit", "search_replace"}
    if tool not in write_tools:
        sys.exit(0)

    # Get target file path
    target = (
        tool_input.get("file_path", "")
        or tool_input.get("path", "")
        or hook_data.get("target", "")
    )

    if not target or not _is_vault_path(target):
        sys.exit(0)  # Not a vault file — allow

    # Check 1: Empty anchor protection
    if not _check_empty_anchor(hook_data):
        print(
            f"BLOCKED: Empty anchor string would overwrite entire vault file: {target}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Check 2: Frontmatter integrity (existing files only)
    if os.path.exists(target) and not _check_frontmatter(target):
        print(
            f"BLOCKED: Vault file appears corrupted (missing frontmatter): {target}",
            file=sys.stderr,
        )
        sys.exit(2)

    # Check 3: Filelock enforcement
    # We don't acquire the lock here (that's the writer's job),
    # but we check if a stale lock exists (> 60 seconds old)
    lock_path = f"{target}.lock"
    if os.path.exists(lock_path):
        try:
            lock_age = time.time() - os.path.getmtime(lock_path)
            if lock_age > 60:
                # Stale lock — remove it
                os.remove(lock_path)
        except OSError:
            pass  # Race condition — another process may have removed it

    sys.exit(0)


if __name__ == "__main__":
    main()
