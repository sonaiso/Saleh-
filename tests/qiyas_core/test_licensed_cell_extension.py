"""Licensed cell extension / closure / boundary — enforcement tests (CELL-*).

Policy C (ratified 2026-06-14): demand-driven closure + full-coverage constraint
+ multiplicity-as-potential-candidates. Potential-only; not Layer 6, not REC-6,
not shadda/gemination, not segmentation, not semantic.
"""

from __future__ import annotations

from pathlib import Path

from qiyas_core.licensed_syllable import (
    AllowedSyllableShape,
    LicensedSyllableCandidate,
)
from qiyas_core.licensed_syllable_sequence import compose_syllable_sequence
from qiyas_core.licensed_cell_extension import (
    CELL_RUNTIME_STATUS,
    CellInvalidatingDifferenceEvidence,
    LicensedCellCovering,
    tile_licensed_cells,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_SRC = REPO_ROOT / "src" / "qiyas_core" / "licensed_cell_extension.py"

# One vocalized example per closed-contract shape.
SHAPE_EXAMPLES = {
    "CV": "بَ",
    "CVV": "بَا",
    "CVC": "مِن",
    "CVVC": "قَالْ",
    "CVCC": "بَيت",
    "CVVCC": "قَالْتْ",
}


def _only(analysis) -> LicensedCellCovering:
    assert len(analysis.coverings) == 1, analysis.run
    return analysis.coverings[0]


# ─────────────────────────────────────────────────────────────────────────────
# CELL-EXTEND — single-cell extension within the closed contract
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_EXTEND_01_each_closed_shape_forms_one_cell():
    """CELL-EXTEND-01: each of the six closed shapes tiles to one licensed cell."""
    for shape_str, surface in SHAPE_EXAMPLES.items():
        analysis = tile_licensed_cells(surface)
        cov = _only(analysis)
        assert cov.length == 1
        assert cov.cell_shapes == (shape_str,)
        assert cov.cells[0].shape is AllowedSyllableShape(shape_str)


def test_CELL_EXTEND_02_baa_is_same_cell_extension_not_two_cells():
    """CELL-EXTEND-02: بَا is one cell CV→CVV (extension), not [بَ][ا]."""
    cov = _only(tile_licensed_cells("بَا"))
    assert cov.length == 1
    assert cov.cell_shapes == ("CVV",)
    # the CV-first early-close branch is recorded as a residual, not a candidate
    branches = {r.branch_first_cell_surface for r in tile_licensed_cells("بَا").residuals}
    assert "بَ" in branches


def test_CELL_EXTEND_03_bayt_is_one_cvcc_cell():
    """CELL-EXTEND-03: بَيت is a single CVCC cell."""
    cov = _only(tile_licensed_cells("بَيت"))
    assert cov.length == 1
    assert cov.cell_shapes == ("CVCC",)


# ─────────────────────────────────────────────────────────────────────────────
# CELL-CLOSURE / CELL-BOUNDARY — closure only with licensed gate/demand evidence
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_CLOSURE_01_closure_evidence_present_and_minimal_complete():
    """CELL-CLOSURE-01: every cell carries minimal-complete closure evidence."""
    cov = _only(tile_licensed_cells("ضَرَبَ"))
    assert len(cov.closure_evidence) == cov.length
    for ce in cov.closure_evidence:
        assert ce.minimally_complete is True
        assert ce.licensed_beginning is True
        assert ce.licensed_ending is True
        assert ce.no_open_demand is True


def test_CELL_BOUNDARY_01_boundary_carries_gate_witnesses():
    """CELL-BOUNDARY-01: boundary evidence bundles the canonical gate claims."""
    cov = _only(tile_licensed_cells("ضَرَبَ"))
    for be in cov.boundary_evidence:
        assert be.gate_beginning == "وادي:beginning:licensed"
        assert be.gate_ending == "وادي:ending:licensed"
        assert be.demand_discharged is True


# ─────────────────────────────────────────────────────────────────────────────
# CELL-COVERAGE — full coverage, no stranded units
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_COVERAGE_01_covering_covers_run_exactly():
    """CELL-COVERAGE-01: a covering's cells concatenate back to the run."""
    for surface in ("بَ", "بَا", "بَيت", "ضَرَبَ", *SHAPE_EXAMPLES.values()):
        for cov in tile_licensed_cells(surface).coverings:
            assert "".join(c.surface_form_vocalized for c in cov.cells) == surface
            assert cov.surface_form_vocalized == surface
            assert cov.identity_preserved is True


def test_CELL_COVERAGE_02_spans_contiguous_non_overlapping():
    """CELL-COVERAGE-02: cell spans are contiguous, ordered, gap-free."""
    cov = _only(tile_licensed_cells("ضَرَبَ"))
    spans = [
        (c.boundary_evidence.start_index, c.boundary_evidence.end_index)
        for c in cov.cells
    ]
    assert spans[0][0] == 0
    assert spans[-1][1] == len("ضَرَبَ")
    for a, b in zip(spans, spans[1:]):
        assert a[1] == b[0]  # no gap, no overlap


# ─────────────────────────────────────────────────────────────────────────────
# CELL-RESIDUAL — branches that fail full coverage become residuals
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_RESIDUAL_01_daraba_cvc_first_branch_is_residual():
    """CELL-RESIDUAL-01: ضَرَبَ covers as CV/CV/CV; the CVC-first branch residuals."""
    analysis = tile_licensed_cells("ضَرَبَ")
    cov = _only(analysis)
    assert cov.cell_shapes == ("CV", "CV", "CV")
    residual_branches = {r.branch_first_cell_surface for r in analysis.residuals}
    assert "ضَر" in residual_branches  # the CVC-first stranded branch
    for r in analysis.residuals:
        assert r.candidate_emitted is False
        assert r.fariq_claim.startswith("فارق:")


def test_CELL_RESIDUAL_02_shadda_has_no_covering():
    """CELL-RESIDUAL-02: شَاذّ admits no covering (shadda unsupported); residuals only."""
    analysis = tile_licensed_cells("شَاذّ")
    assert len(analysis.coverings) == 0
    assert len(analysis.residuals) >= 1
    # No shadda/gemination expansion: the shadda codepoint is never rewritten.
    for cov in analysis.coverings:  # (none)
        assert False


# ─────────────────────────────────────────────────────────────────────────────
# CELL-MULTIPLICITY — surface all coverings; never auto-disambiguate
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_MULTIPLICITY_01_all_coverings_surfaced_no_auto_pick():
    """CELL-MULTIPLICITY-01: coverings are returned as a tuple (plural); the
    runtime never auto-selects one. Under the current closed contract no licensed
    shape decomposes into smaller licensed shapes, so coverings are unique-or-
    empty — verified here — but the surfacing mechanism is multiplicity-capable."""
    for surface in ("بَ", "بَا", "بَيت", "ضَرَبَ", "مِن", "قَالْ", "قَالْتْ"):
        analysis = tile_licensed_cells(surface)
        assert isinstance(analysis.coverings, tuple)
        assert len(analysis.coverings) <= 1  # uniqueness property of this contract


# ─────────────────────────────────────────────────────────────────────────────
# CELL-COMPAT — closed cells reuse LicensedSyllableCandidate + feed Layer 5
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_COMPAT_01_cells_are_licensed_syllable_candidates():
    """CELL-COMPAT-01: closed cells are the existing Layer 4 type (no forked family)."""
    cov = _only(tile_licensed_cells("ضَرَبَ"))
    for c in cov.cells:
        assert isinstance(c, LicensedSyllableCandidate)
        assert c.potential_only is True


def test_CELL_COMPAT_02_cells_compose_in_layer5():
    """CELL-COMPAT-02: the cells feed Layer 5 compose_syllable_sequence."""
    cov = _only(tile_licensed_cells("ضَرَبَ"))
    candidate, invalidation = compose_syllable_sequence(cov.cells)
    assert invalidation is None
    assert candidate is not None
    assert candidate.length == 3
    assert candidate.constituent_shapes == ("CV", "CV", "CV")


# ─────────────────────────────────────────────────────────────────────────────
# CELL-POT / CELL-NONSEM — potential-only, non-semantic, registry untouched
# ─────────────────────────────────────────────────────────────────────────────


def test_CELL_POT_01_potential_only_and_not_introduced():
    """CELL-POT-01: analysis is potential-only with no semantic status."""
    a = tile_licensed_cells("ضَرَبَ")
    assert a.runtime_status == CELL_RUNTIME_STATUS
    assert a.meaning_status == "not_introduced"
    assert a.hukm_status == "not_introduced"
    assert a.irab_status == "not_introduced"
    assert a.dalalah_status == "not_introduced"
    assert a.reality_status == "not_introduced"
    assert _only(a).potential_only is True


def test_CELL_NONSEM_01_module_defines_no_forbidden_families():
    """CELL-NONSEM-01: no segmentation/word/lafz/semantic types in the module."""
    src = MODULE_SRC.read_text(encoding="utf-8")
    for forbidden in (
        "class SegmentCandidate",
        "class IntraSurfaceSegmentCandidate",
        "class LicensedSurfaceSegmentSequence",
        "class LicensedIntraSurfaceSegmentation",
        "class WordCandidate",
        "class LafzCandidate",
        "class HukmCandidate",
        "class RealityClaim",
        "class FinalMeaning",
    ):
        assert forbidden not in src, forbidden


def test_CELL_REG_01_canonical_registry_unchanged():
    """CELL-REG-01: the canonical master registry still has exactly 19 layers,
    and no registry layer outputs a cell-tiling type."""
    from qiyas_core.slot_geometry_core import build_master_registry_seed

    layers = list(build_master_registry_seed().all_layers())
    assert len(layers) == 19
    outputs = {s.branch.output_type for s in layers}
    assert "LicensedCellCovering" not in outputs


def test_CELL_L4_01_layer4_behavior_unchanged():
    """CELL-L4-01: Layer 4 still licenses a single CV token (the reuse hook added
    no behavior change)."""
    from qiyas_core.licensed_syllable import analyze_licensed_syllables

    la = analyze_licensed_syllables("بِ")
    assert len(la.candidates) == 1
    assert la.candidates[0].shape is AllowedSyllableShape.CV
