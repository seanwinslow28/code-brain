#!/bin/bash
# PreToolUse hook (Bash): Blocks network access to non-whitelisted domains.
# Prevents unauthorized curl/wget/nc calls to external services.
# Exit code 2 = deny, 0 = allow.

# Read hook context from stdin (JSON)
HOOK_DATA=$(cat)

# Extract tool name and command.
# Contract (measured 2026-08-28): the tool name is `tool_name`, NOT `tool`,
# and the command lives at `tool_input.command`, NOT top level. Parsed with
# python3 so escaped quotes cannot truncate the value.
PARSED=$(printf '%s' "$HOOK_DATA" | python3 -c '
import json, sys
try:
    d = json.loads(sys.stdin.read())
except Exception:
    print(""); print(""); sys.exit(0)
print(d.get("tool_name", ""))
print((d.get("tool_input") or {}).get("command", "").replace("\n", " "))
' 2>/dev/null)
TOOL_NAME=$(printf '%s\n' "$PARSED" | sed -n '1p')
COMMAND=$(printf '%s\n' "$PARSED" | sed -n '2p')

# Only check shell commands
if [ "$TOOL_NAME" != "Bash" ]; then
    exit 0
fi

# Network tools to monitor
NETWORK_TOOLS="curl|wget|nc|ncat|netcat|httpie|http"

# Check if command uses a network tool
if ! echo "$COMMAND" | grep -qEi "\\b($NETWORK_TOOLS)\\b"; then
    exit 0
fi

# Whitelisted domains (add your trusted domains here)
WHITELIST=(
    "127.0.0.1"
    "localhost"
    "api.github.com"
    "github.com"
    "raw.githubusercontent.com"
    "registry.npmjs.org"
    "pypi.org"
    "api.anthropic.com"
    "api.openai.com"
    "api.elevenlabs.io"
    "huggingface.co"
    "api-inference.huggingface.co"
    "supabase.co"
    "zapier.com"
    "hooks.zapier.com"
)

# Extract URLs/domains from the command
DOMAINS=$(echo "$COMMAND" | grep -oEi 'https?://[^/"[:space:]]+' | sed 's|https\?://||' | cut -d: -f1)

# If no URLs found, allow (might be piping to curl, etc.)
if [ -z "$DOMAINS" ]; then
    exit 0
fi

# Check each domain against whitelist
for domain in $DOMAINS; do
    ALLOWED=false
    for allowed_domain in "${WHITELIST[@]}"; do
        # Check exact match or subdomain match
        if [ "$domain" = "$allowed_domain" ] || echo "$domain" | grep -q "\\.$allowed_domain$"; then
            ALLOWED=true
            break
        fi
    done

    if [ "$ALLOWED" = false ]; then
        echo "BLOCKED: Network access to non-whitelisted domain: $domain" >&2
        echo "Command: $COMMAND" >&2
        echo "Add '$domain' to WHITELIST in network-access-control.sh to allow." >&2
        exit 2  # Exit code 2 = deny
    fi
done

# All domains whitelisted — allow
exit 0