"""SCG-P5 MufradWord IMPLEMENTED — registry enforcement tests (P5-IMPL-*).

Narrow SCG-P5 implementation (2026-06-18). Advances ONLY P5_MUFRAD_WORD_CONTRACTS
to IMPLEMENTED via `build_p5_implemented_registry`, atop the implemented P4 phase.

P6–P12 remain SPECIFIED; freeze stays ACTIVE for P6+; no P6 runtime;
`build_p8_implemented_registry` remains absent.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p4_implemented_registry,
    build_p5_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
)


def test_P5_IMPL_ADVANCE_01_p5_implemented():
    assert build_p5_implemented_registry().get(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS).status is LayerStatus.IMPLEMENTED


def test_P5_IMPL_ADVANCE_02_p0_p4_implemented_preserved():
    reg = build_p5_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4")
    )


def test_P5_IMPL_ADVANCE_03_p6_p12_remain_specified():
    reg = build_p5_implemented_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5")
    )


def test_P5_IMPL_ADVANCE_04_base_leaves_p5_specified():
    assert build_p4_implemented_registry().get(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS).status is LayerStatus.SPECIFIED


def test_P5_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p5_implemented_registry().all_layers())) == 19


def test_P5_IMPL_ADVANCE_06_only_p0_through_p5_implemented():
    reg = build_p5_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == {"SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5"}


# ─────────────────────────────────────────────────────────────────────────────
# Gate + no-P6
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_IMPL_GATE_01_origin_is_jamid_mushtaq_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS)
    assert spec.origin.layer_id == "P4_JAMID_MUSHTAQ"
    assert spec.origin.output_type == "JamidMushtaqCandidate"


def test_P5_IMPL_NOFULL_01_no_full_p1_implemented_builder():
    assert not hasattr(MRS, "build_p1_implemented_registry")


def test_P5_IMPL_NOFULL_02_no_p6_implemented_builder():
    assert not hasattr(MRS, "build_p8_implemented_registry")


def test_P5_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS, LayerStatus.IMPLEMENTED)


def test_P5_IMPL_NORUNTIME_02_p6_not_advanced_by_p5_builder():
    assert build_p5_implemented_registry().get(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE).status is LayerStatus.SPECIFIED
