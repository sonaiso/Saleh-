"""Constitutional tests for identity and trace invariants."""

import pytest

from tests.qiyas_core.constitutional_helpers import (
    assert_disjoint_ids,
    assert_no_self_trace,
)
from tests.qiyas_core.fixtures.candidates import (
    make_unicode_candidate,
    make_haraka_candidate,
    make_atomic_unit_candidate,
    make_candidate_with_overlapping_ids,
)


@pytest.mark.identity_trace
@pytest.mark.constitution
class TestIdentityTraceInvariants:
    """Test that identity_ids and trace_ids follow constitutional rules."""

    def test_identity_and_trace_ids_are_disjoint(self):
        """identity_ids ∩ trace_ids must be empty"""
        candidates = [
            make_unicode_candidate(
                identity_ids=("id:u:1",),
                trace_ids=("id:ancestor:1",),
            ),
            make_haraka_candidate(
                identity_ids=("id:h:1",),
                trace_ids=("id:ancestor:2",),
            ),
            make_atomic_unit_candidate(
                identity_ids=("id:a:1",),
                trace_ids=("id:u:1", "id:h:1"),  # Different from own identity
            ),
        ]

        for candidate in candidates:
            assert_disjoint_ids(candidate)

    def test_no_self_trace(self):
        """Candidate's own identity_id must not appear in trace_ids"""
        candidate = make_unicode_candidate(
            identity_ids=("id:unicode:1",),
            trace_ids=("id:ancestor:1", "id:ancestor:2"),
        )
        assert_no_self_trace(candidate)

    def test_overlapping_ids_rejected(self):
        """Overlapping identity and trace IDs must be rejected"""
        # Attempting to create candidate with overlapping IDs should raise
        with pytest.raises(ValueError, match="identity_ids and trace_ids must be disjoint"):
            make_candidate_with_overlapping_ids(overlapping_id="id:overlap")

    def test_trace_ids_propagate_from_inputs(self):
        """trace_ids should include ancestor identity_ids"""
        # Create atomic unit with trace from unicode and haraka
        candidate = make_atomic_unit_candidate(
            identity_ids=("id:atomic:1",),
            trace_ids=("id:unicode:1", "id:haraka:1"),  # Ancestors
        )

        # Verify ancestors are in trace but not in identity
        assert "id:unicode:1" in candidate.trace_ids
        assert "id:haraka:1" in candidate.trace_ids
        assert "id:unicode:1" not in candidate.identity_ids
        assert "id:haraka:1" not in candidate.identity_ids

        assert_disjoint_ids(candidate)

    def test_identity_ids_not_empty_for_accepted_candidate(self):
        """Accepted candidates should have non-empty identity_ids"""
        from qiyas_core.enums import CandidateStatus

        candidate = make_unicode_candidate(
            status=CandidateStatus.ACCEPTED,
            identity_ids=("id:unicode:1",),
        )

        assert len(candidate.identity_ids) > 0

    def test_empty_trace_ids_allowed(self):
        """Empty trace_ids is valid for root candidates"""
        candidate = make_unicode_candidate(
            identity_ids=("id:unicode:1",),
            trace_ids=(),  # Empty - this is a root
        )

        assert_disjoint_ids(candidate)  # Should pass
        assert len(candidate.trace_ids) == 0

    def test_disjoint_assertion_catches_overlap(self):
        """Helper detects overlap between identity and trace"""
        # We can't actually create a candidate with overlap (it's blocked by __post_init__)
        # So we test that attempting to create one raises
        with pytest.raises(ValueError):
            make_candidate_with_overlapping_ids(overlapping_id="id:test")

    def test_multiple_identity_ids_all_disjoint_from_trace(self):
        """All identity_ids must be disjoint from all trace_ids"""
        candidate = make_atomic_unit_candidate(
            identity_ids=("id:atomic:1", "id:atomic:2"),
            trace_ids=("id:trace:1", "id:trace:2", "id:trace:3"),
        )

        assert_disjoint_ids(candidate)

        # Verify none of the identity IDs appear in trace
        for identity_id in candidate.identity_ids:
            assert identity_id not in candidate.trace_ids

    def test_trace_can_contain_multiple_ancestors(self):
        """trace_ids can contain multiple ancestor identities"""
        candidate = make_atomic_unit_candidate(
            identity_ids=("id:atomic:1",),
            trace_ids=(
                "id:unicode:1",
                "id:haraka:1",
                "id:input:1",
                "id:input:2",
            ),
        )

        assert len(candidate.trace_ids) == 4
        assert_disjoint_ids(candidate)

    def test_identity_not_in_own_trace(self):
        """A candidate's identity must not appear in its own trace"""
        candidate = make_unicode_candidate(
            identity_ids=("id:unicode:specific",),
            trace_ids=("id:other:1", "id:other:2"),
        )

        # Identity not in trace
        assert "id:unicode:specific" not in candidate.trace_ids
        assert_no_self_trace(candidate)
