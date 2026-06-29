from council.discovery.whitespace import _drop_rate, _sharpen_actions, whitespace_hero


def _hero(blind_spots, tier="standard", segment="dev", verified_count=5, dropped_count=1):
    return "\n".join(whitespace_hero(blind_spots=blind_spots, tier=tier, segment=segment,
                                     verified_count=verified_count, dropped_count=dropped_count))


def test_drop_rate_zero_denominator():
    assert _drop_rate(0, 0) == 0.0


def test_drop_rate_fraction():
    assert _drop_rate(4, 8) == 8 / 12


def test_rule1_backfill_present_iff_gaps():
    a = _sharpen_actions(has_gaps=True, n_gaps=3, tier="standard", segment="dev",
                         verified_count=5, dropped_count=1)
    assert any("Backfill the 3 gaps below" in x for x in a)
    b = _sharpen_actions(has_gaps=False, n_gaps=0, tier="standard", segment="dev",
                         verified_count=5, dropped_count=1)
    assert not any("Backfill the" in x for x in b)


def test_rule1_singular_gap():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=5, dropped_count=1)
    assert any("Backfill the 1 gap below" in x for x in a)


def test_rule2_segment_present_iff_empty():
    empty = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="",
                             verified_count=5, dropped_count=1)
    assert any("--segment" in x for x in empty)
    setseg = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                              verified_count=5, dropped_count=1)
    assert not any("--segment" in x for x in setseg)


def test_rule2_whitespace_only_segment_treated_as_empty():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="   ",
                         verified_count=5, dropped_count=1)
    assert any("--segment" in x for x in a)


def test_rule3_no_verified():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=0, dropped_count=3)
    assert any("nothing survived verification" in x for x in a)


def test_rule4_fires_at_50pct_not_deep():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=4, dropped_count=8)   # 67%
    assert any("Raise tier to `deep`" in x and "67%" in x for x in a)


def test_rule4_silent_below_threshold():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="standard", segment="dev",
                         verified_count=51, dropped_count=49)  # 49%
    assert not any("Raise tier" in x for x in a)


def test_rule4_silent_on_deep_tier():
    a = _sharpen_actions(has_gaps=True, n_gaps=1, tier="deep", segment="dev",
                         verified_count=1, dropped_count=9)   # 90% but already deep
    assert not any("Raise tier" in x for x in a)


def test_hero_heading_and_caveat_present():
    md = _hero(["no SSO talk"])
    assert "## ⭐ Whitespace Map — what this run MISSED" in md
    assert "absence-of-evidence" in md


def test_hero_per_gap_action_uniform_and_references_supplement():
    md = _hero(["no SSO talk", "no latency data"])
    assert "1. no SSO talk" in md and "2. no latency data" in md
    assert md.count("→ Backfill (agent WebSearch/WebFetch, solution-side)") == 2
    assert "Web Supplement (gap-fill)" in md


def test_hero_sharpen_list_renumbered_after_filtering():
    # segment set, verified>0, deep tier, low drop, gaps present → only rule 1 fires → "1."
    md = _hero(["g1"], tier="deep", segment="dev", verified_count=5, dropped_count=0)
    assert "**Sharpen the next run:**" in md
    assert "1. Backfill the 1 gap below" in md
    assert "2. " not in md.split("Gaps the panel")[0]  # no second sharpen item


def test_hero_no_sharpen_header_when_all_rules_silent():
    md = _hero([], tier="deep", segment="dev", verified_count=5, dropped_count=0)
    assert "**Sharpen the next run:**" not in md


def test_hero_empty_gaps_note():
    md = _hero([], tier="deep", segment="dev", verified_count=5, dropped_count=0)
    assert "No blind spots surfaced" in md
    assert "Backfill the" not in md


def test_hero_empty_gaps_still_fires_rules_2_4():
    # spec lines 121-122: no gaps → rule 1 omitted, but rules 2-4 still render if applicable
    md = _hero([], tier="standard", segment="", verified_count=0, dropped_count=5)  # 100% drop
    assert "No blind spots surfaced" in md
    assert "**Sharpen the next run:**" in md
    assert "Backfill the" not in md                       # rule 1 omitted (no gaps)
    assert "--segment" in md                              # rule 2
    assert "nothing survived verification" in md          # rule 3
    assert "Raise tier to `deep`" in md and "100%" in md  # rule 4
    assert "1. Add `--segment" in md                      # renumbered from 1 (no rule-1 line)


def test_hero_blank_gaps_filtered():
    md = _hero(["  ", "real gap"])
    assert "1. real gap" in md
    assert "2. " not in md.split("Gaps the panel")[1]  # only one real gap rendered
