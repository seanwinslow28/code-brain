"""judge.evaluate() — the heartbeat of the control plane.

Given an ActionProposal (what an actor wants to do) and a Policy (the rules
it's gated by), call a local-model judge and return a JudgeDecision.

Why local model: gemma4:e4b on Mac Mini Ollama ($0/decision) keeps the
control plane free to operate. Cost-economics fluency isn't a separate
calculator — it's an architecture choice you can see in the bill of materials.

Why fail-open via JUDGE_UNAVAILABLE: when the judge model is down or slow,
the wrapped agent's caller falls open to Sean's manual review (Tier-A
canonical control). Cadence preservation > theoretical bypass risk. The
ledger row captures the unavailability so the dashboard plots it directly.

Why JSON output with retry: gemma4:e4b is a 4B-parameter model. It will
occasionally emit malformed JSON. Three retries (with the parse error in
the retry prompt) covers 95%+ of real cases; the 5% that fail land as
JUDGE_UNAVAILABLE rows so we can see the model-availability tail in the
dashboard instead of hiding it as an exception.

Routing: this module routes via the HybridRouter "judge_layer" task profile,
which is added to config.toml's [routing.task_map] in the same PR. The
profile points at gemma4:e4b on mac_mini. fallback_to_api stays True at the
[routing] level — if Mac Mini is down, the router falls back to Claude API
for a paid eval. That's an explicit design choice: a real judge run on the
expensive path is better than no judge.

Testing seam: _call_router(task, system, user, timeout_s) is the single
HTTP boundary. Unit tests monkeypatch this function instead of mocking
httpx + asyncio + tomllib. evaluate() itself is otherwise pure.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path

from lib.judge.schema import ActionProposal, JudgeDecision, Outcome
from lib.judge.policy import Policy, Rule

logger = logging.getLogger(__name__)

# Task name registered in config.toml [routing.task_map] for this module.
# Changing this string requires a matching config.toml edit in the same PR.
JUDGE_TASK_KEY = "judge_layer"

# Default model name to report on JUDGE_UNAVAILABLE rows when we never
# successfully routed (e.g., config load failed before the router could tell
# us which model would have been used). Lets the dashboard still attribute
# the unavailable rows to a plausible attempted model.
_DEFAULT_ATTEMPTED_MODEL = "gemma4:e4b"

# How long the local model has to respond. Substack-Drafter's _route uses
# 300s for drafts; judge decisions should be sub-30s on gemma4:e4b. If a
# call exceeds the timeout, we land in JUDGE_UNAVAILABLE rather than blocking
# the wrapped agent for minutes.
_JUDGE_TIMEOUT_S = 30.0

# Max retries on JSON-parse failure. The retry prompt includes the parse
# error from the prior attempt so the model can self-correct. Higher than 3
# spends too much wall-clock on a 4B-parameter model that's clearly not
# emitting JSON today; lower than 3 misses the easy "drop the prose preamble"
# self-correction case.
_MAX_PARSE_RETRIES = 3


# ─── HTTP transport — the single seam for tests ──────────────────────────────


def _call_router(
    *,
    task: str,
    system: str,
    user: str,
    timeout_s: float,
) -> tuple[str, str]:
    """Route through HybridRouter, POST the prompt, return (text, model_used).

    This is the only HTTP boundary in the judge module. Unit tests monkeypatch
    this function directly (matches the substack-drafter test pattern). Real
    runs hit Mac Mini Ollama via the judge_layer task profile.

    Raises:
        JudgeTransportError: any router resolution, HTTP, or timeout failure.
            evaluate() catches this and returns Outcome.JUDGE_UNAVAILABLE.
    """
    import asyncio
    import tomllib

    import httpx

    from lib.hybrid_router import HybridRouter, WOLUnavailable

    config_path = Path(__file__).parent.parent.parent / "config.toml"
    try:
        with open(config_path, "rb") as fh:
            config = tomllib.load(fh)
    except (FileNotFoundError, OSError, tomllib.TOMLDecodeError) as exc:
        raise JudgeTransportError(
            f"Could not load agents-sdk/config.toml: {exc}"
        ) from exc

    router = HybridRouter.from_config(config)

    try:
        decision = asyncio.run(router.route(task))
    except WOLUnavailable as exc:
        raise JudgeTransportError(
            f"HybridRouter could not reach a machine for task {task!r}: {exc}"
        ) from exc
    except Exception as exc:
        # Catch-all for router failures so the caller doesn't have to know
        # the router's internal exception taxonomy.
        raise JudgeTransportError(
            f"Router resolution failed for task {task!r}: {exc}"
        ) from exc

    # gemma4:e4b runs on Ollama. The OpenAI-compat fallback path is here for
    # forward-compat when the [routing] fallback_to_api kicks in and routes
    # to Claude API for a paid eval — same shape, different runtime.
    if decision.runtime == "ollama":
        full_prompt = f"<system>\n{system}\n</system>\n\n{user}"
        payload = {
            "model": decision.model,
            "prompt": full_prompt,
            "stream": False,
            # Lower temperature for judging — we want consistent rule
            # application, not creative rewrites of the rules.
            "options": {"temperature": 0.0},
        }
        endpoint = f"{decision.base_url}/api/generate"
        try:
            resp = httpx.post(endpoint, json=payload, timeout=timeout_s)
            resp.raise_for_status()
            text = resp.json().get("response", "")
        except (httpx.HTTPError, httpx.ReadTimeout, httpx.ConnectError) as exc:
            raise JudgeTransportError(
                f"Ollama call to {endpoint} (model={decision.model}) failed: {exc}"
            ) from exc
        return text, decision.model

    # OpenAI-compatible path (mlx-lm, lm-studio, or Claude API fallback)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    payload = {"model": decision.model, "messages": messages, "stream": False}
    endpoint = f"{decision.base_url}/v1/chat/completions"
    try:
        resp = httpx.post(endpoint, json=payload, timeout=timeout_s)
        resp.raise_for_status()
        body = resp.json()
        text = body["choices"][0]["message"]["content"]
    except (httpx.HTTPError, httpx.ReadTimeout, httpx.ConnectError, KeyError, IndexError) as exc:
        raise JudgeTransportError(
            f"OpenAI-compat call to {endpoint} (model={decision.model}) failed: {exc}"
        ) from exc
    return text, decision.model


class JudgeTransportError(Exception):
    """Raised by _call_router on any router / HTTP / parse-shape failure.

    Caught by evaluate(); the caller never sees this exception — it sees a
    JudgeDecision with outcome=JUDGE_UNAVAILABLE instead.
    """


# ─── Prompt building ─────────────────────────────────────────────────────────


def _build_system_prompt(policy: Policy) -> str:
    """Build the system prompt enumerating the policy rules + the output
    contract the judge must follow.

    Why explicit JSON instructions: gemma4:e4b's prose-vs-JSON discrimination
    is reliable when the format is unambiguous. The retry prompt (Day 3
    parse-failure path) appends the parse error verbatim so the model can
    self-correct.

    The system prompt ends with a *demonstration* JSON block, not a Markdown
    code fence — small local models sometimes wrap the WHOLE response in a
    fence that confuses lighter-weight parsers. We use bare braces.
    """
    rules_block = "\n\n".join(
        _format_rule_for_prompt(i, rule) for i, rule in enumerate(policy.rules)
    )

    fallback_str = (
        policy.fallback_outcome.value
        if hasattr(policy.fallback_outcome, "value")
        else str(policy.fallback_outcome)
    )

    return (
        f"You are the judge layer of an agent control plane. You evaluate a "
        f"proposed action from a production agent against a policy and emit "
        f"a single JSON object naming the outcome.\n\n"
        f"Active policy: {policy.name} (version {policy.version}) gating "
        f"the {policy.agent} actor.\n\n"
        f"Rules (evaluated in order; FIRST MATCH WINS):\n\n{rules_block}\n\n"
        f"If no rule fires, return outcome={fallback_str!r} (the policy's "
        f"fallback_outcome).\n\n"
        f"OUTPUT CONTRACT — emit EXACTLY one JSON object with the shape:\n"
        f'{{"outcome": "<ALLOW|BLOCK|REVISE|ESCALATE>", '
        f'"matched_rule_id": "<rule_id or null>", '
        f'"feedback": "<text or null>", '
        f'"quarantine_reason": "<text or null>"}}\n\n'
        f"- outcome MUST be one of ALLOW / BLOCK / REVISE / ESCALATE.\n"
        f"- feedback REQUIRED on REVISE; null otherwise. Use the matched "
        f"rule's feedback_template, customized with details from the "
        f"proposal.\n"
        f"- quarantine_reason REQUIRED on ESCALATE; null otherwise. Use the "
        f"matched rule's quarantine_reason, customized with details from "
        f"the proposal.\n"
        f"- matched_rule_id is the rule id (string) that fired, or null on "
        f"fallback.\n\n"
        f"Emit ONLY the JSON object. No prose, no Markdown fence, no commentary."
    )


def _format_rule_for_prompt(index: int, rule: Rule) -> str:
    """Format one Rule for inclusion in the system prompt."""
    outcome_str = rule.outcome.value if hasattr(rule.outcome, "value") else str(rule.outcome)
    parts = [
        f"Rule {index + 1} (id={rule.id!r}):",
        f"  Condition: {rule.condition.strip()}",
        f"  If fires → outcome={outcome_str}",
    ]
    if rule.feedback_template:
        parts.append(f"  feedback_template: {rule.feedback_template.strip()}")
    if rule.quarantine_reason:
        parts.append(f"  quarantine_reason: {rule.quarantine_reason.strip()}")
    return "\n".join(parts)


def _build_user_prompt(proposal: ActionProposal, retry_context: str = "") -> str:
    """Build the user prompt — the ActionProposal serialized as labeled YAML.

    Why YAML-shaped (not raw JSON dump): the local model reads YAML-style
    key:value blocks more cleanly than nested-JSON. Plus, this makes the
    prompt human-readable in retry-debug traces in the JSONL ledger.

    retry_context: when set (parse-retry path), prepended verbatim with the
    parse error from the prior attempt so the model can self-correct.
    """
    fields = [
        ("intended_action", proposal.intended_action),
        ("target_surface", proposal.target_surface),
        ("evidence_used", proposal.evidence_used),
        ("authorization_basis", proposal.authorization_basis),
        ("expected_consequence", proposal.expected_consequence),
        ("rollback_path", proposal.rollback_path),
        ("exposure_level", proposal.exposure_level),
        ("human_review_required", proposal.human_review_required),
    ]
    rendered = "\n".join(f"{k}: {_yaml_value(v)}" for k, v in fields)

    user = (
        f"ActionProposal to evaluate:\n\n{rendered}\n\n"
        f"Return your verdict as the JSON object specified in the system prompt."
    )
    if retry_context:
        user = f"{retry_context}\n\n{user}"
    return user


def _yaml_value(value: object) -> str:
    """Render a single field value in YAML-readable form."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        if not value:
            return "[]"
        return "\n  - " + "\n  - ".join(str(v) for v in value)
    return str(value)


# ─── Output parsing ──────────────────────────────────────────────────────────


# Matches the first balanced JSON object in a blob of text. Local models often
# wrap output in prose preambles ("Sure, here's the JSON: {...}") — we want
# the first {...} block. Greedy on the content, lazy on the outer braces.
_JSON_OBJECT_RE = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", re.DOTALL)


class JudgeParseError(Exception):
    """Raised when the model's output can't be parsed into the JSON contract.

    Carries the failing text + a human-readable reason. The retry prompt
    appends this reason verbatim so the model can self-correct.
    """

    def __init__(self, *, raw_text: str, reason: str) -> None:
        super().__init__(f"{reason}\n\nRaw output: {raw_text[:300]}")
        self.raw_text = raw_text
        self.reason = reason


def _parse_judge_output(raw_text: str) -> dict:
    """Extract the JSON object from raw_text + sanity-check the outcome key.

    Raises:
        JudgeParseError: if no JSON object found OR outcome key is missing OR
            outcome value is not one of the 4 model-emittable outcomes (the
            5th — JUDGE_UNAVAILABLE — is set by evaluate(), not by the model).
    """
    # First pass: try parsing the entire text as JSON (clean output case).
    text = raw_text.strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return _validate_parsed_outcome(parsed, raw_text)
    except json.JSONDecodeError:
        pass

    # Second pass: extract the first JSON object from the text and parse it.
    match = _JSON_OBJECT_RE.search(text)
    if not match:
        raise JudgeParseError(
            raw_text=raw_text,
            reason="No JSON object found in output.",
        )
    try:
        parsed = json.loads(match.group(0))
    except json.JSONDecodeError as exc:
        raise JudgeParseError(
            raw_text=raw_text,
            reason=f"Found a {{...}} block but it didn't parse as JSON: {exc}",
        ) from exc

    if not isinstance(parsed, dict):
        raise JudgeParseError(
            raw_text=raw_text,
            reason=f"Parsed JSON is not an object (got {type(parsed).__name__}).",
        )

    return _validate_parsed_outcome(parsed, raw_text)


# The 4 outcomes the model is allowed to emit. JUDGE_UNAVAILABLE is set by
# evaluate() on transport / parse failure; the model itself cannot return it.
_MODEL_EMITTABLE_OUTCOMES: set[str] = {
    Outcome.ALLOW.value,
    Outcome.BLOCK.value,
    Outcome.REVISE.value,
    Outcome.ESCALATE.value,
}


def _validate_parsed_outcome(parsed: dict, raw_text: str) -> dict:
    """Cross-check the parsed dict against the output contract."""
    if "outcome" not in parsed:
        raise JudgeParseError(
            raw_text=raw_text,
            reason="Parsed JSON is missing required 'outcome' key.",
        )
    outcome_str = parsed["outcome"]
    if outcome_str not in _MODEL_EMITTABLE_OUTCOMES:
        raise JudgeParseError(
            raw_text=raw_text,
            reason=(
                f"outcome={outcome_str!r} is not in the emittable set "
                f"{sorted(_MODEL_EMITTABLE_OUTCOMES)}."
            ),
        )
    # Cross-field consistency the model might miss — if outcome=REVISE but
    # feedback is null, that's a parse error: the contract is unambiguous.
    if outcome_str == Outcome.REVISE.value and not parsed.get("feedback"):
        raise JudgeParseError(
            raw_text=raw_text,
            reason="outcome=REVISE but 'feedback' is null or empty.",
        )
    if outcome_str == Outcome.ESCALATE.value and not parsed.get("quarantine_reason"):
        raise JudgeParseError(
            raw_text=raw_text,
            reason="outcome=ESCALATE but 'quarantine_reason' is null or empty.",
        )
    return parsed


# ─── The actual evaluator ────────────────────────────────────────────────────


def evaluate(
    proposal: ActionProposal,
    policy: Policy,
    *,
    timeout_s: float = _JUDGE_TIMEOUT_S,
    max_parse_retries: int = _MAX_PARSE_RETRIES,
) -> JudgeDecision:
    """Evaluate a proposed action against a policy. Returns a JudgeDecision.

    Never raises. Transport failures, parse failures past retry, and any
    other exception inside the judge pipeline land as
    Outcome.JUDGE_UNAVAILABLE so the caller falls open and Sean's manual
    review remains the canonical control (Tier-A preserved).

    Args:
        proposal:           The actor's typed proposal.
        policy:             The loaded policy gating the actor.
        timeout_s:          Per-call HTTP timeout. Default 30s.
        max_parse_retries:  Max retries when the model's output won't parse.
                            Default 3.

    Returns:
        JudgeDecision with outcome in {ALLOW, BLOCK, REVISE, ESCALATE,
        JUDGE_UNAVAILABLE}. The model emits the first 4; this function emits
        JUDGE_UNAVAILABLE on any unrecoverable path.
    """
    start = time.monotonic()
    system = _build_system_prompt(policy)
    attempted_model = _DEFAULT_ATTEMPTED_MODEL
    retry_context = ""
    last_parse_error: str | None = None

    for attempt in range(max_parse_retries + 1):
        user = _build_user_prompt(proposal, retry_context=retry_context)

        try:
            raw_text, model_used = _call_router(
                task=JUDGE_TASK_KEY,
                system=system,
                user=user,
                timeout_s=timeout_s,
            )
            # Once the router told us a model, attribute future JUDGE_UNAVAILABLE
            # rows to the correct model — gives the dashboard true per-model
            # availability stats instead of always blaming the default.
            attempted_model = model_used
        except JudgeTransportError as exc:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            logger.warning(
                "judge.evaluate transport failure (attempt %d): %s",
                attempt + 1,
                exc,
            )
            return JudgeDecision(
                outcome=Outcome.JUDGE_UNAVAILABLE,
                model_used=attempted_model,
                latency_ms=elapsed_ms,
            )
        except Exception as exc:  # noqa: BLE001 — fail-open is intentional
            elapsed_ms = int((time.monotonic() - start) * 1000)
            logger.exception(
                "judge.evaluate unexpected error (attempt %d): %s",
                attempt + 1,
                exc,
            )
            return JudgeDecision(
                outcome=Outcome.JUDGE_UNAVAILABLE,
                model_used=attempted_model,
                latency_ms=elapsed_ms,
            )

        try:
            parsed = _parse_judge_output(raw_text)
        except JudgeParseError as exc:
            last_parse_error = exc.reason
            logger.info(
                "judge.evaluate parse failure (attempt %d): %s",
                attempt + 1,
                exc.reason,
            )
            # On retry, prepend the parse error so the model can self-correct.
            # If we're out of retries, fall through to JUDGE_UNAVAILABLE below.
            if attempt < max_parse_retries:
                retry_context = (
                    f"Your previous response failed to parse. Reason: "
                    f"{exc.reason}\n\n"
                    f"Emit ONLY a single JSON object matching the output "
                    f"contract from the system prompt. No prose, no Markdown."
                )
                continue
            break  # exhausted retries; fall to JUDGE_UNAVAILABLE

        # Successful parse — turn the dict into a JudgeDecision.
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return JudgeDecision(
            outcome=Outcome(parsed["outcome"]),
            feedback=parsed.get("feedback"),
            quarantine_reason=parsed.get("quarantine_reason"),
            model_used=attempted_model,
            latency_ms=elapsed_ms,
        )

    # Exhausted retries — JUDGE_UNAVAILABLE with elapsed time and the last
    # parse error logged.
    elapsed_ms = int((time.monotonic() - start) * 1000)
    logger.warning(
        "judge.evaluate exhausted %d retries; last parse error: %s",
        max_parse_retries,
        last_parse_error,
    )
    return JudgeDecision(
        outcome=Outcome.JUDGE_UNAVAILABLE,
        model_used=attempted_model,
        latency_ms=elapsed_ms,
    )
