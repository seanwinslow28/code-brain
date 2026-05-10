"""Tests for structural_checks module."""
import pytest
from lib.skill_optimizer.structural_checks import (
    substack_format_intro,
    anti_pattern_overreference,
)


class TestSubstackFormatIntro:
    def test_passes_on_good_intro(self):
        text = (
            "I spent eleven months building Zapier workflows with the quiet "
            "devotion of a man assembling IKEA furniture — following instructions "
            "I half-understood, ignoring the leftover pieces, and telling myself "
            "it looked right enough. Each new automation felt like progress, even "
            "when half of them quietly broke at 2 AM and only surfaced when a "
            "coworker DMed me a screenshot of the pipeline alert. The kind of "
            "progress that compounds into shame.\n\n"
            "Thirty-seven zaps. Each one a small miracle of duct tape and prayer.\n\n"
            "Agents do."
        )
        passed, reason = substack_format_intro(text)
        assert passed is True, reason

    def test_fails_when_first_paragraph_too_short(self):
        text = "Short.\n\nSecond paragraph here is the real meat.\n\nClose."
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "first paragraph" in reason.lower()

    def test_fails_when_first_paragraph_too_long(self):
        long_para = " ".join(["word"] * 250) + "."
        text = f"{long_para}\n\nSecond.\n\nClose."
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "first paragraph" in reason.lower()

    def test_fails_when_no_paragraph_breaks(self):
        text = "One block of text without any paragraph breaks at all so it just runs on like this and never lets the reader breathe."
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "paragraph break" in reason.lower()

    def test_fails_when_closer_too_long(self):
        text = (
            "First paragraph here has enough words to clear the sixty word minimum "
            "threshold without trouble because we are padding it out intentionally "
            "to make the first paragraph rule pass for this test case here. We "
            "add a second sentence to push the count comfortably past sixty so "
            "the structural check moves on to evaluate the closer rule, which is "
            "what this particular test is actually trying to exercise here today.\n\n"
            "Second paragraph.\n\n"
            "This closing sentence is absolutely far too long to count as a Sean closer because it just keeps going and going past twelve words easily."
        )
        passed, reason = substack_format_intro(text)
        assert passed is False
        assert "closer" in reason.lower()


class TestAntiPatternOverreference:
    def test_passes_when_no_noun_overused(self):
        text = (
            "I sat down with my coffee and stared at the screen.\n\n"
            "The terminal blinked back at me.\n\n"
            "It was a Tuesday."
        )
        passed, reason = anti_pattern_overreference(text)
        assert passed is True, reason

    def test_fails_when_coffee_appears_three_times(self):
        text = (
            "I made coffee. Then more coffee. Then I drank the coffee.\n\n"
            "End scene."
        )
        passed, reason = anti_pattern_overreference(text)
        assert passed is False
        assert "coffee" in reason.lower()

    def test_passes_with_callback_pattern(self):
        # Opening word and closing callback may legitimately re-use an image.
        # The function should allow up to 2 instances; 2 instances pass.
        text = (
            "The ferry horn cut through the morning fog.\n\n"
            "Twelve paragraphs later, we are back to where we started.\n\n"
            "The ferry horn sounds the same as it always did."
        )
        passed, reason = anti_pattern_overreference(text)
        assert passed is True

    def test_case_insensitive(self):
        text = "Coffee and COFFEE and coffee."
        passed, reason = anti_pattern_overreference(text)
        assert passed is False
