"""
Haraka Role Spectrum Rules — Γ_haraka (Gamma-haraka) spectrum-opening function.

Constitutional contract: docs/qiyas_core/HARAKA_ROLE_SPECTRUM_CONTRACT.md

This module implements the QiyasRules for Γ_haraka, the spectrum-opening
function that produces role hypotheses for haraka carriers.

**Phase 3 scope (this PR):**
  ✓ HARAKA_ROLE_SPECTRUM_RULE
  ✓ Hypothesis generation logic
  ✓ Constitutional constraints enforcement
  ✓ Forbidden outputs declaration

**Constitutional principle:**
  Γ ≠ Λ
  Γ = Spectrum opener (hypothesis generator)
  Λ = Selector (context-dependent chooser, FUTURE)

  Γ produces POTENTIAL roles only.
  Γ does NOT produce SELECTED roles.
  Γ does NOT produce FINAL judgments.

**Layer:** HarakaRoleSpectrumQiyas
**Input (far):** SlotCandidate (with HarakaFunctionCarrier)
**Output:** HarakaRoleSpectrum
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule

# Constitutional forbidden outputs (§ 4.1 of contract)
FORBIDDEN_HARAKA_ROLE_SPECTRUM = (
    "WeightCandidate",  # Wazn
    "CaseEffect",  # I'rab
    "Irab",
    "ArudCandidate",  # 'Arūḍ
    "FinalFunction",
    "FinalMeaning",
    "HukmCandidate",
    "RealityClaim",
    "SelectedRole",  # Final role selection
    "DeterminedFunction",  # Final function determination
    "FinalCaseJudgment",
    "FinalPattern",
    "FinalMeterJudgment",
    "FinalSyllable",
    "FinalMorphologicalJudgment",
    "FinalIdafaJudgment",
    "FinalWaqfJudgment",
)

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


# ---------------------------------------------------------------------------
# Main Spectrum Generation Rule
# ---------------------------------------------------------------------------

HARAKA_ROLE_SPECTRUM_RULE = QiyasRule(
    rule_id="haraka_role_spectrum.gamma_haraka",
    layer="HarakaRoleSpectrumQiyas",
    pattern=QiyasPattern.OPENING,  # Spectrum opener
    asl_type="HarakaRoleDomain",
    far_type="SlotCandidate",
    required_effective_wasf=(
        "has_haraka_carrier",
        "has_position_context",
        "has_alignment_evidence",
        "identity_preserved",
    ),
    required_illah=(
        "belongs_to_haraka_role_domain",
        "spectrum_generation_valid",
    ),
    required_wadi_gates=_ALL_WADI,
    invalidating_differences=(
        # These would block spectrum generation
        "missing_haraka_carrier",
        "missing_position_context",
        "missing_alignment_evidence",
        "identity_not_preserved",
    ),
    neutral_identity_domain="haraka_role_spectrum_identity",
    output_candidate_type="HarakaRoleSpectrum",
    forbidden_outputs=FORBIDDEN_HARAKA_ROLE_SPECTRUM,
    rank_ceiling=EvidenceRank.ANALOGICAL,  # Constitutional requirement § 2.2
)
