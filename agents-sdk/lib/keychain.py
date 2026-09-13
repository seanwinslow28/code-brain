"""macOS Keychain credential helper for the agent fleet.

Service prefix: com.sean.agents
All credentials are stored/retrieved via the `security` CLI tool.
No .env files — this is the only sanctioned credential path.

Usage as a module:
    from lib.keychain import get_credential, set_credential
    api_key = get_credential("anthropic_api_key")

Usage as a CLI:
    python3 lib/keychain.py set anthropic_api_key sk-ant-...
    pbpaste | python3 lib/keychain.py set --stdin anthropic_api_key  # secret off argv
    python3 lib/keychain.py get anthropic_api_key
    python3 lib/keychain.py list
    python3 lib/keychain.py delete anthropic_api_key
"""

from __future__ import annotations

import subprocess
import sys

SERVICE_PREFIX = "com.sean.agents"


def _run_security(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a macOS `security` command."""
    return subprocess.run(
        ["security", *args],
        capture_output=True,
        text=True,
        check=check,
    )


def set_credential(name: str, value: str) -> None:
    """Store a credential in macOS Keychain.

    Overwrites if the entry already exists.
    """
    service = f"{SERVICE_PREFIX}.{name}"
    # Delete existing entry (ignore errors if not found)
    _run_security(
        ["delete-generic-password", "-s", service, "-a", name],
        check=False,
    )
    _run_security([
        "add-generic-password",
        "-s", service,
        "-a", name,
        "-w", value,
        "-U",  # update if exists
    ])


def get_credential(name: str) -> str | None:
    """Retrieve a credential from macOS Keychain.

    Returns None if not found.
    """
    service = f"{SERVICE_PREFIX}.{name}"
    result = _run_security(
        ["find-generic-password", "-s", service, "-a", name, "-w"],
        check=False,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def list_credentials() -> list[str]:
    """List all credential names stored under our service prefix.

    Parses `security dump-keychain` output for our service prefix.
    """
    result = _run_security(["dump-keychain"], check=False)
    if result.returncode != 0:
        return []

    names: list[str] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith('"svce"') and SERVICE_PREFIX in line:
            # Extract the service name after the prefix dot
            # Format: "svce"<blob>="com.sean.agents.credential_name"
            start = line.find(SERVICE_PREFIX)
            if start == -1:
                continue
            end = line.find('"', start)
            full_service = line[start:end] if end != -1 else line[start:]
            suffix = full_service[len(SERVICE_PREFIX) + 1:]  # strip prefix + dot
            if suffix:
                names.append(suffix)
    return sorted(set(names))


def delete_credential(name: str) -> bool:
    """Delete a credential from macOS Keychain.

    Returns True if deleted, False if not found.
    """
    service = f"{SERVICE_PREFIX}.{name}"
    result = _run_security(
        ["delete-generic-password", "-s", service, "-a", name],
        check=False,
    )
    return result.returncode == 0


USAGE = (
    "Usage: python3 lib/keychain.py <set|get|list|delete> [name] [value]\n"
    "  set --stdin <name>   read the value from stdin — keeps the secret off the\n"
    "                       command line, so no shell parse and no shell history.\n"
    "                       e.g. pbpaste | python3 lib/keychain.py set --stdin claude_code_oauth_token"
)


def _read_stdin_value() -> str:
    """Read a single-line secret from stdin.

    Strips the trailing newline a pipe adds and nothing else: leading and
    interior characters belong to the secret. An interior newline means the
    caller piped a transcript rather than a bare token, which is how a
    truncated 34-character credential once ended up in the Keychain looking
    healthy — refuse it instead of storing junk.
    """
    value = sys.stdin.read().rstrip("\r\n")
    if not value:
        raise ValueError("no value on stdin")
    if "\n" in value or "\r" in value:
        raise ValueError("value spans multiple lines — pipe only the secret itself")
    return value


def _cli(argv: list[str] | None = None) -> None:
    """CLI entry point for manual credential management."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(USAGE)
        sys.exit(1)

    command, rest = args[0], args[1:]

    if command == "set":
        if rest[:1] == ["--stdin"]:
            if len(rest) != 2:
                print("Usage: <producer> | python3 lib/keychain.py set --stdin <name>")
                sys.exit(1)
            name = rest[1]
            try:
                value = _read_stdin_value()
            except ValueError as exc:
                print(f"Refusing to store: {exc}")
                sys.exit(1)
        else:
            if len(rest) != 2:
                print("Usage: python3 lib/keychain.py set <name> <value>")
                print("   or: <producer> | python3 lib/keychain.py set --stdin <name>")
                sys.exit(1)
            name, value = rest
        set_credential(name, value)
        # Length only, never the value — this is the round-trip check that would
        # have caught the truncated token years earlier.
        print(f"Stored: {name} ({len(value)} chars)")

    elif command == "get":
        if len(rest) != 1:
            print("Usage: python3 lib/keychain.py get <name>")
            sys.exit(1)
        value = get_credential(rest[0])
        if value is None:
            print(f"Not found: {rest[0]}")
            sys.exit(1)
        print(value)

    elif command == "list":
        creds = list_credentials()
        if not creds:
            print("No credentials found.")
        else:
            for name in creds:
                print(f"  {name}")

    elif command == "delete":
        if len(rest) != 1:
            print("Usage: python3 lib/keychain.py delete <name>")
            sys.exit(1)
        if delete_credential(rest[0]):
            print(f"Deleted: {rest[0]}")
        else:
            print(f"Not found: {rest[0]}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print("Commands: set, get, list, delete")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
