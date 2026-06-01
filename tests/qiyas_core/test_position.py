"""
Tests for PositionCarrier layer — Gap #5 of ALGEBRAIC_FOUNDATION_CONTRACT.md.
"""

from qiyas_core.enums import CandidateStatus, EvidenceRank
from qiyas_core.kernel import QiyasKernel
from qiyas_core.position_adapter import PositionLayerAdapter
from qiyas_core.rules.position_rules import (
    INITIAL_POSITION_RULE,
    MEDIAL_POSITION_RULE,
    FINAL_POSITION_RULE,
    ISOLATED_POSITION_RULE,
    POSITION_INITIAL,
    POSITION_MEDIAL,
    POSITION_FINAL,
    POSITION_ISOLATED,
)


def _adapter() -> PositionLayerAdapter:
    return PositionLayerAdapter(kernel=QiyasKernel())


def test_initial_position_accepted():
    """INITIAL position rule accepts a letter at index 0."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_INITIAL, index=0)

    assert len(result.accepted) == 1
    c = result.accepted[0]
    assert c.status == CandidateStatus.ACCEPTED
    assert c.candidate_type == "PositionCarrier"
    assert "initial" in c.source_rule_id


def test_medial_position_accepted():
    """MEDIAL position rule accepts a letter at index 1."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_MEDIAL, index=1)

    assert len(result.accepted) == 1
    assert "medial" in result.accepted[0].source_rule_id


def test_final_position_accepted():
    """FINAL position rule accepts a letter at index 2."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_FINAL, index=2)

    assert len(result.accepted) == 1
    assert "final" in result.accepted[0].source_rule_id


def test_isolated_position_accepted():
    """ISOLATED position rule accepts a single-letter word."""
    result = _adapter().prove_from_codepoint(0x0648, position_type=POSITION_ISOLATED, index=0)

    assert len(result.accepted) == 1
    assert "isolated" in result.accepted[0].source_rule_id


def test_position_carrier_type():
    """Output candidate_type must be PositionCarrier."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_INITIAL)
    assert result.accepted[0].candidate_type == "PositionCarrier"


def test_position_carrier_rank():
    """Rank must be FORM."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_INITIAL)
    assert result.accepted[0].rank == EvidenceRank.FORMAL_STRUCTURE


def test_position_preserves_codepoint_identity():
    """Output must preserve the source codepoint identity."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_MEDIAL, index=1)
    c = result.accepted[0]
    assert "identity:codepoint:0628" in set(c.identity_ids)


def test_position_trace_not_in_identity():
    """trace_ids and identity_ids must be disjoint."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_INITIAL)
    c = result.accepted[0]
    assert not (set(c.identity_ids) & set(c.trace_ids))


def test_position_output_flags():
    """Output must have CandidateOnly flag."""
    result = _adapter().prove_from_codepoint(0x0628, position_type=POSITION_INITIAL)
    assert "CandidateOnly" in result.accepted[0].output_flags


def test_position_ambiguous_difference_blocks():
    """position_type_ambiguous fariq must block the position rule."""
    import uuid
    from qiyas_core.evidence import Evidence, EvidenceSet
    from qiyas_core.kernel import QiyasContext, QiyasKernel, QiyasRequest
    from qiyas_core.node import QiyasNodeRef

    kernel = QiyasKernel()

    asl = QiyasNodeRef(
        node_id="اصل:position_domain",
        node_type="PositionDomain",
        identity_ids=("identity:position_domain",),
        trace_ids=("trace:asl",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )
    far = QiyasNodeRef(
        node_id="فرع:letter_codepoint:0628:pos0",
        node_type="LetterCodePoint",
        identity_ids=("identity:codepoint:0628",),
        trace_ids=("trace:far",),
        rank=EvidenceRank.FORMAL_STRUCTURE,
    )

    proves = (
        "اصل:established",
        "فرع:determined",
        "وصف:has_position_index:evidenced",
        "وصف:has_position_type:initial:evidenced",
        "وصف:within_word_determined:evidenced",
        "علة:belongs_to_position_domain:verified",
        "علة:position_type_is:initial:verified",
        "وادي:cause:established",
        "وادي:condition:satisfied",
        "وادي:obstacle:absent",
        "وادي:validity:valid",
        "وادي:corruption:absent",
        "وادي:nullity:absent",
        # Invalidating difference
        "فارق:position_type_ambiguous:present",
    )

    evidence = EvidenceSet(items=(
        Evidence(
            evidence_id=f"ev:pos_ambiguous:{uuid.uuid4().hex[:8]}",
            source_layer="PositionQiyas",
            proves=proves,
            rank=EvidenceRank.FORMAL_STRUCTURE,
            trace_ids=("trace:ev",),
        ),
    ))

    request = QiyasRequest(
        rule=INITIAL_POSITION_RULE,
        asl=asl,
        far=far,
        evidence=evidence,
        context=QiyasContext(layer="PositionQiyas"),
    )

    result = kernel.apply(request)
    assert len(result.blocked) == 1
    assert any(r.residual_type == "blocking_fariq_present" for r in result.residuals)


def test_position_forbids_syllable():
    """PositionCarrier layer must forbid SyllableCandidate."""
    assert "SyllableCandidate" in INITIAL_POSITION_RULE.forbidden_outputs
    assert "SyllableCandidate" in MEDIAL_POSITION_RULE.forbidden_outputs
    assert "SyllableCandidate" in FINAL_POSITION_RULE.forbidden_outputs
    assert "SyllableCandidate" in ISOLATED_POSITION_RULE.forbidden_outputs


def test_position_forbids_meaning():
    """PositionCarrier layer must forbid MeaningCandidate."""
    assert "MeaningCandidate" in INITIAL_POSITION_RULE.forbidden_outputs


def test_position_forbids_hukm():
    """PositionCarrier layer must forbid HukmCandidate."""
    assert "HukmCandidate" in INITIAL_POSITION_RULE.forbidden_outputs


def test_position_layer_name():
    """All position rules must be in the PositionQiyas layer."""
    for rule in (
        INITIAL_POSITION_RULE, MEDIAL_POSITION_RULE,
        FINAL_POSITION_RULE, ISOLATED_POSITION_RULE,
    ):
        assert rule.layer == "PositionQiyas"
