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


MABNI_MURAB_CLOSURE_READINESS_VALIDATION = QiyasRule(
    rule_id="mabni_murab_closure_readiness.validation",
    layer="MabniMurabClosureReadinessQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="ClosureReadinessCandidate",
    far_type="MabniMurabContext",
    required_effective_wasf=(
        "closure_type_distinguishable",
        "mabni_murab_closure_ready",
    ),
    required_illah=(
        "mabni_murab_closure_determinable",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "conflicting_mabni_murab_evidence",
        "closure_type_indeterminate",
    ),
    neutral_identity_domain="mabni_murab_closure_identity",
    output_candidate_type="MabniMurabClosureReadinessCandidate",
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
