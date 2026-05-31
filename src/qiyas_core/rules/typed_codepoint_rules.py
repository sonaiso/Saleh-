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


TYPED_CODEPOINT_CLASSIFICATION = QiyasRule(
    rule_id="typed_codepoint.classification",
    layer="TypedCodePointClassificationQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="TypedCodePointClassificationDomain",
    far_type="UnicodeCandidate",
    # Generic wasf/illah that applies to all classifications
    # The specific type is determined by the candidate_type, not by wasf/illah
    required_effective_wasf=("is_classifiable_codepoint",),
    required_illah=("belongs_to_typed_domain",),
    required_wadi_gates=ALL_WADI,
    # Disjoint union proof: these differences invalidate classification
    # if multiple types are claimed simultaneously
    invalidating_differences=(
        "multiple_classes_claimed",  # If more than one classification type is claimed
        "ambiguous_classification",  # If classification logic is ambiguous
        "letter_haraka_overlap",  # If codepoint claims to be both letter and haraka
        "boundary_punctuation_overlap",  # If codepoint claims to be both boundary and punctuation
    ),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="TypedCodePoint",
    forbidden_outputs=(
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
    ),
    rank_ceiling=EvidenceRank.FORM,
)
