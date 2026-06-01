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

# TypedCodePoint layer — PR #29 source-of-truth fix: typed_codepoint_rules.py
# now imports this tuple directly instead of maintaining its own local copy.
FORBIDDEN_TYPED_CODEPOINT: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # PR #29 — global recursion closure: a pre-slot tagging layer cannot
    # jump to the composition layer or to its hypothetical successor.
    "SlotCandidate",
    "SlotGeometry",
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
    # PR #29 — global recursion closure: atomic identity proof cannot
    # produce the composition output or its successor.
    "SlotCandidate",
    "SlotGeometry",
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
    # PR #29 — global recursion closure: atomic function proof cannot
    # produce the composition output or its successor.
    "SlotCandidate",
    "SlotGeometry",
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
    # PR #29 — global recursion closure: atomic position proof cannot
    # produce the composition output or its successor.
    "SlotCandidate",
    "SlotGeometry",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "CaseEffect",
    "Irab",
)

# SlotCandidate layer
# PR #28 — SlotGeometry is now explicitly forbidden by the slot rule itself,
# not merely by the structural constraint that output_candidate_type =
# "SlotCandidate". This closes the constitutional jump
# SlotCandidate* → SlotGeometry at the forbidden-outputs level.
FORBIDDEN_SLOT: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "SlotGeometry",        # slot ⊬ slot_geometry (multi-slot architecture deferred)
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

# ConditionedTypedSequence layer (PR #25 — pre-slot alignment proof)
# Per CLAUDE.md §7: ConditionedTypedSequence MUST NOT produce
# LetterIdentityCarrier, HarakaFunctionCarrier, SlotCandidate, or
# SlotGeometry. Per CLAUDE.md §14, these are the explicit non-goals
# for the CTS PR.
FORBIDDEN_CONDITIONED_TYPED_SEQUENCE: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "LetterIdentityCarrier",
    "HarakaFunctionCarrier",
    # PR #29 — defensive lateral closure: CTS produces PositionEvidence,
    # NEVER PositionCarrier (which is the output of PositionQiyas).
    # Listing this here prevents a hand-rolled CTS rule from accidentally
    # impersonating PositionQiyas's output.
    "PositionCarrier",
    "SlotCandidate",
    "SlotGeometry",
    "SyllableCandidate",
    "PronunciationCandidate",
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "CaseEffect",
    "Irab",
    "FinalCaseJudgment",
)


# ---------------------------------------------------------------------------
# Registry mapping layer name → forbidden tuple
# ---------------------------------------------------------------------------

LAYER_FORBIDDEN_OUTPUTS: dict[str, tuple[str, ...]] = {
    "TypedCodePointClassificationQiyas": FORBIDDEN_TYPED_CODEPOINT,
    "LetterIdentityQiyas": FORBIDDEN_LETTER_IDENTITY,
    "HarakaFunctionQiyas": FORBIDDEN_HARAKA_FUNCTION,
    "PositionQiyas": FORBIDDEN_POSITION,
    "ConditionedTypedSequenceQiyas": FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    "SlotQiyas": FORBIDDEN_SLOT,
    "SyllableQiyas": FORBIDDEN_SYLLABLE,
}


def get_forbidden_outputs(layer: str) -> tuple[str, ...]:
    """Return the forbidden-outputs tuple for the given layer name."""
    return LAYER_FORBIDDEN_OUTPUTS.get(layer, CONSTITUTIONAL_BASE)
