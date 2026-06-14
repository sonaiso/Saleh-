"""Layer 5 LicensedSyllableSequenceCandidate — enforcement tests (LAYER5-*).

Authorization: narrow Layer 5 authorization (2026-06-14), potential-only,
not a global unfreeze, not REC-6, not Layer 6+.

These tests prove:
  LAYER5-COMPOSE-*  — valid adjacent Layer 4 candidates compose
  LAYER5-INVALID-*  — non-adjacency / disorder / unlicensed / drift invalidate
  LAYER5-IDENT-*    — surface + codepoint identity preserved
  LAYER5-POT-*      — potential-only, no semantic statuses
  LAYER5-NONSEM-*   — no wordhood/meaning/grammar/hukm/... in API or render
  LAYER5-REG-*      — canonical 19-layer registry unchanged
  LAYER5-L4-*       — Layer 4 behavior unchanged
"""

from __future__ import annotations

from pathlib import Path

from qiyas_core.licensed_syllable import (
    CANDIDATE_RUNTIME_STATUS,
    AllowedSyllableShape,
    BoundaryEvidence,
    LicensedSyllableCandidate,
    PhoneticEconomyEvidence,
    SyllableShapeEvidence,
    analyze_licensed_syllables,
)
from qiyas_core.licensed_syllable_sequence import (
    LAYER5_RUNTIME_STATUS,
    SEQUENCE_CANDIDATE_RUNTIME_STATUS,
    LicensedSyllableSequenceCandidate,
    analyze_licensed_syllable_sequence,
    compose_syllable_sequence,
    render_licensed_syllable_sequence_analysis,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_SRC = REPO_ROOT / "src" / "qiyas_core" / "licensed_syllable_sequence.py"

EXPECTED_REGISTRY_LAYER_COUNT = 19


def _cp(surface: str) -> tuple[str, ...]:
    return tuple(f"U+{ord(ch):04X}" for ch in surface)


def _l4(
    token_index: int,
    surface: str,
    start: int,
    end: int,
    *,
    identity: bool = True,
    boundary: bool = True,
    licensed: bool = True,
) -> LicensedSyllableCandidate:
    """Construct a Layer 4 candidate for composition tests."""
    cps = _cp(surface)
    boundary_ev = BoundaryEvidence(
        token_index=token_index,
        start_index=start,
        end_index=end,
        preceding_text="",
        following_text="",
        has_left_boundary=True,
        has_right_boundary=True,
        boundary_preserved=boundary,
        source="test",
    )
    shape_ev = SyllableShapeEvidence(
        shape=AllowedSyllableShape.CV,
        surface_form_vocalized=surface,
        surface_codepoints=cps,
        surface_codepoint_names=tuple("X" for _ in surface),
        shape_reason="test",
        allowed=True,
    )
    econ_ev = PhoneticEconomyEvidence(
        minimal_complete_syllable=True,
        no_unnecessary_expansion=True,
        shape_allowed=True,
        boundary_preserved=boundary,
        identity_preserved=identity,
        economy_satisfied=True,
        reason="test",
    )
    return LicensedSyllableCandidate(
        token_index=token_index,
        surface_form_vocalized=surface,
        surface_codepoints=cps,
        surface_codepoint_names=tuple("X" for _ in surface),
        shape=AllowedSyllableShape.CV,
        boundary_evidence=boundary_ev,
        shape_evidence=shape_ev,
        economy_evidence=econ_ev,
        identity_preserved=identity,
        potential_only=licensed,
        runtime_status=CANDIDATE_RUNTIME_STATUS if licensed else "blocked",
    )


def _valid_run() -> list[LicensedSyllableCandidate]:
    return [
        _l4(0, "بِ", 0, 2),
        _l4(1, "ضَ", 3, 5),
        _l4(2, "وَ", 6, 8),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-COMPOSE — valid composition
# ─────────────────────────────────────────────────────────────────────────────


def test_LAYER5_COMPOSE_01_valid_adjacent_candidates_compose():
    """LAYER5-COMPOSE-01: adjacent, ordered, licensed candidates compose."""
    candidate, invalidation = compose_syllable_sequence(_valid_run())
    assert invalidation is None
    assert isinstance(candidate, LicensedSyllableSequenceCandidate)
    assert candidate.length == 3
    assert candidate.constituent_token_indices == (0, 1, 2)
    assert candidate.token_index_span == (0, 2)
    assert candidate.constituent_shapes == ("CV", "CV", "CV")


def test_LAYER5_COMPOSE_02_end_to_end_analyze_composes():
    """LAYER5-COMPOSE-02: analyze over real space-separated CV tokens composes."""
    analysis = analyze_licensed_syllable_sequence("بِ ضَ وَ يَ")
    assert len(analysis.candidates) == 1
    assert len(analysis.invalidations) == 0
    assert analysis.candidates[0].length == 4


def test_LAYER5_COMPOSE_03_single_candidate_is_a_trivial_sequence():
    """LAYER5-COMPOSE-03: a single licensed candidate composes (vacuous adjacency)."""
    candidate, invalidation = compose_syllable_sequence([_l4(0, "بِ", 0, 2)])
    assert invalidation is None
    assert candidate is not None and candidate.length == 1


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-INVALID — invalidation paths (no candidate emitted)
# ─────────────────────────────────────────────────────────────────────────────


def test_LAYER5_INVALID_01_non_adjacent_invalidates():
    """LAYER5-INVALID-01: token-index gap invalidates."""
    candidate, invalidation = compose_syllable_sequence(
        [_l4(0, "بِ", 0, 2), _l4(2, "ضَ", 6, 8)]
    )
    assert candidate is None
    assert invalidation is not None and invalidation.adjacent is False


def test_LAYER5_INVALID_02_out_of_order_invalidates():
    """LAYER5-INVALID-02: descending token order invalidates."""
    candidate, invalidation = compose_syllable_sequence(
        [_l4(1, "ضَ", 3, 5), _l4(0, "بِ", 0, 2)]
    )
    assert candidate is None
    assert invalidation is not None and invalidation.ordered is False


def test_LAYER5_INVALID_03_empty_invalidates():
    """LAYER5-INVALID-03: no lower candidates invalidates."""
    candidate, invalidation = compose_syllable_sequence([])
    assert candidate is None
    assert invalidation is not None


def test_LAYER5_INVALID_04_unlicensed_lower_invalidates():
    """LAYER5-INVALID-04: an unlicensed lower candidate invalidates."""
    candidate, invalidation = compose_syllable_sequence(
        [_l4(0, "بِ", 0, 2), _l4(1, "ضَ", 3, 5, licensed=False)]
    )
    assert candidate is None
    assert invalidation is not None


def test_LAYER5_INVALID_05_identity_drift_invalidates():
    """LAYER5-INVALID-05: identity drift in a lower candidate invalidates."""
    candidate, invalidation = compose_syllable_sequence(
        [_l4(0, "بِ", 0, 2), _l4(1, "ضَ", 3, 5, identity=False)]
    )
    assert candidate is None
    assert invalidation is not None and invalidation.identity_preserved is False


def test_LAYER5_INVALID_06_boundary_drift_invalidates():
    """LAYER5-INVALID-06: boundary drift in a lower candidate invalidates."""
    candidate, invalidation = compose_syllable_sequence(
        [_l4(0, "بِ", 0, 2), _l4(1, "ضَ", 3, 5, boundary=False)]
    )
    assert candidate is None
    assert invalidation is not None and invalidation.boundary_preserved is False


def test_LAYER5_INVALID_07_overlapping_spans_invalidate():
    """LAYER5-INVALID-07: overlapping character spans invalidate."""
    candidate, invalidation = compose_syllable_sequence(
        [_l4(0, "بِ", 0, 5), _l4(1, "ضَ", 3, 8)]
    )
    assert candidate is None
    assert invalidation is not None


def test_LAYER5_INVALID_08_no_candidate_emitted_on_any_invalidation():
    """LAYER5-INVALID-08: every invalidation path yields no candidate."""
    bad_inputs = (
        [],
        [_l4(0, "بِ", 0, 2), _l4(2, "ضَ", 6, 8)],          # gap
        [_l4(1, "ضَ", 3, 5), _l4(0, "بِ", 0, 2)],          # disorder
        [_l4(0, "بِ", 0, 2, licensed=False)],              # unlicensed
        [_l4(0, "بِ", 0, 2, identity=False)],              # identity drift
        [_l4(0, "بِ", 0, 2, boundary=False)],              # boundary drift
    )
    for inp in bad_inputs:
        candidate, invalidation = compose_syllable_sequence(inp)
        assert candidate is None
        assert invalidation is not None and invalidation.candidate_emitted is False


def test_LAYER5_INVALID_09_unlicensed_lower_from_analyze_invalidates():
    """LAYER5-INVALID-09: a multi-syllable token Layer 4 cannot license makes the
    sequence invalidate (missing/unlicensed lower units)."""
    analysis = analyze_licensed_syllable_sequence("ضَرَبَ")
    assert len(analysis.candidates) == 0
    assert len(analysis.invalidations) == 1


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-IDENT — identity / surface / codepoint preservation
# ─────────────────────────────────────────────────────────────────────────────


def test_LAYER5_IDENT_01_surface_round_trip():
    """LAYER5-IDENT-01: surface_form_vocalized is the ordered join of constituents."""
    candidate, _ = compose_syllable_sequence(_valid_run())
    assert candidate is not None
    assert " ".join(candidate.constituent_surfaces) == candidate.surface_form_vocalized


def test_LAYER5_IDENT_02_exact_codepoint_identity_preserved():
    """LAYER5-IDENT-02: surface codepoints match the composed surface exactly."""
    candidate, _ = compose_syllable_sequence(_valid_run())
    assert candidate is not None
    assert candidate.surface_codepoints == _cp(candidate.surface_form_vocalized)


def test_LAYER5_IDENT_03_constituent_surfaces_preserved_verbatim():
    """LAYER5-IDENT-03: each constituent surface is preserved unchanged."""
    run = _valid_run()
    candidate, _ = compose_syllable_sequence(run)
    assert candidate is not None
    assert candidate.constituent_surfaces == tuple(c.surface_form_vocalized for c in run)


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-POT — potential-only, non-semantic statuses
# ─────────────────────────────────────────────────────────────────────────────


def test_LAYER5_POT_01_candidate_is_potential_only():
    """LAYER5-POT-01: emitted candidate is potential-only."""
    candidate, _ = compose_syllable_sequence(_valid_run())
    assert candidate is not None
    assert candidate.potential_only is True
    assert candidate.runtime_status == SEQUENCE_CANDIDATE_RUNTIME_STATUS


def test_LAYER5_POT_02_analysis_statuses_not_introduced():
    """LAYER5-POT-02: the analysis bundle introduces no semantic status."""
    analysis = analyze_licensed_syllable_sequence("بِ ضَ")
    assert analysis.runtime_status == LAYER5_RUNTIME_STATUS
    assert analysis.meaning_status == "not_introduced"
    assert analysis.hukm_status == "not_introduced"
    assert analysis.irab_status == "not_introduced"
    assert analysis.dalalah_status == "not_introduced"
    assert analysis.reality_status == "not_introduced"


def test_LAYER5_COMPOSE_04_sequence_with_cvcc_constituent():
    """LAYER5-COMPOSE-04: Layer 5 composes a sequence that includes a Layer 4
    CVCC candidate (e.g. 'بَيت'), now that CVCC is in the closed contract."""
    analysis = analyze_licensed_syllable_sequence("بَ مَا مِن بَيت")
    assert len(analysis.candidates) == 1
    assert len(analysis.invalidations) == 0
    candidate = analysis.candidates[0]
    assert candidate.length == 4
    assert "CVCC" in candidate.constituent_shapes
    assert candidate.identity_preserved is True


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-NONSEM — no semantic / grammatical surface in API or render
# ─────────────────────────────────────────────────────────────────────────────

FORBIDDEN_TERMS = (
    "wordhood",
    "lafz",
    "root",
    "wazn",
    "morphology",
    "grammar",
    "hukm",
    "i'rab",
    "dalalah",
    "tafsir",
    "meaning",
    "realityclaim",
    "finalmeaning",
)
BOUNDARY_HEADER = "## Constitutional Boundary"


def test_LAYER5_NONSEM_01_render_has_no_positive_semantic_terms():
    """LAYER5-NONSEM-01: forbidden terms appear only inside the negation
    (Constitutional Boundary) section of the render, never as positive claims."""
    analysis = analyze_licensed_syllable_sequence("بِ ضَ وَ يَ")
    render = render_licensed_syllable_sequence_analysis(analysis)
    boundary_index = render.find(BOUNDARY_HEADER)
    assert boundary_index >= 0
    head = render[:boundary_index].lower()
    for term in FORBIDDEN_TERMS:
        assert term not in head, (
            f"forbidden term {term!r} appears outside the negation section"
        )


def test_LAYER5_NONSEM_02_public_api_names_have_no_semantic_terms():
    """LAYER5-NONSEM-02: public dataclass/function names carry no semantic term."""
    import qiyas_core.licensed_syllable_sequence as m

    public = [n for n in dir(m) if not n.startswith("_")]
    for name in public:
        low = name.lower()
        for term in FORBIDDEN_TERMS:
            assert term not in low, f"public name {name!r} contains {term!r}"


def test_LAYER5_NONSEM_03_module_defines_no_forbidden_output_types():
    """LAYER5-NONSEM-03: the module source defines no forbidden higher-layer types."""
    src = MODULE_SRC.read_text(encoding="utf-8")
    for forbidden in (
        "class WordCandidate",
        "class LafzCandidate",
        "class DalalahCandidate",
        "class HukmCandidate",
        "class RealityClaim",
        "class FinalMeaning",
    ):
        assert forbidden not in src, f"module defines {forbidden!r}"


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-REG — canonical registry untouched
# ─────────────────────────────────────────────────────────────────────────────


def test_LAYER5_REG_01_canonical_registry_count_unchanged():
    """LAYER5-REG-01: the canonical master registry still has exactly 19 layers."""
    from qiyas_core.slot_geometry_core import build_master_registry_seed

    layers = list(build_master_registry_seed().all_layers())
    assert len(layers) == EXPECTED_REGISTRY_LAYER_COUNT


def test_LAYER5_REG_02_layer5_type_not_in_registry():
    """LAYER5-REG-02: no registry layer outputs the Layer 5 sequence type."""
    from qiyas_core.slot_geometry_core import build_master_registry_seed

    output_types = {
        s.branch.output_type for s in build_master_registry_seed().all_layers()
    }
    assert "LicensedSyllableSequenceCandidate" not in output_types


# ─────────────────────────────────────────────────────────────────────────────
# LAYER5-L4 — Layer 4 behavior unchanged
# ─────────────────────────────────────────────────────────────────────────────


def test_LAYER5_L4_01_layer4_still_licenses_cv_token():
    """LAYER5-L4-01: Layer 4 still licenses a CV token independently of Layer 5."""
    la = analyze_licensed_syllables("بِ")
    assert len(la.candidates) == 1
    assert la.candidates[0].shape is AllowedSyllableShape.CV
    assert la.runtime_status == "layer4_potential_only"
