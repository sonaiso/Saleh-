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


CARRIER_FUNCTION_CLASSIFICATION = QiyasRule(
    rule_id="carrier_function.classification",
    layer="CarrierFunctionQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="AtomicUnitCandidate",
    far_type="CarrierCodepoint",
    required_effective_wasf=("carrier_has_phonotactic_role",),
    required_illah=("carrier_function_determinable",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "non_carrier_codepoint",
        "carrier_function_indeterminate",
    ),
    neutral_identity_domain="carrier_function_identity",
    output_candidate_type="CarrierFunctionCandidate",
    forbidden_outputs=(
        "SyllableCandidate",
        "PronunciationCandidate",
        "DalCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ),
    rank_ceiling=EvidenceRank.FORM,
)
