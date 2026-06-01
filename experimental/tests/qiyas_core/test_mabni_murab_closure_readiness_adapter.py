"""
Tests for MabniMurabClosureReadinessLayerAdapter.

Validates mabni/muʿrab closure readiness enforces:
- Mabni readiness records stable internal form but defers external reference
- Muʿrab readiness defers governor/case dependency
- Conflicting mabni+murab evidence blocks
- No final meaning or case judgment is produced
- No forbidden outputs appear
"""
from qiyas_core.enums import CandidateStatus, ClosureReadiness
from qiyas_core.kernel import QiyasKernel
from qiyas_core.mabni_murab_closure_readiness_adapter import MabniMurabClosureReadinessLayerAdapter


def test_mabni_closure_defers_external_reference():
    """Mabni readiness should defer external reference/complement."""
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.MABNI_CLOSURE_READY,
        has_external_reference_evidence=False,
        has_complement_evidence=False,
        trace_prefix="test_mabni_defer"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Mabni should be DEFERRED if external reference is pending
    assert candidate.status == CandidateStatus.DEFERRED
    assert candidate.candidate_type == "MabniMurabClosureReadinessCandidate"
    assert candidate.layer == "MabniMurabClosureReadinessQiyas"

    # Verify no forbidden outputs
    forbidden = {
        "SyllableCandidate", "LafzCandidate", "WordCandidate",
        "MeaningCandidate", "IfadahCandidate", "SyntaxCandidate",
        "RelationCandidate", "HukmCandidate", "RealityClaim", "FinalMeaning"
    }
    assert not (candidate.output_flags & forbidden)


def test_mabni_closure_accepted_with_reference():
    """Mabni readiness should be accepted when reference/complement evidence exists."""
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.MABNI_CLOSURE_READY,
        has_external_reference_evidence=True,
        has_complement_evidence=True,
        trace_prefix="test_mabni_accept"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.candidate_type == "MabniMurabClosureReadinessCandidate"


def test_murab_closure_defers_governor():
    """Muʿrab readiness should defer governor dependency."""
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.MURAB_CLOSURE_DEFERRED,
        has_governor_evidence=False,
        has_case_position_evidence=False,
        trace_prefix="test_murab_defer"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Muʿrab should always be DEFERRED
    assert candidate.status == CandidateStatus.DEFERRED
    assert candidate.candidate_type == "MabniMurabClosureReadinessCandidate"


def test_murab_closure_still_deferred_with_governor():
    """Muʿrab readiness should remain deferred even with governor evidence."""
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.MURAB_CLOSURE_DEFERRED,
        has_governor_evidence=True,
        has_case_position_evidence=True,
        trace_prefix="test_murab_still_defer"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    # Muʿrab closure readiness must remain deferred
    assert candidate.status == CandidateStatus.DEFERRED
    assert candidate.candidate_type == "MabniMurabClosureReadinessCandidate"


def test_unknown_closure_blocks():
    """Unknown closure should be blocked."""
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.UNKNOWN_CLOSURE,
        trace_prefix="test_unknown_block"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == CandidateStatus.BLOCKED
    assert candidate.candidate_type == "MabniMurabClosureReadinessCandidate"


def test_mabni_murab_identity_trace_disjoint():
    """identity_ids and trace_ids must be disjoint."""
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.MABNI_CLOSURE_READY,
        has_external_reference_evidence=True,
        trace_prefix="test_disjoint"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]

    # identity_ids and trace_ids must be disjoint
    assert not (set(candidate.identity_ids) & set(candidate.trace_ids))


def test_mabni_murab_rank_does_not_exceed_form():
    """Rank should not exceed FORM for readiness layers."""
    from qiyas_core.enums import EvidenceRank
    kernel = QiyasKernel()
    adapter = MabniMurabClosureReadinessLayerAdapter(kernel)

    result = adapter.process_validation(
        closure_readiness=ClosureReadiness.MABNI_CLOSURE_READY,
        has_external_reference_evidence=True,
        trace_prefix="test_rank"
    )

    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.rank == EvidenceRank.FORMAL_STRUCTURE
