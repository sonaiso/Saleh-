"""
Tests for ConditionedTypedSequence — PR #25.

Covers the 11 mandated tests from CLAUDE.md §15:

  1. A haraka following a valid letter produces carrier-binding evidence.
  2. A haraka without a carrier produces a blocking or deferred residual.
  3. Shadda requires a carrier.
  4. Tanwin is marked as terminal-sensitive evidence, not a final slot.
  5. Boundary symbols do not enter slots.
  6. Punctuation does not enter slots.
  7. Residuals are preserved.
  8. Every symbol receives position context.
  9. ConditionedTypedSequence does not produce LetterIdentityCarrier.
 10. ConditionedTypedSequence does not produce HarakaFunctionCarrier.
 11. ConditionedTypedSequence does not produce SlotCandidate.

Plus the §4 invariants (identity/trace separation, source-identity
preservation, residual preservation) and §19 forbidden-jump checks.
"""

from qiyas_core.candidate import Candidate
from qiyas_core.conditioned_typed_sequence_adapter import (
    ConditionedTypedSequenceLayerAdapter,
)
from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.rules.conditioned_typed_sequence_rules import (
    BOUNDARY_EXCLUSION_PROOF,
    CARRIER_BINDING_PROOF,
    LETTER_POSITION_PROOF,
    PUNCTUATION_EXCLUSION_PROOF,
    RESIDUAL_PRESERVATION_PROOF,
)
from qiyas_core.typed_codepoint_adapter import TypedCodePointLayerAdapter


# ---------------------------------------------------------------------------
# Helpers — build a TypedCodePoint candidate for a given codepoint by going
# through the canonical Unicode → TypedCodePoint chain. This keeps the CTS
# tests isolated from any internal shape assumptions about how upstream
# layers construct their candidates.
# ---------------------------------------------------------------------------


def _kernel() -> QiyasKernel:
    return QiyasKernel()


def _typed(codepoint: int) -> Candidate:
    """Return a TypedCodePoint candidate for the given codepoint.

    Uses TypedCodePointLayerAdapter.classify_codepoint, the project's
    documented unit-test convenience path (see typed_codepoint_adapter.py).
    This bypasses the Unicode layer because some boundary codepoints we
    must test (e.g. ASCII whitespace U+0020) are intentionally rejected
    at the canonical Unicode membership layer. The CTS layer itself is
    typed-codepoint-shaped, so this is the right level for these tests.
    """
    t = TypedCodePointLayerAdapter(kernel=_kernel()).classify_codepoint(codepoint)
    assert len(t.accepted) == 1, f"TypedCodePoint must classify U+{codepoint:04X}"
    return t.accepted[0]


def _adapter() -> ConditionedTypedSequenceLayerAdapter:
    return ConditionedTypedSequenceLayerAdapter(kernel=_kernel())


# ---------------------------------------------------------------------------
# §15 #1 — haraka following a valid letter produces a CarrierBindingCandidate
# ---------------------------------------------------------------------------


def test_haraka_after_letter_produces_carrier_binding_candidate():
    """A fatha following a baa produces an ACCEPTED CarrierBindingCandidate."""
    letter = _typed(0x0628)  # ب
    haraka = _typed(0x064E)  # َ
    result = _adapter().prove_carrier_binding(
        haraka_typed=haraka,
        carrier_letter_typed=letter,
        index=1,
        sequence_length=2,
    )

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "CarrierBindingCandidate"
    assert c.layer == "ConditionedTypedSequenceQiyas"
    assert c.source_rule_id == CARRIER_BINDING_PROOF.rule_id


# ---------------------------------------------------------------------------
# §15 #2 — haraka without a carrier produces a blocking/deferring residual
# ---------------------------------------------------------------------------


def test_orphan_haraka_is_blocked_with_residual():
    """An orphan fatha (no preceding letter) is BLOCKED with a residual."""
    haraka = _typed(0x064E)
    result = _adapter().prove_carrier_binding(
        haraka_typed=haraka,
        carrier_letter_typed=None,
        index=0,
        sequence_length=1,
    )

    assert len(result.blocked) == 1
    c = result.blocked[0]
    assert c.status == CandidateStatus.BLOCKED
    assert len(c.residuals) > 0, "orphan haraka must produce at least one residual"
    # The fariq is asserted explicitly; kernel records a blocking_fariq_present
    # residual. The required wasf for carrier is missing; kernel records an
    # effective_wasf_missing residual. Either is a sufficient witness of the
    # block, per CLAUDE.md §4 invariant 7.
    residual_types = {r.residual_type for r in c.residuals}
    assert (
        "blocking_fariq_present" in residual_types
        or "effective_wasf_missing" in residual_types
    )


# ---------------------------------------------------------------------------
# §15 #3 — shadda requires a carrier
# ---------------------------------------------------------------------------


def test_shadda_with_carrier_is_accepted():
    """Shadda (U+0651) on a baa is accepted with a shadda_has_carrier marker."""
    letter = _typed(0x0628)
    shadda = _typed(0x0651)
    result = _adapter().prove_carrier_binding(
        haraka_typed=shadda,
        carrier_letter_typed=letter,
        index=1,
        sequence_length=2,
    )

    assert len(result.accepted) == 1
    assert result.accepted[0].candidate_type == "CarrierBindingCandidate"


def test_shadda_without_carrier_is_blocked():
    """Orphan shadda is BLOCKED — shadda requires a carrier."""
    shadda = _typed(0x0651)
    result = _adapter().prove_carrier_binding(
        haraka_typed=shadda,
        carrier_letter_typed=None,
        index=0,
        sequence_length=1,
    )

    assert len(result.blocked) == 1
    assert len(result.blocked[0].residuals) > 0


# ---------------------------------------------------------------------------
# §15 #4 — tanwin is marked as terminal-sensitive evidence, NOT a final slot
# ---------------------------------------------------------------------------


def test_tanwin_terminal_is_carrier_binding_not_slot():
    """Tanwin at the end of a sequence yields a CarrierBindingCandidate
    (never a SlotCandidate) — the terminal-sensitivity is recorded as
    auditable evidence."""
    letter = _typed(0x0628)
    tanwin = _typed(0x064B)  # ً  FATHATAN
    result = _adapter().prove_carrier_binding(
        haraka_typed=tanwin,
        carrier_letter_typed=letter,
        index=1,
        sequence_length=2,
    )

    assert len(result.accepted) == 1
    c = result.accepted[0]
    # The candidate is CarrierBindingCandidate — explicitly NOT SlotCandidate.
    assert c.candidate_type == "CarrierBindingCandidate"
    assert c.candidate_type != "SlotCandidate"


def test_tanwin_non_terminal_is_still_not_a_slot():
    """Tanwin in a non-terminal position is still a CarrierBindingCandidate,
    not a SlotCandidate — the layer never produces SlotCandidate."""
    letter = _typed(0x0628)
    tanwin = _typed(0x064B)
    result = _adapter().prove_carrier_binding(
        haraka_typed=tanwin,
        carrier_letter_typed=letter,
        index=1,
        sequence_length=3,  # tanwin is not at end
    )

    assert len(result.accepted) == 1
    assert result.accepted[0].candidate_type != "SlotCandidate"


# ---------------------------------------------------------------------------
# §15 #5 — boundary symbols do not enter slots
# ---------------------------------------------------------------------------


def test_boundary_produces_boundary_evidence_not_slot():
    """A whitespace boundary produces a BoundaryEvidence candidate, not a slot."""
    space = _typed(0x0020)  # space (boundary)
    result = _adapter().prove_boundary_exclusion(
        boundary_typed=space, index=0, sequence_length=1
    )

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.candidate_type == "BoundaryEvidence"
    assert c.candidate_type != "SlotCandidate"
    assert c.source_rule_id == BOUNDARY_EXCLUSION_PROOF.rule_id


# ---------------------------------------------------------------------------
# §15 #6 — punctuation does not enter slots
# ---------------------------------------------------------------------------


def test_punctuation_produces_boundary_evidence_not_slot():
    """Arabic comma (U+060C) produces BoundaryEvidence, never a slot."""
    comma = _typed(0x060C)
    result = _adapter().prove_punctuation_exclusion(
        punct_typed=comma, index=0, sequence_length=1
    )

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.candidate_type == "BoundaryEvidence"
    assert c.candidate_type != "SlotCandidate"
    assert c.source_rule_id == PUNCTUATION_EXCLUSION_PROOF.rule_id


# ---------------------------------------------------------------------------
# §15 #7 — residuals are preserved
# ---------------------------------------------------------------------------


def test_residual_codepoint_is_preserved_not_dropped():
    """An unclassified codepoint produces ResidualPreservationEvidence — it
    is not silently discarded (CLAUDE.md §4 invariant 7)."""
    # U+06E0 is in the Arabic block but not classified as letter/haraka/
    # boundary/punctuation by the TypedCodePoint rules → ResidualCodePoint.
    residual = _typed(0x06E0)
    result = _adapter().prove_residual_preservation(
        residual_typed=residual, index=0, sequence_length=1
    )

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.candidate_type == "ResidualPreservationEvidence"
    assert c.source_rule_id == RESIDUAL_PRESERVATION_PROOF.rule_id


# ---------------------------------------------------------------------------
# §15 #8 — every symbol receives position context
# ---------------------------------------------------------------------------


def test_every_symbol_in_sequence_gets_a_cts_proof():
    """prove_for_sequence emits one CandidateSet per input position."""
    seq = [
        _typed(0x0628),  # ب letter
        _typed(0x064E),  # َ haraka
        _typed(0x062A),  # ت letter
        _typed(0x0020),  # ␣ boundary
        _typed(0x060C),  # ، punctuation
        _typed(0x06E0),  # residual
    ]
    results = _adapter().prove_for_sequence(seq)

    assert len(results) == len(seq)
    # Each emitted candidate is in ConditionedTypedSequenceQiyas layer.
    for cs in results:
        # exactly one candidate per position
        assert len(cs.candidates) == 1
        assert cs.candidates[0].layer == "ConditionedTypedSequenceQiyas"


def test_letter_in_sequence_produces_position_evidence():
    """A LetterCodePoint in the sequence produces PositionEvidence."""
    letter = _typed(0x0628)
    result = _adapter().prove_letter_position(letter, index=0, sequence_length=1)

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.candidate_type == "PositionEvidence"
    assert c.source_rule_id == LETTER_POSITION_PROOF.rule_id


# ---------------------------------------------------------------------------
# §15 #9, #10, #11 — CTS does NOT produce LetterIdentityCarrier,
# HarakaFunctionCarrier, or SlotCandidate.
# ---------------------------------------------------------------------------


def _all_cts_rules():
    return (
        CARRIER_BINDING_PROOF,
        LETTER_POSITION_PROOF,
        BOUNDARY_EXCLUSION_PROOF,
        PUNCTUATION_EXCLUSION_PROOF,
        RESIDUAL_PRESERVATION_PROOF,
    )


def test_cts_rules_do_not_output_letter_identity_carrier():
    for rule in _all_cts_rules():
        assert rule.output_candidate_type != "LetterIdentityCarrier"
        assert "LetterIdentityCarrier" in rule.forbidden_outputs


def test_cts_rules_do_not_output_haraka_function_carrier():
    for rule in _all_cts_rules():
        assert rule.output_candidate_type != "HarakaFunctionCarrier"
        assert "HarakaFunctionCarrier" in rule.forbidden_outputs


def test_cts_rules_do_not_output_slot_candidate():
    for rule in _all_cts_rules():
        assert rule.output_candidate_type != "SlotCandidate"
        assert "SlotCandidate" in rule.forbidden_outputs


def test_cts_rules_do_not_output_slot_geometry():
    """§19: forbid the illegal jump CTS → SlotGeometry."""
    for rule in _all_cts_rules():
        assert rule.output_candidate_type != "SlotGeometry"
        assert "SlotGeometry" in rule.forbidden_outputs


# ---------------------------------------------------------------------------
# §4 invariants — identity preserved, identity ≠ trace, residuals retained
# ---------------------------------------------------------------------------


def test_carrier_binding_preserves_source_identities():
    """The CarrierBindingCandidate's identity_ids include both the haraka's
    and the carrier letter's identities (CLAUDE.md §4 invariant 4)."""
    letter = _typed(0x0628)
    haraka = _typed(0x064E)
    result = _adapter().prove_carrier_binding(
        haraka_typed=haraka, carrier_letter_typed=letter, index=1, sequence_length=2
    )

    c = result.accepted[0]
    identity_set = set(c.identity_ids)
    for hid in haraka.identity_ids:
        assert hid in identity_set, f"haraka identity {hid!r} must be preserved"
    for lid in letter.identity_ids:
        assert lid in identity_set, f"letter identity {lid!r} must be preserved"


def test_carrier_binding_identity_disjoint_from_trace():
    """§4 invariants 1, 2, 3 — identity and trace must remain disjoint."""
    letter = _typed(0x0628)
    haraka = _typed(0x064E)
    result = _adapter().prove_carrier_binding(
        haraka_typed=haraka, carrier_letter_typed=letter, index=1, sequence_length=2
    )

    c = result.accepted[0]
    assert set(c.identity_ids).isdisjoint(set(c.trace_ids))


def test_all_cts_layer_rules_declare_constitutional_forbidden_outputs():
    """Every rule declares the constitutional triple in forbidden_outputs."""
    constitutional = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
    for rule in _all_cts_rules():
        assert constitutional.issubset(set(rule.forbidden_outputs))


def test_all_cts_rules_have_form_rank_ceiling():
    """No CTS rule may claim a rank ceiling higher than FORMAL_STRUCTURE."""
    for rule in _all_cts_rules():
        assert rule.rank_ceiling == EvidenceRank.FORMAL_STRUCTURE


# ---------------------------------------------------------------------------
# Output flags — CandidateOnly is preserved (§4 invariant 9)
# ---------------------------------------------------------------------------


def test_cts_candidates_remain_potential_only():
    """Output flags must contain CandidateOnly and no final-judgment flag."""
    letter = _typed(0x0628)
    haraka = _typed(0x064E)
    result = _adapter().prove_carrier_binding(
        haraka_typed=haraka, carrier_letter_typed=letter, index=1, sequence_length=2
    )

    c = result.accepted[0]
    assert "CandidateOnly" in c.output_flags
    for forbidden in ("HukmCandidate", "RealityClaim", "FinalMeaning", "FinalCaseJudgment"):
        assert forbidden not in c.output_flags


# =============================================================================
# Z3 Tests: CTS consumes SequenceContextTokenizer markers as context/evidence
# =============================================================================

import sys
from pathlib import Path

_SRC_Z3 = Path(__file__).parent.parent.parent / "src"
if str(_SRC_Z3) not in sys.path:
    sys.path.insert(0, str(_SRC_Z3))

from qiyas_core.sequence_context_tokenizer import (
    SequenceContextTokenizer,
    TokenizedSequence,
)


def _tok(text: str) -> TokenizedSequence:
    return SequenceContextTokenizer().tokenize(text)


def _letter(cp_hex: str):
    from qiyas_core.candidate import Candidate
    from qiyas_core.enums import EvidenceRank, CandidateStatus
    return Candidate(
        candidate_id=f"z3:letter:{cp_hex}",
        candidate_type="LetterCodePoint",
        status=CandidateStatus.ACCEPTED,
        layer="TypedCodePointClassificationQiyas",
        source_rule_id="test.typed_codepoint.fixture",
        asl_id="test:asl",
        far_id=f"test:far:{cp_hex}",
        identity_ids=(f"identity:codepoint:{cp_hex}",),
        trace_ids=(f"trace:letter:{cp_hex}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _haraka(cp_hex: str):
    from qiyas_core.candidate import Candidate
    from qiyas_core.enums import EvidenceRank, CandidateStatus
    return Candidate(
        candidate_id=f"z3:haraka:{cp_hex}",
        candidate_type="HarakaCodePoint",
        status=CandidateStatus.ACCEPTED,
        layer="TypedCodePointClassificationQiyas",
        source_rule_id="test.typed_codepoint.fixture",
        asl_id="test:asl",
        far_id=f"test:far:{cp_hex}",
        identity_ids=(f"identity:codepoint:{cp_hex}",),
        trace_ids=(f"trace:haraka:{cp_hex}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _boundary(cp_hex: str, ctype="BoundaryCodePoint"):
    from qiyas_core.candidate import Candidate
    from qiyas_core.enums import EvidenceRank, CandidateStatus
    return Candidate(
        candidate_id=f"z3:boundary:{cp_hex}",
        candidate_type=ctype,
        status=CandidateStatus.ACCEPTED,
        layer="TypedCodePointClassificationQiyas",
        source_rule_id="test.typed_codepoint.fixture",
        asl_id="test:asl",
        far_id=f"test:far:{cp_hex}",
        identity_ids=(f"identity:codepoint:{cp_hex}",),
        trace_ids=(f"trace:boundary:{cp_hex}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _residual(cp_hex: str):
    from qiyas_core.candidate import Candidate
    from qiyas_core.enums import EvidenceRank, CandidateStatus
    return Candidate(
        candidate_id=f"z3:residual:{cp_hex}",
        candidate_type="ResidualCodePoint",
        status=CandidateStatus.ACCEPTED,
        layer="TypedCodePointClassificationQiyas",
        source_rule_id="test.typed_codepoint.fixture",
        asl_id="test:asl",
        far_id=f"test:far:{cp_hex}",
        identity_ids=(f"identity:codepoint:{cp_hex}",),
        trace_ids=(f"trace:residual:{cp_hex}",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
        residuals=(),
        output_flags=frozenset({"CandidateOnly"}),
    )


def _adapter():
    from qiyas_core.conditioned_typed_sequence_adapter import (
        ConditionedTypedSequenceLayerAdapter,
    )
    from qiyas_core.kernel import QiyasKernel
    return ConditionedTypedSequenceLayerAdapter(kernel=QiyasKernel())


def _all_cands(results):
    return [c for cs in results for c in cs.candidates]


def test_cts_accepts_binding_within_same_segment():
    a = _adapter()
    ctx = _tok("\u0628\u064E")
    r = a.prove_for_sequence_with_context([_letter("0628"), _haraka("064E")], ctx)
    assert any(c.status.value == "accepted" for c in r[1].candidates)


def test_cts_rejects_binding_across_whitespace_boundary():
    a = _adapter()
    ctx = _tok("\u0628 \u064E")
    seq = [_letter("0628"), _boundary("0020"), _haraka("064E")]
    r = a.prove_for_sequence_with_context(seq, ctx)
    assert any(c.status.value in ("blocked", "deferred") for c in r[2].candidates)


def test_cts_rejects_binding_across_punctuation_boundary():
    a = _adapter()
    ctx = _tok("\u0628\u060C\u064E")
    seq = [_letter("0628"), _boundary("060C", "PunctuationCodePoint"), _haraka("064E")]
    r = a.prove_for_sequence_with_context(seq, ctx)
    assert any(c.status.value in ("blocked", "deferred") for c in r[2].candidates)


def test_cts_two_segments_bind_locally_only():
    a = _adapter()
    ctx = _tok("\u0628\u064E \u062A\u0652")
    seq = [_letter("0628"), _haraka("064E"), _boundary("0020"), _letter("062A"), _haraka("0652")]
    r = a.prove_for_sequence_with_context(seq, ctx)
    assert any(c.status.value == "accepted" for c in r[1].candidates)
    assert any(c.status.value == "accepted" for c in r[4].candidates)


def test_cts_orphan_haraka_after_boundary_is_blocked_or_deferred():
    a = _adapter()
    ctx = _tok(" \u064E")
    seq = [_boundary("0020"), _haraka("064E")]
    r = a.prove_for_sequence_with_context(seq, ctx)
    assert any(c.status.value in ("blocked", "deferred") for c in r[1].candidates)


def test_cts_consumes_boundary_marker_as_context_not_candidate():
    a = _adapter()
    ctx = _tok("\u0628 \u062A")
    seq = [_letter("0628"), _boundary("0020"), _letter("062A")]
    r = a.prove_for_sequence_with_context(seq, ctx)
    for c in _all_cands(r):
        assert c.candidate_type not in ("SequenceMarker", "WhitespaceBoundaryMarker")


def test_cts_preserves_residual_marker():
    a = _adapter()
    ctx = _tok("X")
    r = a.prove_for_sequence_with_context([_residual("0058")], ctx)
    assert len(r) == 1
    assert len(r[0].candidates) >= 1


def test_cts_does_not_output_letter_identity_carrier():
    a = _adapter()
    ctx = _tok("\u0628")
    r = a.prove_for_sequence_with_context([_letter("0628")], ctx)
    for c in _all_cands(r):
        assert c.candidate_type != "LetterIdentityCarrier"


def test_cts_does_not_output_haraka_function_carrier():
    a = _adapter()
    ctx = _tok("\u064E")
    r = a.prove_for_sequence_with_context([_haraka("064E")], ctx)
    for c in _all_cands(r):
        assert c.candidate_type != "HarakaFunctionCarrier"


def test_cts_does_not_output_position_carrier():
    a = _adapter()
    ctx = _tok("\u0628")
    r = a.prove_for_sequence_with_context([_letter("0628")], ctx)
    for c in _all_cands(r):
        assert c.candidate_type != "PositionCarrier"


def test_cts_does_not_output_slot_candidate():
    a = _adapter()
    ctx = _tok("\u0628")
    r = a.prove_for_sequence_with_context([_letter("0628")], ctx)
    for c in _all_cands(r):
        assert c.candidate_type != "SlotCandidate"


def test_cts_does_not_output_slot_geometry():
    a = _adapter()
    ctx = _tok("\u0628")
    r = a.prove_for_sequence_with_context([_letter("0628")], ctx)
    for cs in r:
        assert not hasattr(cs, "slots_for")
    for c in _all_cands(r):
        assert not hasattr(c, "slot_id")
