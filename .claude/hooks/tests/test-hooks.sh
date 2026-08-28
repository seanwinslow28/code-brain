#!/bin/bash
# Regression suite for the PreToolUse security hooks.
#
# Exists because both hooks silently no-opped for ~6 months (16,888 recorded
# no-op runs) and nothing surfaced it. These tests assert the hooks actually
# FIRE, not merely that they exit cleanly -- a hook that always exits 0 passes
# a "does it run" check and fails every test here.
#
# Payload shapes below are copied from real Claude Code payloads captured
# 2026-08-28. If Claude Code changes the contract, these fail loudly.
#
# Usage: bash .claude/hooks/tests/test-hooks.sh
set -uo pipefail
cd "$(dirname "$0")/../../.." || exit 1

HIGHRISK=".claude/hooks/require-confirm-highrisk.sh"
SECRETS=".claude/hooks/block-secrets.py"
PASS=0; FAIL=0

payload() { # $1=tool_name $2=key $3=value
  python3 -c '
import json,sys
key,val = sys.argv[2], sys.argv[3]
print(json.dumps({"hook_event_name":"PreToolUse","tool_name":sys.argv[1],
                  "tool_input":{key:val},"session_id":"test","cwd":"/tmp"}))' "$1" "$2" "$3"
}

check() { # $1=label $2=expected(deny|ask|allow) $3=actual_exit $4=stdout
  local got
  if [ "$3" -eq 2 ]; then got=deny
  elif printf '%s' "$4" | grep -q '"permissionDecision"[[:space:]]*:[[:space:]]*"ask"'; then got=ask
  elif [ "$3" -eq 0 ]; then got=allow
  else got="exit$3"; fi
  if [ "$got" = "$2" ]; then PASS=$((PASS+1)); printf '  ok    %-9s %s\n' "[$got]" "$1"
  else FAIL=$((FAIL+1)); printf '  FAIL  expected=%-5s got=%-5s %s\n' "$2" "$got" "$1"; fi
}

run_highrisk() { # $1=expected $2=command
  local out rc
  out=$(payload Bash command "$2" | bash "$HIGHRISK" 2>/dev/null); rc=$?
  check "$2" "$1" "$rc" "$out"
}

run_secrets() { # $1=expected $2=path $3=tool
  local out rc
  out=$(payload "${3:-Write}" file_path "$2" | python3 "$SECRETS" 2>/dev/null); rc=$?
  check "${3:-Write} $2" "$1" "$rc" "$out"
}

echo "== require-confirm-highrisk.sh: catastrophic => deny =="
run_highrisk deny 'rm -rf /'
run_highrisk deny 'rm -rf ~'
run_highrisk deny 'sudo rm -rf /var/log'
run_highrisk deny 'mkfs.ext4 /dev/sda1'
run_highrisk deny 'dd if=/dev/zero of=/dev/disk2 bs=1m'
run_highrisk deny 'diskutil eraseDisk JHFS+ Blank /dev/disk2'
run_highrisk deny 'fdisk /dev/sda'

echo "== require-confirm-highrisk.sh: destructive => ask =="
run_highrisk ask 'rm -rf build/'
run_highrisk ask 'rm -f stale.txt'
run_highrisk ask 'chmod 777 deploy.sh'
run_highrisk ask 'sudo chown seanwinslow /usr/local/lib'
run_highrisk ask 'git checkout .'

echo "== require-confirm-highrisk.sh: ordinary work => allow (no false positives) =="
run_highrisk allow 'git log --format=%h -5'
run_highrisk allow 'ls -la 2>/dev/null'
run_highrisk allow 'echo hello > /dev/null'
run_highrisk allow 'npm run format'
run_highrisk allow 'chmod +x /Users/seanwinslow/bin/tool'
run_highrisk allow 'git status --porcelain'
run_highrisk allow 'python3 scripts/validate.py'

echo "== require-confirm-highrisk.sh: contract guards =="
out=$(payload Write file_path /tmp/x.txt | bash "$HIGHRISK" 2>/dev/null); check "non-Bash tool ignored" allow $? "$out"
out=$(printf 'not json' | bash "$HIGHRISK" 2>/dev/null); check "malformed payload fails CLOSED" deny $? "$out"
# The original bug, pinned: a payload carrying only the phantom "tool" key
# carries no `tool_name`, so the hook cannot vouch for it and must fail CLOSED.
# If someone reverts to reading "tool", this command would be allowed through
# and this test goes red.
out=$(printf '{"tool":"bash","command":"rm -rf /"}' | bash "$HIGHRISK" 2>/dev/null); check "legacy phantom-field payload fails CLOSED" deny $? "$out"

echo "== block-secrets.py: sensitive writes => deny =="
run_secrets deny '.env'
run_secrets deny 'app/.env.local'
run_secrets deny 'infra/secrets/tokens.json'
run_secrets deny 'src/api_key.ts'
run_secrets deny '/Users/seanwinslow/.ssh/id_rsa'
run_secrets deny 'config/secrets.yml'
run_secrets deny 'deploy/prod_password.txt'
run_secrets deny 'app/.env' Edit

run_secrets deny 'x/client_secret.json'

echo "== block-secrets.py: exemptions and calibration (0 false positives over 6,883 tracked files) =="
run_secrets allow 'agents-sdk/.env.example'
run_secrets allow 'tools/llm-council/.env.example'
run_secrets allow 'config/database.yml.template'
# These three are why "**/*key*", "**/*secret*" and "**/*credential*" are NOT
# used as patterns -- shared/ and plugin/ shipped the broader forms.
run_secrets allow 'agents-sdk/lib/keychain.py'
run_secrets allow '.claude/hooks/block-secrets.py'
run_secrets allow 'vault/knowledge/connections/credential-rotency-vs-infrastructure-stability.md'

echo "== block-secrets.py: ordinary writes => allow =="
run_secrets allow 'README.md'
run_secrets allow 'src/app.ts'
run_secrets allow 'docs/environment.md'
run_secrets allow 'vault/00_inbox/tickets.md'
run_secrets allow '.env' Bash

echo
echo "passed=$PASS failed=$FAIL"
[ "$FAIL" -eq 0 ]
