"""
Ifadah Speech-Force Rules — SCG-P12 (IfadahSpeechForce). TERMINAL layer.

The ifadah (speech-force) possibility rule:
  IrabGeometryCandidate (accepted P11) → IfadahCandidate

SCG-P12 reads an **accepted P11 IrabGeometryCandidate** and builds an **ifadah
(speech-force) possibility** — خبر / إنشاء / طلب — as a candidate-only speech-force
hypothesis (إمكان إفادة كلامية), the END of the structural spine
(IFADAH_CONSTITUTION.md + SCG-P11 design gate / design resolution).

THE HUKM/REALITY FRONTIER (the hardest boundary in Saleh-):
  "Ifadah" here is the *structural possibility* that an utterance carries a speech
  force — NOT a decision of truth, NOT a reality claim, NOT a hukm, NOT a final
  meaning. Saleh- stops at *licensed structural possibility*; it never crosses into
  reality, truth, or hukm. HukmCandidate / RealityClaim / RealityMapping /
  TruthJudgment / FinalMeaning / IrabFinalDecision are all forbidden, and the
  changes assign_reality_claim / assign_truth_value / assign_hukm are blocked.

TERMINAL: target_boundary_opens = () — P12 opens NO successor phase. It only CLOSES
the `ifadah_candidates` prior that P11 opened. There is no P13.

P12 does NOT re-prove i'rab geometry: it consumes a single accepted P11 candidate
and builds the speech-force possibility inside it.

Layer: IfadahSpeechForceQiyas
Input (far): IrabGeometryCandidate (a single accepted P11 candidate)
Output:      IfadahCandidate
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_IFADAH
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)

# P12 is TERMINAL — it OPENS nothing (matches the P12 LayerSpec target_boundary_opens=()).
OPENED_PRIORS: tuple[str, ...] = ()
# Prior P12 CLOSES (the one P11 opened). [CANON — P12 LayerSpec target_boundary_closes].
CLOSED_PRIORS = ("ifadah_candidates",)

# Ifadah-speech-force verdict reasons. P12 discriminates the speech-force possibility
# it reads from an accepted P11 i'rab geometry into ACCEPT / DEFER / BLOCK via the
# kernel's `فارق:` (block) / `defer:` (defer) machinery — never hardcoded all-pass.
#   ACCEPT : an accepted P11 i'rab geometry with closed ifadah context, structural
#            speech-force + ifadah-boundary + mukhatab-context evidence, identity
#            preserved → an ifadah POSSIBILITY (not a reality/truth/hukm claim).
#   DEFER  : i'rab geometry present but the speech-force possibility is under-determined.
#   BLOCK  : structural contradiction (no ifadah precondition, identity collapse,
#            speech-force conflict, a forbidden-output attempt, or a final-judgment
#            attempt — the reality/truth/hukm frontier guard).
#
# [CANON] exact existing-spec names (used verbatim):
IFADAH_PRECONDITION_BLOCKED = "ifadah_precondition_blocked"          # BLOCK (فارق) — spec blocker
SPEECH_FORCE_CONFLICT = "speech_force_conflict"                      # BLOCK (فارق) — spec invalidating_difference
# [DESIGN] ratified at the P12 implementation gate (mirrors the P9/P10/P11 guards):
IDENTITY_COLLAPSE_BLOCKED = "identity_collapse_blocked"              # BLOCK (فارق)
FORBIDDEN_OUTPUT_ATTEMPTED = "forbidden_output_attempted"            # BLOCK (فارق)
FINAL_JUDGMENT_ATTEMPTED = "final_judgment_attempted"                # BLOCK (فارق) — frontier guard
IFADAH_CONTEXT_UNDERSPECIFIED = "ifadah_context_underspecified"              # DEFER
SPEECH_FORCE_READINESS_UNDERSPECIFIED = "speech_force_readiness_underspecified"  # DEFER
COMPLETION_BOUNDARY_UNDERSPECIFIED = "completion_boundary_underspecified"    # DEFER
CARRIED_IRAB_GEOMETRY_RESIDUALS = "carried_irab_geometry_residuals"          # DEFER
IFADAH_IDENTITY_UNDERSPECIFIED = "ifadah_identity_underspecified"            # DEFER

DEFER_REASONS = (
    IFADAH_CONTEXT_UNDERSPECIFIED,
    SPEECH_FORCE_READINESS_UNDERSPECIFIED,
    COMPLETION_BOUNDARY_UNDERSPECIFIED,
    CARRIED_IRAB_GEOMETRY_RESIDUALS,
    IFADAH_IDENTITY_UNDERSPECIFIED,
)

IFADAH_RULE = QiyasRule(
    rule_id="ifadah_speech_force.compose",
    layer="IfadahSpeechForceQiyas",
    pattern=QiyasPattern.MEMBERSHIP,
    asl_type="IfadahSpeechForceDomain",
    far_type="IrabGeometryCandidate",
    required_effective_wasf=(
        "has_irab_geometry_ref",
        "has_speech_force_evidence",
        "has_ifadah_boundary_evidence",
        "has_mukhatab_context_evidence",
        "ifadah_context_closed_present",
        "upstream_identity_preserved",
    ),
    required_illah=(
        "belongs_to_ifadah_speech_force_domain",
        "ifadah_speech_force_composition_licensed",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        IFADAH_PRECONDITION_BLOCKED,
        SPEECH_FORCE_CONFLICT,
        IDENTITY_COLLAPSE_BLOCKED,
        FORBIDDEN_OUTPUT_ATTEMPTED,
        FINAL_JUDGMENT_ATTEMPTED,
    ),
    neutral_identity_domain="ifadah_speech_force_identity",
    output_candidate_type="IfadahCandidate",
    forbidden_outputs=FORBIDDEN_IFADAH,
    rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
)
