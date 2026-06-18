"""
Root Stem Rules — SCG-P3 (RootStemClosure).

The structural root/stem possibility rule:
  RegistryProjectionCandidate → RootStemCandidate

SCG-P3 closes a structural root/stem *POSSIBILITY* (إمكان جذر/ساق) from the
registry projection of slot geometry (ROOT_STEM_CLOSURE_CONSTITUTION.md). It is a
CANDIDATE-ONLY structural closure:

  - NOT final root extraction, NOT a root judgment (RootCandidate forbidden).
  - NOT wazn (WeightCandidate forbidden), NOT morphology, NOT wordhood.
  - NOT lexical meaning / dalalah / i'rab / hukm.

RootStemCandidate carries STRUCTURAL evidence only (registry_projection_ref,
slot_sequence_refs, structural_root_stem_signature, root_pattern_evidence,
stem_boundary_evidence) and preserves the slot_candidate identities. It OPENS
jamid/mushtaq + word-pattern PRIORS for SCG-P4; it never emits them.

Layer: RootStemQiyas
Input (far): RegistryProjectionCandidate
Output:      RootStemCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_ROOT_STEM
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# Structural priors P3 OPENS (as priors for SCG-P4), never produces.
OPENED_PRIORS = ("jamid_mushtaq_candidates", "word_pattern_candidates")

ROOT_STEM_RULE = QiyasRule(
    rule_id="root_stem.close",
    layer="RootStemQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="RootStemClosureDomain",
    far_type="RegistryProjectionCandidate",
    required_effective_wasf=(
        "has_registry_projection",
        "structural_root_stem_signature_derived",
        "has_slot_sequence_refs",
        "has_root_pattern_evidence",
        "has_stem_boundary_evidence",
        "slot_candidate_identities_preserved",
    ),
    required_illah=(
        "belongs_to_root_stem_closure_domain",
        "root_stem_closure_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        "root_pattern_conflict",
        "root_pattern_blocked",
    ),
    neutral_identity_domain="root_stem_identity",
    output_candidate_type="RootStemCandidate",
    forbidden_outputs=FORBIDDEN_ROOT_STEM,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
