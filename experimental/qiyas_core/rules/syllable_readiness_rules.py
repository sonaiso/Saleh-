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


SYLLABLE_READINESS_VALIDATION = QiyasRule(
    rule_id="syllable_readiness.validation",
    layer="SyllableReadinessQiyas",
    pattern=QiyasPattern.CAPABILITY,
    asl_type="PhonoFunctionalUnitCandidate",
    far_type="SyllableContext",
    required_effective_wasf=(
        "minimal_syllabic_structure",
        "left_demand_resolved",
        "right_capability_resolved",
        "syllable_order_equilibrium",
        "minimal_phonotactic_economy",
        "closure_readiness_analyzed",
    ),
    required_illah=(
        "minimal_syllable_readiness",
        "left_right_order_fit",
    ),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "mark_without_carrier",
        "shadda_without_carrier",
        "initial_sukun",
        "additional_diacritic_as_vowel",
        "non_letter_carrier_in_syllable",
        "left_right_mismatch",
        "order_imbalance",
    ),
    neutral_identity_domain="syllable_readiness_identity",
    output_candidate_type="SyllableReadinessCandidate",
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
