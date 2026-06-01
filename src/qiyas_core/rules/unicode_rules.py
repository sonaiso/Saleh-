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


UNICODE_ARABIC_MEMBERSHIP = QiyasRule(
    rule_id="unicode.arabic.membership",
    layer="UnicodeQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="ArabicUnicodeBlock",
    far_type="InputCodepoint",
    required_effective_wasf=("unicode_codepoint_in_arabic_range",),
    required_illah=("belongs_to_arabic_script_domain",),
    required_wadi_gates=ALL_WADI,
    invalidating_differences=("non_arabic_codepoint", "control_character"),
    neutral_identity_domain="unicode_identity",
    output_candidate_type="UnicodeCandidate",
    forbidden_outputs=(
        # PR #29 — global recursion closure: UnicodeQiyas is the
        # outermost pre-slot membership layer; it cannot jump to the
        # composition layer or to its hypothetical successor.
        "SlotCandidate",
        "SlotGeometry",
        "PronunciationCandidate",
        # PR #31 — normalized from the abbreviated "DalCandidate" to the
        # canonical layer-output name "DalalahCandidate" as defined in
        # LAYER_CONTRACT_CONSTITUTION.md §7.7 (DalalahTypeGate).
        "DalalahCandidate",
        "HukmCandidate",
        "RealityClaim",
        "FinalMeaning",
    ),
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
