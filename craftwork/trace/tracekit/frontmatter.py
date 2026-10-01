"""A YAML subset parser for record and label frontmatter — stdlib only.

The subset is exactly what the templates use, no more:

- `key: scalar` — null/~ → None, true/false, integers, quoted strings,
  anything else as the raw string (instants stay strings).
- `key:` followed by an indented block — a list (`- item`) or a mapping.
- list items that are scalars, or mappings (`- path: x` with continuation
  lines at the key's indent).
- flow lists of scalars: `[]`, `[a, b]`.
- comments: `# …` at line start or after whitespace, outside quotes.

Anything else raises FrontmatterError with the line number, so a record the
checker cannot read is a loud failure, never a silent skip.
"""
from __future__ import annotations

import re
from typing import Any

__all__ = ["FrontmatterError", "parse_yaml_subset", "split_frontmatter"]


class FrontmatterError(ValueError):
    """The text is not in the record frontmatter subset."""


_FENCE = "---"


def split_frontmatter(doc: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter mapping, body) for a document opening with `---`."""
    lines = doc.split("\n")
    if not lines or lines[0].strip() != _FENCE:
        raise FrontmatterError("document does not open with a --- frontmatter fence")
    for i in range(1, len(lines)):
        if lines[i].strip() == _FENCE:
            header = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1 :])
            return parse_yaml_subset(header), body
    raise FrontmatterError("frontmatter fence never closes")


# --------------------------------------------------------------------------- #
# scalars
# --------------------------------------------------------------------------- #

_INT = re.compile(r"^-?\d+$")


def _strip_comment(raw: str) -> str:
    """Drop a trailing ` # comment` that sits outside quotes."""
    out = []
    quote: str | None = None
    for i, ch in enumerate(raw):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or raw[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _scalar(text: str, lineno: int) -> Any:
    text = text.strip()
    if text == "" or text in ("null", "~"):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if _INT.match(text):
        return int(text)
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        inner = text[1:-1]
        if text[0] == '"':
            inner = inner.replace('\\"', '"').replace("\\\\", "\\")
        else:
            inner = inner.replace("''", "'")
        return inner
    if text.startswith("["):
        if not text.endswith("]"):
            raise FrontmatterError(f"line {lineno}: flow list never closes")
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_scalar(part, lineno) for part in inner.split(",")]
    if text.startswith("{"):
        raise FrontmatterError(f"line {lineno}: flow mappings are outside the subset; use a block")
    return text


# --------------------------------------------------------------------------- #
# blocks
# --------------------------------------------------------------------------- #


class _Line:
    __slots__ = ("no", "indent", "text")

    def __init__(self, no: int, indent: int, text: str):
        self.no, self.indent, self.text = no, indent, text


def _lines(src: str) -> list[_Line]:
    out = []
    for i, raw in enumerate(src.split("\n"), start=1):
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise FrontmatterError(f"line {i}: tabs are not indentation; use spaces")
        text = _strip_comment(raw)
        if not text.strip():
            continue
        indent = len(text) - len(text.lstrip(" "))
        out.append(_Line(i, indent, text.strip()))
    return out


_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_\-]*):(?:\s+(.*))?$")


def parse_yaml_subset(src: str) -> dict[str, Any]:
    lines = _lines(src)
    value, nxt = _parse_block(lines, 0, expect_indent=lines[0].indent if lines else 0)
    if nxt != len(lines):
        ln = lines[nxt]
        raise FrontmatterError(f"line {ln.no}: unexpected indentation")
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise FrontmatterError("line 1: the top level must be a mapping")
    return value


def _parse_block(lines: list[_Line], i: int, expect_indent: int) -> tuple[Any, int]:
    """Parse the block starting at lines[i] whose lines sit at expect_indent."""
    if i >= len(lines) or lines[i].indent != expect_indent:
        return None, i
    if lines[i].text.startswith("- "):
        return _parse_list(lines, i, expect_indent)
    return _parse_mapping(lines, i, expect_indent)


def _parse_mapping(lines: list[_Line], i: int, indent: int) -> tuple[dict[str, Any], int]:
    out: dict[str, Any] = {}
    while i < len(lines):
        ln = lines[i]
        if ln.indent < indent:
            break
        if ln.indent > indent:
            raise FrontmatterError(f"line {ln.no}: unexpected indentation")
        if ln.text.startswith("- "):
            raise FrontmatterError(f"line {ln.no}: list item where a key was expected")
        m = _KEY.match(ln.text)
        if not m:
            raise FrontmatterError(f"line {ln.no}: expected `key: value`, got {ln.text!r}")
        key, rest = m.group(1), m.group(2)
        if key in out:
            raise FrontmatterError(f"line {ln.no}: duplicate key {key!r}")
        i += 1
        if rest is None or rest.strip() == "":
            # nested block, or nothing
            if i < len(lines) and lines[i].indent > indent:
                value, i = _parse_block(lines, i, lines[i].indent)
            else:
                value = None
        else:
            value = _scalar(rest, ln.no)
            if i < len(lines) and lines[i].indent > indent:
                raise FrontmatterError(f"line {lines[i].no}: unexpected indentation under a scalar")
        out[key] = value
    return out, i


def _parse_list(lines: list[_Line], i: int, indent: int) -> tuple[list[Any], int]:
    out: list[Any] = []
    while i < len(lines):
        ln = lines[i]
        if ln.indent < indent:
            break
        if ln.indent > indent:
            raise FrontmatterError(f"line {ln.no}: unexpected indentation")
        if not ln.text.startswith("- "):
            raise FrontmatterError(f"line {ln.no}: expected a `- ` list item")
        item_text = ln.text[2:].strip()
        m = _KEY.match(item_text)
        if m and (m.group(2) is None or not m.group(2).startswith("[") or True) and _looks_like_mapping_item(item_text):
            # a mapping item: the first key is on the dash line, the rest continue at indent+2
            key_indent = indent + 2
            first = _Line(ln.no, key_indent, item_text)
            sub = [first]
            j = i + 1
            while j < len(lines) and lines[j].indent >= key_indent:
                sub.append(lines[j])
                j += 1
            value, consumed = _parse_mapping(sub, 0, key_indent)
            if consumed != len(sub):
                bad = sub[consumed]
                raise FrontmatterError(f"line {bad.no}: unexpected indentation")
            out.append(value)
            i = j
        else:
            out.append(_scalar(item_text, ln.no))
            i += 1
    return out, i


def _looks_like_mapping_item(text: str) -> bool:
    """`path: x` is a mapping item; `sha256:abc` (no space) or a URL is a scalar."""
    m = _KEY.match(text)
    if not m:
        return False
    rest = m.group(2)
    return rest is None or rest != "" or text.endswith(":")
