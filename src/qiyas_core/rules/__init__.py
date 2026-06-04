# qiyas_core canonical rules (PR #1)
# All pre-constitutional rules moved to experimental/ per Path A isolation
# TypedCodePoint rules: 5 canonical rules for type-specific classification (PR #24)
# Algebraic Foundation rules: letter identity, haraka function, position, slot (Gap #3-6)

from .typed_codepoint_rules import (
    LETTER_CODEPOINT_CLASSIFICATION,
    HARAKA_CODEPOINT_CLASSIFICATION,
    BOUNDARY_CODEPOINT_CLASSIFICATION,
    PUNCTUATION_CODEPOINT_CLASSIFICATION,
    RESIDUAL_CODEPOINT_CLASSIFICATION,
)
from .unicode_rules import UNICODE_ARABIC_MEMBERSHIP
from .letter_identity_rules import (
    LETTER_IDENTITY_RULES,
    BAA_IDENTITY_RULE,
    TAA_IDENTITY_RULE,
    SEEN_IDENTITY_RULE,
    SHEEN_IDENTITY_RULE,
    MEEM_IDENTITY_RULE,
    get_letter_identity_rule,
)
from .haraka_function_rules import (
    HARAKA_FUNCTION_RULES,
    FATHA_FUNCTION_RULE,
    DAMMA_FUNCTION_RULE,
    KASRA_FUNCTION_RULE,
    SUKUN_FUNCTION_RULE,
    SHADDA_FUNCTION_RULE,
    TANWIN_FATH_FUNCTION_RULE,
    TANWIN_DAMM_FUNCTION_RULE,
    TANWIN_KASR_FUNCTION_RULE,
    get_haraka_function_rule,
)
from .position_rules import (
    POSITION_RULES,
    INITIAL_POSITION_RULE,
    MEDIAL_POSITION_RULE,
    FINAL_POSITION_RULE,
    ISOLATED_POSITION_RULE,
    get_position_rule,
)
from .minimal_unit_readiness_rules import (
    MINIMAL_UNIT_READINESS_ADMIT_RULE,
    MINIMAL_UNIT_READINESS_RULES,
)
from .slot_geometry_rules import (
    SLOT_GEOMETRY_EXTEND_RULE,
    SLOT_GEOMETRY_RULES,
    SLOT_GEOMETRY_SEED_RULE,
    get_slot_geometry_rule_for_construction_mode,
)
from .slot_rules import SLOT_COMPOSITION_RULE

__all__ = [
    # TypedCodePoint
    "LETTER_CODEPOINT_CLASSIFICATION",
    "HARAKA_CODEPOINT_CLASSIFICATION",
    "BOUNDARY_CODEPOINT_CLASSIFICATION",
    "PUNCTUATION_CODEPOINT_CLASSIFICATION",
    "RESIDUAL_CODEPOINT_CLASSIFICATION",
    "UNICODE_ARABIC_MEMBERSHIP",
    # LetterIdentity
    "LETTER_IDENTITY_RULES",
    "BAA_IDENTITY_RULE",
    "TAA_IDENTITY_RULE",
    "SEEN_IDENTITY_RULE",
    "SHEEN_IDENTITY_RULE",
    "MEEM_IDENTITY_RULE",
    "get_letter_identity_rule",
    # HarakaFunction
    "HARAKA_FUNCTION_RULES",
    "FATHA_FUNCTION_RULE",
    "DAMMA_FUNCTION_RULE",
    "KASRA_FUNCTION_RULE",
    "SUKUN_FUNCTION_RULE",
    "SHADDA_FUNCTION_RULE",
    "TANWIN_FATH_FUNCTION_RULE",
    "TANWIN_DAMM_FUNCTION_RULE",
    "TANWIN_KASR_FUNCTION_RULE",
    "get_haraka_function_rule",
    # Position
    "POSITION_RULES",
    "INITIAL_POSITION_RULE",
    "MEDIAL_POSITION_RULE",
    "FINAL_POSITION_RULE",
    "ISOLATED_POSITION_RULE",
    "get_position_rule",
    # Slot
    "SLOT_COMPOSITION_RULE",
    # SlotGeometry (Phase-2 Batch 1)
    "SLOT_GEOMETRY_SEED_RULE",
    "SLOT_GEOMETRY_EXTEND_RULE",
    "SLOT_GEOMETRY_RULES",
    "get_slot_geometry_rule_for_construction_mode",
    # MinimalIndependentUnitReadiness (Phase-2 follow-up)
    "MINIMAL_UNIT_READINESS_ADMIT_RULE",
    "MINIMAL_UNIT_READINESS_RULES",
]
