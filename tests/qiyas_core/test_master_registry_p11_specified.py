"""SCG-P11 Irab Geometry — SPEC-level enforcement tests (P11-SPEC-*).

Narrow SCG-P8–P12 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO actual i‘rab judgment, NO final case decision, no
IMPLEMENTED status. Canonical SCG registry track only (NOT the runtime syllable
track). P11 is the most judgment-adjacent layer — it maps i‘rab *geometry* as
candidates, never an i‘rab ruling.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p10_specified_registry,
    build_p11_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P11_IRAB_GEOMETRY,
    LAYER_ID_P12_IFADAH_SPEECH_FORCE,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "IRAB_GEOMETRY_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = ("IfadahCandidate",)


def _p11(registry):
    return registry.get(LAYER_ID_P11_IRAB_GEOMETRY)


# ─────────────────────────────────────────────────────────────────────────────
# P11-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P11_SPEC_ROW_01_row_exists():
    spec = _p11(build_master_registry_seed())
    assert spec.id == "P11_IRAB_GEOMETRY"
    assert spec.name == "IrabGeometryLayer"
    assert spec.phase == "SCG-P11"


def test_P11_SPEC_ROW_02_output_type_is_irab_geometry_candidate_only():
    assert _p11(build_master_registry_seed()).branch.output_type == "IrabGeometryCandidate"


def test_P11_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P11" in text and "IrabGeometryCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P11-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P11_SPEC_STATUS_01_specified_via_builder():
    assert _p11(build_p11_specified_registry()).status is LayerStatus.SPECIFIED


def test_P11_SPEC_STATUS_02_base_and_p10_leave_p11_planned():
    assert _p11(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p11(build_p10_specified_registry()).status is LayerStatus.PLANNED


def test_P11_SPEC_STATUS_03_p12_remains_planned():
    assert build_p11_specified_registry().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE).status is LayerStatus.PLANNED


def test_P11_SPEC_STATUS_04_p0_implemented_p1_p10_specified_preserved():
    reg = build_p11_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in (
            "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5",
            "SCG-P6", "SCG-P7", "SCG-P8", "SCG-P9", "SCG-P10",
        )
    )


def test_P11_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p11_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P11-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P11_SPEC_NOJUMP_01_forbids_downstream_ifadah_output():
    forbidden = _p11(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P11_SPEC_NOJUMP_02_consumes_only_relation_geometry_candidate():
    assert _p11(build_master_registry_seed()).origin.output_type == "RelationGeometryCandidate"


def test_P11_SPEC_NOJUMP_03_opens_ifadah_prior_but_does_not_produce_it():
    spec = _p11(build_master_registry_seed())
    assert "ifadah_speech_force_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "IrabGeometryCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P11_SPEC_NOJUMP_04_p11_to_p12_is_single_licensed_edge():
    # P11 has no forbidden-direct-next ids; the only forward edge is P11 -> P12,
    # and the downstream output IfadahCandidate is held in forbidden_outputs.
    spec = _p11(build_master_registry_seed())
    assert spec.forbidden_direct_next_layer_ids == ()
    assert "IfadahCandidate" in spec.forbidden_outputs


# ─────────────────────────────────────────────────────────────────────────────
# P11-SPEC-NOIRABJUDGMENT — i'rab geometry mapped, never an i'rab ruling
# ─────────────────────────────────────────────────────────────────────────────


def test_P11_SPEC_NOIRABJUDGMENT_01_forbidden_changes_block_case_judgment_ifadah_hukm():
    spec = _p11(build_master_registry_seed())
    for change in ("assign_case_judgment", "assign_ifadah", "assign_hukm"):
        assert change in spec.forbidden_changes


def test_P11_SPEC_NOIRABJUDGMENT_02_no_case_judgment_or_final_irab_decision_outputs():
    forbidden = _p11(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "CaseJudgment", "IrabFinalDecision"):
        assert name in forbidden


def test_P11_SPEC_NOIRABJUDGMENT_03_output_is_candidate_only_with_structural_fields():
    spec = _p11(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "relation_geometry_ref",
        "irab_position_evidence",
        "case_marker_evidence",
        "waqf_readiness_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P11-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P11_SPEC_IDENTITY_01_preserves_relation_geometry_identity():
    assert "relation_geometry_identity" in _p11(build_master_registry_seed()).preserves_ids


def test_P11_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p11(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P11-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P11_SPEC_NORUNTIME_01_no_p11_implemented_builder():
    # P11 is now IMPLEMENTED via build_p11_implemented_registry; the SPECIFIED
    # builder must still stop P11 at SPECIFIED (no runtime advance from the spec).
    assert hasattr(MRS, "build_p11_implemented_registry")
    assert _p11(build_p11_specified_registry()).status is LayerStatus.SPECIFIED


def test_P11_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p11(build_p11_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P11_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p10_specified_registry()  # P11 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P11_IRAB_GEOMETRY, LayerStatus.IMPLEMENTED)


def test_P11_SPEC_NORUNTIME_04_p12_not_advanced_by_p11_builder():
    assert build_p11_specified_registry().get(LAYER_ID_P12_IFADAH_SPEECH_FORCE).status is LayerStatus.PLANNED
