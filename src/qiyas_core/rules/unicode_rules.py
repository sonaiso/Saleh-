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


UNICODE_ARABIC_MEMBERSHIP = QiyasRule(
    rule_id="unicode.arabic.membership",
    layer="UnicodeQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicUnicodeBlock",
    far_type="InputCodepoint",
    required_effective_wasf=("unicode_codepoint_in_arabic_range",),
    required_illah=("belongs_to_arabic_script_domain",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=("non_arabic_codepoint", "control_character"),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="UnicodeCandidate",
    forbidden_outputs=(
        "PronunciationCandidate",
        "DalCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ),
    rank_ceiling=EvidenceRank.FORM,
)
