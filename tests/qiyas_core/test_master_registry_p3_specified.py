"""SCG-P3 Root Stem Closure — SPEC-level enforcement tests (P3-SPEC-*).

Narrow SCG-P3-only spec-authoring authorization (2026-06-15). SPEC ONLY:
no runtime, no adapter, NO root extraction, no IMPLEMENTED status. Canonical
SCG registry track only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p2_specified_registry,
    build_p3_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P2_REGISTRY_PROJECTION,
    LAYER_ID_P3_ROOT_STEM_CLOSURE,
    LAYER_ID_P4_JAMID_MUSHTAQ,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "ROOT_STEM_CLOSURE_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "JamidMushtaqCandidate",
    "MufradWordCandidate",
    "VerbalSignifiedCandidate",
    "CompositionReadinessCandidate",
    "AmilMamulCandidate",
    "SentenceGeometryCandidate",
    "RelationGeometryCandidate",
    "IrabGeometryCandidate",
    "IfadahCandidate",
)


def _p3(registry):
    return registry.get(LAYER_ID_P3_ROOT_STEM_CLOSURE)


# ─────────────────────────────────────────────────────────────────────────────
# P3-SPEC-ROW
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_SPEC_ROW_01_row_exists():
    spec = _p3(build_master_registry_seed())
    assert spec.id == "P3_ROOT_STEM_CLOSURE"
    assert spec.name == "RootStemClosureLayer"
    assert spec.phase == "SCG-P3"


def test_P3_SPEC_ROW_02_output_type_is_root_stem_candidate_only():
    assert _p3(build_master_registry_seed()).branch.output_type == "RootStemCandidate"


def test_P3_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P3" in text and "RootStemCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P3-SPEC-STATUS
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_SPEC_STATUS_01_specified_via_builder():
    assert _p3(build_p3_specified_registry()).status is LayerStatus.SPECIFIED


def test_P3_SPEC_STATUS_02_base_and_p2_leave_p3_planned():
    assert _p3(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p3(build_p2_specified_registry()).status is LayerStatus.PLANNED


def test_P3_SPEC_STATUS_03_p4_to_p12_remain_planned():
    reg = build_p3_specified_registry()
    for spec in reg.all_layers():
        if spec.phase not in ("SCG-P0", "SCG-P1", "SCG-P2", "SCG-P3"):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P3_SPEC_STATUS_04_p0_implemented_p1_p2_specified_preserved():
    reg = build_p3_specified_registry()
    assert all(
        s.status is LayerStatus.IMPLEMENTED for s in reg.all_layers() if s.phase == "SCG-P0"
    )
    assert all(
        s.status is LayerStatus.SPECIFIED
        for s in reg.all_layers()
        if s.phase in ("SCG-P1", "SCG-P2")
    )


def test_P3_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p3_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P3-SPEC-NOJUMP
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p3(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P3_SPEC_NOJUMP_02_consumes_only_registry_projection_candidate():
    assert _p3(build_master_registry_seed()).origin.output_type == "RegistryProjectionCandidate"


def test_P3_SPEC_NOJUMP_03_opens_priors_but_does_not_produce_them():
    spec = _p3(build_master_registry_seed())
    assert "jamid_mushtaq_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "RootStemCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P3_SPEC_NOJUMP_04_forbids_direct_next_p8_p9_p12():
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    spec = _p3(build_master_registry_seed())
    for lid in (
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P9_SENTENCE_GEOMETRY,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ):
        assert lid in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P3-SPEC-NOROOT — no root extraction / wazn / morphology / final judgment
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_SPEC_NOROOT_01_forbidden_changes_block_meaning_irab_case():
    spec = _p3(build_master_registry_seed())
    for change in ("assign_meaning", "assign_irab", "assign_case"):
        assert change in spec.forbidden_changes


def test_P3_SPEC_NOROOT_02_no_final_root_or_word_or_meaning_judgment_outputs():
    forbidden = _p3(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning", "MeaningCandidate", "WordTypeJudgment"):
        assert name in forbidden


def test_P3_SPEC_NOROOT_03_output_is_candidate_only_possibility():
    spec = _p3(build_master_registry_seed())
    assert spec.branch.output_type.endswith("Candidate")
    # structural possibility, not extraction — required evidence fields are
    # structural (slot/pattern/boundary), not lexical-root lookups.
    assert set(spec.minimum_required_fields) == {
        "slot_sequence_refs",
        "root_pattern_evidence",
        "stem_boundary_evidence",
    }


# ─────────────────────────────────────────────────────────────────────────────
# P3-SPEC-IDENTITY / RESIDUAL
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_SPEC_IDENTITY_01_preserves_slot_candidate_identities():
    assert "slot_candidate_identities" in _p3(build_master_registry_seed()).preserves_ids


def test_P3_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p3(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P3-SPEC-NORUNTIME
# ─────────────────────────────────────────────────────────────────────────────


def test_P3_SPEC_NORUNTIME_01_no_p3_implemented_builder():
    assert not hasattr(MRS, "build_p3_implemented_registry")


def test_P3_SPEC_NORUNTIME_02_builder_stops_at_specified():
    assert _p3(build_p3_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P3_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    """Lifecycle cannot skip SPECIFIED: P3 PLANNED -> IMPLEMENTED is rejected."""
    reg = build_p2_specified_registry()  # P3 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P3_ROOT_STEM_CLOSURE, LayerStatus.IMPLEMENTED)


def test_P3_SPEC_NORUNTIME_04_p4_not_advanced_by_p3_builder():
    assert build_p3_specified_registry().get(LAYER_ID_P4_JAMID_MUSHTAQ).status is LayerStatus.PLANNED
