#!/usr/bin/env python3
"""Unit tests for the Oracle's news lane (#239). No network, no model, no render.

    python3 .claude/skills/content-oracle/test_news_lane.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import news_lane as nl  # noqa: E402

PULL = """# News pull -- 2026-09-03 (window 2026-08-27 to 2026-09-03, legs hn,youtube,web)

# BRANCH agents -- query: AI agents news this week

### YouTube Videos

**abc123** (score:78) Some Channel (2026-09-03) [23,376 views, 551 likes]
  A Big Week In Agents
  https://www.youtube.com/watch?v=abc123
  Highlights:
    - "quote"

### Hacker News Stories

**HN1** (score:95) hn/someone (2026-08-28) [117pts, 36cmt]
  Terminal-Bench-Science: Evaluating AI agents on scientific research workflows
  https://news.ycombinator.com/item?id=49472820
  *HN story about ...*

### Web Results

**W1** [WEB] (score:66) openai.com (2026-09-01) [date:med]
  Introducing a thing
  https://openai.com/index/introducing-a-thing
  Snippet text...
"""


def _item(n: int, title: str, p1: str, p2: str, p3: str) -> str:
    return f"## {title}\n\n{p1}\n\n{p2}\n\n{p3}\n\n"


def _report(items: list[str], sources: list[str], sources_last: bool = True, fence: bool = True) -> str:
    body = "---\ntype: oracle-report\ndate: 2026-09-03\n---\n\n# The week in AI, Thursday\n\nA quiet week.\n\n"
    src = "## Sources\n\n" + ("```text\n" if fence else "") + "\n".join(sources) + ("\n```\n" if fence else "\n")
    if sources_last:
        return body + "".join(items) + src
    return body + items[0] + src + "".join(items[1:])


GOOD_ITEMS = [
    _item(1, "OpenAI ships a thing",
          "OpenAI said on its own blog this week that it shipped a thing.",
          "The thing can now do a job it could not do last week.",
          "Card: run the thing on a task, expect it to finish."),
    _item(2, "A benchmark for research agents",
          "A group posted a benchmark on Hacker News, and the thread argued about it.",
          "Agents can now be scored on a real research workflow rather than a toy task.",
          "Card: run one fleet agent against it, expect a low score and a lesson."),
]
GOOD_SOURCES = [
    "1. Introducing a thing -- https://openai.com/index/introducing-a-thing",
    "2. https://news.ycombinator.com/item?id=49472820",
]


class PullIndex(unittest.TestCase):
    def test_parse_pull_indexes_titles_and_urls_without_transcripts(self):
        items = nl.parse_pull(PULL)
        self.assertEqual([i.section for i in items], ["YouTube Videos", "Hacker News Stories", "Web Results"])
        self.assertEqual(items[0].title, "A Big Week In Agents")
        self.assertEqual(items[0].url, "https://www.youtube.com/watch?v=abc123")
        self.assertEqual(items[1].url, "https://news.ycombinator.com/item?id=49472820")
        self.assertEqual(items[2].who, "openai.com")
        self.assertTrue(all(i.branch == "agents" for i in items))
        idx = nl.render_index(items, date(2026, 8, 27), date(2026, 9, 3))
        self.assertIn("In window, per branch: agents 3", idx)
        self.assertNotIn("quote", idx)
        idx = nl.render_index(items, date(2026, 9, 1), date(2026, 9, 3))
        self.assertIn("agents 2", idx)
        self.assertIn("Out of window (1)", idx)

    def test_pull_commands_use_news_phrasing_and_free_legs(self):
        cmds = nl.pull_commands(["news", "creativity"], 7, nl.DEFAULT_SEARCH)
        self.assertEqual([(b, leg) for b, leg, _ in cmds], [("news", "youtube,web"), ("creativity", "youtube,web")])
        self.assertIn("latest AI news this week", cmds[0][2])    # youtube + web: NEWS phrasing
        self.assertIn("--quick", cmds[0][2])
        self.assertNotIn("reddit", nl.DEFAULT_SEARCH)
        self.assertNotIn("this week", nl.BRANCHES["news"][1])    # hn: bare nouns

    def test_hn_items_format_in_the_compact_shape_with_the_story_url_first(self):
        items = [{"object_id": "1", "title": "A benchmark for agents", "url": "https://example.org/post",
                  "hn_url": "https://news.ycombinator.com/item?id=1", "author": "someone", "date": "2026-08-28",
                  "engagement": {"points": 117, "num_comments": 36}, "relevance": 0.95}]
        text = "# BRANCH agents -- leg hn -- query: AI agents\n\n" + nl.format_hn_items(items)
        parsed = nl.parse_pull(text)
        self.assertEqual(parsed[0].section, "Hacker News Stories")
        self.assertEqual(parsed[0].url, "https://example.org/post")
        self.assertEqual(parsed[0].title, "A benchmark for agents")
        self.assertIn("Thread: https://news.ycombinator.com/item?id=1", text)
        self.assertIn("[117pts, 36cmt]", text)
        self.assertIn("No Hacker News stories", nl.format_hn_items([]))
        with self.assertRaises(SystemExit):
            nl.pull_commands(["nope"], 7, nl.DEFAULT_SEARCH)

    def test_strip_ansi(self):
        self.assertEqual(nl.strip_ansi("\x1b[93mReddit\x1b[0m done"), "Reddit done")


class SpokenSafe(unittest.TestCase):
    def test_date_in_words(self):
        self.assertEqual(nl.date_in_words(date(2026, 9, 6)), "Sunday, September sixth, twenty twenty-six")
        self.assertEqual(nl.date_in_words(date(2026, 9, 22)), "Tuesday, September twenty-second, twenty twenty-six")
        self.assertEqual(nl.date_in_words(date(2026, 9, 30)), "Wednesday, September thirtieth, twenty twenty-six")

    def test_figures_catch_percent_money_magnitude_multiplier_only(self):
        found = nl.figure_sentences(
            "It runs three models. GLM 5.3 Flash scored well. Open models took sixty-two percent of tokens. "
            "It costs eleven thousand dollars. It is four times faster than before. Version 2 shipped.")
        kinds = [k for k, _ in found]
        self.assertEqual(kinds, ["percentage", "money", "multiplier"])  # first match per sentence

    def test_not_words_rules(self):
        rep = nl.parse_report(_report([_item(1, "T", "On 2026-09-01 it shipped.", "Now it can.", "Card: do.")],
                                      ["1. https://openai.com/x"]))
        errors, _ = nl.lint_report(rep)
        self.assertTrue(any("ISO date" in e for e in errors))
        rep = nl.parse_report(_report([_item(1, "T", "It has 23,376 views.", "Now it can.", "Card: do.")],
                                      ["1. https://openai.com/x"]))
        errors, _ = nl.lint_report(rep)
        self.assertTrue(any("thousands separator" in e for e in errors))
        rep = nl.parse_report(_report([_item(1, "T", "GLM 5.3 Flash shipped.", "Now it can.", "Card: do.")],
                                      ["1. https://openai.com/x"]))
        errors, _ = nl.lint_report(rep)
        self.assertEqual(errors, [])


class Lint(unittest.TestCase):
    def test_good_report_is_clean_with_a_length_warning(self):
        rep = nl.parse_report(_report(GOOD_ITEMS, GOOD_SOURCES))
        self.assertEqual(len(rep.items), 2)
        self.assertEqual(sorted(rep.sources), [1, 2])
        errors, warnings = nl.lint_report(rep)
        self.assertEqual(errors, [])
        self.assertTrue(any("band is 1200-1500" in w for w in warnings))

    def test_shape_violations(self):
        seven = [_item(i, f"T{i}", "A.", "B.", "C.") for i in range(1, 8)]
        srcs = [f"{i}. https://openai.com/{i}" for i in range(1, 8)]
        errors, _ = nl.lint_report(nl.parse_report(_report(seven, srcs)))
        self.assertTrue(any("7 items" in e for e in errors))

        four_paras = ["## T\n\nA.\n\nB.\n\nC.\n\nD.\n\n"]
        errors, _ = nl.lint_report(nl.parse_report(_report(four_paras, ["1. https://openai.com/x"])))
        self.assertTrue(any("4 paragraphs" in e for e in errors))

        table = [_item(1, "T", "| a | b |\n| - | - |", "B.", "C.")]
        errors, _ = nl.lint_report(nl.parse_report(_report(table, ["1. https://openai.com/x"])))
        self.assertTrue(any("table" in e for e in errors))

        long_list = [_item(1, "T", "- one\n- two\n- three\n- four", "B.", "C.")]
        errors, _ = nl.lint_report(nl.parse_report(_report(long_list, ["1. https://openai.com/x"])))
        self.assertTrue(any("a list of 4" in e for e in errors))

        raw_url = [_item(1, "T", "See https://openai.com/x for more.", "B.", "C.")]
        errors, _ = nl.lint_report(nl.parse_report(_report(raw_url, ["1. https://openai.com/x"])))
        self.assertTrue(any("raw URL" in e for e in errors))

        sub = [_item(1, "T", "### deeper", "B.", "C.")]
        errors, _ = nl.lint_report(nl.parse_report(_report(sub, ["1. https://openai.com/x"])))
        self.assertTrue(any("sub-heading" in e for e in errors))

        long_item = [_item(1, "T", "word " * 260, "B.", "C.")]
        errors, _ = nl.lint_report(nl.parse_report(_report(long_item, ["1. https://openai.com/x"])))
        self.assertTrue(any("words; an item over 250" in e for e in errors))

    def test_sources_rules(self):
        errors, _ = nl.lint_report(nl.parse_report(_report(GOOD_ITEMS, ["1. https://openai.com/x"])))
        self.assertTrue(any("no line numbered 2" in e for e in errors))
        errors, _ = nl.lint_report(nl.parse_report(_report(GOOD_ITEMS, GOOD_SOURCES + ["3. https://openai.com/y"])))
        self.assertTrue(any("names item 3" in e for e in errors))
        errors, _ = nl.lint_report(nl.parse_report(_report(GOOD_ITEMS, GOOD_SOURCES, fence=False)))
        self.assertTrue(any("code fence" in e for e in errors))
        errors, _ = nl.lint_report(nl.parse_report(_report(GOOD_ITEMS, GOOD_SOURCES, sources_last=False)))
        self.assertTrue(any("last section" in e for e in errors))
        errors, _ = nl.lint_report(nl.parse_report("".join(GOOD_ITEMS)))
        self.assertTrue(any("no `## Sources`" in e for e in errors))

    def test_hard_cap(self):
        big = [_item(i, f"T{i}", "word " * 300, "B.", "C.") for i in range(1, 8)]  # 7 items is its own error; the cap is the point
        srcs = [f"{i}. https://openai.com/{i}" for i in range(1, 8)]
        errors, _ = nl.lint_report(nl.parse_report(_report(big, srcs)))
        self.assertTrue(any("hard cap is 2000" in e for e in errors))


class TierGate(unittest.TestCase):
    def test_figure_without_citable_source_fails_and_with_one_passes(self):
        item = [_item(1, "T", "A video said open models took sixty-two percent of tokens.", "B.", "C.")]
        rep = nl.parse_report(_report(item, ["1. https://www.youtube.com/watch?v=abc"]))
        errors, warnings, record = nl.audit_report(rep, resolve=False)
        self.assertEqual(len(errors), 1)
        self.assertIn("percentage with no tier A/B source", errors[0])
        self.assertEqual(record[0]["tiers"], ["D forum/UGC"])
        rep = nl.parse_report(_report(item, ["1. https://www.youtube.com/watch?v=abc",
                                             "1. https://openai.com/index/the-post"]))
        errors, warnings, record = nl.audit_report(rep, resolve=False)
        self.assertEqual(errors, [])
        self.assertTrue(record[0]["citable"])

    def test_item_without_figures_may_run_on_forum_sources(self):
        item = [_item(1, "T", "A thread on Hacker News argued about a benchmark.", "B.", "C.")]
        rep = nl.parse_report(_report(item, ["1. https://news.ycombinator.com/item?id=1"]))
        errors, warnings, _ = nl.audit_report(rep, resolve=False)
        self.assertEqual(errors, [])
        self.assertTrue(any("no figure may" in w for w in warnings))


class Gists(unittest.TestCase):
    def _write(self, rows) -> Path:
        d = Path(tempfile.mkdtemp())
        p = d / "gists.json"
        p.write_text(json.dumps(rows), encoding="utf-8")
        return p

    def test_clean_gists_trace_to_the_pull(self):
        p = self._write([{"happened": "A benchmark for research agents was posted",
                          "can_now": "Agents can be scored on a real research workflow",
                          "source": "https://news.ycombinator.com/item?id=49472820"}])
        self.assertEqual(nl.check_gists(p, PULL), [])

    def test_untraced_missing_and_leaky_gists_fail(self):
        p = self._write([
            {"happened": "Something", "can_now": "Something else", "source": "https://example.com/nowhere"},
            {"happened": "No source", "can_now": "At all"},
            {"happened": "Mail me at a@b.co", "can_now": "x", "source": "https://openai.com/index/introducing-a-thing"},
            {"happened": "See https://openai.com/x", "can_now": "x", "source": "https://openai.com/index/introducing-a-thing"},
        ])
        problems = nl.check_gists(p, PULL)
        self.assertTrue(any("not in the pull" in x for x in problems))
        self.assertTrue(any("no source" in x for x in problems))
        self.assertTrue(any("email address" in x for x in problems))
        self.assertTrue(any("carries a URL" in x for x in problems))

    def test_report_fence_counts_as_provenance(self):
        p = self._write([{"happened": "x", "can_now": "y", "source": "https://openai.com/index/introducing-a-thing"}])
        report = _report(GOOD_ITEMS, GOOD_SOURCES)
        self.assertEqual(nl.check_gists(p, None, report), [])

    def test_bad_shape(self):
        p = self._write([{"happened": "x"}])
        self.assertTrue(nl.check_gists(p, PULL)[0].startswith("gists file:"))


class Template(unittest.TestCase):
    def test_template_checks_clean_apart_from_placeholders(self):
        text = nl.template_text(date(2026, 9, 6), 3)
        rep = nl.parse_report(text)
        self.assertEqual(len(rep.items), 3)
        self.assertEqual(sorted(rep.sources), [1, 2, 3])
        errors, _ = nl.lint_report(rep)
        self.assertEqual(errors, [])
        self.assertIn("Sunday, September sixth, twenty twenty-six", text)

    def test_refuses_a_tracked_path(self):
        with self.assertRaises(SystemExit):
            nl.refuse_unless_ignored(nl.REPO / "docs" / "would-be-tracked.md")
        nl.refuse_unless_ignored(nl.REPORTS_DIR / "not-created.md")  # ignored: no raise


if __name__ == "__main__":
    unittest.main(verbosity=1)
