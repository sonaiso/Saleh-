"""Constitutional tests for candidate boundary discipline."""

import pytest

from tests.qiyas_core.constitutional_helpers import assert_no_higher_outputs
from tests.qiyas_core.fixtures.candidates import (
    make_unicode_candidate,
    make_haraka_candidate,
    make_atomic_unit_candidate,
)


@pytest.mark.adapter
@pytest.mark.no_higher_outputs
@pytest.mark.constitution
class TestCandidateBoundaries:
    """Test that layers respect candidate type boundaries."""

    def test_atomic_unit_never_produces_syllable(self):
        """AtomicUnitCandidate layer must never produce SyllableCandidate"""
        candidates = [
            make_atomic_unit_candidate(candidate_id="atomic:1"),
            make_atomic_unit_candidate(candidate_id="atomic:2"),
        ]

        # Should not produce SyllableCandidate
        assert_no_higher_outputs(candidates, ["SyllableCandidate"])

    def test_atomic_unit_never_produces_word(self):
        """AtomicUnitCandidate layer must never produce WordCandidate"""
        candidates = [make_atomic_unit_candidate()]
        assert_no_higher_outputs(candidates, ["WordCandidate"])

    def test_atomic_unit_never_produces_meaning(self):
        """AtomicUnitCandidate layer must never produce MeaningCandidate"""
        candidates = [make_atomic_unit_candidate()]
        assert_no_higher_outputs(candidates, ["MeaningCandidate"])

    def test_haraka_never_produces_atomic_unit(self):
        """HarakaCandidate layer must never produce AtomicUnitCandidate"""
        candidates = [
            make_haraka_candidate(candidate_id="haraka:1"),
            make_haraka_candidate(candidate_id="haraka:2"),
        ]
        assert_no_higher_outputs(candidates, ["AtomicUnitCandidate"])

    def test_haraka_never_produces_syllable(self):
        """HarakaCandidate layer must never produce SyllableCandidate"""
        candidates = [make_haraka_candidate()]
        assert_no_higher_outputs(candidates, ["SyllableCandidate"])

    def test_unicode_never_produces_haraka(self):
        """UnicodeCandidate layer must never produce HarakaCandidate"""
        candidates = [
            make_unicode_candidate(candidate_id="unicode:1"),
            make_unicode_candidate(candidate_id="unicode:2"),
        ]
        assert_no_higher_outputs(candidates, ["HarakaCandidate"])

    def test_unicode_never_produces_atomic_unit(self):
        """UnicodeCandidate layer must never produce AtomicUnitCandidate"""
        candidates = [make_unicode_candidate()]
        assert_no_higher_outputs(candidates, ["AtomicUnitCandidate"])

    def test_no_layer_produces_hukm_candidate(self):
        """No current layer should produce HukmCandidate"""
        candidates = [
            make_unicode_candidate(),
            make_haraka_candidate(),
            make_atomic_unit_candidate(),
        ]
        assert_no_higher_outputs(candidates, ["HukmCandidate"])

    def test_no_layer_produces_reality_claim(self):
        """No current layer should produce RealityClaim"""
        candidates = [
            make_unicode_candidate(),
            make_haraka_candidate(),
            make_atomic_unit_candidate(),
        ]
        assert_no_higher_outputs(candidates, ["RealityClaim"])

    def test_no_layer_produces_final_meaning(self):
        """No current layer should produce FinalMeaning"""
        candidates = [
            make_unicode_candidate(),
            make_haraka_candidate(),
            make_atomic_unit_candidate(),
        ]
        assert_no_higher_outputs(candidates, ["FinalMeaning"])

    def test_multiple_forbidden_types_respected(self):
        """Layers must respect all forbidden output types"""
        candidates = [make_atomic_unit_candidate()]

        # AtomicUnit should not produce any of these
        forbidden_types = [
            "SyllableCandidate",
            "WordCandidate",
            "MeaningCandidate",
            "HukmCandidate",
            "RealityClaim",
            "FinalMeaning",
        ]
        assert_no_higher_outputs(candidates, forbidden_types)

    def test_boundary_violation_detection(self):
        """Helper correctly detects boundary violations"""
        # Create a candidate that violates boundary
        from qiyas_core.candidate import Candidate
        from qiyas_core.enums import CandidateStatus, EvidenceRank

        syllable_candidate = Candidate(
            candidate_id="syllable:1",
            candidate_type="SyllableCandidate",  # Forbidden type
            status=CandidateStatus.ACCEPTED,
            layer="AtomicUnitQiyas",  # Wrong layer for this type
            source_rule_id="rule:atomic",
            asl_id="اصل:1",
            far_id="فرع:1",
            identity_ids=("id:1",),
            rank=EvidenceRank.FORMAL_STRUCTURE,
            residuals=(),
            trace_ids=(),
            output_flags=frozenset(),
        )

        # Should raise AssertionError
        with pytest.raises(AssertionError, match="forbidden type"):
            assert_no_higher_outputs([syllable_candidate], ["SyllableCandidate"])
