#!/usr/bin/env python3
"""Build the blind-read console for the spread run.

Assigns each draft a random letter, seals the mapping to a file the reader does
not open, and emits a self-contained HTML page. Metrics and Sean's published
final are embedded but gated behind ranking submission, so neither can anchor
the read. Stdlib only.
"""
import html, json, random, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SEED = 20260901

ARM_META = {
    "a01-opus5-cc":          ("Claude Opus 5",        "Claude Code subagent", "full"),
    "a02-opus5-cc-twin":     ("Claude Opus 5",        "Claude Code subagent", "full"),
    "a03-gpt55-codex":       ("GPT-5.5",              "Codex CLI",            "full"),
    "a04-gpt55-api":         ("GPT-5.5",              "OpenRouter API",       "full"),
    "a05-gemini31pro":       ("Gemini 3.1 Pro",       "OpenRouter API",       "full"),
    "a06-grok46":            ("Grok 4.6",             "OpenRouter API",       "full"),
    "a07-kimi-k3":           ("Kimi K3",              "OpenRouter API",       "full"),
    "a08-glm53":             ("GLM 5.3",              "OpenRouter API",       "full"),
    "a09-deepseek-v4":       ("DeepSeek v4 Pro",      "OpenRouter API",       "full"),
    "a10-mistral-lg":        ("Mistral Large 2512",   "OpenRouter API",       "full"),
    "a11-opus5-cc-stripped": ("Claude Opus 5",        "Claude Code subagent", "stripped"),
    "a12-qwen36-local":      ("Qwen3.6 35B-A3B",      "local Ollama @64K",    "full"),
}


def to_blocks(md: str) -> list[dict]:
    """Split a draft into title / subtitle / paragraphs. Drafts vary in whether
    they use markdown markers, so detect structurally rather than by syntax."""
    lines = [l.rstrip() for l in md.strip().splitlines()]
    lines = [l for l in lines if l.strip() not in ("---", "***")]
    blocks, title, sub = [], None, None
    body: list[str] = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if title is None:
            title = re.sub(r"^#+\s*", "", s).strip("*_ ")
            continue
        if sub is None:
            sub = re.sub(r"^#+\s*", "", s).strip("*_ ")
            continue
        body.append(s)
    for p in body:
        if re.match(r"^#{1,6}\s", p):
            blocks.append({"t": "h", "x": re.sub(r"^#+\s*", "", p)})
        elif p.startswith(">"):
            blocks.append({"t": "q", "x": p.lstrip("> ").strip()})
        else:
            blocks.append({"t": "p", "x": p})
    return [{"title": title or "", "subtitle": sub or "", "body": blocks}]


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s


def render_draft(d: dict) -> str:
    out = [f'<h2 class="d-title">{inline(d["title"])}</h2>']
    if d["subtitle"]:
        out.append(f'<p class="d-sub">{inline(d["subtitle"])}</p>')
    for b in d["body"]:
        tag = {"h": "h3", "q": "blockquote", "p": "p"}[b["t"]]
        cls = ' class="d-h"' if b["t"] == "h" else ""
        out.append(f"<{tag}{cls}>{inline(b['x'])}</{tag}>")
    return "\n".join(out)


def main() -> None:
    drafts = sorted(p for p in (HERE / "drafts").glob("*.md") if p.read_text().strip())
    arms = [p.stem for p in drafts]
    letters = list("ABCDEFGHIJKL")[: len(arms)]
    rng = random.Random(SEED)
    shuffled = arms[:]
    rng.shuffle(shuffled)
    mapping = dict(zip(letters, shuffled))

    (HERE / "SEALED-MAPPING.json").write_text(json.dumps(
        {L: {"arm": a, "model": ARM_META[a][0], "harness": ARM_META[a][1], "samples": ARM_META[a][2]}
         for L, a in mapping.items()}, indent=2) + "\n")

    meas = {}
    mp = HERE / "measurements.json"
    if mp.exists():
        meas = json.loads(mp.read_text())

    items = []
    for L in letters:
        arm = mapping[L]
        text = (HERE / "drafts" / f"{arm}.md").read_text()
        d = to_blocks(text)[0]
        m = meas.get(arm, {}).get("analyzer", {}).get("metrics", {})
        sl = m.get("sentence_length", {})
        items.append({
            "letter": L, "html": render_draft(d), "words": len(text.split()),
            "model": ARM_META[arm][0], "harness": ARM_META[arm][1], "samples": ARM_META[arm][2],
            "metrics": {
                "sentences": sl.get("n"), "mean": sl.get("mean"), "cv": sl.get("cv"),
                "short": sl.get("short_share"), "long": sl.get("long_share"),
                "mattr": round(m.get("lexical_diversity", {}).get("mattr", 0) or 0, 3),
            },
        })

    final_p = ROOT / "vault/20_projects/substack-studio/rules-off-experiment/arm-b-publish-ready.md"
    final_html = render_draft(to_blocks(final_p.read_text())[0]) if final_p.exists() else ""

    tpl = (HERE / "console_template.html").read_text()
    page = tpl.replace("/*__DATA__*/", json.dumps(items)).replace("<!--__FINAL__-->", final_html)
    (HERE / "console.html").write_text(page)
    print(f"console.html — {len(items)} drafts, letters {letters[0]}–{letters[-1]}")
    print("sealed mapping written to SEALED-MAPPING.json")


if __name__ == "__main__":
    main()
