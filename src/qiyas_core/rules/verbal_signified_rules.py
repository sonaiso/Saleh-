"""
Verbal Signified Rules — SCG-P6 (VerbalSignified).

The verbal-signified possibility rule:
  MufradWordCandidate → VerbalSignifiedCandidate

SCG-P6 answers ONLY: "what verbal-signified semantic POSSIBILITIES does this
MufradWordCandidate open?" (VERBAL_SIGNIFIED_CONSTITUTION.md). It is a
CANDIDATE-ONLY layer that OPENS meaning + dalalah PRIORS — it never decides them:

  - NOT actual meaning (MeaningCandidate forbidden), NOT dalalah
    (DalalahCandidate / DalalahJudgment forbidden), NOT tafsir, NOT hukm,
    NOT reality / final meaning.

VerbalSignifiedCandidate carries STRUCTURAL evidence only (mufrad_word identity,
opened meaning priors, opened dalalah priors) and preserves the upstream
identities. The priors are PRIORS for downstream phases; never emitted as
candidates here.

Layer: VerbalSignifiedQiyas
Input (far): MufradWordCandidate
Output:      VerbalSignifiedCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_VERBAL_SIGNIFIED
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Allowed STRUCTURAL verbal-signified carrier prior types (SCG-P6 strengthening,
# 2026-06-18). Structural ONLY — never a verb/فعل/tense/aspect/voice/meaning
# judgment. The adapter SELECTS one input-dependently from the carrier geometry.
VERBAL_CARRIER_GEOMETRY_CLASS = "VerbalCarrierGeometryClass"          # rich consonantal carrier
STRUCTURAL_SIGNIFIED_CARRIER_PRIOR = "StructuralSignifiedCarrierPrior"  # minimal carrier
SHORT_VOWEL_CADENCE_PRIOR = "ShortVowelCadencePrior"                  # CVCV-cadence carrier
GEMINATED_CARRIER_POSSIBILITY = "GeminatedCarrierPossibility"        # gemination-bearing carrier
ALLOWED_VERBAL_SIGNIFIED_PRIOR_TYPES = (
    VERBAL_CARRIER_GEOMETRY_CLASS,
    STRUCTURAL_SIGNIFIED_CARRIER_PRIOR,
    SHORT_VOWEL_CADENCE_PRIOR,
    GEMINATED_CARRIER_POSSIBILITY,
)

# Verbal-signified carrier verdict reasons. P6 is no longer a forwarding stamp:
# it reads the upstream P5 verdict + carrier geometry and discriminates into
# ACCEPT / DEFER / BLOCK via the kernel's `فارق:` (block) / `defer:` (defer).
#   ACCEPT : P5 ACCEPT and verbal-signified carrier geometry — n_consonants >= 2
#            AND (nC>=3 with short-vowel cadence, OR gemination with nC>=2).
#   DEFER  : isolated word-unit support exists but verbal-carrier cadence is
#            underspecified (e.g. long-vowel-only CVVC nominal-looking units).
#   BLOCK  : P5 was DEFER/BLOCK (non-accepted upstream), or no vowel geometry.
SIGNIFIED_CLASS_CONFLICT = "signified_class_conflict"                # BLOCK (فارق)
VERBAL_SIGNIFIED_AMBIGUITY_BLOCKING = "verbal_signified_ambiguity_blocking"  # BLOCK (فارق)
VERBAL_CARRIER_UNDERSPECIFIED = "verbal_carrier_underspecified"      # DEFER (defer)

# Structural PRIORS P6 OPENS, never produces. These are *priors toward* meaning
# and dalalah — never MeaningCandidate / DalalahCandidate themselves.
OPENED_PRIORS = ("meaning_priors", "dalalah_priors")

VERBAL_SIGNIFIED_RULE = QiyasRule(
    rule_id="verbal_signified.open",
    layer="VerbalSignifiedQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="VerbalSignifiedDomain",
    far_type="MufradWordCandidate",
    required_effective_wasf=(
        "has_mufrad_word_candidate",
        "structural_signified_possibility_derived",
        "opens_meaning_priors",
        "opens_dalalah_priors",
        "mufrad_word_identity_preserved",
    ),
    required_illah=(
        "belongs_to_verbal_signified_domain",
        "verbal_signified_opening_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        SIGNIFIED_CLASS_CONFLICT,
        VERBAL_SIGNIFIED_AMBIGUITY_BLOCKING,
    ),
    neutral_identity_domain="verbal_signified_identity",
    output_candidate_type="VerbalSignifiedCandidate",
    forbidden_outputs=FORBIDDEN_VERBAL_SIGNIFIED,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
