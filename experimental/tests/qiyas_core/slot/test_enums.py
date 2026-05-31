"""Tests for SlotGeometry enums."""

import pytest

from qiyas_core.slot import (
    SlotAmbiguityPolicy,
    SlotBoundary,
    SlotDirection,
    SlotMultiplicity,
    SlotState,
)


def test_slot_direction_enum():
    """Test SlotDirection enum values."""
    assert SlotDirection.INTERNAL.value == "internal"
    assert SlotDirection.LEFT_TO_RIGHT.value == "left_to_right"
    assert SlotDirection.RIGHT_TO_LEFT.value == "right_to_left"
    assert SlotDirection.BIDIRECTIONAL.value == "bidirectional"
    assert SlotDirection.CONTEXTUAL.value == "contextual"


def test_slot_boundary_enum():
    """Test SlotBoundary enum values."""
    assert SlotBoundary.INTRA_ATOMIC.value == "intra_atomic"
    assert SlotBoundary.INTRA_LAFZ.value == "intra_lafz"
    assert SlotBoundary.INTRA_WORD.value == "intra_word"
    assert SlotBoundary.INTER_WORD.value == "inter_word"
    assert SlotBoundary.INTRA_COMPOSITION.value == "intra_composition"
    assert SlotBoundary.INTER_SENTENCE.value == "inter_sentence"
    assert SlotBoundary.MAQAM_CONTEXT.value == "maqam_context"


def test_slot_state_enum():
    """Test SlotState enum values."""
    assert SlotState.OPEN.value == "open"
    assert SlotState.PARTIAL.value == "partial"
    assert SlotState.FILLED.value == "filled"
    assert SlotState.DEFERRED.value == "deferred"
    assert SlotState.BLOCKED.value == "blocked"
    assert SlotState.CONFLICTED.value == "conflicted"
    assert SlotState.CLOSED.value == "closed"


def test_slot_multiplicity_enum():
    """Test SlotMultiplicity enum values."""
    assert SlotMultiplicity.SINGLE.value == "single"
    assert SlotMultiplicity.MULTIPLE.value == "multiple"


def test_slot_ambiguity_policy_enum():
    """Test SlotAmbiguityPolicy enum values."""
    assert SlotAmbiguityPolicy.DEFER.value == "defer"
    assert SlotAmbiguityPolicy.RANK.value == "rank"
    assert SlotAmbiguityPolicy.BLOCK.value == "block"
