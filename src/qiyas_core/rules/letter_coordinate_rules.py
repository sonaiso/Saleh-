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
    invalidating_diffs: tuple[str, ...],
    has_abjad: bool = True,
    abjad_value: int | None = None,
    morpho_role_bits: str | None = None,
) -> QiyasRule:
    """
    Build a coordinate enrichment rule for a letter (Option C - Layer 2).

    Requires identity wasf/illah (from Layer 1) PLUS coordinate wasf:
      - Sound identity (phonetic proxy)
      - Makhraj (articulation place)
      - Sifat (voicing, manner, emphasis)
      - Abjad numeric (if applicable) - VALUE-SPECIFIC
      - Morphological role bits (if applicable)

    Proves invalidating_differences absence (fariq) in evidence.

    Args:
        letter_name: Lowercase Latin letter name (e.g., "baa", "taa")
        codepoint: Unicode codepoint
        sound_identity: Phonetic description (e.g., "VOICED_BILABIAL_STOP")
        makhraj: Articulation place (e.g., "BILABIAL")
        voicing: Voice quality (e.g., "VOICED")
        manner: Manner of articulation (e.g., "STOP")
        emphasis: Emphasis ("EMPHATIC" or "NON_EMPHATIC")
        invalidating_diffs: Tuple of fariq identifiers (e.g., ("baa_vs_meem",))
        has_abjad: Whether letter has Abjad numeric value (default True)
        abjad_value: Specific Abjad numeric value (e.g., 2 for BAA)
        morpho_role_bits: Morphological role classification (e.g., "SAALATAMUUNIIHA", "EXPANDED_MULTI_ROLE")
    """
    cp_hex = f"{codepoint:04x}"

    # Build required wasf (inherits identity from Layer 1, adds coordinates)
    required_wasf = [
        "has_letter_codepoint",
        f"has_unicode_identity:{cp_hex}",
        f"has_script_identity:{letter_name}",
        f"has_latin_name:{letter_name}",
        # Layer 2 coordinates
        f"has_sound_identity:{sound_identity}",
        f"has_makhraj:{makhraj}",
        f"has_voicing:{voicing}",
        f"has_manner:{manner}",
        f"has_emphasis:{emphasis}",
    ]

    if has_abjad:
        required_wasf.append("has_abjad_system:ABJAD")
        if abjad_value is not None:
            required_wasf.append(f"has_abjad_value:{abjad_value}")
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
# Letter coordinate rules (minimal slice: BAA, TAA, SEEN, KAF)
# ---------------------------------------------------------------------------

# BAA - EXPANDED_MULTI_ROLE
BAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="baa",
    codepoint=0x0628,
    sound_identity="VOICED_BILABIAL_STOP",
    makhraj="BILABIAL",
    voicing="VOICED",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    invalidating_diffs=("baa_vs_meem", "baa_vs_faa", "baa_vs_taa", "baa_vs_waw"),
    has_abjad=True,
    abjad_value=2,
    morpho_role_bits="EXPANDED_MULTI_ROLE",
)

# TAA - SAALATAMUUNIIHA
TAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="taa",
    codepoint=0x062A,
    sound_identity="VOICELESS_DENTAL_STOP",
    makhraj="DENTAL",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    invalidating_diffs=("taa_vs_baa", "taa_vs_daal", "taa_vs_taa_emphatic"),
    has_abjad=True,
    abjad_value=400,
    morpho_role_bits="SAALATAMUUNIIHA",
)

# SEEN - SAALATAMUUNIIHA
SEEN_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="seen",
    codepoint=0x0633,
    sound_identity="VOICELESS_ALVEOLAR_FRICATIVE",
    makhraj="ALVEOLAR",
    voicing="VOICELESS",
    manner="FRICATIVE",
    emphasis="NON_EMPHATIC",
    invalidating_diffs=("seen_vs_saad", "seen_vs_sheen", "seen_vs_zay"),
    has_abjad=True,
    abjad_value=60,
    morpho_role_bits="SAALATAMUUNIIHA",
)

# KAF - EXPANDED_MULTI_ROLE
KAF_COORDINATE_RULE = _make_letter_coordinate_rule(
    letter_name="kaf",
    codepoint=0x0643,
    sound_identity="VOICELESS_VELAR_STOP",
    makhraj="VELAR",
    voicing="VOICELESS",
    manner="STOP",
    emphasis="NON_EMPHATIC",
    invalidating_diffs=("kaf_vs_qaf", "kaf_vs_ghayn"),
    has_abjad=True,
    abjad_value=20,
    morpho_role_bits="EXPANDED_MULTI_ROLE",
)


# Map: codepoint → coordinate rule
LETTER_COORDINATE_RULES: dict[int, QiyasRule] = {
    0x0628: BAA_COORDINATE_RULE,
    0x062A: TAA_COORDINATE_RULE,
    0x0633: SEEN_COORDINATE_RULE,
    0x0643: KAF_COORDINATE_RULE,
}


def get_letter_coordinate_rule(codepoint: int) -> QiyasRule | None:
    """Return the ArabicLetterCoordinateQiyas rule for the given letter codepoint."""
    return LETTER_COORDINATE_RULES.get(codepoint)
