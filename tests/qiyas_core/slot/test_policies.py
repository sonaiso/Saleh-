"""Tests for slot policy dataclasses."""

import pytest

from qiyas_core.enums import EvidenceRank
from qiyas_core.slot.policies import (
    SlotClosurePolicy,
    SlotDifferencePolicy,
    SlotEffectPolicy,
    SlotEffectSpec,
    SlotEvidenceProfile,
    SlotFailurePolicy,
    SlotRankPolicy,
    SlotResidualPolicy,
    SlotTracePolicy,
    SlotWadiPolicy,
)


def test_slot_evidence_profile_creation():
    """Test creating SlotEvidenceProfile."""
    profile = SlotEvidenceProfile(
        rank_floor=EvidenceRank.FORM,
        rank_ceiling=EvidenceRank.QIYAS,
        required_evidence_claims=("claim1",),
        optional_evidence_claims=("claim2",),
        evidence_merge_policy="min",
    )
    assert profile.rank_floor == EvidenceRank.FORM
    assert profile.rank_ceiling == EvidenceRank.QIYAS
    assert profile.evidence_merge_policy == "min"


def test_slot_evidence_profile_rejects_invalid_rank_range():
    """Test that rank_floor cannot exceed rank_ceiling."""
    with pytest.raises(ValueError, match="rank_floor cannot exceed rank_ceiling"):
        SlotEvidenceProfile(
            rank_floor=EvidenceRank.QIYAS,
            rank_ceiling=EvidenceRank.FORM,
            required_evidence_claims=(),
            optional_evidence_claims=(),
            evidence_merge_policy="min",
        )


def test_slot_rank_policy_creation():
    """Test creating SlotRankPolicy."""
    policy = SlotRankPolicy(
        minimum_required_rank=EvidenceRank.FORM,
        rank_merge_strategy="min",
        rank_degradation_factors=("factor1",),
    )
    assert policy.minimum_required_rank == EvidenceRank.FORM
    assert policy.rank_merge_strategy == "min"


def test_slot_wadi_policy_creation():
    """Test creating SlotWadiPolicy."""
    policy = SlotWadiPolicy(
        sabab_conditions=("sabab1",),
        shart_conditions=("shart1",),
        mani_conditions=("mani1",),
        sihha_conditions=("sihha1",),
        fasad_conditions=("fasad1",),
        butlan_conditions=("butlan1",),
    )
    assert policy.sabab_conditions == ("sabab1",)
    assert policy.shart_conditions == ("shart1",)


def test_slot_difference_policy_creation():
    """Test creating SlotDifferencePolicy."""
    policy = SlotDifferencePolicy(
        invalidating_differences=("inv1",),
        blocking_differences=("block1",),
        deferring_differences=("defer1",),
        ranking_differences=("rank1",),
        non_blocking_differences=("allow1",),
    )
    assert policy.invalidating_differences == ("inv1",)
    assert policy.blocking_differences == ("block1",)


def test_slot_closure_policy_creation():
    """Test creating SlotClosurePolicy."""
    policy = SlotClosurePolicy(
        closure_type="internal",
        requires_evidence=("evidence1",),
        deferred_if=("condition1",),
        blocked_if=("blocker1",),
        closes_on=("trigger1",),
    )
    assert policy.closure_type == "internal"
    assert policy.requires_evidence == ("evidence1",)


def test_slot_closure_policy_requires_closure_type():
    """Test that closure_type is required."""
    with pytest.raises(ValueError, match="closure_type is required"):
        SlotClosurePolicy(
            closure_type="",
            requires_evidence=(),
            deferred_if=(),
            blocked_if=(),
            closes_on=(),
        )


def test_slot_residual_policy_creation():
    """Test creating SlotResidualPolicy."""
    policy = SlotResidualPolicy(
        blocking_residuals=("block1",),
        deferring_residuals=("defer1",),
        ranking_residuals=("rank1",),
        opening_residuals=("open1",),
        evidence_request_residuals=("request1",),
    )
    assert policy.blocking_residuals == ("block1",)
    assert policy.opening_residuals == ("open1",)


def test_slot_effect_spec_creation():
    """Test creating SlotEffectSpec."""
    effect = SlotEffectSpec(
        effect_type="close_slot",
        target="current_slot",
        conditions=("condition1",),
    )
    assert effect.effect_type == "close_slot"
    assert effect.target == "current_slot"


def test_slot_effect_policy_creation():
    """Test creating SlotEffectPolicy."""
    policy = SlotEffectPolicy(
        on_success=(
            SlotEffectSpec(
                effect_type="close",
                target="slot",
                conditions=(),
            ),
        ),
        on_partial=(),
        on_deferred=(),
    )
    assert len(policy.on_success) == 1
    assert policy.on_success[0].effect_type == "close"


def test_slot_failure_policy_creation():
    """Test creating SlotFailurePolicy."""
    policy = SlotFailurePolicy(
        failure_strategy="defer",
        fallback_slots=("slot1",),
        propagate_failure=False,
        create_residual=True,
    )
    assert policy.failure_strategy == "defer"
    assert policy.propagate_failure is False


def test_slot_failure_policy_requires_failure_strategy():
    """Test that failure_strategy is required."""
    with pytest.raises(ValueError, match="failure_strategy is required"):
        SlotFailurePolicy(
            failure_strategy="",
            fallback_slots=(),
            propagate_failure=False,
            create_residual=True,
        )


def test_slot_trace_policy_creation():
    """Test creating SlotTracePolicy."""
    policy = SlotTracePolicy(
        preserve_input_trace=True,
        add_slot_trace=True,
        add_evidence_trace=True,
        add_residual_trace=True,
        trace_merge_strategy="append",
    )
    assert policy.preserve_input_trace is True
    assert policy.trace_merge_strategy == "append"


def test_slot_trace_policy_requires_trace_merge_strategy():
    """Test that trace_merge_strategy is required."""
    with pytest.raises(ValueError, match="trace_merge_strategy is required"):
        SlotTracePolicy(
            preserve_input_trace=True,
            add_slot_trace=True,
            add_evidence_trace=True,
            add_residual_trace=True,
            trace_merge_strategy="",
        )
