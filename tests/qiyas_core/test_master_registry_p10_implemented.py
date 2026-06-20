"""SCG-P10 RelationGeometry IMPLEMENTED — registry enforcement tests (P10-IMPL-*).

Narrow SCG-P10 implementation (2026-06-20). Advances ONLY P10_RELATION_GEOMETRY to
IMPLEMENTED via `build_p10_implemented_registry`, atop the implemented P9 phase.

P11–P12 remain SPECIFIED; freeze stays ACTIVE above P10; no P11 runtime;
`build_p13_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p9_implemented_registry,
    build_p10_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P10_RELATION_GEOMETRY,
    LAYER_ID_P11_IRAB_GEOMETRY,
)

_IMPL_PHASES = ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5",
                "SCG-P6", "SCG-P7", "SCG-P8", "SCG-P9", "SCG-P10")


def test_P10_IMPL_ADVANCE_01_p10_implemented():
    assert build_p10_implemented_registry().get(LAYER_ID_P10_RELATION_GEOMETRY).status is LayerStatus.IMPLEMENTED


def test_P10_IMPL_ADVANCE_02_p0_p9_implemented_preserved():
    reg = build_p10_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in _IMPL_PHASES[:-1]  # P0..P9
    )


def test_P10_IMPL_ADVANCE_03_p11_p12_remain_specified():
    reg = build_p10_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in _IMPL_PHASES
    )


def test_P10_IMPL_ADVANCE_04_base_leaves_p10_specified():
    assert build_p9_implemented_registry().get(LAYER_ID_P10_RELATION_GEOMETRY).status is LayerStatus.SPECIFIED


def test_P10_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p10_implemented_registry().all_layers())) == 19


def test_P10_IMPL_ADVANCE_06_only_p0_through_p10_implemented():
    reg = build_p10_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == set(_IMPL_PHASES)


def test_P10_IMPL_GATE_01_origin_is_sentence_geometry_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P10_RELATION_GEOMETRY)
    assert spec.origin.layer_id == "P9_SENTENCE_GEOMETRY"
    assert spec.origin.output_type == "SentenceGeometryCandidate"


def test_P10_IMPL_NOFULL_01_no_p11_implemented_builder():
    assert not hasattr(MRS, "build_p13_implemented_registry")


def test_P10_IMPL_FREEZE_01_freeze_active_above_p10():
    # No phase beyond P10 is IMPLEMENTED → the freeze for P11+ remains ACTIVE.
    reg = build_p10_implemented_registry()
    assert not any(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase not in _IMPL_PHASES
    )


def test_P10_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P10_RELATION_GEOMETRY, LayerStatus.IMPLEMENTED)


def test_P10_IMPL_NORUNTIME_02_p11_not_advanced_by_p10_builder():
    assert build_p10_implemented_registry().get(LAYER_ID_P11_IRAB_GEOMETRY).status is LayerStatus.SPECIFIED
