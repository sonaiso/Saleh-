"""
Letter Identity Rules

Constitutional rules for proving atomic letter identities (BAA, TAA, SEEN, etc.)
from LetterCodePoint. This is an independent atomic path that does NOT require
sequence context or ConditionedTypedSequence.

Architecture:
    TypedCodePoint (if LetterCodePoint)
      ↓
    LetterIdentityCarrier(BAA | TAA | SEEN | ...)

Forbidden: This layer does NOT produce SlotCandidate or require sequence validation.
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule


ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


# Forbidden outputs: LetterIdentityCarrier is atomic, not compositional
FORBIDDEN_LETTER_IDENTITY_OUTPUTS = (
    "SlotCandidate",
    "SlotGeometry",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "FormCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "IfadahCandidate",
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
)


# ---------------------------------------------------------------------------
# Helper to build a per-letter rule (Option C - Layer 1: Pure Identity Only)
# ---------------------------------------------------------------------------

def _make_letter_identity_rule(
    letter_name: str,
    codepoint: int,
    arabic_name: str,
) -> QiyasRule:
    """
    Build a pure identity rule for a letter (Option C - Layer 1).

    Requires ONLY identity wasf/illah:
      - Unicode identity
      - Script identity
      - Name identity (Latin + Arabic)
      - Specific letter identity

    Does NOT require (moved to ArabicLetterCoordinateCarrier - Layer 2):
      - Sound identity
      - Makhraj
      - Sifat
      - Invalidating differences (fariq)

    Args:
        letter_name: Lowercase Latin letter name (e.g., "baa", "taa")
        codepoint: Unicode codepoint
        arabic_name: Arabic name (e.g., "باء", "تاء")
    """
    cp_hex = f"{codepoint:04x}"
    return QiyasRule(
        rule_id=f"letter_identity.{letter_name}",
        layer="LetterIdentityQiyas",
        pattern=QiyasPattern.MEMBERSHIP,
        asl_type="LetterIdentityDomain",
        far_type="LetterCodePoint",
        required_effective_wasf=(
            "has_letter_codepoint",
            f"has_unicode_identity:{cp_hex}",
            f"has_script_identity:{letter_name}",
            f"has_latin_name:{letter_name}",
            f"has_arabic_name:{arabic_name}",
        ),
        required_illah=(
            "belongs_to_letter_identity_domain",
            f"letter_identity_is:{letter_name}",
        ),
        required_wadi_gates=ALL_WADI,
        invalidating_differences=(),  # Moved to Layer 2
        neutral_identity_domain="letter_identity",
        output_candidate_type="LetterIdentityCarrier",
        forbidden_outputs=FORBIDDEN_LETTER_IDENTITY_OUTPUTS,
        rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
    )


# ---------------------------------------------------------------------------
# All Arabic letter identity rules (Option C - Layer 1: Pure Identity)
# Generated using simplified helper - no phonetic/makhraj in Layer 1
# ---------------------------------------------------------------------------

HAMZA_IDENTITY_RULE = _make_letter_identity_rule(
    "hamza", 0x0621, "همزة",
)

ALEF_MADDA_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_madda", 0x0622, "ألف ممدودة",
)

ALEF_HAMZA_ABOVE_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_hamza_above", 0x0623, "ألف بهمزة فوق",
)

WAW_HAMZA_IDENTITY_RULE = _make_letter_identity_rule(
    "waw_hamza", 0x0624, "واو بهمزة",
)

ALEF_HAMZA_BELOW_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_hamza_below", 0x0625, "ألف بهمزة تحت",
)

YEH_HAMZA_IDENTITY_RULE = _make_letter_identity_rule(
    "yeh_hamza", 0x0626, "ياء بهمزة",
)

ALEF_IDENTITY_RULE = _make_letter_identity_rule(
    "alef", 0x0627, "ألف",
)

BAA_IDENTITY_RULE = _make_letter_identity_rule(
    "baa", 0x0628, "باء",
)

TEH_MARBUTA_IDENTITY_RULE = _make_letter_identity_rule(
    "teh_marbuta", 0x0629, "تاء مربوطة",
)

TAA_IDENTITY_RULE = _make_letter_identity_rule(
    "taa", 0x062A, "تاء",
)

THAA_IDENTITY_RULE = _make_letter_identity_rule(
    "thaa", 0x062B, "ثاء",
)

JEEM_IDENTITY_RULE = _make_letter_identity_rule(
    "jeem", 0x062C, "جيم",
)

HAA_IDENTITY_RULE = _make_letter_identity_rule(
    "haa", 0x062D, "حاء",
)

KHAA_IDENTITY_RULE = _make_letter_identity_rule(
    "khaa", 0x062E, "خاء",
)

DAL_IDENTITY_RULE = _make_letter_identity_rule(
    "dal", 0x062F, "دال",
)

DHAL_IDENTITY_RULE = _make_letter_identity_rule(
    "thaal", 0x0630, "ذال",
)

RAA_IDENTITY_RULE = _make_letter_identity_rule(
    "raa", 0x0631, "راء",
)

ZAY_IDENTITY_RULE = _make_letter_identity_rule(
    "zay", 0x0632, "زاي",
)

SEEN_IDENTITY_RULE = _make_letter_identity_rule(
    "seen", 0x0633, "سين",
)

SHEEN_IDENTITY_RULE = _make_letter_identity_rule(
    "sheen", 0x0634, "شين",
)

SAAD_IDENTITY_RULE = _make_letter_identity_rule(
    "saad", 0x0635, "صاد",
)

DAAD_IDENTITY_RULE = _make_letter_identity_rule(
    "daad", 0x0636, "ضاد",
)

TAA_EMPHATIC_IDENTITY_RULE = _make_letter_identity_rule(
    "taa_emphatic", 0x0637, "طاء",
)

DHAA_IDENTITY_RULE = _make_letter_identity_rule(
    "dhaa", 0x0638, "ظاء",
)

AYN_IDENTITY_RULE = _make_letter_identity_rule(
    "ayn", 0x0639, "عين",
)

GHAYN_IDENTITY_RULE = _make_letter_identity_rule(
    "ghayn", 0x063A, "غين",
)

TATWEEL_IDENTITY_RULE = _make_letter_identity_rule(
    "tatweel", 0x0640, "تطويل",
)

FAA_IDENTITY_RULE = _make_letter_identity_rule(
    "faa", 0x0641, "فاء",
)

QAF_IDENTITY_RULE = _make_letter_identity_rule(
    "qaf", 0x0642, "قاف",
)

KAF_IDENTITY_RULE = _make_letter_identity_rule(
    "kaf", 0x0643, "كاف",
)

LAM_IDENTITY_RULE = _make_letter_identity_rule(
    "lam", 0x0644, "لام",
)

MEEM_IDENTITY_RULE = _make_letter_identity_rule(
    "meem", 0x0645, "ميم",
)

NOON_IDENTITY_RULE = _make_letter_identity_rule(
    "noon", 0x0646, "نون",
)

HAA_FINAL_IDENTITY_RULE = _make_letter_identity_rule(
    "haa_final", 0x0647, "هاء",
)

WAW_IDENTITY_RULE = _make_letter_identity_rule(
    "waw", 0x0648, "واو",
)

ALEF_MAKSURA_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_maksura", 0x0649, "ألف مقصورة",
)

YAA_IDENTITY_RULE = _make_letter_identity_rule(
    "yaa", 0x064A, "ياء",
)

# ---------------------------------------------------------------------------
# Map: codepoint → rule
# ---------------------------------------------------------------------------

LETTER_IDENTITY_RULES: dict[int, QiyasRule] = {
    0x0621: HAMZA_IDENTITY_RULE,
    0x0622: ALEF_MADDA_IDENTITY_RULE,
    0x0623: ALEF_HAMZA_ABOVE_IDENTITY_RULE,
    0x0624: WAW_HAMZA_IDENTITY_RULE,
    0x0625: ALEF_HAMZA_BELOW_IDENTITY_RULE,
    0x0626: YEH_HAMZA_IDENTITY_RULE,
    0x0627: ALEF_IDENTITY_RULE,
    0x0628: BAA_IDENTITY_RULE,
    0x0629: TEH_MARBUTA_IDENTITY_RULE,
    0x062A: TAA_IDENTITY_RULE,
    0x062B: THAA_IDENTITY_RULE,
    0x062C: JEEM_IDENTITY_RULE,
    0x062D: HAA_IDENTITY_RULE,
    0x062E: KHAA_IDENTITY_RULE,
    0x062F: DAL_IDENTITY_RULE,
    0x0630: DHAL_IDENTITY_RULE,
    0x0631: RAA_IDENTITY_RULE,
    0x0632: ZAY_IDENTITY_RULE,
    0x0633: SEEN_IDENTITY_RULE,
    0x0634: SHEEN_IDENTITY_RULE,
    0x0635: SAAD_IDENTITY_RULE,
    0x0636: DAAD_IDENTITY_RULE,
    0x0637: TAA_EMPHATIC_IDENTITY_RULE,
    0x0638: DHAA_IDENTITY_RULE,
    0x0639: AYN_IDENTITY_RULE,
    0x063A: GHAYN_IDENTITY_RULE,
    0x0640: TATWEEL_IDENTITY_RULE,
    0x0641: FAA_IDENTITY_RULE,
    0x0642: QAF_IDENTITY_RULE,
    0x0643: KAF_IDENTITY_RULE,
    0x0644: LAM_IDENTITY_RULE,
    0x0645: MEEM_IDENTITY_RULE,
    0x0646: NOON_IDENTITY_RULE,
    0x0647: HAA_FINAL_IDENTITY_RULE,
    0x0648: WAW_IDENTITY_RULE,
    0x0649: ALEF_MAKSURA_IDENTITY_RULE,
    0x064A: YAA_IDENTITY_RULE,
}


def get_letter_identity_rule(codepoint: int) -> QiyasRule | None:
    """Return the LetterIdentityQiyas rule for the given Arabic letter codepoint."""
    return LETTER_IDENTITY_RULES.get(codepoint)
