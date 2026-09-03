#!/usr/bin/env python3
"""Unit tests for the Oracle's frame stage (#238). No model calls; nothing is dispatched.

    python3 .claude/skills/content-oracle/test_frame_stage.py
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import frame_stage as fs  # noqa: E402


class DeckParsing(unittest.TestCase):
    def setUp(self):
        self.natives, self.deck = fs.load_decks()

    def test_natives_are_the_three_ruled_lenses(self):
        self.assertEqual(sorted(self.natives), ["falsifier", "off-label", "studio"])
        for f in self.natives.values():
            self.assertTrue(f.persona and f.forcing and f.banned, f.id)
            self.assertFalse(f.wild)

    def test_creative_partner_deck_reads_with_the_same_parser(self):
        self.assertGreaterEqual(len(self.deck), 12)
        wild = sorted(f.id for f in self.deck.values() if f.wild)
        self.assertEqual(wild, ["alien-anthropologist", "inversion"])
        self.assertIn("story-spine", self.deck)
        self.assertEqual(self.deck["story-spine"].domain, "story / writing")
        self.assertNotIn("*(wild)*", self.deck["inversion"].persona)

    def test_card_carries_persona_forcing_and_ban(self):
        card = self.natives["falsifier"].card()
        self.assertIn("LENS: falsifier", card)
        self.assertIn("Forcing move:", card)
        self.assertIn("Banned:", card)


class Selection(unittest.TestCase):
    def setUp(self):
        self.natives, self.deck = fs.load_decks()

    def test_two_natives_one_foreign_one_wild(self):
        sel = fs.select_frames(self.natives, self.deck, date(2026, 9, 6))
        self.assertEqual(len(sel.natives), 2)
        self.assertTrue(all(f.id in self.natives for f in sel.natives))
        self.assertFalse(sel.foreign.wild)
        self.assertNotIn(sel.foreign.domain, fs.STORY_DOMAINS)
        self.assertTrue(sel.wild.wild)
        self.assertEqual(len(set(sel.ids)), 4)

    def test_rotation_changes_week_to_week(self):
        a = fs.select_frames(self.natives, self.deck, date(2026, 9, 6)).ids
        b = fs.select_frames(self.natives, self.deck, date(2026, 9, 13)).ids
        c = fs.select_frames(self.natives, self.deck, date(2026, 9, 20)).ids
        self.assertNotEqual(a, b)
        self.assertNotEqual(b, c)
        # deterministic: the same date picks the same four
        self.assertEqual(a, fs.select_frames(self.natives, self.deck, date(2026, 9, 6)).ids)

    def test_overrides_are_honoured_and_checked(self):
        sel = fs.select_frames(self.natives, self.deck, date(2026, 9, 6),
                               native_ids=["studio", "off-label"], foreign_id="pre-mortem",
                               wild_id="inversion")
        self.assertEqual(sel.ids, ["studio", "off-label", "pre-mortem", "inversion"])
        with self.assertRaises(ValueError):
            fs.select_frames(self.natives, self.deck, date(2026, 9, 6), native_ids=["studio"])
        with self.assertRaises(ValueError):
            fs.select_frames(self.natives, self.deck, date(2026, 9, 6), foreign_id="story-spine")
        with self.assertRaises(ValueError):
            fs.select_frames(self.natives, self.deck, date(2026, 9, 6), wild_id="pre-mortem")


class PayloadGuard(unittest.TestCase):
    CLEAN = (
        "- Rebuilt the Oracle's supply after week one produced only boring commit-shaped cards.\n"
        "- Wired a Sunday drift scan so retired instructions cannot quietly survive in live files.\n"
        "- Two machines; the laptop became the authoritative one for the private layer.\n"
    )

    def test_clean_summary_passes(self):
        self.assertEqual(fs.inspect_payload(self.CLEAN, [], []), [])

    def test_paths_identifiers_and_shas_are_refused(self):
        dirty = self.CLEAN + (
            "- see /Users/someone/notes.md\n"
            "- sidecar at ~/.creative-harness/partner-sessions/x.md\n"
            "- mail someone@example.com\n"
            "- commit 8d4ca474a fixed it\n"
        )
        problems = fs.inspect_payload(dirty, [], [])
        joined = "\n".join(problems)
        for name in ("absolute path", "sidecar path", "email address", "commit sha"):
            self.assertIn(name, joined)

    def test_verbatim_line_from_a_private_file_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            private = Path(tmp) / "2026-09-01.md"
            lifted = "I spent the whole evening arguing with the gate about a sentence it had not read."
            private.write_text(f"## Sessions\n\n{lifted}\n", encoding="utf-8")
            summary = self.CLEAN + f"- {lifted}\n"
            problems = fs.inspect_payload(summary, [], [private])
            self.assertTrue(any("verbatim" in p for p in problems), problems)
            self.assertEqual(fs.inspect_payload(self.CLEAN, [], [private]), [])

    def test_gists_are_checked_and_capped(self):
        bad = [fs.Gist("A lab shipped a thing; ping /Users/x", "does more")]
        self.assertTrue(any("gist 0: absolute path" in p for p in fs.inspect_payload(self.CLEAN, bad, [])))
        many = [fs.Gist(f"item {i}", "can") for i in range(fs.GIST_MAX_ITEMS + 1)]
        self.assertTrue(any("gists; cap" in p for p in fs.inspect_payload(self.CLEAN, many, [])))

    def test_oversized_summary_is_not_stripped(self):
        problems = fs.inspect_payload("x" * (fs.SUMMARY_MAX_CHARS + 1), [], [])
        self.assertTrue(any("not stripped" in p for p in problems))


class Prompts(unittest.TestCase):
    def test_payload_carries_lens_and_gist_lines_but_never_the_source(self):
        natives, _ = fs.load_decks()
        gists = [fs.Gist("A vendor released a model", "runs two-hour tasks", "https://example.com/post")]
        system, user = fs.build_prompts(natives["off-label"], "- a stripped week\n", gists)
        self.assertIn("LENS: off-label", system)
        self.assertIn("ANGLE <n> [off-label]", system)
        self.assertIn("A vendor released a model", user)
        self.assertIn("Can now: runs two-hour tasks", user)
        self.assertNotIn("example.com", user)
        self.assertNotIn("example.com", system)

    def test_no_gists_is_said_out_loud(self):
        natives, _ = fs.load_decks()
        _, user = fs.build_prompts(natives["studio"], "- a stripped week\n", [])
        self.assertIn("none supplied", user)


class Output(unittest.TestCase):
    def test_angles_count_only_when_stamped_with_own_lens(self):
        text = "ANGLE 1 [studio]\nExperiment: x\n\nANGLE 2 [studio]\nExperiment: y\n\nANGLE 3 [falsifier]\n"
        self.assertEqual(fs.count_angles(text, "studio"), 2)
        self.assertEqual(fs.count_angles(text, "off-label"), 0)

    def test_render_keeps_failed_slots_visible(self):
        natives, deck = fs.load_decks()
        sel = fs.select_frames(natives, deck, date(2026, 9, 6))
        results = [
            fs.GeneratorResult(sel.frames[0], True, text="ANGLE 1 [x]\nExperiment: a", cost_usd=0.05, angles=1),
            fs.GeneratorResult(sel.frames[1], False, error="exit 1"),
            fs.GeneratorResult(sel.frames[2], True, text="ANGLE 1 [y]\nExperiment: b", cost_usd=0.05, angles=1),
            fs.GeneratorResult(sel.frames[3], False, error="no ANGLE blocks", text="prose"),
        ]
        out = fs.render(sel, results, date(2026, 9, 6),
                        [fs.Gist("h", "c", "https://example.com/a")], "sonnet")
        self.assertIn("4 attempted, 2 returned", out)
        self.assertIn("FAILED SLOT: exit 1", out)
        self.assertIn("Returned text, unstamped:", out)
        self.assertIn("https://example.com/a", out)   # provocation sources belong on the card
        self.assertIn("Bank record stub", out)

    def test_dry_run_renders_the_exact_payload(self):
        natives, deck = fs.load_decks()
        sel = fs.select_frames(natives, deck, date(2026, 9, 6))
        out = fs.render_dry_run(sel, "- a stripped week\n", [])
        self.assertIn("nothing dispatched", out)
        self.assertIn("=== USER PAYLOAD", out)
        self.assertIn("a stripped week", out)


if __name__ == "__main__":
    unittest.main()
