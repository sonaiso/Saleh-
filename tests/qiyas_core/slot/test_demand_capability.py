"""Tests for SlotDemand and SlotCapability."""

import pytest

from qiyas_core.slot import SlotCapability, SlotDemand


def test_slot_demand_creation():
    """Test creating a valid SlotDemand."""
    demand = SlotDemand(
        demand_type="carrier_mark_binding",
        required_evidence=("wasf:carrier_accepts_mark",),
        required_capabilities=("mark_bindable",),
        optional_evidence=("unicode:validated",),
    )
    assert demand.demand_type == "carrier_mark_binding"
    assert demand.required_evidence == ("wasf:carrier_accepts_mark",)
    assert demand.required_capabilities == ("mark_bindable",)
    assert demand.optional_evidence == ("unicode:validated",)


def test_slot_demand_requires_demand_type():
    """Test that demand_type is required."""
    with pytest.raises(ValueError, match="demand_type is required"):
        SlotDemand(
            demand_type="",
            required_evidence=(),
            required_capabilities=(),
            optional_evidence=(),
        )


def test_slot_capability_creation():
    """Test creating a valid SlotCapability."""
    capability = SlotCapability(
        capability_type="atomic_unit_ready",
        provides_evidence=("atomic:bound",),
        satisfies_demands=("syllable_building",),
    )
    assert capability.capability_type == "atomic_unit_ready"
    assert capability.provides_evidence == ("atomic:bound",)
    assert capability.satisfies_demands == ("syllable_building",)


def test_slot_capability_requires_capability_type():
    """Test that capability_type is required."""
    with pytest.raises(ValueError, match="capability_type is required"):
        SlotCapability(
            capability_type="",
            provides_evidence=(),
            satisfies_demands=(),
        )
