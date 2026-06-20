"""SCG-P9 SentenceGeometry IMPLEMENTED — registry enforcement tests (P9-IMPL-*).

Narrow SCG-P9 implementation (2026-06-20). Advances ONLY P9_SENTENCE_GEOMETRY to
IMPLEMENTED via `build_p9_implemented_registry`, atop the implemented P8 phase.

P10–P12 remain SPECIFIED; freeze stays ACTIVE above P9; no P10 runtime;
`build_p11_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p8_implemented_registry,
    build_p9_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P9_SENTENCE_GEOMETRY,
    LAYER_ID_P10_RELATION_GEOMETRY,
)

_IMPL_PHASES = ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5",
                "SCG-P6", "SCG-P7", "SCG-P8", "SCG-P9")


def test_P9_IMPL_ADVANCE_01_p9_implemented():
    assert build_p9_implemented_registry().get(LAYER_ID_P9_SENTENCE_GEOMETRY).status is LayerStatus.IMPLEMENTED


def test_P9_IMPL_ADVANCE_02_p0_p8_implemented_preserved():
    reg = build_p9_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in _IMPL_PHASES[:-1]  # P0..P8
    )


def test_P9_IMPL_ADVANCE_03_p10_p12_remain_specified():
    reg = build_p9_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in _IMPL_PHASES
    )


def test_P9_IMPL_ADVANCE_04_base_leaves_p9_specified():
    assert build_p8_implemented_registry().get(LAYER_ID_P9_SENTENCE_GEOMETRY).status is LayerStatus.SPECIFIED


def test_P9_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p9_implemented_registry().all_layers())) == 19


def test_P9_IMPL_ADVANCE_06_only_p0_through_p9_implemented():
    reg = build_p9_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == set(_IMPL_PHASES)


def test_P9_IMPL_GATE_01_origin_is_amil_mamul_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P9_SENTENCE_GEOMETRY)
    assert spec.origin.layer_id == "P8_AMIL_MAMUL"
    assert spec.origin.output_type == "AmilMamulCandidate"


def test_P9_IMPL_NOFULL_01_no_p10_implemented_builder():
    assert not hasattr(MRS, "build_p11_implemented_registry")


def test_P9_IMPL_FREEZE_01_freeze_active_above_p9():
    # No phase beyond P9 is IMPLEMENTED → the freeze for P10+ remains ACTIVE.
    reg = build_p9_implemented_registry()
    assert not any(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase not in _IMPL_PHASES
    )


def test_P9_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P9_SENTENCE_GEOMETRY, LayerStatus.IMPLEMENTED)


def test_P9_IMPL_NORUNTIME_02_p10_not_advanced_by_p9_builder():
    assert build_p9_implemented_registry().get(LAYER_ID_P10_RELATION_GEOMETRY).status is LayerStatus.SPECIFIED
