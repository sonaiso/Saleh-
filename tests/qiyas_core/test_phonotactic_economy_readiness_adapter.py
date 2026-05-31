"""
Tests for PhonotacticEconomyReadinessLayerAdapter.

Validates phonotactic economy readiness enforces:
- Minimal phonotactic economy satisfied
- No redundant structure
- Constitutional boundaries
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.phonotactic_economy_readiness_adapter import PhonotacticEconomyReadinessLayerAdapter


def test_adapter_validates_minimal_phonotactic_economy():
    """Minimal phonotactic economy should be validated."""
    kernel = QiyasKernel()
    adapter = PhonotacticEconomyReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)  # Ba + Fatha

    assert result.layer == "PhonotacticEconomyReadinessQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "PhonotacticEconomyReadinessCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_phonotactic_economy_forbidden_outputs_enforced():
    """PhonotacticEconomyReadinessCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = PhonotacticEconomyReadinessLayerAdapter(kernel=kernel)

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


def test_phonotactic_economy_does_not_produce_syllable():
    """PhonotacticEconomyReadinessCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = PhonotacticEconomyReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "PhonotacticEconomyReadinessCandidate must not produce SyllableCandidate"


def test_phonotactic_economy_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for phonotactic economy."""
    kernel = QiyasKernel()
    adapter = PhonotacticEconomyReadinessLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E)

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"
