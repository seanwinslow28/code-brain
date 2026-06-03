"""Async subprocess wrappers for Codex CLI and Anti-Gravity CLI.

Smoke-tested 2026-05-21 — see agents-sdk/docs/multi-cli-integration-patterns.md
§Smoke Test Evidence for the ground-truth behavior. These wrappers are the
single point in the codebase that knows the CLIs' trust flags, sandbox modes,
and output shapes. Both vault_critic and (future) tools/llm-council adapters
import from here.

Trust flags / sandbox modes are set explicitly per invocation; silent reliance
on inherited env is a latent bug we are deliberately avoiding.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import time
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

_CODEX_TOKENS_RE = re.compile(r"tokens used\s*\n\s*([\d,]+)")


async def _pump_stream(stream, buf: bytearray) -> None:
    """Continuously read a subprocess pipe into `buf` until EOF.

    Run as a background task so partial output is always accumulated in `buf`,
    even when the parent abandons the wait on timeout. This is what makes the
    timeout path able to report what the child streamed before it hung —
    `asyncio.wait_for(proc.communicate())` discards that on cancellation.
    """
    if stream is None:
        return
    while True:
        try:
            chunk = await stream.read(65536)
        except Exception:
            break
        if not chunk:
            break
        buf.extend(chunk)


def _write_ag_timeout_capture(
    debug_log_dir: Path,
    *,
    timeout_s: float,
    duration_s: float,
    cmd: list[str],
    stdout_text: str,
    stderr_text: str,
    probe_text: str = "",
) -> Path | None:
    """Persist gemini's partial output at the moment of a timeout kill.

    Writes a timestamped log under `debug_log_dir` so a failing nightly/kickstart
    run leaves behind exactly what the CLI last printed before it hung — the
    decisive clue for the zero-token 120s hang. Best-effort; never raises.

    `probe_text`: optional IP-family-split reachability probe captured at the
    failure moment (see `_probe_google_reachability`), appended as its own
    section so the sub-cause (IPv6-only vs all-Google vs DNS) is discriminable.
    """
    try:
        debug_log_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
        out_path = debug_log_dir / f"ag-timeout-{stamp}.log"
        # Redact the prompt arg (large, may contain vault content); keep flags.
        redacted_cmd = [
            "<prompt>" if i > 0 and cmd[i - 1] == "-p" else part
            for i, part in enumerate(cmd)
        ]
        probe_section = (
            f"\n===== CONNECTIVITY PROBE (post-timeout) =====\n{probe_text}\n"
            if probe_text else ""
        )
        body = (
            f"# Anti-Gravity (gemini) timeout capture\n"
            f"captured_utc: {datetime.now(timezone.utc).isoformat()}\n"
            f"timeout_s: {timeout_s}\n"
            f"actual_duration_s: {duration_s:.2f}\n"
            f"cmd: {redacted_cmd}\n"
            f"stdout_len: {len(stdout_text)}\n"
            f"stderr_len: {len(stderr_text)}\n"
            f"{probe_section}"
            f"\n===== STDOUT =====\n{stdout_text}\n"
            f"\n===== STDERR =====\n{stderr_text}\n"
        )
        out_path.write_text(body, encoding="utf-8")
        return out_path
    except Exception:
        return None


# Hosts the gemini CLI must reach. cloudcode-pa is the Code Assist
# (oauth-personal) model endpoint; play.googleapis is Clearcut telemetry — the
# host that logs UND_ERR_CONNECT_TIMEOUT in the 2026-06-03 nightly captures.
_GOOGLE_PROBE_HOSTS = ("cloudcode-pa.googleapis.com", "play.googleapis.com")
# Non-Google control: Codex/OpenAI survive the same 03:30 window, so if this
# connects while Google times out, the fault is Google-reachability-specific.
_PROBE_CONTROL_HOST = "api.openai.com"
# Run the probe at most once per process — bounds added wall-time on a 5-timeout
# night to a single ~10s burst instead of 5×.
_ag_probe_emitted = False


async def _run_probe_cmd(label: str, args: list[str], timeout: float = 12.0) -> str:
    """Run one diagnostic command, return a 'label: output' line. Never raises."""
    try:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        try:
            out, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            return f"{label}: PROBE-TIMEOUT after {timeout}s"
        text = (out or b"").decode("utf-8", errors="replace").strip()
        return f"{label}: {text or '(no output)'}"
    except FileNotFoundError as exc:
        return f"{label}: probe-tool-missing ({exc})"
    except Exception as exc:  # noqa: BLE001 - diagnostics must never crash the agent
        return f"{label}: probe-error ({exc})"


async def _probe_google_reachability() -> str:
    """Probe IP-family-split reachability to Google API hosts at the failure moment.

    Fired only on an Anti-Gravity timeout (and only under VAULT_CRITIC_AG_DEBUG,
    once per process). Discriminates the nightly zero-token hang between
    (a) IPv6-to-Google broken, (b) all-Google unreachable, and (c) DNS — by
    comparing per-family TCP connect against a non-Google control. Best-effort;
    returns a formatted text block, never raises.
    """
    def _curl(host: str, family: str) -> list[str]:
        return [
            "curl", family, "-sS", "-o", "/dev/null", "--connect-timeout", "8",
            "-w", "http=%{http_code} connect=%{time_connect}s tcp=%{remote_ip}",
            f"https://{host}/",
        ]

    tasks = []
    for host in _GOOGLE_PROBE_HOSTS:
        tasks.append(_run_probe_cmd(f"curl4 {host}", _curl(host, "-4")))
        tasks.append(_run_probe_cmd(f"curl6 {host}", _curl(host, "-6")))
        tasks.append(_run_probe_cmd(f"digA   {host}", ["dig", "+short", "+time=5", "A", host]))
        tasks.append(_run_probe_cmd(f"digAAAA {host}", ["dig", "+short", "+time=5", "AAAA", host]))
    tasks.append(_run_probe_cmd(
        f"curl4 {_PROBE_CONTROL_HOST} (control)", _curl(_PROBE_CONTROL_HOST, "-4")))
    lines = await asyncio.gather(*tasks)
    return "\n".join(lines)


def parse_codex_tokens(stderr_text: str) -> int | None:
    """Return the token count from Codex's `tokens used` footer, or None.

    Codex prints `tokens used\\n<count>` at the end of stderr. The count may
    or may not contain comma thousands separators depending on terminal width.
    """
    m = _CODEX_TOKENS_RE.search(stderr_text or "")
    if not m:
        return None
    return int(m.group(1).replace(",", ""))


@dataclass(frozen=True)
class CLIResponse:
    """Result of a single CLI invocation.

    `text` is the raw markdown response (Codex stdout or Anti-Gravity
    `response` field). `tokens` is None when the CLI did not report a
    token count. `rate_capped` is set by the wrapper when the CLI's
    stderr matches a known rate-cap signature; the caller MUST treat
    rate-capped responses as failures even if exit_code == 0.
    """

    cli: Literal["codex", "antigravity"]
    text: str
    tokens: int | None
    duration_s: float
    exit_code: int
    rate_capped: bool
    error: str | None

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.rate_capped and self.error is None


_RATE_CAP_PATTERNS = (
    "rate limit",
    "429",
    "quota",
    "resource_exhausted",
    "too many requests",
)


def detect_rate_cap(cli: str, stderr_text: str) -> bool:
    """Heuristic rate-cap detector. True when stderr looks rate-capped.

    Both Codex and Anti-Gravity surface rate-cap errors as free-text or JSON
    in stderr (no consistent structured signal). We match a small set of
    case-insensitive substrings that cover the documented + anecdotal shapes.
    False positives on non-cap errors are tolerable — the run is marked
    partial either way and the wrapper logs full stderr.
    """
    lowered = (stderr_text or "").lower()
    return any(p in lowered for p in _RATE_CAP_PATTERNS)


CODEX_BINARY = "/opt/homebrew/bin/codex"
CODEX_DEFAULT_TIMEOUT_S = 120


async def run_codex(prompt: str, timeout_s: float = CODEX_DEFAULT_TIMEOUT_S) -> CLIResponse:
    """Invoke `codex exec` with read-only sandbox and skip-git-repo-check.

    Runs from `Path.home()` (trusted per ~/.codex/config.toml `[projects]`).
    Captures stdout (markdown response) and stderr (session metadata +
    `tokens used` footer). Returns a CLIResponse — never raises on CLI failure;
    timeouts and rate-caps surface via response fields.
    """
    cmd = [
        CODEX_BINARY,
        "exec",
        "--sandbox", "read-only",
        "--skip-git-repo-check",
        prompt,
    ]
    t0 = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
        )
    except FileNotFoundError as exc:
        return CLIResponse(
            cli="codex", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"codex binary missing: {exc}",
        )

    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except ProcessLookupError:
            pass
        return CLIResponse(
            cli="codex", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"codex timeout after {timeout_s}s",
        )

    stdout_text = stdout.decode("utf-8", errors="replace")
    stderr_text = stderr.decode("utf-8", errors="replace")
    return CLIResponse(
        cli="codex",
        text=stdout_text,
        tokens=parse_codex_tokens(stderr_text),
        duration_s=time.monotonic() - t0,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        rate_capped=detect_rate_cap("codex", stderr_text),
        error=None if proc.returncode == 0 else stderr_text[:500],
    )


ANTIGRAVITY_BINARY = "/opt/homebrew/bin/gemini"
ANTIGRAVITY_DEFAULT_TIMEOUT_S = 120


def _antigravity_tokens(payload: dict) -> int | None:
    """Pluck the total token count from Anti-Gravity stats, model-name-agnostic.

    `stats.models` is a {<model_name>: {tokens: {total: int, ...}}} map.
    The model name is whichever the auto-router resolved to and may change
    over time, so we read whichever single key is present.
    """
    models = (payload.get("stats") or {}).get("models") or {}
    if not models:
        return None
    # If multiple models surface (multi-model routing in a future CLI version),
    # sum them — total across the call is the right number for our manifest.
    total = 0
    found = False
    for entry in models.values():
        tk = (entry or {}).get("tokens") or {}
        if "total" in tk:
            total += int(tk["total"])
            found = True
    return total if found else None


async def run_antigravity(
    prompt: str,
    timeout_s: float = ANTIGRAVITY_DEFAULT_TIMEOUT_S,
    debug_log_dir: Path | None = None,
) -> CLIResponse:
    """Invoke `gemini -p` with JSON output and plan approval mode.

    Trust set via GEMINI_CLI_TRUST_WORKSPACE=true added to the inherited
    process env (the var is set explicitly per invocation; the surrounding
    env is preserved). Sandbox via --approval-mode plan (read-only per
    smoke test). Returns a CLIResponse; never raises on CLI failure.

    `debug_log_dir`: when set, a timeout drains and persists gemini's partial
    stdout/stderr to a timestamped file there (diagnostic for the nightly
    zero-token hang — see POSTMORTEM-2026-06-01-vault-critic-antigravity.md).

    `VAULT_CRITIC_AG_DEBUG=1` in the env appends gemini's own `--debug` flag,
    which streams startup/auth/request progress to stderr. Reversible probe for
    the kickstart run — leave unset for normal nightly behavior.
    """
    cmd = [
        ANTIGRAVITY_BINARY,
        "-p", prompt,
        "--output-format", "json",
        "--approval-mode", "plan",
        # Disable all configured MCP servers for this invocation. The critic
        # only needs the model to emit a text critique — it never calls a tool.
        # Loading the 6 MCP servers from ~/.gemini/settings.json (chrome-devtools
        # → Chrome on :9222, npx/uvx subprocesses, remote zapier) makes startup
        # heavy and fragile: it works interactively (~12-18s) but hangs past the
        # per-CLI timeout on the unattended 3:30am nightly run (Chrome closed,
        # post-wake window), producing 0 sessions / 0 tokens / 5-of-5 failures
        # while the lightweight Codex CLI in the same process succeeds. Passing
        # a single non-existent server name allows zero servers. (2026-06-01)
        "--allowed-mcp-server-names", "__none__",
    ]
    if os.environ.get("VAULT_CRITIC_AG_DEBUG") == "1":
        cmd.append("--debug")
    env = {**os.environ, "GEMINI_CLI_TRUST_WORKSPACE": "true"}
    t0 = time.monotonic()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(Path.home()),
            env=env,
        )
    except FileNotFoundError as exc:
        return CLIResponse(
            cli="antigravity", text="", tokens=None,
            duration_s=time.monotonic() - t0,
            exit_code=-1, rate_capped=False,
            error=f"gemini binary missing: {exc}",
        )

    # Pump both pipes into buffers via background tasks so partial output is
    # always captured — including when we abandon the wait on timeout.
    out_buf = bytearray()
    err_buf = bytearray()
    out_task = asyncio.create_task(_pump_stream(proc.stdout, out_buf))
    err_task = asyncio.create_task(_pump_stream(proc.stderr, err_buf))

    timed_out = False
    try:
        await asyncio.wait_for(proc.wait(), timeout=timeout_s)
    except asyncio.TimeoutError:
        timed_out = True
        try:
            proc.kill()
        except ProcessLookupError:
            pass

    # Let the pumps grab any final buffered bytes. The bulk is already captured
    # mid-stream; gemini's node children can hold the pipe open past SIGKILL, so
    # cap this short rather than waiting on a slow EOF.
    try:
        await asyncio.wait_for(
            asyncio.gather(out_task, err_task, return_exceptions=True),
            timeout=2,
        )
    except asyncio.TimeoutError:
        out_task.cancel()
        err_task.cancel()

    stdout_text = bytes(out_buf).decode("utf-8", errors="replace")
    stderr_text = bytes(err_buf).decode("utf-8", errors="replace")
    duration = time.monotonic() - t0

    if timed_out:
        capture_path = None
        if debug_log_dir is not None:
            # Diagnostic only: under the same reversible AG_DEBUG switch, run the
            # reachability probe once to capture the network state at the failure
            # moment. Refutes/confirms the Google-host-unreachable root cause that
            # the 2026-06-03 captures point to (play.googleapis.com connect-timeout
            # while Codex/OpenAI succeed in the same process).
            global _ag_probe_emitted
            probe_text = ""
            if os.environ.get("VAULT_CRITIC_AG_DEBUG") == "1" and not _ag_probe_emitted:
                _ag_probe_emitted = True
                probe_text = await _probe_google_reachability()
            capture_path = _write_ag_timeout_capture(
                debug_log_dir,
                timeout_s=timeout_s,
                duration_s=duration,
                cmd=cmd,
                stdout_text=stdout_text,
                stderr_text=stderr_text,
                probe_text=probe_text,
            )
        suffix = f" (capture: {capture_path})" if capture_path else ""
        return CLIResponse(
            cli="antigravity", text="", tokens=None,
            duration_s=duration,
            exit_code=-1, rate_capped=False,
            error=f"antigravity timeout after {timeout_s}s{suffix}",
        )

    rate_capped = detect_rate_cap("antigravity", stderr_text)

    try:
        payload = json.loads(stdout_text)
    except json.JSONDecodeError as exc:
        return CLIResponse(
            cli="antigravity", text=stdout_text, tokens=None,
            duration_s=duration,
            exit_code=proc.returncode if proc.returncode is not None else -1,
            rate_capped=rate_capped,
            error=f"antigravity json parse failed: {exc}",
        )

    return CLIResponse(
        cli="antigravity",
        text=str(payload.get("response", "")),
        tokens=_antigravity_tokens(payload),
        duration_s=duration,
        exit_code=proc.returncode if proc.returncode is not None else -1,
        rate_capped=rate_capped,
        error=None if proc.returncode == 0 else stderr_text[:500],
    )
