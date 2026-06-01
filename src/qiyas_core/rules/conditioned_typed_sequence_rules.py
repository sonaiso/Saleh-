"""
Conditioned Typed Sequence Rules — PR #25.

Layer: ConditionedTypedSequenceQiyas

Per CLAUDE.md §7, this layer produces ONLY:
    AlignmentEvidence
    CarrierBindingCandidate
    CarrierBindingEvidence
    PositionEvidence
    BoundaryEvidence
    ResidualPreservationEvidence
    SequenceAdmissibilityProof

It MUST NOT produce:
    LetterIdentityCarrier
    HarakaFunctionCarrier
    SlotCandidate
    SlotGeometry
    FinalMeaning
    HukmCandidate
    RealityClaim

Per CLAUDE.md §8, SlotCandidate cannot be produced without
CarrierBindingEvidence (or AlignmentEvidence) from this layer. The
inverse does NOT hold: this layer does not require any downstream
layer to produce its evidence.

Five sister-rules mirror the five TypedCodePoint classifications so
that every symbol in the sequence is given a position context (CLAUDE.md
§7 bullet "every symbol has position and context").
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_CONDITIONED_TYPED_SEQUENCE
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

_CTS_LAYER = "ConditionedTypedSequenceQiyas"
_CTS_DOMAIN = "ConditionedTypedSequenceDomain"


# ---------------------------------------------------------------------------
# 1. CARRIER_BINDING_PROOF
#    HarakaCodePoint with an immediately-preceding LetterCodePoint
#    in the sequence → CarrierBindingCandidate.
#    A haraka with no carrier triggers the invalidating-difference
#    "haraka_without_carrier" and produces a blocked candidate.
# ---------------------------------------------------------------------------

CARRIER_BINDING_PROOF = QiyasRule(
    rule_id="conditioned_typed_sequence.carrier_binding",
    layer=_CTS_LAYER,
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type=_CTS_DOMAIN,
    far_type="HarakaCodePoint",
    required_effective_wasf=(
        "has_haraka_in_sequence",
        "preceded_by_letter_codepoint",
        "sequence_index_determined",
        "carrier_alignment_determined",
    ),
    required_illah=(
        "belongs_to_conditioned_typed_sequence_domain",
        "carrier_binding_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "haraka_without_carrier",
        "carrier_is_boundary",
        "carrier_is_punctuation",
        "orphan_mark",
    ),
    neutral_identity_domain="conditioned_typed_sequence_identity",
    output_candidate_type="CarrierBindingCandidate",
    forbidden_outputs=FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# ---------------------------------------------------------------------------
# 2. LETTER_POSITION_PROOF
#    LetterCodePoint in the sequence → PositionEvidence
#    (every letter gets sequence-context evidence regardless of binding).
# ---------------------------------------------------------------------------

LETTER_POSITION_PROOF = QiyasRule(
    rule_id="conditioned_typed_sequence.letter_position",
    layer=_CTS_LAYER,
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type=_CTS_DOMAIN,
    far_type="LetterCodePoint",
    required_effective_wasf=(
        "has_letter_in_sequence",
        "sequence_index_determined",
        "neighbor_context_determined",
    ),
    required_illah=(
        "belongs_to_conditioned_typed_sequence_domain",
        "letter_position_in_sequence_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "letter_position_ambiguous",
        "sequence_index_out_of_bounds",
    ),
    neutral_identity_domain="conditioned_typed_sequence_identity",
    output_candidate_type="PositionEvidence",
    forbidden_outputs=FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# ---------------------------------------------------------------------------
# 3. BOUNDARY_EXCLUSION_PROOF
#    BoundaryCodePoint (whitespace) → BoundaryEvidence.
#    Proves the boundary is excluded from any slot composition.
# ---------------------------------------------------------------------------

BOUNDARY_EXCLUSION_PROOF = QiyasRule(
    rule_id="conditioned_typed_sequence.boundary_exclusion",
    layer=_CTS_LAYER,
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type=_CTS_DOMAIN,
    far_type="BoundaryCodePoint",
    required_effective_wasf=(
        "has_boundary_in_sequence",
        "sequence_index_determined",
        "boundary_excluded_from_slot",
    ),
    required_illah=(
        "belongs_to_conditioned_typed_sequence_domain",
        "boundary_exclusion_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "boundary_enters_slot",
    ),
    neutral_identity_domain="conditioned_typed_sequence_identity",
    output_candidate_type="BoundaryEvidence",
    forbidden_outputs=FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# ---------------------------------------------------------------------------
# 4. PUNCTUATION_EXCLUSION_PROOF
#    PunctuationCodePoint → BoundaryEvidence.
#    Punctuation is treated as a sequence-barrier (same candidate type
#    as whitespace boundaries) so it cannot enter a slot composition.
# ---------------------------------------------------------------------------

PUNCTUATION_EXCLUSION_PROOF = QiyasRule(
    rule_id="conditioned_typed_sequence.punctuation_exclusion",
    layer=_CTS_LAYER,
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type=_CTS_DOMAIN,
    far_type="PunctuationCodePoint",
    required_effective_wasf=(
        "has_punctuation_in_sequence",
        "sequence_index_determined",
        "punctuation_excluded_from_slot",
    ),
    required_illah=(
        "belongs_to_conditioned_typed_sequence_domain",
        "punctuation_exclusion_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "punctuation_enters_slot",
    ),
    neutral_identity_domain="conditioned_typed_sequence_identity",
    output_candidate_type="BoundaryEvidence",
    forbidden_outputs=FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# ---------------------------------------------------------------------------
# 5. RESIDUAL_PRESERVATION_PROOF
#    ResidualCodePoint → ResidualPreservationEvidence.
#    Records that an unclassified symbol exists in the sequence with a
#    position; the residual is preserved (not silently dropped) per
#    CLAUDE.md §4 invariant 7.
# ---------------------------------------------------------------------------

RESIDUAL_PRESERVATION_PROOF = QiyasRule(
    rule_id="conditioned_typed_sequence.residual_preservation",
    layer=_CTS_LAYER,
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type=_CTS_DOMAIN,
    far_type="ResidualCodePoint",
    required_effective_wasf=(
        "has_residual_codepoint_in_sequence",
        "sequence_index_determined",
        "residual_preserved",
    ),
    required_illah=(
        "belongs_to_conditioned_typed_sequence_domain",
        "residual_preservation_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "residual_silently_discarded",
    ),
    neutral_identity_domain="conditioned_typed_sequence_identity",
    output_candidate_type="ResidualPreservationEvidence",
    forbidden_outputs=FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

CTS_RULES_BY_FAR_TYPE: dict[str, QiyasRule] = {
    "HarakaCodePoint":      CARRIER_BINDING_PROOF,
    "LetterCodePoint":      LETTER_POSITION_PROOF,
    "BoundaryCodePoint":    BOUNDARY_EXCLUSION_PROOF,
    "PunctuationCodePoint": PUNCTUATION_EXCLUSION_PROOF,
    "ResidualCodePoint":    RESIDUAL_PRESERVATION_PROOF,
}


def get_cts_rule_for_far_type(far_type: str) -> QiyasRule | None:
    """Return the CTS rule for a given TypedCodePoint candidate_type."""
    return CTS_RULES_BY_FAR_TYPE.get(far_type)
