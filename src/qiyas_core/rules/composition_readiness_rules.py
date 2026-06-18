"""
Composition Readiness Rules — SCG-P7 (CompositionReadiness).

The readiness-gate rule:
  VerbalSignifiedCandidate → CompositionReadinessCandidate

SCG-P7 answers ONLY: "is this verbal-signified unit structurally READY to enter
composition?" (COMPOSITION_READINESS_CONSTITUTION.md). It is a CANDIDATE-ONLY
readiness attestation:

  - It performs NO actual composition, NO syntax, NO amil/mamul relation,
    NO i'rab, NO meaning / dalalah / hukm.

CompositionReadinessCandidate carries STRUCTURAL evidence only
(verbal_signified_candidate_ref, slot_sequence_refs, composition_readiness_evidence,
structural_composability_profile) and preserves the upstream identities. It OPENS
amil/mamul + sentence-geometry PRIORS for SCG-P8/P9; it never emits them.

Layer: CompositionReadinessQiyas
Input (far): VerbalSignifiedCandidate
Output:      CompositionReadinessCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_COMPOSITION_READINESS
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Structural PRIORS P7 OPENS (as priors for SCG-P8/P9), never produces.
OPENED_PRIORS = ("amil_mamul_relation_priors", "sentence_geometry_priors")

COMPOSITION_READINESS_RULE = QiyasRule(
    rule_id="composition_readiness.attest",
    layer="CompositionReadinessQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="CompositionReadinessDomain",
    far_type="VerbalSignifiedCandidate",
    required_effective_wasf=(
        "has_verbal_signified_candidate",
        "structural_composability_profile_derived",
        "has_composition_readiness_evidence",
        "has_slot_sequence_refs",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_composition_readiness_domain",
        "composition_readiness_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "composition_readiness_conflict",
        "composition_precondition_blocked",
    ),
    neutral_identity_domain="composition_readiness_identity",
    output_candidate_type="CompositionReadinessCandidate",
    forbidden_outputs=FORBIDDEN_COMPOSITION_READINESS,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
