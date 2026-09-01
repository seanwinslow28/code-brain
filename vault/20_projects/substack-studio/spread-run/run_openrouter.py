#!/usr/bin/env python3
"""Fire the single-shot spread-run arms through OpenRouter.

Every call is pinned to zero-data-retention, non-collecting providers; the
open-weight arms from Chinese labs are additionally restricted to US hosts.
Writes one draft per arm plus a costs.json manifest. Stdlib only.
"""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

US_HOSTS = ["Fireworks", "Together", "BaseTen", "DeepInfra", "Parasail", "Modal", "CoreWeave"]

# arm id -> (openrouter slug, context bundle, provider allowlist or None)
ARMS = {
    "a04-gpt55-api":    ("openai/gpt-5.5",                "context-full.md", None),
    "a05-gemini31pro":  ("google/gemini-3.1-pro-preview", "context-full.md", None),
    "a06-grok46":       ("x-ai/grok-4.6",                 "context-full.md", None),
    "a07-kimi-k3":      ("moonshotai/kimi-k3",            "context-full.md", US_HOSTS),
    "a08-glm53":        ("z-ai/glm-5.3",                  "context-full.md", US_HOSTS),
    "a09-deepseek-v4":  ("deepseek/deepseek-v4-pro",      "context-full.md", US_HOSTS),
    "a10-mistral-lg":   ("mistralai/mistral-large-2512",  "context-full.md", None),
}


def api_key() -> str:
    for p in (ROOT / ".env", ROOT / "tools/llm-council/.env", ROOT / "agents-sdk/.env"):
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip().startswith("OPENROUTER_API_KEY"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENROUTER_API_KEY not found")


def run(arm: str, slug: str, bundle: str, only, key: str, prompt: str, zdr: bool = True) -> dict:
    """One arm. `zdr=True` demands a zero-retention endpoint; callers fall back to
    `zdr=False` (still non-collecting) for first-party vendors that offer no ZDR tier."""
    context = (HERE / bundle).read_text()
    provider = {"data_collection": "deny"}
    if zdr:
        provider["zdr"] = True
    if only:
        provider["only"] = only
    body = json.dumps({
        "model": slug,
        "messages": [{"role": "user", "content": f"{prompt}\n\n{context}"}],
        "max_tokens": 32000,
        "temperature": 1,
        "provider": provider,
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.time()
    try:
        d = json.load(urllib.request.urlopen(req, timeout=900))
    except urllib.error.HTTPError as e:
        return {"arm": arm, "model": slug, "error": f"HTTP {e.code}: {e.read().decode()[:300]}"}
    except Exception as e:  # noqa: BLE001
        return {"arm": arm, "model": slug, "error": f"{type(e).__name__}: {e}"}
    if "error" in d:
        return {"arm": arm, "model": slug, "error": str(d["error"])[:300]}
    msg = d["choices"][0]["message"]
    text = (msg.get("content") or "").strip()
    reasoning_chars = len(msg.get("reasoning") or "")
    usage = d.get("usage", {})
    (HERE / "drafts" / f"{arm}.md").write_text(text + "\n")
    return {
        "arm": arm, "model": slug, "provider": d.get("provider"),
        "words": len(text.split()), "seconds": round(time.time() - t0, 1),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "cost_usd": usage.get("cost"), "reasoning_chars": reasoning_chars,
        "finish": d["choices"][0].get("finish_reason"),
    }


def main() -> None:
    key = api_key()
    prompt = (HERE / "PROMPT.md").read_text().split("-->", 1)[1].strip()
    only_arms = sys.argv[1:] or list(ARMS)
    out = []
    for arm in only_arms:
        slug, bundle, allow = ARMS[arm]
        print(f"[{arm}] {slug} ...", flush=True)
        r = run(arm, slug, bundle, allow, key, prompt)
        if "No endpoints found matching your data policy" in str(r.get("error", "")):
            print("    no ZDR endpoint; retrying non-collecting only", flush=True)
            r = run(arm, slug, bundle, allow, key, prompt, zdr=False)
            r["zdr"] = False
        print("   ", json.dumps(r)[:220], flush=True)
        out.append(r)
    manifest = HERE / "costs.json"
    prev = json.loads(manifest.read_text()) if manifest.exists() else []
    manifest.write_text(json.dumps(prev + out, indent=2) + "\n")
    total = sum(r.get("cost_usd") or 0 for r in out)
    print(f"\nTOTAL THIS BATCH: ${total:.4f}")


if __name__ == "__main__":
    main()
