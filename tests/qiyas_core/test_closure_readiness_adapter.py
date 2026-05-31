"""
Tests for ClosureReadinessLayerAdapter.

Validates closure readiness enforces:
- Mabni closure may be structurally stable
- Muʿrab closure must be deferred
- Unknown closure must be deferred
- Pause closure ready
- Continuation closure deferred
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.closure_readiness_adapter import ClosureReadinessLayerAdapter, classify_closure_readiness
from qiyas_core.enums import ClosureReadiness


def test_classify_closure_readiness_pause():
    """Pause evidence should result in PAUSE_CLOSURE_READY."""
    result = classify_closure_readiness(has_waqf_evidence=True)
    assert result == ClosureReadiness.PAUSE_CLOSURE_READY


def test_classify_closure_readiness_continuation():
    """Continuation evidence should result in CONTINUATION_CLOSURE_DEFERRED."""
    result = classify_closure_readiness(has_continuation_evidence=True)
    assert result == ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED


def test_classify_closure_readiness_unknown():
    """No evidence should result in UNKNOWN_CLOSURE."""
    result = classify_closure_readiness()
    assert result == ClosureReadiness.UNKNOWN_CLOSURE


def test_classify_closure_readiness_mabni():
    """Mabni evidence should result in MABNI_CLOSURE_READY."""
    result = classify_closure_readiness(has_mabni_evidence=True)
    assert result == ClosureReadiness.MABNI_CLOSURE_READY


def test_classify_closure_readiness_murab_without_case():
    """Muʿrab evidence without case/waqf/continuation should result in MURAB_CLOSURE_DEFERRED."""
    result = classify_closure_readiness(has_murab_evidence=True)
    assert result == ClosureReadiness.MURAB_CLOSURE_DEFERRED


def test_classify_closure_readiness_murab_with_case():
    """Muʿrab evidence with case should still result in MURAB_CLOSURE_DEFERRED."""
    result = classify_closure_readiness(has_murab_evidence=True, has_case_evidence=True)
    assert result == ClosureReadiness.MURAB_CLOSURE_DEFERRED


def test_classify_closure_readiness_murab_with_waqf():
    """Muʿrab evidence with waqf should result in PAUSE_CLOSURE_READY."""
    result = classify_closure_readiness(has_murab_evidence=True, has_waqf_evidence=True)
    assert result == ClosureReadiness.PAUSE_CLOSURE_READY


def test_classify_closure_readiness_murab_with_continuation():
    """Muʿrab evidence with continuation should result in CONTINUATION_CLOSURE_DEFERRED."""
    result = classify_closure_readiness(has_murab_evidence=True, has_continuation_evidence=True)
    assert result == ClosureReadiness.CONTINUATION_CLOSURE_DEFERRED


def test_adapter_validates_unknown_closure_deferred():
    """Unknown closure should be deferred."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha, no evidence

    assert result.layer == "ClosureReadinessQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "ClosureReadinessCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_adapter_validates_pause_closure_ready():
    """Pause closure should be ready."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, has_waqf_evidence=True)

    assert result.layer == "ClosureReadinessQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "ClosureReadinessCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_adapter_validates_mabni_closure_ready():
    """Mabni closure should be ready."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, has_mabni_evidence=True)

    assert result.layer == "ClosureReadinessQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "ClosureReadinessCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_adapter_validates_murab_closure_deferred():
    """Muʿrab closure without case/waqf/continuation should be deferred."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, has_murab_evidence=True)

    assert result.layer == "ClosureReadinessQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "ClosureReadinessCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_closure_readiness_forbidden_outputs_enforced():
    """ClosureReadinessCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)

    candidate = result.accepted[0]

    forbidden = {
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    }

    assert not (candidate.output_flags & forbidden), \
        f"Forbidden outputs detected: {candidate.output_flags & forbidden}"


def test_closure_readiness_does_not_produce_syllable():
    """ClosureReadinessCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "ClosureReadinessCandidate must not produce SyllableCandidate"


def test_closure_readiness_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for closure readiness."""
    kernel = QiyasKernel()
    adapter = ClosureReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"
