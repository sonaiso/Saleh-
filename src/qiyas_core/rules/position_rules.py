"""
Position Rules — Gap #5 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

Layer: PositionQiyas
Input (far): PositionEvidence  (canonical origin — emitted by ConditionedTypedSequence;
             SCG-P1 PR-2). The codepoint is carried only as a trace/bridge reference,
             never as the consumed canonical identity.
Output:      PositionCarrier

A PositionCarrier carries:
  index, position_type (INITIAL/MEDIAL/FINAL/ISOLATED),
  within_word, at_boundary, accepts_haraka/shadda/tanwin,
  waqf_eligible, wasl_eligible.

The single POSITION_RULE proves that a codepoint occupies a determinable
position in a sequence.  Adapters supply the concrete position evidence.
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_POSITION
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Position types
POSITION_INITIAL = "INITIAL"
POSITION_MEDIAL = "MEDIAL"
POSITION_FINAL = "FINAL"
POSITION_ISOLATED = "ISOLATED"

ALL_POSITION_TYPES = (
    POSITION_INITIAL,
    POSITION_MEDIAL,
    POSITION_FINAL,
    POSITION_ISOLATED,
)


def _make_position_rule(position_type: str) -> QiyasRule:
    return QiyasRule(
        rule_id=f"position.{position_type.lower()}",
        layer="PositionQiyas",
        pattern=QiyasPattern.MEMBERSHIP,
        asl_type="PositionDomain",
        # SCG-P1 PR-2: canonical origin is the ConditionedTypedSequence PositionEvidence.
        far_type="PositionEvidence",
        required_effective_wasf=(
            "has_position_index",
            f"has_position_type:{position_type.lower()}",
            "within_word_determined",
        ),
        required_illah=(
            "belongs_to_position_domain",
            f"position_type_is:{position_type.lower()}",
        ),
        required_wadi_gates=_ALL_WADI,
        invalidating_differences=(
            "position_type_ambiguous",
            "index_out_of_bounds",
        ),
        neutral_identity_domain="position_identity",
        output_candidate_type="PositionCarrier",
        forbidden_outputs=FORBIDDEN_POSITION,
        rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
    )


INITIAL_POSITION_RULE = _make_position_rule(POSITION_INITIAL)
MEDIAL_POSITION_RULE = _make_position_rule(POSITION_MEDIAL)
FINAL_POSITION_RULE = _make_position_rule(POSITION_FINAL)
ISOLATED_POSITION_RULE = _make_position_rule(POSITION_ISOLATED)


POSITION_RULES: dict[str, QiyasRule] = {
    POSITION_INITIAL: INITIAL_POSITION_RULE,
    POSITION_MEDIAL: MEDIAL_POSITION_RULE,
    POSITION_FINAL: FINAL_POSITION_RULE,
    POSITION_ISOLATED: ISOLATED_POSITION_RULE,
}


def get_position_rule(position_type: str) -> QiyasRule | None:
    """Return the PositionQiyas rule for the given position type string."""
    return POSITION_RULES.get(position_type.upper())
