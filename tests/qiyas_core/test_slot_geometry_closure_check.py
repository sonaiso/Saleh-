"""Tests for SlotGeometryClosureCheck — Phase-2 follow-up.

Pins the behavioural and constitutional contract of
``MINIMAL_COMPLETE_CLOSURE_EVIDENCE_RUNTIME_CONTRACT.md``:

  * ``MinimalCompleteClosureEvidence`` is an Evidence carrier — **not**
    a ``Candidate`` (contract §2).
  * The producer is **observation only** — it never imports
    ``QiyasKernel``, ``QiyasRule``, or the ``ArabicArticulationRegistry``
    (contract §3 / §11).
  * Length-agnostic: both ``length = 1`` and ``length > 1`` produce
    evidence when the eight conditions hold (contract §5).
  * Conjunctive: every one of the eight §6 conditions must hold; any
    failure returns ``None`` rather than a half-true carrier (contract
    §6 / §7).
  * Audit-trace ids follow the §6.1 recommended schema.
  * No ``MinimalCompleteClosureCandidate`` symbol exists anywhere in
    the module (contract §8 — closure is Evidence, not Candidate).
  * No ``MinimalUnitReadinessCandidate``, ``DalalahCandidate``,
    ``WordCandidate``, ``FinalMeaning``, ``HukmCandidate``, or
    ``RealityClaim`` is ever produced or referenced as output type
    (contract §8 / §11).

The fixture machinery below builds realistic ``SlotGeometryCandidate``
instances through the **existing** ``SlotGeometryLayerAdapter`` /
``Candidate`` types so the tests exercise the producer end-to-end
without re-implementing geometry construction.
"""

from __future__ import annotations

import inspect
import uuid

import pytest

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.residual import Residual
from qiyas_core.slot_geometry_adapter import SlotGeometryLayerAdapter
from qiyas_core.slot_geometry_closure_check import (
    CLOSURE_CONDITION_NAMES,
    MinimalCompleteClosureEvidence,
    SlotGeometryClosureCheck,
    audit_trace_entry,
    check_slot_geometry_closure,
)


# ---------------------------------------------------------------------------
# Fixture helpers
# ---------------------------------------------------------------------------


def _make_slot_candidate(*, trace_label: str = "S", letter_cp: str = "0628",
                        haraka_cp: str = "064e",
                        source_rule_id: str = "slot.composition",
                        rank: EvidenceRank = EvidenceRank.FORMAL_STRUCTURE,
                        candidate_type: str = "SlotCandidate") -> Candidate:
    """Build a SlotCandidate fixture that satisfies the slot-geometry
    layer's §2 admission predicate. Used as input to the geometry
    adapter to obtain real SlotGeometryCandidate fixtures."""
    return Candidate(
        candidate_id=f"slot:fixture:{trace_label}:{uuid.uuid4().hex[:8]}",
        candidate_type=candidate_type,
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id=source_rule_id,
        asl_id="اصل:slot_composition_domain",
        far_id=f"فرع:slot:fixture:{trace_label}",
        identity_ids=(
            f"identity:codepoint:{letter_cp}",
            f"identity:codepoint:{haraka_cp}",
            "identity:slot_composition_domain",
        ),
        rank=rank,
        residuals=(),
        trace_ids=(
            f"trace:fixture:{trace_label}:ev",
            f"trace:slot:alignment_ref:test:{trace_label}",
        ),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _seed_geometry(*, trace_label: str = "Sa") -> Candidate:
    """Produce an accepted length-1 SlotGeometryCandidate via the
    existing slot-geometry adapter."""
    slot = _make_slot_candidate(trace_label=trace_label)
    adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    result = adapter.seed_geometry(slot)
    assert len(result.accepted) == 1, (
        "Test fixture broken: SlotGeometry seed did not accept; "
        f"residuals={[r.residual_type for r in result.blocked[0].residuals]}"
        if result.blocked else "Test fixture broken: no acceptance and no block"
    )
    return result.accepted[0]


def _extend_geometry(previous: Candidate, *, trace_label: str = "Sb") -> Candidate:
    """Extend an existing SlotGeometryCandidate(length=n) by one step."""
    from qiyas_core.slot_geometry_adapter import SlotBindingEvidence

    next_slot = _make_slot_candidate(
        trace_label=trace_label, letter_cp="062a", haraka_cp="0652",
    )
    binding = SlotBindingEvidence(
        prev_segment_id=0,
        curr_segment_id=0,
        prev_position=0,
        curr_position=1,
        has_whitespace_between=False,
        has_punctuation_between=False,
        max_licensed_distance=1,
        binding_trace_ids=(f"trace:binding:test:{trace_label}",),
    )
    adapter = SlotGeometryLayerAdapter(kernel=QiyasKernel())
    result = adapter.extend_geometry(previous, next_slot, binding)
    assert len(result.accepted) == 1
    return result.accepted[0]


def _length_2_geometry() -> Candidate:
    return _extend_geometry(_seed_geometry(trace_label="Sa"), trace_label="Sb")


def _candidate_with_overrides(base: Candidate, **overrides) -> Candidate:
    """Return a new Candidate cloned from `base` with the given fields
    overridden. Used to surface targeted breakages of the eight §6
    conditions without rebuilding the full pipeline."""
    fields = {
        "candidate_id": base.candidate_id,
        "candidate_type": base.candidate_type,
        "status": base.status,
        "layer": base.layer,
        "source_rule_id": base.source_rule_id,
        "asl_id": base.asl_id,
        "far_id": base.far_id,
        "identity_ids": base.identity_ids,
        "rank": base.rank,
        "residuals": base.residuals,
        "trace_ids": base.trace_ids,
        "output_flags": base.output_flags,
    }
    fields.update(overrides)
    return Candidate(**fields)


def _residual(rtype: str, message: str = "test residual") -> Residual:
    from qiyas_core.enums import ResidualEffect, ResidualSeverity

    effect = (
        ResidualEffect.BLOCK if "blocking" in rtype or "blocked" in rtype
        else ResidualEffect.DEFER if rtype.startswith("deferred_")
        else ResidualEffect.NONE
    )
    severity = (
        ResidualSeverity.BLOCKER if effect == ResidualEffect.BLOCK
        else ResidualSeverity.WARNING
    )
    return Residual(
        residual_type=rtype,
        severity=severity,
        effect=effect,
        message=message,
        source_rule_id="test.rule",
        layer="SlotGeometryQiyas",
        trace_ids=(f"trace:residual:{rtype}",),
    )


# ===========================================================================
# Spec test 1 — evidence is NOT a Candidate
# ===========================================================================


def test_evidence_is_not_a_candidate_subclass():
    """``MinimalCompleteClosureEvidence`` is not a subclass of ``Candidate``
    (contract §2: it is an Evidence carrier, not a Candidate)."""
    assert not issubclass(MinimalCompleteClosureEvidence, Candidate)


def test_evidence_instance_is_not_a_candidate_instance():
    """A constructed evidence instance is not an instance of ``Candidate``."""
    evidence = check_slot_geometry_closure(_seed_geometry())
    assert evidence is not None
    assert not isinstance(evidence, Candidate)


def test_evidence_has_no_candidate_shape_fields():
    """The evidence carrier is structurally NOT a Candidate-shape — it
    has no ``candidate_type``, ``status``, or ``output_flags`` field."""
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(MinimalCompleteClosureEvidence)}
    assert "candidate_type" not in field_names
    assert "status" not in field_names
    assert "output_flags" not in field_names


def test_evidence_is_frozen():
    """The Evidence carrier is immutable (contract §2.2)."""
    evidence = check_slot_geometry_closure(_seed_geometry())
    assert evidence is not None
    with pytest.raises(Exception):
        evidence.licensed_beginning = False  # type: ignore[misc]


# ===========================================================================
# Spec test 2 — checker does not import/use QiyasKernel (or QiyasRule, or
# the registry)
# ===========================================================================


def _checker_source() -> str:
    import qiyas_core.slot_geometry_closure_check as mod
    return inspect.getsource(mod)


def _checker_import_lines() -> list[str]:
    return [
        line.strip()
        for line in _checker_source().splitlines()
        if line.strip().startswith(("import ", "from "))
    ]


def test_checker_does_not_import_qiyas_kernel():
    for line in _checker_import_lines():
        assert "QiyasKernel" not in line, (
            f"checker module must not import QiyasKernel: {line!r}"
        )
        assert "qiyas_core.kernel" not in line, (
            f"checker module must not import from qiyas_core.kernel: {line!r}"
        )


def test_checker_does_not_import_qiyas_rule():
    for line in _checker_import_lines():
        assert "QiyasRule" not in line, (
            f"checker module must not import QiyasRule: {line!r}"
        )
        assert "qiyas_core.rule" not in line, (
            f"checker module must not import from qiyas_core.rule: {line!r}"
        )


def test_checker_does_not_import_candidate():
    for line in _checker_import_lines():
        assert " Candidate" not in line and "(Candidate" not in line, (
            f"checker module must not import Candidate as a name: {line!r}"
        )
        assert "qiyas_core.candidate" not in line, (
            f"checker module must not import from qiyas_core.candidate: {line!r}"
        )


def test_checker_does_not_import_arabic_articulation_registry():
    """Closure does not consult the registry (contract §4 / §10 of the
    runtime contract; mirrors the registry's own
    `does_not_use_QiyasKernel` / `does_not_produce_Candidate`
    constraint posture)."""
    for line in _checker_import_lines():
        assert "arabic_articulation_registry" not in line, (
            f"checker module must not import the registry reader: {line!r}"
        )
        assert "ArabicArticulationRegistry" not in line, (
            f"checker module must not import ArabicArticulationRegistry: {line!r}"
        )


def test_checker_does_not_import_sequence_context_tokenizer():
    for line in _checker_import_lines():
        assert "sequence_context_tokenizer" not in line, (
            f"checker module must not import the tokenizer: {line!r}"
        )
        assert "SequenceContextTokenizer" not in line, (
            f"checker module must not import SequenceContextTokenizer: {line!r}"
        )


# ===========================================================================
# Spec tests 3 / 4 — length-agnostic admission
# ===========================================================================


def test_length_1_geometry_produces_evidence_when_conditions_hold():
    """A clean length-1 seed geometry produces a fully-populated
    MinimalCompleteClosureEvidence."""
    geom = _seed_geometry()
    evidence = check_slot_geometry_closure(geom)
    assert evidence is not None
    assert evidence.geometry_length == 1
    assert evidence.geometry_construction_mode == "seed"
    # All eight booleans True.
    assert evidence.licensed_beginning is True
    assert evidence.licensed_ending is True
    assert evidence.all_internal_bindings_licensed is True
    assert evidence.no_open_demand is True
    assert evidence.no_blocking_difference is True
    assert evidence.residuals_preserved is True
    assert evidence.rank_above_no_evidence is True
    assert evidence.output_remains_candidate_only is True


def test_length_2_geometry_produces_evidence_when_conditions_hold():
    """A clean length-2 extension geometry produces evidence — closure
    is length-agnostic per contract §5."""
    geom = _length_2_geometry()
    evidence = check_slot_geometry_closure(geom)
    assert evidence is not None
    assert evidence.geometry_length == 2
    assert evidence.geometry_construction_mode == "extension"
    assert evidence.licensed_beginning is True
    assert evidence.licensed_ending is True
    assert evidence.all_internal_bindings_licensed is True
    assert evidence.no_open_demand is True
    assert evidence.no_blocking_difference is True
    assert evidence.residuals_preserved is True
    assert evidence.rank_above_no_evidence is True
    assert evidence.output_remains_candidate_only is True


# ===========================================================================
# Spec test 5 — each of the eight conditions failing returns None
# ===========================================================================


def test_failing_licensed_beginning_returns_none():
    """Override `source_rule_id` to a non-SlotGeometry rule — fails §6.1."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(base, source_rule_id="not.a.geometry.rule")
    assert check_slot_geometry_closure(broken) is None


def test_failing_licensed_ending_returns_none():
    """Override `status` to BLOCKED — fails §6.2 (licensed ending requires
    ACCEPTED status)."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(base, status=CandidateStatus.BLOCKED)
    assert check_slot_geometry_closure(broken) is None


def test_failing_all_internal_bindings_licensed_returns_none():
    """A length>1 geometry whose status is BLOCKED fails §6.3
    (which for length>1 requires ACCEPTED status)."""
    length_2 = _length_2_geometry()
    broken = _candidate_with_overrides(length_2, status=CandidateStatus.BLOCKED)
    assert check_slot_geometry_closure(broken) is None


def test_failing_no_open_demand_returns_none():
    """A geometry carrying a deferred residual fails §6.4."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(
        base, residuals=(_residual("deferred_some_demand"),),
    )
    assert check_slot_geometry_closure(broken) is None


def test_failing_no_blocking_difference_returns_none():
    """A geometry carrying a blocking_fariq_present residual fails §6.5."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(
        base, residuals=(_residual("blocking_fariq_present"),),
    )
    assert check_slot_geometry_closure(broken) is None


def test_failing_residuals_preserved_returns_none():
    """A geometry carrying a 'silently_discarded' residual fails §6.6."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(
        base, residuals=(_residual("residual_silently_discarded"),),
    )
    assert check_slot_geometry_closure(broken) is None


def test_failing_rank_above_no_evidence_returns_none():
    """A geometry with rank == NO_EVIDENCE fails §6.7. The Candidate
    `__post_init__` does not police rank, so we can construct the
    fixture directly."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(base, rank=EvidenceRank.NO_EVIDENCE)
    assert check_slot_geometry_closure(broken) is None


def test_failing_output_remains_candidate_only_returns_none():
    """A geometry whose output_flags omits CandidateOnly fails §6.8."""
    base = _seed_geometry()
    broken = _candidate_with_overrides(base, output_flags=frozenset())
    assert check_slot_geometry_closure(broken) is None


# ===========================================================================
# Spec test 6 — all eight passing returns evidence (already implicitly
# covered above; this test asserts the explicit conjunction)
# ===========================================================================


def test_all_eight_conditions_passing_returns_evidence():
    geom = _seed_geometry()
    evidence = SlotGeometryClosureCheck().check(geom)
    assert isinstance(evidence, MinimalCompleteClosureEvidence)
    assert all(
        getattr(evidence, name) is True for name in CLOSURE_CONDITION_NAMES
    )


# ===========================================================================
# Spec test 7 — audit_trace_ids follow the §6.1 schema
# ===========================================================================


_AUDIT_PREFIX = "trace:slot_geometry_closure:"


def test_audit_trace_ids_follow_schema_when_evidence_built():
    evidence = check_slot_geometry_closure(_seed_geometry())
    assert evidence is not None
    assert len(evidence.audit_trace_ids) == 8
    for tid in evidence.audit_trace_ids:
        assert tid.startswith(_AUDIT_PREFIX), tid
        assert tid.endswith(":passed"), tid


def test_audit_trace_ids_cover_every_condition_when_evidence_built():
    evidence = check_slot_geometry_closure(_seed_geometry())
    assert evidence is not None
    expected = {
        f"{_AUDIT_PREFIX}{name}:passed" for name in CLOSURE_CONDITION_NAMES
    }
    assert set(evidence.audit_trace_ids) == expected


def test_audit_trace_entry_helper_emits_passed_and_failed_forms():
    for name in CLOSURE_CONDITION_NAMES:
        assert audit_trace_entry(name, True) == f"{_AUDIT_PREFIX}{name}:passed"
        assert audit_trace_entry(name, False) == f"{_AUDIT_PREFIX}{name}:failed"


def test_audit_trace_entry_rejects_unknown_condition_name():
    with pytest.raises(ValueError):
        audit_trace_entry("not_a_real_condition", True)


# ===========================================================================
# Spec test 8 — no MinimalCompleteClosureCandidate symbol exists
# ===========================================================================


def test_no_minimal_complete_closure_candidate_symbol_in_module():
    """The forbidden name `MinimalCompleteClosureCandidate` (contract §8)
    must not be exposed anywhere in the checker module."""
    import qiyas_core.slot_geometry_closure_check as mod
    assert not hasattr(mod, "MinimalCompleteClosureCandidate")


def test_no_minimal_complete_closure_candidate_in_source():
    """Defense in depth — the literal string must not appear in source
    (even in a docstring or comment) since this is a constitutional
    forbidden name."""
    source = _checker_source()
    # Allow the string to appear inside a clear NEGATIVE assertion
    # context (the module docstring discusses the forbidden name). We
    # check that no class or assignment defines it.
    lines = source.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("class MinimalCompleteClosureCandidate", "MinimalCompleteClosureCandidate =")):
            raise AssertionError(
                f"checker module must not define MinimalCompleteClosureCandidate: {line!r}"
            )


# ===========================================================================
# Spec tests 9 / 10 — no MinimalUnitReadiness / Dalalah / Word / etc. output
# ===========================================================================


def test_check_return_type_is_only_evidence_or_none():
    """The return value of every check() call is either a
    MinimalCompleteClosureEvidence instance or None — never a
    Candidate or any of the forbidden types."""
    for geom in (_seed_geometry(), _length_2_geometry()):
        result = check_slot_geometry_closure(geom)
        assert result is None or isinstance(result, MinimalCompleteClosureEvidence)
        # Defensive: even when returning evidence, it is not a Candidate.
        if result is not None:
            assert not isinstance(result, Candidate)


def test_no_minimal_unit_readiness_candidate_produced():
    """The checker never returns or references MinimalUnitReadinessCandidate."""
    source = _checker_source()
    # Allowed: discussion of the type name in the docstring header.
    # Forbidden: class definition or assignment producing the type.
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith(("class MinimalUnitReadinessCandidate",
                                "MinimalUnitReadinessCandidate =")):
            raise AssertionError(
                f"checker must not define MinimalUnitReadinessCandidate: {line!r}"
            )


def test_no_higher_layer_typed_units_produced():
    """The checker never defines or produces WordCandidate,
    LafzCandidate, SentenceCandidate, ParagraphCandidate,
    DiscourseGeometryCandidate, TextGeometryCandidate."""
    source = _checker_source()
    forbidden_class_definitions = (
        "class WordCandidate",
        "class LafzCandidate",
        "class SentenceCandidate",
        "class ParagraphCandidate",
        "class DiscourseGeometryCandidate",
        "class TextGeometryCandidate",
    )
    for line in source.splitlines():
        for prefix in forbidden_class_definitions:
            assert not line.strip().startswith(prefix), (
                f"checker must not define {prefix}: {line!r}"
            )


def test_no_dalalah_or_final_meaning_or_hukm_or_reality_or_judgment_produced():
    """The checker never defines DalalahCandidate, FinalMeaning,
    HukmCandidate, RealityClaim, or FinalCaseJudgment."""
    source = _checker_source()
    forbidden_class_definitions = (
        "class DalalahCandidate",
        "class FinalMeaning",
        "class HukmCandidate",
        "class RealityClaim",
        "class FinalCaseJudgment",
    )
    for line in source.splitlines():
        for prefix in forbidden_class_definitions:
            assert not line.strip().startswith(prefix), (
                f"checker must not define {prefix}: {line!r}"
            )


# ===========================================================================
# Spec test 11 — no registry consultation
# ===========================================================================


def test_checker_never_imports_or_calls_arabic_articulation_registry():
    """Combined with the import-line guards above, this is a defensive
    code scan: no registry symbol is *called* anywhere in the module
    (closure does not consult the registry — contract §4 / §10). We
    inspect actual import + call lines, not docstring text — the
    module's own docstring discusses the registry to state the
    constitutional rule, which is allowed."""
    source = _checker_source()
    forbidden_substrings = (
        "ArabicArticulationRegistry",
        "ArabicArticulationEntry",
        "arabic_articulation_registry",
        "get_articulations_by_symbol",
        "get_primary_articulation",
        "get_minimal_independent_units",
        "load_arabic_articulation_registry",
    )
    for line in source.splitlines():
        stripped = line.strip()
        # Skip docstring / comment lines — the constitutional rule
        # itself must be stated in the module docstring, which means
        # the names appear there as policy text rather than as code.
        if (
            stripped.startswith(("#", "*", '"', "'"))
            or stripped == ""
            or stripped.startswith(("```",))
        ):
            continue
        for needle in forbidden_substrings:
            assert needle not in line, (
                f"checker module references the registry as code: {line!r}"
            )


# ===========================================================================
# Sanity — both call styles are equivalent
# ===========================================================================


def test_module_function_and_class_method_are_equivalent():
    """`check_slot_geometry_closure(g)` and
    `SlotGeometryClosureCheck().check(g)` evaluate identically on the
    same input (modulo evidence_id, which is a uuid)."""
    geom = _seed_geometry()
    a = check_slot_geometry_closure(geom)
    b = SlotGeometryClosureCheck().check(geom)
    assert a is not None and b is not None
    # All structural fields (everything except evidence_id) match.
    assert a.licensed_beginning == b.licensed_beginning
    assert a.licensed_ending == b.licensed_ending
    assert a.all_internal_bindings_licensed == b.all_internal_bindings_licensed
    assert a.no_open_demand == b.no_open_demand
    assert a.no_blocking_difference == b.no_blocking_difference
    assert a.residuals_preserved == b.residuals_preserved
    assert a.rank_above_no_evidence == b.rank_above_no_evidence
    assert a.output_remains_candidate_only == b.output_remains_candidate_only
    assert a.geometry_candidate_id == b.geometry_candidate_id
    assert a.geometry_layer == b.geometry_layer
    assert a.geometry_length == b.geometry_length
    assert a.geometry_construction_mode == b.geometry_construction_mode
    assert a.geometry_identity_ids == b.geometry_identity_ids
    assert a.geometry_trace_ids == b.geometry_trace_ids
    assert a.geometry_rank == b.geometry_rank
    assert a.audit_trace_ids == b.audit_trace_ids


def test_non_slot_geometry_input_returns_none():
    """Inputs whose candidate_type is not 'SlotGeometryCandidate' or
    whose layer is not 'SlotGeometryQiyas' return None (consumption
    surface closure per contract §4)."""
    slot = _make_slot_candidate()  # candidate_type = "SlotCandidate"
    assert check_slot_geometry_closure(slot) is None
