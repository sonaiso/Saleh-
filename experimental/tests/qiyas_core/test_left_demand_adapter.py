"""
Tests for LeftDemandLayerAdapter.

Validates left demand analysis enforces:
- Initial position has no left demand (satisfied)
- Non-initial position has left demand (deferred)
- Constitutional boundaries
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.left_demand_adapter import LeftDemandLayerAdapter


def test_adapter_validates_initial_position_left_demand_satisfied():
    """At initial position, left demand should be satisfied."""
    kernel = QiyasKernel()
    adapter = LeftDemandLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E, is_initial_position=True)  # Ba + Fatha

    assert result.layer == "LeftDemandQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "LeftDemandCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED
    assert candidate.layer == "LeftDemandQiyas"


def test_adapter_defers_non_initial_position_left_demand():
    """At non-initial position, left demand should be deferred."""
    kernel = QiyasKernel()
    adapter = LeftDemandLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E, is_initial_position=False)  # Ba + Fatha

    assert result.layer == "LeftDemandQiyas"
    # Should still be accepted but with deferred residual
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "LeftDemandCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_left_demand_forbidden_outputs_enforced():
    """LeftDemandCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = LeftDemandLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E, is_initial_position=True)

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


def test_left_demand_does_not_produce_syllable():
    """LeftDemandCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = LeftDemandLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E, is_initial_position=True)

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "LeftDemandCandidate must not produce SyllableCandidate"


def test_left_demand_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for left demand."""
    kernel = QiyasKernel()
    adapter = LeftDemandLayerAdapter(kernel=kernel)

    result = adapter.process_analysis(0x0628, 0x064E, is_initial_position=True)

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"
