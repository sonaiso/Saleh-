"""Tests for SlotRoleSpec."""

import pytest

from qiyas_core.slot import SlotRoleSpec


def test_slot_role_spec_creation():
    """Test creating a valid SlotRoleSpec."""
    role = SlotRoleSpec(
        role_name="carrier",
        required_type="UnicodeCandidate",
        required_capabilities=("accepts_mark",),
        optional_evidence=("unicode:validated",),
    )
    assert role.role_name == "carrier"
    assert role.required_type == "UnicodeCandidate"
    assert role.required_capabilities == ("accepts_mark",)
    assert role.optional_evidence == ("unicode:validated",)


def test_slot_role_spec_requires_role_name():
    """Test that role_name is required."""
    with pytest.raises(ValueError, match="role_name is required"):
        SlotRoleSpec(
            role_name="",
            required_type="UnicodeCandidate",
            required_capabilities=(),
            optional_evidence=(),
        )


def test_slot_role_spec_requires_required_type():
    """Test that required_type is required."""
    with pytest.raises(ValueError, match="required_type is required"):
        SlotRoleSpec(
            role_name="carrier",
            required_type="",
            required_capabilities=(),
            optional_evidence=(),
        )


def test_slot_role_spec_empty_capabilities():
    """Test SlotRoleSpec with empty capabilities."""
    role = SlotRoleSpec(
        role_name="mark",
        required_type="HarakaCandidate",
        required_capabilities=(),
        optional_evidence=(),
    )
    assert role.required_capabilities == ()
