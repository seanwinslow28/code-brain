"""LLM-judge runner — wraps Qwen3-14B (local Ollama) and Sonnet 4.6 (sample-check).

Ensemble strategy (per spec Section 4.2): single-judge for `signature_move_present`,
3-judge majority vote for `sounds_like_sean` and `no_anti_pattern_violation`.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional, Protocol


class _LLMClient(Protocol):
    def complete(self, prompt: str, model: str = ..., temperature: float = ..., seed: int = ...) -> str: ...


@dataclass
class JudgeResult:
    passed: bool
    raw_response: str
    reason: str


@dataclass
class EnsembleResult:
    passed: bool  # majority decision
    individual_results: list[JudgeResult]
    yes_count: int
    no_count: int


class JudgeRunner:
    def __init__(
        self,
        local_client: _LLMClient,
        sonnet_client: Optional[_LLMClient],
        prompt_template: str,
    ):
        self.local = local_client
        self.sonnet = sonnet_client
        self.template = prompt_template

    @staticmethod
    def _parse_yes_no(response: str) -> tuple[bool | None, str]:
        last_line = response.strip().splitlines()[-1].strip().upper() if response.strip() else ""
        if last_line == "YES":
            return True, "yes"
        if last_line == "NO":
            return False, "no"
        return None, f"ambiguous (last line: {last_line!r})"

    def judge_single(
        self,
        output: str,
        anchors: list[str],
        question: str,
        mode: str,
        use_sonnet: bool = False,
        seed: int = 0,
    ) -> JudgeResult:
        a1 = anchors[0] if len(anchors) >= 1 else ""
        a2 = anchors[1] if len(anchors) >= 2 else ""
        prompt = self.template.format(
            output=output, anchor_1=a1, anchor_2=a2, question=question, mode=mode,
        )
        client = self.sonnet if (use_sonnet and self.sonnet) else self.local
        model = "claude-sonnet-4-6" if (use_sonnet and self.sonnet) else "qwen3-14b-research:latest"
        raw = client.complete(prompt=prompt, model=model, temperature=0.0, seed=seed)
        parsed, reason = self._parse_yes_no(raw)
        if parsed is None:
            return JudgeResult(passed=False, raw_response=raw, reason=reason)
        return JudgeResult(passed=parsed, raw_response=raw, reason=reason)
