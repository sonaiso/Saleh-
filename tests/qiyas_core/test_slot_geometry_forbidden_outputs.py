"""Focused tests for SlotGeometry forbidden outputs centralization (PR #65).

Verifies that SLOT_GEOMETRY_SEED_RULE and SLOT_GEOMETRY_EXTEND_RULE still
forbid all 12 higher-layer outputs after centralization to forbidden_outputs.py.

Per PR #65 Micro Safety PR requirements:
- Both seed and extend rules must forbid the constitutional base (3 items)
- Both seed and extend rules must forbid 9 higher-layer outputs
- Total: 12 forbidden outputs per rule
- The centralized tuple must match the original local tuple exactly
"""

from qiyas_core.forbidden_outputs import CONSTITUTIONAL_BASE, FORBIDDEN_SLOT_GEOMETRY
from qiyas_core.rules.slot_geometry_rules import (
    SLOT_GEOMETRY_EXTEND_RULE,
    SLOT_GEOMETRY_SEED_RULE,
)


def test_slot_geometry_seed_rule_forbidden_outputs():
    """SLOT_GEOMETRY_SEED_RULE must reference centralized forbidden outputs."""
    assert SLOT_GEOMETRY_SEED_RULE.forbidden_outputs == FORBIDDEN_SLOT_GEOMETRY


def test_slot_geometry_extend_rule_forbidden_outputs():
    """SLOT_GEOMETRY_EXTEND_RULE must reference centralized forbidden outputs."""
    assert SLOT_GEOMETRY_EXTEND_RULE.forbidden_outputs == FORBIDDEN_SLOT_GEOMETRY


def test_forbidden_slot_geometry_contains_constitutional_base():
    """Centralized FORBIDDEN_SLOT_GEOMETRY must include constitutional base."""
    for item in CONSTITUTIONAL_BASE:
        assert item in FORBIDDEN_SLOT_GEOMETRY


def test_forbidden_slot_geometry_contains_all_twelve_outputs():
    """Centralized FORBIDDEN_SLOT_GEOMETRY must forbid all 12 higher-layer outputs.

    Constitutional base (3):
    - HukmCandidate
    - RealityClaim
    - FinalMeaning

    Higher-layer outputs (9):
    - FinalCaseJudgment
    - DalalahCandidate
    - WordCandidate
    - LafzCandidate
    - SentenceCandidate
    - ParagraphCandidate
    - DiscourseGeometryCandidate
    - TextGeometryCandidate
    - MinimalCompletionReadinessCandidate
    """
    required = {
        # Constitutional base
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
        # Higher-layer outputs
        "FinalCaseJudgment",
        "DalalahCandidate",
        "WordCandidate",
        "LafzCandidate",
        "SentenceCandidate",
        "ParagraphCandidate",
        "DiscourseGeometryCandidate",
        "TextGeometryCandidate",
        "MinimalCompletionReadinessCandidate",
    }
    for forbidden_output in required:
        assert forbidden_output in FORBIDDEN_SLOT_GEOMETRY


def test_forbidden_slot_geometry_exact_count():
    """Centralized FORBIDDEN_SLOT_GEOMETRY must contain exactly 12 items."""
    assert len(FORBIDDEN_SLOT_GEOMETRY) == 12
