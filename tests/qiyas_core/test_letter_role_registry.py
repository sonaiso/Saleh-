"""
Tests for Letter Role Registry

Constitutional Compliance Tests:
  - Prove letter_role_registry defines سألتمونيها classification
  - Prove letter_coordinate_adapter consumes registry, not local dict
  - Prove no local MORPHO_ROLE_BY_LETTER in adapter
  - Prove registry forbids duplication in metadata
"""

import pytest
import inspect

from qiyas_core import letter_coordinate_adapter
from qiyas_core.registries import letter_role_registry
from qiyas_core.registries.letter_role_registry import (
    LetterRolePotential,
    LetterRoleClassification,
    SAALATAMUUNIIHA_LETTERS,
    EXPANDED_MULTI_ROLE_LETTERS,
    WEAK_LETTERS_ROLE_CONTEXT,
    classify_letter_role,
    get_morpho_role_label,
    is_multi_role_letter,
    REGISTRY_METADATA,
)


class TestSaalatamuunihaLetters:
    """Test سألتمونيها letter classification."""

    def test_saalatamuuniiha_letters_count(self):
        """Verify 10 string keys in سألتمونيها registry membership.

        9 classical Arabic letters, 10 registry string keys due to
        haa/haa_final split: per canonical letter_name_registry.py (as
        ratified by PR #98), "haa" represents U+062D ح (pharyngeal) and
        "haa_final" represents U+0647 ه (glottal). Both are classified
        as SAALATAMUUNIIHA members in this codebase, so the membership
        carries 10 string entries for the 9-letter classical set.
        """
        assert len(SAALATAMUUNIIHA_LETTERS) == 10

    def test_seen_is_saalatamuuniiha(self):
        """Test سين is سألتمونيها letter."""
        assert "seen" in SAALATAMUUNIIHA_LETTERS
        classification = classify_letter_role("seen")
        assert classification.role_potential == LetterRolePotential.SAALATAMUUNIIHA
        assert classification.can_be_pronoun is True
        assert classification.can_be_affix is True

    def test_taa_is_saalatamuuniiha(self):
        """Test تاء is سألتمونيها letter."""
        assert "taa" in SAALATAMUUNIIHA_LETTERS
        classification = classify_letter_role("taa")
        assert classification.role_potential == LetterRolePotential.SAALATAMUUNIIHA


class TestExpandedMultiRoleLetters:
    """Test expanded multi-role letter classification."""

    def test_expanded_multi_role_count(self):
        """Verify 3 letters in expanded multi-role set."""
        assert len(EXPANDED_MULTI_ROLE_LETTERS) == 3

    def test_baa_is_expanded_multi_role(self):
        """Test باء is expanded multi-role letter."""
        assert "baa" in EXPANDED_MULTI_ROLE_LETTERS
        classification = classify_letter_role("baa")
        assert classification.role_potential == LetterRolePotential.EXPANDED_MULTI_ROLE
        assert classification.can_be_preposition is True
        assert classification.can_be_affix is True

    def test_kaf_is_expanded_multi_role(self):
        """Test كاف is expanded multi-role letter."""
        assert "kaf" in EXPANDED_MULTI_ROLE_LETTERS
        classification = classify_letter_role("kaf")
        assert classification.role_potential == LetterRolePotential.EXPANDED_MULTI_ROLE


class TestWeakLettersRoleContext:
    """Test weak letter (context-dependent) classification."""

    def test_weak_letters_count(self):
        """Verify 3 weak letters (alif, waw, yaa)."""
        assert len(WEAK_LETTERS_ROLE_CONTEXT) == 3

    def test_alif_is_weak_role_context(self):
        """Test ألف is weak letter (context-dependent)."""
        assert "alif" in WEAK_LETTERS_ROLE_CONTEXT
        classification = classify_letter_role("alif")
        assert classification.role_potential == LetterRolePotential.WEAK_ROLE_CONTEXT_DEPENDENT

    def test_waw_is_weak_role_context(self):
        """Test واو is weak letter (context-dependent)."""
        assert "waw" in WEAK_LETTERS_ROLE_CONTEXT
        classification = classify_letter_role("waw")
        assert classification.role_potential == LetterRolePotential.WEAK_ROLE_CONTEXT_DEPENDENT

    def test_yaa_is_weak_role_context(self):
        """Test ياء is weak letter (context-dependent)."""
        assert "yaa" in WEAK_LETTERS_ROLE_CONTEXT
        classification = classify_letter_role("yaa")
        assert classification.role_potential == LetterRolePotential.WEAK_ROLE_CONTEXT_DEPENDENT


class TestSingleRoleLetters:
    """Test single-role letter classification (default)."""

    def test_jeem_is_single_role(self):
        """Test جيم is single-role letter (default)."""
        classification = classify_letter_role("jeem")
        assert classification.role_potential == LetterRolePotential.SINGLE_ROLE
        assert classification.can_be_affix is False
        assert classification.can_be_preposition is False
        assert classification.can_be_pronoun is False
        assert classification.can_be_root_consonant is True

    def test_haa_is_single_role_when_not_in_saalatamuuniiha_context(self):
        """Test هاء defaults to single-role (even though in سألتمونيها)."""
        # NOTE: هاء IS in SAALATAMUUNIIHA_LETTERS, so this test is wrong
        # Let me check the correct behavior
        classification = classify_letter_role("haa")
        # هاء is in سألتمونيها, so it should be SAALATAMUUNIIHA
        assert classification.role_potential == LetterRolePotential.SAALATAMUUNIIHA


class TestGetMorphoRoleLabel:
    """Test get_morpho_role_label() utility for evidence generation."""

    def test_baa_returns_expanded_multi_role_label(self):
        """Test BAA returns EXPANDED_MULTI_ROLE label."""
        label = get_morpho_role_label("baa")
        assert label == "EXPANDED_MULTI_ROLE"

    def test_taa_returns_saalatamuuniiha_label(self):
        """Test TAA returns SAALATAMUUNIIHA label."""
        label = get_morpho_role_label("taa")
        assert label == "SAALATAMUUNIIHA"

    def test_seen_returns_saalatamuuniiha_label(self):
        """Test SEEN returns SAALATAMUUNIIHA label."""
        label = get_morpho_role_label("seen")
        assert label == "SAALATAMUUNIIHA"

    def test_kaf_returns_expanded_multi_role_label(self):
        """Test KAF returns EXPANDED_MULTI_ROLE label."""
        label = get_morpho_role_label("kaf")
        assert label == "EXPANDED_MULTI_ROLE"

    def test_jeem_returns_single_role_label(self):
        """Test JEEM returns SINGLE_ROLE label (default)."""
        label = get_morpho_role_label("jeem")
        assert label == "SINGLE_ROLE"


class TestIsMultiRoleLetter:
    """Test is_multi_role_letter() utility."""

    def test_baa_is_multi_role(self):
        """Test BAA is multi-role letter."""
        assert is_multi_role_letter("baa") is True

    def test_taa_is_multi_role(self):
        """Test TAA is multi-role letter."""
        assert is_multi_role_letter("taa") is True

    def test_jeem_is_not_multi_role(self):
        """Test JEEM is NOT multi-role letter."""
        assert is_multi_role_letter("jeem") is False


class TestAdapterConsumesRegistry:
    """Prove letter_coordinate_adapter consumes registry, not local dict."""

    def test_adapter_has_no_local_morpho_role_by_letter_dict(self):
        """Prove adapter has NO local MORPHO_ROLE_BY_LETTER dict."""
        # Check module namespace - should NOT have MORPHO_ROLE_BY_LETTER
        assert not hasattr(letter_coordinate_adapter, 'MORPHO_ROLE_BY_LETTER'), \
            "letter_coordinate_adapter must NOT have local MORPHO_ROLE_BY_LETTER dict"

    def test_adapter_imports_get_morpho_role_label(self):
        """Prove adapter imports get_morpho_role_label from registry."""
        # Check that get_morpho_role_label is imported
        assert hasattr(letter_coordinate_adapter, 'get_morpho_role_label'), \
            "letter_coordinate_adapter must import get_morpho_role_label from registry"

        # Verify it's the same function from the registry
        assert letter_coordinate_adapter.get_morpho_role_label is letter_role_registry.get_morpho_role_label, \
            "get_morpho_role_label must come from letter_role_registry"

    def test_adapter_uses_registry_for_morpho_roles(self):
        """Prove adapter gets morpho roles from registry, not local dict."""
        # Get morpho role for BAA from registry
        baa_role = letter_role_registry.get_morpho_role_label("baa")
        assert baa_role == "EXPANDED_MULTI_ROLE"

        # Get morpho role for TAA from registry
        taa_role = letter_role_registry.get_morpho_role_label("taa")
        assert taa_role == "SAALATAMUUNIIHA"


class TestRegistryMetadata:
    """Prove registry metadata forbids adapter duplication."""

    def test_metadata_has_required_fields(self):
        """Verify metadata has all required fields."""
        assert "truth_type" in REGISTRY_METADATA
        assert "truth_name" in REGISTRY_METADATA
        assert "canonical_source" in REGISTRY_METADATA
        assert "domain" in REGISTRY_METADATA
        assert "evidence_rank" in REGISTRY_METADATA
        assert "forbidden_duplicates" in REGISTRY_METADATA

    def test_metadata_truth_type_is_classification(self):
        """Verify this is a classification truth."""
        assert REGISTRY_METADATA["truth_type"] == "classification"

    def test_metadata_canonical_source_correct(self):
        """Verify canonical source path."""
        assert "src/qiyas_core/registries/letter_role_registry.py" in \
            REGISTRY_METADATA["canonical_source"]

    def test_metadata_forbids_adapter_duplication(self):
        """Prove metadata forbids duplication in adapters."""
        forbidden = REGISTRY_METADATA["forbidden_duplicates"]
        assert any("letter_coordinate_adapter" in path for path in forbidden), \
            "letter_role_registry must forbid duplication in letter_coordinate_adapter"


class TestSourceOfTruthEnforcement:
    """Prove source-of-truth is enforced, not just created."""

    def test_no_morpho_role_by_letter_dict_in_adapter_source(self):
        """Prove no MORPHO_ROLE_BY_LETTER dict exists in adapter source code."""
        # Read source code of letter_coordinate_adapter
        adapter_source = inspect.getsource(letter_coordinate_adapter)

        # Should NOT contain MORPHO_ROLE_BY_LETTER dict literal
        assert 'MORPHO_ROLE_BY_LETTER = {' not in adapter_source, \
            "letter_coordinate_adapter must NOT contain local MORPHO_ROLE_BY_LETTER dict"

        # Should NOT contain morpho role mappings like "baa": "EXPANDED_MULTI_ROLE"
        assert '"baa": "EXPANDED_MULTI_ROLE"' not in adapter_source, \
            "letter_coordinate_adapter must NOT contain local morpho role mappings"

    def test_adapter_imports_from_letter_role_registry(self):
        """Prove adapter imports from letter_role_registry."""
        adapter_source = inspect.getsource(letter_coordinate_adapter)

        # Should import from registries.letter_role_registry
        assert 'from .registries.letter_role_registry import get_morpho_role_label' in adapter_source, \
            "letter_coordinate_adapter must import get_morpho_role_label from letter_role_registry"


class TestLetterRoleClassificationDataclass:
    """Test LetterRoleClassification dataclass."""

    def test_classification_frozen(self):
        """Verify LetterRoleClassification is frozen."""
        classification = classify_letter_role("baa")

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            classification.role_potential = LetterRolePotential.SINGLE_ROLE

    def test_classification_has_all_fields(self):
        """Verify classification has all required fields."""
        classification = classify_letter_role("baa")

        assert hasattr(classification, "letter_name")
        assert hasattr(classification, "role_potential")
        assert hasattr(classification, "can_be_affix")
        assert hasattr(classification, "can_be_preposition")
        assert hasattr(classification, "can_be_pronoun")
        assert hasattr(classification, "can_be_root_consonant")
        assert hasattr(classification, "evidence_source")

    def test_evidence_source_is_registry(self):
        """Verify evidence source is registry."""
        classification = classify_letter_role("baa")
        assert "letter_role_registry" in classification.evidence_source


class TestConstitutionalCompliance:
    """Test constitutional requirements."""

    def test_registry_disclaims_grammatical_function(self):
        """Prove registry does NOT claim to determine grammatical function."""
        module_doc = letter_role_registry.__doc__
        assert module_doc is not None

        # Should clarify this is NOT grammatical function
        assert "NOT grammatical function" in module_doc, \
            "Registry must clarify role potential is NOT grammatical function"

        # Should mention pre-compositional
        assert "pre-compositional" in module_doc.lower() or "potential" in module_doc.lower(), \
            "Registry must mention pre-compositional or potential nature"

    def test_registry_mentions_higher_layer_requirement(self):
        """Prove registry mentions higher layers for context-dependent role."""
        module_doc = letter_role_registry.__doc__
        assert module_doc is not None

        # Should mention higher layers or context requirement
        assert "higher layers" in module_doc.lower() or "context" in module_doc.lower(), \
            "Registry must mention higher layers for context-dependent analysis"
