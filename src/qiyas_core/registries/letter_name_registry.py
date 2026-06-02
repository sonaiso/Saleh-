"""
Letter Name Registry - Single Source of Truth

Constitutional Basis:
  - SOURCE_OF_TRUTH_REGISTRY.md § 4: "Letter name mapping" canonical source
  - CANONICAL_ARCHITECTURE_CONTROL_FRAME.md § 1.5: API Authority Principle

Purpose:
  This is the ONLY canonical source for letter name mappings.
  All adapters MUST import from this registry, NOT redefine locally.

Truth Type: Identity Truth
Domain: Controlled Vocalized Arabic
Evidence Rank: FORMAL_STRUCTURE

Forbidden:
  - DO NOT duplicate these mappings in adapters
  - DO NOT redefine in tests
  - DO NOT create parallel name sources

Consuming Components:
  - src/qiyas_core/letter_identity_adapter.py
  - src/qiyas_core/rules/letter_identity_rules.py
  - tests/qiyas_core/test_letter_identity_adapter.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LetterNames:
    """
    Complete letter name identity (Latin + Arabic).

    This preserves both naming systems without preference:
      - Latin name: for code/international reference
      - Arabic name: for native script identity
    """
    latin_name: str      # e.g., "baa", "taa", "seen"
    arabic_name: str     # e.g., "باء", "تاء", "سين"
    codepoint: int       # Unicode codepoint (e.g., 0x0628)


# Canonical mapping: Unicode codepoint → Latin letter name
# This is the single source of truth for Latin letter names
LATIN_LETTER_NAMES: dict[int, str] = {
    0x0621: "hamza",
    0x0622: "alif_madda",
    0x0623: "alif_hamza_above",
    0x0624: "waw_hamza",
    0x0625: "alif_hamza_below",
    0x0626: "yaa_hamza",
    0x0627: "alif",
    0x0628: "baa",
    0x0629: "taa_marbuta",
    0x062A: "taa",
    0x062B: "thaa",
    0x062C: "jeem",
    0x062D: "haa",
    0x062E: "khaa",
    0x062F: "dal",
    0x0630: "thaal",
    0x0631: "raa",
    0x0632: "zay",
    0x0633: "seen",
    0x0634: "sheen",
    0x0635: "saad",
    0x0636: "daad",
    0x0637: "taa_emphatic",
    0x0638: "dhaa",
    0x0639: "ayn",
    0x063A: "ghayn",
    0x0640: "tatweel",
    0x0641: "faa",
    0x0642: "qaf",
    0x0643: "kaf",
    0x0644: "lam",
    0x0645: "meem",
    0x0646: "noon",
    0x0647: "haa_final",
    0x0648: "waw",
    0x0649: "alif_maksura",
    0x064A: "yaa",
}


# Canonical mapping: Unicode codepoint → Arabic letter name
# This is the single source of truth for Arabic letter names
ARABIC_LETTER_NAMES: dict[int, str] = {
    0x0621: "همزة",
    0x0622: "ألف ممدودة",
    0x0623: "ألف بهمزة فوق",
    0x0624: "واو بهمزة",
    0x0625: "ألف بهمزة تحت",
    0x0626: "ياء بهمزة",
    0x0627: "ألف",
    0x0628: "باء",
    0x0629: "تاء مربوطة",
    0x062A: "تاء",
    0x062B: "ثاء",
    0x062C: "جيم",
    0x062D: "حاء",
    0x062E: "خاء",
    0x062F: "دال",
    0x0630: "ذال",
    0x0631: "راء",
    0x0632: "زاي",
    0x0633: "سين",
    0x0634: "شين",
    0x0635: "صاد",
    0x0636: "ضاد",
    0x0637: "طاء",
    0x0638: "ظاء",
    0x0639: "عين",
    0x063A: "غين",
    0x0640: "تطويل",
    0x0641: "فاء",
    0x0642: "قاف",
    0x0643: "كاف",
    0x0644: "لام",
    0x0645: "ميم",
    0x0646: "نون",
    0x0647: "هاء",
    0x0648: "واو",
    0x0649: "ألف مقصورة",
    0x064A: "ياء",
}


def get_letter_names(codepoint: int) -> LetterNames | None:
    """
    Get complete letter name identity (Latin + Arabic).

    This is the canonical API for letter name lookup.

    Args:
        codepoint: Unicode codepoint (e.g., 0x0628 for BAA)

    Returns:
        LetterNames with both Latin and Arabic names, or None if unknown

    Example:
        >>> names = get_letter_names(0x0628)
        >>> names.latin_name
        'baa'
        >>> names.arabic_name
        'باء'
    """
    latin = LATIN_LETTER_NAMES.get(codepoint)
    arabic = ARABIC_LETTER_NAMES.get(codepoint)

    if latin is None or arabic is None:
        return None

    return LetterNames(
        latin_name=latin,
        arabic_name=arabic,
        codepoint=codepoint
    )


def is_known_arabic_letter(codepoint: int) -> bool:
    """
    Check if codepoint is a known Arabic letter in this registry.

    Args:
        codepoint: Unicode codepoint

    Returns:
        True if letter is in canonical registry, False otherwise
    """
    return codepoint in LATIN_LETTER_NAMES


# Registry metadata for source-of-truth compliance
REGISTRY_METADATA = {
    "truth_type": "identity",
    "truth_name": "letter_name_mapping",
    "canonical_source": "src/qiyas_core/registries/letter_name_registry.py",
    "domain": "controlled_vocalized_arabic",
    "evidence_rank": "FORMAL_STRUCTURE",
    "forbidden_duplicates": [
        "src/qiyas_core/letter_identity_adapter.py",  # Must import, not redefine
        "src/qiyas_core/letter_coordinate_adapter.py",
        "src/qiyas_core/slot_adapter.py",
        "tests/qiyas_core/conftest.py",
    ],
}
