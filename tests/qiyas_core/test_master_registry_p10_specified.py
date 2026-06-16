"""SCG-P10 Relation Geometry — SPEC-level enforcement tests (P10-SPEC-*).

Narrow SCG-P8–P12 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO actual i‘rab judgment, no IMPLEMENTED status.
Canonical SCG registry track only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p9_specified_registry,
    build_p10_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P10_RELATION_GEOMETRY,
    LAYER_ID_P11_IRAB_GEOMETRY,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "RELATION_GEOMETRY_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p10(registry):
    return registry.get(LAYER_ID_P10_RELATION_GEOMETRY)


# ─────────────────────────────────────────────────────────────────────────────
# P10-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P10_SPEC_ROW_01_row_exists():
    spec = _p10(build_master_registry_seed())
    assert spec.id == "P10_RELATION_GEOMETRY"
    assert spec.name == "RelationGeometryLayer"
    assert spec.phase == "SCG-P10"


def test_P10_SPEC_ROW_02_output_type_is_relation_geometry_candidate_only():
    assert _p10(build_master_registry_seed()).branch.output_type == "RelationGeometryCandidate"


def test_P10_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P10" in text and "RelationGeometryCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P10-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P10_SPEC_STATUS_01_specified_via_builder():
    assert _p10(build_p10_specified_registry()).status is LayerStatus.SPECIFIED


def test_P10_SPEC_STATUS_02_base_and_p9_leave_p10_planned():
    assert _p10(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p10(build_p9_specified_registry()).status is LayerStatus.PLANNED


def test_P10_SPEC_STATUS_03_p11_to_p12_remain_planned():
    reg = build_p10_specified_registry()
    for spec in reg.all_layers():
        if spec.phase in ("SCG-P11", "SCG-P12"):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P10_SPEC_STATUS_04_p0_implemented_p1_p9_specified_preserved():
    reg = build_p10_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in (
            "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6", "SCG-P7", "SCG-P8", "SCG-P9",
        )
    )


def test_P10_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p10_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P10-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P10_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p10(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P10_SPEC_NOJUMP_02_consumes_only_sentence_geometry_candidate():
    assert _p10(build_master_registry_seed()).origin.output_type == "SentenceGeometryCandidate"


def test_P10_SPEC_NOJUMP_03_opens_irab_geometry_prior_but_does_not_produce_it():
    spec = _p10(build_master_registry_seed())
    assert "irab_geometry_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "RelationGeometryCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P10_SPEC_NOJUMP_04_forbids_direct_next_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p10(build_master_registry_seed())
    assert LAYER_ID_P12_IFADAH_SPEECH_FORCE in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P10-SPEC-NOIRAB — relations mapped, no parse / i'rab / ifadah closed
# ─────────────────────────────────────────────────────────────────────────────


def test_P10_SPEC_NOIRAB_01_forbidden_changes_block_irab_case_ifadah():
    spec = _p10(build_master_registry_seed())
    for change in ("assign_irab", "assign_case", "assign_ifadah"):
        assert change in spec.forbidden_changes


def test_P10_SPEC_NOIRAB_02_no_irab_case_or_ifadah_outputs():
    forbidden = _p10(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "IrabCandidate", "CaseJudgment", "IfadahCandidate"):
        assert name in forbidden


def test_P10_SPEC_NOIRAB_03_output_is_candidate_only_with_structural_fields():
    spec = _p10(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "sentence_geometry_ref",
        "relation_type_evidence",
        "dependency_scope_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P10-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P10_SPEC_IDENTITY_01_preserves_sentence_geometry_identity():
    assert "sentence_geometry_identity" in _p10(build_master_registry_seed()).preserves_ids


def test_P10_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p10(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P10-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P10_SPEC_NORUNTIME_01_no_p10_implemented_builder():
    assert not hasattr(MRS, "build_p10_implemented_registry")


def test_P10_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p10(build_p10_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P10_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p9_specified_registry()  # P10 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P10_RELATION_GEOMETRY, LayerStatus.IMPLEMENTED)


def test_P10_SPEC_NORUNTIME_04_p11_not_advanced_by_p10_builder():
    assert build_p10_specified_registry().get(LAYER_ID_P11_IRAB_GEOMETRY).status is LayerStatus.PLANNED
