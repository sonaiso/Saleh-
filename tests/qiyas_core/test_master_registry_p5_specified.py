"""SCG-P5 Mufrad Word Contracts — SPEC-level enforcement tests (P5-SPEC-*).

Narrow SCG-P4–P7 spec-authoring authorization (2026-06-16). SPEC ONLY:
no runtime, no adapter, NO lexical-word claim, NO word-meaning claim, no
IMPLEMENTED status. Canonical SCG registry track only (NOT the runtime syllable
track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p4_specified_registry,
    build_p5_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P5_MUFRAD_WORD_CONTRACTS,
    LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "MUFRAD_WORD_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "VerbalSignifiedCandidate",
    "CompositionReadinessCandidate",
    "AmilMamulCandidate",
    "SentenceGeometryCandidate",
    "RelationGeometryCandidate",
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p5(registry):
    return registry.get(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS)


# ─────────────────────────────────────────────────────────────────────────────
# P5-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_SPEC_ROW_01_row_exists():
    spec = _p5(build_master_registry_seed())
    assert spec.id == "P5_MUFRAD_WORD_CONTRACTS"
    assert spec.name == "MufradWordContractsLayer"
    assert spec.phase == "SCG-P5"


def test_P5_SPEC_ROW_02_output_type_is_mufrad_word_candidate_only():
    assert _p5(build_master_registry_seed()).branch.output_type == "MufradWordCandidate"


def test_P5_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P5" in text and "MufradWordCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P5-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_SPEC_STATUS_01_specified_via_builder():
    assert _p5(build_p5_specified_registry()).status is LayerStatus.SPECIFIED


def test_P5_SPEC_STATUS_02_base_and_p4_leave_p5_planned():
    assert _p5(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p5(build_p4_specified_registry()).status is LayerStatus.PLANNED


def test_P5_SPEC_STATUS_03_p6_to_p12_remain_planned():
    reg = build_p5_specified_registry()
    for spec in reg.all_layers():
        if spec.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4", "SCG-P5"):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P5_SPEC_STATUS_04_p0_implemented_p1_p4_specified_preserved():
    reg = build_p5_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in ("SCG-P1", "SCG-P2", "SCG-P3", "SCG-P4")
    )


def test_P5_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p5_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P5-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p5(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P5_SPEC_NOJUMP_02_consumes_only_jamid_mushtaq_candidate():
    assert _p5(build_master_registry_seed()).origin.output_type == "JamidMushtaqCandidate"


def test_P5_SPEC_NOJUMP_03_opens_priors_but_does_not_produce_them():
    spec = _p5(build_master_registry_seed())
    assert "verbal_signified_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "MufradWordCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P5_SPEC_NOJUMP_04_forbids_direct_next_p9_p11_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p5(build_master_registry_seed())
    for lid in (
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P11_IRAB_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ):
        assert lid in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P5-SPEC-NOLEX — no lexical wordhood / meaning / i'rab / case
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_SPEC_NOLEX_01_forbidden_changes_block_irab_case_meaning():
    spec = _p5(build_master_registry_seed())
    for change in ("assign_irab", "assign_case", "assign_meaning"):
        assert change in spec.forbidden_changes


def test_P5_SPEC_NOLEX_02_no_irab_case_or_sentence_outputs():
    forbidden = _p5(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "IrabCandidate", "CaseEffect", "SentenceCandidate"):
        assert name in forbidden


def test_P5_SPEC_NOLEX_03_output_is_candidate_only_with_structural_fields():
    spec = _p5(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    assert set(spec.minimum_required_fields) == {
        "root_stem_ref",
        "word_class_evidence",
        "word_boundary_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P5-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_SPEC_IDENTITY_01_preserves_jamid_mushtaq_candidate_identity():
    assert "jamid_mushtaq_candidate_identity" in _p5(build_master_registry_seed()).preserves_ids


def test_P5_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p5(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P5-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P5_SPEC_NORUNTIME_01_specified_builder_stops_at_specified():
    # SCG-P5 MufradWord is IMPLEMENTED as of 2026-06-18 via
    # build_p5_implemented_registry; the SPEC builder must still stop at SPECIFIED.
    assert hasattr(MRS, "build_p5_implemented_registry")
    assert _p5(build_p5_specified_registry()).status is LayerStatus.SPECIFIED


def test_P5_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p5(build_p5_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P5_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    reg = build_p4_specified_registry()  # P5 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P5_MUFRAD_WORD_CONTRACTS, LayerStatus.IMPLEMENTED)


def test_P5_SPEC_NORUNTIME_04_p6_not_advanced_by_p5_builder():
    assert build_p5_specified_registry().get(LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE).status is LayerStatus.PLANNED
