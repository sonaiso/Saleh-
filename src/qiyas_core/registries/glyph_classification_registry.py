"""
Glyph Classification Registry - Single Source of Truth

Constitutional Basis:
  - GLYPH_CLASSIFICATION_GATE_PLAN.md: Complete glyph taxonomy
  - SOURCE_OF_TRUTH_REGISTRY.md § 4: "Glyph classification" canonical source
  - FULL_LAYER_2_PLAN.md § 3: GlyphClassificationGate requirement

Purpose:
  Classify glyph types BEFORE assigning phonetic/morphological coordinates.
  This is the ONLY canonical source for glyph classification.

Critical Distinction:
  - CoreArabicLetter (ب ت ج) → Direct coordinate assignment
  - HamzaSeatGlyph (أ إ ؤ ئ) → Requires decomposition
  - WeakLetterGlyph (و ي ا) → Context-dependent role
  - TatweelGlyph (ـ) → NO coordinates (spacing only)
  - ComplexGlyph (آ لا) → Requires decomposition gate

Truth Type: Classification Truth
Domain: Controlled Vocalized Arabic
Evidence Rank: FORMAL_STRUCTURE

Forbidden:
  - DO NOT duplicate these classifications in adapters
  - DO NOT create parallel glyph classification logic
  - DO NOT treat all glyphs as simple letters
"""

from enum import Enum
from dataclasses import dataclass


class GlyphClass(Enum):
    """
    Glyph classification taxonomy.

    CRITICAL: This classification happens BEFORE coordinate assignment.
    Different glyph classes require different processing strategies.
    """
    CORE_ARABIC_LETTER = "core_arabic_letter"
    # Simple letters with direct 1:1 phonetic mapping
    # Strategy: Direct coordinate assignment
    # Examples: ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه

    HAMZA_SEAT_GLYPH = "hamza_seat_glyph"
    # Hamza on a seat (composite glyph)
    # Strategy: Decompose into hamza + seat, then coordinate each
    # Examples: أ (alif+hamza above), إ (alif+hamza below),
    #           ؤ (waw+hamza), ئ (yaa+hamza), ء (standalone hamza)

    WEAK_LETTER_GLYPH = "weak_letter_glyph"
    # Letters with multiple potential roles (context-dependent)
    # Strategy: Requires RoleDisambiguationGate in higher layers
    # Examples: و (waw), ي (yaa), ا (alif)
    # Roles: carrier | madd | diphthong | orthographic

    TATWEEL_GLYPH = "tatweel_glyph"
    # Spacing/justification glyph, NOT a letter
    # Strategy: NO phonetic coordinates, NO morpho role
    # Example: ـ (U+0640 TATWEEL)

    ORTHOGRAPHIC_VARIANT = "orthographic_variant"
    # Orthographic form variants
    # Strategy: Special coordinate handling, terminal-position sensitivity
    # Examples: ى (alif maqsurah U+0649), ة (taa marbuta U+0629)

    COMPLEX_GLYPH = "complex_glyph"
    # Glyphs requiring decomposition before coordinates
    # Strategy: Decomposition gate required
    # Examples: آ (alif with madda U+0622), لا (lam-alif ligature U+FEFB)

    PUNCTUATION = "punctuation"
    # Arabic punctuation marks
    # Strategy: NO phonetic coordinates
    # Examples: ، (comma), ؛ (semicolon), ؟ (question mark)

    BOUNDARY = "boundary"
    # Whitespace, line breaks
    # Strategy: NO coordinates, boundary evidence only
    # Example: space, newline

    RESIDUAL = "residual"
    # Unclassified or unknown glyph
    # Strategy: Defer to residual handling


@dataclass(frozen=True)
class GlyphClassification:
    """
    Result of glyph classification with evidence.
    """
    codepoint: int
    glyph_class: GlyphClass
    requires_decomposition: bool
    requires_role_disambiguation: bool
    allows_phonetic_coordinates: bool
    evidence_source: str = "glyph_classification_registry"


# Core Arabic Letters (25 letters)
# Simple letters with direct phonetic coordinates
CORE_ARABIC_LETTERS: frozenset[int] = frozenset({
    0x0628,  # ب BAA
    0x062A,  # ت TAA
    0x062B,  # ث THAA
    0x062C,  # ج JEEM
    0x062D,  # ح HAA
    0x062E,  # خ KHAA
    0x062F,  # د DAL
    0x0630,  # ذ THAAL
    0x0631,  # ر RAA
    0x0632,  # ز ZAY
    0x0633,  # س SEEN
    0x0634,  # ش SHEEN
    0x0635,  # ص SAAD
    0x0636,  # ض DAAD
    0x0637,  # ط TAA_EMPHATIC
    0x0638,  # ظ DHAA
    0x0639,  # ع AYN
    0x063A,  # غ GHAYN
    0x0641,  # ف FAA
    0x0642,  # ق QAF
    0x0643,  # ك KAF
    0x0644,  # ل LAM
    0x0645,  # م MEEM
    0x0646,  # ن NOON
    0x0647,  # ه HAA
    # Note: و ي ا excluded (weak letters, context-dependent)
})


# Hamza Seat Glyphs (5 forms)
# Require decomposition into hamza + seat
HAMZA_SEAT_GLYPHS: frozenset[int] = frozenset({
    0x0621,  # ء Standalone hamza
    0x0623,  # أ Alif with hamza above
    0x0624,  # ؤ Waw with hamza
    0x0625,  # إ Alif with hamza below
    0x0626,  # ئ Yaa with hamza
})


# Weak Letter Glyphs (3 letters)
# Context-dependent classification, multiple potential roles
WEAK_LETTER_GLYPHS: frozenset[int] = frozenset({
    0x0627,  # ا Alif
    0x0648,  # و Waw
    0x064A,  # ي Yaa
})


# Orthographic Variants (2 forms)
# Special coordinate handling
ORTHOGRAPHIC_VARIANTS: frozenset[int] = frozenset({
    0x0629,  # ة Taa marbuta
    0x0649,  # ى Alif maqsurah
})


# Complex Glyphs (composite forms)
# Require decomposition before coordinates
COMPLEX_GLYPHS: frozenset[int] = frozenset({
    0x0622,  # آ Alif with madda above (madda = hamza + alif)
    # Note: Lam-alif ligatures (U+FEF5-FEFB) can be added when needed
})


# Tatweel (spacing glyph)
TATWEEL_GLYPH: int = 0x0640  # ـ


# Arabic Punctuation
ARABIC_PUNCTUATION: frozenset[int] = frozenset({
    0x060C,  # ، Arabic comma
    0x061B,  # ؛ Arabic semicolon
    0x061F,  # ؟ Arabic question mark
})


def classify_glyph(codepoint: int) -> GlyphClassification:
    """
    Classify glyph type BEFORE coordinate assignment.

    This is the canonical API for glyph classification.

    Args:
        codepoint: Unicode codepoint

    Returns:
        GlyphClassification with class and processing requirements

    Example:
        >>> classification = classify_glyph(0x0628)  # BAA
        >>> classification.glyph_class
        GlyphClass.CORE_ARABIC_LETTER
        >>> classification.allows_phonetic_coordinates
        True

        >>> classification = classify_glyph(0x0640)  # TATWEEL
        >>> classification.glyph_class
        GlyphClass.TATWEEL_GLYPH
        >>> classification.allows_phonetic_coordinates
        False
    """
    # Core Arabic Letters
    if codepoint in CORE_ARABIC_LETTERS:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.CORE_ARABIC_LETTER,
            requires_decomposition=False,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=True,
        )

    # Hamza Seat Glyphs
    if codepoint in HAMZA_SEAT_GLYPHS:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.HAMZA_SEAT_GLYPH,
            requires_decomposition=True,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=True,  # After decomposition
        )

    # Weak Letter Glyphs
    if codepoint in WEAK_LETTER_GLYPHS:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.WEAK_LETTER_GLYPH,
            requires_decomposition=False,
            requires_role_disambiguation=True,
            allows_phonetic_coordinates=True,  # Context-dependent
        )

    # Tatweel
    if codepoint == TATWEEL_GLYPH:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.TATWEEL_GLYPH,
            requires_decomposition=False,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=False,  # NOT a letter
        )

    # Orthographic Variants
    if codepoint in ORTHOGRAPHIC_VARIANTS:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.ORTHOGRAPHIC_VARIANT,
            requires_decomposition=False,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=True,  # Special handling
        )

    # Complex Glyphs
    if codepoint in COMPLEX_GLYPHS:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.COMPLEX_GLYPH,
            requires_decomposition=True,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=True,  # After decomposition
        )

    # Punctuation
    if codepoint in ARABIC_PUNCTUATION:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.PUNCTUATION,
            requires_decomposition=False,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=False,
        )

    # Boundaries (space, newline, etc.)
    if codepoint in {0x0020, 0x000A, 0x000D}:
        return GlyphClassification(
            codepoint=codepoint,
            glyph_class=GlyphClass.BOUNDARY,
            requires_decomposition=False,
            requires_role_disambiguation=False,
            allows_phonetic_coordinates=False,
        )

    # Unknown/Residual
    return GlyphClassification(
        codepoint=codepoint,
        glyph_class=GlyphClass.RESIDUAL,
        requires_decomposition=False,
        requires_role_disambiguation=False,
        allows_phonetic_coordinates=False,
    )


def is_core_letter(codepoint: int) -> bool:
    """
    Check if codepoint is a core Arabic letter.

    Core letters have direct 1:1 phonetic mappings.

    Args:
        codepoint: Unicode codepoint

    Returns:
        True if core letter, False otherwise
    """
    return codepoint in CORE_ARABIC_LETTERS


def requires_decomposition(codepoint: int) -> bool:
    """
    Check if glyph requires decomposition before coordinates.

    Args:
        codepoint: Unicode codepoint

    Returns:
        True if decomposition required, False otherwise
    """
    return codepoint in HAMZA_SEAT_GLYPHS or codepoint in COMPLEX_GLYPHS


# Registry metadata for source-of-truth compliance
REGISTRY_METADATA = {
    "truth_type": "classification",
    "truth_name": "glyph_classification",
    "canonical_source": "src/qiyas_core/registries/glyph_classification_registry.py",
    "domain": "controlled_vocalized_arabic",
    "evidence_rank": "FORMAL_STRUCTURE",
    "forbidden_duplicates": [
        "src/qiyas_core/letter_identity_adapter.py",
        "src/qiyas_core/letter_coordinate_adapter.py",
        "src/qiyas_core/gates/",  # Future gates import, not redefine
    ],
}
