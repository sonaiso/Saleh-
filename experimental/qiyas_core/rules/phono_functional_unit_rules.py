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


PHONO_FUNCTIONAL_UNIT_BINDING = QiyasRule(
    rule_id="phono_functional_unit.binding",
    layer="PhonoFunctionalUnitQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="CarrierFunctionCandidate",
    far_type="MarkFunctionCandidate",
    required_effective_wasf=("carrier_and_mark_functional",),
    required_illah=("phonotactic_unit_composable",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "carrier_function_incomplete",
        "mark_function_incomplete",
        "phonotactic_incompatibility",
    ),
    neutral_identity_domain="phono_functional_unit_identity",
    output_candidate_type="PhonoFunctionalUnitCandidate",
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
