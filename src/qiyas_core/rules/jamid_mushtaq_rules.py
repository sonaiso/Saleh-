"""
Jamid/Mushtaq Rules — SCG-P4 (JamidMushtaq).

The structural derivation-class possibility rule:
  RootStemCandidate → JamidMushtaqCandidate

SCG-P4 opens a structural derivation-class *POSSIBILITY* (إمكان تصنيف جامد/مشتق)
from the root/stem possibility. It is a CANDIDATE-ONLY structural classification:

  - NOT a final judgment that the word IS jamid or mushtaq (WordTypeJudgment forbidden).
  - NOT wazn (WeightCandidate forbidden), NOT morphology, NOT wordhood.
  - NOT lexical meaning / dalalah / i'rab / hukm.

CRITICAL: `jamid_mushtaq_prior_type` is a STRUCTURAL derivation-geometry category,
NEVER a linguistic label (Jamid / Mushtaq / Derived / Verb / Noun / Root / Wazn) —
so the الأصل-الثالث morphological judgment never leaks in.

JamidMushtaqCandidate carries STRUCTURAL evidence only and preserves the
root_stem identity. It OPENS word-type PRIORS for SCG-P5; it never emits them.

Layer: JamidMushtaqQiyas
Input (far): RootStemCandidate
Output:      JamidMushtaqCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_JAMID_MUSHTAQ
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Allowed STRUCTURAL derivation-prior categories (structural ONLY — never the
# linguistic جامد/مشتق judgment). The adapter must use one of these.
DERIVATION_GEOMETRY_CLASS = "DerivationGeometryClass"
STRUCTURAL_DERIVATION_PRIOR = "StructuralDerivationPrior"
ALLOWED_DERIVATION_PRIOR_TYPES = (
    DERIVATION_GEOMETRY_CLASS,
    STRUCTURAL_DERIVATION_PRIOR,
)

# Structural priors P4 OPENS (as priors for SCG-P5), never produces.
OPENED_PRIORS = ("word_type_candidates",)

JAMID_MUSHTAQ_RULE = QiyasRule(
    rule_id="jamid_mushtaq.classify",
    layer="JamidMushtaqQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="JamidMushtaqDomain",
    far_type="RootStemCandidate",
    required_effective_wasf=(
        "has_root_stem_candidate",
        "structural_derivation_possibility_derived",
        "has_jamid_mushtaq_prior_type",
        "has_pattern_evidence",
        "root_stem_candidate_identity_preserved",
    ),
    required_illah=(
        "belongs_to_jamid_mushtaq_domain",
        "jamid_mushtaq_classification_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "derivation_classification_conflict",
        "derivation_pattern_blocked",
    ),
    neutral_identity_domain="jamid_mushtaq_identity",
    output_candidate_type="JamidMushtaqCandidate",
    forbidden_outputs=FORBIDDEN_JAMID_MUSHTAQ,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
