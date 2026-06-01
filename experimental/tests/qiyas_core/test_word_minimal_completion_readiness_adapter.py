"""
Tests for WordMinimalCompletionReadinessLayerAdapter.

Validates word minimal completion readiness enforces:
- Word completion requires WordInternalClosureReadinessCandidate
- Missing components block word completion
- No final WordCandidate is produced
- No forbidden outputs appear
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.word_minimal_completion_readiness_adapter import WordMinimalCompletionReadinessLayerAdapter


def test_word_completion_accepted_with_minimal_components():
    """Word minimal completion should be accepted when all minimal components are present."""
    kernel = QiyasKernel()
    adapter = WordMinimalCompletionReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        word_closure_readiness_candidate_id="word_closure_1",
        has_minimal_components=True,
        trace_prefix="test_word_complete"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "WordMinimalCompletionReadinessCandidate"
    assert candidate.layer == "WordMinimalCompletionReadinessQiyas"

    # Verify no forbidden outputs
    forbidden = {
        "SyllableCandidate", "LafzCandidate", "WordCandidate",
        "MeaningCandidate", "IfadahCandidate", "SyntaxCandidate",
        "RelationCandidate", "HukmCandidate", "RealityClaim", "FinalMeaning"
    }
    assert not (candidate.output_flags & forbidden)


def test_word_completion_blocked_with_missing_components():
    """Word minimal completion should be blocked when specific components are missing."""
    kernel = QiyasKernel()
    adapter = WordMinimalCompletionReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        word_closure_readiness_candidate_id="word_closure_1",
        has_minimal_components=False,
        missing_components=["root", "pattern"],
        trace_prefix="test_word_blocked"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "WordMinimalCompletionReadinessCandidate"


def test_word_completion_blocked_without_component_info():
    """Word minimal completion should be blocked when component info is unknown."""
    kernel = QiyasKernel()
    adapter = WordMinimalCompletionReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        word_closure_readiness_candidate_id="word_closure_1",
        has_minimal_components=False,
        missing_components=[],  # Unknown what's missing
        trace_prefix="test_word_blocked_unknown"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Blocked because required wasf/illah are missing
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "WordMinimalCompletionReadinessCandidate"


def test_word_completion_identity_trace_disjoint():
    """identity_ids and trace_ids must be disjoint."""
    kernel = QiyasKernel()
    adapter = WordMinimalCompletionReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        word_closure_readiness_candidate_id="word_closure_1",
        has_minimal_components=True,
        trace_prefix="test_disjoint"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]

    # identity_ids and trace_ids must be disjoint
    assert not (set(candidate.identity_ids) & set(candidate.trace_ids))


def test_word_completion_rank_does_not_exceed_form():
    """Rank should not exceed FORM for readiness layers."""
    from qiyas_core.enums import EvidenceRank
    kernel = QiyasKernel()
    adapter = WordMinimalCompletionReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        word_closure_readiness_candidate_id="word_closure_1",
        has_minimal_components=True,
        trace_prefix="test_rank"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE
