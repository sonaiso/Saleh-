"""
Slot Rules — Gap #6 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

The first algebraic composition rule:
  LetterIdentityCarrier + HarakaFunctionCarrier + PositionCarrier → SlotCandidate

Only produced when:
  Compatible(letter, haraka, position)
  AND PreserveIdentity(letter, haraka, position)

SlotCandidate contains:
  consonantal_identity + vocalic_function + position +
  acoustic_sequence + energy_profile (consonant-dominant).

Constitutional law:
  SlotCandidate ⊬ SyllableCandidate (adjacency not yet established)
  SlotCandidate ⊬ MeaningCandidate

Layer: SlotQiyas
Input (far): LetterIdentityCarrier (the carrier; haraka + position proven in evidence)
Output:      SlotCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_SLOT
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

SLOT_COMPOSITION_RULE = QiyasRule(
    rule_id="slot.composition",
    layer="SlotQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="SlotCompositionDomain",
    far_type="LetterIdentityCarrier",
    required_effective_wasf=(
        "has_letter_identity_carrier",
        "has_haraka_function_carrier",
        "has_position_carrier",
        # PR #26 — SlotCandidate now requires explicit alignment evidence
        # from ConditionedTypedSequenceQiyas. The two compatibility wasfs
        # below MUST be derived from that prior proof; the adapter no
        # longer asserts them autonomously.
        "has_alignment_evidence",
        "compatible_letter_haraka",
        "compatible_letter_position",
        "identity_preserved",
    ),
    required_illah=(
        "belongs_to_slot_composition_domain",
        "slot_composition_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "haraka_carrier_mismatch",
        "position_identity_conflict",
        "slot_composition_blocked",
    ),
    neutral_identity_domain="slot_identity",
    output_candidate_type="SlotCandidate",
    forbidden_outputs=FORBIDDEN_SLOT,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
