"""Licensed shadda expansion — enforcement tests (SHADDA-*).

Codepoint-faithful consonant doubling, potential-only evidence layer:
  Cّ + carried V  -> Cْ + C V   (عَدَّ -> عَدْدَ)
  Cّ no vowel     -> Cْ + C     (شَاذّ -> شَاذْذ, NOT شَاذْذَ)

The original surface is the identity carrier (never replaced); the shadda
codepoint is retained; the expansion is additive trace/evidence only.

Honest coverage note: under the current six-shape contract the bare trace
شَاذْذ reduces to CVVCC (a licensed coda), so cell-extension covers it. These
tests assert that truth; no vowel is invented and no residual is fabricated.
"""

from __future__ import annotations

from pathlib import Path

from qiyas_core.licensed_shadda_expansion import (
    SHADDA_RUNTIME_STATUS,
    LicensedShaddaExpansionEvidence,
    ShaddaExpansionResidual,
    cover_expanded_trace,
    expand_shadda,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_SRC = REPO_ROOT / "src" / "qiyas_core" / "licensed_shadda_expansion.py"
SIX_SHAPES = {"CV", "CVV", "CVC", "CVVC", "CVCC", "CVVCC"}


# ─────────────────────────────────────────────────────────────────────────────
# SHADDA-EXPAND — codepoint-faithful expansion
# ─────────────────────────────────────────────────────────────────────────────


def test_SHADDA_EXPAND_01_explicit_vowel_adda():
    """SHADDA-EXPAND-01: عَدَّ -> عَدْدَ (first copy sukun, second copy reuses fatha)."""
    ev = expand_shadda("عَدَّ").evidence
    assert isinstance(ev, LicensedShaddaExpansionEvidence)
    assert ev.trace.expanded_form == "عَدْدَ"
    assert ev.trace.site_carried_vowels == ("fatha",)
    assert ev.trace.site_bare == (False,)
    assert ev.final_consonant_bare is False


def test_SHADDA_EXPAND_02_bare_shaadd():
    """SHADDA-EXPAND-02: شَاذّ -> شَاذْذ (bare second consonant, no vowel)."""
    ev = expand_shadda("شَاذّ").evidence
    assert ev is not None
    assert ev.trace.expanded_form == "شَاذْذ"
    assert ev.trace.site_carried_vowels == (None,)
    assert ev.trace.site_bare == (True,)
    assert ev.final_consonant_bare is True


def test_SHADDA_EXPAND_03_shaadd_not_converted_to_fatha_form():
    """SHADDA-EXPAND-03: شَاذّ is NOT converted to شَاذْذَ — no final fatha invented."""
    ev = expand_shadda("شَاذّ").evidence
    assert ev.trace.expanded_form != "شَاذْذَ"
    assert ev.trace.expanded_form == "شَاذْذ"


def test_SHADDA_EXPAND_04_no_vowel_invented():
    """SHADDA-EXPAND-04: the bare expansion adds only sukun + a duplicate
    consonant — no short-vowel codepoint (fatha/damma/kasra) is introduced."""
    ev = expand_shadda("شَاذّ").evidence
    original_vowels = [c for c in "شَاذّ" if c in ("َ", "ُ", "ِ")]
    expanded_vowels = [c for c in ev.trace.expanded_form if c in ("َ", "ُ", "ِ")]
    assert expanded_vowels == original_vowels  # no new vowel


# ─────────────────────────────────────────────────────────────────────────────
# SHADDA-IDENTITY — identity carrier / source / shadda preservation
# ─────────────────────────────────────────────────────────────────────────────


def test_SHADDA_IDENTITY_01_original_surface_preserved():
    """SHADDA-IDENTITY-01: the original surface is returned unchanged."""
    a = expand_shadda("شَاذّ")
    assert a.original_surface == "شَاذّ"
    assert a.evidence.surface_form_vocalized == "شَاذّ"


def test_SHADDA_IDENTITY_02_original_codepoints_include_shadda():
    """SHADDA-IDENTITY-02: U+0651 shadda is retained in the original codepoints."""
    ev = expand_shadda("شَاذّ").evidence
    assert "U+0651" in ev.trace.original_codepoints
    assert ev.shadda_retained_in_identity is True


def test_SHADDA_IDENTITY_03_expansion_is_additive_not_replacement():
    """SHADDA-IDENTITY-03: the expanded form is additive trace; the source string
    object is not mutated/replaced."""
    src = "عَدَّ"
    a = expand_shadda(src)
    assert a.original_surface == src
    assert a.evidence.trace.expanded_form != src  # additive, distinct trace
    assert a.evidence.identity_preserved is True


# ─────────────────────────────────────────────────────────────────────────────
# SHADDA-FEED — additive integration with licensed cell extension
# ─────────────────────────────────────────────────────────────────────────────


def test_SHADDA_FEED_01_adda_trace_covers_cvc_cv():
    """SHADDA-FEED-01: عَدْدَ feeds cell-extension and covers using existing shapes."""
    ev = expand_shadda("عَدَّ").evidence
    cov = cover_expanded_trace(ev)
    shapes = {"/".join(c.cell_shapes) for c in cov.coverings}
    assert shapes == {"CVC/CV"}
    # Policy C multiplicity preserved (sukun attaches left or right), potential-only.
    assert len(cov.coverings) >= 2
    for c in cov.coverings:
        assert c.potential_only is True


def test_SHADDA_FEED_02_bare_shaadd_trace_covers_as_cvvcc_not_residual():
    """SHADDA-FEED-02 (honest coverage): شَاذْذ reduces to CVVCC — a licensed coda
    shape — so the bare trace IS covered as a single CVVCC cell, NOT residual.
    No vowel is invented and the contract is unchanged; a bare final consonant
    is a permitted coda (as in قَالْتْ)."""
    ev = expand_shadda("شَاذّ").evidence
    cov = cover_expanded_trace(ev)
    shapes = {"/".join(c.cell_shapes) for c in cov.coverings}
    assert shapes == {"CVVCC"}


def test_SHADDA_FEED_03_only_six_shapes_no_ccv_no_new_shape():
    """SHADDA-FEED-03: every covering of an expanded trace uses only the six
    licensed shapes — no CCV, no new shape admitted."""
    for surface in ("عَدَّ", "شَاذّ"):
        ev = expand_shadda(surface).evidence
        for c in cover_expanded_trace(ev).coverings:
            for shp in c.cell_shapes:
                assert shp in SIX_SHAPES, (surface, shp)


# ─────────────────────────────────────────────────────────────────────────────
# SHADDA-RESIDUAL / SHADDA-LAYER — residual + no-candidate-from-this-layer
# ─────────────────────────────────────────────────────────────────────────────


def test_SHADDA_RESIDUAL_01_shadda_without_base_is_residual():
    """SHADDA-RESIDUAL-01: a shadda with no base consonant yields a residual,
    no expansion evidence."""
    a = expand_shadda("ّ")  # bare shadda alone
    assert a.evidence is None
    assert len(a.residuals) == 1
    assert isinstance(a.residuals[0], ShaddaExpansionResidual)
    assert a.residuals[0].fariq_claim.startswith("فارق:")


def test_SHADDA_LAYER_01_layer_emits_evidence_not_a_candidate():
    """SHADDA-LAYER-01: the shadda layer produces evidence/trace, never a
    candidate — it does not by itself force any surface to be valid."""
    a = expand_shadda("شَاذّ")
    assert isinstance(a.evidence, LicensedShaddaExpansionEvidence)
    # no field named *Candidate is produced by this layer
    assert not hasattr(a.evidence, "candidate")


# ─────────────────────────────────────────────────────────────────────────────
# SHADDA-POT / SHADDA-NONSEM — potential-only, non-semantic, registry untouched
# ─────────────────────────────────────────────────────────────────────────────


def test_SHADDA_POT_01_potential_only_and_not_introduced():
    """SHADDA-POT-01: potential-only; no semantic status introduced."""
    a = expand_shadda("عَدَّ")
    assert a.runtime_status == SHADDA_RUNTIME_STATUS
    assert a.meaning_status == "not_introduced"
    assert a.hukm_status == "not_introduced"
    assert a.irab_status == "not_introduced"
    assert a.dalalah_status == "not_introduced"
    assert a.reality_status == "not_introduced"
    assert a.evidence.potential_only is True


def test_SHADDA_NONSEM_01_module_defines_no_forbidden_families():
    """SHADDA-NONSEM-01: no word/lafz/segment/semantic types in the module."""
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


def test_SHADDA_CONTRACT_01_six_shape_contract_unchanged():
    """SHADDA-CONTRACT-01: the Layer 4 closed contract is still the six shapes."""
    from qiyas_core.licensed_syllable import ALLOWED_SYLLABLE_SHAPES

    assert {s.value for s in ALLOWED_SYLLABLE_SHAPES} == SIX_SHAPES


def test_SHADDA_REG_01_canonical_registry_unchanged():
    """SHADDA-REG-01: the canonical master registry still has 19 layers."""
    from qiyas_core.slot_geometry_core import build_master_registry_seed

    assert len(list(build_master_registry_seed().all_layers())) == 19
