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


WORD_MINIMAL_COMPLETION_READINESS_VALIDATION = QiyasRule(
    rule_id="word_minimal_completion_readiness.validation",
    layer="WordMinimalCompletionReadinessQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="WordInternalClosureReadinessCandidate",
    far_type="WordCompletionContext",
    required_effective_wasf=(
        "word_closure_readiness_available",
        "minimal_word_components_present",
        "word_minimal_completion_ready",
    ),
    required_illah=(
        "word_minimal_completion_fit",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "word_components_missing",
        "word_completion_blocked",
    ),
    neutral_identity_domain="word_minimal_completion_identity",
    output_candidate_type="WordMinimalCompletionReadinessCandidate",
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
    rank_ceiling=EvidenceRank.FORM,
)
