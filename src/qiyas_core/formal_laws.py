"""
Formal Laws — Gaps #9/#10 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Economy(x, P):
  ¬∃y < x : Licensed(y, P) ∧ EquivalentPurpose(y, x, P)
  A candidate x is economical w.r.t. purpose P if no strictly simpler
  licensed candidate y exists that serves the same purpose.

MSL(x, P) — Minimal Sufficient Licensure:
  Licensed(x, P) ∧ Sufficient(x, P) ∧ ∀y < x : ¬Sufficient(y, P)
  x is minimally sufficient: it is licensed, it suffices for P, and
  no simpler licensed candidate also suffices.

Order relation (<):
  x < y  iff  x.complexity < y.complexity
  where complexity = number of non-empty fields proven in evidence
  (approximated here by candidate rank ordinal + residual count as tiebreaker).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol


# ---------------------------------------------------------------------------
# Protocols / type aliases
# ---------------------------------------------------------------------------

class HasComplexity(Protocol):
    """Any object that can be compared by complexity."""
    @property
    def complexity(self) -> int: ...


@dataclass(frozen=True)
class CandidateItem:
    """
    Lightweight candidate representation for formal-law testing.

    complexity: integer measure of candidate complexity (lower = simpler).
    licensed:   whether the candidate is licensed under purpose P.
    sufficient: whether the candidate is sufficient for purpose P.
    label:      human-readable identifier.
    """
    label: str
    complexity: int
    licensed: bool
    sufficient: bool

    def __lt__(self, other: CandidateItem) -> bool:
        return self.complexity < other.complexity

    def __le__(self, other: CandidateItem) -> bool:
        return self.complexity <= other.complexity


# ---------------------------------------------------------------------------
# Order relation
# ---------------------------------------------------------------------------

def simpler_than(x: CandidateItem, y: CandidateItem) -> bool:
    """
    Order relation: x < y  iff  x.complexity < y.complexity.

    This formalises the 'less complex' direction of the economy ordering.
    A smaller complexity value means x requires fewer proof obligations
    (fewer layers, fewer evidence items) than y.
    """
    return x.complexity < y.complexity


# ---------------------------------------------------------------------------
# Predicates
# ---------------------------------------------------------------------------

def Licensed(x: CandidateItem, purpose: str) -> bool:  # noqa: N802
    """
    Predicate: x is licensed under purpose P.

    In the formal model, 'licensed' means the candidate has passed through
    QiyasKernel.apply() and received CandidateStatus.ACCEPTED for the layer
    associated with purpose P.  Here we delegate to x.licensed.
    """
    return x.licensed


def Sufficient(x: CandidateItem, purpose: str) -> bool:  # noqa: N802
    """
    Predicate: x is sufficient for purpose P.

    'Sufficient' means x carries all proof obligations required by P —
    i.e. all wasf, illah, and wadi conditions for P are satisfied by x.
    Here we delegate to x.sufficient.
    """
    return x.sufficient


def EquivalentPurpose(  # noqa: N802
    x: CandidateItem,
    y: CandidateItem,
    purpose: str,
) -> bool:
    """
    Predicate: x and y serve the same purpose P.

    Two candidates serve the same purpose if both are licensed and
    sufficient for P.  In the full system this would compare their
    output_candidate_type and layer; here we use Sufficient as proxy.
    """
    return Sufficient(x, purpose) and Sufficient(y, purpose)


# ---------------------------------------------------------------------------
# Economy
# ---------------------------------------------------------------------------

def Economy(  # noqa: N802
    x: CandidateItem,
    purpose: str,
    candidates: list[CandidateItem],
) -> bool:
    """
    Economy(x, P) ⇔ ¬∃y < x : Licensed(y, P) ∧ EquivalentPurpose(y, x, P)

    Returns True iff no simpler licensed candidate y exists that serves
    the same purpose as x.

    Args:
        x:          The candidate under test.
        purpose:    The purpose string P.
        candidates: The full set of candidates (including x) to search.

    Returns:
        True if x is economical, False otherwise.
    """
    for y in candidates:
        if y is x:
            continue
        if simpler_than(y, x) and Licensed(y, purpose) and EquivalentPurpose(y, x, purpose):
            return False
    return True


# ---------------------------------------------------------------------------
# Minimal Sufficient Licensure
# ---------------------------------------------------------------------------

def MSL(  # noqa: N802
    x: CandidateItem,
    purpose: str,
    candidates: list[CandidateItem],
) -> bool:
    """
    MSL(x, P) ⇔ Licensed(x, P) ∧ Sufficient(x, P) ∧ ∀y < x : ¬Sufficient(y, P)

    Returns True iff x is minimally sufficient for P: licensed, sufficient,
    and no simpler candidate in candidates is also sufficient.

    Args:
        x:          The candidate under test.
        purpose:    The purpose string P.
        candidates: The full set of candidates (including x) to search.

    Returns:
        True if x is minimally sufficient, False otherwise.
    """
    if not Licensed(x, purpose):
        return False
    if not Sufficient(x, purpose):
        return False
    for y in candidates:
        if y is x:
            continue
        if simpler_than(y, x) and Sufficient(y, purpose):
            return False
    return True
