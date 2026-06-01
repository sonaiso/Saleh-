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


MARK_FUNCTION_CLASSIFICATION = QiyasRule(
    rule_id="mark_function.classification",
    layer="MarkFunctionQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="AtomicUnitCandidate",
    far_type="MarkCodepoint",
    required_effective_wasf=("mark_has_phonotactic_role",),
    required_illah=("mark_function_determinable",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "non_diacritic_mark",
        "mark_function_indeterminate",
    ),
    neutral_identity_domain="mark_function_identity",
    output_candidate_type="MarkFunctionCandidate",
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
