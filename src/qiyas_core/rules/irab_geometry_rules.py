"""
Irab Geometry Rules — SCG-P11 (IrabGeometry).

The i'rab-position-geometry possibility rule:
  RelationGeometryCandidate (accepted P10) → IrabGeometryCandidate

SCG-P11 reads an **accepted P10 RelationGeometryCandidate** and maps the geometry
of i'rab — the i'rab *positions and their possibilities* (المواضع الإعرابية
وإمكاناتها) — as a candidate-only structural geometry (إمكان موضع إعرابي), NOT an
i'rab judgment (IRAB_GEOMETRY_CONSTITUTION.md + SCG_P11 design gate / design
resolution).

THE JUDGMENT-ADJACENCY BOUNDARY (most judgment-adjacent layer in Saleh-):
  P11 names *where* i'rab could fall and *what* it could be — as geometry of
  possibilities. It must NEVER assert that a token *is* marfū'/manṣūb/majrūr/majzūm
  as a verdict. case_marker_evidence is NOT CaseJudgment; irab_position_evidence is
  NOT IrabFinalDecision. CaseJudgment / IrabFinalDecision / IfadahCandidate / hukm /
  reality / meaning / dalalah / final syntax label / any P12 candidate are forbidden.

It OPENS only `ifadah_speech_force_candidates` as a prior (ACCEPT only); it never
emits IfadahCandidate or any P12 object. It also CLOSES the `irab_geometry_candidates`
prior that P10 opened.

P11 does NOT re-prove relation geometry: it consumes a single accepted P10
candidate and refines i'rab-position geometry inside it (design resolution Q3).

Layer: IrabGeometryQiyas
Input (far): RelationGeometryCandidate (a single accepted P10 candidate)
Output:      IrabGeometryCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_IRAB_GEOMETRY
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Structural priors P11 OPENS (as priors for SCG-P12), never produces. [CANON —
# matches the P11 LayerSpec target_boundary_opens].
OPENED_PRIORS = ("ifadah_speech_force_candidates",)
# Prior P11 CLOSES (the one P10 opened). [CANON — P11 LayerSpec target_boundary_closes].
CLOSED_PRIORS = ("irab_geometry_candidates",)

# I'rab-geometry verdict reasons. P11 discriminates the i'rab-position geometry it
# reads from an accepted P10 relation geometry into ACCEPT / DEFER / BLOCK via the
# kernel's `فارق:` (block) / `defer:` (defer) machinery — never hardcoded all-pass.
#   ACCEPT : an accepted P10 relation geometry with closed i'rab context, structural
#            i'rab-position + case-marker + waqf-readiness evidence, identity
#            preserved → opens ifadah-speech-force priors. (positions, not a verdict)
#   DEFER  : relation geometry present but the i'rab geometry is under-determined.
#   BLOCK  : structural contradiction (no i'rab context, identity collapse,
#            i'rab-position conflict, or a forbidden-output attempt).
#
# [CANON] exact existing-spec names (used verbatim):
IRAB_CONTEXT_BLOCKED = "irab_context_blocked"                  # BLOCK (فارق) — spec blocker
IRAB_POSITION_CONFLICT = "irab_position_conflict"              # BLOCK (فارق) — spec invalidating_difference
# [DESIGN] ratified at the P11 implementation gate (mirrors the P9/P10 guards):
IDENTITY_COLLAPSE_BLOCKED = "identity_collapse_blocked"        # BLOCK (فارق)
FORBIDDEN_OUTPUT_ATTEMPTED = "forbidden_output_attempted"      # BLOCK (فارق)
IRAB_CONTEXT_UNDERSPECIFIED = "irab_context_underspecified"            # DEFER
IRAB_POSITION_UNDERSPECIFIED = "irab_position_underspecified"          # DEFER
CASE_MARKER_UNDERSPECIFIED = "case_marker_underspecified"              # DEFER
WAQF_READINESS_UNDERSPECIFIED = "waqf_readiness_underspecified"        # DEFER
CARRIED_RELATION_GEOMETRY_RESIDUALS = "carried_relation_geometry_residuals"  # DEFER
IRAB_IDENTITY_UNDERSPECIFIED = "irab_identity_underspecified"          # DEFER

DEFER_REASONS = (
    IRAB_CONTEXT_UNDERSPECIFIED,
    IRAB_POSITION_UNDERSPECIFIED,
    CASE_MARKER_UNDERSPECIFIED,
    WAQF_READINESS_UNDERSPECIFIED,
    CARRIED_RELATION_GEOMETRY_RESIDUALS,
    IRAB_IDENTITY_UNDERSPECIFIED,
)

IRAB_GEOMETRY_RULE = QiyasRule(
    rule_id="irab_geometry.compose",
    layer="IrabGeometryQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="IrabGeometryDomain",
    far_type="RelationGeometryCandidate",
    required_effective_wasf=(
        "has_relation_geometry_ref",
        "has_irab_position_evidence",
        "has_case_marker_evidence",
        "has_waqf_readiness_evidence",
        "irab_context_closed_present",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_irab_geometry_domain",
        "irab_geometry_composition_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        IRAB_CONTEXT_BLOCKED,
        IRAB_POSITION_CONFLICT,
        IDENTITY_COLLAPSE_BLOCKED,
        FORBIDDEN_OUTPUT_ATTEMPTED,
    ),
    neutral_identity_domain="irab_geometry_identity",
    output_candidate_type="IrabGeometryCandidate",
    forbidden_outputs=FORBIDDEN_IRAB_GEOMETRY,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
