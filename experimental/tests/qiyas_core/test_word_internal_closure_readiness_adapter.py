"""
Tests for WordInternalClosureReadinessLayerAdapter.

Validates word internal closure readiness enforces:
- Word closure requires LafzInternalClosureReadinessCandidate evidence
- Missing lafz closure readiness blocks word closure
- Word boundary capability required for closure
- No final WordCandidate is produced
- No forbidden outputs appear
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.word_internal_closure_readiness_adapter import WordInternalClosureReadinessLayerAdapter


def test_word_closure_accepted_with_lafz_readiness():
    """Word internal closure should be accepted when lafz readiness and boundary evidence exists."""
    kernel = QiyasKernel()
    adapter = WordInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        lafz_closure_readiness_candidates=["lafz_closure_1", "lafz_closure_2"],
        has_word_boundary_capability=True,
        trace_prefix="test_word_1"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "WordInternalClosureReadinessCandidate"
    assert candidate.layer == "WordInternalClosureReadinessQiyas"

    # Verify no forbidden outputs
    forbidden = {
        "SyllableCandidate", "LafzCandidate", "WordCandidate",
        "MeaningCandidate", "IfadahCandidate", "SyntaxCandidate",
        "RelationCandidate", "HukmCandidate", "RealityClaim", "FinalMeaning"
    }
    assert not (candidate.output_flags & forbidden)


def test_word_closure_blocked_without_lafz_readiness():
    """Word internal closure should be blocked when lafz readiness is missing."""
    kernel = QiyasKernel()
    adapter = WordInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        lafz_closure_readiness_candidates=[],  # No lafz readiness
        has_word_boundary_capability=True,
        trace_prefix="test_word_blocked"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "WordInternalClosureReadinessCandidate"


def test_word_closure_blocked_without_boundary():
    """Word internal closure should be blocked when word boundary is not established."""
    kernel = QiyasKernel()
    adapter = WordInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        lafz_closure_readiness_candidates=["lafz_closure_1"],
        has_word_boundary_capability=False,  # No boundary capability
        trace_prefix="test_word_blocked_boundary"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Blocked because required wasf/illah are missing
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "WordInternalClosureReadinessCandidate"


def test_word_closure_identity_trace_disjoint():
    """identity_ids and trace_ids must be disjoint."""
    kernel = QiyasKernel()
    adapter = WordInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        lafz_closure_readiness_candidates=["lafz_closure_1"],
        has_word_boundary_capability=True,
        trace_prefix="test_disjoint"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]

    # identity_ids and trace_ids must be disjoint
    assert not (set(candidate.identity_ids) & set(candidate.trace_ids))


def test_word_closure_rank_does_not_exceed_form():
    """Rank should not exceed FORM for readiness layers."""
    from qiyas_core.enums import EvidenceRank
    kernel = QiyasKernel()
    adapter = WordInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        lafz_closure_readiness_candidates=["lafz_closure_1"],
        has_word_boundary_capability=True,
        trace_prefix="test_rank"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE
