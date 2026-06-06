"""
Arabic Letter Coordinate Rules (Layer 2)

Option C Architecture - Layer 2: ArabicLetterCoordinateCarrier

Constitutional rules for enriching LetterIdentityCarrier with coordinate data:
  - Phonetic proxy (sound_identity)
  - Makhraj (articulation place)
  - Sifat (phonetic features)
  - Abjad numeric values
  - Invalidating differences (fariq)
  - Morphological role potential bits

Architecture:
    LetterIdentityCarrier
      ↓
    ArabicLetterCoordinateCarrier(+ phonetic + makhraj + sifat + abjad + fariq + morpho_role)

Forbidden: This layer does NOT produce SlotCandidate or require sequence context.
"""

from qiyas_core.enums import EvidenceRank, QiyasPattern, WadiGate
from qiyas_core.rule import QiyasRule
from qiyas_core.abjad_system import get_abjad_coordinate
from qiyas_core.registries.letter_fariq_registry import get_fariq_pairs


ALL_WADI = (
    WadiGate.CAUSE,
    WadiGate.CONDITION,
    WadiGate.OBSTACLE,
    WadiGate.VALIDITY,
    WadiGate.CORRUPTION,
    WadiGate.NULLITY,
)


# Forbidden outputs: ArabicLetterCoordinateCarrier is still atomic, not compositional
FORBIDDEN_COORDINATE_OUTPUTS = (
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
# Helper to build a coordinate enrichment rule (Option C - Layer 2)
# ---------------------------------------------------------------------------

def _make_letter_coordinate_rule(
    letter_name: str,
    codepoint: int,
    sound_identity: str,
    makhraj: str,
    voicing: str,
    manner: str,
    emphasis: str,
    morpho_role_bits: str | None = None,
) -> QiyasRule:
    """
    Build a coordinate enrichment rule for a letter (Option C - Layer 2).

    Requires identity wasf/illah (from Layer 1) PLUS coordinate wasf:
      - Sound identity (phonetic proxy)
      - Makhraj (articulation place)
      - Sifat (voicing, manner, emphasis)
      - Abjad numeric (if applicable) - fetched from abjad_system.py
      - Morphological role bits (if applicable)

    Derives invalidating_differences from letter_fariq_registry (single source of truth).

    Args:
        letter_name: Lowercase Latin letter name (e.g., "baa", "taa")
        codepoint: Unicode codepoint
        sound_identity: Phonetic description (e.g., "VOICED_BILABIAL_STOP")
        makhraj: Articulation place (e.g., "BILABIAL")
        voicing: Voice quality (e.g., "VOICED")
        manner: Manner of articulation (e.g., "STOP")
        emphasis: Emphasis ("EMPHATIC" or "NON_EMPHATIC")
        morpho_role_bits: Morphological role classification (e.g., "SAALATAMUUNIIHA", "EXPANDED_MULTI_ROLE")
    """
    cp_hex = f"{codepoint:04x}"

    # Derive invalidating_differences from letter_fariq_registry (single source of truth)
    fariq_pairs = get_fariq_pairs(codepoint)
    invalidating_diffs = tuple(
        f"{pair.letter1_name}_vs_{pair.letter2_name}"
        for pair in fariq_pairs
    )

    # Build required wasf (inherits identity from Layer 1, adds coordinates)
    required_wasf = [
        "has_letter_codepoint",
        f"has_unicode_identity:{cp_hex}",
        f"has_script_identity:{letter_name}",
        f"has_latin_name:{letter_name}",
        # Note: has_arabic_name is optional in Layer 2 rules (not all letters may have it)
        # Layer 2 coordinates
        f"has_sound_identity:{sound_identity}",
        f"has_makhraj:{makhraj}",
        f"has_voicing:{voicing}",
        f"has_manner:{manner}",
        f"has_emphasis:{emphasis}",
    ]

    # Get Abjad value from single source of truth (abjad_system.py)
    abjad_coord = get_abjad_coordinate(codepoint)
    if abjad_coord:
        required_wasf.append("has_abjad_system:ABJAD")
        required_wasf.append(f"has_abjad_value:{abjad_coord.numeric_value}")
        required_wasf.append("abjad_semantic_force:FORBIDDEN")

    if morpho_role_bits:
        required_wasf.append(f"has_morpho_role:{morpho_role_bits}")

    # Build required illah
    required_illah = [
        "belongs_to_letter_identity_domain",
        f"letter_identity_is:{letter_name}",
        "belongs_to_letter_coordinate_domain",
    ]

    return QiyasRule(
        rule_id=f"letter_coordinate.{letter_name}",
        layer="ArabicLetterCoordinateQiyas",
        pattern=QiyasPattern.MEMBERSHIP,
        asl_type="LetterCoordinateDomain",
        far_type="LetterIdentityCarrier",
        required_effective_wasf=tuple(required_wasf),
        required_illah=tuple(required_illah),
        required_wadi_gates=ALL_WADI,
        invalidating_differences=invalidating_diffs,
        neutral_identity_domain="letter_coordinate",
        output_candidate_type="ArabicLetterCoordinateCarrier",
        forbidden_outputs=FORBIDDEN_COORDINATE_OUTPUTS,
        rank_ceiling=EvidenceRank.FORMAL_STRUCTURE,
    )


# ---------------------------------------------------------------------------
# Letter coordinate rules (full Arabic alphabet: 28 core letters)
# Ordered by Unicode codepoint (U+0621 … U+064A)
# ---------------------------------------------------------------------------

# U+0621 ء HAMZA
HAMZA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="hamza",
    codepoint=0x0621,
    sound_identity="VOICELESS_GLOTTAL_STOP",
    makhraj="GLOTTAL",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,  # No Abjad value, single role
)

# U+0628 ب BAA - EXPANDED_MULTI_ROLE
BAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="baa",
    codepoint=0x0628,
    sound_identity="VOICED_BILABIAL_STOP",
    makhraj="BILABIAL",
    voicing="VOICED",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="EXPANDED_MULTI_ROLE",
)

# U+062A ت TAA - SAALATAMUUNIIHA
TAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="taa",
    codepoint=0x062A,
    sound_identity="VOICELESS_DENTAL_STOP",
    makhraj="DENTAL",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",
)

# U+062B ث THAA
THAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="thaa",
    codepoint=0x062B,
    sound_identity="VOICELESS_INTERDENTAL_FRICATIVE",
    makhraj="INTERDENTAL",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+062C ج JEEM
JEEM_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="jeem",
    codepoint=0x062C,
    sound_identity="VOICED_POSTALVEOLAR_AFFRICATE",
    makhraj="POSTALVEOLAR",
    voicing="VOICED",
    manner="AFFRICATE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+062D ح HAA (pharyngeal)
HAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="haa",
    codepoint=0x062D,
    sound_identity="VOICELESS_PHARYNGEAL_FRICATIVE",
    makhraj="PHARYNGEAL",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",  # ه in سألتمونيها
)

# U+062E خ KHAA
KHAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="khaa",
    codepoint=0x062E,
    sound_identity="VOICELESS_UVULAR_FRICATIVE",
    makhraj="UVULAR",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+062F د DAAL
DAAL_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="dal",
    codepoint=0x062F,
    sound_identity="VOICED_DENTAL_STOP",
    makhraj="DENTAL",
    voicing="VOICED",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0630 ذ DHAAL
DHAAL_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="thaal",
    codepoint=0x0630,
    sound_identity="VOICED_INTERDENTAL_FRICATIVE",
    makhraj="INTERDENTAL",
    voicing="VOICED",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0631 ر RAA
RAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="raa",
    codepoint=0x0631,
    sound_identity="VOICED_ALVEOLAR_TRILL",
    makhraj="ALVEOLAR",
    voicing="VOICED",
    manner="TRILL",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0632 ز ZAY
ZAY_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="zay",
    codepoint=0x0632,
    sound_identity="VOICED_ALVEOLAR_FRICATIVE",
    makhraj="ALVEOLAR",
    voicing="VOICED",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0633 س SEEN - SAALATAMUUNIIHA
SEEN_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="seen",
    codepoint=0x0633,
    sound_identity="VOICELESS_ALVEOLAR_FRICATIVE",
    makhraj="ALVEOLAR",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",
)

# U+0634 ش SHEEN
SHEEN_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="sheen",
    codepoint=0x0634,
    sound_identity="VOICELESS_POSTALVEOLAR_FRICATIVE",
    makhraj="POSTALVEOLAR",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0635 ص SAAD (emphatic)
SAAD_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="saad",
    codepoint=0x0635,
    sound_identity="VOICELESS_EMPHATIC_ALVEOLAR_FRICATIVE",
    makhraj="ALVEOLAR",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="EMPHATIC",
    morpho_role_bits=None,
)

# U+0636 ض DAAD (emphatic)
DAAD_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="daad",
    codepoint=0x0636,
    sound_identity="VOICED_EMPHATIC_DENTAL_STOP",
    makhraj="DENTAL",
    voicing="VOICED",
    manner="STOP",
    emphasis="EMPHATIC",
    morpho_role_bits=None,
)

# U+0637 ط TAA_EMPHATIC
TAA_EMPHATIC_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="taa_emphatic",
    codepoint=0x0637,
    sound_identity="VOICELESS_EMPHATIC_DENTAL_STOP",
    makhraj="DENTAL",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="EMPHATIC",
    morpho_role_bits=None,
)

# U+0638 ظ DHAA_EMPHATIC
DHAA_EMPHATIC_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="dhaa_emphatic",
    codepoint=0x0638,
    sound_identity="VOICED_EMPHATIC_INTERDENTAL_FRICATIVE",
    makhraj="INTERDENTAL",
    voicing="VOICED",
    manner="FRICATIVE",
    emphasis="EMPHATIC",
    morpho_role_bits=None,
)

# U+0639 ع AYN
AYN_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="ayn",
    codepoint=0x0639,
    sound_identity="VOICED_PHARYNGEAL_FRICATIVE",
    makhraj="PHARYNGEAL",
    voicing="VOICED",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+063A غ GHAIN
GHAIN_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="ghayn",
    codepoint=0x063A,
    sound_identity="VOICED_UVULAR_FRICATIVE",
    makhraj="UVULAR",
    voicing="VOICED",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0641 ف FAA - EXPANDED_MULTI_ROLE
FAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="faa",
    codepoint=0x0641,
    sound_identity="VOICELESS_LABIODENTAL_FRICATIVE",
    makhraj="LABIODENTAL",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="EXPANDED_MULTI_ROLE",
)

# U+0642 ق QAF
QAF_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="qaf",
    codepoint=0x0642,
    sound_identity="VOICELESS_UVULAR_STOP",
    makhraj="UVULAR",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    morpho_role_bits=None,
)

# U+0643 ك KAF - EXPANDED_MULTI_ROLE
KAF_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="kaf",
    codepoint=0x0643,
    sound_identity="VOICELESS_VELAR_STOP",
    makhraj="VELAR",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="EXPANDED_MULTI_ROLE",
)

# U+0644 ل LAAM - SAALATAMUUNIIHA
LAAM_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="lam",
    codepoint=0x0644,
    sound_identity="VOICED_ALVEOLAR_LATERAL",
    makhraj="ALVEOLAR",
    voicing="VOICED",
    manner="LATERAL",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",
)

# U+0645 م MEEM - SAALATAMUUNIIHA
MEEM_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="meem",
    codepoint=0x0645,
    sound_identity="VOICED_BILABIAL_NASAL",
    makhraj="BILABIAL",
    voicing="VOICED",
    manner="NASAL",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",
)

# U+0646 ن NOON - SAALATAMUUNIIHA
NOON_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="noon",
    codepoint=0x0646,
    sound_identity="VOICED_ALVEOLAR_NASAL",
    makhraj="ALVEOLAR",
    voicing="VOICED",
    manner="NASAL",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",
)

# U+0647 ه HAA_FINAL (glottal) - SAALATAMUUNIIHA
HAA_FINAL_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="haa_final",
    codepoint=0x0647,
    sound_identity="VOICELESS_GLOTTAL_FRICATIVE",
    makhraj="GLOTTAL",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    morpho_role_bits="SAALATAMUUNIIHA",
)


# Map: codepoint → coordinate rule
# Complete 28-letter Arabic alphabet (consonantal core letters)
LETTER_COORDINATE_RULES: dict[int, QiyasRule] = {
    0x0621: HAMZA_COORDINATE_RULE,
    0x0628: BAA_COORDINATE_RULE,
    0x062A: TAA_COORDINATE_RULE,
    0x062B: THAA_COORDINATE_RULE,
    0x062C: JEEM_COORDINATE_RULE,
    0x062D: HAA_COORDINATE_RULE,
    0x062E: KHAA_COORDINATE_RULE,
    0x062F: DAAL_COORDINATE_RULE,
    0x0630: DHAAL_COORDINATE_RULE,
    0x0631: RAA_COORDINATE_RULE,
    0x0632: ZAY_COORDINATE_RULE,
    0x0633: SEEN_COORDINATE_RULE,
    0x0634: SHEEN_COORDINATE_RULE,
    0x0635: SAAD_COORDINATE_RULE,
    0x0636: DAAD_COORDINATE_RULE,
    0x0637: TAA_EMPHATIC_COORDINATE_RULE,
    0x0638: DHAA_EMPHATIC_COORDINATE_RULE,
    0x0639: AYN_COORDINATE_RULE,
    0x063A: GHAIN_COORDINATE_RULE,
    0x0641: FAA_COORDINATE_RULE,
    0x0642: QAF_COORDINATE_RULE,
    0x0643: KAF_COORDINATE_RULE,
    0x0644: LAAM_COORDINATE_RULE,
    0x0645: MEEM_COORDINATE_RULE,
    0x0646: NOON_COORDINATE_RULE,
    0x0647: HAA_FINAL_COORDINATE_RULE,
}


def get_letter_coordinate_rule(codepoint: int) -> QiyasRule | None:
    """Return the ArabicLetterCoordinateQiyas rule for the given letter codepoint."""
    return LETTER_COORDINATE_RULES.get(codepoint)
