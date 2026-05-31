"""Constitutional tests for SlotGeometry protocol."""

import pytest

from qiyas_core.slot.policies.difference import SlotDifferencePolicy
from tests.qiyas_core.constitutional_helpers import assert_slot_policy_disjoint


@pytest.mark.slot_geometry
@pytest.mark.constitution
class TestSlotGeometryConstitution:
    """Test that SlotGeometry implementations follow constitutional requirements."""

    def test_slot_difference_policy_disjoint_categories(self):
        """SlotDifferencePolicy categories must be disjoint"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a",),
            blocking_differences=("diff_b",),
            deferring_differences=("diff_c",),
            ranking_differences=("diff_d",),
            non_blocking_differences=("diff_e",),
        )

        # Should pass - all disjoint
        assert_slot_policy_disjoint(policy)

    def test_invalidating_and_blocking_cannot_overlap(self):
        """invalidating_differences ∩ blocking_differences = ∅"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a", "diff_b"),
            blocking_differences=("diff_b", "diff_c"),  # diff_b overlaps
            deferring_differences=(),
            ranking_differences=(),
            non_blocking_differences=(),
        )

        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)

    def test_invalidating_and_non_blocking_cannot_overlap(self):
        """invalidating_differences ∩ non_blocking_differences = ∅"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a",),
            blocking_differences=(),
            deferring_differences=(),
            ranking_differences=(),
            non_blocking_differences=("diff_a",),  # Overlap
        )

        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)

    def test_blocking_and_non_blocking_cannot_overlap(self):
        """blocking_differences ∩ non_blocking_differences = ∅"""
        policy = SlotDifferencePolicy(
            invalidating_differences=(),
            blocking_differences=("diff_a",),
            deferring_differences=(),
            ranking_differences=(),
            non_blocking_differences=("diff_a",),  # Overlap
        )

        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)

    def test_invalidating_and_deferring_cannot_overlap(self):
        """invalidating_differences ∩ deferring_differences = ∅"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a",),
            blocking_differences=(),
            deferring_differences=("diff_a",),  # Overlap
            ranking_differences=(),
            non_blocking_differences=(),
        )

        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)

    def test_all_categories_can_be_non_empty(self):
        """All categories can have values as long as they're disjoint"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a", "diff_b"),
            blocking_differences=("diff_c", "diff_d"),
            deferring_differences=("diff_e",),
            ranking_differences=("diff_f", "diff_g"),
            non_blocking_differences=("diff_h",),
        )

        # All categories populated, all disjoint - should pass
        assert_slot_policy_disjoint(policy)

    def test_empty_categories_allowed(self):
        """Empty categories are allowed"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a",),
            blocking_differences=(),  # Empty
            deferring_differences=(),  # Empty
            ranking_differences=(),  # Empty
            non_blocking_differences=(),  # Empty
        )

        # Should pass - empty categories don't overlap
        assert_slot_policy_disjoint(policy)

    def test_all_empty_categories_allowed(self):
        """All categories can be empty"""
        policy = SlotDifferencePolicy(
            invalidating_differences=(),
            blocking_differences=(),
            deferring_differences=(),
            ranking_differences=(),
            non_blocking_differences=(),
        )

        # Should pass
        assert_slot_policy_disjoint(policy)

    def test_multiple_overlaps_detected(self):
        """Multiple overlaps are detected"""
        policy = SlotDifferencePolicy(
            invalidating_differences=("diff_a", "diff_b"),
            blocking_differences=("diff_a",),  # Overlaps with invalidating
            deferring_differences=("diff_b",),  # Overlaps with invalidating
            ranking_differences=(),
            non_blocking_differences=(),
        )

        # Should detect overlap
        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)

    def test_ranking_and_non_blocking_cannot_overlap(self):
        """ranking_differences ∩ non_blocking_differences = ∅"""
        policy = SlotDifferencePolicy(
            invalidating_differences=(),
            blocking_differences=(),
            deferring_differences=(),
            ranking_differences=("diff_a",),
            non_blocking_differences=("diff_a",),  # Overlap
        )

        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)

    def test_deferring_and_blocking_cannot_overlap(self):
        """deferring_differences ∩ blocking_differences = ∅"""
        policy = SlotDifferencePolicy(
            invalidating_differences=(),
            blocking_differences=("diff_a",),
            deferring_differences=("diff_a",),  # Overlap
            ranking_differences=(),
            non_blocking_differences=(),
        )

        with pytest.raises(AssertionError, match="overlapping differences"):
            assert_slot_policy_disjoint(policy)
