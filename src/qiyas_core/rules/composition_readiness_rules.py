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

# Allowed STRUCTURAL composition-readiness prior types (SCG-P7 strengthening,
# 2026-06-18). Structural ONLY — never a final grammar/word-type/syntax judgment.
# The adapter SELECTS one input-dependently from the readiness geometry.
CADENCE_BOUNDARY_PRIOR = "CadenceBoundaryPrior"                       # clean cadence + closed boundary
COMPOSITION_READINESS_GEOMETRY_CLASS = "CompositionReadinessGeometryClass"  # rich cadence skeleton
GEMINATED_READINESS_POSSIBILITY = "GeminatedReadinessPossibility"    # gemination-bearing readiness
STRUCTURAL_READINESS_PRIOR = "StructuralReadinessPrior"              # minimal readiness
ALLOWED_COMPOSITION_READINESS_PRIOR_TYPES = (
    CADENCE_BOUNDARY_PRIOR,
    COMPOSITION_READINESS_GEOMETRY_CLASS,
    GEMINATED_READINESS_POSSIBILITY,
    STRUCTURAL_READINESS_PRIOR,
)

# Composition-readiness verdict reasons. P7 is no longer a forwarding stamp: it
# reads the upstream P6 verdict + carrier geometry and discriminates into
# ACCEPT / DEFER / BLOCK via the kernel's `فارق:` (block) / `defer:` (defer).
#   ACCEPT : P6 ACCEPT and a clean composition boundary — short-vowel cadence
#            AND n_consonants >= 3 (an unambiguous operand for composition).
#   DEFER  : P6-accepted carrier, but its composition boundary is ambiguous
#            (e.g. long-vowel-heavy / non-cadence shapes) — under-specified.
#   BLOCK  : P6 was DEFER/BLOCK (non-accepted upstream), or no usable geometry.
COMPOSITION_READINESS_CONFLICT = "composition_readiness_conflict"          # BLOCK (فارق)
COMPOSITION_PRECONDITION_BLOCKED = "composition_precondition_blocked"      # BLOCK (فارق)
COMPOSITION_READINESS_UNDERSPECIFIED = "composition_readiness_underspecified"  # DEFER (defer)

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
        COMPOSITION_READINESS_CONFLICT,
        COMPOSITION_PRECONDITION_BLOCKED,
    ),
    neutral_identity_domain="composition_readiness_identity",
    output_candidate_type="CompositionReadinessCandidate",
    forbidden_outputs=FORBIDDEN_COMPOSITION_READINESS,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
