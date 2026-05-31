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
    """Order equilibrium should be validated when both left and right are accepted."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=True,
        left_demand_accepted=True, right_capability_accepted=True
    )  # Ba + Fatha

    assert result.layer == "SyllableOrderEquilibriumQiyas"
    assert len(result.accepted) == 1

    candidate = result.accepted[0]
    assert candidate.candidate_type == "SyllableOrderEquilibriumCandidate"
    assert candidate.status == CandidateStatus.ACCEPTED


def test_order_equilibrium_forbidden_outputs_enforced():
    """SyllableOrderEquilibriumCandidate must not produce forbidden outputs."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=True,
        left_demand_accepted=True, right_capability_accepted=True
    )

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

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=True,
        left_demand_accepted=True, right_capability_accepted=True
    )

    candidate = result.accepted[0]

    assert "SyllableCandidate" not in candidate.output_flags, \
        "SyllableOrderEquilibriumCandidate must not produce SyllableCandidate"


def test_order_equilibrium_identity_trace_separation():
    """Identity IDs and trace IDs must be disjoint for order equilibrium."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=True,
        left_demand_accepted=True, right_capability_accepted=True
    )

    candidate = result.accepted[0]
    identity_set = set(candidate.identity_ids)
    trace_set = set(candidate.trace_ids)

    assert identity_set.isdisjoint(trace_set), "identity_ids and trace_ids must be disjoint"


def test_order_equilibrium_blocked_when_left_demand_deferred():
    """Order equilibrium must be blocked when left demand is deferred."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=False,
        left_demand_accepted=False, right_capability_accepted=True
    )

    # Should still produce a candidate, but it will be blocked due to invalidating difference
    assert result.layer == "SyllableOrderEquilibriumQiyas"
    # The kernel will block this due to left_demand_unresolved invalidating difference
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableOrderEquilibriumCandidate"
    assert candidate.status == CandidateStatus.BLOCKED


def test_order_equilibrium_blocked_when_right_capability_deferred():
    """Order equilibrium must be blocked when right capability is deferred."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=True,
        left_demand_accepted=True, right_capability_accepted=False
    )

    # Should be blocked due to right_capability_unresolved invalidating difference
    assert result.layer == "SyllableOrderEquilibriumQiyas"
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableOrderEquilibriumCandidate"
    assert candidate.status == CandidateStatus.BLOCKED


def test_order_equilibrium_blocked_when_both_deferred():
    """Order equilibrium must be blocked when both left and right are deferred."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=False,
        left_demand_accepted=False, right_capability_accepted=False
    )

    # Should be blocked due to both left and right invalidating differences
    assert result.layer == "SyllableOrderEquilibriumQiyas"
    assert len(result.blocked) == 1

    candidate = result.blocked[0]
    assert candidate.candidate_type == "SyllableOrderEquilibriumCandidate"
    assert candidate.status == CandidateStatus.BLOCKED


def test_order_equilibrium_does_not_auto_prove_left_right_order_fit():
    """Order equilibrium must not prove left_right_order_fit automatically."""
    kernel = QiyasKernel()
    adapter = SyllableOrderEquilibriumLayerAdapter(kernel=kernel)

    # Without explicit acceptance, should not prove order fit
    result = adapter.process_validation(
        0x0628, 0x064E, is_initial_position=True,
        left_demand_accepted=False, right_capability_accepted=False
    )

    assert result.layer == "SyllableOrderEquilibriumQiyas"
    assert len(result.blocked) == 1

    # The blocked candidate should not have proven left_right_order_fit
    candidate = result.blocked[0]
    assert candidate.status == CandidateStatus.BLOCKED
