"""
Letter Identity Rules — Gap #3 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

One canonical QiyasRule per Arabic letter identity, proving:
  unicode_identity + script_identity + sound_identity + makhraj + sifat.

Layer: LetterIdentityQiyas
Input (far): LetterCodePoint
Output:      LetterIdentityCarrier
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.forbidden_outputs import FORBIDDEN_LETTER_IDENTITY
from qiyas_core.rule import QiyasRule

_ALL_WADI = (
    WadiGate.SABAB,
    WadiGate.SHART,
    WadiGate.MANI,
    WadiGate.SIHHA,
    WadiGate.FASAD,
    WadiGate.BUTLAN,
)

# ---------------------------------------------------------------------------
# Helper to build a per-letter rule
# ---------------------------------------------------------------------------

def _make_letter_identity_rule(
    letter_name: str,
    codepoint: int,
    sound_identity: str,
    makhraj_source: str,
    voicing: str,
    manner: str,
    emphasis: str,
    invalidating_diffs: tuple[str, ...],
) -> QiyasRule:
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
            f"has_sound_identity:{sound_identity.lower()}",
            f"has_makhraj:{makhraj_source.lower()}",
        ),
        required_illah=(
            "belongs_to_letter_identity_domain",
            f"letter_identity_is:{letter_name}",
        ),
        required_wadi_gates=_ALL_WADI,
        invalidating_differences=invalidating_diffs,
        neutral_identity_domain="letter_identity",
        output_candidate_type="LetterIdentityCarrier",
        forbidden_outputs=FORBIDDEN_LETTER_IDENTITY,
        rank_ceiling=EvidenceRank.FORM,
    )


# ---------------------------------------------------------------------------
# 28 letter rules (ordered by Unicode codepoint)
# ---------------------------------------------------------------------------

HAMZA_IDENTITY_RULE = _make_letter_identity_rule(
    "hamza", 0x0621, "VOICELESS_GLOTTAL_STOP",
    "GLOTTAL", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("hamza_vs_ayn", "hamza_vs_haa_glottal"),
)

ALEF_MADDA_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_madda", 0x0622, "LONG_VOWEL_CARRIER_ALEF",
    "GLOTTAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("alef_madda_vs_waw", "alef_madda_vs_yaa"),
)

ALEF_HAMZA_ABOVE_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_hamza_above", 0x0623, "VOICELESS_GLOTTAL_STOP_ABOVE",
    "GLOTTAL", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("alef_hamza_above_vs_ayn",),
)

WAW_HAMZA_IDENTITY_RULE = _make_letter_identity_rule(
    "waw_hamza", 0x0624, "BILABIAL_HAMZA_WAW",
    "BILABIAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("waw_hamza_vs_baa",),
)

ALEF_HAMZA_BELOW_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_hamza_below", 0x0625, "VOICELESS_GLOTTAL_STOP_BELOW",
    "GLOTTAL", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("alef_hamza_below_vs_ayn",),
)

YEH_HAMZA_IDENTITY_RULE = _make_letter_identity_rule(
    "yeh_hamza", 0x0626, "PALATAL_HAMZA_YEH",
    "PALATAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("yeh_hamza_vs_yaa",),
)

ALEF_IDENTITY_RULE = _make_letter_identity_rule(
    "alef", 0x0627, "LONG_VOWEL_CARRIER_BARE_ALEF",
    "GLOTTAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("alef_vs_waw", "alef_vs_yaa"),
)

BAA_IDENTITY_RULE = _make_letter_identity_rule(
    "baa", 0x0628, "VOICED_BILABIAL_STOP",
    "BILABIAL", "VOICED", "STOP", "NON_EMPHATIC",
    ("baa_vs_meem", "baa_vs_faa", "baa_vs_taa", "baa_vs_waw"),
)

TAA_MARBUTA_IDENTITY_RULE = _make_letter_identity_rule(
    "taa_marbuta", 0x0629, "VOICELESS_DENTAL_STOP_MARBUTA",
    "DENTAL", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("taa_marbuta_vs_taa", "taa_marbuta_vs_haa"),
)

TAA_IDENTITY_RULE = _make_letter_identity_rule(
    "taa", 0x062A, "VOICELESS_DENTAL_STOP",
    "DENTAL", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("taa_vs_baa", "taa_vs_thaa", "taa_vs_daal"),
)

THAA_IDENTITY_RULE = _make_letter_identity_rule(
    "thaa", 0x062B, "VOICELESS_INTERDENTAL_FRICATIVE",
    "INTERDENTAL", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("thaa_vs_taa", "thaa_vs_dhaal"),
)

JEEM_IDENTITY_RULE = _make_letter_identity_rule(
    "jeem", 0x062C, "VOICED_POSTALVEOLAR_AFFRICATE",
    "POSTALVEOLAR", "VOICED", "AFFRICATE", "NON_EMPHATIC",
    ("jeem_vs_sheen", "jeem_vs_zay"),
)

HAA_PHARYNGEAL_IDENTITY_RULE = _make_letter_identity_rule(
    "haa_pharyngeal", 0x062D, "VOICELESS_PHARYNGEAL_FRICATIVE",
    "PHARYNGEAL", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("haa_pharyngeal_vs_ayn", "haa_pharyngeal_vs_haa_glottal"),
)

KHAA_IDENTITY_RULE = _make_letter_identity_rule(
    "khaa", 0x062E, "VOICELESS_UVULAR_FRICATIVE",
    "UVULAR", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("khaa_vs_ghain", "khaa_vs_kaf"),
)

DAAL_IDENTITY_RULE = _make_letter_identity_rule(
    "daal", 0x062F, "VOICED_DENTAL_STOP",
    "DENTAL", "VOICED", "STOP", "NON_EMPHATIC",
    ("daal_vs_taa", "daal_vs_daad"),
)

DHAAL_IDENTITY_RULE = _make_letter_identity_rule(
    "dhaal", 0x0630, "VOICED_INTERDENTAL_FRICATIVE",
    "INTERDENTAL", "VOICED", "FRICATIVE", "NON_EMPHATIC",
    ("dhaal_vs_thaa", "dhaal_vs_zay"),
)

RAA_IDENTITY_RULE = _make_letter_identity_rule(
    "raa", 0x0631, "VOICED_ALVEOLAR_TRILL",
    "ALVEOLAR", "VOICED", "TRILL", "NON_EMPHATIC",
    ("raa_vs_laam", "raa_vs_noon"),
)

ZAY_IDENTITY_RULE = _make_letter_identity_rule(
    "zay", 0x0632, "VOICED_ALVEOLAR_FRICATIVE",
    "ALVEOLAR", "VOICED", "FRICATIVE", "NON_EMPHATIC",
    ("zay_vs_seen", "zay_vs_dhaal"),
)

SEEN_IDENTITY_RULE = _make_letter_identity_rule(
    "seen", 0x0633, "VOICELESS_ALVEOLAR_FRICATIVE",
    "ALVEOLAR", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("seen_vs_sheen", "seen_vs_zay", "seen_vs_saad"),
)

SHEEN_IDENTITY_RULE = _make_letter_identity_rule(
    "sheen", 0x0634, "VOICELESS_POSTALVEOLAR_FRICATIVE",
    "POSTALVEOLAR", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("sheen_vs_seen", "sheen_vs_jeem"),
)

SAAD_IDENTITY_RULE = _make_letter_identity_rule(
    "saad", 0x0635, "VOICELESS_EMPHATIC_ALVEOLAR_FRICATIVE",
    "ALVEOLAR", "VOICELESS", "FRICATIVE", "EMPHATIC",
    ("saad_vs_seen", "saad_vs_daad"),
)

DAAD_IDENTITY_RULE = _make_letter_identity_rule(
    "daad", 0x0636, "VOICED_EMPHATIC_DENTAL_STOP",
    "DENTAL", "VOICED", "STOP", "EMPHATIC",
    ("daad_vs_daal", "daad_vs_taa_emphatic"),
)

TAA_EMPHATIC_IDENTITY_RULE = _make_letter_identity_rule(
    "taa_emphatic", 0x0637, "VOICELESS_EMPHATIC_DENTAL_STOP",
    "DENTAL", "VOICELESS", "STOP", "EMPHATIC",
    ("taa_emphatic_vs_taa", "taa_emphatic_vs_daad"),
)

DHAA_EMPHATIC_IDENTITY_RULE = _make_letter_identity_rule(
    "dhaa_emphatic", 0x0638, "VOICED_EMPHATIC_INTERDENTAL_FRICATIVE",
    "INTERDENTAL", "VOICED", "FRICATIVE", "EMPHATIC",
    ("dhaa_emphatic_vs_dhaal",),
)

AYN_IDENTITY_RULE = _make_letter_identity_rule(
    "ayn", 0x0639, "VOICED_PHARYNGEAL_FRICATIVE",
    "PHARYNGEAL", "VOICED", "FRICATIVE", "NON_EMPHATIC",
    ("ayn_vs_haa_pharyngeal", "ayn_vs_hamza"),
)

GHAIN_IDENTITY_RULE = _make_letter_identity_rule(
    "ghain", 0x063A, "VOICED_UVULAR_FRICATIVE",
    "UVULAR", "VOICED", "FRICATIVE", "NON_EMPHATIC",
    ("ghain_vs_khaa", "ghain_vs_qaf"),
)

FAA_IDENTITY_RULE = _make_letter_identity_rule(
    "faa", 0x0641, "VOICELESS_LABIODENTAL_FRICATIVE",
    "LABIODENTAL", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("faa_vs_baa", "faa_vs_waw"),
)

QAF_IDENTITY_RULE = _make_letter_identity_rule(
    "qaf", 0x0642, "VOICELESS_UVULAR_STOP",
    "UVULAR", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("qaf_vs_kaf", "qaf_vs_ghain"),
)

KAF_IDENTITY_RULE = _make_letter_identity_rule(
    "kaf", 0x0643, "VOICELESS_VELAR_STOP",
    "VELAR", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("kaf_vs_qaf", "kaf_vs_gaf"),
)

LAAM_IDENTITY_RULE = _make_letter_identity_rule(
    "laam", 0x0644, "VOICED_ALVEOLAR_LATERAL",
    "ALVEOLAR", "VOICED", "LATERAL", "NON_EMPHATIC",
    ("laam_vs_noon", "laam_vs_raa"),
)

MEEM_IDENTITY_RULE = _make_letter_identity_rule(
    "meem", 0x0645, "VOICED_BILABIAL_NASAL",
    "BILABIAL", "VOICED", "NASAL", "NON_EMPHATIC",
    ("meem_vs_baa", "meem_vs_noon"),
)

NOON_IDENTITY_RULE = _make_letter_identity_rule(
    "noon", 0x0646, "VOICED_ALVEOLAR_NASAL",
    "ALVEOLAR", "VOICED", "NASAL", "NON_EMPHATIC",
    ("noon_vs_meem", "noon_vs_laam"),
)

HAA_GLOTTAL_IDENTITY_RULE = _make_letter_identity_rule(
    "haa_glottal", 0x0647, "VOICELESS_GLOTTAL_FRICATIVE",
    "GLOTTAL", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("haa_glottal_vs_haa_pharyngeal", "haa_glottal_vs_hamza"),
)

WAW_IDENTITY_RULE = _make_letter_identity_rule(
    "waw", 0x0648, "VOICED_BILABIAL_APPROXIMANT",
    "BILABIAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("waw_vs_baa", "waw_vs_meem", "waw_vs_yaa"),
)

ALEF_MAQSURA_IDENTITY_RULE = _make_letter_identity_rule(
    "alef_maqsura", 0x0649, "LONG_VOWEL_CARRIER_ALEF_MAQSURA",
    "PALATAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("alef_maqsura_vs_yaa",),
)

YAA_IDENTITY_RULE = _make_letter_identity_rule(
    "yaa", 0x064A, "VOICED_PALATAL_APPROXIMANT",
    "PALATAL", "VOICED", "APPROXIMANT", "NON_EMPHATIC",
    ("yaa_vs_waw", "yaa_vs_jeem"),
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
    0x0629: TAA_MARBUTA_IDENTITY_RULE,
    0x062A: TAA_IDENTITY_RULE,
    0x062B: THAA_IDENTITY_RULE,
    0x062C: JEEM_IDENTITY_RULE,
    0x062D: HAA_PHARYNGEAL_IDENTITY_RULE,
    0x062E: KHAA_IDENTITY_RULE,
    0x062F: DAAL_IDENTITY_RULE,
    0x0630: DHAAL_IDENTITY_RULE,
    0x0631: RAA_IDENTITY_RULE,
    0x0632: ZAY_IDENTITY_RULE,
    0x0633: SEEN_IDENTITY_RULE,
    0x0634: SHEEN_IDENTITY_RULE,
    0x0635: SAAD_IDENTITY_RULE,
    0x0636: DAAD_IDENTITY_RULE,
    0x0637: TAA_EMPHATIC_IDENTITY_RULE,
    0x0638: DHAA_EMPHATIC_IDENTITY_RULE,
    0x0639: AYN_IDENTITY_RULE,
    0x063A: GHAIN_IDENTITY_RULE,
    0x0641: FAA_IDENTITY_RULE,
    0x0642: QAF_IDENTITY_RULE,
    0x0643: KAF_IDENTITY_RULE,
    0x0644: LAAM_IDENTITY_RULE,
    0x0645: MEEM_IDENTITY_RULE,
    0x0646: NOON_IDENTITY_RULE,
    0x0647: HAA_GLOTTAL_IDENTITY_RULE,
    0x0648: WAW_IDENTITY_RULE,
    0x0649: ALEF_MAQSURA_IDENTITY_RULE,
    0x064A: YAA_IDENTITY_RULE,
}


def get_letter_identity_rule(codepoint: int) -> QiyasRule | None:
    """Return the LetterIdentityQiyas rule for the given Arabic letter codepoint."""
    return LETTER_IDENTITY_RULES.get(codepoint)
