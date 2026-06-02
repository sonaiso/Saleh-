"""
Qiyas Core Registries

Single source of truth for all identity and classification mappings.

Constitutional Requirement (SOURCE_OF_TRUTH_REGISTRY.md):
  - Each truth has ONE canonical source
  - No truth duplication across adapters
  - All consuming components must import from these registries

Registries in this module:
  - letter_name_registry: Letter name → identity mappings
  - glyph_classification_registry: Glyph type classification
  - letter_fariq_registry: Invalidating difference pairs
"""

from .letter_name_registry import (
    ARABIC_LETTER_NAMES,
    LATIN_LETTER_NAMES,
    get_letter_names,
    is_known_arabic_letter,
)
from .glyph_classification_registry import (
    GlyphClass,
    CORE_ARABIC_LETTERS,
    HAMZA_SEAT_GLYPHS,
    WEAK_LETTER_GLYPHS,
    ORTHOGRAPHIC_VARIANTS,
    COMPLEX_GLYPHS,
    classify_glyph,
    is_core_letter,
    requires_decomposition,
)
from .letter_fariq_registry import (
    LETTER_FARIQ_PAIRS,
    get_fariq_pairs,
    has_invalidating_difference,
)

__all__ = [
    # Letter names
    "ARABIC_LETTER_NAMES",
    "LATIN_LETTER_NAMES",
    "get_letter_names",
    "is_known_arabic_letter",
    # Glyph classification
    "GlyphClass",
    "CORE_ARABIC_LETTERS",
    "HAMZA_SEAT_GLYPHS",
    "WEAK_LETTER_GLYPHS",
    "ORTHOGRAPHIC_VARIANTS",
    "COMPLEX_GLYPHS",
    "classify_glyph",
    "is_core_letter",
    "requires_decomposition",
    # Letter fariq
    "LETTER_FARIQ_PAIRS",
    "get_fariq_pairs",
    "has_invalidating_difference",
]
