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


WORD_INTERNAL_CLOSURE_READINESS_VALIDATION = QiyasRule(
    rule_id="word_internal_closure_readiness.validation",
    layer="WordInternalClosureReadinessQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="LafzInternalClosureReadinessCandidate",
    far_type="WordClosureContext",
    required_effective_wasf=(
        "lafz_closure_readiness_available",
        "word_boundary_capability",
        "word_internal_closure_ready",
    ),
    required_illah=(
        "word_internal_closure_fit",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "lafz_closure_readiness_missing",
        "word_boundary_conflict",
        "word_closure_readiness_conflict",
    ),
    neutral_identity_domain="word_internal_closure_identity",
    output_candidate_type="WordInternalClosureReadinessCandidate",
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
