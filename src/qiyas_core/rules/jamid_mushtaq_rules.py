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
# linguistic جامد/مشتق judgment). SCG-P4 strengthening (2026-06-18): the adapter
# now SELECTS one input-dependently from the structural derivation geometry
# (gemination / consonantal-skeleton size) — it is no longer the constant
# DerivationGeometryClass. None of these is a final جامد/مشتق label.
DERIVATION_GEOMETRY_CLASS = "DerivationGeometryClass"            # full skeleton (nC>=3)
DERIVATION_GEOMETRY_PRIOR = "DerivationGeometryPrior"            # minimal skeleton (nC==2)
STRUCTURAL_DERIVATION_POSSIBILITY = "StructuralDerivationPossibility"  # gemination-bearing
STRUCTURAL_DERIVATION_PRIOR = "StructuralDerivationPrior"        # legacy alias (kept)
ALLOWED_DERIVATION_PRIOR_TYPES = (
    DERIVATION_GEOMETRY_CLASS,
    DERIVATION_GEOMETRY_PRIOR,
    STRUCTURAL_DERIVATION_POSSIBILITY,
    STRUCTURAL_DERIVATION_PRIOR,
)

# Derivation-geometry verdict reasons (SCG-P4 strengthening). P4 is no longer a
# forwarding stamp: it discriminates the derivation geometry it reads from the
# upstream RootStemCandidate into ACCEPT / DEFER / BLOCK, routed through the
# kernel's existing `فارق:` (block) / `defer:` (defer) machinery.
#   ACCEPT : P3 ACCEPT and a consonantal skeleton (n_consonants >= 2) able to
#            open a derivation-geometry possibility.
#   DEFER  : derivation skeleton too thin (n_consonants == 1) — underspecified.
#   BLOCK  : P3 was DEFER/BLOCK, or the derivation geometry conflicts.
DERIVATION_CLASSIFICATION_CONFLICT = "derivation_classification_conflict"  # BLOCK (فارق)
DERIVATION_PATTERN_BLOCKED = "derivation_pattern_blocked"                  # BLOCK (فارق)
DERIVATION_UNDERSPECIFIED = "derivation_underspecified"                    # DEFER (defer)

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
        DERIVATION_CLASSIFICATION_CONFLICT,
        DERIVATION_PATTERN_BLOCKED,
    ),
    neutral_identity_domain="jamid_mushtaq_identity",
    output_candidate_type="JamidMushtaqCandidate",
    forbidden_outputs=FORBIDDEN_JAMID_MUSHTAQ,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
