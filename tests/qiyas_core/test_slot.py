"""
Tests for SlotCandidate layer — Gap #6 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Required tests (from contract):
  test_slot_requires_letter_identity
  test_slot_requires_haraka_function
  test_slot_requires_position
  test_slot_compatible_baa_fatha
  test_slot_preserves_identity
  test_slot_forbids_syllable_before_adjacency
"""

import uuid

from qiyas_core.candidate import Candidate
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.evidence import Evidence, EvidenceSet
from qiyas_core.kernel import QiyasContext, QiyasKernel, QiyasRequest
from qiyas_core.node import QiyasNodeRef
from qiyas_core.rules.slot_rules import SLOT_COMPOSITION_RULE
from qiyas_core.slot_adapter import SlotLayerAdapter


def _kernel() -> QiyasKernel:
    return QiyasKernel()


def _adapter() -> SlotLayerAdapter:
    return SlotLayerAdapter(kernel=_kernel())


def _make_carrier(
    candidate_type: str,
    layer: str,
    source_rule_id: str,
    identity_ids: tuple[str, ...],
    label: str = "test",
) -> Candidate:
    """Build a minimal carrier Candidate for slot composition tests."""
    return Candidate(
        candidate_id=f"{label}:{uuid.uuid4().hex[:8]}",
        candidate_type=candidate_type,
        status=CandidateStatus.ACCEPTED,
        layer=layer,
        source_rule_id=source_rule_id,
        asl_id=f"اصل:{layer}",
        far_id=f"فرع:{label}",
        identity_ids=identity_ids,
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        trace_ids=(f"trace:{label}",),
        output_flags=frozenset(),
    )


def _baa_letter_carrier() -> Candidate:
    return _make_carrier(
        "LetterIdentityCarrier",
        "LetterIdentityQiyas",
        "letter_identity.baa",
        ("identity:codepoint:0628", "identity:letter_identity_domain"),
        "baa_carrier",
    )


def _fatha_haraka_carrier() -> Candidate:
    return _make_carrier(
        "HarakaFunctionCarrier",
        "HarakaFunctionQiyas",
        "haraka_function.fatha",
        ("identity:codepoint:064e", "identity:haraka_function_domain"),
        "fatha_carrier",
    )


def _initial_position_carrier() -> Candidate:
    return _make_carrier(
        "PositionCarrier",
        "PositionQiyas",
        "position.initial",
        ("identity:codepoint:0628:pos0", "identity:position_domain"),
        "initial_position",
    )


def _alignment_for(
    letter_carrier: Candidate,
    haraka_carrier: Candidate,
    candidate_type: str = "CarrierBindingCandidate",
    status: CandidateStatus = CandidateStatus.ACCEPTED,
    rank: EvidenceRank = EvidenceRank.FORMAL_STRUCTURE,
) -> Candidate:
    """
    Build an upstream alignment proof (CarrierBindingCandidate) that
    witnesses the binding of the given letter+haraka pair. Its
    identity_ids must cover both carriers' identity:codepoint:* entries
    so SlotLayerAdapter accepts it as valid.
    """
    letter_cps = tuple(
        i for i in letter_carrier.identity_ids
        if i.startswith("identity:codepoint:")
    )
    haraka_cps = tuple(
        i for i in haraka_carrier.identity_ids
        if i.startswith("identity:codepoint:")
    )
    return Candidate(
        candidate_id=f"alignment:{uuid.uuid4().hex[:8]}",
        candidate_type=candidate_type,
        status=status,
        layer="ConditionedTypedSequenceQiyas",
        source_rule_id="conditioned_typed_sequence.carrier_binding",
        asl_id="اصل:conditioned_typed_sequence_domain",
        far_id="فرع:carrier_binding_proof",
        identity_ids=letter_cps + haraka_cps,
        rank=rank,
        residuals=(),
        trace_ids=("trace:alignment",),
        output_flags=frozenset(),
    )


# ---------------------------------------------------------------------------
# Contract-required tests
# ---------------------------------------------------------------------------

def test_slot_compatible_baa_fatha():
    """Contract test: BAA + FATHA + INITIAL + alignment → SlotCandidate accepted."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    position = _initial_position_carrier()
    alignment = _alignment_for(letter, haraka)

    result = _adapter().compose_slot(letter, haraka, position, alignment_evidence=alignment)

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "SlotCandidate"
    assert c.rank == EvidenceRank.FORMAL_STRUCTURE
    assert c.layer == "SlotQiyas"


def test_slot_preserves_identity():
    """Contract test: SlotCandidate output must preserve all input identity_ids."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    position = _initial_position_carrier()
    alignment = _alignment_for(letter, haraka)

    result = _adapter().compose_slot(letter, haraka, position, alignment_evidence=alignment)
    c = result.accepted[0]

    all_input_ids = (
        set(letter.identity_ids)
        | set(haraka.identity_ids)
        | set(position.identity_ids)
    )
    output_ids = set(c.identity_ids)
    assert all_input_ids.issubset(output_ids), (
        f"Missing identities: {all_input_ids - output_ids}"
    )


def test_slot_forbids_syllable_before_adjacency():
    """
    Contract test: SlotCandidate layer forbids SyllableCandidate.
    Verified by forbidden_outputs on SLOT_COMPOSITION_RULE.
    """
    assert "SyllableCandidate" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_requires_letter_identity():
    """
    Contract test: Without letter identity wasf, slot composition is blocked.
    """
    kernel = _kernel()

    asl = QiyasNodeRef(
        node_id="اصل:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )
    far = QiyasNodeRef(
        node_id="فرع:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    # Missing: wasf:has_letter_identity_carrier:evidenced
    proves = (
        "اصل:established",
        "فرع:determined",
        # has_haraka and position present but NOT letter_identity
        "وصف:has_haraka_function_carrier:evidenced",
        "وصف:has_position_carrier:evidenced",
        "وصف:compatible_letter_haraka:evidenced",
        "وصف:compatible_letter_position:evidenced",
        "وصف:has_alignment_evidence:evidenced",
        "وصف:identity_preserved:evidenced",
        "علة:belongs_to_slot_composition_domain:verified",
        "علة:slot_composition_licensed:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_no_letter:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=SLOT_COMPOSITION_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="SlotQiyas"),
    )

    result = kernel.apply(request)
    assert len(result.blocked) == 1
    assert any(r.residual_type == "effective_wasf_missing" for r in result.residuals)


def test_slot_requires_haraka_function():
    """
    Contract test: Without haraka function wasf, slot composition is blocked.
    """
    kernel = _kernel()

    asl = QiyasNodeRef(
        node_id="اصل:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )
    far = QiyasNodeRef(
        node_id="فرع:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    # Missing: wasf:has_haraka_function_carrier:evidenced
    proves = (
        "اصل:established",
        "فرع:determined",
        "وصف:has_letter_identity_carrier:evidenced",
        # has_haraka missing
        "وصف:has_position_carrier:evidenced",
        "وصف:compatible_letter_haraka:evidenced",
        "وصف:compatible_letter_position:evidenced",
        "وصف:has_alignment_evidence:evidenced",
        "وصف:identity_preserved:evidenced",
        "علة:belongs_to_slot_composition_domain:verified",
        "علة:slot_composition_licensed:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_no_haraka:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=SLOT_COMPOSITION_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="SlotQiyas"),
    )

    result = kernel.apply(request)
    assert len(result.blocked) == 1
    assert any(r.residual_type == "effective_wasf_missing" for r in result.residuals)


def test_slot_requires_position():
    """
    Contract test: Without position carrier wasf, slot composition is blocked.
    """
    kernel = _kernel()

    asl = QiyasNodeRef(
        node_id="اصل:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )
    far = QiyasNodeRef(
        node_id="فرع:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    # Missing: wasf:has_position_carrier:evidenced
    proves = (
        "اصل:established",
        "فرع:determined",
        "وصف:has_letter_identity_carrier:evidenced",
        "وصف:has_haraka_function_carrier:evidenced",
        # position missing
        "وصف:compatible_letter_haraka:evidenced",
        "وصف:compatible_letter_position:evidenced",
        "وصف:has_alignment_evidence:evidenced",
        "وصف:identity_preserved:evidenced",
        "علة:belongs_to_slot_composition_domain:verified",
        "علة:slot_composition_licensed:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_no_position:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=SLOT_COMPOSITION_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="SlotQiyas"),
    )

    result = kernel.apply(request)
    assert len(result.blocked) == 1
    assert any(r.residual_type == "effective_wasf_missing" for r in result.residuals)


# ---------------------------------------------------------------------------
# Additional tests
# ---------------------------------------------------------------------------

def test_slot_output_type():
    """SlotCandidate output_candidate_type must be 'SlotCandidate'."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    result = _adapter().compose_slot(
        letter,
        haraka,
        _initial_position_carrier(),
        alignment_evidence=_alignment_for(letter, haraka),
    )
    assert result.accepted[0].candidate_type == "SlotCandidate"


def test_slot_trace_not_in_identity():
    """trace_ids and identity_ids must be disjoint in SlotCandidate."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    result = _adapter().compose_slot(
        letter,
        haraka,
        _initial_position_carrier(),
        alignment_evidence=_alignment_for(letter, haraka),
    )
    c = result.accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_slot_output_flags():
    """SlotCandidate must have CandidateOnly flag."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    result = _adapter().compose_slot(
        letter,
        haraka,
        _initial_position_carrier(),
        alignment_evidence=_alignment_for(letter, haraka),
    )
    assert "CandidateOnly" in result.accepted[0].output_flags


def test_slot_carrier_mismatch_blocks():
    """haraka_carrier_mismatch fariq must block slot composition."""
    kernel = _kernel()

    asl = QiyasNodeRef(
        node_id="اصل:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )
    far = QiyasNodeRef(
        node_id="فرع:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    proves = (
        "اصل:established",
        "فرع:determined",
        "وصف:has_letter_identity_carrier:evidenced",
        "وصف:has_haraka_function_carrier:evidenced",
        "وصف:has_position_carrier:evidenced",
        "وصف:compatible_letter_haraka:evidenced",
        "وصف:compatible_letter_position:evidenced",
        "وصف:has_alignment_evidence:evidenced",
        "وصف:identity_preserved:evidenced",
        "علة:belongs_to_slot_composition_domain:verified",
        "علة:slot_composition_licensed:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
        # Invalidating difference
        "فارق:haraka_carrier_mismatch:present",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_mismatch:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=SLOT_COMPOSITION_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="SlotQiyas"),
    )

    result = kernel.apply(request)
    assert len(result.blocked) == 1
    assert any(r.residual_type == "blocking_fariq_present" for r in result.residuals)


def test_slot_forbids_meaning():
    """SlotCandidate layer must forbid MeaningCandidate."""
    assert "MeaningCandidate" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_forbids_hukm():
    """SlotCandidate layer must forbid HukmCandidate."""
    assert "HukmCandidate" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_layer_name():
    """SLOT_COMPOSITION_RULE must be in SlotQiyas layer."""
    assert SLOT_COMPOSITION_RULE.layer == "SlotQiyas"


# ---------------------------------------------------------------------------
# PR #26 — SlotCandidate must consume explicit alignment evidence.
#
# Seventeen mandated tests from the maintainer's brief.
# ---------------------------------------------------------------------------


def _wasf_missing_in_residuals(result, wasf_name: str) -> bool:
    """True if any residual message mentions the named missing wasf.

    The kernel emits residual messages of the form
    ``الوصف المؤثر غير مثبت: <wasf>`` for effective_wasf_missing.
    """
    return any(
        r.residual_type == "effective_wasf_missing" and wasf_name in r.message
        for r in result.residuals
    )


# §15 #1 — SlotCandidate is NOT produced without alignment evidence.

def test_slot_not_produced_without_alignment_evidence():
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
        alignment_evidence=None,
    )
    assert len(result.accepted) == 0
    assert len(result.blocked) == 1
    assert result.blocked[0].candidate_type == "SlotCandidate"
    # The candidate's status is BLOCKED (not produced as an accepted
    # SlotCandidate) — the algebraic obligation §8 is enforced by the
    # kernel via the missing has_alignment_evidence wasf.
    assert _wasf_missing_in_residuals(result, "has_alignment_evidence")


# §15 #2 — Joining all four pillars produces a SlotCandidate.

def test_slot_produced_from_all_four_pillars():
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    position = _initial_position_carrier()
    alignment = _alignment_for(letter, haraka)

    result = _adapter().compose_slot(
        letter, haraka, position, alignment_evidence=alignment
    )
    assert len(result.accepted) == 1
    assert result.accepted[0].candidate_type == "SlotCandidate"


# §15 #3, #4, #5 — Missing Letter / Haraka / Position blocks or defers.
#
# These are already covered by the pre-PR-26 contract tests
#   test_slot_requires_letter_identity
#   test_slot_requires_haraka_function
#   test_slot_requires_position
# (above). Those tests construct the QiyasRequest directly with one of
# the three carrier wasfs missing and verify the kernel blocks with an
# effective_wasf_missing residual. After PR #26 they still hold because
# the new has_alignment_evidence wasf is explicitly added to their
# proves tuples, so the only missing wasf in each test is the one the
# test is meant to isolate. No new test is added here — the existing
# tests already cover §15 #3, #4, #5 verbatim.


# §15 #6 — Missing AlignmentEvidence blocks or defers.

def test_slot_missing_alignment_blocks():
    """Already covered by #1, but here we explicitly check that the
    compatibility wasfs are flagged missing when alignment is absent."""
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
        alignment_evidence=None,
    )
    assert len(result.blocked) == 1
    # All three alignment-derived wasfs must be reported missing.
    assert _wasf_missing_in_residuals(result, "has_alignment_evidence")
    assert _wasf_missing_in_residuals(result, "compatible_letter_haraka")
    assert _wasf_missing_in_residuals(result, "compatible_letter_position")


# §15 #7 — Adapter no longer self-asserts compatible_letter_haraka.

def test_adapter_does_not_self_assert_compatible_letter_haraka():
    """When no alignment is supplied, the adapter must NOT emit
    `وصف:compatible_letter_haraka:evidenced` in the evidence set."""
    request = _adapter().build_request(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
        alignment_evidence=None,
    )
    assert not request.evidence.proves("وصف:compatible_letter_haraka:evidenced")


# §15 #8 — Adapter no longer self-asserts compatible_letter_position.

def test_adapter_does_not_self_assert_compatible_letter_position():
    request = _adapter().build_request(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
        alignment_evidence=None,
    )
    assert not request.evidence.proves("وصف:compatible_letter_position:evidenced")


def test_adapter_does_not_self_assert_has_alignment_evidence():
    """Symmetric guard for the new has_alignment_evidence wasf."""
    request = _adapter().build_request(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
        alignment_evidence=None,
    )
    assert not request.evidence.proves("وصف:has_alignment_evidence:evidenced")


def test_adapter_does_assert_compat_wasfs_when_alignment_present():
    """Symmetric positive case: when valid alignment is supplied, the
    three alignment-derived wasfs MUST appear in the evidence set."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    request = _adapter().build_request(
        letter,
        haraka,
        _initial_position_carrier(),
        alignment_evidence=_alignment_for(letter, haraka),
    )
    assert request.evidence.proves("وصف:has_alignment_evidence:evidenced")
    assert request.evidence.proves("وصف:compatible_letter_haraka:evidenced")
    assert request.evidence.proves("وصف:compatible_letter_position:evidenced")


def test_adapter_rejects_alignment_with_wrong_identity_coverage():
    """An alignment proof whose identity_ids do NOT cover both the
    letter's and the haraka's codepoint identities is treated as no
    alignment at all — the compat wasfs are not asserted."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    other_haraka = _make_carrier(
        "HarakaFunctionCarrier",
        "HarakaFunctionQiyas",
        "haraka_function.damma",
        ("identity:codepoint:064f", "identity:haraka_function_domain"),
        "damma_other",
    )
    # Alignment is for (baa, damma), not for (baa, fatha)
    mismatched_alignment = _alignment_for(letter, other_haraka)
    request = _adapter().build_request(
        letter, haraka, _initial_position_carrier(),
        alignment_evidence=mismatched_alignment,
    )
    assert not request.evidence.proves("وصف:has_alignment_evidence:evidenced")


def test_adapter_rejects_alignment_with_blocked_status():
    """A blocked CarrierBindingCandidate cannot serve as alignment."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    blocked_alignment = _alignment_for(
        letter, haraka, status=CandidateStatus.BLOCKED
    )
    request = _adapter().build_request(
        letter, haraka, _initial_position_carrier(),
        alignment_evidence=blocked_alignment,
    )
    assert not request.evidence.proves("وصف:has_alignment_evidence:evidenced")


# §15 #9 — Identity is preserved.

def test_slot_alignment_path_preserves_identity():
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    position = _initial_position_carrier()
    result = _adapter().compose_slot(
        letter, haraka, position,
        alignment_evidence=_alignment_for(letter, haraka),
    )
    c = result.accepted[0]
    output_ids = set(c.identity_ids)
    all_input_ids = (
        set(letter.identity_ids)
        | set(haraka.identity_ids)
        | set(position.identity_ids)
    )
    assert all_input_ids.issubset(output_ids)


# §15 #10 — Trace is separated from identity.

def test_slot_alignment_path_identity_trace_disjoint():
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    result = _adapter().compose_slot(
        letter, haraka, _initial_position_carrier(),
        alignment_evidence=_alignment_for(letter, haraka),
    )
    c = result.accepted[0]
    assert set(c.identity_ids).isdisjoint(set(c.trace_ids))


# §15 #11 — Residuals are preserved.

def test_slot_residuals_preserved_when_blocked():
    """When the slot is blocked, the residuals must be present on the
    blocked candidate (CLAUDE.md §4 invariant 7 — residuals must not
    be hidden or silently discarded)."""
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
        alignment_evidence=None,
    )
    c = result.blocked[0]
    assert len(c.residuals) > 0
    # The result-level residuals must mirror the candidate's residuals.
    assert len(result.residuals) > 0


# §15 #12 — Rank is computed by meet semantics.

def test_slot_rank_is_meet_of_inputs_and_ceiling():
    """The accepted SlotCandidate rank is the meet of all inputs.

    SLOT_COMPOSITION_RULE has rank_ceiling = FORMAL_STRUCTURE, so even
    when every carrier comes in higher, the output cannot exceed it.
    """
    letter = _baa_letter_carrier()           # FORMAL_STRUCTURE
    haraka = _fatha_haraka_carrier()         # FORMAL_STRUCTURE
    position = _initial_position_carrier()   # FORMAL_STRUCTURE
    result = _adapter().compose_slot(
        letter, haraka, position,
        alignment_evidence=_alignment_for(letter, haraka),
    )
    assert result.accepted[0].rank == EvidenceRank.FORMAL_STRUCTURE


def test_slot_rank_ceiling_caps_the_meet():
    assert SLOT_COMPOSITION_RULE.rank_ceiling == EvidenceRank.FORMAL_STRUCTURE


# §15 #13 — Output remains CandidateOnly.

def test_slot_output_flag_is_candidate_only():
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    result = _adapter().compose_slot(
        letter, haraka, _initial_position_carrier(),
        alignment_evidence=_alignment_for(letter, haraka),
    )
    c = result.accepted[0]
    assert "CandidateOnly" in c.output_flags
    for forbidden in ("HukmCandidate", "RealityClaim", "FinalMeaning", "FinalCaseJudgment"):
        assert forbidden not in c.output_flags


# §15 #14–#17 — SlotCandidate layer forbids SlotGeometry, FinalMeaning,
# HukmCandidate, and RealityClaim by rule declaration.

def test_slot_rule_forbids_slot_geometry():
    # Structural witness retained for clarity: the rule's
    # output_candidate_type is "SlotCandidate", not "SlotGeometry".
    assert SLOT_COMPOSITION_RULE.output_candidate_type == "SlotCandidate"
    assert SLOT_COMPOSITION_RULE.output_candidate_type != "SlotGeometry"


def test_slot_rule_explicitly_forbids_slot_geometry():
    """PR #28 — SlotGeometry is now declared explicitly in
    forbidden_outputs, not merely implied by output_candidate_type.
    This closes the constitutional jump SlotCandidate* → SlotGeometry
    at the forbidden-outputs layer."""
    assert "SlotGeometry" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_rule_forbids_final_meaning():
    assert "FinalMeaning" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_rule_forbids_hukm_candidate():
    assert "HukmCandidate" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_rule_forbids_reality_claim():
    assert "RealityClaim" in SLOT_COMPOSITION_RULE.forbidden_outputs


def test_slot_rule_declares_constitutional_triple():
    """All three of the constitutional final-output bans must appear
    in this layer's forbidden_outputs."""
    triple = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    assert triple.issubset(set(SLOT_COMPOSITION_RULE.forbidden_outputs))
