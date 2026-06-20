"""SCG-P12 Ifadah Speech Force — SPEC-level enforcement tests (P12-SPEC-*).

Narrow SCG-P8–P12 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO reality claim, NO truth value, NO hukm, no final
meaning, no IMPLEMENTED status. Canonical SCG registry track only (NOT the
runtime syllable track). P12 is the TERMINAL phase of the canonical spine — it
opens no successor and never crosses into reality / truth / hukm.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p11_specified_registry,
    build_p12_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P12_IFADAH_SPEECH_FORCE,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "IFADAH_CONSTITUTION.md"


def _p12(registry):
    return registry.get(LAYER_ID_P12_IFADAH_SPEECH_FORCE)


# ─────────────────────────────────────────────────────────────────────────────
# P12-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P12_SPEC_ROW_01_row_exists():
    spec = _p12(build_master_registry_seed())
    assert spec.id == "P12_IFADAH_SPEECH_FORCE"
    assert spec.name == "IfadahSpeechForceLayer"
    assert spec.phase == "SCG-P12"


def test_P12_SPEC_ROW_02_output_type_is_ifadah_candidate_only():
    assert _p12(build_master_registry_seed()).branch.output_type == "IfadahCandidate"


def test_P12_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P12" in text and "IfadahCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P12-SPEC-STATUS — completes the canonical spine specification
# ─────────────────────────────────────────────────────────────────────────────


def test_P12_SPEC_STATUS_01_specified_via_builder():
    assert _p12(build_p12_specified_registry()).status is LayerStatus.SPECIFIED


def test_P12_SPEC_STATUS_02_base_and_p11_leave_p12_planned():
    assert _p12(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p12(build_p11_specified_registry()).status is LayerStatus.PLANNED


def test_P12_SPEC_STATUS_03_spine_specification_complete_p1_to_p12():
    reg = build_p12_specified_registry()
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase != "SCG-P0"
    )


def test_P12_SPEC_STATUS_04_only_p0_implemented_no_layer_beyond_p0():
    reg = build_p12_specified_registry()
    implemented = [s.phase for s in reg.all_layers() if s.status is LayerStatus.IMPLEMENTED]
    assert set(implemented) == {"SCG-P0"}


def test_P12_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p12_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P12-SPEC-TERMINAL — no successor phase, no downstream candidate
# ─────────────────────────────────────────────────────────────────────────────


def test_P12_SPEC_TERMINAL_01_opens_nothing():
    assert _p12(build_master_registry_seed()).target_boundary_opens == ()


def test_P12_SPEC_TERMINAL_02_no_forbidden_direct_next_ids():
    assert _p12(build_master_registry_seed()).forbidden_direct_next_layer_ids == ()


def test_P12_SPEC_TERMINAL_03_consumes_only_irab_geometry_candidate():
    assert _p12(build_master_registry_seed()).origin.output_type == "IrabGeometryCandidate"


# ─────────────────────────────────────────────────────────────────────────────
# P12-SPEC-NOREALITY — speech-force possibility, never reality / truth / hukm
# ─────────────────────────────────────────────────────────────────────────────


def test_P12_SPEC_NOREALITY_01_forbidden_changes_block_reality_truth_hukm():
    spec = _p12(build_master_registry_seed())
    for change in ("assign_reality_claim", "assign_truth_value", "assign_hukm"):
        assert change in spec.forbidden_changes


def test_P12_SPEC_NOREALITY_02_reality_truth_and_final_decision_outputs_forbidden():
    forbidden = _p12(build_master_registry_seed()).forbidden_outputs
    for name in (
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "IrabFinalDecision", "RealityMapping", "TruthJudgment",
    ):
        assert name in forbidden


def test_P12_SPEC_NOREALITY_03_output_is_candidate_only_with_structural_fields():
    spec = _p12(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "irab_geometry_ref",
        "speech_force_evidence",
        "ifadah_boundary_evidence",
        "mukhatab_context_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P12-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P12_SPEC_IDENTITY_01_preserves_irab_geometry_identity():
    assert "irab_geometry_identity" in _p12(build_master_registry_seed()).preserves_ids


def test_P12_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p12(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P12-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P12_SPEC_NORUNTIME_01_no_p12_implemented_builder():
    # P12 is now IMPLEMENTED via build_p12_implemented_registry (the terminal layer);
    # the SPECIFIED builder must still stop P12 at SPECIFIED (no runtime advance from
    # the spec).
    assert hasattr(MRS, "build_p12_implemented_registry")
    assert _p12(build_p12_specified_registry()).status is LayerStatus.SPECIFIED


def test_P12_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p12(build_p12_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P12_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p11_specified_registry()  # P12 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P12_IFADAH_SPEECH_FORCE, LayerStatus.IMPLEMENTED)
