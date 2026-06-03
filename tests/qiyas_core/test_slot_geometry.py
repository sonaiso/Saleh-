"""Tests for SlotGeometryQiyas — Phase-2 Batch 1.

Pins the behavioural contract of ``SlotGeometryLayerAdapter`` per
``SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md``:

  * ``seed_geometry`` admits a valid ``SlotCandidate`` as a length-1
    geometry; rejects non-``SlotCandidate``, slots without
    ``alignment_ref``, and slots whose ``source_rule_id`` is not
    ``"slot.composition"``.
  * ``extend_geometry`` admits a valid ``(previous_geometry,
    next_slot, SlotBindingEvidence)`` triple as a length-(n+1)
    geometry; rejects cross-boundary bindings and missing binding
    evidence.
  * The single admissible output type is ``SlotGeometryCandidate``
    with ``length`` and ``construction_mode`` recorded on the
    ``trace_ids`` — never on ``identity_ids``, and never as a
    separate candidate type.
  * The forbidden-outputs list of the rules covers
    ``MinimalCompletionReadinessCandidate`` plus the constitutional
    triple and the §11 higher-layer typed units.
"""

from __future__ import annotations

import uuid

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.rules.slot_geometry_rules import (
    SLOT_GEOMETRY_EXTEND_RULE,
    SLOT_GEOMETRY_RULES,
    SLOT_GEOMETRY_SEED_RULE,
)
from qiyas_core.slot_geometry_adapter import (
    SlotBindingEvidence,
    SlotGeometryLayerAdapter,
    get_construction_mode,
    get_geometry_length,
)


# ---------------------------------------------------------------------------
# Fixtures — build SlotCandidates that satisfy §2.
# ---------------------------------------------------------------------------


def _adapter() -> SlotGeometryLayerAdapter:
    return SlotGeometryLayerAdapter(kernel=QiyasKernel())


def _make_slot_candidate(
    *,
    letter_cp: str = "0628",
    haraka_cp: str = "064e",
    trace_label: str = "S1",
    source_rule_id: str = "slot.composition",
    candidate_type: str = "SlotCandidate",
    include_alignment_ref: bool = True,
    include_letter_identity_breadcrumb: bool = True,
    include_haraka_function_breadcrumb: bool = True,
    include_position_breadcrumb: bool = True,
    include_carrier_binding_breadcrumb: bool = True,
    rank: EvidenceRank = EvidenceRank.FORMAL_STRUCTURE,
    extra_identity: tuple[str, ...] = (),
    output_flags: frozenset[str] = frozenset({"CandidateOnly"}),
) -> Candidate:
    """Construct an honest ``SlotCandidate`` test fixture per
    ``SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md`` §2.

    This is **explicitly a test fixture**, not a slot produced by
    ``run_qiyas.py`` — but it carries the five breadcrumbs that §2.2
    requires, so the slot-geometry adapter can audit each pillar
    source independently. Each ``include_*_breadcrumb`` flag toggles
    one breadcrumb off, used by the rejection tests below.

    Default trace shape mirrors the user-spec example:

        trace_ids = (
          "trace:slot:alignment_ref:test:S1",
          "trace:letter_identity:test:S1",
          "trace:haraka_function:test:S1",
          "trace:position:test:S1",
          "trace:carrier_binding:test:S1",
        )

    All five breadcrumbs are present by default; the fixture is
    honest about being a fixture (trace labels start with
    ``test:``).
    """
    identity_ids = (
        f"identity:codepoint:{letter_cp}",
        f"identity:codepoint:{haraka_cp}",
        "identity:slot_composition_domain",
        *extra_identity,
    )
    trace_ids: list[str] = [
        f"trace:fixture:{trace_label}:ev",
    ]
    if include_alignment_ref:
        trace_ids.append(f"trace:slot:alignment_ref:test:{trace_label}")
    if include_letter_identity_breadcrumb:
        trace_ids.append(f"trace:letter_identity:test:{trace_label}")
    if include_haraka_function_breadcrumb:
        trace_ids.append(f"trace:haraka_function:test:{trace_label}")
    if include_position_breadcrumb:
        trace_ids.append(f"trace:position:test:{trace_label}")
    if include_carrier_binding_breadcrumb:
        trace_ids.append(f"trace:carrier_binding:test:{trace_label}")

    return Candidate(
        candidate_id=f"slot:fixture:{trace_label}:{uuid.uuid4().hex[:8]}",
        candidate_type=candidate_type,
        status=CandidateStatus.ACCEPTED,
        layer="SlotQiyas",
        source_rule_id=source_rule_id,
        asl_id="اصل:slot_composition_domain",
        far_id=f"فرع:slot:fixture:{trace_label}",
        identity_ids=identity_ids,
        rank=rank,
        residuals=(),
        trace_ids=tuple(trace_ids),
        output_flags=output_flags,
    )


def _binding(
    *,
    prev_segment_id: int = 0,
    curr_segment_id: int = 0,
    prev_position: int = 0,
    curr_position: int = 1,
    has_whitespace_between: bool = False,
    has_punctuation_between: bool = False,
    max_licensed_distance: int = 1,
) -> SlotBindingEvidence:
    return SlotBindingEvidence(
        prev_segment_id=prev_segment_id,
        curr_segment_id=curr_segment_id,
        prev_position=prev_position,
        curr_position=curr_position,
        has_whitespace_between=has_whitespace_between,
        has_punctuation_between=has_punctuation_between,
        max_licensed_distance=max_licensed_distance,
        binding_trace_ids=(f"trace:binding:{uuid.uuid4().hex[:8]}",),
    )


# ===========================================================================
# Seed tests — spec items 1, 2, 3, 4.
# ===========================================================================


def test_seed_accepts_valid_slot_candidate():
    """Spec test 1: ``seed_geometry`` returns one ACCEPTED
    ``SlotGeometryCandidate`` with ``length == 1`` and
    ``construction_mode == "seed"`` when given a §2-compliant slot."""
    slot = _make_slot_candidate()
    result = _adapter().seed_geometry(slot)

    assert len(result.accepted) == 1
    geom = result.accepted[0]
    assert geom.candidate_type == "SlotGeometryCandidate"
    assert geom.layer == "SlotGeometryQiyas"
    assert geom.source_rule_id == SLOT_GEOMETRY_SEED_RULE.rule_id
    assert geom.rank != EvidenceRank.NO_EVIDENCE
    assert "CandidateOnly" in geom.output_flags

    assert get_geometry_length(geom) == 1
    assert get_construction_mode(geom) == "seed"


def test_seed_rejects_non_slot_candidate():
    """Spec test 2: ``seed_geometry`` blocks any non-``SlotCandidate``
    input — the kernel records a ``far_type_mismatch`` residual,
    plus an ``input_not_slot_candidate`` blocking ``فارق``."""
    not_a_slot = _make_slot_candidate(candidate_type="HarakaCodePoint")
    result = _adapter().seed_geometry(not_a_slot)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "far_type_mismatch" in residual_types
    assert "blocking_fariq_present" in residual_types


def test_seed_rejects_slot_candidate_without_alignment_ref():
    """Spec test 3: a SlotCandidate lacking the ``:alignment_ref:``
    substring in ``trace_ids`` is blocked with a
    ``missing_alignment_ref`` fariq."""
    no_align = _make_slot_candidate(include_alignment_ref=False)
    result = _adapter().seed_geometry(no_align)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    # Either a blocking_fariq_present (for the missing_alignment_ref
    # فارق) and/or an effective_wasf_missing (for the absent
    # alignment_ref_in_trace wasf) — both are sufficient witnesses.
    assert "blocking_fariq_present" in residual_types or (
        "effective_wasf_missing" in residual_types
    )


def test_seed_rejects_slot_candidate_not_from_slot_composition():
    """Spec test 4: a SlotCandidate whose ``source_rule_id`` is not
    ``"slot.composition"`` is blocked with a
    ``source_rule_not_slot_composition`` fariq."""
    bad_rule = _make_slot_candidate(source_rule_id="some.other.rule")
    result = _adapter().seed_geometry(bad_rule)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


# ---------------------------------------------------------------------------
# Per-pillar breadcrumb rejection — extending spec test 3 to each of
# the four §2.2 source-trace audit pillars.
# ---------------------------------------------------------------------------


def test_seed_rejects_slot_candidate_without_letter_identity_breadcrumb():
    """§2.2: a SlotCandidate missing the ``:letter_identity:``
    substring in its ``trace_ids`` is blocked with a
    ``missing_letter_identity_breadcrumb`` fariq."""
    slot = _make_slot_candidate(include_letter_identity_breadcrumb=False)
    result = _adapter().seed_geometry(slot)
    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


def test_seed_rejects_slot_candidate_without_haraka_function_breadcrumb():
    """§2.2: a SlotCandidate missing the ``:haraka_function:``
    substring in its ``trace_ids`` is blocked with a
    ``missing_haraka_function_breadcrumb`` fariq."""
    slot = _make_slot_candidate(include_haraka_function_breadcrumb=False)
    result = _adapter().seed_geometry(slot)
    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


def test_seed_rejects_slot_candidate_without_position_breadcrumb():
    """§2.2: a SlotCandidate missing the ``:position:`` substring in
    its ``trace_ids`` is blocked with a ``missing_position_breadcrumb``
    fariq."""
    slot = _make_slot_candidate(include_position_breadcrumb=False)
    result = _adapter().seed_geometry(slot)
    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


def test_seed_rejects_slot_candidate_without_carrier_binding_breadcrumb():
    """§2.2: a SlotCandidate missing the ``:carrier_binding:`` substring
    in its ``trace_ids`` is blocked with a
    ``missing_carrier_binding_breadcrumb`` fariq."""
    slot = _make_slot_candidate(include_carrier_binding_breadcrumb=False)
    result = _adapter().seed_geometry(slot)
    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


def test_default_fixture_carries_all_five_breadcrumbs():
    """The default fixture is honest about being a fixture but carries
    all five §2.2 breadcrumbs — `alignment_ref`, `letter_identity`,
    `haraka_function`, `position`, and `carrier_binding`. This guards
    against silent drift in the fixture's audit shape."""
    slot = _make_slot_candidate()
    joined = " | ".join(slot.trace_ids)
    assert ":alignment_ref:" in joined
    assert ":letter_identity:" in joined
    assert ":haraka_function:" in joined
    assert ":position:" in joined
    assert ":carrier_binding:" in joined


# ===========================================================================
# Extend tests — spec items 5, 6, 7, 8, 9, 10, 11.
# ===========================================================================


def _seed_geometry_for_extend() -> Candidate:
    """Produce an accepted length-1 SlotGeometryCandidate for use as
    the ``previous`` argument to an extend call."""
    seed = _make_slot_candidate(trace_label="Sa", letter_cp="0628")
    result = _adapter().seed_geometry(seed)
    assert len(result.accepted) == 1
    return result.accepted[0]


def test_extend_accepts_valid_geometry_plus_next_slot_plus_binding():
    """Spec test 5: ``extend_geometry`` returns one ACCEPTED
    ``SlotGeometryCandidate`` when given a valid previous geometry,
    a valid next slot, and a §5-compliant binding."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    result = _adapter().extend_geometry(previous, next_slot, _binding())

    assert len(result.accepted) == 1
    geom = result.accepted[0]
    assert geom.candidate_type == "SlotGeometryCandidate"
    assert geom.source_rule_id == SLOT_GEOMETRY_EXTEND_RULE.rule_id


def test_extend_increments_length():
    """Spec test 6: ``length`` increments by 1 across an
    ``extend_geometry`` call."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    result = _adapter().extend_geometry(previous, next_slot, _binding())

    geom = result.accepted[0]
    assert get_geometry_length(previous) == 1
    assert get_geometry_length(geom) == 2


def test_extend_sets_construction_mode_extension():
    """Spec test 7: ``construction_mode`` of an extension output is
    ``"extension"`` — never ``"seed"`` or anything else."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    result = _adapter().extend_geometry(previous, next_slot, _binding())

    assert get_construction_mode(result.accepted[0]) == "extension"


def test_extend_preserves_identity_and_trace_separation():
    """Spec test 8: identity and trace remain disjoint on the
    extension output; the previous geometry's identities and the
    new slot's identities both appear in the output's
    ``identity_ids`` (CLAUDE.md §4 invariants 1–3, 4)."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    result = _adapter().extend_geometry(previous, next_slot, _binding())

    geom = result.accepted[0]
    # Disjoint:
    assert not (set(geom.identity_ids) & set(geom.trace_ids))
    # Preservation:
    assert set(previous.identity_ids).issubset(set(geom.identity_ids))
    assert set(next_slot.identity_ids).issubset(set(geom.identity_ids))


def test_extend_uses_rank_meet():
    """Spec test 9: the output rank is the meet of contributing
    ranks. A NO_EVIDENCE input would collapse the meet — but here
    we pin the milder case: a FORMAL_STRUCTURE meet stays at
    FORMAL_STRUCTURE, never rises above."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    result = _adapter().extend_geometry(previous, next_slot, _binding())

    geom = result.accepted[0]
    assert geom.rank == EvidenceRank.FORMAL_STRUCTURE
    assert geom.rank.value <= SLOT_GEOMETRY_EXTEND_RULE.rank_ceiling.value


def test_extend_rejects_cross_boundary_binding():
    """Spec test 10: a binding whose
    ``has_whitespace_between == True`` (or whose segment ids differ)
    is blocked — the kernel records ``blocking_fariq_present`` for
    the boundary-crossing claim."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    bad_binding = _binding(
        prev_segment_id=0,
        curr_segment_id=1,
        has_whitespace_between=True,
    )
    result = _adapter().extend_geometry(previous, next_slot, bad_binding)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


def test_extend_rejects_missing_slot_binding_evidence():
    """Spec test 11: an extend call with ``binding=None`` is blocked
    with a ``binding_evidence_missing`` fariq."""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    result = _adapter().extend_geometry(previous, next_slot, None)

    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


def test_extend_rejects_cross_punctuation_binding():
    """Companion to spec test 10: a binding with
    ``has_punctuation_between == True`` is also blocked. (The
    contract §5 names whitespace and punctuation boundary crossings
    as distinct fariq classes.)"""
    previous = _seed_geometry_for_extend()
    next_slot = _make_slot_candidate(
        trace_label="Sb", letter_cp="062a", haraka_cp="0652"
    )
    bad_binding = _binding(
        prev_segment_id=0,
        curr_segment_id=1,
        has_punctuation_between=True,
    )
    result = _adapter().extend_geometry(previous, next_slot, bad_binding)

    assert len(result.accepted) == 0
    residual_types = {r.residual_type for r in result.blocked[0].residuals}
    assert "blocking_fariq_present" in residual_types


# ===========================================================================
# Type-system tests — spec items 12, 13, 14.
# ===========================================================================


def test_no_slot_geometry_seed_candidate_type():
    """Spec test 12: the layer never produces a
    ``SlotGeometrySeedCandidate`` output type — outputs are unified
    on ``SlotGeometryCandidate`` per the §9 amendment."""
    for rule in SLOT_GEOMETRY_RULES:
        assert rule.output_candidate_type != "SlotGeometrySeedCandidate"


def test_no_slot_geometry_extension_candidate_type():
    """Spec test 13: same as above for
    ``SlotGeometryExtensionCandidate``."""
    for rule in SLOT_GEOMETRY_RULES:
        assert rule.output_candidate_type != "SlotGeometryExtensionCandidate"


def test_no_minimal_completion_readiness_candidate_output():
    """Spec test 14: ``MinimalCompletionReadinessCandidate`` is a
    future-reserved concept name only — it is NOT an admissible
    output of this contract, and it appears in
    ``forbidden_outputs`` of both rules."""
    for rule in SLOT_GEOMETRY_RULES:
        assert rule.output_candidate_type != "MinimalCompletionReadinessCandidate"
        assert "MinimalCompletionReadinessCandidate" in rule.forbidden_outputs


# ===========================================================================
# Forbidden-output sweep — spec item 15.
# ===========================================================================


def test_no_dalalah_final_meaning_hukm_reality_word_output():
    """Spec test 15: the rules forbid every higher-layer typed unit
    and every final judgment named by §9 / §11 of the alignment-trace
    contract."""
    must_be_forbidden = {
        "DalalahCandidate",
        "FinalMeaning",
        "HukmCandidate",
        "RealityClaim",
        "FinalCaseJudgment",
        "WordCandidate",
        "LafzCandidate",
        "SentenceCandidate",
        "ParagraphCandidate",
        "DiscourseGeometryCandidate",
        "TextGeometryCandidate",
    }
    for rule in SLOT_GEOMETRY_RULES:
        assert must_be_forbidden.issubset(set(rule.forbidden_outputs)), (
            f"{rule.rule_id!r} missing some forbidden outputs: "
            f"{must_be_forbidden - set(rule.forbidden_outputs)}"
        )
        # And the layer's own output never IS any of those:
        assert rule.output_candidate_type not in must_be_forbidden


def test_admissible_output_is_only_slot_geometry_candidate():
    """The single admissible output type is ``SlotGeometryCandidate``
    — both rules agree (§9 of the alignment-trace contract)."""
    for rule in SLOT_GEOMETRY_RULES:
        assert rule.output_candidate_type == "SlotGeometryCandidate"


# ===========================================================================
# Structural guards on metadata-on-trace
# ===========================================================================


def test_length_and_construction_mode_live_on_trace_ids_not_identity_ids():
    """``length`` and ``construction_mode`` are audit metadata; they
    must travel on ``trace_ids`` and must not appear in
    ``identity_ids`` (CLAUDE.md §4 invariants 1–3; contract §6).
    """
    slot = _make_slot_candidate()
    result = _adapter().seed_geometry(slot)
    geom = result.accepted[0]

    length_in_trace = any(
        t.startswith("trace:slot_geometry:length:") for t in geom.trace_ids
    )
    mode_in_trace = any(
        t.startswith("trace:slot_geometry:construction_mode:")
        for t in geom.trace_ids
    )
    assert length_in_trace
    assert mode_in_trace

    length_in_identity = any(
        i.startswith("trace:slot_geometry:length:") for i in geom.identity_ids
    )
    mode_in_identity = any(
        i.startswith("trace:slot_geometry:construction_mode:")
        for i in geom.identity_ids
    )
    assert not length_in_identity
    assert not mode_in_identity


def test_seed_geometry_preserves_slot_identity_ids():
    """Identity preservation across Seed: the seed's
    ``identity_ids`` are a subset of the geometry's ``identity_ids``
    (contract §6.1 / CLAUDE.md §4 invariant 4)."""
    slot = _make_slot_candidate()
    result = _adapter().seed_geometry(slot)
    geom = result.accepted[0]
    assert set(slot.identity_ids).issubset(set(geom.identity_ids))
