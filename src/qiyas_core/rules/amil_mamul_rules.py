"""
Amil/Mamul Rules — SCG-P8 (AmilMamul).

The operator–operand relation-possibility rule:
  CompositionReadinessCandidate → AmilMamulCandidate

SCG-P8 answers ONLY: "which candidate dependency/attachment RELATIONS are
structurally admissible between already-produced verbal-signified candidates?"
(AMIL_MAMUL_CONSTITUTION.md). It is a CANDIDATE-ONLY structural relation:

  - NOT an actual i'rab / case judgment (IrabCandidate/CaseJudgment forbidden),
    NOT a grammatical/syntactic judgment, NOT meaning / dalalah / hukm / tafsir.

CRITICAL: `amil_mamul_prior_type` is a STRUCTURAL relation-geometry category,
NEVER a grammatical/case label — the i'rab judgment never leaks in here.

AmilMamulCandidate carries STRUCTURAL evidence only and preserves the upstream
identities. It OPENS grammatical-relation + i'rab PRIORS for SCG-P9+; it never
emits them.

Layer: AmilMamulQiyas
Input (far): CompositionReadinessCandidate
Output:      AmilMamulCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_AMIL_MAMUL
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Allowed STRUCTURAL relation-prior categories (SCG-P8 strengthening, 2026-06-18).
# Structural ONLY — never an actual i'rab/case/grammatical label (no Amil/Mamul/
# Marfu/Mansub/Subject/Object). The adapter SELECTS one input-dependently from the
# relation geometry it reads upstream.
RELATION_GEOMETRY_CLASS = "RelationGeometryClass"                  # multi-vowel skeleton (nC>=3, vowels==2)
STRUCTURAL_RELATION_PRIOR = "StructuralRelationPrior"             # minimal relation prior
RELATION_CADENCE_GEOMETRY_CLASS = "RelationCadenceGeometryClass"  # rich alternating skeleton (vowels>=3)
COMPACT_RELATION_POSSIBILITY = "CompactRelationPossibility"       # compact/geminated relation carrier
ALLOWED_AMIL_MAMUL_PRIOR_TYPES = (
    RELATION_GEOMETRY_CLASS,
    STRUCTURAL_RELATION_PRIOR,
    RELATION_CADENCE_GEOMETRY_CLASS,
    COMPACT_RELATION_POSSIBILITY,
)

# Relation-geometry verdict reasons. P8 is no longer a forwarding stamp: it reads
# the upstream P7 verdict + composition geometry and discriminates the RELATION
# possibility into ACCEPT / DEFER / BLOCK via the kernel's `فارق:` / `defer:`
# machinery. This stays RELATION-POSSIBILITY-only — never an actual i'rab/case.
#   ACCEPT : P7 ACCEPT and a multi-vowel alternating skeleton able to host an
#            operator–operand relation (n_consonants >= 3 AND cadence AND vowels >= 2).
#   DEFER  : P7-accepted operand whose relation geometry is too compact /
#            single-vowel to host a relation possibility (underspecified).
#   BLOCK  : P7 was DEFER/BLOCK (non-accepted upstream), or no usable geometry.
AMIL_CLASS_CONFLICT = "amil_class_conflict"                       # BLOCK (فارق)
AMIL_MAMUL_RELATION_BLOCKED = "amil_mamul_relation_blocked"       # BLOCK (فارق)
RELATION_GEOMETRY_UNDERSPECIFIED = "relation_geometry_underspecified"  # DEFER (defer)

# Structural PRIORS P8 OPENS (as priors for SCG-P9+), never produces.
OPENED_PRIORS = ("grammatical_relation_priors", "irab_priors")

AMIL_MAMUL_RULE = QiyasRule(
    rule_id="amil_mamul.relate",
    layer="AmilMamulQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="AmilMamulDomain",
    far_type="CompositionReadinessCandidate",
    required_effective_wasf=(
        "has_composition_readiness_candidate",
        "structural_relation_possibility_derived",
        "has_amil_mamul_prior_type",
        "opens_relation_priors",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_amil_mamul_domain",
        "amil_mamul_relation_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        AMIL_CLASS_CONFLICT,
        AMIL_MAMUL_RELATION_BLOCKED,
    ),
    neutral_identity_domain="amil_mamul_identity",
    output_candidate_type="AmilMamulCandidate",
    forbidden_outputs=FORBIDDEN_AMIL_MAMUL,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
