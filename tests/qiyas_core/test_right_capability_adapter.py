"""
Tests for RightCapabilityLayerAdapter.

Validates right capability analysis enforces:
- Sukun allows continuation
- Short vowels allow continuation or closure
- Constitutional boundaries
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.right_capability_adapter import RightCapabilityLayerAdapter


def test_adapter_validates_sukun_continuation_capable():
    """Sukun should be continuation capable."""
    kernel = QiyasKernel()
    adapter = RightCapabilityLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x0652)  # Ba + Sukun

    assert result.layer == "RightCapabilityQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "RightCapabilityCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_adapter_validates_fatha_continuation_and_closure_capable():
    """Fatha should be both continuation and closure capable."""
    kernel = QiyasKernel()
    adapter = RightCapabilityLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E)  # Ba + Fatha

    assert result.layer == "RightCapabilityQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "RightCapabilityCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_right_capability_forbidden_outputs_enforced():
    """RightCapabilityCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = RightCapabilityLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E)

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


def test_right_capability_does_not_produce_syllable():
    """RightCapabilityCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = RightCapabilityLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E)

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "RightCapabilityCandidate must not produce SyllableCandidate"


def test_right_capability_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for right capability."""
    kernel = QiyasKernel()
    adapter = RightCapabilityLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E)

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"
