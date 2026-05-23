"""Generate a 32K-token prompt with a needle at the 28K-token mark.

Uses lorem-ipsum-style filler (no external deps; deterministic given a seed)
so each model sees the same haystack distribution. The needle is a randomly
generated 12-character uppercase token; the model is asked to recall it.

Token counting is approximate (chars/4 heuristic). Targeted budget: 32K tokens
≈ 128K characters of filler.
"""
from __future__ import annotations

import random
import string
from dataclasses import dataclass

CHAR_PER_TOKEN = 4  # Conservative estimate; matches OpenAI's old rule of thumb.

_FILLER_PARA = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
    "consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse "
    "cillum dolore eu fugiat nulla pariatur. "
)


@dataclass
class HaystackPrompt:
    prompt: str
    needle: str
    needle_position_chars: int


def make_needle(rng: random.Random) -> str:
    """Generate a 12-char uppercase needle (alphanumeric, no ambiguous chars)."""
    alphabet = "".join(c for c in string.ascii_uppercase + string.digits if c not in "OIL01")
    return "".join(rng.choices(alphabet, k=12))


def generate(
    seed: int = 42,
    target_tokens: int = 32000,
    needle_position_tokens: int = 28000,
) -> HaystackPrompt:
    rng = random.Random(seed)
    needle = make_needle(rng)
    target_chars = target_tokens * CHAR_PER_TOKEN
    needle_char_position = needle_position_tokens * CHAR_PER_TOKEN

    filler = (_FILLER_PARA * ((target_chars // len(_FILLER_PARA)) + 1))[:target_chars]
    sentence = f" The secret code is {needle}. Remember it. "
    injected = filler[:needle_char_position] + sentence + filler[needle_char_position:target_chars]

    prompt = (
        "Read the following long document carefully. At the end, I will ask you "
        "to recall a specific 12-character code that appears somewhere inside. "
        "Do not summarize the document — only output the code when asked.\n\n"
        "DOCUMENT:\n"
        f"{injected}\n\n"
        "QUESTION: What was the 12-character secret code? Output ONLY the code, "
        "nothing else."
    )
    return HaystackPrompt(prompt=prompt, needle=needle, needle_position_chars=needle_char_position)


if __name__ == "__main__":
    import json
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    result = generate(seed=seed)
    print(json.dumps({"seed": seed, "needle": result.needle, "prompt_chars": len(result.prompt)}))
