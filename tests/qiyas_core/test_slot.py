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
        asl_id=f"asl:{layer}",
        far_id=f"far:{label}",
        identity_ids=identity_ids,
        rank=EvidenceRank.FORM,
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


# ---------------------------------------------------------------------------
# Contract-required tests
# ---------------------------------------------------------------------------

def test_slot_compatible_baa_fatha():
    """Contract test: BAA + FATHA + INITIAL → SlotCandidate accepted."""
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
    )

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "SlotCandidate"
    assert c.rank == EvidenceRank.FORM
    assert c.layer == "SlotQiyas"


def test_slot_preserves_identity():
    """Contract test: SlotCandidate output must preserve all input identity_ids."""
    letter = _baa_letter_carrier()
    haraka = _fatha_haraka_carrier()
    position = _initial_position_carrier()

    result = _adapter().compose_slot(letter, haraka, position)
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
        node_id="asl:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )
    far = QiyasNodeRef(
        node_id="far:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    # Missing: wasf:has_letter_identity_carrier:evidenced
    proves = (
        "asl:established",
        "far:determined",
        # has_haraka and position present but NOT letter_identity
        "wasf:has_haraka_function_carrier:evidenced",
        "wasf:has_position_carrier:evidenced",
        "wasf:compatible_letter_haraka:evidenced",
        "wasf:compatible_letter_position:evidenced",
        "wasf:identity_preserved:evidenced",
        "illah:belongs_to_slot_composition_domain:verified",
        "illah:slot_composition_licensed:verified",
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_no_letter:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORM,
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
        node_id="asl:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )
    far = QiyasNodeRef(
        node_id="far:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    # Missing: wasf:has_haraka_function_carrier:evidenced
    proves = (
        "asl:established",
        "far:determined",
        "wasf:has_letter_identity_carrier:evidenced",
        # has_haraka missing
        "wasf:has_position_carrier:evidenced",
        "wasf:compatible_letter_haraka:evidenced",
        "wasf:compatible_letter_position:evidenced",
        "wasf:identity_preserved:evidenced",
        "illah:belongs_to_slot_composition_domain:verified",
        "illah:slot_composition_licensed:verified",
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_no_haraka:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORM,
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
        node_id="asl:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )
    far = QiyasNodeRef(
        node_id="far:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    # Missing: wasf:has_position_carrier:evidenced
    proves = (
        "asl:established",
        "far:determined",
        "wasf:has_letter_identity_carrier:evidenced",
        "wasf:has_haraka_function_carrier:evidenced",
        # position missing
        "wasf:compatible_letter_haraka:evidenced",
        "wasf:compatible_letter_position:evidenced",
        "wasf:identity_preserved:evidenced",
        "illah:belongs_to_slot_composition_domain:verified",
        "illah:slot_composition_licensed:verified",
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_no_position:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORM,
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
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
    )
    assert result.accepted[0].candidate_type == "SlotCandidate"


def test_slot_trace_not_in_identity():
    """trace_ids and identity_ids must be disjoint in SlotCandidate."""
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
    )
    c = result.accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_slot_output_flags():
    """SlotCandidate must have CandidateOnly flag."""
    result = _adapter().compose_slot(
        _baa_letter_carrier(),
        _fatha_haraka_carrier(),
        _initial_position_carrier(),
    )
    assert "CandidateOnly" in result.accepted[0].output_flags


def test_slot_carrier_mismatch_blocks():
    """haraka_carrier_mismatch fariq must block slot composition."""
    kernel = _kernel()

    asl = QiyasNodeRef(
        node_id="asl:slot_composition_domain",
        node_type="SlotCompositionDomain",
        identity_ids=("identity:slot_composition_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORM,
    )
    far = QiyasNodeRef(
        node_id="far:test",
        node_type="LetterIdentityCarrier",
        identity_ids=("identity:test",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORM,
    )

    proves = (
        "asl:established",
        "far:determined",
        "wasf:has_letter_identity_carrier:evidenced",
        "wasf:has_haraka_function_carrier:evidenced",
        "wasf:has_position_carrier:evidenced",
        "wasf:compatible_letter_haraka:evidenced",
        "wasf:compatible_letter_position:evidenced",
        "wasf:identity_preserved:evidenced",
        "illah:belongs_to_slot_composition_domain:verified",
        "illah:slot_composition_licensed:verified",
        "wadi:sabab:established",
        "wadi:shart:satisfied",
        "wadi:mani:absent",
        "wadi:sihha:valid",
        "wadi:fasad:absent",
        "wadi:butlan:absent",
        # Invalidating difference
        "fariq:haraka_carrier_mismatch:present",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:slot_mismatch:{uuid.uuid4().hex[:8]}",
            source_layer="SlotQiyas",
            proves=proves,
            rank=EvidenceRank.FORM,
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
