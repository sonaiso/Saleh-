"""
RecursiveProofContract — Gap #11 of ALGEBRAIC_FOUNDATION_CONTRACT.md.

A unified dataclass template that every layer in the algebraic foundation
chain must instantiate, proving that all layers share the same proof
structure.

Layers:
  TypedCodePoint, LetterIdentityCarrier, HarakaFunctionCarrier,
  PositionCarrier, SlotCandidate (and future layers)

Each layer is an instance of RecursiveProofContract with its own:
  inputs, effective_wasf, jami_illah, invalidating_fariq, evidence,
  identity_preservation, economy, minimal_sufficiency, forbidden_outputs,
  trace, output.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RecursiveProofContract:
    """
    Universal proof-contract template for every algebraic layer.

    This dataclass is instantiated once per layer to document and enforce
    that every layer satisfies the same algebraic invariants.
    """

    # Layer identification
    layer_name: str
    rule_id: str

    # Inputs: tuple of input candidate types consumed by this layer
    inputs: tuple[str, ...]

    # Effective wasf: tuple of effective-attribute strings proven
    effective_wasf: tuple[str, ...]

    # Jami' illah: tuple of shared-cause strings verified
    jami_illah: tuple[str, ...]

    # Invalidating differences: tuple of difference labels that block
    invalidating_fariq: tuple[str, ...]

    # Evidence: human-readable summary of what is proven
    evidence: tuple[str, ...]

    # Identity preservation: tuple of identity_ids that must be in output
    identity_preservation: tuple[str, ...]

    # Economy: bool — does this layer satisfy Economy(x, P)?
    economy: bool

    # Minimal sufficiency: bool — does this layer satisfy MSL(x, P)?
    minimal_sufficiency: bool

    # Forbidden outputs: tuple of output types explicitly prohibited
    forbidden_outputs: tuple[str, ...]

    # Trace: tuple of trace_id prefixes expected in output
    trace: tuple[str, ...]

    # Output: the output_candidate_type produced
    output: str

    def validate(self) -> list[str]:
        """
        Validate constitutional invariants.

        Returns:
            List of violation messages (empty if all invariants pass).
        """
        violations: list[str] = []

        required_forbidden = {"HukmCandidate", "RealityClaim", "FinalMeaning"}
        if not required_forbidden.issubset(set(self.forbidden_outputs)):
            missing = required_forbidden - set(self.forbidden_outputs)
            violations.append(
                f"[{self.layer_name}] Missing constitutional forbidden outputs: {missing}"
            )

        if not self.effective_wasf:
            violations.append(f"[{self.layer_name}] effective_wasf must not be empty")

        if not self.jami_illah:
            violations.append(f"[{self.layer_name}] jami_illah must not be empty")

        if not self.inputs:
            violations.append(f"[{self.layer_name}] inputs must not be empty")

        if not self.output:
            violations.append(f"[{self.layer_name}] output must not be empty")

        if not self.identity_preservation:
            violations.append(f"[{self.layer_name}] identity_preservation must not be empty")

        return violations

    def is_valid(self) -> bool:
        """Return True iff validate() returns no violations."""
        return len(self.validate()) == 0


# ---------------------------------------------------------------------------
# Canonical contract instances for the Phase-1 layers
# ---------------------------------------------------------------------------

TYPED_CODEPOINT_CONTRACT = RecursiveProofContract(
    layer_name="TypedCodePointClassificationQiyas",
    rule_id="typed_codepoint.*_classification",
    inputs=("UnicodeCandidate",),
    effective_wasf=("is_classifiable_codepoint", "is_arabic_letter"),
    jami_illah=("belongs_to_typed_domain", "belongs_to_letter_class"),
    invalidating_fariq=("multiple_classes_claimed", "ambiguous_classification"),
    evidence=("unicode codepoint proven in arabic letter range",),
    identity_preservation=("identity:codepoint:{hex}",),
    economy=True,
    minimal_sufficiency=True,
    forbidden_outputs=(
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "AtomicUnitCandidate", "SyllableCandidate", "MeaningCandidate",
    ),
    trace=("typed:{hex}:ev",),
    output="LetterCodePoint",
)

LETTER_IDENTITY_CONTRACT = RecursiveProofContract(
    layer_name="LetterIdentityQiyas",
    rule_id="letter_identity.{arabic_name}",
    inputs=("LetterCodePoint",),
    effective_wasf=(
        "has_letter_codepoint",
        "has_unicode_identity:{hex}",
        "has_script_identity:{name}",
        "has_sound_identity:{sound}",
        "has_makhraj:{place}",
    ),
    jami_illah=(
        "belongs_to_letter_identity_domain",
        "letter_identity_is:{name}",
    ),
    invalidating_fariq=(
        "{name}_vs_{other_letter}",
    ),
    evidence=("phonetic profile proven: makhraj + sifat + sound identity",),
    identity_preservation=(
        "identity:codepoint:{hex}",
        "identity:letter_identity_domain",
    ),
    economy=True,
    minimal_sufficiency=True,
    forbidden_outputs=(
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "RootCandidate", "WeightCandidate", "MeaningCandidate",
    ),
    trace=("letter_identity:{hex}:ev",),
    output="LetterIdentityCarrier",
)

HARAKA_FUNCTION_CONTRACT = RecursiveProofContract(
    layer_name="HarakaFunctionQiyas",
    rule_id="haraka_function.{arabic_name}",
    inputs=("HarakaCodePoint",),
    effective_wasf=(
        "has_haraka_codepoint",
        "has_unicode_identity:{hex}",
        "has_vocalic_function:{function}",
    ),
    jami_illah=(
        "belongs_to_haraka_function_domain",
        "haraka_function_is:{name}",
    ),
    invalidating_fariq=(
        "{name}_vs_{other_haraka}",
    ),
    evidence=("vocalic energy profile proven: duration + aperture + tongue position",),
    identity_preservation=(
        "identity:codepoint:{hex}",
        "identity:haraka_function_domain",
    ),
    economy=True,
    minimal_sufficiency=True,
    forbidden_outputs=(
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "CaseEffect", "Irab", "SyllableCandidate", "MeaningCandidate",
    ),
    trace=("haraka_function:{hex}:ev",),
    output="HarakaFunctionCarrier",
)

POSITION_CONTRACT = RecursiveProofContract(
    layer_name="PositionQiyas",
    rule_id="position.{position_type}",
    inputs=("LetterCodePoint",),
    effective_wasf=(
        "has_position_index",
        "has_position_type:{type}",
        "within_word_determined",
    ),
    jami_illah=(
        "belongs_to_position_domain",
        "position_type_is:{type}",
    ),
    invalidating_fariq=(
        "position_type_ambiguous",
        "index_out_of_bounds",
    ),
    evidence=("position proven: index + type + within_word",),
    identity_preservation=(
        "identity:codepoint:{hex}",
        "identity:position_domain",
    ),
    economy=True,
    minimal_sufficiency=True,
    forbidden_outputs=(
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "SyllableCandidate", "MeaningCandidate", "CaseEffect",
    ),
    trace=("position:{hex}:{index}:ev",),
    output="PositionCarrier",
)

SLOT_CONTRACT = RecursiveProofContract(
    layer_name="SlotQiyas",
    rule_id="slot.composition",
    inputs=("LetterIdentityCarrier", "HarakaFunctionCarrier", "PositionCarrier"),
    effective_wasf=(
        "has_letter_identity_carrier",
        "has_haraka_function_carrier",
        "has_position_carrier",
        "compatible_letter_haraka",
        "compatible_letter_position",
        "identity_preserved",
    ),
    jami_illah=(
        "belongs_to_slot_composition_domain",
        "slot_composition_licensed",
    ),
    invalidating_fariq=(
        "haraka_carrier_mismatch",
        "position_identity_conflict",
        "slot_composition_blocked",
    ),
    evidence=("slot composition proven: compatible + identity preserved",),
    identity_preservation=(
        "identity:slot_composition_domain",
    ),
    economy=True,
    minimal_sufficiency=True,
    forbidden_outputs=(
        "HukmCandidate", "RealityClaim", "FinalMeaning",
        "SyllableCandidate", "MeaningCandidate", "CaseEffect",
    ),
    trace=("slot:{letter}:{haraka}:ev",),
    output="SlotCandidate",
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

PHASE1_CONTRACTS: tuple[RecursiveProofContract, ...] = (
    TYPED_CODEPOINT_CONTRACT,
    LETTER_IDENTITY_CONTRACT,
    HARAKA_FUNCTION_CONTRACT,
    POSITION_CONTRACT,
    SLOT_CONTRACT,
)
