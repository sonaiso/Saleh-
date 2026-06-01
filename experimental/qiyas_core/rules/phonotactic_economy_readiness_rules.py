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


PHONOTACTIC_ECONOMY_READINESS_VALIDATION = QiyasRule(
    rule_id="phonotactic_economy_readiness.validation",
    layer="PhonotacticEconomyReadinessQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="PhonoFunctionalUnitCandidate",
    far_type="PhonotacticEconomyContext",
    required_effective_wasf=("minimal_phonotactic_economy",),
    required_illah=("phonotactic_economy_sufficient",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "phonotactic_redundancy",
        "minimal_economy_violated",
    ),
    neutral_identity_domain="phonotactic_economy_readiness_identity",
    output_candidate_type="PhonotacticEconomyReadinessCandidate",
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
