"""
Tests for SyllableOrderEquilibriumLayerAdapter.

Validates syllable order equilibrium enforces:
- Left demand and right capability alignment
- Order equilibrium verification
- Constitutional boundaries
"""
from qiyas_core.enums import CandidateStatus
from qiyas_core.kernel import QiyasKernel
from qiyas_core.syllable_order_equilibrium_adapter import SyllableOrderEquilibriumLayerAdapter


def test_adapter_validates_order_equilibrium():
    """Order equilibrium should be validated."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, is_initial_position=True)  # Ba + Fatha

    assert result.layer == "SyllableOrderEquilibriumQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "SyllableOrderEquilibriumCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_order_equilibrium_forbidden_outputs_enforced():
    """SyllableOrderEquilibriumCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, is_initial_position=True)

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


def test_order_equilibrium_does_not_produce_syllable():
    """SyllableOrderEquilibriumCandidate must never produce SyllableCandidate."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, is_initial_position=True)

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "SyllableOrderEquilibriumCandidate must not produce SyllableCandidate"


def test_order_equilibrium_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for order equilibrium."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(0x0628, 0x064E, is_initial_position=True)

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"
