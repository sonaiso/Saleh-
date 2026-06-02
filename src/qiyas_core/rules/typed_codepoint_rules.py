from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_TYPED_CODEPOINT
from qiyas_core.rule import QiyasRule


ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


# PR #29 source-of-truth fix: the previous local tuple
# `FORBIDDEN_TYPED_CODEPOINT` has been removed. Every rule below
# now uses `FORBIDDEN_TYPED_CODEPOINT` imported from
# `qiyas_core.forbidden_outputs`, so the global recursion closure
# (SlotCandidate, SlotGeometry) propagates here automatically.


LETTER_CODEPOINT_CLASSIFICATION = QiyasRule(
    rule_id="typed_codepoint.letter_classification",
    layer="TypedCodePointClassificationQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="TypedCodePointClassificationDomain",
    far_type="UnicodeCandidate",
    required_effective_wasf=(
        "is_classifiable_codepoint",
        "is_arabic_letter",
    ),
    required_illah=(
        "belongs_to_typed_domain",
        "belongs_to_letter_class",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "multiple_classes_claimed",
        "ambiguous_classification",
        "letter_haraka_overlap",
    ),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="LetterCodePoint",
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


HARAKA_CODEPOINT_CLASSIFICATION = QiyasRule(
    rule_id="typed_codepoint.haraka_classification",
    layer="TypedCodePointClassificationQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="TypedCodePointClassificationDomain",
    far_type="UnicodeCandidate",
    required_effective_wasf=(
        "is_classifiable_codepoint",
        "is_arabic_haraka",
    ),
    required_illah=(
        "belongs_to_typed_domain",
        "belongs_to_haraka_class",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "multiple_classes_claimed",
        "ambiguous_classification",
        "letter_haraka_overlap",
    ),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="HarakaCodePoint",
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


# Z4 declassification (PRE_QIYAS_TOKENIZER_CONSTITUTION §6):
#   `BOUNDARY_CODEPOINT_CLASSIFICATION` is **legacy unreachable** in any
#   canonical execution path. `UnicodeQiyas` rejects whitespace before it
#   can reach the TypedCodePoint layer, and `SequenceContextTokenizer`
#   (Z2) is the constitutional source of whitespace evidence. The rule
#   survives only to keep legacy unit fixtures and external re-exports
#   stable. Do not add new canonical callers.
BOUNDARY_CODEPOINT_CLASSIFICATION = QiyasRule(
    rule_id="typed_codepoint.boundary_classification",
    layer="TypedCodePointClassificationQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="TypedCodePointClassificationDomain",
    far_type="UnicodeCandidate",
    required_effective_wasf=(
        "is_classifiable_codepoint",
        "is_whitespace_boundary",
    ),
    required_illah=(
        "belongs_to_typed_domain",
        "belongs_to_boundary_class",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "multiple_classes_claimed",
        "ambiguous_classification",
        "boundary_punctuation_overlap",
    ),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="BoundaryCodePoint",
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


PUNCTUATION_CODEPOINT_CLASSIFICATION = QiyasRule(
    rule_id="typed_codepoint.punctuation_classification",
    layer="TypedCodePointClassificationQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="TypedCodePointClassificationDomain",
    far_type="UnicodeCandidate",
    required_effective_wasf=(
        "is_classifiable_codepoint",
        "is_arabic_punctuation",
    ),
    required_illah=(
        "belongs_to_typed_domain",
        "belongs_to_punctuation_class",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "multiple_classes_claimed",
        "ambiguous_classification",
        "boundary_punctuation_overlap",
    ),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="PunctuationCodePoint",
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)


RESIDUAL_CODEPOINT_CLASSIFICATION = QiyasRule(
    rule_id="typed_codepoint.residual_classification",
    layer="TypedCodePointClassificationQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="TypedCodePointClassificationDomain",
    far_type="UnicodeCandidate",
    required_effective_wasf=(
        "is_classifiable_codepoint",
        "is_unclassified_codepoint",
    ),
    required_illah=(
        "belongs_to_typed_domain",
        "belongs_to_residual_class",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "multiple_classes_claimed",
        "ambiguous_classification",
    ),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="ResidualCodePoint",
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
