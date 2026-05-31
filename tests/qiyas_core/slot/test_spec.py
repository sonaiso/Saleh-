"""Tests for SlotSpec aggregate."""

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
    SlotEffectSpec,
    SlotEvidenceProfile,
    SlotFailurePolicy,
    SlotRankPolicy,
    SlotResidualPolicy,
    SlotRoleSpec,
    SlotSpec,
    SlotState,
    SlotTracePolicy,
    SlotWadiPolicy,
)


def create_minimal_slot_spec() -> SlotSpec:
    """Create a minimal valid SlotSpec for testing."""
    return SlotSpec(
        # Identity
        slot_id="test_slot",
        slot_family_id="test_family",
        slot_type="test_type",
        layer="TestLayer",
        domain="TestDomain",
        subdomain=None,
        # Geometry
        boundary=SlotBoundary.INTRA_ATOMIC,
        direction=SlotDirection.INTERNAL,
        state=SlotState.OPEN,
        # Roles
        roles=(
            SlotRoleSpec(
                role_name="test_role",
                required_type="TestCandidate",
                required_capabilities=(),
                optional_evidence=(),
            ),
        ),
        # Demand and Capability
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
        # Policies
        evidence_profile=SlotEvidenceProfile(
            rank_floor=EvidenceRank.FORM,
            rank_ceiling=EvidenceRank.QIYAS,
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
            minimum_required_rank=EvidenceRank.FORM,
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
        # Relationships
        depends_on_slots=(),
        opens_slots=(),
        blocks_slots=(),
        composes_with=(),
        # Context
        required_context_keys=(),
        optional_context_keys=(),
        # Outputs
        forbidden_outputs=(),
        output_candidate_type="TestCandidate",
    )


def test_slot_spec_creation():
    """Test creating a valid SlotSpec."""
    spec = create_minimal_slot_spec()
    assert spec.slot_id == "test_slot"
    assert spec.slot_family_id == "test_family"
    assert spec.slot_type == "test_type"
    assert spec.layer == "TestLayer"
    assert spec.domain == "TestDomain"
    assert spec.subdomain is None


def test_slot_spec_requires_slot_id():
    """Test that slot_id is required."""
    with pytest.raises(ValueError, match="slot_id is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["slot_id"] = ""
        SlotSpec(**spec_dict)


def test_slot_spec_requires_slot_family_id():
    """Test that slot_family_id is required."""
    with pytest.raises(ValueError, match="slot_family_id is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["slot_family_id"] = ""
        SlotSpec(**spec_dict)


def test_slot_spec_requires_slot_type():
    """Test that slot_type is required."""
    with pytest.raises(ValueError, match="slot_type is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["slot_type"] = ""
        SlotSpec(**spec_dict)


def test_slot_spec_requires_layer():
    """Test that layer is required."""
    with pytest.raises(ValueError, match="layer is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["layer"] = ""
        SlotSpec(**spec_dict)


def test_slot_spec_requires_domain():
    """Test that domain is required."""
    with pytest.raises(ValueError, match="domain is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["domain"] = ""
        SlotSpec(**spec_dict)


def test_slot_spec_requires_at_least_one_role():
    """Test that at least one role is required."""
    with pytest.raises(ValueError, match="At least one role is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["roles"] = ()
        SlotSpec(**spec_dict)


def test_slot_spec_requires_output_candidate_type():
    """Test that output_candidate_type is required."""
    with pytest.raises(ValueError, match="output_candidate_type is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["output_candidate_type"] = ""
        SlotSpec(**spec_dict)


def test_slot_spec_requires_forbidden_outputs():
    """Test that forbidden_outputs is required."""
    with pytest.raises(ValueError, match="forbidden_outputs is required"):
        spec_dict = create_minimal_slot_spec().__dict__.copy()
        spec_dict["forbidden_outputs"] = None
        SlotSpec(**spec_dict)


def test_slot_spec_preserves_depends_on_slots():
    """Test that depends_on_slots is preserved."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["depends_on_slots"] = ("slot1", "slot2")
    spec = SlotSpec(**spec_dict)
    assert spec.depends_on_slots == ("slot1", "slot2")


def test_slot_spec_preserves_opens_slots():
    """Test that opens_slots is preserved."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["opens_slots"] = ("slot3",)
    spec = SlotSpec(**spec_dict)
    assert spec.opens_slots == ("slot3",)


def test_slot_spec_preserves_blocks_slots():
    """Test that blocks_slots is preserved."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["blocks_slots"] = ("slot4", "slot5")
    spec = SlotSpec(**spec_dict)
    assert spec.blocks_slots == ("slot4", "slot5")


def test_slot_spec_preserves_composes_with():
    """Test that composes_with is preserved."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["composes_with"] = ("slot6",)
    spec = SlotSpec(**spec_dict)
    assert spec.composes_with == ("slot6",)


def test_slot_spec_with_subdomain():
    """Test SlotSpec with subdomain."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["subdomain"] = "TestSubdomain"
    spec = SlotSpec(**spec_dict)
    assert spec.subdomain == "TestSubdomain"


def test_slot_spec_with_multiple_roles():
    """Test SlotSpec with multiple roles."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["roles"] = (
        SlotRoleSpec(
            role_name="carrier",
            required_type="UnicodeCandidate",
            required_capabilities=(),
            optional_evidence=(),
        ),
        SlotRoleSpec(
            role_name="mark",
            required_type="HarakaCandidate",
            required_capabilities=(),
            optional_evidence=(),
        ),
    )
    spec = SlotSpec(**spec_dict)
    assert len(spec.roles) == 2
    assert spec.roles[0].role_name == "carrier"
    assert spec.roles[1].role_name == "mark"


def test_slot_spec_with_context_keys():
    """Test SlotSpec with context requirements."""
    spec_dict = create_minimal_slot_spec().__dict__.copy()
    spec_dict["required_context_keys"] = ("pause_state",)
    spec_dict["optional_context_keys"] = ("continuation_state",)
    spec = SlotSpec(**spec_dict)
    assert spec.required_context_keys == ("pause_state",)
    assert spec.optional_context_keys == ("continuation_state",)
