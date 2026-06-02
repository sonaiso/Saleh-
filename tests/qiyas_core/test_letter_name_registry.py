"""
Tests for Letter Name Registry

Constitutional Compliance Tests:
  - Verify single source of truth
  - Verify all 28+ Arabic letters covered
  - Verify Latin/Arabic name consistency
  - Verify no duplication in adapters
"""

import pytest

from qiyas_core.registries.letter_name_registry import (
    ARABIC_LETTER_NAMES,
    LATIN_LETTER_NAMES,
    get_letter_names,
    is_known_arabic_letter,
    LetterNames,
    REGISTRY_METADATA,
)


class TestLetterNameRegistryCompleteness:
    """Test that registry is complete and consistent."""

    def test_registry_has_28_classical_letters(self):
        """Verify all 28 classical Arabic letters are present."""
        # Classical 28 letters
        classical_letters = {
            0x0627,  # alif
            0x0628,  # baa
            0x062A,  # taa
            0x062B,  # thaa
            0x062C,  # jeem
            0x062D,  # haa
            0x062E,  # khaa
            0x062F,  # dal
            0x0630,  # thaal
            0x0631,  # raa
            0x0632,  # zay
            0x0633,  # seen
            0x0634,  # sheen
            0x0635,  # saad
            0x0636,  # daad
            0x0637,  # taa_emphatic
            0x0638,  # dhaa
            0x0639,  # ayn
            0x063A,  # ghayn
            0x0641,  # faa
            0x0642,  # qaf
            0x0643,  # kaf
            0x0644,  # lam
            0x0645,  # meem
            0x0646,  # noon
            0x0647,  # haa_final
            0x0648,  # waw
            0x064A,  # yaa
        }

        for letter_cp in classical_letters:
            assert letter_cp in LATIN_LETTER_NAMES, \
                f"Classical letter U+{letter_cp:04X} missing from LATIN_LETTER_NAMES"
            assert letter_cp in ARABIC_LETTER_NAMES, \
                f"Classical letter U+{letter_cp:04X} missing from ARABIC_LETTER_NAMES"

    def test_latin_and_arabic_registries_have_same_keys(self):
        """Verify Latin and Arabic registries cover same letters."""
        assert set(LATIN_LETTER_NAMES.keys()) == set(ARABIC_LETTER_NAMES.keys()), \
            "Latin and Arabic name registries must have identical keys"

    def test_no_empty_names(self):
        """Verify no letter has empty name."""
        for codepoint, name in LATIN_LETTER_NAMES.items():
            assert name and len(name) > 0, \
                f"Empty Latin name for U+{codepoint:04X}"

        for codepoint, name in ARABIC_LETTER_NAMES.items():
            assert name and len(name) > 0, \
                f"Empty Arabic name for U+{codepoint:04X}"

    def test_letter_names_are_lowercase(self):
        """Verify Latin names use lowercase convention."""
        for codepoint, name in LATIN_LETTER_NAMES.items():
            # Allow underscores, but check alphabetic parts are lowercase
            alpha_parts = [part for part in name.split('_') if part.isalpha()]
            for part in alpha_parts:
                assert part.islower(), \
                    f"Latin name '{name}' for U+{codepoint:04X} should be lowercase"


class TestGetLetterNames:
    """Test get_letter_names() API."""

    def test_get_letter_names_baa(self):
        """Test getting names for BAA."""
        names = get_letter_names(0x0628)

        assert names is not None
        assert isinstance(names, LetterNames)
        assert names.latin_name == "baa"
        assert names.arabic_name == "باء"
        assert names.codepoint == 0x0628

    def test_get_letter_names_taa(self):
        """Test getting names for TAA."""
        names = get_letter_names(0x062A)

        assert names is not None
        assert names.latin_name == "taa"
        assert names.arabic_name == "تاء"
        assert names.codepoint == 0x062A

    def test_get_letter_names_seen(self):
        """Test getting names for SEEN."""
        names = get_letter_names(0x0633)

        assert names is not None
        assert names.latin_name == "seen"
        assert names.arabic_name == "سين"
        assert names.codepoint == 0x0633

    def test_get_letter_names_kaf(self):
        """Test getting names for KAF."""
        names = get_letter_names(0x0643)

        assert names is not None
        assert names.latin_name == "kaf"
        assert names.arabic_name == "كاف"
        assert names.codepoint == 0x0643

    def test_get_letter_names_unknown_returns_none(self):
        """Test that unknown codepoint returns None."""
        names = get_letter_names(0x0041)  # Latin 'A'
        assert names is None

        names = get_letter_names(0x9999)  # Invalid
        assert names is None

    def test_get_letter_names_hamza_forms(self):
        """Test hamza and its various seats."""
        # Standalone hamza
        names = get_letter_names(0x0621)
        assert names is not None
        assert names.latin_name == "hamza"

        # Alif with hamza above
        names = get_letter_names(0x0623)
        assert names is not None
        assert names.latin_name == "alif_hamza_above"

        # Waw with hamza
        names = get_letter_names(0x0624)
        assert names is not None
        assert names.latin_name == "waw_hamza"

    def test_get_letter_names_orthographic_variants(self):
        """Test orthographic variants."""
        # Taa marbuta
        names = get_letter_names(0x0629)
        assert names is not None
        assert names.latin_name == "taa_marbuta"

        # Alif maqsurah
        names = get_letter_names(0x0649)
        assert names is not None
        assert names.latin_name == "alif_maksura"


class TestIsKnownArabicLetter:
    """Test is_known_arabic_letter() API."""

    def test_known_letters_return_true(self):
        """Test that known letters return True."""
        assert is_known_arabic_letter(0x0628) is True  # baa
        assert is_known_arabic_letter(0x062A) is True  # taa
        assert is_known_arabic_letter(0x0633) is True  # seen
        assert is_known_arabic_letter(0x0643) is True  # kaf

    def test_unknown_codepoints_return_false(self):
        """Test that unknown codepoints return False."""
        assert is_known_arabic_letter(0x0041) is False  # Latin 'A'
        assert is_known_arabic_letter(0x9999) is False  # Invalid
        assert is_known_arabic_letter(0x0020) is False  # Space

    def test_all_registered_letters_are_known(self):
        """Verify is_known_arabic_letter consistent with registry."""
        for codepoint in LATIN_LETTER_NAMES.keys():
            assert is_known_arabic_letter(codepoint) is True, \
                f"Registered letter U+{codepoint:04X} should be known"


class TestRegistryMetadata:
    """Test registry metadata for source-of-truth compliance."""

    def test_metadata_has_required_fields(self):
        """Verify metadata has all required fields."""
        assert "truth_type" in REGISTRY_METADATA
        assert "truth_name" in REGISTRY_METADATA
        assert "canonical_source" in REGISTRY_METADATA
        assert "domain" in REGISTRY_METADATA
        assert "evidence_rank" in REGISTRY_METADATA
        assert "forbidden_duplicates" in REGISTRY_METADATA

    def test_metadata_truth_type_is_identity(self):
        """Verify this is an identity truth."""
        assert REGISTRY_METADATA["truth_type"] == "identity"

    def test_metadata_domain_is_controlled_arabic(self):
        """Verify domain is controlled vocalized Arabic."""
        assert REGISTRY_METADATA["domain"] == "controlled_vocalized_arabic"

    def test_metadata_canonical_source_path_correct(self):
        """Verify canonical source path is correct."""
        assert "src/qiyas_core/registries/letter_name_registry.py" in \
            REGISTRY_METADATA["canonical_source"]

    def test_metadata_forbids_adapter_duplication(self):
        """Verify adapters are forbidden from duplicating this truth."""
        forbidden = REGISTRY_METADATA["forbidden_duplicates"]
        assert "src/qiyas_core/letter_identity_adapter.py" in forbidden, \
            "letter_identity_adapter.py must import, not duplicate"


class TestConstitutionalCompliance:
    """Test constitutional requirements."""

    def test_letter_names_frozen(self):
        """Verify LetterNames dataclass is frozen."""
        names = get_letter_names(0x0628)
        assert names is not None

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            names.latin_name = "modified"

    def test_registry_coverage_matches_abjad_system(self):
        """Verify registry covers same letters as Abjad system."""
        # Import Abjad system to verify consistency
        from qiyas_core.abjad_system import ABJAD_VALUES

        # All letters with Abjad values should have names
        for codepoint in ABJAD_VALUES.keys():
            assert is_known_arabic_letter(codepoint), \
                f"Letter with Abjad value U+{codepoint:04X} missing from name registry"

    def test_no_semantic_force_in_names(self):
        """Verify names are identity only, not semantic."""
        # Names should be neutral identifiers, not semantic descriptions
        for codepoint, name in LATIN_LETTER_NAMES.items():
            # Should not contain semantic words like "meaning", "hukm", etc.
            assert "meaning" not in name.lower()
            assert "hukm" not in name.lower()
            assert "semantic" not in name.lower()
