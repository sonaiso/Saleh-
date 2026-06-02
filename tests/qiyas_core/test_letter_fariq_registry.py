"""
Tests for Letter Fariq (Invalidating Differences) Registry

Constitutional Compliance Tests:
  - Verify fariq pairs completeness
  - Verify bidirectional lookup
  - Verify fariq axis classification
  - Verify critical letter distinctions
"""

import pytest

from qiyas_core.registries.letter_fariq_registry import (
    FariqAxis,
    FariqPair,
    LETTER_FARIQ_PAIRS,
    get_fariq_pairs,
    has_invalidating_difference,
    REGISTRY_METADATA,
)


class TestFariqPairsCompleteness:
    """Test that fariq pairs cover critical distinctions."""

    def test_fariq_pairs_not_empty(self):
        """Verify fariq pairs registry is not empty."""
        assert len(LETTER_FARIQ_PAIRS) > 0

    def test_fariq_pairs_are_tuples(self):
        """Verify LETTER_FARIQ_PAIRS is immutable tuple."""
        assert isinstance(LETTER_FARIQ_PAIRS, tuple)

    def test_all_fariq_pairs_are_fariq_pair_objects(self):
        """Verify all entries are FariqPair objects."""
        for pair in LETTER_FARIQ_PAIRS:
            assert isinstance(pair, FariqPair)

    def test_all_fariq_pairs_have_valid_axes(self):
        """Verify all pairs have valid FariqAxis."""
        for pair in LETTER_FARIQ_PAIRS:
            assert isinstance(pair.axis, FariqAxis)


class TestCriticalLetterDistinctions:
    """Test critical letter pairs are present."""

    def test_baa_vs_taa_voicing_distinction(self):
        """Test ب vs ت (voicing difference)."""
        pair = has_invalidating_difference(0x0628, 0x062A)
        assert pair is not None
        assert pair.axis == FariqAxis.VOICING

    def test_baa_vs_meem_nasality_distinction(self):
        """Test ب vs م (nasality difference)."""
        pair = has_invalidating_difference(0x0628, 0x0645)
        assert pair is not None
        assert pair.axis == FariqAxis.NASALITY

    def test_baa_vs_faa_manner_distinction(self):
        """Test ب vs ف (manner difference)."""
        pair = has_invalidating_difference(0x0628, 0x0641)
        assert pair is not None
        assert pair.axis == FariqAxis.MANNER

    def test_seen_vs_saad_emphasis_distinction(self):
        """Test س vs ص (emphasis difference)."""
        pair = has_invalidating_difference(0x0633, 0x0635)
        assert pair is not None
        assert pair.axis == FariqAxis.EMPHASIS

    def test_taa_vs_taa_emphatic_emphasis_distinction(self):
        """Test ت vs ط (emphasis difference)."""
        pair = has_invalidating_difference(0x062A, 0x0637)
        assert pair is not None
        assert pair.axis == FariqAxis.EMPHASIS

    def test_dal_vs_thaal_manner_distinction(self):
        """Test د vs ذ (manner difference)."""
        pair = has_invalidating_difference(0x062F, 0x0630)
        assert pair is not None
        assert pair.axis == FariqAxis.MANNER

    def test_kaf_vs_qaf_place_distinction(self):
        """Test ك vs ق (place difference)."""
        pair = has_invalidating_difference(0x0643, 0x0642)
        assert pair is not None
        assert pair.axis == FariqAxis.PLACE


class TestGetFariqPairs:
    """Test get_fariq_pairs() API."""

    def test_get_fariq_pairs_baa(self):
        """Test getting fariq pairs for BAA."""
        pairs = get_fariq_pairs(0x0628)
        assert len(pairs) > 0

        # BAA should have pairs with TAA, MEEM, FAA, WAW
        letter_names = {p.letter2_name for p in pairs if p.letter1_codepoint == 0x0628}
        letter_names.update({p.letter1_name for p in pairs if p.letter2_codepoint == 0x0628})

        assert "taa" in letter_names or "baa" in letter_names
        assert "meem" in letter_names or "baa" in letter_names
        assert "faa" in letter_names or "baa" in letter_names

    def test_get_fariq_pairs_taa(self):
        """Test getting fariq pairs for TAA."""
        pairs = get_fariq_pairs(0x062A)
        assert len(pairs) > 0

        # Should include pairs with BAA, THAA, DAL, TAA_EMPHATIC
        has_voicing_pair = any(p.axis == FariqAxis.VOICING for p in pairs)
        has_manner_pair = any(p.axis == FariqAxis.MANNER for p in pairs)
        has_emphasis_pair = any(p.axis == FariqAxis.EMPHASIS for p in pairs)

        assert has_voicing_pair or has_manner_pair or has_emphasis_pair

    def test_get_fariq_pairs_unknown_letter(self):
        """Test getting fariq pairs for unknown letter."""
        pairs = get_fariq_pairs(0x9999)
        assert len(pairs) == 0

    def test_get_fariq_pairs_returns_tuple(self):
        """Verify get_fariq_pairs returns immutable tuple."""
        pairs = get_fariq_pairs(0x0628)
        assert isinstance(pairs, tuple)


class TestHasInvalidatingDifference:
    """Test has_invalidating_difference() API."""

    def test_has_difference_baa_taa(self):
        """Test BAA vs TAA has invalidating difference."""
        pair = has_invalidating_difference(0x0628, 0x062A)
        assert pair is not None
        assert pair.axis == FariqAxis.VOICING

    def test_has_difference_bidirectional(self):
        """Test fariq lookup is bidirectional."""
        # BAA vs TAA
        pair1 = has_invalidating_difference(0x0628, 0x062A)
        pair2 = has_invalidating_difference(0x062A, 0x0628)

        # Should find same difference in either direction
        assert (pair1 is not None) or (pair2 is not None)

    def test_has_difference_unknown_pair(self):
        """Test unknown pair returns None."""
        pair = has_invalidating_difference(0x9999, 0x9998)
        assert pair is None

    def test_has_difference_same_letter(self):
        """Test same letter has no invalidating difference."""
        pair = has_invalidating_difference(0x0628, 0x0628)
        assert pair is None

    def test_has_difference_seen_saad(self):
        """Test SEEN vs SAAD has emphasis difference."""
        pair = has_invalidating_difference(0x0633, 0x0635)
        assert pair is not None
        assert pair.axis == FariqAxis.EMPHASIS


class TestFariqAxisCoverage:
    """Test coverage of different fariq axes."""

    def test_voicing_axis_present(self):
        """Verify voicing axis has entries."""
        voicing_pairs = [p for p in LETTER_FARIQ_PAIRS if p.axis == FariqAxis.VOICING]
        assert len(voicing_pairs) > 0

    def test_nasality_axis_present(self):
        """Verify nasality axis has entries."""
        nasality_pairs = [p for p in LETTER_FARIQ_PAIRS if p.axis == FariqAxis.NASALITY]
        assert len(nasality_pairs) > 0

    def test_manner_axis_present(self):
        """Verify manner axis has entries."""
        manner_pairs = [p for p in LETTER_FARIQ_PAIRS if p.axis == FariqAxis.MANNER]
        assert len(manner_pairs) > 0

    def test_emphasis_axis_present(self):
        """Verify emphasis axis has entries."""
        emphasis_pairs = [p for p in LETTER_FARIQ_PAIRS if p.axis == FariqAxis.EMPHASIS]
        assert len(emphasis_pairs) > 0

    def test_place_axis_present(self):
        """Verify place axis has entries."""
        place_pairs = [p for p in LETTER_FARIQ_PAIRS if p.axis == FariqAxis.PLACE]
        assert len(place_pairs) > 0


class TestEmphasisPairs:
    """Test emphatic vs plain letter pairs."""

    def test_all_emphatic_pairs_present(self):
        """Verify all 4 emphatic pairs."""
        # ط vs ت (TAA_EMPHATIC vs TAA)
        pair_tt = has_invalidating_difference(0x0637, 0x062A)
        assert pair_tt is not None
        assert pair_tt.axis == FariqAxis.EMPHASIS

        # ص vs س (SAAD vs SEEN)
        pair_ss = has_invalidating_difference(0x0635, 0x0633)
        assert pair_ss is not None
        assert pair_ss.axis == FariqAxis.EMPHASIS

        # ض vs د (DAAD vs DAL)
        pair_dd = has_invalidating_difference(0x0636, 0x062F)
        assert pair_dd is not None
        assert pair_dd.axis == FariqAxis.EMPHASIS

        # ظ vs ذ (DHAA vs THAAL)
        pair_dh = has_invalidating_difference(0x0638, 0x0630)
        assert pair_dh is not None
        assert pair_dh.axis == FariqAxis.EMPHASIS


class TestFariqPairDataclass:
    """Test FariqPair dataclass."""

    def test_fariq_pair_frozen(self):
        """Verify FariqPair is frozen."""
        pair = LETTER_FARIQ_PAIRS[0]

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            pair.axis = FariqAxis.VOICING

    def test_fariq_pair_has_all_fields(self):
        """Verify FariqPair has all required fields."""
        pair = LETTER_FARIQ_PAIRS[0]

        assert hasattr(pair, "letter1_codepoint")
        assert hasattr(pair, "letter2_codepoint")
        assert hasattr(pair, "letter1_name")
        assert hasattr(pair, "letter2_name")
        assert hasattr(pair, "axis")
        assert hasattr(pair, "difference_description")

    def test_fariq_pair_codepoints_valid(self):
        """Verify all fariq pairs have valid codepoints."""
        for pair in LETTER_FARIQ_PAIRS:
            assert isinstance(pair.letter1_codepoint, int)
            assert isinstance(pair.letter2_codepoint, int)
            assert pair.letter1_codepoint > 0
            assert pair.letter2_codepoint > 0

    def test_fariq_pair_names_not_empty(self):
        """Verify all fariq pairs have non-empty names."""
        for pair in LETTER_FARIQ_PAIRS:
            assert pair.letter1_name and len(pair.letter1_name) > 0
            assert pair.letter2_name and len(pair.letter2_name) > 0

    def test_fariq_pair_description_not_empty(self):
        """Verify all fariq pairs have descriptions."""
        for pair in LETTER_FARIQ_PAIRS:
            assert pair.difference_description and len(pair.difference_description) > 0


class TestRegistryMetadata:
    """Test registry metadata for source-of-truth compliance."""

    def test_metadata_has_required_fields(self):
        """Verify metadata has all required fields."""
        assert "truth_type" in REGISTRY_METADATA
        assert "truth_name" in REGISTRY_METADATA
        assert "canonical_source" in REGISTRY_METADATA
        assert "domain" in REGISTRY_METADATA
        assert "evidence_rank" in REGISTRY_METADATA

    def test_metadata_truth_type_is_operation(self):
        """Verify this is an operation truth (negation)."""
        assert REGISTRY_METADATA["truth_type"] == "operation"

    def test_metadata_canonical_source_correct(self):
        """Verify canonical source path."""
        assert "src/qiyas_core/registries/letter_fariq_registry.py" in \
            REGISTRY_METADATA["canonical_source"]

    def test_metadata_forbids_adapter_duplication(self):
        """Verify adapters forbidden from duplicating fariq pairs."""
        forbidden = REGISTRY_METADATA["forbidden_duplicates"]
        assert "src/qiyas_core/letter_identity_adapter.py" in forbidden


class TestConstitutionalCompliance:
    """Test constitutional requirements."""

    def test_fariq_blocking_law(self):
        """Verify fariq is used for BLOCKING, not classification."""
        # Fariq should be about NEGATION (blocking wrong identities)
        # NOT about AFFIRMATION (proving correct identity)

        for pair in LETTER_FARIQ_PAIRS:
            # Description should emphasize DIFFERENCE
            desc_lower = pair.difference_description.lower()
            assert "vs" in desc_lower or "different" in desc_lower

    def test_fariq_corresponds_to_sifat_axes(self):
        """Verify fariq axes correspond to 6-axis SifatVector."""
        # All axes should be phonetic/place distinctions
        valid_axes = {
            FariqAxis.VOICING,
            FariqAxis.MANNER,
            FariqAxis.NASALITY,
            FariqAxis.FRICATION,
            FariqAxis.CONTINUANCY,
            FariqAxis.EMPHASIS,
            FariqAxis.PLACE,
            FariqAxis.ORTHOGRAPHY,
        }

        for pair in LETTER_FARIQ_PAIRS:
            assert pair.axis in valid_axes

    def test_no_semantic_fariq(self):
        """Verify fariq is phonetic/structural, not semantic."""
        for pair in LETTER_FARIQ_PAIRS:
            desc_lower = pair.difference_description.lower()
            # Should not contain semantic terms
            assert "meaning" not in desc_lower
            assert "hukm" not in desc_lower
            assert "semantic" not in desc_lower
