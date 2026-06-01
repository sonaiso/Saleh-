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


LAFZ_MINIMAL_COMPLETION_READINESS_VALIDATION = QiyasRule(
    rule_id="lafz_minimal_completion_readiness.validation",
    layer="LafzMinimalCompletionReadinessQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="LafzInternalClosureReadinessCandidate",
    far_type="LafzCompletionContext",
    required_effective_wasf=(
        "lafz_closure_readiness_available",
        "minimal_lafz_components_present",
        "lafz_minimal_completion_ready",
    ),
    required_illah=(
        "lafz_minimal_completion_fit",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "lafz_components_missing",
        "lafz_completion_blocked",
    ),
    neutral_identity_domain="lafz_minimal_completion_identity",
    output_candidate_type="LafzMinimalCompletionReadinessCandidate",
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
