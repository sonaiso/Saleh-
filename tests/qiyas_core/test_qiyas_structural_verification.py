"""Unified structural verification — enforcement tests (VERIFY-*).

The authoritative public structural verifier consumes licensed shadda expansion
before the final covering report. Direct single-cell Layer 4 remains a labeled
diagnostic only and never overrides the licensed shadda path. Potential-only.
"""

from __future__ import annotations

from pathlib import Path

from qiyas_core.qiyas_structural_verification import (
    COVERED_DIRECT,
    COVERED_VIA_SHADDA_EXPANSION,
    RESIDUAL,
    STRUCTURAL_RUNTIME_STATUS,
    verify_token_structure,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_SRC = REPO_ROOT / "src" / "qiyas_core" / "qiyas_structural_verification.py"
SIX_SHAPES = {"CV", "CVV", "CVC", "CVVC", "CVCC", "CVVCC"}


def _all_shapes(v) -> set[str]:
    out: set[str] = set()
    for cov in v.direct_covering_shapes + v.shadda_expansion_covering_shapes:
        out.update(cov)
    return out


# ─────────────────────────────────────────────────────────────────────────────
# VERIFY-SHADDA — شَاذّ final status via licensed shadda expansion
# ─────────────────────────────────────────────────────────────────────────────


def test_VERIFY_SHADDA_01_shaadd_final_status_is_covered_via_shadda_expansion():
    v = verify_token_structure("شَاذّ")
    assert v.final_status == COVERED_VIA_SHADDA_EXPANSION


def test_VERIFY_SHADDA_02_identity_and_codepoints_preserved():
    v = verify_token_structure("شَاذّ")
    assert v.identity_surface == "شَاذّ"
    assert v.identity_preserved is True
    assert "U+0651" in v.identity_codepoints  # shadda retained in identity


def test_VERIFY_SHADDA_03_expansion_trace_and_covering():
    v = verify_token_structure("شَاذّ")
    assert v.shadda_expansion_trace == "شَاذْذ"
    assert ("CVVCC",) in v.shadda_expansion_covering_shapes


def test_VERIFY_SHADDA_04_no_vowel_invented_no_source_replacement():
    v = verify_token_structure("شَاذّ")
    assert v.vowel_invented is False
    assert v.identity_surface == "شَاذّ"  # source unchanged


def test_VERIFY_SHADDA_05_direct_layer4_diagnostic_visible_but_not_final():
    v = verify_token_structure("شَاذّ")
    # The direct Layer 4 diagnostic remains visible...
    assert v.direct_layer4_diagnostic_status == "invalid_direct_shadda_unsupported"
    assert "shadda" in v.direct_layer4_diagnostic_reason
    # ...but does NOT set the final public status.
    assert v.final_status == COVERED_VIA_SHADDA_EXPANSION


def test_VERIFY_SHADDA_06_adda_expansion_and_covering():
    v = verify_token_structure("عَدَّ")
    assert v.final_status == COVERED_VIA_SHADDA_EXPANSION
    assert v.shadda_expansion_trace == "عَدْدَ"
    assert ("CVC", "CV") in v.shadda_expansion_covering_shapes
    # Policy-C multiplicity surfaced (sukun attaches left or right).
    assert len(v.shadda_expansion_covering_shapes) >= 2
    assert v.vowel_invented is False


# ─────────────────────────────────────────────────────────────────────────────
# VERIFY-DIRECT — direct covering reports covered_direct
# ─────────────────────────────────────────────────────────────────────────────


def test_VERIFY_DIRECT_01_six_shape_direct_examples():
    cases = {
        "بَ": "CV",
        "مَا": "CVV",
        "مِن": "CVC",
        "بَاب": "CVVC",
        "بَيت": "CVCC",
    }
    for surface, shape in cases.items():
        v = verify_token_structure(surface)
        assert v.final_status == COVERED_DIRECT, surface
        assert (shape,) in v.direct_covering_shapes, (surface, shape)
        assert v.shadda_present is False


def test_VERIFY_DIRECT_02_daraba_covered_direct_via_cell_extension():
    """ضَرَبَ is covered_direct via cell-extension (CV/CV/CV) even though the
    single-cell Layer 4 diagnostic invalidates it."""
    v = verify_token_structure("ضَرَبَ")
    assert v.final_status == COVERED_DIRECT
    assert ("CV", "CV", "CV") in v.direct_covering_shapes
    assert v.direct_layer4_diagnostic_status == "invalid_direct"


# ─────────────────────────────────────────────────────────────────────────────
# VERIFY-RESIDUAL — neither path covers
# ─────────────────────────────────────────────────────────────────────────────


def test_VERIFY_RESIDUAL_01_non_arabic_is_residual():
    v = verify_token_structure("hello")
    assert v.final_status == RESIDUAL


def test_VERIFY_RESIDUAL_02_uncoverable_shadda_is_residual_diagnostics_preserved():
    """شّ expands (شْش) but does not cover → residual; diagnostics preserved."""
    v = verify_token_structure("شّ")
    assert v.final_status == RESIDUAL
    assert v.shadda_expansion_trace == "شْش"          # expansion evidence preserved
    assert v.shadda_expansion_covering_shapes == ()   # not covered
    assert v.direct_layer4_diagnostic_status.startswith("invalid")  # diagnostic visible


# ─────────────────────────────────────────────────────────────────────────────
# VERIFY-INVARIANTS — shapes, registry, statuses, no semantic surface
# ─────────────────────────────────────────────────────────────────────────────


def test_VERIFY_INV_01_only_six_shapes_no_ccv_no_new_shape():
    for surface in ("شَاذّ", "عَدَّ", "بَ", "مَا", "مِن", "بَاب", "بَيت", "ضَرَبَ"):
        v = verify_token_structure(surface)
        assert _all_shapes(v) <= SIX_SHAPES, (surface, _all_shapes(v))


def test_VERIFY_INV_02_potential_only_and_not_introduced():
    v = verify_token_structure("شَاذّ")
    assert v.runtime_status == STRUCTURAL_RUNTIME_STATUS
    assert v.meaning_status == "not_introduced"
    assert v.hukm_status == "not_introduced"
    assert v.irab_status == "not_introduced"
    assert v.dalalah_status == "not_introduced"
    assert v.reality_status == "not_introduced"


def test_VERIFY_INV_03_registry_count_unchanged():
    from qiyas_core.slot_geometry_core import build_master_registry_seed

    assert len(list(build_master_registry_seed().all_layers())) == 19


def test_VERIFY_INV_04_module_defines_no_forbidden_families():
    src = MODULE_SRC.read_text(encoding="utf-8")
    for forbidden in (
        "class WordCandidate",
        "class LafzCandidate",
        "class SegmentCandidate",
        "class HukmCandidate",
        "class RealityClaim",
        "class FinalMeaning",
    ):
        assert forbidden not in src, forbidden


def test_VERIFY_INV_05_final_status_vocabulary_is_exactly_three():
    assert {COVERED_DIRECT, COVERED_VIA_SHADDA_EXPANSION, RESIDUAL} == {
        "covered_direct",
        "covered_via_shadda_expansion",
        "residual",
    }
