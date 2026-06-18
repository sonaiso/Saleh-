"""SCG-P1 PR-2 sequence + position IMPLEMENTED — enforcement tests (P1-IMPL-*).

Narrow SCG-P1 PR-2 implementation authorization (2026-06-17). Advances ONLY
ConditionedTypedSequence then PositionCarrier from SPECIFIED to IMPLEMENTED via
`build_p1_sequence_position_implemented_registry`, atop the PR-1 atomic carriers.

Decisions encoded:
  - CTS = domain/layer name + evidence-family conformance (no new container, no
    LayerSpec output_type change, no schema change).
  - PositionCarrier consumes the CTS `PositionEvidence` and preserves
    `conditioned_sequence_identity` as canonical; the codepoint is trace/bridge only.

SlotCandidate stays SPECIFIED; Letter + Haraka stay IMPLEMENTED; P2-P12 stay
SPECIFIED (the spec spine is complete); freeze stays ACTIVE for everything else.
"""

from __future__ import annotations

import pytest

from qiyas_core.kernel import QiyasKernel
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.conditioned_typed_sequence_adapter import ConditionedTypedSequenceLayerAdapter
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.rules import conditioned_typed_sequence_rules as CTS_RULES
from qiyas_core.rule import QiyasRule
from qiyas_core.slot_geometry_core import (
    LayerStatus,
    build_p1_atomic_carriers_implemented_registry,
    build_p1_sequence_position_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)

_CTS_EVIDENCE_FAMILY = {
    "CarrierBindingCandidate",
    "PositionEvidence",
    "BoundaryEvidence",
    "ResidualPreservationEvidence",
}
_SEQUENCE_POSITION = (LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE, LAYER_ID_P1_POSITION_CARRIER)
_ATOMIC = (LAYER_ID_P1_LETTER_IDENTITY_CARRIER, LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)


def _cts_rules():
    return [v for v in vars(CTS_RULES).values() if isinstance(v, QiyasRule)]


def _make_position_evidence(codepoint: int, index: int = 0, length: int = 1):
    """Run the canonical TypedCodePoint -> ConditionedTypedSequence path to get a
    real PositionEvidence candidate."""
    kernel = QiyasKernel()
    typed = TypedCodePointLayerAdapter(kernel=kernel).classify_codepoint(codepoint)
    assert typed.accepted, "codepoint must classify as a LetterCodePoint"
    cts = ConditionedTypedSequenceLayerAdapter(kernel=kernel)
    ev = cts.prove_letter_position(typed.accepted[0], index=index, sequence_length=length)
    assert ev.accepted, "CTS must emit a PositionEvidence for a sequence letter"
    return ev.accepted[0]


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-ADVANCE
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_ADVANCE_01_cts_and_position_implemented():
    reg = build_p1_sequence_position_implemented_registry()
    for lid in _SEQUENCE_POSITION:
        assert reg.get(lid).status is LayerStatus.IMPLEMENTED, lid


def test_P1_IMPL_ADVANCE_02_atomic_carriers_still_implemented():
    reg = build_p1_sequence_position_implemented_registry()
    for lid in _ATOMIC:
        assert reg.get(lid).status is LayerStatus.IMPLEMENTED, lid


def test_P1_IMPL_ADVANCE_03_slot_remains_specified():
    reg = build_p1_sequence_position_implemented_registry()
    assert reg.get(LAYER_ID_P1_SLOT_CANDIDATE).status is LayerStatus.SPECIFIED


def test_P1_IMPL_ADVANCE_04_p2_p12_specified_p0_implemented():
    reg = build_p1_sequence_position_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1")
    )


def test_P1_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p1_sequence_position_implemented_registry().all_layers())) == 19


def test_P1_IMPL_ADVANCE_06_exactly_four_p1_layers_implemented():
    reg = build_p1_sequence_position_implemented_registry()
    impl_p1 = {s.id for s in reg.all_layers() if s.phase == "SCG-P1" and s.status is LayerStatus.IMPLEMENTED}
    assert impl_p1 == set(_ATOMIC) | set(_SEQUENCE_POSITION)


def test_P1_IMPL_ADVANCE_07_base_leaves_cts_position_specified():
    base = build_p1_atomic_carriers_implemented_registry()
    for lid in _SEQUENCE_POSITION:
        assert base.get(lid).status is LayerStatus.SPECIFIED, lid


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-GATE — dependency-gate ordering (CTS CROSS from P0; Position INTRA from CTS)
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_GATE_01_cts_origin_is_p0_typed_codepoint():
    reg = build_p1_sequence_position_implemented_registry()
    assert reg.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE).origin.layer_id == "P0_TYPED_CODEPOINT"


def test_P1_IMPL_GATE_02_position_origin_is_cts_intra():
    reg = build_p1_sequence_position_implemented_registry()
    pos = reg.get(LAYER_ID_P1_POSITION_CARRIER)
    assert pos.origin.layer_id == LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE
    # Both end IMPLEMENTED, proving CTS was implemented before Position (gate honored).
    assert reg.get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE).status is LayerStatus.IMPLEMENTED
    assert pos.status is LayerStatus.IMPLEMENTED


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-NOFULL
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_NOFULL_01_no_full_p1_or_p3_implemented_builders():
    # The slot-only partial (PR-3) and build_p2_implemented_registry (SCG-P2,
    # 2026-06-18) are authorized; only the FULL build_p1_implemented_registry and
    # any P3+ implemented builder remain forbidden.
    for name in (
        "build_p1_implemented_registry",
        "build_p3_implemented_registry",
    ):
        assert not hasattr(MRS, name), name


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-CTS-CONFORMANCE — domain name + evidence family (option a)
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_CTS_CONFORMANCE_01_rules_emit_only_evidence_family():
    rules = _cts_rules()
    assert rules, "CTS rules must be importable"
    for rule in rules:
        assert rule.output_candidate_type in _CTS_EVIDENCE_FAMILY, rule.output_candidate_type


def test_P1_IMPL_CTS_CONFORMANCE_02_no_literal_conditioned_typed_sequence_output():
    for rule in _cts_rules():
        assert rule.output_candidate_type != "ConditionedTypedSequence"


def test_P1_IMPL_CTS_CONFORMANCE_03_layerspec_output_type_unchanged():
    # Domain-name convention: the LayerSpec output_type stays "ConditionedTypedSequence"
    # (no schema/output_type change); the runtime emits the evidence family.
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE)
    assert spec.branch.output_type == "ConditionedTypedSequence"


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-POSITION-CONFORMANCE — consumes CTS PositionEvidence, preserves seq identity
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_POSITION_CONFORMANCE_01_consumes_cts_position_evidence():
    evidence = _make_position_evidence(0x0628, index=0, length=3)
    assert evidence.candidate_type == "PositionEvidence"
    result = PositionLayerAdapter(kernel=QiyasKernel()).prove_position(evidence, index=0)
    assert result.accepted, "PositionCarrier must be provable from CTS PositionEvidence"
    assert result.accepted[0].candidate_type == "PositionCarrier"


def test_P1_IMPL_POSITION_CONFORMANCE_02_preserves_conditioned_sequence_identity():
    evidence = _make_position_evidence(0x0628, index=0, length=3)
    c = PositionLayerAdapter(kernel=QiyasKernel()).prove_position(evidence, index=0).accepted[0]
    assert "identity:conditioned_typed_sequence_domain" in set(c.identity_ids)


def test_P1_IMPL_POSITION_CONFORMANCE_03_codepoint_is_trace_not_canonical_identity():
    evidence = _make_position_evidence(0x0628, index=0, length=3)
    c = PositionLayerAdapter(kernel=QiyasKernel()).prove_position(evidence, index=0).accepted[0]
    assert not any(iid.startswith("identity:codepoint:") for iid in c.identity_ids)
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_P1_IMPL_POSITION_CONFORMANCE_04_output_type_matches_layerspec():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P1_POSITION_CARRIER)
    assert spec.branch.output_type == "PositionCarrier"
    evidence = _make_position_evidence(0x0628)
    c = PositionLayerAdapter(kernel=QiyasKernel()).prove_position(evidence).accepted[0]
    assert c.candidate_type == spec.branch.output_type
