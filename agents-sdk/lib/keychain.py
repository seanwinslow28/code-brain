"""macOS Keychain credential helper for the agent fleet.

Service prefix: com.sean.agents
All credentials are stored/retrieved via the `security` CLI tool.
No .env files — this is the only sanctioned credential path.

Usage as a module:
    from lib.keychain import get_credential, set_credential
    api_key = get_credential("anthropic_api_key")

Usage as a CLI:
    python3 lib/keychain.py set anthropic_api_key sk-ant-...
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


def _cli() -> None:
    """CLI entry point for manual credential management."""
    if len(sys.argv) < 2:
        print("Usage: python3 lib/keychain.py <set|get|list|delete> [name] [value]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "set":
        if len(sys.argv) != 4:
            print("Usage: python3 lib/keychain.py set <name> <value>")
            sys.exit(1)
        set_credential(sys.argv[2], sys.argv[3])
        print(f"Stored: {sys.argv[2]}")

    elif command == "get":
        if len(sys.argv) != 3:
            print("Usage: python3 lib/keychain.py get <name>")
            sys.exit(1)
        value = get_credential(sys.argv[2])
        if value is None:
            print(f"Not found: {sys.argv[2]}")
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
        if len(sys.argv) != 3:
            print("Usage: python3 lib/keychain.py delete <name>")
            sys.exit(1)
        if delete_credential(sys.argv[2]):
            print(f"Deleted: {sys.argv[2]}")
        else:
            print(f"Not found: {sys.argv[2]}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print("Commands: set, get, list, delete")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
