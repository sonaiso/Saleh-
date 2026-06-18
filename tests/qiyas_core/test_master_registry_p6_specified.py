"""SCG-P6 Verbal Signified Alone — SPEC-level enforcement tests (P6-SPEC-*).

Narrow SCG-P4–P7 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO lexical meaning, NO dalalah closure, no IMPLEMENTED
status. Canonical SCG registry track only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p5_specified_registry,
    build_p6_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
    LAYER_ID_P7_COMPOSITION_READINESS,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "VERBAL_SIGNIFIED_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "CompositionReadinessCandidate",
    "AmilMamulCandidate",
    "SentenceGeometryCandidate",
    "RelationGeometryCandidate",
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p6(registry):
    return registry.get(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE)


# ─────────────────────────────────────────────────────────────────────────────
# P6-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_SPEC_ROW_01_row_exists():
    spec = _p6(build_master_registry_seed())
    assert spec.id == "P6_VERBAL_SIGNIFIED_ALONE"
    assert spec.name == "VerbalSignifiedAloneLayer"
    assert spec.phase == "SCG-P6"


def test_P6_SPEC_ROW_02_output_type_is_verbal_signified_candidate_only():
    assert _p6(build_master_registry_seed()).branch.output_type == "VerbalSignifiedCandidate"


def test_P6_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P6" in text and "VerbalSignifiedCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P6-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_SPEC_STATUS_01_specified_via_builder():
    assert _p6(build_p6_specified_registry()).status is LayerStatus.SPECIFIED


def test_P6_SPEC_STATUS_02_base_and_p5_leave_p6_planned():
    assert _p6(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p6(build_p5_specified_registry()).status is LayerStatus.PLANNED


def test_P6_SPEC_STATUS_03_p7_to_p12_remain_planned():
    reg = build_p6_specified_registry()
    for spec in reg.all_layers():
        if spec.phase not in (
            "SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5", "SCG-P6",
        ):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P6_SPEC_STATUS_04_p0_implemented_p1_p5_specified_preserved():
    reg = build_p6_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in ("SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5")
    )


def test_P6_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p6_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P6-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p6(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P6_SPEC_NOJUMP_02_consumes_only_mufrad_word_candidate():
    assert _p6(build_master_registry_seed()).origin.output_type == "MufradWordCandidate"


def test_P6_SPEC_NOJUMP_03_opens_prior_but_does_not_produce_it():
    spec = _p6(build_master_registry_seed())
    assert "composition_readiness_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "VerbalSignifiedCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P6_SPEC_NOJUMP_04_forbids_direct_next_p9_p11_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p6(build_master_registry_seed())
    for lid in (
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ):
        assert lid in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P6-SPEC-NOMEANING — signified opened, meaning never closed
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_SPEC_NOMEANING_01_forbidden_changes_block_meaning_irab_case():
    spec = _p6(build_master_registry_seed())
    for change in ("assign_meaning", "assign_irab", "assign_case"):
        assert change in spec.forbidden_changes


def test_P6_SPEC_NOMEANING_02_meaning_judgment_and_absolutes_forbidden():
    forbidden = _p6(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "MeaningJudgment"):
        assert name in forbidden


def test_P6_SPEC_NOMEANING_03_output_is_candidate_only_with_structural_fields():
    spec = _p6(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "mufrad_word_ref",
        "signified_class_evidence",
        "verbal_identity_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P6-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_SPEC_IDENTITY_01_preserves_mufrad_word_candidate_identity():
    assert "mufrad_word_candidate_identity" in _p6(build_master_registry_seed()).preserves_ids


def test_P6_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p6(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P6-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P6_SPEC_NORUNTIME_01_specified_builder_stops_at_specified():
    # SCG-P6 VerbalSignified is IMPLEMENTED as of 2026-06-18 via
    # build_p6_implemented_registry; the SPEC builder must still stop at SPECIFIED.
    assert hasattr(MRS, "build_p6_implemented_registry")
    assert _p6(build_p6_specified_registry()).status is LayerStatus.SPECIFIED


def test_P6_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p6(build_p6_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P6_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p5_specified_registry()  # P6 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE, LayerStatus.IMPLEMENTED)


def test_P6_SPEC_NORUNTIME_04_p7_not_advanced_by_p6_builder():
    assert build_p6_specified_registry().get(LAYER_ID_P7_COMPOSITION_READINESS).status is LayerStatus.PLANNED
