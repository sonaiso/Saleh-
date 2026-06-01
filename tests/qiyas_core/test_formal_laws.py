"""
Tests for formal laws (Economy, MSL) — Gaps #9/#10 of ALGEBRAIC_FOUNDATION_CONTRACT.md.
"""

from qiyas_core.formal_laws import (
    CandidateItem,
    Economy,
    MSL,
    Licensed,
    Sufficient,
    EquivalentPurpose,
    simpler_than,
)


# ---------------------------------------------------------------------------
# Order relation tests
# ---------------------------------------------------------------------------

def test_simpler_than_by_complexity():
    """x < y iff x.complexity < y.complexity."""
    x = CandidateItem("x", complexity=1, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=2, licensed=True, sufficient=True)
    assert simpler_than(x, y)
    assert not simpler_than(y, x)


def test_simpler_than_equal_complexity():
    """Equal complexity → neither is simpler."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=3, licensed=True, sufficient=True)
    assert not simpler_than(x, y)
    assert not simpler_than(y, x)


def test_candidateitem_lt():
    """CandidateItem supports < operator."""
    x = CandidateItem("x", 1, True, True)
    y = CandidateItem("y", 2, True, True)
    assert x < y
    assert not y < x


# ---------------------------------------------------------------------------
# Predicates
# ---------------------------------------------------------------------------

def test_licensed_predicate_true():
    x = CandidateItem("x", 1, licensed=True, sufficient=False)
    assert Licensed(x, "purpose:P")


def test_licensed_predicate_false():
    x = CandidateItem("x", 1, licensed=False, sufficient=False)
    assert not Licensed(x, "purpose:P")


def test_sufficient_predicate_true():
    x = CandidateItem("x", 1, licensed=True, sufficient=True)
    assert Sufficient(x, "purpose:P")


def test_sufficient_predicate_false():
    x = CandidateItem("x", 1, licensed=True, sufficient=False)
    assert not Sufficient(x, "purpose:P")


def test_equivalent_purpose_both_sufficient():
    x = CandidateItem("x", 1, licensed=True, sufficient=True)
    y = CandidateItem("y", 2, licensed=True, sufficient=True)
    assert EquivalentPurpose(x, y, "P")


def test_equivalent_purpose_one_insufficient():
    x = CandidateItem("x", 1, licensed=True, sufficient=True)
    y = CandidateItem("y", 2, licensed=True, sufficient=False)
    assert not EquivalentPurpose(x, y, "P")


# ---------------------------------------------------------------------------
# Economy tests
# ---------------------------------------------------------------------------

def test_economy_true_when_no_simpler_licensed_equivalent():
    """Economy holds when x is the unique licensed sufficient candidate."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    candidates = [x]
    assert Economy(x, "P", candidates)


def test_economy_false_when_simpler_licensed_equivalent_exists():
    """Economy fails when a simpler licensed sufficient candidate y exists."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=1, licensed=True, sufficient=True)
    candidates = [x, y]
    assert not Economy(x, "P", candidates)
    # y itself is economical (no simpler candidate)
    assert Economy(y, "P", candidates)


def test_economy_true_when_simpler_candidate_not_licensed():
    """Economy holds if the simpler candidate is not licensed."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=1, licensed=False, sufficient=True)
    candidates = [x, y]
    assert Economy(x, "P", candidates)


def test_economy_true_when_simpler_candidate_not_sufficient():
    """Economy holds if the simpler candidate is not sufficient."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=1, licensed=True, sufficient=False)
    candidates = [x, y]
    assert Economy(x, "P", candidates)


def test_economy_ignores_self():
    """Economy compares against all candidates except x itself."""
    x = CandidateItem("x", complexity=1, licensed=True, sufficient=True)
    candidates = [x]
    assert Economy(x, "P", candidates)


# ---------------------------------------------------------------------------
# MSL tests
# ---------------------------------------------------------------------------

def test_msl_true_for_minimal_sufficient():
    """MSL holds for the unique licensed sufficient candidate."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    candidates = [x]
    assert MSL(x, "P", candidates)


def test_msl_false_when_not_licensed():
    """MSL fails when x is not licensed."""
    x = CandidateItem("x", complexity=3, licensed=False, sufficient=True)
    candidates = [x]
    assert not MSL(x, "P", candidates)


def test_msl_false_when_not_sufficient():
    """MSL fails when x is not sufficient."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=False)
    candidates = [x]
    assert not MSL(x, "P", candidates)


def test_msl_false_when_simpler_sufficient_exists():
    """MSL fails if a simpler sufficient candidate exists."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=1, licensed=True, sufficient=True)
    candidates = [x, y]
    assert not MSL(x, "P", candidates)
    # y is the MSL
    assert MSL(y, "P", candidates)


def test_msl_true_when_simpler_candidate_not_sufficient():
    """MSL holds when the simpler candidate is not sufficient."""
    x = CandidateItem("x", complexity=3, licensed=True, sufficient=True)
    y = CandidateItem("y", complexity=1, licensed=True, sufficient=False)
    candidates = [x, y]
    assert MSL(x, "P", candidates)


def test_economy_and_msl_consistent():
    """
    For the minimal element of a licensed+sufficient set:
    both Economy and MSL should hold.
    """
    a = CandidateItem("a", complexity=1, licensed=True, sufficient=True)
    b = CandidateItem("b", complexity=2, licensed=True, sufficient=True)
    c = CandidateItem("c", complexity=3, licensed=True, sufficient=True)
    candidates = [a, b, c]

    # Only 'a' is both economical and MSL
    assert Economy(a, "P", candidates)
    assert MSL(a, "P", candidates)

    assert not Economy(b, "P", candidates)
    assert not MSL(b, "P", candidates)

    assert not Economy(c, "P", candidates)
    assert not MSL(c, "P", candidates)
