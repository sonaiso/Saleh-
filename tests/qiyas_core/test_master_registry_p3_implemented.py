"""SCG-P3 RootStemClosure IMPLEMENTED — registry enforcement tests (P3-IMPL-*).

Narrow SCG-P3 implementation (2026-06-18). Advances ONLY P3_ROOT_STEM_CLOSURE to
IMPLEMENTED via `build_p3_implemented_registry`, atop the implemented P2 phase.

P4–P12 remain SPECIFIED; freeze stays ACTIVE for P4+; no P4 runtime;
`build_p4_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p2_implemented_registry,
    build_p3_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P3_ROOT_STEM_CLOSURE,
    LAYER_ID_P4_JAMID_MUSHTAQ,
)


def test_P3_IMPL_ADVANCE_01_p3_implemented():
    assert build_p3_implemented_registry().get(LAYER_ID_P3_ROOT_STEM_CLOSURE).status is LayerStatus.IMPLEMENTED


def test_P3_IMPL_ADVANCE_02_p0_p1_p2_implemented_preserved():
    reg = build_p3_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in ("SCG-P0", "SCG-P1", "SCG-P2")
    )


def test_P3_IMPL_ADVANCE_03_p4_p12_remain_specified():
    reg = build_p3_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3")
    )


def test_P3_IMPL_ADVANCE_04_base_leaves_p3_specified():
    assert build_p2_implemented_registry().get(LAYER_ID_P3_ROOT_STEM_CLOSURE).status is LayerStatus.SPECIFIED


def test_P3_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p3_implemented_registry().all_layers())) == 19


def test_P3_IMPL_ADVANCE_06_only_p0_p1_p2_p3_implemented():
    reg = build_p3_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == {"SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3"}


# ─────────────────────────────────────────────────────────────────────────────
# Gate + no-P4
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_IMPL_GATE_01_origin_is_registry_projection_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P3_ROOT_STEM_CLOSURE)
    assert spec.origin.layer_id == "P2_REGISTRY_PROJECTION"
    assert spec.origin.output_type == "RegistryProjectionCandidate"


def test_P3_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P3_IMPL_NOFULL_02_no_p5_implemented_builder():
    # build_p4_implemented_registry is authorized as of SCG-P4 (2026-06-18).
    assert not hasattr(MRS, "build_p10_implemented_registry")


def test_P3_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P3_ROOT_STEM_CLOSURE, LayerStatus.IMPLEMENTED)


def test_P3_IMPL_NORUNTIME_02_p4_not_advanced_by_p3_builder():
    assert build_p3_implemented_registry().get(LAYER_ID_P4_JAMID_MUSHTAQ).status is LayerStatus.SPECIFIED
