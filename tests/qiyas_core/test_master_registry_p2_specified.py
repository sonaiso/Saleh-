"""SCG-P2 Registry Projection — SPEC-level enforcement tests (P2-SPEC-*).

Narrow SCG-P2-only spec-authoring authorization (2026-06-15). SPEC ONLY:
no runtime, no adapter, no IMPLEMENTED status. Canonical SCG registry track
only (NOT the runtime syllable track).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qiyas_core.slot_geometry_core import (
    LayerStatus,
    RegistryViolation,
    build_master_registry_seed,
    build_p1_specified_registry,
    build_p2_specified_registry,
)
from qiyas_core.slot_geometry_core import master_registry_seed as MRS
from qiyas_core.slot_geometry_core.master_registry_seed import (
    LAYER_ID_P1_SLOT_CANDIDATE,
    LAYER_ID_P2_REGISTRY_PROJECTION,
    LAYER_ID_P3_ROOT_STEM_CLOSURE,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SPEC_DOC = REPO_ROOT / "docs" / "qiyas_core" / "REGISTRY_PROJECTION_CONSTITUTION.md"

DOWNSTREAM_OUTPUT_TYPES = (
    "RootStemCandidate",
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


def _p2(registry):
    return registry.get(LAYER_ID_P2_REGISTRY_PROJECTION)


# ─────────────────────────────────────────────────────────────────────────────
# P2-SPEC-ROW — row exists, output type, doc
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_SPEC_ROW_01_row_exists():
    spec = _p2(build_master_registry_seed())
    assert spec.id == "P2_REGISTRY_PROJECTION"
    assert spec.name == "RegistryProjectionLayer"
    assert spec.phase == "SCG-P2"


def test_P2_SPEC_ROW_02_output_type_is_registry_projection_candidate_only():
    assert _p2(build_master_registry_seed()).branch.output_type == "RegistryProjectionCandidate"


def test_P2_SPEC_ROW_03_spec_doc_present():
    assert SPEC_DOC.is_file()
    text = SPEC_DOC.read_text(encoding="utf-8")
    assert "SCG-P2" in text and "RegistryProjectionCandidate" in text


# ─────────────────────────────────────────────────────────────────────────────
# P2-SPEC-STATUS — PLANNED -> SPECIFIED via build_p2_specified_registry only
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_SPEC_STATUS_01_specified_via_builder():
    assert _p2(build_p2_specified_registry()).status is LayerStatus.SPECIFIED


def test_P2_SPEC_STATUS_02_seed_and_p1_leave_p2_planned():
    assert _p2(build_master_registry_seed()).status is LayerStatus.PLANNED
    assert _p2(build_p1_specified_registry()).status is LayerStatus.PLANNED


def test_P2_SPEC_STATUS_03_p3_to_p12_remain_planned():
    reg = build_p2_specified_registry()
    for spec in reg.all_layers():
        if spec.phase not in ("SCG-P0", "SCG-P1", "SCG-P2"):
            assert spec.status is LayerStatus.PLANNED, spec.id


def test_P2_SPEC_STATUS_04_p0_implemented_p1_specified_preserved():
    reg = build_p2_specified_registry()
    p0 = [s for s in reg.all_layers() if s.phase == "SCG-P0"]
    p1 = [s for s in reg.all_layers() if s.phase == "SCG-P1"]
    assert all(s.status is LayerStatus.IMPLEMENTED for s in p0)
    assert all(s.status is LayerStatus.SPECIFIED for s in p1)


def test_P2_SPEC_STATUS_05_layer_count_unchanged():
    assert len(list(build_p2_specified_registry().all_layers())) == 19


# ─────────────────────────────────────────────────────────────────────────────
# P2-SPEC-NOJUMP — does not produce P3+ outputs; no P1->P3 jump
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_SPEC_NOJUMP_01_forbids_all_downstream_output_types():
    forbidden = _p2(build_master_registry_seed()).forbidden_outputs
    for name in DOWNSTREAM_OUTPUT_TYPES:
        assert name in forbidden, name


def test_P2_SPEC_NOJUMP_02_opens_priors_but_does_not_produce_them():
    spec = _p2(build_master_registry_seed())
    # It OPENS root/word priors (for P3) but its only OUTPUT is the projection.
    assert "root_stem_candidates" in spec.target_boundary_opens
    assert spec.branch.output_type == "RegistryProjectionCandidate"
    assert spec.branch.output_type not in DOWNSTREAM_OUTPUT_TYPES


def test_P2_SPEC_NOJUMP_03_no_direct_p1_to_p3_path():
    """P3 depends on P2's output, so SCG-P1 -> SCG-P3 necessarily skips P2."""
    seed = build_master_registry_seed()
    assert seed.get(LAYER_ID_P2_REGISTRY_PROJECTION).origin.output_type == "SlotCandidate"
    assert seed.get(LAYER_ID_P3_ROOT_STEM_CLOSURE).origin.output_type == "RegistryProjectionCandidate"


def test_P2_SPEC_NOJUMP_04_forbids_direct_next_p6_p8_p12():
    spec = _p2(build_master_registry_seed())
    from qiyas_core.slot_geometry_core.master_registry_seed import (
        LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    )
    for lid in (
        LAYER_ID_P6_VERBAL_SIGNIFIED_ALONE,
        LAYER_ID_P8_AMIL_MAMUL,
        LAYER_ID_P12_IFADAH_SPEECH_FORCE,
    ):
        assert lid in spec.forbidden_direct_next_layer_ids


# ─────────────────────────────────────────────────────────────────────────────
# P2-SPEC-CLAIM — no root/word/meaning/irab claim; absolutes forbidden
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_SPEC_CLAIM_01_forbidden_changes_block_root_meaning_irab():
    spec = _p2(build_master_registry_seed())
    for change in ("assign_root", "assign_meaning", "assign_irab"):
        assert change in spec.forbidden_changes


def test_P2_SPEC_CLAIM_02_absolutes_forbidden():
    forbidden = _p2(build_master_registry_seed()).forbidden_outputs
    for name in ("HukmCandidate", "RealityClaim", "FinalMeaning"):
        assert name in forbidden


def test_P2_SPEC_CLAIM_03_candidate_only_output():
    assert _p2(build_master_registry_seed()).branch.output_type.endswith("Candidate")


# ─────────────────────────────────────────────────────────────────────────────
# P2-SPEC-IDENTITY / RESIDUAL — identity not consumed; residuals explicit
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_SPEC_IDENTITY_01_preserves_slot_candidate_identity():
    spec = _p2(build_master_registry_seed())
    assert "slot_candidate_identity" in spec.preserves_ids
    assert spec.origin.output_type == "SlotCandidate"


def test_P2_SPEC_RESIDUAL_01_blockers_and_invalidating_differences_explicit():
    spec = _p2(build_master_registry_seed())
    assert spec.blockers and spec.invalidating_differences


# ─────────────────────────────────────────────────────────────────────────────
# P2-SPEC-NORUNTIME — no IMPLEMENTED, no implemented builder
# ─────────────────────────────────────────────────────────────────────────────


def test_P2_SPEC_NORUNTIME_01_specified_builder_stops_at_specified():
    # SCG-P2 RegistryProjection is IMPLEMENTED as of 2026-06-18 via
    # build_p2_implemented_registry; the SPEC builder must still stop at SPECIFIED.
    assert hasattr(MRS, "build_p2_implemented_registry")
    assert _p2(build_p2_specified_registry()).status is LayerStatus.SPECIFIED


def test_P2_SPEC_NORUNTIME_02_builder_stops_at_specified_not_implemented():
    assert _p2(build_p2_specified_registry()).status is not LayerStatus.IMPLEMENTED


def test_P2_SPEC_NORUNTIME_03_direct_planned_to_implemented_raises():
    """Lifecycle cannot skip SPECIFIED: P2 PLANNED -> IMPLEMENTED is rejected."""
    reg = build_p1_specified_registry()  # P2 still PLANNED here
    with pytest.raises(RegistryViolation):
        reg.update_status(LAYER_ID_P2_REGISTRY_PROJECTION, LayerStatus.IMPLEMENTED)
