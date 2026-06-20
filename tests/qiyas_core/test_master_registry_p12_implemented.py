"""SCG-P12 IfadahSpeechForce IMPLEMENTED — registry enforcement tests (P12-IMPL-*).

Narrow SCG-P12 implementation (2026-06-20). Advances ONLY P12_IFADAH_SPEECH_FORCE
to IMPLEMENTED via `build_p12_implemented_registry`, atop the implemented P11 phase.

P12 is the TERMINAL layer of the 19-layer SCG spine: there is no P13, no
`build_p13_implemented_registry`, and the structural spine is now fully implemented.
"""

from __future__ import annotations

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_p11_implemented_registry,
    build_p12_implemented_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P12_IFADAH_SPEECH_FORCE,
)

_IMPL_PHASES = tuple(f"SCG-P{i}" for i in range(13))  # P0..P12 — the full spine


def test_P12_IMPL_ADVANCE_01_p12_implemented():
    assert build_p12_implemented_registry().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE).status is LayerStatus.IMPLEMENTED


def test_P12_IMPL_ADVANCE_02_p0_p11_implemented_preserved():
    reg = build_p12_implemented_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED
        for s in reg.all_layers()
        if s.phase in _IMPL_PHASES[:-1]  # P0..P11
    )


def test_P12_IMPL_ADVANCE_03_whole_spine_implemented():
    reg = build_p12_implemented_registry()
    assert all(s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers())


def test_P12_IMPL_ADVANCE_04_base_leaves_p12_specified():
    assert build_p11_implemented_registry().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE).status is LayerStatus.SPECIFIED


def test_P12_IMPL_ADVANCE_05_layer_count_unchanged():
    assert len(list(build_p12_implemented_registry().all_layers())) == 19


def test_P12_IMPL_ADVANCE_06_only_p0_through_p12_implemented():
    reg = build_p12_implemented_registry()
    impl_phases = {s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED}
    assert impl_phases == set(_IMPL_PHASES)


def test_P12_IMPL_GATE_01_origin_is_irab_geometry_candidate():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
    assert spec.origin.layer_id == "P11_IRAB_GEOMETRY"
    assert spec.origin.output_type == "IrabGeometryCandidate"


def test_P12_IMPL_TERMINAL_01_opens_nothing():
    spec = MRS.build_master_registry_seed().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)
    assert spec.target_boundary_opens == ()
    assert spec.forbidden_direct_next_layer_ids == ()


def test_P12_IMPL_TERMINAL_02_no_p13_layer_id_exists():
    assert not any("P13" in name for name in dir(MRS) if name.startswith("LAYER_ID_"))


def test_P12_IMPL_NOFULL_01_no_p13_implemented_builder():
    assert not hasattr(MRS, "build_p13_implemented_registry")


def test_P12_IMPL_NORUNTIME_01_direct_planned_to_implemented_blocked_in_seed():
    seed = MRS.build_master_registry_seed()
    with pytest.raises(RegistryViolation):
        seed.update_status(LAYER_ID_P12_IFADAH_SPEECH_FORCE, LayerStatus.IMPLEMENTED)
