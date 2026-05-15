import pytest
from council.profiles import Profile, PROFILES, get_profile


def test_premium_profile_exists():
    p = get_profile("premium")
    assert p.name == "premium"
    assert len(p.models) == 4
    assert p.chairman  # non-empty
    assert p.max_cost_per_query > 0


def test_variance_profile_exists():
    p = get_profile("variance")
    assert p.name == "variance"
    assert len(p.models) == 4
    assert p.chairman
    assert p.max_cost_per_query > 0


def test_unknown_profile_raises():
    with pytest.raises(KeyError):
        get_profile("nonexistent")


def test_chairman_must_be_listed_in_models_or_distinct():
    for name in ("premium", "variance"):
        p = get_profile(name)
        # Chairman is either one of the four council models, OR a distinct fifth model.
        # Either is allowed; what's NOT allowed is an empty chairman.
        assert p.chairman != ""


def test_profile_max_cost_is_positive_float():
    for name in ("premium", "variance"):
        p = get_profile(name)
        assert isinstance(p.max_cost_per_query, float)
        assert p.max_cost_per_query > 0


def test_premium_more_expensive_than_variance():
    # Premium uses frontier models; variance mixes mid-tier. Caps should reflect this.
    assert get_profile("premium").max_cost_per_query >= get_profile("variance").max_cost_per_query
