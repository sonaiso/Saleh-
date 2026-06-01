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


RIGHT_CAPABILITY_ANALYSIS = QiyasRule(
    rule_id="right_capability.analysis",
    layer="RightCapabilityQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="PhonoFunctionalUnitCandidate",
    far_type="RightContext",
    required_effective_wasf=("right_position_analyzed",),
    required_illah=("right_capability_determinable",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "right_context_indeterminate",
        "position_unknown",
    ),
    neutral_identity_domain="right_capability_identity",
    output_candidate_type="RightCapabilityCandidate",
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
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
