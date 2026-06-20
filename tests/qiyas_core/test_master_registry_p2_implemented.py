"""SCG-P2 RegistryProjection IMPLEMENTED — registry enforcement tests (P2-IMPL-*).

Narrow SCG-P2 implementation authorization (2026-06-18). Advances ONLY
P2_REGISTRY_PROJECTION from SPECIFIED to IMPLEMENTED via
`build_p2_implemented_registry`, atop the fully-implemented P1 phase.

P3–P12 remain SPECIFIED; freeze stays ACTIVE for P3+; no P3 runtime; no full
`build_p1_implemented_registry`.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p1_slot_implemented_registry,
    build_p2_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P2_REGISTRY_PROJECTION,
    LAYER_ID_P3_ROOT_STEM_CLOSURE,
)


def test_P2_IMPL_ADVANCE_01_p2_implemented():
    assert build_p2_implemented_registry().get(LAYER_ID_P2_REGISTRY_PROJECTION).status is LayerStatus.IMPLEMENTED


def test_P2_IMPL_ADVANCE_02_p0_p1_implemented_preserved():
    reg = build_p2_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in ("SCG-P0", "SCG-P1")
    )


def test_P2_IMPL_ADVANCE_03_p3_p12_remain_specified():
    reg = build_p2_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1", "SCG-P2")
    )


def test_P2_IMPL_ADVANCE_04_base_leaves_p2_specified():
    assert build_p1_slot_implemented_registry().get(LAYER_ID_P2_REGISTRY_PROJECTION).status is LayerStatus.SPECIFIED


def test_P2_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p2_implemented_registry().all_layers())) == 19


def test_P2_IMPL_ADVANCE_06_only_p0_p1_p2_implemented():
    reg = build_p2_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == {"SCG-P0", "SCG-P1", "SCG-P2"}


# ─────────────────────────────────────────────────────────────────────────────
# Gate + no-full-builder + no-P3
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_IMPL_GATE_01_origin_is_slot_candidate():
    assert MRS.build_master_registry_seed().get(LAYER_ID_P2_REGISTRY_PROJECTION).origin.layer_id == "P1_SLOT_CANDIDATE"


def test_P2_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P2_IMPL_NOFULL_02_no_p5_implemented_builder():
    # build_p3/build_p4_implemented_registry are authorized as of SCG-P3/P4.
    assert not hasattr(MRS, "build_p10_implemented_registry")


def test_P2_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    # In the seed, P2 is PLANNED; a direct jump to IMPLEMENTED is a lifecycle skip.
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED)


def test_P2_IMPL_NORUNTIME_02_p3_not_advanced_by_p2_builder():
    assert build_p2_implemented_registry().get(LAYER_ID_P3_ROOT_STEM_CLOSURE).status is LayerStatus.SPECIFIED
