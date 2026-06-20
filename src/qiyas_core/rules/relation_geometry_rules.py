"""
Relation Geometry Rules — SCG-P10 (RelationGeometry).

The internal-relation-geometry possibility rule:
  SentenceGeometryCandidate (accepted P9) → RelationGeometryCandidate

SCG-P10 reads an **accepted P9 SentenceGeometryCandidate** and maps the internal
relations between its sentence components — تبعية، عطف، إبدال، توكيد — as a
candidate-only **relation geometry** (إمكان هندسة علاقات), a structural spatial
arrangement, NOT a grammatical ruling (RELATION_GEOMETRY_CONSTITUTION.md +
SCG_P10 design gate / design resolution).

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT an i'rab / case judgment (IrabCandidate / CaseJudgment forbidden), NOT
    ifadah (IfadahCandidate forbidden), NOT meaning / dalalah / final syntax label
    / hukm / reality / final meaning, NOT any downstream (P11+) candidate.

It OPENS only `irab_geometry_candidates` as a prior (ACCEPT only); it never emits
IrabGeometryCandidate or any P11+ object. It also CLOSES the
`relation_geometry_candidates` prior that P9 opened.

P10 does NOT re-prove sentencehood: the multi-unit requirement is already enforced
at P9. P10 refines relation geometry **inside** an accepted sentence geometry, and
requires at least **one** accepted P9 SentenceGeometryCandidate (design
resolution Q3).

Layer: RelationGeometryQiyas
Input (far): SentenceGeometryCandidate (a single accepted P9 candidate)
Output:      RelationGeometryCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_RELATION_GEOMETRY
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Structural priors P10 OPENS (as priors for SCG-P11), never produces. [CANON —
# matches the P10 LayerSpec target_boundary_opens].
OPENED_PRIORS = ("irab_geometry_candidates",)
# Prior P10 CLOSES (the one P9 opened). [CANON — P10 LayerSpec target_boundary_closes].
CLOSED_PRIORS = ("relation_geometry_candidates",)

# Relation-geometry verdict reasons. P10 discriminates the relation geometry it
# reads from an accepted P9 sentence geometry into ACCEPT / DEFER / BLOCK via the
# kernel's `فارق:` (block) / `defer:` (defer) machinery — never hardcoded all-pass.
#   ACCEPT : an accepted P9 sentence geometry with closed relation scope,
#            structural relation-type evidence, and dependency-scope evidence,
#            with the multi-unit identity preserved → opens irab-geometry priors.
#   DEFER  : sentence geometry present but the relation geometry is under-determined.
#   BLOCK  : structural contradiction (no relation structure, identity collapse,
#            relation-type conflict, or a forbidden-output attempt).
#
# [CANON] exact existing-spec names (used verbatim):
RELATION_STRUCTURE_BLOCKED = "relation_structure_blocked"        # BLOCK (فارق) — spec blocker
RELATION_TYPE_CONFLICT = "relation_type_conflict"                # BLOCK (فارق) — spec invalidating_difference
# [DESIGN] ratified at the P10 implementation gate (mirrors the P9 guards):
IDENTITY_COLLAPSE_BLOCKED = "identity_collapse_blocked"          # BLOCK (فارق)
FORBIDDEN_OUTPUT_ATTEMPTED = "forbidden_output_attempted"        # BLOCK (فارق)
RELATION_SCOPE_UNDERSPECIFIED = "relation_scope_underspecified"          # DEFER
RELATION_TYPE_UNDERSPECIFIED = "relation_type_underspecified"            # DEFER
DEPENDENCY_SCOPE_UNDERSPECIFIED = "dependency_scope_underspecified"      # DEFER
CARRIED_SENTENCE_GEOMETRY_RESIDUALS = "carried_sentence_geometry_residuals"  # DEFER
RELATION_IDENTITY_UNDERSPECIFIED = "relation_identity_underspecified"    # DEFER

DEFER_REASONS = (
    RELATION_SCOPE_UNDERSPECIFIED,
    RELATION_TYPE_UNDERSPECIFIED,
    DEPENDENCY_SCOPE_UNDERSPECIFIED,
    CARRIED_SENTENCE_GEOMETRY_RESIDUALS,
    RELATION_IDENTITY_UNDERSPECIFIED,
)

RELATION_GEOMETRY_RULE = QiyasRule(
    rule_id="relation_geometry.compose",
    layer="RelationGeometryQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="RelationGeometryDomain",
    far_type="SentenceGeometryCandidate",
    required_effective_wasf=(
        "has_sentence_geometry_ref",
        "has_relation_type_evidence",
        "has_dependency_scope_evidence",
        "relation_scope_closed_present",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_relation_geometry_domain",
        "relation_geometry_composition_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        RELATION_STRUCTURE_BLOCKED,
        RELATION_TYPE_CONFLICT,
        IDENTITY_COLLAPSE_BLOCKED,
        FORBIDDEN_OUTPUT_ATTEMPTED,
    ),
    neutral_identity_domain="relation_geometry_identity",
    output_candidate_type="RelationGeometryCandidate",
    forbidden_outputs=FORBIDDEN_RELATION_GEOMETRY,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
