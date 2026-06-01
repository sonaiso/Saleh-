"""
Tests for LafzInternalClosureReadinessLayerAdapter.

Validates lafz internal closure readiness enforces:
- Lafz closure requires SyllableReadinessCandidate evidence (not SyllableCandidate)
- Missing syllable readiness blocks lafz closure
- Lafz order must be preserved for closure
- No final LafzCandidate is produced
- No forbidden outputs appear
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.lafz_internal_closure_readiness_adapter import LafzInternalClosureReadinessLayerAdapter


def test_lafz_closure_accepted_with_syllable_readiness():
    """Lafz internal closure should be accepted when syllable readiness and order evidence exists."""
    kernel = QiyasKernel()
    adapter = LafzInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        syllable_readiness_candidates=["syl_ready_1", "syl_ready_2"],
        closure_readiness_candidates=["closure_ready_1", "closure_ready_2"],
        has_syllable_order_equilibrium=True,
        has_phonotactic_economy=True,
        trace_prefix="test_lafz_1"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "LafzInternalClosureReadinessCandidate"
    assert candidate.layer == "LafzInternalClosureReadinessQiyas"

    # Verify no forbidden outputs
    forbidden = {
        "SyllableCandidate", "LafzCandidate", "WordCandidate",
        "MeaningCandidate", "IfadahCandidate", "SyntaxCandidate",
        "RelationCandidate", "HukmCandidate", "RealityClaim", "FinalMeaning"
    }
    assert not (candidate.output_flags & forbidden)


def test_lafz_closure_blocked_without_syllable_readiness():
    """Lafz internal closure should be blocked when syllable readiness is missing."""
    kernel = QiyasKernel()
    adapter = LafzInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        syllable_readiness_candidates=[],  # No syllable readiness
        closure_readiness_candidates=[],
        trace_prefix="test_lafz_blocked"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "LafzInternalClosureReadinessCandidate"


def test_lafz_closure_blocked_without_order():
    """Lafz internal closure should be blocked when syllable order is not established."""
    kernel = QiyasKernel()
    adapter = LafzInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        syllable_readiness_candidates=["syl_ready_1"],
        closure_readiness_candidates=["closure_ready_1"],
        has_syllable_order_equilibrium=False,  # No order equilibrium
        trace_prefix="test_lafz_blocked_order"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Blocked because required wasf internal_lafz_order_preserved is missing
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "LafzInternalClosureReadinessCandidate"


def test_lafz_closure_blocked_without_closure_readiness():
    """Lafz internal closure should be blocked when closure readiness is missing."""
    kernel = QiyasKernel()
    adapter = LafzInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        syllable_readiness_candidates=["syl_ready_1"],
        closure_readiness_candidates=[],  # No closure readiness
        has_syllable_order_equilibrium=True,
        trace_prefix="test_lafz_blocked_closure"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Blocked because required wasf/illah for closure are missing
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "LafzInternalClosureReadinessCandidate"


def test_lafz_closure_identity_trace_disjoint():
    """identity_ids and trace_ids must be disjoint."""
    kernel = QiyasKernel()
    adapter = LafzInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        syllable_readiness_candidates=["syl_ready_1"],
        closure_readiness_candidates=["closure_ready_1"],
        has_syllable_order_equilibrium=True,
        trace_prefix="test_disjoint"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]

    # identity_ids and trace_ids must be disjoint
    assert not (set(candidate.identity_ids) & set(candidate.trace_ids))


def test_lafz_closure_rank_does_not_exceed_form():
    """Rank should not exceed FORM for readiness layers."""
    from qiyas_core.enums import EvidenceRank
    kernel = QiyasKernel()
    adapter = LafzInternalClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        syllable_readiness_candidates=["syl_ready_1"],
        closure_readiness_candidates=["closure_ready_1"],
        has_syllable_order_equilibrium=True,
        trace_prefix="test_rank"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE
