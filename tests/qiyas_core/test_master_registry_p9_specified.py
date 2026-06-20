"""SCG-P9 Sentence Geometry — SPEC-level enforcement tests (P9-SPEC-*).

Narrow SCG-P8–P12 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO actual i‘rab judgment, NO ifadah, no IMPLEMENTED
status. Canonical SCG registry track only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p8_specified_registry,
    build_p9_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P9_SENTENCE_GEOMETRY,
    LAYER_ID_P10_RELATION_GEOMETRY,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "SENTENCE_GEOMETRY_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "RelationGeometryCandidate",
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p9(registry):
    return registry.get(LAYER_ID_P9_SENTENCE_GEOMETRY)


# ─────────────────────────────────────────────────────────────────────────────
# P9-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P9_SPEC_ROW_01_row_exists():
    spec = _p9(build_master_registry_seed())
    assert spec.id == "P9_SENTENCE_GEOMETRY"
    assert spec.name == "SentenceGeometryLayer"
    assert spec.phase == "SCG-P9"


def test_P9_SPEC_ROW_02_output_type_is_sentence_geometry_candidate_only():
    assert _p9(build_master_registry_seed()).branch.output_type == "SentenceGeometryCandidate"


def test_P9_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P9" in text and "SentenceGeometryCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P9-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P9_SPEC_STATUS_01_specified_via_builder():
    assert _p9(build_p9_specified_registry()).status is LayerStatus.SPECIFIED


def test_P9_SPEC_STATUS_02_base_and_p8_leave_p9_planned():
    assert _p9(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p9(build_p8_specified_registry()).status is LayerStatus.PLANNED


def test_P9_SPEC_STATUS_03_p10_to_p12_remain_planned():
    reg = build_p9_specified_registry()
    for spec in reg.all_layers():
        if spec.phase in ("SCG-P10", "SCG-P11", "SCG-P12"):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P9_SPEC_STATUS_04_p0_implemented_p1_p8_specified_preserved():
    reg = build_p9_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in (
            "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6", "SCG-P7", "SCG-P8",
        )
    )


def test_P9_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p9_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P9-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P9_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p9(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P9_SPEC_NOJUMP_02_consumes_only_amil_mamul_candidate():
    assert _p9(build_master_registry_seed()).origin.output_type == "AmilMamulCandidate"


def test_P9_SPEC_NOJUMP_03_opens_relation_geometry_prior_but_does_not_produce_it():
    spec = _p9(build_master_registry_seed())
    assert "relation_geometry_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "SentenceGeometryCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P9_SPEC_NOJUMP_04_forbids_direct_next_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p9(build_master_registry_seed())
    assert LAYER_ID_P12_IFADAH_SPEECH_FORCE in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P9-SPEC-NOIRAB — arrangement opened, no verdict / i'rab / ifadah closed
# ─────────────────────────────────────────────────────────────────────────────


def test_P9_SPEC_NOIRAB_01_forbidden_changes_block_irab_case_ifadah():
    spec = _p9(build_master_registry_seed())
    for change in ("assign_irab", "assign_case", "assign_ifadah"):
        assert change in spec.forbidden_changes


def test_P9_SPEC_NOIRAB_02_no_irab_case_or_ifadah_outputs():
    forbidden = _p9(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "IrabCandidate", "CaseJudgment", "IfadahCandidate"):
        assert name in forbidden


def test_P9_SPEC_NOIRAB_03_output_is_candidate_only_with_structural_fields():
    spec = _p9(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "amil_mamul_refs",
        "sentence_type_evidence",
        "isnad_boundary_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P9-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P9_SPEC_IDENTITY_01_preserves_amil_mamul_candidate_identities():
    assert "amil_mamul_candidate_identities" in _p9(build_master_registry_seed()).preserves_ids


def test_P9_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p9(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P9-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P9_SPEC_NORUNTIME_01_spec_builder_keeps_p9_specified_not_implemented():
    # P9 is now IMPLEMENTED via build_p9_implemented_registry; the SPECIFIED
    # builder must still stop P9 at SPECIFIED (no runtime advance from the spec).
    assert hasattr(MRS, "build_p9_implemented_registry")
    assert _p9(build_p9_specified_registry()).status is LayerStatus.SPECIFIED


def test_P9_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p9(build_p9_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P9_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p8_specified_registry()  # P9 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P9_SENTENCE_GEOMETRY, LayerStatus.IMPLEMENTED)


def test_P9_SPEC_NORUNTIME_04_p10_not_advanced_by_p9_builder():
    assert build_p9_specified_registry().get(LAYER_ID_P10_RELATION_GEOMETRY).status is LayerStatus.PLANNED
