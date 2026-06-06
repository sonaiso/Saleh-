"""
Letter Morphological Role Registry - Single Source of Truth

Constitutional Basis:
  - SOURCE_OF_TRUTH_REGISTRY.md § 5: Letter role potential registry
  - FULL_LAYER_2_PLAN.md § 4.3: Morphological role bits
  - CLAUDE.md § 2: No local duplicates in adapters

Purpose:
  Define which letters have multi-role potential for pre-compositional analysis.
  This is NOT grammatical function (that requires context).
  This is role POTENTIAL before composition.

Critical Distinction:
  - Pre-compositional role potential: What roles this letter CAN take
  - Grammatical function: Actual role in context (requires higher layers)

Truth Type: Classification Truth (Role Potential)
Domain: Controlled Vocalized Arabic
Evidence Rank: FORMAL_STRUCTURE

Forbidden:
  - DO NOT duplicate this registry in adapters
  - DO NOT confuse role potential with grammatical function
  - DO NOT claim this determines actual morphological role in context
"""

from dataclasses import dataclass
from enum import Enum


class LetterRolePotential(Enum):
    """
    Pre-compositional role potential classification.

    CRITICAL: This is NOT grammatical function.
    This is role POTENTIAL before composition into morphemes/words.
    """
    SAALATAMUUNIIHA = "saalatamuuniiha"
    # Letters in سألتمونيها set - multi-role verb/pronoun affixes
    # Examples: س ت ل م ن ي ه ا
    # Potential: subject/object pronoun, verb affix, nominal

    EXPANDED_MULTI_ROLE = "expanded_multi_role"
    # Letters with multi-role potential beyond سألتمونيها
    # Examples: ب (preposition, prefix, nominal), ك (preposition, suffix, nominal)
    # Potential: preposition, affix, nominal

    SINGLE_ROLE = "single_role"
    # Letters with primarily consonantal role
    # Most core Arabic letters
    # Potential: root consonant, nominal consonant

    WEAK_ROLE_CONTEXT_DEPENDENT = "weak_role_context_dependent"
    # Weak letters (و ي ا) with context-dependent role
    # Potential: carrier | madd | diphthong | orthographic
    # Requires RoleDisambiguationGate in higher layers


@dataclass(frozen=True)
class LetterRoleClassification:
    """
    Result of letter role potential classification.
    """
    letter_name: str
    role_potential: LetterRolePotential
    can_be_affix: bool
    can_be_preposition: bool
    can_be_pronoun: bool
    can_be_root_consonant: bool
    evidence_source: str = "letter_role_registry"


# سألتمونيها letters - core multi-role verb/pronoun affixes
SAALATAMUUNIIHA_LETTERS: frozenset[str] = frozenset({
    "seen",   # س
    "alif",   # ا (also weak letter)
    "lam",    # ل
    "taa",    # ت
    "meem",   # م
    "waw",    # و (also weak letter)
    "noon",   # ن
    "yaa",    # ي (also weak letter)
    "haa",    # ه
    "haa_final",  # ه (U+0647 glottal — same SAALATAMUUNIIHA classification as "haa")
})


# Expanded multi-role letters (preposition, affix, nominal potential)
EXPANDED_MULTI_ROLE_LETTERS: frozenset[str] = frozenset({
    "baa",    # ب - preposition, prefix, nominal
    "kaf",    # ك - preposition, suffix, nominal
    "faa",    # ف - conjunction, prefix, nominal
})


# Weak letters (context-dependent role)
WEAK_LETTERS_ROLE_CONTEXT: frozenset[str] = frozenset({
    "alif",   # ا - carrier | madd | orthographic
    "waw",    # و - carrier | madd | diphthong | consonant
    "yaa",    # ي - carrier | madd | diphthong | consonant
})


def classify_letter_role(letter_name: str) -> LetterRoleClassification:
    """
    Classify letter role potential BEFORE composition.

    This is NOT grammatical function.
    This is role POTENTIAL.

    Args:
        letter_name: Lowercase letter name (e.g., "baa", "taa", "seen")

    Returns:
        LetterRoleClassification with role potential and capability flags

    Example:
        >>> classification = classify_letter_role("baa")
        >>> classification.role_potential
        LetterRolePotential.EXPANDED_MULTI_ROLE
        >>> classification.can_be_preposition
        True

        >>> classification = classify_letter_role("taa")
        >>> classification.role_potential
        LetterRolePotential.SAALATAMUUNIIHA
        >>> classification.can_be_pronoun
        True
    """
    # Weak letters (context-dependent)
    if letter_name in WEAK_LETTERS_ROLE_CONTEXT:
        return LetterRoleClassification(
            letter_name=letter_name,
            role_potential=LetterRolePotential.WEAK_ROLE_CONTEXT_DEPENDENT,
            can_be_affix=True,
            can_be_preposition=False,
            can_be_pronoun=True,
            can_be_root_consonant=True,
        )

    # سألتمونيها letters
    if letter_name in SAALATAMUUNIIHA_LETTERS:
        return LetterRoleClassification(
            letter_name=letter_name,
            role_potential=LetterRolePotential.SAALATAMUUNIIHA,
            can_be_affix=True,
            can_be_preposition=False,
            can_be_pronoun=True,
            can_be_root_consonant=True,
        )

    # Expanded multi-role letters
    if letter_name in EXPANDED_MULTI_ROLE_LETTERS:
        return LetterRoleClassification(
            letter_name=letter_name,
            role_potential=LetterRolePotential.EXPANDED_MULTI_ROLE,
            can_be_affix=True,
            can_be_preposition=True,
            can_be_pronoun=False,
            can_be_root_consonant=True,
        )

    # Single-role letters (default for most core letters)
    return LetterRoleClassification(
        letter_name=letter_name,
        role_potential=LetterRolePotential.SINGLE_ROLE,
        can_be_affix=False,
        can_be_preposition=False,
        can_be_pronoun=False,
        can_be_root_consonant=True,
    )


def get_morpho_role_label(letter_name: str) -> str:
    """
    Get morphological role label for evidence generation.

    This is the legacy label used in letter_coordinate_adapter.
    Prefer using classify_letter_role() for full classification.

    Args:
        letter_name: Lowercase letter name

    Returns:
        Role label string (e.g., "SAALATAMUUNIIHA", "EXPANDED_MULTI_ROLE", "SINGLE_ROLE")
    """
    classification = classify_letter_role(letter_name)
    return classification.role_potential.value.upper()


def is_multi_role_letter(letter_name: str) -> bool:
    """
    Check if letter has multi-role potential.

    Args:
        letter_name: Lowercase letter name

    Returns:
        True if letter can take multiple roles, False otherwise
    """
    classification = classify_letter_role(letter_name)
    return classification.role_potential in {
        LetterRolePotential.SAALATAMUUNIIHA,
        LetterRolePotential.EXPANDED_MULTI_ROLE,
        LetterRolePotential.WEAK_ROLE_CONTEXT_DEPENDENT,
    }


# Registry metadata for source-of-truth compliance
REGISTRY_METADATA = {
    "truth_type": "classification",
    "truth_name": "letter_role_potential",
    "canonical_source": "src/qiyas_core/registries/letter_role_registry.py",
    "domain": "controlled_vocalized_arabic",
    "evidence_rank": "FORMAL_STRUCTURE",
    "forbidden_duplicates": [
        "src/qiyas_core/letter_identity_adapter.py",
        "src/qiyas_core/letter_coordinate_adapter.py",
    ],
    "notes": [
        "This is pre-compositional role POTENTIAL, not grammatical function.",
        "Actual morphological role requires context and higher-layer analysis.",
        "سألتمونيها classification is canonical for verb/pronoun affixes.",
    ],
}
