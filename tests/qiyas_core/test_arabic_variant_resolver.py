"""Tests for ArabicVariantResolver — runtime producer.

Pins the constitutional contract of
``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` §3 (producer discipline) and
``ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md`` §§4-5 (admissibility):

  * ``ArabicVariantResolver`` is the reserved §3.1 producer name.
  * Returns ``ArabicVariantResolutionEvidence | None`` only —
    never a ``Candidate`` of any type.
  * Closed consumption surface: only
    ``SlotGeometryCandidate(length=1, construction_mode="seed")`` plus
    ``ArabicArticulationRegistry`` metadata read-only; no kernel, no
    MIU adapter, no raw text, no tokenizer.
  * Absence / conflict / malformed / unlicensed-basis ⇒ ``None``
    (NEVER BLOCK; CLAUDE.md §4 invariant 7, contract §7).
  * ``(و, non_madd)`` and ``(ي, non_madd)`` licensed by
    ``haraka_function_self`` only in this PR; both other admissible
    bases (``intra_utterance_position`` secondary;
    ``haraka_function_before`` for madd) are deferred.
  * ``ا`` is future-extensibility only ⇒ ``None``.
  * No forbidden Candidate types (Word / Lafz / Sentence / Paragraph
    / Dalalah / FinalMeaning / Hukm / Reality / FinalCaseJudgment /
    MinimalUnitReadinessCandidate).
  * No ``QiyasKernel`` import / invocation.
  * No MIU adapter import.
  * No registry mutation (read-only).
"""

from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

from qiyas_core import arabic_variant_resolver as avr
from qiyas_core.arabic_variant_resolution_evidence import (
    ArabicVariantResolutionEvidence,
    FIXED_GEOMETRY_CONSTRUCTION_MODE,
    FIXED_GEOMETRY_LAYER,
    FIXED_GEOMETRY_LENGTH,
)
from qiyas_core.arabic_variant_resolver import (
    ArabicVariantResolver,
    resolve_arabic_variant,
)


# ---------------------------------------------------------------------------
# Lightweight fixture matching the SlotGeometryCandidate protocol
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class _GeomFixture:
    candidate_type: str
    layer: str
    candidate_id: str
    identity_ids: tuple[str, ...]
    trace_ids: tuple[str, ...]


# Hex codepoints (no 0x prefix), matching the MIU adapter convention.
_WAW = "0648"      # و
_YAA = "064a"      # ي
_ALIF = "0627"     # ا
_BAA = "0628"      # ب
_FATHA = "064e"    # ـَ
_DAMMA = "064f"    # ـُ
_KASRA = "0650"    # ـِ
_SUKUN = "0652"    # ـْ


def _make_geom(
    *,
    letter_cp: str,
    haraka_cp: str | None = _FATHA,
    candidate_type: str = "SlotGeometryCandidate",
    layer: str = FIXED_GEOMETRY_LAYER,
    candidate_id: str = "geom:fixture:test",
    extra_identity: tuple[str, ...] = (),
    length: int = FIXED_GEOMETRY_LENGTH,
    mode: str = FIXED_GEOMETRY_CONSTRUCTION_MODE,
) -> _GeomFixture:
    identity_ids: tuple[str, ...] = (
        f"identity:codepoint:{letter_cp}",
    )
    if haraka_cp is not None:
        identity_ids = identity_ids + (f"identity:codepoint:{haraka_cp}",)
    identity_ids = identity_ids + extra_identity
    trace_ids = (
        f"trace:fixture:{candidate_id}",
        f"trace:slot_geometry:length:{length}",
        f"trace:slot_geometry:construction_mode:{mode}",
    )
    return _GeomFixture(
        candidate_type=candidate_type,
        layer=layer,
        candidate_id=candidate_id,
        identity_ids=identity_ids,
        trace_ids=trace_ids,
    )


# ---------------------------------------------------------------------------
# 1. Resolver class exists
# ---------------------------------------------------------------------------


def test_resolver_class_exists_and_is_dataclass() -> None:
    """§3.1: ``ArabicVariantResolver`` is the reserved producer name."""
    assert dataclasses.is_dataclass(ArabicVariantResolver)


def test_resolver_class_is_frozen() -> None:
    """The producer is stateless; the class is a frozen dataclass."""
    resolver = ArabicVariantResolver()
    with pytest.raises(dataclasses.FrozenInstanceError):
        resolver.some_field = "x"  # type: ignore[attr-defined]


def test_resolver_instances_are_equal() -> None:
    """Stateless producers: two instances compare equal."""
    assert ArabicVariantResolver() == ArabicVariantResolver()


# ---------------------------------------------------------------------------
# 2. Returns ArabicVariantResolutionEvidence | None only
# ---------------------------------------------------------------------------


def test_resolver_returns_evidence_for_licensed_case() -> None:
    """§3.2: licensed (و, non_madd) case returns the Evidence carrier."""
    resolver = ArabicVariantResolver()
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    result = resolver.resolve(geom)
    assert isinstance(result, ArabicVariantResolutionEvidence)


def test_resolver_returns_none_for_out_of_scope_symbol() -> None:
    """§3.2: out-of-scope symbol returns None (NEVER a Candidate)."""
    resolver = ArabicVariantResolver()
    geom = _make_geom(letter_cp=_BAA, haraka_cp=_FATHA)
    assert resolver.resolve(geom) is None


def test_callable_form_mirrors_resolve_method() -> None:
    """``resolver(geom)`` is equivalent to ``resolver.resolve(geom)``."""
    resolver = ArabicVariantResolver()
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    a = resolver.resolve(geom)
    b = resolver(geom)
    assert (a is None) == (b is None)
    assert a.symbol == b.symbol  # type: ignore[union-attr]
    assert a.selected_variant == b.selected_variant  # type: ignore[union-attr]
    assert a.selection_basis == b.selection_basis  # type: ignore[union-attr]


def test_module_level_convenience_function_works() -> None:
    """Module-level convenience function mirrors the class method."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    direct = ArabicVariantResolver().resolve(geom)
    convenience = resolve_arabic_variant(geom)
    assert direct is not None and convenience is not None
    assert direct.symbol == convenience.symbol
    assert direct.selected_variant == convenience.selected_variant
    assert direct.selected_entry_id == convenience.selected_entry_id


# ---------------------------------------------------------------------------
# 3. No Candidate fields, no Candidate production
# ---------------------------------------------------------------------------


def test_returned_evidence_has_no_candidate_shape_fields() -> None:
    """§2 of resolution contract: Evidence carrier ≠ Candidate."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert not hasattr(result, "candidate_type")
    assert not hasattr(result, "status")
    assert not hasattr(result, "output_flags")


# ---------------------------------------------------------------------------
# 4-7. Scope guards via AST imports
# ---------------------------------------------------------------------------


def _imported_module_names(module) -> set[str]:
    """AST-based set of dotted module names imported by ``module``.

    Avoids matching contract citations in docstrings — only real
    ``import`` / ``from … import`` statements count."""
    tree = ast.parse(inspect.getsource(module))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
    return imported


def test_resolver_does_not_import_miu_adapter() -> None:
    """§3.3: the producer does not call back into MIU readiness."""
    imported = _imported_module_names(avr)
    for mod in imported:
        assert "minimal_unit_readiness" not in mod, (
            f"MIU import is forbidden in this PR: {mod}"
        )


def test_resolver_does_not_import_qiyas_kernel() -> None:
    """§3.3: the producer does not invoke ``QiyasKernel.apply``;
    the module imports nothing kernel-related."""
    imported = _imported_module_names(avr)
    for mod in imported:
        assert "kernel" not in mod, (
            f"kernel import is forbidden: {mod}"
        )


def test_resolver_uses_only_read_only_registry_api() -> None:
    """§4 item 2 + §3.3: registry is metadata-only and read-only.
    The module must not call any mutation helper."""
    source = inspect.getsource(avr)
    assert "save_articulation" not in source
    assert "set_articulation" not in source
    assert "update_articulation" not in source
    # Read-only reader is permissible and is used.
    assert "get_articulations_by_symbol" in source


def test_module_does_not_define_forbidden_types() -> None:
    """§3.3 + §8 of resolution contract."""
    forbidden = (
        "WordCandidate",
        "LafzCandidate",
        "SentenceCandidate",
        "ParagraphCandidate",
        "DalalahCandidate",
        "FinalMeaning",
        "HukmCandidate",
        "RealityClaim",
        "FinalCaseJudgment",
        "MinimalUnitReadinessCandidate",
        "ArabicVariantResolutionCandidate",
        "SlotCandidate",
        "SlotGeometryCandidate",
    )
    for name in forbidden:
        assert not hasattr(avr, name), (
            f"forbidden symbol must not be defined here: {name}"
        )


# ---------------------------------------------------------------------------
# 8. Absence ⇒ None
# ---------------------------------------------------------------------------


def test_wrong_candidate_type_returns_none() -> None:
    """§4 surface gate: only SlotGeometryCandidate is admissible."""
    geom = _make_geom(letter_cp=_WAW, candidate_type="SlotCandidate")
    assert ArabicVariantResolver().resolve(geom) is None


def test_wrong_layer_returns_none() -> None:
    """§4 surface gate: only the SlotGeometryQiyas layer is admissible."""
    geom = _make_geom(letter_cp=_WAW, layer="SlotQiyas")
    assert ArabicVariantResolver().resolve(geom) is None


def test_length_greater_than_one_returns_none() -> None:
    """§4 / §6.1: only length=1 seed geometries are admissible."""
    geom = _make_geom(letter_cp=_WAW, length=2)
    assert ArabicVariantResolver().resolve(geom) is None


def test_construction_mode_extension_returns_none() -> None:
    """§4 / §6.1: only construction_mode='seed' is admissible."""
    geom = _make_geom(letter_cp=_WAW, mode="extension")
    assert ArabicVariantResolver().resolve(geom) is None


def test_absence_of_haraka_returns_none() -> None:
    """No haraka codepoint on the geometry ⇒ no licensed basis ⇒
    None (CLAUDE.md §4 invariant 7: malformed ⇒ DEFER, never BLOCK)."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=None)
    assert ArabicVariantResolver().resolve(geom) is None


def test_absence_of_letter_returns_none() -> None:
    """No Arabic-letter codepoint in identity_ids ⇒ None
    (geometry not interpretable by the resolver)."""
    geom = _GeomFixture(
        candidate_type="SlotGeometryCandidate",
        layer=FIXED_GEOMETRY_LAYER,
        candidate_id="geom:no_letter",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=(
            "trace:slot_geometry:length:1",
            "trace:slot_geometry:construction_mode:seed",
        ),
    )
    assert ArabicVariantResolver().resolve(geom) is None


# ---------------------------------------------------------------------------
# 9. Conflict ⇒ None
# ---------------------------------------------------------------------------


def test_unscoped_single_variant_symbol_returns_none() -> None:
    """§5: ب has only one registry entry; the resolver does not apply
    even when surface conditions match."""
    geom = _make_geom(letter_cp=_BAA, haraka_cp=_FATHA)
    assert ArabicVariantResolver().resolve(geom) is None


# ---------------------------------------------------------------------------
# 10. Unlicensed basis ⇒ None
# ---------------------------------------------------------------------------


def test_sukun_bearing_waw_does_not_emit_madd() -> None:
    """§4.2: madd on و is licensed ONLY by ``haraka_function_before``,
    which requires preceding-slot context not preserved on Phase-1
    length=1 seed geometries. Resolver returns None — it does NOT
    synthesize madd from sukun-bearing waw alone."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_SUKUN)
    assert ArabicVariantResolver().resolve(geom) is None


def test_sukun_bearing_ya_does_not_emit_madd() -> None:
    """§5.2: same discipline as §4.2 for ي."""
    geom = _make_geom(letter_cp=_YAA, haraka_cp=_SUKUN)
    assert ArabicVariantResolver().resolve(geom) is None


# ---------------------------------------------------------------------------
# 11. Valid non_madd evidence for licensed و case
# ---------------------------------------------------------------------------


def test_waw_with_fatha_produces_non_madd_evidence() -> None:
    """§4.1: (و, non_madd) licensed by ``haraka_function_self``
    when the slot carries an active (non-sukun) haraka witness."""
    geom = _make_geom(
        letter_cp=_WAW,
        haraka_cp=_FATHA,
        candidate_id="geom:waw_fatha_001",
    )
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert result.symbol == "و"
    assert result.selected_variant == "non_madd"
    assert result.selected_entry_id == "lips_waw_non_madd"
    assert result.selection_basis == ("haraka_function_self",)
    assert result.geometry_candidate_id == "geom:waw_fatha_001"
    assert result.geometry_layer == FIXED_GEOMETRY_LAYER
    assert result.geometry_length == FIXED_GEOMETRY_LENGTH
    assert result.geometry_construction_mode == FIXED_GEOMETRY_CONSTRUCTION_MODE
    # Verbatim preservation of geometry audit anchors.
    assert result.geometry_identity_ids == geom.identity_ids
    assert result.geometry_trace_ids == geom.trace_ids
    # Identity/trace separation invariant.
    assert set(result.geometry_identity_ids).isdisjoint(
        set(result.audit_trace_ids)
    )


def test_waw_with_damma_also_produces_non_madd_evidence() -> None:
    """§4.1: damma also satisfies ``haraka_function_self`` for و."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_DAMMA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert result.selected_variant == "non_madd"
    assert result.selection_basis == ("haraka_function_self",)


def test_waw_with_kasra_also_produces_non_madd_evidence() -> None:
    """§4.1: kasra also satisfies ``haraka_function_self`` for و."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_KASRA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert result.selected_variant == "non_madd"


# ---------------------------------------------------------------------------
# 12. madd path — no synthesis without preceding-slot context;
#     no MIU decision either way
# ---------------------------------------------------------------------------


def test_resolver_does_not_synthesize_madd_without_preceding_context() -> None:
    """§4.2 / §5.2: the only licensed basis for madd is
    ``haraka_function_before``. Phase-1 length=1 seeds do not
    preserve preceding-slot context, so the resolver always returns
    None for the sukun-bearing case — and never makes a MIU decision
    either way."""
    sukun_waw = _make_geom(letter_cp=_WAW, haraka_cp=_SUKUN)
    sukun_ya = _make_geom(letter_cp=_YAA, haraka_cp=_SUKUN)
    assert ArabicVariantResolver().resolve(sukun_waw) is None
    assert ArabicVariantResolver().resolve(sukun_ya) is None


def test_unrelated_extra_identity_tags_do_not_flip_decision() -> None:
    """Adding unrelated identity tags must not change the decision —
    the resolver reads only letter and haraka codepoint identities."""
    enriched = _make_geom(
        letter_cp=_WAW,
        haraka_cp=_SUKUN,
        extra_identity=(
            "identity:some_other_tag",
            "identity:slot_composition_domain",
        ),
    )
    assert ArabicVariantResolver().resolve(enriched) is None


# ---------------------------------------------------------------------------
# 13. ي follows the same discipline
# ---------------------------------------------------------------------------


def test_ya_with_kasra_produces_non_madd_evidence() -> None:
    """§5.1: (ي, non_madd) licensed by ``haraka_function_self``
    when the slot carries an active haraka witness."""
    geom = _make_geom(
        letter_cp=_YAA,
        haraka_cp=_KASRA,
        candidate_id="geom:ya_kasra_001",
    )
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert result.symbol == "ي"
    assert result.selected_variant == "non_madd"
    assert result.selected_entry_id == "tongue_ya_non_madd"
    assert result.selection_basis == ("haraka_function_self",)


def test_ya_with_fatha_produces_non_madd_evidence() -> None:
    """§5.1: fatha also satisfies ``haraka_function_self`` for ي."""
    geom = _make_geom(letter_cp=_YAA, haraka_cp=_FATHA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert result.symbol == "ي"
    assert result.selected_variant == "non_madd"
    assert result.selected_entry_id == "tongue_ya_non_madd"


# ---------------------------------------------------------------------------
# 14. ا future-extensibility only ⇒ None
# ---------------------------------------------------------------------------


def test_alif_returns_none_regardless_of_haraka() -> None:
    """§6: this contract does not define ا-specific variant semantics.
    The resolver returns None for ا regardless of haraka witness."""
    resolver = ArabicVariantResolver()
    alif_fatha = _make_geom(letter_cp=_ALIF, haraka_cp=_FATHA)
    alif_sukun = _make_geom(letter_cp=_ALIF, haraka_cp=_SUKUN)
    alif_no_haraka = _make_geom(letter_cp=_ALIF, haraka_cp=None)
    assert resolver.resolve(alif_fatha) is None
    assert resolver.resolve(alif_sukun) is None
    assert resolver.resolve(alif_no_haraka) is None


# ---------------------------------------------------------------------------
# Additional invariants — selection_basis discipline
# ---------------------------------------------------------------------------


def test_resolver_does_not_emit_secondary_basis_alone() -> None:
    """§4.1 / §5.1: ``intra_utterance_position`` is SECONDARY only,
    licensing non_madd ONLY in conjunction with the primary basis.
    This initial implementation does not emit it at all (deferred
    to a later implementation contract)."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert "intra_utterance_position" not in result.selection_basis


def test_resolver_does_not_emit_haraka_function_before_basis() -> None:
    """§4.2 / §5.2: ``haraka_function_before`` requires preceding-slot
    context not preserved on Phase-1 length=1 seed. This
    implementation does not emit it."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert "haraka_function_before" not in result.selection_basis


def test_resolver_does_not_emit_registry_default_basis() -> None:
    """§3 fact 2 / §4.1: ``registry_default`` is reserved-but-
    unavailable. The resolver never emits it."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert "registry_default" not in result.selection_basis


def test_resolver_selection_basis_is_exactly_primary_only() -> None:
    """This implementation only emits exactly the primary
    ``haraka_function_self`` basis for non_madd — nothing else."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert result.selection_basis == ("haraka_function_self",)


# ---------------------------------------------------------------------------
# Audit-trace schema discipline
# ---------------------------------------------------------------------------


def test_audit_trace_ids_follow_recommended_schema() -> None:
    """§6.2: ``audit_trace_ids`` includes the five recommended entries
    (symbol, selected_variant, selected_entry_id, basis, geometry_id)."""
    geom = _make_geom(
        letter_cp=_WAW,
        haraka_cp=_FATHA,
        candidate_id="geom:audit_check",
    )
    result = ArabicVariantResolver().resolve(geom)
    assert result is not None
    assert "trace:arabic_variant_resolution:symbol:و" in result.audit_trace_ids
    assert (
        "trace:arabic_variant_resolution:selected_variant:non_madd"
        in result.audit_trace_ids
    )
    assert (
        "trace:arabic_variant_resolution:selected_entry_id:lips_waw_non_madd"
        in result.audit_trace_ids
    )
    assert (
        "trace:arabic_variant_resolution:basis:haraka_function_self"
        in result.audit_trace_ids
    )
    assert (
        "trace:arabic_variant_resolution:geometry_id:geom:audit_check"
        in result.audit_trace_ids
    )


def test_resolver_is_deterministic_modulo_evidence_id() -> None:
    """§3.2: given the same input the resolver returns equivalent
    evidence (modulo the nondeterministic evidence_id uuid)."""
    geom = _make_geom(letter_cp=_WAW, haraka_cp=_FATHA)
    a = ArabicVariantResolver().resolve(geom)
    b = ArabicVariantResolver().resolve(geom)
    assert a is not None and b is not None
    assert a.symbol == b.symbol
    assert a.selected_variant == b.selected_variant
    assert a.selected_entry_id == b.selected_entry_id
    assert a.selection_basis == b.selection_basis
    assert a.geometry_candidate_id == b.geometry_candidate_id
    assert a.geometry_identity_ids == b.geometry_identity_ids
    assert a.audit_trace_ids == b.audit_trace_ids
    # Only the evidence_id differs (uuid-based, non-deterministic).
    assert a.evidence_id != b.evidence_id
