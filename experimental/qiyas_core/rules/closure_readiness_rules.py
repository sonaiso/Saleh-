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


CLOSURE_READINESS_VALIDATION = QiyasRule(
    rule_id="closure_readiness.validation",
    layer="ClosureReadinessQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="PhonoFunctionalUnitCandidate",
    far_type="ClosureContext",
    required_effective_wasf=("closure_readiness_analyzed",),
    required_illah=("closure_readiness_determinable",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "closure_context_indeterminate",
        "conflicting_mabni_murab_evidence",
    ),
    neutral_identity_domain="closure_readiness_identity",
    output_candidate_type="ClosureReadinessCandidate",
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
