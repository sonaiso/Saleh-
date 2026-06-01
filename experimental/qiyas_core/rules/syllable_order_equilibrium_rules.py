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


SYLLABLE_ORDER_EQUILIBRIUM_VALIDATION = QiyasRule(
    rule_id="syllable_order_equilibrium.validation",
    layer="SyllableOrderEquilibriumQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="LeftDemandCandidate",
    far_type="RightCapabilityCandidate",
    required_effective_wasf=("left_demand_resolved", "right_capability_resolved"),
    required_illah=("left_right_order_fit",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "left_demand_unresolved",
        "right_capability_unresolved",
        "left_right_mismatch",
        "order_imbalance",
        "economy_not_verified",
    ),
    neutral_identity_domain="syllable_order_equilibrium_identity",
    output_candidate_type="SyllableOrderEquilibriumCandidate",
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
