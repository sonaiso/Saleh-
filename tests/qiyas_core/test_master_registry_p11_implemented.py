"""SCG-P11 IrabGeometry IMPLEMENTED — registry enforcement tests (P11-IMPL-*).

Narrow SCG-P11 implementation (2026-06-20). Advances ONLY P11_IRAB_GEOMETRY to
IMPLEMENTED via `build_p11_implemented_registry`, atop the implemented P10 phase.

P12 remains SPECIFIED; freeze stays ACTIVE above P11; no P12 runtime;
`build_p13_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p10_implemented_registry,
    build_p11_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P11_IRAB_GEOMETRY,
    LAYER_ID_P12_IFADAH_SPEECH_FORCE,
)

_IMPL_PHASES = ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5",
                "SCG-P6", "SCG-P7", "SCG-P8", "SCG-P9", "SCG-P10", "SCG-P11")


def test_P11_IMPL_ADVANCE_01_p11_implemented():
    assert build_p11_implemented_registry().get(LAYER_ID_P11_IRAB_GEOMETRY).status is LayerStatus.IMPLEMENTED


def test_P11_IMPL_ADVANCE_02_p0_p10_implemented_preserved():
    reg = build_p11_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in _IMPL_PHASES[:-1]  # P0..P10
    )


def test_P11_IMPL_ADVANCE_03_p12_remains_specified():
    reg = build_p11_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in _IMPL_PHASES
    )


def test_P11_IMPL_ADVANCE_04_base_leaves_p11_specified():
    assert build_p10_implemented_registry().get(LAYER_ID_P11_IRAB_GEOMETRY).status is LayerStatus.SPECIFIED


def test_P11_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p11_implemented_registry().all_layers())) == 19


def test_P11_IMPL_ADVANCE_06_only_p0_through_p11_implemented():
    reg = build_p11_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == set(_IMPL_PHASES)


def test_P11_IMPL_GATE_01_origin_is_relation_geometry_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P11_IRAB_GEOMETRY)
    assert spec.origin.layer_id == "P10_RELATION_GEOMETRY"
    assert spec.origin.output_type == "RelationGeometryCandidate"


def test_P11_IMPL_NOFULL_01_no_p12_implemented_builder():
    assert not hasattr(MRS, "build_p13_implemented_registry")


def test_P11_IMPL_FREEZE_01_freeze_active_above_p11():
    # No phase beyond P11 is IMPLEMENTED → the freeze for P12 remains ACTIVE.
    reg = build_p11_implemented_registry()
    assert not any(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase not in _IMPL_PHASES
    )


def test_P11_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P11_IRAB_GEOMETRY, LayerStatus.IMPLEMENTED)


def test_P11_IMPL_NORUNTIME_02_p12_not_advanced_by_p11_builder():
    assert build_p11_implemented_registry().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE).status is LayerStatus.SPECIFIED
