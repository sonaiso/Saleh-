from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule


ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


HARAKA_ARABIC_DIACRITIC = QiyasRule(
    rule_id="haraka.arabic.diacritic",
    layer="HarakaQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicDiacriticDomain",
    far_type="InputCodepoint",
    required_effective_wasf=("codepoint_is_arabic_combining_mark",),
    required_illah=("belongs_to_haraka_vocalization_domain",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=("non_haraka_codepoint", "non_combining_character"),
    neutral_identity_domain="haraka_identity",
    output_candidate_type="HarakaCandidate",
    forbidden_outputs=(
        "AtomicUnitCandidate",
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ),
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
