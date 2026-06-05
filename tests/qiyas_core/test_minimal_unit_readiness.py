"""Tests for MinimalIndependentUnitReadinessQiyas.

Pins the behavioural contract of
``MinimalIndependentUnitReadinessLayerAdapter`` per
``MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md`` and the revised
implementation spec:

  * Positive admissible symbols in this batch:
        بِ، فَ، كَ، لِ، سَ، أَ، تَ        → ACCEPTED
  * Negative:
        ضَ، صَ                              → BLOCKED (registry rejects)
        ضَرَبَ                              → BLOCKED (length > 1)
  * Deferral:
        وَ، يَ                              → DEFERRED (variant ambiguity)
  * Output is always ``MinimalUnitReadinessCandidate`` with
    ``output_flags ⊇ {CandidateOnly}``; never ``WordCandidate``,
    ``DalalahCandidate``, ``FinalMeaning``, ``HukmCandidate``,
    ``RealityClaim``, ``MinimalIndependentMeaningCandidate``, etc.
  * The ``is_minimal_unit_ready`` metadata marker lives on
    ``trace_ids``, never on ``identity_ids``.
"""

from __future__ import annotations

import inspect
import uuid

import pytest

from qiyas_core import minimal_unit_readiness_adapter as miu_adapter_mod
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
from qiyas_core.rules.minimal_unit_readiness_rules import (
    MINIMAL_UNIT_READINESS_ADMIT_RULE,
    MINIMAL_UNIT_READINESS_RULES,
)
from qiyas_core.slot_geometry_adapter import (
    SlotBindingEvidence,
    SlotGeometryLayerAdapter,
)
from qiyas_core.slot_geometry_closure_check import (
    MinimalCompleteClosureEvidence,
    check_slot_geometry_closure,
)


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _adapter() -> MinimalIndependentUnitReadinessLayerAdapter:
    return MinimalIndependentUnitReadinessLayerAdapter(kernel=QiyasKernel())


def _make_slot_candidate(*, trace_label: str, letter_cp: str,
                        haraka_cp: str = "064e") -> Candidate:
    """Build a SlotCandidate fixture for an arbitrary letter+haraka pair."""
    return Candidate(
        candidate_id=f"slot:fixture:{trace_label}:{uuid.uuid4().hex[:8]}",
        candidate_type="SlotCandidate",
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id="slot.composition",
        asl_id="اصل:slot_composition_domain",
        far_id=f"فرع:slot:fixture:{trace_label}",
        identity_ids=(
            f"identity:codepoint:{letter_cp}",
            f"identity:codepoint:{haraka_cp}",
            "identity:slot_composition_domain",
        ),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(
            f"trace:fixture:{trace_label}:ev",
            f"trace:slot:alignment_ref:test:{trace_label}",
        ),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _seed_geometry_for_letter(letter_cp: str, *, trace_label: str = "S",
                               haraka_cp: str = "064e") -> Candidate:
    """Produce a real SlotGeometryCandidate(length=1) for the given
    letter codepoint by running the existing slot-geometry adapter."""
    slot = _make_slot_candidate(
        trace_label=trace_label,
        letter_cp=letter_cp,
        haraka_cp=haraka_cp,
    )
    geom_adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    result = geom_adapter.seed_geometry(slot)
    assert len(result.accepted) == 1, (
        f"Test fixture broken: SlotGeometry seed did not accept "
        f"letter_cp={letter_cp}; "
        f"residuals={[r.residual_type for r in result.blocked[0].residuals]}"
        if result.blocked else "no acceptance and no block"
    )
    return result.accepted[0]


def _length_2_geometry() -> Candidate:
    """Produce a length=2 SlotGeometryCandidate (ب + ت) for the
    'outside scope' test (ضَرَبَ is morally similar; we use ب+ت
    because the adapter pipeline accepts it cleanly)."""
    first = _make_slot_candidate(trace_label="Sa", letter_cp="0628")
    second = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652",
    )
    geom_adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    seed = geom_adapter.seed_geometry(first).accepted[0]
    binding = SlotBindingEvidence(
        prev_segment_id=0,
        curr_segment_id=0,
        prev_position=0,
        curr_position=1,
        has_whitespace_between=False,
        has_punctuation_between=False,
        max_licensed_distance=1,
        binding_trace_ids=(f"trace:binding:test:{uuid.uuid4().hex[:8]}",),
    )
    result = geom_adapter.extend_geometry(seed, second, binding)
    assert len(result.accepted) == 1
    return result.accepted[0]


def _closure_for(geom: Candidate) -> MinimalCompleteClosureEvidence:
    """Produce real closure evidence for a geometry via the existing
    checker. Used as the third witness for the readiness admission."""
    evidence = check_slot_geometry_closure(geom)
    assert evidence is not None, (
        "Test fixture broken: closure check did not produce evidence"
    )
    return evidence


# Codepoint mapping for the symbols we exercise in this batch.
_CP = {
    # admissible — single-variant, can_function_as_minimal_independent_unit=True
    "ب": "0628",   # baa
    "ف": "0641",   # faa
    "ك": "0643",   # kaf
    "ل": "0644",   # lam
    "س": "0633",   # seen
    "أ": "0623",   # interrogative hamza
    "ت": "062a",   # taa
    # rejected — single-variant, can_function_as_minimal_independent_unit=False
    "ض": "0636",
    "ص": "0635",
    # deferred — multi-variant
    "و": "0648",   # madd + non_madd
    "ي": "064a",   # madd + non_madd
}


def _residual_types(candidate: Candidate) -> set[str]:
    return {r.residual_type for r in candidate.residuals}


# ===========================================================================
# 1. Positive admissible — بِ، فَ، كَ، لِ، سَ، أَ، تَ → ACCEPTED
# ===========================================================================


@pytest.mark.parametrize(
    "symbol,letter_cp",
    [
        ("ب", _CP["ب"]),
        ("ف", _CP["ف"]),
        ("ك", _CP["ك"]),
        ("ل", _CP["ل"]),
        ("س", _CP["س"]),
        ("أ", _CP["أ"]),
        ("ت", _CP["ت"]),
    ],
)
def test_admits_eligible_single_variant_letter(symbol, letter_cp):
    """Each of the seven core eligible letters produces an ACCEPTED
    MinimalUnitReadinessCandidate when paired with a haraka."""
    geom = _seed_geometry_for_letter(letter_cp, trace_label=symbol)
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)

    assert len(result.accepted) == 1, (
        f"{symbol!r} should be admitted but was not; "
        f"blocked={[_residual_types(c) for c in result.blocked]}; "
        f"deferred={[_residual_types(c) for c in result.deferred]}"
    )
    c = result.accepted[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert c.layer == "MinimalIndependentUnitReadinessQiyas"
    assert c.source_rule_id == MINIMAL_UNIT_READINESS_ADMIT_RULE.rule_id
    assert "CandidateOnly" in c.output_flags
    assert c.rank != EvidenceRank.NO_EVIDENCE


# ===========================================================================
# 2. Negative — ضَ، صَ → BLOCKED by registry metadata
# ===========================================================================


@pytest.mark.parametrize(
    "symbol,letter_cp",
    [
        ("ض", _CP["ض"]),
        ("ص", _CP["ص"]),
    ],
)
def test_blocks_registry_ineligible_letter(symbol, letter_cp):
    """Single-variant letters whose registry metadata says
    can_function_as_minimal_independent_unit=False are BLOCKED with
    the symbol_not_eligible_for_minimal_unit fariq."""
    geom = _seed_geometry_for_letter(letter_cp, trace_label=symbol)
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    c = result.blocked[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert c.status == CandidateStatus.BLOCKED
    assert "CandidateOnly" in c.output_flags
    assert "blocking_fariq_present" in _residual_types(c)


# ===========================================================================
# 3. Negative — length>1 (ضَرَبَ-like) → BLOCKED with length_not_one
# ===========================================================================


def test_blocks_length_greater_than_one_geometry():
    """A length>1 SlotGeometryCandidate is outside the readiness layer's
    admission gate (MIU §2 admits only length=1). The block carries the
    length_not_one fariq and the construction_mode_not_seed fariq
    (since extension != seed)."""
    geom = _length_2_geometry()
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    c = result.blocked[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert c.status == CandidateStatus.BLOCKED
    assert "CandidateOnly" in c.output_flags
    assert "blocking_fariq_present" in _residual_types(c)


# ===========================================================================
# 4. Deferral — وَ، يَ → DEFERRED by variant ambiguity
# ===========================================================================


@pytest.mark.parametrize(
    "symbol,letter_cp",
    [
        ("و", _CP["و"]),
        ("ي", _CP["ي"]),
    ],
)
def test_defers_variant_ambiguous_letter(symbol, letter_cp):
    """و and ي each have two registry variants (madd + non-madd). The
    readiness layer refuses to choose between them without future
    variant evidence and DEFERS instead (contract §4.2 / §7 / §13.3 of
    MINIMAL_INDEPENDENT_UNIT_READINESS_CONTRACT.md)."""
    haraka = "064e" if symbol == "و" else "064e"  # fatha
    geom = _seed_geometry_for_letter(
        letter_cp, trace_label=symbol, haraka_cp=haraka,
    )
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)

    assert len(result.accepted) == 0
    assert len(result.deferred) == 1
    c = result.deferred[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert c.status == CandidateStatus.DEFERRED
    assert "CandidateOnly" in c.output_flags
    assert "deferred_variant_ambiguity" in _residual_types(c)


# ===========================================================================
# 5. Closure evidence missing → BLOCKED
# ===========================================================================


def test_blocks_when_closure_evidence_missing():
    """closure_evidence=None blocks the admission with the
    closure_evidence_missing fariq."""
    geom = _seed_geometry_for_letter(_CP["ب"], trace_label="ba_no_closure")
    result = _adapter().admit(geom, closure_evidence=None)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    c = result.blocked[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert c.status == CandidateStatus.BLOCKED
    assert "CandidateOnly" in c.output_flags
    assert "blocking_fariq_present" in _residual_types(c)


# ===========================================================================
# 6. Non-SlotGeometryCandidate input → BLOCKED
# ===========================================================================


def test_blocks_non_slot_geometry_input():
    """A bare SlotCandidate (not a SlotGeometryCandidate) is blocked at
    the consumption-surface gate per MIU §2."""
    slot = _make_slot_candidate(trace_label="raw_slot", letter_cp=_CP["ب"])
    # We need a closure-evidence-shaped object to satisfy the second
    # witness; build a minimal one structurally (it would never be
    # produced by SlotGeometryClosureCheck for a SlotCandidate).
    closure = MinimalCompleteClosureEvidence(
        licensed_beginning=True, licensed_ending=True,
        all_internal_bindings_licensed=True, no_open_demand=True,
        no_blocking_difference=True, residuals_preserved=True,
        rank_above_no_evidence=True, output_remains_candidate_only=True,
        geometry_candidate_id="fake",
        geometry_layer="SlotGeometryQiyas",
        geometry_length=1,
        geometry_construction_mode="seed",
        geometry_identity_ids=(),
        geometry_trace_ids=(),
        geometry_rank="FORMAL_STRUCTURE",
        evidence_id="ev:fake",
        audit_trace_ids=(),
    )

    result = _adapter().admit(slot, closure)
    assert len(result.accepted) == 0
    # Either blocked or deferred — both witness rejection. The kernel
    # records far_type_mismatch + blocking_fariq_present residuals.
    assert (len(result.blocked) + len(result.deferred)) == 1


# ===========================================================================
# 7. Output type guarantees — never WordCandidate / Dalalah / FinalMeaning /
#    Hukm / RealityClaim / MinimalIndependentMeaningCandidate
# ===========================================================================


def test_admitted_output_is_only_minimal_unit_readiness_candidate():
    """Across every admissible / blocked / deferred case, the candidate
    type is always MinimalUnitReadinessCandidate — never any of the
    forbidden higher-layer types."""
    forbidden_types = {
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
    }
    cases = [
        (_CP["ب"], "admit"),       # ACCEPTED case
        (_CP["ض"], "block_reg"),   # BLOCKED by registry
        (_CP["و"], "defer"),       # DEFERRED by ambiguity
    ]
    for letter_cp, label in cases:
        geom = _seed_geometry_for_letter(letter_cp, trace_label=label)
        closure = _closure_for(geom)
        result = _adapter().admit(geom, closure)
        all_candidates = (
            list(result.accepted) + list(result.blocked) + list(result.deferred)
        )
        assert len(all_candidates) >= 1, label
        for c in all_candidates:
            assert c.candidate_type == "MinimalUnitReadinessCandidate", (
                f"{label}: got candidate_type={c.candidate_type!r}"
            )
            assert c.candidate_type not in forbidden_types


def test_rule_forbidden_outputs_contains_constitutional_set():
    """The rule's forbidden_outputs tuple covers the §8 contract list +
    CONSTITUTIONAL_BASE + the forbidden MinimalIndependentMeaningCandidate
    name."""
    must_be_forbidden = {
        "HukmCandidate", "RealityClaim", "FinalMeaning", "FinalCaseJudgment",
        "DalalahCandidate", "WordCandidate", "LafzCandidate",
        "SentenceCandidate", "ParagraphCandidate",
        "DiscourseGeometryCandidate", "TextGeometryCandidate",
        "MinimalIndependentMeaningCandidate",
    }
    for rule in MINIMAL_UNIT_READINESS_RULES:
        assert must_be_forbidden.issubset(set(rule.forbidden_outputs))
        assert rule.output_candidate_type == "MinimalUnitReadinessCandidate"
        assert rule.output_candidate_type not in must_be_forbidden


# ===========================================================================
# 8. is_minimal_unit_ready lives on trace_ids, never on identity_ids
# ===========================================================================


def test_is_minimal_unit_ready_marker_on_trace_ids_not_identity_ids():
    """Per MIU contract §5: ``is_minimal_unit_ready`` is metadata on
    ``trace_ids`` only — never on ``identity_ids``."""
    geom = _seed_geometry_for_letter(_CP["ب"], trace_label="ba_marker")
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)
    assert len(result.accepted) == 1
    c = result.accepted[0]

    ready_in_trace = any(
        t.startswith("trace:miu_readiness:is_minimal_unit_ready:")
        for t in c.trace_ids
    )
    assert ready_in_trace, "ready marker must appear in trace_ids"

    ready_in_identity = any(
        i.startswith("trace:miu_readiness:is_minimal_unit_ready:")
        for i in c.identity_ids
    )
    assert not ready_in_identity, "ready marker must not appear in identity_ids"


def test_admitted_candidate_has_ready_marker_true():
    """An ACCEPTED MinimalUnitReadinessCandidate carries an
    ``is_minimal_unit_ready:true`` trace entry."""
    geom = _seed_geometry_for_letter(_CP["ف"], trace_label="fa_ready")
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)
    c = result.accepted[0]
    assert any(
        t == "trace:miu_readiness:is_minimal_unit_ready:true"
        for t in c.trace_ids
    )


def test_blocked_candidate_has_ready_marker_false():
    """A BLOCKED MinimalUnitReadinessCandidate carries an
    ``is_minimal_unit_ready:false`` trace entry — the marker still
    appears, but reflects the actual readiness state."""
    geom = _seed_geometry_for_letter(_CP["ض"], trace_label="dad_not_ready")
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)
    c = result.blocked[0]
    assert any(
        t == "trace:miu_readiness:is_minimal_unit_ready:false"
        for t in c.trace_ids
    )


# ===========================================================================
# 9. Constitutional structural guards
# ===========================================================================


def test_identity_trace_separation_preserved_in_output():
    """Per CLAUDE.md §4 invariants 1–3, the output's identity_ids and
    trace_ids remain disjoint."""
    geom = _seed_geometry_for_letter(_CP["ك"], trace_label="kaf_id")
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)
    c = result.accepted[0]
    assert set(c.identity_ids).isdisjoint(set(c.trace_ids))


def test_geometry_identity_preserved_in_readiness_output():
    """Identity preservation: the geometry's identity_ids appear in the
    readiness candidate's identity_ids (CLAUDE.md §4 invariant 4)."""
    geom = _seed_geometry_for_letter(_CP["ل"], trace_label="lam_pres")
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)
    c = result.accepted[0]
    assert set(geom.identity_ids).issubset(set(c.identity_ids))


def test_no_forbidden_final_flags_on_output():
    """The output's output_flags never contains a final-judgment flag."""
    forbidden = {
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "FinalCaseJudgment", "DalalahCandidate",
    }
    for letter_cp, label in [
        (_CP["س"], "seen_flags"),
        (_CP["ض"], "dad_flags"),
    ]:
        geom = _seed_geometry_for_letter(letter_cp, trace_label=label)
        closure = _closure_for(geom)
        result = _adapter().admit(geom, closure)
        all_candidates = (
            list(result.accepted) + list(result.blocked) + list(result.deferred)
        )
        for c in all_candidates:
            assert not (c.output_flags & forbidden)


# ===========================================================================
# 10. Source-scan guards — no forbidden type names defined in the module
# ===========================================================================


def _adapter_source() -> str:
    import qiyas_core.minimal_unit_readiness_adapter as mod
    return inspect.getsource(mod)


def _rule_source() -> str:
    import qiyas_core.rules.minimal_unit_readiness_rules as mod
    return inspect.getsource(mod)


def test_no_minimal_independent_meaning_candidate_class_defined():
    """The forbidden name MinimalIndependentMeaningCandidate (MIU §5)
    must not be defined as a class anywhere in the adapter or rule
    module."""
    for source in (_adapter_source(), _rule_source()):
        for line in source.splitlines():
            stripped = line.strip()
            assert not stripped.startswith(
                ("class MinimalIndependentMeaningCandidate",
                 "MinimalIndependentMeaningCandidate =")
            ), f"forbidden type defined: {line!r}"


def test_no_higher_layer_typed_unit_classes_defined():
    """No WordCandidate / LafzCandidate / SentenceCandidate /
    ParagraphCandidate / DalalahCandidate / FinalMeaning / HukmCandidate
    / RealityClaim / FinalCaseJudgment class is defined in the
    adapter or rule modules."""
    forbidden_class_definitions = (
        "class WordCandidate",
        "class LafzCandidate",
        "class SentenceCandidate",
        "class ParagraphCandidate",
        "class DiscourseGeometryCandidate",
        "class TextGeometryCandidate",
        "class DalalahCandidate",
        "class FinalMeaning",
        "class HukmCandidate",
        "class RealityClaim",
        "class FinalCaseJudgment",
    )
    for source in (_adapter_source(), _rule_source()):
        for line in source.splitlines():
            for prefix in forbidden_class_definitions:
                assert not line.strip().startswith(prefix), (
                    f"forbidden type defined: {line!r}"
                )


# ===========================================================================
# 11. Sanity — visual readout of the four cases (single test)
# ===========================================================================


def test_overview_visual_readout_of_four_cases():
    """One test that exercises an ACCEPTED, BLOCKED-by-registry,
    BLOCKED-by-length, and DEFERRED case in sequence, recording the
    resulting status for each. This is the single test the maintainer
    requested as a visual end-to-end witness."""
    cases = [
        ("بِ — accepted", _seed_geometry_for_letter(_CP["ب"], trace_label="O_ba"), "accepted"),
        ("ضَ — blocked by registry",
         _seed_geometry_for_letter(_CP["ض"], trace_label="O_dad"), "blocked"),
        ("ضَرَبَ-like — blocked by length>1",
         _length_2_geometry(), "blocked"),
        ("وَ — deferred by variant ambiguity",
         _seed_geometry_for_letter(_CP["و"], trace_label="O_waw"), "deferred"),
    ]
    adapter = _adapter()
    for label, geom, expected_bucket in cases:
        closure = _closure_for(geom)
        result = adapter.admit(geom, closure)
        bucket = (
            "accepted" if result.accepted
            else "deferred" if result.deferred
            else "blocked"
        )
        assert bucket == expected_bucket, (
            f"{label}: expected {expected_bucket}, got {bucket}; "
            f"residuals="
            f"{[_residual_types(c) for c in (result.accepted + result.blocked + result.deferred)]}"
        )


# ===========================================================================
# 9. PR #82 — optional ArabicVariantResolutionEvidence consumption
# ===========================================================================
#
# Per ARABIC_VARIANT_RESOLUTION_CONTRACT.md §7 / §10.3 the MIU
# readiness layer accepts an OPTIONAL evidence carrier that removes
# the `variant_ambiguity` defer reason for multi-variant symbols
# (و / ي). Presence of evidence does NOT by itself authorise
# admission; ALL existing MIU invariants still apply.
#
# Registry-eligibility facts for this section (verified against
# data/arabic_articulation_registry.json):
#   lips_waw_non_madd  →  can_function_as_minimal_independent_unit = True
#   jawf_waw_madd      →  can_function_as_minimal_independent_unit = False
#   tongue_ya_non_madd →  can_function_as_minimal_independent_unit = False
#   jawf_ya_madd       →  can_function_as_minimal_independent_unit = False
# ---------------------------------------------------------------------------


def _make_waw_geometry(*, trace_label: str = "W_var") -> Candidate:
    return _seed_geometry_for_letter(
        _CP["و"], trace_label=trace_label, haraka_cp="064e",  # fatha
    )


def _make_ya_geometry(*, trace_label: str = "Y_var") -> Candidate:
    return _seed_geometry_for_letter(
        _CP["ي"], trace_label=trace_label, haraka_cp="064e",  # fatha
    )


def _evidence_for(geom: Candidate) -> ArabicVariantResolutionEvidence:
    """Run the real resolver against a real seed geometry."""
    ev = ArabicVariantResolver().resolve(geom)
    assert ev is not None, (
        "Test fixture broken: resolver returned None for what should be "
        "a licensed non_madd case."
    )
    return ev


# --- Case D: وَ + valid non_madd evidence → ACCEPTED -----------------


def test_waw_with_valid_non_madd_evidence_is_accepted():
    """Case D (Phase 4): و is multi-variant; supplied evidence
    resolves to lips_waw_non_madd which is eligible. With all other
    MIU gates passing, the result is ACCEPTED. variant_ambiguity is
    no longer in the residuals."""
    geom = _make_waw_geometry(trace_label="W_accept")
    closure = _closure_for(geom)
    evidence = _evidence_for(geom)

    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    assert len(result.accepted) == 1, (
        f"وَ + non_madd evidence must accept; "
        f"blocked={[_residual_types(c) for c in result.blocked]}; "
        f"deferred={[_residual_types(c) for c in result.deferred]}"
    )
    c = result.accepted[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert c.status == CandidateStatus.ACCEPTED
    assert "CandidateOnly" in c.output_flags
    assert "deferred_variant_ambiguity" not in _residual_types(c)


def test_waw_with_evidence_output_has_only_candidate_only_flag():
    """Variant evidence does not introduce any forbidden output
    flag. CandidateOnly is the only output flag."""
    geom = _make_waw_geometry(trace_label="W_flag")
    closure = _closure_for(geom)
    evidence = _evidence_for(geom)

    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    c = result.accepted[0]
    assert c.output_flags == frozenset({"CandidateOnly"})


def test_waw_with_evidence_does_not_produce_meaning_or_hukm():
    """The ACCEPTED candidate's candidate_type and output_flags
    contain NO Word / Dalalah / FinalMeaning / Hukm / Reality
    fingerprint."""
    geom = _make_waw_geometry(trace_label="W_no_meaning")
    closure = _closure_for(geom)
    evidence = _evidence_for(geom)

    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    c = result.accepted[0]
    forbidden = {
        "WordCandidate", "LafzCandidate", "DalalahCandidate",
        "FinalMeaning", "HukmCandidate", "RealityClaim",
        "FinalCaseJudgment", "MinimalIndependentMeaningCandidate",
    }
    assert c.candidate_type not in forbidden
    assert not (frozenset(forbidden) & c.output_flags)


def test_waw_with_evidence_records_variant_resolution_trace():
    """An audit trace entry records that variant resolution
    evidence was applied; it lives on trace_ids, never on
    identity_ids."""
    geom = _make_waw_geometry(trace_label="W_audit")
    closure = _closure_for(geom)
    evidence = _evidence_for(geom)

    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    c = result.accepted[0]
    on_trace = any(
        t.startswith("trace:miu_readiness:variant_resolution:applied:")
        for t in c.trace_ids
    )
    assert on_trace, (
        f"variant_resolution applied trace missing; trace_ids={c.trace_ids}"
    )
    on_identity = any(
        i.startswith("trace:miu_readiness:variant_resolution:")
        for i in c.identity_ids
    )
    assert not on_identity, "variant_resolution audit must not appear on identity_ids"


# --- Case B repeat: وَ without evidence still DEFERRED ---------------


def test_waw_without_evidence_still_deferred():
    """Case B unchanged: omitting variant_resolution_evidence
    preserves the existing DEFERRED behaviour for وَ."""
    geom = _make_waw_geometry(trace_label="W_no_ev")
    closure = _closure_for(geom)
    result = _adapter().admit(geom, closure)
    assert len(result.deferred) == 1
    c = result.deferred[0]
    assert c.status == CandidateStatus.DEFERRED
    assert "deferred_variant_ambiguity" in _residual_types(c)


# --- Case C: invalid evidence variants ------------------------------


def test_waw_with_evidence_for_different_geometry_is_deferred():
    """Case F (Phase 4): evidence whose geometry_candidate_id does
    not match the consumed geometry is foreign; treated as absent
    (DEFER, never BLOCK)."""
    geom_a = _make_waw_geometry(trace_label="W_mismatch_a")
    geom_b = _make_waw_geometry(trace_label="W_mismatch_b")
    closure = _closure_for(geom_a)
    evidence_for_b = _evidence_for(geom_b)

    result = _adapter().admit(
        geom_a, closure, variant_resolution_evidence=evidence_for_b,
    )
    assert len(result.deferred) == 1
    c = result.deferred[0]
    assert c.status == CandidateStatus.DEFERRED
    assert "deferred_variant_ambiguity" in _residual_types(c)


def test_waw_with_evidence_for_different_symbol_is_deferred():
    """Evidence whose symbol does not match is foreign; DEFER."""
    geom_waw = _make_waw_geometry(trace_label="W_wrongsym")
    geom_ya = _make_ya_geometry(trace_label="Y_wrongsym")
    closure = _closure_for(geom_waw)
    evidence_for_ya = _evidence_for(geom_ya)

    result = _adapter().admit(
        geom_waw, closure, variant_resolution_evidence=evidence_for_ya,
    )
    assert len(result.deferred) == 1
    assert "deferred_variant_ambiguity" in _residual_types(
        result.deferred[0]
    )


def test_waw_with_malformed_evidence_unreserved_variant_is_deferred():
    """Evidence carrying a non-reserved variant label is malformed;
    treated as absent (DEFER, not BLOCK)."""
    geom = _make_waw_geometry(trace_label="W_malformed_var")
    closure = _closure_for(geom)
    malformed = ArabicVariantResolutionEvidence(
        symbol="و",
        selected_variant="invented_label",
        selected_entry_id="lips_waw_non_madd",
        selection_basis=("haraka_function_self",),
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        evidence_id="ev:malformed:001",
        audit_trace_ids=(),
    )
    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=malformed,
    )
    assert len(result.deferred) == 1
    assert "deferred_variant_ambiguity" in _residual_types(
        result.deferred[0]
    )


def test_waw_with_malformed_evidence_unknown_entry_id_is_deferred():
    """Evidence pointing to a registry entry id that does not exist
    is malformed; treated as absent (DEFER, not BLOCK)."""
    geom = _make_waw_geometry(trace_label="W_malformed_entry")
    closure = _closure_for(geom)
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
        evidence_id="ev:malformed:002",
        audit_trace_ids=(),
    )
    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=malformed,
    )
    assert len(result.deferred) == 1


def test_waw_with_inconsistent_variant_label_is_deferred():
    """Evidence whose selected_variant disagrees with the registry
    entry's variant field is inconsistent; treated as absent (DEFER)."""
    geom = _make_waw_geometry(trace_label="W_inconsistent")
    closure = _closure_for(geom)
    # selected_variant says madd but selected_entry_id points to the
    # non_madd entry — disagreement.
    inconsistent = ArabicVariantResolutionEvidence(
        symbol="و",
        selected_variant="madd",
        selected_entry_id="lips_waw_non_madd",  # actually non_madd
        selection_basis=("haraka_function_before",),
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        evidence_id="ev:inconsistent:001",
        audit_trace_ids=(),
    )
    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=inconsistent,
    )
    assert len(result.deferred) == 1


# --- Case E: synthetic madd evidence ⇒ BLOCKED via eligibility -------


def test_waw_with_synthetic_madd_evidence_is_blocked_by_eligibility():
    """Case E (Phase 4): if a future resolver supplies madd evidence
    for و, the resolved entry jawf_waw_madd has
    can_function_as_minimal_independent_unit = False. Variant
    ambiguity is removed, but the readiness layer BLOCKS via
    symbol_not_eligible_for_minimal_unit. No meaning, no hukm."""
    geom = _make_waw_geometry(trace_label="W_madd_block")
    closure = _closure_for(geom)
    madd_evidence = ArabicVariantResolutionEvidence(
        symbol="و",
        selected_variant="madd",
        selected_entry_id="jawf_waw_madd",
        selection_basis=("haraka_function_before",),
        geometry_candidate_id=geom.candidate_id,
        geometry_layer=FIXED_GEOMETRY_LAYER,
        geometry_length=FIXED_GEOMETRY_LENGTH,
        geometry_construction_mode=FIXED_GEOMETRY_CONSTRUCTION_MODE,
        geometry_identity_ids=tuple(geom.identity_ids),
        geometry_trace_ids=tuple(geom.trace_ids),
        evidence_id="ev:madd_synth:001",
        audit_trace_ids=(),
    )
    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=madd_evidence,
    )
    assert len(result.blocked) == 1, (
        f"Expected BLOCKED via eligibility; "
        f"accepted={len(result.accepted)} deferred={len(result.deferred)}"
    )
    c = result.blocked[0]
    assert c.status == CandidateStatus.BLOCKED
    assert "blocking_fariq_present" in _residual_types(c)
    # The candidate is still MinimalUnitReadinessCandidate — never
    # Word / Dalalah / Meaning / Hukm / Reality.
    assert c.candidate_type == "MinimalUnitReadinessCandidate"


# --- يَ — conservative: registry non-eligible for tongue_ya_non_madd ----


def test_ya_with_valid_non_madd_evidence_is_blocked_by_eligibility():
    """ي + valid non_madd evidence: the registry entry
    `tongue_ya_non_madd` has
    can_function_as_minimal_independent_unit = False under the
    current registry. variant_ambiguity is removed, BUT the
    readiness layer BLOCKS via symbol_not_eligible_for_minimal_unit.
    This pins the conservative behaviour: presence of evidence does
    not by itself authorise admission."""
    geom = _make_ya_geometry(trace_label="Y_block_eligibility")
    closure = _closure_for(geom)
    evidence = _evidence_for(geom)

    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=evidence,
    )
    assert len(result.blocked) == 1, (
        f"يَ + non_madd evidence must be BLOCKED via eligibility under "
        f"the current registry; accepted={len(result.accepted)} "
        f"deferred={len(result.deferred)}"
    )
    c = result.blocked[0]
    assert c.candidate_type == "MinimalUnitReadinessCandidate"
    assert "blocking_fariq_present" in _residual_types(c)


# --- Evidence does not override structural gates --------------------


def test_evidence_does_not_override_length_greater_than_one():
    """Case G (Phase 4): variant evidence must not bypass the
    length=1 gate. A length>1 geometry stays BLOCKED even with
    valid resolver evidence."""
    geom = _length_2_geometry()
    closure = _closure_for(geom)
    # Build a fixture evidence carrier for this geometry (no real
    # resolver runs because the resolver requires length=1).
    forced = ArabicVariantResolutionEvidence(
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
        evidence_id="ev:forced_for_length2:001",
        audit_trace_ids=(),
    )
    result = _adapter().admit(
        geom, closure, variant_resolution_evidence=forced,
    )
    assert len(result.accepted) == 0
    # Length and construction-mode fariqs block regardless of evidence.
    assert (len(result.blocked) + len(result.deferred)) == 1


def test_evidence_does_not_override_missing_closure():
    """Case G/H continuation: missing closure evidence still
    BLOCKS, regardless of variant resolution evidence presence."""
    geom = _make_waw_geometry(trace_label="W_no_closure_with_ev")
    # Build evidence from the geometry directly so symbol/id match.
    evidence = ArabicVariantResolver().resolve(geom)
    assert evidence is not None
    result = _adapter().admit(
        geom, closure_evidence=None,
        variant_resolution_evidence=evidence,
    )
    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    c = result.blocked[0]
    assert "blocking_fariq_present" in _residual_types(c)


# --- Constitutional guards on the MIU module ------------------------


def test_miu_adapter_does_not_define_forbidden_candidate_types():
    """The MIU adapter module must NOT define any forbidden Candidate
    type per CLAUDE.md §3 / §19 + MIU contract §8."""
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
        "DiscourseGeometryCandidate",
        "TextGeometryCandidate",
        "MinimalIndependentMeaningCandidate",
        "SentenceGeometry",
    )
    for name in forbidden:
        assert not hasattr(miu_adapter_mod, name), (
            f"forbidden symbol must not be defined in MIU adapter: {name}"
        )


def test_miu_adapter_does_not_import_forbidden_higher_layers():
    """The MIU adapter module must NOT import from any forbidden
    higher-layer module (Word/Lafz/Dalalah/Sentence/Discourse/Text/
    Meaning/Hukm/Reality). The existing QiyasKernel usage is
    PRESERVED — MIU is a Qiyas-shaped adapter by design and the
    guard targets only the forbidden higher layers.
    """
    import ast as _ast
    source = inspect.getsource(miu_adapter_mod)
    tree = _ast.parse(source)
    imported: set[str] = set()
    for node in _ast.walk(tree):
        if isinstance(node, _ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, _ast.Import):
            for alias in node.names:
                imported.add(alias.name)
    forbidden_substrings = (
        "word", "lafz", "dalalah",
        "sentence", "discourse", "text_geometry",
        "meaning", "hukm", "reality",
        "final_case_judgment",
        "minimal_independent_meaning",
        "sentence_geometry",
    )
    for mod in imported:
        lower = mod.lower()
        for needle in forbidden_substrings:
            assert needle not in lower, (
                f"forbidden higher-layer import in MIU adapter: {mod}"
            )


def test_miu_adapter_does_not_mutate_registry():
    """The MIU adapter must consume the registry read-only. No
    writer / setter / save / mutation helpers may appear."""
    source = inspect.getsource(miu_adapter_mod)
    forbidden_calls = (
        "save_articulation",
        "set_articulation",
        "update_articulation",
        "add_articulation",
        "delete_articulation",
    )
    for needle in forbidden_calls:
        assert needle not in source, (
            f"registry-mutation helper must not be called: {needle}"
        )
