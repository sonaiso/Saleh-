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

# SlotGeometry layer (PR #64 → PR #65 centralization)
# Per SLOT_GEOMETRY_ALIGNMENT_TRACE_CONTRACT.md §9 and §11:
# SlotGeometryQiyas produces only SlotGeometryCandidate (§9).
# Seed and extension are construction modes, not separate candidate types.
# MinimalCompletionReadinessCandidate is future-reserved, NOT admissible yet.
FORBIDDEN_SLOT_GEOMETRY: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    "FinalCaseJudgment",
    "DalalahCandidate",
    "WordCandidate",
    "LafzCandidate",
    "SentenceCandidate",
    "ParagraphCandidate",
    "DiscourseGeometryCandidate",
    "TextGeometryCandidate",
    "MinimalCompletionReadinessCandidate",
)

# HarakaRoleSpectrum layer (Layer Γ — Gamma-haraka)
# Per HARAKA_ROLE_SPECTRUM_CONTRACT.md § 8:
# Γ_haraka (spectrum opener) produces POTENTIAL roles only.
# Λ (lambda selectors, FUTURE) will consume the spectrum and select roles.
# Γ ≠ Λ — Gamma opens, Lambda selects.
FORBIDDEN_HARAKA_ROLE_SPECTRUM: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # Weight/Pattern layer (Wazn)
    "WeightCandidate",
    "RootCandidate",
    "PatternCandidate",
    "MorphemeCandidate",
    # Case/Composition layer (I'rab)
    "CaseEffect",
    "Irab",
    "CaseJudgment",
    "CompositionCandidate",
    # Prosody layer ('Arud)
    "ArudCandidate",
    "MeterJudgment",
    # Selection outputs (Lambda outputs, not Gamma)
    "SelectedRole",
    "FinalFunction",
    "DeterminedRole",
    # Syllable layer (Λ_syllable output, not Γ output)
    "SyllableCandidate",
    "SyllableConstituent",
    # Higher layers
    "WordCandidate",
    "MeaningCandidate",
    "IfadahCandidate",
)


# ---------------------------------------------------------------------------
# Registry mapping layer name → forbidden tuple
# ---------------------------------------------------------------------------

# RegistryProjection layer (SCG-P2) — projects slot geometry onto registry
# membership classes only. Forbids every downstream canonical type (no-jump) and
# every morphological / lexical / semantic output (no early الأصل-الثالث leak).
FORBIDDEN_REGISTRY_PROJECTION: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # Exact downstream canonical output types (SCG-P3..P12) — no-jump.
    "RootStemCandidate",            # SCG-P3
    "JamidMushtaqCandidate",        # SCG-P4
    "MufradWordCandidate",          # SCG-P5
    "VerbalSignifiedCandidate",     # SCG-P6
    "CompositionReadinessCandidate",  # SCG-P7
    "AmilMamulCandidate",           # SCG-P8
    "SentenceGeometryCandidate",    # SCG-P9
    "RelationGeometryCandidate",    # SCG-P10
    "IrabGeometryCandidate",        # SCG-P11
    "IfadahCandidate",              # SCG-P12
    # Morphological / lexical / grammatical / semantic outputs (never produced).
    "SlotGeometry",
    "RootCandidate",
    "WeightCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "CaseEffect",
    "Irab",
)

# RootStem layer (SCG-P3) — closes a structural root/stem POSSIBILITY only.
# Forbids every downstream canonical type (no-jump) AND every final-root / wazn /
# morphology / word / meaning output (RootStemCandidate is a structural candidate,
# NOT a final root: RootCandidate/WeightCandidate are therefore forbidden).
FORBIDDEN_ROOT_STEM: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # Exact downstream canonical output types (SCG-P4..P12) — no-jump.
    "JamidMushtaqCandidate",        # SCG-P4
    "MufradWordCandidate",          # SCG-P5
    "VerbalSignifiedCandidate",     # SCG-P6
    "CompositionReadinessCandidate",  # SCG-P7
    "AmilMamulCandidate",           # SCG-P8
    "SentenceGeometryCandidate",    # SCG-P9
    "RelationGeometryCandidate",    # SCG-P10
    "IrabGeometryCandidate",        # SCG-P11
    "IfadahCandidate",              # SCG-P12
    # Final-root / wazn / morphology / word / meaning (never produced).
    "RootCandidate",                # final root judgment (≠ structural RootStemCandidate)
    "WeightCandidate",              # wazn
    "FormCandidate",
    "WordCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "CaseEffect",
    "Irab",
    "SlotGeometry",
)

# JamidMushtaq layer (SCG-P4) — opens a structural derivation-class POSSIBILITY
# only. It is NOT the final judgment that the word IS jamid or mushtaq
# (WordTypeJudgment forbidden), NOT wazn, NOT morphology, NOT meaning.
FORBIDDEN_JAMID_MUSHTAQ: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # Exact downstream canonical output types (SCG-P5..P12) — no-jump.
    "MufradWordCandidate",          # SCG-P5
    "VerbalSignifiedCandidate",     # SCG-P6
    "CompositionReadinessCandidate",  # SCG-P7
    "AmilMamulCandidate",           # SCG-P8
    "SentenceGeometryCandidate",    # SCG-P9
    "RelationGeometryCandidate",    # SCG-P10
    "IrabGeometryCandidate",        # SCG-P11
    "IfadahCandidate",              # SCG-P12
    # Final جامد/مشتق judgment + morphology + wazn + word + meaning (never produced).
    "WordTypeJudgment",             # final jamid/mushtaq judgment
    "RootCandidate",
    "WeightCandidate",              # wazn
    "FormCandidate",
    "WordCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "IrabCandidate",
    "CaseEffect",
    "Irab",
    "SlotGeometry",
)

# MufradWord layer (SCG-P5) — a candidate-only WORDHOOD layer. Answers only
# "could this structure form a potential single-word unit?" — NOT a final lexical
# word (WordCandidate forbidden), NOT a dictionary entry, NOT morphology, NOT
# grammar/meaning/i'rab/hukm.
FORBIDDEN_MUFRAD_WORD: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # Exact downstream canonical output types (SCG-P6..P12) — no-jump.
    "VerbalSignifiedCandidate",     # SCG-P6
    "CompositionReadinessCandidate",  # SCG-P7
    "AmilMamulCandidate",           # SCG-P8
    "SentenceGeometryCandidate",    # SCG-P9
    "RelationGeometryCandidate",    # SCG-P10
    "IrabGeometryCandidate",        # SCG-P11
    "IfadahCandidate",              # SCG-P12
    # Final lexical word / morphology / wazn / meaning / grammar (never produced).
    "WordCandidate",                # final lexical word (≠ candidate MufradWordCandidate)
    "WordTypeJudgment",
    "LexicalEntryCandidate",
    "RootCandidate",
    "WeightCandidate",              # wazn
    "FormCandidate",
    "MeaningCandidate",
    "DalalahCandidate",
    "IrabCandidate",
    "CaseEffect",
    "Irab",
    "SlotGeometry",
)

# VerbalSignified layer (SCG-P6) — opens verbal-signified semantic POSSIBILITIES
# (meaning/dalalah PRIORS) only. It NEVER produces actual meaning, dalalah,
# tafsir, hukm, or reality — those would cross into الأصل-الثالث / final judgment.
FORBIDDEN_VERBAL_SIGNIFIED: tuple[str, ...] = (
    *CONSTITUTIONAL_BASE,
    # Exact downstream canonical output types (SCG-P7..P12) — no-jump.
    "CompositionReadinessCandidate",  # SCG-P7
    "AmilMamulCandidate",           # SCG-P8
    "SentenceGeometryCandidate",    # SCG-P9
    "RelationGeometryCandidate",    # SCG-P10
    "IrabGeometryCandidate",        # SCG-P11
    "IfadahCandidate",              # SCG-P12
    # Meaning / dalalah / tafsir — never produced (only PRIORS are opened).
    "MeaningCandidate",
    "MeaningJudgment",
    "DalalahCandidate",
    "DalalahJudgment",
    "TafsirCandidate",
    # Word / morphology / grammar.
    "WordCandidate",
    "WordTypeJudgment",
    "RootCandidate",
    "WeightCandidate",
    "IrabCandidate",
    "CaseEffect",
    "Irab",
    "SlotGeometry",
)

LAYER_FORBIDDEN_OUTPUTS: dict[str, tuple[str, ...]] = {
    "TypedCodePointClassificationQiyas": FORBIDDEN_TYPED_CODEPOINT,
    "LetterIdentityQiyas": FORBIDDEN_LETTER_IDENTITY,
    "HarakaFunctionQiyas": FORBIDDEN_HARAKA_FUNCTION,
    "PositionQiyas": FORBIDDEN_POSITION,
    "ConditionedTypedSequenceQiyas": FORBIDDEN_CONDITIONED_TYPED_SEQUENCE,
    "SlotQiyas": FORBIDDEN_SLOT,
    "RegistryProjectionQiyas": FORBIDDEN_REGISTRY_PROJECTION,
    "RootStemQiyas": FORBIDDEN_ROOT_STEM,
    "JamidMushtaqQiyas": FORBIDDEN_JAMID_MUSHTAQ,
    "MufradWordQiyas": FORBIDDEN_MUFRAD_WORD,
    "VerbalSignifiedQiyas": FORBIDDEN_VERBAL_SIGNIFIED,
    "SlotGeometryQiyas": FORBIDDEN_SLOT_GEOMETRY,
    "HarakaRoleSpectrumQiyas": FORBIDDEN_HARAKA_ROLE_SPECTRUM,
    "SyllableQiyas": FORBIDDEN_SYLLABLE,
}


def get_forbidden_outputs(layer: str) -> tuple[str, ...]:
    """Return the forbidden-outputs tuple for the given layer name."""
    return LAYER_FORBIDDEN_OUTPUTS.get(layer, CONSTITUTIONAL_BASE)
