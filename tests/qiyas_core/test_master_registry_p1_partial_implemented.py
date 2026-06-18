"""SCG-P1 PR-1 atomic-carriers IMPLEMENTED — enforcement tests (P1-IMPL-*).

Narrow SCG-P1 PR-1 implementation authorization (2026-06-17). Advances ONLY the
two atomic carriers — LetterIdentityCarrier (certify-and-wire as-is) and
HarakaMarkIdentityCarrier (canonical emit, legacy alias only) — from SPECIFIED to
IMPLEMENTED via `build_p1_atomic_carriers_implemented_registry`, through the
implementation-dependency gate (both are CROSS edges from a fully-IMPLEMENTED P0).

This is NOT a full P1 implementation: ConditionedTypedSequence, PositionCarrier,
and SlotCandidate remain SPECIFIED; P2-P12 remain PLANNED; freeze stays ACTIVE for
every layer except the two named atomic carriers.

Also pins runtime↔registry output-type CONFORMANCE for the two carriers.
"""

from __future__ import annotations

import pytest

from qiyas_core.kernel import QiyasKernel
from qiyas_core.letter_identity_adapter import LetterIdentityLayerAdapter
from qiyas_core.haraka_function_adapter import HarakaFunctionLayerAdapter
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter
from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p1_specified_registry,
    build_p1_atomic_carriers_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P1_LETTER_IDENTITY_CARRIER,
    LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER,
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)

_ATOMIC = (LAYER_ID_P1_LETTER_IDENTITY_CARRIER, LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER)
_REMAINING_P1 = (
    LAYER_ID_P1_CONDITIONED_TYPED_SEQUENCE,
    LAYER_ID_P1_POSITION_CARRIER,
    LAYER_ID_P1_SLOT_CANDIDATE,
)


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-ADVANCE — only the two atomic carriers reach IMPLEMENTED
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_ADVANCE_01_letter_and_haraka_implemented():
    reg = build_p1_atomic_carriers_implemented_registry()
    for lid in _ATOMIC:
        assert reg.get(lid).status is LayerStatus.IMPLEMENTED, lid


def test_P1_IMPL_ADVANCE_02_cts_position_slot_remain_specified():
    reg = build_p1_atomic_carriers_implemented_registry()
    for lid in _REMAINING_P1:
        assert reg.get(lid).status is LayerStatus.SPECIFIED, lid


def test_P1_IMPL_ADVANCE_03_p0_implemented_p2_p12_specified():
    # The implemented-registry builders sit atop the completed spec spine
    # (build_p12_specified_registry), so P2-P12 are SPECIFIED, not PLANNED.
    reg = build_p1_atomic_carriers_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1")
    )


def test_P1_IMPL_ADVANCE_04_layer_count_unchanged():
    assert len(list(build_p1_atomic_carriers_implemented_registry().all_layers())) == 19


def test_P1_IMPL_ADVANCE_05_only_p0_and_two_carriers_implemented():
    reg = build_p1_atomic_carriers_implemented_registry()
    implemented = {s.id for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    p0_ids = {s.id for s in reg.all_layers() if s.phase == "SCG-P0"}
    assert implemented == p0_ids | set(_ATOMIC)


def test_P1_IMPL_ADVANCE_06_base_and_specified_leave_carriers_below_implemented():
    # In the seed everything is PLANNED; in p1_specified the carriers are SPECIFIED.
    assert all(
        build_master_registry_seed().get(lid).status is LayerStatus.PLANNED for lid in _ATOMIC
    )
    assert all(
        build_p1_specified_registry().get(lid).status is LayerStatus.SPECIFIED for lid in _ATOMIC
    )


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-GATE — dependency gate honored (CROSS from a fully-IMPLEMENTED P0)
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_GATE_01_carriers_origin_is_p0_typed_codepoint():
    reg = build_master_registry_seed()
    for lid in _ATOMIC:
        assert reg.get(lid).origin.layer_id == "P0_TYPED_CODEPOINT"


def test_P1_IMPL_GATE_02_planned_to_implemented_still_blocked():
    # Lifecycle skip remains forbidden: from the seed (PLANNED) a direct jump raises.
    reg = build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P1_LETTER_IDENTITY_CARRIER, LayerStatus.IMPLEMENTED)


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-NOFULL — no full P1 implemented builder, no CTS/Position/Slot impl
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P1_IMPL_NOFULL_02_no_downstream_implemented_builders():
    # NOTE: build_p1_slot_implemented_registry is authorized as of SCG-P1 PR-3
    # (slot-only partial); it is intentionally NOT listed as forbidden here.
    # build_p2_implemented_registry is authorized as of SCG-P2 (2026-06-18).
    for name in (
        "build_p1_conditioned_typed_sequence_implemented_registry",
        "build_p1_position_implemented_registry",
        "build_p6_implemented_registry",
    ):
        assert not hasattr(MRS, name), name


# ─────────────────────────────────────────────────────────────────────────────
# P1-IMPL-CONFORMANCE — runtime emitted output_type == registry LayerSpec output
# ─────────────────────────────────────────────────────────────────────────────


def test_P1_IMPL_CONFORMANCE_01_letter_runtime_matches_layerspec():
    reg = build_master_registry_seed()
    expected = reg.get(LAYER_ID_P1_LETTER_IDENTITY_CARRIER).branch.output_type
    assert expected == "LetterIdentityCarrier"
    # Constitutional path: codepoint -> TypedCodePoint(LetterCodePoint) -> LetterIdentityCarrier.
    kernel = QiyasKernel()
    typed = TypedCodePointLayerAdapter(kernel=kernel).classify_codepoint(0x0628)
    assert typed.accepted, "BAA must classify as a LetterCodePoint"
    result = LetterIdentityLayerAdapter(kernel=kernel).process_letter_codepoint(typed.accepted[0])
    assert result.accepted, "BAA must yield a LetterIdentityCarrier"
    assert result.accepted[0].candidate_type == expected


def test_P1_IMPL_CONFORMANCE_02_haraka_runtime_matches_layerspec_canonical():
    reg = build_master_registry_seed()
    expected = reg.get(LAYER_ID_P1_HARAKA_MARK_IDENTITY_CARRIER).branch.output_type
    assert expected == "HarakaMarkIdentityCarrier"
    result = HarakaFunctionLayerAdapter(kernel=QiyasKernel()).prove_from_codepoint(0x064E)
    assert result.accepted, "FATHA must yield a HarakaMarkIdentityCarrier"
    assert result.accepted[0].candidate_type == expected


def test_P1_IMPL_CONFORMANCE_03_haraka_runtime_not_legacy_alias():
    result = HarakaFunctionLayerAdapter(kernel=QiyasKernel()).prove_from_codepoint(0x064E)
    assert result.accepted[0].candidate_type != "HarakaFunctionCarrier"
