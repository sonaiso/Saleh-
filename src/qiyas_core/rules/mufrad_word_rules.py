"""
Mufrad Word Rules — SCG-P5 (MufradWord).

The candidate-only wordhood rule:
  JamidMushtaqCandidate → MufradWordCandidate

SCG-P5 answers ONLY: "could this root/stem structure form a potential
single-word unit (إمكان كلمة مفردة)?" (MUFRAD_WORD_CONSTITUTION.md). It is a
CANDIDATE-ONLY structural wordhood contract:

  - NOT a final lexical word (WordCandidate forbidden), NOT a dictionary entry,
    NOT morphology, NOT grammar, NOT lexical meaning / dalalah / i'rab / hukm.

MufradWordCandidate carries STRUCTURAL wordhood evidence only
(jamid_mushtaq_candidate_ref, slot_sequence_refs, structural_word_boundary_evidence,
structural_wordhood_evidence) and preserves the upstream identities. It OPENS
verbal-signified + phrase-level PRIORS for SCG-P6; it never emits them.

Layer: MufradWordQiyas
Input (far): JamidMushtaqCandidate
Output:      MufradWordCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_MUFRAD_WORD
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Allowed STRUCTURAL word-unit prior categories (SCG-P5 strengthening, 2026-06-18).
# Structural ONLY — never a noun/verb/مفرد/singular/word judgment. The adapter
# SELECTS one input-dependently from the word-unit geometry it reads upstream.
STRUCTURAL_WORD_UNIT_PRIOR = "StructuralWordUnitPrior"        # minimal unit body
MUFRAD_UNIT_GEOMETRY_CLASS = "MufradUnitGeometryClass"        # multi-vowel body
ISOLATED_UNIT_BOUNDARY_PRIOR = "IsolatedUnitBoundaryPrior"    # closed-ending body
WORD_UNIT_SHAPE_POSSIBILITY = "WordUnitShapePossibility"      # gemination-bearing body
ALLOWED_MUFRAD_WORD_PRIOR_TYPES = (
    STRUCTURAL_WORD_UNIT_PRIOR,
    MUFRAD_UNIT_GEOMETRY_CLASS,
    ISOLATED_UNIT_BOUNDARY_PRIOR,
    WORD_UNIT_SHAPE_POSSIBILITY,
)

# Word-unit verdict reasons. P5 is no longer a forwarding stamp: it reads the
# upstream P4 verdict + word-unit geometry and discriminates into ACCEPT / DEFER
# / BLOCK via the kernel's existing `فارق:` (block) / `defer:` (defer) machinery.
#   ACCEPT : P4 ACCEPT and enough isolated-word-unit body (n_consonants >= 2 and
#            one of: >=2 vowels, closed ending, gemination).
#   DEFER  : word-unit geometry too thin to open an isolated unit.
#   BLOCK  : P4 was DEFER/BLOCK (non-accepted upstream), or geometry conflicts.
WORD_CLASS_CONFLICT = "word_class_conflict"                   # BLOCK (فارق)
WORD_TYPE_AMBIGUITY_BLOCKING = "word_type_ambiguity_blocking"  # BLOCK (فارق)
WORD_UNIT_UNDERSPECIFIED = "word_unit_underspecified"        # DEFER (defer)

# Structural priors P5 OPENS (as priors for SCG-P6), never produces.
OPENED_PRIORS = ("verbal_signified_candidates", "phrase_level_priors")

MUFRAD_WORD_RULE = QiyasRule(
    rule_id="mufrad_word.form",
    layer="MufradWordQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="MufradWordDomain",
    far_type="JamidMushtaqCandidate",
    required_effective_wasf=(
        "has_jamid_mushtaq_candidate",
        "structural_wordhood_evidence_derived",
        "has_structural_word_boundary_evidence",
        "has_slot_sequence_refs",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_mufrad_word_domain",
        "mufrad_word_formation_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        WORD_CLASS_CONFLICT,
        WORD_TYPE_AMBIGUITY_BLOCKING,
    ),
    neutral_identity_domain="mufrad_word_identity",
    output_candidate_type="MufradWordCandidate",
    forbidden_outputs=FORBIDDEN_MUFRAD_WORD,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
