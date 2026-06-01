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


LAFZ_INTERNAL_CLOSURE_READINESS_VALIDATION = QiyasRule(
    rule_id="lafz_internal_closure_readiness.validation",
    layer="LafzInternalClosureReadinessQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="SyllableReadinessCandidate",
    far_type="LafzClosureContext",
    required_effective_wasf=(
        "syllable_readiness_available",
        "internal_lafz_order_preserved",
        "lafz_internal_closure_ready",
    ),
    required_illah=(
        "lafz_internal_closure_fit",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "syllable_readiness_missing",
        "lafz_order_conflict",
        "closure_readiness_conflict",
    ),
    neutral_identity_domain="lafz_internal_closure_identity",
    output_candidate_type="LafzInternalClosureReadinessCandidate",
    forbidden_outputs=(
        "SyllableCandidate",
        "LafzCandidate",
        "WordCandidate",
        "MeaningCandidate",
        "IfadahCandidate",
        "SyntaxCandidate",
        "RelationCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ),
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
