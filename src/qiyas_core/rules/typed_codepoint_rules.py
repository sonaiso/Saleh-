from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule


ALL_WADI = (
    WadiGate.SABAB,
    WadiGate.SHART,
    WadiGate.MANI,
    WadiGate.SIHHA,
    WadiGate.FASAD,
    WadiGate.BUTLAN,
)


FORBIDDEN_TYPED_CODEPOINT_OUTPUTS = (
    "AtomicUnitCandidate",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "FormCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
)


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
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
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
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
)


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
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
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
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
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
    forbidden_outputs=FORBIDDEN_TYPED_CODEPOINT_OUTPUTS,
    rank_ceiling=EvidenceRank.FORM,
)
