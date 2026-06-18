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
        "signified_class_conflict",
        "verbal_signified_ambiguity_blocking",
    ),
    neutral_identity_domain="verbal_signified_identity",
    output_candidate_type="VerbalSignifiedCandidate",
    forbidden_outputs=FORBIDDEN_VERBAL_SIGNIFIED,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
