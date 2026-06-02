"""
Letter Fariq (Invalidating Differences) Registry - Single Source of Truth

Constitutional Basis:
  - SIFAT_VECTOR_CONTRACT.md: Fariq negation system
  - SOURCE_OF_TRUTH_REGISTRY.md § 4: "Letter fariq pairs" canonical source
  - PROJECT_MATHEMATICAL_FOUNDATION.md: Invalidating difference blocking

Purpose:
  Define ALL invalidating difference pairs between Arabic letters.
  Used to NEGATE wrong identities through fariq evidence.

Critical Law:
  Invalidating difference blocks licensing.

  Example:
    If proving ب (BAA), must negate:
      - fariq:ب_vs_ت:present (voicing difference blocks TAA)
      - fariq:ب_vs_م:present (nasality difference blocks MEEM)
      - fariq:ب_vs_ف:present (manner difference blocks FAA)

Truth Type: Operation Truth (Negation)
Domain: Controlled Vocalized Arabic
Evidence Rank: FORMAL_STRUCTURE

Forbidden:
  - DO NOT duplicate fariq pairs in adapters
  - DO NOT create ad-hoc invalidating differences
  - DO NOT skip fariq negation in identity proofs
"""

from dataclasses import dataclass
from enum import Enum


class FariqAxis(Enum):
    """
    Axes along which invalidating differences occur.

    These correspond to SifatVector axes (6-axis system).
    """
    VOICING = "voicing"           # VOICED vs VOICELESS
    MANNER = "manner"             # STOP, FRICATIVE, NASAL, etc.
    NASALITY = "nasality"         # NASAL vs ORAL
    FRICATION = "frication"       # FRICATIVE vs NON_FRICATIVE
    CONTINUANCY = "continuancy"   # CONTINUANT vs NON_CONTINUANT
    EMPHASIS = "emphasis"         # EMPHATIC vs NON_EMPHATIC
    PLACE = "place"               # MAKHRAJ difference
    ORTHOGRAPHY = "orthography"   # Orthographic form difference


@dataclass(frozen=True)
class FariqPair:
    """
    Invalidating difference pair between two letters.

    Format: letter1 vs letter2 along specific axis.
    Used to generate fariq:{letter1}_vs_{letter2}:present evidence.
    """
    letter1_codepoint: int
    letter2_codepoint: int
    letter1_name: str
    letter2_name: str
    axis: FariqAxis
    difference_description: str


# Canonical fariq pairs registry
# This is the single source of truth for ALL invalidating differences

LETTER_FARIQ_PAIRS: tuple[FariqPair, ...] = (
    # BAA (ب) vs other letters
    FariqPair(
        letter1_codepoint=0x0628,
        letter2_codepoint=0x062A,
        letter1_name="baa",
        letter2_name="taa",
        axis=FariqAxis.VOICING,
        difference_description="ب voiced vs ت voiceless (same place, different voicing)"
    ),
    FariqPair(
        letter1_codepoint=0x0628,
        letter2_codepoint=0x0645,
        letter1_name="baa",
        letter2_name="meem",
        axis=FariqAxis.NASALITY,
        difference_description="ب oral vs م nasal (same place, different nasality)"
    ),
    FariqPair(
        letter1_codepoint=0x0628,
        letter2_codepoint=0x0641,
        letter1_name="baa",
        letter2_name="faa",
        axis=FariqAxis.MANNER,
        difference_description="ب stop vs ف fricative (different manner)"
    ),
    FariqPair(
        letter1_codepoint=0x0628,
        letter2_codepoint=0x0648,
        letter1_name="baa",
        letter2_name="waw",
        axis=FariqAxis.MANNER,
        difference_description="ب stop vs و approximant (different manner)"
    ),

    # TAA (ت) vs other letters
    FariqPair(
        letter1_codepoint=0x062A,
        letter2_codepoint=0x0628,
        letter1_name="taa",
        letter2_name="baa",
        axis=FariqAxis.VOICING,
        difference_description="ت voiceless vs ب voiced"
    ),
    FariqPair(
        letter1_codepoint=0x062A,
        letter2_codepoint=0x062B,
        letter1_name="taa",
        letter2_name="thaa",
        axis=FariqAxis.MANNER,
        difference_description="ت stop vs ث fricative"
    ),
    FariqPair(
        letter1_codepoint=0x062A,
        letter2_codepoint=0x062F,
        letter1_name="taa",
        letter2_name="dal",
        axis=FariqAxis.VOICING,
        difference_description="ت voiceless vs د voiced"
    ),
    FariqPair(
        letter1_codepoint=0x062A,
        letter2_codepoint=0x0637,
        letter1_name="taa",
        letter2_name="taa_emphatic",
        axis=FariqAxis.EMPHASIS,
        difference_description="ت plain vs ط emphatic"
    ),

    # SEEN (س) vs other letters
    FariqPair(
        letter1_codepoint=0x0633,
        letter2_codepoint=0x0635,
        letter1_name="seen",
        letter2_name="saad",
        axis=FariqAxis.EMPHASIS,
        difference_description="س plain vs ص emphatic"
    ),
    FariqPair(
        letter1_codepoint=0x0633,
        letter2_codepoint=0x0634,
        letter1_name="seen",
        letter2_name="sheen",
        axis=FariqAxis.PLACE,
        difference_description="س alveolar vs ش post-alveolar"
    ),
    FariqPair(
        letter1_codepoint=0x0633,
        letter2_codepoint=0x062B,
        letter1_name="seen",
        letter2_name="thaa",
        axis=FariqAxis.PLACE,
        difference_description="س alveolar vs ث dental"
    ),

    # KAF (ك) vs other letters
    FariqPair(
        letter1_codepoint=0x0643,
        letter2_codepoint=0x0642,
        letter1_name="kaf",
        letter2_name="qaf",
        axis=FariqAxis.PLACE,
        difference_description="ك velar vs ق uvular"
    ),
    FariqPair(
        letter1_codepoint=0x0643,
        letter2_codepoint=0x062C,
        letter1_name="kaf",
        letter2_name="jeem",
        axis=FariqAxis.VOICING,
        difference_description="ك voiceless vs ج voiced"
    ),

    # DAL (د) vs other letters
    FariqPair(
        letter1_codepoint=0x062F,
        letter2_codepoint=0x0630,
        letter1_name="dal",
        letter2_name="thaal",
        axis=FariqAxis.MANNER,
        difference_description="د stop vs ذ fricative"
    ),
    FariqPair(
        letter1_codepoint=0x062F,
        letter2_codepoint=0x0636,
        letter1_name="dal",
        letter2_name="daad",
        axis=FariqAxis.EMPHASIS,
        difference_description="د plain vs ض emphatic"
    ),

    # MEEM (م) vs other letters
    FariqPair(
        letter1_codepoint=0x0645,
        letter2_codepoint=0x0628,
        letter1_name="meem",
        letter2_name="baa",
        axis=FariqAxis.NASALITY,
        difference_description="م nasal vs ب oral"
    ),
    FariqPair(
        letter1_codepoint=0x0645,
        letter2_codepoint=0x0646,
        letter1_name="meem",
        letter2_name="noon",
        axis=FariqAxis.PLACE,
        difference_description="م bilabial vs ن alveolar"
    ),

    # NOON (ن) vs other letters
    FariqPair(
        letter1_codepoint=0x0646,
        letter2_codepoint=0x0645,
        letter1_name="noon",
        letter2_name="meem",
        axis=FariqAxis.PLACE,
        difference_description="ن alveolar vs م bilabial"
    ),
    FariqPair(
        letter1_codepoint=0x0646,
        letter2_codepoint=0x0644,
        letter1_name="noon",
        letter2_name="lam",
        axis=FariqAxis.NASALITY,
        difference_description="ن nasal vs ل oral"
    ),

    # WAW (و) vs other letters
    FariqPair(
        letter1_codepoint=0x0648,
        letter2_codepoint=0x0641,
        letter1_name="waw",
        letter2_name="faa",
        axis=FariqAxis.MANNER,
        difference_description="و approximant vs ف fricative"
    ),
    FariqPair(
        letter1_codepoint=0x0648,
        letter2_codepoint=0x0628,
        letter1_name="waw",
        letter2_name="baa",
        axis=FariqAxis.MANNER,
        difference_description="و approximant vs ب stop"
    ),

    # YAA (ي) vs other letters
    FariqPair(
        letter1_codepoint=0x064A,
        letter2_codepoint=0x062C,
        letter1_name="yaa",
        letter2_name="jeem",
        axis=FariqAxis.MANNER,
        difference_description="ي approximant vs ج affricate"
    ),

    # ALIF (ا) vs other letters
    FariqPair(
        letter1_codepoint=0x0627,
        letter2_codepoint=0x0639,
        letter1_name="alif",
        letter2_name="ayn",
        axis=FariqAxis.MANNER,
        difference_description="ا approximant/vowel vs ع fricative"
    ),

    # HAA (ح) vs other letters
    FariqPair(
        letter1_codepoint=0x062D,
        letter2_codepoint=0x062E,
        letter1_name="haa",
        letter2_name="khaa",
        axis=FariqAxis.VOICING,
        difference_description="ح voiceless vs خ voiced"
    ),
    FariqPair(
        letter1_codepoint=0x062D,
        letter2_codepoint=0x0639,
        letter1_name="haa",
        letter2_name="ayn",
        axis=FariqAxis.VOICING,
        difference_description="ح voiceless vs ع voiced"
    ),

    # Emphatic pairs
    FariqPair(
        letter1_codepoint=0x0637,
        letter2_codepoint=0x062A,
        letter1_name="taa_emphatic",
        letter2_name="taa",
        axis=FariqAxis.EMPHASIS,
        difference_description="ط emphatic vs ت plain"
    ),
    FariqPair(
        letter1_codepoint=0x0635,
        letter2_codepoint=0x0633,
        letter1_name="saad",
        letter2_name="seen",
        axis=FariqAxis.EMPHASIS,
        difference_description="ص emphatic vs س plain"
    ),
    FariqPair(
        letter1_codepoint=0x0636,
        letter2_codepoint=0x062F,
        letter1_name="daad",
        letter2_name="dal",
        axis=FariqAxis.EMPHASIS,
        difference_description="ض emphatic vs د plain"
    ),
    FariqPair(
        letter1_codepoint=0x0638,
        letter2_codepoint=0x0630,
        letter1_name="dhaa",
        letter2_name="thaal",
        axis=FariqAxis.EMPHASIS,
        difference_description="ظ emphatic vs ذ plain"
    ),

    # Add more fariq pairs as needed for complete coverage
)


def get_fariq_pairs(letter_codepoint: int) -> tuple[FariqPair, ...]:
    """
    Get all fariq pairs for a given letter.

    Used to generate fariq negation evidence when proving letter identity.

    Args:
        letter_codepoint: Unicode codepoint of the letter

    Returns:
        Tuple of all FariqPair entries where this letter appears

    Example:
        >>> pairs = get_fariq_pairs(0x0628)  # BAA
        >>> len(pairs) > 0
        True
        >>> any(p.letter1_name == "baa" and p.letter2_name == "taa" for p in pairs)
        True
    """
    return tuple(
        pair for pair in LETTER_FARIQ_PAIRS
        if pair.letter1_codepoint == letter_codepoint
        or pair.letter2_codepoint == letter_codepoint
    )


def has_invalidating_difference(
    letter1_codepoint: int,
    letter2_codepoint: int
) -> FariqPair | None:
    """
    Check if two letters have an invalidating difference.

    Args:
        letter1_codepoint: First letter codepoint
        letter2_codepoint: Second letter codepoint

    Returns:
        FariqPair if invalidating difference exists, None otherwise

    Example:
        >>> pair = has_invalidating_difference(0x0628, 0x062A)  # BAA vs TAA
        >>> pair is not None
        True
        >>> pair.axis == FariqAxis.VOICING
        True
    """
    for pair in LETTER_FARIQ_PAIRS:
        if (pair.letter1_codepoint == letter1_codepoint and
            pair.letter2_codepoint == letter2_codepoint):
            return pair
        if (pair.letter1_codepoint == letter2_codepoint and
            pair.letter2_codepoint == letter1_codepoint):
            return pair
    return None


# Registry metadata for source-of-truth compliance
REGISTRY_METADATA = {
    "truth_type": "operation",
    "truth_name": "letter_fariq_pairs",
    "canonical_source": "src/qiyas_core/registries/letter_fariq_registry.py",
    "domain": "controlled_vocalized_arabic",
    "evidence_rank": "FORMAL_STRUCTURE",
    "forbidden_duplicates": [
        "src/qiyas_core/letter_identity_adapter.py",
        "src/qiyas_core/letter_coordinate_adapter.py",
        "src/qiyas_core/rules/letter_identity_rules.py",
    ],
}
