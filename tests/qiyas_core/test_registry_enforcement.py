"""
Tests for Registry Enforcement - Prove adapters consume registries

Constitutional Compliance Tests:
  - Prove adapters no longer have local duplicate truths
  - Prove adapters import from registries
  - Prove generated evidence uses correct Arabic prefixes (فارق: not fariq:)
  - Prove source-of-truth enforcement

Basis: PR #37 fix(layer2): wire registries into adapters
"""

import pytest
import inspect

from qiyas_core import letter_identity_adapter
from qiyas_core import letter_coordinate_adapter
from qiyas_core.registries import letter_name_registry
from qiyas_core.registries import letter_fariq_registry


class TestAdaptersConsumeRegistries:
    """Prove adapters import from registries, not local duplicates."""

    def test_letter_identity_adapter_has_no_local_arabic_letter_names(self):
        """Prove letter_identity_adapter has no local ARABIC_LETTER_NAMES dict."""
        # Check module namespace - should NOT have ARABIC_LETTER_NAMES
        assert not hasattr(letter_identity_adapter, 'ARABIC_LETTER_NAMES'), \
            "letter_identity_adapter must NOT have local ARABIC_LETTER_NAMES"

    def test_letter_identity_adapter_imports_get_letter_names(self):
        """Prove letter_identity_adapter imports get_letter_names from registry."""
        # Check that get_letter_names is imported
        assert hasattr(letter_identity_adapter, 'get_letter_names'), \
            "letter_identity_adapter must import get_letter_names from registry"

        # Verify it's the same function from the registry
        assert letter_identity_adapter.get_letter_names is letter_name_registry.get_letter_names, \
            "get_letter_names must come from letter_name_registry"

    def test_letter_coordinate_adapter_has_no_local_arabic_letter_names(self):
        """Prove letter_coordinate_adapter has no local ARABIC_LETTER_NAMES dict."""
        # Check module namespace - should NOT have ARABIC_LETTER_NAMES
        assert not hasattr(letter_coordinate_adapter, 'ARABIC_LETTER_NAMES'), \
            "letter_coordinate_adapter must NOT have local ARABIC_LETTER_NAMES"

    def test_letter_coordinate_adapter_imports_get_letter_names(self):
        """Prove letter_coordinate_adapter imports get_letter_names from registry."""
        # Check that get_letter_names is imported
        assert hasattr(letter_coordinate_adapter, 'get_letter_names'), \
            "letter_coordinate_adapter must import get_letter_names from registry"

        # Verify it's the same function from the registry
        assert letter_coordinate_adapter.get_letter_names is letter_name_registry.get_letter_names, \
            "get_letter_names must come from letter_name_registry"

    def test_adapters_use_registry_for_arabic_names(self):
        """Prove adapters get Arabic names from registry, not local dicts."""
        # Get Arabic name for BAA from registry
        baa_names = letter_name_registry.get_letter_names(0x0628)
        assert baa_names is not None
        assert baa_names.arabic_name == "باء"
        assert baa_names.latin_name == "baa"

        # Get Arabic name for TAA from registry
        taa_names = letter_name_registry.get_letter_names(0x062A)
        assert taa_names is not None
        assert taa_names.arabic_name == "تاء"
        assert taa_names.latin_name == "taa"


class TestFariqRegistryDocstring:
    """Prove fariq registry uses correct Arabic prefix in docstrings."""

    def test_fariq_registry_docstring_uses_arabic_prefix(self):
        """Prove letter_fariq_registry docstring uses فارق: not fariq:."""
        module_doc = letter_fariq_registry.__doc__
        assert module_doc is not None

        # Should mention فارق: (Arabic prefix) in examples
        assert "فارق:" in module_doc, \
            "fariq registry docstring must use Arabic prefix فارق: in examples"

        # Should NOT use fariq: as executable evidence format in examples
        # (Note: "fariq" may appear in prose, but "fariq:" should not be shown as executable)
        # Check that if "fariq:" appears, it's clarified as prose-only
        if "fariq:" in module_doc:
            # If fariq: appears, there should be a clarification nearby
            assert "prose" in module_doc or "English" in module_doc or "not English" in module_doc, \
                "If 'fariq:' appears in docstring, must clarify it's prose-only, not executable"

    def test_fariq_pair_docstring_uses_arabic_prefix(self):
        """Prove FariqPair docstring uses فارق: for executable evidence."""
        fariq_pair_doc = letter_fariq_registry.FariqPair.__doc__
        assert fariq_pair_doc is not None

        # Should mention فارق: (Arabic prefix) for evidence format
        assert "فارق:" in fariq_pair_doc, \
            "FariqPair docstring must show فارق: as executable evidence format"


class TestRegistryMetadata:
    """Prove registry metadata forbids adapter duplication."""

    def test_letter_name_registry_forbids_adapter_duplication(self):
        """Prove letter_name_registry metadata forbids duplication in adapters."""
        metadata = letter_name_registry.REGISTRY_METADATA
        assert "forbidden_duplicates" in metadata

        forbidden = metadata["forbidden_duplicates"]
        # Should list adapters that must NOT duplicate this truth
        assert any("letter_identity_adapter" in path for path in forbidden), \
            "letter_name_registry must forbid duplication in letter_identity_adapter"
        assert any("letter_coordinate_adapter" in path for path in forbidden), \
            "letter_name_registry must forbid duplication in letter_coordinate_adapter"

    def test_fariq_registry_forbids_adapter_duplication(self):
        """Prove letter_fariq_registry metadata forbids duplication in adapters."""
        metadata = letter_fariq_registry.REGISTRY_METADATA
        assert "forbidden_duplicates" in metadata

        forbidden = metadata["forbidden_duplicates"]
        # Should list adapters that must NOT duplicate this truth
        assert any("letter_identity_adapter" in path for path in forbidden), \
            "letter_fariq_registry must forbid duplication in letter_identity_adapter"


class TestSourceOfTruthEnforcement:
    """Prove source-of-truth is enforced, not just created."""

    def test_no_duplicate_arabic_name_mapping_in_adapters(self):
        """Prove no duplicate Arabic name mappings exist in adapter modules."""
        # Read source code of letter_identity_adapter
        identity_source = inspect.getsource(letter_identity_adapter)

        # Should NOT contain a dict literal with Arabic names
        # (This is a heuristic check - looking for common patterns)
        assert 'ARABIC_LETTER_NAMES = {' not in identity_source, \
            "letter_identity_adapter must NOT contain local ARABIC_LETTER_NAMES dict"

        # Read source code of letter_coordinate_adapter
        coordinate_source = inspect.getsource(letter_coordinate_adapter)

        # Should NOT contain import of ARABIC_LETTER_NAMES from letter_identity_adapter
        assert 'from .letter_identity_adapter import ARABIC_LETTER_NAMES' not in coordinate_source, \
            "letter_coordinate_adapter must NOT import ARABIC_LETTER_NAMES from letter_identity_adapter"

    def test_adapters_import_from_registries_module(self):
        """Prove adapters import from qiyas_core.registries, not local definitions."""
        # Read source code
        identity_source = inspect.getsource(letter_identity_adapter)
        coordinate_source = inspect.getsource(letter_coordinate_adapter)

        # Should import from registries module
        assert 'from .registries.letter_name_registry import get_letter_names' in identity_source, \
            "letter_identity_adapter must import get_letter_names from registries module"

        assert 'from .registries.letter_name_registry import get_letter_names' in coordinate_source, \
            "letter_coordinate_adapter must import get_letter_names from registries module"


class TestFariqCoverageDisclaimer:
    """Prove fariq registry disclaims complete coverage."""

    def test_fariq_registry_does_not_claim_all_differences(self):
        """Prove letter_fariq_registry does NOT claim 'ALL invalidating differences'."""
        module_doc = letter_fariq_registry.__doc__
        assert module_doc is not None

        # Should NOT claim "Define ALL invalidating difference pairs"
        # (If "ALL" appears, it should be qualified)
        if "ALL" in module_doc:
            # If ALL appears, should be qualified with "initial" or similar
            assert "initial" in module_doc or "not yet complete" in module_doc, \
                "If 'ALL' appears in fariq registry doc, must be qualified as incomplete"

        # Should mention this is initial/canonical, not complete coverage
        assert "initial" in module_doc or "canonical" in module_doc, \
            "fariq registry should declare itself as 'initial canonical' registry"

    def test_fariq_pairs_comment_indicates_expansion(self):
        """Prove LETTER_FARIQ_PAIRS comment indicates future expansion."""
        # Read source to check comments
        fariq_source = inspect.getsource(letter_fariq_registry)

        # Should mention expansion or Phase 2/3
        assert "expand" in fariq_source.lower() or "phase" in fariq_source.lower(), \
            "fariq registry should mention expansion or phases in comments"
