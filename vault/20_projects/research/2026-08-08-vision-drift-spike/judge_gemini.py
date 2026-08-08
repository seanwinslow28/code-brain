#!/usr/bin/env python3
"""Drift-spike judge: gemini vision models over the case manifest.

Usage: judge_gemini.py --model gemini-3.5-flash --n 3 --out results/gemini-flash.json
"""
import argparse
import json
import mimetypes
import pathlib
import re
import subprocess
import sys
import time

from google import genai
from google.genai import types

SPIKE = pathlib.Path(__file__).parent

PROMPT = """You are a series-consistency reviewer for a serialized visual work \
(webcomic / animated series / illustrated serial). You will see:
1. CANON REFERENCE image(s) — how this character is established in the series so far.
2. Optionally, a CANON UPDATE note — an intentional, creator-declared change to the character or the series' art style.
3. One CANDIDATE image — a frame from the newest installment.

Judge whether the CANDIDATE is consistent with this character's canon.

Rules:
- Undeclared changes to character identity, facial features, body proportions, anatomy (e.g. number of limbs), color palette, or art-style register ARE drift.
- Changes declared in the CANON UPDATE note are intentional and are NOT drift — but the note only covers what it declares; any OTHER undeclared change is still drift.
- Legitimate variation in pose, camera angle/view, facial expression, framing, cropping, or scene context is NOT drift.

Respond with STRICT JSON only, no prose around it:
{"verdict": "consistent" | "drifted", "drift_axes": [<zero or more of: "identity","proportion","anatomy","palette","style-register","other">], "receipt": "<one sentence naming the specific visual evidence for your verdict>", "confidence": <0.0-1.0>}
"""


def keychain_key() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", "com.sean.agents.gemini_api_key", "-w"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def img_part(path: pathlib.Path) -> types.Part:
    mime = mimetypes.guess_type(str(path))[0] or "image/png"
    return types.Part.from_bytes(data=path.read_bytes(), mime_type=mime)


def parse_json(text: str):
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-3.5-flash")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    manifest = json.loads((SPIKE / "manifest.json").read_text())
    root = pathlib.Path(manifest["anima_root"])
    client = genai.Client(api_key=keychain_key())

    results = []
    for case in manifest["cases"]:
        refs = [root / p for p in manifest["ref_sets"][case["refs"]]]
        cand = root / case["candidate"]
        contents: list = [PROMPT, f"\nCANON REFERENCE images ({len(refs)}):"]
        contents += [img_part(p) for p in refs]
        if case["note"]:
            contents.append(f"\nCANON UPDATE note: {case['note']}")
        else:
            contents.append("\nCANON UPDATE note: (none provided)")
        contents.append("\nCANDIDATE image:")
        contents.append(img_part(cand))

        votes = []
        for i in range(args.n):
            for attempt in range(3):
                try:
                    resp = client.models.generate_content(model=args.model, contents=contents)
                    parsed = parse_json(resp.text or "")
                    if parsed and parsed.get("verdict") in ("consistent", "drifted"):
                        votes.append(parsed)
                    else:
                        votes.append({"verdict": "unparseable", "raw": (resp.text or "")[:400]})
                    break
                except Exception as e:  # noqa: BLE001
                    if attempt == 2:
                        votes.append({"verdict": "error", "error": str(e)[:300]})
                    else:
                        time.sleep(5 * (attempt + 1))
        drifted = sum(1 for v in votes if v.get("verdict") == "drifted")
        consistent = sum(1 for v in votes if v.get("verdict") == "consistent")
        majority = "drifted" if drifted > consistent else "consistent" if consistent > drifted else "tie"
        results.append({"id": case["id"], "majority": majority,
                        "votes": votes, "n_drift": drifted, "n_consistent": consistent})
        print(f"{case['id']}: {majority} ({drifted}d/{consistent}c)", flush=True)

    out = SPIKE / args.out
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"model": args.model, "n": args.n, "results": results}, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
