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
        "word_class_conflict",
        "word_type_ambiguity_blocking",
    ),
    neutral_identity_domain="mufrad_word_identity",
    output_candidate_type="MufradWordCandidate",
    forbidden_outputs=FORBIDDEN_MUFRAD_WORD,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
