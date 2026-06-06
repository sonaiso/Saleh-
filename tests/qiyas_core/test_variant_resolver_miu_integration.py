"""Integration tests for the resolver ↔ MIU readiness chain.

Pins the post-PR-#82 cross-layer behaviour as a dedicated coverage
target whose **intent** is "the chain":

    ArabicVariantResolver().resolve(geometry)
        → ArabicVariantResolutionEvidence | None
        → MinimalIndependentUnitReadinessLayerAdapter.admit(
              geometry,
              closure_evidence,
              variant_resolution_evidence=evidence,
          )
        → MinimalUnitReadinessCandidate (ACCEPTED / BLOCKED / DEFERRED)

This file is **not** a re-implementation of the per-layer unit tests
in ``test_arabic_variant_resolver.py``, ``test_arabic_variant_resolution_
evidence.py``, or ``test_minimal_unit_readiness.py``. Those pin the
behaviour of each layer in isolation. The tests here pin the
**cross-layer agreement**: that the resolver's emitted evidence is a
shape the MIU adapter accepts, and that the constitutional discipline
(§7 absence-≠-BLOCK, §10.3 license-not-require) of
``ARABIC_VARIANT_RESOLUTION_CONTRACT.md`` actually holds end-to-end
under the merged baseline at main@a0729bf (PRs #78-#82).

Authority basis:
  CLAUDE.md §0 / §3 / §4 / §5 / §7 / §8 / §9 / §11 / §14 / §19 / §20,
  ARABIC_VARIANT_RESOLUTION_CONTRACT.md §3 / §4 / §6 / §7 / §8 / §10,
  ARABIC_VARIANT_SELECTION_RULES_CONTRACT.md §4 / §5 / §7 / §9,
  MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md §2 / §3 / §4 / §5
    / §7 / §10.

Scope discipline (this PR):
  * tests-only — no `src/` change, no `docs/` change, no registry change.
  * single new file.
  * uses the public API of already-merged layers only.
  * does NOT depend on:
      - secondary basis (`intra_utterance_position`, `haraka_function_*`,
        `preceding_letter_identity`, `following_letter_identity`,
        `registry_default`),
      - alif (ا) semantics,
      - any `Word*` / `Lafz*` / `Dalalah*` / `Final*` / `Hukm*` /
        `Reality*` / `Sentence*` / `Discourse*` / `Text*` / `Amil*`
        symbols.
"""

from __future__ import annotations

import ast
import inspect
import uuid

import pytest

from qiyas_core.arabic_articulation_registry import (
    get_articulation_by_id,
    get_articulations_by_symbol,
)
from qiyas_core.arabic_variant_resolution_evidence import (
    ArabicVariantResolutionEvidence,
    FIXED_GEOMETRY_CONSTRUCTION_MODE,
    FIXED_GEOMETRY_LAYER,
    FIXED_GEOMETRY_LENGTH,
)
from qiyas_core.arabic_variant_resolver import ArabicVariantResolver
from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.minimal_unit_readiness_adapter import (
    MinimalIndependentUnitReadinessLayerAdapter,
)
# SlotGeometry moved to experimental/ per RESET_CONSTITUTION.md §7
# These imports are from experimental code and should be migrated
import sys
from pathlib import Path
experimental_path = Path(__file__).parent.parent.parent / "experimental"
sys.path.insert(0, str(experimental_path))
from qiyas_core.slot_geometry_adapter import (
    SlotBindingEvidence,
    SlotGeometryLayerAdapter,
)
from qiyas_core.slot_geometry_closure_check import (
    check_slot_geometry_closure,
)
sys.path.pop(0)


# ---------------------------------------------------------------------------
# Local self-contained fixture helpers
#
# Mirrors the patterns in tests/qiyas_core/test_minimal_unit_readiness.py
# but kept local so this file is fully standalone (the prompt asked for
# "test file مستقلًا قدر الإمكان"). Helper duplication is acceptable
# per the prompt for an integration-coverage file.
# ---------------------------------------------------------------------------


_FATHA = "064e"
_DAMMA = "064f"
_KASRA = "0650"
_SUKUN = "0652"

_CP = {
    # Single-variant, registry-eligible.
    "ب": "0628",
    # Single-variant, registry NOT eligible (negative case).
    "ض": "0636",
    # Multi-variant — variant resolution applies.
    "و": "0648",
    "ي": "064a",
}


def _make_slot_candidate(
    *, trace_label: str, letter_cp: str, haraka_cp: str = _FATHA,
) -> Candidate:
    return Candidate(
        candidate_id=f"slot:integ:{trace_label}:{uuid.uuid4().hex[:8]}",
        candidate_type="SlotCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id="slot.composition",
        asl_id="اصل:slot_composition_domain",
        far_id=f"فرع:slot:integ:{trace_label}",
        identity_ids=(
            f"identity:codepoint:{letter_cp}",
            f"identity:codepoint:{haraka_cp}",
            "identity:slot_composition_domain",
        ),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(
            f"trace:integ:{trace_label}:ev",
            f"trace:slot:alignment_ref:integ:{trace_label}",
        ),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _seed_geometry_for_letter(
    letter_cp: str, *, trace_label: str, haraka_cp: str = _FATHA,
) -> Candidate:
    """Produce a real ``SlotGeometryCandidate(length=1)`` via the
    existing slot-geometry adapter — the same path the runtime uses."""
    slot = _make_slot_candidate(
        trace_label=trace_label, letter_cp=letter_cp, haraka_cp=haraka_cp,
    )
    geom_adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    result = geom_adapter.seed_geometry(slot)
    assert len(result.accepted) == 1, (
        "Integration test fixture broken: SlotGeometry seed did not "
        f"accept letter_cp={letter_cp}"
    )
    return result.accepted[0]


def _length_2_geometry() -> Candidate:
    """Real length=2 SlotGeometryCandidate for the length-gate case
    (Case 6). Uses ب + ت the same way the MIU unit-test fixture does."""
    first = _make_slot_candidate(trace_label="L2_a", letter_cp="0628")
    second = _make_slot_candidate(
        trace_label="L2_b", letter_cp="062a", haraka_cp=_SUKUN,
    )
    geom_adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    seed = geom_adapter.seed_geometry(first).accepted[0]
    binding = SlotBindingEvidence(
        prev_segment_id=0, curr_segment_id=0,
        prev_position=0, curr_position=1,
        has_whitespace_between=False, has_punctuation_between=False,
        max_licensed_distance=1,
        binding_trace_ids=(f"trace:binding:integ:{uuid.uuid4().hex[:8]}",),
    )
    result = geom_adapter.extend_geometry(seed, second, binding)
    assert len(result.accepted) == 1
    return result.accepted[0]


def _miu_adapter() -> MinimalIndependentUnitReadinessLayerAdapter:
    return MinimalIndependentUnitReadinessLayerAdapter(kernel=QiyasKernel())


def _classify(result):
    if result.accepted:
        return "ACCEPTED", result.accepted[0]
    if result.deferred:
        return "DEFERRED", result.deferred[0]
    return "BLOCKED", result.blocked[0]


def _residual_types(candidate: Candidate) -> set[str]:
    return {r.residual_type for r in candidate.residuals}


_NO_MEANING_TYPES = frozenset({
    "WordCandidate",
    "LafzCandidate",
    "SentenceCandidate",
    "ParagraphCandidate",
    "DalalahCandidate",
    "FinalMeaning",
    "HukmCandidate",
    "RealityClaim",
    "FinalCaseJudgment",
    "DiscourseGeometryCandidate",
    "TextGeometryCandidate",
    "MinimalIndependentMeaningCandidate",
    "SentenceGeometry",
})


def _assert_no_meaning_or_hukm(candidate: Candidate) -> None:
    """Pin the constitutional invariant that no MIU output ever
    carries a higher-layer fingerprint (CLAUDE.md §4 invariant 9 +
    MIU contract §8 forbidden outputs)."""
    assert candidate.candidate_type == "MinimalUnitReadinessCandidate", (
        f"candidate_type must remain MinimalUnitReadinessCandidate; "
        f"got {candidate.candidate_type!r}"
    )
    assert candidate.candidate_type not in _NO_MEANING_TYPES
    assert not (_NO_MEANING_TYPES & set(candidate.output_flags)), (
        f"output_flags leaked a higher-layer name: "
        f"{sorted(_NO_MEANING_TYPES & set(candidate.output_flags))}"
    )


# ===========================================================================
# Group 1 — End-to-end canonical cases for the resolver ↔ MIU chain
# ===========================================================================


# --- Case 1: بِ baseline accepted without resolver -------------------


def test_integ_case_1_baa_accepted_without_resolver():
    """Baseline single-variant case — the resolver is irrelevant; the
    MIU layer alone admits بِ."""
    geom = _seed_geometry_for_letter(_CP["ب"], trace_label="C1_baa")
    closure = check_slot_geometry_closure(geom)
    assert closure is not None

    result = _miu_adapter().admit(geom, closure)
    bucket, c = _classify(result)

    assert bucket == "ACCEPTED"
    assert c.status == CandidateStatus.ACCEPTED
    assert c.output_flags == frozenset({"CandidateOnly"})
    _assert_no_meaning_or_hukm(c)


# --- Case 2: ضَ baseline blocked -------------------------------------


def test_integ_case_2_dad_blocked():
    """Single-variant, registry-NOT-eligible letter remains BLOCKED.
    Resolver involvement does not change the outcome."""
    geom = _seed_geometry_for_letter(_CP["ض"], trace_label="C2_dad")
    closure = check_slot_geometry_closure(geom)
    assert closure is not None

    result = _miu_adapter().admit(geom, closure)
    bucket, c = _classify(result)

    assert bucket == "BLOCKED"
    assert c.status == CandidateStatus.BLOCKED
    assert "blocking_fariq_present" in _residual_types(c)
    _assert_no_meaning_or_hukm(c)


# --- Case 3: وَ without resolver evidence ----------------------------


def test_integ_case_3_waw_deferred_without_resolver():
    """Multi-variant symbol + no evidence ⇒ DEFERRED via
    `deferred_variant_ambiguity`. Never BLOCKED, never ACCEPTED."""
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="C3_waw_no_ev")
    closure = check_slot_geometry_closure(geom)
    assert closure is not None

    result = _miu_adapter().admit(geom, closure)  # no evidence kwarg
    bucket, c = _classify(result)

    assert bucket == "DEFERRED"
    assert c.status == CandidateStatus.DEFERRED
    assert "deferred_variant_ambiguity" in _residual_types(c)
    _assert_no_meaning_or_hukm(c)


# --- Case 4: وَ with resolver evidence → ACCEPTED ---------------------


def test_integ_case_4_waw_with_resolver_accepted():
    """The full chain. Build geometry → run resolver → pass evidence
    to MIU.admit → ACCEPTED. This is the ONLY runtime path that
    flips وَ from DEFERRED to ACCEPTED under the current baseline."""
    # Step 1: build geometry.
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="C4_waw_with_ev")

    # Step 2: build closure evidence.
    closure = check_slot_geometry_closure(geom)
    assert closure is not None

    # Step 3: run resolver on the same geometry.
    resolver = ArabicVariantResolver()
    evidence = resolver.resolve(geom)
    assert isinstance(evidence, ArabicVariantResolutionEvidence)
    assert evidence.symbol == "و"
    assert evidence.selected_variant == "non_madd"
    assert evidence.selected_entry_id == "lips_waw_non_madd"
    assert evidence.selection_basis == ("haraka_function_self",)
    assert evidence.geometry_candidate_id == geom.candidate_id

    # Step 4: pass evidence into MIU.admit.
    result = _miu_adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    bucket, c = _classify(result)

    # Step 5: cross-layer assertions.
    assert bucket == "ACCEPTED"
    assert c.status == CandidateStatus.ACCEPTED
    assert c.output_flags == frozenset({"CandidateOnly"})
    # variant_ambiguity must NOT appear in residuals on the accepted path.
    rtypes = _residual_types(c)
    assert "deferred_variant_ambiguity" not in rtypes
    assert "blocking_fariq_present" not in rtypes
    _assert_no_meaning_or_hukm(c)


# --- Case 5: يَ with resolver evidence → BLOCKED (conservative) -------


def test_integ_case_5_ya_with_resolver_blocked_conservatively():
    """يَ + valid non_madd evidence ⇒ BLOCKED through registry
    eligibility (`tongue_ya_non_madd.can_function_as_minimal_independent_unit
    == False`). This locks the constitutional discipline: evidence
    presence does NOT by itself authorise admission."""
    geom = _seed_geometry_for_letter(_CP["ي"], trace_label="C5_ya_with_ev")
    closure = check_slot_geometry_closure(geom)
    assert closure is not None

    evidence = ArabicVariantResolver().resolve(geom)
    assert isinstance(evidence, ArabicVariantResolutionEvidence)
    assert evidence.symbol == "ي"
    assert evidence.selected_variant == "non_madd"
    assert evidence.selected_entry_id == "tongue_ya_non_madd"

    result = _miu_adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    bucket, c = _classify(result)

    # CRITICAL: NOT ACCEPTED, even though evidence is valid and
    # variant ambiguity is resolved. Eligibility comes from the
    # registry entry, not from the resolver.
    assert bucket != "ACCEPTED", (
        f"يَ unexpectedly became ACCEPTED — registry eligibility "
        f"must dominate evidence presence; bucket={bucket}"
    )
    assert bucket == "BLOCKED"
    assert c.status == CandidateStatus.BLOCKED
    assert "blocking_fariq_present" in _residual_types(c)
    _assert_no_meaning_or_hukm(c)


# --- Case 6: ضَرَبَ-like length > 1 → BLOCKED ------------------------


def test_integ_case_6_length_2_geometry_blocked():
    """A length>1 geometry stays BLOCKED. Variant evidence (even if
    constructed) must not override the structural length gate."""
    geom = _length_2_geometry()
    closure = check_slot_geometry_closure(geom)
    # closure may or may not be available for length-2 geometries
    # depending on construction; either way MIU should not admit.

    # Run with no evidence first.
    result = _miu_adapter().admit(geom, closure)
    bucket, c = _classify(result)
    assert bucket != "ACCEPTED"
    _assert_no_meaning_or_hukm(c)

    # Also pass a synthetic evidence that names the length-2 geometry,
    # to prove the length gate dominates evidence.
    synthetic = ArabicVariantResolutionEvidence(
        symbol="و",
        selected_variant="non_madd",
        selected_entry_id="lips_waw_non_madd",
        selection_basis=("haraka_function_self",),
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        evidence_id="ev:integ_synth_for_length2",
        audit_trace_ids=(),
    )
    result2 = _miu_adapter().admit(
        geom, closure, variant_resolution_evidence=synthetic,
    )
    bucket2, c2 = _classify(result2)
    assert bucket2 != "ACCEPTED", (
        "Length gate must dominate variant evidence; "
        f"got bucket={bucket2} on length>1 geometry."
    )
    _assert_no_meaning_or_hukm(c2)


# --- Case 7: وَ with foreign/mismatched evidence → DEFERRED ----------


def test_integ_case_7_waw_with_foreign_evidence_deferred():
    """Evidence whose `geometry_candidate_id` belongs to a DIFFERENT
    geometry is foreign; the §7 discipline says foreign-or-invalid
    is treated as absent ⇒ DEFER, never BLOCK."""
    geom_a = _seed_geometry_for_letter(_CP["و"], trace_label="C7_waw_a")
    geom_b = _seed_geometry_for_letter(_CP["و"], trace_label="C7_waw_b")
    closure_a = check_slot_geometry_closure(geom_a)
    assert closure_a is not None

    foreign_evidence = ArabicVariantResolver().resolve(geom_b)
    assert isinstance(foreign_evidence, ArabicVariantResolutionEvidence)
    # Sanity: the foreign evidence really points at geom_b, not geom_a.
    assert foreign_evidence.geometry_candidate_id == geom_b.candidate_id
    assert foreign_evidence.geometry_candidate_id != geom_a.candidate_id

    result = _miu_adapter().admit(
        geom_a, closure_a, variant_resolution_evidence=foreign_evidence,
    )
    bucket, c = _classify(result)

    assert bucket == "DEFERRED", (
        f"Foreign evidence must DEFER (§7), not BLOCK; got {bucket}"
    )
    assert c.status == CandidateStatus.DEFERRED
    assert "deferred_variant_ambiguity" in _residual_types(c)
    _assert_no_meaning_or_hukm(c)


# ===========================================================================
# Group 2 — Cross-layer properties
# ===========================================================================


# --- Property 1: resolver selected entry agrees with registry --------


@pytest.mark.parametrize(
    "symbol,letter_cp",
    [("و", _CP["و"]), ("ي", _CP["ي"])],
)
def test_integ_property_resolver_entry_belongs_to_registry(symbol, letter_cp):
    """For every multi-variant symbol the resolver emits evidence for,
    the selected_entry_id MUST be a real registry entry whose symbol
    and variant agree with the evidence. Pins the resolver↔registry
    contract from PR #78 §6.1 and PR #79 §3."""
    geom = _seed_geometry_for_letter(
        letter_cp, trace_label=f"P1_{symbol}",
    )
    evidence = ArabicVariantResolver().resolve(geom)
    assert isinstance(evidence, ArabicVariantResolutionEvidence)
    assert evidence.symbol == symbol

    # The selected_entry_id MUST resolve in the registry.
    entry = get_articulation_by_id(evidence.selected_entry_id)
    assert entry is not None, (
        f"selected_entry_id={evidence.selected_entry_id!r} not in registry"
    )
    # The entry's symbol and variant MUST agree with the evidence.
    assert entry.symbol == evidence.symbol
    assert entry.variant == evidence.selected_variant

    # And the entry MUST be among `get_articulations_by_symbol`.
    all_entries_for_symbol = get_articulations_by_symbol(symbol)
    assert entry.id in {e.id for e in all_entries_for_symbol}


# --- Property 2: MIU ACCEPTED ⇒ resolved entry eligible --------------


def test_integ_property_miu_accepted_implies_eligibility():
    """For every (و) integration case that reaches ACCEPTED via
    variant evidence, the resolved registry entry MUST have
    can_function_as_minimal_independent_unit == True. Output flags
    MUST be exactly {CandidateOnly}. No higher-layer fingerprint.

    This catches any future bug where presence of evidence alone
    admits MIU without delegating to registry eligibility."""
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="P2_waw")
    closure = check_slot_geometry_closure(geom)
    assert closure is not None
    evidence = ArabicVariantResolver().resolve(geom)
    assert evidence is not None

    result = _miu_adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    if result.accepted:
        c = result.accepted[0]
        # The entry the evidence resolved to MUST be eligible.
        entry = get_articulation_by_id(evidence.selected_entry_id)
        assert entry is not None
        assert entry.can_function_as_minimal_independent_unit is True, (
            f"MIU admitted on entry that is NOT minimal-unit eligible: "
            f"{entry.id!r}"
        )
        # Output discipline.
        assert c.output_flags == frozenset({"CandidateOnly"})
        _assert_no_meaning_or_hukm(c)
    else:
        # The current baseline accepts وَ with valid evidence; if it
        # does not, fail loudly because that contradicts PR #82.
        pytest.fail(
            "Baseline regression: وَ with valid resolver evidence "
            "is no longer ACCEPTED at main."
        )


# --- Property 3: absent / foreign / malformed evidence never BLOCKS by itself ---


def test_integ_property_absent_evidence_defers():
    """Absent evidence on multi-variant symbol ⇒ DEFER (never BLOCK)."""
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="P3_absent")
    closure = check_slot_geometry_closure(geom)
    result = _miu_adapter().admit(geom, closure)
    bucket, c = _classify(result)
    assert bucket == "DEFERRED"
    assert "deferred_variant_ambiguity" in _residual_types(c)


def test_integ_property_foreign_evidence_defers():
    """Foreign evidence (for a different geometry id) ⇒ DEFER, not BLOCK."""
    geom_a = _seed_geometry_for_letter(_CP["و"], trace_label="P3_for_a")
    geom_b = _seed_geometry_for_letter(_CP["و"], trace_label="P3_for_b")
    closure_a = check_slot_geometry_closure(geom_a)
    foreign = ArabicVariantResolver().resolve(geom_b)
    assert foreign is not None
    result = _miu_adapter().admit(
        geom_a, closure_a, variant_resolution_evidence=foreign,
    )
    bucket, c = _classify(result)
    assert bucket == "DEFERRED"
    assert "deferred_variant_ambiguity" in _residual_types(c)


def test_integ_property_malformed_evidence_defers():
    """Evidence pointing at a registry entry that does not exist ⇒
    DEFER, not BLOCK (§7 — malformed treated as absent)."""
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="P3_malformed")
    closure = check_slot_geometry_closure(geom)
    malformed = ArabicVariantResolutionEvidence(
        symbol="و",
        selected_variant="non_madd",
        selected_entry_id="does_not_exist_in_registry",
        selection_basis=("haraka_function_self",),
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        evidence_id="ev:integ_malformed:001",
        audit_trace_ids=(),
    )
    result = _miu_adapter().admit(
        geom, closure, variant_resolution_evidence=malformed,
    )
    bucket, c = _classify(result)
    assert bucket == "DEFERRED"
    assert "deferred_variant_ambiguity" in _residual_types(c)


# --- Property 4: AST guard — no forbidden imports in this file ------


_FORBIDDEN_IMPORT_SUBSTRINGS = (
    "word",
    "lafz",
    "dalalah",
    "sentence",
    "discourse",
    "text_geometry",
    "meaning",
    "hukm",
    "reality",
    "final_case",
    "amil",
)


def test_integ_property_no_forbidden_imports_in_this_file():
    """AST guard: this integration test file MUST NOT import from any
    higher-layer or forbidden module. Locks the scope discipline that
    this PR is tests-only and stays below MIU readiness."""
    import qiyas_core.arabic_variant_resolver as _avr  # noqa: F401
    # Resolve this file by inspecting our own module name.
    import sys
    this_module = sys.modules[__name__]
    src = inspect.getsource(this_module)
    tree = ast.parse(src)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)

    for mod in imported:
        lower = mod.lower()
        for needle in _FORBIDDEN_IMPORT_SUBSTRINGS:
            assert needle not in lower, (
                f"forbidden import detected: {mod!r} contains {needle!r}"
            )


# ===========================================================================
# Group 3 — Regression locks
# ===========================================================================


def test_integ_regression_no_auto_caller_side_wiring_assumed():
    """The integration MUST be manual: the test itself wires
    `ArabicVariantResolver().resolve(geom)` to
    `MIU.admit(..., variant_resolution_evidence=evidence)`. There is
    no production adapter that does this automatically, by design.

    The regression lock is structural: if a future change introduces
    a hidden auto-wiring inside `MIU.admit` that calls the resolver
    itself, the explicit DEFERRED case (Case 3 — no evidence) would
    silently flip to ACCEPTED. So we re-assert Case 3 here under a
    different label and a fresh geometry, to keep the lock visible
    from the integration test surface."""
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="REG_auto")
    closure = check_slot_geometry_closure(geom)

    # CRITICAL: do NOT pass evidence. MIU must DEFER.
    result = _miu_adapter().admit(geom, closure)
    bucket, c = _classify(result)
    assert bucket == "DEFERRED", (
        f"Regression: MIU appears to auto-wire to resolver; "
        f"got bucket={bucket} without explicit evidence."
    )
    assert "deferred_variant_ambiguity" in _residual_types(c)


def test_integ_regression_only_primary_basis_used():
    """The current implementation uses ONLY the primary basis
    `haraka_function_self` for non_madd. Lock that no secondary or
    madd-side basis sneaks into the integration path."""
    geom = _seed_geometry_for_letter(_CP["و"], trace_label="REG_basis")
    evidence = ArabicVariantResolver().resolve(geom)
    assert evidence is not None
    # The exact basis tuple.
    assert evidence.selection_basis == ("haraka_function_self",)
    # And the explicitly NOT-emitted bases.
    forbidden_bases = {
        "haraka_function_before",
        "haraka_function_after",
        "preceding_letter_identity",
        "following_letter_identity",
        "registry_default",
        "intra_utterance_position",
    }
    assert not (forbidden_bases & set(evidence.selection_basis))


def test_integ_regression_alif_remains_out_of_resolver_scope():
    """ا remains future-extensibility only (PR #78 §6 / PR #79 §6).
    The resolver returns None; MIU behaves on the registry's existing
    single entry. This lock is a single assertion — we do NOT expand
    alif coverage in this PR."""
    geom = _seed_geometry_for_letter("0627", trace_label="REG_alif")  # ا
    evidence = ArabicVariantResolver().resolve(geom)
    assert evidence is None, (
        f"ا must remain future-extensibility only; got evidence={evidence!r}"
    )
