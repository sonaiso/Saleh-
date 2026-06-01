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
    WadiGate.SABAB,
    WadiGate.SHART,
    WadiGate.MANI,
    WadiGate.SIHHA,
    WadiGate.FASAD,
    WadiGate.BUTLAN,
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
    abjad_value: int | None = None,
    morpho_role_bits: str | None = None,
) -> QiyasRule:
    """
    Build a coordinate enrichment rule for a letter (Option C - Layer 2).

    Requires identity wasf/illah (from Layer 1) PLUS coordinate wasf:
      - Sound identity (phonetic proxy)
      - Makhraj (articulation place)
      - Sifat (voicing, manner, emphasis)
      - Abjad numeric value (if applicable)
      - Morphological role bits (if applicable)

    Proves invalidating_differences absence (fariq) in evidence.

    Args:
        letter_name: Lowercase Latin letter name (e.g., \"baa\", \"taa\")
        codepoint: Unicode codepoint
        sound_identity: Phonetic description (e.g., \"VOICED_BILABIAL_STOP\")
        makhraj: Articulation place (e.g., \"BILABIAL\")
        voicing: Voice quality (e.g., \"VOICED\")
        manner: Manner of articulation (e.g., \"STOP\")
        emphasis: Emphasis (\"EMPHATIC\" or \"NON_EMPHATIC\")
        invalidating_diffs: Tuple of fariq identifiers (e.g., (\"baa_vs_meem\",))
        abjad_value: Specific Abjad numeric value (e.g., 2 for BAA)
        morpho_role_bits: Morphological role classification (e.g., \"SAALATAMUUNIIHA\", \"EXPANDED_MULTI_ROLE\")
    """
    cp_hex = f\"{codepoint:04x}\"

    # Build required wasf (inherits identity from Layer 1, adds coordinates)
    required_wasf = [
        \"has_letter_codepoint\",
        f\"has_unicode_identity:{cp_hex}\",
        f\"has_script_identity:{letter_name}\",
        f\"has_latin_name:{letter_name}\",
        # Layer 2 coordinates
        f\"has_sound_identity:{sound_identity}\",
        f\"has_makhraj:{makhraj}\",
        f\"has_voicing:{voicing}\",
        f\"has_manner:{manner}\",
        f\"has_emphasis:{emphasis}\",
    ]

    if abjad_value is not None:
        required_wasf.append(\"has_abjad_system:ABJAD\")
        required_wasf.append(f\"has_abjad_value:{abjad_value}\")
        required_wasf.append(\"abjad_semantic_force:FORBIDDEN\")

    if morpho_role_bits:
        required_wasf.append(f\"has_morpho_role:{morpho_role_bits}\")

    # Build required illah
    required_illah = [
        \"belongs_to_letter_identity_domain\",
        f\"letter_identity_is:{letter_name}\",
        \"belongs_to_letter_coordinate_domain\",
    ]

    return QiyasRule(
        rule_id=f\"letter_coordinate.{letter_name}\",
        layer=\"ArabicLetterCoordinateQiyas\",
        pattern=QiyasPattern.MEMBERSHIP,
        asl_type=\"LetterCoordinateDomain\",
        far_type=\"LetterIdentityCarrier\",
        required_effective_wasf=tuple(required_wasf),
        required_illah=tuple(required_illah),
        required_wadi_gates=ALL_WADI,
        invalidating_differences=invalidating_diffs,
        neutral_identity_domain=\"letter_coordinate\",
        output_candidate_type=\"ArabicLetterCoordinateCarrier\",
        forbidden_outputs=FORBIDDEN_COORDINATE_OUTPUTS,
        rank_ceiling=EvidenceRank.FORM,
    )


# ---------------------------------------------------------------------------
# Coordinate rules for minimum required letters: BAA, TAA, SEEN, KAF
# ---------------------------------------------------------------------------

BAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    "baa", 0x0628, "VOICED_BILABIAL_STOP",
    "BILABIAL", "VOICED", "STOP", "NON_EMPHATIC",
    ("baa_vs_meem", "baa_vs_faa", "baa_vs_taa", "baa_vs_waw"),
    abjad_value=2,
    morpho_role_bits="EXPANDED_MULTI_ROLE",  # ب has prepositional and root potential
)

TAA_COORDINATE_RULE = _make_letter_coordinate_rule(
    "taa", 0x062A, "VOICELESS_DENTAL_STOP",
    "DENTAL", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("taa_vs_baa", "taa_vs_thaa", "taa_vs_daal"),
    abjad_value=400,
    morpho_role_bits="SAALATAMUUNIIHA",  # ت is part of سألتمونيها
)

SEEN_COORDINATE_RULE = _make_letter_coordinate_rule(
    "seen", 0x0633, "VOICELESS_ALVEOLAR_FRICATIVE",
    "ALVEOLAR", "VOICELESS", "FRICATIVE", "NON_EMPHATIC",
    ("seen_vs_sheen", "seen_vs_zay", "seen_vs_saad"),
    abjad_value=60,
    morpho_role_bits="SAALATAMUUNIIHA",  # س is part of سألتمونيها
)

KAF_COORDINATE_RULE = _make_letter_coordinate_rule(
    "kaf", 0x0643, "VOICELESS_VELAR_STOP",
    "VELAR", "VOICELESS", "STOP", "NON_EMPHATIC",
    ("kaf_vs_qaf", "kaf_vs_gaf"),
    abjad_value=20,
    morpho_role_bits="EXPANDED_MULTI_ROLE",  # ك has similative/pronoun and root potential
)


# Map: codepoint → coordinate rule
LETTER_COORDINATE_RULES: dict[int, QiyasRule] = {
    0x0628: BAA_COORDINATE_RULE,
    0x062A: TAA_COORDINATE_RULE,
    0x0633: SEEN_COORDINATE_RULE,
    0x0643: KAF_COORDINATE_RULE,
}


def get_letter_coordinate_rule(codepoint: int) -> QiyasRule | None:
    \"\"\"Return the ArabicLetterCoordinateQiyas rule for the given letter codepoint.\"\"\"
    return LETTER_COORDINATE_RULES.get(codepoint)
