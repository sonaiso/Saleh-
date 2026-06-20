"""
Sentence Geometry Rules — SCG-P9 (SentenceGeometry).

The multi-unit sentence-geometry possibility rule:
  AmilMamulCandidate (≥2 word/segment-level units) → SentenceGeometryCandidate

SCG-P9 is the FIRST multi-unit layer. It organizes عامل–معمول relation candidates
from **distinct word/segment-level units** into a candidate-only **sentence
geometry** (إمكان هندسة جملية) — a structural spatial arrangement, NOT a
grammatical ruling (SENTENCE_GEOMETRY_CONSTITUTION.md + the SCG-P9 design gate /
design resolution).

CANDIDATE-ONLY and STRUCTURAL-ONLY:
  - NOT an i'rab / case judgment (IrabCandidate / CaseJudgment forbidden), NOT
    ifadah (IfadahCandidate forbidden), NOT meaning / dalalah / final syntax label
    / hukm / reality / final meaning, NOT any downstream (P10+) candidate.

It OPENS only `relation_geometry_candidates` as a prior (ACCEPT only); it never
emits RelationGeometryCandidate or any P10+ object.

Layer: SentenceGeometryQiyas
Input (far): AmilMamulCandidate (a collection of ≥2 unit-level accepted traces)
Output:      SentenceGeometryCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_SENTENCE_GEOMETRY
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Structural priors P9 OPENS (as priors for SCG-P10), never produces. [CANON —
# matches the P9 LayerSpec target_boundary_opens].
OPENED_PRIORS = ("relation_geometry_candidates",)

# Sentence-geometry verdict reasons. P9 discriminates the multi-unit geometry it
# reads from ≥2 accepted P8 units into ACCEPT / DEFER / BLOCK via the kernel's
# `فارق:` (block) / `defer:` (defer) machinery — never hardcoded all-pass.
#   ACCEPT : ≥2 distinct word/segment units, structurally-licensed adjacency, a
#            closed sentence-geometry boundary → opens relation-geometry priors.
#   DEFER  : ≥2 units but the multi-unit geometry is under-determined.
#   BLOCK  : structural contradiction (e.g. <2 distinct units, identity collapse,
#            sentence-type conflict, or a forbidden-output attempt).
#
# [CANON] exact existing-spec names (used verbatim):
SENTENCE_STRUCTURE_BLOCKED = "sentence_structure_blocked"        # BLOCK (فارق)
SENTENCE_TYPE_CONFLICT = "sentence_type_conflict"                # BLOCK (فارق)
# [DESIGN] ratified at the P9 implementation gate:
IDENTITY_COLLAPSE_BLOCKED = "identity_collapse_blocked"          # BLOCK (فارق)
FORBIDDEN_OUTPUT_ATTEMPTED = "forbidden_output_attempted"        # BLOCK (فارق)
ADJACENCY_UNDERSPECIFIED = "adjacency_underspecified"            # DEFER
SENTENCE_BOUNDARY_UNDERSPECIFIED = "sentence_boundary_underspecified"  # DEFER
RELATION_COVERAGE_UNDERSPECIFIED = "relation_coverage_underspecified"  # DEFER
CARRIED_UPSTREAM_RESIDUALS = "carried_upstream_residuals"        # DEFER
IDENTITY_JOIN_UNDERSPECIFIED = "identity_join_underspecified"    # DEFER

DEFER_REASONS = (
    ADJACENCY_UNDERSPECIFIED,
    SENTENCE_BOUNDARY_UNDERSPECIFIED,
    RELATION_COVERAGE_UNDERSPECIFIED,
    CARRIED_UPSTREAM_RESIDUALS,
    IDENTITY_JOIN_UNDERSPECIFIED,
)

SENTENCE_GEOMETRY_RULE = QiyasRule(
    rule_id="sentence_geometry.compose",
    layer="SentenceGeometryQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="SentenceGeometryDomain",
    far_type="AmilMamulCandidate",
    required_effective_wasf=(
        "has_amil_mamul_refs",
        "has_sentence_type_evidence",
        "has_isnad_boundary_evidence",
        "multi_unit_geometry_present",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_sentence_geometry_domain",
        "sentence_geometry_composition_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        SENTENCE_STRUCTURE_BLOCKED,
        SENTENCE_TYPE_CONFLICT,
        IDENTITY_COLLAPSE_BLOCKED,
        FORBIDDEN_OUTPUT_ATTEMPTED,
    ),
    neutral_identity_domain="sentence_geometry_identity",
    output_candidate_type="SentenceGeometryCandidate",
    forbidden_outputs=FORBIDDEN_SENTENCE_GEOMETRY,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
