"""
Registry Projection Rules — SCG-P2 (RegistryProjection).

The first post-slot projection rule:
  SlotCandidate → RegistryProjectionCandidate

SCG-P2 answers ONE question (REGISTRY_PROJECTION_CONSTITUTION.md §§9–12):
  "To which registered STRUCTURAL membership class(es) could this slot geometry
   belong?"  — a projection of slot geometry onto registry membership classes.

It is NOT root / wazn / word / meaning / i'rab / hukm. It carries:
  - registry_entry_ref      a canonical structural signature derived from the
                            SlotCandidate geometry (no coined class names; no
                            named registry is introduced).
  - membership_prior_type   a structural registry category (e.g.
                            GeometryMembershipClass) — NEVER a linguistic
                            category (Verb/Noun/Derived/Jamid/Root/Wazn).

It OPENS root/stem + word-type PRIORS; it never emits RootStemCandidate or any
downstream / semantic output (FORBIDDEN_REGISTRY_PROJECTION).

Layer: RegistryProjectionQiyas
Input (far): SlotCandidate
Output:      RegistryProjectionCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_REGISTRY_PROJECTION
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Allowed structural membership-prior categories (structural ONLY — never a
# linguistic/morphological label). The adapter must use one of these.
GEOMETRY_MEMBERSHIP_CLASS = "GeometryMembershipClass"
STRUCTURAL_MEMBERSHIP_PRIOR = "StructuralMembershipPrior"
ALLOWED_MEMBERSHIP_PRIOR_TYPES = (
    GEOMETRY_MEMBERSHIP_CLASS,
    STRUCTURAL_MEMBERSHIP_PRIOR,
)

# The structural priors P2 OPENS (as priors for SCG-P3), never produces.
OPENED_PRIORS = ("root_stem_candidates", "word_type_priors")

REGISTRY_PROJECTION_RULE = QiyasRule(
    rule_id="registry_projection.project",
    layer="RegistryProjectionQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="RegistryProjectionDomain",
    far_type="SlotCandidate",
    required_effective_wasf=(
        "has_slot_candidate",
        "structural_signature_derived",
        "has_registry_entry_ref",
        "has_membership_prior_type",
        "slot_candidate_identity_preserved",
    ),
    required_illah=(
        "belongs_to_registry_projection_domain",
        "registry_projection_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "registry_membership_conflict",
        "slot_candidate_blocked",
    ),
    neutral_identity_domain="registry_projection_identity",
    output_candidate_type="RegistryProjectionCandidate",
    forbidden_outputs=FORBIDDEN_REGISTRY_PROJECTION,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
