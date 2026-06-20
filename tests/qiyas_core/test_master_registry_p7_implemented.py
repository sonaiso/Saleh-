"""SCG-P7 CompositionReadiness IMPLEMENTED — registry enforcement tests (P7-IMPL-*).

Narrow SCG-P7 implementation (2026-06-18). Advances ONLY P7_COMPOSITION_READINESS
to IMPLEMENTED via `build_p7_implemented_registry`, atop the implemented P6 phase.

P8–P12 remain SPECIFIED; freeze stays ACTIVE for P8+; no P8 runtime;
`build_p10_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p6_implemented_registry,
    build_p7_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P7_COMPOSITION_READINESS,
    LAYER_ID_P8_AMIL_MAMUL,
)


def test_P7_IMPL_ADVANCE_01_p7_implemented():
    assert build_p7_implemented_registry().get(LAYER_ID_P7_COMPOSITION_READINESS).status is LayerStatus.IMPLEMENTED


def test_P7_IMPL_ADVANCE_02_p0_p6_implemented_preserved():
    reg = build_p7_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6")
    )


def test_P7_IMPL_ADVANCE_03_p8_p12_remain_specified():
    reg = build_p7_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4",
                           "SCG-P5", "SCG-P6", "SCG-P7")
    )


def test_P7_IMPL_ADVANCE_04_base_leaves_p7_specified():
    assert build_p6_implemented_registry().get(LAYER_ID_P7_COMPOSITION_READINESS).status is LayerStatus.SPECIFIED


def test_P7_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p7_implemented_registry().all_layers())) == 19


def test_P7_IMPL_ADVANCE_06_only_p0_through_p7_implemented():
    reg = build_p7_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == {"SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4",
                           "SCG-P5", "SCG-P6", "SCG-P7"}


# ─────────────────────────────────────────────────────────────────────────────
# Gate + no-P8
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_IMPL_GATE_01_origin_is_verbal_signified_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P7_COMPOSITION_READINESS)
    assert spec.origin.layer_id == "P6_VERBAL_SIGNIFIED_ALONE"
    assert spec.origin.output_type == "VerbalSignifiedCandidate"


def test_P7_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P7_IMPL_NOFULL_02_no_p8_implemented_builder():
    assert not hasattr(MRS, "build_p10_implemented_registry")


def test_P7_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P7_COMPOSITION_READINESS, LayerStatus.IMPLEMENTED)


def test_P7_IMPL_NORUNTIME_02_p8_not_advanced_by_p7_builder():
    assert build_p7_implemented_registry().get(LAYER_ID_P8_AMIL_MAMUL).status is LayerStatus.SPECIFIED
