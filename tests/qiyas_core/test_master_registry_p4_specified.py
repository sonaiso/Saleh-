"""SCG-P4 Jamid/Mushtaq — SPEC-level enforcement tests (P4-SPEC-*).

Narrow SCG-P4–P7 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO root extraction, NO wazn assignment, no IMPLEMENTED
status. Canonical SCG registry track only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p3_specified_registry,
    build_p4_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P4_JAMID_MUSHTAQ,
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "JAMID_MUSHTAQ_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "MufradWordCandidate",
    "VerbalSignifiedCandidate",
    "CompositionReadinessCandidate",
    "AmilMamulCandidate",
    "SentenceGeometryCandidate",
    "RelationGeometryCandidate",
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p4(registry):
    return registry.get(LAYER_ID_P4_JAMID_MUSHTAQ)


# ─────────────────────────────────────────────────────────────────────────────
# P4-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_SPEC_ROW_01_row_exists():
    spec = _p4(build_master_registry_seed())
    assert spec.id == "P4_JAMID_MUSHTAQ"
    assert spec.name == "JamidMushtaqLayer"
    assert spec.phase == "SCG-P4"


def test_P4_SPEC_ROW_02_output_type_is_jamid_mushtaq_candidate_only():
    assert _p4(build_master_registry_seed()).branch.output_type == "JamidMushtaqCandidate"


def test_P4_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P4" in text and "JamidMushtaqCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P4-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_SPEC_STATUS_01_specified_via_builder():
    assert _p4(build_p4_specified_registry()).status is LayerStatus.SPECIFIED


def test_P4_SPEC_STATUS_02_base_and_p3_leave_p4_planned():
    assert _p4(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p4(build_p3_specified_registry()).status is LayerStatus.PLANNED


def test_P4_SPEC_STATUS_03_p5_to_p12_remain_planned():
    reg = build_p4_specified_registry()
    for spec in reg.all_layers():
        if spec.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4"):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P4_SPEC_STATUS_04_p0_implemented_p1_p3_specified_preserved():
    reg = build_p4_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in ("SCG-P1", "SCG-P2", "SCG-P3")
    )


def test_P4_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p4_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P4-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p4(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P4_SPEC_NOJUMP_02_consumes_only_root_stem_candidate():
    assert _p4(build_master_registry_seed()).origin.output_type == "RootStemCandidate"


def test_P4_SPEC_NOJUMP_03_opens_word_type_prior_but_does_not_produce_it():
    spec = _p4(build_master_registry_seed())
    assert "word_type_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "JamidMushtaqCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P4_SPEC_NOJUMP_04_forbids_direct_next_p8_p9_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p4(build_master_registry_seed())
    for lid in (
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ):
        assert lid in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P4-SPEC-NOROOT — no root extraction / wazn / meaning / final judgment
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_SPEC_NOROOT_01_forbidden_changes_block_meaning_irab_case():
    spec = _p4(build_master_registry_seed())
    for change in ("assign_meaning", "assign_irab", "assign_case"):
        assert change in spec.forbidden_changes


def test_P4_SPEC_NOROOT_02_no_word_type_or_meaning_judgment_outputs():
    forbidden = _p4(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "WordTypeJudgment", "MeaningCandidate"):
        assert name in forbidden


def test_P4_SPEC_NOROOT_03_output_is_candidate_only_with_structural_fields():
    spec = _p4(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "root_stem_ref",
        "derivation_class_evidence",
        "pattern_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P4-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_SPEC_IDENTITY_01_preserves_root_stem_candidate_identity():
    assert "root_stem_candidate_identity" in _p4(build_master_registry_seed()).preserves_ids


def test_P4_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p4(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P4-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P4_SPEC_NORUNTIME_01_specified_builder_stops_at_specified():
    # SCG-P4 JamidMushtaq is IMPLEMENTED as of 2026-06-18 via
    # build_p4_implemented_registry; the SPEC builder must still stop at SPECIFIED.
    assert hasattr(MRS, "build_p4_implemented_registry")
    assert _p4(build_p4_specified_registry()).status is LayerStatus.SPECIFIED


def test_P4_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p4(build_p4_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P4_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p3_specified_registry()  # P4 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P4_JAMID_MUSHTAQ, LayerStatus.IMPLEMENTED)


def test_P4_SPEC_NORUNTIME_04_p5_not_advanced_by_p4_builder():
    assert build_p4_specified_registry().get(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS).status is LayerStatus.PLANNED
