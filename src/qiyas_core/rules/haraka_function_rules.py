"""
Haraka Function Rules — Gap #4 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

One canonical QiyasRule per Arabic haraka, proving vocalic function:
  FATHA → OPENING_FUNCTION
  DAMMA → ROUNDING_FUNCTION
  KASRA → FRONTING_FUNCTION
  SUKUN → CLOSURE_FUNCTION
  SHADDA → COMPRESSION_FUNCTION (GEMINATION)
  TANWIN variants → TANWIN_*_FUNCTION

Constitutional law:
  HarakaFunctionCarrier ⊬ CaseEffect
  HarakaFunctionCarrier ⊬ I'rab
  HarakaFunctionCarrier ⊬ Hukm

Layer: HarakaFunctionQiyas
Input (far): HarakaCodePoint
Output:      HarakaMarkIdentityCarrier  (canonical, REC-3 / SCG-P1 PR-1)

REC-3 / SCG-P1 PR-1 transitional-alias note: the canonical emitted candidate
type is ``HarakaMarkIdentityCarrier``. The legacy spelling
``HarakaFunctionCarrier`` survives only as a transitional alias (registry compat
constant + sibling forbidden_outputs) and is NOT the canonical runtime output.
This PR does not perform a coordinated rename across all consumers.
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_HARAKA_FUNCTION
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


def _make_haraka_rule(
    haraka_name: str,
    codepoint: int,
    vocalic_function: str,
    invalidating_diffs: tuple[str, ...],
) -> QiyasRule:
    cp_hex = f"{codepoint:04x}"
    return QiyasRule(
        rule_id=f"haraka_function.{haraka_name}",
        layer="HarakaFunctionQiyas",
        pattern=QiyasPattern.MEMBERSHIP,
        asl_type="HarakaFunctionDomain",
        far_type="HarakaCodePoint",
        required_effective_wasf=(
            "has_haraka_codepoint",
            f"has_unicode_identity:{cp_hex}",
            f"has_vocalic_function:{vocalic_function.lower()}",
        ),
        required_illah=(
            "belongs_to_haraka_function_domain",
            f"haraka_function_is:{haraka_name}",
        ),
        required_wadi_gates=_ALL_WADI,
        invalidating_differences=invalidating_diffs,
        neutral_identity_domain="haraka_identity",
        output_candidate_type="HarakaMarkIdentityCarrier",
        forbidden_outputs=FORBIDDEN_HARAKA_FUNCTION,
        rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
    )


# ---------------------------------------------------------------------------
# Rules for each haraka
# ---------------------------------------------------------------------------

FATHA_FUNCTION_RULE = _make_haraka_rule(
    "fatha", 0x064E, "OPENING_FUNCTION",
    ("fatha_vs_damma", "fatha_vs_kasra"),
)

DAMMA_FUNCTION_RULE = _make_haraka_rule(
    "damma", 0x064F, "ROUNDING_FUNCTION",
    ("damma_vs_fatha", "damma_vs_kasra"),
)

KASRA_FUNCTION_RULE = _make_haraka_rule(
    "kasra", 0x0650, "FRONTING_FUNCTION",
    ("kasra_vs_fatha", "kasra_vs_damma"),
)

SUKUN_FUNCTION_RULE = _make_haraka_rule(
    "sukun", 0x0652, "CLOSURE_FUNCTION",
    ("sukun_vs_fatha", "sukun_vs_shadda"),
)

SHADDA_FUNCTION_RULE = _make_haraka_rule(
    "shadda", 0x0651, "COMPRESSION_FUNCTION",
    ("shadda_vs_sukun", "shadda_vs_fatha"),
)

TANWIN_FATH_FUNCTION_RULE = _make_haraka_rule(
    "tanwin_fath", 0x064B, "TANWIN_OPEN_FUNCTION",
    ("tanwin_fath_vs_tanwin_damm", "tanwin_fath_vs_fatha"),
)

TANWIN_DAMM_FUNCTION_RULE = _make_haraka_rule(
    "tanwin_damm", 0x064C, "TANWIN_ROUND_FUNCTION",
    ("tanwin_damm_vs_tanwin_fath", "tanwin_damm_vs_damma"),
)

TANWIN_KASR_FUNCTION_RULE = _make_haraka_rule(
    "tanwin_kasr", 0x064D, "TANWIN_FRONT_FUNCTION",
    ("tanwin_kasr_vs_tanwin_fath", "tanwin_kasr_vs_kasra"),
)


# ---------------------------------------------------------------------------
# Map: codepoint → rule
# ---------------------------------------------------------------------------

HARAKA_FUNCTION_RULES: dict[int, QiyasRule] = {
    0x064B: TANWIN_FATH_FUNCTION_RULE,
    0x064C: TANWIN_DAMM_FUNCTION_RULE,
    0x064D: TANWIN_KASR_FUNCTION_RULE,
    0x064E: FATHA_FUNCTION_RULE,
    0x064F: DAMMA_FUNCTION_RULE,
    0x0650: KASRA_FUNCTION_RULE,
    0x0651: SHADDA_FUNCTION_RULE,
    0x0652: SUKUN_FUNCTION_RULE,
}


def get_haraka_function_rule(codepoint: int) -> QiyasRule | None:
    """Return the HarakaFunctionQiyas rule for the given haraka codepoint."""
    return HARAKA_FUNCTION_RULES.get(codepoint)
