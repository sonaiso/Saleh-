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


LEFT_DEMAND_ANALYSIS = QiyasRule(
    rule_id="left_demand.analysis",
    layer="LeftDemandQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="PhonoFunctionalUnitCandidate",
    far_type="LeftContext",
    required_effective_wasf=("left_position_analyzed",),
    required_illah=("left_demand_determinable",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "left_context_indeterminate",
        "position_unknown",
    ),
    neutral_identity_domain="left_demand_identity",
    output_candidate_type="LeftDemandCandidate",
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
