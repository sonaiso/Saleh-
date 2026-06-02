"""
Tests for Glyph Classification Registry

Constitutional Compliance Tests:
  - Verify glyph taxonomy completeness
  - Verify classification logic correctness
  - Verify decomposition requirements
  - Verify phonetic coordinate allowance rules
"""

import pytest

from qiyas_core.registries.glyph_classification_registry import (
    GlyphClass,
    GlyphClassification,
    CORE_ARABIC_LETTERS,
    STANDALONE_HAMZA,
    HAMZA_SEAT_GLYPHS,
    WEAK_LETTER_GLYPHS,
    ORTHOGRAPHIC_VARIANTS,
    COMPLEX_GLYPHS,
    TATWEEL_GLYPH,
    ARABIC_PUNCTUATION,
    classify_glyph,
    is_core_letter,
    requires_decomposition,
    REGISTRY_METADATA,
)


class TestCoreArabicLetters:
    """Test core Arabic letter classification."""

    def test_core_letters_count(self):
        """Verify 25 core letters (28 classical minus 3 weak)."""
        assert len(CORE_ARABIC_LETTERS) == 25

    def test_weak_letters_excluded_from_core(self):
        """Verify و ي ا not in core letters (context-dependent)."""
        assert 0x0627 not in CORE_ARABIC_LETTERS  # alif
        assert 0x0648 not in CORE_ARABIC_LETTERS  # waw
        assert 0x064A not in CORE_ARABIC_LETTERS  # yaa

    def test_baa_is_core_letter(self):
        """Test BAA is core letter."""
        assert 0x0628 in CORE_ARABIC_LETTERS
        assert is_core_letter(0x0628) is True

        classification = classify_glyph(0x0628)
        assert classification.glyph_class == GlyphClass.CORE_ARABIC_LETTER
        assert classification.allows_phonetic_coordinates is True
        assert classification.requires_decomposition is False

    def test_taa_is_core_letter(self):
        """Test TAA is core letter."""
        assert 0x062A in CORE_ARABIC_LETTERS
        assert is_core_letter(0x062A) is True

        classification = classify_glyph(0x062A)
        assert classification.glyph_class == GlyphClass.CORE_ARABIC_LETTER

    def test_seen_is_core_letter(self):
        """Test SEEN is core letter."""
        assert 0x0633 in CORE_ARABIC_LETTERS
        assert is_core_letter(0x0633) is True

        classification = classify_glyph(0x0633)
        assert classification.glyph_class == GlyphClass.CORE_ARABIC_LETTER

    def test_kaf_is_core_letter(self):
        """Test KAF is core letter."""
        assert 0x0643 in CORE_ARABIC_LETTERS
        assert is_core_letter(0x0643) is True

        classification = classify_glyph(0x0643)
        assert classification.glyph_class == GlyphClass.CORE_ARABIC_LETTER


class TestHamzaSeatGlyphs:
    """Test hamza seat glyph classification."""

    def test_hamza_seat_count(self):
        """Verify 4 hamza seat forms (standalone hamza excluded)."""
        assert len(HAMZA_SEAT_GLYPHS) == 4

    def test_standalone_hamza_classification(self):
        """Test standalone hamza U+0621 as separate class."""
        # Standalone hamza is NOT a seat glyph
        assert 0x0621 not in HAMZA_SEAT_GLYPHS
        assert 0x0621 == STANDALONE_HAMZA

        classification = classify_glyph(0x0621)
        assert classification.glyph_class == GlyphClass.STANDALONE_HAMZA
        assert classification.requires_decomposition is False  # It's atomic
        assert classification.allows_phonetic_coordinates is True

    def test_alif_hamza_above_classification(self):
        """Test alif with hamza above U+0623."""
        assert 0x0623 in HAMZA_SEAT_GLYPHS

        classification = classify_glyph(0x0623)
        assert classification.glyph_class == GlyphClass.HAMZA_SEAT_GLYPH
        assert classification.requires_decomposition is True

    def test_waw_hamza_classification(self):
        """Test waw with hamza U+0624."""
        assert 0x0624 in HAMZA_SEAT_GLYPHS

        classification = classify_glyph(0x0624)
        assert classification.glyph_class == GlyphClass.HAMZA_SEAT_GLYPH
        assert classification.requires_decomposition is True

    def test_alif_hamza_below_classification(self):
        """Test alif with hamza below U+0625."""
        assert 0x0625 in HAMZA_SEAT_GLYPHS

        classification = classify_glyph(0x0625)
        assert classification.glyph_class == GlyphClass.HAMZA_SEAT_GLYPH

    def test_yaa_hamza_classification(self):
        """Test yaa with hamza U+0626."""
        assert 0x0626 in HAMZA_SEAT_GLYPHS

        classification = classify_glyph(0x0626)
        assert classification.glyph_class == GlyphClass.HAMZA_SEAT_GLYPH


class TestWeakLetterGlyphs:
    """Test weak letter (context-dependent) classification."""

    def test_weak_letter_count(self):
        """Verify 3 weak letters (alif, waw, yaa)."""
        assert len(WEAK_LETTER_GLYPHS) == 3

    def test_alif_is_weak_letter(self):
        """Test alif U+0627 is weak letter."""
        assert 0x0627 in WEAK_LETTER_GLYPHS

        classification = classify_glyph(0x0627)
        assert classification.glyph_class == GlyphClass.WEAK_LETTER_GLYPH
        assert classification.requires_role_disambiguation is True
        assert classification.requires_decomposition is False
        assert classification.allows_phonetic_coordinates is True

    def test_waw_is_weak_letter(self):
        """Test waw U+0648 is weak letter."""
        assert 0x0648 in WEAK_LETTER_GLYPHS

        classification = classify_glyph(0x0648)
        assert classification.glyph_class == GlyphClass.WEAK_LETTER_GLYPH
        assert classification.requires_role_disambiguation is True

    def test_yaa_is_weak_letter(self):
        """Test yaa U+064A is weak letter."""
        assert 0x064A in WEAK_LETTER_GLYPHS

        classification = classify_glyph(0x064A)
        assert classification.glyph_class == GlyphClass.WEAK_LETTER_GLYPH
        assert classification.requires_role_disambiguation is True


class TestTatweelGlyph:
    """Test tatweel (spacing) classification."""

    def test_tatweel_classification(self):
        """Test tatweel U+0640 is NOT a letter."""
        assert TATWEEL_GLYPH == 0x0640

        classification = classify_glyph(0x0640)
        assert classification.glyph_class == GlyphClass.TATWEEL_GLYPH
        assert classification.allows_phonetic_coordinates is False
        assert classification.requires_decomposition is False
        assert classification.requires_role_disambiguation is False

    def test_tatweel_not_core_letter(self):
        """Verify tatweel is NOT a core letter."""
        assert TATWEEL_GLYPH not in CORE_ARABIC_LETTERS
        assert is_core_letter(TATWEEL_GLYPH) is False


class TestOrthographicVariants:
    """Test orthographic variant classification."""

    def test_orthographic_variant_count(self):
        """Verify 2 orthographic variants."""
        assert len(ORTHOGRAPHIC_VARIANTS) == 2

    def test_taa_marbuta_classification(self):
        """Test taa marbuta U+0629."""
        assert 0x0629 in ORTHOGRAPHIC_VARIANTS

        classification = classify_glyph(0x0629)
        assert classification.glyph_class == GlyphClass.ORTHOGRAPHIC_VARIANT
        assert classification.allows_phonetic_coordinates is True
        assert classification.requires_decomposition is False

    def test_alif_maqsurah_classification(self):
        """Test alif maqsurah U+0649."""
        assert 0x0649 in ORTHOGRAPHIC_VARIANTS

        classification = classify_glyph(0x0649)
        assert classification.glyph_class == GlyphClass.ORTHOGRAPHIC_VARIANT


class TestComplexGlyphs:
    """Test complex glyph classification."""

    def test_alif_madda_classification(self):
        """Test alif with madda U+0622."""
        assert 0x0622 in COMPLEX_GLYPHS

        classification = classify_glyph(0x0622)
        assert classification.glyph_class == GlyphClass.COMPLEX_GLYPH
        assert classification.requires_decomposition is True
        assert classification.allows_phonetic_coordinates is True

    def test_complex_glyph_requires_decomposition(self):
        """Verify complex glyphs require decomposition."""
        assert requires_decomposition(0x0622) is True


class TestPunctuation:
    """Test punctuation classification."""

    def test_arabic_comma_classification(self):
        """Test Arabic comma U+060C."""
        assert 0x060C in ARABIC_PUNCTUATION

        classification = classify_glyph(0x060C)
        assert classification.glyph_class == GlyphClass.PUNCTUATION
        assert classification.allows_phonetic_coordinates is False

    def test_arabic_semicolon_classification(self):
        """Test Arabic semicolon U+061B."""
        assert 0x061B in ARABIC_PUNCTUATION

        classification = classify_glyph(0x061B)
        assert classification.glyph_class == GlyphClass.PUNCTUATION

    def test_arabic_question_mark_classification(self):
        """Test Arabic question mark U+061F."""
        assert 0x061F in ARABIC_PUNCTUATION

        classification = classify_glyph(0x061F)
        assert classification.glyph_class == GlyphClass.PUNCTUATION


class TestBoundaries:
    """Test boundary classification."""

    def test_space_classification(self):
        """Test space U+0020 is boundary."""
        classification = classify_glyph(0x0020)
        assert classification.glyph_class == GlyphClass.BOUNDARY
        assert classification.allows_phonetic_coordinates is False

    def test_newline_classification(self):
        """Test newline U+000A is boundary."""
        classification = classify_glyph(0x000A)
        assert classification.glyph_class == GlyphClass.BOUNDARY


class TestResidual:
    """Test residual (unknown) classification."""

    def test_unknown_codepoint_classification(self):
        """Test unknown codepoint classified as residual."""
        classification = classify_glyph(0x9999)
        assert classification.glyph_class == GlyphClass.RESIDUAL
        assert classification.allows_phonetic_coordinates is False

    def test_latin_letter_classification(self):
        """Test Latin letter classified as residual."""
        classification = classify_glyph(0x0041)  # 'A'
        assert classification.glyph_class == GlyphClass.RESIDUAL


class TestRequiresDecomposition:
    """Test requires_decomposition() utility."""

    def test_hamza_seat_requires_decomposition(self):
        """Verify hamza seats require decomposition (standalone hamza does NOT)."""
        assert requires_decomposition(0x0621) is False  # standalone hamza is atomic
        assert requires_decomposition(0x0623) is True  # alif hamza above
        assert requires_decomposition(0x0624) is True  # waw hamza

    def test_complex_glyph_requires_decomposition(self):
        """Verify complex glyphs require decomposition."""
        assert requires_decomposition(0x0622) is True  # alif madda

    def test_core_letter_does_not_require_decomposition(self):
        """Verify core letters do not require decomposition."""
        assert requires_decomposition(0x0628) is False  # baa
        assert requires_decomposition(0x062A) is False  # taa
        assert requires_decomposition(0x0633) is False  # seen


class TestGlyphClassificationDataclass:
    """Test GlyphClassification dataclass."""

    def test_classification_frozen(self):
        """Verify GlyphClassification is frozen."""
        classification = classify_glyph(0x0628)

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            classification.glyph_class = GlyphClass.RESIDUAL

    def test_classification_has_all_fields(self):
        """Verify classification has all required fields."""
        classification = classify_glyph(0x0628)

        assert hasattr(classification, "codepoint")
        assert hasattr(classification, "glyph_class")
        assert hasattr(classification, "requires_decomposition")
        assert hasattr(classification, "requires_role_disambiguation")
        assert hasattr(classification, "allows_phonetic_coordinates")
        assert hasattr(classification, "evidence_source")

    def test_evidence_source_is_registry(self):
        """Verify evidence source is registry."""
        classification = classify_glyph(0x0628)
        assert "glyph_classification_registry" in classification.evidence_source


class TestRegistryMetadata:
    """Test registry metadata for source-of-truth compliance."""

    def test_metadata_has_required_fields(self):
        """Verify metadata has all required fields."""
        assert "truth_type" in REGISTRY_METADATA
        assert "truth_name" in REGISTRY_METADATA
        assert "canonical_source" in REGISTRY_METADATA
        assert "domain" in REGISTRY_METADATA
        assert "evidence_rank" in REGISTRY_METADATA

    def test_metadata_truth_type_is_classification(self):
        """Verify this is a classification truth."""
        assert REGISTRY_METADATA["truth_type"] == "classification"

    def test_metadata_canonical_source_correct(self):
        """Verify canonical source path."""
        assert "src/qiyas_core/registries/glyph_classification_registry.py" in \
            REGISTRY_METADATA["canonical_source"]


class TestConstitutionalCompliance:
    """Test constitutional requirements."""

    def test_no_layer_jump_to_coordinates(self):
        """Verify classification happens BEFORE coordinates."""
        # Classification should not produce coordinates
        classification = classify_glyph(0x0628)

        assert not hasattr(classification, "makhraj_coordinate")
        assert not hasattr(classification, "sifat_vector")
        assert not hasattr(classification, "abjad_coordinate")

    def test_tatweel_explicitly_forbidden_coordinates(self):
        """Verify tatweel explicitly forbidden from coordinates."""
        classification = classify_glyph(TATWEEL_GLYPH)
        assert classification.allows_phonetic_coordinates is False

    def test_punctuation_forbidden_coordinates(self):
        """Verify punctuation forbidden from coordinates."""
        for punct_cp in ARABIC_PUNCTUATION:
            classification = classify_glyph(punct_cp)
            assert classification.allows_phonetic_coordinates is False

    def test_boundaries_forbidden_coordinates(self):
        """Verify boundaries forbidden from coordinates."""
        classification = classify_glyph(0x0020)  # space
        assert classification.allows_phonetic_coordinates is False
