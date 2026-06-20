"""SCG-P6 VerbalSignified IMPLEMENTED — registry enforcement tests (P6-IMPL-*).

Narrow SCG-P6 implementation (2026-06-18). Advances ONLY P6_VERBAL_SIGNIFIED_ALONE
to IMPLEMENTED via `build_p6_implemented_registry`, atop the implemented P5 phase.

P7–P12 remain SPECIFIED; freeze stays ACTIVE for P7+; no P7 runtime;
`build_p11_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p5_implemented_registry,
    build_p6_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
    LAYER_ID_P7_COMPOSITION_READINESS,
)


def test_P6_IMPL_ADVANCE_01_p6_implemented():
    assert build_p6_implemented_registry().get(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE).status is LayerStatus.IMPLEMENTED


def test_P6_IMPL_ADVANCE_02_p0_p5_implemented_preserved():
    reg = build_p6_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5")
    )


def test_P6_IMPL_ADVANCE_03_p7_p12_remain_specified():
    reg = build_p6_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6")
    )


def test_P6_IMPL_ADVANCE_04_base_leaves_p6_specified():
    assert build_p5_implemented_registry().get(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE).status is LayerStatus.SPECIFIED


def test_P6_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p6_implemented_registry().all_layers())) == 19


def test_P6_IMPL_ADVANCE_06_only_p0_through_p6_implemented():
    reg = build_p6_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == {"SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6"}


# ─────────────────────────────────────────────────────────────────────────────
# Gate + no-P7
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_IMPL_GATE_01_origin_is_mufrad_word_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE)
    assert spec.origin.layer_id == "P5_MUFRAD_WORD_CONTRACTS"
    assert spec.origin.output_type == "MufradWordCandidate"


def test_P6_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P6_IMPL_NOFULL_02_no_p7_implemented_builder():
    assert not hasattr(MRS, "build_p11_implemented_registry")


def test_P6_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE, LayerStatus.IMPLEMENTED)


def test_P6_IMPL_NORUNTIME_02_p7_not_advanced_by_p6_builder():
    assert build_p6_implemented_registry().get(LAYER_ID_P7_COMPOSITION_READINESS).status is LayerStatus.SPECIFIED
