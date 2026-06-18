"""SCG-P7 Composition Readiness — SPEC-level enforcement tests (P7-SPEC-*).

Narrow SCG-P4–P7 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO actual composition, NO realized isnad, no IMPLEMENTED
status. Canonical SCG registry track only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p6_specified_registry,
    build_p7_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P7_COMPOSITION_READINESS,
    LAYER_ID_P8_AMIL_MAMUL,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "COMPOSITION_READINESS_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "AmilMamulCandidate",
    "SentenceGeometryCandidate",
    "RelationGeometryCandidate",
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p7(registry):
    return registry.get(LAYER_ID_P7_COMPOSITION_READINESS)


# ─────────────────────────────────────────────────────────────────────────────
# P7-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_SPEC_ROW_01_row_exists():
    spec = _p7(build_master_registry_seed())
    assert spec.id == "P7_COMPOSITION_READINESS"
    assert spec.name == "CompositionReadinessLayer"
    assert spec.phase == "SCG-P7"


def test_P7_SPEC_ROW_02_output_type_is_composition_readiness_candidate_only():
    assert _p7(build_master_registry_seed()).branch.output_type == "CompositionReadinessCandidate"


def test_P7_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P7" in text and "CompositionReadinessCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P7-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_SPEC_STATUS_01_specified_via_builder():
    assert _p7(build_p7_specified_registry()).status is LayerStatus.SPECIFIED


def test_P7_SPEC_STATUS_02_base_and_p6_leave_p7_planned():
    assert _p7(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p7(build_p6_specified_registry()).status is LayerStatus.PLANNED


def test_P7_SPEC_STATUS_03_p8_to_p12_remain_planned():
    reg = build_p7_specified_registry()
    for spec in reg.all_layers():
        if spec.phase not in (
            "SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6", "SCG-P7",
        ):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P7_SPEC_STATUS_04_p0_implemented_p1_p6_specified_preserved():
    reg = build_p7_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in ("SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6")
    )


def test_P7_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p7_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P7-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p7(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P7_SPEC_NOJUMP_02_consumes_only_verbal_signified_candidate():
    assert _p7(build_master_registry_seed()).origin.output_type == "VerbalSignifiedCandidate"


def test_P7_SPEC_NOJUMP_03_opens_amil_mamul_prior_but_does_not_produce_it():
    spec = _p7(build_master_registry_seed())
    assert "amil_mamul_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "CompositionReadinessCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P7_SPEC_NOJUMP_04_forbids_direct_next_p11_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p7(build_master_registry_seed())
    for lid in (LAYER_ID_P11_IRAB_GEOMETRY, LAYER_ID_P12_IFADAH_SPEECH_FORCE):
        assert lid in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P7-SPEC-NOCOMPOSE — readiness only, never actual composition / isnad / i'rab
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_SPEC_NOCOMPOSE_01_forbidden_changes_block_irab_case_meaning():
    spec = _p7(build_master_registry_seed())
    for change in ("assign_irab", "assign_case", "assign_meaning"):
        assert change in spec.forbidden_changes


def test_P7_SPEC_NOCOMPOSE_02_no_irab_case_or_sentence_outputs():
    forbidden = _p7(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "IrabCandidate", "CaseEffect", "SentenceCandidate"):
        assert name in forbidden


def test_P7_SPEC_NOCOMPOSE_03_output_is_candidate_only_with_structural_fields():
    spec = _p7(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "verbal_signified_refs",
        "composition_boundary_evidence",
        "isnad_readiness_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P7-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_SPEC_IDENTITY_01_preserves_verbal_signified_candidate_identities():
    assert "verbal_signified_candidate_identities" in _p7(build_master_registry_seed()).preserves_ids


def test_P7_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p7(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P7-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P7_SPEC_NORUNTIME_01_specified_builder_stops_at_specified():
    # SCG-P7 CompositionReadiness is IMPLEMENTED as of 2026-06-18 via
    # build_p7_implemented_registry; the SPEC builder must still stop at SPECIFIED.
    assert hasattr(MRS, "build_p7_implemented_registry")
    assert _p7(build_p7_specified_registry()).status is LayerStatus.SPECIFIED


def test_P7_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p7(build_p7_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P7_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p6_specified_registry()  # P7 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P7_COMPOSITION_READINESS, LayerStatus.IMPLEMENTED)


def test_P7_SPEC_NORUNTIME_04_p8_not_advanced_by_p7_builder():
    assert build_p7_specified_registry().get(LAYER_ID_P8_AMIL_MAMUL).status is LayerStatus.PLANNED
