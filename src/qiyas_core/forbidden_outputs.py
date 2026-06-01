"""
ForbiddenOutputRegistry — Centralized forbidden-output declarations.

Every layer in the algebraic foundation chain must forbid at least the
constitutional triple {HukmCandidate, RealityClaim, FinalMeaning}, plus
layer-specific higher-level types that must not be produced prematurely.

Gap #12 of ALGEBRAIC_FOUNDATION_CONTRACT.md.
"""

# ---------------------------------------------------------------------------
# Constitutional base (required by QiyasKernel._check_forbidden_outputs_declared)
# ---------------------------------------------------------------------------

CONSTITUTIONAL_BASE: tuple[str, ...] = (
    "HukmCandidate",
    "RealityClaim",
    "FinalMeaning",
)

# ---------------------------------------------------------------------------
# Layer-specific registries
# ---------------------------------------------------------------------------

# TypedCodePoint layer: already exists; kept here for reference/registry use.
FORBIDDEN_TYPED_CODEPOINT: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "AtomicUnitCandidate",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "FormCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "IfadahCandidate",
)

# LetterIdentityCarrier layer
FORBIDDEN_LETTER_IDENTITY: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "SyllableCandidate",
    "PronunciationCandidate",
    "FormCandidate",
)

# HarakaFunctionCarrier layer
FORBIDDEN_HARAKA_FUNCTION: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "CaseEffect",
    "Irab",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
)

# PositionCarrier layer
FORBIDDEN_POSITION: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "CaseEffect",
    "Irab",
)

# SlotCandidate layer
FORBIDDEN_SLOT: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "SyllableCandidate",   # slot ⊬ syllable (adjacency not yet established)
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "CaseEffect",
    "Irab",
)

# SyllableCandidate layer (future)
FORBIDDEN_SYLLABLE: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "CaseEffect",
    "Irab",
)


# ---------------------------------------------------------------------------
# Registry mapping layer name → forbidden tuple
# ---------------------------------------------------------------------------

LAYER_FORBIDDEN_OUTPUTS: dict[str, tuple[str, ...]] = {
    "TypedCodePointClassificationQiyas": FORBIDDEN_TYPED_CODEPOINT,
    "LetterIdentityQiyas": FORBIDDEN_LETTER_IDENTITY,
    "HarakaFunctionQiyas": FORBIDDEN_HARAKA_FUNCTION,
    "PositionQiyas": FORBIDDEN_POSITION,
    "SlotQiyas": FORBIDDEN_SLOT,
    "SyllableQiyas": FORBIDDEN_SYLLABLE,
}


def get_forbidden_outputs(layer: str) -> tuple[str, ...]:
    """Return the forbidden-outputs tuple for the given layer name."""
    return LAYER_FORBIDDEN_OUTPUTS.get(layer, CONSTITUTIONAL_BASE)
