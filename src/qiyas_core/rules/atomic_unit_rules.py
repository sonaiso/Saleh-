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


ATOMIC_UNIT_BINDING = QiyasRule(
    rule_id="atomic_unit.binding",
    layer="AtomicUnitQiyas",
    pattern=QiyasPattern.COMPOSITION_FIT,
    asl_type="UnicodeCandidate",
    far_type="HarakaCandidate",
    required_effective_wasf=("carrier_accepts_mark",),
    required_illah=("licensed_atomic_binding",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=(
        "carrier_is_not_arabic_letter",
        "mark_is_not_arabic_diacritic",
        "mark_without_carrier",
        "carrier_rejects_mark",
    ),
    neutral_identity_domain="atomic_unit_identity",
    output_candidate_type="AtomicUnitCandidate",
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
