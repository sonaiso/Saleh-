"""Tests for SlotGeometry protocol."""

from typing import Any

import pytest

from qiyas_core.enums import EvidenceRank
from qiyas_core.slot import (
    SlotBoundary,
    SlotCapability,
    SlotClosurePolicy,
    SlotDemand,
    SlotDifferencePolicy,
    SlotDirection,
    SlotEffectPolicy,
    SlotEvidenceProfile,
    SlotFailurePolicy,
    SlotGeometry,
    SlotRankPolicy,
    SlotResidualPolicy,
    SlotRoleSpec,
    SlotSpec,
    SlotState,
    SlotTracePolicy,
    SlotWadiPolicy,
)


class TestSlotGeometry:
    """Test implementation of SlotGeometry protocol."""

    def slots_for(self, context: dict[str, Any]) -> tuple[SlotSpec, ...]:
        """Return test slot specs."""
        return (
            SlotSpec(
                slot_id="test_slot_1",
                slot_family_id="test_family",
                slot_type="test_type",
                layer="TestLayer",
                domain="TestDomain",
                subdomain=None,
                boundary=SlotBoundary.INTRA_ATOMIC,
                direction=SlotDirection.INTERNAL,
                state=SlotState.OPEN,
                roles=(
                    SlotRoleSpec(
                        role_name="test_role",
                        required_type="TestCandidate",
                        required_capabilities=(),
                        optional_evidence=(),
                    ),
                ),
                demand=SlotDemand(
                    demand_type="test_demand",
                    required_evidence=(),
                    required_capabilities=(),
                    optional_evidence=(),
                ),
                capability=SlotCapability(
                    capability_type="test_capability",
                    provides_evidence=(),
                    satisfies_demands=(),
                ),
                evidence_profile=SlotEvidenceProfile(
                    rank_floor=EvidenceRank.FORMAL_STRUCTURE,
                    rank_ceiling=EvidenceRank.ANALOGICAL,
                    required_evidence_claims=(),
                    optional_evidence_claims=(),
                    evidence_merge_policy="min",
                ),
                wadi_policy=SlotWadiPolicy(
                    sabab_conditions=(),
                    shart_conditions=(),
                    mani_conditions=(),
                    sihha_conditions=(),
                    fasad_conditions=(),
                    butlan_conditions=(),
                ),
                difference_policy=SlotDifferencePolicy(
                    invalidating_differences=(),
                    blocking_differences=(),
                    deferring_differences=(),
                    ranking_differences=(),
                    non_blocking_differences=(),
                ),
                closure_policy=SlotClosurePolicy(
                    closure_type="internal",
                    requires_evidence=(),
                    deferred_if=(),
                    blocked_if=(),
                    closes_on=(),
                ),
                rank_policy=SlotRankPolicy(
                    minimum_required_rank=EvidenceRank.FORMAL_STRUCTURE,
                    rank_merge_strategy="min",
                    rank_degradation_factors=(),
                ),
                residual_policy=SlotResidualPolicy(
                    blocking_residuals=(),
                    deferring_residuals=(),
                    ranking_residuals=(),
                    opening_residuals=(),
                    evidence_request_residuals=(),
                ),
                effect_policy=SlotEffectPolicy(
                    on_success=(),
                    on_partial=(),
                    on_deferred=(),
                ),
                failure_policy=SlotFailurePolicy(
                    failure_strategy="defer",
                    fallback_slots=(),
                    propagate_failure=False,
                    create_residual=True,
                ),
                trace_policy=SlotTracePolicy(
                    preserve_input_trace=True,
                    add_slot_trace=True,
                    add_evidence_trace=True,
                    add_residual_trace=True,
                    trace_merge_strategy="append",
                ),
                depends_on_slots=(),
                opens_slots=(),
                blocks_slots=(),
                composes_with=(),
                required_context_keys=(),
                optional_context_keys=(),
                forbidden_outputs=(),
                output_candidate_type="TestCandidate",
            ),
        )


def test_slot_geometry_protocol():
    """Test that TestSlotGeometry implements SlotGeometry protocol."""
    geometry = TestSlotGeometry()
    slots = geometry.slots_for({})
    assert len(slots) == 1
    assert slots[0].slot_id == "test_slot_1"


def test_slot_geometry_returns_tuple():
    """Test that SlotGeometry.slots_for returns tuple."""
    geometry = TestSlotGeometry()
    slots = geometry.slots_for({})
    assert isinstance(slots, tuple)


def test_slot_geometry_does_not_produce_candidates():
    """Test that SlotGeometry does not produce CandidateSet.

    This is a documentation test - SlotGeometry protocol does not
    have methods that produce candidates. Only slots_for() is defined.
    """
    geometry = TestSlotGeometry()
    # Verify the protocol only has slots_for method
    # Other methods like build_request, produce_candidates should NOT exist
    assert hasattr(geometry, "slots_for")
    assert not hasattr(geometry, "build_request")
    assert not hasattr(geometry, "produce_candidates")
    assert not hasattr(geometry, "call_kernel")
